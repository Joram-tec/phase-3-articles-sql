from Lib.db.connection import get_connection
from Lib.models.author import Author
from Lib.models.magazine import Magazine
from Lib.models.article import Article

def clear_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")

    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")

    #cursor.execute("DELETE FROM sqlite_sequence") 
    conn.close()

def seed_authors():
    authors = [
        {"name": "Joram Wayne", "specialty": "Technology"},
        {"name": "Austin Miana", "specialty": "Horror"},
        {"name": "Eunice Wangui", "specialty": "Science Fiction"},
        {"name": "GlGalo Austen", "specialty": "Romance"},
        {"name": "Bill Chris", "specialty": "Mystery"},
        {"name": "Ada Lovelace", "specialty": "Programming"},
        {"name": "Mary Shelley", "specialty": "Horror"},
        {"name": "Octavia Butler", "specialty": "Sci-Fi"},
        {"name": "Jane Austen", "specialty": "Romance"},
        {"name": "Agatha Christie", "specialty": "Mystery"}
]
    for author in authors:
        Author(name=author["name"]).save()

def seed_magazines():
    magazines = [
        {"name": "Code Challenges", "category": "Programming"},
        {"name": "Chilling Vibes", "category": "Horror"},
        {"name": "Light Visions", "category": "Sci-Fi"},
        {"name": "Nymphomaniac Love", "category": "Romance"},
        {"name": "The society ", "category": "Mystery"}
    ]
    for magazine in magazines:
        Magazine(name=magazine["name"], category=magazine["category"]).save()

def seed_articles():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM authors")
    authors = {row["name"]: row["id"] for row in cursor.fetchall()}
    
    cursor.execute("SELECT id, name, category FROM magazines")
    magazines = {row["category"]: row["id"] for row in cursor.fetchall()}
    
    
    articles = [
        {"title": "The First Algorithm", "author": "Ada Lovelace", "magazine_category": "Programming"},
        {"title": "Frankenstein's Code", "author": "Mary Shelley", "magazine_category": "Horror"},
        {"title": "Kindred Systems", "author": "Octavia Butler", "magazine_category": "Sci-Fi"},
        {"title": "Pride and Programming", "author": "Jane Austen", "magazine_category": "Romance"},
        {"title": "Murder in the Codebase", "author": "Agatha Christie", "magazine_category": "Mystery"},

        {"title": "The Analytical Engine", "author": "Ada Lovelace", "magazine_category": "Programming"},
        {"title": "The Last Man", "author": "Mary Shelley", "magazine_category": "Horror"},
        {"title": "Parable of the Programmer", "author": "Octavia Butler", "magazine_category": "Sci-Fi"}
    ]
    
    for article in articles:
        Article(
            title=article["title"],
            author_id=authors[article["author"]],
            magazine_id=magazines[article["magazine_category"]]
        ).save()
    
    conn.close()

def seed_database():
    """Run all seeding functions"""
    print("Cleared old data!")
    clear_database()
    
    print("Seeding authors!")
    seed_authors()
    
    print("Seeding magazines!")
    seed_magazines()
    
    print("Seeding articles!")
    seed_articles()
    
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()