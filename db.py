import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Venmo app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Secures a connection with the database and
        stores it in an instance variable
        """

        self.conn = sqlite3.connect(
            "todo.db", check_same_thread=False
        )

        self.delete_puzzle_table()
        self.create_puzzle_table()

    def create_puzzle_table(self):
        """
        Using SQL, create puzzle table
        """

        try:
            self.conn.execute(
                """
                CREATE TABLE puzzle (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    hint TEXT NOT NULL
                );
                """
            )
        except Exception as e:
            print(e)

    def delete_puzzle_table(self):
        """
        Using SQL, deletes a puzzle table
        """

        self.conn.execute("DROP TABLE IF EXISTS puzzle;")

    def get_all_puzzles(self):
        """
        Using SQL, gets all puzzles in the puzzle table
        """

        cursor = self.conn.execute("SELECT * FROM puzzle;")
        puzzles = []

        for row in cursor:
            puzzles.append({"id" : row[0], "word": row[1], "hint": row[2]}) 
        return puzzles
    
    def insert_puzzle_table(self, word, hint):
        """
        Using SQL, adds a new puzzle in the puzzles table
        """
        cursor = self.conn.execute("INSERT INTO puzzle (word, hint) VALUES (?, ?);", (word, hint))
        self.conn.commit()
        return cursor.lastrowid

    def get_puzzle_by_id(self, id):
        """
        Using SQL, gets a puzzle by ID
        """
        cursor = self.conn.execute("SELECT * FROM puzzle WHERE ID = ?;", (id,))

        for row in cursor:
            return {"id" : row[0], "word": row[1], "hint": row[2]}
        return None
    
    def update_puzzle_by_id(self, id, word, hint):
        """
        Using SQL, updates a puzzle by ID
        """
        self.conn.execute(
            """
            UPDATE puzzle
            SET word = ?, hint = ?
            WHERE id = ?;
            """,
            (word, hint, id)
        )
        self.conn.commit()
     
    def delete_puzzle_by_id(self, id):
        """
        Using SQL, deletes a puzzle by id
        """
        self.conn.execute(
            """
            DELETE FROM puzzle
            WHERE id = ?;
            """,
            (id,)
        )

        self.conn.commit()



# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
