# Rust Database Libraries

## Overview

| Library | Type | Compile-Time | Runtime | Learning Curve | Best For |
|---------|------|--------------|---------|----------------|----------|
| **SQLx 0.8** | Query Builder | ✅ Queries | Async (Tokio) | Medium | Type safety, performance |
| **SeaORM 1.x** | ORM | ✅ Schema | Async (Tokio) | Medium | ORM features, relations |
| **Diesel 2.3** | ORM | ✅ Schema | Sync/Async | High | Mature, stable, compile-time guarantees |

## SQLx (Recommended)

**Key Feature:** Compile-time query validation - queries are checked against your database schema at build time.

### Installation

```toml
# Cargo.toml
[dependencies]
sqlx = { version = "0.8", features = ["postgres", "runtime-tokio", "tls-native-tls"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }

[build-dependencies]
sqlx = { version = "0.8", features = ["postgres"] }
```

### Setup

```bash
# Set DATABASE_URL for compile-time checking
export DATABASE_URL="postgresql://user:pass@localhost/db"

# Install SQLx CLI
cargo install sqlx-cli

# Create database and run migrations
sqlx database create
sqlx migrate add initial_schema
sqlx migrate run
```

### Migrations

```sql
-- migrations/20231201000000_initial_schema.sql
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

### Usage

```rust
use sqlx::postgres::PgPoolOptions;
use sqlx::{FromRow, PgPool};
use serde::{Deserialize, Serialize};

#[derive(Debug, FromRow, Serialize, Deserialize)]
struct User {
    id: i32,
    email: String,
    name: String,
}

#[derive(Debug, FromRow, Serialize, Deserialize)]
struct Post {
    id: i32,
    title: String,
    content: Option<String>,
    published: bool,
    author_id: i32,
}

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    // Create connection pool
    let pool = PgPoolOptions::new()
        .max_connections(20)
        .min_connections(5)
        .acquire_timeout(std::time::Duration::from_secs(30))
        .connect(&std::env::var("DATABASE_URL").unwrap())
        .await?;

    // Create
    let user = sqlx::query_as::<_, User>(
        "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id, email, name"
    )
    .bind("test@example.com")
    .bind("Test User")
    .fetch_one(&pool)
    .await?;

    println!("Created user: {:?}", user);

    // Read - compile-time checked query!
    let users = sqlx::query_as::<_, User>(
        "SELECT id, email, name FROM users WHERE email LIKE $1"
    )
    .bind("%@example.com")
    .fetch_all(&pool)
    .await?;

    // Update
    sqlx::query("UPDATE users SET name = $1 WHERE id = $2")
        .bind("Updated Name")
        .bind(user.id)
        .execute(&pool)
        .await?;

    // Delete
    sqlx::query("DELETE FROM users WHERE id = $1")
        .bind(user.id)
        .execute(&pool)
        .await?;

    // Transaction
    let mut tx = pool.begin().await?;
    sqlx::query("INSERT INTO users (email, name) VALUES ($1, $2)")
        .bind("user1@example.com")
        .bind("User 1")
        .execute(&mut *tx)
        .await?;
    sqlx::query("INSERT INTO users (email, name) VALUES ($1, $2)")
        .bind("user2@example.com")
        .bind("User 2")
        .execute(&mut *tx)
        .await?;
    tx.commit().await?;

    Ok(())
}
```

### Compile-Time Checked Macros

```rust
// sqlx::query! macro - fully type-checked at compile time
let user = sqlx::query!(
    "SELECT id, email, name FROM users WHERE id = $1",
    user_id
)
.fetch_one(&pool)
.await?;

// Returns anonymous struct with fields:
// user.id: i32
// user.email: String
// user.name: String

