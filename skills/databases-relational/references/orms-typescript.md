# TypeScript ORMs and Query Builders

## Overview

| Library | Context7 ID | Trust | Snippets | Score | Type | Best For |
|---------|-------------|-------|----------|-------|------|----------|
| **Prisma 6.x** | `/prisma/prisma` | High | 115 | 96.4 | ORM | Best DX, migrations, type generation |
| Prisma Docs | `/prisma/docs` | High | 4,281 | - | - | Comprehensive documentation |
| **Drizzle ORM** | `/llmstxt/orm_drizzle_team-llms.txt` | High | 4,037 | 95.4 | Query Builder | Performance, SQL-like syntax |
| Drizzle Docs | `/drizzle-team/drizzle-orm-docs` | High | 1,666 | - | - | Documentation |
| **Kysely** | - | - | - | - | Query Builder | Type-safe SQL builder |
| **TypeORM** | - | - | - | - | ORM | Legacy projects, decorators |

## Prisma (Recommended for Best DX)

**Context7:** `/prisma/prisma` (96.4 score, 4,281 doc snippets)

### Installation

```bash
npm install prisma @prisma/client
npx prisma init
```

### Schema Definition

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  createdAt DateTime @default(now())
  posts     Post[]
  profile   Profile?

  @@index([email])
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  authorId  Int
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  @@index([authorId])
}

model Profile {
  id     Int    @id @default(autoincrement())
  bio    String
  userId Int    @unique
  user   User   @relation(fields: [userId], references: [id])
}
```

### Generate Client

```bash
npx prisma migrate dev --name init  # Create migration + generate client
npx prisma generate  # Regenerate client after schema changes
```

### Usage

```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Create
const user = await prisma.user.create({
  data: {
    email: 'test@example.com',
    name: 'Test User',
    posts: {
      create: [
        { title: 'First Post', content: 'Hello World' },
        { title: 'Second Post', content: 'More content' }
      ]
    }
  },
  include: { posts: true }  // Include relations
})

// Read
const user = await prisma.user.findUnique({
  where: { email: 'test@example.com' },
  include: { posts: true, profile: true }
})

const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 0
})

// Update
const updated = await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Updated Name' }
})

// Delete
await prisma.user.delete({
  where: { id: 1 }
})

// Transactions
await prisma.$transaction([
  prisma.user.create({ data: { email: 'user1@example.com', name: 'User 1' } }),
  prisma.user.create({ data: { email: 'user2@example.com', name: 'User 2' } })
])

// Raw SQL
const users = await prisma.$queryRaw`SELECT * FROM users WHERE email = ${email}`
```

### Next.js Integration

```typescript
// lib/prisma.ts (connection pooling for serverless)
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ['query', 'error', 'warn'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

// app/api/users/route.ts
import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  const users = await prisma.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await prisma.user.create({ data: body })
  return NextResponse.json(user)
}
```

### Migrations

```bash
npx prisma migrate dev --name add_users  # Development
npx prisma migrate deploy  # Production
npx prisma migrate reset  # Reset database
npx prisma db push  # Prototype mode (skip migrations)
```

**Why Prisma?**
- Best-in-class TypeScript types (autocomplete for everything)
- Visual database browser (Prisma Studio: `npx prisma studio`)
- Migrations built-in
- Excellent documentation
- Large community

## Drizzle ORM (Recommended for Performance)

**Context7:** `/drizzle-team/drizzle-orm-docs` (95.4 score, 4,037 snippets)

### Installation

```bash
npm install drizzle-orm pg
npm install -D drizzle-kit
```

### Schema Definition

```typescript
// schema.ts
import { pgTable, serial, text, integer, boolean, timestamp } from 'drizzle-orm/pg-core'
import { relations } from 'drizzle-orm'

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
})

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  authorId: integer('author_id').references(() => users.id, { onDelete: 'cascade' }),
})

