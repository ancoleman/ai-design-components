# RAG Pipeline Blueprint

**Version:** 2.0.0
**Category:** ai-ml
**Type:** Backend-focused with optional frontend

---

## Trigger Keywords

**Primary:**
- rag, rag pipeline
- semantic search
- embeddings
- vector search
- document qa, document q&a
- knowledge base
- retrieval augmented generation

**Secondary:**
- similarity search
- context retrieval
- ai search
- intelligent search
- document assistant

**Context indicators:**
- "with vector database"
- "using embeddings"
- "semantic similarity"
- "document understanding"

---

## Skill Chain (Pre-configured)

### Pure Backend Pattern (Default)

```
1. ingesting-data          # Document loading and processing
2. databases-vector        # Vector store (Qdrant/pgvector)
3. ai-data-engineering     # RAG pipeline, chunking, embeddings
4. implementing-api-patterns            # REST/GraphQL endpoints
5. [OPTIONAL] model-serving          # Self-hosted LLM inference
6. [OPTIONAL] securing-authentication          # API authentication
7. [OPTIONAL] observability          # Monitoring and logging
```

### With Chat UI Pattern

```
1. theming-components      # Design tokens and theming
2. building-ai-chat        # Chat interface with streaming
3. building-forms          # Additional input components
4. implementing-api-patterns            # Backend API
5. databases-vector        # Vector store
6. ai-data-engineering     # RAG pipeline
7. [OPTIONAL] model-serving          # Self-hosted LLM
8. [OPTIONAL] securing-authentication          # Authentication
9. assembling-components   # Wire frontend + backend
```

---

## Pre-configured Defaults

### ingesting-data

**Optimized for document processing:**

```yaml
source_type: "files"
supported_formats:
  - PDF
  - Markdown (.md)
  - Text (.txt)
  - JSON
  - HTML

batch_size: 100
incremental: true
duplicate_detection: true

processing:
  clean_text: true
  extract_metadata: true
  preserve_structure: true
```

### databases-vector

**Production-ready vector store:**

```yaml
database: "Qdrant"  # Self-hosted, production-ready
alternatives: ["pgvector", "Pinecone"]

dimensions: 1536  # OpenAI text-embedding-3-small
# OR: 384 for sentence-transformers/all-MiniLM-L6-v2

distance_metric: "cosine"
index_type: "HNSW"

configuration:
  collection_name: "documents"
  vector_size: 1536
  on_disk_payload: true

  hnsw_config:
    m: 16
    ef_construct: 100
```

### ai-data-engineering

**RAG-optimized chunking and embeddings:**

```yaml
chunking_strategy: "recursive"
chunk_size: 512
chunk_overlap: 50

embedding_model: "text-embedding-3-small"
embedding_provider: "OpenAI"
# OR: "sentence-transformers/all-MiniLM-L6-v2" for local

pipeline_steps:
  1. Document parsing
  2. Text cleaning
  3. Semantic chunking
  4. Embedding generation
  5. Vector indexing
  6. Metadata storage

metadata_extraction:
  - document_title
  - source_file
  - created_date
  - chunk_index
  - section_heading

retrieval_strategy: "hybrid"  # Vector + keyword
top_k: 5
reranking: true
```

### implementing-api-patterns

**Streaming-enabled API:**

```yaml
style: "REST"
framework: "FastAPI"
streaming: true

endpoints:
  POST /chat:
    - Accepts query
    - Retrieves context from vector DB
    - Calls LLM with context
    - Streams response

  POST /embed:
    - Generates embeddings
    - Returns vector

  GET /search:
    - Semantic search
    - Returns top-k documents

features:
  - SSE (Server-Sent Events) for streaming
  - Request validation
  - Error handling
  - Rate limiting
```

### model-serving (Optional)

**Self-hosted LLM inference:**

```yaml
serving_engine: "vLLM"  # High-throughput GPU serving
alternatives: ["Ollama", "BentoML"]

model_defaults:
  - meta-llama/Llama-2-7b-chat-hf
  - mistralai/Mistral-7B-Instruct-v0.2

configuration:
  max_tokens: 2048
  temperature: 0.7
  streaming: true

  vllm_config:
    gpu_memory_utilization: 0.9
    max_num_seqs: 64
```

