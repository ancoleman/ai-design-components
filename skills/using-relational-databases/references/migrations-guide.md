# Database Migrations Guide


## Table of Contents

- [Safe Migration Patterns](#safe-migration-patterns)
  - [Multi-Phase Deployments](#multi-phase-deployments)
- [Common Patterns](#common-patterns)
  - [1. Adding a Column](#1-adding-a-column)
  - [2. Dropping a Column](#2-dropping-a-column)
  - [3. Renaming a Column](#3-renaming-a-column)
  - [4. Creating Indexes](#4-creating-indexes)
  - [5. Adding Foreign Keys](#5-adding-foreign-keys)
  - [6. Changing Column Type](#6-changing-column-type)
- [Migration Tools by Language](#migration-tools-by-language)
  - [Python (Alembic + SQLAlchemy)](#python-alembic-sqlalchemy)
  - [TypeScript (Prisma Migrate)](#typescript-prisma-migrate)
  - [TypeScript (Drizzle Kit)](#typescript-drizzle-kit)
  - [Rust (SQLx)](#rust-sqlx)
  - [Go (golang-migrate)](#go-golang-migrate)
- [Best Practices](#best-practices)
  - [1. Test Migrations in Staging](#1-test-migrations-in-staging)
  - [2. Measure Migration Duration](#2-measure-migration-duration)
  - [3. Concurrent Migrations](#3-concurrent-migrations)
  - [4. Monitor During Migration](#4-monitor-during-migration)
  - [5. Rollback Plan](#5-rollback-plan)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Don't Use Transactions for Long Operations](#dont-use-transactions-for-long-operations)
  - [❌ Don't Assume Migration Speed](#dont-assume-migration-speed)
  - [❌ Don't Mix Schema and Data Changes](#dont-mix-schema-and-data-changes)
- [Resources](#resources)

## Safe Migration Patterns

### Multi-Phase Deployments

**Problem:** Dropping columns or renaming tables can break running application instances during deployment.

**Solution:** Multi-phase migrations that maintain backward compatibility.

## Common Patterns

### 1. Adding a Column

**Safe (Single Phase):**
```sql
-- Phase 1: Add column (nullable)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Later: Make NOT NULL after backfill
-- ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

**Why Safe:** New code can write to column, old code ignores it.

### 2. Dropping a Column

**Unsafe:**
```sql
-- DON'T DO THIS
ALTER TABLE users DROP COLUMN deprecated_field;
-- Running instances will crash!
```

**Safe (Multi-Phase):**
```sql
-- Phase 1: Make nullable, deploy code that doesn't use column
ALTER TABLE users ALTER COLUMN deprecated_field DROP NOT NULL;

-- Phase 2: Drop constraints, deploy
-- (Deploy and monitor)

-- Phase 3: Drop column after confirming no code uses it
-- ALTER TABLE users DROP COLUMN deprecated_field;
```

### 3. Renaming a Column

**Unsafe:**
```sql
-- DON'T DO THIS
ALTER TABLE users RENAME COLUMN email TO user_email;
-- Running instances will fail!
```

**Safe (Multi-Phase):**
```sql
-- Phase 1: Add new column
ALTER TABLE users ADD COLUMN user_email VARCHAR(255);

-- Phase 2: Backfill data, deploy code writing to BOTH columns
UPDATE users SET user_email = email WHERE user_email IS NULL;

-- Phase 3: Make NOT NULL, deploy code reading from new column
-- ALTER TABLE users ALTER COLUMN user_email SET NOT NULL;

-- Phase 4: Drop old column, deploy code using only new column
-- ALTER TABLE users DROP COLUMN email;
```

### 4. Creating Indexes

**Unsafe (Blocks Writes):**
```sql
-- DON'T DO THIS in production
CREATE INDEX idx_users_email ON users(email);
-- Locks table during creation!
```

**Safe (PostgreSQL):**
```sql
-- Create concurrently (doesn't block writes)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

**Note:** `CONCURRENTLY` cannot run inside a transaction. MySQL/MariaDB use `ALGORITHM=INPLACE, LOCK=NONE`.

### 5. Adding Foreign Keys

**Safe Pattern:**
```sql
-- Phase 1: Add column (nullable)
ALTER TABLE posts ADD COLUMN author_id INTEGER;

-- Phase 2: Backfill data
UPDATE posts SET author_id = (SELECT id FROM users WHERE users.email = posts.author_email);

-- Phase 3: Create index (important for performance!)
CREATE INDEX CONCURRENTLY idx_posts_author_id ON posts(author_id);

-- Phase 4: Add constraint
ALTER TABLE posts
ADD CONSTRAINT fk_posts_author
FOREIGN KEY (author_id)
REFERENCES users(id)
ON DELETE CASCADE;

-- Phase 5: Make NOT NULL
-- ALTER TABLE posts ALTER COLUMN author_id SET NOT NULL;
```

### 6. Changing Column Type

**Unsafe:**
```sql
-- DON'T DO THIS
ALTER TABLE users ALTER COLUMN age TYPE BIGINT;
-- Rewrites entire table, locks for duration!
```

**Safe (Multi-Phase):**
```sql
-- Phase 1: Add new column with new type
ALTER TABLE users ADD COLUMN age_bigint BIGINT;

-- Phase 2: Backfill, deploy code writing to both
UPDATE users SET age_bigint = age WHERE age_bigint IS NULL;

-- Phase 3: Drop old column, deploy code using new column
-- ALTER TABLE users DROP COLUMN age;
-- ALTER TABLE users RENAME COLUMN age_bigint TO age;
```

## Migration Tools by Language

### Python (Alembic + SQLAlchemy)

```bash
# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Example Migration:**
```python
# alembic/versions/001_add_users.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
```

### TypeScript (Prisma Migrate)

```bash
# Create migration
npx prisma migrate dev --name add_users

# Apply to production
npx prisma migrate deploy

# Reset (development only!)
npx prisma migrate reset
```

### TypeScript (Drizzle Kit)

```bash
# Generate migration
npx drizzle-kit generate:pg

# Apply migration
npx drizzle-kit push:pg

# Or use custom migration runner
```

### Rust (SQLx)

```bash
# Create migration
sqlx migrate add add_users

# Run migrations
sqlx migrate run

# Revert
sqlx migrate revert
```

**Embed in Binary:**
```rust
sqlx::migrate!("./migrations")
    .run(&pool)
    .await?;
```

### Go (golang-migrate)

```bash
# Create migration
migrate create -ext sql -dir migrations -seq add_users

# Run migrations
migrate -path migrations -database "postgresql://..." up

# Rollback
migrate -path migrations -database "postgresql://..." down 1
```

## Best Practices

### 1. Test Migrations in Staging

```bash
# Copy production data to staging
pg_dump -h prod -d mydb | psql -h staging -d mydb_staging

# Run migration in staging
alembic upgrade head

# Test application against staging

# If successful, run in production
```

### 2. Measure Migration Duration

```bash
# Time migration
time alembic upgrade head

# For large tables (>1M rows), expect:
# - Adding column: Seconds
# - Creating index: Minutes to hours
# - Changing column type: Minutes to hours (table rewrite)
```

### 3. Concurrent Migrations

**PostgreSQL Specific:**

```sql
-- Create index without blocking writes
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- If it fails, drop and retry (can't retry CONCURRENTLY in transaction)
DROP INDEX CONCURRENTLY IF EXISTS idx_users_email;
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Add constraint without long lock (PostgreSQL 12+)
ALTER TABLE posts ADD CONSTRAINT fk_posts_author
FOREIGN KEY (author_id) REFERENCES users(id) NOT VALID;

-- Validate separately (acquires brief lock)
ALTER TABLE posts VALIDATE CONSTRAINT fk_posts_author;
```

### 4. Monitor During Migration

```sql
-- Check progress (PostgreSQL)
SELECT pid, now() - query_start AS duration, state, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Check locks
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query,
       blocking_activity.query AS current_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

### 5. Rollback Plan

Always have rollback:

```sql
-- Migration (up)
CREATE TABLE new_table (...);

-- Rollback (down)
DROP TABLE new_table;
```

Test rollback in staging:
```bash
alembic upgrade head  # Apply
alembic downgrade -1  # Rollback
alembic upgrade head  # Re-apply
```

## Common Pitfalls

### ❌ Don't Use Transactions for Long Operations

```sql
-- BAD - Locks for entire duration
BEGIN;
CREATE INDEX idx_users_email ON users(email);  -- Takes 10 minutes
COMMIT;

-- GOOD - No transaction, use CONCURRENTLY
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### ❌ Don't Assume Migration Speed

```python
# BAD - No timeout
def upgrade():
    op.execute("UPDATE large_table SET column = ...")  # Could take hours!

# GOOD - Add timeout or break into batches
def upgrade():
    conn = op.get_bind()
    conn.execute(text("SET statement_timeout = '10min'"))
    # Or batch updates:
    # UPDATE large_table SET column = ... WHERE id BETWEEN 1 AND 10000;
```

### ❌ Don't Mix Schema and Data Changes

```python
# BAD
def upgrade():
    op.create_table('users', ...)
    op.execute("INSERT INTO users VALUES (...)")  # Data migration

# GOOD - Separate migrations
# 001_create_users_table.py - Schema
# 002_populate_initial_users.py - Data
```

## Resources

- Alembic: https://alembic.sqlalchemy.org/
- Prisma Migrate: https://www.prisma.io/docs/concepts/components/prisma-migrate
- Drizzle Kit: https://orm.drizzle.team/kit-docs/overview
- SQLx Migrations: https://github.com/launchbadge/sqlx/tree/main/sqlx-cli
- golang-migrate: https://github.com/golang-migrate/migrate