// Define relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}))

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}))
```

### Usage

```typescript
import { drizzle } from 'drizzle-orm/node-postgres'
import { eq, like, desc, and, or } from 'drizzle-orm'
import { Pool } from 'pg'
import { users, posts } from './schema'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const db = drizzle(pool)

// Create
const newUser = await db.insert(users).values({
  email: 'test@example.com',
  name: 'Test User'
}).returning()

// Read
const allUsers = await db.select().from(users)

const user = await db.select().from(users).where(eq(users.id, 1))

const filtered = await db.select().from(users).where(
  and(
    like(users.email, '%@example.com'),
    eq(users.name, 'Test User')
  )
)

// Update
await db.update(users)
  .set({ name: 'Updated Name' })
  .where(eq(users.id, 1))

// Delete
await db.delete(users).where(eq(users.id, 1))

// Joins (type-safe!)
const usersWithPosts = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId))

// Relations (automatic joins)
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
})

// Transactions
await db.transaction(async (tx) => {
  await tx.insert(users).values({ email: 'user1@example.com', name: 'User 1' })
  await tx.insert(users).values({ email: 'user2@example.com', name: 'User 2' })
})
```

### Migrations

```typescript
// drizzle.config.ts
import type { Config } from 'drizzle-kit'

export default {
  schema: './schema.ts',
  out: './drizzle',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config
```

```bash
npx drizzle-kit generate:pg  # Generate migrations
npx drizzle-kit push:pg  # Push schema directly (prototyping)
npx drizzle-kit studio  # Visual database browser
```

**Why Drizzle?**
- SQL-like syntax (easy migration from raw SQL)
- Zero runtime overhead (no proxies, minimal abstractions)
- ~14KB bundle size (vs Prisma's client generation)
- Fully type-safe with excellent inference
- Fast performance

## Kysely (Type-Safe SQL Builder)

### Installation

```bash
npm install kysely pg
```

### Schema Definition

```typescript
// types.ts
import { Generated, Insertable, Selectable, Updateable } from 'kysely'

export interface Database {
  users: UsersTable
  posts: PostsTable
}

export interface UsersTable {
  id: Generated<number>
  email: string
  name: string
  created_at: Generated<Date>
}

export interface PostsTable {
  id: Generated<number>
  title: string
  content: string | null
  published: Generated<boolean>
  author_id: number
}

export type User = Selectable<UsersTable>
export type NewUser = Insertable<UsersTable>
export type UserUpdate = Updateable<UsersTable>
```

### Usage

```typescript
import { Kysely, PostgresDialect } from 'kysely'
import { Pool } from 'pg'
import { Database } from './types'

const db = new Kysely<Database>({
  dialect: new PostgresDialect({
    pool: new Pool({ connectionString: process.env.DATABASE_URL })
  })
})

// Create
const user = await db
  .insertInto('users')
  .values({ email: 'test@example.com', name: 'Test User' })
  .returningAll()
  .executeTakeFirstOrThrow()

// Read
const users = await db.selectFrom('users').selectAll().execute()

const user = await db
  .selectFrom('users')
  .selectAll()
  .where('email', '=', 'test@example.com')
  .executeTakeFirst()

// Update
await db
  .updateTable('users')
  .set({ name: 'Updated Name' })
  .where('id', '=', 1)
  .execute()

// Delete
await db.deleteFrom('users').where('id', '=', 1).execute()

// Joins
const usersWithPosts = await db
  .selectFrom('users')
  .leftJoin('posts', 'posts.author_id', 'users.id')
  .select([
    'users.id',
    'users.email',
    'users.name',
    'posts.title',
    'posts.content'
  ])
  .execute()

// Transactions
await db.transaction().execute(async (trx) => {
  await trx.insertInto('users').values({ email: 'user1@example.com', name: 'User 1' }).execute()
  await trx.insertInto('users').values({ email: 'user2@example.com', name: 'User 2' }).execute()
})
```

**Why Kysely?**
- Pure SQL builder (no ORM magic)
- Excellent TypeScript inference
- Lightweight (~10KB)
- Database-agnostic (PostgreSQL, MySQL, SQLite)
- Type-safe query building

## TypeORM (Legacy)

**Use when:** Maintaining existing TypeORM projects, prefer decorators.

```typescript
import { Entity, PrimaryGeneratedColumn, Column, OneToMany, ManyToOne } from 'typeorm'

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number

  @Column({ unique: true })
  email: string

  @Column()
  name: string

  @OneToMany(() => Post, post => post.author)
  posts: Post[]
}

