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
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS glucose_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                value_mmol REAL NOT NULL,
                timestamp TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()

    @classmethod
    def create(cls, user_id, value_mmol, notes=None):
        conn = Database.connect()
        cursor = Database.get_cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO glucose_entries (user_id, value_mmol, timestamp, notes) VALUES (?, ?, ?, ?)",
            (user_id, value_mmol, timestamp, notes)
        )
        conn.commit()
        entry_id = cursor.lastrowid
        return cls(user_id, value_mmol, notes, timestamp, entry_id)

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute("SELECT id, user_id, value_mmol, timestamp, notes FROM glucose_entries")
        rows = cursor.fetchall()
        return [cls(row[1], row[2], row[4], row[3], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, entry_id):
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT id, user_id, value_mmol, timestamp, notes FROM glucose_entries WHERE id = ?",
            (entry_id,)
        )
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[4], row[3], row[0])
        return None

    @classmethod
    def find_by_user(cls, user_id):
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT id, user_id, value_mmol, timestamp, notes FROM glucose_entries WHERE user_id = ?",
            (user_id,)
        )
        rows = cursor.fetchall()
        return [cls(row[1], row[2], row[4], row[3], row[0]) for row in rows]

    @classmethod
    def update(cls, entry_id, value_mmol=None, notes=None):
        conn = Database.connect()
        cursor = Database.get_cursor()

        fields = []
        values = []

        if value_mmol is not None:
            fields.append("value_mmol = ?")
            values.append(value_mmol)

        if notes is not None:
            fields.append("notes = ?")
            values.append(notes)

        if not fields:
            raise ValueError("No fields to update")

        values.append(entry_id)
        query = f"UPDATE glucose_entries SET {', '.join(fields)} WHERE id = ?"

        try:
            cursor.execute(query, tuple(values))
            conn.commit()
            print(f"Entry {entry_id} updated successfully.")
            return cls.find_by_id(entry_id)
        except Exception as e:
            print("Database error:", e)
            return None

    @classmethod
    def delete(cls, entry_id):
        conn = Database.connect()
        cursor = Database.get_cursor()

        try:
            cursor.execute("DELETE FROM glucose_entries WHERE id = ?", (entry_id,))
            conn.commit()
            print(f"Entry {entry_id} deleted.")
            return True
        except Exception as e:
            print("Database error:", e)
            return False