### building-ai-chat (Optional - for UI)

**Chat interface defaults:**

```yaml
streaming: true
context_display: true
source_citations: true

features:
  - Message history
  - Typing indicators
  - Error states
  - Retry logic
  - Copy response
  - Regenerate
```

---

## Quick Questions (4 Maximum)

These questions are asked ONCE at the beginning to set all defaults:

### 1. Document Types
```
What types of documents will you process?
A) PDF files
B) Markdown/Text files
C) Web pages (HTML)
D) Code repositories
E) Mixed (multiple types)

[Default: E - Mixed]
```

**Impact:** Configures ingesting-data parsers and chunking strategies

### 2. Embedding Provider
```
Which embedding provider?
A) OpenAI (text-embedding-3-small, hosted, $$$)
B) Cohere (embed-english-v3.0, hosted, $$)
C) Local (sentence-transformers, self-hosted, free)

[Default: A - OpenAI]
```

**Impact:** Sets embedding model, dimensions, and vector DB config

### 3. Include Chat UI
```
Include a chat interface?
A) Yes - Full chat UI with streaming
B) No - API only

[Default: B - API only]
```

**Impact:** Adds building-ai-chat, theming-components, assembling-components

### 4. LLM Provider
```
LLM provider for responses?
A) OpenAI (GPT-4, hosted, $$$)
B) Anthropic (Claude, hosted, $$$)
C) Self-hosted (vLLM/Ollama, free, requires GPU)
D) API only (no LLM, just retrieval)

[Default: A - OpenAI]
```

**Impact:** Adds model-serving if self-hosted, configures API integration

---

## Generated Output Structure

### Pure Backend (API Only)

```
rag-pipeline/
├── src/
│   ├── ingestion/
│   │   ├── loaders.py              # PDF, markdown, text loaders
│   │   ├── processors.py           # Text cleaning, metadata extraction
│   │   └── batch_processor.py      # Batch ingestion logic
│   │
│   ├── chunking/
│   │   ├── strategies.py           # Recursive, semantic, fixed
│   │   ├── splitters.py            # Document splitting logic
│   │   └── overlap_manager.py      # Chunk overlap handling
│   │
│   ├── embeddings/
│   │   ├── generator.py            # Embedding generation
│   │   ├── models.py               # OpenAI/Cohere/local model loading
│   │   └── batch_embed.py          # Batch embedding processing
│   │
│   ├── vector_store/
│   │   ├── client.py               # Qdrant client wrapper
│   │   ├── indexing.py             # Vector indexing logic
│   │   ├── search.py               # Hybrid search (vector + keyword)
│   │   └── reranking.py            # Result reranking
│   │
│   ├── retrieval/
│   │   ├── retriever.py            # Main retrieval orchestrator
│   │   ├── context_builder.py      # Context assembly
│   │   └── metadata_filter.py      # Metadata-based filtering
│   │
│   ├── api/
│   │   ├── main.py                 # FastAPI app
│   │   ├── routes/
│   │   │   ├── chat.py             # POST /chat endpoint
│   │   │   ├── search.py           # GET /search endpoint
│   │   │   └── embed.py            # POST /embed endpoint
│   │   ├── models.py               # Pydantic request/response models
│   │   └── streaming.py            # SSE streaming handlers
│   │
│   └── config/
│       ├── settings.py             # Environment configuration
│       └── prompts.py              # RAG system prompts
│
├── tests/
│   ├── test_chunking.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   └── test_api.py
│
├── scripts/
│   ├── ingest_documents.py         # CLI for document ingestion
│   ├── create_collection.py        # Initialize vector DB
│   └── test_search.py              # Test retrieval quality
│
├── .env.example
├── pyproject.toml
├── README.md
└── docker-compose.yml              # Qdrant + API services
```

### With Chat UI

**Additional files:**

