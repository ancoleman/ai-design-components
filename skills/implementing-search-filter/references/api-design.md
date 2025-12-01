# Search API Design Patterns

## RESTful Search Endpoints

### Basic Search API Design
```python
from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

app = FastAPI()

class SearchFilters(BaseModel):
    """Validated search filters."""
    category: Optional[List[str]] = Field(None, description="Filter by categories")
    brand: Optional[List[str]] = Field(None, description="Filter by brands")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    in_stock: Optional[bool] = Field(None, description="Only in-stock items")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")

    @validator('max_price')
    def validate_price_range(cls, v, values):
        if v and 'min_price' in values and values['min_price']:
            if v < values['min_price']:
                raise ValueError('max_price must be greater than min_price')
        return v

class SearchRequest(BaseModel):
    """Search request body for POST requests."""
    query: Optional[str] = Field(None, min_length=1, max_length=200)
    filters: Optional[SearchFilters] = None
    sort_by: Optional[str] = Field('relevance', regex='^(relevance|price_asc|price_desc|newest|rating)$')
    page: int = Field(1, ge=1, le=100)
    size: int = Field(20, ge=1, le=100)
    include_facets: bool = Field(True, description="Include facet counts")

class SearchResponse(BaseModel):
    """Search response structure."""
    total: int
    page: int
    size: int
    items: List[Dict[str, Any]]
    facets: Optional[Dict[str, List[Dict]]] = None
    query_time_ms: float

    class Config:
        json_schema_extra = {
            "example": {
                "total": 150,
                "page": 1,
                "size": 20,
                "items": [...],
                "facets": {
                    "category": [
                        {"value": "Electronics", "count": 45},
                        {"value": "Books", "count": 32}
                    ]
                },
                "query_time_ms": 125.5
            }
        }

# GET endpoint for simple searches
@app.get("/api/v1/search", response_model=SearchResponse)
async def search_get(
    q: Optional[str] = Query(None, min_length=1, max_length=200, description="Search query"),
    category: Optional[List[str]] = Query(None, description="Categories filter"),
    brand: Optional[List[str]] = Query(None, description="Brands filter"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    in_stock: Optional[bool] = Query(None, description="Stock filter"),
    sort: str = Query('relevance', regex='^(relevance|price_asc|price_desc|newest|rating)$'),
    page: int = Query(1, ge=1, le=100),
    size: int = Query(20, ge=1, le=100)
):
    """
    Search products with query and filters.

    - **q**: Search query text
    - **category**: Filter by categories (multiple allowed)
    - **brand**: Filter by brands (multiple allowed)
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **in_stock**: Show only in-stock items
    - **sort**: Sort order
    - **page**: Page number (1-based)
    - **size**: Results per page
    """

    # Build filters
    filters = SearchFilters(
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )

    # Execute search
    results = await perform_search(
        query=q,
        filters=filters,
        sort_by=sort,
        page=page,
        size=size
    )

    return results

# POST endpoint for complex searches
@app.post("/api/v1/search", response_model=SearchResponse)
async def search_post(request: SearchRequest):
    """
    Advanced search with complex filters.

    Accepts a JSON body with search parameters.
    Useful for complex queries that exceed URL length limits.
    """

    results = await perform_search(
        query=request.query,
        filters=request.filters,
        sort_by=request.sort_by,
        page=request.page,
        size=request.size,
        include_facets=request.include_facets
    )

    return results
```

### Autocomplete API
```python
class AutocompleteResponse(BaseModel):
    """Autocomplete suggestions response."""
    suggestions: List[Dict[str, Any]]
    query_time_ms: float

@app.get("/api/v1/autocomplete", response_model=AutocompleteResponse)
async def autocomplete(
    q: str = Query(..., min_length=2, max_length=50, description="Query prefix"),
    size: int = Query(10, ge=1, le=20, description="Number of suggestions"),
    include_categories: bool = Query(False, description="Include category in suggestions")
):
    """
    Get autocomplete suggestions for search input.

    Returns suggestions based on partial query match.
    Optimized for real-time typeahead functionality.
    """

    import time
    start_time = time.time()

    # Get suggestions from search backend
    suggestions = await get_autocomplete_suggestions(
        prefix=q,
        size=size,
        include_categories=include_categories
    )

    query_time_ms = (time.time() - start_time) * 1000

    return AutocompleteResponse(
        suggestions=suggestions,
        query_time_ms=query_time_ms
    )
```

## Advanced Query Parameters

