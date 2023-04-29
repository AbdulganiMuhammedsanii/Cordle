import json

from db import db
from flask import Flask, request
from db import Puzzle

#define cms filename
app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error" : message}), code

# your routes here
@app.route("/")
@app.route("/api/puzzles/")
def get_courses():
    """
    Endpoint for getting all puzzles  
    """
    #returns all the puzzles that exist with all the initialized fields
    puzzles = [e.serialize() for e in Puzzle.query.all()]
    return success_response({"puzzles": puzzles}, 200)


@app.route("/api/puzzles/", methods = ["POST"])
def create_course():
    """
    Endpoint for creating a new puzzle  
    """
    #creates the new puzzle with the appropriate fields
    body = json.loads(request.data)
    if body.get("word","") == "" and body.get("hint","") == "":
        return failure_response("No puzzle word or hint!", 400)
    if body.get("hint","") == "":
        return failure_response("No puzzle hint!", 400)
    if body.get("word",False) is False:
        return failure_response("No puzzle word!", 400)
    new_puzzle = Puzzle(
        word = body.get("word"),
        hint = body.get("hint"),
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



@app.route("/api/courses/<int:puzzle_id>/", methods=["DELETE"])
def delete_course(puzzle_id):
    """
    Endpoint for deleting a puzzle by id
    """
    #deleting a puzzle by deleting it from the session after
    #first querying that it is present in the list.
    puzzle = Puzzle.query.filter_by(id=puzzle_id).first()
    if puzzle is None:
        return failure_response("Course not found!")
    db.session.delete(puzzle)
    db.session.commit()
    return success_response(puzzle.serialize(), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