```
frontend/
├── tokens.css                      # Design tokens
├── styles/
│   └── global.css                  # Global theming
│
├── components/
│   ├── ChatInterface.tsx           # Main chat component
│   ├── ChatInterface.css           # Token-based styles
│   ├── ChatMessage.tsx             # Message bubble
│   ├── ChatMessage.css
│   ├── SourceCitation.tsx          # Document citations
│   └── SourceCitation.css
│
├── api/
│   └── chat.ts                     # API client with streaming
│
├── hooks/
│   └── useChat.ts                  # Chat state management
│
└── pages/
    └── index.tsx                   # Main chat page
```

---

## Key Features

### Hybrid Search
- Vector similarity (semantic)
- Keyword matching (BM25)
- Weighted scoring
- Metadata filtering

### Semantic Chunking
- Recursive character splitting
- Configurable chunk size and overlap
- Preserves document structure
- Markdown-aware splitting

### Streaming Responses
- Server-Sent Events (SSE)
- Token-by-token streaming
- Progress indicators
- Error recovery

### Context Management
- Smart context window usage
- Dynamic chunk selection
- Reranking for relevance
- Source citation tracking

### Production-Ready
- Docker deployment
- Environment configuration
- Error handling
- Logging and monitoring
- Rate limiting

---

## Integration Steps

### 1. Environment Setup

```bash
# .env file
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=optional-api-key

# Embedding config
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# LLM config (if using OpenAI)
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7

# API config
API_PORT=8000
API_HOST=0.0.0.0
```

### 2. Start Services

```bash
# Start Qdrant (vector database)
docker-compose up -d qdrant

# Create collection
python scripts/create_collection.py

# Ingest documents
python scripts/ingest_documents.py --dir ./data/documents

# Start API server
uvicorn src.api.main:app --reload
```

### 3. Test Retrieval

```bash
# Test semantic search
python scripts/test_search.py --query "How do I configure the RAG pipeline?"

# Test full chat flow
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "stream": true}'
```

### 4. Frontend (if included)

```bash
cd frontend
npm install
npm run dev

# Visit http://localhost:3000
```

---

## Advanced Configuration Options

### Custom Chunking Strategy

```python
# Override in ai-data-engineering config
chunking_strategy: "semantic"  # Uses sentence embeddings
semantic_threshold: 0.5         # Similarity threshold for chunk boundaries
```

### Reranking Models

```python
# Add to retrieval config
reranker: "cross-encoder/ms-marco-MiniLM-L-12-v2"
rerank_top_k: 20  # Rerank top 20, return top 5
```

### Multi-Modal Documents

```python
# Enable in ingesting-data
extract_images: true
image_captioning: true
table_extraction: true
```

### Hybrid Search Weights

```python
# Adjust in vector_store/search.py
vector_weight: 0.7   # 70% semantic
keyword_weight: 0.3  # 30% keyword
```

---

## Performance Optimizations

### Batch Processing
- Ingest documents in batches of 100
- Parallel embedding generation
- Bulk vector insertion

### Caching
- Cache embeddings for frequent queries
- Redis for response caching
- LRU cache for retrieval results

### Monitoring
- Track retrieval latency
- Monitor embedding generation time
- Log LLM token usage
- Alert on error rates

---

## Common Use Cases

### 1. Internal Documentation Q&A
```
Documents: Engineering docs (Markdown)
Embedding: Local (sentence-transformers)
LLM: Self-hosted (Ollama)
UI: Yes (chat interface)
```

### 2. Customer Support Knowledge Base
```
Documents: Support articles (HTML, PDF)
Embedding: OpenAI
LLM: GPT-4
UI: Yes (integrated into support portal)
Auth: Yes (user-specific context)
```

### 3. Code Search
```
Documents: Code repositories
Embedding: OpenAI Code Search
LLM: GPT-4
UI: No (API only, IDE integration)
```

### 4. Research Paper Assistant
```
Documents: PDFs, arXiv papers
Embedding: Cohere (research-focused)
LLM: Claude (long context)
UI: Yes (chat + citation display)
```

---

## Dependencies Installed

```toml
[tool.poetry.dependencies]
python = "^3.10"

# Vector database
qdrant-client = "^1.7.0"

# Embeddings
openai = "^1.12.0"
sentence-transformers = "^2.3.1"  # Local embeddings
cohere = "^4.45"  # Alternative

# Document processing
pypdf = "^4.0.0"
markdown = "^3.5"
beautifulsoup4 = "^4.12.0"

# API
fastapi = "^0.109.0"
uvicorn = "^0.27.0"
pydantic = "^2.6.0"
sse-starlette = "^2.0.0"  # Streaming

# LLM (if using OpenAI/Anthropic)
anthropic = "^0.18.0"

# Utils
python-dotenv = "^1.0.0"
tenacity = "^8.2.0"  # Retry logic
```

