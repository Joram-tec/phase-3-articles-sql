from Lib.db.connection import get_connection
from Lib.models.article import Article

class Magazine:
    def __init__(self, name, category, id=None):
        if not name:
            raise ValueError("Magazine name cannot be empty.")
        if not category:
            raise ValueError("Magazine category cannot be empty.")

        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (self.name, self.category)
        )
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"], category=row["category"])
        return None

    @classmethod
    def get(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"], category=row["category"])
        return None


    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [
            Article(
                id=row["id"],
                title=row["title"],
                author_id=row["author_id"],
                magazine_id=row["magazine_id"]
            )
            for row in rows
        ]

    def update(self, new_name=None, new_category=None):
        if not self.id:
            raise ValueError("Magazine must be saved before updating.")

        self.name = new_name or self.name
        self.category = new_category or self.category

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
            (self.name, self.category, self.id)
        )
        conn.commit()
        conn.close()

    def delete(self):
        if not self.id:
            raise ValueError("Magazine must be saved before deleting.")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM magazines WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
        self.id = None
