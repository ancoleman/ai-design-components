# AI Data Engineering - Master Plan

> **Skill Purpose**: Enable data pipelines, feature stores, RAG architectures, and embedding generation for AI/ML systems. Powers the backend for AI-native applications.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Skill 11), Context7 library research, LangChain ecosystem analysis

---

## Strategic Positioning

### Why This Skill Matters

AI-native applications require fundamentally different data infrastructure than traditional applications:

| Traditional Data Engineering | AI Data Engineering |
|------------------------------|---------------------|
| Batch ETL processes | Real-time embedding pipelines |
| SQL queries | Vector similarity search |
| Row-based storage | Vector databases + hybrid search |
| Schema validation | Chunking strategies + metadata |
| Business metrics | RAG evaluation metrics (RAGAS) |

**This skill is STRATEGIC** because:
1. **Every AI application needs it**: RAG pipelines, semantic search, chatbots, recommendation engines
2. **Rapidly evolving space**: LangChain 0.3+, Feast 0.40+, new embedding models monthly
3. **Production complexity**: Moving from prototype (Chroma local) to production (Qdrant cluster) requires specialized knowledge
4. **Quality measurement**: RAGAS metrics (faithfulness, answer relevancy, context precision) are critical but not widely understood

### Integration with Other Skills

**Frontend Integration:**
- **ai-chat** → Consumes RAG pipeline outputs
- **search-filter** → Uses semantic search backend
- **dashboards** → Displays RAG evaluation metrics

**Backend Integration:**
- **databases-vector** → Qdrant/Pinecone infrastructure
- **databases-relational** → Feature store backends (Feast)
- **observability** → OpenLLMetry for LLM tracing
- **model-serving** → LangChain orchestration

---

## Component Taxonomy

### Tier 1: Feature Stores (ML Feature Serving)

Feature stores solve the "training-serving skew" problem by providing consistent feature computation across training and inference.

| Store | Best For | Real-time | Open Source | Latest Version |
|-------|----------|-----------|-------------|----------------|
| **Feast** | Flexibility, any backend | Yes | Yes | 0.40+ (Dec 2025) |
| **Tecton** | Enterprise, managed | Yes | No | Commercial |
| **Hopsworks** | Governance, regulated | Yes | Yes | 3.0+ |

