"""
FastAPI search endpoint implementation with validation and caching.

This example shows how to build a production-ready search API with FastAPI,
including request validation, response caching, and error handling.
"""

from fastapi import FastAPI, Query, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import hashlib
import json
import time
from functools import lru_cache

app = FastAPI(title="Product Search API", version="1.0.0")


# Enums and Models
class SortOrder(str, Enum):
    """Available sort orders."""
    relevance = "relevance"
    price_asc = "price_asc"
    price_desc = "price_desc"
    newest = "newest"
    oldest = "oldest"
    rating = "rating"


class SearchFilters(BaseModel):
    """Search filter model with validation."""

    categories: Optional[List[str]] = Field(None, max_items=20, description="Product categories")
    brands: Optional[List[str]] = Field(None, max_items=20, description="Product brands")
    min_price: Optional[float] = Field(None, ge=0, le=1000000, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, le=1000000, description="Maximum price")
    in_stock: Optional[bool] = Field(None, description="Only show in-stock items")
    min_rating: Optional[float] = Field(None, ge=1, le=5, description="Minimum rating")

    @validator('max_price')
    def validate_price_range(cls, v, values):
        """Ensure max_price >= min_price."""
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v < values['min_price']:
                raise ValueError('max_price must be greater than or equal to min_price')
        return v


class SearchRequest(BaseModel):
    """Search request model for POST endpoint."""

    query: Optional[str] = Field(None, min_length=1, max_length=200, description="Search query")
    filters: Optional[SearchFilters] = Field(None, description="Search filters")
    sort_by: SortOrder = Field(SortOrder.relevance, description="Sort order")
    page: int = Field(1, ge=1, le=100, description="Page number")
    per_page: int = Field(20, ge=1, le=100, description="Results per page")
    include_facets: bool = Field(True, description="Include facet counts")


class Product(BaseModel):
    """Product model."""

    id: str
    title: str
    description: Optional[str]
    category: str
    brand: str
    price: float
    rating: Optional[float]
    in_stock: bool
    image_url: Optional[str]
    created_at: datetime


