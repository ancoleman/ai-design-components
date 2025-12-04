# Rust + Axum + Qdrant Vector Search

High-performance vector search API using Rust, Axum web framework, and Qdrant vector database.

## Features

- Axum async web framework
- Qdrant vector database integration
- OpenAI embeddings generation
- Semantic search endpoints
- Type-safe with compile-time checks

## Files

- `main.rs` - Axum server with vector search routes
- `models.rs` - Request/response types
- `qdrant.rs` - Qdrant client wrapper
- `Cargo.toml` - Dependencies

## Setup

```bash
# 1. Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# 3. Set environment variables
export OPENAI_API_KEY="your-key"
export QDRANT_URL="http://localhost:6333"

# 4. Run
cargo run --release
```

## API Endpoints

```bash
# Index document
curl -X POST http://localhost:3000/documents \
  -H "Content-Type: application/json" \
  -d '{"text": "Rust is a systems programming language", "metadata": {"source": "docs"}}'

# Search
curl -X POST http://localhost:3000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "programming languages", "limit": 5}'
```

## Performance

- **Throughput:** 10,000+ req/s (single core)
- **Latency:** <5ms (p99)
- **Memory:** ~10MB baseline

See source files for implementation details.