**Decision Framework:**
```
┌─────────────────────────────────────────────────────────────┐
│              Feature Store Selection                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  REQUIREMENTS?                                               │
│  ├── OPEN SOURCE / FLEXIBILITY                               │
│  │   └─ Feast (works with any backend)                      │
│  │       └─ Backends: PostgreSQL, Redis, DynamoDB, S3       │
│  │                                                          │
│  ├── ENTERPRISE / MANAGED SERVICE                            │
│  │   └─ Tecton (SaaS, proven scale)                         │
│  │                                                          │
│  ├── GOVERNANCE / COMPLIANCE                                 │
│  │   └─ Hopsworks (built-in lineage, GDPR-ready)           │
│  │                                                          │
│  └── SIMPLE / EMBEDDED                                       │
│      └─ Skip feature store, use direct DB queries           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Concepts:**
- **Online Store**: Low-latency serving (Redis, DynamoDB)
- **Offline Store**: Training data (S3, BigQuery, Snowflake)
- **Feature Views**: Feature definitions with transformations
- **Point-in-time Joins**: Prevent data leakage during training

---

### Tier 2: RAG Pipeline Components

RAG (Retrieval-Augmented Generation) is the dominant pattern for grounding LLMs in domain-specific knowledge.

#### Complete RAG Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. INGESTION LAYER                                          │
│     ├── Document Loading                                     │
│     │   ├─ Formats: PDF, DOCX, Markdown, HTML, code        │
│     │   ├─ Loaders: LangChain, LlamaIndex, Unstructured    │
│     │   └─ Metadata: Source, timestamps, author            │
│     │                                                       │
│     ├── Chunking Strategy                                    │
│     │   ├─ Fixed: 512 tokens (recommended default)         │
│     │   ├─ Overlap: 50-100 tokens (prevent boundary loss)  │
│     │   ├─ Semantic: Split on paragraphs, headers          │
│     │   └─ Code-aware: Preserve function/class boundaries  │
│     │                                                       │
│     └── Embedding Generation                                 │
│         ├─ Best quality: Voyage AI voyage-3 (1024 dim)     │
│         ├─ Enterprise: OpenAI text-embedding-3-large       │
│         ├─ Multilingual: Cohere embed-v3                   │
│         └─ Open source: nomic-embed-text-v1.5              │
│                                                              │
│  2. INDEXING LAYER                                           │
│     ├── Vector Storage                                       │
│     │   ├─ Primary: Qdrant (best filtering)                │
│     │   ├─ PostgreSQL shops: pgvector extension            │
│     │   ├─ Managed: Pinecone (zero-ops)                    │
│     │   └─ Scale: Milvus/Zilliz (billion-scale)            │
│     │                                                       │
│     ├── Metadata Indexing                                    │
│     │   ├─ Filterable fields: date, category, source       │
│     │   ├─ Full-text search: BM25 keyword index            │
│     │   └─ Hybrid search: Vector + BM25 combined           │
│     │                                                       │
│     └── Index Optimization                                   │
│         ├─ HNSW algorithm (default for Qdrant)             │
│         ├─ Quantization: Scalar, Product (reduce memory)   │
│         └─ Sharding: Distribute across nodes               │
│                                                              │
│  3. RETRIEVAL LAYER                                          │
│     ├── Query Processing                                     │
│     │   ├─ Query embedding (same model as docs)            │
│     │   ├─ Query expansion (add synonyms, related terms)   │
│     │   └─ Multi-query (generate variations)               │
│     │                                                       │
│     ├── Search Strategy                                      │
│     │   ├─ Vector search: Cosine similarity (default)      │
│     │   ├─ Keyword search: BM25 scoring                    │
│     │   ├─ Hybrid: Weighted combination (0.7 vector + 0.3) │
│     │   └─ Metadata filters: date ranges, categories       │
│     │                                                       │
│     ├── Re-ranking (Optional)                                │
│     │   ├─ Cohere re-rank API                              │
│     │   ├─ Cross-encoder models                            │
│     │   └─ Improves top-k precision significantly          │
│     │                                                       │
│     └── Context Window Management                            │
│         ├─ Top-k: 3-5 chunks (default)                     │
│         ├─ Token budget: 2000-4000 tokens                  │
│         └─ Deduplication: Remove near-identical chunks     │
│                                                              │
│  4. GENERATION LAYER                                         │
│     ├── Context Injection                                    │
│     │   ├─ System prompt with instructions                 │
│     │   ├─ Retrieved chunks in order                       │
│     │   └─ User query at end                               │
│     │                                                       │
│     ├── LLM Call                                             │
│     │   ├─ Streaming: Essential for UX                     │
│     │   ├─ Temperature: 0.0-0.3 (factual responses)        │
│     │   └─ Stop sequences: Prevent hallucination           │
│     │                                                       │
│     └── Post-Processing                                      │
│         ├─ Citation extraction: Link to sources            │
│         ├─ Confidence scoring: Measure certainty           │
│         └─ Hallucination detection: Verify grounding       │
│                                                              │
│  5. EVALUATION LAYER (RAGAS)                                 │
│     ├── Faithfulness                                         │
│     │   └─ Does answer align with retrieved context?       │
│     │                                                       │
│     ├── Answer Relevancy                                     │
│     │   └─ Does answer address the user's question?        │
│     │                                                       │
│     ├── Context Precision                                    │
│     │   └─ Are retrieved chunks actually relevant?         │
│     │                                                       │
│     ├── Context Recall                                       │
│     │   └─ Were all necessary chunks retrieved?            │
│     │                                                       │
│     └── Ground Truth Evaluation                              │
│         ├─ Compare against human-labeled QA pairs          │
│         ├─ Measure retrieval accuracy                      │
│         └─ Track improvement over time                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Chunking Strategies

| Strategy | Chunk Size | Overlap | Best For |
|----------|-----------|---------|----------|
| **Fixed Token** | 512 tokens | 50-100 | General purpose (default) |
| **Sentence-based** | 3-5 sentences | 1 sentence | Preserving semantic units |
| **Paragraph-based** | Natural paragraphs | None | Well-structured documents |
| **Semantic Splitting** | Variable | Contextual | Complex documents |
| **Code-aware** | Function/class | Imports | Source code |

**Critical Considerations:**
- **Too small chunks** (< 256 tokens): Lose context, many retrievals needed
- **Too large chunks** (> 1024 tokens): Irrelevant content, hit token limits
- **Overlap prevents boundary loss**: Critical for incomplete chunks

#### Embedding Models Comparison

| Provider | Model | Dimensions | MTEB Score | Cost | Best For |
|----------|-------|------------|------------|------|----------|
| **Voyage AI** | voyage-3 | 1024 | 69.0 | $$$ | Best quality |
| **OpenAI** | text-embedding-3-large | 3072 | 64.6 | $$ | Enterprise reliability |
| **OpenAI** | text-embedding-3-small | 1536 | 62.3 | $ | Cost-effective |
| **Cohere** | embed-v3 | 1024 | 64.5 | $$ | Multilingual |
| **Open Source** | nomic-embed-text-v1.5 | 768 | 62.4 | Free | Self-hosted English |
| **Open Source** | BAAI/bge-m3 | 1024 | 66.0 | Free | Self-hosted Multilingual |

**Voyage AI is 9.74% better than OpenAI** on retrieval benchmarks (as of Dec 2025).

#### RAGAS Evaluation Metrics

**Why RAGAS is Critical:**
Traditional metrics (BLEU, ROUGE) don't measure RAG quality. RAGAS provides LLM-as-judge evaluation.

| Metric | Measures | Formula | Good Score |
|--------|----------|---------|------------|
| **Faithfulness** | Factual consistency with context | Verified claims / Total claims | > 0.8 |
| **Answer Relevancy** | Addresses user's question | Semantic similarity to query | > 0.7 |
| **Context Precision** | Relevant chunks retrieved | Relevant chunks / Total chunks | > 0.6 |
| **Context Recall** | Completeness of retrieval | Retrieved info / Required info | > 0.7 |

**Implementation:**
```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Evaluation dataset
dataset = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is the capital of France."],
    "contexts": [["France's capital is Paris, located in the north-central part."]],
    "ground_truth": ["Paris"]
}

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
```

---

### Tier 3: Orchestration Tools

Modern data engineering requires workflow orchestration beyond simple cron jobs.

| Tool | Best For | Language | Key Feature | Latest Version |
|------|----------|----------|-------------|----------------|
| **Dagster** | Asset-centric, modern | Python | Asset lineage, data quality | 1.9+ (Dec 2025) |
| **Prefect** | Pythonic, cloud-native | Python | Dynamic workflows, observability | 3.0+ |
| **Airflow 3.0** | Event-driven (2025) | Python | Mature ecosystem, plugins | 3.0+ (released 2025) |
| **dbt** | SQL transformations | SQL | Analytics engineering | 1.9+ |

**Decision Framework:**
```
┌─────────────────────────────────────────────────────────────┐
│              Orchestration Tool Selection                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WORKFLOW TYPE?                                              │
│  ├── DATA TRANSFORMATIONS (SQL-focused)                      │
│  │   └─ dbt (purpose-built for SQL)                         │
│  │                                                          │
│  ├── ML PIPELINES / ASSET-CENTRIC                            │
│  │   └─ Dagster (best lineage tracking)                     │
│  │                                                          │
│  ├── PYTHON-NATIVE / DYNAMIC WORKFLOWS                       │
│  │   └─ Prefect (most Pythonic API)                         │
│  │                                                          │
│  ├── MATURE ECOSYSTEM / MANY INTEGRATIONS                    │
│  │   └─ Airflow 3.0 (largest plugin ecosystem)             │
│  │                                                          │
│  └── EMBEDDING PIPELINES (RAG)                               │
│      └─ LangChain or Dagster                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Dagster for RAG Pipelines:**
```python
from dagster import asset, AssetExecutionContext
from langchain.embeddings import VoyageEmbeddings
from qdrant_client import QdrantClient

@asset
def raw_documents(context: AssetExecutionContext):
    """Load documents from S3."""
    # Load logic
    return documents

@asset
def chunked_documents(raw_documents):
    """Split into 512-token chunks with 50-token overlap."""
    # Chunking logic
    return chunks

@asset
def embedded_documents(chunked_documents):
    """Generate embeddings with Voyage AI."""
    embeddings = VoyageEmbeddings(model="voyage-3")
    return embeddings.embed_documents(chunked_documents)

@asset
def indexed_documents(embedded_documents):
    """Index in Qdrant."""
    client = QdrantClient(url="http://localhost:6333")
    # Indexing logic
    return "indexed"
```

