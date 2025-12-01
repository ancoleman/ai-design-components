"""
Django REST Framework filter backend implementation.

This example demonstrates advanced filtering with Django REST Framework,
including custom filter backends, faceted search, and query optimization.
"""

from django.db import models
from django.db.models import Q, Count, Avg, F, Value, CharField
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as df
from django.core.cache import cache
from typing import Dict, List, Any
import json
import hashlib


# Models
class Product(models.Model):
    """Product model with search-optimized fields."""

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    in_stock = models.BooleanField(default=True, db_index=True)
    tags = models.ManyToManyField('Tag', related_name='products')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # PostgreSQL specific: Full-text search vector
    search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')

    class Meta:
        indexes = [
            models.Index(fields=['category', 'brand']),
            models.Index(fields=['price', '-created_at']),
            models.Index(fields=['-rating', 'in_stock']),
        ]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


# Custom Filter Backend
class FacetedSearchBackend(filters.BaseFilterBackend):
    """Custom filter backend for faceted search with dynamic counts."""

    def filter_queryset(self, request, queryset, view):
        """Apply filters while maintaining facet counts."""

        # Get filter parameters
        params = request.query_params

        # Text search
        query = params.get('q', '').strip()
        if query:
            queryset = self._apply_text_search(queryset, query)

        # Category filter
        categories = params.getlist('category')
        if categories:
            queryset = queryset.filter(category__slug__in=categories)

        # Brand filter
        brands = params.getlist('brand')
        if brands:
            queryset = queryset.filter(brand__slug__in=brands)

        # Price range
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Stock filter
        in_stock = params.get('in_stock')
        if in_stock:
            queryset = queryset.filter(in_stock=in_stock.lower() == 'true')

        # Rating filter
        min_rating = params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset

    def _apply_text_search(self, queryset, query):
        """Apply PostgreSQL full-text search."""
        from django.db import connection

        if connection.vendor == 'postgresql':
            # Use PostgreSQL full-text search
            search_query = SearchQuery(query, config='english')
            search_vector = SearchVector('title', weight='A') + \
                          SearchVector('description', weight='B')

            queryset = queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
        else:
            # Fallback to LIKE queries
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return queryset


# Django Filter
class ProductFilter(df.FilterSet):
    """Product filter using django-filter."""

    q = df.CharFilter(method='search')
    category = df.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    brand = df.ModelMultipleChoiceFilter(
        field_name='brand__slug',
        to_field_name='slug',
        queryset=Brand.objects.all()
    )
    min_price = df.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = df.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = df.BooleanFilter()
    min_rating = df.NumberFilter(field_name='rating', lookup_expr='gte')
    tags = df.ModelMultipleChoiceFilter(
        field_name='tags__name',
        to_field_name='name',
        queryset=Tag.objects.all()
    )

    # Date filters
    created_after = df.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = df.DateFilter(field_name='created_at', lookup_expr='lte')

    # Ordering
    o = df.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('rating', 'rating'),
            ('created_at', 'newest'),
        ),
        field_labels={
            'price': 'Price',
            '-price': 'Price (high to low)',
            'rating': 'Rating (low to high)',
            '-rating': 'Rating (high to low)',
            '-created_at': 'Newest first',
        }
    )

    def search(self, queryset, name, value):
        """Custom search method with relevance scoring."""
        if not value:
            return queryset

        # PostgreSQL full-text search
        from django.db import connection

        if connection.vendor == 'postgresql':
            search_query = SearchQuery(value, config='english')
            search_vector = SearchVector('title', weight='A') + \
                          SearchVector('description', weight='B')

            return queryset.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(
                Q(title__icontains=value) |
                Q(description__icontains=value)
            ).order_by('-rank')

        # Fallback for other databases
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )

    class Meta:
        model = Product
        fields = ['q', 'category', 'brand', 'min_price', 'max_price',
                 'in_stock', 'min_rating', 'tags']


