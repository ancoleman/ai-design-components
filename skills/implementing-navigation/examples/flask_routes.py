"""
Flask Blueprint Organization Example

This example demonstrates:
- Blueprint-based route organization
- Route guards and authentication
- Error handling
- RESTful API patterns
- Navigation hierarchy
"""

from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from typing import Dict, List, Any

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# ====================
# Main Navigation Routes
# ====================

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home page with navigation structure."""
    nav_items = get_navigation_structure()
    return render_template('index.html', navigation=nav_items)

@main_bp.route('/about')
def about():
    """About page."""
    breadcrumbs = [
        {'label': 'Home', 'href': url_for('main.home')},
        {'label': 'About', 'href': url_for('main.about'), 'current': True}
    ]
    return render_template('about.html', breadcrumbs=breadcrumbs)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling."""
    if request.method == 'POST':
        # Process contact form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Send email or save to database
        process_contact_form(name, email, message)

        return redirect(url_for('main.contact_success'))

    return render_template('contact.html')

# ====================
# Product Navigation
# ====================

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def product_list():
    """Product listing with filtering."""
    # Get filter parameters
    category = request.args.get('category')
    sort = request.args.get('sort', 'name')
    page = request.args.get('page', 1, type=int)

    # Fetch products
    products = get_products(category=category, sort=sort, page=page)

    # Build breadcrumbs
    breadcrumbs = [
        {'label': 'Home', 'href': url_for('main.home')},
        {'label': 'Products', 'href': url_for('products.product_list'), 'current': True}
    ]

    return render_template('products/list.html',
                         products=products,
                         breadcrumbs=breadcrumbs,
                         current_category=category)

@products_bp.route('/category/<category_slug>')
def product_category(category_slug: str):
    """Product category page."""
    category = get_category_by_slug(category_slug)
    if not category:
        abort(404)

    products = get_products_by_category(category_slug)

    # Build breadcrumbs with category
    breadcrumbs = [
        {'label': 'Home', 'href': url_for('main.home')},
        {'label': 'Products', 'href': url_for('products.product_list')},
        {'label': category['name'], 'href': url_for('products.product_category', category_slug=category_slug), 'current': True}
    ]

    return render_template('products/category.html',
                         category=category,
                         products=products,
                         breadcrumbs=breadcrumbs)

@products_bp.route('/<int:product_id>')
def product_detail(product_id: int):
    """Product detail page."""
    product = get_product(product_id)
    if not product:
        abort(404)

    # Build full breadcrumb trail
    breadcrumbs = build_product_breadcrumbs(product)

    # Get related navigation
    related_products = get_related_products(product_id)

    return render_template('products/detail.html',
                         product=product,
                         breadcrumbs=breadcrumbs,
                         related_products=related_products)

# ====================
# Admin Routes with Authentication
# ====================

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator for admin-only routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    """Admin dashboard with navigation stats."""
    stats = {
        'total_pages': count_pages(),
        'total_products': count_products(),
        'navigation_depth': calculate_navigation_depth(),
        'broken_links': check_broken_links()
    }

    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/navigation')
@admin_required
def manage_navigation():
    """Manage site navigation structure."""
    nav_structure = get_full_navigation_structure()
    return render_template('admin/navigation.html', navigation=nav_structure)

@admin_bp.route('/navigation/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_required
def edit_navigation_item(item_id: int):
    """Edit navigation item."""
    nav_item = get_navigation_item(item_id)

    if request.method == 'POST':
        nav_item['label'] = request.form.get('label')
        nav_item['href'] = request.form.get('href')
        nav_item['parent_id'] = request.form.get('parent_id', type=int)
        nav_item['order'] = request.form.get('order', type=int)

        save_navigation_item(nav_item)
        return redirect(url_for('admin.manage_navigation'))

    return render_template('admin/edit_navigation.html', item=nav_item)

# ====================
# API Routes for Dynamic Navigation
# ====================

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/navigation')
def api_navigation():
    """Get navigation structure as JSON."""
    nav_structure = get_navigation_structure()
    return jsonify(nav_structure)

@api_bp.route('/navigation/breadcrumbs')
def api_breadcrumbs():
    """Calculate breadcrumbs for current path."""
    path = request.args.get('path', '/')
    breadcrumbs = calculate_breadcrumbs(path)
    return jsonify(breadcrumbs)

@api_bp.route('/navigation/search')
def api_navigation_search():
    """Search navigation items."""
    query = request.args.get('q', '')
    results = search_navigation(query)
    return jsonify(results)

@api_bp.route('/navigation/sitemap')
def api_sitemap():
    """Generate sitemap for SEO."""
    sitemap = generate_sitemap()
    return jsonify(sitemap)

# ====================
# Helper Functions
# ====================

def get_navigation_structure() -> List[Dict[str, Any]]:
    """Get main navigation structure."""
    return [
        {
            'id': 'home',
            'label': 'Home',
            'href': url_for('main.home'),
            'icon': 'home'
        },
        {
            'id': 'products',
            'label': 'Products',
            'href': url_for('products.product_list'),
            'icon': 'shopping-cart',
            'children': [
                {
                    'label': 'Electronics',
                    'href': url_for('products.product_category', category_slug='electronics')
                },
                {
                    'label': 'Clothing',
                    'href': url_for('products.product_category', category_slug='clothing')
                },
                {
                    'label': 'Books',
                    'href': url_for('products.product_category', category_slug='books')
                }
            ]
        },
        {
            'id': 'about',
            'label': 'About',
            'href': url_for('main.about'),
            'icon': 'info'
        },
        {
            'id': 'contact',
            'label': 'Contact',
            'href': url_for('main.contact'),
            'icon': 'mail'
        }
    ]

def calculate_breadcrumbs(path: str) -> List[Dict[str, Any]]:
    """Calculate breadcrumb trail for given path."""
    breadcrumbs = [
        {'label': 'Home', 'href': '/'}
    ]

    # Parse path and build breadcrumbs
    segments = [s for s in path.split('/') if s]
    current_path = ''

    for i, segment in enumerate(segments):
        current_path += '/' + segment
        is_last = i == len(segments) - 1

        # Look up proper label for segment
        label = get_label_for_segment(segment, current_path)

        breadcrumbs.append({
            'label': label,
            'href': current_path,
            'current': is_last
        })

    return breadcrumbs

def build_product_breadcrumbs(product: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build breadcrumb trail for product."""
    breadcrumbs = [
        {'label': 'Home', 'href': url_for('main.home')},
        {'label': 'Products', 'href': url_for('products.product_list')}
    ]

    if product.get('category'):
        breadcrumbs.append({
            'label': product['category']['name'],
            'href': url_for('products.product_category',
                          category_slug=product['category']['slug'])
        })

    breadcrumbs.append({
        'label': product['name'],
        'href': url_for('products.product_detail', product_id=product['id']),
        'current': True
    })

    return breadcrumbs

# ====================
# Register Blueprints
# ====================

app.register_blueprint(main_bp)
app.register_blueprint(products_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

# ====================
# Error Handlers
# ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with navigation context."""
    if request.path.startswith('/api'):
        return jsonify({'error': 'Not found'}), 404

    return render_template('errors/404.html',
                         navigation=get_navigation_structure()), 404

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors."""
    if request.path.startswith('/api'):
        return jsonify({'error': 'Forbidden'}), 403

    return render_template('errors/403.html',
                         navigation=get_navigation_structure()), 403

if __name__ == '__main__':
    app.run(debug=True)