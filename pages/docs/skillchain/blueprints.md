---
sidebar_position: 4
title: Blueprints
description: Pre-configured skill chains for common patterns
---

# Blueprints

Blueprints are pre-configured skill chains that provide fast-track workflows for common application patterns. Instead of answering 12+ questions, blueprints reduce setup to just 3-4 key decisions.

## What are Blueprints?

A blueprint is a pre-configured skill chain that:

1. **Matches common patterns** - Recognizes dashboard, CRUD API, RAG pipeline, etc.
2. **Pre-selects skills** - Automatically chooses the right skills in correct order
3. **Provides smart defaults** - Offers opinionated defaults that work together
4. **Reduces questions** - Only asks essential configuration questions
5. **Ensures consistency** - All pieces integrate seamlessly

### Benefits

| Without Blueprint | With Blueprint |
|-------------------|----------------|
| 12+ configuration questions | 3-4 key questions |
| Must understand skill dependencies | Dependencies pre-configured |
| Risk of incompatible choices | Tested combinations only |
| 8-12 minute setup | 5-7 minute setup |

## Available Blueprints

### Dashboard Blueprint

**Pattern:** Analytics dashboards with charts, KPIs, and data tables

**Trigger Keywords:**
- dashboard
- analytics
- admin panel
- metrics
- KPI
- overview
- reporting
- stats

**Pre-Configured Skills:**
1. theming-components (foundation)
2. designing-layouts (structure)
3. creating-dashboards (dashboard layout)
4. visualizing-data (charts)
5. building-tables (optional: data tables)
6. providing-feedback (loading states)
7. assembling-components (final assembly)

**Questions Asked (3):**
1. Color scheme? (blue-gray, purple, green, custom)
2. Chart types? (bar, line, pie, area, scatter)
3. Include data tables? (yes/no)

**Example Usage:**
```bash
/skillchain analytics dashboard with revenue charts

# Skillchain detects "dashboard" and "analytics"
# Offers dashboard blueprint
# Asks 3 questions
# Generates themed dashboard in 5 minutes
```

**Output Includes:**
- Themed UI with consistent design tokens
- Responsive grid layout (sidebar + main content)
- 4 KPI cards with icons
- Charts (using your selected types)
- Optional data table with sorting/pagination
- Loading skeletons
- Dark mode support

---

### CRUD API Blueprint

**Pattern:** REST API with database, authentication, and CRUD operations

**Trigger Keywords:**
- REST API
- CRUD
- backend API
- FastAPI
- database API
- postgres api
- api server

**Pre-Configured Skills:**
1. api-patterns (REST endpoints)
2. databases-relational (Postgres/MySQL/SQLite)
3. auth-security (JWT authentication)
4. observability (optional: monitoring)
5. deploying-applications (optional: deployment)

**Questions Asked (4):**
1. Backend framework? (fastapi/express/axum/hono)
2. Database? (postgres/mysql/sqlite)
3. Authentication? (jwt/oauth/none)
4. Include deployment? (yes/no)

**Example Usage:**
```bash
/skillchain REST API with PostgreSQL database

# Skillchain detects "REST API" and "PostgreSQL"
# Offers crud-api blueprint
# Asks 4 questions
# Generates production-ready API in 6 minutes
```

**Output Includes:**
- REST endpoints (GET, POST, PUT, DELETE)
- Database models and migrations
- JWT authentication middleware
- Request validation with Pydantic/Zod
- Error handling
- OpenAPI/Swagger documentation
- Optional: Kubernetes deployment configs
- Optional: OpenTelemetry observability

**Multi-Language Support:**

| Framework | Language | Ecosystem |
|-----------|----------|-----------|
| FastAPI | Python | Pydantic, SQLAlchemy |
| Express | TypeScript | Zod, Prisma/Drizzle |
| Axum | Rust | Serde, SeaORM |
| Hono | TypeScript | Edge-optimized |

---

### RAG Pipeline Blueprint

**Pattern:** RAG system with vector search, embeddings, and document processing

