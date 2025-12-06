# Embedding Model Selection Guide

Comprehensive decision framework for selecting embedding models based on requirements, costs, and quality trade-offs.

## Table of Contents

1. [Decision Framework](#decision-framework)
2. [Model Comparison Matrix](#model-comparison-matrix)
3. [Cost Analysis](#cost-analysis)
4. [Quality Benchmarks](#quality-benchmarks)
5. [Use Case Recommendations](#use-case-recommendations)

## Decision Framework

### Question 1: Data Privacy Requirements

**Do you have data privacy requirements preventing external API calls?**

- **YES** → Must use local models (sentence-transformers)
  - Government/healthcare data
  - Proprietary business information
  - GDPR/compliance requirements
  - Zero external data transmission

- **NO** → Continue to Question 2

### Question 2: Query Volume

**What is your expected embedding query volume?**

- **<1M embeddings/month** → OpenAI API recommended
  - Simple integration, no infrastructure
  - Predictable costs ($0-$50/month)
  - High reliability (99.9% uptime SLA)

- **1M-10M embeddings/month** → Evaluate costs carefully
  - Calculate API costs vs. GPU infrastructure
  - Consider hybrid approach (local + API)
  - Expected API cost: $20-$1,300/month

- **>10M embeddings/month** → Local models recommended
  - API costs become prohibitive ($1,300+/month)
  - GPU infrastructure more cost-effective
  - Full control over scaling

### Question 3: Quality Requirements

**What is your quality requirement?**

- **HIGHEST** → `text-embedding-3-large` (3,072 dims, $0.13/1M tokens)
  - Research applications requiring maximum accuracy
  - Small corpora where quality outweighs cost
  - Premium products with quality SLAs

- **HIGH** → `text-embedding-3-small` (1,536 dims, $0.02/1M tokens)
  - Production RAG systems
  - Customer-facing semantic search
  - General purpose retrieval

- **GOOD** → `BGE-base-en-v1.5` (768 dims, local)
  - Cost-sensitive applications
  - High-volume search systems
  - Acceptable quality with zero API costs

- **FAST** → `all-MiniLM-L6-v2` (384 dims, local)
  - Real-time applications requiring low latency
  - Massive scale (100M+ embeddings)
  - Prototyping and development

### Question 4: Multilingual Support

**Do you need multilingual support?**

- **YES** → Specialized multilingual models
  - **API:** Cohere `embed-multilingual-v3.0` (100+ languages)
  - **Local:** `multilingual-e5-base` (100+ languages)
  - **Local:** `paraphrase-multilingual-MiniLM-L12-v2` (50+ languages)

- **NO** → English-optimized models (better quality)
  - `text-embedding-3-small/large` (OpenAI)
  - `BGE-base/large-en-v1.5` (local)
  - `all-MiniLM-L6-v2` (local)

## Model Comparison Matrix

### API-Based Models (OpenAI)

| Model | Dimensions | Cost (1M tokens) | Quality (MTEB) | Latency | Best For |
|-------|-----------|------------------|----------------|---------|----------|
| text-embedding-3-small | 1,536 | $0.02 | 62.3% | 50-200ms | General purpose |
| text-embedding-3-large | 3,072 | $0.13 | 64.6% | 50-200ms | Premium quality |

**Matryoshka Support:** Both models support variable dimensionality (256, 512, 1,024, 1,536, 3,072)
- Embed once, use at multiple dimensions
- Trade quality for storage/speed as needed

### API-Based Models (Cohere)

| Model | Dimensions | Cost (1M tokens) | Quality | Latency | Best For |
|-------|-----------|------------------|---------|---------|----------|
| embed-english-v3.0 | 1,024 | $0.10 | 64.5% | 50-200ms | English-only |
| embed-multilingual-v3.0 | 1,024 | $0.10 | 62.0% | 50-200ms | 100+ languages |

**Compression Support:** Cohere models support compression-aware embeddings for reduced storage.

### Local Models (sentence-transformers)

| Model | Dimensions | Parameters | Quality (MTEB) | GPU Memory | Best For |
|-------|-----------|-----------|----------------|------------|----------|
| all-MiniLM-L6-v2 | 384 | 22M | 58.8% | 512 MB | Fast inference, low resource |
| BGE-base-en-v1.5 | 768 | 109M | 63.6% | 2 GB | SOTA quality, English |
| BGE-large-en-v1.5 | 1,024 | 335M | 64.2% | 4 GB | Maximum local quality |
| multilingual-e5-base | 768 | 278M | 61.5% | 2 GB | Cross-lingual retrieval |
| nomic-embed-text-v1 | 768 | 137M | 62.4% | 2 GB | Fully open, reproducible |

**MTEB:** Massive Text Embedding Benchmark (higher is better, max 100%)

### Inference Speed Comparison

**Hardware:** NVIDIA RTX 3090 GPU, batch size 32

| Model | Throughput (texts/sec) | Latency (ms) |
|-------|----------------------|--------------|
| all-MiniLM-L6-v2 | 10,000 | 3.2 |
| BGE-base-en-v1.5 | 4,000 | 8.0 |
| BGE-large-en-v1.5 | 1,500 | 21.3 |
| text-embedding-3-small (API) | 1,000 | 100-200 |
| text-embedding-3-large (API) | 1,000 | 100-200 |

## Cost Analysis

### API Cost Scenarios

**Assumptions:**
- Average document: 2,000 characters → 500 tokens
- Average query: 100 characters → 25 tokens

**Scenario 1: Small Application (10K documents, 1K queries/month)**

| Model | Document Cost | Query Cost | Total/month |
|-------|--------------|-----------|-------------|
| text-embedding-3-small | $0.10 | $0.0005 | $0.10 |
| text-embedding-3-large | $0.65 | $0.0033 | $0.65 |

**Recommendation:** Either API model works; choose based on quality needs.

**Scenario 2: Medium Application (100K documents, 10K queries/month)**

| Model | Document Cost | Query Cost | Total/month |
|-------|--------------|-----------|-------------|
| text-embedding-3-small | $1.00 | $0.005 | $1.00 |
| text-embedding-3-large | $6.50 | $0.033 | $6.53 |
| Local (GPU server) | $0 | $0 | $150 (GPU) |

**Recommendation:** API still cost-effective; local if GPU already available.

**Scenario 3: Large Application (1M documents, 100K queries/month)**

| Model | Document Cost | Query Cost | Total/month |
|-------|--------------|-----------|-------------|
| text-embedding-3-small | $10.00 | $0.05 | $10.05 |
| text-embedding-3-large | $65.00 | $0.33 | $65.33 |
| Local (GPU server) | $0 | $0 | $150 (GPU) |

**Recommendation:** Local models cost-effective at this scale.

**Scenario 4: Enterprise (10M documents, 1M queries/month)**

| Model | Document Cost | Query Cost | Total/month |
|-------|--------------|-----------|-------------|
| text-embedding-3-small | $100.00 | $0.50 | $100.50 |
| text-embedding-3-large | $650.00 | $3.25 | $653.25 |
| Local (multi-GPU) | $0 | $0 | $300 (GPUs) |

**Recommendation:** Local models strongly recommended.

### GPU Infrastructure Costs (2025)

| GPU | Cloud Cost ($/month) | Purchase Cost | Throughput (texts/sec) |
|-----|---------------------|---------------|----------------------|
| NVIDIA RTX 3090 | N/A (desktop) | $1,500 | 10,000 (MiniLM) |
| AWS g5.xlarge (A10G) | $400 | N/A | 8,000 (MiniLM) |
| AWS g5.2xlarge (A10G) | $800 | N/A | 15,000 (MiniLM) |
| Apple M2 Max (MPS) | N/A (laptop) | $3,000 | 3,000 (MiniLM) |

**Break-even Analysis:**
- If embedding costs >$150/month → Local GPU economical
- If embedding costs >$400/month → Cloud GPU economical

## Quality Benchmarks

### Retrieval Quality (MTEB Benchmark)

**Task:** Retrieve relevant documents for a query (higher is better)

| Model | Retrieval (nDCG@10) | Clustering | Classification |
|-------|-------------------|-----------|---------------|
| text-embedding-3-large | 64.6% | 49.0% | 70.9% |
| text-embedding-3-small | 62.3% | 47.2% | 69.6% |
| BGE-large-en-v1.5 | 64.2% | 46.9% | 75.0% |
| BGE-base-en-v1.5 | 63.6% | 46.1% | 74.4% |
| all-MiniLM-L6-v2 | 58.8% | 42.4% | 63.0% |

**Key Insight:** BGE models match or exceed OpenAI quality on many tasks, with zero API costs.

### Quality vs. Dimensions

**Experiment:** Same model (text-embedding-3-large) at different dimensions (Matryoshka)

| Dimensions | Retrieval Quality | Storage (1M vectors) | Search Speed |
|-----------|------------------|---------------------|--------------|
| 3,072 | 100% (baseline) | 12 GB | 40ms |
| 1,536 | 98% | 6 GB | 25ms |
| 1,024 | 95% | 4 GB | 18ms |
| 512 | 90% | 2 GB | 12ms |
| 256 | 82% | 1 GB | 8ms |

**Trade-off:** 50% dimension reduction (3,072 → 1,536) loses only 2% quality but halves storage and improves search speed by 37%.

## Use Case Recommendations

### Use Case 1: Startup MVP (Rapid Development)

**Requirements:**
- Fast development, limited budget
- 1K-10K documents
- Acceptable quality, not critical

**Recommendation:** `all-MiniLM-L6-v2` (local)
- **Pros:** Free, fast inference, simple setup
- **Cons:** Lower quality than premium models
- **Expected Cost:** $0 (uses existing hardware)

### Use Case 2: Production RAG (Customer-Facing)

**Requirements:**
- High quality retrieval
- 10K-100K documents
- Moderate query volume (10K-100K/month)

**Recommendation:** `text-embedding-3-small` (API)
- **Pros:** High quality, reliable, simple integration
- **Cons:** API costs ($1-$10/month)
- **Expected Cost:** $5-$50/month

### Use Case 3: Enterprise Search (High Volume)

**Requirements:**
- 1M+ documents
- 100K+ queries/month
- Quality important but cost-sensitive

**Recommendation:** `BGE-base-en-v1.5` (local)
- **Pros:** SOTA quality, zero API costs, full control
- **Cons:** Requires GPU infrastructure
- **Expected Cost:** $150-$400/month (GPU)

### Use Case 4: Multi-Lingual Support

**Requirements:**
- 50+ languages
- Moderate volume
- Cross-lingual retrieval (query in English, retrieve Spanish)

**Recommendation:** `multilingual-e5-base` (local) or Cohere `embed-multilingual-v3.0` (API)
- **Pros:** Strong cross-lingual performance
- **Cons:** Lower quality than English-only models
- **Expected Cost:** $0 (local) or $0.10/1M tokens (API)

### Use Case 5: Research/Academic

**Requirements:**
- Maximum quality
- Small corpus (1K-10K documents)
- Cost not primary concern

**Recommendation:** `text-embedding-3-large` (API)
- **Pros:** Highest quality available
- **Cons:** 6.5x more expensive than text-embedding-3-small
- **Expected Cost:** $0.65-$65/month

## Selection Decision Tree

```
START
│
├─ Data Privacy Required? → YES → Local Models
│  │                               ├─ High Quality → BGE-base/large-en-v1.5
│  │                               └─ Fast/Cheap → all-MiniLM-L6-v2
│  │
│  └─ NO → Continue
│     │
│     ├─ Query Volume?
│     │  ├─ <1M/month → API Models
│     │  │              ├─ Max Quality → text-embedding-3-large
│     │  │              └─ Balanced → text-embedding-3-small
│     │  │
│     │  ├─ 1M-10M/month → Calculate Costs
│     │  │                 ├─ Cost > $150 → Local (BGE-base)
│     │  │                 └─ Cost < $150 → API (text-embedding-3-small)
│     │  │
│     │  └─ >10M/month → Local Models (BGE-base-en-v1.5)
│     │
│     └─ Multilingual?
│        ├─ YES → multilingual-e5-base (local) or Cohere embed-multilingual (API)
│        └─ NO → Continue to quality tier above
```

## Migration Strategies

### Migrating from API to Local

**Scenario:** Outgrowing API tier, need cost reduction

**Steps:**
1. **Benchmark Local Models:** Test BGE-base-en-v1.5 on sample queries
2. **Evaluate Quality Delta:** Compare retrieval metrics (nDCG, precision@k)
3. **Provision GPU Infrastructure:** AWS g5.xlarge or local GPU
4. **Parallel Run:** Run API and local in parallel for 1-2 weeks
5. **Cutover:** Switch to local once quality validated
6. **Monitor:** Track quality metrics post-migration

**Expected Results:**
- Cost reduction: 70-90%
- Quality delta: 0-5% (BGE-base vs. text-embedding-3-small)
- Setup time: 1-2 weeks

### Migrating from Local to API

**Scenario:** Scaling complexity, prefer managed service

**Steps:**
1. **Select API Model:** Choose text-embedding-3-small or -large
2. **Implement Caching:** Add Redis caching to reduce API costs
3. **Gradual Migration:** Embed new documents via API, keep old embeddings
4. **Monitor Costs:** Track API usage, ensure within budget
5. **Optimize:** Batch requests, use caching, monitor hit rates

**Expected Results:**
- Cost increase: 50-300% (offset by operational simplicity)
- Quality improvement: 0-5%
- Setup time: 1 week

## Summary Recommendations

**Default Choices by Scenario:**

| Scenario | Recommended Model | Reasoning |
|----------|------------------|-----------|
| MVP/Prototype | all-MiniLM-L6-v2 | Zero cost, fast iteration |
| Small App | text-embedding-3-small | Simple, reliable, affordable |
| Production RAG | text-embedding-3-small | Quality + convenience |
| High Volume | BGE-base-en-v1.5 | Cost-effective at scale |
| Enterprise | BGE-base-en-v1.5 | Control + cost savings |
| Multilingual | multilingual-e5-base | Cross-lingual performance |
| Research | text-embedding-3-large | Maximum quality |

**Key Principles:**
1. Start with API models for simplicity
2. Migrate to local when costs exceed GPU infrastructure
3. Always implement caching (70-90% cost reduction)
4. Monitor quality metrics during model changes
5. Test with real queries before committing to a model
