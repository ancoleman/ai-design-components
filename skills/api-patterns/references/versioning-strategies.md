# API Versioning Strategies

API versioning enables backward-compatible changes while evolving the API over time without breaking existing clients.

## Versioning Strategies Comparison

| Strategy | Discoverability | Cache-Friendly | Implementation | Best For |
|----------|----------------|----------------|----------------|----------|
| URI Path | Excellent | Yes | Easy | Public APIs (recommended) |
| Query Parameter | Good | Yes | Easy | Simple APIs |
| Header | Poor | No | Medium | Internal APIs |
| Media Type | Poor | Yes | Complex | Hypermedia APIs |

## URI Path Versioning (Recommended)

**Advantages:**
- Most visible and discoverable
- Works with all HTTP clients
- Cache-friendly (different URLs)
- Easy to route in API gateways

**Disadvantages:**
- URL changes between versions
- Can lead to code duplication

### FastAPI Implementation

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# Version 1
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/items")
async def list_items_v1():
    return {"items": [{"id": 1, "name": "Item"}]}

@v1_router.get("/items/{item_id}")
async def get_item_v1(item_id: int):
    return {"id": item_id, "name": "Item"}

# Version 2 (breaking change: renamed field)
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/items")
async def list_items_v2():
    return {"items": [{"id": 1, "title": "Item"}]}  # Changed "name" to "title"

@v2_router.get("/items/{item_id}")
async def get_item_v2(item_id: int):
    return {"id": item_id, "title": "Item", "description": "New field"}

# Register routers
app.include_router(v1_router)
app.include_router(v2_router)
```

### Hono Implementation

```typescript
import { Hono } from 'hono'

const app = new Hono()

// Version 1
const v1 = new Hono()
v1.get('/items', (c) => c.json({ items: [{ id: 1, name: 'Item' }] }))
v1.get('/items/:id', (c) => c.json({ id: c.req.param('id'), name: 'Item' }))

// Version 2
const v2 = new Hono()
v2.get('/items', (c) => c.json({ items: [{ id: 1, title: 'Item' }] }))
v2.get('/items/:id', (c) => c.json({ id: c.req.param('id'), title: 'Item' }))

// Mount versions
app.route('/api/v1', v1)
app.route('/api/v2', v2)

export default app
```

### Shared Logic Pattern

Avoid duplication by sharing business logic:

```python
from typing import Protocol

class ItemRepository(Protocol):
    async def get_item(self, item_id: int) -> dict:
        ...

# Shared business logic
class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def get_item(self, item_id: int) -> dict:
        return await self.repo.get_item(item_id)

service = ItemService(item_repo)

# Version 1 adapter
@v1_router.get("/items/{item_id}")
async def get_item_v1(item_id: int):
    item = await service.get_item(item_id)
    return {"id": item["id"], "name": item["title"]}  # Map to v1 format

# Version 2 uses raw format
@v2_router.get("/items/{item_id}")
async def get_item_v2(item_id: int):
    return await service.get_item(item_id)
```

## Query Parameter Versioning

**Advantages:**
- No URL changes
- Easy to implement
- Optional (can default to latest)

**Disadvantages:**
- Less discoverable
- Can be ignored by clients
- Complicates caching

### FastAPI Implementation

```python
from fastapi import Query
from enum import Enum

class APIVersion(str, Enum):
    v1 = "v1"
    v2 = "v2"

@app.get("/api/items")
async def list_items(version: APIVersion = Query(APIVersion.v2, alias="api-version")):
    if version == APIVersion.v1:
        return {"items": [{"id": 1, "name": "Item"}]}
    else:  # v2
        return {"items": [{"id": 1, "title": "Item"}]}
```

### Hono Implementation

```typescript
app.get('/api/items', (c) => {
  const version = c.req.query('api-version') || 'v2'

  if (version === 'v1') {
    return c.json({ items: [{ id: 1, name: 'Item' }] })
  } else {
    return c.json({ items: [{ id: 1, title: 'Item' }] })
  }
})
```

## Header Versioning

**Advantages:**
- Clean URLs
- Supports content negotiation
- Can version independently

**Disadvantages:**
- Not discoverable in browser
- Harder to test
- Cache complexity

### FastAPI Implementation

```python
from fastapi import Header, HTTPException