**Trigger Keywords:**
- RAG
- semantic search
- vector search
- embeddings
- document Q&A
- knowledge base
- AI search

**Pre-Configured Skills:**
1. ingesting-data (document ingestion)
2. databases-vector (Qdrant/pgvector/Pinecone)
3. ai-data-engineering (chunking, embeddings)
4. api-patterns (query API)
5. model-serving (optional: LLM hosting)
6. building-ai-chat (optional: UI)

**Questions Asked (4):**
1. Vector database? (qdrant/pgvector/pinecone)
2. Embedding model? (openai/sentence-transformers/cohere)
3. LLM provider? (openai/anthropic/ollama/vllm)
4. Include chat UI? (yes/no)

**Example Usage:**
```bash
/skillchain RAG pipeline with semantic search

# Skillchain detects "RAG" and "semantic search"
# Offers rag-pipeline blueprint
# Asks 4 questions
# Generates complete RAG system in 7 minutes
```

**Output Includes:**
- Document ingestion (PDF, TXT, MD, DOCX)
- Chunking strategy (semantic, fixed, recursive)
- Vector database setup with collections
- Embedding generation pipeline
- Semantic search API endpoint
- RAG query pipeline with context retrieval
- Optional: LLM hosting with vLLM/Ollama
- Optional: Chat UI with streaming responses

**Data Flow:**
```
Documents → Chunking → Embeddings → Vector DB
                                        ↓
User Query → Embedding → Similarity Search → Retrieved Context
                                        ↓
                            LLM (context + query) → Response
```

---

## Using Blueprints

### Automatic Detection

Blueprints are automatically detected based on keywords in your goal:

```bash
# Dashboard blueprint detected
/skillchain analytics dashboard
/skillchain admin panel with metrics
/skillchain KPI overview

# CRUD API blueprint detected
/skillchain REST API with postgres
/skillchain FastAPI CRUD endpoints
/skillchain backend API server

# RAG pipeline blueprint detected
/skillchain RAG system
/skillchain semantic search with embeddings
/skillchain document Q&A knowledge base
```

### Detection Confidence

Blueprints use a confidence threshold (70%):

```
Confidence calculation:
- Primary keyword match: +10 points each
- Secondary keyword match: +5 points each
- Threshold: 7 points (70%)

Example:
"/skillchain analytics dashboard with KPI cards"
- "analytics" (secondary): +5
- "dashboard" (primary): +10
- "KPI" (secondary): +5
Total: 20 points (200%) → HIGH confidence, offer blueprint
```

### Blueprint Prompt

When detected, you'll see:

```
🎯 I detected this matches our 'dashboard' blueprint!

This blueprint provides:
- Pre-configured skill chain (7 skills)
- Optimized defaults
- Only 3 questions instead of 12+
- Estimated time: 5 minutes

Would you like to use the dashboard blueprint?
  → yes (use preset with 3 questions)
  → no (manual configuration with 12+ questions)
  → customize (preset + ability to modify defaults)
```

### Choosing an Option

**Option 1: Yes (Recommended)**
```
You: yes

# Uses blueprint with minimal questions
# Fastest path to working code
# Best for prototyping and common patterns
```

**Option 2: No**
```
You: no

# Manual skill selection
# Full control over every decision
# Best for unique requirements
```

**Option 3: Customize**
```
You: customize

# Starts with blueprint configuration
# Allows overriding specific defaults
# Best for "mostly standard" patterns
```

## Creating Custom Blueprints

You can extend skillchain with your own blueprints.

### Blueprint Structure

```yaml
# .claude/commands/skillchain/blueprints/my-blueprint.md
---
description: "Brief description"
allowed-tools: ["Skill", "Read", "Write"]
---

# My Custom Blueprint

## Pattern Detection
Primary keywords: [list]
Secondary keywords: [list]
Exclusions: [list]

## Pre-configured Skills
1. skill-name-1 (invocation path)
2. skill-name-2 (invocation path)
...

## Questions
1. Question text?
   - Option A (default)
   - Option B
   - Option C

2. Next question?
   ...

## Defaults
skill-name-1:
  config_key: default_value

## Output Configuration
[Instructions for assembling components]
```

