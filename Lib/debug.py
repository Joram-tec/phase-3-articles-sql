from Lib.models.author import Author
from Lib.models.magazine import Magazine
from Lib.models.article import Article

def print_all_data():
    """Print all database content in readable format"""
    print("=== AUTHORS ===")
    for author in Author.get_all():
        print(f"{author.id}: {author.name}")

    print("\n=== MAGAZINES ===")
    for mag in Magazine.get_all():
        print(f"{mag.id}: {mag.name} ({mag.category})")

    print("\n=== ARTICLES ===")
    for article in Article.get_all():
        author = Author.get(article.author_id)
        magazine = Magazine.get(article.magazine_id)
        print(f"{article.id}: '{article.title}'")
        print(f"   By: {author.name if author else 'Unknown'}")
        print(f"   In: {magazine.name if magazine else 'Unknown'}\n")

if __name__ == "__main__":
    print_all_data()