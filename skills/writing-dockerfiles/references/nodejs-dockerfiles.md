# Node.js Dockerfiles

Complete patterns for containerizing Node.js applications with npm, pnpm, and yarn.

## Table of Contents

1. [Base Image Selection](#base-image-selection)
2. [Pattern 1: npm (Standard)](#pattern-1-npm-standard)
3. [Pattern 2: pnpm (Monorepos)](#pattern-2-pnpm-monorepos)
4. [Pattern 3: yarn (Classic)](#pattern-3-yarn-classic)
5. [TypeScript Compilation](#typescript-compilation)
6. [Common Node.js Pitfalls](#common-nodejs-pitfalls)

## Base Image Selection

**Recommended Node.js base images:**

| Image | Size | Use Case |
|-------|------|----------|
| `node:20-alpine` | ~180MB | Production (recommended) |
| `node:20-slim` | ~250MB | If Alpine compatibility issues |
| `node:20` | ~1GB | Development only |
| `gcr.io/distroless/nodejs20-debian12` | ~150MB | Maximum security |

**Version pinning:**
```dockerfile
# ✅ Good: Exact version
FROM node:20.11.0-alpine

# ⚠️ OK: Minor version pinned
FROM node:20-alpine

# ❌ Bad: Unpredictable
FROM node:alpine
FROM node:latest
```

**Built-in node user:**
All official Node images include a `node` user (UID 1000) for non-root execution.

## Pattern 1: npm (Standard)

**Use when:**
- Standard Node.js projects
- Single-repo applications
- No workspace/monorepo requirements

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies (use npm ci for reproducible builds)
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy source code
COPY . .

# Build application (if TypeScript or bundling needed)
RUN npm run build

# Prune dev dependencies
RUN npm prune --omit=dev

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy production node_modules and built code
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Use built-in node user
USER node

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Key commands:**
- `npm ci` → Clean install from package-lock.json (reproducible)
- `npm install` → May update package-lock.json (avoid in Docker)
- `npm prune --omit=dev` → Remove dev dependencies

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 200-350MB

## Pattern 2: pnpm (Monorepos)

**Use when:**
- Monorepo projects
- Need efficient disk usage (pnpm store)
- Turborepo or Nx workspaces

**Multi-stage Dockerfile (monorepo-optimized):**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

# Enable Corepack for pnpm
RUN corepack enable && corepack prepare pnpm@8.15.0 --activate

WORKDIR /app

# Copy workspace configuration
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

# Copy package.json files for all packages (leverage layer caching)
COPY packages/api/package.json ./packages/api/
COPY packages/shared/package.json ./packages/shared/

# Install all dependencies
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build specific package
RUN pnpm --filter=api build

# Prune to production dependencies for specific package
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm --filter=api --prod deploy pruned

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy pruned production dependencies and built code
COPY --from=builder /app/pruned/node_modules ./node_modules
COPY --from=builder /app/pruned/dist ./dist
COPY --from=builder /app/pruned/package.json ./

# Use built-in node user
USER node

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**pnpm-workspace.yaml:**
```yaml
packages:
  - 'packages/*'
```

**Key pnpm commands:**
- `pnpm install --frozen-lockfile` → Reproducible install
- `pnpm --filter=api build` → Build specific package
- `pnpm --prod deploy pruned` → Create production-only deploy

**Build command:**
```bash
docker build -t myapp-api:latest .
```

**Expected size:** 180-320MB

## Pattern 3: yarn (Classic)

**Use when:**
- Existing yarn projects
- Yarn 1.x (classic) in use

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./

# Install dependencies
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --frozen-lockfile --production=false

# Copy source code
COPY . .

# Build application
RUN yarn build

# Install production dependencies only
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --frozen-lockfile --production=true --ignore-scripts --prefer-offline

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy production dependencies and built code
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Use built-in node user
USER node

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Key yarn commands:**
- `yarn install --frozen-lockfile` → Reproducible install
- `--production=false` → Install all deps (for building)
- `--production=true` → Production deps only

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 200-350MB

## TypeScript Compilation

**Pattern: Separate build and runtime stages**

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy TypeScript source
COPY tsconfig.json ./
COPY src ./src

# Compile TypeScript to JavaScript
RUN npm run build

# Prune dev dependencies (TypeScript no longer needed)
RUN npm prune --omit=dev

# Runtime stage (no TypeScript, just Node.js)
FROM node:20-alpine

WORKDIR /app

# Copy compiled JavaScript and production dependencies
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER node

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**tsconfig.json (example):**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**package.json scripts:**
```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts"
  }
}
```

## Common Node.js Pitfalls

### Pitfall 1: Using npm install Instead of npm ci

**Problem:** `npm install` may update package-lock.json, causing non-reproducible builds.

```dockerfile
# ❌ Non-reproducible builds
RUN npm install
```

**Solution:** Always use `npm ci` in Docker:
```dockerfile
# ✅ Reproducible builds from package-lock.json
RUN npm ci
```

### Pitfall 2: Not Pruning Dev Dependencies

**Problem:** Dev dependencies bloat production image.

```dockerfile
# ❌ Includes dev dependencies (jest, typescript, etc.)
RUN npm ci
# Image size: 500MB+
```

**Solution:** Prune dev dependencies or use `--omit=dev`:
```dockerfile
# ✅ Production dependencies only
RUN npm ci --omit=dev
# OR
RUN npm ci && npm prune --omit=dev
# Image size: 250MB
```

### Pitfall 3: Copying node_modules Before Install

**Problem:** Local node_modules (from different OS) conflicts with Docker install.

```dockerfile
# ❌ Copies local node_modules (macOS) to Linux container
COPY . .
RUN npm ci
```

**Solution:** Copy package files first, install, then copy source:
```dockerfile
# ✅ Correct order
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

**Better:** Use .dockerignore to exclude node_modules:
```
node_modules/
dist/
```

### Pitfall 4: Not Using Cache Mounts for npm

**Problem:** Re-downloads packages every build.

```dockerfile
# ❌ Re-downloads every time
RUN npm ci
```

**Solution:** Use BuildKit cache mount:
```dockerfile
# ✅ Persistent cache across builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

### Pitfall 5: Running as Root

**Problem:** Security risk if container is compromised.

```dockerfile
# ❌ Runs as root (UID 0)
CMD ["node", "dist/index.js"]
```

**Solution:** Use built-in node user:
```dockerfile
# ✅ Runs as non-root (UID 1000)
USER node
CMD ["node", "dist/index.js"]
```

### Pitfall 6: Not Setting NODE_ENV

**Problem:** Express and other frameworks behave differently in production.

```dockerfile
# ❌ Defaults to development mode
CMD ["node", "dist/index.js"]
```

**Solution:** Set NODE_ENV=production:
```dockerfile
# ✅ Production optimizations enabled
ENV NODE_ENV=production
CMD ["node", "dist/index.js"]
```

## Express.js Complete Example

**Production-ready Express API:**

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy source code
COPY . .

# Build application (if TypeScript)
RUN npm run build

# Prune dev dependencies
RUN npm prune --omit=dev

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy production files
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Use built-in node user
USER node

# Production environment
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**src/index.ts:**
```typescript
import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

**Expected size:** 220-300MB

## Next.js Complete Example

**Production-optimized Next.js application:**

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Builder stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Build Next.js application
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy necessary files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Use built-in node user
USER node

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

EXPOSE 3000
CMD ["node", "server.js"]
```

**next.config.js (required for standalone):**
```javascript
module.exports = {
  output: 'standalone',
};
```

**Expected size:** 150-250MB (standalone output is optimized)

## NestJS Complete Example

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy source code
COPY . .

# Build NestJS application
RUN npm run build

# Prune dev dependencies
RUN npm prune --omit=dev

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy production files
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Use built-in node user
USER node

ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

EXPOSE 3000
CMD ["node", "dist/main.js"]
```

**Expected size:** 250-350MB

## Private npm Registry Example

**Using BuildKit secret mount for NPM_TOKEN:**

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install from private registry using secret
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    --mount=type=cache,target=/root/.npm \
    npm ci

# Copy source and build
COPY . .
RUN npm run build
RUN npm prune --omit=dev

# Runtime stage
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER node

ENV NODE_ENV=production

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**.npmrc file (local, not committed):**
```
//registry.npmjs.org/:_authToken=${NPM_TOKEN}
```

**Build command:**
```bash
# Create temporary .npmrc with token
echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc.tmp

# Build with secret mount
docker buildx build --secret id=npmrc,src=.npmrc.tmp -t myapp:latest .

# Clean up
rm .npmrc.tmp
```

**Alternative: Environment variable substitution**
```dockerfile
RUN --mount=type=secret,id=npm_token \
    echo "//registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token)" > ~/.npmrc && \
    npm ci && \
    rm ~/.npmrc
```

## Summary

**Choose package manager based on needs:**

| Package Manager | Use Case | Build Time | Cache Efficiency | Monorepo Support |
|----------------|----------|------------|------------------|------------------|
| npm | Standard projects | Medium | Good | Limited |
| pnpm | Monorepos, efficiency | Fast | Excellent | Excellent |
| yarn | Existing yarn projects | Medium | Good | Good |

**Key takeaways:**
- Always use multi-stage builds
- Use `npm ci` (not `npm install`) for reproducible builds
- Use BuildKit cache mounts for package managers
- Prune dev dependencies in production
- Use built-in `node` user (UID 1000)
- Set `NODE_ENV=production`
- Use Alpine variants for smaller images
- Copy package files before source code (layer caching)
- Exclude node_modules in .dockerignore
