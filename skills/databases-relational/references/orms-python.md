# Python ORMs and Database Libraries

## Overview

Python database libraries span from high-level ORMs to low-level drivers, each with different trade-offs.

| Library | Context7 ID | Type | Async | Type Safety | Best For |
|---------|-------------|------|-------|-------------|----------|
| **SQLAlchemy 2.0** | `/websites/sqlalchemy_en_21` | ORM + Core | ✅ | Pydantic v2 | Production apps, flexibility |
| **SQLModel** | - | ORM | ✅ | Pydantic v2 | FastAPI, rapid prototyping |
| **Tortoise ORM** | - | ORM | ✅ | Pydantic | Async-first apps |
| **asyncpg** | - | Driver | ✅ | Manual | Maximum performance |
| **psycopg3** | - | Driver | ✅ | Manual | PostgreSQL-specific |

## SQLAlchemy 2.0 (Recommended for Most Projects)

**Context7:** `/websites/sqlalchemy_en_21` (7,090 snippets)
**ORM Docs:** `/websites/sqlalchemy_en_20_orm` (2,047 snippets)

### Core Concepts

SQLAlchemy 2.0 has two layers:
1. **Core**: Low-level SQL expression language (query builder)
2. **ORM**: High-level object-relational mapping

**Installation:**
```bash
pip install sqlalchemy[asyncio] asyncpg  # For PostgreSQL
pip install sqlalchemy[asyncio] aiomysql  # For MySQL
```

### ORM Pattern (Declarative)

**Define Models:**
```python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="posts")

# Create engine with connection pooling
engine = create_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

# Create tables
Base.metadata.create_all(engine)
```

**CRUD Operations:**
```python
# Create
with Session(engine) as session:
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
    session.refresh(user)  # Get generated ID
    print(user.id)

# Read
with Session(engine) as session:
    user = session.query(User).filter(User.email == "test@example.com").first()
    # Or using modern select() syntax
    from sqlalchemy import select
    stmt = select(User).where(User.email == "test@example.com")
    user = session.execute(stmt).scalar_one()

# Update
with Session(engine) as session:
    user = session.query(User).filter(User.id == 1).first()
    user.name = "Updated Name"
    session.commit()

# Delete
with Session(engine) as session:
    user = session.query(User).filter(User.id == 1).first()
    session.delete(user)
    session.commit()
```

**Relationships and Joins:**
```python
with Session(engine) as session:
    # Eager loading (fetch posts with users in one query)
    from sqlalchemy.orm import joinedload
    users = session.query(User).options(joinedload(User.posts)).all()

    # Explicit join
    stmt = (
        select(User, Post)
        .join(Post)
        .where(User.email.like('%@example.com'))
    )
    results = session.execute(stmt).all()
```

### Async Support (SQLAlchemy 2.0+)

**Async Engine:**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)

# Usage with FastAPI
from fastapi import Depends

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.get("/users/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user
```

### Core (Query Builder)

Use Core for complex queries, better performance, or when ORM overhead unnecessary.

```python
from sqlalchemy import Table, Column, Integer, String, MetaData, select, insert

metadata = MetaData()

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, unique=True, nullable=False),
    Column('name', String, nullable=False)
)

# Create
stmt = insert(users).values(email="test@example.com", name="Test User")
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

# Read
stmt = select(users).where(users.c.email == "test@example.com")
with engine.connect() as conn:
    result = conn.execute(stmt)
    row = result.fetchone()

# Complex query
from sqlalchemy import func
stmt = (
    select(users.c.name, func.count(posts.c.id).label('post_count'))
    .select_from(users.join(posts))
    .group_by(users.c.name)
    .having(func.count(posts.c.id) > 5)
)
```

### Transactions

```python
from sqlalchemy import text

with Session(engine) as session:
    try:
        session.begin()  # Explicit transaction
        session.execute(text("UPDATE users SET name = 'Alice' WHERE id = 1"))
        session.execute(text("UPDATE posts SET title = 'New Title' WHERE user_id = 1"))
        session.commit()
    except Exception:
        session.rollback()
        raise
```

## SQLModel (FastAPI Integration)

**Installation:**
```bash
pip install sqlmodel
```

**Define Models:**
```python
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    posts: List["Post"] = Relationship(back_populates="author")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")
    author: User = Relationship(back_populates="posts")

engine = create_engine("postgresql://user:pass@localhost/db")
SQLModel.metadata.create_all(engine)
```

**FastAPI Integration:**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=List[User])
def list_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users
```

**Why SQLModel?**
- Pydantic validation built-in
- Single model class for DB and API
- Type hints throughout
- FastAPI integration seamless
- Built on SQLAlchemy (can drop to SQLAlchemy for complex queries)

## asyncpg (High Performance)

Direct PostgreSQL driver with best performance.

**Installation:**
```bash
pip install asyncpg
```

