---
sidebar_position: 12
title: AI Data Engineering
description: Data pipelines, feature stores, and embedding generation for AI/ML systems
tags: [backend, ai, ml, rag, embeddings, pipelines]
---

# AI Data Engineering

Build data infrastructure for AI/ML systems including RAG pipelines, feature stores, and embedding generation. Provides architecture patterns, orchestration workflows, and evaluation metrics for production AI applications.

## When to Use

Use when:
- Building RAG (Retrieval-Augmented Generation) pipelines
- Implementing semantic search or vector databases
- Setting up ML feature stores for real-time serving
- Creating embedding generation pipelines
- Evaluating RAG quality with RAGAS metrics
- Orchestrating data workflows for AI systems

Skip if:
- Building traditional CRUD applications (use databases-relational)
- Simple key-value storage (use databases-nosql)
- No AI/ML components in the application

## Multi-Language Support

This skill provides patterns for:
- **Python**: LangChain, LlamaIndex, Feast, Dagster (primary for AI/ML)
- **TypeScript**: LangChain.js (frontend integration)
- All languages: API consumption of AI services

## RAG Pipeline Architecture

RAG pipelines have 5 distinct stages:

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline (5 Stages)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. INGESTION → Load documents (PDF, DOCX, Markdown)        │
│  2. INDEXING → Chunk (512 tokens) + Embed + Store           │
│  3. RETRIEVAL → Query embedding + Vector search + Filters   │
│  4. GENERATION → Context injection + LLM streaming          │
│  5. EVALUATION → RAGAS metrics (faithfulness, relevancy)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Chunking Strategies

Chunking is the most critical decision for RAG quality. Poor chunking breaks retrieval.

**Default Recommendation:**
- **Size:** 512 tokens
- **Overlap:** 50-100 tokens
- **Method:** Fixed token-based

**Why these values:**
- Too small (under 256 tokens): Loses context, requires many retrievals
- Too large (over 1024 tokens): Includes irrelevant content, hits token limits
- Overlap prevents information loss at chunk boundaries

**Alternative strategies:**

```python
# Code-aware chunking (preserves functions/classes)
from langchain.text_splitter import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python",
    chunk_size=512,
    chunk_overlap=50
)

# Semantic chunking (splits on meaning, not tokens)
from langchain.text_splitter import SemanticChunker

semantic_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile"
)
```

## Embedding Generation

Embedding quality directly impacts retrieval accuracy.

**Primary Recommendation: Voyage AI voyage-3**
- Dimensions: 1024
- MTEB Score: 69.0 (highest as of Dec 2025)
- Cost: $$$ but 9.74% better than OpenAI
- Use for: Production systems requiring best retrieval quality

**Cost-Effective Alternative: OpenAI text-embedding-3-small**
- Dimensions: 1536
- MTEB Score: 62.3
- Cost: $ (5x cheaper than voyage-3)
- Use for: Development, prototyping, cost-sensitive applications

**Implementation:**

```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# Production (best quality)
embeddings = VoyageAIEmbeddings(
    model="voyage-3",
    voyage_api_key="your-api-key"
)

# Development (cost-effective)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key="your-api-key"
)
```

## RAGAS Evaluation Metrics

Traditional metrics (BLEU, ROUGE) don't measure RAG quality. RAGAS provides LLM-as-judge evaluation.

**4 Core Metrics:**

| Metric | Measures | Good Score |
|--------|----------|------------|
| **Faithfulness** | Factual consistency with retrieved context | > 0.8 |
| **Answer Relevancy** | Does answer address the user's question? | > 0.7 |
| **Context Precision** | Are retrieved chunks actually relevant? | > 0.6 |
| **Context Recall** | Were all necessary chunks retrieved? | > 0.7 |

**Quick evaluation:**

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

dataset = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is the capital of France."],
    "contexts": [["France's capital is Paris."]],
    "ground_truth": ["Paris"]
}

result = evaluate(dataset, metrics=[faithfulness, answer_relevancy])
print(f"Faithfulness: {result['faithfulness']}")
print(f"Answer Relevancy: {result['answer_relevancy']}")
```

## Feature Stores

Feature stores solve the "training-serving skew" problem by providing consistent feature computation.

**Primary Recommendation: Feast** - Open source, works with any backend (PostgreSQL, Redis, DynamoDB, S3, BigQuery, Snowflake)

**Basic usage:**

```python
from feast import FeatureStore
store = FeatureStore(repo_path="feature_repo/")

# Online serving (low-latency)
features = store.get_online_features(
    features=["user_features:total_orders"],
    entity_rows=[{"user_id": 1001}]
).to_dict()
```

## LangChain Orchestration

LangChain is the primary framework for LLM orchestration with the largest ecosystem.

**Basic RAG Chain:**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from langchain_voyageai import VoyageAIEmbeddings

# Setup retriever
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    embedding=VoyageAIEmbeddings(model="voyage-3")
)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# Build chain
prompt = ChatPromptTemplate.from_template(
    "Answer based on context:\n{context}\n\nQuestion: {question}"
)
chain = {"context": retriever, "question": lambda x: x} | prompt | ChatOpenAI() | StrOutputParser()

# Stream response
for chunk in chain.stream("What is the capital of France?"):
    print(chunk, end="", flush=True)
```

