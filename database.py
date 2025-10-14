import sqlite3
import os

DB_PATH = os.path.join("data", "blood_glucose.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE
        );
    """)

    # Create glucose_entries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS glucose_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            value REAL NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Creates the database tables when running this file directly
    create_tables()
    print("Database and tables created successfully!")

