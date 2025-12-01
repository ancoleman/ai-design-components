# Flask Routing Patterns

## Table of Contents
- [Basic Route Configuration](#basic-route-configuration)
- [Blueprint Organization](#blueprint-organization)
- [Route Parameters & Validation](#route-parameters--validation)
- [Middleware & Route Guards](#middleware--route-guards)
- [RESTful API Routes](#restful-api-routes)
- [Error Handling](#error-handling)

## Basic Route Configuration

### Simple Routes

```python
from flask import Flask, render_template, request, jsonify
from typing import Dict, Any

app = Flask(__name__)

# Basic route
@app.route('/')
def home():
    """Home page route."""
    return render_template('index.html')

# Multiple HTTP methods
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form."""
    if request.method == 'POST':
        # Process form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Save to database or send email
        process_contact_form(name, email, message)

        return jsonify({'status': 'success', 'message': 'Thank you for contacting us!'})

    # GET request - show form
    return render_template('contact.html')

# Route with multiple paths
@app.route('/about')
@app.route('/about-us')
def about():
    """About page with multiple URL patterns."""
    return render_template('about.html')
```

### Dynamic Routes

```python
from flask import abort
from werkzeug.routing import BaseConverter
import re

# Simple dynamic route
@app.route('/user/<username>')
def user_profile(username: str):
    """User profile page."""
    user = get_user_by_username(username)
    if not user:
        abort(404)
    return render_template('profile.html', user=user)

# Route with type conversion
@app.route('/product/<int:product_id>')
def product_detail(product_id: int):
    """Product detail page with integer ID."""
    product = get_product(product_id)
    if not product:
        abort(404)
    return render_template('product.html', product=product)

# Multiple parameters
@app.route('/category/<category>/page/<int:page>')
def category_products(category: str, page: int = 1):
    """Category listing with pagination."""
    products = get_products_by_category(category, page=page, per_page=20)
    return render_template('category.html',
                         products=products,
                         category=category,
                         page=page)

# Custom converter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

# Use custom converter for slug pattern
@app.route('/article/<regex("[a-zA-Z0-9-]+"):slug>')
def article(slug: str):
    """Article with SEO-friendly slug."""
    article = get_article_by_slug(slug)
    if not article:
        abort(404)
    return render_template('article.html', article=article)
```

## Blueprint Organization

### Modular Application Structure

```python
# blueprints/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = authenticate_user(username, password)
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('main.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        # Registration logic
        user_data = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }

        if create_user(user_data):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')

    return render_template('auth/register.html')
```

```python
# blueprints/api.py
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from marshmallow import Schema, fields, ValidationError

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

# Schema for validation
class ProductSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    category = fields.Str(required=True)
    description = fields.Str()

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class ProductList(Resource):
    def get(self):
        """Get all products."""
        products = get_all_products()
        return products_schema.dump(products)

    def post(self):
        """Create new product."""
        try:
            data = product_schema.load(request.json)
            product = create_product(data)
            return product_schema.dump(product), 201
        except ValidationError as err:
            return {'errors': err.messages}, 400

class ProductDetail(Resource):
    def get(self, product_id):
        """Get single product."""
        product = get_product(product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        return product_schema.dump(product)

    def put(self, product_id):
        """Update product."""
        try:
            data = product_schema.load(request.json)
            product = update_product(product_id, data)
            if not product:
                return {'message': 'Product not found'}, 404
            return product_schema.dump(product)
        except ValidationError as err:
            return {'errors': err.messages}, 400

    def delete(self, product_id):
        """Delete product."""
        if delete_product(product_id):
            return {'message': 'Product deleted'}, 204
        return {'message': 'Product not found'}, 404

# Register resources
api.add_resource(ProductList, '/products')
api.add_resource(ProductDetail, '/products/<int:product_id>')
```

```python
# app.py - Main application
from flask import Flask
from blueprints.auth import auth_bp
from blueprints.api import api_bp
from blueprints.admin import admin_bp

def create_app(config_name='production'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # Main routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
```

## Route Parameters & Validation

### Request Validation

```python
from flask import request, jsonify
from functools import wraps
from marshmallow import Schema, fields, validate, ValidationError

# Validation decorator
def validate_json(schema: Schema):
    """Decorator to validate JSON request data."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = schema.load(request.json)
                return f(data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': err.messages
                }), 400
        return wrapper
    return decorator

# Request schemas
class SearchSchema(Schema):
    q = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str()
    min_price = fields.Float(validate=validate.Range(min=0))
    max_price = fields.Float(validate=validate.Range(min=0))
    sort = fields.Str(validate=validate.OneOf(['price', 'name', 'date']))
    page = fields.Int(validate=validate.Range(min=1), missing=1)
    per_page = fields.Int(validate=validate.Range(min=1, max=100), missing=20)

@app.route('/api/search')
def search():
    """Search endpoint with query parameter validation."""
    schema = SearchSchema()

    try:
        # Validate query parameters
        params = schema.load(request.args)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    # Perform search with validated parameters
    results = perform_search(
        query=params['q'],
        category=params.get('category'),
        min_price=params.get('min_price'),
        max_price=params.get('max_price'),
        sort_by=params.get('sort', 'name'),
        page=params['page'],
        per_page=params['per_page']
    )

    return jsonify({
        'results': results,
        'page': params['page'],
        'total': len(results)
    })
```

### URL Building

```python
from flask import url_for, redirect

@app.route('/old-product/<int:id>')
def old_product_url(id):
    """Redirect old URLs to new structure."""
    return redirect(url_for('product_detail', product_id=id), code=301)

@app.route('/generate-urls')
def generate_urls():
    """Example of URL generation."""
    urls = {
        'home': url_for('index', _external=True),
        'login': url_for('auth.login', _external=True),
        'product': url_for('product_detail', product_id=123, _external=True),
        'category': url_for('category_products',
                          category='electronics',
                          page=2,
                          _external=True),
        # With query parameters
        'search': url_for('search', q='laptop', category='electronics', _external=True)
    }

    return jsonify(urls)
```

## Middleware & Route Guards

### Authentication Middleware

```python
from functools import wraps
from flask import g, request, redirect, url_for, jsonify
from flask_login import current_user
import jwt

def login_required(f):
    """Decorator for routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator for role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))

            if not any(role in current_user.roles for role in roles):
                abort(403)  # Forbidden

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def api_key_required(f):
    """Decorator for API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return jsonify({'message': 'API key required'}), 401

        if not validate_api_key(api_key):
            return jsonify({'message': 'Invalid API key'}), 401

        return f(*args, **kwargs)
    return decorated_function

# JWT authentication for APIs
def jwt_required(f):
    """Decorator for JWT authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token required'}), 401

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.current_user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function

# Usage examples
@app.route('/admin')
@role_required('admin', 'moderator')
def admin_panel():
    """Admin panel - requires admin or moderator role."""
    return render_template('admin/dashboard.html')

@app.route('/api/protected')
@jwt_required
def protected_api():
    """Protected API endpoint."""
    return jsonify({
        'message': 'Access granted',
        'user_id': g.current_user_id
    })
```

### Request Hooks

```python
@app.before_request
def before_request():
    """Execute before each request."""
    # Log request
    app.logger.info(f'{request.method} {request.path} - {request.remote_addr}')

    # Check maintenance mode
    if app.config.get('MAINTENANCE_MODE') and request.path != '/maintenance':
        return redirect(url_for('maintenance'))

    # Set request start time for performance monitoring
    g.request_start_time = time.time()

@app.after_request
def after_request(response):
    """Execute after each request."""
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # Log response time
    if hasattr(g, 'request_start_time'):
        elapsed = time.time() - g.request_start_time
        app.logger.info(f'Request took {elapsed:.3f}s')

    return response

@app.teardown_request
def teardown_request(exception):
    """Clean up after request."""
    if exception:
        app.logger.error(f'Request exception: {exception}')

    # Close database connections
    if hasattr(g, 'db_conn'):
        g.db_conn.close()
```

## RESTful API Routes

### Resource-Based Routes

```python
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask import Blueprint

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Response fields
product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'category': fields.String,
    'created_at': fields.DateTime,
    'uri': fields.Url('api.product_detail', absolute=True)
}

# Request parser
product_parser = reqparse.RequestParser()
product_parser.add_argument('name', type=str, required=True, help='Name is required')
product_parser.add_argument('price', type=float, required=True, help='Price is required')
product_parser.add_argument('category', type=str, required=True)
product_parser.add_argument('description', type=str)

class ProductListResource(Resource):
    @marshal_with(product_fields)
    def get(self):
        """Get all products."""
        # Parse query parameters
        parser = reqparse.RequestParser()
        parser.add_argument('category', type=str, location='args')
        parser.add_argument('sort', type=str, choices=['price', 'name'], location='args')
        parser.add_argument('page', type=int, default=1, location='args')
        args = parser.parse_args()

        products = get_products(
            category=args['category'],
            sort=args['sort'],
            page=args['page']
        )
        return products

    @marshal_with(product_fields)
    def post(self):
        """Create new product."""
        args = product_parser.parse_args()
        product = create_product(**args)
        return product, 201

class ProductDetailResource(Resource):
    @marshal_with(product_fields)
    def get(self, product_id):
        """Get single product."""
        product = get_product(product_id)
        if not product:
            api.abort(404, message=f"Product {product_id} not found")
        return product

    @marshal_with(product_fields)
    def put(self, product_id):
        """Update product."""
        args = product_parser.parse_args()
        product = update_product(product_id, **args)
        if not product:
            api.abort(404, message=f"Product {product_id} not found")
        return product

    def delete(self, product_id):
        """Delete product."""
        if not delete_product(product_id):
            api.abort(404, message=f"Product {product_id} not found")
        return '', 204

# Nested resources
class ProductReviewsResource(Resource):
    def get(self, product_id):
        """Get reviews for a product."""
        reviews = get_product_reviews(product_id)
        return {'reviews': reviews}

    def post(self, product_id):
        """Add review to product."""
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, required=True, choices=[1,2,3,4,5])
        parser.add_argument('comment', type=str, required=True)
        args = parser.parse_args()

        review = add_product_review(product_id, **args)
        return review, 201

# Register resources
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductDetailResource, '/products/<int:product_id>')
api.add_resource(ProductReviewsResource, '/products/<int:product_id>/reviews')

app.register_blueprint(api_bp, url_prefix='/api/v1')
```

## Error Handling

### Custom Error Pages

```python
from flask import render_template, jsonify

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    if request.path.startswith('/api'):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors."""
    if request.path.startswith('/api'):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    # Log the error
    app.logger.error(f'Internal error: {error}')

    if request.path.startswith('/api'):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    return render_template('errors/500.html'), 500

# Custom exception classes
class APIException(Exception):
    """Base API exception."""
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class ValidationError(APIException):
    """Validation error exception."""
    status_code = 400

class AuthenticationError(APIException):
    """Authentication error exception."""
    status_code = 401

class AuthorizationError(APIException):
    """Authorization error exception."""
    status_code = 403

@app.errorhandler(APIException)
def handle_api_exception(error):
    """Handle custom API exceptions."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/search')
@limiter.limit("10 per minute")
def search_api():
    """Rate-limited search endpoint."""
    query = request.args.get('q')
    results = perform_search(query)
    return jsonify(results)

@app.errorhandler(429)
def rate_limit_exceeded(e):
    """Handle rate limit exceeded."""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': f'{e.description}'
    }), 429
```