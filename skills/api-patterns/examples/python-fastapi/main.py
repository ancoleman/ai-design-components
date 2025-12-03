"""
FastAPI Complete REST API Example

Demonstrates:
- Automatic OpenAPI documentation
- Pydantic v2 validation
- Cursor-based pagination
- Rate limiting
- Error handling
- CORS configuration
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Items API",
    description="REST API for managing items with pagination and rate limiting",
    version="1.0.0",
    openapi_tags=[
        {"name": "items", "description": "Item operations"},
        {"name": "health", "description": "Health check"}
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Models
class ItemBase(BaseModel):
    """Base item model"""
    name: str = Field(..., min_length=1, max_length=100, example="Widget")
    description: str = Field(..., max_length=500, example="A useful widget")
    price: float = Field(..., gt=0, example=29.99)


class ItemCreate(ItemBase):
    """Model for creating items"""
    pass


class Item(ItemBase):
    """Complete item model with ID"""
    id: str = Field(..., example="item_123")
    created_at: datetime = Field(..., example="2025-12-02T10:00:00Z")

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """Paginated response model"""
    items: list[Item]
    next_cursor: Optional[str] = None
    has_more: bool


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str


# In-memory database (replace with real database)
ITEMS_DB: dict[str, dict] = {
    "1": {
        "id": "1",
        "name": "Widget A",
        "description": "First widget",
        "price": 19.99,
        "created_at": datetime.now()
    },
    "2": {
        "id": "2",
        "name": "Widget B",
        "description": "Second widget",
        "price": 29.99,
        "created_at": datetime.now()
    }
}


# Routes
@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    response_description="Service health status"
)
async def health_check():
    """
    Check if the service is running.

    Returns a simple status message.
    """
    return {"status": "healthy", "timestamp": datetime.now()}


@app.get(
    "/items",
    tags=["items"],
    response_model=PaginatedResponse,
    summary="List items with cursor pagination",
    response_description="Paginated list of items"
)
@limiter.limit("100/minute")
async def list_items(
    cursor: Optional[str] = Query(
        None,
        description="Cursor for pagination (ID of last item from previous page)"
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Number of items per page"
    )
):
    """
    Retrieve paginated list of items.

    Uses cursor-based pagination for scalability:
    - **cursor**: ID of last item from previous page (omit for first page)
    - **limit**: Number of items to return (max 100)

    Returns:
    - **items**: List of item objects
    - **next_cursor**: Cursor for next page (null if no more pages)
    - **has_more**: Boolean indicating if more pages exist
    """
    # Convert dict to sorted list
    all_items = sorted(
        ITEMS_DB.values(),
        key=lambda x: x["id"]
    )

    # Apply cursor filter
    if cursor:
        all_items = [item for item in all_items if item["id"] > cursor]

    # Check if more results exist
    has_more = len(all_items) > limit
    items = all_items[:limit]

    # Next cursor is last item's ID
    next_cursor = items[-1]["id"] if items and has_more else None

    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more
    }


@app.get(
    "/items/{item_id}",
    tags=["items"],
    response_model=Item,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Item not found"
        }
    },
    summary="Get item by ID"
)
async def get_item(item_id: str):
    """
    Retrieve a specific item by ID.

    - **item_id**: Unique identifier of the item

    Raises:
    - **404**: Item not found
    """
    item = ITEMS_DB.get(item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with id '{item_id}' not found"
        )

    return item


@app.post(
    "/items",
    tags=["items"],
    response_model=Item,
    status_code=201,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Validation error"
        }
    },
    summary="Create new item"
)
@limiter.limit("10/minute")
async def create_item(item: ItemCreate):
    """
    Create a new item.

    Request body:
    - **name**: Item name (1-100 characters)
    - **description**: Item description (max 500 characters)
    - **price**: Item price (must be positive)

    Returns the created item with generated ID and timestamp.
    """
    # Generate new ID
    new_id = str(len(ITEMS_DB) + 1)

    # Create item
    new_item = {
        "id": new_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "created_at": datetime.now()
    }

    ITEMS_DB[new_id] = new_item

    return new_item


@app.put(
    "/items/{item_id}",
    tags=["items"],
    response_model=Item,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Item not found"
        }
    },
    summary="Update item"
)
async def update_item(item_id: str, item: ItemCreate):
    """
    Update an existing item.

    - **item_id**: ID of item to update

    Request body contains new values for all fields.

    Raises:
    - **404**: Item not found
    """
    if item_id not in ITEMS_DB:
        raise HTTPException(
            status_code=404,
            detail=f"Item with id '{item_id}' not found"
        )

    # Update item
    ITEMS_DB[item_id].update({
        "name": item.name,
        "description": item.description,
        "price": item.price
    })

    return ITEMS_DB[item_id]


@app.delete(
    "/items/{item_id}",
    tags=["items"],
    status_code=204,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Item not found"
        }
    },
    summary="Delete item"
)
async def delete_item(item_id: str):
    """
    Delete an item.

    - **item_id**: ID of item to delete

    Raises:
    - **404**: Item not found
    """
    if item_id not in ITEMS_DB:
        raise HTTPException(
            status_code=404,
            detail=f"Item with id '{item_id}' not found"
        )

    del ITEMS_DB[item_id]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

# Automatic documentation available at:
# - http://localhost:8000/docs (Swagger UI)
# - http://localhost:8000/redoc (ReDoc)
# - http://localhost:8000/openapi.json (OpenAPI spec)
