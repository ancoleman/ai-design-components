# RAG Pipeline Architecture

Complete guide to the 5-stage RAG pipeline with implementation patterns.

## Table of Contents

- [Overview](#overview)
- [Stage 1: Ingestion](#stage-1-ingestion)
- [Stage 2: Indexing](#stage-2-indexing)
- [Stage 3: Retrieval](#stage-3-retrieval)
- [Stage 4: Generation](#stage-4-generation)
- [Stage 5: Evaluation](#stage-5-evaluation)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## Overview

RAG (Retrieval-Augmented Generation) grounds LLMs in domain-specific knowledge through 5 distinct stages:

```
Documents → Chunks → Embeddings → Vector DB → Retrieval → LLM → Response
    ↓          ↓          ↓           ↓           ↓        ↓        ↓
INGESTION  INDEXING   INDEXING   INDEXING   RETRIEVAL  GENERATION  EVALUATION
```

## Stage 1: Ingestion

Load documents from various sources and formats.

### Supported Formats

| Format | Loader | Best For |
|--------|--------|----------|
| **PDF** | `PyPDFLoader` | Research papers, reports |
| **DOCX** | `Docx2txtLoader` | Business documents |
| **Markdown** | `UnstructuredMarkdownLoader` | Technical documentation |
| **HTML** | `BeautifulSoupLoader` | Web pages, wikis |
| **Code** | `TextLoader` | Source code repositories |

### Implementation

```python
from langchain.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)

# PDF documents
pdf_loader = PyPDFLoader("document.pdf")
pdf_docs = pdf_loader.load()

# Markdown documentation
md_loader = UnstructuredMarkdownLoader("README.md")
md_docs = md_loader.load()

# Add metadata
for doc in pdf_docs:
    doc.metadata["source"] = "research_papers"
    doc.metadata["category"] = "ml_research"
    doc.metadata["date"] = "2025-12-01"
```

### Metadata Best Practices

Always include metadata for filtering during retrieval:

```python
metadata = {
    "source": str,        # Original file path
    "title": str,         # Document title
    "category": str,      # Classification
    "date": str,          # Creation/update date (ISO format)
    "author": str,        # Author name
    "tags": List[str]     # Searchable tags
}
```

## Stage 2: Indexing

Split documents into chunks, generate embeddings, and store in vector database.

### Chunking

**Default Strategy: Fixed Token**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,              # Default recommended size
    chunk_overlap=50,            # Prevent boundary information loss
    length_function=len,         # Use token count
    separators=["\n\n", "\n", " ", ""]  # Split on natural boundaries
)

chunks = splitter.split_documents(documents)
```

**Code-Aware Strategy:**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python",
    chunk_size=512,
    chunk_overlap=50
)

# Preserves function/class boundaries
code_chunks = code_splitter.split_documents(code_documents)
```

**Semantic Strategy:**

```python
from langchain.text_splitter import SemanticChunker
from langchain_voyageai import VoyageAIEmbeddings

semantic_splitter = SemanticChunker(
    embeddings=VoyageAIEmbeddings(model="voyage-3"),
    breakpoint_threshold_type="percentile"  # Split at meaning boundaries
)

semantic_chunks = semantic_splitter.split_documents(documents)
```

### Embedding Generation

**Production: Voyage AI**

```python
from langchain_voyageai import VoyageAIEmbeddings

embeddings = VoyageAIEmbeddings(
    model="voyage-3",
    voyage_api_key="your-api-key",
    batch_size=128  # Batch for performance
)

vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
```

**Development: OpenAI**

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # 5x cheaper than voyage-3
    openai_api_key="your-api-key"
)
```

### Vector Database Storage

**Qdrant (Recommended):**

```python
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore

# Initialize client
client = QdrantClient(url="http://localhost:6333")

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=models.VectorParams(
        size=1024,  # Voyage-3 dimension
        distance=models.Distance.COSINE
    )
)

# Index documents
vectorstore = QdrantVectorStore(
    client=client,
    collection_name="documents",
    embedding=embeddings
)

vectorstore.add_documents(chunks)
```

**pgvector (PostgreSQL Shops):**

```python
from langchain_postgres import PGVector

vectorstore = PGVector(
    connection_string="postgresql://user:pass@localhost:5432/db",
    collection_name="documents",
    embedding_function=embeddings
)

vectorstore.add_documents(chunks)
```

## Stage 3: Retrieval

Query the vector database and return most relevant chunks.

### Basic Vector Search

```python
from langchain_qdrant import QdrantVectorStore

vectorstore = QdrantVectorStore(
    client=client,
    collection_name="documents",
    embedding=embeddings
)

# Simple retrieval
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}  # Return top 5 chunks
)

results = retriever.get_relevant_documents("What is the capital of France?")
```

### Maximum Marginal Relevance (MMR)

Returns diverse results, not just similar ones:

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,  # Fetch 20, return diverse 5
        "lambda_mult": 0.5  # Balance relevance vs diversity
    }
)
```

### Hybrid Search (Vector + BM25)

Combines semantic search with keyword matching:

```python
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever

# Vector retriever
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# BM25 keyword retriever
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

# Ensemble with weights
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.7, 0.3]  # 70% vector, 30% keyword
)

results = ensemble_retriever.get_relevant_documents("machine learning algorithms")
```

### Metadata Filtering

Filter by document properties:

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Filter by category and date
search_filter = Filter(
    must=[
        FieldCondition(
            key="category",
            match=MatchValue(value="ml_research")
        ),
        FieldCondition(
            key="date",
            range={"gte": "2024-01-01"}
        )
    ]
)

results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=search_filter,
    limit=5
)
```

### Re-Ranking

Improve precision with cross-encoder re-ranking:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Base retriever (fetch 20 candidates)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

# Cohere re-ranker (return best 5)
compressor = CohereRerank(
    model="rerank-english-v3.0",
    top_n=5
)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

results = compression_retriever.get_relevant_documents("machine learning")
```

