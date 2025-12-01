# WTForms: Flask and Django Form Handling

**WTForms is a flexible forms validation and rendering library for Python. It's the traditional choice for Flask applications and works well with Django alongside Django Forms.**

## Why WTForms?

**Framework Integration:**
- **Flask-WTF** - Seamless Flask integration with CSRF protection
- **Django compatibility** - Works alongside Django Forms
- **Template rendering** - Generates HTML form fields
- **Validation** - Comprehensive built-in validators

**Features:**
- **CSRF protection** - Built-in with Flask-WTF
- **File uploads** - Easy file handling
- **Localization** - I18n support
- **Custom validators** - Easy to extend

**When to Use:**
- ✅ Flask applications (primary use case)
- ✅ Server-rendered forms (Jinja2, Django templates)
- ✅ Traditional web applications
- ✅ Need CSRF protection out-of-the-box

**When to Use Pydantic Instead:**
- ✅ FastAPI applications
- ✅ API-first applications (JSON requests)
- ✅ Want modern Python type hints

---

## Installation

```bash
# Basic WTForms
pip install wtforms

# Flask integration with CSRF protection
pip install flask-wtf

# Email validation
pip install email-validator

# For Flask applications (recommended)
pip install flask flask-wtf email-validator
```

---

## Flask Integration

### Basic Flask Form

```python
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for CSRF

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Form is valid
        email = form.email.data
        password = form.password.data

        # Process login
        # ...

        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))

    # Render form (GET request or validation failed)
    return render_template('login.html', form=form)
```

**Template (login.html):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>

    <!-- Flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <form method="POST" action="">
        <!-- CSRF token (automatically included with Flask-WTF) -->
        {{ form.hidden_tag() }}

        <div>
            {{ form.email.label }}
            {{ form.email(size=32) }}
            {% if form.email.errors %}
                {% for error in form.email.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>

        <div>
            {{ form.password.label }}
            {{ form.password(size=32) }}
            {% if form.password.errors %}
                {% for error in form.password.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>

        <div>
            {{ form.submit() }}
        </div>
    </form>
</body>
</html>
```

---

## Field Types

### Text Fields

```python
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length

class TextFieldsForm(FlaskForm):
    # Single-line text
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])

    # Multi-line text
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])

    # Password (masked)
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])

    # Email
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
```

---

### Numeric Fields

```python
from wtforms import IntegerField, DecimalField
from wtforms.validators import NumberRange

class NumericFieldsForm(FlaskForm):
    # Integer
    age = IntegerField('Age', validators=[
        DataRequired(),
        NumberRange(min=18, max=120, message='Age must be between 18 and 120')
    ])

    # Decimal/Float
    price = DecimalField('Price', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ])
```

---

### Selection Fields

```python
from wtforms import SelectField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired

class SelectionForm(FlaskForm):
    # Dropdown select
    country = SelectField('Country', choices=[
        ('us', 'United States'),
        ('ca', 'Canada'),
        ('mx', 'Mexico')
    ], validators=[DataRequired()])

    # Radio buttons
    shipping = RadioField('Shipping Method', choices=[
        ('standard', 'Standard (5-7 days)'),
        ('express', 'Express (2-3 days)')
    ], validators=[DataRequired()])

    # Multiple select
    interests = SelectMultipleField('Interests', choices=[
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('art', 'Art'),
        ('technology', 'Technology')
    ])
```

---

### Boolean and Choice Fields

```python
from wtforms import BooleanField
from wtforms.validators import DataRequired

class BooleanForm(FlaskForm):
    # Checkbox
    remember_me = BooleanField('Remember Me')

    # Required checkbox (e.g., terms of service)
    terms = BooleanField('I accept the terms', validators=[
        DataRequired(message='You must accept the terms')
    ])
```

---

### Date and Time Fields

```python
from wtforms import DateField, DateTimeField
from wtforms.validators import DataRequired

