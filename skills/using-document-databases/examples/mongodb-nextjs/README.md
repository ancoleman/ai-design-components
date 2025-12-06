# MongoDB + Next.js Example

Full-stack Next.js 14 application with MongoDB, demonstrating CRUD operations, server components, and real-time updates.

## Stack

- Next.js 14 (App Router)
- MongoDB (with Motor/PyMongo or native Node driver)
- Server Components + API Routes
- TypeScript
- Tailwind CSS

## Features

- CRUD operations (Create, Read, Update, Delete)
- Server-side data fetching
- API routes for database operations
- Optimistic updates
- Form validation
- Error handling

## Project Structure

```
mongodb-nextjs/
├── app/
│   ├── page.tsx             # Home page (Server Component)
│   ├── posts/
│   │   ├── page.tsx         # Posts list
│   │   ├── [id]/page.tsx    # Post detail
│   │   └── new/page.tsx     # Create post
│   └── api/
│       └── posts/
│           ├── route.ts     # GET /api/posts, POST /api/posts
│           └── [id]/
│               └── route.ts # GET/PUT/DELETE /api/posts/:id
├── lib/
│   └── mongodb.ts           # MongoDB client singleton
├── models/
│   └── post.ts              # TypeScript types
└── package.json
```

## Quick Start

```bash
# Install
npm install mongodb

# Configure
cp .env.example .env
# Set MONGODB_URI=mongodb://localhost:27017/myapp

# Run
npm run dev
```

## MongoDB Connection

```typescript
// lib/mongodb.ts
import { MongoClient } from 'mongodb';

if (!process.env.MONGODB_URI) {
  throw new Error('Please add MONGODB_URI to .env');
}

const uri = process.env.MONGODB_URI;
const options = {};

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

if (process.env.NODE_ENV === 'development') {
  // Preserve client across hot reloads
  if (!(global as any)._mongoClientPromise) {
    client = new MongoClient(uri, options);
    (global as any)._mongoClientPromise = client.connect();
  }
  clientPromise = (global as any)._mongoClientPromise;
} else {
  client = new MongoClient(uri, options);
  clientPromise = client.connect();
}

export default clientPromise;
```

## Server Component (Read)

```typescript
// app/posts/page.tsx
import clientPromise from '@/lib/mongodb';

export default async function PostsPage() {
  const client = await clientPromise;
  const db = client.db('myapp');

  const posts = await db.collection('posts')
    .find({})
    .sort({ createdAt: -1 })
    .limit(20)
    .toArray();

  return (
    <div>
      <h1>Posts</h1>
      {posts.map((post) => (
        <PostCard key={post._id.toString()} post={post} />
      ))}
    </div>
  );
}
```

## API Route (Create)

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';
import clientPromise from '@/lib/mongodb';

export async function POST(request: NextRequest) {
  const { title, content } = await request.json();

  const client = await clientPromise;
  const db = client.db('myapp');

  const result = await db.collection('posts').insertOne({
    title,
    content,
    createdAt: new Date(),
    updatedAt: new Date(),
  });

  return NextResponse.json({
    id: result.insertedId.toString(),
    title,
    content,
  }, { status: 201 });
}

export async function GET() {
  const client = await clientPromise;
  const db = client.db('myapp');

  const posts = await db.collection('posts')
    .find({})
    .sort({ createdAt: -1 })
    .toArray();

  return NextResponse.json({ posts });
}
```

## Client Component (Optimistic Update)

```typescript
'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';

function CreatePostForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newPost) => fetch('/api/posts', {
      method: 'POST',
      body: JSON.stringify(newPost),
    }).then(r => r.json()),

    onMutate: async (newPost) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['posts'] });

      const previous = queryClient.getQueryData(['posts']);

      queryClient.setQueryData(['posts'], (old: any) => [
        ...old,
        { ...newPost, _id: 'temp-id' },
      ]);

      return { previous };
    },

    onError: (err, newPost, context) => {
      // Rollback on error
      queryClient.setQueryData(['posts'], context?.previous);
    },

    onSuccess: () => {
      // Refetch to get server data
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  return <form onSubmit={(e) => {
    e.preventDefault();
    mutation.mutate({ title: '...', content: '...' });
  }} />;
}
```

## Integration Summary

| Frontend Skill | MongoDB Pattern | Backend Pattern |
|----------------|-----------------|-----------------|
| **Forms** | insertOne, updateOne | POST/PUT API routes with validation |
| **Tables** | find() with cursor pagination | GET with cursor parameter |
| **Search** | $text index + aggregation | Text search + filters API |
| **Media** | GridFS | Upload/download with streams |
| **Dashboards** | Aggregation pipeline | GET with date ranges, grouping |
| **AI Chat** | Vector search (Atlas) | Semantic search API |

## Best Practices

1. **Singleton connection** - Reuse MongoDB client
2. **Index query fields** - All find() filters should have indexes
3. **Cursor pagination** - Not offset for large collections
4. **Optimistic updates** - Better UX for mutations
5. **Error boundaries** - Graceful error handling
6. **TypeScript types** - Type safety for documents
7. **Validation** - Zod/Pydantic on API layer
8. **Connection pooling** - Default is usually sufficient

## Resources

- Next.js + MongoDB: https://github.com/vercel/next.js/tree/canary/examples/with-mongodb
- MongoDB Node Driver: https://www.mongodb.com/docs/drivers/node/