// sqlx::query_as! - checked + custom struct
let user = sqlx::query_as!(
    User,
    "SELECT id, email, name FROM users WHERE email = $1",
    "test@example.com"
)
.fetch_one(&pool)
.await?;
```

### Axum Integration

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    routing::{get, post},
    Json, Router,
};
use serde_json::json;
use sqlx::PgPool;

#[tokio::main]
async fn main() {
    let pool = PgPoolOptions::new()
        .max_connections(20)
        .connect(&std::env::var("DATABASE_URL").unwrap())
        .await
        .unwrap();

    let app = Router::new()
        .route("/users", post(create_user))
        .route("/users/:id", get(get_user))
        .with_state(pool);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn create_user(
    State(pool): State<PgPool>,
    Json(payload): Json<CreateUserPayload>,
) -> Result<Json<User>, StatusCode> {
    let user = sqlx::query_as::<_, User>(
        "INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id, email, name"
    )
    .bind(&payload.email)
    .bind(&payload.name)
    .fetch_one(&pool)
    .await
    .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok(Json(user))
}

async fn get_user(
    State(pool): State<PgPool>,
    Path(id): Path<i32>,
) -> Result<Json<User>, StatusCode> {
    let user = sqlx::query_as::<_, User>(
        "SELECT id, email, name FROM users WHERE id = $1"
    )
    .bind(id)
    .fetch_one(&pool)
    .await
    .map_err(|_| StatusCode::NOT_FOUND)?;

    Ok(Json(user))
}

#[derive(Deserialize)]
struct CreateUserPayload {
    email: String,
    name: String,
}
```

**Why SQLx?**
- Compile-time query validation (catch errors before runtime!)
- Zero cost abstractions
- Async-first with Tokio
- PostgreSQL, MySQL, SQLite support
- Excellent performance

## SeaORM (Full ORM)

### Installation

```toml
[dependencies]
sea-orm = { version = "1", features = ["sqlx-postgres", "runtime-tokio-native-tls", "macros"] }
tokio = { version = "1", features = ["full"] }
```

### Entity Definition

```rust
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub email: String,
    pub name: String,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::post::Entity")]
    Post,
}

impl Related<super::post::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Post.def()
    }
}

impl ActiveModelBehavior for ActiveModel {}
```

### Usage

```rust
use sea_orm::*;

#[tokio::main]
async fn main() -> Result<(), DbErr> {
    let db = Database::connect("postgresql://user:pass@localhost/db").await?;

    // Create
    let user = users::ActiveModel {
        email: Set("test@example.com".to_owned()),
        name: Set("Test User".to_owned()),
        ..Default::default()
    };
    let insert_result = user.insert(&db).await?;

    // Read
    let user = Users::find_by_id(1).one(&db).await?;

    let users = Users::find()
        .filter(users::Column::Email.contains("@example.com"))
        .order_by_asc(users::Column::Name)
        .all(&db)
        .await?;

    // Update
    let mut user: users::ActiveModel = user.unwrap().into();
    user.name = Set("Updated Name".to_owned());
    user.update(&db).await?;

    // Delete
    user.delete(&db).await?;

    // Relations
    let users_with_posts = Users::find()
        .find_with_related(Posts)
        .all(&db)
        .await?;

    Ok(())
}
```

**Why SeaORM?**
- Full ORM features (relations, migrations, CLI)
- Active Record + Data Mapper patterns
- Async-first
- Good documentation

## Diesel (Mature, Stable)

### Installation

```toml
[dependencies]
diesel = { version = "2.3", features = ["postgres", "r2d2"] }
diesel-async = { version = "0.5", features = ["postgres", "tokio"] }
dotenvy = "0.15"
```

### Schema Definition

```rust
// src/schema.rs (generated by Diesel CLI)
diesel::table! {
    users (id) {
        id -> Int4,
        email -> Varchar,
        name -> Varchar,
    }
}

diesel::table! {
    posts (id) {
        id -> Int4,
        title -> Text,
        content -> Nullable<Text>,
        published -> Bool,
        author_id -> Int4,
    }
}

diesel::joinable!(posts -> users (author_id));
diesel::allow_tables_to_appear_in_same_query!(users, posts);
```

