"""
Feast Feature Store Example

Demonstrates feature store patterns including:
- Feature definitions and entity relationships
- Online/offline feature serving
- Point-in-time correct feature retrieval
- Feature freshness and materialization
"""

from datetime import datetime, timedelta
from feast import Entity, Feature, FeatureView, FileSource, ValueType, Field
from feast.types import Float32, Int64, String
from feast import FeatureStore
import pandas as pd
import numpy as np


# =============================================================================
# Feature Definitions (feature_repo/features.py)
# =============================================================================

# Define entities (primary keys for feature lookup)
customer = Entity(
    name="customer_id",
    description="Unique customer identifier",
    value_type=ValueType.INT64,
)

product = Entity(
    name="product_id",
    description="Unique product identifier",
    value_type=ValueType.INT64,
)

# Define data source (offline store)
customer_features_source = FileSource(
    path="data/customer_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

transaction_features_source = FileSource(
    path="data/transaction_features.parquet",
    timestamp_field="event_timestamp",
)

# Define feature views (logical groupings of features)
customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    ttl=timedelta(days=90),  # Feature freshness window
    schema=[
        Field(name="total_purchases", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="customer_segment", dtype=String),
        Field(name="lifetime_value", dtype=Float32),
        Field(name="days_since_last_purchase", dtype=Int64),
    ],
    source=customer_features_source,
    online=True,  # Enable online serving
)

transaction_features = FeatureView(
    name="transaction_features",
    entities=[customer, product],
    ttl=timedelta(days=30),
    schema=[
        Field(name="purchase_count_7d", dtype=Int64),
        Field(name="purchase_count_30d", dtype=Int64),
        Field(name="avg_quantity", dtype=Float32),
        Field(name="total_spend_30d", dtype=Float32),
    ],
    source=transaction_features_source,
    online=True,
)


# =============================================================================
# Feature Store Operations
# =============================================================================

def create_sample_data():
    """Generate sample feature data for demonstration."""
    np.random.seed(42)
    n_customers = 1000
    n_products = 100

    # Customer features
    customer_data = pd.DataFrame({
        "customer_id": range(1, n_customers + 1),
        "total_purchases": np.random.randint(1, 100, n_customers),
        "avg_order_value": np.random.uniform(20, 500, n_customers).astype(np.float32),
        "customer_segment": np.random.choice(["bronze", "silver", "gold", "platinum"], n_customers),
        "lifetime_value": np.random.uniform(100, 10000, n_customers).astype(np.float32),
        "days_since_last_purchase": np.random.randint(0, 365, n_customers),
        "event_timestamp": datetime.now() - timedelta(hours=1),
        "created_timestamp": datetime.now() - timedelta(days=30),
    })

    # Transaction features (customer x product combinations)
    n_transactions = 5000
    transaction_data = pd.DataFrame({
        "customer_id": np.random.randint(1, n_customers + 1, n_transactions),
        "product_id": np.random.randint(1, n_products + 1, n_transactions),
        "purchase_count_7d": np.random.randint(0, 10, n_transactions),
        "purchase_count_30d": np.random.randint(0, 50, n_transactions),
        "avg_quantity": np.random.uniform(1, 10, n_transactions).astype(np.float32),
        "total_spend_30d": np.random.uniform(0, 1000, n_transactions).astype(np.float32),
        "event_timestamp": datetime.now() - timedelta(hours=1),
    })

    return customer_data, transaction_data


def initialize_feature_store(repo_path: str = "feature_repo"):
    """
    Initialize Feast feature store.

    Run `feast apply` to register feature definitions:
    $ cd feature_repo && feast apply
    """
    store = FeatureStore(repo_path=repo_path)
    return store


def materialize_features(store: FeatureStore, end_date: datetime = None):
    """
    Materialize features from offline to online store.

    This populates the online store (Redis/DynamoDB) for low-latency serving.
    Should be run on a schedule (e.g., hourly) to keep features fresh.
    """
    if end_date is None:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=7)

    store.materialize(
        start_date=start_date,
        end_date=end_date,
    )
    print(f"Features materialized from {start_date} to {end_date}")


def get_online_features(store: FeatureStore, customer_ids: list):
    """
    Retrieve features from online store for real-time inference.

    Typical latency: <10ms for Redis online store
    Use case: Real-time recommendation, fraud detection
    """
    entity_rows = [{"customer_id": cid} for cid in customer_ids]

    features = store.get_online_features(
        features=[
            "customer_features:total_purchases",
            "customer_features:avg_order_value",
            "customer_features:customer_segment",
            "customer_features:lifetime_value",
        ],
        entity_rows=entity_rows,
    ).to_df()

    return features


def get_historical_features(
    store: FeatureStore,
    entity_df: pd.DataFrame,
):
    """
    Retrieve point-in-time correct features for training.

    Entity dataframe must include:
    - Entity columns (customer_id, product_id)
    - event_timestamp column for point-in-time join

    Feast ensures features are retrieved as they existed at event_timestamp,
    preventing data leakage in training.
    """
    training_data = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "customer_features:total_purchases",
            "customer_features:avg_order_value",
            "customer_features:customer_segment",
            "customer_features:lifetime_value",
            "customer_features:days_since_last_purchase",
        ],
    ).to_df()

    return training_data


def create_training_dataset(store: FeatureStore):
    """
    Create training dataset with point-in-time correct features.

    This pattern ensures training data reflects the state of features
    at the time of each historical event, preventing future data leakage.
    """
    # Historical events with timestamps
    events = pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5] * 100,
        "event_timestamp": pd.date_range(
            start=datetime.now() - timedelta(days=90),
            periods=500,
            freq="H"
        ),
        "label": np.random.randint(0, 2, 500),  # Target variable
    })

    # Get point-in-time correct features
    training_df = get_historical_features(store, events)

    print(f"Training dataset shape: {training_df.shape}")
    print(f"Features: {training_df.columns.tolist()}")

    return training_df


# =============================================================================
# Feature Store Configuration (feature_repo/feature_store.yaml)
# =============================================================================

FEATURE_STORE_CONFIG = """
project: ml_platform
registry: data/registry.db
provider: local

online_store:
  type: redis
  connection_string: "localhost:6379"

offline_store:
  type: file

entity_key_serialization_version: 2
"""


# =============================================================================
# Production Patterns
# =============================================================================

def production_inference_example():
    """
    Production inference pattern using Feast.

    1. Receive prediction request with entity IDs
    2. Fetch features from online store (<10ms)
    3. Combine with request features
    4. Run model inference
    5. Return prediction
    """
    store = initialize_feature_store()

    # Incoming request
    request = {
        "customer_id": 123,
        "product_id": 456,
        "request_features": {
            "device_type": "mobile",
            "time_of_day": "evening",
        }
    }

    # Fetch stored features
    online_features = get_online_features(store, [request["customer_id"]])

    # Combine all features
    model_input = {
        **request["request_features"],
        **online_features.iloc[0].to_dict(),
    }

    print(f"Model input features: {model_input}")
    # model.predict(model_input)


if __name__ == "__main__":
    # Generate sample data
    customer_df, transaction_df = create_sample_data()
    print(f"Customer features shape: {customer_df.shape}")
    print(f"Transaction features shape: {transaction_df.shape}")

    # In production, you would:
    # 1. Save data to parquet files
    # 2. Run `feast apply` to register features
    # 3. Run `feast materialize` to populate online store
    # 4. Use get_online_features for inference

    print("\nFeature store configuration:")
    print(FEATURE_STORE_CONFIG)
