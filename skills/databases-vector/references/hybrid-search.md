# Hybrid Search: Vector + Keyword (BM25)

Combine vector similarity search with keyword matching for superior retrieval quality in RAG systems.

## Why Hybrid Search

**Problem with vector-only search:**
- Misses exact keyword matches
- Poor with acronyms/proper nouns
- Struggles with rare terms

**Problem with keyword-only search (BM25):**
- No semantic understanding
- Fails on paraphrases
- No concept of meaning similarity

**Solution: Hybrid = Vector + BM25**
- Vector captures semantic meaning
- BM25 ensures exact matches
- Combined provides best retrieval quality

## Architecture

```
User Query: "OAuth refresh token implementation"
           │
    ┌──────┴──────┐
    │             │
Vector Search   BM25 Search
(Semantic)      (Keyword)
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

---

## Qdrant Implementation

### Enable Hybrid Search

```python
from qdrant_client import QdrantClient, models

client = QdrantClient("localhost", port=6333)

# Create collection with BM25 support
client.create_collection(
    collection_name="documents",
    vectors_config=models.VectorParams(
        size=1024,
        distance=models.Distance.COSINE
    ),
    # Enable BM25 indexing
    sparse_vectors_config={
        "text": models.SparseVectorParams(
            modifier=models.Modifier.IDF
        )
    }
)
```

### Insert Documents with BM25

```python
from qdrant_client.models import PointStruct, SparseVector
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def create_bm25_vector(text: str) -> SparseVector:
    """Tokenize text for BM25"""
    tokens = tokenizer.encode(text)
    # Create sparse vector (token_id -> frequency)
    token_counts = {}
    for token in tokens:
        token_counts[token] = token_counts.get(token, 0) + 1

    return SparseVector(
        indices=list(token_counts.keys()),
        values=list(token_counts.values())
    )

# Insert with dense + sparse vectors
points = [
    PointStruct(
        id=1,
        vector={
            "dense": dense_embedding,  # From OpenAI/Voyage
            "text": create_bm25_vector(chunk_text)  # BM25 tokens
        },
        payload={"text": chunk_text, "source": "docs/auth.md"}
    )
]

client.upsert(collection_name="documents", points=points)
```

### Hybrid Search Query

```python
def hybrid_search(query: str, limit: int = 5):
    # 1. Get query embeddings
    query_dense = get_embedding(query)  # OpenAI/Voyage API
    query_sparse = create_bm25_vector(query)

    # 2. Hybrid search with fusion
    results = client.query_points(
        collection_name="documents",
        prefetch=[
            # Vector search (top 20)
            models.Prefetch(
                query=query_dense,
                using="dense",
                limit=20
            ),
            # BM25 search (top 20)
            models.Prefetch(
                query=query_sparse,
                using="text",
                limit=20
            )
        ],
        # Reciprocal Rank Fusion
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=limit
    )

    return results.points
```

---

## Reciprocal Rank Fusion (RRF)

### Formula

For each document in results:
```
RRF_score = Σ (1 / (k + rank_i))
```

Where:
- `k` = constant (typically 60)
- `rank_i` = rank in result set i (1-indexed)

### Example

Document appears in:
- Vector search: rank 3
- BM25 search: rank 1

```python
rrf_score = 1/(60+3) + 1/(60+1) = 0.0159 + 0.0164 = 0.0323
```

Higher score = better match.

### Manual RRF Implementation

```python
from collections import defaultdict

def reciprocal_rank_fusion(
    vector_results: List[tuple],  # (doc_id, score)
    bm25_results: List[tuple],
    k: int = 60
) -> List[tuple]:
    """Combine results using RRF"""

    rrf_scores = defaultdict(float)

    # Add vector search scores
    for rank, (doc_id, _) in enumerate(vector_results, start=1):
        rrf_scores[doc_id] += 1 / (k + rank)

    # Add BM25 scores
    for rank, (doc_id, _) in enumerate(bm25_results, start=1):
        rrf_scores[doc_id] += 1 / (k + rank)

    # Sort by RRF score
    sorted_results = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_results
```

---

## LangChain Integration

```python
from langchain_qdrant import QdrantVectorStore
from langchain_voyageai import VoyageAIEmbeddings
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# 1. Vector retriever
embeddings = VoyageAIEmbeddings(model="voyage-3")
vector_store = QdrantVectorStore(
    client=client,
    collection_name="documents",
    embedding=embeddings
)
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 10})

# 2. BM25 retriever
documents = load_all_documents()
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 10

# 3. Ensemble (hybrid) retriever
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.5, 0.5],  # Equal weighting
    c=60  # RRF constant
)

# 4. Use in RAG chain
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=ensemble_retriever,
    return_source_documents=True
)

result = qa_chain({"query": "How do I refresh OAuth tokens?"})
```

---

## Performance Comparison

**Benchmark (MTEB retrieval tasks):**

| Method | Recall@5 | Recall@10 | Latency |
|--------|----------|-----------|---------|
| Vector only | 0.72 | 0.81 | 10ms |
| BM25 only | 0.65 | 0.75 | 5ms |
| **Hybrid (RRF)** | **0.84** | **0.91** | 15ms |

**Conclusion:** Hybrid provides 12-point recall improvement at minimal latency cost.

---

## When to Use Hybrid

✅ **Use hybrid when:**
- Queries contain acronyms (OAuth, JWT, API)
- Proper nouns matter (company names, product names)
- Exact keyword matches are critical
- Domain-specific terminology

❌ **Skip hybrid when:**
- Pure conversational queries
- Latency budget <10ms
- Documents are short (<100 tokens)

---

## Advanced: Re-Ranking

Add a second stage re-ranker for even better results.

### Cohere Re-Rank

```python
import cohere

co = cohere.Client(api_key="your-key")

# 1. Hybrid search (top 20)
candidates = hybrid_search(query, limit=20)

# 2. Re-rank with Cohere
reranked = co.rerank(
    query=query,
    documents=[c.payload["text"] for c in candidates],
    model="rerank-english-v3.0",
    top_n=5
)

# 3. Final top 5 results
top_docs = [candidates[r.index] for r in reranked.results]
```

### Cross-Encoder Re-Ranking (Self-Hosted)

```python
from sentence_transformers import CrossEncoder

model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

# Score query-document pairs
pairs = [(query, doc.payload["text"]) for doc in candidates]
scores = model.predict(pairs)

# Sort by score
reranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
top_docs = [doc for doc, score in reranked[:5]]
```

---

## Implementation Checklist

- [ ] Vector embeddings configured (Voyage/OpenAI)
- [ ] BM25 indexing enabled (Qdrant sparse vectors)
- [ ] Query tokenization matches document tokenization
- [ ] RRF fusion configured (k=60 default)
- [ ] Tested on representative queries
- [ ] Optional: Re-ranking layer added
- [ ] Latency monitored (<50ms target)
- [ ] Recall metrics tracked (>0.80 target)

---

## Troubleshooting

**Poor hybrid performance:**
1. Check tokenization consistency (query vs documents)
2. Tune RRF k parameter (try 30-90 range)
3. Adjust vector/BM25 weights (try 0.6/0.4 or 0.4/0.6)
4. Ensure BM25 index is built correctly
5. Add re-ranking stage if needed

**Slow queries:**
1. Reduce prefetch limits (20 → 10)
2. Use query filters to reduce search space
3. Cache frequent queries
4. Consider separate BM25 index (not Qdrant)

---

## Resources

- Qdrant Hybrid Search: https://qdrant.tech/documentation/concepts/hybrid-queries/
- RRF Paper: https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
- Cohere Re-Rank: https://cohere.com/rerank
