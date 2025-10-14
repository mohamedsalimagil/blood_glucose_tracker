import sqlite3
import os

class Database:
    def __init__(self, db_name="blood_glucose.db"):
        db_folder = "data"
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
        db_path = os.path.join(db_folder, db_name)

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_cursor(self):
        return self.cursor

    def close(self):
        self.connection.close()
