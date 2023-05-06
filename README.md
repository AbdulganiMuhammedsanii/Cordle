# Cordle
Backend:
The Puzzle App backend is a simple, yet powerful API that allows users to manage puzzles and track their progress. 
This repository contains the Python code and database models for the backend part of the app. 
The app is designed to provide a solid foundation for further development and expansion.

Key Components
The backend of the app mainly consists of two parts:

Application File (app.py)
Database Models (db.py)

The app.py file contains the main Flask application, providing an API to manage puzzles and users. 
The app uses SQLAlchemy and relationship mapping to interact with an SQL database.

The Flask application defines several API endpoints to perform the following operations:

-Get all puzzles
-Create a new puzzle
-Get a specific puzzle by id
-Delete a puzzle
-Get the number of puzzles in the database
-Get a user by id
-Add a completed puzzle to a user
-Register a new user
-Log in a user
-Update a user's session
-Log out a user

Database Models
The db.py file contains the necessary code to set up the database and define the data models for the Flask web application. 
It uses SQLAlchemy as the ORM to interact with an SQLite database. The file contains two main classes:

Puzzle: This class represents a puzzle with a word and a hint.
User: This class represents a user with an email, a password, and a list of completed puzzles.
A many-to-many relationship exists between puzzles and users, representing the association 
between users and the puzzles they have completed. 


Future Development
This backend provides a solid foundation for further development and expansion. 
Some areas we could potentially improvement:
-Implementing more secure user authentication
-Adding support for more complex puzzle types
-Adding a more complex scoring system or leaderboards
-Feel free to fork this repository and build upon it to create your own!
