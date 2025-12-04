# Python FastAPI Template

Starter template for Python backend applications using FastAPI.

## Stack

- FastAPI (async web framework)
- SQLAlchemy 2.0 (ORM)
- Pydantic 2.0 (validation)
- PostgreSQL (database)
- Alembic (migrations)

## Project Structure

```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── config.py            # Settings and environment
│   ├── database.py          # Database connection
│   ├── dependencies.py      # Shared dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/             # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   └── services/            # Business logic
│       ├── __init__.py
│       └── user_service.py
├── alembic/                 # Database migrations
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your database URL

# 4. Run migrations
alembic upgrade head

# 5. Start server
uvicorn app.main:app --reload
```

Access API docs: http://localhost:8000/docs

## Use with Skill

This template is referenced by the `assembling-components` skill for rapidly scaffolding Python backend applications.
