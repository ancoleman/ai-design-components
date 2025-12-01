# FastAPI Routing Patterns

## Table of Contents
- [Basic Routing](#basic-routing)
- [Router Organization](#router-organization)
- [Path Parameters & Validation](#path-parameters--validation)
- [Dependencies & Middleware](#dependencies--middleware)
- [WebSocket Routes](#websocket-routes)
- [API Versioning](#api-versioning)

## Basic Routing

### Simple Route Definitions

```python
from fastapi import FastAPI, Query, Path, Body, Header, Cookie
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Basic routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Multiple HTTP methods
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """Get item by ID."""
    return {"item_id": item_id}

@app.post("/items")
async def create_item(item: dict = Body(...)):
    """Create new item."""
    return {"created": item}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: dict = Body(...)):
    """Update existing item."""
    return {"updated": item_id, "item": item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete item."""
    return {"deleted": item_id}

# Response model
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool = True

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item_with_model(item_id: int) -> ItemResponse:
    """Get item with response model."""
    # Fetch from database
    item = await fetch_item(item_id)
    return ItemResponse(**item)
```

### Request Body Models

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0, le=1000000)
    category: ProductCategory
    tags: List[str] = []
    in_stock: bool = True

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError('Too many tags (max 10)')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 999.99,
                "category": "electronics",
                "tags": ["computer", "portable"],
                "in_stock": True
            }
        }

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0, le=1000000)
    category: Optional[ProductCategory] = None
    tags: Optional[List[str]] = None
    in_stock: Optional[bool] = None

@app.post("/products", response_model=Product, status_code=201)
async def create_product(product: Product):
    """Create new product."""
    # Save to database
    saved_product = await save_product(product.dict())
    return saved_product

@app.patch("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, updates: ProductUpdate):
    """Partially update product."""
    # Update only provided fields
    update_data = updates.dict(exclude_unset=True)
    updated_product = await update_product_db(product_id, update_data)
    return updated_product
```

## Router Organization

### Modular Router Structure

```python
# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(User):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=User, status_code=201)
async def register(user: UserCreate):
    """Register new user."""
    # Hash password and save user
    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    new_user = await create_user(user_dict)
    return User(**new_user)

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token."""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = await get_user(username=username)
    if user is None:
        raise credentials_exception

    return User(**user)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user
```

```python
# routers/products.py
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

class ProductFilters:
    """Dependency for product filtering."""
    def __init__(
        self,
        category: Optional[str] = Query(None, description="Filter by category"),
        min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
        max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
        search: Optional[str] = Query(None, description="Search in name and description"),
        sort: str = Query("created_at", regex="^(price|name|created_at)$"),
        order: str = Query("desc", regex="^(asc|desc)$"),
        page: int = Query(1, ge=1),
        per_page: int = Query(20, ge=1, le=100)
    ):
        self.category = category
        self.min_price = min_price
        self.max_price = max_price
        self.search = search
        self.sort = sort
        self.order = order
        self.page = page
        self.per_page = per_page

@router.get("/", response_model=List[Product])
async def get_products(
    filters: ProductFilters = Depends(),
    db: Session = Depends(get_db)
):
    """Get products with filtering and pagination."""
    query = db.query(ProductModel)

    if filters.category:
        query = query.filter(ProductModel.category == filters.category)

    if filters.min_price:
        query = query.filter(ProductModel.price >= filters.min_price)

    if filters.max_price:
        query = query.filter(ProductModel.price <= filters.max_price)

    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            ProductModel.name.ilike(search_term) |
            ProductModel.description.ilike(search_term)
        )

    # Sorting
    sort_column = getattr(ProductModel, filters.sort)
    if filters.order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    # Pagination
    offset = (filters.page - 1) * filters.per_page
    products = query.offset(offset).limit(filters.per_page).all()

    return products

@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get single product."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

```python
# main.py - Main application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, products, orders, admin

app = FastAPI(title="E-commerce API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(
    admin.router,
    prefix="/admin",
    dependencies=[Depends(require_admin)]
)

@app.on_event("startup")
async def startup_event():
    """Initialize database and other resources."""
    await init_database()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources."""
    await close_database()
```

## Path Parameters & Validation

### Advanced Path Parameters

```python
from fastapi import Path, Query, HTTPException
from typing import Optional
from datetime import date

@app.get("/users/{user_id}")
async def read_user(
    user_id: int = Path(..., gt=0, description="The ID of the user"),
):
    """Get user by ID with validation."""
    return {"user_id": user_id}

@app.get("/posts/{year}/{month}/{day}/{slug}")
async def read_post(
    year: int = Path(..., ge=2000, le=2100),
    month: int = Path(..., ge=1, le=12),
    day: int = Path(..., ge=1, le=31),
    slug: str = Path(..., regex="^[a-z0-9]+(?:-[a-z0-9]+)*$")
):
    """Get blog post by date and slug."""
    post_date = date(year, month, day)
    post = await get_post_by_date_and_slug(post_date, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Multiple path parameters with validation
@app.get("/categories/{category}/items/{item_id}")
async def read_category_item(
    category: str = Path(..., min_length=1, max_length=50),
    item_id: int = Path(..., gt=0),
    q: Optional[str] = Query(None, max_length=50)
):
    """Get item in specific category."""
    return {
        "category": category,
        "item_id": item_id,
        "q": q
    }

# Enum path parameters
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """Get ML model by name."""
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

### Query Parameters

```python
from typing import List, Optional
from fastapi import Query

@app.get("/items/")
async def read_items(
    # Required query parameter
    q: str = Query(..., min_length=3, max_length=50, description="Search query"),

    # Optional with default
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),

    # List query parameters
    tags: List[str] = Query([], description="Filter by tags"),

    # Alias for query parameter
    sort_by: str = Query("created_at", alias="sort-by"),

    # Deprecated parameter
    old_param: Optional[str] = Query(None, deprecated=True),

    # Regular expression validation
    item_id: Optional[str] = Query(None, regex="^[A-Z]{2}[0-9]{4}$")
):
    """Read items with complex query parameters."""
    results = {
        "q": q,
        "skip": skip,
        "limit": limit,
        "tags": tags,
        "sort_by": sort_by
    }

    if old_param:
        results["warning"] = "old_param is deprecated"

    return results
```

## Dependencies & Middleware

### Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from typing import Optional, Annotated

# Database dependency
async def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependencies
async def get_token_header(x_token: str = Header(...)):
    """Validate token header."""
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-Token header"
        )

class RoleChecker:
    """Check user role dependency."""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return user

# Rate limiting dependency
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, calls: int = 10, period: int = 60):
        self.calls = calls
        self.period = timedelta(seconds=period)
        self.calls_made = defaultdict(list)

    async def __call__(self, request: Request):
        client_ip = request.client.host
        now = datetime.now()

        # Clean old calls
        self.calls_made[client_ip] = [
            call_time for call_time in self.calls_made[client_ip]
            if call_time > now - self.period
        ]

        if len(self.calls_made[client_ip]) >= self.calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )

        self.calls_made[client_ip].append(now)

# Using dependencies
@app.get("/admin/users", dependencies=[Depends(RoleChecker(["admin"]))])
async def get_all_users(
    db: Session = Depends(get_db),
    rate_limit: None = Depends(RateLimiter(calls=5, period=60))
):
    """Get all users - admin only."""
    return db.query(User).all()

# Dependency with sub-dependencies
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Get current active user."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Get current user's items."""
    return [{"item_id": "Foo", "owner": current_user.username}]
```

### Middleware

```python
from fastapi import Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

# Custom middleware
class TimingMiddleware(BaseHTTPMiddleware):
    """Measure request processing time."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        # Log slow requests
        if process_time > 1.0:
            logging.warning(f"Slow request: {request.url.path} took {process_time:.2f}s")

        return response

class AuthMiddleware(BaseHTTPMiddleware):
    """Check authentication for protected routes."""

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        public_paths = ["/", "/health", "/docs", "/redoc", "/openapi.json"]
        if request.url.path in public_paths or request.url.path.startswith("/auth"):
            return await call_next(request)

        # Check for API key or token
        api_key = request.headers.get("X-API-Key")
        auth_header = request.headers.get("Authorization")

        if not api_key and not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required"}
            )

        return await call_next(request)

# Add middleware to app
app.add_middleware(TimingMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)
```

## WebSocket Routes

### WebSocket Endpoints

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json

class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: Optional[str] = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: Optional[str] = None):
        self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_to_user(self, message: str, user_id: str):
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Basic WebSocket endpoint."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client left the chat")

@app.websocket("/ws/chat/{room_id}")
async def chat_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: Optional[str] = Query(None)
):
    """Chat room WebSocket."""
    # Authenticate user
    user = await authenticate_websocket(token)
    if not user:
        await websocket.close(code=1008, reason="Authentication failed")
        return

    await websocket.accept()

    # Join room
    await join_room(room_id, user.id, websocket)

    try:
        while True:
            message = await websocket.receive_json()

            # Process message
            if message["type"] == "chat":
                await broadcast_to_room(
                    room_id,
                    {
                        "type": "message",
                        "user": user.username,
                        "text": message["text"],
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
            elif message["type"] == "typing":
                await broadcast_to_room(
                    room_id,
                    {
                        "type": "typing",
                        "user": user.username
                    },
                    exclude=websocket
                )

    except WebSocketDisconnect:
        await leave_room(room_id, user.id)
        await broadcast_to_room(
            room_id,
            {
                "type": "user_left",
                "user": user.username
            }
        )
```

## API Versioning

### Version-Based Routing

```python
# api/v1/routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.get("/users")
async def get_users_v1():
    """V1 users endpoint."""
    return {"version": "1.0", "users": []}

# api/v2/routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v2")

@router.get("/users")
async def get_users_v2():
    """V2 users endpoint with pagination."""
    return {
        "version": "2.0",
        "users": [],
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 0
        }
    }

# main.py
from api.v1 import routes as v1_routes
from api.v2 import routes as v2_routes

app = FastAPI()

# Include versioned routers
app.include_router(v1_routes.router, tags=["v1"])
app.include_router(v2_routes.router, tags=["v2"])

# Header-based versioning
from fastapi import Header

@app.get("/users")
async def get_users(
    api_version: str = Header(None, alias="X-API-Version")
):
    """Version selection via header."""
    if api_version == "2.0":
        return await get_users_v2()
    else:
        # Default to v1
        return await get_users_v1()

# Accept header versioning
@app.get("/products")
async def get_products(
    accept: str = Header(None)
):
    """Version via Accept header."""
    if accept and "version=2" in accept:
        return {"version": "2.0", "products": []}
    return {"version": "1.0", "products": []}
```

### Deprecation Handling

```python
from warnings import warn
from functools import wraps

def deprecated(version: str, alternative: str = None):
    """Decorator to mark endpoints as deprecated."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            warning_msg = f"Endpoint {func.__name__} is deprecated as of version {version}"
            if alternative:
                warning_msg += f". Use {alternative} instead."
            warn(warning_msg, DeprecationWarning, stacklevel=2)

            # Add deprecation header to response
            response = await func(*args, **kwargs)
            if isinstance(response, dict):
                response = JSONResponse(
                    content=response,
                    headers={
                        "X-API-Deprecation": f"version={version}",
                        "X-API-Deprecation-Alternative": alternative or ""
                    }
                )
            return response
        return wrapper
    return decorator

@app.get("/old-endpoint")
@deprecated(version="2.0", alternative="/new-endpoint")
async def old_endpoint():
    """Deprecated endpoint."""
    return {"message": "This endpoint is deprecated"}
```