# OpenAPI Documentation Guide

## Overview

OpenAPI (formerly Swagger) provides a standard way to document REST APIs. This guide covers automatic generation with FastAPI, Hono, Axum, and Gin.

## Table of Contents

- [OpenAPI 3.1 Basics](#openapi-31-basics)
- [FastAPI (Automatic)](#fastapi-automatic)
- [Hono (Middleware)](#hono-middleware)
- [Axum (utoipa)](#axum-utoipa)
- [Gin (swaggo/swag)](#gin-swaggoswag)
- [Interactive Documentation](#interactive-documentation)

## OpenAPI 3.1 Basics

### Minimal OpenAPI Document

```yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: API for managing users and posts

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:3000/v1
    description: Development

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags:
        - users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
```

## FastAPI (Automatic)

FastAPI generates OpenAPI automatically from Python type hints.

### Zero Configuration

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="My API",
    description="API for managing users",
    version="1.0.0",
    openapi_tags=[
        {"name": "users", "description": "User operations"},
        {"name": "posts", "description": "Post operations"}
    ]
)

class User(BaseModel):
    """User model"""
    name: str
    email: EmailStr
    age: int | None = None

@app.get(
    "/users",
    tags=["users"],
    summary="List all users",
    response_description="List of users"
)
async def list_users(
    limit: int = 20,
    offset: int = 0
) -> list[User]:
    """
    Retrieve a list of users.

    - **limit**: Maximum number of users to return
    - **offset**: Number of users to skip
    """
    return get_users_from_db(limit, offset)

@app.post(
    "/users",
    tags=["users"],
    status_code=201,
    response_model=User
)
async def create_user(user: User) -> User:
    """Create a new user"""
    return create_user_in_db(user)

# Docs automatically available at:
# - /docs (Swagger UI)
# - /redoc (ReDoc)
# - /openapi.json (OpenAPI spec)
```

### Advanced Configuration

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="Comprehensive API documentation",
        routes=app.routes,
    )

    # Add custom fields
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Response Models

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str

class UserResponse(BaseModel):
    user: User

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "User not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        }
    }
)
async def get_user(user_id: str):
    user = get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}
```

## Hono (Middleware)

### Installation

```bash
npm install @hono/zod-openapi
```

### Setup

```typescript
import { OpenAPIHono, createRoute, z } from '@hono/zod-openapi'

const app = new OpenAPIHono()

const UserSchema = z.object({
  id: z.string().openapi({ example: '123' }),
  name: z.string().openapi({ example: 'Alice' }),
  email: z.string().email().openapi({ example: 'alice@example.com' })
})

const getUserRoute = createRoute({
  method: 'get',
  path: '/users/{id}',
  request: {
    params: z.object({
      id: z.string()
    })
  },
  responses: {
    200: {
      content: {
        'application/json': {
          schema: UserSchema
        }
      },
      description: 'User found'
    },
    404: {
      description: 'User not found'
    }
  },
  tags: ['users'],
  summary: 'Get user by ID'
})

app.openapi(getUserRoute, (c) => {
  const { id } = c.req.valid('param')
  const user = getUserFromDB(id)

  if (!user) {
    return c.json({ error: 'Not found' }, 404)
  }

  return c.json(user, 200)
})

// Serve OpenAPI spec
app.doc('/openapi.json', {
  openapi: '3.1.0',
  info: {
    title: 'My API',
    version: '1.0.0'
  }
})

// Swagger UI
import { swaggerUI } from '@hono/swagger-ui'
app.get('/docs', swaggerUI({ url: '/openapi.json' }))

export default app
```

## Axum (utoipa)

### Installation

```toml
[dependencies]
utoipa = { version = "4", features = ["axum_extras"] }
utoipa-swagger-ui = { version = "6", features = ["axum"] }
```

### Implementation

```rust
use axum::{Router, Json};
use utoipa::{OpenApi, ToSchema};
use utoipa_swagger_ui::SwaggerUi;

#[derive(serde::Serialize, ToSchema)]
struct User {
    #[schema(example = "123")]
    id: String,
    #[schema(example = "Alice")]
    name: String,
    #[schema(example = "alice@example.com")]
    email: String,
}

#[derive(OpenApi)]
#[openapi(
    paths(
        list_users,
        get_user,
        create_user
    ),
    components(
        schemas(User)
    ),
    tags(
        (name = "users", description = "User management endpoints")
    )
)]
struct ApiDoc;

/// List all users
#[utoipa::path(
    get,
    path = "/users",
    tag = "users",
    responses(
        (status = 200, description = "List of users", body = Vec<User>)
    )
)]
async fn list_users() -> Json<Vec<User>> {
    Json(get_users_from_db())
}

/// Get user by ID
#[utoipa::path(
    get,
    path = "/users/{id}",
    tag = "users",
    params(
        ("id" = String, Path, description = "User ID")
    ),
    responses(
        (status = 200, description = "User found", body = User),
        (status = 404, description = "User not found")
    )
)]
async fn get_user(
    axum::extract::Path(id): axum::extract::Path<String>
) -> Result<Json<User>, StatusCode> {
    match get_user_from_db(&id) {
        Some(user) => Ok(Json(user)),
        None => Err(StatusCode::NOT_FOUND)
    }
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/users", get(list_users))
        .route("/users/:id", get(get_user))
        .merge(SwaggerUi::new("/docs").url("/openapi.json", ApiDoc::openapi()));

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

## Gin (swaggo/swag)

### Installation

```bash
go install github.com/swaggo/swag/cmd/swag@latest
```

### Implementation

```go
package main

import (
    "github.com/gin-gonic/gin"
    swaggerFiles "github.com/swaggo/files"
    ginSwagger "github.com/swaggo/gin-swagger"

    _ "example.com/docs" // Generated by swag init
)

type User struct {
    ID    string `json:"id" example:"123"`
    Name  string `json:"name" example:"Alice"`
    Email string `json:"email" example:"alice@example.com"`
}

// @title My API
// @version 1.0
// @description API for managing users
// @host localhost:8080
// @BasePath /api/v1
func main() {
    r := gin.Default()

    v1 := r.Group("/api/v1")
    {
        v1.GET("/users", listUsers)
        v1.GET("/users/:id", getUser)
        v1.POST("/users", createUser)
    }

    // Swagger docs
    r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

    r.Run(":8080")
}

// @Summary List users
// @Description Get list of all users
// @Tags users
// @Accept json
// @Produce json
// @Param limit query int false "Limit" default(20)
// @Success 200 {array} User
// @Router /users [get]
func listUsers(c *gin.Context) {
    users := getUsersFromDB()
    c.JSON(200, users)
}

// @Summary Get user
// @Description Get user by ID
// @Tags users
// @Accept json
// @Produce json
// @Param id path string true "User ID"
// @Success 200 {object} User
// @Failure 404 {object} ErrorResponse
// @Router /users/{id} [get]
func getUser(c *gin.Context) {
    id := c.Param("id")
    user, exists := getUserFromDB(id)

    if !exists {
        c.JSON(404, gin.H{"error": "User not found"})
        return
    }

    c.JSON(200, user)
}

// @Summary Create user
// @Description Create a new user
// @Tags users
// @Accept json
// @Produce json
// @Param user body User true "User"
// @Success 201 {object} User
// @Failure 400 {object} ErrorResponse
// @Router /users [post]
func createUser(c *gin.Context) {
    var user User
    if err := c.ShouldBindJSON(&user); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }

    created := createUserInDB(user)
    c.JSON(201, created)
}
```

### Generate Docs

```bash
swag init
# Creates docs/ directory with swagger.json and swagger.yaml
```

## Interactive Documentation

### Swagger UI Customization

```python
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={"persistAuthorization": True}
    )
```

### ReDoc Customization

```python
from fastapi.openapi.docs import get_redoc_html

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@latest/bundles/redoc.standalone.js",
    )
```

## Best Practices

1. **Use semantic versioning** - Version your API (v1, v2)
2. **Document all endpoints** - Include descriptions and examples
3. **Define schemas** - Reuse schema definitions
4. **Include examples** - Real-world request/response examples
5. **Document error responses** - All possible error codes
6. **Add security schemes** - Document authentication methods
7. **Tag endpoints** - Group related endpoints
8. **Include server URLs** - Production, staging, development
9. **Keep docs in sync** - Auto-generation preferred
10. **Test with Swagger UI** - Verify docs are usable
