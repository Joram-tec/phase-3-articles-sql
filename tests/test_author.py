import pytest
from Lib.models.author import Author
from Lib.db.connection import get_connection

@pytest.fixture
def clean_db():
    """Clean authors table before each test."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='authors'")  # reset autoincrement for authors only
    conn.commit()
    conn.close()
    yield

def test_author_creation_and_retrieval(clean_db):
    author = Author(name="Jane Doe")
    author.save()
    assert author.id is not None
    assert author.name == "Jane Doe"

    retrieved = Author.get(author.id)
    assert retrieved is not None
    assert retrieved.id == author.id
    assert retrieved.name == "Jane Doe"

def test_author_validation(clean_db):
    with pytest.raises(ValueError):
        Author(name="").save()  # empty name invalid
