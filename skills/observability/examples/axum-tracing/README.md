# Rust Axum + OpenTelemetry Tracing Example

Production-ready Rust application with OpenTelemetry instrumentation using tracing crate.

## Features

- Axum web framework
- tracing crate (structured logging + spans)
- tracing-opentelemetry bridge
- OpenTelemetry export to OTLP
- Log-trace correlation
- Prometheus metrics

## Files

```
axum-tracing/
├── src/
│   ├── main.rs              # Server with tracing setup
│   ├── routes.rs            # API routes
│   └── telemetry.rs         # OpenTelemetry configuration
├── Cargo.toml
└── .env.example
```

## Quick Start

```bash
# Start LGTM stack (in separate directory)
cd ../lgtm-docker-compose
docker-compose up -d

# Run Axum app
cargo run
```

Access:
- API: http://localhost:3000
- Grafana: http://localhost:3000 (admin/admin)

## Implementation

### Dependencies (Cargo.toml)

```toml
[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
tracing-opentelemetry = "0.22"
opentelemetry = { version = "0.21", features = ["trace"] }
opentelemetry-otlp = { version = "0.14", features = ["grpc-tonic"] }
opentelemetry_sdk = { version = "0.21", features = ["rt-tokio"] }
```

### Tracing Setup

```rust
// src/telemetry.rs
use opentelemetry::global;
use opentelemetry_otlp::WithExportConfig;
use opentelemetry_sdk::{runtime, trace as sdktrace};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

pub fn init_telemetry() {
    // OpenTelemetry tracer
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint("http://localhost:4317")
        )
        .with_trace_config(
            sdktrace::config()
                .with_resource(opentelemetry_sdk::Resource::new(vec![
                    opentelemetry::KeyValue::new("service.name", "axum-api"),
                ]))
        )
        .install_batch(runtime::Tokio)
        .unwrap();

    // Tracing subscriber with OpenTelemetry layer
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new("info"))
        .with(tracing_subscriber::fmt::layer().json())
        .with(tracing_opentelemetry::layer().with_tracer(tracer))
        .init();
}
```

### Instrumented Handler

```rust
// src/routes.rs
use axum::{extract::Path, Json};
use tracing::{info, instrument};
use serde::Serialize;

#[derive(Serialize)]
struct User {
    id: u64,
    name: String,
}

#[instrument(fields(user_id = %user_id))]
async fn get_user(Path(user_id): Path<u64>) -> Json<User> {
    // Log with trace context automatically included
    info!(user_id = user_id, "Fetching user from database");

    // Simulate DB query
    let user = User {
        id: user_id,
        name: "John Doe".to_string(),
    };

    info!(user_id = user_id, "User found");

    Json(user)
}
```

### Main Server

```rust
// src/main.rs
mod routes;
mod telemetry;

use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    // Initialize telemetry
    telemetry::init_telemetry();

    let app = Router::new()
        .route("/users/:id", get(routes::get_user));

    println!("Server running on http://localhost:3000");

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();

    // Shutdown telemetry
    opentelemetry::global::shutdown_tracer_provider();
}
```

## Log Output

```json
{
  "timestamp": "2025-12-03T10:30:00.123Z",
  "level": "INFO",
  "message": "Fetching user from database",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "user_id": 42
}
```

## Query in Grafana

```logql
{service_name="axum-api"} |= "trace_id=4bf92f3577b34da6a3ce929d0e0e4736"
```

## Benefits

- Automatic trace context propagation
- Zero-cost abstractions (compile-time only)
- Structured logging built-in
- OpenTelemetry standard compliance
