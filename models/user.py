from db.database import Database

class User:
    db = Database()  # Shared database connection

    def __init__(self, name, age, email, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.email = email

    # ---------- Property Validations ----------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string.")
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Age must be a positive integer.")
        self._age = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format.")
        self._email = value

    # ---------- ORM METHODS ----------
    @classmethod
    def create_table(cls):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
        """
        cls.db.execute_query(query)

    @classmethod
    def create(cls, name, age, email):
        user = cls(name, age, email)
        query = "INSERT INTO users (name, age, email) VALUES (?, ?, ?);"
        cls.db.execute_query(query, (user.name, user.age, user.email))
        user.id = cls.db.get_cursor().lastrowid
        return user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        rows = cls.db.execute_query(query).fetchall()
        return [cls(id=row[0], name=row[1], age=row[2], email=row[3]) for row in rows]

    @classmethod
    def find_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = ?;"
        row = cls.db.execute_query(query, (user_id,)).fetchone()
        if row:
            return cls(id=row[0], name=row[1], age=row[2], email=row[3])
        return None

    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM users WHERE id = ?;"
        cls.db.execute_query(query, (user_id,))
        return True