```json
// Frontend dependencies (if UI included)
{
  "dependencies": {
    "react": "^18.2.0",
    "next": "^14.1.0",
    "eventsource-parser": "^1.1.1"  // SSE client
  }
}
```

---

## Next Steps After Generation

1. **Review configuration** - Verify embedding dimensions, chunk sizes
2. **Test with sample documents** - Run ingestion script
3. **Tune retrieval** - Adjust top_k, reranking, hybrid weights
4. **Add monitoring** - Set up observability (optional skill)
5. **Deploy** - Use deploying-applications skill for production
6. **Iterate** - Monitor relevance metrics, adjust chunking/prompts

---

## Blueprint Metadata

**Created:** 2024-12-02
**Skillchain Version:** 2.0.0
**Average Questions:** 4
**Estimated Time:** 8-12 minutes
**Complexity:** Medium-High
**Token Estimate:** ~1800 tokens (backend only), ~2500 tokens (with UI)

---

## Deliverables Specification

This section defines concrete validation checks for blueprint promises, ensuring skills produce what users expect.

### Deliverables

```yaml
deliverables:
  "Document loading and ingestion":
    primary_skill: ingesting-data
    required_files:
      - src/ingestion/loaders.py
      - src/ingestion/processors.py
    content_checks:
      - pattern: "class.*Loader|def.*load_|PyPDF|markdown"
        in: src/ingestion/loaders.py
      - pattern: "clean_text|extract_metadata"
        in: src/ingestion/processors.py
    maturity_required: [starter, intermediate, advanced]

  "Chunking strategies implementation":
    primary_skill: ai-data-engineering
    required_files:
      - src/chunking/strategies.py
      - src/chunking/splitters.py
    content_checks:
      - pattern: "chunk_size|chunk_overlap|RecursiveCharacterTextSplitter"
        in: src/chunking/
      - pattern: "512|split_documents"
        in: src/chunking/strategies.py
    maturity_required: [starter, intermediate, advanced]

  "Embedding generation pipeline":
    primary_skill: ai-data-engineering
    required_files:
      - src/embeddings/generator.py
      - src/embeddings/models.py
    content_checks:
      - pattern: "VoyageAI|OpenAI.*Embeddings|embed_documents"
        in: src/embeddings/
      - pattern: "voyage-3|text-embedding-3-small"
        in: src/embeddings/models.py
    maturity_required: [starter, intermediate, advanced]

  "Vector database setup (Qdrant)":
    primary_skill: using-vector-databases
    required_files:
      - src/vector_store/client.py
      - src/vector_store/indexing.py
    content_checks:
      - pattern: "QdrantClient|create_collection"
        in: src/vector_store/client.py
      - pattern: "VectorParams|Distance\\.COSINE|upsert"
        in: src/vector_store/indexing.py
    maturity_required: [starter, intermediate, advanced]

  "Hybrid search (vector + keyword)":
    primary_skill: using-vector-databases
    required_files:
      - src/vector_store/search.py
    content_checks:
      - pattern: "hybrid.*search|BM25|vector.*keyword"
        in: src/vector_store/search.py
      - pattern: "search.*query_vector|ReciprocalRankFusion"
        in: src/vector_store/search.py
    maturity_required: [intermediate, advanced]

  "Retrieval orchestration":
    primary_skill: ai-data-engineering
    required_files:
      - src/retrieval/retriever.py
      - src/retrieval/context_builder.py
    content_checks:
      - pattern: "retrieve|get_relevant|as_retriever"
        in: src/retrieval/retriever.py
      - pattern: "build_context|format_context"
        in: src/retrieval/context_builder.py
    maturity_required: [starter, intermediate, advanced]

  "Reranking implementation":
    primary_skill: using-vector-databases
    required_files:
      - src/vector_store/reranking.py
    content_checks:
      - pattern: "rerank|cross.encoder|Cohere.*rerank"
        in: src/vector_store/reranking.py
    maturity_required: [intermediate, advanced]

  "Streaming API endpoints":
    primary_skill: implementing-api-patterns
    required_files:
      - src/api/main.py
      - src/api/routes/chat.py
      - src/api/streaming.py
    content_checks:
      - pattern: "FastAPI|@app\\.(post|get)"
        in: src/api/main.py
      - pattern: "StreamingResponse|Server.Sent.Events|SSE"
        in: src/api/streaming.py
      - pattern: "POST /chat|stream.*response"
        in: src/api/routes/chat.py
    maturity_required: [starter, intermediate, advanced]

  "RAG chain implementation":
    primary_skill: ai-data-engineering
    required_files:
      - src/api/routes/chat.py
    content_checks:
      - pattern: "retriever|vector.*store|llm"
        in: src/api/routes/chat.py
      - pattern: "context.*query|RetrievalQA|chain"
        in: src/api/routes/chat.py
    maturity_required: [starter, intermediate, advanced]

  "RAGAS evaluation":
    primary_skill: ai-data-engineering
    required_files:
      - scripts/evaluate_rag.py
    content_checks:
      - pattern: "import ragas|from ragas"
        in: scripts/evaluate_rag.py
      - pattern: "faithfulness|answer_relevancy|context_precision|context_recall"
        in: scripts/evaluate_rag.py
    maturity_required: [intermediate, advanced]

  "LLM serving configuration (if self-hosted)":
    primary_skill: model-serving
    required_files:
      - src/config/settings.py
    content_checks:
      - pattern: "vllm|ollama|LLM_MODEL|base_url"
        in: src/config/settings.py
    maturity_required: [intermediate, advanced]
    conditional: "Answer to Q4 = 'C - Self-hosted'"

  "Chat UI components (if UI included)":
    primary_skill: building-ai-chat
    required_files:
      - frontend/components/ChatInterface.tsx
      - frontend/components/ChatMessage.tsx
    content_checks:
      - pattern: "useState|useEffect|StreamingResponse"
        in: frontend/components/ChatInterface.tsx
      - pattern: "message|role|content"
        in: frontend/components/ChatMessage.tsx
    maturity_required: [starter, intermediate, advanced]
    conditional: "Answer to Q3 = 'A - Yes'"

  "Source citation display (if UI included)":
    primary_skill: building-ai-chat
    required_files:
      - frontend/components/SourceCitation.tsx
    content_checks:
      - pattern: "source|citation|document|metadata"
        in: frontend/components/SourceCitation.tsx
    maturity_required: [intermediate, advanced]
    conditional: "Answer to Q3 = 'A - Yes'"

  "Docker Compose for services":
    primary_skill: assembling-components
    required_files:
      - docker-compose.yml
    content_checks:
      - pattern: "qdrant:|services:"
        in: docker-compose.yml
      - pattern: "image:.*qdrant|ports:.*6333"
        in: docker-compose.yml
    maturity_required: [starter, intermediate, advanced]

  "Document ingestion script":
    primary_skill: ingesting-data
    required_files:
      - scripts/ingest_documents.py
    content_checks:
      - pattern: "def.*ingest|load.*documents"
        in: scripts/ingest_documents.py
      - pattern: "chunk|embed|vector.*store"
        in: scripts/ingest_documents.py
    maturity_required: [starter, intermediate, advanced]

  "Qdrant collection setup script":
    primary_skill: using-vector-databases
    required_files:
      - scripts/create_collection.py
    content_checks:
      - pattern: "create_collection|QdrantClient"
        in: scripts/create_collection.py
      - pattern: "VectorParams|dimension|distance"
        in: scripts/create_collection.py
    maturity_required: [starter, intermediate, advanced]

  "Environment configuration":
    primary_skill: assembling-components
    required_files:
      - .env.example
    content_checks:
      - pattern: "OPENAI_API_KEY|VOYAGE_API_KEY"
        in: .env.example
      - pattern: "QDRANT_URL|EMBEDDING_MODEL"
        in: .env.example
    maturity_required: [starter, intermediate, advanced]

  "API request/response models":
    primary_skill: implementing-api-patterns
    required_files:
      - src/api/models.py
    content_checks:
      - pattern: "BaseModel|Pydantic|class.*Request|class.*Response"
        in: src/api/models.py
      - pattern: "query|message|context"
        in: src/api/models.py
    maturity_required: [starter, intermediate, advanced]

  "RAG system prompts":
    primary_skill: ai-data-engineering
    required_files:
      - src/config/prompts.py
    content_checks:
      - pattern: "system.*prompt|Answer based on|context"
        in: src/config/prompts.py
    maturity_required: [starter, intermediate, advanced]

  "Unit tests for chunking":
    primary_skill: assembling-components
    required_files:
      - tests/test_chunking.py
    content_checks:
      - pattern: "def test_|pytest|assert"
        in: tests/test_chunking.py
      - pattern: "chunk_size|overlap"
        in: tests/test_chunking.py
    maturity_required: [intermediate, advanced]

  "Unit tests for embeddings":
    primary_skill: assembling-components
    required_files:
      - tests/test_embeddings.py
    content_checks:
      - pattern: "def test_|pytest|assert"
        in: tests/test_embeddings.py
      - pattern: "embed|vector|dimension"
        in: tests/test_embeddings.py
    maturity_required: [intermediate, advanced]

  "Unit tests for retrieval":
    primary_skill: assembling-components
    required_files:
      - tests/test_retrieval.py
    content_checks:
      - pattern: "def test_|pytest|assert"
        in: tests/test_retrieval.py
      - pattern: "retrieve|search|relevance"
        in: tests/test_retrieval.py
    maturity_required: [intermediate, advanced]

  "API integration tests":
    primary_skill: assembling-components
    required_files:
      - tests/test_api.py
    content_checks:
      - pattern: "def test_|pytest|TestClient"
        in: tests/test_api.py
      - pattern: "post.*chat|response.*status_code"
        in: tests/test_api.py
    maturity_required: [advanced]

  "README with setup instructions":
    primary_skill: assembling-components
    required_files:
      - README.md
    content_checks:
      - pattern: "## Setup|## Installation|## Quick Start"
        in: README.md
      - pattern: "docker-compose|pip install|environment"
        in: README.md
    maturity_required: [starter, intermediate, advanced]
```

