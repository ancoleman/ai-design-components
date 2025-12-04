# SQLite Implementation Guide

SQLite patterns, Turso edge deployment, and embedded database best practices.

## When to Choose SQLite

- **Embedded applications** - Mobile apps, desktop software, edge devices
- **Edge deployment** - Turso for global low-latency reads (<10ms)
- **Local-first apps** - Offline-capable PWAs, mobile apps
- **Prototyping** - Zero-config development databases
- **Small-medium datasets** - <100GB with proper indexing

**When PostgreSQL/MySQL is better:** Multi-user writes, complex transactions, >100GB data

## Installation

```bash
# Included with Python
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"

# TypeScript
npm install better-sqlite3

# Rust
cargo add rusqlite

# Go (built-in)
import "database/sql"
import _ "github.com/mattn/go-sqlite3"
```

## Basic Usage

### Python

```python
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
''')

# Insert
cursor.execute('INSERT INTO users (email, name) VALUES (?, ?)', ('user@example.com', 'John'))
conn.commit()

# Query
cursor.execute('SELECT * FROM users WHERE email = ?', ('user@example.com',))
user = cursor.fetchone()
```

### TypeScript (better-sqlite3)

```typescript
import Database from 'better-sqlite3';

const db = new Database('app.db');

// Create table
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
  )
`);

// Prepared statement (faster for multiple inserts)
const insert = db.prepare('INSERT INTO users (email, name) VALUES (?, ?)');
insert.run('user@example.com', 'John');

// Query
const user = db.prepare('SELECT * FROM users WHERE email = ?').get('user@example.com');
```

## Turso (Edge SQLite)

**libSQL (SQLite fork) deployed globally with <10ms reads.**

### Setup

```bash
# Install Turso CLI
curl -sSfL https://get.tur.so/install.sh | bash

# Create database
turso db create myapp

# Get connection URL
turso db show myapp --url
```

### TypeScript Integration

```typescript
import { createClient } from '@libsql/client';

const db = createClient({
  url: 'libsql://myapp-username.turso.io',
  authToken: process.env.TURSO_AUTH_TOKEN,
});

// Query
const result = await db.execute('SELECT * FROM users WHERE email = ?', ['user@example.com']);
console.log(result.rows);

// Transaction
await db.batch([
  { sql: 'INSERT INTO users (email, name) VALUES (?, ?)', args: ['a@example.com', 'Alice'] },
  { sql: 'INSERT INTO posts (user_id, title) VALUES (?, ?)', args: [1, 'Hello'] },
]);
```

### Drizzle ORM + Turso

```typescript
import { drizzle } from 'drizzle-orm/libsql';
import { createClient } from '@libsql/client';

const client = createClient({ url: process.env.TURSO_URL, authToken: process.env.TURSO_TOKEN });
const db = drizzle(client);

const users = await db.select().from(usersTable).where(eq(usersTable.email, 'user@example.com'));
```

## Performance Optimization

### Write-Ahead Logging (WAL)

```sql
-- Enable WAL mode (significantly faster writes)
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB cache
PRAGMA temp_store = MEMORY;
```

**Benefits:**
- Concurrent reads during writes
- Faster writes (3-5x)
- Better crash recovery

### Indexing

```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

-- Analyze query plan
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com';
```

### Connection Pooling (Not Needed)

SQLite uses file locking, not connection pooling. Use a single connection per application.

## Full-Text Search

```sql
-- Create FTS5 virtual table
CREATE VIRTUAL TABLE articles_fts USING fts5(title, content);

-- Insert data
INSERT INTO articles_fts (title, content) VALUES ('SQLite Guide', 'Full-text search in SQLite...');

-- Search
SELECT * FROM articles_fts WHERE articles_fts MATCH 'full-text' ORDER BY rank;
```

## Backup and Restore

```bash
# Backup
sqlite3 app.db ".backup backup.db"

# Or with CLI
sqlite3 app.db "VACUUM INTO 'backup.db'"

# Restore
cp backup.db app.db
```

## Multi-Database (Attach)

```sql
ATTACH DATABASE 'analytics.db' AS analytics;

SELECT u.name, COUNT(a.id) as events
FROM users u
JOIN analytics.events a ON u.id = a.user_id
GROUP BY u.id;

DETACH DATABASE analytics;
```

## Concurrency

**SQLite concurrency model:**
- Multiple readers OR one writer
- WAL mode allows concurrent reads during writes
- IMMEDIATE transaction for write intent

```python
# Proper transaction handling
conn.execute('BEGIN IMMEDIATE')
try:
    conn.execute('UPDATE users SET name = ? WHERE id = ?', ('Alice', 1))
    conn.execute('INSERT INTO audit_log (action) VALUES (?)', ('update_user',))
    conn.commit()
except Exception as e:
    conn.rollback()
    raise
```

## Turso Embedded Replicas

**Local-first with cloud sync:**
```typescript
import { createClient } from '@libsql/client';

const db = createClient({
  url: 'file:local.db',  // Local SQLite file
  syncUrl: 'libsql://myapp.turso.io',  // Turso cloud
  authToken: process.env.TURSO_TOKEN,
});

// Sync to cloud
await db.sync();
```

## Best Practices

1. **Enable WAL mode** for better write performance
2. **Use prepared statements** to prevent SQL injection
3. **Single connection per app** (no pooling needed)
4. **Index foreign keys** manually
5. **Use INTEGER PRIMARY KEY** for auto-increment (alias for rowid)
6. **VACUUM regularly** to reclaim space
7. **Analyze after bulk inserts** to update query planner stats
8. **Use transactions** for multiple writes
9. **Limit database size** to <100GB for optimal performance
10. **Consider Turso** for edge deployment with replication

## Common Pitfalls

**INTEGER vs INT:**
```sql
-- ✅ INTEGER PRIMARY KEY (alias for rowid, auto-increment)
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);

-- ❌ INT PRIMARY KEY (not alias for rowid, manual management)
CREATE TABLE users (id INT PRIMARY KEY, name TEXT);
```

**Type affinity (not strict types):**
```sql
-- SQLite allows any value in any column (dynamic typing)
INSERT INTO users (id, name) VALUES ('abc', 123);  -- Valid but wrong!

-- Use CHECK constraints for validation
CREATE TABLE users (
  id INTEGER PRIMARY KEY CHECK(typeof(id) = 'integer'),
  name TEXT CHECK(typeof(name) = 'text')
);
```

## Migration to PostgreSQL/MySQL

**Use pgLoader or custom scripts:**
```bash
# Export SQLite to CSV
sqlite3 app.db ".mode csv" ".once users.csv" "SELECT * FROM users"

# Import to PostgreSQL
psql -d mydb -c "\COPY users FROM 'users.csv' CSV HEADER"
```

## Resources

- SQLite Docs: https://www.sqlite.org/docs.html
- Turso Docs: https://docs.turso.tech/
- better-sqlite3: https://github.com/WiseLibs/better-sqlite3
- libSQL: https://github.com/tursodatabase/libsql
