import os
import sqlite3


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

    @classmethod
    def init_db(cls):
        """Creates required tables if they don't exist."""
        conn = cls.connect()
        cursor = cls.get_cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS glucose_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                value_mmol REAL NOT NULL,
                timestamp TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """
        )

        conn.commit()
        print("✓ Database tables initialized")
