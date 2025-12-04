# MySQL Implementation Guide

MySQL-specific patterns, PlanetScale integration, and best practices for production deployments.

## When to Choose MySQL

- **Legacy system compatibility** - Existing MySQL infrastructure
- **PlanetScale serverless** - Non-blocking schema changes, branch-based workflows
- **WordPress/PHP ecosystems** - Native integration
- **Read replicas** - Built-in replication

**When PostgreSQL is better:** JSON operations, advanced indexing (GiST, GIN), extensions (PostGIS, pgvector)

## Installation

```bash
# Docker
docker run --name mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.2

# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# macOS (Homebrew)
brew install mysql
brew services start mysql
```

## Connection Configuration

### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "mysql+pymysql://user:password@localhost:3306/dbname?charset=utf8mb4",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections every hour
    echo=False,
)
```

### TypeScript (Prisma)

```prisma
// schema.prisma
datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
  relationMode = "prisma"  // For PlanetScale (no foreign keys)
}

// .env
DATABASE_URL="mysql://user:password@localhost:3306/dbname"
```

### Go (database/sql)

```go
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)

dsn := "user:password@tcp(localhost:3306)/dbname?parseTime=true&charset=utf8mb4"
db, err := sql.Open("mysql", dsn)
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(time.Hour)
```

## Schema Design Differences

### JSON Support

**MySQL 8.0+:**
```sql
CREATE TABLE products (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  attributes JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query JSON
SELECT * FROM products WHERE JSON_EXTRACT(attributes, '$.color') = 'red';

-- Index JSON path
ALTER TABLE products ADD COLUMN color VARCHAR(50)
  GENERATED ALWAYS AS (JSON_UNQUOTE(JSON_EXTRACT(attributes, '$.color'))) STORED;
CREATE INDEX idx_color ON products(color);
```

### Auto-Increment Primary Keys

**MySQL default (vs PostgreSQL SERIAL):**
```sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### UUID Primary Keys

```sql
-- MySQL 8.0+ has UUID() function
CREATE TABLE sessions (
  id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
  user_id BIGINT NOT NULL,
  expires_at TIMESTAMP NOT NULL
);

-- Query with UUID
SELECT * FROM sessions WHERE id = UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000');
```

## PlanetScale Integration

### Non-Blocking Schema Changes

**PlanetScale's killer feature:** Schema changes don't lock tables.

**Deploy request workflow:**
```bash
# 1. Create development branch
pscale branch create mydb dev-feature

# 2. Make schema changes
pscale shell mydb dev-feature
mysql> ALTER TABLE users ADD COLUMN phone VARCHAR(20);

# 3. Create deploy request
pscale deploy-request create mydb dev-feature

# 4. Review and deploy (zero downtime)
pscale deploy-request deploy mydb 1

# 5. Merge to main
# PlanetScale automatically merges after successful deploy
```

### Prisma + PlanetScale Setup

```prisma
// schema.prisma
datasource db {
  provider     = "mysql"
  url          = env("DATABASE_URL")
  relationMode = "prisma"  // Required for PlanetScale (no FK constraints)
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  posts     Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  userId   Int
  title    String
  user     User   @relation(fields: [userId], references: [id])

  @@index([userId])  // Manual index (no FK constraint)
}
```

**Connection string:**
```bash
# PlanetScale connection (from dashboard)
DATABASE_URL="mysql://username:password@aws.connect.psdb.cloud/dbname?ssl={"rejectUnauthorized":true}"
```

### Database Branching

```bash
# Create branch from main
pscale branch create mydb feature-xyz --from main

# Connect to branch
pscale connect mydb feature-xyz --port 3309

# Run migrations on branch
npm run prisma migrate dev

# Deploy to main via deploy request
pscale deploy-request create mydb feature-xyz
```

## Full-Text Search

```sql
CREATE TABLE articles (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  FULLTEXT(title, content)
);

-- Full-text search
SELECT * FROM articles
WHERE MATCH(title, content) AGAINST('database optimization' IN NATURAL LANGUAGE MODE);

-- Boolean mode (AND, OR, NOT)
SELECT * FROM articles
WHERE MATCH(title, content) AGAINST('+MySQL -PostgreSQL' IN BOOLEAN MODE);
```

## Replication Setup

### Primary-Replica Replication

**Primary server (my.cnf):**
```ini
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_do_db = mydb
```

**Replica server (my.cnf):**
```ini
[mysqld]
server-id = 2
relay-log = /var/log/mysql/mysql-relay-bin
log_bin = /var/log/mysql/mysql-bin.log
read_only = 1
```

**Configure replication:**
```sql
-- On primary
CREATE USER 'replicator'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
SHOW MASTER STATUS;  -- Note File and Position

-- On replica
CHANGE MASTER TO
  MASTER_HOST='primary-host',
  MASTER_USER='replicator',
  MASTER_PASSWORD='password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=107;

START SLAVE;
SHOW SLAVE STATUS\G
```

## Performance Optimization

### Index Strategy

**Composite index order matters:**
```sql
-- Query: WHERE user_id = ? AND created_at > ? ORDER BY created_at DESC
CREATE INDEX idx_user_created ON posts(user_id, created_at DESC);

-- Query: WHERE status = ? AND priority = ? ORDER BY created_at DESC
CREATE INDEX idx_status_priority_created ON tasks(status, priority, created_at DESC);
```

**Covering indexes:**
```sql
-- Query: SELECT id, title, created_at FROM posts WHERE user_id = ?
CREATE INDEX idx_user_id_covering ON posts(user_id, id, title, created_at);
```

### Query Optimization

**Use EXPLAIN to analyze queries:**
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

EXPLAIN FORMAT=JSON SELECT u.*, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;
```

### Connection Pooling

**Optimal pool sizes:**
```python
# Formula: (core_count * 2) + effective_spindle_count
# For 4 cores + SSD: (4 * 2) + 1 = 9 ≈ 10

engine = create_engine(
    "mysql+pymysql://...",
    pool_size=10,
    max_overflow=20,
)
```

## MySQL vs PostgreSQL Syntax Differences

| Feature | MySQL | PostgreSQL |
|---------|-------|------------|
| **Auto-increment** | `AUTO_INCREMENT` | `SERIAL` or `GENERATED ALWAYS AS IDENTITY` |
| **String concat** | `CONCAT(a, b)` | `a || b` or `CONCAT(a, b)` |
| **Limit/Offset** | `LIMIT 10 OFFSET 20` | `LIMIT 10 OFFSET 20` (same) |
| **Date functions** | `NOW()`, `CURDATE()` | `NOW()`, `CURRENT_DATE` |
| **JSON extract** | `JSON_EXTRACT(col, '$.key')` | `col->>'key'` or `col->'key'` |
| **Case-sensitivity** | Case-insensitive by default | Case-sensitive by default |
| **Boolean** | `TINYINT(1)` (0/1) | `BOOLEAN` (true/false) |

## Backup and Restore

### Logical Backup (mysqldump)

```bash
# Full database backup
mysqldump -u root -p --single-transaction --routines --triggers mydb > backup.sql

# Restore
mysql -u root -p mydb < backup.sql

# Compressed backup
mysqldump -u root -p mydb | gzip > backup.sql.gz

# Restore from compressed
gunzip < backup.sql.gz | mysql -u root -p mydb
```

### Point-in-Time Recovery

```bash
# Enable binary logging (my.cnf)
[mysqld]
log_bin = /var/log/mysql/mysql-bin.log
binlog_format = ROW
expire_logs_days = 7

# Restore to specific point in time
mysqlbinlog --stop-datetime="2025-12-03 10:30:00" mysql-bin.000001 | mysql -u root -p mydb
```

## Migration from MySQL to PostgreSQL

**Use pgLoader for automated migration:**
```bash
pgloader mysql://user:pass@localhost/mydb postgresql://user:pass@localhost/mydb

# Custom migration script
pgloader mysql.load

# mysql.load
LOAD DATABASE
  FROM mysql://root@localhost/mydb
  INTO postgresql://user@localhost/mydb
  WITH include drop, create tables, create indexes
  SET maintenance_work_mem to '512MB',
      work_mem to '128MB';
```

## Serverless: PlanetScale vs Neon (PostgreSQL)

| Feature | PlanetScale (MySQL) | Neon (PostgreSQL) |
|---------|---------------------|-------------------|
| **Branching** | ✓✓✓ (Non-blocking deploys) | ✓✓ (Git-like workflow) |
| **Autoscaling** | ✓ (Connection pooling) | ✓✓ (Compute autoscaling) |
| **Scale-to-zero** | ✗ | ✓✓✓ |
| **Foreign Keys** | ✗ (Application-level) | ✓✓✓ (Database-level) |
| **JSON Queries** | ✓ (Limited) | ✓✓✓ (JSONB optimized) |
| **Read replicas** | ✓✓ (Built-in) | ✓ (Manual setup) |
| **Pricing** | $29/month (Scaler plan) | $19/month (Launch plan) |

**Choose PlanetScale if:**
- Non-blocking schema changes are critical
- MySQL ecosystem required
- Read replicas needed

**Choose Neon if:**
- Need PostgreSQL features (JSONB, arrays, extensions)
- Want scale-to-zero compute
- Database branching for preview environments

## Best Practices

1. **Use utf8mb4** (not utf8) for full Unicode support
2. **Enable strict SQL mode** - Prevents silent data truncation
3. **Use InnoDB engine** (default in MySQL 8.0+)
4. **Index foreign keys** manually (especially with PlanetScale)
5. **Use prepared statements** to prevent SQL injection
6. **Monitor slow query log** regularly
7. **Set appropriate connection pool sizes** (10-20 for web APIs)
8. **Use `SELECT * FROM` sparingly** (specify columns)
9. **Avoid `OR` in WHERE clauses** (use `UNION` instead)
10. **Backup before schema changes** (even with PlanetScale)

## Common Pitfalls

**Implicit type conversion:**
```sql
-- ❌ Slow (varchar column, int comparison)
SELECT * FROM users WHERE id = 123;  -- id is VARCHAR

-- ✅ Fast (proper type)
SELECT * FROM users WHERE id = '123';
```

**N+1 queries:**
```python
# ❌ N+1 problem
users = db.query(User).all()
for user in users:
    posts = db.query(Post).filter(Post.user_id == user.id).all()  # N queries

# ✅ Eager loading
users = db.query(User).options(joinedload(User.posts)).all()  # 1 query
```

## Resources

- MySQL Docs: https://dev.mysql.com/doc/
- PlanetScale Docs: https://planetscale.com/docs
- MySQL Performance Blog: https://www.percona.com/blog/