@app.get("/api/items")
async def list_items(api_version: str = Header(default="v2", alias="X-API-Version")):
    if api_version == "v1":
        return {"items": [{"id": 1, "name": "Item"}]}
    elif api_version == "v2":
        return {"items": [{"id": 1, "title": "Item"}]}
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported API version: {api_version}")
```

### Hono Implementation

```typescript
app.get('/api/items', (c) => {
  const version = c.req.header('X-API-Version') || 'v2'

  if (version === 'v1') {
    return c.json({ items: [{ id: 1, name: 'Item' }] })
  } else if (version === 'v2') {
    return c.json({ items: [{ id: 1, title: 'Item' }] })
  } else {
    return c.json({ error: `Unsupported API version: ${version}` }, 400)
  }
})
```

### Vary Header (for Caching)

```python
from fastapi import Response

@app.get("/api/items")
async def list_items(
    response: Response,
    api_version: str = Header(default="v2", alias="X-API-Version")
):
    # Tell caches to vary by X-API-Version header
    response.headers["Vary"] = "X-API-Version"

    if api_version == "v1":
        return {"items": [{"id": 1, "name": "Item"}]}
    else:
        return {"items": [{"id": 1, "title": "Item"}]}
```

## Media Type Versioning (Content Negotiation)

**Advantages:**
- RESTful (uses Accept header)
- Clean URLs
- Supports multiple representations

**Disadvantages:**
- Complex implementation
- Not widely understood
- Difficult to test

### FastAPI Implementation

```python
from fastapi import Request, Response, HTTPException

@app.get("/api/items")
async def list_items(request: Request, response: Response):
    accept = request.headers.get("Accept", "application/json")

    if "application/vnd.myapi.v1+json" in accept:
        response.headers["Content-Type"] = "application/vnd.myapi.v1+json"
        return {"items": [{"id": 1, "name": "Item"}]}
    elif "application/vnd.myapi.v2+json" in accept or "application/json" in accept:
        response.headers["Content-Type"] = "application/vnd.myapi.v2+json"
        return {"items": [{"id": 1, "title": "Item"}]}
    else:
        raise HTTPException(status_code=406, detail="Not Acceptable")
```

### Client Usage

```typescript
// Version 1
const res1 = await fetch('/api/items', {
  headers: { 'Accept': 'application/vnd.myapi.v1+json' }
})

// Version 2
const res2 = await fetch('/api/items', {
  headers: { 'Accept': 'application/vnd.myapi.v2+json' }
})
```

## Sunset Policy (Deprecation)

Communicate version deprecation to clients:

```python
from datetime import datetime, timedelta

@v1_router.get("/items")
async def list_items_v1(response: Response):
    # Deprecation headers
    sunset_date = datetime.now() + timedelta(days=180)  # 6 months
    response.headers["Sunset"] = sunset_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers["Deprecation"] = "true"
    response.headers["Link"] = '</api/v2/items>; rel="successor-version"'

    return {"items": [{"id": 1, "name": "Item"}]}
```

### Enforce Sunset

```python
@v1_router.get("/items")
async def list_items_v1():
    sunset_date = datetime(2025, 12, 31)

    if datetime.now() > sunset_date:
        raise HTTPException(
            status_code=410,  # Gone
            detail="This API version has been sunset. Please use /api/v2/items"
        )

    return {"items": [{"id": 1, "name": "Item"}]}
```

## Gradual Migration Strategy

### Feature Flags

```python
from enum import Enum

class Feature(str, Enum):
    NEW_ITEM_FORMAT = "new_item_format"

feature_flags = {
    Feature.NEW_ITEM_FORMAT: False  # Gradually roll out to users
}

@app.get("/api/items")
async def list_items(user_id: int):
    if feature_flags[Feature.NEW_ITEM_FORMAT] or is_beta_user(user_id):
        return {"items": [{"id": 1, "title": "Item"}]}  # New format
    else:
        return {"items": [{"id": 1, "name": "Item"}]}  # Old format
```

### Dual Write (During Migration)

```python
@app.post("/api/items")
async def create_item(item: ItemCreate):
    # Write to old table
    await db_v1.insert(Item(name=item.name))

    # Also write to new table (for migration testing)
    await db_v2.insert(ItemV2(title=item.name, description=item.description))

    return {"id": 1, "name": item.name}
```

## Semantic Versioning for APIs

**Major.Minor.Patch (e.g., v2.1.3)**

- **Major:** Breaking changes (field removal, endpoint removal)
- **Minor:** Backward-compatible additions (new fields, new endpoints)
- **Patch:** Bug fixes, performance improvements

**URI Pattern:**
```
/api/v2/items        # Major version in URI
/api/v2.1/items      # Optional: Include minor version
```

**Example:**
```python
v2_0_router = APIRouter(prefix="/api/v2.0")  # Original v2
v2_1_router = APIRouter(prefix="/api/v2.1")  # Added new fields

