from db.database import Database
from datetime import datetime

class GlucoseEntry:
    def __init__(self, user_id, value_mmol, notes=None, timestamp=None, id=None):
        self.id = id
        self.user_id = user_id
        self.value_mmol = value_mmol
        self.notes = notes
        self.timestamp = timestamp or datetime.now().isoformat()

    @classmethod
    def create_table(cls):
        db = Database()
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS glucose_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                value_mmol REAL NOT NULL,
                timestamp TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        db.close()

    @classmethod
    def create(cls, user_id, value_mmol, notes=None):
        db = Database()
        timestamp = datetime.now().isoformat()
        cursor = db.execute_query(
            "INSERT INTO glucose_entries (user_id, value_mmol, timestamp, notes) VALUES (?, ?, ?, ?)",
            (user_id, value_mmol, timestamp, notes)
        )
        entry_id = cursor.lastrowid
        db.close()
        return cls(user_id, value_mmol, notes, timestamp, entry_id)

    @classmethod
    def get_all(cls):
        db = Database()
        cursor = db.execute_query(
            "SELECT id, user_id, value_mmol, timestamp, notes FROM glucose_entries"
        )
        rows = cursor.fetchall()
        db.close()
        return [cls(row[1], row[2], row[4], row[3], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, entry_id):
        db = Database()
        cursor = db.execute_query(
            "SELECT id, user_id, value_mmol, timestamp, notes FROM glucose_entries WHERE id = ?",
            (entry_id,)
        )
        row = cursor.fetchone()
        db.close()
        if row:
            return cls(row[1], row[2], row[4], row[3], row[0])
        return None

    @classmethod
    def find_by_user(cls, user_id):
        db = Database()
        cursor = db.execute_query(
            "SELECT id, user_id, value_mmol, timestamp, notes FROM glucose_entries WHERE user_id = ?",
            (user_id,)
        )
        rows = cursor.fetchall()
        db.close()
        return [cls(row[1], row[2], row[4], row[3], row[0]) for row in rows]

    @classmethod
    def delete(cls, entry_id):
        db = Database()
        db.execute_query("DELETE FROM glucose_entries WHERE id = ?", (entry_id,))
        db.close()
