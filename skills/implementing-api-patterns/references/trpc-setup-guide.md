# tRPC Setup Guide

## Overview

tRPC enables end-to-end type safety between TypeScript frontend and backend with zero codegen. This guide covers router patterns, middleware, validation, and React Query integration.

**Context7:** `/trpc/trpc` (Trust: High, Score: 92.7, Snippets: 900)

## Table of Contents

- [Core Concepts](#core-concepts)
- [Basic Setup](#basic-setup)
- [Router Patterns](#router-patterns)
- [Middleware](#middleware)
- [Validation with Zod](#validation-with-zod)
- [React Query Integration](#react-query-integration)
- [Error Handling](#error-handling)
- [Subscriptions](#subscriptions)

## Core Concepts

### What is tRPC?

tRPC allows you to build APIs with TypeScript that automatically share types between client and server. No code generation, no schema files, just TypeScript.

**Key Benefits:**
- **Type safety:** Frontend knows exact shape of backend responses
- **Autocomplete:** Full IntelliSense for API calls
- **Refactoring:** Rename backend function, frontend updates automatically
- **DX:** Instant feedback on breaking changes

### When to Use tRPC

✅ **Use tRPC when:**
- Full-stack TypeScript application
- Same team owns frontend and backend
- Want E2E type safety without codegen
- Rapid development priority

❌ **Avoid tRPC when:**
- Public API for third-party developers (use REST + OpenAPI)
- Multiple frontend frameworks (tRPC is TypeScript-only)
- Different teams own frontend/backend
- Need REST compatibility

## Basic Setup

### Installation

```bash
# Server
npm install @trpc/server zod

# Client (React)
npm install @trpc/client @trpc/react-query @tanstack/react-query
```

### Server Setup

```typescript
// server/trpc.ts
import { initTRPC } from '@trpc/server'

const t = initTRPC.create()

export const router = t.router
export const publicProcedure = t.procedure
```

```typescript
// server/routers/app.ts
import { z } from 'zod'
import { router, publicProcedure } from '../trpc'

export const appRouter = router({
  hello: publicProcedure
    .input(z.object({ name: z.string() }))
    .query(({ input }) => {
      return { greeting: `Hello ${input.name}!` }
    }),

  createUser: publicProcedure
    .input(z.object({
      name: z.string(),
      email: z.string().email()
    }))
    .mutation(async ({ input }) => {
      const user = await db.user.create({
        data: input
      })
      return user
    })
})

export type AppRouter = typeof appRouter
```

```typescript
// server/index.ts (Express)
import express from 'express'
import * as trpcExpress from '@trpc/server/adapters/express'
import { appRouter } from './routers/app'

const app = express()

app.use(
  '/trpc',
  trpcExpress.createExpressMiddleware({
    router: appRouter
  })
)

app.listen(3000)
```

```typescript
// server/index.ts (Standalone HTTP)
import { createHTTPServer } from '@trpc/server/adapters/standalone'
import { appRouter } from './routers/app'

createHTTPServer({
  router: appRouter
}).listen(3000)
```

### Client Setup

```typescript
// client/trpc.ts
import { createTRPCReact } from '@trpc/react-query'
import type { AppRouter } from '../server/routers/app'

export const trpc = createTRPCReact<AppRouter>()
```

```typescript
// client/App.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { httpBatchLink } from '@trpc/client'
import { trpc } from './trpc'

const queryClient = new QueryClient()

const trpcClient = trpc.createClient({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/trpc'
    })
  ]
})

function App() {
  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        <YourApp />
      </QueryClientProvider>
    </trpc.Provider>
  )
}
```

## Router Patterns

### Nested Routers

Organize routes by feature:

```typescript
// server/routers/users.ts
import { router, publicProcedure } from '../trpc'
import { z } from 'zod'

export const usersRouter = router({
  list: publicProcedure.query(async () => {
    return db.user.findMany()
  }),

  getById: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      return db.user.findUnique({ where: { id: input.id } })
    }),

  create: publicProcedure
    .input(z.object({
      name: z.string(),
      email: z.string().email()
    }))
    .mutation(async ({ input }) => {
      return db.user.create({ data: input })
    }),

  update: publicProcedure
    .input(z.object({
      id: z.string(),
      name: z.string().optional(),
      email: z.string().email().optional()
    }))
    .mutation(async ({ input }) => {
      const { id, ...data } = input
      return db.user.update({
        where: { id },
        data
      })
    }),

  delete: publicProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ input }) => {
      return db.user.delete({ where: { id: input.id } })
    })
})
```

```typescript
// server/routers/posts.ts
export const postsRouter = router({
  list: publicProcedure.query(() => db.post.findMany()),
  // ... other post routes
})
```

```typescript
// server/routers/app.ts
import { router } from '../trpc'
import { usersRouter } from './users'
import { postsRouter } from './posts'

export const appRouter = router({
  users: usersRouter,
  posts: postsRouter
})

export type AppRouter = typeof appRouter
```

**Client usage:**
```typescript
// Type-safe nested routes!
const users = trpc.users.list.useQuery()
const user = trpc.users.getById.useQuery({ id: '123' })
const createUser = trpc.users.create.useMutation()
```

### Context Pattern

Share data across all procedures (auth, database, etc.):

```typescript
// server/context.ts
import { inferAsyncReturnType } from '@trpc/server'
import * as trpcExpress from '@trpc/server/adapters/express'

export const createContext = ({
  req,
  res
}: trpcExpress.CreateExpressContextOptions) => {
  async function getUserFromHeader() {
    if (req.headers.authorization) {
      // Decode JWT, fetch user, etc.
      return getUser(req.headers.authorization)
    }
    return null
  }

  return {
    req,
    res,
    user: getUserFromHeader(),
    db
  }
}

export type Context = inferAsyncReturnType<typeof createContext>
```

```typescript
// server/trpc.ts
import { initTRPC } from '@trpc/server'
import type { Context } from './context'

const t = initTRPC.context<Context>().create()

export const router = t.router
export const publicProcedure = t.procedure
```

**Usage in procedures:**
```typescript
export const appRouter = router({
  getProfile: publicProcedure.query(async ({ ctx }) => {
    if (!ctx.user) {
      throw new TRPCError({ code: 'UNAUTHORIZED' })
    }
    return ctx.user
  })
})
```

## Middleware

### Authentication Middleware

```typescript
// server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server'
import type { Context } from './context'

const t = initTRPC.context<Context>().create()

const isAuthed = t.middleware(async ({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' })
  }

  return next({
    ctx: {
      user: ctx.user // Narrow type to non-null
    }
  })
})

export const router = t.router
export const publicProcedure = t.procedure
export const protectedProcedure = t.procedure.use(isAuthed)
```

**Usage:**
```typescript
export const appRouter = router({
  public: publicProcedure.query(() => {
    return { message: 'Anyone can access' }
  }),

  protected: protectedProcedure.query(({ ctx }) => {
    // ctx.user is guaranteed to exist here
    return { message: `Hello ${ctx.user.name}` }
  })
})
```

### Logging Middleware

```typescript
const logger = t.middleware(async ({ path, type, next }) => {
  const start = Date.now()

  const result = await next()

  const duration = Date.now() - start
  console.log(`${type} ${path} - ${duration}ms`)

  return result
})

export const loggedProcedure = t.procedure.use(logger)
```

### Rate Limiting Middleware

```typescript
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s')
})

const rateLimited = t.middleware(async ({ ctx, next }) => {
  const identifier = ctx.user?.id || ctx.req.ip

  const { success } = await ratelimit.limit(identifier)

  if (!success) {
    throw new TRPCError({
      code: 'TOO_MANY_REQUESTS',
      message: 'Rate limit exceeded'
    })
  }

  return next()
})

export const limitedProcedure = t.procedure.use(rateLimited)
```

## Validation with Zod

### Input Validation

```typescript
import { z } from 'zod'

const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(18).max(120).optional(),
  role: z.enum(['user', 'admin']).default('user')
})

export const appRouter = router({
  createUser: publicProcedure
    .input(createUserSchema)
    .mutation(async ({ input }) => {
      // input is typed and validated!
      return db.user.create({ data: input })
    })
})
```

### Output Validation

```typescript
const userOutputSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  createdAt: z.date()
})

export const appRouter = router({
  getUser: publicProcedure
    .input(z.object({ id: z.string() }))
    .output(userOutputSchema)
    .query(async ({ input }) => {
      const user = await db.user.findUnique({ where: { id: input.id } })

      if (!user) {
        throw new TRPCError({ code: 'NOT_FOUND' })
      }

      // Return value is validated against output schema
      return user
    })
})
```

### Reusable Schemas

```typescript
// schemas/user.ts
export const userSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  createdAt: z.date()
})

export const createUserSchema = userSchema.omit({ id: true, createdAt: true })
export const updateUserSchema = createUserSchema.partial()

// routers/users.ts
import { userSchema, createUserSchema, updateUserSchema } from '../schemas/user'

export const usersRouter = router({
  create: publicProcedure
    .input(createUserSchema)
    .output(userSchema)
    .mutation(({ input }) => db.user.create({ data: input })),

  update: publicProcedure
    .input(z.object({ id: z.string(), data: updateUserSchema }))
    .output(userSchema)
    .mutation(({ input }) =>
      db.user.update({ where: { id: input.id }, data: input.data })
    )
})
```

## React Query Integration

### Queries

```typescript
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = trpc.users.getById.useQuery({ id: userId })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <div>{data.name}</div>
}
```

### Mutations

```typescript
function CreateUserForm() {
  const createUser = trpc.users.create.useMutation()
  const utils = trpc.useUtils()

  const handleSubmit = async (data: CreateUserInput) => {
    await createUser.mutateAsync(data, {
      onSuccess: () => {
        // Invalidate users list query
        utils.users.list.invalidate()
      }
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <button type="submit" disabled={createUser.isLoading}>
        {createUser.isLoading ? 'Creating...' : 'Create User'}
      </button>

      {createUser.error && (
        <div>Error: {createUser.error.message}</div>
      )}
    </form>
  )
}
```

### Optimistic Updates

```typescript
function UpdateUserForm({ userId }: { userId: string }) {
  const utils = trpc.useUtils()
  const updateUser = trpc.users.update.useMutation({
    onMutate: async (newData) => {
      // Cancel outgoing refetches
      await utils.users.getById.cancel({ id: userId })

      // Snapshot previous value
      const previousUser = utils.users.getById.getData({ id: userId })

      // Optimistically update
      utils.users.getById.setData({ id: userId }, (old) => ({
        ...old!,
        ...newData.data
      }))

      return { previousUser }
    },
    onError: (err, newData, context) => {
      // Rollback on error
      utils.users.getById.setData({ id: userId }, context.previousUser)
    },
    onSettled: () => {
      // Refetch after success or error
      utils.users.getById.invalidate({ id: userId })
    }
  })

  return (/* form */)
}
```

### Infinite Queries

```typescript
function UserList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage
  } = trpc.users.list.useInfiniteQuery(
    { limit: 20 },
    {
      getNextPageParam: (lastPage) => lastPage.nextCursor
    }
  )

  const allUsers = data?.pages.flatMap(page => page.items) ?? []

  return (
    <div>
      {allUsers.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}

      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  )
}
```

## Error Handling

### Throwing Errors

```typescript
import { TRPCError } from '@trpc/server'

export const appRouter = router({
  getUser: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      const user = await db.user.findUnique({ where: { id: input.id } })

      if (!user) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: `User with id ${input.id} not found`
        })
      }

      return user
    })
})
```

**Error Codes:**
- `BAD_REQUEST` - Invalid input
- `UNAUTHORIZED` - Not authenticated
- `FORBIDDEN` - Not authorized
- `NOT_FOUND` - Resource not found
- `TIMEOUT` - Request timeout
- `CONFLICT` - Resource conflict
- `PRECONDITION_FAILED` - Precondition failed
- `PAYLOAD_TOO_LARGE` - Payload too large
- `METHOD_NOT_SUPPORTED` - Method not supported
- `TOO_MANY_REQUESTS` - Rate limited
- `INTERNAL_SERVER_ERROR` - Server error

### Custom Error Data

```typescript
throw new TRPCError({
  code: 'BAD_REQUEST',
  message: 'Validation failed',
  cause: validationError,
  data: {
    fields: {
      email: ['Email is required', 'Email must be valid']
    }
  }
})
```

### Client Error Handling

```typescript
function Component() {
  const { error } = trpc.users.getById.useQuery({ id: '123' })

  if (error) {
    // error.data contains custom error data
    if (error.data?.code === 'NOT_FOUND') {
      return <NotFound />
    }

    return <div>Error: {error.message}</div>
  }

  return <div>Success</div>
}
```

## Subscriptions

Real-time updates via WebSocket:

```typescript
// server/routers/posts.ts
import { observable } from '@trpc/server/observable'
import { EventEmitter } from 'events'

const ee = new EventEmitter()

export const postsRouter = router({
  onPostCreated: publicProcedure.subscription(() => {
    return observable<Post>((emit) => {
      const onCreate = (post: Post) => {
        emit.next(post)
      }

      ee.on('post:created', onCreate)

      return () => {
        ee.off('post:created', onCreate)
      }
    })
  }),

  create: publicProcedure
    .input(createPostSchema)
    .mutation(async ({ input }) => {
      const post = await db.post.create({ data: input })

      // Emit event
      ee.emit('post:created', post)

      return post
    })
})
```

```typescript
// client
function PostFeed() {
  trpc.posts.onPostCreated.useSubscription(undefined, {
    onData(post) {
      console.log('New post:', post)
      // Update UI, invalidate queries, etc.
    }
  })

  return <div>...</div>
}
```

## Best Practices

1. **Organize routers by feature** - `users`, `posts`, not `queries`, `mutations`
2. **Use Zod for validation** - Type-safe input/output validation
3. **Leverage middleware** - DRY for auth, logging, rate limiting
4. **Type your context** - Makes procedures type-safe
5. **Use React Query features** - Optimistic updates, infinite queries, caching
6. **Handle errors properly** - Use appropriate error codes
7. **Version breaking changes** - Nested routers make versioning easier
8. **Document procedures** - JSDoc comments for IntelliSense

## OpenAPI Integration

Expose tRPC as REST API:

```bash
npm install trpc-openapi
```

```typescript
import { generateOpenApiDocument } from 'trpc-openapi'
import { appRouter } from './routers/app'

export const openApiDocument = generateOpenApiDocument(appRouter, {
  title: 'My API',
  version: '1.0.0',
  baseUrl: 'http://localhost:3000'
})
```

See `openapi-documentation.md` for full integration guide.
