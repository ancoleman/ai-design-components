# Rust Axum Template

> Complete scaffolding template for high-performance web applications using Axum with tower middleware.

## Project Structure

```
project-name/
├── Cargo.toml                 # Dependencies and metadata
├── Cargo.lock
├── .env                       # Environment variables
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── main.rs                # Application entry point
│   ├── lib.rs                 # Library crate (optional)
│   ├── config.rs              # Configuration
│   ├── error.rs               # Error handling
│   ├── routes/                # HTTP routes
│   │   ├── mod.rs
│   │   ├── dashboard.rs
│   │   └── health.rs
│   ├── handlers/              # Request handlers
│   │   ├── mod.rs
│   │   └── dashboard_handler.rs
│   ├── models/                # Data structures
│   │   ├── mod.rs
│   │   └── dashboard.rs
│   ├── services/              # Business logic
│   │   ├── mod.rs
│   │   └── dashboard_service.rs
│   └── middleware/            # Custom middleware
│       └── mod.rs
├── static/                    # Static assets
│   ├── css/
│   │   └── tokens.css
│   └── js/
├── templates/                 # Tera templates
│   ├── base.html
│   └── dashboard.html
└── tests/
    └── integration_tests.rs
```

## Core Files

### Cargo.toml

```toml
[package]
name = "{{PROJECT_NAME}}"
version = "1.0.0"
edition = "2021"
authors = ["{{AUTHOR}}"]
description = "{{PROJECT_DESCRIPTION}}"

[dependencies]
# Web framework
axum = "0.7"
tokio = { version = "1.35", features = ["full"] }
tower = "0.4"
tower-http = { version = "0.5", features = ["fs", "trace", "cors"] }

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Configuration
dotenvy = "0.15"
config = "0.14"

# Templating
tera = "1.19"

# Tracing
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

# Error handling
thiserror = "1.0"
anyhow = "1.0"

[dev-dependencies]
axum-test = "14.0"
```

### src/main.rs

```rust
//! Application entry point.

mod config;
mod error;
mod handlers;
mod models;
mod routes;
mod services;

use axum::Router;
use std::net::SocketAddr;
use tower_http::services::ServeDir;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use crate::config::Config;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::try_from_default_env()
            .unwrap_or_else(|_| "info".into()))
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Load configuration
    let config = Config::from_env()?;
    tracing::info!("Starting {} v{}", config.app_name, config.version);

    // Build application
    let app = Router::new()
        .merge(routes::create_router())
        .nest_service("/static", ServeDir::new("static"))
        .layer(TraceLayer::new_for_http());

    // Run server
    let addr = SocketAddr::from(([0, 0, 0, 0], config.port));
    tracing::info!("Listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
```

### src/config.rs

```rust
//! Application configuration.

use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Config {
    #[serde(default = "default_app_name")]
    pub app_name: String,

    #[serde(default = "default_version")]
    pub version: String,

    #[serde(default = "default_port")]
    pub port: u16,

    #[serde(default)]
    pub debug: bool,
}

fn default_app_name() -> String {
    "{{PROJECT_NAME}}".into()
}

fn default_version() -> String {
    "1.0.0".into()
}

fn default_port() -> u16 {
    3000
}

impl Config {
    pub fn from_env() -> anyhow::Result<Self> {
        dotenvy::dotenv().ok();

        let config = config::Config::builder()
            .add_source(config::Environment::default())
            .build()?;

        Ok(config.try_deserialize()?)
    }
}
```

### src/error.rs

```rust
//! Application error types.

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Bad request: {0}")]
    BadRequest(String),

    #[error("Internal server error")]
    InternalError(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg.clone()),
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            AppError::InternalError(_) => {
                tracing::error!("Internal error: {:?}", self);
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error".into())
            }
        };

        let body = Json(json!({
            "error": message,
            "status": status.as_u16(),
        }));

        (status, body).into_response()
    }
}
```

### src/routes/mod.rs

```rust
//! Route definitions.

pub mod dashboard;
pub mod health;

use axum::{routing::get, Router};

pub fn create_router() -> Router {
    Router::new()
        .route("/api/health", get(health::health_check))
        .route("/api/dashboard", get(dashboard::get_dashboard))
        .route("/api/dashboard/data", get(dashboard::get_dashboard_data))
}
```

### src/routes/health.rs

```rust
//! Health check routes.

use axum::Json;
use serde::Serialize;

#[derive(Serialize)]
pub struct HealthResponse {
    status: String,
    version: String,
}

pub async fn health_check() -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok".into(),
        version: env!("CARGO_PKG_VERSION").into(),
    })
}
```

### src/routes/dashboard.rs

```rust
//! Dashboard routes.

use axum::Json;

use crate::models::dashboard::{DashboardData, KpiData};

pub async fn get_dashboard() -> &'static str {
    // In production, render a template here
    "Dashboard"
}

pub async fn get_dashboard_data() -> Json<DashboardData> {
    Json(DashboardData {
        kpis: vec![
            KpiData {
                label: "Total Threats".into(),
                value: 1234,
                trend: 15.3,
                trend_direction: "up".into(),
            },
            KpiData {
                label: "Blocked Attacks".into(),
                value: 892,
                trend: 8.2,
                trend_direction: "up".into(),
            },
            KpiData {
                label: "Active Alerts".into(),
                value: 23,
                trend: -5.1,
                trend_direction: "down".into(),
            },
        ],
    })
}
```

### src/models/mod.rs

```rust
//! Data models.

pub mod dashboard;
```

### src/models/dashboard.rs

```rust
//! Dashboard data models.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KpiData {
    pub label: String,
    pub value: i64,
    pub trend: f64,
    pub trend_direction: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DashboardData {
    pub kpis: Vec<KpiData>,
}
```

### templates/base.html (Tera)

```html
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme | default(value='light') }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }} - {{PROJECT_NAME}}</title>

  <!-- Design tokens FIRST -->
  <link rel="stylesheet" href="/static/css/tokens.css">
  <link rel="stylesheet" href="/static/css/dashboard.css">

  <script>
    (function() {
      const theme = localStorage.getItem('theme') || 'light';
      document.documentElement.setAttribute('data-theme', theme);
    })();
  </script>
</head>
<body>
  {% block content %}{% endblock %}

  <script>
    function toggleTheme() {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    }
  </script>
</body>
</html>
```

### Dockerfile

```dockerfile
# Build stage
FROM rust:1.75-slim as builder

WORKDIR /app
COPY . .
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim

WORKDIR /app

# Copy binary
COPY --from=builder /app/target/release/{{PROJECT_NAME}} .

# Copy static files and templates
COPY static/ ./static/
COPY templates/ ./templates/

# Run
EXPOSE 3000
CMD ["./{{PROJECT_NAME}}"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./static:/app/static
      - ./templates:/app/templates
    environment:
      - RUST_LOG=info
      - PORT=3000
```

## Commands

```bash
# Build
cargo build

# Run development server (with auto-reload using cargo-watch)
cargo watch -x run

# Validate CSS tokens
python scripts/validate_tokens.py static

# Run tests
cargo test

# Production build
cargo build --release

# Format code
cargo fmt

# Lint
cargo clippy
```

## Integration Checklist

- [ ] `tokens.css` exists in static/css/
- [ ] Templates load tokens.css before other styles
- [ ] Tower-http serves static files correctly
- [ ] Error types implement IntoResponse
- [ ] Tracing configured for observability
- [ ] Configuration loads from environment
- [ ] Dockerfile builds successfully
- [ ] Tests cover critical routes
