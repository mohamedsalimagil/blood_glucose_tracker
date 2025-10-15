from db.database import Database

class User:
    def __init__(self, name, age, email, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.email = email

    @classmethod
    def create_table(cls):
        db = Database()
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE
            );
        """)
        db.close()

    @classmethod
    def create(cls, name, age, email):
        db = Database()
        cursor = db.execute_query(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            (name, age, email)
        )
        user_id = cursor.lastrowid
        db.close()
        return cls(name, age, email, user_id)

    @classmethod
    def get_all(cls):
        db = Database()
        cursor = db.execute_query("SELECT id, name, age, email FROM users")
        rows = cursor.fetchall()
        db.close()
        return [cls(row[1], row[2], row[3], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, user_id):
        db = Database()
        cursor = db.execute_query(
            "SELECT id, name, age, email FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        db.close()
        if row:
            return cls(row[1], row[2], row[3], row[0])
        return None

    @classmethod
    def update(cls, user_id, name=None, age=None, email=None):
        db = Database()
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
            raise ValueError("No data provided to update.")

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"

        try:
            db.execute_query(query, tuple(values))
            print(f"User {user_id} updated successfully.")
            return cls.find_by_id(user_id)
        except Exception as e:
            print("Database error:", e)
            return None
        finally:
            db.close()

    @classmethod
    def delete(cls, user_id):
        db = Database()
        db.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
        db.close()
