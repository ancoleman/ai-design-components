"""
Flask-WTF Form Example

Demonstrates:
- Flask-WTF form classes
- WTForms validators
- CSRF protection
- File upload
- Custom validators
"""

from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, EmailField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Custom validators
def validate_username(form, field):
    """Check if username is available (mock)"""
    taken_usernames = ['admin', 'user', 'test']
    if field.data.lower() in taken_usernames:
        raise ValidationError('This username is already taken')

def validate_strong_password(form, field):
    """Validate password strength"""
    password = field.data

    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')

    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter')

    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one number')

    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?]', password):
        raise ValidationError('Password must contain at least one special character')

# Forms
class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(message='Name is required'),
            Length(min=2, max=100, message='Name must be between 2 and 100 characters')
        ]
    )

    email = EmailField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address')
        ]
    )

    subject = StringField(
        'Subject',
        validators=[
            DataRequired(message='Subject is required'),
            Length(min=5, max=200)
        ]
    )

    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Message is required'),
            Length(min=20, max=2000, message='Message must be between 20 and 2000 characters')
        ]
    )

    newsletter = BooleanField('Subscribe to Newsletter')

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp(r'^[a-zA-Z0-9_-]+$', message='Username can only contain letters, numbers, underscores, and hyphens'),
            validate_username  # Custom validator
        ]
    )

    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=100),
            validate_strong_password  # Custom validator
        ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(min=1, max=50)
        ]
    )

    country = SelectField(
        'Country',
        choices=[
            ('', 'Select a country'),
            ('US', 'United States'),
            ('UK', 'United Kingdom'),
            ('CA', 'Canada'),
            ('DE', 'Germany'),
            ('FR', 'France'),
        ],
        validators=[DataRequired()]
    )

    terms = BooleanField(
        'I accept the Terms and Conditions',
        validators=[
            DataRequired(message='You must accept the terms and conditions')
        ]
    )

class ImageUploadForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    image = FileField(
        'Image',
        validators=[
            FileRequired(message='Please select an image'),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='Images only (JPG, PNG, GIF)')
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[Length(max=500)]
    )

# Routes
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Process form
        flash(f'Thank you, {form.name.data}! We will contact you at {form.email.data}', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create user
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = ImageUploadForm()

    if form.validate_on_submit():
        # Save file
        file = form.image.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash(f'Image "{form.title.data}" uploaded successfully!', 'success')
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

# Template example for contact.html
CONTACT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Contact Form</title>
</head>
<body>
    <h1>Contact Us</h1>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <form method="POST" novalidate>
        {{ form.hidden_tag() }}

        <div>
            {{ form.name.label }}
            {{ form.name(class_="form-control") }}
            {% if form.name.errors %}
                <span class="error">{{ form.name.errors[0] }}</span>
            {% endif %}
        </div>

        <div>
            {{ form.email.label }}
            {{ form.email(class_="form-control", type="email") }}
            {% if form.email.errors %}
                <span class="error">{{ form.email.errors[0] }}</span>
            {% endif %}
        </div>

        <div>
            {{ form.subject.label }}
            {{ form.subject(class_="form-control") }}
            {% if form.subject.errors %}
                <span class="error">{{ form.subject.errors[0] }}</span>
            {% endif %}
        </div>

        <div>
            {{ form.message.label }}
            {{ form.message(class_="form-control", rows="5") }}
            {% if form.message.errors %}
                <span class="error">{{ form.message.errors[0] }}</span>
            {% endif %}
        </div>

        <div>
            {{ form.newsletter() }} {{ form.newsletter.label }}
        </div>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''
```