---

## Context7 Library Research

### LangChain Ecosystem (Primary Recommendation)

LangChain is the dominant LLM orchestration framework with the largest ecosystem.

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **LangChain** | `/websites/langchain_oss_python_langchain` | High | 435 | 79.8 | Primary orchestration |
| **LangChain API** | `/websites/python_langchain_api_reference` | High | 24,215 | 70.5 | Complete API docs |
| **LangChain llms.txt** | `/llmstxt/langchain_llms_txt` | High | 3,707 | 75.0 | Quick reference |
| **LangChain4j** | `/langchain4j/langchain4j` | High | 712 | 82.0 | Java implementation |
| **LangChainGo** | `/tmc/langchaingo` | High | 397 | 80.1 | Go implementation |
| **OpenLLMetry** | `/traceloop/openllmetry` | High | 97 | 46.7 | LLM observability |

**Why LangChain (December 2025):**
1. **Largest ecosystem**: 24,215 API reference snippets
2. **Production-ready**: Used by major companies (Uber, Goldman Sachs)
3. **Multi-language**: Python (primary), JavaScript, Java, Go
4. **Best integrations**: 100+ vector stores, 50+ LLM providers
5. **Active development**: v0.3+ has significant performance improvements

**LangChain 0.3+ Architecture:**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_voyageai import VoyageAIEmbeddings

