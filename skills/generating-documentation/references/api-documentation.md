# API Documentation Reference

Comprehensive guide to API documentation with OpenAPI specifications and rendering tools.

## Table of Contents

1. [OpenAPI Specification](#openapi-specification)
2. [Design-First vs Code-First](#design-first-vs-code-first)
3. [Swagger UI Setup](#swagger-ui-setup)
4. [Redoc Setup](#redoc-setup)
5. [Scalar Setup](#scalar-setup)
6. [Best Practices](#best-practices)
7. [Integration with Documentation Sites](#integration-with-documentation-sites)

## OpenAPI Specification

OpenAPI (formerly Swagger) is the standard for REST API documentation.

### Complete Example

```yaml
openapi: 3.1.0
info:
  title: E-Commerce API
  version: 2.0.0
  description: API for managing products, orders, and customers
  contact:
    name: API Support
    email: api@example.com
    url: https://support.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v2
    description: Production
  - url: https://staging-api.example.com/v2
    description: Staging
  - url: http://localhost:3000/v2
    description: Local development

tags:
  - name: Products
    description: Product management operations
  - name: Orders
    description: Order processing operations
  - name: Customers
    description: Customer management operations

paths:
  /products:
    get:
      summary: List all products
      description: Retrieve a paginated list of products with optional filtering
      operationId: listProducts
      tags: [Products]
      parameters:
        - name: limit
          in: query
          description: Maximum number of products to return
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: offset
          in: query
          description: Number of products to skip
          required: false
          schema:
            type: integer
            minimum: 0
            default: 0
        - name: category
          in: query
          description: Filter by category
          required: false
          schema:
            type: string
            enum: [electronics, clothing, books, food]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
              examples:
                success:
                  value:
                    data:
                      - id: "prod_123"
                        name: "Laptop"
                        price: 999.99
                        category: "electronics"
                      - id: "prod_456"
                        name: "T-Shirt"
                        price: 29.99
                        category: "clothing"
                    pagination:
                      limit: 20
                      offset: 0
                      total: 156
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a product
      description: Create a new product in the catalog
      operationId: createProduct
      tags: [Products]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateProductRequest'
            examples:
              electronics:
                value:
                  name: "Wireless Headphones"
                  description: "Noise-cancelling over-ear headphones"
                  price: 199.99
                  category: "electronics"
                  inventory: 50
      responses:
        '201':
          description: Product created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /products/{productId}:
    get:
      summary: Get a product
      description: Retrieve a single product by ID
      operationId: getProduct
      tags: [Products]
      parameters:
        - name: productId
          in: path
          description: Product ID
          required: true
          schema:
            type: string
            pattern: '^prod_[a-zA-Z0-9]+$'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: Update a product
      description: Update an existing product
      operationId: updateProduct
      tags: [Products]
      security:
        - bearerAuth: []
      parameters:
        - name: productId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateProductRequest'
      responses:
        '200':
          description: Product updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Product:
      type: object
      required:
        - id
        - name
        - price
        - category
      properties:
        id:
          type: string
          pattern: '^prod_[a-zA-Z0-9]+$'
          example: "prod_abc123"
          description: Unique product identifier
        name:
          type: string
          minLength: 1
          maxLength: 200
          example: "Laptop"
        description:
          type: string
          maxLength: 2000
          example: "High-performance laptop for professionals"
        price:
          type: number
          format: double
          minimum: 0
          example: 999.99
        category:
          type: string
          enum: [electronics, clothing, books, food]
          example: "electronics"
        inventory:
          type: integer
          minimum: 0
          example: 50
        createdAt:
          type: string
          format: date-time
          example: "2025-01-15T10:30:00Z"
        updatedAt:
          type: string
          format: date-time
          example: "2025-01-16T14:20:00Z"

    CreateProductRequest:
      type: object
      required:
        - name
        - price
        - category
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 2000
        price:
          type: number
          format: double
          minimum: 0
        category:
          type: string
          enum: [electronics, clothing, books, food]
        inventory:
          type: integer
          minimum: 0
          default: 0

    UpdateProductRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 2000
        price:
          type: number
          format: double
          minimum: 0
        inventory:
          type: integer
          minimum: 0

    Pagination:
      type: object
      properties:
        limit:
          type: integer
          example: 20
        offset:
          type: integer
          example: 0
        total:
          type: integer
          example: 156

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          example: "INVALID_REQUEST"
        message:
          type: string
          example: "The request is invalid"
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              issue:
                type: string

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "INVALID_REQUEST"
            message: "Invalid product data"
            details:
              - field: "price"
                issue: "Price must be greater than 0"

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "UNAUTHORIZED"
            message: "Authentication required"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "NOT_FOUND"
            message: "Product not found"

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login

security:
  - bearerAuth: []
```

## Design-First vs Code-First

### Design-First Approach

Write the OpenAPI specification first, then implement the API.

**Workflow:**

1. Write OpenAPI spec (YAML/JSON)
2. Review spec with stakeholders (frontend, product)
3. Generate server stubs from spec
4. Implement API handlers
5. Validate implementation matches spec

**Tools:**

- **OpenAPI Generator**: Generate server stubs
- **Prism**: Mock server from OpenAPI spec
- **Stoplight Studio**: Visual OpenAPI editor

**Example (Generate Node.js stubs):**

```bash
# Install generator
npm install -g @openapitools/openapi-generator-cli

# Generate Express server
openapi-generator-cli generate \
  -i openapi.yaml \
  -g nodejs-express-server \
  -o server/
```

**Pros:**
- API contract defined before implementation
- Parallel frontend/backend development
- Early validation and feedback
- Documentation never out of sync

**Cons:**
- OpenAPI spec authoring can be verbose
- Learning curve for OpenAPI syntax
- Code generation may produce boilerplate

### Code-First Approach

Implement the API, then generate OpenAPI spec from code.

**Workflow:**

1. Implement API endpoints with decorators/annotations
2. Add documentation comments to code
3. Generate OpenAPI spec from code
4. Publish generated spec to documentation

**Tools:**

- **FastAPI** (Python): Auto-generates OpenAPI
- **NestJS** (Node.js): Swagger decorators
- **Springdoc** (Java): Auto-generates from Spring annotations
- **tsoa** (TypeScript): Generates from TypeScript decorators

**Example (FastAPI):**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Product API",
    description="API for managing products",
    version="1.0.0"
)

class Product(BaseModel):
    id: str
    name: str
    price: float

class CreateProductRequest(BaseModel):
    name: str
    price: float

@app.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Get a product",
    description="Retrieve a single product by ID"
)
async def get_product(product_id: str):
    """
    Get a product by ID.

    - **product_id**: The product's unique identifier
    """
    # Implementation
    return {"id": product_id, "name": "Laptop", "price": 999.99}

# OpenAPI spec auto-generated at /openapi.json
# Swagger UI available at /docs
# Redoc available at /redoc
```

**Pros:**
- Faster initial development
- Spec always matches implementation
- Familiar workflow for developers
- Less context switching

**Cons:**
- Documentation lags behind development
- Harder to get early feedback on API design
- Requires discipline to maintain comments

### Recommendation

- **New APIs**: Design-first (better planning, parallel development)
- **Existing APIs**: Code-first (easier migration)
- **Large teams**: Design-first (contract-driven development)
- **Solo projects**: Either (personal preference)
- **Public APIs**: Design-first (better stakeholder review)

## Swagger UI Setup

Interactive API documentation with "Try it out" functionality.

### Standalone HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>API Documentation</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "https://api.example.com/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
      });
    };
  </script>
</body>
</html>
```

### React Integration

```typescript
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

function ApiDocs() {
  return (
    <SwaggerUI
      url="https://api.example.com/openapi.json"
      docExpansion="list"
      defaultModelsExpandDepth={1}
    />
  );
}
```

## Redoc Setup

Beautiful, read-only API documentation with three-column layout.

### Standalone HTML

```html
<!DOCTYPE html>
<html>
<head>
  <title>API Documentation</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      margin: 0;
      padding: 0;
    }
  </style>
</head>
<body>
  <redoc spec-url='https://api.example.com/openapi.json'></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

### React Integration

```typescript
import { RedocStandalone } from 'redoc';

function ApiDocs() {
  return (
    <RedocStandalone
      specUrl="https://api.example.com/openapi.json"
      options={{
        nativeScrollbars: true,
        theme: {
          colors: {
            primary: {
              main: '#3f51b5'
            }
          },
          typography: {
            fontSize: '16px'
          }
        }
      }}
    />
  );
}
```

## Scalar Setup

Modern API documentation with cutting-edge UX (2025).

### Installation

```bash
npm install @scalar/api-reference
```

### React Integration

```typescript
import { ApiReference } from '@scalar/api-reference';
import '@scalar/api-reference/style.css';

function ApiDocs() {
  return (
    <ApiReference
      configuration={{
        spec: {
          url: 'https://api.example.com/openapi.json',
        },
        theme: 'purple',
      }}
    />
  );
}
```

## Best Practices

### 1. Use OpenAPI 3.1

OpenAPI 3.1 is fully compatible with JSON Schema 2020-12.

### 2. Organize with Tags

Group related endpoints:

```yaml
tags:
  - name: Users
    description: User management operations
  - name: Products
    description: Product catalog operations

paths:
  /users:
    get:
      tags: [Users]
      # ...
```

### 3. Reusable Components

Define schemas, responses, parameters once:

```yaml
components:
  schemas:
    User:
      type: object
      # ...

  responses:
    NotFound:
      description: Resource not found
      # ...

  parameters:
    PageLimit:
      name: limit
      in: query
      schema:
        type: integer
        default: 20
```

### 4. Rich Examples

Provide concrete examples for clarity:

```yaml
schema:
  $ref: '#/components/schemas/User'
examples:
  adminUser:
    value:
      id: "usr_123"
      email: "admin@example.com"
      role: "admin"
  standardUser:
    value:
      id: "usr_456"
      email: "user@example.com"
      role: "user"
```

### 5. Validation Rules

Use JSON Schema validation:

```yaml
properties:
  email:
    type: string
    format: email
    pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  age:
    type: integer
    minimum: 18
    maximum: 120
  username:
    type: string
    minLength: 3
    maxLength: 30
```

### 6. Document Security

Define authentication schemes:

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read: Read access
            write: Write access

security:
  - bearerAuth: []
  - apiKey: []
```

## Integration with Documentation Sites

### Docusaurus Integration

Install plugins:

```bash
npm install docusaurus-plugin-openapi-docs docusaurus-theme-openapi-docs
```

Configure:

```javascript
// docusaurus.config.js
module.exports = {
  plugins: [
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'api',
        docsPluginId: 'classic',
        config: {
          api: {
            specPath: 'openapi/api.yaml',
            outputDir: 'docs/api',
            sidebarOptions: {
              groupPathsBy: 'tag',
            },
          },
        },
      },
    ],
  ],
  themes: ['docusaurus-theme-openapi-docs'],
};
```

### MkDocs Integration

Install plugin:

```bash
pip install mkdocs-swagger-ui-tag
```

Configure:

```yaml
# mkdocs.yml
plugins:
  - swagger-ui-tag

markdown_extensions:
  - swagger-ui
```

Embed in Markdown:

```markdown
# API Reference

<swagger-ui src="openapi.yaml"/>
```

## Validation

Validate OpenAPI specs:

```bash
# Using Redocly CLI
npm install -g @redocly/cli
redocly lint openapi.yaml

# Using Spectral
npm install -g @stoplight/spectral-cli
spectral lint openapi.yaml
```
