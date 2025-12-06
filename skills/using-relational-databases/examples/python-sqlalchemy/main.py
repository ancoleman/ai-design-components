"""
FastAPI + SQLAlchemy 2.0 Example

Production-ready example with:
- Async SQLAlchemy
- Connection pooling
- Password hashing (Argon2)
- Pydantic validation
- Error handling
"""

import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db")

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # Recommended: 10-20 for web APIs
    max_overflow=10,        # Extra connections under load
    pool_pre_ping=True,     # Verify connection before use
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=True               # Log SQL queries (disable in production)
)

async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

# Pydantic schemas
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserUpdate(BaseModel):
    name: str | None = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="User API", version="1.0.0")

# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Routes
@app.on_event("startup")
async def startup():
    """Create tables on startup (use Alembic in production)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    """Create a new user with hashed password."""
    # Check if email exists
    stmt = select(User).where(User.email == user.email)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    password_hash = pwd_context.hash(user.password)

    # Create user
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=password_hash
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    """Get user by ID."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    """List users with pagination."""
    stmt = select(User).offset(skip).limit(limit)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update user."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_update.name:
        user.name = user_update.name

    await session.commit()
    await session.refresh(user)
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    """Delete user."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await session.delete(user)
    await session.commit()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
