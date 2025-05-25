import pytest
from Lib.models.author import Author
from Lib.models.magazine import Magazine
from Lib.models.article import Article
from Lib.db.connection import get_connection

@pytest.fixture
def clean_db():
    """Clean articles, authors, and magazines tables before each test."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('articles', 'authors', 'magazines')")
    conn.commit()
    conn.close()
    yield

@pytest.fixture
def sample_author_and_magazine(clean_db):
    """Create and save an author and a magazine for article tests."""
    author = Author(name="Test Author")
    author.save()
    magazine = Magazine(name="Test Magazine", category="Testing")
    magazine.save()
    return author, magazine

def test_article_creation_and_relationships(sample_author_and_magazine):
    author, magazine = sample_author_and_magazine
    article = Article(title="New Discoveries", author_id=author.id, magazine_id=magazine.id)
    article.save()

    assert article.id is not None
    assert article.title == "New Discoveries"
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id

    # Check author.articles() returns the article
    author_articles = author.articles()
    assert any(a.title == "New Discoveries" for a in author_articles)

    # Check magazine.articles() returns the article
    magazine_articles = magazine.articles()
    assert any(a.title == "New Discoveries" for a in magazine_articles)

def test_article_validation(sample_author_and_magazine):
    author, magazine = sample_author_and_magazine

    with pytest.raises(ValueError):
        Article(title="", author_id=author.id, magazine_id=magazine.id).save()  # empty title

    with pytest.raises(ValueError):
        Article(title="Valid Title", author_id=99999, magazine_id=magazine.id).save()  # invalid author_id

    with pytest.raises(ValueError):
        Article(title="Valid Title", author_id=author.id, magazine_id=99999).save()  # invalid magazine_id

def test_article_deletion(sample_author_and_magazine):
    author, magazine = sample_author_and_magazine
    article = Article(title="Delete Me", author_id=author.id, magazine_id=magazine.id)
    article.save()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM articles WHERE id = ?", (article.id,))
    assert cursor.fetchone() is not None

   
    conn.commit()

    cursor.execute("SELECT id FROM articles WHERE id = ?", (article.id,))
    assert cursor.fetchone() is None
    conn.close()
