# Database Querying Patterns

## SQLAlchemy Dynamic Queries

### Basic Filter Building
```python
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Dict, List, Any, Optional

class SearchQueryBuilder:
    """Build dynamic SQLAlchemy queries from search parameters."""

    def __init__(self, model, session: Session):
        self.model = model
        self.session = session
        self.query = session.query(model)

    def add_text_search(self, search_term: str, columns: List[str]):
        """Add text search across multiple columns."""
        if not search_term:
            return self

        search_term = f"%{search_term}%"
        conditions = []

        for column in columns:
            if hasattr(self.model, column):
                conditions.append(
                    getattr(self.model, column).ilike(search_term)
                )

        if conditions:
            self.query = self.query.filter(or_(*conditions))

        return self

    def add_filters(self, filters: Dict[str, Any]):
        """Add exact match filters."""
        for key, value in filters.items():
            if value is not None and hasattr(self.model, key):
                if isinstance(value, list):
                    # IN clause for multiple values
                    self.query = self.query.filter(
                        getattr(self.model, key).in_(value)
                    )
                else:
                    # Exact match
                    self.query = self.query.filter(
                        getattr(self.model, key) == value
                    )

        return self

    def add_range_filter(self, column: str, min_val: Any, max_val: Any):
        """Add range filter (e.g., price range)."""
        if hasattr(self.model, column):
            if min_val is not None:
                self.query = self.query.filter(
                    getattr(self.model, column) >= min_val
                )
            if max_val is not None:
                self.query = self.query.filter(
                    getattr(self.model, column) <= max_val
                )

        return self

    def add_sorting(self, sort_by: str, order: str = 'asc'):
        """Add sorting to query."""
        if hasattr(self.model, sort_by):
            column = getattr(self.model, sort_by)
            if order == 'desc':
                self.query = self.query.order_by(column.desc())
            else:
                self.query = self.query.order_by(column.asc())

        return self

    def paginate(self, page: int = 1, per_page: int = 20):
        """Add pagination."""
        offset = (page - 1) * per_page
        self.query = self.query.offset(offset).limit(per_page)
        return self

    def execute(self):
        """Execute the query and return results."""
        return self.query.all()

    def count(self):
        """Get total count without pagination."""
        return self.query.count()
```

### Advanced Text Search with PostgreSQL
```python
from sqlalchemy import text, func
from sqlalchemy.dialects.postgresql import TSVECTOR

class PostgreSQLSearch:
    """Full-text search using PostgreSQL."""

    @staticmethod
    def create_search_vector(model):
        """Create tsvector index for full-text search."""
        # Add this to your model
        search_vector = func.to_tsvector(
            'english',
            func.coalesce(model.title, '') + ' ' +
            func.coalesce(model.description, '') + ' ' +
            func.coalesce(model.tags, '')
        )
        return search_vector

    def search_products(self, session: Session, query: str, filters: Dict = None):
        """Perform full-text search with ranking."""
        from models import Product

        # Create tsquery
        search_query = func.plainto_tsquery('english', query)

        # Build base query with ranking
        q = session.query(
            Product,
            func.ts_rank(
                func.to_tsvector('english', Product.search_text),
                search_query
            ).label('rank')
        ).filter(
            func.to_tsvector('english', Product.search_text).match(search_query)
        )

        # Add additional filters
        if filters:
            for key, value in filters.items():
                if hasattr(Product, key):
                    q = q.filter(getattr(Product, key) == value)

        # Order by relevance
        q = q.order_by(text('rank DESC'))

        return q.all()

    def create_search_index(self, session: Session):
        """Create GIN index for better performance."""
        sql = """
        CREATE INDEX idx_product_search_vector
        ON products
        USING GIN (to_tsvector('english',
            COALESCE(title, '') || ' ' ||
            COALESCE(description, '') || ' ' ||
            COALESCE(tags, '')
        ));
        """
        session.execute(text(sql))
        session.commit()
```