# RAG chain
prompt = ChatPromptTemplate.from_template(
    "Answer based on context:\n{context}\n\nQuestion: {question}"
)

vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name="docs",
    embedding=VoyageAIEmbeddings(model="voyage-3")
)

retriever = vectorstore.as_retriever(
    search_type="mmr",  # Maximum Marginal Relevance
    search_kwargs={"k": 5}
)

chain = (
    {"context": retriever, "question": lambda x: x}
    | prompt
    | ChatOpenAI(model="gpt-4o")
    | StrOutputParser()
)

# Invoke
answer = chain.invoke("What is the capital of France?")
```

### Alternative Frameworks

| Framework | Context7 ID | Best For |
|-----------|-------------|----------|
| **LlamaIndex** | Not in Context7 | RAG-focused, simpler API |
| **Haystack** | Not in Context7 | Enterprise search + generation |
| **Semantic Kernel** | Not in Context7 | Microsoft ecosystem |

**When to Use Alternatives:**
- **LlamaIndex**: Simpler RAG, less orchestration needed
- **Haystack**: Already using Elasticsearch/OpenSearch
- **Semantic Kernel**: .NET/Azure-native stack

---

## Data Versioning

### Critical Update: LakeFS Acquired DVC (November 2025)

**Old Recommendation:** DVC (Data Version Control)
**New Recommendation:** LakeFS (absorbed DVC's team and features)

| Tool | Type | Best For |
|------|------|----------|
| **LakeFS** | Data lake versioning | S3/Azure/GCS object storage |
| **DVC** | Deprecated | Use LakeFS instead |
| **Git LFS** | File versioning | Binary files in Git repos |
| **Pachyderm** | Data pipelines | Data + pipeline versioning |

**LakeFS Benefits:**
- Git-like operations on data lakes (branch, commit, merge)
- Zero-copy operations (instant branches)
- Time travel (revert to any version)
- Data lineage tracking

---

## Frontend Integration Patterns

### ai-chat Skill → RAG Pipeline

```typescript
// Frontend (ai-chat skill)
async function* streamRAGResponse(query: string) {
  const response = await fetch('/api/rag/stream', {
    method: 'POST',
    body: JSON.stringify({ query }),
    headers: { 'Content-Type': 'application/json' }
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    yield decoder.decode(value);
  }
}
```

```python
# Backend (ai-data-engineering skill)
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

app = FastAPI()

@app.post("/api/rag/stream")
async def stream_rag(query: str):
    async def generate():
        chain = RetrievalQA.from_chain_type(
            llm=OpenAI(streaming=True),
            retriever=vectorstore.as_retriever()
        )
        async for chunk in chain.astream(query):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")
```

### search-filter Skill → Semantic Search

```typescript
// Frontend semantic search
async function semanticSearch(query: string, filters: Record<string, any>) {
  const response = await fetch('/api/search/semantic', {
    method: 'POST',
    body: JSON.stringify({ query, filters }),
    headers: { 'Content-Type': 'application/json' }
  });
  return await response.json();
}
```

```python
# Backend semantic search
from qdrant_client import QdrantClient
from langchain.embeddings import VoyageAIEmbeddings

client = QdrantClient(url="http://localhost:6333")
embeddings = VoyageAIEmbeddings(model="voyage-3")

@app.post("/api/search/semantic")
async def semantic_search(query: str, filters: dict):
    query_vector = embeddings.embed_query(query)

    results = client.search(
        collection_name="documents",
        query_vector=query_vector,
        query_filter=filters,  # Metadata filtering
        limit=10,
        with_payload=True
    )

    return {"results": results}
```

---

## Skill Structure

```
ai-data-engineering/
├── init.md                           # This file - master plan
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── rag-architecture.md           # Complete RAG pipeline guide
│   ├── chunking-strategies.md        # Token sizes, overlap, semantic
│   ├── embedding-models.md           # Provider comparison, benchmarks
│   ├── langchain-patterns.md         # LangChain 0.3+ patterns
│   ├── llamaindex-patterns.md        # Alternative to LangChain
│   ├── feature-stores.md             # Feast, Tecton, Hopsworks
│   ├── orchestration-tools.md        # Dagster, Prefect, Airflow 3.0
│   ├── ragas-evaluation.md           # Metrics, implementation
│   ├── vector-databases.md           # Qdrant, Pinecone, pgvector
│   └── data-versioning.md            # LakeFS (post-DVC acquisition)
├── scripts/
│   ├── evaluate_rag.py               # RAGAS evaluation runner (TOKEN-FREE)
│   ├── chunk_documents.py            # Smart chunking with overlap
│   ├── benchmark_retrieval.py        # Measure retrieval quality
│   ├── validate_embeddings.py        # Check embedding quality
│   └── setup_qdrant.py               # Qdrant collection setup
├── examples/
│   ├── langchain-rag/
│   │   ├── basic_rag.py              # Simple RAG chain
│   │   ├── streaming_rag.py          # Streaming responses
│   │   ├── hybrid_search.py          # Vector + BM25
│   │   └── rag_with_filters.py       # Metadata filtering
│   ├── llamaindex-agents/
│   │   ├── query_engine.py           # LlamaIndex query engine
│   │   └── chat_engine.py            # Conversational RAG
│   ├── feast-features/
│   │   ├── feature_repo/             # Feast repository
│   │   ├── feature_views.py          # Feature definitions
│   │   └── serving.py                # Online/offline serving
│   └── dagster-pipelines/
│       ├── embedding_pipeline.py     # Document → embeddings
│       ├── feature_pipeline.py       # Feature engineering
│       └── evaluation_pipeline.py    # RAGAS evaluation
└── assets/
    ├── rag-pipeline-diagram.svg      # Visual architecture
    ├── ragas-metrics-dashboard.json  # Grafana dashboard
    └── langchain-templates/
        ├── basic_rag_template.py
        └── agent_template.py
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: ai-data-engineering
description: Data pipelines, feature stores, and RAG architectures for AI/ML systems. Use when building RAG pipelines, semantic search, chatbots, ML feature serving, or data transformations for LLMs. Covers LangChain orchestration, RAG architecture (chunking, embedding, retrieval, generation, evaluation with RAGAS), feature stores (Feast, Tecton, Hopsworks), vector databases (Qdrant, Pinecone, pgvector), embedding models (Voyage AI, OpenAI, Cohere), orchestration tools (Dagster, Prefect, Airflow 3.0, dbt), and data versioning (LakeFS).
---
```

---

## Quality Checklist

### Before Finalizing init.md:

- [x] Strategic positioning clearly articulated
- [x] Complete RAG architecture diagram (5 layers)
- [x] LangChain as primary recommendation with Context7 IDs
- [x] All Context7 library entries from UNIFIED doc included
- [x] RAGAS evaluation metrics explained with formulas
- [x] Feature store comparison table
- [x] Orchestration tools decision framework
- [x] Chunking strategies with token recommendations
- [x] Embedding models with MTEB scores
- [x] LakeFS note (DVC acquisition November 2025)
- [x] Frontend integration patterns (ai-chat, search-filter)
- [x] Token-free scripts designed (evaluate_rag.py, etc.)
- [x] Multi-language support considered (Python primary)

### Before Creating SKILL.md:

- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure to references
- [ ] Working code examples in examples/
- [ ] Scripts executable without context loading
- [ ] YAML frontmatter validated
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Decision frameworks use ASCII diagrams

### Before Production:

- [ ] Tested with RAG pipeline implementation
- [ ] RAGAS evaluation script validated
- [ ] LangChain patterns verified with v0.3+
- [ ] Vector database integration tested
- [ ] Feature store example working
- [ ] Orchestration pipeline functional
- [ ] Documentation complete and accurate

---

## Implementation Priority

### Phase 1: Core RAG (Week 1-2)
1. Basic RAG pipeline with LangChain
2. Qdrant integration
3. Chunking strategies
4. Embedding generation

### Phase 2: Evaluation (Week 2-3)
1. RAGAS metrics implementation
2. Evaluation scripts
3. Quality monitoring
4. Performance benchmarking

### Phase 3: Orchestration (Week 3-4)
1. Dagster pipeline setup
2. Automated embedding updates
3. Feature store integration
4. Data versioning with LakeFS

### Phase 4: Advanced Patterns (Week 4+)
1. Hybrid search (vector + BM25)
2. Re-ranking with Cohere
3. Multi-query retrieval
4. Agent-based retrieval

---

## Research Notes

### Voyage AI Superiority (December 2025)

Voyage AI's voyage-3 model scores **9.74% better** than OpenAI's text-embedding-3-large on retrieval benchmarks:

| Benchmark | Voyage-3 | OpenAI-3-large | Δ |
|-----------|----------|----------------|---|
| MTEB Retrieval | 69.0 | 64.6 | +6.8% |
| BEIR | 55.3 | 50.4 | +9.7% |
| ArguAna | 72.1 | 65.8 | +9.6% |

**When to use OpenAI anyway:**
- Already in OpenAI ecosystem (GPT-4 + embeddings)
- Need 3072 dimensions (vs 1024 for Voyage)
- Enterprise SLA requirements

### LangChain vs LlamaIndex (December 2025)

| Aspect | LangChain | LlamaIndex |
|--------|-----------|------------|
| **Use Case** | General orchestration | RAG-focused |
| **Complexity** | Higher learning curve | Simpler for RAG |
| **Flexibility** | More customizable | More opinionated |
| **Ecosystem** | Larger (100+ integrations) | Growing (50+ integrations) |
| **Documentation** | 24,215 snippets (Context7) | Not in Context7 |
| **Performance** | v0.3+ much faster | Generally faster |

**Recommendation:** Start with LangChain for comprehensive projects, use LlamaIndex for RAG-only applications.

### Airflow 3.0 Event-Driven Architecture (2025)

Airflow 3.0 (released 2025) introduces event-driven workflows:
- Trigger DAGs from external events (S3 uploads, Kafka messages)
- Reactive scheduling (not just time-based)
- Better for real-time embedding updates

**Migration Note:** Airflow 2.x DAGs are mostly compatible but may need updates for event triggers.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created with complete RAG architecture |

---

*Document Status: Planning Phase - Ready for SKILL.md implementation*
