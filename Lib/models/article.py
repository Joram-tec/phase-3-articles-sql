from Lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
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
            cls(title=row[1], author_id=row[2], magazine_id=row[3], id=row[0])
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
            return cls(title=row[1], author_id=row[2], magazine_id=row[3], id=row[0])
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
        self.id = None  # Clear ID after deletion
@classmethod
def get_all(cls):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()
    conn.close()
    return [cls(**row) for row in rows]

@classmethod
def get(cls, article_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    return cls(**row) if row else None