### Maturity Profiles

```yaml
maturity_profiles:
  starter:
    description: "Learning-focused RAG system with working examples, extensive documentation, and simple deployment"

    require_additionally:
      - "Document loading and ingestion"
      - "Chunking strategies implementation"
      - "Embedding generation pipeline"
      - "Vector database setup (Qdrant)"
      - "Retrieval orchestration"
      - "Streaming API endpoints"
      - "RAG chain implementation"
      - "Docker Compose for services"
      - "Document ingestion script"
      - "Qdrant collection setup script"
      - "Environment configuration"
      - "API request/response models"
      - "RAG system prompts"
      - "README with setup instructions"

    skip_deliverables:
      - "Hybrid search (vector + keyword)"
      - "Reranking implementation"
      - "RAGAS evaluation"
      - "LLM serving configuration (if self-hosted)"
      - "Unit tests for chunking"
      - "Unit tests for embeddings"
      - "Unit tests for retrieval"
      - "API integration tests"

    empty_dirs_allowed:
      - data/documents/
      - data/chunks/
      - tests/
      - models/

    generation_adjustments:
      - Use OpenAI embeddings (simpler setup than Voyage AI)
      - Include extensive inline comments and docstrings
      - Provide sample documents for testing
      - Use basic vector search (not hybrid)
      - Skip RAGAS evaluation (focus on getting it working)
      - Docker Compose instead of Kubernetes
      - Include Jupyter notebook for exploration

  intermediate:
    description: "Production-ready RAG with hybrid search, reranking, evaluation metrics, and comprehensive testing"

    require_additionally:
      - "Hybrid search (vector + keyword)"
      - "Reranking implementation"
      - "RAGAS evaluation"
      - "Unit tests for chunking"
      - "Unit tests for embeddings"
      - "Unit tests for retrieval"
      - "Source citation display (if UI included)"

    skip_deliverables:
      - "API integration tests"

    empty_dirs_allowed:
      - data/documents/
      - data/chunks/
      - models/

    generation_adjustments:
      - Enable hybrid search (vector + BM25)
      - Add reranking with cross-encoder or Cohere
      - Implement RAGAS evaluation pipeline
      - Add comprehensive unit tests
      - Include performance monitoring
      - Support both OpenAI and Voyage AI embeddings
      - Add metadata filtering capabilities
      - Include source citation tracking

  advanced:
    description: "Enterprise-scale RAG with full testing, advanced retrieval, self-hosted LLM support, and production deployment"

    require_additionally:
      - "Hybrid search (vector + keyword)"
      - "Reranking implementation"
      - "RAGAS evaluation"
      - "LLM serving configuration (if self-hosted)"
      - "Unit tests for chunking"
      - "Unit tests for embeddings"
      - "Unit tests for retrieval"
      - "API integration tests"
      - "Source citation display (if UI included)"

    skip_deliverables: []

    empty_dirs_allowed:
      - data/documents/
      - data/chunks/

    generation_adjustments:
      - Full hybrid search with weighted scoring
      - Multi-stage reranking (cross-encoder + LLM)
      - Comprehensive RAGAS evaluation with tracking
      - Complete test suite (unit + integration)
      - vLLM integration for self-hosted LLMs
      - Advanced metadata filtering and faceting
      - Multi-modal support (text + images)
      - Semantic caching for performance
      - Kubernetes deployment manifests
      - Prometheus metrics and Grafana dashboards
      - CI/CD pipeline for embeddings updates
```

