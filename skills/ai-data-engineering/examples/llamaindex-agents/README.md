# LlamaIndex RAG Example

LlamaIndex alternative to LangChain with simpler API for RAG-focused applications.

## Setup

```bash
pip install -r requirements.txt
```

Create `.env`:

```bash
OPENAI_API_KEY=your-key
VOYAGE_API_KEY=your-key  # Optional
QDRANT_URL=http://localhost:6333
```

## When to Use LlamaIndex vs LangChain

**Use LlamaIndex when:**
- Building pure RAG applications
- Want simpler API
- Don't need complex agent orchestration
- Prefer opinionated defaults

**Use LangChain when:**
- Need general LLM orchestration
- Building complex agent workflows
- Want more control and flexibility
- Need extensive integrations

## Examples

### Query Engine (`query_engine.py`)

Simple RAG query engine:

```bash
python query_engine.py
```

Features:
- Automatic chunking
- Simplified indexing
- Built-in query optimization

## File Descriptions

- `query_engine.py` - Basic LlamaIndex RAG (100 lines)
- `requirements.txt` - Dependencies
- `README.md` - This file
