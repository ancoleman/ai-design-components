# Feature Stores

Centralized platforms for managing, serving, and ensuring consistency of ML features between training and inference.

## Table of Contents

- [Overview](#overview)
- [Core Concepts](#core-concepts)
- [Platform Comparison](#platform-comparison)
- [Online vs Offline Serving](#online-vs-offline-serving)
- [Point-in-Time Correctness](#point-in-time-correctness)
- [Feature Versioning](#feature-versioning)
- [Real-Time Feature Computation](#real-time-feature-computation)
- [Implementation Examples](#implementation-examples)

## Overview

Feature stores solve the **training/serving skew** problem by centralizing feature definitions and ensuring identical feature logic in both training and inference.

### The Training/Serving Skew Problem

**Without Feature Store:**
```python
# Training (data scientist's notebook)
def compute_user_features(user_data):
    # Compute average purchase amount over last 30 days
    return user_data.groupby('user_id')['amount'].mean()

# Inference (production API, written 6 months later by different engineer)
def compute_user_features(user_id):
    # BUG: Uses last 7 days instead of 30 days
    return db.query(f"SELECT AVG(amount) FROM purchases WHERE user_id={user_id} AND date > NOW() - INTERVAL 7 DAYS")
```

**Result:** Model performs well in training (uses 30-day average) but fails in production (uses 7-day average).

**With Feature Store:**
```python
# Feature definition (single source of truth)
@feature_view
def user_avg_purchase_30d(user_data: DataFrame):
    return user_data.groupby('user_id')['amount'].rolling(window='30d').mean()

# Training: Fetches from offline store
training_features = feature_store.get_historical_features(
    entity_rows=training_entity_df,
    features=['user_avg_purchase_30d']
)

# Inference: Fetches from online store (same logic, different storage)
inference_features = feature_store.get_online_features(
    entity_rows={'user_id': 12345},
    features=['user_avg_purchase_30d']
)
```

**Result:** Identical feature logic guarantees consistency.

## Core Concepts

### Feature Definition

```python
# Feast feature definition
from feast import Entity, Feature, FeatureView, ValueType
from feast.data_source import FileSource

# Entity (join key)
user = Entity(
    name="user_id",
    value_type=ValueType.INT64,
    description="User identifier"
)

# Data source (offline)
user_features_source = FileSource(
    path="s3://ml-data/user_features.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# Feature view (feature definitions)
user_features_fv = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=30),  # Time-to-live in online store
    features=[
        Feature(name="total_purchases", dtype=ValueType.INT64),
        Feature(name="avg_purchase_amount", dtype=ValueType.DOUBLE),
        Feature(name="days_since_last_purchase", dtype=ValueType.INT64),
        Feature(name="favorite_category", dtype=ValueType.STRING),
    ],
    online=True,  # Enable online serving
    source=user_features_source,
    tags={"team": "growth", "version": "v2"}
)
```

### Feature Registry

Central metadata store containing:
- **Feature definitions**: Schema, types, descriptions
- **Data sources**: Offline (training) and online (inference)
- **Feature lineage**: Upstream dependencies and transformations
- **Feature statistics**: Min, max, mean, distribution
- **Access control**: Who can read/write features

### Entity

Join key for features (e.g., `user_id`, `product_id`, `transaction_id`).

```python
# Single entity
user = Entity(name="user_id", value_type=ValueType.INT64)

# Multiple entities (composite key)
user_product_interactions = FeatureView(
    name="user_product_interactions",
    entities=["user_id", "product_id"],  # Composite key
    features=[
        Feature(name="num_views", dtype=ValueType.INT64),
        Feature(name="num_purchases", dtype=ValueType.INT64),
    ],
    ...
)
```

### Time-to-Live (TTL)

Maximum age for features in online store before eviction.

```python
# Features expire after 7 days
user_features_fv = FeatureView(
    name="user_features",
    ttl=timedelta(days=7),  # Features older than 7 days evicted
    ...
)
```

**Use Cases:**
- Short TTL (hours): Real-time aggregations (recent click count)
- Medium TTL (days): User preferences, recent behavior
- Long TTL (months): Static attributes (user demographics)

## Platform Comparison

### Feast (Open-Source)

**Architecture:**
```
Offline Store                Online Store
(Training)                   (Inference)
    |                            |
Parquet/BigQuery -----------> Redis/DynamoDB
    |                            |
    └─ Point-in-Time Join        └─ Low-Latency Lookup
    └─ Historical Features       └─ Latest Features
```

**Strengths:**
- Open-source, cloud-agnostic (no vendor lock-in)
- Most popular feature store (5,000+ GitHub stars)
- Active community and growing ecosystem
- Supports multiple storage backends

**Offline Stores (Training):**
- Parquet files (S3, GCS, Azure Blob)
- BigQuery (Google Cloud)
- Snowflake
- Redshift (AWS)
- Spark (Databricks)

**Online Stores (Inference):**
- Redis (most common, low latency)
- DynamoDB (AWS, managed)
- Datastore (Google Cloud)
- SQLite (local development)

**Getting Started:**
```bash
# Install Feast
pip install feast

# Initialize Feast repository
feast init feature_repo
cd feature_repo

# Define features (edit feature_repo/features.py)

# Apply to registry
feast apply

# Materialize to online store
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

**Limitations:**
- No built-in UI (third-party: Feast UI)
- Manual materialization scheduling (use Airflow/cron)
- No integrated monitoring (external tools needed)

### Tecton (Managed, Enterprise)

**Strengths:**
- Fully managed service (no infrastructure management)
- Feast-compatible API (can migrate from Feast)
- Integrated monitoring and alerting
- Real-time feature computation (streaming)
- Multi-cloud support (AWS, GCP, Azure)

**Architecture:**
```
Data Sources
    |
Tecton Transformation Engine
    |
    ├─ Batch Features (scheduled)
    |  └─ Offline Store (S3/GCS)
    |
    ├─ Stream Features (Kafka/Kinesis)
    |  └─ Online Store (DynamoDB/Redis)
    |
    └─ Real-Time Features (on-demand)
       └─ Computed at request time
```

**Feature Types:**
1. **Batch Features**: Pre-computed, scheduled (hourly/daily)
2. **Stream Features**: Real-time aggregations (Kafka, Kinesis)
3. **On-Demand Features**: Computed at request time (lightweight)

**Pricing:**
- Enterprise-focused: $$$$ (contact sales)
- Consumption-based: Feature reads, materialization compute

**When to Choose:**
- Need managed solution (no DevOps burden)
- Real-time features critical (streaming aggregations)
- Enterprise budget available
- Multi-cloud deployment

### Hopsworks (Self-Hosted with UI)

**Strengths:**
- Open-source with full-featured UI
- Python SDK and SQL interface
- Integrated notebook environment
- Feature monitoring built-in
- RonDB for ultra-low-latency online serving (<1ms)

**Architecture:**
```
Hopsworks Platform
    |
    ├─ Feature Store
    |  ├─ Offline: Hive, S3, JDBC
    |  └─ Online: RonDB (NDB Cluster)
    |
    ├─ Feature Monitoring
    |  └─ Data validation, drift detection
    |
    └─ UI (feature catalog, lineage)
```

**When to Choose:**
- Need UI for data scientists
- Self-hosted requirement
- Ultra-low-latency serving (<1ms)

### SageMaker Feature Store (AWS)

**Strengths:**
- Integrated with AWS ML ecosystem
- Fully managed (no infrastructure)
- Point-in-time queries built-in
- Automatic data quality monitoring

**Architecture:**
```
Offline Store: S3 (Glue Data Catalog)
Online Store: DynamoDB (managed)
```

**Limitations:**
- AWS lock-in (cannot migrate to other clouds)
- Higher cost than self-hosted alternatives
- Less flexible than Feast

**When to Choose:**
- Already using AWS SageMaker
- Need managed AWS solution
- AWS-only deployment acceptable

### Databricks Feature Store

**Strengths:**
- Integrated with Databricks notebooks and Delta Lake
- Unity Catalog integration (governance)
- Automatic feature lineage tracking
- No separate infrastructure needed

**Limitations:**
- Databricks lock-in
- Online serving requires external store (Cosmos DB, DynamoDB)

**When to Choose:**
- Already using Databricks
- Need Unity Catalog governance

### Vertex AI Feature Store (GCP)

**Strengths:**
- Integrated with GCP Vertex AI
- Fully managed
- BigQuery and Bigtable storage

**Limitations:**
- GCP lock-in
- Smaller ecosystem than Feast

**When to Choose:**
- Using GCP Vertex AI
- Need managed GCP solution

## Online vs Offline Serving

### Offline Store (Training)

**Purpose:** Historical features for model training and backtesting.

**Storage:** Data warehouses, object storage
- Parquet files (S3, GCS, Azure Blob)
- BigQuery, Snowflake, Redshift
- Delta Lake (Databricks)

**Access Pattern:**
- Batch queries: Millions of rows
- Point-in-time joins: Features as of specific timestamps
- Latency: Seconds to minutes acceptable

**Example Query:**
```python
# Fetch historical features for training
training_df = feature_store.get_historical_features(
    entity_df=entity_df,  # DataFrame with entity IDs and timestamps
    features=[
        'user_features:total_purchases',
        'user_features:avg_purchase_amount',
        'user_features:days_since_last_purchase',
    ]
)

# entity_df:
#   user_id | event_timestamp
#   --------|------------------
#   123     | 2023-06-01 10:00
#   456     | 2023-06-01 11:00
#   789     | 2023-06-01 12:00

# Result: Features as of each timestamp (point-in-time correctness)
```

### Online Store (Inference)

**Purpose:** Low-latency feature retrieval for real-time predictions.

**Storage:** Key-value stores
- Redis (most common): <10ms latency
- DynamoDB (AWS managed): <10ms latency
- Bigtable (GCP): <10ms latency
- RonDB (Hopsworks): <1ms latency

**Access Pattern:**
- Single-row lookups: Fetch features for one entity
- Latency: <10ms (P99)
- High throughput: 10K+ requests/second

**Example Query:**
```python
# Fetch latest features for inference
features = feature_store.get_online_features(
    features=[
        'user_features:total_purchases',
        'user_features:avg_purchase_amount',
        'user_features:days_since_last_purchase',
    ],
    entity_rows=[{'user_id': 123}]
).to_dict()

# Result: Latest feature values for user 123
# {
#   'user_id': [123],
#   'total_purchases': [42],
#   'avg_purchase_amount': [87.50],
#   'days_since_last_purchase': [3]
# }
```

### Materialization (Offline → Online)

**Process:** Copy features from offline store to online store for low-latency serving.

```python
# Feast materialization
from datetime import datetime, timedelta

# Materialize last 7 days of features
feature_store.materialize(
    start_date=datetime.now() - timedelta(days=7),
    end_date=datetime.now()
)

# Incremental materialization (only new data)
feature_store.materialize_incremental(
    end_date=datetime.now()
)
```

**Scheduling:** Use Airflow, cron, or cloud scheduler
```python
# Airflow DAG
from airflow import DAG
from airflow.operators.python import PythonOperator

def materialize_features():
    feature_store.materialize_incremental(datetime.now())

dag = DAG('materialize_features', schedule_interval='@hourly')

materialize_task = PythonOperator(
    task_id='materialize',
    python_callable=materialize_features,
    dag=dag
)
```

## Point-in-Time Correctness

Ensure no future data leakage during training by only using features available at prediction time.

### The Problem: Data Leakage

**Incorrect (future data leakage):**
```python
# Training at 2023-06-01 10:00
# BUG: Uses all data including future transactions
user_features = df.groupby('user_id').agg({
    'amount': 'sum',  # Includes purchases AFTER 2023-06-01 10:00
    'num_purchases': 'count'
})
```

**Correct (point-in-time):**
```python
# Training at 2023-06-01 10:00
# Only uses data BEFORE 2023-06-01 10:00
user_features = df[df['timestamp'] < '2023-06-01 10:00'].groupby('user_id').agg({
    'amount': 'sum',
    'num_purchases': 'count'
})
```

### Point-in-Time Join Implementation

**Manual (Error-Prone):**
```python
# Manual point-in-time join (easy to get wrong)
def point_in_time_join(events, features):
    result = []
    for event in events:
        entity_id = event['user_id']
        event_time = event['timestamp']

        # Find latest feature values BEFORE event_time
        feature_row = features[
            (features['user_id'] == entity_id) &
            (features['timestamp'] < event_time)
        ].sort_values('timestamp', ascending=False).iloc[0]

        result.append({**event, **feature_row})

    return result
```

**Feature Store (Automatic):**
```python
# Feast handles point-in-time join automatically
training_df = feature_store.get_historical_features(
    entity_df=events_df,  # Contains user_id and event_timestamp
    features=['user_features:total_purchases', 'user_features:avg_amount']
)
# Result: Features as of each event_timestamp (no future data)
```

### Visualization

```
Timeline for user 123:

Time:       10:00    11:00    12:00    13:00    14:00
            |        |        |        |        |
Features:   [v1] ----+------- [v2] ----+------- [v3]
                     |                 |
Training:       [Event A]         [Event B]
                Fetches v1        Fetches v2

Event A (11:00): Uses features v1 (computed at 10:00)
Event B (13:00): Uses features v2 (computed at 12:00)

Never uses features v3 (computed at 14:00) for events A or B.
```

## Feature Versioning

Track feature schema changes and maintain backward compatibility.

### Versioning Strategies

**1. Schema Evolution (Backward Compatible)**
```python
# Version 1: Initial features
user_features_v1 = FeatureView(
    name="user_features",
    features=[
        Feature(name="total_purchases", dtype=ValueType.INT64),
        Feature(name="avg_purchase_amount", dtype=ValueType.DOUBLE),
    ],
    ...
)

# Version 2: Add new feature (backward compatible)
user_features_v2 = FeatureView(
    name="user_features",
    features=[
        Feature(name="total_purchases", dtype=ValueType.INT64),
        Feature(name="avg_purchase_amount", dtype=ValueType.DOUBLE),
        Feature(name="days_since_last_purchase", dtype=ValueType.INT64),  # NEW
    ],
    ...
)
# Old models continue using v1 features
# New models can use v2 features
```

**2. Feature View Versioning (Breaking Changes)**
```python
# Breaking change: Rename or change dtype
user_features_v1 = FeatureView(name="user_features_v1", ...)
user_features_v2 = FeatureView(name="user_features_v2", ...)

# Model metadata tracks which version used
model_metadata = {
    'model_version': 'v2.0',
    'features': ['user_features_v2:total_purchases', 'user_features_v2:avg_amount'],
    'feature_store_commit': 'abc123'  # Git commit of feature definitions
}
```

**3. Git-Based Versioning**
```bash
# Feature definitions in Git
git tag v1.0.0  # Tag feature store version

# Model tracks Git tag
model_metadata = {
    'feature_store_version': 'v1.0.0'
}
```

### Feature Deprecation

```python
# Mark feature as deprecated
user_features_fv = FeatureView(
    name="user_features",
    features=[
        Feature(
            name="legacy_field",
            dtype=ValueType.STRING,
            labels={"deprecated": "true", "deprecation_date": "2024-12-31"}
        ),
    ],
    ...
)
```

## Real-Time Feature Computation

Compute features on-demand at request time for ultra-fresh features.

### Stream Features (Kafka/Kinesis)

**Use Case:** Real-time aggregations (clicks in last 5 minutes, recent transactions).

```python
# Tecton stream feature
from tecton import stream_feature_view, Aggregation
from datetime import timedelta

@stream_feature_view(
    source=user_clicks_stream,  # Kafka topic
    entities=[user],
    mode='spark_sql',
    online=True,
    offline=True,
    features=[
        Aggregation(
            column='click_count',
            function='sum',
            time_window=timedelta(minutes=5)
        ),
        Aggregation(
            column='click_count',
            function='sum',
            time_window=timedelta(hours=1)
        ),
    ],
    tags={'team': 'growth'}
)
def user_click_counts(user_clicks):
    return user_clicks.select('user_id', 'click_count', 'timestamp')
```

**Architecture:**
```
Kafka Topic (user_clicks)
    |
Stream Processor (Flink/Spark Streaming)
    |
Compute Aggregations (5min, 1hr windows)
    |
    ├─ Online Store (Redis) - Latest values
    └─ Offline Store (S3) - Historical values
```

### On-Demand Features

**Use Case:** Lightweight transformations computed at request time.

```python
# Feast on-demand feature
from feast import on_demand_feature_view, Field
from feast.types import Float64

@on_demand_feature_view(
    sources=[user_features_fv],
    schema=[
        Field(name="purchase_frequency_per_day", dtype=Float64),
    ],
)
def user_derived_features(inputs: pd.DataFrame) -> pd.DataFrame:
    """Compute on-demand features at request time."""
    df = pd.DataFrame()
    df['purchase_frequency_per_day'] = (
        inputs['total_purchases'] / inputs['days_since_signup']
    )
    return df
```

**When to Use:**
- Lightweight transformations (<1ms compute)
- Derived from existing features
- No need to pre-compute and store

**When NOT to Use:**
- Heavy computation (>10ms)
- Need offline store for training
- Complex aggregations

## Implementation Examples

### Example 1: Feast Setup (Local Development)

```bash
# Install Feast
pip install feast

# Initialize repository
feast init feature_repo
cd feature_repo
```

**Define features (`feature_repo/features.py`):**
```python
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float64, Int64, String

# Entity
user = Entity(
    name="user_id",
    description="User identifier"
)

# Data source (offline)
user_features_source = FileSource(
    path="data/user_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# Feature view
user_features_fv = FeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=30),
    schema=[
        Field(name="total_purchases", dtype=Int64),
        Field(name="avg_purchase_amount", dtype=Float64),
        Field(name="favorite_category", dtype=String),
    ],
    online=True,
    source=user_features_source,
    tags={"team": "growth"}
)
```

**Apply to registry:**
```bash
feast apply
```

**Generate training data:**
```python
from feast import FeatureStore
from datetime import datetime

fs = FeatureStore(repo_path=".")

# Entity dataframe (events to fetch features for)
entity_df = pd.DataFrame({
    'user_id': [1, 2, 3],
    'event_timestamp': [
        datetime(2023, 6, 1, 10, 0),
        datetime(2023, 6, 1, 11, 0),
        datetime(2023, 6, 1, 12, 0),
    ]
})

# Fetch historical features (point-in-time join)
training_df = fs.get_historical_features(
    entity_df=entity_df,
    features=['user_features:total_purchases', 'user_features:avg_purchase_amount']
).to_df()

print(training_df)
```

**Materialize to online store:**
```python
# Materialize to Redis/SQLite
fs.materialize_incremental(end_date=datetime.now())

# Fetch online features (inference)
online_features = fs.get_online_features(
    features=['user_features:total_purchases', 'user_features:avg_purchase_amount'],
    entity_rows=[{'user_id': 1}, {'user_id': 2}]
).to_dict()

print(online_features)
```

### Example 2: Feast with Redis (Production)

**`feature_store.yaml`:**
```yaml
project: fraud_detection
registry: s3://ml-feature-store/registry.db
provider: aws

online_store:
  type: redis
  connection_string: "redis.example.com:6379,password=secret"

offline_store:
  type: file
  path: s3://ml-feature-store/offline
```

**Materialize to Redis (scheduled):**
```python
# materialize_job.py
from feast import FeatureStore
from datetime import datetime, timedelta
import schedule
import time

fs = FeatureStore(repo_path=".")

def materialize_features():
    """Materialize last 1 hour of features to Redis."""
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=1)

    print(f"Materializing {start_date} to {end_date}")
    fs.materialize(start_date=start_date, end_date=end_date)
    print("Materialization complete")

# Schedule hourly
schedule.every().hour.do(materialize_features)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 3: Feature Store Integration in ML Pipeline

```python
# train.py
from feast import FeatureStore
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import mlflow

# Initialize feature store
fs = FeatureStore(repo_path=".")

# Entity dataframe (training labels)
labels_df = pd.read_parquet("s3://ml-data/labels.parquet")
# Columns: user_id, event_timestamp, is_fraud (label)

# Fetch historical features (point-in-time join)
training_df = fs.get_historical_features(
    entity_df=labels_df[['user_id', 'event_timestamp']],
    features=[
        'user_features:total_purchases',
        'user_features:avg_purchase_amount',
        'transaction_features:amount',
        'transaction_features:merchant_category',
    ]
).to_df()

# Merge with labels
training_df = training_df.merge(labels_df[['user_id', 'event_timestamp', 'is_fraud']], on=['user_id', 'event_timestamp'])

# Train model
X = training_df.drop(columns=['user_id', 'event_timestamp', 'is_fraud'])
y = training_df['is_fraud']

model = RandomForestClassifier()
model.fit(X, y)

# Log to MLflow with feature metadata
with mlflow.start_run():
    mlflow.log_param("features", list(X.columns))
    mlflow.log_param("feature_store_commit", get_git_commit())
    mlflow.sklearn.log_model(model, "model")
```

```python
# predict.py (inference)
from feast import FeatureStore
import mlflow

fs = FeatureStore(repo_path=".")
model = mlflow.sklearn.load_model("models:/fraud-detection/production")

def predict_fraud(user_id, transaction_data):
    """Real-time fraud prediction."""

    # Fetch online features (from Redis)
    features = fs.get_online_features(
        features=[
            'user_features:total_purchases',
            'user_features:avg_purchase_amount',
            'transaction_features:amount',
            'transaction_features:merchant_category',
        ],
        entity_rows=[{
            'user_id': user_id,
            'transaction_id': transaction_data['transaction_id']
        }]
    ).to_dict()

    # Convert to model input format
    X = pd.DataFrame(features)

    # Predict
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]

    return {
        'is_fraud': bool(prediction),
        'fraud_probability': float(probability)
    }
```

### Example 4: Feature Monitoring

```python
# monitor_features.py
from feast import FeatureStore
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd

fs = FeatureStore(repo_path=".")

# Fetch reference dataset (training data)
reference_df = fs.get_historical_features(
    entity_df=reference_entities,
    features=['user_features:total_purchases', 'user_features:avg_purchase_amount']
).to_df()

# Fetch current dataset (recent production data)
current_df = fs.get_historical_features(
    entity_df=current_entities,
    features=['user_features:total_purchases', 'user_features:avg_purchase_amount']
).to_df()

# Detect drift
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference_df, current_data=current_df)

# Save report
report.save_html("feature_drift_report.html")

# Check if drift detected
drift_results = report.as_dict()
if drift_results['metrics'][0]['result']['dataset_drift']:
    print("⚠️  DRIFT DETECTED in features")
    # Trigger retraining pipeline
else:
    print("✓ No drift detected")
```
