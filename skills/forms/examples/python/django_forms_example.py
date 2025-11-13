"""
Django Forms Example

Demonstrates:
- Django Form classes
- ModelForm for database models
- Custom validators
- Clean methods
- Form rendering in templates
"""

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import User
import re

# Custom Validators
def validate_username_available(value):
    """Check if username is available"""
    if User.objects.filter(username=value).exists():
        raise ValidationError(
            'This username is already taken',
            code='username_taken'
        )

def validate_strong_password(value):
    """Validate password strength"""
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long')

    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter')

    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter')

    if not re.search(r'[0-9]', value):
        raise ValidationError('Password must contain at least one number')

def validate_age(value):
    """Validate user age"""
    if value < 13:
        raise ValidationError('You must be at least 13 years old')
    if value > 120:
        raise ValidationError('Please enter a valid age')

# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your full name',
            'class': 'form-control',
            'aria-label': 'Full name'
        }),
        error_messages={
            'required': 'Please enter your name',
            'min_length': 'Name must be at least 2 characters',
            'max_length': 'Name must be less than 100 characters'
        }
    )

    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message='Please enter a valid email address')],
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'form-control',
            'aria-label': 'Email address'
        })
    )

    subject = forms.CharField(
        max_length=200,
        min_length=5,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Subject of your inquiry',
            'class': 'form-control'
        })
    )

    message = forms.CharField(
        max_length=2000,
        min_length=20,
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Your message...',
            'class': 'form-control',
            'rows': 5
        })
    )

    category = forms.ChoiceField(
        choices=[
            ('', 'Select a category'),
            ('sales', 'Sales Inquiry'),
            ('support', 'Technical Support'),
            ('billing', 'Billing Question'),
            ('other', 'Other'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    newsletter = forms.BooleanField(
        required=False,
        initial=False,
        label='Subscribe to newsletter'
    )

    def clean_message(self):
        """Custom cleaning for message field"""
        message = self.cleaned_data.get('message')

        if message:
            # Remove excessive whitespace
            message = ' '.join(message.split())

            # Check for spam patterns (simple example)
            spam_words = ['viagra', 'casino', 'lottery']
            if any(word in message.lower() for word in spam_words):
                raise ValidationError('Your message appears to contain spam content')

        return message

# Registration Form
class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9_-]+$',
                message='Username can only contain letters, numbers, underscores, and hyphens'
            ),
            validate_username_available
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username',
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'form-control'
        })
    )

    password = forms.CharField(
        max_length=100,
        min_length=8,
        required=True,
        validators=[validate_strong_password],
        widget=forms.PasswordInput(attrs={
            'placeholder': 'At least 8 characters',
            'class': 'form-control'
        })
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control'
        })
    )

    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    age = forms.IntegerField(
        required=True,
        validators=[validate_age],
        widget=forms.NumberInput(attrs={
            'min': 13,
            'max': 120,
            'class': 'form-control'
        })
    )

    terms = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'You must accept the terms and conditions to register'
        }
    )

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match')

        return cleaned_data

    def clean_email(self):
        """Check if email is already registered"""
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')

        return email

# Views example
from django.shortcuts import render, redirect
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            messages.success(request, 'Account created successfully!')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
```
