# Data Versioning for AI/ML Pipelines

Version control for datasets, embeddings, and model artifacts using LakeFS and DVC.

## Why Data Versioning

**The Problem:**
- "Which embedding model generated these vectors?"
- "What data was the model trained on?"
- "How do I reproduce this RAG result?"
- "Can I A/B test different chunking strategies?"

**The Solution:** Git-like operations for data (branch, commit, merge, rollback).

## LakeFS (Recommended)

**Git for data lakes.** Acquired DVC team (November 2025) - now the unified standard.

### Key Features

- Branch, commit, merge operations on data
- Time travel (access historical versions)
- Zero-copy branching (instant, no duplication)
- Works with S3, Azure Blob, GCS
- Iceberg/Delta Lake integration

### Installation

```bash
# Docker
docker run -p 8000:8000 treeverse/lakefs:latest

# Access UI: http://localhost:8000
# Default credentials: AKIAIOSFOLQUICKSTART / wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Basic Workflow

```python
import lakefs

# Initialize client
client = lakefs.Client(
    host="http://localhost:8000",
    username="AKIAIOSFOLQUICKSTART",
    password="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
)

# Create repository
repo = client.repositories.create(
    name="my-rag-pipeline",
    storage_namespace="s3://my-bucket/lakefs/",
)

# Create branch for experiment
branch = repo.branch("main").create("experiment-voyage-3-embeddings")

# Upload data to branch
branch.object("embeddings/voyage-3.parquet").upload("local-file.parquet")

# Commit changes
branch.commit(message="Switch to Voyage AI embeddings")

# Merge to main after validation
branch.merge_into("main")
```

### RAG Pipeline Integration

```python
# Version embeddings pipeline
def generate_embeddings_versioned(documents, branch_name="main"):
    # 1. Create experimental branch
    branch = repo.branch("main").create(f"embeddings-{branch_name}")

    # 2. Generate embeddings
    embeddings = voyage_ai.embed(documents)

    # 3. Save to branch
    branch.object("embeddings/vectors.parquet").upload_dataframe(embeddings)

    # 4. Run evaluation
    metrics = evaluate_rag(embeddings)

    # 5. Commit with metrics
    branch.commit(
        message=f"Generated embeddings using Voyage AI",
        metadata={"recall": metrics.recall, "precision": metrics.precision}
    )

    # 6. Merge if metrics improved
    if metrics.recall > baseline_recall:
        branch.merge_into("main")
        print("✓ Embeddings improved, merged to main")
    else:
        print("✗ No improvement, branch preserved for analysis")
```

### Compare Experiments

```python
# Compare two chunking strategies
main_branch = repo.branch("main")
exp_branch = repo.branch("chunking-semantic")

# Get diff
diff = exp_branch.diff(other=main_branch)
print(f"Changed objects: {len(diff.results)}")

# Compare metrics
main_metrics = main_branch.object("metrics.json").read()
exp_metrics = exp_branch.object("metrics.json").read()

print(f"Main recall: {main_metrics['recall']}")
print(f"Experiment recall: {exp_metrics['recall']}")
```

## DVC (Alternative)

**Data Version Control** - Git-like tool specifically for ML datasets.

**Note:** DVC team acquired by LakeFS (Nov 2025). LakeFS now recommended for new projects.

### Installation

```bash
pip install dvc[s3]  # or [gs], [azure]
```

### Basic Workflow

```bash
# Initialize DVC
dvc init

# Track data file
dvc add data/embeddings.parquet

# Commit tracking file (.dvc)
git add data/embeddings.parquet.dvc data/.gitignore
git commit -m "Add embeddings"

# Push data to remote storage
dvc push

# Pull data on another machine
dvc pull
```

### DVC Pipelines

```yaml
# dvc.yaml
stages:
  chunk_documents:
    cmd: python scripts/chunk.py
    deps:
      - data/raw/documents.pdf
    params:
      - chunk_size
      - overlap
    outs:
      - data/chunks/

  generate_embeddings:
    cmd: python scripts/embed.py
    deps:
      - data/chunks/
    outs:
      - data/embeddings/vectors.parquet

  evaluate:
    cmd: python scripts/evaluate.py
    deps:
      - data/embeddings/vectors.parquet
    metrics:
      - metrics.json
```

```bash
# Run pipeline
dvc repro

# View metrics across experiments
dvc metrics show

# Compare experiments
dvc metrics diff experiment-1 experiment-2
```

## Comparison: LakeFS vs DVC

| Feature | LakeFS | DVC |
|---------|--------|-----|
| **Branching** | Zero-copy (instant) | Full copy (slow) |
| **Scale** | Petabytes | Gigabytes-Terabytes |
| **Format** | Any (object storage) | Any (file-based) |
| **Integration** | S3 API compatible | Git-based |
| **UI** | Web UI included | CLI only |
| **Team** | Same team (acquired DVC) | Merged into LakeFS |
| **Best for** | Production data lakes | Small ML projects |

**Recommendation:** Use LakeFS for new projects (unified future direction).

## Embedding Versioning Best Practices

### 1. Version Embedding Model + Data Together

```python
embedding_metadata = {
    "model": "voyage-3",
    "model_version": "1.0",
    "dimensions": 1024,
    "input_data_version": "main@abc123",
    "chunking_strategy": "fixed-512-50",
    "generated_at": "2025-12-03T10:00:00Z",
}
```

### 2. Immutable Embeddings

Never update existing embeddings in-place. Create new versions.

```python
# ❌ Don't update
embeddings/vectors.parquet  # Update in place

# ✅ Do version
embeddings/v1/vectors.parquet
embeddings/v2/vectors.parquet  # New version
```

### 3. Tag Important Versions

```bash
# LakeFS tags
lakefs tag create my-repo production-v1.0 --ref main

# DVC tags
git tag -a embeddings-v1.0 -m "Voyage AI production embeddings"
dvc push
```

## Experiment Tracking Integration

### MLflow + LakeFS

```python
import mlflow

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("chunk_size", 512)
    mlflow.log_param("embedding_model", "voyage-3")
    mlflow.log_param("data_version", branch.head.id)

    # Generate embeddings
    embeddings = generate_embeddings()

    # Log metrics
    metrics = evaluate_rag(embeddings)
    mlflow.log_metrics(metrics)

    # Log LakeFS commit
    mlflow.log_param("lakefs_commit", branch.head.id)
```

## Reproducibility Checklist

- [ ] Data version tracked (LakeFS/DVC)
- [ ] Embedding model version recorded
- [ ] Chunking parameters documented
- [ ] Random seeds set (for reproducible experiments)
- [ ] Dependencies pinned (requirements.txt)
- [ ] Evaluation metrics logged
- [ ] Commit hash recorded
- [ ] Environment documented (Python version, OS)

## Resources

- LakeFS Docs: https://docs.lakefs.io/
- DVC Docs: https://dvc.org/doc
- MLflow: https://mlflow.org/docs/
