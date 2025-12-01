# Pydantic Forms: Python Validation with FastAPI

**Pydantic is a data validation library that uses Python type hints to validate data at runtime. It's the recommended validation solution for modern Python projects, especially with FastAPI.**

## Why Pydantic?

**Python Integration:**
- **Type hints** - Leverages Python's type system
- **Runtime validation** - Validates data at runtime
- **Automatic documentation** - FastAPI generates OpenAPI/Swagger docs
- **Data conversion** - Automatic type coercion

**Developer Experience:**
- **Clear error messages** - Detailed validation errors
- **IDE support** - Autocomplete and type checking
- **Composable** - Build complex models from simple ones
- **JSON Schema** - Automatic JSON schema generation

**When to Use:**
- ✅ FastAPI applications (primary use case)
- ✅ API request/response validation
- ✅ Configuration management
- ✅ Data pipelines and ETL
- ✅ Any Python project needing validation

---

## Installation

```bash
# Basic Pydantic
pip install pydantic

# With email validation
pip install 'pydantic[email]'

# FastAPI (includes Pydantic)
pip install fastapi

# Development server
pip install 'uvicorn[standard]'
```

---

## Basic Usage

### Simple Model

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    is_active: bool = True  # Default value
    bio: Optional[str] = None  # Optional field

# Create instance (validates automatically)
user = User(
    name="John Doe",
    email="john@example.com",
    age=30
)

print(user.name)  # "John Doe"
print(user.model_dump())  # Convert to dict
print(user.model_dump_json())  # Convert to JSON string

# Validation error
try:
    invalid_user = User(
        name="Jane",
        email="invalid-email",  # ❌ Invalid email
        age="thirty"  # ❌ Should be int
    )
except ValidationError as e:
    print(e.errors())
    # [
    #   {
    #     'loc': ('email',),
    #     'msg': 'value is not a valid email address',
    #     'type': 'value_error.email'
    #   },
    #   {
    #     'loc': ('age',),
    #     'msg': 'value is not a valid integer',
    #     'type': 'type_error.integer'
    #   }
    # ]
```

---

## Field Validation

### Field Constraints

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    # String constraints
    username: str = Field(
        ...,  # Required (no default)
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z0-9_]+$',  # Regex pattern
        description="Username (alphanumeric and underscore only)"
    )

    # Email validation
    email: EmailStr = Field(..., description="Valid email address")

    # Number constraints
    age: int = Field(
        ...,
        ge=18,  # Greater than or equal
        le=120,  # Less than or equal
        description="Age must be between 18 and 120"
    )

    # Float constraints
    height: float = Field(
        ...,
        gt=0.0,  # Greater than
        lt=3.0,  # Less than
        description="Height in meters"
    )

    # Optional with default
    is_active: bool = Field(default=True)

    # Optional (can be None)
    bio: Optional[str] = Field(
        default=None,
        max_length=500,
        description="User bio (max 500 characters)"
    )

    # List with constraints
    tags: list[str] = Field(
        default_factory=list,  # Default to empty list
        max_length=10,  # Max 10 tags
        description="User tags"
    )
```

**Field Parameters:**
- `...` - Required field (Ellipsis)
- `default=value` - Default value
- `default_factory=func` - Default from function (e.g., `list`, `dict`)
- `min_length`, `max_length` - String/list length
- `ge`, `le` - Greater/less than or equal (inclusive)
- `gt`, `lt` - Greater/less than (exclusive)
- `pattern` - Regex pattern for strings
- `description` - Field description (API docs)

---

### Custom Validators

```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Any

class PasswordModel(BaseModel):
    password: str
    confirm_password: str

    # Field validator (single field)
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain number')
        if not any(char in '!@#$%^&*' for char in v):
            raise ValueError('Password must contain special character')
        return v

    # Model validator (cross-field validation)
    @model_validator(mode='after')
    def validate_passwords_match(self) -> 'PasswordModel':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self


class UsernameModel(BaseModel):
    username: str

    # Validator with transformation
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        # Transform to lowercase
        v = v.lower().strip()
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
```

---

## FastAPI Integration

### Basic Form Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=18, le=120)

@app.post("/api/register")
async def register_user(user: UserRegistration):
    # Pydantic automatically validates request body
    # If validation fails, FastAPI returns 422 with error details

    # Process registration
    # user.username, user.email, etc. are all validated

    return {
        "message": "Registration successful",
        "username": user.username,
        "email": user.email
    }

