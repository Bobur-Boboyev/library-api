# 📚 Library API

A production-ready REST API for managing books, authors, and genres — built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [Database](#database)
- [API Overview](#api-overview)
- [Development](#development)
- [Notes](#notes)

---

## Features

- Full CRUD for **Books**, **Authors**, and **Genres**
- **Many-to-many** relationship between Books and Genres
- **Filtering & search** on all list endpoints
- Automatic request/response validation via Pydantic v2
- Auto-generated interactive docs (Swagger UI & ReDoc)
- Clean separation of concerns: models / schemas / crud / routers

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.111 |
| Language | Python 3.11+ |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL |
| DB Driver | psycopg2-binary |
| Validation | Pydantic v2 |
| Settings | pydantic-settings |
| Server | Uvicorn |

---

## Project Structure

```
library-api/
├── app/
│   ├── main.py              # App entry point, router registration
│   ├── config.py            # Settings loaded from .env
│   ├── database.py          # Engine, SessionLocal, Base
│   ├── dependencies.py      # Shared FastAPI dependencies (get_db)
│   │
│   ├── models/
│   │   ├── __init__.py      # Imports all models (required for Base.metadata)
│   │   ├── author.py        # Author ORM model
│   │   ├── genre.py         # Genre ORM model + book_genres association table
│   │   └── book.py          # Book ORM model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── author.py        # AuthorCreate / AuthorUpdate / AuthorResponse
│   │   ├── genre.py         # GenreCreate / GenreUpdate / GenreResponse
│   │   └── book.py          # BookCreate / BookUpdate / BookResponse
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── author.py        # Author DB operations
│   │   ├── genre.py         # Genre DB operations
│   │   └── book.py          # Book DB operations
│   │
│   └── routers/
│       ├── __init__.py
│       ├── authors.py       # /authors endpoints
│       ├── genres.py        # /genres endpoints
│       └── books.py         # /books endpoints
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourname/library-api.git
cd library-api

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/librarydb` |

**Example `.env`:**
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/librarydb
```

### Running the App

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload

# Custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The app will be available at:

| Interface | URL |
|---|---|
| API Base | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/ |

---

## Database

Tables are created automatically on startup via:

```python
Base.metadata.create_all(bind=engine)
```

### Schema Overview

```
authors
  id            INTEGER  PK
  first_name    VARCHAR(100)
  last_name     VARCHAR(100)
  bio           TEXT  (nullable)
  born_date     DATE  (nullable)

genres
  id            INTEGER  PK
  name          VARCHAR(100)  UNIQUE
  description   TEXT  (nullable)

books
  id             INTEGER  PK
  title          VARCHAR(255)
  description    TEXT  (nullable)
  isbn           VARCHAR(20)  UNIQUE (nullable)
  published_year SMALLINT  (nullable)
  pages          INTEGER  (nullable)
  author_id      INTEGER  FK → authors.id  ON DELETE CASCADE

book_genres  (association table)
  book_id        INTEGER  FK → books.id   ON DELETE CASCADE
  genre_id       INTEGER  FK → genres.id  ON DELETE CASCADE
```

### Relationships

- `Author` → `Book` : one-to-many (one author has many books)
- `Book` ↔ `Genre` : many-to-many (via `book_genres` table)
- Deleting an author cascades and deletes all their books

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authors/` | List authors (search, pagination) |
| POST | `/authors/` | Create author |
| GET | `/authors/{id}` | Get author by ID |
| PATCH | `/authors/{id}` | Update author |
| DELETE | `/authors/{id}` | Delete author |
| GET | `/authors/{id}/books` | Get all books by an author |
| GET | `/genres/` | List genres (search, pagination) |
| POST | `/genres/` | Create genre |
| GET | `/genres/{id}` | Get genre by ID |
| PATCH | `/genres/{id}` | Update genre |
| DELETE | `/genres/{id}` | Delete genre |
| GET | `/genres/{id}/books` | Get all books in a genre |
| GET | `/books/` | List books (search, filter, pagination) |
| POST | `/books/` | Create book |
| GET | `/books/{id}` | Get book by ID |
| PATCH | `/books/{id}` | Update book |
| DELETE | `/books/{id}` | Delete book |

For full request/response details see [API_DOCS.md](./API_DOCS.md).

---

## Development

### Code Style

The project follows standard Python conventions. Recommended tools:

```bash
pip install ruff black

ruff check .      # linting
black .           # formatting
```

### Adding a New Resource

1. Add ORM model in `app/models/`
2. Register it in `app/models/__init__.py`
3. Add Pydantic schemas in `app/schemas/`
4. Add CRUD functions in `app/crud/`
5. Add router in `app/routers/`
6. Register router in `app/main.py`

---

## Notes

- All list endpoints support `skip` and `limit` for pagination (`limit` max: 100)
- `PATCH` endpoints use partial updates — only provided fields are changed
- Deleting an author will cascade-delete all their books
- Genre names are unique (case-insensitive check)
- ISBN uniqueness is enforced at the application layer
- `genre_ids` is a list of existing genre IDs sent when creating or updating a book
