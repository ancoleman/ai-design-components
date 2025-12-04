"""
Django URL Pattern Organization
Demonstrates best practices for organizing URL patterns in Django applications.
"""

from django.urls import path, include
from django.contrib import admin
from . import views

# Root URL configuration (myproject/urls.py)
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # API endpoints (namespaced)
    path('api/v1/', include('api.urls', namespace='api')),

    # App-specific URLs (include pattern)
    path('blog/', include('blog.urls')),
    path('shop/', include('shop.urls')),
    path('accounts/', include('accounts.urls')),

    # Root pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]


# App-level URL configuration (blog/urls.py)
app_name = 'blog'  # Namespace for reverse URL lookups

urlpatterns = [
    # List view
    path('', views.PostListView.as_view(), name='post_list'),

    # Detail view with slug
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    # Create, update, delete
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Category filtering
    path('category/<slug:category_slug>/', views.PostByCategoryView.as_view(), name='posts_by_category'),

    # Tag filtering
    path('tag/<slug:tag_slug>/', views.PostByTagView.as_view(), name='posts_by_tag'),

    # Comments (nested)
    path('<int:post_id>/comments/', include('comments.urls')),
]


# API URL configuration (api/urls.py)
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CommentViewSet

app_name = 'api'

# Router for ViewSets (automatic CRUD endpoints)
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Router-generated URLs
    path('', include(router.urls)),

    # Custom API endpoints
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('auth/refresh/', views.RefreshTokenAPIView.as_view(), name='refresh'),

    # Nested resources
    path('posts/<int:post_id>/comments/', views.PostCommentsAPIView.as_view(), name='post_comments'),

    # Search endpoints
    path('search/', views.SearchAPIView.as_view(), name='search'),
    path('search/posts/', views.PostSearchAPIView.as_view(), name='post_search'),
]


# E-commerce URL patterns (shop/urls.py)
app_name = 'shop'

urlpatterns = [
    # Product listings
    path('', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),

    # Cart operations
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

    # Checkout flow
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/shipping/', views.ShippingView.as_view(), name='checkout_shipping'),
    path('checkout/payment/', views.PaymentView.as_view(), name='checkout_payment'),
    path('checkout/confirm/', views.ConfirmOrderView.as_view(), name='checkout_confirm'),

    # Order management
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]


# URL pattern with multiple parameters
urlpatterns = [
    # Date-based archive
    path(
        'archive/<int:year>/<int:month>/<int:day>/',
        views.DayArchiveView.as_view(),
        name='day_archive'
    ),

    # Nested resources with multiple IDs
    path(
        'projects/<int:project_id>/tasks/<int:task_id>/comments/',
        views.TaskCommentsView.as_view(),
        name='task_comments'
    ),
]


# Advanced URL patterns with converters
from django.urls import register_converter

class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value

register_converter(FourDigitYearConverter, 'yyyy')

urlpatterns = [
    # Custom converter usage
    path('archive/<yyyy:year>/', views.YearArchiveView.as_view(), name='year_archive'),

    # Built-in converters
    path('user/<uuid:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post'),
    path('page/<path:page_path>/', views.PageView.as_view(), name='page'),
]


# Reverse URL lookups (usage in views/templates)
"""
# In views.py
from django.urls import reverse
from django.shortcuts import redirect

def create_post(request):
    # ... create post logic ...
    return redirect('blog:post_detail', slug=post.slug)

# Using reverse()
url = reverse('blog:post_detail', kwargs={'slug': 'my-post'})
# Result: /blog/my-post/

url = reverse('api:post-detail', kwargs={'pk': 123})
# Result: /api/v1/posts/123/

# In templates
{% url 'blog:post_detail' slug=post.slug %}
{% url 'shop:product_detail' slug='laptop-pro' %}
{% url 'api:user-list' %}
"""


# Best Practices Summary
"""
1. Use include() for app-specific URLs
2. Use app_name for namespacing
3. Use descriptive names for URL patterns
4. Group related URLs logically
5. Use slug fields for SEO-friendly URLs
6. Version API endpoints (api/v1/, api/v2/)
7. Use routers for ViewSets (DRF)
8. Keep URL patterns DRY (Don't Repeat Yourself)
9. Use path() over re_path() when possible
10. Document complex URL patterns
"""
