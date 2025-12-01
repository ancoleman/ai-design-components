"""
SQLAlchemy search implementation with dynamic filtering and pagination.

This example demonstrates building complex search queries with SQLAlchemy,
including full-text search, faceted filtering, and performance optimization.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, Index, func, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.dialects.postgresql import TSVECTOR
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

Base = declarative_base()


class Product(Base):
    """Product model with search-optimized fields."""

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), index=True)
    brand = Column(String(50), index=True)
    price = Column(Float, index=True)
    rating = Column(Float)
    in_stock = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    tags = Column(Text)  # Comma-separated tags

    # PostgreSQL full-text search vector (optional)
    search_vector = Column(TSVECTOR)

    # Composite indexes for common filter combinations
    __table_args__ = (
        Index('idx_category_brand', 'category', 'brand'),
        Index('idx_price_category', 'price', 'category'),
        Index('idx_created_desc', created_at.desc()),
    )


class ProductSearcher:
    """Advanced product search with SQLAlchemy."""

    def __init__(self, session):
        self.session = session

    def search(
        self,
        query: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: str = 'relevance',
        page: int = 1,
        per_page: int = 20,
        include_facets: bool = True
    ) -> Dict[str, Any]:
        """
        Perform product search with filters and facets.

        Args:
            query: Search query text
            filters: Dictionary of filters to apply
            sort_by: Sort order (relevance, price_asc, price_desc, newest, rating)
            page: Page number (1-based)
            per_page: Results per page
            include_facets: Whether to include facet counts

        Returns:
            Dictionary with results, facets, and metadata
        """
        filters = filters or {}

        # Build base query
        base_query = self.session.query(Product)

        # Apply text search
        if query:
            base_query = self._add_text_search(base_query, query)

        # Apply filters
        base_query = self._apply_filters(base_query, filters)

        # Get total count before pagination
        total_count = base_query.count()

        # Apply sorting
        sorted_query = self._apply_sorting(base_query, sort_by, bool(query))

        # Apply pagination
        paginated_query = self._apply_pagination(sorted_query, page, per_page)

        # Execute query
        results = paginated_query.all()

        # Get facets if requested
        facets = {}
        if include_facets:
            facets = self._get_facets(base_query, filters)

        return {
            'results': [self._serialize_product(p) for p in results],
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page,
            'facets': facets
        }

    def _add_text_search(self, query: Query, search_term: str) -> Query:
        """Add full-text search to query."""

        # Check if using PostgreSQL
        if self.session.bind.dialect.name == 'postgresql':
            # Use PostgreSQL full-text search
            search_query = func.plainto_tsquery('english', search_term)

            # Create search vector from multiple fields
            search_vector = func.to_tsvector(
                'english',
                func.coalesce(Product.title, '') + ' ' +
                func.coalesce(Product.description, '') + ' ' +
                func.coalesce(Product.tags, '')
            )

            # Add search condition and ranking
            query = query.filter(search_vector.match(search_query))

            # Add relevance score for sorting
            query = query.add_columns(
                func.ts_rank(search_vector, search_query).label('relevance')
            )
        else:
            # Fallback to LIKE for other databases
            search_pattern = f'%{search_term}%'
            query = query.filter(
                or_(
                    Product.title.ilike(search_pattern),
                    Product.description.ilike(search_pattern),
                    Product.tags.ilike(search_pattern)
                )
            )

        return query

    def _apply_filters(self, query: Query, filters: Dict[str, Any]) -> Query:
        """Apply filters to query."""

        # Category filter
        if 'categories' in filters and filters['categories']:
            query = query.filter(Product.category.in_(filters['categories']))

        # Brand filter
        if 'brands' in filters and filters['brands']:
            query = query.filter(Product.brand.in_(filters['brands']))

        # Price range filter
        if 'min_price' in filters:
            query = query.filter(Product.price >= filters['min_price'])
        if 'max_price' in filters:
            query = query.filter(Product.price <= filters['max_price'])

        # Stock filter
        if filters.get('in_stock'):
            query = query.filter(Product.in_stock == True)

        # Rating filter
        if 'min_rating' in filters:
            query = query.filter(Product.rating >= filters['min_rating'])

        # Date range filter
        if 'date_from' in filters:
            query = query.filter(Product.created_at >= filters['date_from'])
        if 'date_to' in filters:
            query = query.filter(Product.created_at <= filters['date_to'])

        return query

    def _apply_sorting(self, query: Query, sort_by: str, has_search: bool) -> Query:
        """Apply sorting to query."""

        sort_options = {
            'price_asc': Product.price.asc(),
            'price_desc': Product.price.desc(),
            'newest': Product.created_at.desc(),
            'oldest': Product.created_at.asc(),
            'rating': Product.rating.desc(),
        }

        if sort_by == 'relevance' and has_search:
            # Sort by relevance if text search was performed
            if self.session.bind.dialect.name == 'postgresql':
                query = query.order_by(text('relevance DESC'))
            else:
                # Fallback to newest for non-PostgreSQL
                query = query.order_by(Product.created_at.desc())
        elif sort_by in sort_options:
            query = query.order_by(sort_options[sort_by])
        else:
            # Default sort
            query = query.order_by(Product.created_at.desc())

        return query

    def _apply_pagination(self, query: Query, page: int, per_page: int) -> Query:
        """Apply pagination to query."""
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page)

    def _get_facets(self, base_query: Query, active_filters: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Get facet counts for filters."""
        facets = {}

        # Category facets
        category_query = self._get_base_facet_query(base_query, active_filters, 'categories')
        category_facets = category_query.with_entities(
            Product.category,
            func.count(Product.id).label('count')
        ).group_by(Product.category).all()

        facets['categories'] = [
            {'value': cat, 'count': count}
            for cat, count in category_facets if cat
        ]

        # Brand facets
        brand_query = self._get_base_facet_query(base_query, active_filters, 'brands')
        brand_facets = brand_query.with_entities(
            Product.brand,
            func.count(Product.id).label('count')
        ).group_by(Product.brand).all()

        facets['brands'] = [
            {'value': brand, 'count': count}
            for brand, count in brand_facets if brand
        ]

        # Price range facets
        facets['price_ranges'] = self._get_price_range_facets(base_query, active_filters)

        # In stock count
        in_stock_query = self._get_base_facet_query(base_query, active_filters, 'in_stock')
        in_stock_count = in_stock_query.filter(Product.in_stock == True).count()

        facets['availability'] = [
            {'value': 'in_stock', 'count': in_stock_count}
        ]

        return facets

    def _get_base_facet_query(
        self,
        base_query: Query,
        active_filters: Dict[str, Any],
        exclude_filter: str
    ) -> Query:
        """
        Get base query for facet counting, excluding the current filter.
        This ensures facet counts show what would be available if that filter was removed.
        """
        # Clone the base query
        facet_query = base_query

        # Apply all filters except the one we're counting
        filters_to_apply = {k: v for k, v in active_filters.items() if k != exclude_filter}
        return self._apply_filters(self.session.query(Product), filters_to_apply)

    def _get_price_range_facets(self, base_query: Query, active_filters: Dict[str, Any]) -> List[Dict]:
        """Calculate price range facets."""

        # Define price ranges
        ranges = [
            (0, 50, 'Under $50'),
            (50, 100, '$50 - $100'),
            (100, 200, '$100 - $200'),
            (200, 500, '$200 - $500'),
            (500, None, 'Over $500')
        ]

        # Get base query without price filters
        query_without_price = self._get_base_facet_query(
            base_query,
            active_filters,
            'price'
        )

        facets = []
        for min_price, max_price, label in ranges:
            range_query = query_without_price
            range_query = range_query.filter(Product.price >= min_price)
            if max_price:
                range_query = range_query.filter(Product.price < max_price)

            count = range_query.count()
            if count > 0:
                facets.append({
                    'value': f'{min_price}-{max_price or "inf"}',
                    'label': label,
                    'count': count
                })

        return facets

    def _serialize_product(self, product: Product) -> Dict:
        """Serialize product for API response."""
        return {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'category': product.category,
            'brand': product.brand,
            'price': product.price,
            'rating': product.rating,
            'in_stock': product.in_stock,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'tags': product.tags.split(',') if product.tags else []
        }


