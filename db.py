from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here

class Puzzle(db.Model):
    """
    Puzzle model 
    """
    #Puzzle table with all the fields necessary to initialize the puzzle.
    
    __tablename__ = "puzzle"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    word = db.Column(db.String, nullable=False)
    hint = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes a Puzzle object
        """
        
        self.word = kwargs.get("word", "")
        self.hint = kwargs.get("hint","")
    

    #serialize puzzle field
    def serialize(self):
        """
        Siderializes a Puzzle object
        """

        return {
            "id": self.id,
            "word": self.word,
            "hint": self.hint,


        }
    #simple serialize here returns puzzle values that don't have personal
    #information about users, etc.
    def simple_serialize(self):
        """
        Siderializes a Task object
        """

        return {
            "id": self.id,
            "code": self.word,
            "name": self.hint,

        }