# Serializers
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer with nested relationships."""

    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'category', 'brand',
                 'price', 'rating', 'in_stock', 'tags', 'created_at']


class FacetSerializer(serializers.Serializer):
    """Facet serializer for filter options."""

    value = serializers.CharField()
    label = serializers.CharField()
    count = serializers.IntegerField()


class SearchResultSerializer(serializers.Serializer):
    """Search result with facets."""

    products = ProductSerializer(many=True)
    facets = serializers.DictField(child=FacetSerializer(many=True))
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()


# Custom Pagination
class SearchPagination(PageNumberPagination):
    """Custom pagination for search results."""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Include additional metadata in response."""
        return Response({
            'products': data,
            'pagination': {
                'total': self.page.paginator.count,
                'page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'total_pages': self.page.paginator.num_pages,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            }
        })


# ViewSet
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Product search and filter viewset."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        FacetedSearchBackend,
        df.DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_class = ProductFilter
    pagination_class = SearchPagination
    ordering_fields = ['price', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Optimize queryset with select/prefetch related."""
        queryset = super().get_queryset()

        # Optimize database queries
        queryset = queryset.select_related('category', 'brand')
        queryset = queryset.prefetch_related('tags')

        # Add annotations for computed fields
        queryset = queryset.annotate(
            review_count=Count('reviews', distinct=True),
            avg_rating=Avg('reviews__rating')
        )

        return queryset

    def list(self, request, *args, **kwargs):
        """Override list to include facets."""

        # Check cache
        cache_key = self._get_cache_key(request)
        cached_result = cache.get(cache_key)

        if cached_result:
            return Response(cached_result)

        # Get filtered queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Get facets before pagination
        facets = self._get_facets(queryset, request)

        # Paginate
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['facets'] = facets

            # Cache result
            cache.set(cache_key, response.data, 300)  # 5 minutes

            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'products': serializer.data,
            'facets': facets
        })

    def _get_facets(self, queryset, request):
        """Generate facet counts for filters."""

        facets = {}

        # Category facets
        category_facets = queryset.values('category__name', 'category__slug')\
            .annotate(count=Count('id'))\
            .order_by('-count')[:20]

        facets['categories'] = [
            {
                'value': item['category__slug'],
                'label': item['category__name'],
                'count': item['count']
            }
            for item in category_facets
        ]

        # Brand facets
        brand_facets = queryset.values('brand__name', 'brand__slug')\
            .annotate(count=Count('id'))\
            .order_by('-count')[:20]

        facets['brands'] = [
            {
                'value': item['brand__slug'],
                'label': item['brand__name'],
                'count': item['count']
            }
            for item in brand_facets
        ]

        # Price range facets
        price_ranges = [
            (0, 50, 'Under $50'),
            (50, 100, '$50-$100'),
            (100, 200, '$100-$200'),
            (200, 500, '$200-$500'),
            (500, None, 'Over $500')
        ]

        price_facets = []
        for min_price, max_price, label in price_ranges:
            count_query = queryset.filter(price__gte=min_price)
            if max_price:
                count_query = count_query.filter(price__lt=max_price)

            count = count_query.count()
            if count > 0:
                price_facets.append({
                    'value': f'{min_price}-{max_price or "inf"}',
                    'label': label,
                    'count': count
                })

        facets['price_ranges'] = price_facets

        # In stock count
        in_stock_count = queryset.filter(in_stock=True).count()
        out_of_stock_count = queryset.filter(in_stock=False).count()

        facets['availability'] = [
            {'value': 'true', 'label': 'In Stock', 'count': in_stock_count},
            {'value': 'false', 'label': 'Out of Stock', 'count': out_of_stock_count}
        ]

        return facets

    def _get_cache_key(self, request):
        """Generate cache key from request parameters."""
        params = dict(request.query_params)
        # Sort for consistent hashing
        params_str = json.dumps(params, sort_keys=True)
        return f'search:{hashlib.md5(params_str.encode()).hexdigest()}'

    @action(detail=False, methods=['get'])
    def autocomplete(self, request):
        """Autocomplete endpoint for search suggestions."""

        query = request.query_params.get('q', '').strip()
        if len(query) < 2:
            return Response({'suggestions': []})

        # Get suggestions from products
        suggestions = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        ).values('title').distinct()[:10]

        # Format response
        return Response({
            'query': query,
            'suggestions': [
                {
                    'text': item['title'],
                    'type': 'product'
                }
                for item in suggestions
            ]
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export search results to CSV."""

        queryset = self.filter_queryset(self.get_queryset())

        # Limit export size
        queryset = queryset[:1000]

        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Title', 'Category', 'Brand', 'Price', 'In Stock'])

        for product in queryset:
            writer.writerow([
                product.id,
                product.title,
                product.category.name,
                product.brand.name,
                product.price,
                product.in_stock
            ])

        return response


# Management Command for Search Index
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Management command to rebuild search index."""

    help = 'Rebuild PostgreSQL search index'

    def handle(self, *args, **options):
        from django.db import connection

        with connection.cursor() as cursor:
            # Create GIN index for full-text search
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS products_search_vector_idx
                ON products_product
                USING GIN(
                    to_tsvector('english',
                        COALESCE(title, '') || ' ' ||
                        COALESCE(description, '')
                    )
                )
            """)

            self.stdout.write(
                self.style.SUCCESS('Successfully created search index')
            )


# URLs
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]