"""
Basic FastAPI Form Handling Example

Demonstrates:
- FastAPI with Pydantic validation
- User registration endpoint
- Contact form endpoint
- Login endpoint
- Custom error responses
- Email validation
- Password validation
- Cross-field validation

Installation:
    pip install fastapi uvicorn 'pydantic[email]'

Run:
    uvicorn basic_form:app --reload

Then visit: http://localhost:8000/docs for Swagger UI
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import date, datetime

app = FastAPI(
    title="Form API",
    description="FastAPI form handling with Pydantic validation",
    version="1.0.0"
)


# ============================================================================
# 1. Contact Form
# ============================================================================

class ContactForm(BaseModel):
    """Contact form submission"""

    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Valid email address")
    subject: str = Field(..., min_length=5, max_length=200, description="Email subject")
    message: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Message content (20-2000 characters)"
    )
    newsletter: bool = Field(default=False, description="Subscribe to newsletter")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name doesn't contain special characters"""
        v = v.strip()
        if not all(char.isalpha() or char.isspace() for char in v):
            raise ValueError('Name can only contain letters and spaces')
        return v

    @field_validator('email')
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        """Convert email to lowercase"""
        return v.lower()


@app.post("/api/contact", status_code=status.HTTP_200_OK)
async def submit_contact_form(form_data: ContactForm):
    """
    Submit a contact form

    Validation:
    - Name: 2-100 characters, letters and spaces only
    - Email: Valid email format
    - Subject: 5-200 characters
    - Message: 20-2000 characters
    """

    # Simulate processing (e.g., send email, save to database)
    print(f"Contact form submission from {form_data.name} ({form_data.email})")
    print(f"Subject: {form_data.subject}")
    print(f"Message: {form_data.message}")
    print(f"Newsletter subscription: {form_data.newsletter}")

    return {
        "message": "Thank you for contacting us! We'll get back to you within 24 hours.",
        "email": form_data.email,
        "newsletter_subscribed": form_data.newsletter
    }


# ============================================================================
# 2. User Registration
# ============================================================================

class UserRegistration(BaseModel):
    """User registration form"""

    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="Username (3-20 characters, alphanumeric and underscore only)"
    )
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password (min 8 characters)")
    confirm_password: str = Field(..., description="Password confirmation")
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    date_of_birth: date = Field(..., description="Date of birth (YYYY-MM-DD)")
    terms_accepted: bool = Field(..., description="Must accept terms and conditions")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Username validation and transformation"""
        v = v.lower()  # Convert to lowercase

        # Check reserved usernames
        reserved = ['admin', 'root', 'administrator', 'system', 'user']
        if v in reserved:
            raise ValueError('Username is reserved')

        return v

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Password strength validation"""
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')

        if not any(char in '!@#$%^&*(),.?":{}|<>' for char in v):
            raise ValueError('Password must contain at least one special character')

        return v

    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: date) -> date:
        """Ensure user is at least 18 years old"""
        from datetime import timedelta
        min_age_date = date.today() - timedelta(days=365 * 18)

        if v > min_age_date:
            raise ValueError('You must be at least 18 years old to register')

        return v

    @model_validator(mode='after')
    def validate_passwords_match(self) -> 'UserRegistration':
        """Ensure password and confirm_password match"""
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

    @model_validator(mode='after')
    def validate_terms(self) -> 'UserRegistration':
        """Ensure terms are accepted"""
        if not self.terms_accepted:
            raise ValueError('You must accept the terms and conditions')
        return self


@app.post("/api/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegistration):
    """
    Register a new user

    Validation:
    - Username: 3-20 characters, alphanumeric and underscore only, not reserved
    - Email: Valid email format
    - Password: Min 8 characters, must contain uppercase, lowercase, number, and special character
    - Passwords must match
    - Age: Must be 18 or older
    - Terms: Must be accepted
    """

    # Simulate user creation (in real app: hash password, save to database)
    print(f"Registering user: {user_data.username}")
    print(f"Email: {user_data.email}")
    print(f"Name: {user_data.first_name} {user_data.last_name}")
    print(f"Date of birth: {user_data.date_of_birth}")

    return {
        "message": "Registration successful!",
        "username": user_data.username,
        "email": user_data.email,
        "created_at": datetime.now().isoformat()
    }


# ============================================================================
# 3. Login Form
# ============================================================================

class LoginForm(BaseModel):
    """User login form"""

    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Password")
    remember_me: bool = Field(default=False, description="Remember me")

    @field_validator('email')
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        return v.lower()


@app.post("/api/login")
async def login(credentials: LoginForm):
    """
    User login endpoint

    In a real application, you would:
    1. Query database for user by email
    2. Verify password hash matches
    3. Generate and return JWT token
    """

    # Simulate authentication (in real app: verify against database)
    # This is just an example - NEVER hardcode credentials!
    if credentials.email == "test@example.com" and credentials.password == "Password123!":
        return {
            "message": "Login successful",
            "token": "example_jwt_token_here",
            "token_type": "bearer",
            "remember_me": credentials.remember_me
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )


# ============================================================================
# 4. Custom Error Handling
# ============================================================================

from fastapi.exceptions import RequestValidationError
from fastapi import Request


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom validation error response format

    Converts Pydantic validation errors to user-friendly format:
    {
        "errors": {
            "field_name": "Error message"
        }
    }
    """
    errors = {}

    for error in exc.errors():
        field = error['loc'][-1]  # Get field name
        message = error['msg']

        # Customize error messages based on error type
        if error['type'] == 'string_too_short':
            ctx = error.get('ctx', {})
            min_length = ctx.get('min_length', 0)
            message = f"Must be at least {min_length} characters long"

        elif error['type'] == 'string_too_long':
            ctx = error.get('ctx', {})
            max_length = ctx.get('max_length', 0)
            message = f"Must be less than {max_length} characters long"

        elif error['type'] == 'value_error.email':
            message = "Please enter a valid email address"

        elif error['type'] == 'value_error':
            # Custom validation error messages (from validators)
            message = str(error.get('ctx', {}).get('error', message))

        errors[field] = message

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation failed",
            "errors": errors
        }
    )


# ============================================================================
# 5. Health Check Endpoint
# ============================================================================

@app.get("/")
async def root():
    """API health check and info"""
    return {
        "name": "Form API",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "contact": "/api/contact",
            "register": "/api/register",
            "login": "/api/login",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


# ============================================================================
# Example Usage (Client Side)
# ============================================================================

"""
# Example using httpx or requests

import httpx

# Contact form submission
contact_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Question about your service",
    "message": "I would like to know more about your premium plan features.",
    "newsletter": True
}

response = httpx.post("http://localhost:8000/api/contact", json=contact_data)
print(response.json())

# User registration
registration_data = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "terms_accepted": True
}

response = httpx.post("http://localhost:8000/api/register", json=registration_data)
print(response.json())

# Login
login_data = {
    "email": "test@example.com",
    "password": "Password123!",
    "remember_me": True
}

response = httpx.post("http://localhost:8000/api/login", json=login_data)
print(response.json())
"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
