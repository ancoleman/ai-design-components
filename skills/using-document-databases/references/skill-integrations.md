# Document Database Integration with Frontend Skills

Integration patterns for connecting MongoDB/DynamoDB with frontend component skills.


## Table of Contents

- [Forms Skill Integration](#forms-skill-integration)
  - [Form Submission → MongoDB](#form-submission-mongodb)
- [Tables Skill Integration](#tables-skill-integration)
  - [MongoDB → TanStack Table](#mongodb-tanstack-table)
- [Search-Filter Skill Integration](#search-filter-skill-integration)
  - [MongoDB Full-Text Search](#mongodb-full-text-search)
- [Media Skill Integration](#media-skill-integration)
  - [GridFS for Large Files](#gridfs-for-large-files)
- [Dashboard Skill Integration](#dashboard-skill-integration)
  - [Real-Time Metrics with Change Streams](#real-time-metrics-with-change-streams)
- [AI Chat Skill Integration](#ai-chat-skill-integration)
  - [MongoDB Atlas Vector Search](#mongodb-atlas-vector-search)
- [Feedback Skill Integration](#feedback-skill-integration)
  - [Event Logging with TTL](#event-logging-with-ttl)
- [Best Practices](#best-practices)
  - [Connection Reuse](#connection-reuse)
  - [Error Handling](#error-handling)
  - [Validation](#validation)
- [Resources](#resources)

## Forms Skill Integration

### Form Submission → MongoDB

```typescript
// Frontend (React Hook Form)
import { useForm } from 'react-hook-form';

function CreateUserForm() {
  const { register, handleSubmit } = useForm();

  const onSubmit = async (data) => {
    await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      <input {...register('name')} />
      <button>Submit</button>
    </form>
  );
}

// Backend (FastAPI + MongoDB)
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str

@app.post("/api/users")
async def create_user(user: UserCreate):
    result = await db.users.insert_one({
        "email": user.email,
        "name": user.name,
        "createdAt": datetime.utcnow(),
    })

    return {"id": str(result.inserted_id)}
```

## Tables Skill Integration

### MongoDB → TanStack Table

```typescript
// Frontend
import { useQuery } from '@tanstack/react-query';
import { useReactTable, getCoreRowModel } from '@tanstack/react-table';

function UserTable() {
  const { data } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
  });

  const table = useReactTable({
    data: data?.users || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return <Table />;
}

// Backend (Cursor Pagination)
@app.get("/api/users")
async def list_users(cursor: Optional[str] = None, limit: int = 20):
    query = {}
    if cursor:
        query["_id"] = {"$lt": ObjectId(cursor)}

    users = await db.users.find(query).sort("_id", -1).limit(limit).to_list(limit)

    return {
        "users": users,
        "nextCursor": str(users[-1]["_id"]) if users else None,
        "hasMore": len(users) == limit,
    }
```

## Search-Filter Skill Integration

### MongoDB Full-Text Search

```javascript
// Create text index
db.products.createIndex({
  name: "text",
  description: "text",
  tags: "text"
})

// Search with filters
db.products.find({
  $text: { $search: "laptop" },
  price: { $lte: 1000 },
  category: "electronics",
}).sort({ score: { $meta: "textScore" } })
```

```typescript
// Frontend
@app.get("/api/products/search")
async def search_products(
    q: str,
    category: Optional[str] = None,
    maxPrice: Optional[float] = None,
):
    query = { "$text": { "$search": q } }

    if category:
        query["category"] = category
    if maxPrice:
        query["price"] = { "$lte": maxPrice }

    products = await db.products.find(query).sort([
        ("score", { "$meta": "textScore" })
    ]).to_list(20)

    return {"products": products}
```

## Media Skill Integration

### GridFS for Large Files

```python
from gridfs import GridFS
from motor.motor_asyncio import AsyncIOMotorGridFS

fs = AsyncIOMotorGridFS(db)

# Upload file
@app.post("/api/upload")
async def upload_file(file: UploadFile):
    file_id = await fs.upload_from_stream(
        filename=file.filename,
        source=file.file,
        metadata={
            "contentType": file.content_type,
            "uploadedBy": current_user.id,
            "uploadedAt": datetime.utcnow(),
        }
    )

    return {"fileId": str(file_id)}

# Download file
@app.get("/api/files/{file_id}")
async def download_file(file_id: str):
    grid_out = await fs.open_download_stream(ObjectId(file_id))

    return StreamingResponse(
        grid_out,
        media_type=grid_out.metadata.get("contentType"),
    )
```

## Dashboard Skill Integration

### Real-Time Metrics with Change Streams

```python
# Backend (FastAPI + SSE)
from fastapi.responses import StreamingResponse

@app.get("/api/metrics/stream")
async def stream_metrics():
    async def generate():
        async with db.orders.watch() as stream:
            async for change in stream:
                if change["operationType"] == "insert":
                    # Calculate updated metrics
                    metrics = await calculate_metrics()
                    yield f"data: {json.dumps(metrics)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )
```

```typescript
// Frontend
useEffect(() => {
  const es = new EventSource('/api/metrics/stream');
  es.onmessage = (e) => {
    const metrics = JSON.parse(e.data);
    setDashboardMetrics(metrics);
  };
  return () => es.close();
}, []);
```

## AI Chat Skill Integration

### MongoDB Atlas Vector Search

```python
# Create vector search index (Atlas UI or API)
# Index definition:
{
  "mappings": {
    "fields": {
      "embedding": {
        "type": "knnVector",
        "dimensions": 1024,
        "similarity": "cosine"
      }
    }
  }
}

# Semantic search in chat history
@app.post("/api/chat/search")
async def search_chat_history(query: str):
    query_embedding = voyage_ai.embed(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 5,
            }
        },
        {
            "$project": {
                "message": 1,
                "timestamp": 1,
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ]

    results = await db.chat_messages.aggregate(pipeline).to_list(5)
    return {"results": results}
```

## Feedback Skill Integration

### Event Logging with TTL

```javascript
// Auto-delete events after 90 days
db.events.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 7776000 }  // 90 days
)

// Log user events
db.events.insertOne({
  userId: 123,
  type: "button_click",
  button: "submit",
  page: "/checkout",
  createdAt: new Date(),
})

// Aggregate for analytics
db.events.aggregate([
  { $match: { type: "button_click" } },
  { $group: {
      _id: { button: "$button", page: "$page" },
      count: { $sum: 1 }
  }},
  { $sort: { count: -1 } },
])
```

## Best Practices

### Connection Reuse

```typescript
// ✓ Singleton pattern
let client: MongoClient;

export async function getDatabase() {
  if (!client) {
    client = new MongoClient(process.env.MONGODB_URI);
    await client.connect();
  }
  return client.db('myapp');
}

// ✗ Don't create new connections per request
async function handler() {
  const client = new MongoClient(uri);  // BAD
  await client.connect();
}
```

### Error Handling

```typescript
try {
  await db.users.insertOne({ email: "user@example.com" });
} catch (error) {
  if (error.code === 11000) {
    return { error: "Email already exists" };
  }
  throw error;
}
```

### Validation

```javascript
// Schema validation (MongoDB 3.6+)
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "name"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^.+@.+\..+$"
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 120
        }
      }
    }
  }
})
```

## Resources

- Motor (Async Python): https://motor.readthedocs.io/
- MongoDB Node Driver: https://www.mongodb.com/docs/drivers/node/
- Prisma MongoDB: https://www.prisma.io/docs/concepts/database-connectors/mongodb
