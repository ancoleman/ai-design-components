# Qdrant Python RAG Pipeline Example

Complete implementation of a production-ready RAG (Retrieval-Augmented Generation) pipeline using Qdrant, LangChain, and OpenAI.

## Features

- Document ingestion with semantic chunking
- Hybrid search (vector + BM25 keyword)
- Metadata filtering
- RAGAS evaluation
- FastAPI REST API
- Docker Compose deployment

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- OpenAI API key

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Running with Docker Compose

```bash
# Start Qdrant
docker-compose up -d

# Run the application
python main.py
```

## Project Structure

```
qdrant-python/
├── main.py              # FastAPI application
├── rag_pipeline.py      # RAG implementation
├── document_loader.py   # Document ingestion
├── evaluation.py        # RAGAS evaluation
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Qdrant deployment
├── .env.example         # Environment template
└── README.md            # This file
```

## API Endpoints

### Ingest Documents
```bash
POST /ingest
{
  "file_path": "path/to/document.md",
  "metadata": {
    "source_type": "documentation",
    "product_version": "v2.0"
  }
}
```

### Search
```bash
POST /search
{
  "query": "How do I implement OAuth refresh tokens?",
  "limit": 5,
  "filter": {
    "source_type": "documentation"
  }
}
```

### Generate Answer (RAG)
```bash
POST /generate
{
  "query": "Explain OAuth refresh tokens",
  "limit": 5
}
```

## Usage Example

```python
from rag_pipeline import RAGPipeline

# Initialize
rag = RAGPipeline(
    qdrant_url="localhost",
    collection_name="documents",
    embedding_model="text-embedding-3-large"
)

# Ingest documents
rag.ingest_document(
    file_path="docs/api-reference.md",
    metadata={"source": "api-docs"}
)

# Search
results = rag.search(
    query="OAuth implementation",
    limit=5,
    filter={"source": "api-docs"}
)

# Generate answer
answer = rag.generate_answer(
    query="How do I implement OAuth?",
    limit=5
)
print(answer)
```

## Evaluation

Run RAGAS evaluation:

```bash
python evaluation.py
```

Metrics:
- Faithfulness: >0.90 (minimal hallucination)
- Answer Relevancy: >0.85 (addresses query)
- Context Recall: >0.80 (sufficient context)
- Context Precision: >0.75 (minimal noise)

## Configuration

Edit `.env`:

```bash
# OpenAI API Key
OPENAI_API_KEY=your-api-key-here

# Qdrant Configuration
QDRANT_URL=localhost
QDRANT_PORT=6333

# Embedding Model
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSIONS=1024

# Chunking Strategy
CHUNK_SIZE=512
CHUNK_OVERLAP=50

# LLM Configuration
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.1
```

## Production Deployment

1. Enable Qdrant authentication
2. Set up TLS/HTTPS
3. Configure rate limiting
4. Add monitoring (Prometheus/Grafana)
5. Set up backups
6. Use managed Qdrant Cloud for high availability

## Troubleshooting

**Issue:** Qdrant connection fails
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# View logs
docker logs qdrant
```

**Issue:** Poor retrieval quality
- Adjust chunking strategy (chunk size, overlap)
- Try hybrid search instead of vector-only
- Add metadata filtering
- Implement re-ranking

**Issue:** High costs
- Switch to text-embedding-3-small
- Implement semantic caching
- Reduce chunk overlap
- Use self-hosted embeddings

## License

MIT