@Entity()
export class Post {
  @PrimaryGeneratedColumn()
  id: number

  @Column()
  title: string

  @Column({ nullable: true })
  content: string

  @ManyToOne(() => User, user => user.posts)
  author: User
}
```

## Comparison: When to Use Each

### Choose Prisma When:
- Want best developer experience
- Need visual database browser
- Prefer schema-first approach
- Building with Next.js/serverless
- Team new to databases

### Choose Drizzle When:
- Performance critical
- Prefer SQL-like syntax
- Want minimal bundle size
- Comfortable with SQL
- Need full query control

### Choose Kysely When:
- Want pure SQL builder
- Don't need ORM features
- Prefer explicit queries
- Type safety priority
- Lightweight solution

### Choose TypeORM When:
- Maintaining legacy code
- Prefer decorators
- Like Active Record pattern
- Need repository pattern

## Best Practices

### Connection Pooling for Serverless

```typescript
// Prisma (automatic pooling)
// Configure in DATABASE_URL:
// postgresql://user:pass@host/db?connection_limit=1&pool_timeout=30

// Drizzle + pg
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 1,  // Serverless: 1-2 connections per function
  idleTimeoutMillis: 30000,
})

// Use connection pooler (pgBouncer) for serverless
// DATABASE_URL=postgresql://user:pass@pooler-host:6543/db?pgbouncer=true
```

### Type-Safe Queries

```typescript
// Prisma (automatic)
const user = await prisma.user.findUnique({ where: { id: 1 } })
//    ^? User | null (inferred)

// Drizzle (automatic)
const users = await db.select().from(users)
//    ^? { id: number; email: string; name: string }[]

// Kysely (automatic)
const user = await db.selectFrom('users').selectAll().execute()
//    ^? User[]
```

### Pagination

```typescript
// Prisma
const users = await prisma.user.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { createdAt: 'desc' }
})

// Drizzle
const users = await db.select().from(users)
  .limit(pageSize)
  .offset((page - 1) * pageSize)
  .orderBy(desc(users.createdAt))

// Kysely
const users = await db.selectFrom('users')
  .selectAll()
  .limit(pageSize)
  .offset((page - 1) * pageSize)
  .orderBy('created_at', 'desc')
  .execute()
```

### Transactions

```typescript
// Prisma
await prisma.$transaction([
  prisma.user.create({ data: { email: 'user1@example.com', name: 'User 1' } }),
  prisma.post.create({ data: { title: 'Post 1', authorId: 1 } })
])

// Drizzle
await db.transaction(async (tx) => {
  await tx.insert(users).values({ email: 'user1@example.com', name: 'User 1' })
  await tx.insert(posts).values({ title: 'Post 1', authorId: 1 })
})

// Kysely
await db.transaction().execute(async (trx) => {
  await trx.insertInto('users').values({ email: 'user1@example.com', name: 'User 1' }).execute()
  await trx.insertInto('posts').values({ title: 'Post 1', author_id: 1 }).execute()
})
```

## Resources

- Prisma Docs: https://www.prisma.io/docs
- Drizzle Docs: https://orm.drizzle.team/
- Kysely Docs: https://kysely.dev/
- TypeORM Docs: https://typeorm.io/