## Orchestration Tools

Modern AI pipelines require workflow orchestration beyond cron jobs.

**Primary Recommendation: Dagster (for ML/AI pipelines)**

Asset-centric design, best lineage tracking, perfect for RAG.

**Example: Embedding Pipeline**

```python
from dagster import asset
from langchain_voyageai import VoyageAIEmbeddings

@asset
def raw_documents():
    """Load documents from S3."""
    return documents

@asset
def chunked_documents(raw_documents):
    """Split into 512-token chunks with 50-token overlap."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    return splitter.split_documents(raw_documents)

@asset
def embedded_documents(chunked_documents):
    """Generate embeddings with Voyage AI."""
    embeddings = VoyageAIEmbeddings(model="voyage-3")
    return embeddings.embed_documents([doc.page_content for doc in chunked_documents])
```

## Integration with Frontend Skills

### ai-chat Skill → RAG Backend

The ai-chat skill consumes RAG pipeline outputs for streaming responses.

**Backend API (FastAPI):**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/api/rag/stream")
async def stream_rag(query: str):
    async def generate():
        chain = RetrievalQA.from_chain_type(llm=OpenAI(streaming=True), retriever=vectorstore.as_retriever())
        async for chunk in chain.astream(query):
            yield chunk
    return StreamingResponse(generate(), media_type="text/plain")
```

### search-filter Skill → Semantic Search

The search-filter skill uses semantic search backends for vector similarity.

**Backend (Qdrant + Voyage AI):**

```python
from qdrant_client import QdrantClient
from langchain_voyageai import VoyageAIEmbeddings

@app.post("/api/search/semantic")
async def semantic_search(query: str, filters: dict):
    query_vector = VoyageAIEmbeddings(model="voyage-3").embed_query(query)
    results = QdrantClient().search(
        collection_name="documents",
        query_vector=query_vector,
        query_filter=filters,
        limit=10
    )
    return {"results": results}
```

## Data Versioning

**Primary Recommendation: LakeFS** (acquired DVC team November 2025)

Git-like operations on data lakes: branch, commit, merge, time travel. Works with S3/Azure/GCS.

```python
import lakefs

branch = lakefs.Branch("main").create("experiment-voyage-3")
branch.commit("Updated embeddings to voyage-3")
branch.merge_into("main")
```

## Quick Start Workflow

**1. Set up vector database:**

```bash
python scripts/setup_qdrant.py --collection docs --dimension 1024
```

**2. Chunk and embed documents:**

```bash
python scripts/chunk_documents.py \
  --input data/documents/ \
  --chunk-size 512 \
  --overlap 50 \
  --output data/chunks/
```

**3. Evaluate with RAGAS:**

```bash
python scripts/evaluate_rag.py \
  --dataset data/eval_qa.json \
  --output results/ragas_metrics.json
```

## Troubleshooting

**Common Issues:**

**1. Poor retrieval quality** - Check chunk size (try 512 tokens), increase overlap (50-100), try hybrid search, re-rank with Cohere

**2. Slow embedding generation** - Batch documents (100-1000), use async APIs, cache with Redis, use smaller model for dev

**3. High LLM costs** - Reduce retrieved chunks (k=3), use cheaper re-ranking models, cache frequent queries

## Best Practices

**Chunking:** Default to 512 tokens with 50-token overlap. Use semantic chunking for complex documents. Preserve code structure for source code.

**Embeddings:** Use Voyage AI voyage-3 for production, OpenAI text-embedding-3-small for development. Never mix embedding models (re-embed everything if changing).

**Evaluation:** Run RAGAS metrics on every pipeline change. Maintain test dataset of 50+ question-answer pairs. Track metrics over time.

**Orchestration:** Use Dagster for ML/AI pipelines, dbt for SQL transformations only. Version control all pipeline code.

**Frontend Integration:** Always stream LLM responses. Implement retry logic. Show citations/sources to users. Handle empty results gracefully.

## Related Skills

- [Vector Databases](./databases-vector) - Store and query embeddings
- [Model Serving](./model-serving) - Serve LLMs for RAG generation
- [AI Chat](../frontend/ai-chat) - Frontend chat interface
- [Search & Filter](../frontend/search-filter) - Semantic search UI

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/ai-data-engineering)
- LangChain: https://python.langchain.com/
- LlamaIndex: https://www.llamaindex.ai/
- Feast: https://feast.dev/
- RAGAS: https://docs.ragas.io/
- Dagster: https://dagster.io/