### Query DSL Support
```python
from typing import Union
import json

class QueryDSL(BaseModel):
    """Domain Specific Language for complex queries."""

    # Boolean operators
    must: Optional[List[Union[str, Dict]]] = None
    should: Optional[List[Union[str, Dict]]] = None
    must_not: Optional[List[Union[str, Dict]]] = None

    # Field-specific queries
    fields: Optional[Dict[str, Any]] = None

    # Advanced options
    fuzzy: Optional[bool] = False
    boost: Optional[Dict[str, float]] = None
    minimum_should_match: Optional[int] = None

@app.post("/api/v1/search/advanced")
async def advanced_search(
    query_dsl: QueryDSL,
    filters: Optional[SearchFilters] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
):
    """
    Execute advanced search with query DSL.

    Supports boolean logic, field-specific queries, and boosting.

    Example query DSL:
    ```json
    {
        "must": ["laptop"],
        "should": ["gaming", "professional"],
        "must_not": ["refurbished"],
        "fields": {
            "brand": "dell",
            "category": "computers"
        },
        "fuzzy": true,
        "boost": {
            "title": 2.0,
            "description": 1.5
        }
    }
    ```
    """

    # Build and execute complex query
    results = await execute_dsl_query(
        dsl=query_dsl,
        filters=filters,
        page=page,
        size=size
    )

    return results
```

### GraphQL Search Schema
```python
import strawberry
from typing import Optional, List

@strawberry.type
class Product:
    id: str
    title: str
    description: str
    price: float
    category: str
    brand: str
    rating: Optional[float]
    in_stock: bool

@strawberry.type
class SearchResult:
    total: int
    items: List[Product]
    facets: Optional[str]  # JSON string of facets

@strawberry.input
class SearchInput:
    query: Optional[str] = None
    category: Optional[List[str]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: str = "relevance"
    page: int = 1
    size: int = 20

@strawberry.type
class Query:
    @strawberry.field
    async def search(self, input: SearchInput) -> SearchResult:
        """GraphQL search endpoint."""
        results = await perform_search(
            query=input.query,
            filters={
                'category': input.category,
                'min_price': input.min_price,
                'max_price': input.max_price
            },
            sort_by=input.sort_by,
            page=input.page,
            size=input.size
        )

        return SearchResult(
            total=results['total'],
            items=[Product(**item) for item in results['items']],
            facets=json.dumps(results.get('facets', {}))
        )

schema = strawberry.Schema(query=Query)
```

## Pagination Strategies

### Offset-Based Pagination
```python
class OffsetPagination:
    """Traditional offset-based pagination."""

    @staticmethod
    def paginate(
        query,
        page: int = 1,
        per_page: int = 20,
        max_per_page: int = 100
    ):
        """Apply offset pagination to query."""
        # Validate inputs
        page = max(1, page)
        per_page = min(max_per_page, max(1, per_page))

        # Calculate offset
        offset = (page - 1) * per_page

        # Get total count
        total = query.count()

        # Apply pagination
        items = query.offset(offset).limit(per_page).all()

        # Calculate metadata
        total_pages = (total + per_page - 1) // per_page
        has_next = page < total_pages
        has_prev = page > 1

        return {
            'items': items,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': has_next,
            'has_prev': has_prev,
            'next_page': page + 1 if has_next else None,
            'prev_page': page - 1 if has_prev else None
        }
```

### Cursor-Based Pagination
```python
import base64
from datetime import datetime

class CursorPagination:
    """Cursor-based pagination for real-time data."""

    @staticmethod
    def encode_cursor(position: Dict) -> str:
        """Encode position as cursor."""
        cursor_data = json.dumps(position, default=str)
        return base64.b64encode(cursor_data.encode()).decode()

    @staticmethod
    def decode_cursor(cursor: str) -> Dict:
        """Decode cursor to position."""
        try:
            cursor_data = base64.b64decode(cursor.encode()).decode()
            return json.loads(cursor_data)
        except:
            raise ValueError("Invalid cursor")

    @staticmethod
    def paginate_with_cursor(
        query,
        cursor: Optional[str] = None,
        limit: int = 20,
        order_by: str = 'created_at'
    ):
        """Apply cursor pagination."""

        # Decode cursor if provided
        if cursor:
            position = CursorPagination.decode_cursor(cursor)
            query = query.filter(
                getattr(Product, order_by) > position[order_by]
            )

        # Order and limit
        query = query.order_by(getattr(Product, order_by))
        items = query.limit(limit + 1).all()

        # Check if there are more items
        has_next = len(items) > limit
        if has_next:
            items = items[:-1]  # Remove extra item

        # Create next cursor
        next_cursor = None
        if items and has_next:
            last_item = items[-1]
            next_cursor = CursorPagination.encode_cursor({
                order_by: getattr(last_item, order_by)
            })

        return {
            'items': items,
            'next_cursor': next_cursor,
            'has_next': has_next
        }

@app.get("/api/v1/search/cursor")
async def search_with_cursor(
    q: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """Search with cursor-based pagination."""

    results = await search_with_cursor_pagination(
        query=q,
        cursor=cursor,
        limit=limit
    )

    return results
```