### Validation Process

After all skills complete, the skillchain orchestrator validates deliverables:

1. **File Existence Check:**
   - Verify all required files exist based on maturity profile
   - Allow empty directories specified in `empty_dirs_allowed`

2. **Content Pattern Matching:**
   - Search each file for expected patterns using regex
   - Ensure RAG-specific implementations (chunking, embedding, retrieval)

3. **Conditional Deliverable Handling:**
   - Skip deliverables marked as conditional if prerequisites not met
   - Example: Skip "Chat UI components" if Q3 answer is "B - API only"

4. **Maturity Profile Application:**
   - Apply generation adjustments based on selected maturity level
   - Starter: Simple setup, extensive docs, basic features
   - Intermediate: Production patterns, testing, advanced retrieval
   - Advanced: Full testing, self-hosted LLM, enterprise features

5. **Report Generation:**
   - List missing required files
   - List failed content checks
   - Provide remediation suggestions
   - Flag critical gaps (e.g., missing vector store setup)

### Example Validation Output

```
✓ RAG Pipeline Validation Results

PASSED (18/23):
  ✓ Document loading and ingestion
  ✓ Chunking strategies implementation (512 tokens, 50 overlap)
  ✓ Embedding generation pipeline (Voyage AI voyage-3)
  ✓ Vector database setup (Qdrant with HNSW)
  ✓ Hybrid search implementation
  ✓ Retrieval orchestration
  ✓ Streaming API endpoints (SSE)
  ✓ RAG chain implementation
  ✓ Docker Compose for services
  ✓ Document ingestion script
  ✓ Qdrant collection setup script
  ✓ Environment configuration
  ✓ API request/response models
  ✓ RAG system prompts
  ✓ Unit tests for chunking
  ✓ Unit tests for embeddings
  ✓ Unit tests for retrieval
  ✓ README with setup instructions

FAILED (2/23):
  ✗ Reranking implementation
    - Missing file: src/vector_store/reranking.py
    - Remediation: Implement cross-encoder reranking or Cohere rerank API

  ✗ RAGAS evaluation
    - File exists: scripts/evaluate_rag.py
    - Missing pattern: "faithfulness|answer_relevancy"
    - Remediation: Import and use RAGAS metrics for evaluation

SKIPPED (3/23) - Not required for intermediate maturity:
  - API integration tests
  - LLM serving configuration (API-only mode selected)
  - Source citation display (API-only mode)

RECOMMENDATIONS:
  1. Add reranking to improve retrieval quality (10-20% accuracy gain)
  2. Implement RAGAS evaluation for production monitoring
  3. Consider adding integration tests for advanced maturity
```
