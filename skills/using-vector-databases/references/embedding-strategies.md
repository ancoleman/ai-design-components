# Embedding Generation Strategies


## Table of Contents

- [Overview](#overview)
- [Embedding Model Comparison (2025)](#embedding-model-comparison-2025)
  - [Quality Benchmark: MTEB (Massive Text Embedding Benchmark)](#quality-benchmark-mteb-massive-text-embedding-benchmark)
- [Managed Embedding APIs](#managed-embedding-apis)
  - [Voyage AI (Highest Quality)](#voyage-ai-highest-quality)
  - [OpenAI (Enterprise Standard)](#openai-enterprise-standard)
  - [OpenAI text-embedding-3-small (Cost-Optimized)](#openai-text-embedding-3-small-cost-optimized)
  - [Cohere (Multilingual Leader)](#cohere-multilingual-leader)
  - [Google text-embedding-004](#google-text-embedding-004)
- [Self-Hosted (Open Source) Models](#self-hosted-open-source-models)
  - [nomic-embed-text-v1.5 (English, Best Open Source)](#nomic-embed-text-v15-english-best-open-source)
  - [BAAI/bge-m3 (Multilingual)](#baaibge-m3-multilingual)
  - [jina-embeddings-v2 (Long Documents)](#jina-embeddings-v2-long-documents)
- [Batch Processing Strategies](#batch-processing-strategies)
  - [API Rate Limiting](#api-rate-limiting)
  - [Caching by Content Hash](#caching-by-content-hash)
- [Embedding for Different Content Types](#embedding-for-different-content-types)
  - [Text Documents](#text-documents)
  - [Code](#code)
  - [Queries (Search)](#queries-search)
- [Cost Optimization Strategies](#cost-optimization-strategies)
  - [1. Dimension Reduction (Maturity Shortening)](#1-dimension-reduction-maturity-shortening)
  - [2. Use Smaller Models for Less Critical Content](#2-use-smaller-models-for-less-critical-content)
  - [3. Self-Host for High Volume](#3-self-host-for-high-volume)
- [Quality vs. Cost Trade-Off Matrix](#quality-vs-cost-trade-off-matrix)
- [Monitoring Embedding Quality](#monitoring-embedding-quality)
- [Migration Between Embedding Models](#migration-between-embedding-models)
- [Best Practices](#best-practices)
  - [1. Normalize Embeddings](#1-normalize-embeddings)
  - [2. Consistent Preprocessing](#2-consistent-preprocessing)
  - [3. Separate Query and Document Embeddings (if supported)](#3-separate-query-and-document-embeddings-if-supported)
- [Additional Resources](#additional-resources)

## Overview

Embedding models convert text, images, audio, or code into dense vector representations that capture semantic meaning. Choosing the right embedding model balances quality, cost, latency, and deployment requirements.

## Embedding Model Comparison (2025)

### Quality Benchmark: MTEB (Massive Text Embedding Benchmark)

Higher scores indicate better semantic understanding across diverse tasks.

| Provider | Model | Dimensions | MTEB Score | Cost ($/1M tokens) | Best For |
|----------|-------|------------|------------|-------------------|----------|
| **Voyage AI** | voyage-3 | 1024 | 69.3 | ~$0.12 | Highest quality |
| **OpenAI** | text-embedding-3-large | 3072 | 64.6 | ~$0.13 | Enterprise reliability |
| **Cohere** | embed-v3 | 1024 | 64.5 | ~$0.10 | Multilingual (100+ langs) |
| **OpenAI** | text-embedding-3-small | 1536 | 62.3 | ~$0.02 | Cost-optimized |
| **Google** | text-embedding-004 | 768 | 62.0 | ~$0.025 | GCP ecosystem |
| **nomic** | nomic-embed-text-v1.5 | 768 | 62.4 | Free (self-hosted) | Privacy, English |
| **BAAI** | bge-m3 | 1024 | 63.5 | Free (self-hosted) | Multilingual, open |
| **jina** | jina-embeddings-v2 | 768 | 60.4 | Free (self-hosted) | Long docs (8K context) |

**Voyage AI Advantage:** 9.74% better performance than OpenAI on MTEB, making it the quality leader.

## Managed Embedding APIs

### Voyage AI (Highest Quality)

```python
import voyageai

client = voyageai.Client(api_key="your-api-key")

# Generate embeddings
embeddings = client.embed(
    texts=["Document text 1", "Document text 2"],
    model="voyage-3",  # or voyage-large-2, voyage-code-2
    input_type="document"  # or "query" for search queries
)

# Extract vectors
vectors = [emb.embedding for emb in embeddings.embeddings]
```

**When to use:**
- Best quality matters more than cost
- High-stakes search applications
- Enterprise RAG systems requiring maximum accuracy
- Budget allows ~$0.12/1M tokens

### OpenAI (Enterprise Standard)

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Generate embeddings
response = client.embeddings.create(
    input=["Document text 1", "Document text 2"],
    model="text-embedding-3-large"  # or text-embedding-3-small
)

# Extract vectors
vectors = [item.embedding for item in response.data]
```

**Dimension Reduction (Maturity Shortening):**
```python
# Reduce 3072d to 1024d for cost savings
response = client.embeddings.create(
    input=["Document text"],
    model="text-embedding-3-large",
    dimensions=1024  # Can be: 256, 512, 1024, 1536, 3072
)
```

**When to use:**
- Enterprise reliability required
- Integration simplicity valued
- Dimension reduction needed (3072d → 1024d)
- Cost: $0.13/1M tokens acceptable

### OpenAI text-embedding-3-small (Cost-Optimized)

```python
response = client.embeddings.create(
    input=["Document text"],
    model="text-embedding-3-small"  # 1536 dimensions
)
```

**When to use:**
- Budget constraints critical
- 90-95% of large model quality acceptable
- Cost: $0.02/1M tokens (6x cheaper than large)
- High-volume applications

### Cohere (Multilingual Leader)

```python
import cohere

client = cohere.Client(api_key="your-api-key")

# Generate embeddings
response = client.embed(
    texts=["Document text 1", "Document text 2"],
    model="embed-v3",  # or embed-english-v3.0
    input_type="search_document"  # or "search_query", "classification"
)

vectors = response.embeddings
```

**When to use:**
- Global applications (100+ languages)
- Non-English content dominant
- Need input type optimization (document vs. query)
- Cost: ~$0.10/1M tokens

### Google text-embedding-004

```python
from google.cloud import aiplatform

# Generate embeddings via Vertex AI
embeddings = aiplatform.TextEmbedding.from_pretrained(
    model_name="text-embedding-004"
)

vectors = embeddings.get_embeddings(["Document text"])
```

**When to use:**
- Already using GCP ecosystem
- Vertex AI integration required
- Cost: ~$0.025/1M tokens
- 768 dimensions sufficient

## Self-Hosted (Open Source) Models

### nomic-embed-text-v1.5 (English, Best Open Source)

```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True)

# Generate embeddings
embeddings = model.encode([
    "Document text 1",
    "Document text 2"
], convert_to_numpy=True)
```

**Specifications:**
- **Dimensions:** 768
- **License:** Apache 2.0
- **Context length:** 8192 tokens
- **Quality:** Competitive with commercial models
- **Cost:** Free (infrastructure only)

**When to use:**
- Privacy-critical applications
- English-only content
- Self-hosting required
- Budget for GPU infrastructure

### BAAI/bge-m3 (Multilingual)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-m3')

# Generate embeddings
embeddings = model.encode([
    "English text",
    "中文文本",
    "Texte français"
], convert_to_numpy=True)
```

**Specifications:**
- **Dimensions:** 1024
- **License:** MIT
- **Languages:** 100+ languages
- **Context length:** 8192 tokens

**When to use:**
- Multilingual content
- Self-hosting required
- Strong performance needed
- License flexibility important

### jina-embeddings-v2 (Long Documents)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('jinaai/jina-embeddings-v2-base-en')

# Generate embeddings for long documents
embeddings = model.encode([
    long_technical_doc  # Up to 8192 tokens
], convert_to_numpy=True)
```

**Specifications:**
- **Dimensions:** 768
- **License:** Apache 2.0
- **Context length:** 8192 tokens (2x most models)
- **Best for:** Technical documentation, long articles

**When to use:**
- Documents exceed 512 tokens regularly
- Technical documentation embedding
- Self-hosting preferred
- Long-form content

## Batch Processing Strategies

### API Rate Limiting

```python
import time
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
def generate_embeddings_with_retry(texts, model="text-embedding-3-large"):
    response = client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]

# Batch processing
batch_size = 100  # Adjust based on API limits
all_embeddings = []

for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    embeddings = generate_embeddings_with_retry(batch)
    all_embeddings.extend(embeddings)
    time.sleep(1)  # Rate limiting
```

### Caching by Content Hash

```python
import hashlib
import json

class EmbeddingCache:
    def __init__(self, cache_file="embedding_cache.json"):
        self.cache_file = cache_file
        try:
            with open(cache_file, 'r') as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.cache = {}

    def get_hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def get(self, text):
        hash_key = self.get_hash(text)
        return self.cache.get(hash_key)

    def set(self, text, embedding):
        hash_key = self.get_hash(text)
        self.cache[hash_key] = embedding
        self._save()

    def _save(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

# Usage
cache = EmbeddingCache()

def get_embedding_cached(text):
    cached = cache.get(text)
    if cached:
        return cached

    # Generate new embedding
    response = client.embeddings.create(input=[text], model="text-embedding-3-large")
    embedding = response.data[0].embedding
    cache.set(text, embedding)
    return embedding
```

## Embedding for Different Content Types

### Text Documents

```python
# Standard text embedding
def embed_document(text, model="text-embedding-3-large"):
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
```

### Code

```python
# Use code-specific models
import voyageai

client = voyageai.Client(api_key="your-api-key")

# Voyage Code-2 optimized for code
embeddings = client.embed(
    texts=["def hello_world():\n    print('Hello, world!')"],
    model="voyage-code-2",
    input_type="document"
)

# Alternative: OpenAI with code prefix
response = openai_client.embeddings.create(
    input=["CODE:\ndef hello_world():\n    print('Hello, world!')"],
    model="text-embedding-3-large"
)
```

### Queries (Search)

```python
# Use query-specific input type
import voyageai

client = voyageai.Client(api_key="your-api-key")

# Mark as query (not document)
query_embedding = client.embed(
    texts=["How do I implement OAuth refresh tokens?"],
    model="voyage-3",
    input_type="query"  # Optimizes for search queries
).embeddings[0].embedding

# Cohere query optimization
import cohere
cohere_client = cohere.Client(api_key="your-api-key")

query_embedding = cohere_client.embed(
    texts=["search query"],
    model="embed-v3",
    input_type="search_query"  # vs. "search_document"
).embeddings[0]
```

## Cost Optimization Strategies

### 1. Dimension Reduction (Maturity Shortening)

```python
# OpenAI: Reduce from 3072d to 1024d
response = client.embeddings.create(
    input=["text"],
    model="text-embedding-3-large",
    dimensions=1024  # 3x fewer dimensions = lower storage/compute
)
```

**Savings:**
- Storage: 3x reduction
- Vector search: 2-3x faster
- Quality loss: <5% in most cases

### 2. Use Smaller Models for Less Critical Content

```python
# High-value content: Use voyage-3
important_embeddings = voyage_client.embed(
    texts=important_docs,
    model="voyage-3"
)

# Supplementary content: Use text-embedding-3-small
supplementary_embeddings = openai_client.embeddings.create(
    input=supplementary_docs,
    model="text-embedding-3-small"  # 6x cheaper
)
```

### 3. Self-Host for High Volume

```python
# One-time setup cost, zero per-request cost
model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5')

# Free embeddings after infrastructure cost
embeddings = model.encode(millions_of_documents)
```

**Break-even analysis:**
- API cost: $0.12/1M tokens
- Self-hosted: GPU instance ~$500/month
- Break-even: ~4M tokens/month (~2M documents)

## Quality vs. Cost Trade-Off Matrix

| Use Case | Quality Need | Volume | Recommendation | Monthly Cost (1M docs) |
|----------|--------------|--------|----------------|------------------------|
| **Enterprise RAG** | Highest | Medium | Voyage AI voyage-3 | $60-120 |
| **Production Search** | High | High | OpenAI 3-large (1024d) | $40-65 |
| **Chatbot** | Medium | Medium | OpenAI 3-small | $10-20 |
| **Content Recommendation** | Medium | High | Self-hosted nomic | $500 (fixed) |
| **Internal Tools** | Low | Low | OpenAI 3-small | $5-10 |
| **Privacy-Critical** | High | Any | Self-hosted bge-m3 | $500-1000 (fixed) |

## Monitoring Embedding Quality

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Test semantic similarity
test_pairs = [
    ("OAuth refresh token", "token renewal mechanism"),  # Should be similar
    ("OAuth refresh token", "chocolate cake recipe")     # Should be different
]

for text1, text2 in test_pairs:
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    similarity = cosine_similarity([emb1], [emb2])[0][0]
    print(f"'{text1}' <-> '{text2}': {similarity:.3f}")
```

## Migration Between Embedding Models

```python
# Regenerate all embeddings when changing models
def migrate_embeddings(old_collection, new_model):
    # 1. Retrieve all documents
    docs = old_collection.scroll(limit=10000)

    # 2. Generate new embeddings
    new_embeddings = []
    for doc in docs:
        embedding = generate_embedding(doc.payload['text'], new_model)
        new_embeddings.append(embedding)

    # 3. Create new collection with new dimensions
    new_collection = create_collection(
        name="documents_v2",
        vector_size=len(new_embeddings[0])
    )

    # 4. Insert with new embeddings
    new_collection.upsert(new_embeddings, payloads=[d.payload for d in docs])
```

## Best Practices

### 1. Normalize Embeddings
```python
import numpy as np

def normalize_embedding(embedding):
    return embedding / np.linalg.norm(embedding)

# Normalized embeddings work better with cosine distance
```

### 2. Consistent Preprocessing
```python
def preprocess_text(text):
    # Consistent preprocessing for embeddings
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text
```

### 3. Separate Query and Document Embeddings (if supported)
```python
# Document embedding
doc_emb = voyage_client.embed(
    texts=[document],
    model="voyage-3",
    input_type="document"
)

# Query embedding
query_emb = voyage_client.embed(
    texts=[query],
    model="voyage-3",
    input_type="query"
)
```

## Additional Resources

- **MTEB Leaderboard:** https://huggingface.co/spaces/mteb/leaderboard
- **Voyage AI Docs:** https://docs.voyageai.com/
- **OpenAI Embeddings Guide:** https://platform.openai.com/docs/guides/embeddings
- **Sentence Transformers:** https://www.sbert.net/
- **Cohere Embeddings:** https://docs.cohere.com/docs/embeddings
