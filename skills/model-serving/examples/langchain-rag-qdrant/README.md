# LangChain RAG with Qdrant

Complete RAG (Retrieval-Augmented Generation) pipeline using LangChain and Qdrant vector database.

## Files

- `basic_rag.py` - Simple RAG chain
- `streaming_rag.py` - Streaming responses with SSE
- `hybrid_search.py` - Vector + BM25 hybrid search
- `requirements.txt` - Python dependencies

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# 3. Set API keys
export OPENAI_API_KEY="your-key"
export VOYAGE_API_KEY="your-key"  # Optional, for better embeddings

# 4. Run examples
python basic_rag.py
python streaming_rag.py
```

## Architecture

```
User Query
    ↓
Embedding (Voyage AI / OpenAI)
    ↓
Vector Search (Qdrant)
    ↓
Context + Query → LLM (OpenAI / vLLM)
    ↓
Streaming Response
```

## Key Features

- **Chunking:** 512 tokens with 50-token overlap
- **Embeddings:** Voyage AI voyage-3 (1024d)
- **Vector DB:** Qdrant with hybrid search
- **LLM:** OpenAI GPT-4 or self-hosted vLLM
- **Streaming:** Server-Sent Events (SSE)

See individual Python files for detailed implementation.