class SearchOptimizer:
    """Query optimization utilities."""

    @staticmethod
    def explain_query(session, query: Query) -> str:
        """Get query execution plan (PostgreSQL)."""
        if session.bind.dialect.name != 'postgresql':
            return "EXPLAIN only available for PostgreSQL"

        sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
        result = session.execute(f"EXPLAIN ANALYZE {sql}")
        return '\n'.join([row[0] for row in result])

    @staticmethod
    def add_search_indexes(engine):
        """Create optimized indexes for search."""

        with engine.connect() as conn:
            # Full-text search index (PostgreSQL)
            if engine.dialect.name == 'postgresql':
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_product_search_vector
                    ON products
                    USING GIN(to_tsvector('english',
                        COALESCE(title, '') || ' ' ||
                        COALESCE(description, '') || ' ' ||
                        COALESCE(tags, '')
                    ))
                """)

            # Standard indexes for filtering
            conn.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_products_price ON products(price)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_products_in_stock ON products(in_stock)")

            conn.commit()


# Usage Example
if __name__ == '__main__':
    # Setup database
    engine = create_engine('postgresql://user:pass@localhost/shop')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables and indexes
    Base.metadata.create_all(engine)
    SearchOptimizer.add_search_indexes(engine)

    # Initialize searcher
    searcher = ProductSearcher(session)

    # Perform search
    results = searcher.search(
        query='laptop',
        filters={
            'categories': ['Electronics', 'Computers'],
            'min_price': 500,
            'max_price': 2000,
            'in_stock': True
        },
        sort_by='price_asc',
        page=1,
        per_page=20,
        include_facets=True
    )

    print(f"Found {results['total']} products")
    print(f"Page {results['page']} of {results['total_pages']}")
    print(f"Facets: {results['facets']}")