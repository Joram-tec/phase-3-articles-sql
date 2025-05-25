import pytest
from Lib.models.magazine import Magazine
from Lib.db.connection import get_connection

@pytest.fixture
def clean_db():
    """Clean magazines table before each test."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='magazines'")  # reset autoincrement for magazines only
    conn.commit()
    conn.close()
    yield

def test_magazine_creation_and_retrieval(clean_db):
    mag = Magazine(name="Science Weekly", category="Science")
    mag.save()
    assert mag.id is not None
    assert mag.name == "Science Weekly"
    assert mag.category == "Science"

    retrieved = Magazine.get(mag.id)
    assert retrieved is not None
    assert retrieved.name == mag.name
    assert retrieved.category == mag.category

def test_magazine_validation(clean_db):
    with pytest.raises(ValueError):
        Magazine(name="", category="Tech").save()  # empty name invalid

    with pytest.raises(ValueError):
        Magazine(name="Tech Mag", category="").save()  # empty category invalid
