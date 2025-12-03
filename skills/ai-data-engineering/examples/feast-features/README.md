# Feast Feature Store Example

Complete feature store implementation with Feast for ML feature serving.

## Setup

```bash
pip install -r requirements.txt
```

## Initialize Feast Repository

```bash
# Create feature repository
feast init feature_repo
cd feature_repo
```

## Run Example

```bash
python setup_features.py
```

This will:
1. Define user features
2. Generate sample data
3. Apply features to registry
4. Materialize to online store
5. Demonstrate online/offline serving

## File Descriptions

- `setup_features.py` - Complete feature store setup
- `requirements.txt` - Dependencies
- `README.md` - This file

## Key Concepts

**Feature View:** Definition of features and their sources
**Entity:** Join key (e.g., user_id)
**Online Store:** Low-latency serving (Redis, DynamoDB)
**Offline Store:** Training data (S3, BigQuery)

## Production Deployment

See `setup_features.py` for production configuration with:
- Redis online store
- S3 offline store
- Point-in-time joins
- Feature versioning
