from db.database import Database


class User:
    def __init__(self, name, age=None, email=None, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.email = email

    @classmethod
    def create_table(cls):
        db = Database()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE
        );
        """
        db.execute_query(create_table_query)
        db.close()

    @classmethod
    def create(cls, name, age=None, email=None):
        db = Database()
        insert_query = """
        INSERT INTO users (name, age, email)
        VALUES (?, ?, ?);
        """
        cursor = db.execute_query(insert_query, (name, age, email))
        db.close()
        return cls(name=name, age=age, email=email, id=cursor.lastrowid)

    @classmethod
    def get_all(cls):
        db = Database()
        select_query = "SELECT id, name, age, email FROM users;"
        cursor = db.execute_query(select_query)
        rows = cursor.fetchall()
        db.close()

        return [cls(id=row[0], name=row[1], age=row[2], email=row[3]) for row in rows]

    @classmethod
    def find_by_id(cls, user_id):
        db = Database()
        query = "SELECT id, name, age, email FROM users WHERE id = ?;"
        cursor = db.execute_query(query, (user_id,))
        row = cursor.fetchone()
        db.close()

        if row:
            return cls(id=row[0], name=row[1], age=row[2], email=row[3])
        return None

    @classmethod
    def delete(cls, user_id):
        db = Database()
        delete_query = "DELETE FROM users WHERE id = ?;"
        db.execute_query(delete_query, (user_id,))
        db.close()
