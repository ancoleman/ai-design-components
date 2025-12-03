"""
Feast Feature Store Complete Example

Demonstrates:
1. Feature definition
2. Data generation
3. Feature materialization
4. Online serving (low-latency)
5. Offline serving (training)
"""

import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from feast import FeatureStore, Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String
from feast.value_type import ValueType


def generate_sample_data():
    """Generate sample user features data."""

    # Sample user IDs
    user_ids = list(range(1001, 1101))  # 100 users

    # Generate features
    data = {
        "user_id": user_ids,
        "total_orders": np.random.randint(0, 100, size=len(user_ids)),
        "avg_order_value": np.random.uniform(10.0, 500.0, size=len(user_ids)),
        "lifetime_value": np.random.uniform(100.0, 5000.0, size=len(user_ids)),
        "days_since_last_order": np.random.randint(0, 365, size=len(user_ids)),
        "event_timestamp": [datetime.now() for _ in user_ids]
    }

    df = pd.DataFrame(data)

    # Save to parquet
    os.makedirs("data", exist_ok=True)
    df.to_parquet("data/user_features.parquet")

    print(f"Generated {len(df)} user feature records")
    return df


def setup_feature_store():
    """Initialize Feast feature repository."""

    # Check if feature_store.yaml exists
    if not os.path.exists("feature_store.yaml"):
        print("\nCreating feature repository...")
        os.system("feast init feature_repo")
        os.chdir("feature_repo")
        print("Feature repository created!")
    else:
        print("Feature repository already exists")


def define_features():
    """Define feature views and entities."""

    # Entity: User
    user = Entity(
        name="user",
        join_keys=["user_id"],
        description="User entity for ML features"
    )

    # Data source
    user_source = FileSource(
        path="../data/user_features.parquet",
        timestamp_field="event_timestamp"
    )

    # Feature View: User Features
    user_features = FeatureView(
        name="user_features",
        entities=[user],
        schema=[
            Field(name="total_orders", dtype=Int64),
            Field(name="avg_order_value", dtype=Float32),
            Field(name="lifetime_value", dtype=Float32),
            Field(name="days_since_last_order", dtype=Int64)
        ],
        source=user_source,
        ttl=timedelta(days=1)  # Features valid for 1 day
    )

    # Write feature definitions to features.py
    features_code = f"""
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64
from datetime import timedelta

# Entity
user = Entity(
    name="user",
    join_keys=["user_id"],
    description="User entity for ML features"
)

# Data source
user_source = FileSource(
    path="../data/user_features.parquet",
    timestamp_field="event_timestamp"
)

# Feature View
user_features = FeatureView(
    name="user_features",
    entities=[user],
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="lifetime_value", dtype=Float32),
        Field(name="days_since_last_order", dtype=Int64)
    ],
    source=user_source,
    ttl=timedelta(days=1)
)
"""

    with open("features.py", "w") as f:
        f.write(features_code)

    print("Feature definitions created in features.py")


def apply_features():
    """Apply feature definitions to registry."""
    print("\nApplying features to registry...")
    os.system("feast apply")
    print("Features applied!")


def materialize_features():
    """Materialize features to online store."""
    print("\nMaterializing features to online store...")

    store = FeatureStore(repo_path=".")

    # Materialize from start_date to now
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now()

    store.materialize(
        start_date=start_date,
        end_date=end_date
    )

    print("Features materialized!")


def demo_online_serving():
    """Demonstrate online feature serving."""
    print("\n=== Online Serving Demo ===\n")

    store = FeatureStore(repo_path=".")

    # Get features for a single user (low-latency)
    features = store.get_online_features(
        features=[
            "user_features:total_orders",
            "user_features:avg_order_value",
            "user_features:lifetime_value",
            "user_features:days_since_last_order"
        ],
        entity_rows=[{"user_id": 1001}]
    ).to_dict()

    print("Online Features for user_id=1001:")
    for key, value in features.items():
        if key != "user_id":
            print(f"  {key}: {value[0]}")


def demo_offline_serving():
    """Demonstrate offline feature serving for training."""
    print("\n=== Offline Serving Demo ===\n")

    store = FeatureStore(repo_path=".")

    # Entity dataframe (users and timestamps for training)
    entity_df = pd.DataFrame({
        "user_id": [1001, 1002, 1003, 1004, 1005],
        "event_timestamp": [
            datetime.now() for _ in range(5)
        ]
    })

    # Get historical features (point-in-time correct)
    training_data = store.get_historical_features(
        entity_df=entity_df,
        features=[
            "user_features:total_orders",
            "user_features:avg_order_value",
            "user_features:lifetime_value",
            "user_features:days_since_last_order"
        ]
    ).to_df()

    print("Training Data (Historical Features):")
    print(training_data.head())

    # Simulate training
    print("\nSimulated Model Training:")
    X = training_data[["total_orders", "avg_order_value", "lifetime_value"]]
    print(f"Training features shape: {X.shape}")
    print("Model would be trained here...")


def demo_prediction_serving():
    """Demonstrate using features for prediction."""
    print("\n=== Prediction Serving Demo ===\n")

    store = FeatureStore(repo_path=".")

    # Get features for prediction
    user_id = 1010

    features = store.get_online_features(
        features=[
            "user_features:total_orders",
            "user_features:avg_order_value",
            "user_features:lifetime_value"
        ],
        entity_rows=[{"user_id": user_id}]
    ).to_dict()

    # Create feature vector
    feature_vector = [
        features["total_orders"][0],
        features["avg_order_value"][0],
        features["lifetime_value"][0]
    ]

    print(f"Feature vector for user_id={user_id}:")
    print(f"  {feature_vector}")

    # Simulate prediction
    prediction = sum(feature_vector) / len(feature_vector)  # Dummy prediction
    print(f"\nSimulated prediction: {prediction:.2f}")


def main():
    """Main Feast feature store demo."""

    print("=== Feast Feature Store Demo ===\n")

    # Step 1: Generate sample data
    print("Step 1: Generating sample data...")
    generate_sample_data()

    # Step 2: Setup feature store
    print("\nStep 2: Setting up feature store...")
    setup_feature_store()

    # Step 3: Define features
    print("\nStep 3: Defining features...")
    define_features()

    # Step 4: Apply to registry
    print("\nStep 4: Applying features...")
    apply_features()

    # Step 5: Materialize to online store
    print("\nStep 5: Materializing features...")
    materialize_features()

    # Step 6: Demo online serving
    demo_online_serving()

    # Step 7: Demo offline serving
    demo_offline_serving()

    # Step 8: Demo prediction serving
    demo_prediction_serving()

    print("\n=== Demo Complete ===")
    print("\nKey Takeaways:")
    print("1. Features defined ONCE in features.py")
    print("2. Same features used for training (offline) and serving (online)")
    print("3. No training-serving skew!")
    print("4. Point-in-time correctness for training data")
    print("5. Low-latency online serving for predictions")


if __name__ == "__main__":
    main()
