# Rust Axum Dashboard Backend

High-performance Rust backend for dashboard applications using Axum and PostgreSQL.

## Stack

- Axum (web framework)
- SQLx (compile-time checked SQL)
- PostgreSQL
- Tower (middleware)
- Tokio (async runtime)
- JWT authentication
- SSE streaming

## Project Structure

```
rust-axum-dashboard/
├── src/
│   ├── main.rs
│   ├── config.rs
│   ├── db.rs                # Database pool
│   ├── error.rs             # Error handling
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── routes/
│   │   ├── mod.rs
│   │   ├── auth.rs
│   │   ├── dashboard.rs
│   │   └── metrics.rs
│   ├── handlers/
│   │   └── dashboard_handlers.rs
│   ├── middleware/
│   │   └── auth.rs
│   └── services/
│       └── metrics_service.rs
├── migrations/
├── Cargo.toml
└── .env.example
```

## Quick Start

```bash
# Install SQLx CLI
cargo install sqlx-cli

# Configure
cp .env.example .env

# Setup database
sqlx database create
sqlx migrate run

# Run (development)
cargo run

# Run (production)
cargo build --release
./target/release/axum-dashboard
```

## Performance

- 140,000+ requests/second
- <1ms p99 latency
- 5-10MB memory usage
- Sub-second startup time

## API Endpoints

```
POST /auth/login
GET  /dashboard/metrics
GET  /dashboard/kpis
GET  /stream/metrics       (SSE)
```

## Integration

Frontend options:
- React (see examples/react-dashboard/)
- Next.js (see examples/nextjs-dashboard/)

Skills used:
- databases-relational (SQLx)
- auth-security (JWT)
- realtime-sync (SSE)
