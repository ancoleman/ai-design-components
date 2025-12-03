# Python SQLAlchemy Example

Production-ready FastAPI + SQLAlchemy 2.0 + PostgreSQL example with connection pooling and migrations.

## Features

- SQLAlchemy 2.0 with async support
- FastAPI REST API
- Connection pooling configuration
- Alembic migrations
- User CRUD operations
- Password hashing with Argon2

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
# Set database URL
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

# Run migrations
alembic upgrade head
```

## Running

```bash
# Development server with auto-reload
uvicorn main:app --reload

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Create User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User", "password": "securepassword"}'
```

### Get User
```bash
curl http://localhost:8000/users/1
```

### List Users
```bash
curl "http://localhost:8000/users?skip=0&limit=10"
```

### Update User
```bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/users/1
```

## Connection Pooling

Configured in `main.py`:

```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # 20 normal connections
    max_overflow=10,        # 10 extra under load (total max = 30)
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=3600,      # Recycle after 1 hour
)
```

**Tuning:**
- Web API: `pool_size=20`, `max_overflow=10`
- Background worker: `pool_size=5`, `max_overflow=5`
- Serverless: `pool_size=1`, `max_overflow=0` (use pgBouncer)

## Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Project Structure

```
python-sqlalchemy/
├── alembic/
│   └── versions/
│       └── 001_initial.py
├── models.py          # Database models
├── schemas.py         # Pydantic schemas
├── main.py            # FastAPI application
├── requirements.txt   # Python dependencies
└── README.md
```

## Production Checklist

- [ ] Use environment variables for DATABASE_URL
- [ ] Enable SSL for database connections
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Add rate limiting
- [ ] Implement authentication/authorization
- [ ] Set up monitoring (prometheus, datadog)
- [ ] Use pgBouncer for connection pooling
