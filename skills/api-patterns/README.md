# API Patterns Skill

> Comprehensive guide for designing and implementing APIs across REST, GraphQL, gRPC, and tRPC patterns.

## Overview

This skill provides framework selection guidance, pagination strategies, OpenAPI documentation, and frontend integration patterns for Python, TypeScript, Rust, and Go.

**Status**: Production-ready
**Version**: 1.0.0
**Date**: December 2025

## Quick Start

### For Users

1. **Choose API pattern** based on consumers:
   - Public API → REST (FastAPI, Hono, Axum, Gin)
   - TypeScript full-stack → tRPC
   - Flexible data fetching → GraphQL
   - Service-to-service → gRPC

2. **Reference SKILL.md** for decision frameworks and quick examples

3. **Use references/** for deep-dive guides:
   - `rest-design-principles.md` - REST best practices
   - `pagination-patterns.md` - Cursor vs offset pagination
   - `trpc-setup-guide.md` - tRPC E2E type safety
   - `graphql-schema-design.md` - GraphQL schemas, N+1 prevention
   - `grpc-protobuf-guide.md` - gRPC and Protocol Buffers
   - `openapi-documentation.md` - Auto-generated docs

4. **Explore examples/** for complete working projects

5. **Run scripts/** for token-free validation:
   - `generate_openapi.py` - Extract OpenAPI specs
   - `validate_api_spec.py` - Validate OpenAPI 3.1
   - `benchmark_endpoints.py` - Load test APIs

### For Developers

See `init.md` for master plan and architecture decisions.

## Structure

```
api-patterns/
├── SKILL.md                        # Main skill file (<500 lines)
├── README.md                       # This file
├── init.md                         # Master plan
├── references/                     # Detailed guides (one level deep)
│   ├── rest-design-principles.md
│   ├── pagination-patterns.md
│   ├── trpc-setup-guide.md
│   ├── graphql-schema-design.md
│   ├── grpc-protobuf-guide.md
│   └── openapi-documentation.md
├── examples/                       # Working code examples
│   ├── python-fastapi/
│   │   ├── main.py
│   │   └── requirements.txt
│   └── typescript-hono/
│       ├── index.ts
│       └── package.json
└── scripts/                        # Token-free utilities
    ├── generate_openapi.py
    ├── validate_api_spec.py
    └── benchmark_endpoints.py
```

## Key Features

### Multi-Paradigm Coverage

- **REST**: FastAPI (Python), Hono (TypeScript), Axum (Rust), Gin (Go)
- **GraphQL**: Strawberry (Python), Pothos (TypeScript), async-graphql (Rust), gqlgen (Go)
- **gRPC**: grpcio (Python), Connect-Go (Go), Tonic (Rust)
- **tRPC**: TypeScript E2E type safety with zero codegen

### Context7 Research

All framework recommendations validated with Context7:
- FastAPI: `/websites/fastapi_tiangolo` (Score: 79.8, Snippets: 29,015)
- Hono: `/llmstxt/hono_dev_llms_txt` (Score: 92.1, Snippets: 1,817)
- tRPC: `/trpc/trpc` (Score: 92.7, Snippets: 900)
- Axum: `/websites/rs_axum_axum` (Score: 77.5, Snippets: 7,260)

### Performance Benchmarks

| Framework | Req/s | Latency | Cold Start | Best For |
|-----------|-------|---------|------------|----------|
| Axum (Rust) | ~140k | <1ms | N/A | Max throughput |
| Gin (Go) | ~100k+ | 1-2ms | N/A | Mature ecosystem |
| Hono (TS) | ~50k | <5ms | <5ms | Edge deployment |
| FastAPI (Python) | ~40k | 5-10ms | 1-2s | Developer experience |

### Pagination Strategies

**Cursor-based (Recommended for Scale)**:
- Scales to billions of records
- No skipped/duplicate records
- Handles real-time data changes
- Working examples in Python, TypeScript

**Offset-based (Simple Cases)**:
- Direct page number access
- Simple implementation
- Use for static, small datasets

### OpenAPI Auto-Generation

- **FastAPI**: Zero configuration, automatic docs at `/docs`, `/redoc`
- **Hono**: Middleware plugin with Swagger UI
- **Axum**: utoipa crate with annotations
- **Gin**: swaggo/swag with comment annotations

### Frontend Integration

Explicit patterns for connecting to all frontend skills:
- **forms** → POST/PUT/PATCH endpoints
- **tables** → GET + cursor pagination
- **dashboards** → GET + SSE for real-time
- **ai-chat** → POST + SSE streaming
- **search-filter** → GraphQL flexible queries
- **media** → POST multipart file uploads

## Examples

### FastAPI (Python)

```bash
cd examples/python-fastapi
pip install -r requirements.txt
python main.py
# Visit http://localhost:8000/docs
```

**Features**:
- Automatic OpenAPI documentation
- Cursor-based pagination
- Rate limiting (slowapi)
- Pydantic v2 validation

### Hono (TypeScript)

```bash
cd examples/typescript-hono
bun install
bun run dev
# Visit http://localhost:3000/docs
```

**Features**:
- Edge-first (14KB, <5ms cold start)
- Zod validation
- OpenAPI middleware
- Runs on any runtime (Node, Deno, Bun, Cloudflare Workers)

## Scripts Usage

### Generate OpenAPI Spec

```bash
python scripts/generate_openapi.py examples/python-fastapi/main.py openapi.json
```

Extracts OpenAPI specification without running the server.

### Validate OpenAPI Spec

```bash
python scripts/validate_api_spec.py openapi.json
```

Validates against OpenAPI 3.1 schema, reports errors and warnings.

### Benchmark Endpoints

```bash
python scripts/benchmark_endpoints.py http://localhost:8000 --requests 1000 --concurrency 10
```

Load tests API endpoints and reports:
- Requests per second
- Latency (avg, min, max, p50, p95, p99)
- Success/failure rates

## Decision Framework

### Choose API Pattern

```
WHO CONSUMES YOUR API?

PUBLIC/THIRD-PARTY → REST
├─ Python → FastAPI
├─ TypeScript → Hono
├─ Rust → Axum
└─ Go → Gin

FRONTEND TEAM (same org)
├─ TypeScript full-stack → tRPC
└─ Complex data needs → GraphQL

SERVICE-TO-SERVICE → gRPC
└─ High performance needed

MOBILE APPS
├─ Bandwidth constrained → GraphQL
└─ Simple CRUD → REST
```

### Choose Framework by Language

**Python**: FastAPI (modern, auto-docs) > Flask (lightweight) > Django REST

**TypeScript**: Hono (edge-first) > tRPC (full-stack TS) > Express (legacy)

**Rust**: Axum (ergonomics) > Actix-web (max perf) > Rocket (easy DX)

**Go**: Gin (standard) > net/http (stdlib) > Echo/Fiber (enterprise)

## Best Practices

1. **Use cursor pagination** for production APIs (not offset)
2. **Auto-generate OpenAPI docs** (FastAPI, Hono)
3. **Validate with Zod/Pydantic** (type-safe validation)
4. **Implement rate limiting** (prevent abuse)
5. **Use gRPC for microservices** (high performance)
6. **Use tRPC for TypeScript full-stack** (E2E type safety)
7. **Document all endpoints** (descriptions, examples)
8. **Handle errors properly** (RFC 7807 Problem Details)
9. **Enable CORS** (for browser clients)
10. **Version APIs** (URI versioning: `/api/v1/`)

## Integration with Other Skills

### forms Skill
Use POST/PUT endpoints with Pydantic/Zod validation for form submissions.

### tables Skill
Implement cursor pagination for scalable table data fetching.

### dashboards Skill
Combine REST endpoints with SSE for real-time dashboard updates.

### ai-chat Skill
Use SSE streaming for LLM response streaming to chat interfaces.

### search-filter Skill
Implement GraphQL for flexible filtering and field selection.

### databases-* Skills
Connect API endpoints to database operations (PostgreSQL, MongoDB, etc.).

## Production Checklist

- [ ] Authentication implemented (JWT, OAuth2, API keys)
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Error handling comprehensive
- [ ] OpenAPI docs generated and accessible
- [ ] Pagination implemented (cursor-based preferred)
- [ ] Validation schemas defined (Pydantic, Zod)
- [ ] Database connection pooling configured
- [ ] Logging structured and comprehensive
- [ ] Metrics/monitoring integrated (Prometheus)
- [ ] HTTPS enforced (reverse proxy with SSL)
- [ ] Environment variables for configuration

## Resources

### Official Documentation
- **FastAPI**: https://fastapi.tiangolo.com
- **Hono**: https://hono.dev
- **tRPC**: https://trpc.io
- **Axum**: https://docs.rs/axum

### Context7 Sources
- FastAPI: `/websites/fastapi_tiangolo`, `/fastapi/fastapi`
- Hono: `/llmstxt/hono_dev_llms_txt`, `/honojs/hono`
- tRPC: `/trpc/trpc`, `/websites/trpc_io`
- Axum: `/websites/rs_axum_axum`, `/tokio-rs/axum`

### Related Skills
- `forms` - Form validation and submission
- `tables` - Data table integration with pagination
- `dashboards` - Real-time dashboard APIs
- `ai-chat` - SSE streaming for chat interfaces
- `databases-sql` - SQL database integration
- `auth-security` - Authentication and authorization

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-02 | Initial production release |

## License

MIT License - See repository root for details

---

**Built with Claude Code following Anthropic's best practices for Skills development.**
