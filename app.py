import datetime
import json

from flask import Flask, request
from db import Puzzle, User, db
import users_dao
import os

app = Flask(__name__)
db_filename = "cordle.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    """
    Generalized success response function
    """
    return json.dumps(data), code

def failure_response(message, code=404):
    """
    Generalized failure response function
    """
    return json.dumps({"error" : message}), code

#-------PUZZLES-----------------------------------------------------------------
@app.route("/")
@app.route("/api/puzzles/")
def get_puzzles():
    """
    Endpoint for getting all puzzles  
    """
    #returns all the puzzles that exist with all the initialized fields
    puzzles = [e.serialize() for e in Puzzle.query.all()]
    return success_response({"puzzles": puzzles}, 200)


@app.route("/api/puzzles/", methods = ["POST"])
def create_puzzles():
    """
    Endpoint for creating a new puzzle  
    """
    #creates the new puzzle with the appropriate fields
    body = json.loads(request.data)
    word = body.get("word")
    hint = body.get("hint")
    if word is None or word == "" or hint is None or hint is "":
        return failure_response("Invalid word or hint", 400)
    new_puzzle = Puzzle(
        word = word,
        hint = hint,
    )
    #add new puzzle to the session and return it if successful
    db.session.add(new_puzzle)
    db.session.commit()
    return success_response(new_puzzle.serialize(), 201)


@app.route("/api/puzzles/<int:puzzle_id>/")
def get_specific_puzzle(puzzle_id):
    """
    Endpoint for getting a puzzle by id
    """
    #query for a specific puzzle and then if found, return that 
    #puzzle element.
    puzzle = Puzzle.query.filter_by(id=puzzle_id).first()
    if puzzle is None:
        return failure_response("Puzzle not found!", 404)
    return success_response(puzzle.serialize(), 201)



@app.route("/api/puzzles/<int:puzzle_id>/", methods=["DELETE"])
def delete_puzzle(puzzle_id):
    """
    Endpoint for deleting a puzzle by id
    """
    #deleting a puzzle by deleting it from the session after
    #first querying that it is present in the list.
    puzzle = Puzzle.query.filter_by(id=puzzle_id).first()
    if puzzle is None:
        return failure_response("Puzzle not found!")
    db.session.delete(puzzle)
    db.session.commit()
    return success_response(puzzle.serialize(), 200)

@app.route("/api/puzzles/number/")
def get_number_of_puzzles():
    """
    Endpoint for getting the number of puzzles in the database
    """
    query_set = Puzzle.query.all()
    number = 0
    for a in query_set:
        number+=1
    
    return success_response({"number of puzzles in database" : number}, 200)

#-----USERS--------------------------------------------------------------------
@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/add/", methods=["POST"])
def add_user(user_id):
    """
    Endpoint for adding a completed puzzle to a user
    """
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response("User not found!")
    body = json.loads(request.data)
    puzzle_id = body.get("puzzle_id")
    if not user_id:
        return failure_response("required fields not supplied", 400)
    puzzle = Puzzle.query.filter_by(id = puzzle_id).first()
    if not puzzle:
        return failure_response("Invalid puzzle id", 400)
    
    user.puzzles.append(puzzle)
    
    db.session.commit()
    
    return success_response(user.serialize())

#-----AUTHENTICATION-----------------------------------------------------------
def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")
    
    if auth_header is None:
        return False, json.dumps({"error":"Missing auth header"})

    bearer_token = auth_header.replace("Bearer", "").strip()
    if not bearer_token:
        return False, json.dumps({"error":"Invalid auth header"})
    
    return True, bearer_token

@app.route("/register/", methods=["POST"])
def register_account():
    """
    Endpoint for registering a new user
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if email is None or password is None:
        return failure_response("Invalid email or password", 400)
    
    created, user = users_dao.create_user(email, password)

    if not created:
        return failure_response("User already exists.", 400)
    
    return success_response(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token,
        }
    )

    
@app.route("/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in a user
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if email is None or password is None:
        return failure_response("Invalid email or password", 400)
    
    success, user = users_dao.verify_credentials(email, password)

    if not success:
        return failure_response("Incorrect email or password.")
    
    return success_response(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token,
        }
    )

@app.route("/session/", methods=["POST"])
def update_session():
    """
    Endpoint for updating a user's session
    """
    success, update_token = extract_token(request)

    if not success:
        return update_token
    
    user = users_dao.renew_session(update_token)

    if user is None:
        return json.dumps({"error": "Invalid update token."})
    
    return success_response(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token,
        }
    ) 

@app.route("/secret/", methods=["GET"])
def secret_message():
    """
    Endpoint for verifying a session token and returning a secret message

    In your project, you will use the same logic for any endpoint that needs 
    authentication
    """
    success, session_token = extract_token(request)

    if not success:
        return session_token
    
    user = users_dao.get_user_by_session_token(session_token)

    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    
    return json.dumps({"message" : "Success"})


@app.route("/logout/", methods=["POST"])
def logout():
    """
    Endpoint for logging out a user
    """
    success, session_token = extract_token(request)

    if not success:
        return session_token
    
    user = users_dao.get_user_by_session_token(session_token)

    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    
    user.session_expiration = datetime.datetime.now()
    db.session.commit()

    return json.dumps({"message": "User has logged out"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
