"""
Comprehensive Pydantic Validation Examples

Demonstrates:
- Email validation
- Phone number validation
- Password strength validation
- Date validation
- Credit card validation (Luhn algorithm)
- Cross-field validation
- Nested models
- Custom validators
- Enums and choices
- Conditional validation

Installation:
    pip install 'pydantic[email]'
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional, Literal
from datetime import date, datetime
from enum import Enum
import re


# ============================================================================
# 1. Email Validation
# ============================================================================

class EmailValidationExample(BaseModel):
    """Email validation with transformation"""

    email: EmailStr = Field(..., description="Valid email address")
    confirm_email: EmailStr = Field(..., description="Email confirmation")

    @field_validator('email', 'confirm_email')
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        """Convert email to lowercase"""
        return v.lower()

    @model_validator(mode='after')
    def emails_match(self) -> 'EmailValidationExample':
        """Ensure emails match"""
        if self.email != self.confirm_email:
            raise ValueError('Email addresses do not match')
        return self


# Example usage
try:
    email_form = EmailValidationExample(
        email="John@Example.com",
        confirm_email="john@example.com"
    )
    print(f"Valid emails: {email_form.email}")
except ValueError as e:
    print(f"Validation error: {e}")


# ============================================================================
# 2. Phone Number Validation
# ============================================================================

class PhoneValidation(BaseModel):
    """Phone number validation (US format)"""

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Phone number (US format)"
    )

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate and format US phone number"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', v)

        # US phone number: 10 digits
        if len(digits) != 10:
            raise ValueError('Phone number must be 10 digits')

        # Optional: Format as (555) 123-4567
        formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

        return formatted


# Example usage
phone = PhoneValidation(phone="555-123-4567")
print(f"Formatted phone: {phone.phone}")  # (555) 123-4567


# ============================================================================
# 3. Password Strength Validation
# ============================================================================

class PasswordStrengthValidation(BaseModel):
    """Strong password validation"""

    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Enforce strong password requirements"""
        errors = []

        if not any(char.islower() for char in v):
            errors.append('at least one lowercase letter')

        if not any(char.isupper() for char in v):
            errors.append('at least one uppercase letter')

        if not any(char.isdigit() for char in v):
            errors.append('at least one number')

        if not any(char in '!@#$%^&*(),.?":{}|<>' for char in v):
            errors.append('at least one special character')

        if errors:
            raise ValueError(f"Password must contain {', '.join(errors)}")

        return v

    @model_validator(mode='after')
    def passwords_match(self) -> 'PasswordStrengthValidation':
        """Ensure passwords match"""
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self


# Example usage
password_form = PasswordStrengthValidation(
    password="SecurePass123!",
    confirm_password="SecurePass123!"
)
print("Password is valid and strong")


# ============================================================================
# 4. Date Validation
# ============================================================================

class DateValidation(BaseModel):
    """Date validation with age check"""

    date_of_birth: date = Field(..., description="Date of birth")
    start_date: date = Field(..., description="Start date")
    end_date: date = Field(..., description="End date")

    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: date) -> date:
        """Ensure user is at least 18 years old"""
        from datetime import timedelta
        today = date.today()
        min_age_date = today - timedelta(days=365 * 18)

        if v > min_age_date:
            raise ValueError('Must be at least 18 years old')

        # Not in the future
        if v > today:
            raise ValueError('Date of birth cannot be in the future')

        return v

    @field_validator('start_date')
    @classmethod
    def start_date_not_past(cls, v: date) -> date:
        """Start date cannot be in the past"""
        if v < date.today():
            raise ValueError('Start date cannot be in the past')
        return v

    @model_validator(mode='after')
    def validate_date_range(self) -> 'DateValidation':
        """Ensure end_date is after start_date"""
        if self.end_date <= self.start_date:
            raise ValueError('End date must be after start date')
        return self


# Example usage
date_form = DateValidation(
    date_of_birth=date(1990, 1, 1),
    start_date=date.today(),
    end_date=date(2025, 12, 31)
)
print("Dates are valid")


# ============================================================================
# 5. Credit Card Validation (Luhn Algorithm)
# ============================================================================

def luhn_checksum(card_number: str) -> bool:
    """Validate credit card number using Luhn algorithm"""
    digits = [int(d) for d in card_number]
    checksum = 0

    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:  # Every second digit from right
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0


class CreditCardValidation(BaseModel):
    """Credit card validation"""

    card_number: str = Field(
        ...,
        min_length=13,
        max_length=19,
        description="Credit card number"
    )
    expiry: str = Field(..., pattern=r'^(0[1-9]|1[0-2])\/\d{2}$', description="Expiry (MM/YY)")
    cvv: str = Field(..., pattern=r'^\d{3,4}$', description="CVV (3-4 digits)")

    @field_validator('card_number')
    @classmethod
    def validate_card_number(cls, v: str) -> str:
        """Validate credit card using Luhn algorithm"""
        # Remove spaces and dashes
        v = re.sub(r'[\s-]', '', v)

        # Must be digits only
        if not v.isdigit():
            raise ValueError('Card number must contain only digits')

        # Check length (13-19 digits)
        if not (13 <= len(v) <= 19):
            raise ValueError('Card number must be 13-19 digits')

        # Luhn algorithm check
        if not luhn_checksum(v):
            raise ValueError('Invalid credit card number')

        return v

    @field_validator('expiry')
    @classmethod
    def validate_expiry(cls, v: str) -> str:
        """Ensure card is not expired"""
        month, year = v.split('/')
        expiry_date = date(2000 + int(year), int(month), 1)

        if expiry_date < date.today().replace(day=1):
            raise ValueError('Card has expired')

        return v