### Faceted Search with Aggregations
```python
from sqlalchemy import func, distinct

class FacetedSearch:
    """Generate facets with counts for filters."""

    def get_facets(self, session: Session, base_filters: Dict = None):
        """Get available facets with counts."""
        from models import Product

        facets = {}

        # Base query with existing filters
        base_query = session.query(Product)
        if base_filters:
            for key, value in base_filters.items():
                if key != 'category':  # Don't apply the facet we're counting
                    base_query = base_query.filter(
                        getattr(Product, key) == value
                    )

        # Category facet
        category_facets = base_query.with_entities(
            Product.category,
            func.count(Product.id).label('count')
        ).group_by(Product.category).all()

        facets['category'] = [
            {'value': cat, 'count': count}
            for cat, count in category_facets
        ]

        # Brand facet
        brand_facets = base_query.with_entities(
            Product.brand,
            func.count(Product.id).label('count')
        ).group_by(Product.brand).all()

        facets['brand'] = [
            {'value': brand, 'count': count}
            for brand, count in brand_facets
        ]

        # Price range facet
        price_ranges = [
            (0, 50, 'Under $50'),
            (50, 100, '$50 - $100'),
            (100, 200, '$100 - $200'),
            (200, None, 'Over $200')
        ]

        facets['price_range'] = []
        for min_price, max_price, label in price_ranges:
            q = base_query
            q = q.filter(Product.price >= min_price)
            if max_price:
                q = q.filter(Product.price < max_price)

            count = q.count()
            if count > 0:
                facets['price_range'].append({
                    'value': f"{min_price}-{max_price or 'inf'}",
                    'label': label,
                    'count': count
                })

        return facets
```

## Django ORM Patterns

### Django Filter Backend
```python
from django.db.models import Q, Count, Avg
from django_filters import FilterSet, CharFilter, RangeFilter
from rest_framework import filters

class ProductFilter(FilterSet):
    """Django filter for product search."""

    search = CharFilter(method='search_filter')
    price = RangeFilter()
    category = CharFilter(field_name='category__name', lookup_expr='iexact')
    brand = CharFilter(field_name='brand', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['search', 'price', 'category', 'brand', 'in_stock']

    def search_filter(self, queryset, name, value):
        """Custom search across multiple fields."""
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(tags__icontains=value)
        )

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet with search and filtering."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['price', 'created_at', 'rating']
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        """Optimize query with select_related and prefetch_related."""
        queryset = super().get_queryset()
        queryset = queryset.select_related('category', 'brand')
        queryset = queryset.prefetch_related('reviews', 'images')

        # Add annotations for computed fields
        queryset = queryset.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )

        return queryset
```

### Django Full-Text Search
```python
from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank, TrigramSimilarity
)

class PostgreSQLFullTextSearch:
    """PostgreSQL full-text search in Django."""

    def search_products(self, query: str):
        """Perform full-text search with ranking."""
        from products.models import Product

        # Create search vector
        search_vector = SearchVector(
            'title', weight='A'
        ) + SearchVector(
            'description', weight='B'
        ) + SearchVector(
            'tags', weight='C'
        )

        # Create search query
        search_query = SearchQuery(query, config='english')

        # Perform search with ranking
        results = Product.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(
            search=search_query
        ).order_by('-rank')

        return results

    def trigram_search(self, query: str):
        """Use trigram similarity for fuzzy matching."""
        from products.models import Product

        return Product.objects.annotate(
            similarity=TrigramSimilarity('title', query)
        ).filter(
            similarity__gt=0.1
        ).order_by('-similarity')

    def combined_search(self, query: str):
        """Combine full-text and trigram search."""
        from products.models import Product

        # Full-text search
        search_vector = SearchVector('title', 'description')
        search_query = SearchQuery(query)

        # Combine with trigram similarity
        results = Product.objects.annotate(
            search_rank=SearchRank(search_vector, search_query),
            title_similarity=TrigramSimilarity('title', query),
            combined_score=F('search_rank') + F('title_similarity')
        ).filter(
            Q(search=search_query) | Q(title_similarity__gt=0.1)
        ).order_by('-combined_score')

        return results
```

