# Auth.js + Next.js Example

Complete authentication implementation using Auth.js v5 with Next.js 15.

## Features

- OAuth 2.1 providers (Google, GitHub)
- Credentials authentication (email + password)
- JWT sessions with EdDSA signing
- Protected routes via middleware
- Role-based access control
- Refresh token rotation

## Setup

```bash
npm install next@15 next-auth@beta jose zod @node-rs/argon2
```

## Environment Variables

Create `.env.local`:

```env
# Auth.js
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-generate-with-openssl-rand-base64-32

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/auth_demo
```

## File Structure

```
authjs-nextjs/
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...nextauth]/
│   │           └── route.ts         # Auth.js configuration
│   ├── login/
│   │   └── page.tsx                 # Login page
│   ├── dashboard/
│   │   └── page.tsx                 # Protected dashboard
│   └── layout.tsx                   # Root layout
├── lib/
│   ├── auth.ts                      # Auth.js setup
│   ├── db.ts                        # Database client
│   └── password.ts                  # Password hashing
├── middleware.ts                    # Route protection
└── types/
    └── next-auth.d.ts               # TypeScript types
```

## Implementation

### 1. Auth.js Configuration

**app/api/auth/[...nextauth]/route.ts:**

```typescript
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import GitHubProvider from 'next-auth/providers/github'
import CredentialsProvider from 'next-auth/providers/credentials'
import { z } from 'zod'
import { hash, verify } from '@node-rs/argon2'
import { db } from '@/lib/db'

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    // OAuth 2.1 Providers (PKCE automatic)
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          prompt: 'consent',
          access_type: 'offline',
          response_type: 'code',
        },
      },
    }),

    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),

    // Credentials Provider
    CredentialsProvider({
      id: 'credentials',
      name: 'Email and Password',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const result = LoginSchema.safeParse(credentials)
        if (!result.success) {
          throw new Error('Invalid credentials')
        }

        const { email, password } = result.data

        // Find user
        const user = await db.user.findUnique({ where: { email } })
        if (!user?.passwordHash) {
          throw new Error('Invalid credentials')
        }

        // Verify password (Argon2id, timing-safe)
        const isValid = await verify(user.passwordHash, password)
        if (!isValid) {
          throw new Error('Invalid credentials')
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role,
        }
      },
    }),
  ],

  session: {
    strategy: 'jwt',
    maxAge: 7 * 24 * 60 * 60, // 7 days
  },

  callbacks: {
    async jwt({ token, user, account, trigger }) {
      // Initial sign in
      if (user) {
        token.id = user.id
        token.role = user.role
      }

      // OAuth tokens
      if (account) {
        token.accessToken = account.access_token
        token.refreshToken = account.refresh_token
        token.accessTokenExpires = account.expires_at
      }

      // Refresh access token if expired
      if (trigger === 'update' && token.accessTokenExpires) {
        if (Date.now() < token.accessTokenExpires * 1000) {
          return token
        }
        return refreshAccessToken(token)
      }

      return token
    },

    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
        session.user.role = token.role as string
      }
      return session
    },

    async authorized({ auth, request }) {
      const { pathname } = request.nextUrl

      // Public routes
      if (pathname === '/login' || pathname === '/') {
        return true
      }

      // Protected routes
      if (pathname.startsWith('/dashboard')) {
        return !!auth?.user
      }

      // Admin routes
      if (pathname.startsWith('/admin')) {
        return auth?.user?.role === 'admin'
      }

      return true
    },
  },

  pages: {
    signIn: '/login',
    error: '/login',
  },
})

async function refreshAccessToken(token: any) {
  try {
    const response = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id: process.env.GOOGLE_CLIENT_ID!,
        client_secret: process.env.GOOGLE_CLIENT_SECRET!,
        grant_type: 'refresh_token',
        refresh_token: token.refreshToken,
      }),
    })

    const refreshedTokens = await response.json()

    if (!response.ok) {
      throw refreshedTokens
    }

    return {
      ...token,
      accessToken: refreshedTokens.access_token,
      accessTokenExpires: Date.now() + refreshedTokens.expires_in * 1000,
      refreshToken: refreshedTokens.refresh_token ?? token.refreshToken,
    }
  } catch (error) {
    console.error('Error refreshing access token', error)
    return { ...token, error: 'RefreshAccessTokenError' }
  }
}

export const { GET, POST } = handlers
```