@v2_0_router.get("/items/{item_id}")
async def get_item_v2_0(item_id: int):
    return {"id": item_id, "title": "Item"}

@v2_1_router.get("/items/{item_id}")
async def get_item_v2_1(item_id: int):
    return {"id": item_id, "title": "Item", "tags": ["new", "feature"]}

# Both v2 and v2.1 clients work
app.include_router(v2_0_router)
app.include_router(v2_1_router)
```

## Backward Compatibility Techniques

### Field Aliasing

Support both old and new field names:

```python
from pydantic import BaseModel, Field

class ItemV2(BaseModel):
    id: int
    title: str = Field(alias="name")  # Accept both "title" and "name"

@app.post("/api/v2/items")
async def create_item(item: ItemV2):
    return item
```

### Optional Fields

Add new fields as optional:

```python
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None  # New field, optional for backward compatibility
```

### Default Values

```python
class Item(BaseModel):
    id: int
    name: str
    status: str = "active"  # New field with default
```

## OpenAPI Documentation for Multiple Versions

### Separate OpenAPI Specs

```python
v1_app = FastAPI(title="My API", version="1.0.0", openapi_url="/api/v1/openapi.json")
v2_app = FastAPI(title="My API", version="2.0.0", openapi_url="/api/v2/openapi.json")

# Register endpoints...

app.mount("/api/v1", v1_app)
app.mount("/api/v2", v2_app)

# Docs available at:
# - /api/v1/docs (v1 Swagger UI)
# - /api/v2/docs (v2 Swagger UI)
```

### Version Selector in Docs

```python
app = FastAPI(
    title="My API",
    version="2.0.0",
    openapi_tags=[
        {"name": "v1", "description": "Version 1 (deprecated)"},
        {"name": "v2", "description": "Version 2 (current)"},
    ]
)

@app.get("/api/v1/items", tags=["v1"], deprecated=True)
async def list_items_v1():
    return {"items": []}

@app.get("/api/v2/items", tags=["v2"])
async def list_items_v2():
    return {"items": []}
```

## Version Negotiation Logic

### Intelligent Default

```python
LATEST_VERSION = "v2"
SUPPORTED_VERSIONS = ["v1", "v2"]

def get_api_version(request: Request) -> str:
    # 1. Check URI path
    if "/api/v1/" in str(request.url):
        return "v1"
    elif "/api/v2/" in str(request.url):
        return "v2"

    # 2. Check header
    header_version = request.headers.get("X-API-Version")
    if header_version in SUPPORTED_VERSIONS:
        return header_version

    # 3. Check query parameter
    query_version = request.query_params.get("api-version")
    if query_version in SUPPORTED_VERSIONS:
        return query_version

    # 4. Default to latest
    return LATEST_VERSION
```

## Testing Multiple Versions

```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.parametrize("version,expected_field", [
    ("v1", "name"),
    ("v2", "title"),
])
def test_item_field_name(version, expected_field):
    client = TestClient(app)
    response = client.get(f"/api/{version}/items/1")
    assert response.status_code == 200
    assert expected_field in response.json()
```

## Recommendation Matrix

| Scenario | Strategy | Notes |
|----------|----------|-------|
| Public REST API | URI Path | Most discoverable, cache-friendly |
| Internal Microservices | Header or Query Param | Flexibility over discoverability |
| Mobile Apps | URI Path | Works with all HTTP clients |
| GraphQL API | Schema Evolution | Field deprecation, not versioning |
| Breaking Changes | URI Path (major version) | /api/v1 → /api/v2 |
| Minor Additions | Same version | Add optional fields, don't version |
| Bug Fixes | No version change | Patch-level change |

**Default recommendation:** URI path versioning (e.g., `/api/v1`, `/api/v2`) for public APIs.

## Migration Checklist

When releasing a new API version:

- [ ] Update OpenAPI documentation
- [ ] Add deprecation headers to old version
- [ ] Set sunset date (6-12 months)
- [ ] Communicate to API consumers (email, blog post)
- [ ] Monitor usage of old version
- [ ] Provide migration guide with examples
- [ ] Run both versions in parallel during migration
- [ ] Remove old version only after usage drops to <5%
