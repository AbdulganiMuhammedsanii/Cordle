import json
from flask import Flask, request
import db
DB = db.DatabaseDriver()


app = Flask(__name__)


@app.route("/")
@app.route("/puzzles/")
def get_puzzles():
    """
    Endpoint for getting all puzzles
    """
    return json.dumps({"puzzles": DB.get_all_puzzles()}), 200



@app.route("/puzzles/", methods = ["POST"])
def create_puzzles():
    """
    Endpoint for creating a new puzzle
    """

    body = json.loads(request.data)
    word = body.get("word")
    hint = body.get("hint")

    puzzle_id = DB.insert_puzzle_table(word, hint)
    puzzle = DB.get_puzzle_by_id(puzzle_id)
    if puzzle is None:
        return json.dumps({"error": "Something went wrong while making puzzle"}), 400
    return json.dumps(puzzle), 201



@app.route("/puzzles/<int:puzzle_id>/")
def get_specific_puzzle(puzzle_id):
    """
    Endpoint for getting a puzzle by ID
    """
    
    puzzle = DB.get_puzzle_by_id(puzzle_id)
    if puzzle is None:
        return json.dumps({"error": "Puzzle not found!"}), 404
    return json.dumps(puzzle), 200
 

@app.route("/puzzles/<int:puzzle_id>", methods = ["POST"])
def update_puzzle(puzzle_id):
    """
    Endpoint for updating a puzzle by ID
    """

    body = json.loads(request.data)
    word = body.get("name")
    hint = body.get("hint")
    
    DB.update_puzzle_by_id(puzzle_id, word, hint)

    puzzle = DB.get_puzzle_by_id(puzzle_id)
    if puzzle is None:
        return json.dumps({"error": "puzzle not found!"}), 404
    return json.dumps(puzzle), 200 


@app.route("/puzzles/<int:puzzle_id>/", methods=["DELETE"])
def delete_puzzle(puzzle_id):
    puzzle = DB.get_puzzle_by_id(puzzle_id)
    if puzzle is None:
       return json.dumps({"error": "Puzzle not found!"}), 404 
    DB.delete_puzzle_by_id(puzzle_id)
    return json.dumps(puzzle), 200


# your routes here


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
