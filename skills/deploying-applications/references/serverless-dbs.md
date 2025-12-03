# Serverless Databases (Scale-to-Zero)

Serverless database options that automatically scale to zero when not in use.

## Table of Contents

- [Neon PostgreSQL](#neon-postgresql)
- [Turso SQLite](#turso-sqlite)
- [PlanetScale MySQL](#planetscale-mysql)
- [Comparison](#comparison)

## Neon PostgreSQL

Serverless PostgreSQL with database branching and scale-to-zero compute.

### Key Features

- **Database Branching**: Create instant copies like Git branches
- **Scale-to-Zero**: Compute pauses after inactivity, resumes on first query
- **Separate Compute/Storage**: Pay only for what you use
- **PostgreSQL Compatibility**: Full Postgres 15/16 features
- **Cold Start**: <1 second

### When to Use

- Development environments (branch per PR)
- Variable traffic applications
- Cost-sensitive projects
- Need PostgreSQL features

### Pricing Model

- **Compute**: Per-hour usage (pauses automatically)
- **Storage**: Per GB/month
- **Free Tier**: 0.5 GB storage, reasonable compute

### Setup

**Sign Up**:
```bash
# Visit https://neon.tech
# Create project via dashboard
```

**Create Branch (Database Branching)**:

```bash
# Install Neon CLI
npm i -g neonctl

# Create branch from main
neonctl branches create --project-id <project-id> --name feature-123

# Get connection string
neonctl connection-string feature-123
```

**Connect from Application**:

```typescript
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  // Neon requires SSL
  ssl: { rejectUnauthorized: false }
});

// Queries work exactly like standard PostgreSQL
const result = await pool.query('SELECT * FROM users LIMIT 10');
```

### Pulumi Integration

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as neon from "@pulumiverse/neon";

// Create Neon project
const project = new neon.Project("my-app", {
    name: "my-app-production",
    regionId: "aws-us-east-1",
});

// Create main branch
const mainBranch = new neon.Branch("main", {
    projectId: project.id,
    name: "main",
});

// Create database on branch
const database = new neon.Database("app-db", {
    projectId: project.id,
    branchId: mainBranch.id,
    name: "myapp",
    ownerName: "neondb_owner",
});

// Export connection string
export const connectionString = pulumi.interpolate`postgres://neondb_owner:${project.databasePassword}@${mainBranch.host}/myapp`;
```

### Database Branching Workflow

**Development Pattern**:

```bash
# Create branch for feature
neonctl branches create --name feature-auth-refactor

# Get connection string
neonctl connection-string feature-auth-refactor

# Use in local development
export DATABASE_URL=<branch-connection-string>

# Test migrations
npm run migrate

# Merge feature, delete branch
neonctl branches delete feature-auth-refactor
```

**CI/CD Pattern**:

```yaml
# .github/workflows/test.yml
name: Test
on: pull_request

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Create Neon branch
        id: create-branch
        run: |
          BRANCH=$(neonctl branches create \
            --project-id ${{ secrets.NEON_PROJECT_ID }} \
            --name pr-${{ github.event.pull_request.number }} \
            --output json)
          echo "connection_string=$(echo $BRANCH | jq -r .connection_string)" >> $GITHUB_OUTPUT

      - name: Run tests
        env:
          DATABASE_URL: ${{ steps.create-branch.outputs.connection_string }}
        run: npm test

      - name: Delete branch
        if: always()
        run: |
          neonctl branches delete pr-${{ github.event.pull_request.number }}
```

## Turso SQLite

Edge SQLite database with sub-millisecond read latency.

### Key Features

- **Edge Deployment**: 200+ global locations
- **Sub-millisecond Reads**: <1ms from edge
- **libSQL**: SQLite fork with improved replication
- **Multi-region Replication**: Automatic data sync
- **Embedded Replicas**: Local SQLite + edge sync

### When to Use

- Edge functions (Cloudflare Workers, Deno Deploy)
- Global applications requiring low latency
- Read-heavy workloads
- Simple data models (SQLite)

### Pricing Model

- **Rows Read**: Per million rows
- **Rows Written**: Per million rows
- **Storage**: Per GB/month
- **Free Tier**: 500 MB storage, 1B row reads/month

### Setup

```bash
# Install Turso CLI
brew install tursodatabase/tap/turso

# Sign up
turso auth signup

# Create database
turso db create my-app

# Get connection URL
turso db show my-app --url

# Get auth token
turso db tokens create my-app
```

### Client Usage (TypeScript)

**Edge Function (Cloudflare Workers)**:

```typescript
import { createClient } from '@libsql/client/web';

export default {
  async fetch(request: Request, env: Env) {
    const client = createClient({
      url: env.TURSO_DATABASE_URL,
      authToken: env.TURSO_AUTH_TOKEN,
    });

    // Query from edge (sub-millisecond latency)
    const result = await client.execute({
      sql: 'SELECT * FROM users WHERE id = ?',
      args: [userId],
    });

    return new Response(JSON.stringify(result.rows));
  },
};
```

**Server-Side (Node.js)**:

```typescript
import { createClient } from '@libsql/client';

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!,
});

// Batch queries for efficiency
const batch = await client.batch([
  { sql: 'SELECT * FROM users WHERE active = ?', args: [true] },
  { sql: 'SELECT COUNT(*) FROM orders', args: [] },
]);

console.log(batch[0].rows); // Active users
console.log(batch[1].rows); // Order count
```

### Multi-Region Replication

```bash
# Create database with replicas
turso db create my-app --location iad --location fra --location syd

# Turso automatically routes reads to nearest replica
# Writes go to primary region
```

### Embedded Replicas (Local + Edge Sync)

```typescript
import { createClient } from '@libsql/client';

const client = createClient({
  url: 'file:local.db', // Local SQLite file
  syncUrl: process.env.TURSO_DATABASE_URL,
  authToken: process.env.TURSO_AUTH_TOKEN,
  syncInterval: 60, // Sync every 60 seconds
});

// Read from local file (instant)
const local = await client.execute('SELECT * FROM users LIMIT 10');

// Sync with edge
await client.sync();
```

## PlanetScale MySQL

Serverless MySQL powered by Vitess (YouTube's infrastructure).

### Key Features

- **Non-blocking Schema Changes**: Deploy migrations without downtime
- **Vitess-powered**: Battle-tested at Google/YouTube scale
- **Database Branching**: Development branches like Git
- **Per-row Pricing**: Pay only for rows read/written
- **Horizontal Scaling**: Automatic sharding

### When to Use

- MySQL-dependent applications
- Frequent schema changes
- Large-scale MySQL workloads
- Need MySQL compatibility

### Pricing Model

- **Rows Read**: Per billion rows
- **Rows Written**: Per million rows
- **Storage**: Per GB/month
- **Free Tier**: 5 GB storage, 1B rows read/month

### Setup

```bash
# Install PlanetScale CLI
brew install planetscale/tap/pscale

# Login
pscale auth login

# Create database
pscale database create my-app --region us-east

# Create branch
pscale branch create my-app dev

# Connect (creates proxy)
pscale connect my-app dev
```

### Connection (Node.js)

```typescript
import mysql from 'mysql2/promise';

const connection = await mysql.createConnection({
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  ssl: {
    rejectUnauthorized: true
  }
});

const [rows] = await connection.execute(
  'SELECT * FROM users WHERE email = ?',
  [email]
);
```

### Non-Blocking Schema Changes

**Traditional MySQL** (Blocking):
```sql
-- Table locks during migration
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
-- Downtime for large tables
```

**PlanetScale** (Non-blocking):
```bash
# 1. Create development branch
pscale branch create my-app add-phone-field

# 2. Connect and run migration
pscale connect my-app add-phone-field
mysql> ALTER TABLE users ADD COLUMN phone VARCHAR(20);

# 3. Create deploy request
pscale deploy-request create my-app add-phone-field

# 4. Review schema diff in UI
# 5. Deploy (non-blocking, zero downtime)
pscale deploy-request deploy my-app 1
```

### Branching Workflow

```bash
# Main branch (production)
pscale branch create my-app main

# Development branch
pscale branch create my-app dev --from main

# Feature branch
pscale branch create my-app feature-auth --from dev

# Promote to production
pscale deploy-request create my-app feature-auth
pscale deploy-request deploy my-app 1
```

## Comparison

### Feature Matrix

| Feature | Neon | Turso | PlanetScale |
|---------|------|-------|-------------|
| **Database** | PostgreSQL | SQLite | MySQL |
| **Scale-to-Zero** | ✅ Compute | ✅ Full | ❌ Always on |
| **Cold Start** | <1s | <1ms | N/A |
| **Edge Deployment** | ❌ | ✅ 200+ locations | ❌ |
| **Branching** | ✅ | ❌ | ✅ |
| **Replication** | ✅ | ✅ | ✅ |
| **ACID** | ✅ Full | ✅ Full | ✅ Full |
| **Max Connections** | Pooled | Unlimited | Pooled |
| **Free Tier** | 0.5 GB | 500 MB | 5 GB |

### Use Case Recommendations

**Neon (PostgreSQL)**:
- ✅ Need PostgreSQL features (JSONB, arrays, full-text search)
- ✅ Development branches (one per PR)
- ✅ Variable traffic (scale-to-zero cost savings)
- ✅ Familiar PostgreSQL ecosystem

**Turso (SQLite)**:
- ✅ Edge functions (Cloudflare Workers, Deno Deploy)
- ✅ Global low-latency (<50ms)
- ✅ Read-heavy workloads
- ✅ Simple data models
- ❌ Complex joins or large writes

**PlanetScale (MySQL)**:
- ✅ MySQL-dependent applications
- ✅ Frequent schema changes
- ✅ Large-scale workloads (>100 GB)
- ✅ Need horizontal sharding
- ❌ Scale-to-zero not available

### Cost Comparison (Example Workload)

**Assumptions**: 1M requests/month, 10 GB storage, 50% idle time

| Database | Monthly Cost | Scale-to-Zero Savings |
|----------|--------------|----------------------|
| **Neon** | ~$15 | ~$7.50 (50% savings) |
| **Turso** | ~$10 | Included (edge routing) |
| **PlanetScale** | ~$39 | N/A (always on) |

**Note**: Actual costs vary based on workload patterns.

## Integration Patterns

### With Pulumi

**Neon**:
```typescript
import * as neon from "@pulumiverse/neon";

const project = new neon.Project("app", {
    name: "my-app",
    regionId: "aws-us-east-1",
});
```

**Turso** (via environment variables):
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as cloudflare from "@pulumi/cloudflare";

const worker = new cloudflare.WorkerScript("api", {
    name: "api",
    content: pulumi.asset.FileAsset("./dist/worker.js"),
    secretTextBindings: [
        {
            name: "TURSO_DATABASE_URL",
            text: config.requireSecret("tursoUrl"),
        },
        {
            name: "TURSO_AUTH_TOKEN",
            text: config.requireSecret("tursoToken"),
        },
    ],
});
```

**PlanetScale** (connection string):
```typescript
import * as aws from "@pulumi/aws";

const lambda = new aws.lambda.Function("api", {
    runtime: "nodejs20.x",
    handler: "index.handler",
    environment: {
        variables: {
            DATABASE_URL: config.requireSecret("planetscaleUrl"),
        },
    },
});
```

### With Edge Functions

**Cloudflare Workers + Turso**:
```typescript
import { Hono } from 'hono'
import { createClient } from '@libsql/client/web'

const app = new Hono()

app.get('/users/:id', async (c) => {
  const client = createClient({
    url: c.env.TURSO_URL,
    authToken: c.env.TURSO_TOKEN,
  })

  const result = await client.execute({
    sql: 'SELECT * FROM users WHERE id = ?',
    args: [c.req.param('id')],
  })

  return c.json(result.rows[0])
})

export default app
```

**Deno Deploy + Turso**:
```typescript
import { serve } from "https://deno.land/std/http/server.ts";
import { createClient } from "npm:@libsql/client/web";

const client = createClient({
  url: Deno.env.get("TURSO_URL")!,
  authToken: Deno.env.get("TURSO_TOKEN")!,
});

serve(async (req: Request) => {
  const url = new URL(req.url);
  const id = url.searchParams.get("id");

  const result = await client.execute({
    sql: "SELECT * FROM users WHERE id = ?",
    args: [id],
  });

  return new Response(JSON.stringify(result.rows[0]));
});
```

## Best Practices

### Connection Pooling

**Neon (PostgreSQL)**:
```typescript
import { Pool } from 'pg';

// Use connection pooling
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Reuse pool across requests
export const query = (text: string, params: any[]) => {
  return pool.query(text, params);
};
```

**Turso (SQLite)**:
```typescript
// Create client once, reuse
const client = createClient({
  url: process.env.TURSO_URL!,
  authToken: process.env.TURSO_TOKEN!,
});

// Use batch queries for efficiency
const results = await client.batch([
  { sql: 'SELECT * FROM users', args: [] },
  { sql: 'SELECT * FROM posts', args: [] },
]);
```

### Error Handling

```typescript
try {
  const result = await client.execute({
    sql: 'SELECT * FROM users WHERE id = ?',
    args: [userId],
  });

  if (result.rows.length === 0) {
    throw new Error('User not found');
  }

  return result.rows[0];
} catch (error) {
  if (error.code === 'ECONNREFUSED') {
    // Database unavailable (cold start?)
    // Retry with exponential backoff
  }
  throw error;
}
```

### Migrations

**Neon (PostgreSQL) - Use branches**:
```bash
# Create migration branch
neonctl branches create migration-add-users

# Test migration
psql $MIGRATION_BRANCH_URL -f migrations/001_add_users.sql

# If successful, apply to main
psql $MAIN_BRANCH_URL -f migrations/001_add_users.sql
```

**Turso (SQLite) - Use schema versioning**:
```typescript
const SCHEMA_VERSION = 2;

async function migrate(client: Client) {
  const { rows } = await client.execute(
    'SELECT version FROM schema_version'
  );

  const currentVersion = rows[0]?.version || 0;

  if (currentVersion < 1) {
    await client.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)');
  }

  if (currentVersion < 2) {
    await client.execute('ALTER TABLE users ADD COLUMN email TEXT');
  }

  await client.execute(
    'UPDATE schema_version SET version = ?',
    [SCHEMA_VERSION]
  );
}
```

**PlanetScale - Use deploy requests**:
```bash
# Always use branches + deploy requests
pscale branch create my-app migration
pscale connect my-app migration
# Run migration
pscale deploy-request create my-app migration
pscale deploy-request deploy my-app 1
```
