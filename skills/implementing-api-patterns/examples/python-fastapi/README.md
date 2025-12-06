# FastAPI Complete REST API Example

Complete REST API demonstrating FastAPI best practices.

## Features

- Automatic OpenAPI documentation
- Pydantic v2 validation
- Cursor-based pagination
- Rate limiting (slowapi)
- CORS configuration
- Error handling
- Type hints throughout

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

## Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Health Check
- `GET /health` - Check service status

### Items
- `GET /items?cursor={cursor}&limit={limit}` - List items (cursor pagination)
- `GET /items/{id}` - Get item by ID
- `POST /items` - Create item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

## Example Requests

### List items (first page)
```bash
curl http://localhost:8000/items?limit=10
```

### List items (next page)
```bash
curl http://localhost:8000/items?cursor=5&limit=10
```

### Create item
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Widget",
    "description": "A brand new widget",
    "price": 39.99
  }'
```

### Get item
```bash
curl http://localhost:8000/items/1
```

### Update item
```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Widget",
    "description": "An updated widget",
    "price": 49.99
  }'
```

### Delete item
```bash
curl -X DELETE http://localhost:8000/items/1
```

## Rate Limits

- `GET /items`: 100 requests/minute
- `POST /items`: 10 requests/minute

## Production Considerations

1. **Database**: Replace in-memory dict with real database (PostgreSQL, MongoDB)
2. **Authentication**: Add JWT or OAuth2 authentication
3. **Caching**: Add Redis for caching expensive queries
4. **Logging**: Add structured logging
5. **Monitoring**: Add Prometheus metrics
6. **HTTPS**: Run behind reverse proxy (Nginx) with SSL
7. **Environment variables**: Use `.env` for configuration

## Frontend Integration

See `implementing-api-patterns/SKILL.md` for frontend integration examples with React, forms skill, and tables skill.
