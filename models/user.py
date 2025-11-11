from db.database import Database
from models.glucose_entry import GlucoseEntry


class User:
    def __init__(self, name, age, email, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.email = email

    @classmethod
    def create_table(cls):
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE
            );
        """
        )
        conn.commit()

    @classmethod
    def create(cls, name, age, email):
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (name, age, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return cls(name, age, email, user_id)

    @classmethod
    def get_all(cls):
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute("SELECT id, name, age, email FROM users")
        rows = cursor.fetchall()
        return [cls(row[1], row[2], row[3], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, user_id):
        conn = Database.connect()
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT id, name, age, email FROM users WHERE id = ?", (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[0])
        return None

    @classmethod
    def update(cls, user_id, name=None, age=None, email=None):
        conn = Database.connect()
        cursor = Database.get_cursor()

        fields = []
        values = []

        if name is not None:
            fields.append("name = ?")
            values.append(name)

        if age is not None:
            fields.append("age = ?")
            values.append(age)

        if email is not None:
            fields.append("email = ?")
            values.append(email)

        if not fields:
            raise ValueError("No fields to update")

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"

        try:
            cursor.execute(query, tuple(values))
            conn.commit()
            print(f"User {user_id} updated successfully.")
            return cls.find_by_id(user_id)
        except Exception as e:
            print("Database error:", e)
            return None

    @classmethod
    def delete(cls, user_id):
        conn = Database.connect()
        cursor = Database.get_cursor()

        # Delete related glucose entries first
        cursor.execute("DELETE FROM glucose_entries WHERE user_id = ?", (user_id,))

        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        print(f"User {user_id} and related entries deleted.")

    # Relationship methods
    def glucose_entries(self):
        return GlucoseEntry.find_by_user(self.id)

    def add_glucose_entry(self, value_mmol, notes=None):
        return GlucoseEntry.create(self.id, value_mmol, notes)