### 2. Login Page

**app/login/page.tsx:**

```typescript
'use client'

import { signIn } from 'next-auth/react'
import { useState } from 'react'
import { z } from 'zod'

const LoginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be 8+ characters'),
})

export default function LoginPage() {
  const [error, setError] = useState('')

  async function handleCredentialsLogin(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)

    const result = LoginSchema.safeParse({
      email: formData.get('email'),
      password: formData.get('password'),
    })

    if (!result.success) {
      setError(result.error.errors[0].message)
      return
    }

    const response = await signIn('credentials', {
      email: result.data.email,
      password: result.data.password,
      redirect: false,
    })

    if (response?.error) {
      setError('Invalid credentials')
    } else {
      window.location.href = '/dashboard'
    }
  }

  async function handleOAuthLogin(provider: 'google' | 'github') {
    await signIn(provider, { callbackUrl: '/dashboard' })
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full space-y-8">
        <h2 className="text-3xl font-bold text-center">Sign In</h2>

        {/* OAuth Providers */}
        <div className="space-y-3">
          <button
            onClick={() => handleOAuthLogin('google')}
            className="w-full flex items-center justify-center gap-3 px-4 py-2 border rounded-lg hover:bg-gray-50"
          >
            Continue with Google
          </button>

          <button
            onClick={() => handleOAuthLogin('github')}
            className="w-full flex items-center justify-center gap-3 px-4 py-2 border rounded-lg hover:bg-gray-50"
          >
            Continue with GitHub
          </button>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or continue with</span>
          </div>
        </div>

        {/* Credentials Login */}
        <form onSubmit={handleCredentialsLogin} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          {error && (
            <div className="text-red-600 text-sm">{error}</div>
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  )
}
```

### 3. Protected Dashboard

**app/dashboard/page.tsx:**

```typescript
import { auth } from '@/app/api/auth/[...nextauth]/route'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Session Information</h2>

        <dl className="space-y-2">
          <div>
            <dt className="font-medium text-gray-700">Email:</dt>
            <dd className="text-gray-900">{session.user?.email}</dd>
          </div>

          <div>
            <dt className="font-medium text-gray-700">Name:</dt>
            <dd className="text-gray-900">{session.user?.name}</dd>
          </div>

          <div>
            <dt className="font-medium text-gray-700">Role:</dt>
            <dd className="text-gray-900">{session.user?.role}</dd>
          </div>
        </dl>
      </div>
    </div>
  )
}
```

### 4. Middleware (Route Protection)

**middleware.ts:**

```typescript
import { auth } from '@/app/api/auth/[...nextauth]/route'

export default auth((req) => {
  const { pathname } = req.nextUrl

  // Redirect authenticated users away from login
  if (pathname === '/login' && req.auth) {
    return Response.redirect(new URL('/dashboard', req.url))
  }

  // Protect dashboard routes
  if (pathname.startsWith('/dashboard') && !req.auth) {
    return Response.redirect(new URL('/login', req.url))
  }

  // Protect admin routes
  if (pathname.startsWith('/admin') && req.auth?.user?.role !== 'admin') {
    return Response.redirect(new URL('/dashboard', req.url))
  }
})

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

## Database Schema (Prisma)

**prisma/schema.prisma:**

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id           String    @id @default(cuid())
  email        String    @unique
  name         String?
  passwordHash String?
  role         String    @default("user")
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt

  @@index([email])
}
```

## Running the Example

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up database:**
   ```bash
   npx prisma migrate dev
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Test:**
   - Visit http://localhost:3000/login
   - Sign in with Google/GitHub or credentials
   - Access /dashboard (protected route)

## Security Features

- OAuth 2.1 with PKCE (automatic in Auth.js)
- Argon2id password hashing (OWASP 2025 parameters)
- JWT sessions with EdDSA signing
- HTTP-only cookies for session storage
- CSRF protection (built-in)
- Role-based access control
- Refresh token rotation

## Production Checklist

- [ ] Set strong NEXTAUTH_SECRET
- [ ] Configure OAuth redirect URIs in providers
- [ ] Enable HTTPS
- [ ] Set up rate limiting on login endpoint
- [ ] Implement password reset flow
- [ ] Add email verification
- [ ] Set up monitoring and alerting
- [ ] Configure session timeout
- [ ] Add audit logging