**Usage:**
```python
import asyncpg

async def main():
    # Create connection pool
    pool = await asyncpg.create_pool(
        user='user',
        password='password',
        database='database',
        host='localhost',
        min_size=5,
        max_size=20
    )

    # Query
    async with pool.acquire() as conn:
        # Select
        rows = await conn.fetch('SELECT * FROM users WHERE email = $1', 'test@example.com')
        for row in rows:
            print(row['id'], row['email'], row['name'])

        # Insert
        user_id = await conn.fetchval(
            'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id',
            'new@example.com', 'New User'
        )

        # Transaction
        async with conn.transaction():
            await conn.execute('UPDATE users SET name = $1 WHERE id = $2', 'Alice', 1)
            await conn.execute('UPDATE posts SET title = $1 WHERE user_id = $2', 'New Title', 1)

    await pool.close()
```

**When to Use asyncpg:**
- Maximum performance needed
- Willing to write raw SQL
- PostgreSQL-specific features
- Microservices with simple queries

## Tortoise ORM (Async-First)

**Installation:**
```bash
pip install tortoise-orm asyncpg  # For PostgreSQL
```

**Define Models:**
```python
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    name = fields.CharField(max_length=255)
    posts = fields.ReverseRelation["Post"]

    class Meta:
        table = "users"

class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField(null=True)
    author = fields.ForeignKeyField('models.User', related_name='posts')

    class Meta:
        table = "posts"

# Generate Pydantic models
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
```

**FastAPI Integration:**
```python
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

@app.post("/users/", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await User.create(**user.dict())
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get("/users/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))

register_tortoise(
    app,
    db_url="postgres://user:pass@localhost:5432/db",
    modules={"models": ["myapp.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
```

## Comparison: When to Use Each

### Choose SQLAlchemy 2.0 When:
- Need maximum flexibility (ORM + Core)
- Working with complex schemas
- Require advanced features (polymorphic inheritance, hybrid properties)
- Want to switch between sync/async
- Team experienced with SQLAlchemy

### Choose SQLModel When:
- Using FastAPI
- Want Pydantic integration
- Prefer simple, type-safe API
- Rapid prototyping
- Can drop to SQLAlchemy for complex queries

### Choose Tortoise ORM When:
- Async-first application
- Like Django ORM syntax
- Need Pydantic models from ORM
- Simpler learning curve than SQLAlchemy

### Choose asyncpg When:
- Maximum performance critical
- Simple queries, minimal ORM needed
- PostgreSQL-only application
- Microservices architecture

## Migration Tools

### Alembic (SQLAlchemy)

**Installation:**
```bash
pip install alembic
alembic init alembic
```

**Create Migration:**
```bash
alembic revision --autogenerate -m "Add users table"
alembic upgrade head  # Apply migration
alembic downgrade -1  # Rollback one migration
```

**Migration File:**
```python
# alembic/versions/001_add_users.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
```

### Aerich (Tortoise ORM)

**Installation:**
```bash
pip install aerich
aerich init -t config.TORTOISE_ORM
aerich init-db
```

**Create Migration:**
```bash
aerich migrate --name "add_users"
aerich upgrade
aerich downgrade
```

## Best Practices

### Use Connection Pooling
```python
# SQLAlchemy
engine = create_engine(
    "postgresql+asyncpg://...",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)

# asyncpg
pool = await asyncpg.create_pool(
    ...,
    min_size=10,
    max_size=20,
    max_queries=50000,  # Recycle connection after 50k queries
    max_inactive_connection_lifetime=300  # Recycle after 5 min idle
)
```

### Use Transactions for Multi-Statement Operations
```python
# SQLAlchemy
with Session(engine) as session:
    try:
        session.begin()
        session.add(user)
        session.add(post)
        session.commit()
    except Exception:
        session.rollback()
        raise

# asyncpg
async with conn.transaction():
    await conn.execute(...)
    await conn.execute(...)
```

### Use Parameterized Queries (Prevent SQL Injection)
```python
# GOOD - Parameterized
user = session.query(User).filter(User.email == email).first()
stmt = select(User).where(User.email == email)

# BAD - String interpolation (SQL injection risk!)
session.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### Batch Operations for Performance
```python
# SQLAlchemy bulk insert
session.bulk_insert_mappings(User, [
    {"email": "user1@example.com", "name": "User 1"},
    {"email": "user2@example.com", "name": "User 2"},
    # ... thousands of rows
])

# asyncpg batch insert
await conn.executemany(
    'INSERT INTO users (email, name) VALUES ($1, $2)',
    [('user1@example.com', 'User 1'), ('user2@example.com', 'User 2')]
)
```

### Index Frequently Queried Columns
```python
class User(Base):
    __tablename__ = 'users'
    email = Column(String, unique=True, index=True)  # Index for WHERE clauses
    created_at = Column(DateTime, index=True)  # Index for ORDER BY
```

## Resources

- SQLAlchemy 2.0 Docs: https://docs.sqlalchemy.org/en/20/
- SQLModel Docs: https://sqlmodel.tiangolo.com/
- Tortoise ORM Docs: https://tortoise.github.io/
- asyncpg Docs: https://magicstack.github.io/asyncpg/
- Alembic Docs: https://alembic.sqlalchemy.org/
