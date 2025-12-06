# Production-Ready Express.js Application Dockerfile
#
# This example demonstrates:
# - Multi-stage build with npm
# - BuildKit cache mounts for npm packages
# - TypeScript compilation
# - Production dependencies only in runtime
# - Non-root user (built-in node user)
# - Health check implementation
#
# Expected image size: 220-300MB
#
# Build: docker build -f nodejs-express.Dockerfile -t express-app:latest .
# Run: docker run -p 3000:3000 express-app:latest

# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install all dependencies (including devDependencies for building)
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy source code
COPY . .

# Build TypeScript to JavaScript
RUN npm run build

# Prune development dependencies
RUN npm prune --omit=dev

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy production node_modules and built code
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Use built-in node user (UID 1000)
USER node

# Production environment
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

EXPOSE 3000

CMD ["node", "dist/index.js"]
