# LangChain RAG Examples

Complete working examples of RAG pipelines using LangChain 0.3+.

## Setup

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Set environment variables:**

Create `.env` file:

```bash
# Required
OPENAI_API_KEY=your-openai-key
VOYAGE_API_KEY=your-voyage-key  # Optional, for best embedding quality

# Optional (defaults to localhost)
QDRANT_URL=http://localhost:6333
```

3. **Start Qdrant (local):**

```bash
docker run -p 6333:6333 qdrant/qdrant
```

## Examples

### 1. Basic RAG (`basic_rag.py`)

Simplest production RAG implementation:

```bash
python basic_rag.py
```

**Features:**
- Document loading
- Chunking (512 tokens, 50 overlap)
- Embedding generation (Voyage AI or OpenAI)
- Vector storage (Qdrant)
- Retrieval + generation

### 2. Streaming RAG (`streaming_rag.py`)

RAG with streaming responses:

```bash
python streaming_rag.py
```

**Features:**
- All basic RAG features
- Streaming LLM responses
- Better UX for long answers
- FastAPI endpoint included

### 3. Hybrid Search (`hybrid_search.py`)

Combines vector and keyword search:

```bash
python hybrid_search.py
```

**Features:**
- Vector search (semantic)
- BM25 search (keyword)
- Ensemble retrieval (70% vector, 30% keyword)
- Better recall and precision

## Usage Patterns

### Quick Start

```python
from langchain_qdrant import QdrantVectorStore
from langchain_voyageai import VoyageAIEmbeddings
from qdrant_client import QdrantClient

# Initialize
client = QdrantClient(url="http://localhost:6333")
embeddings = VoyageAIEmbeddings(model="voyage-3")

vectorstore = QdrantVectorStore(
    client=client,
    collection_name="docs",
    embedding=embeddings
)

# Add documents
vectorstore.add_documents(documents)

# Query
results = vectorstore.similarity_search("What is machine learning?", k=5)
```

### Production Deployment

See `streaming_rag.py` for FastAPI integration:

```bash
# Start server
uvicorn streaming_rag:app --reload

# Query
curl -X POST http://localhost:8000/api/rag/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

## File Descriptions

- `basic_rag.py` - Complete RAG implementation (150 lines)
- `streaming_rag.py` - Streaming + FastAPI (200 lines)
- `hybrid_search.py` - Vector + BM25 hybrid (180 lines)
- `requirements.txt` - All dependencies
- `README.md` - This file

## Troubleshooting

**Error: "Collection not found"**
- Run `python basic_rag.py` first to create collection
- Or create manually in Qdrant

**Error: "No API key provided"**
- Set `OPENAI_API_KEY` and `VOYAGE_API_KEY` in `.env`

**Slow responses:**
- Use `text-embedding-3-small` instead of `voyage-3` for development
- Reduce `k` (retrieve fewer chunks)

**Poor quality:**
- Increase chunk overlap (50 → 100)
- Try hybrid search
- Add re-ranking