### Usage

```rust
use diesel::prelude::*;
use diesel::r2d2::{self, ConnectionManager};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Queryable, Selectable)]
#[diesel(table_name = users)]
struct User {
    id: i32,
    email: String,
    name: String,
}

#[derive(Insertable)]
#[diesel(table_name = users)]
struct NewUser {
    email: String,
    name: String,
}

fn main() {
    let database_url = std::env::var("DATABASE_URL").unwrap();
    let manager = ConnectionManager::<PgConnection>::new(database_url);
    let pool = r2d2::Pool::builder().build(manager).unwrap();

    let mut conn = pool.get().unwrap();

    // Create
    let new_user = NewUser {
        email: "test@example.com".to_string(),
        name: "Test User".to_string(),
    };
    diesel::insert_into(users::table)
        .values(&new_user)
        .execute(&mut conn)
        .unwrap();

    // Read
    let results = users::table
        .filter(users::email.like("%@example.com"))
        .select(User::as_select())
        .load(&mut conn)
        .unwrap();

    // Update
    diesel::update(users::table.find(1))
        .set(users::name.eq("Updated Name"))
        .execute(&mut conn)
        .unwrap();

    // Delete
    diesel::delete(users::table.find(1))
        .execute(&mut conn)
        .unwrap();
}
```

**Why Diesel?**
- Mature and stable (oldest Rust ORM)
- Compile-time guarantees
- Excellent performance
- CLI for schema management

## Comparison

### Choose SQLx When:
- Want compile-time query validation
- Prefer writing SQL directly
- Need maximum performance
- Want minimal abstraction

### Choose SeaORM When:
- Need full ORM features
- Want entity relations
- Prefer Active Record pattern
- Need migrations + CLI tools

### Choose Diesel When:
- Need maximum stability
- Want compile-time type safety
- Prefer Data Mapper pattern
- Have complex schema

## Best Practices

### Connection Pooling

```rust
// SQLx
let pool = PgPoolOptions::new()
    .max_connections(20)
    .min_connections(5)
    .acquire_timeout(Duration::from_secs(30))
    .idle_timeout(Some(Duration::from_secs(600)))
    .max_lifetime(Some(Duration::from_secs(3600)))
    .connect(&database_url)
    .await?;

// Diesel
let manager = ConnectionManager::<PgConnection>::new(database_url);
let pool = r2d2::Pool::builder()
    .max_size(20)
    .connection_timeout(Duration::from_secs(30))
    .build(manager)?;
```

### Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DatabaseError {
    #[error("Database error: {0}")]
    Sqlx(#[from] sqlx::Error),

    #[error("User not found")]
    NotFound,

    #[error("Duplicate email")]
    DuplicateEmail,
}

async fn get_user(pool: &PgPool, id: i32) -> Result<User, DatabaseError> {
    sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(id)
        .fetch_one(pool)
        .await
        .map_err(|e| match e {
            sqlx::Error::RowNotFound => DatabaseError::NotFound,
            e => DatabaseError::Sqlx(e),
        })
}
```

### Transactions

```rust
// SQLx
let mut tx = pool.begin().await?;
sqlx::query("INSERT INTO users (email, name) VALUES ($1, $2)")
    .bind("user1@example.com")
    .bind("User 1")
    .execute(&mut *tx)
    .await?;
sqlx::query("INSERT INTO users (email, name) VALUES ($1, $2)")
    .bind("user2@example.com")
    .bind("User 2")
    .execute(&mut *tx)
    .await?;
tx.commit().await?;

// SeaORM
let txn = db.begin().await?;
users::Entity::insert(user1).exec(&txn).await?;
users::Entity::insert(user2).exec(&txn).await?;
txn.commit().await?;
```

## Resources

- SQLx: https://github.com/launchbadge/sqlx
- SeaORM: https://www.sea-ql.org/SeaORM/
- Diesel: https://diesel.rs/
