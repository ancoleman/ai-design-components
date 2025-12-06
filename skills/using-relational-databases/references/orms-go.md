# Go Database Libraries


## Table of Contents

- [Overview](#overview)
- [sqlc (Recommended)](#sqlc-recommended)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Schema](#schema)
  - [Queries](#queries)
  - [Generate Code](#generate-code)
  - [Usage](#usage)
  - [Gin Integration](#gin-integration)
- [GORM (Rapid Development)](#gorm-rapid-development)
  - [Installation](#installation)
  - [Usage](#usage)
- [pgx (PostgreSQL Driver)](#pgx-postgresql-driver)
  - [Installation](#installation)
  - [Usage](#usage)
- [Comparison](#comparison)
  - [Choose sqlc When:](#choose-sqlc-when)
  - [Choose GORM When:](#choose-gorm-when)
  - [Choose pgx When:](#choose-pgx-when)
- [Best Practices](#best-practices)
  - [Connection Pooling](#connection-pooling)
  - [Error Handling](#error-handling)
  - [Migrations](#migrations)
- [Resources](#resources)

## Overview

| Library | Type | Code Gen | Type Safety | Learning Curve | Best For |
|---------|------|----------|-------------|----------------|----------|
| **sqlc** | Query Builder | ✅ From SQL | Excellent | Low | Type-safe, SQL-first |
| **GORM** | ORM | ❌ | Good (tags) | Low | Rapid development |
| **Ent** | ORM | ✅ From schema | Excellent | Medium | Graph queries |
| **pgx** | Driver | ❌ | Manual | Low | PostgreSQL performance |

## sqlc (Recommended)

**Key Feature:** Generates type-safe Go code from SQL queries.

### Installation

```bash
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
```

### Configuration

```yaml
# sqlc.yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "queries.sql"
    schema: "schema.sql"
    gen:
      go:
        package: "db"
        out: "db"
        emit_json_tags: true
        emit_prepared_queries: false
        emit_interface: false
        emit_exact_table_names: false
```

### Schema

```sql
-- schema.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    published BOOLEAN DEFAULT false,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Queries

```sql
-- queries.sql

-- name: GetUser :one
SELECT id, email, name, created_at FROM users WHERE id = $1;

-- name: GetUserByEmail :one
SELECT id, email, name, created_at FROM users WHERE email = $1;

-- name: ListUsers :many
SELECT id, email, name, created_at FROM users ORDER BY id;

-- name: CreateUser :one
INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id, email, name, created_at;

-- name: UpdateUser :exec
UPDATE users SET name = $1 WHERE id = $2;

-- name: DeleteUser :exec
DELETE FROM users WHERE id = $1;

-- name: ListUserPosts :many
SELECT p.id, p.title, p.content, p.published
FROM posts p
JOIN users u ON p.author_id = u.id
WHERE u.id = $1
ORDER BY p.created_at DESC;
```

### Generate Code

```bash
sqlc generate
```

### Usage

```go
package main

import (
    "context"
    "database/sql"
    "log"
    "yourproject/db"

    _ "github.com/lib/pq"
)

func main() {
    // Connect
    conn, err := sql.Open("postgres", "postgresql://user:pass@localhost/db")
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    // Connection pooling
    conn.SetMaxOpenConns(20)
    conn.SetMaxIdleConns(10)
    conn.SetConnMaxLifetime(time.Hour)

    // Create queries instance
    queries := db.New(conn)
    ctx := context.Background()

    // Create
    user, err := queries.CreateUser(ctx, db.CreateUserParams{
        Email: "test@example.com",
        Name:  "Test User",
    })
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Created user: %+v\n", user)

    // Read
    user, err = queries.GetUser(ctx, user.ID)
    if err != nil {
        log.Fatal(err)
    }

    users, err := queries.ListUsers(ctx)
    if err != nil {
        log.Fatal(err)
    }

    // Update
    err = queries.UpdateUser(ctx, db.UpdateUserParams{
        ID:   user.ID,
        Name: "Updated Name",
    })
    if err != nil {
        log.Fatal(err)
    }

    // Delete
    err = queries.DeleteUser(ctx, user.ID)
    if err != nil {
        log.Fatal(err)
    }

    // Transactions
    tx, err := conn.Begin()
    if err != nil {
        log.Fatal(err)
    }
    defer tx.Rollback()

    qtx := queries.WithTx(tx)
    _, err = qtx.CreateUser(ctx, db.CreateUserParams{
        Email: "user1@example.com",
        Name:  "User 1",
    })
    if err != nil {
        log.Fatal(err)
    }

    _, err = qtx.CreateUser(ctx, db.CreateUserParams{
        Email: "user2@example.com",
        Name:  "User 2",
    })
    if err != nil {
        log.Fatal(err)
    }

    if err = tx.Commit(); err != nil {
        log.Fatal(err)
    }
}
```

### Gin Integration

```go
package main

import (
    "database/sql"
    "net/http"
    "yourproject/db"

    "github.com/gin-gonic/gin"
    _ "github.com/lib/pq"
)

func main() {
    conn, _ := sql.Open("postgres", "postgresql://...")
    defer conn.Close()

    queries := db.New(conn)

    r := gin.Default()

    r.POST("/users", func(c *gin.Context) {
        var req struct {
            Email string `json:"email" binding:"required"`
            Name  string `json:"name" binding:"required"`
        }

        if err := c.ShouldBindJSON(&req); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        user, err := queries.CreateUser(c.Request.Context(), db.CreateUserParams{
            Email: req.Email,
            Name:  req.Name,
        })
        if err != nil {
            c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
            return
        }

        c.JSON(http.StatusCreated, user)
    })

    r.GET("/users/:id", func(c *gin.Context) {
        var uri struct {
            ID int32 `uri:"id" binding:"required"`
        }

        if err := c.ShouldBindUri(&uri); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        user, err := queries.GetUser(c.Request.Context(), uri.ID)
        if err != nil {
            c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
            return
        }

        c.JSON(http.StatusOK, user)
    })

    r.Run(":8080")
}
```

**Why sqlc?**
- Type-safe generated code
- SQL-first (full SQL control)
- Zero runtime overhead
- Easy to understand (just Go code)
- Excellent for PostgreSQL

## GORM (Rapid Development)

### Installation

```bash
go get -u gorm.io/gorm
go get -u gorm.io/driver/postgres
```

### Usage

```go
package main

import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
    "time"
)

type User struct {
    ID        uint      `gorm:"primaryKey" json:"id"`
    Email     string    `gorm:"uniqueIndex;not null" json:"email"`
    Name      string    `gorm:"not null" json:"name"`
    CreatedAt time.Time `json:"created_at"`
    Posts     []Post    `gorm:"foreignKey:AuthorID" json:"posts,omitempty"`
}

type Post struct {
    ID        uint      `gorm:"primaryKey" json:"id"`
    Title     string    `gorm:"not null" json:"title"`
    Content   string    `json:"content"`
    Published bool      `gorm:"default:false" json:"published"`
    AuthorID  uint      `gorm:"not null" json:"author_id"`
    CreatedAt time.Time `json:"created_at"`
}

func main() {
    dsn := "host=localhost user=user password=pass dbname=db port=5432 sslmode=disable"
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    if err != nil {
        panic(err)
    }

    // Auto-migrate (creates tables)
    db.AutoMigrate(&User{}, &Post{})

    // Create
    user := User{Email: "test@example.com", Name: "Test User"}
    db.Create(&user)

    // Read
    var foundUser User
    db.First(&foundUser, "email = ?", "test@example.com")

    var users []User
    db.Where("email LIKE ?", "%@example.com").Find(&users)

    // Update
    db.Model(&foundUser).Update("name", "Updated Name")

    // Delete
    db.Delete(&foundUser)

    // Preload relations
    var userWithPosts User
    db.Preload("Posts").First(&userWithPosts, user.ID)

    // Transactions
    db.Transaction(func(tx *gorm.DB) error {
        if err := tx.Create(&User{Email: "user1@example.com", Name: "User 1"}).Error; err != nil {
            return err
        }
        if err := tx.Create(&User{Email: "user2@example.com", Name: "User 2"}).Error; err != nil {
            return err
        }
        return nil
    })
}
```

**Why GORM?**
- Rapid development
- Active Record pattern
- Auto-migrations
- Association handling
- Large community

## pgx (PostgreSQL Driver)

High-performance PostgreSQL driver.

### Installation

```bash
go get github.com/jackc/pgx/v5
go get github.com/jackc/pgx/v5/pgxpool
```

### Usage

```go
package main

import (
    "context"
    "github.com/jackc/pgx/v5/pgxpool"
    "log"
)

type User struct {
    ID    int32
    Email string
    Name  string
}

func main() {
    ctx := context.Background()

    // Connection pool
    pool, err := pgxpool.New(ctx, "postgresql://user:pass@localhost/db")
    if err != nil {
        log.Fatal(err)
    }
    defer pool.Close()

    // Query
    var user User
    err = pool.QueryRow(ctx, "SELECT id, email, name FROM users WHERE id = $1", 1).
        Scan(&user.ID, &user.Email, &user.Name)

    // Insert
    err = pool.QueryRow(ctx,
        "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id",
        "test@example.com", "Test User").Scan(&user.ID)

    // Transaction
    tx, err := pool.Begin(ctx)
    if err != nil {
        log.Fatal(err)
    }
    defer tx.Rollback(ctx)

    _, err = tx.Exec(ctx, "INSERT INTO users (email, name) VALUES ($1, $2)", "user1@example.com", "User 1")
    if err != nil {
        log.Fatal(err)
    }

    err = tx.Commit(ctx)
}
```

**Why pgx?**
- Best PostgreSQL performance
- Low-level control
- Connection pooling built-in
- PostgreSQL-specific features

## Comparison

### Choose sqlc When:
- Want type safety from SQL
- Prefer SQL-first approach
- Need generated code
- PostgreSQL/MySQL/SQLite

### Choose GORM When:
- Rapid development
- Like Active Record
- Need auto-migrations
- Want associations

### Choose pgx When:
- PostgreSQL-only
- Maximum performance
- Low-level control
- Simple queries

## Best Practices

### Connection Pooling

```go
// database/sql
db.SetMaxOpenConns(20)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(time.Hour)
db.SetConnMaxIdleTime(time.Minute * 10)

// pgxpool
config, _ := pgxpool.ParseConfig("postgresql://...")
config.MaxConns = 20
config.MinConns = 5
config.MaxConnLifetime = time.Hour
config.MaxConnIdleTime = time.Minute * 10
pool, _ := pgxpool.NewWithConfig(context.Background(), config)
```

### Error Handling

```go
import "errors"

var (
    ErrNotFound      = errors.New("not found")
    ErrDuplicateEmail = errors.New("duplicate email")
)

func GetUser(ctx context.Context, queries *db.Queries, id int32) (db.User, error) {
    user, err := queries.GetUser(ctx, id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return db.User{}, ErrNotFound
        }
        return db.User{}, fmt.Errorf("get user: %w", err)
    }
    return user, nil
}
```

### Migrations

```bash
# Install golang-migrate
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# Create migration
migrate create -ext sql -dir migrations -seq add_users

# Run migrations
migrate -path migrations -database "postgresql://..." up
```

```sql
-- migrations/000001_add_users.up.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

-- migrations/000001_add_users.down.sql
DROP TABLE users;
```

## Resources

- sqlc: https://sqlc.dev/
- GORM: https://gorm.io/
- pgx: https://github.com/jackc/pgx
- golang-migrate: https://github.com/golang-migrate/migrate