class DateTimeForm(FlaskForm):
    # Date field (HTML5 date input)
    birth_date = DateField('Date of Birth', validators=[
        DataRequired()
    ], format='%Y-%m-%d')

    # DateTime field
    appointment = DateTimeField('Appointment', validators=[
        DataRequired()
    ], format='%Y-%m-%d %H:%M')
```

---

### File Upload

```python
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class FileUploadForm(FlaskForm):
    # Single file upload
    avatar = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])

    submit = SubmitField('Upload')

# Route handling file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = FileUploadForm()

    if form.validate_on_submit():
        file = form.avatar.data
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form)
```

---

## Validators

### Built-in Validators

```python
from wtforms.validators import (
    DataRequired,  # Field must have value
    Email,  # Valid email address
    Length,  # String length constraints
    NumberRange,  # Numeric range
    EqualTo,  # Must equal another field
    Regexp,  # Regex pattern
    URL,  # Valid URL
    Optional,  # Field is optional
    InputRequired,  # Field must be present (but can be empty)
    ValidationError  # For custom validators
)

class ComprehensiveForm(FlaskForm):
    # Required field
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=20, message='Username must be 3-20 characters')
    ])

    # Email validation
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])

    # Regex pattern
    phone = StringField('Phone', validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message='Phone must be 10 digits')
    ])

    # Numeric range
    age = IntegerField('Age', validators=[
        DataRequired(),
        NumberRange(min=18, max=120)
    ])

    # Password confirmation
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    # URL validation
    website = StringField('Website', validators=[
        Optional(),  # Field is optional
        URL(message='Invalid URL')
    ])
```

---

### Custom Validators

```python
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    # Inline custom validator (method on form class)
    def validate_username(self, field):
        """Custom validator: Method name must be validate_<fieldname>"""
        if field.data.lower() in ['admin', 'root', 'administrator']:
            raise ValidationError('Username is reserved')

    def validate_password(self, field):
        """Password strength validation"""
        password = field.data

        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain uppercase letter')

        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain number')

        if not any(char in '!@#$%^&*' for char in password):
            raise ValidationError('Password must contain special character')

# Reusable custom validator function
def username_exists(form, field):
    """Check if username already exists in database"""
    from models import User  # Your User model

    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already taken')

class RegistrationFormWithReusable(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        username_exists  # Reusable validator
    ])
```

---

## Advanced Patterns

### Registration Form

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    terms = BooleanField('I accept the terms', validators=[
        DataRequired(message='You must accept the terms')
    ])

    submit = SubmitField('Register')

    # Custom validators
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

        if not field.data.replace('_', '').isalnum():
            raise ValidationError('Username must be alphanumeric')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_password(self, field):
        password = field.data

        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain uppercase letter')

        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain number')
```

---

### Profile Edit Form

```python
from flask_login import current_user

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])

    bio = TextAreaField('Bio', validators=[
        Length(max=500)
    ])

    submit = SubmitField('Update Profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, field):
        # Only check if username changed
        if field.data != self.original_username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError('Username already taken')

    def validate_email(self, field):
        # Only check if email changed
        if field.data != self.original_email:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError('Email already registered')

# Usage in route
@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(
        original_username=current_user.username,
        original_email=current_user.email
    )

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()

        flash('Profile updated!', 'success')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        # Pre-populate form with current values
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    return render_template('edit_profile.html', form=form)
```

---

### Dynamic Select Choices

```python
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class DynamicForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit')

# Route with dynamic choices
@app.route('/form', methods=['GET', 'POST'])
def dynamic_form():
    form = DynamicForm()

    # Set choices dynamically from database
    from models import Category
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        selected_category_id = form.category.data
        # Process form
        return redirect(url_for('success'))

    return render_template('form.html', form=form)
```

---

### Nested Forms (FieldList)

```python
from wtforms import Form, FieldList, FormField, StringField
from wtforms.validators import DataRequired

class AddressForm(Form):
    """Subform for address"""
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('ZIP', validators=[DataRequired()])

class ContactForm(FlaskForm):
    """Main form with nested address"""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    # Single nested form
    address = FormField(AddressForm)

    # Multiple addresses (dynamic list)
    # addresses = FieldList(FormField(AddressForm), min_entries=1)

    submit = SubmitField('Submit')

# Access nested data
if form.validate_on_submit():
    name = form.name.data
    street = form.address.street.data
    city = form.address.city.data
```