## Query Optimization

### Index Strategies
```python
"""
Database indexes for search optimization.
Add these to your models or migrations.
"""

# SQLAlchemy indexes
from sqlalchemy import Index

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, index=True)  # Single column index
    brand = Column(String, index=True)
    price = Column(Numeric(10, 2), index=True)
    created_at = Column(DateTime, index=True)

    # Composite indexes
    __table_args__ = (
        Index('idx_category_brand', 'category', 'brand'),
        Index('idx_price_category', 'price', 'category'),
        Index('idx_search_fields', 'title', 'description'),  # For text search
    )

# Django indexes
class Product(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=50, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'brand']),
            models.Index(fields=['price', '-created_at']),  # Compound index
            models.Index(fields=['title'], name='title_idx'),
        ]
```

### Query Performance Monitoring
```python
import time
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

@contextmanager
def query_performance_monitor(operation_name: str):
    """Monitor query execution time."""
    start_time = time.time()

    try:
        yield
    finally:
        execution_time = time.time() - start_time

        if execution_time > 1.0:  # Log slow queries
            logger.warning(
                f"Slow query detected: {operation_name} "
                f"took {execution_time:.2f} seconds"
            )
        else:
            logger.info(
                f"Query {operation_name} "
                f"executed in {execution_time:.3f} seconds"
            )

# Usage
def search_products(query: str, filters: Dict):
    with query_performance_monitor("product_search"):
        results = SearchQueryBuilder(Product, session)\
            .add_text_search(query, ['title', 'description'])\
            .add_filters(filters)\
            .execute()

    return results
```

### Query Result Caching
```python
from functools import lru_cache
import hashlib
import json

class QueryCache:
    """Simple query result caching."""

    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds

    def _generate_key(self, query: str, filters: Dict):
        """Generate cache key from query parameters."""
        cache_data = {
            'query': query,
            'filters': filters
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()

    def get(self, query: str, filters: Dict):
        """Get cached results if available."""
        key = self._generate_key(query, filters)

        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return result
            else:
                del self.cache[key]

        return None

    def set(self, query: str, filters: Dict, results):
        """Cache query results."""
        key = self._generate_key(query, filters)
        self.cache[key] = (results, time.time())

    def clear(self):
        """Clear all cached results."""
        self.cache.clear()

# Usage
cache = QueryCache(ttl_seconds=300)

def cached_search(query: str, filters: Dict):
    # Check cache
    cached = cache.get(query, filters)
    if cached:
        return cached

    # Perform search
    results = perform_search(query, filters)

    # Cache results
    cache.set(query, filters, results)

    return results
```

## Security Considerations

### SQL Injection Prevention
```python
class SecureQueryBuilder:
    """Secure query building with input validation."""

    @staticmethod
    def sanitize_search_term(term: str) -> str:
        """Sanitize search input."""
        # Remove SQL special characters
        dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_', '@@', '@']
        for char in dangerous_chars:
            term = term.replace(char, '')

        # Limit length
        return term[:100]

    @staticmethod
    def validate_column_name(column: str, allowed_columns: List[str]) -> bool:
        """Validate column name against whitelist."""
        return column in allowed_columns

    @staticmethod
    def validate_sort_order(order: str) -> str:
        """Validate sort order."""
        return 'desc' if order.lower() == 'desc' else 'asc'

    def build_safe_query(self, params: Dict):
        """Build query with validation."""
        allowed_columns = ['title', 'description', 'category', 'brand', 'price']

        # Validate and sanitize inputs
        if 'search' in params:
            params['search'] = self.sanitize_search_term(params['search'])

        if 'sort_by' in params:
            if not self.validate_column_name(params['sort_by'], allowed_columns):
                params['sort_by'] = 'created_at'  # Default

        if 'order' in params:
            params['order'] = self.validate_sort_order(params['order'])

        # Build query safely using parameterized queries
        return self._build_query(params)
```