# Example usage
credit_card = CreditCardValidation(
    card_number="4532015112830366",  # Valid test card number
    expiry="12/26",
    cvv="123"
)
print("Credit card is valid")


# ============================================================================
# 6. Nested Models (Address)
# ============================================================================

class Address(BaseModel):
    """Address model"""

    street: str = Field(..., min_length=5)
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2, max_length=2, pattern=r'^[A-Z]{2}$')
    zip_code: str = Field(..., pattern=r'^\d{5}$')
    country: str = Field(default='US')

    @field_validator('state')
    @classmethod
    def state_uppercase(cls, v: str) -> str:
        return v.upper()


class UserWithAddress(BaseModel):
    """User with nested address model"""

    name: str = Field(..., min_length=2)
    email: EmailStr
    address: Address  # Nested model


# Example usage
user = UserWithAddress(
    name="John Doe",
    email="john@example.com",
    address={
        "street": "123 Main Street",
        "city": "San Francisco",
        "state": "ca",  # Will be converted to uppercase
        "zip_code": "94102"
    }
)
print(f"User address: {user.address.street}, {user.address.city}, {user.address.state}")


# ============================================================================
# 7. Enums and Choices
# ============================================================================

class AccountType(str, Enum):
    """Account type choices"""
    PERSONAL = "personal"
    BUSINESS = "business"


class Role(str, Enum):
    """User role choices"""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserWithChoices(BaseModel):
    """User with enum choices"""

    username: str
    account_type: AccountType = Field(..., description="Account type")
    role: Role = Field(default=Role.USER, description="User role")


# Example usage
user_choices = UserWithChoices(
    username="johndoe",
    account_type=AccountType.PERSONAL,
    role="admin"  # Can use string or enum value
)
print(f"Account type: {user_choices.account_type.value}")


# ============================================================================
# 8. Conditional Validation (Discriminated Union)
# ============================================================================

class PersonalAccount(BaseModel):
    """Personal account type"""

    account_type: Literal["personal"]
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)


class BusinessAccount(BaseModel):
    """Business account type"""

    account_type: Literal["business"]
    company_name: str = Field(..., min_length=2)
    tax_id: str = Field(..., pattern=r'^\d{9}$')
    contact_person: str = Field(..., min_length=2)


from typing import Union

Account = Union[PersonalAccount, BusinessAccount]


class AccountRegistration(BaseModel):
    """Account registration with discriminated union"""

    email: EmailStr
    account: Account  # Can be either PersonalAccount or BusinessAccount


# Example usage - Personal account
personal_registration = AccountRegistration(
    email="john@example.com",
    account={
        "account_type": "personal",
        "first_name": "John",
        "last_name": "Doe"
    }
)
print(f"Personal account: {personal_registration.account.first_name}")

# Example usage - Business account
business_registration = AccountRegistration(
    email="contact@company.com",
    account={
        "account_type": "business",
        "company_name": "Acme Corp",
        "tax_id": "123456789",
        "contact_person": "Jane Smith"
    }
)
print(f"Business account: {business_registration.account.company_name}")


# ============================================================================
# 9. List and Dict Validation
# ============================================================================

class ArticleSubmission(BaseModel):
    """Article with tags and metadata"""

    title: str = Field(..., min_length=10, max_length=200)
    content: str = Field(..., min_length=100)

    # List validation
    tags: list[str] = Field(..., min_length=1, max_length=5, description="1-5 tags")
    authors: list[EmailStr] = Field(..., min_length=1, description="At least one author")

    # Dict validation
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Ensure tags are lowercase and unique"""
        return list(set(tag.lower() for tag in v))


# Example usage
article = ArticleSubmission(
    title="Introduction to Pydantic Validation",
    content="..." * 50,  # Long content
    tags=["Python", "Pydantic", "validation", "Python"],  # Duplicate will be removed
    authors=["author1@example.com", "author2@example.com"],
    metadata={"category": "tutorial", "difficulty": "intermediate"}
)
print(f"Unique tags: {article.tags}")


# ============================================================================
# 10. Complete Example: User Profile Update
# ============================================================================

class UserProfileUpdate(BaseModel):
    """Complete user profile update with all validation patterns"""

    # Basic fields
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    bio: Optional[str] = Field(None, max_length=500)

    # Phone validation
    phone: Optional[str] = None

    # Address (nested model)
    address: Optional[Address] = None

    # Preferences
    newsletter: bool = Field(default=True)
    notifications: bool = Field(default=True)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """Validate username if provided"""
        if v is not None:
            v = v.lower()
            if not v.replace('_', '').isalnum():
                raise ValueError('Username can only contain letters, numbers, and underscores')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number if provided"""
        if v is not None:
            digits = re.sub(r'\D', '', v)
            if len(digits) != 10:
                raise ValueError('Phone must be 10 digits')
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return v


# Example usage
profile_update = UserProfileUpdate(
    username="johndoe",
    email="john@example.com",
    bio="Software developer passionate about Python",
    phone="5551234567",
    address={
        "street": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94102"
    }
)
print(f"Profile updated: {profile_update.model_dump_json(indent=2)}")


if __name__ == "__main__":
    print("\n=== All validation examples completed successfully! ===")
