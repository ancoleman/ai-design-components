# TypeScript tRPC Full-Stack Example

End-to-end type-safe API using tRPC with Next.js and Prisma.

## Features

- tRPC v11 (E2E type safety)
- Next.js 14 (App Router)
- Prisma (database)
- Zod validation
- React Query integration
- Zero codegen required

## Files

```
typescript-trpc/
├── src/
│   ├── server/
│   │   ├── trpc.ts          # tRPC instance
│   │   ├── routers/
│   │   │   ├── _app.ts      # Root router
│   │   │   ├── auth.ts
│   │   │   └── users.ts
│   │   └── context.ts       # Request context
│   ├── app/
│   │   ├── api/trpc/[trpc]/route.ts
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── utils/
│   │   └── trpc.ts          # Client setup
│   └── components/
│       └── UserList.tsx
├── prisma/schema.prisma
└── package.json
```

## Quick Start

```bash
# Install
npm install

# Setup database
npx prisma migrate dev

# Run dev server
npm run dev
```

## Server Setup

```typescript
// src/server/trpc.ts
import { initTRPC } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.create();

export const router = t.router;
export const publicProcedure = t.procedure;

// src/server/routers/users.ts
export const userRouter = router({
  list: publicProcedure.query(async () => {
    return await prisma.user.findMany();
  }),

  byId: publicProcedure
    .input(z.object({ id: z.number() }))
    .query(async ({ input }) => {
      return await prisma.user.findUnique({ where: { id: input.id } });
    }),

  create: publicProcedure
    .input(z.object({ email: z.string().email(), name: z.string() }))
    .mutation(async ({ input }) => {
      return await prisma.user.create({ data: input });
    }),
});

// src/server/routers/_app.ts
export const appRouter = router({
  user: userRouter,
  auth: authRouter,
});

export type AppRouter = typeof appRouter;
```

## Client Usage

```typescript
'use client';

import { trpc } from '@/utils/trpc';

export function UserList() {
  const { data: users, isLoading } = trpc.user.list.useQuery();
  const createUser = trpc.user.create.useMutation();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {users?.map(user => <div key={user.id}>{user.name}</div>)}

      <button onClick={() => createUser.mutate({
        email: 'new@example.com',
        name: 'New User'
      })}>
        Add User
      </button>
    </div>
  );
}
```

## Type Safety

```typescript
// ✅ Fully type-safe - no manual type definitions needed
const user = await trpc.user.byId.query({ id: 1 });
//    ^? User (inferred from server)

// ❌ TypeScript error if wrong type
await trpc.user.byId.query({ id: "wrong" });  // Error: Expected number
```

## Benefits

- Zero API boilerplate
- Catch errors at compile time
- Autocomplete for all endpoints
- Refactoring safety (rename propagates)
- React Query integration built-in