# Automatic validation error response (422):
# {
#   "detail": [
#     {
#       "type": "string_too_short",
#       "loc": ["body", "username"],
#       "msg": "String should have at least 3 characters",
#       "input": "ab",
#       "ctx": {"min_length": 3}
#     }
#   ]
# }
```

---

### Login Form

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt

app = FastAPI()

class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

@app.post("/api/login")
async def login(credentials: LoginForm):
    # Validate credentials
    user = await get_user_by_email(credentials.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not bcrypt.verify(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate token
    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

---

### Complex Registration Form

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import date

app = FastAPI()

class Address(BaseModel):
    street: str = Field(..., min_length=5)
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2, max_length=2, pattern=r'^[A-Z]{2}$')
    zip_code: str = Field(..., pattern=r'^\d{5}$')
    country: str = Field(default='US')

class UserRegistration(BaseModel):
    # Personal info
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\d{10}$')

    # Account
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)
    confirm_password: str

    # Additional info
    date_of_birth: date
    address: Address  # Nested model

    # Optional
    bio: Optional[str] = Field(default=None, max_length=500)
    newsletter: bool = Field(default=False)

    # Validators
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.lower()
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain number')
        return v

    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: date) -> date:
        from datetime import date, timedelta
        min_age = date.today() - timedelta(days=365*18)
        if v > min_age:
            raise ValueError('Must be at least 18 years old')
        return v

    @model_validator(mode='after')
    def validate_passwords(self) -> 'UserRegistration':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

@app.post("/api/register")
async def register(user: UserRegistration):
    # All validation passed
    return {
        "message": "Registration successful",
        "username": user.username,
        "email": user.email
    }
```

---

## Advanced Patterns

### Enums and Choices

```python
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class AccountType(str, Enum):
    PERSONAL = "personal"
    BUSINESS = "business"

class User(BaseModel):
    username: str
    role: Role  # Must be one of the enum values
    account_type: AccountType

# Usage
user = User(
    username="john",
    role=Role.USER,  # or "user"
    account_type="personal"
)
```

---

### Union Types (Discriminated Unions)

```python
from pydantic import BaseModel, Field
from typing import Literal, Union

class PersonalAccount(BaseModel):
    account_type: Literal["personal"]
    first_name: str
    last_name: str

class BusinessAccount(BaseModel):
    account_type: Literal["business"]
    company_name: str
    tax_id: str
    contact_person: str

# Discriminated union
Account = Union[PersonalAccount, BusinessAccount]

class Registration(BaseModel):
    email: str
    account: Account  # Can be either PersonalAccount or BusinessAccount

# Pydantic uses "account_type" field to determine which model to use
```

---

### List and Dict Validation

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Dict

class Tag(BaseModel):
    id: int
    name: str

class Article(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=100)

    # List of primitive types
    keywords: list[str] = Field(default_factory=list, max_length=10)

    # List of models
    tags: list[Tag] = Field(default_factory=list, max_length=5)

    # List with constraints
    authors: list[str] = Field(..., min_length=1, max_length=3)

    # Dict validation
    metadata: Dict[str, str] = Field(default_factory=dict)

    # List of emails
    contributors: list[EmailStr] = Field(default_factory=list)
```

---

### Optional and Default Values

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    # Required field
    username: str

    # Optional (can be None)
    bio: Optional[str] = None

    # Optional with Field constraints
    website: Optional[str] = Field(default=None, max_length=200)

    # Default value
    is_active: bool = True

    # Default from function
    created_at: datetime = Field(default_factory=datetime.now)

    # Default empty list
    tags: list[str] = Field(default_factory=list)

    # Default empty dict
    settings: dict = Field(default_factory=dict)
```

---

## Async Validation

### Username Availability Check

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
import httpx

app = FastAPI()

class UsernameCheck(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)

    @field_validator('username')
    @classmethod
    def check_availability(cls, v: str) -> str:
        # Note: Pydantic validators are synchronous
        # For async checks, validate in the endpoint
        # This just does basic format validation
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

@app.post("/api/check-username")
async def check_username(data: UsernameCheck):
    # Async validation happens here
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/users/{data.username}")
        if response.status_code == 200:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )

    return {"available": True, "username": data.username}
```

---

## Error Handling

### Custom Error Messages

```python
from pydantic import BaseModel, Field, ValidationError, field_validator

class User(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Username must be 3-20 characters"
    )

    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Email must contain @ symbol (e.g., name@example.com)')
        if not v.endswith(('.com', '.org', '.net')):
            raise ValueError('Email must end with .com, .org, or .net')
        return v.lower()

# Handle validation errors
try:
    user = User(username='ab', email='invalid')
except ValidationError as e:
    for error in e.errors():
        print(f"Field: {error['loc']}")
        print(f"Error: {error['msg']}")
        print(f"Type: {error['type']}")
        print(f"Input: {error['input']}")