---

## CSRF Protection

### Flask-WTF CSRF

```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Enable CSRF protection globally
csrf = CSRFProtect(app)

# CSRF is automatically added to FlaskForm forms via form.hidden_tag()

# For AJAX requests, include CSRF token in headers
# <meta name="csrf-token" content="{{ csrf_token() }}">

# JavaScript:
# const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
# fetch('/api/endpoint', {
#     method: 'POST',
#     headers: {
#         'X-CSRFToken': csrfToken,
#         'Content-Type': 'application/json'
#     },
#     body: JSON.stringify(data)
# })
```

---

## Form Rendering (Templates)

### Manual Rendering (Full Control)

```html
<form method="POST" action="">
    {{ form.hidden_tag() }}

    <div class="field">
        {{ form.username.label }}
        {{ form.username(class="input", placeholder="Enter username") }}
        {% if form.username.errors %}
            <ul class="errors">
                {% for error in form.username.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>

    <div class="field">
        {{ form.email.label }}
        {{ form.email(class="input", type="email") }}
        {% if form.email.errors %}
            <ul class="errors">
                {% for error in form.email.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>

    {{ form.submit(class="button") }}
</form>
```

---

### Macro for Reusable Field Rendering

```html
<!-- macros.html -->
{% macro render_field(field) %}
    <div class="field {% if field.errors %}error{% endif %}">
        {{ field.label }}
        {{ field(**kwargs)|safe }}
        {% if field.errors %}
            <ul class="errors">
                {% for error in field.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
{% endmacro %}

<!-- form.html -->
{% from "macros.html" import render_field %}

<form method="POST" action="">
    {{ form.hidden_tag() }}
    {{ render_field(form.username) }}
    {{ render_field(form.email) }}
    {{ render_field(form.password) }}
    {{ form.submit(class="button") }}
</form>
```

---

## Django Integration

WTForms can work alongside Django Forms:

```python
from wtforms import Form, StringField, validators

class ContactForm(Form):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email', [validators.Email()])
    message = StringField('Message', [validators.Length(min=10)])

# In Django view
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.validate():
            # Process form
            return redirect('success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
```

**Note:** For Django, Django Forms is the more natural choice. Use WTForms only if you need specific WTForms features or want consistency with Flask apps.

---

## Best Practices

1. **Use Flask-WTF for Flask applications**
   ```python
   from flask_wtf import FlaskForm  # ✅ Includes CSRF protection
   ```

2. **Always include CSRF token**
   ```html
   {{ form.hidden_tag() }}  <!-- ✅ Includes CSRF token -->
   ```

3. **Validate on submit**
   ```python
   if form.validate_on_submit():  # ✅ POST request + valid
       # Process form
   ```

4. **Use custom error messages**
   ```python
   validators=[
       DataRequired(message='Field is required'),
       Email(message='Invalid email address')
   ]
   ```

5. **Pre-populate forms for editing**
   ```python
   if request.method == 'GET':
       form.username.data = current_user.username
   ```

6. **Use macros for consistent rendering**
   ```html
   {% from "macros.html" import render_field %}
   {{ render_field(form.username) }}
   ```

7. **Secure file uploads**
   ```python
   from werkzeug.utils import secure_filename
   filename = secure_filename(file.filename)
   ```

---

## Resources

**Official Documentation:**
- WTForms: https://wtforms.readthedocs.io/
- Flask-WTF: https://flask-wtf.readthedocs.io/

**Field Types:**
- https://wtforms.readthedocs.io/en/stable/fields/

**Validators:**
- https://wtforms.readthedocs.io/en/stable/validators/

**Flask Integration:**
- https://flask-wtf.readthedocs.io/en/stable/form/

---

## Next Steps

- Pydantic for FastAPI → `pydantic-forms.md`
- See working examples → `examples/`
- Validation concepts → `../validation-concepts.md`
