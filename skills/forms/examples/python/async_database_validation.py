"""
Async Database Validation Example

Demonstrates:
- Async/await validation
- Database lookups for uniqueness
- Custom async validators
- Debouncing database queries
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
import asyncio
import re

# Mock database (in production, use SQLAlchemy, MongoDB, etc.)
MOCK_DB = {
    'usernames': ['admin', 'user', 'test', 'demo'],
    'emails': ['admin@example.com', 'test@example.com'],
}

# Async validation functions
async def check_username_available(username: str) -> bool:
    """Simulate async database check"""
    await asyncio.sleep(0.1)  # Simulate DB query
    return username.lower() not in MOCK_DB['usernames']

async def check_email_available(email: str) -> bool:
    """Simulate async database check"""
    await asyncio.sleep(0.1)  # Simulate DB query
    return email.lower() not in MOCK_DB['emails']

class UserRegistrationAsync(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        # Enable validation on assignment for better UX
        validate_assignment = True

    @validator('username')
    def validate_username_format(cls, v):
        """Synchronous format validation"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v

    @validator('password')
    def validate_password_strength(cls, v):
        """Synchronous password strength validation"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Must contain number')
        return v

# Async validation (separate from Pydantic model)
async def validate_user_registration(data: dict) -> tuple[bool, dict]:
    """
    Async validation including database checks

    Returns:
        (is_valid, errors_dict)
    """
    errors = {}

    # Check username availability
    if 'username' in data:
        available = await check_username_available(data['username'])
        if not available:
            errors['username'] = 'Username is already taken'

    # Check email availability
    if 'email' in data:
        available = await check_email_available(data['email'])
        if not available:
            errors['email'] = 'Email is already registered'

    is_valid = len(errors) == 0
    return is_valid, errors

# Usage example
async def register_user_example():
    """Complete async validation workflow"""

    # User input
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'SecurePass123'
    }

    try:
        # Step 1: Synchronous validation (Pydantic model)
        user = UserRegistrationAsync(**user_data)
        print("✅ Synchronous validation passed")

        # Step 2: Async validation (database checks)
        is_valid, errors = await validate_user_registration(user_data)

        if not is_valid:
            print("❌ Async validation failed:")
            for field, error in errors.items():
                print(f"  {field}: {error}")
            return None

        print("✅ Async validation passed")

        # Step 3: Create user in database
        print(f"✅ User {user.username} registered successfully")
        return user

    except ValueError as e:
        print(f"❌ Validation error: {e}")
        return None

# With FastAPI
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/api/register-async")
async def register_with_async_validation(user_data: UserRegistrationAsync):
    """
    Registration endpoint with async validation

    Performs both Pydantic validation (sync) and database checks (async)
    """
    # Pydantic validation happens automatically

    # Additional async validation
    is_valid, errors = await validate_user_registration(user_data.dict())

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=errors
        )

    # Create user
    # In production: await database.users.insert_one(user_data.dict())

    return {
        "success": True,
        "message": "User registered successfully",
        "username": user_data.username
    }

# Run async example
if __name__ == "__main__":
    asyncio.run(register_user_example())
```
