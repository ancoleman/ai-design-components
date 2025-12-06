# Hybrid Search Example (Vector + BM25)

Python implementation of hybrid search combining vector similarity and BM25 keyword matching with Reciprocal Rank Fusion.

## Features

- Vector similarity search (semantic)
- BM25 keyword search (exact matching)
- Reciprocal Rank Fusion (RRF) for result merging
- Qdrant hybrid search implementation
- Performance comparison (vector-only vs. keyword-only vs. hybrid)

## Prerequisites

- Python 3.10+
- Qdrant running (Docker or managed)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from hybrid_search import HybridSearchEngine

# Initialize
engine = HybridSearchEngine(
    qdrant_url="localhost",
    collection_name="documents"
)

# Hybrid search
results = engine.search(
    query="OAuth refresh token implementation",
    limit=5
)

for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"Text: {result['text'][:100]}...")
    print()
```

## Running

```bash
# Run example
python hybrid_search_example.py

# Run comparison benchmark
python compare_search_methods.py
```

## How Hybrid Search Works

```
User Query: "OAuth refresh tokens"
           │
    ┌──────┴──────┐
    │             │
Vector Search   Keyword Search
(Semantic)      (BM25)
    │             │
Top 20 docs   Top 20 docs
    │             │
    └──────┬──────┘
           │
   Reciprocal Rank Fusion
   (Merge + Re-rank)
           │
    Final Top 5 Results
```

## Benefits of Hybrid Search

- **Vector search:** Captures semantic meaning ("refresh" ≈ "renewal")
- **Keyword search:** Ensures exact matches aren't missed ("refresh_token" literal)
- **Combined:** Best retrieval quality

## Project Structure

```
hybrid-search/
├── hybrid_search.py              # Main implementation
├── hybrid_search_example.py      # Usage example
├── compare_search_methods.py     # Benchmark comparison
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

See individual files for implementation details.