```

---

### FastAPI Error Response Customization

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Custom error response format
    errors = {}
    for error in exc.errors():
        field = error['loc'][-1]  # Get field name
        message = error['msg']

        # Custom message formatting
        if error['type'] == 'string_too_short':
            ctx = error.get('ctx', {})
            min_length = ctx.get('min_length', 0)
            message = f"Must be at least {min_length} characters long"
        elif error['type'] == 'value_error.email':
            message = "Please enter a valid email address"

        errors[field] = message

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors}
    )

# Response format:
# {
#   "errors": {
#     "username": "Must be at least 3 characters long",
#     "email": "Please enter a valid email address"
#   }
# }
```

---

## Common Validation Patterns

### Email Validation

```python
from pydantic import BaseModel, EmailStr, field_validator

class EmailForm(BaseModel):
    email: EmailStr  # Built-in email validation

    @field_validator('email')
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        return v.lower()

    # Or with specific domain
    @field_validator('email')
    @classmethod
    def company_email(cls, v: str) -> str:
        if not v.endswith('@company.com'):
            raise ValueError('Must be a company email')
        return v
```

---

### Phone Validation

```python
from pydantic import BaseModel, Field, field_validator
import re

class PhoneForm(BaseModel):
    phone: str = Field(..., pattern=r'^\d{10}$')

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Remove formatting
        digits = re.sub(r'\D', '', v)

        # US phone number (10 digits)
        if len(digits) != 10:
            raise ValueError('Phone number must be 10 digits')

        return digits
```

---

### Password Validation

```python
from pydantic import BaseModel, Field, field_validator

class PasswordForm(BaseModel):
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain number')
        if not any(char in '!@#$%^&*(),.?":{}|<>' for char in v):
            raise ValueError('Password must contain special character')
        return v
```

---

### Date Validation

```python
from pydantic import BaseModel, Field, field_validator
from datetime import date, timedelta

class DateRangeForm(BaseModel):
    start_date: date
    end_date: date

    @field_validator('start_date')
    @classmethod
    def start_date_not_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError('Start date cannot be in the past')
        return v

    @field_validator('end_date')
    @classmethod
    def validate_date_range(cls, v: date, info) -> date:
        # Access other fields via info.data
        start_date = info.data.get('start_date')
        if start_date and v < start_date:
            raise ValueError('End date must be after start date')
        return v
```

---

## Configuration and Settings

### Environment Configuration

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    database_pool_size: int = 10

    # API Keys
    api_key: str
    secret_key: str

    # Optional settings
    debug: bool = False
    log_level: str = "INFO"

    # Email
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str

    class Config:
        env_file = ".env"  # Load from .env file
        env_file_encoding = 'utf-8'

# Usage
settings = Settings()  # Loads from environment variables or .env
print(settings.database_url)
```

---

## Best Practices

1. **Use EmailStr for emails**
   ```python
   from pydantic import EmailStr
   email: EmailStr  # ✅ Validates email format
   ```

2. **Use Field for constraints and documentation**
   ```python
   username: str = Field(..., min_length=3, max_length=20, description="Username")
   ```

3. **Use field_validator for complex validation**
   ```python
   @field_validator('password')
   @classmethod
   def validate_password(cls, v: str) -> str:
       # Custom validation logic
       return v
   ```

4. **Use model_validator for cross-field validation**
   ```python
   @model_validator(mode='after')
   def validate_passwords_match(self) -> 'PasswordModel':
       if self.password != self.confirm_password:
           raise ValueError('Passwords do not match')
       return self
   ```

5. **Use enums for choices**
   ```python
   from enum import Enum
   class Role(str, Enum):
       USER = "user"
       ADMIN = "admin"
   ```

6. **Nested models for complex data**
   ```python
   class Address(BaseModel):
       street: str
       city: str

   class User(BaseModel):
       name: str
       address: Address  # Nested model
   ```

7. **Custom error messages**
   ```python
   username: str = Field(..., min_length=3, max_length=20)

   @field_validator('username')
   @classmethod
   def validate_username(cls, v: str) -> str:
       if not v.isalnum():
           raise ValueError('Username must be alphanumeric (letters and numbers only)')
       return v
   ```

---

## Resources

**Official Documentation:**
- Pydantic: https://docs.pydantic.dev/
- FastAPI: https://fastapi.tiangolo.com/

**Validation:**
- Field Types: https://docs.pydantic.dev/latest/concepts/fields/
- Validators: https://docs.pydantic.dev/latest/concepts/validators/
- Custom Types: https://docs.pydantic.dev/latest/concepts/types/

**Integration:**
- FastAPI with Pydantic: https://fastapi.tiangolo.com/tutorial/body/
- Settings Management: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

---

## Next Steps

- WTForms for Flask/Django → `wtforms.md`
- See working examples → `examples/`
- Validation concepts → `../validation-concepts.md`
