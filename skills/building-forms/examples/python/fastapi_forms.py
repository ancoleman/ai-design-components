"""
FastAPI Form Handling Example

Demonstrates:
- FastAPI form endpoints
- Pydantic validation
- File upload handling
- Async validation
- Error responses
"""

from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
import re

app = FastAPI()

# Pydantic models for validation
class ContactForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Valid email address")
    subject: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=20, max_length=2000)
    newsletter: bool = Field(default=False)

    @validator('name')
    def validate_name(cls, v):
        if not re.match(r"^[a-zA-ZÀ-ÿ\s'-]+$", v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v.strip()

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=13, le=120)
    terms: bool = Field(..., description="Must accept terms")

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')

        # Check reserved words
        reserved = ['admin', 'administrator', 'root', 'system']
        if v.lower() in reserved:
            raise ValueError('This username is reserved')

        return v

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?]', v):
            raise ValueError('Password must contain at least one special character')

        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('terms')
    def terms_accepted(cls, v):
        if not v:
            raise ValueError('You must accept the terms and conditions')
        return v

# POST endpoints
@app.post("/api/contact")
async def submit_contact_form(form: ContactForm):
    """
    Contact form submission endpoint

    Returns:
        200: Form submitted successfully
        422: Validation errors
    """
    try:
        # Process form data
        # In production: save to database, send email, etc.

        return {
            "success": True,
            "message": "Thank you for contacting us!",
            "data": form.dict()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error processing form")

@app.post("/api/register")
async def register_user(user: UserRegistration):
    """
    User registration endpoint with comprehensive validation

    Returns:
        201: User created successfully
        400: Username already taken
        422: Validation errors
    """
    # Check username availability (mock)
    taken_usernames = ['admin', 'test', 'demo']
    if user.username.lower() in taken_usernames:
        raise HTTPException(
            status_code=400,
            detail="Username is already taken"
        )

    # In production: create user in database, send welcome email, etc.

    return {
        "success": True,
        "message": "Account created successfully",
        "user_id": "generated-uuid",
        "username": user.username
    }

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None)
):
    """
    File upload endpoint with validation

    Accepts:
        - Images (JPG, PNG, GIF)
        - Max size: 5MB
        - Required metadata: title
    """
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )

    # Validate file size (5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 5MB"
        )

    # In production: save file to storage, process image, create thumbnail, etc.

    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type
    }

# Async validation endpoints
@app.get("/api/check-username/{username}")
async def check_username_availability(username: str):
    """
    Check if username is available (for async validation)

    Returns:
        200: {"available": true/false}
    """
    # Simulate database check
    taken_usernames = ['admin', 'user', 'test', 'demo', 'support']
    available = username.lower() not in taken_usernames

    return {"available": available}

@app.get("/api/check-email/{email}")
async def check_email_availability(email: str):
    """
    Check if email is available

    Returns:
        200: {"available": true/false}
    """
    # Simulate database check
    taken_emails = ['admin@example.com', 'test@example.com']
    available = email.lower() not in taken_emails

    return {"available": available}

# Run with: uvicorn fastapi_forms:app --reload
```
