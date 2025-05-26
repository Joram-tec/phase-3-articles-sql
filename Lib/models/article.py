from Lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        if not title:
            raise ValueError("Article title cannot be empty.")
        if not author_id:
            raise ValueError("Article must have an author_id.")
        if not magazine_id:
            raise ValueError("Article must have a magazine_id.")

        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
    # Validate author_id exists
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM authors WHERE id = ?", (self.author_id,))
        if cursor.fetchone() is None:
            conn.close()
            raise ValueError(f"Author with id {self.author_id} does not exist.")

    # Validate magazine_id exists
        cursor.execute("SELECT 1 FROM magazines WHERE id = ?", (self.magazine_id,))
        if cursor.fetchone() is None:
            conn.close()
            raise ValueError(f"Magazine with id {self.magazine_id} does not exist.")

    # Validate title not empty
        if not self.title:
            conn.close()
            raise ValueError("Article title cannot be empty.")

        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (self.title, self.author_id, self.magazine_id)
     )
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()


    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [
            cls(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"])
            for row in rows
        ]

    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"])
        return None

    def update(self, new_title=None, new_author_id=None, new_magazine_id=None):
        if not self.id:
            raise ValueError("Article must be saved before updating.")

        self.title = new_title or self.title
        self.author_id = new_author_id or self.author_id
        self.magazine_id = new_magazine_id or self.magazine_id

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
            (self.title, self.author_id, self.magazine_id, self.id)
        )
        conn.commit()
        conn.close()

    def delete(self):
        if not self.id:
            raise ValueError("Article must be saved before deleting.")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
        self.id = None
