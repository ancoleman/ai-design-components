"""
FastAPI Router Organization
Demonstrates best practices for organizing routes in FastAPI applications.
"""

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

# Main application instance (main.py)
app = FastAPI(
    title="MyApp API",
    version="1.0.0",
    description="API for MyApp with organized routers"
)


# ============================================================================
# AUTHENTICATION ROUTER (auth.py)
# ============================================================================

auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@auth_router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Authenticate user and return access token"""
    # Authentication logic here
    return TokenResponse(access_token="fake-token", token_type="bearer")

@auth_router.post("/logout")
async def logout():
    """Invalidate user session"""
    return {"message": "Successfully logged out"}

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_token():
    """Refresh access token"""
    return TokenResponse(access_token="new-fake-token")


# ============================================================================
# USERS ROUTER (users.py)
# ============================================================================

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)

class User(BaseModel):
    id: int
    email: str
    name: str

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

@users_router.get("/", response_model=List[User])
async def list_users(skip: int = 0, limit: int = 10):
    """List all users with pagination"""
    return [
        User(id=1, email="user@example.com", name="John Doe"),
        User(id=2, email="jane@example.com", name="Jane Smith"),
    ]

@users_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get user by ID"""
    if user_id == 1:
        return User(id=1, email="user@example.com", name="John Doe")
    raise HTTPException(status_code=404, detail="User not found")

@users_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    return User(id=1, email=user.email, name=user.name)

@users_router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    """Update existing user"""
    return User(id=user_id, email=user.email, name=user.name)

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete user"""
    return None


# ============================================================================
# POSTS ROUTER (posts.py)
# ============================================================================

posts_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

class Post(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    published: bool = False

class PostCreate(BaseModel):
    title: str
    content: str

@posts_router.get("/", response_model=List[Post])
async def list_posts(
    skip: int = 0,
    limit: int = 10,
    published: Optional[bool] = None,
):
    """List posts with optional filtering by published status"""
    return [
        Post(id=1, title="First Post", content="Content here", author_id=1, published=True),
    ]

@posts_router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """Get post by ID"""
    return Post(id=post_id, title="Post Title", content="Post content", author_id=1)

@posts_router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    """Create a new post"""
    return Post(id=1, title=post.title, content=post.content, author_id=1)


# ============================================================================
# NESTED RESOURCES (posts/{post_id}/comments)
# ============================================================================

comments_router = APIRouter(
    prefix="/posts/{post_id}/comments",
    tags=["comments"],
)

class Comment(BaseModel):
    id: int
    post_id: int
    content: str
    author_id: int

class CommentCreate(BaseModel):
    content: str

@comments_router.get("/", response_model=List[Comment])
async def list_post_comments(post_id: int):
    """List all comments for a specific post"""
    return [
        Comment(id=1, post_id=post_id, content="Great post!", author_id=2),
    ]

@comments_router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, comment: CommentCreate):
    """Create a comment on a post"""
    return Comment(id=1, post_id=post_id, content=comment.content, author_id=1)


# ============================================================================
# API VERSIONING (api/v1/ and api/v2/)
# ============================================================================

# API v1 router
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(posts_router)

# API v2 router (with breaking changes)
v2_router = APIRouter(prefix="/api/v2")

v2_users_router = APIRouter(
    prefix="/users",
    tags=["users-v2"],
)

class UserV2(BaseModel):
    id: int
    email: str
    full_name: str  # Changed from 'name'
    is_active: bool = True  # New field

@v2_users_router.get("/", response_model=List[UserV2])
async def list_users_v2():
    """List users (API v2 with breaking changes)"""
    return [
        UserV2(id=1, email="user@example.com", full_name="John Doe", is_active=True),
    ]

v2_router.include_router(v2_users_router)


# ============================================================================
# REGISTER ALL ROUTERS
# ============================================================================

# Register versioned API routers
app.include_router(v1_router)
app.include_router(v2_router)

# Additional routers (no versioning)
app.include_router(comments_router)


# ============================================================================
# DEPENDENCY INJECTION PATTERN
# ============================================================================

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency to get current authenticated user"""
    # Verify token and return user
    if token == "fake-token":
        return User(id=1, email="user@example.com", name="John Doe")
    raise HTTPException(status_code=401, detail="Invalid token")

# Protected route using dependency
@app.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information (protected route)"""
    return current_user


# ============================================================================
# ADVANCED ROUTING PATTERNS
# ============================================================================

# Optional path parameters
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    """Item detail with optional query parameter"""
    if q:
        return {"item_id": item_id, "query": q}
    return {"item_id": item_id}

# Enum path parameters
from enum import Enum

class ModelName(str, Enum):
    gpt4 = "gpt-4"
    claude = "claude-3"
    llama = "llama-3"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """Model selection with enum validation"""
    if model_name == ModelName.gpt4:
        return {"model": "GPT-4", "provider": "OpenAI"}
    return {"model": model_name.value}

# File path parameters
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """Read file with path parameter (allows slashes)"""
    return {"file_path": file_path}


# ============================================================================
# BEST PRACTICES SUMMARY
# ============================================================================
"""
1. Use APIRouter for modular organization
2. Group related endpoints with tags
3. Use prefix for common path segments
4. Version APIs (api/v1, api/v2) for breaking changes
5. Use dependencies for authentication/authorization
6. Use Pydantic models for request/response validation
7. Document endpoints with docstrings
8. Use HTTP status codes correctly (201 for created, 204 for no content)
9. Handle errors with HTTPException
10. Keep routers in separate files for large projects

Project Structure:
myapp/
├── main.py              # FastAPI app instance
├── routers/
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── users.py         # User CRUD routes
│   ├── posts.py         # Post CRUD routes
│   └── comments.py      # Comment routes
├── models/
│   └── schemas.py       # Pydantic models
├── dependencies/
│   └── auth.py          # Authentication dependencies
└── database/
    └── db.py            # Database connection
"""