### Example: E-commerce Blueprint

```yaml
# blueprints/ecommerce.md
---
description: "E-commerce store with product catalog, cart, and checkout"
---

# E-commerce Blueprint

## Pattern Detection
Primary: [store, shop, ecommerce, e-commerce, cart, checkout]
Secondary: [products, catalog, payment, stripe]

## Pre-configured Skills
1. theming-components
2. designing-layouts
3. building-tables (product catalog)
4. building-forms (checkout)
5. providing-feedback (cart notifications)
6. api-patterns (backend)
7. databases-relational (products DB)
8. auth-security (user accounts)
9. assembling-components

## Questions (5)
1. Product categories? (clothing/electronics/services/mixed)
2. Payment provider? (stripe/paypal/square)
3. User accounts? (required/optional/guest-only)
4. Inventory tracking? (yes/no)
5. Include admin panel? (yes/no)

## Defaults
theming-components:
  color_scheme: "commercial-blue"

building-tables:
  product_grid_columns: 3
  show_filters: true

## Output
- Product catalog with search/filter
- Shopping cart with persistence
- Checkout flow (3 steps)
- Payment integration
- Order management API
- Admin dashboard (optional)
```

### Registering Custom Blueprints

Add to `_registry.yaml`:

```yaml
blueprints:
  ecommerce:
    description: "E-commerce store with cart and checkout"
    category: fullstack
    confidence_threshold: 0.7

    triggers:
      primary: [store, shop, ecommerce, cart]
      secondary: [products, catalog, payment]

    skill_chain:
      - theming-components
      - designing-layouts
      - building-tables
      - building-forms
      - api-patterns
      - databases-relational
      - assembling-components

    quick_questions: 5
    estimated_time: "8 minutes"

    file: "{SKILLCHAIN_DIR}/blueprints/ecommerce.md"
```

## Blueprint Best Practices

### 1. Focus on Common Patterns

Create blueprints for patterns you build repeatedly:
- Dashboard (used by 80% of apps)
- CRUD API (foundational backend)
- RAG pipeline (emerging AI pattern)

### 2. Optimize Question Count

Aim for 3-5 questions:
- Too few (1-2): Not enough customization
- Just right (3-5): Fast but flexible
- Too many (8+): Defeats blueprint purpose

### 3. Provide Sensible Defaults

Choose defaults that work for 80% of cases:
```yaml
# Good defaults
color_scheme: "blue-gray"  # Neutral, professional
database: "postgres"       # Most popular
framework: "react"         # Widest adoption
```

### 4. Test Skill Combinations

Ensure pre-configured skills work together:
- All dependencies satisfied
- No conflicting configurations
- Tested end-to-end

### 5. Document Output Clearly

Users should know what they'll get:
```markdown
## Output Includes
- Responsive dashboard layout
- 5 pre-built chart components
- Dark mode support
- Loading states
```

## Troubleshooting

### Blueprint Not Detected

**Problem:** Keywords not matching

**Solution:** Use more specific blueprint keywords
```bash
# Instead of:
/skillchain data display page

# Use:
/skillchain analytics dashboard
```

### Wrong Blueprint Detected

**Problem:** Multiple blueprints match

**Solution:** Add exclusion keywords or be more specific
```bash
# If RAG blueprint triggers for general "search":
/skillchain product search filter  # "filter" + "product" = frontend
```

### Want Blueprint But Need Customization

**Problem:** Blueprint is 90% right

**Solution:** Choose "customize" option
```
Claude: Use dashboard blueprint? (yes/no/customize)
You: customize
```

## Next Steps

- [Understand architecture](./architecture.md) to see how blueprints work internally
- [View usage examples](./usage.md) for blueprint-optimized queries
- [Explore skills](../skills/overview.md) to understand what blueprints orchestrate
