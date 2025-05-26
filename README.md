#  Phase 3: Articles SQL (Without SQLAlchemy)

Welcome to the **Phase 3 Articles Relationships Code Challenge**!  
This project models a simple publishing system involving **Authors**, **Magazines**, and **Articles** using Python and SQLite **without SQLAlchemy**.



##  Overview

This system handles:
- Many-to-many relationships via `Articles`
- Direct interaction with SQLite using `sqlite3`
- Python OOP design
- Manual schema creation and data seeding

---

##  Project Structure
│
├── Lib/
│ ├── db/
│ │ ├── connection.py
│ │ ├── schema.sql
│ │ └── seed.py
│ └── models/
│ ├── author.py
│ ├── magazine.py
│ └── article.py
│
├── scripts/
│ └── setup_db.py
│
├── tests/
│ └── test_article.py
│
└── README.md

---

##  Setup Instructions

> Make sure you're in the project root (`phase-3-articles-sql`) before running the following.

### 1. Install dependencies (if any)
We’re using Python's built-in modules, so just ensure your environment is ready:

```bash
python --version

## 2. Set up the database 
# python -m scripts.setup_db


## 3. Populate tables 
# python -m Lib.db.seed


## 4. Run tests
# pytest


## Author
# Made by @Joram-tec

##  Licensed