## Stage 4: Generation

Inject retrieved context into LLM prompt and generate response.

### Basic RAG Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:

{context}

Question: {question}

If the answer is not in the context, say "I don't have enough information to answer this question."
""")

# LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,  # Factual responses
    streaming=True    # Better UX
)

# Build chain
chain = (
    {"context": retriever, "question": lambda x: x}
    | prompt
    | llm
    | StrOutputParser()
)

# Invoke
answer = chain.invoke("What is machine learning?")
```

### Streaming Responses

Essential for good UX:

```python
# Streaming
for chunk in chain.stream("What is machine learning?"):
    print(chunk, end="", flush=True)
```

### Citation Extraction

Link answers to source documents:

```python
from langchain.chains import RetrievalQAWithSourcesChain

chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

result = chain({"question": "What is machine learning?"})
print(result["answer"])
print("\nSources:")
for doc in result["source_documents"]:
    print(f"- {doc.metadata['source']}")
```

## Stage 5: Evaluation

Measure RAG quality with RAGAS metrics.

### RAGAS Metrics

| Metric | Formula | Good Score |
|--------|---------|------------|
| **Faithfulness** | Verified claims / Total claims | > 0.8 |
| **Answer Relevancy** | Semantic similarity to query | > 0.7 |
| **Context Precision** | Relevant chunks / Total chunks | > 0.6 |
| **Context Recall** | Retrieved info / Required info | > 0.7 |

### Implementation

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# Evaluation dataset
eval_data = {
    "question": [
        "What is the capital of France?",
        "Who wrote Pride and Prejudice?"
    ],
    "answer": [
        "Paris is the capital of France.",
        "Jane Austen wrote Pride and Prejudice."
    ],
    "contexts": [
        ["France's capital city is Paris, located in the north-central part of the country."],
        ["Pride and Prejudice is a novel by Jane Austen, published in 1813."]
    ],
    "ground_truth": [
        "Paris",
        "Jane Austen"
    ]
}

dataset = Dataset.from_dict(eval_data)

# Evaluate
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

print(f"Faithfulness: {result['faithfulness']:.2f}")
print(f"Answer Relevancy: {result['answer_relevancy']:.2f}")
print(f"Context Precision: {result['context_precision']:.2f}")
print(f"Context Recall: {result['context_recall']:.2f}")
```

### Continuous Evaluation

Run evaluations on every pipeline change:

```python
# Track metrics over time
import json
from datetime import datetime

metrics = {
    "timestamp": datetime.now().isoformat(),
    "pipeline_version": "v1.2.0",
    "embedding_model": "voyage-3",
    "chunk_size": 512,
    "results": {
        "faithfulness": result['faithfulness'],
        "answer_relevancy": result['answer_relevancy'],
        "context_precision": result['context_precision'],
        "context_recall": result['context_recall']
    }
}

with open("metrics_history.jsonl", "a") as f:
    f.write(json.dumps(metrics) + "\n")
```

## Production Deployment

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Production RAG Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (ai-chat)                                          │
│    ↓                                                         │
│  API Gateway (FastAPI)                                       │
│    ↓                                                         │
│  LangChain Orchestration                                     │
│    ↓                                                         │
│  Vector DB (Qdrant Cluster)                                  │
│    ↓                                                         │
│  Embedding Pipeline (Dagster)                                │
│    ↓                                                         │
│  Observability (OpenLLMetry + Grafana)                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### FastAPI Backend

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str
    filters: dict = {}

@app.post("/api/rag/stream")
async def stream_rag(query: Query):
    try:
        async def generate():
            async for chunk in chain.astream(query.question):
                yield chunk

        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag/query")
async def query_rag(query: Query):
    try:
        result = chain.invoke(query.question)
        return {"answer": result, "sources": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Caching

Reduce costs and latency with semantic caching:

```python
from langchain.cache import RedisSemanticCache
from langchain.globals import set_llm_cache

set_llm_cache(RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=embeddings,
    score_threshold=0.95  # Cache hit threshold
))
```

### Monitoring

Track LLM calls with OpenLLMetry:

```python
from traceloop.sdk import Traceloop

Traceloop.init(
    app_name="rag_pipeline",
    api_endpoint="http://localhost:4318"
)

# Automatic tracing of LangChain calls
```

## Troubleshooting

### Poor Retrieval Quality

**Symptoms:** Low context precision/recall, irrelevant chunks retrieved

**Solutions:**
1. Reduce chunk size (try 256 tokens)
2. Increase overlap (100 tokens)
3. Use hybrid search (vector + BM25)
4. Add re-ranking with Cohere
5. Try semantic chunking

### Slow Response Times

**Symptoms:** >3s response time, timeout errors

**Solutions:**
1. Reduce k (retrieve 3 chunks instead of 5)
2. Implement semantic caching
3. Use async embedding APIs
4. Add Redis caching layer
5. Use cheaper/faster embedding model for development

### High LLM Costs

**Symptoms:** Unexpected API bills

**Solutions:**
1. Reduce retrieved chunks (k=3)
2. Use GPT-4o-mini instead of GPT-4o
3. Implement semantic caching
4. Deduplicate retrieved chunks
5. Use streaming (prevents re-generation on errors)

### Hallucinations

**Symptoms:** Low faithfulness scores, answers not grounded in context

**Solutions:**
1. Use temperature=0.0 (more deterministic)
2. Improve prompt: "Answer ONLY based on context"
3. Add hallucination detection post-processing
4. Increase number of retrieved chunks
5. Use better embedding model (Voyage AI)

### Memory Issues

**Symptoms:** OOM errors during batch embedding

**Solutions:**
1. Reduce batch size (128 → 64)
2. Use streaming embedding APIs
3. Process documents in batches
4. Use smaller embedding model dimensions
5. Clear cache between batches
