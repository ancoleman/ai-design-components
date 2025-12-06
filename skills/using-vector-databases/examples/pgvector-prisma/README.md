# pgvector + Prisma Integration Example

TypeScript/Node.js example using PostgreSQL with pgvector extension and Prisma ORM.

## Features

- pgvector PostgreSQL extension
- Prisma ORM integration
- Vector similarity search
- OpenAI embeddings
- TypeScript type safety

## Prerequisites

- Node.js 18+
- PostgreSQL 15+ with pgvector extension
- OpenAI API key

## Setup

```bash
# Install dependencies
npm install

# Set up database
cp .env.example .env
# Edit .env with your DATABASE_URL and OPENAI_API_KEY

# Run migrations
npx prisma migrate dev

# Generate Prisma client
npx prisma generate
```

## Usage

```typescript
import { PrismaClient } from '@prisma/client';
import { generateEmbedding, similaritySearch } from './vector-search';

const prisma = new PrismaClient();

// Insert document with embedding
const embedding = await generateEmbedding('Document content');
await prisma.$executeRaw`
  INSERT INTO documents (content, embedding, metadata)
  VALUES (${content}, ${embedding}::vector, ${metadata}::jsonb)
`;

// Search
const results = await similaritySearch('search query', 5);
console.log(results);
```

## Running

```bash
npm run dev
```

## Project Structure

```
pgvector-prisma/
├── package.json
├── tsconfig.json
├── prisma/
│   └── schema.prisma
├── src/
│   ├── index.ts
│   └── vector-search.ts
└── README.md
```

See individual files for implementation details.
