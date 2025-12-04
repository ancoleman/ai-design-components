# FastAPI Dashboard Backend Example

Complete FastAPI backend for dashboard applications with PostgreSQL, authentication, and real-time metrics.

## Features

- User authentication (JWT)
- Dashboard metrics endpoints
- Real-time data streaming (SSE)
- PostgreSQL with SQLAlchemy 2.0
- CORS configuration
- Rate limiting
- OpenAPI documentation

## Project Structure

```
fastapi-dashboard/
├── app/
│   ├── main.py              # FastAPI app
│   ├── auth.py              # JWT authentication
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   └── routers/
│       ├── dashboard.py     # Dashboard endpoints
│       ├── metrics.py       # Metrics streaming
│       └── users.py         # User management
├── requirements.txt
├── .env.example
└── README.md
```

## Endpoints

```
POST   /auth/login          - User login
POST   /auth/refresh        - Refresh token
GET    /dashboard/metrics   - Get dashboard KPIs
GET    /dashboard/charts    - Get chart data
GET    /metrics/stream      - SSE real-time metrics
GET    /users/me            - Get current user
```

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## Integration

This backend pairs with:
- Frontend: React dashboard (see examples/react-dashboard/)
- Database skill: databases-relational
- Auth skill: auth-security
- Real-time skill: realtime-sync (SSE)

## API Documentation

Access auto-generated docs at http://localhost:8000/docs
