import sqlite3
import os

class Database:
    _connection = None
    _cursor = None

    @classmethod
    def connect(cls, db_name="blood_glucose.db"):
        """Creates a single shared connection if not active."""
        if cls._connection is None:
            db_folder = "data"
            if not os.path.exists(db_folder):
                os.makedirs(db_folder)
            db_path = os.path.join(db_folder, db_name)

            cls._connection = sqlite3.connect(db_path)
            cls._cursor = cls._connection.cursor()

        return cls._connection

    @classmethod
    def get_cursor(cls):
        """Return the existing cursor from the shared connection."""
        if cls._cursor is None:
            cls.connect()
        return cls._cursor

    @classmethod
    def execute_query(cls, query, params=()):
        conn = cls.connect()
        cursor = cls.get_cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    @classmethod
    def close(cls):
        """Close the connection if it exists."""
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            cls._cursor = None