class Facet(BaseModel):
    """Facet item model."""

    value: str
    count: int
    label: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response model."""

    products: List[Product]
    total: int
    page: int
    per_page: int
    total_pages: int
    facets: Optional[Dict[str, List[Facet]]] = None
    query_time_ms: float
    cached: bool = False


# Cache Implementation
class SearchCache:
    """Simple in-memory cache for search results."""

    def __init__(self, ttl: int = 300, max_size: int = 100):
        self.cache: Dict[str, tuple] = {}
        self.ttl = ttl
        self.max_size = max_size

    def get_key(self, params: dict) -> str:
        """Generate cache key from search parameters."""
        # Sort keys for consistent hashing
        sorted_params = json.dumps(params, sort_keys=True, default=str)
        return hashlib.md5(sorted_params.encode()).hexdigest()

    def get(self, params: dict) -> Optional[dict]:
        """Get cached result if available and not expired."""
        key = self.get_key(params)

        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return result

            # Expired, remove from cache
            del self.cache[key]

        return None

    def set(self, params: dict, result: dict):
        """Cache search result."""
        # Check cache size limit
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        key = self.get_key(params)
        self.cache[key] = (result, time.time())

    def clear(self):
        """Clear all cached results."""
        self.cache.clear()


# Initialize cache
search_cache = SearchCache(ttl=300, max_size=100)


# Dependency Injection
async def get_search_service():
    """Dependency to get search service."""
    # In production, this would return your actual search service
    # For example, database session, Elasticsearch client, etc.
    return MockSearchService()


# Mock Search Service (replace with actual implementation)
class MockSearchService:
    """Mock search service for demonstration."""

    async def search(self, request: SearchRequest) -> Dict[str, Any]:
        """Perform mock search."""
        # Simulate some processing time
        await asyncio.sleep(0.1)

        # Mock products
        products = [
            {
                "id": f"prod_{i}",
                "title": f"Product {i}",
                "description": f"Description for product {i}",
                "category": "Electronics",
                "brand": "BrandX",
                "price": 100.0 + i * 10,
                "rating": 4.5,
                "in_stock": True,
                "image_url": f"https://example.com/product_{i}.jpg",
                "created_at": datetime.utcnow()
            }
            for i in range(1, 21)
        ]

        # Mock facets
        facets = {
            "categories": [
                {"value": "Electronics", "count": 150},
                {"value": "Computers", "count": 75},
                {"value": "Accessories", "count": 50}
            ],
            "brands": [
                {"value": "BrandX", "count": 100},
                {"value": "BrandY", "count": 80},
                {"value": "BrandZ", "count": 45}
            ],
            "price_ranges": [
                {"value": "0-50", "label": "Under $50", "count": 30},
                {"value": "50-100", "label": "$50-$100", "count": 45},
                {"value": "100-200", "label": "$100-$200", "count": 60},
                {"value": "200-inf", "label": "Over $200", "count": 40}
            ]
        }

        return {
            "products": products,
            "total": 175,
            "facets": facets if request.include_facets else None
        }


# API Endpoints
@app.get("/api/v1/search", response_model=SearchResponse, summary="Search products (GET)")
async def search_get(
    q: Optional[str] = Query(None, min_length=1, max_length=200, description="Search query"),
    category: Optional[List[str]] = Query(None, description="Filter by categories"),
    brand: Optional[List[str]] = Query(None, description="Filter by brands"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    in_stock: Optional[bool] = Query(None, description="Only in-stock items"),
    sort: SortOrder = Query(SortOrder.relevance, description="Sort order"),
    page: int = Query(1, ge=1, le=100, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Results per page"),
    include_facets: bool = Query(True, description="Include facet counts"),
    service: MockSearchService = Depends(get_search_service)
):
    """
    Search products using query parameters.

    This endpoint is suitable for simple searches that can be expressed in URL parameters.
    """
    start_time = time.time()

    # Build search request
    search_request = SearchRequest(
        query=q,
        filters=SearchFilters(
            categories=category,
            brands=brand,
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock
        ),
        sort_by=sort,
        page=page,
        per_page=per_page,
        include_facets=include_facets
    )

    # Check cache
    cache_params = search_request.dict()
    cached_result = search_cache.get(cache_params)

    if cached_result:
        query_time = (time.time() - start_time) * 1000
        return SearchResponse(
            **cached_result,
            query_time_ms=query_time,
            cached=True
        )

    # Perform search
    try:
        results = await service.search(search_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    # Calculate pagination
    total_pages = (results['total'] + per_page - 1) // per_page

    # Build response
    response_data = {
        "products": results['products'],
        "total": results['total'],
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "facets": results.get('facets')
    }

    # Cache result
    search_cache.set(cache_params, response_data)

    query_time = (time.time() - start_time) * 1000
    return SearchResponse(
        **response_data,
        query_time_ms=query_time,
        cached=False
    )


@app.post("/api/v1/search", response_model=SearchResponse, summary="Search products (POST)")
async def search_post(
    request: SearchRequest,
    service: MockSearchService = Depends(get_search_service)
):
    """
    Search products using request body.

    This endpoint is suitable for complex searches with many filters or when the query
    might exceed URL length limits.
    """
    start_time = time.time()

    # Check cache
    cache_params = request.dict()
    cached_result = search_cache.get(cache_params)

    if cached_result:
        query_time = (time.time() - start_time) * 1000
        return SearchResponse(
            **cached_result,
            query_time_ms=query_time,
            cached=True
        )

    # Perform search
    try:
        results = await service.search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    # Calculate pagination
    total_pages = (results['total'] + request.per_page - 1) // request.per_page

    # Build response
    response_data = {
        "products": results['products'],
        "total": results['total'],
        "page": request.page,
        "per_page": request.per_page,
        "total_pages": total_pages,
        "facets": results.get('facets')
    }

    # Cache result
    search_cache.set(cache_params, response_data)

    query_time = (time.time() - start_time) * 1000
    return SearchResponse(
        **response_data,
        query_time_ms=query_time,
        cached=False
    )


@app.get("/api/v1/autocomplete", summary="Get search suggestions")
async def autocomplete(
    q: str = Query(..., min_length=2, max_length=50, description="Query prefix"),
    limit: int = Query(10, ge=1, le=20, description="Number of suggestions"),
    service: MockSearchService = Depends(get_search_service)
):
    """
    Get autocomplete suggestions for search input.

    Returns suggestions based on the provided query prefix.
    """
    # Mock autocomplete suggestions
    suggestions = [
        {
            "text": f"{q} suggestion {i}",
            "category": "Electronics" if i % 2 == 0 else "Computers",
            "type": "product" if i < 5 else "category"
        }
        for i in range(1, min(limit + 1, 11))
    ]

    return {
        "query": q,
        "suggestions": suggestions
    }


@app.delete("/api/v1/cache", summary="Clear search cache")
async def clear_cache():
    """
    Clear the search result cache.

    This endpoint should be protected in production.
    """
    search_cache.clear()
    return {"message": "Cache cleared successfully"}


@app.get("/api/v1/health", summary="Health check")
async def health_check():
    """
    Check if the search service is healthy.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "cache_size": len(search_cache.cache),
        "version": "1.0.0"
    }


# Error Handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid input",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request failed",
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all search requests."""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Log request details
    process_time = time.time() - start_time

    # In production, use proper logging
    if request.url.path.startswith("/api/v1/search"):
        print(f"Search request: {request.url.path}")
        print(f"Query params: {request.url.query}")
        print(f"Process time: {process_time:.3f}s")

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)