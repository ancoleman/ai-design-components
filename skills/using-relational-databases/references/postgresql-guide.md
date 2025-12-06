# PostgreSQL Guide

PostgreSQL is the recommended relational database for maximum flexibility and advanced features.


## Table of Contents

- [When to Choose PostgreSQL](#when-to-choose-postgresql)
- [Core Features](#core-features)
  - [Advanced Data Types](#advanced-data-types)
  - [Full-Text Search](#full-text-search)
  - [Transactions and Isolation Levels](#transactions-and-isolation-levels)
- [PostgreSQL Extensions](#postgresql-extensions)
  - [pgvector (Vector Search)](#pgvector-vector-search)
  - [PostGIS (Geospatial)](#postgis-geospatial)
  - [TimescaleDB (Time-Series)](#timescaledb-time-series)
- [Indexing Strategies](#indexing-strategies)
  - [Index Types](#index-types)
  - [Partial Indexes](#partial-indexes)
  - [Expression Indexes](#expression-indexes)
  - [Composite Indexes](#composite-indexes)
- [Performance Tuning](#performance-tuning)
  - [Query Analysis](#query-analysis)
  - [Connection Pooling](#connection-pooling)
  - [Vacuuming](#vacuuming)
- [Monitoring](#monitoring)
  - [Key Metrics](#key-metrics)
- [Best Practices](#best-practices)
  - [Schema Design](#schema-design)
  - [Security](#security)
  - [Backups](#backups)
- [Common Patterns](#common-patterns)
  - [Soft Deletes](#soft-deletes)
  - [Audit Logs](#audit-logs)
  - [UUID Primary Keys](#uuid-primary-keys)
- [Resources](#resources)

## When to Choose PostgreSQL

**Choose PostgreSQL when:**
- Need advanced data types (JSON, arrays, hstore, custom types)
- Require vector search (pgvector for embeddings)
- Working with geospatial data (PostGIS extension)
- Need time-series optimization (TimescaleDB extension)
- Want graph relationships (Apache AGE extension)
- Maximum standards compliance required (ACID, SQL standard)

**Skip PostgreSQL for:**
- Simple embedded applications (use SQLite)
- Legacy MySQL systems (migration complexity)
- Pure key-value workloads (use Redis)

## Core Features

### Advanced Data Types

**JSON and JSONB:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    profile JSONB  -- JSONB is faster than JSON for queries
);

-- Query JSONB fields
SELECT * FROM users WHERE profile->>'city' = 'San Francisco';
SELECT * FROM users WHERE profile @> '{"premium": true}';

-- Index JSONB for performance
CREATE INDEX idx_users_profile ON users USING GIN (profile);
```

**Arrays:**
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title TEXT,
    tags TEXT[]  -- Array of tags
);

-- Query arrays
SELECT * FROM posts WHERE 'postgresql' = ANY(tags);
SELECT * FROM posts WHERE tags @> ARRAY['postgresql', 'database'];

-- Index arrays
CREATE INDEX idx_posts_tags ON users USING GIN (tags);
```

**Enums:**
```sql
CREATE TYPE user_role AS ENUM ('admin', 'user', 'guest');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    role user_role DEFAULT 'user'
);
```

### Full-Text Search

**Create tsvector column:**
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    search_vector tsvector  -- Auto-updated via trigger
);

-- Create trigger to auto-update search_vector
CREATE FUNCTION articles_search_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.content, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_search_trigger
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW EXECUTE FUNCTION articles_search_update();

-- Create GIN index for fast search
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Search query
SELECT id, title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql & database') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

### Transactions and Isolation Levels

**Basic Transaction:**
```sql
BEGIN;
    INSERT INTO users (email, name) VALUES ('test@example.com', 'Test User');
    INSERT INTO profiles (user_id, bio) VALUES (currval('users_id_seq'), 'Bio text');
COMMIT;
-- Or ROLLBACK to undo changes
```

**Isolation Levels:**
```sql
-- Read Uncommitted (PostgreSQL treats as Read Committed)
BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- Read Committed (default, recommended for most use cases)
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Repeatable Read (consistent snapshot)
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Serializable (strictest, may cause serialization failures)
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

**Use Cases:**
- **Read Committed** (default): Most web applications
- **Repeatable Read**: Financial transactions, reports requiring consistency
- **Serializable**: Critical operations requiring absolute consistency

## PostgreSQL Extensions

### pgvector (Vector Search)

**Installation:**
```sql
CREATE EXTENSION vector;
```

**Usage:**
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)  -- OpenAI embedding dimension
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Insert embeddings
INSERT INTO documents (content, embedding)
VALUES ('Sample text', '[0.1, 0.2, ..., 0.5]');

-- Similarity search (cosine distance)
SELECT id, content, 1 - (embedding <=> '[0.1, 0.2, ..., 0.5]') AS similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ..., 0.5]'
LIMIT 10;
```

**Use Cases:**
- Semantic search
- RAG (Retrieval Augmented Generation)
- Recommendation engines
- Duplicate detection

### PostGIS (Geospatial)

**Installation:**
```sql
CREATE EXTENSION postgis;
```

**Usage:**
```sql
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location GEOGRAPHY(Point, 4326)  -- WGS 84 coordinate system
);

-- Create spatial index
CREATE INDEX idx_locations_location ON locations USING GIST (location);

-- Insert location (longitude, latitude)
INSERT INTO locations (name, location)
VALUES ('San Francisco', ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326));

-- Find locations within 10km
SELECT name, ST_Distance(location, ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326)) AS distance
FROM locations
WHERE ST_DWithin(location, ST_SetSRID(ST_MakePoint(-122.4194, 37.7749), 4326), 10000)
ORDER BY distance;
```

**Use Cases:**
- Location-based services
- Delivery routing
- Store locators
- Geographic analytics

### TimescaleDB (Time-Series)

**Installation:**
```sql
CREATE EXTENSION timescaledb;
```

**Usage:**
```sql
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id INTEGER,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);

-- Convert to hypertable (partitions by time)
SELECT create_hypertable('metrics', 'time');

-- Automatic compression for old data
ALTER TABLE metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'device_id'
);

-- Compression policy (compress data older than 7 days)
SELECT add_compression_policy('metrics', INTERVAL '7 days');

-- Continuous aggregates (materialized views that update automatically)
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS hour,
       device_id,
       AVG(temperature) AS avg_temp,
       MAX(temperature) AS max_temp
FROM metrics
GROUP BY hour, device_id;

-- Refresh policy
SELECT add_continuous_aggregate_policy('metrics_hourly',
    start_offset => INTERVAL '1 month',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
```

**Use Cases:**
- IoT sensor data
- Application metrics
- Financial tick data
- Server monitoring

## Indexing Strategies

### Index Types

**B-Tree (default, most common):**
```sql
CREATE INDEX idx_users_email ON users(email);  -- Exact matches, ranges
CREATE INDEX idx_users_created ON users(created_at DESC);  -- Sorted queries
```

**GIN (Generalized Inverted Index):**
```sql
CREATE INDEX idx_users_tags ON users USING GIN(tags);  -- Arrays
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);  -- Full-text
CREATE INDEX idx_users_profile ON users USING GIN(profile);  -- JSONB
```

**GiST (Generalized Search Tree):**
```sql
CREATE INDEX idx_locations_location ON locations USING GIST(location);  -- PostGIS
CREATE INDEX idx_ranges ON events USING GIST(time_range);  -- Range types
```

**BRIN (Block Range Index):**
```sql
CREATE INDEX idx_logs_timestamp ON logs USING BRIN(timestamp);  -- Time-series
-- Much smaller than B-Tree, ideal for naturally ordered data
```

**Hash:**
```sql
CREATE INDEX idx_users_uuid ON users USING HASH(uuid);  -- Equality only
-- Rarely used, B-Tree is usually better
```

### Partial Indexes

Index only relevant rows:
```sql
-- Only index active users
CREATE INDEX idx_active_users_email ON users(email) WHERE active = true;

-- Only index recent orders
CREATE INDEX idx_recent_orders ON orders(created_at)
WHERE created_at > NOW() - INTERVAL '90 days';
```

### Expression Indexes

Index computed values:
```sql
-- Case-insensitive search
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Query: SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
```

### Composite Indexes

**Index multiple columns:**
```sql
CREATE INDEX idx_users_name_email ON users(last_name, first_name, email);
```

**Order matters:**
- Index works for: `last_name`, `last_name + first_name`, `last_name + first_name + email`
- Index does NOT work for: `first_name`, `email`

**Rule of thumb:** Most selective column first, or match query WHERE order.

## Performance Tuning

### Query Analysis

**EXPLAIN:**
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- Shows query plan without executing
```

**EXPLAIN ANALYZE:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
-- Executes query and shows actual times
```

**Key metrics:**
- **Seq Scan**: Table scan (bad for large tables, add index)
- **Index Scan**: Using index (good)
- **Bitmap Index Scan**: Combining multiple indexes (good)
- **Cost**: Estimated cost (lower is better)
- **Actual Time**: Real execution time

### Connection Pooling

**Recommended configuration:**
```sql
-- postgresql.conf
max_connections = 100  -- Max total connections
shared_buffers = 256MB  -- RAM for caching (25% of RAM)
effective_cache_size = 1GB  -- Available OS cache (50-75% of RAM)
work_mem = 16MB  -- Per-operation memory
maintenance_work_mem = 128MB  -- For VACUUM, CREATE INDEX
```

**Application-side pooling:**
- Web API: 10-20 connections per instance
- Background worker: 5-10 connections
- Serverless: 1-2 connections + pgBouncer

### Vacuuming

PostgreSQL uses MVCC (Multi-Version Concurrency Control) which creates dead tuples on UPDATE/DELETE.

**Auto-vacuum (enabled by default):**
```sql
-- Check last vacuum
SELECT schemaname, relname, last_vacuum, last_autovacuum
FROM pg_stat_user_tables
WHERE schemaname = 'public';
```

**Manual vacuum:**
```sql
VACUUM;  -- Reclaim space, update statistics
VACUUM ANALYZE;  -- Also update planner statistics
VACUUM FULL;  -- Locks table, reclaims all space (rarely needed)
```

**Prevent bloat:**
```sql
-- postgresql.conf
autovacuum = on
autovacuum_vacuum_scale_factor = 0.1  -- Vacuum when 10% dead tuples
autovacuum_analyze_scale_factor = 0.05
```

## Monitoring

### Key Metrics

**Active connections:**
```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
```

**Long-running queries:**
```sql
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '5 minutes';
```

**Database size:**
```sql
SELECT pg_size_pretty(pg_database_size('mydb'));
```

**Table sizes:**
```sql
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**Cache hit ratio (should be >90%):**
```sql
SELECT
    sum(heap_blks_read) AS heap_read,
    sum(heap_blks_hit) AS heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS ratio
FROM pg_statio_user_tables;
```

## Best Practices

### Schema Design

**Use constraints:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);
```

**Use foreign keys:**
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL
);
```

**Use appropriate data types:**
- `SERIAL` or `BIGSERIAL` for auto-incrementing IDs
- `TIMESTAMPTZ` (not `TIMESTAMP`) for timestamps (stores timezone)
- `TEXT` for variable-length strings (no length limit)
- `VARCHAR(n)` only when length constraint required
- `JSONB` (not `JSON`) for JSON data (faster queries)

### Security

**Create application user with limited permissions:**
```sql
CREATE USER myapp_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO myapp_user;
GRANT USAGE ON SCHEMA public TO myapp_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO myapp_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO myapp_user;
```

**Enable SSL:**
```sql
-- postgresql.conf
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'
```

**Connection string with SSL:**
```
postgresql://user:pass@host:5432/db?sslmode=require
```

### Backups

**pg_dump (logical backup):**
```bash
pg_dump -U postgres -d mydb -F c -f mydb_backup.dump
# Restore: pg_restore -U postgres -d mydb mydb_backup.dump
```

**pg_basebackup (physical backup):**
```bash
pg_basebackup -U postgres -D /backup/mydb -F tar -z -P
```

**Continuous archiving (WAL archiving):**
```sql
-- postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/archive/%f'
```

**Point-in-time recovery (PITR):**
Restore base backup + replay WAL files to specific timestamp.

## Common Patterns

### Soft Deletes

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    deleted_at TIMESTAMPTZ  -- NULL = not deleted
);

-- Create partial index (only active users)
CREATE UNIQUE INDEX idx_users_email_active ON users(email)
WHERE deleted_at IS NULL;

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = 123;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Audit Logs

```sql
CREATE TABLE users_audit (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    operation VARCHAR(10),  -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by INTEGER,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE FUNCTION users_audit_trigger() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO users_audit (user_id, operation, old_data)
        VALUES (OLD.id, 'DELETE', row_to_json(OLD));
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO users_audit (user_id, operation, old_data, new_data)
        VALUES (NEW.id, 'UPDATE', row_to_json(OLD), row_to_json(NEW));
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO users_audit (user_id, operation, new_data)
        VALUES (NEW.id, 'INSERT', row_to_json(NEW));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION users_audit_trigger();
```

### UUID Primary Keys

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL
);
```

**Benefits:**
- Globally unique (no conflicts across databases)
- Secure (unpredictable)
- Distributed-friendly

**Drawbacks:**
- Larger storage (16 bytes vs 4 bytes for INTEGER)
- Slower index performance (random inserts)
- Less human-readable

**Recommendation:** Use UUID for distributed systems, SERIAL/BIGSERIAL for single-database apps.

## Resources

**Official Documentation:**
- PostgreSQL Docs: https://www.postgresql.org/docs/
- pgvector: https://github.com/pgvector/pgvector
- PostGIS: https://postgis.net/
- TimescaleDB: https://docs.timescale.com/

**Performance Tools:**
- PgHero: https://github.com/ankane/pghero (performance dashboard)
- pg_stat_statements: Built-in query statistics extension
- EXPLAIN visualizer: https://explain.dalibo.com/

**Community:**
- PostgreSQL Wiki: https://wiki.postgresql.org/
- Planet PostgreSQL: https://planet.postgresql.org/ (blog aggregator)