## Rate Limiting and Caching

### API Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/search")
@limiter.limit("10/second")  # More restrictive limit for search
async def search_rate_limited(
    request: Request,
    q: str = Query(...),
    page: int = 1,
    size: int = 20
):
    """Rate-limited search endpoint."""
    return await perform_search(q, page, size)
```

### Response Caching
```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
import redis

# Initialize cache on startup
@app.on_event("startup")
async def startup():
    redis_client = redis.Redis(host="localhost", port=6379)
    FastAPICache.init(RedisBackend(redis_client), prefix="search-cache:")

@app.get("/api/v1/search")
@cache(expire=300)  # Cache for 5 minutes
async def cached_search(
    q: str,
    category: Optional[List[str]] = None,
    page: int = 1,
    size: int = 20
):
    """Cached search endpoint."""

    # Cache key includes all parameters
    results = await perform_search(
        query=q,
        filters={'category': category},
        page=page,
        size=size
    )

    return results

# Custom cache key generation
def get_cache_key(func, *args, **kwargs):
    """Generate cache key from search parameters."""
    params = {
        'query': kwargs.get('q'),
        'filters': kwargs.get('filters'),
        'page': kwargs.get('page', 1),
        'size': kwargs.get('size', 20)
    }

    # Sort and hash parameters
    import hashlib
    param_str = json.dumps(params, sort_keys=True)
    return f"search:{hashlib.md5(param_str.encode()).hexdigest()}"
```

## Error Handling

### Comprehensive Error Responses
```python
from enum import Enum

class ErrorCode(str, Enum):
    INVALID_QUERY = "INVALID_QUERY"
    INVALID_FILTERS = "INVALID_FILTERS"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"

class ErrorResponse(BaseModel):
    error: ErrorCode
    message: str
    details: Optional[Dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=ErrorCode.INVALID_QUERY,
            message=str(exc),
            details={"path": request.url.path}
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorCode.INTERNAL_ERROR,
            message=exc.detail,
            details={"status_code": exc.status_code}
        ).dict()
    )

# Service health check
@app.get("/api/v1/health")
async def health_check():
    """Check search service health."""
    try:
        # Verify backend connectivity
        await check_elasticsearch_connection()
        await check_database_connection()

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "services": {
                "elasticsearch": "up",
                "database": "up",
                "cache": "up"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="Search service unavailable"
        )
```

## API Documentation

### OpenAPI Specification
```yaml
openapi: 3.0.0
info:
  title: Search API
  version: 1.0.0
  description: Product search and filtering API

paths:
  /api/v1/search:
    get:
      summary: Search products
      parameters:
        - name: q
          in: query
          required: false
          schema:
            type: string
            minLength: 1
            maxLength: 200
          description: Search query

        - name: category
          in: query
          required: false
          schema:
            type: array
            items:
              type: string
          style: form
          explode: true
          description: Filter by categories

        - name: min_price
          in: query
          required: false
          schema:
            type: number
            minimum: 0
          description: Minimum price filter

        - name: max_price
          in: query
          required: false
          schema:
            type: number
            minimum: 0
          description: Maximum price filter

        - name: page
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
          description: Page number

        - name: size
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
          description: Results per page

      responses:
        200:
          description: Search results
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResponse'

        400:
          description: Invalid parameters
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

        429:
          description: Rate limited

        500:
          description: Internal server error

components:
  schemas:
    SearchResponse:
      type: object
      properties:
        total:
          type: integer
          description: Total number of results
        page:
          type: integer
          description: Current page
        size:
          type: integer
          description: Results per page
        items:
          type: array
          items:
            $ref: '#/components/schemas/Product'
        facets:
          type: object
          additionalProperties:
            type: array
            items:
              type: object
              properties:
                value:
                  type: string
                count:
                  type: integer

    Product:
      type: object
      properties:
        id:
          type: string
        title:
          type: string
        description:
          type: string
        price:
          type: number
        category:
          type: string
        brand:
          type: string
        in_stock:
          type: boolean

    ErrorResponse:
      type: object
      properties:
        error:
          type: string
        message:
          type: string
        details:
          type: object
        timestamp:
          type: string
          format: date-time
```