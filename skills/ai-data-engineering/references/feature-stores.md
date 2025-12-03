# Feature Stores: ML Feature Serving

Complete guide to feature stores for solving the training-serving skew problem in ML systems.

## Table of Contents

- [Overview](#overview)
- [Problem: Training-Serving Skew](#problem-training-serving-skew)
- [Feast (Recommended)](#feast-recommended)
- [Alternatives](#alternatives)
- [Implementation Patterns](#implementation-patterns)
- [Production Deployment](#production-deployment)

## Overview

Feature stores solve the "training-serving skew" problem by providing consistent feature computation across training (offline) and inference (online).

**Without Feature Store:**
```
Training: Python notebook → pandas → features → model
Serving:  Production API → SQL → features → model
          ^ Different code = different features = model degradation
```

**With Feature Store:**
```
Training: Feast → features → model
Serving:  Feast → features → model
          ^ Same code = same features = consistent performance
```

## Problem: Training-Serving Skew

### Example Scenario

Building a recommendation model that uses user features:

**Training Time (Data Scientist):**
```python
# Jupyter notebook
import pandas as pd

df = pd.read_sql("SELECT * FROM users", connection)
df['total_orders'] = df.groupby('user_id')['order_count'].sum()
df['avg_order_value'] = df['total_spent'] / df['total_orders']
df['days_since_last_order'] = (datetime.now() - df['last_order_date']).days

# Train model with these features
model = train(df[['total_orders', 'avg_order_value', 'days_since_last_order']])
```

**Serving Time (Engineer):**
```python
# Production API (written 3 months later by different person)
def get_user_features(user_id):
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)

    # Slightly different calculation (BUG!)
    total_orders = user.order_count  # Not summed by group!
    avg_order = user.total_spent / user.order_count  # Dividing different field!
    days_since = (now() - user.last_order).days  # Different datetime handling!

    return [total_orders, avg_order, days_since]
```

**Result:** Model degrades in production because features are computed differently.

### Feature Store Solution

**Define features once, use everywhere:**

```python
from feast import FeatureView, Field, Entity
from feast.types import Float32, Int64
from datetime import timedelta

# Define features ONCE
user_features = FeatureView(
    name="user_features",
    entities=[Entity(name="user", join_keys=["user_id"])],
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="days_since_last_order", dtype=Int64)
    ],
    source=user_source,  # Data source
    ttl=timedelta(days=1)  # Freshness requirement
)
```

**Use in training:**
```python
features = store.get_historical_features(
    entity_df=entity_df,
    features=["user_features:total_orders", "user_features:avg_order_value"]
)
```

**Use in serving (same code!):**
```python
features = store.get_online_features(
    features=["user_features:total_orders", "user_features:avg_order_value"],
    entity_rows=[{"user_id": 1001}]
)
```

## Feast (Recommended)

**Why Feast:**
- Open source (Apache 2.0)
- Works with any backend (PostgreSQL, Redis, DynamoDB, S3, BigQuery, Snowflake)
- No vendor lock-in
- Active development
- Python-native

### Installation

```bash
pip install feast
```

### Quick Start

**1. Initialize feature repository:**

```bash
feast init feature_repo
cd feature_repo
```

**2. Define data source:**

```python
# feature_repo/data_sources.py
from feast import FileSource
from datetime import datetime

user_source = FileSource(
    path="data/user_features.parquet",
    timestamp_field="event_timestamp"
)
```

**3. Define feature view:**

```python
# feature_repo/features.py
from feast import FeatureView, Field, Entity
from feast.types import Float32, Int64
from datetime import timedelta

user = Entity(
    name="user",
    join_keys=["user_id"],
    description="User entity"
)

user_features = FeatureView(
    name="user_features",
    entities=[user],
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="lifetime_value", dtype=Float32),
    ],
    source=user_source,
    ttl=timedelta(days=1)
)
```

**4. Apply to registry:**

```bash
feast apply
```

**5. Materialize features (load to online store):**

```bash
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

### Online Serving (Low-Latency)

For real-time predictions:

```python
from feast import FeatureStore
from datetime import datetime

store = FeatureStore(repo_path="feature_repo/")

# Get features for a single user (< 10ms)
features = store.get_online_features(
    features=[
        "user_features:total_orders",
        "user_features:avg_order_value",
        "user_features:lifetime_value"
    ],
    entity_rows=[{"user_id": 1001}]
).to_dict()

# Use in prediction
prediction = model.predict([
    features["total_orders"][0],
    features["avg_order_value"][0],
    features["lifetime_value"][0]
])
```

### Offline Serving (Training)

For batch training:

```python
import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Entity dataframe (users and timestamps)
entity_df = pd.DataFrame({
    "user_id": [1001, 1002, 1003],
    "event_timestamp": [
        datetime(2025, 1, 1),
        datetime(2025, 1, 1),
        datetime(2025, 1, 1)
    ]
})

# Get historical features (point-in-time correct)
training_data = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "user_features:total_orders",
        "user_features:avg_order_value",
        "user_features:lifetime_value"
    ]
).to_df()

# Train model
X = training_data[["total_orders", "avg_order_value", "lifetime_value"]]
y = training_data["target"]
model.fit(X, y)
```

### Backend Configuration

**PostgreSQL Online Store:**

```yaml
# feature_store.yaml
project: my_project
registry: data/registry.db
provider: local
online_store:
  type: postgres
  host: localhost
  port: 5432
  database: feast
  user: feast_user
  password: feast_password
offline_store:
  type: file
```

**Redis Online Store (Production):**

```yaml
# feature_store.yaml
project: my_project
registry: data/registry.db
provider: local
online_store:
  type: redis
  connection_string: redis://localhost:6379
offline_store:
  type: bigquery
  project_id: my-gcp-project
```

**DynamoDB + S3 (AWS):**

```yaml
# feature_store.yaml
project: my_project
registry: s3://my-bucket/registry.db
provider: aws
online_store:
  type: dynamodb
  region: us-east-1
offline_store:
  type: file
  path: s3://my-bucket/offline-store/
```

### Transformation Features

Compute features on-the-fly:

```python
from feast import FeatureView, Field
from feast.types import Float32
from feast.on_demand_feature_view import on_demand_feature_view

@on_demand_feature_view(
    sources=[user_features],
    schema=[
        Field(name="orders_per_day", dtype=Float32),
    ]
)
def user_derived_features(features_df: pd.DataFrame) -> pd.DataFrame:
    """Compute derived features."""
    features_df["orders_per_day"] = (
        features_df["total_orders"] / features_df["days_active"]
    )
    return features_df
```

### Feature Versioning

Track feature definitions over time:

```python
# feature_repo/features_v2.py
user_features_v2 = FeatureView(
    name="user_features_v2",  # New version
    entities=[user],
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="lifetime_value", dtype=Float32),
        Field(name="purchase_frequency", dtype=Float32),  # New feature
    ],
    source=user_source,
    ttl=timedelta(days=1)
)
```

## Alternatives

### Tecton (Enterprise)

**Best for:** Large enterprises, managed service

**Pros:**
- Fully managed (SaaS)
- Advanced features (streaming, real-time transformations)
- Enterprise support
- Proven at scale (Uber, Netflix)

**Cons:**
- Commercial license (expensive)
- Vendor lock-in
- Less flexibility

**When to use:** Enterprise with large ML teams, budget for managed services

### Hopsworks (Governance)

**Best for:** Regulated industries, compliance requirements

**Pros:**
- Built-in data lineage
- GDPR compliance features
- Feature monitoring
- Model serving integration

**Cons:**
- More complex setup
- Smaller community than Feast
- Resource-intensive

**When to use:** Financial services, healthcare, regulated industries

### Skip Feature Store

**When to skip feature stores:**
- Simple model (< 10 features)
- No retraining (model trained once)
- Same person writes training & serving code
- Low feature complexity
- Prototype/MVP stage

**Use direct database queries instead:**

```python
# Simple feature retrieval
def get_features(user_id: int):
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    return {
        "total_orders": user.order_count,
        "avg_order_value": user.total_spent / user.order_count
    }
```

## Implementation Patterns

### Pattern 1: Batch Feature Computation

Compute features daily for all users:

```python
# feature_pipeline.py
from feast import FeatureStore
import pandas as pd
from datetime import datetime

def compute_daily_features():
    """Compute features for all users daily."""

    # Extract features from database
    df = pd.read_sql("""
        SELECT
            user_id,
            COUNT(*) as total_orders,
            AVG(order_value) as avg_order_value,
            SUM(order_value) as lifetime_value,
            MAX(order_date) as last_order_date
        FROM orders
        WHERE order_date >= CURRENT_DATE - INTERVAL '1 year'
        GROUP BY user_id
    """, db_connection)

    # Add timestamp
    df['event_timestamp'] = datetime.now()

    # Save to offline store
    df.to_parquet("data/user_features.parquet")

    # Materialize to online store
    store = FeatureStore(repo_path="feature_repo/")
    store.materialize_incremental(end_date=datetime.now())

# Run daily
compute_daily_features()
```

### Pattern 2: Real-Time Features

Compute features on-demand:

```python
from feast import FeatureStore
from feast.on_demand_feature_view import on_demand_feature_view
from feast import Field
from feast.types import Float32
import pandas as pd

@on_demand_feature_view(
    sources=[user_static_features],
    schema=[Field(name="recency_score", dtype=Float32)]
)
def real_time_features(features_df: pd.DataFrame) -> pd.DataFrame:
    """Compute real-time recency score."""
    from datetime import datetime

    now = datetime.now()
    features_df["recency_score"] = (
        1.0 / (1.0 + (now - features_df["last_order_date"]).days)
    )
    return features_df
```

### Pattern 3: Streaming Features

Process features from Kafka/Kinesis:

```python
# Requires Feast with streaming support
from feast import FeatureStore, KafkaSource

kafka_source = KafkaSource(
    name="user_events",
    kafka_bootstrap_servers="localhost:9092",
    topic="user_events",
    timestamp_field="event_timestamp",
    message_format={"json": {}}
)

# Define streaming feature view
streaming_features = FeatureView(
    name="streaming_user_features",
    entities=[user],
    schema=[
        Field(name="clicks_last_hour", dtype=Int64),
        Field(name="sessions_last_day", dtype=Int64)
    ],
    source=kafka_source,
    ttl=timedelta(hours=1)
)
```

## Production Deployment

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Feature Store Production Architecture           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Data Sources                                                │
│    ├── PostgreSQL (transactional data)                      │
│    ├── S3 (batch data)                                       │
│    └── Kafka (streaming events)                              │
│         ↓                                                    │
│  Feature Pipeline (Dagster)                                  │
│    ├── Extract                                               │
│    ├── Transform                                             │
│    └── Load to Feast                                         │
│         ↓                                                    │
│  Feast Feature Store                                         │
│    ├── Offline Store (S3/BigQuery) → Training                │
│    └── Online Store (Redis/DynamoDB) → Serving               │
│         ↓                                                    │
│  ML Services                                                 │
│    ├── Training Service (batch)                              │
│    └── Prediction API (real-time)                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Dagster Pipeline

Orchestrate feature computation:

```python
from dagster import asset, AssetExecutionContext
from feast import FeatureStore
import pandas as pd

@asset
def raw_user_data(context: AssetExecutionContext):
    """Extract user data from database."""
    df = pd.read_sql("""
        SELECT user_id, order_date, order_value
        FROM orders
        WHERE order_date >= CURRENT_DATE - INTERVAL '1 year'
    """, db_connection)
    return df

@asset
def user_features(raw_user_data: pd.DataFrame):
    """Transform into features."""
    features = raw_user_data.groupby('user_id').agg({
        'order_value': ['count', 'mean', 'sum']
    }).reset_index()

    features.columns = ['user_id', 'total_orders', 'avg_order_value', 'lifetime_value']
    features['event_timestamp'] = datetime.now()

    return features

@asset
def materialized_features(user_features: pd.DataFrame):
    """Materialize to Feast."""
    # Save to offline store
    user_features.to_parquet("data/user_features.parquet")

    # Materialize to online store
    store = FeatureStore(repo_path="feature_repo/")
    store.materialize_incremental(end_date=datetime.now())

    return {"status": "materialized", "count": len(user_features)}
```

### FastAPI Serving

Serve features via API:

```python
from fastapi import FastAPI, HTTPException
from feast import FeatureStore
from pydantic import BaseModel

app = FastAPI()
store = FeatureStore(repo_path="feature_repo/")

class PredictionRequest(BaseModel):
    user_id: int

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Get prediction for user."""
    try:
        # Get features
        features = store.get_online_features(
            features=[
                "user_features:total_orders",
                "user_features:avg_order_value",
                "user_features:lifetime_value"
            ],
            entity_rows=[{"user_id": request.user_id}]
        ).to_dict()

        # Make prediction
        feature_vector = [
            features["total_orders"][0],
            features["avg_order_value"][0],
            features["lifetime_value"][0]
        ]

        prediction = model.predict([feature_vector])[0]

        return {
            "user_id": request.user_id,
            "prediction": float(prediction),
            "features_used": features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Monitoring

Track feature freshness and quality:

```python
# feature_monitoring.py
from feast import FeatureStore
from datetime import datetime, timedelta

def monitor_feature_freshness():
    """Check feature freshness."""
    store = FeatureStore(repo_path="feature_repo/")

    # Get latest feature timestamp
    features = store.get_online_features(
        features=["user_features:total_orders"],
        entity_rows=[{"user_id": 1001}]
    ).to_dict()

    # Check freshness
    age = datetime.now() - features["event_timestamp"][0]

    if age > timedelta(days=2):
        alert(f"Features are {age.days} days old! Expected < 2 days")

    return {"age_days": age.days, "status": "healthy" if age.days < 2 else "stale"}
```

## Best Practices

1. **Start simple** - Begin with offline store, add online store when needed
2. **Version features** - Use feature view versions (user_features_v1, v2)
3. **Monitor freshness** - Alert when features become stale
4. **Document** - Clearly document feature definitions and business logic
5. **Test consistency** - Validate training/serving features match
6. **Use TTL** - Set appropriate time-to-live for feature freshness
7. **Batch materialize** - Materialize features in batches, not one-by-one
8. **Point-in-time joins** - Use Feast's point-in-time joins to prevent data leakage
