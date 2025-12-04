# Rust Axum Template

High-performance Rust backend template using Axum, SQLx, and PostgreSQL.

## Stack

- Axum (web framework)
- SQLx (compile-time checked queries)
- PostgreSQL (database)
- Tower (middleware)
- Tokio (async runtime)
- Serde (serialization)

## Project Structure

```
my-axum-app/
├── src/
│   ├── main.rs              # Entry point
│   ├── config.rs            # Configuration
│   ├── db.rs                # Database connection pool
│   ├── error.rs             # Error types
│   ├── models/              # Data models
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── routes/              # API routes
│   │   ├── mod.rs
│   │   ├── auth.rs
│   │   └── users.rs
│   ├── handlers/            # Route handlers
│   │   ├── mod.rs
│   │   └── user_handlers.rs
│   ├── services/            # Business logic
│   │   ├── mod.rs
│   │   └── user_service.rs
│   └── middleware/          # Custom middleware
│       ├── mod.rs
│       └── auth.rs
├── migrations/              # SQLx migrations
├── tests/
├── Cargo.toml
├── .env.example
└── README.md
```

## Quick Start

```bash
# 1. Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. Install sqlx-cli
cargo install sqlx-cli --no-default-features --features postgres

# 3. Configure environment
cp .env.example .env
# Edit .env with DATABASE_URL

# 4. Run migrations
sqlx database create
sqlx migrate run

# 5. Build and run
cargo run --release
```

Access API: http://localhost:3000

## Features

- Compile-time SQL query validation
- Automatic JSON serialization
- Tower middleware (CORS, logging, compression)
- Graceful shutdown
- Connection pooling
- Zero-cost abstractions

## Performance

- ~140,000 requests/second (hello world)
- <1ms p99 latency
- ~5MB memory footprint
- Compiles to native binary

## Use with Skill

This template is referenced by the `assembling-components` skill for rapidly scaffolding Rust backend applications.
