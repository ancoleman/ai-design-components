# Django URL Configuration

## Table of Contents
- [URL Configuration Basics](#url-configuration-basics)
- [URL Namespaces](#url-namespaces)
- [Path Converters](#path-converters)
- [Class-Based Views](#class-based-views)
- [URL Reversing](#url-reversing)
- [Advanced Patterns](#advanced-patterns)

## URL Configuration Basics

### Project URL Configuration

```python
# myproject/urls.py - Main URL configuration
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # Include app URLs
    path('', include('core.urls')),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('api/', include('api.urls', namespace='api')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('shop/', include('shop.urls', namespace='shop')),

    # Redirects
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),

    # Third-party apps
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'
handler400 = 'core.views.custom_400'
```

### App URL Configuration

```python
# blog/urls.py - App-specific URLs
from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    # List views
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    path('tag/<slug:tag>/', views.TaggedPostsView.as_view(), name='tagged_posts'),
    path('author/<str:username>/', views.AuthorPostsView.as_view(), name='author_posts'),

    # Detail views
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    # CRUD operations
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # API-like endpoints
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),

    # Archive views
    path('archive/', views.ArchiveView.as_view(), name='archive'),
    path('archive/<int:year>/', views.YearArchiveView.as_view(), name='year_archive'),
    path('archive/<int:year>/<int:month>/', views.MonthArchiveView.as_view(), name='month_archive'),

    # Search
    path('search/', views.SearchView.as_view(), name='search'),

    # RSS/Atom feeds
    path('feed/rss/', views.RSSFeed(), name='rss_feed'),
    path('feed/atom/', views.AtomFeed(), name='atom_feed'),
]
```

## URL Namespaces

### Namespace Organization

```python
# shop/urls.py - E-commerce URLs with namespacing
from django.urls import path, include

app_name = 'shop'

# Product patterns
product_patterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/review/', views.AddReviewView.as_view(), name='add_review'),
]

# Cart patterns
cart_patterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
]

# Checkout patterns
checkout_patterns = [
    path('', views.CheckoutView.as_view(), name='checkout'),
    path('address/', views.AddressView.as_view(), name='checkout_address'),
    path('payment/', views.PaymentView.as_view(), name='checkout_payment'),
    path('confirm/', views.ConfirmView.as_view(), name='checkout_confirm'),
    path('success/<str:order_id>/', views.SuccessView.as_view(), name='checkout_success'),
]

urlpatterns = [
    path('products/', include(product_patterns)),
    path('cart/', include(cart_patterns)),
    path('checkout/', include(checkout_patterns)),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<str:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]
```

### Using Namespaces in Templates

```django
{# templates/shop/product_list.html #}
{% load static %}

{# URL reversing with namespace #}
<a href="{% url 'shop:product_detail' slug=product.slug %}">
    {{ product.name }}
</a>

{# Cart operations #}
<form action="{% url 'shop:add_to_cart' product_id=product.id %}" method="post">
    {% csrf_token %}
    <button type="submit">Add to Cart</button>
</form>

{# Navigation with current page highlighting #}
<nav>
    <a href="{% url 'shop:product_list' %}"
       {% if request.resolver_match.url_name == 'product_list' %}class="active"{% endif %}>
        All Products
    </a>
    <a href="{% url 'shop:cart' %}">
        Cart ({{ cart.item_count }})
    </a>
</nav>
```

## Path Converters

### Built-in Path Converters

```python
from django.urls import path, register_converter
from django.shortcuts import get_object_or_404
from . import views

urlpatterns = [
    # str - Matches any non-empty string (excluding /)
    path('user/<str:username>/', views.user_profile, name='user_profile'),

    # int - Matches positive integers
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),

    # slug - Matches slug strings (letters, numbers, hyphens, underscores)
    path('post/<slug:post_slug>/', views.post_detail, name='post_detail'),

    # uuid - Matches formatted UUID
    path('document/<uuid:doc_id>/', views.document_view, name='document'),

    # path - Matches any string including /
    path('page/<path:page_path>/', views.page_view, name='page'),
]
```

### Custom Path Converters

```python
# converters.py
from datetime import datetime

class DateConverter:
    """Convert YYYY-MM-DD to datetime object."""
    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')

class MonthYearConverter:
    """Convert YYYY-MM to year and month."""
    regex = r'\d{4}-\d{2}'

    def to_python(self, value):
        year, month = value.split('-')
        return {'year': int(year), 'month': int(month)}

    def to_url(self, value):
        return f"{value['year']:04d}-{value['month']:02d}"

# Register custom converters
from django.urls import register_converter
register_converter(DateConverter, 'date')
register_converter(MonthYearConverter, 'month_year')

# Usage in URLs
urlpatterns = [
    path('events/<date:event_date>/', views.events_on_date, name='events_date'),
    path('archive/<month_year:period>/', views.monthly_archive, name='monthly_archive'),
]

# View example
def events_on_date(request, event_date):
    # event_date is already a datetime.date object
    events = Event.objects.filter(date=event_date)
    return render(request, 'events/list.html', {'events': events, 'date': event_date})

def monthly_archive(request, period):
    # period is a dictionary with 'year' and 'month'
    posts = Post.objects.filter(
        created_at__year=period['year'],
        created_at__month=period['month']
    )
    return render(request, 'blog/archive.html', {'posts': posts, 'period': period})
```

## Class-Based Views

### Generic View URLs

```python
# views.py
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView, RedirectView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Article
from .forms import ArticleForm

class ArticleListView(ListView):
    model = Article
    paginate_by = 20
    context_object_name = 'articles'
    template_name = 'articles/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.select_related('author', 'category')

class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'articles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_articles'] = Article.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:5]
        return context

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/form.html'
    success_url = reverse_lazy('articles:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/form.html'

    def get_success_url(self):
        return reverse('articles:detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff

class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = 'articles.delete_article'
    success_url = reverse_lazy('articles:list')
    template_name = 'articles/confirm_delete.html'

# urls.py
urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete'),
]
```

### Viewsets and Routers (DRF)

```python
# api/views.py - Django REST Framework viewsets
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model providing CRUD operations.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def set_favorite(self, request, pk=None):
        """Custom action to favorite a product."""
        product = self.get_object()
        request.user.favorites.add(product)
        return Response({'status': 'favorite set'})

    @action(detail=False)
    def featured(self, request):
        """List featured products."""
        featured = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet, basename='order')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]

# This automatically creates:
# GET /api/products/ - list
# POST /api/products/ - create
# GET /api/products/{id}/ - retrieve
# PUT /api/products/{id}/ - update
# PATCH /api/products/{id}/ - partial_update
# DELETE /api/products/{id}/ - destroy
# POST /api/products/{id}/set_favorite/ - custom action
# GET /api/products/featured/ - custom list action
```

## URL Reversing

### Reverse URL Resolution

```python
# views.py
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def my_view(request):
    # Basic reverse
    url = reverse('blog:post_detail', kwargs={'pk': 123})

    # With arguments
    url = reverse('blog:archive', args=[2025, 12])

    # With query parameters
    from urllib.parse import urlencode
    base_url = reverse('blog:search')
    query_string = urlencode({'q': 'django'})
    url = f'{base_url}?{query_string}'

    return redirect(url)

# Class-based views
class MyFormView(FormView):
    # Use reverse_lazy for class attributes
    success_url = reverse_lazy('success')

    def get_success_url(self):
        # Use reverse in methods
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

# In models
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

# Template tags
from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def build_absolute_uri(request, view_name, *args, **kwargs):
    """Build absolute URL for sharing."""
    path = reverse(view_name, args=args, kwargs=kwargs)
    return request.build_absolute_uri(path)
```

### URL Resolution in Templates

```django
{# Basic URL reversing #}
<a href="{% url 'blog:post_list' %}">All Posts</a>

{# With arguments #}
<a href="{% url 'blog:post_detail' pk=post.pk %}">{{ post.title }}</a>

{# With multiple arguments #}
<a href="{% url 'blog:archive' year=2025 month=12 %}">December 2025</a>

{# Store URL in variable #}
{% url 'blog:post_detail' pk=post.pk as post_url %}
<a href="{{ post_url }}">Read More</a>

{# Absolute URL for sharing #}
{% load custom_tags %}
{% build_absolute_uri request 'blog:post_detail' pk=post.pk as absolute_url %}
<input type="text" value="{{ absolute_url }}" readonly>

{# URL with query parameters #}
<a href="{% url 'blog:search' %}?q={{ query|urlencode }}">Search: {{ query }}</a>

{# Conditional active class #}
<li class="{% if request.resolver_match.url_name == 'post_list' %}active{% endif %}">
    <a href="{% url 'blog:post_list' %}">Posts</a>
</li>
```

## Advanced Patterns

### Dynamic URL Routing

```python
# Dynamic URL patterns based on settings
from django.conf import settings
from django.urls import path, include

urlpatterns = []

# Conditionally include URLs
if settings.BLOG_ENABLED:
    urlpatterns += [
        path('blog/', include('blog.urls')),
    ]

if settings.SHOP_ENABLED:
    urlpatterns += [
        path('shop/', include('shop.urls')),
    ]

if settings.DEBUG:
    urlpatterns += [
        path('test/', include('test_app.urls')),
    ]

# Language-based URL patterns
from django.conf.urls.i18n import i18n_patterns

urlpatterns += i18n_patterns(
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    prefix_default_language=False,
)
```

### Subdomain Routing

```python
# middleware.py
class SubdomainMiddleware:
    """Route requests based on subdomain."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0] if '.' in host else None

        request.subdomain = subdomain

        # Route to different URL configs based on subdomain
        if subdomain == 'api':
            request.urlconf = 'myproject.urls_api'
        elif subdomain == 'admin':
            request.urlconf = 'myproject.urls_admin'
        else:
            request.urlconf = 'myproject.urls'

        response = self.get_response(request)
        return response

# urls_api.py - API subdomain URLs
from django.urls import path, include

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path('v2/', include('api.v2.urls')),
    path('docs/', include('api.docs.urls')),
]
```

### URL Decorators

```python
from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def ajax_required(view_func):
    """Decorator to ensure view only accepts AJAX requests."""
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden('AJAX required')
        return view_func(request, *args, **kwargs)
    return wrapped

def ssl_required(view_func):
    """Decorator to ensure HTTPS."""
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.is_secure() and not settings.DEBUG:
            return redirect('https://' + request.get_host() + request.get_full_path())
        return view_func(request, *args, **kwargs)
    return wrapped

def group_required(*group_names):
    """Decorator to check user group membership."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('auth:login')

            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(group in user_groups for group in group_names):
                return HttpResponseForbidden('Insufficient permissions')

            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator

# Usage in views
@ajax_required
def like_post(request, post_id):
    """AJAX-only endpoint for liking posts."""
    # ...

@ssl_required
@group_required('premium', 'admin')
def premium_content(request):
    """Premium content requiring HTTPS and group membership."""
    # ...
```

### Sitemap Generation

```python
# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'contact']

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

# urls.py
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, PostSitemap, CategorySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
```