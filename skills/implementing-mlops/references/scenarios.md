# MLOps Scenarios

Common MLOps implementation scenarios with recommended tool stacks and architectures.

## Table of Contents

- [Startup MLOps Stack](#startup-mlops-stack)
- [Growth Company Stack](#growth-company-stack)
- [Enterprise Stack](#enterprise-stack)
- [Real-Time ML Systems](#real-time-ml-systems)
- [Batch Prediction Systems](#batch-prediction-systems)
- [LLMOps Implementation](#llmops-implementation)

## Startup MLOps Stack

**Context:** 10-50 person startup, 3-5 data scientists, 3-5 models in production, limited budget, fast iteration needed.

### Recommended Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Experiment Tracking | MLflow (self-hosted) | Free, adequate features, self-hosted on EC2 |
| Model Serving | BentoML | Easiest deployment, fast iteration |
| Pipeline Orchestration | Prefect or cron jobs | Simpler than Airflow, sufficient for <10 pipelines |
| Monitoring | Prometheus + basic drift detection | Open-source, low overhead |
| Feature Store | Skip initially, use database tables | Avoid over-engineering early |
| Infrastructure | AWS (EC2, S3, RDS) | Pay-as-you-go, mature ecosystem |

### Architecture

```
Data Lake (S3)
    |
Cron Job (daily training)
    |
Training Script (Python)
    |
MLflow (EC2 instance)
    |
BentoML (Docker containers)
    |
AWS ALB (load balancer)
    |
Production Traffic
```

### Implementation

```python
# training_pipeline.py (run via cron)
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import bentoml

def train_and_deploy():
    """Simple training and deployment pipeline."""

    # Load data
    df = pd.read_parquet('s3://ml-data/train.parquet')
    X = df.drop('label', axis=1)
    y = df['label']

    # Train
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    # Log to MLflow
    with mlflow.start_run():
        mlflow.log_param('n_estimators', 100)
        mlflow.log_metric('accuracy', model.score(X, y))
        mlflow.sklearn.log_model(model, 'model')

    # Save to BentoML
    bentoml.sklearn.save_model('fraud_detection', model)

    print("Model trained and saved")

# Cron: 0 2 * * * python training_pipeline.py
```

```python
# bentoml_service.py
import bentoml
from bentoml.io import JSON, NumpyNdarray

fraud_detection_runner = bentoml.sklearn.get("fraud_detection:latest").to_runner()
svc = bentoml.Service("fraud_detection", runners=[fraud_detection_runner])

@svc.api(input=NumpyNdarray(), output=JSON())
def predict(features):
    result = fraud_detection_runner.predict.run(features)
    return {"prediction": int(result[0])}

# Deploy: bentoml containerize fraud_detection:latest
```

### Infrastructure Cost Estimate

- EC2 (MLflow server): $50/month (t3.medium)
- EC2 (BentoML serving): $100/month (2x t3.medium)
- S3 (data storage): $50/month (1TB)
- RDS (MLflow database): $50/month (db.t3.small)
- **Total: ~$250/month**

### When to Upgrade

- When reaching 10+ models in production
- When feature engineering becomes complex (add feature store)
- When manual deployment becomes bottleneck (add CI/CD)

## Growth Company Stack

**Context:** 50-500 people, 10-20 data scientists, 20-50 models, $100K+ ML budget, need team collaboration.

### Recommended Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Experiment Tracking | Weights & Biases or MLflow | W&B for collaboration, MLflow if cost-sensitive |
| Model Serving | KServe or BentoML | Kubernetes-native, auto-scaling |
| Pipeline Orchestration | Kubeflow Pipelines or Airflow | ML-specific pipelines, reusable components |
| Monitoring | Evidently + Prometheus + Grafana | Drift detection + performance monitoring |
| Feature Store | Feast | Open-source, production-ready, cloud-agnostic |
| Infrastructure | Kubernetes (EKS/GKE) | Scalable, standardized deployment |

### Architecture

```
Data Warehouse (Snowflake)
    |
Feature Store (Feast)
    |    └─ Offline: Snowflake
    |    └─ Online: Redis
    |
Kubeflow Pipelines (daily training)
    |    └─ Data Validation
    |    └─ Training
    |    └─ Evaluation
    |    └─ Registration (MLflow)
    |
KServe (model serving on Kubernetes)
    |    └─ Auto-scaling
    |    └─ Canary deployments
    |
API Gateway
    |
Production Traffic
```

### Implementation

```python
# kubeflow_pipeline.py
import kfp
from kfp import dsl

@dsl.component
def fetch_features(entity_df_path: str, output_path: dsl.OutputPath()):
    """Fetch features from Feast."""
    from feast import FeatureStore
    import pandas as pd

    fs = FeatureStore(repo_path='.')
    entity_df = pd.read_parquet(entity_df_path)

    training_df = fs.get_historical_features(
        entity_df=entity_df,
        features=['user_features:total_purchases', 'user_features:avg_amount']
    ).to_df()

    training_df.to_parquet(output_path)

@dsl.component
def train_model(training_data_path: dsl.InputPath(), model_path: dsl.OutputPath()):
    """Train model with MLflow tracking."""
    import mlflow
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_parquet(training_data_path)
    X = df.drop('label', axis=1)
    y = df['label']

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=200)
        model.fit(X, y)

        mlflow.log_metric('accuracy', model.score(X, y))
        mlflow.sklearn.log_model(model, 'model', registered_model_name='fraud_detection')

    # Save for deployment
    import pickle
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

@dsl.component
def deploy_to_kserve(model_path: dsl.InputPath()):
    """Deploy model to KServe."""
    import subprocess

    # Create InferenceService
    inference_service = """
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: fraud-detection
spec:
  predictor:
    sklearn:
      storageUri: "s3://models/fraud-detection"
"""

    subprocess.run(['kubectl', 'apply', '-f', '-'], input=inference_service.encode())

@dsl.pipeline(name='fraud-detection-pipeline')
def training_pipeline(entity_df_path: str):
    """Complete training pipeline."""

    fetch_task = fetch_features(entity_df_path=entity_df_path)
    train_task = train_model(training_data_path=fetch_task.output)
    deploy_task = deploy_to_kserve(model_path=train_task.output)

# Compile and run
kfp.compiler.Compiler().compile(training_pipeline, 'pipeline.yaml')
```

### Infrastructure Cost Estimate

- EKS cluster: $150/month (control plane)
- Worker nodes: $1,000/month (10x m5.xlarge)
- RDS (MLflow): $200/month (db.m5.large)
- S3 (data + models): $200/month
- Snowflake: $2,000/month (based on usage)
- Weights & Biases: $4,000/month (20 users x $200/user)
- **Total: ~$7,500/month**

### Team Structure

- ML Platform Team (3-5 engineers): Maintain MLOps infrastructure
- Data Science Teams (15-20 data scientists): Build models
- ML Engineers (5-10): Deploy models, optimize serving

## Enterprise Stack

**Context:** 500+ people, 50+ data scientists, 100+ models, regulatory compliance, multi-cloud, $500K+ budget.

### Recommended Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Experiment Tracking | MLflow (self-hosted) or Neptune.ai | MLflow for cost, Neptune for compliance |
| Model Serving | Seldon Core | Advanced deployments, explainability |
| Pipeline Orchestration | Kubeflow Pipelines | ML-native, enterprise-grade |
| Monitoring | Evidently + Prometheus + Grafana + PagerDuty | Comprehensive monitoring + alerting |
| Feature Store | Feast (self-hosted) | Cloud-agnostic, full control |
| Governance | Custom platform + MLflow | Audit trails, approval workflows |
| Infrastructure | Multi-cloud Kubernetes (EKS + GKE) | Avoid vendor lock-in |

### Architecture

```
Multi-Cloud Data Lake (S3 + GCS)
    |
Feature Store (Feast)
    |    └─ Offline: Snowflake
    |    └─ Online: Redis Cluster (HA)
    |
Kubeflow Pipelines (on-demand + scheduled)
    |    └─ Data Validation (Great Expectations)
    |    └─ Training (distributed on GPUs)
    |    └─ Evaluation (fairness, explainability)
    |    └─ Registration (MLflow)
    |    └─ Approval Workflow
    |
Seldon Core (multi-cluster deployment)
    |    └─ Canary, A/B testing
    |    └─ Explainability (Alibi)
    |    └─ Auto-scaling (HPA + KEDA)
    |
API Gateway (Kong)
    |
Production Traffic (multi-region)
    |
Monitoring Stack
    └─ Evidently (drift detection)
    └─ Prometheus (metrics)
    └─ Grafana (dashboards)
    └─ PagerDuty (alerting)
    └─ ELK (logs)
```

### Governance Workflow

```python
# governance_pipeline.py
class EnterpriseGovernancePipeline:
    """Enterprise model governance pipeline."""

    def register_model(self, model, metadata):
        """Register model with governance checks."""

        # 1. Validation checks
        checks = self.validate_model(model, metadata)

        if not checks['passed']:
            raise ValueError(f"Validation failed: {checks['failures']}")

        # 2. Register to MLflow
        with mlflow.start_run():
            mlflow.sklearn.log_model(model, 'model', registered_model_name=metadata['name'])

            # Log compliance metadata
            mlflow.set_tags({
                'regulatory_framework': 'EU_AI_ACT',
                'risk_classification': 'HIGH_RISK',
                'model_card_url': metadata['model_card_url'],
                'fairness_validated': 'true'
            })

        # 3. Approval workflow
        approval_request = self.create_approval_request(
            model_name=metadata['name'],
            approvers=['risk_manager@company.com', 'vp_engineering@company.com']
        )

        # Wait for approval (async)
        return approval_request

    def validate_model(self, model, metadata):
        """Comprehensive validation."""
        checks = {'passed': True, 'failures': []}

        # Accuracy threshold
        if metadata['accuracy'] < 0.85:
            checks['passed'] = False
            checks['failures'].append('Accuracy below threshold')

        # Fairness check
        if metadata.get('demographic_parity_diff', 1.0) > 0.1:
            checks['passed'] = False
            checks['failures'].append('Fairness violation')

        # Model card
        if not metadata.get('model_card_url'):
            checks['passed'] = False
            checks['failures'].append('Model card missing')

        # Security scan
        if not metadata.get('security_scan_passed'):
            checks['passed'] = False
            checks['failures'].append('Security scan not passed')

        # Load test
        if not metadata.get('load_test_passed'):
            checks['passed'] = False
            checks['failures'].append('Load test not passed')

        return checks
```

### Infrastructure Cost Estimate

- Multi-cloud Kubernetes: $5,000/month (EKS + GKE control plane + nodes)
- GPUs (training): $10,000/month (10x p3.2xlarge for training workloads)
- RDS (MLflow + metadata): $1,000/month (db.r5.2xlarge HA)
- Redis Cluster (feature store): $2,000/month (HA, multi-AZ)
- Snowflake: $10,000/month (enterprise usage)
- S3 + GCS: $1,000/month
- Neptune.ai (optional): $15,000/month (50 users)
- Observability (Datadog/New Relic): $5,000/month
- **Total: ~$50,000/month**

### Team Structure

- ML Platform Team (15-20 engineers): Build and maintain platform
- Data Science Teams (50+ data scientists): Build models
- ML Engineering Teams (20-30): Deploy, optimize, monitor models
- ML Governance Team (5-10): Compliance, risk management

## Real-Time ML Systems

**Context:** Low-latency predictions (<10ms), high throughput (10K+ RPS), streaming data.

### Architecture

```
Kafka (streaming data)
    |
Real-Time Feature Computation (Flink/Spark Streaming)
    |    └─ Compute features on-the-fly
    |    └─ Write to feature store (online)
    |
Feature Store Online (Redis/DynamoDB)
    |
Model Serving (Triton Inference Server / TorchServe)
    |    └─ GPU inference
    |    └─ Batching (micro-batches)
    |    └─ Model optimization (TensorRT)
    |
gRPC API (low latency)
    |
Application (real-time decision)
```

### Implementation

```python
# realtime_feature_computation.py (Flink)
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

# Source: Kafka
t_env.execute_sql("""
    CREATE TABLE transactions (
        user_id BIGINT,
        amount DOUBLE,
        merchant_category STRING,
        event_time TIMESTAMP(3)
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'transactions',
        'properties.bootstrap.servers' = 'localhost:9092'
    )
""")

# Real-time aggregation (last 5 minutes)
t_env.execute_sql("""
    CREATE TABLE user_features AS
    SELECT
        user_id,
        COUNT(*) as txn_count_5m,
        SUM(amount) as total_amount_5m,
        AVG(amount) as avg_amount_5m
    FROM transactions
    GROUP BY TUMBLE(event_time, INTERVAL '5' MINUTE), user_id
""")

# Sink: Redis (feature store online)
t_env.execute_sql("""
    CREATE TABLE feature_store_online (
        user_id BIGINT,
        features STRING
    ) WITH (
        'connector' = 'redis',
        'redis.host' = 'localhost',
        'redis.port' = '6379'
    )
""")

# Write to feature store
t_env.execute_sql("""
    INSERT INTO feature_store_online
    SELECT user_id, CAST(ROW(txn_count_5m, total_amount_5m, avg_amount_5m) AS STRING)
    FROM user_features
""")
```

### Serving Optimization

```python
# triton_serving.py (NVIDIA Triton Inference Server)
# Model optimized with TensorRT for <5ms latency

# triton_config.pbtxt
"""
name: "fraud_detection"
platform: "tensorrt_plan"
max_batch_size: 32
dynamic_batching {
    preferred_batch_size: [8, 16, 32]
    max_queue_delay_microseconds: 1000
}

input [
    {
        name: "input"
        data_type: TYPE_FP32
        dims: [10]
    }
]

output [
    {
        name: "output"
        data_type: TYPE_FP32
        dims: [1]
    }
]
"""

# Triton client
import tritonclient.grpc as grpcclient

triton_client = grpcclient.InferenceServerClient(url="localhost:8001")

# Predict (batched, <5ms latency)
inputs = [grpcclient.InferInput("input", [32, 10], "FP32")]
inputs[0].set_data_from_numpy(batch_data)

outputs = [grpcclient.InferRequestedOutput("output")]

result = triton_client.infer(model_name="fraud_detection", inputs=inputs, outputs=outputs)
predictions = result.as_numpy("output")
```

## Batch Prediction Systems

**Context:** Offline predictions on large datasets (millions-billions of records), latency not critical.

### Architecture

```
Data Warehouse (Snowflake/BigQuery)
    |
Spark Cluster (EMR/Dataproc)
    |    └─ Load model from registry
    |    └─ Batch prediction (parallelized)
    |    └─ Write results back to warehouse
    |
Scheduled Daily (Airflow)
```

### Implementation

```python
# batch_prediction_spark.py
from pyspark.sql import SparkSession
import mlflow.pyfunc

def batch_predict(input_table, output_table, model_uri):
    """Batch prediction on large dataset."""

    spark = SparkSession.builder \
        .appName("BatchPrediction") \
        .config("spark.executor.instances", "50") \
        .config("spark.executor.memory", "8g") \
        .getOrCreate()

    # Load data
    df = spark.sql(f"SELECT * FROM {input_table}")

    # Load model as UDF
    predict_udf = mlflow.pyfunc.spark_udf(
        spark,
        model_uri=model_uri,
        result_type='double'
    )

    # Apply predictions (parallelized across cluster)
    predictions_df = df.withColumn('prediction', predict_udf(*df.columns))

    # Write results
    predictions_df.write \
        .mode('overwrite') \
        .saveAsTable(output_table)

    print(f"Predictions saved to {output_table}")

# Usage: 1 billion records processed in ~30 minutes on 50-node cluster
batch_predict(
    input_table='data_warehouse.transactions',
    output_table='data_warehouse.fraud_predictions',
    model_uri='models:/fraud_detection/Production'
)
```

## LLMOps Implementation

**Context:** Deploy LLM-based applications with RAG, prompt management, and LLM-specific monitoring.

### Architecture

```
User Query
    |
Prompt Registry (versioned prompts)
    |
RAG System
    |    └─ Vector DB (Pinecone/Chroma)
    |    └─ Embedding Model
    |    └─ Retrieval (top-k docs)
    |
LLM Serving (vLLM / TGI)
    |    └─ GPU inference
    |    └─ Batching
    |    └─ Caching
    |
Guardrails (NeMo Guardrails)
    |    └─ Input validation
    |    └─ Output safety checks
    |
Monitoring (LangSmith / Arize Phoenix)
    |    └─ Hallucination detection
    |    └─ Cost tracking
    |    └─ Latency monitoring
    |
Response
```

### Implementation

```python
# llmops_system.py
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langsmith import Client as LangSmithClient

class LLMOpsSystem:
    """Production LLM system with monitoring."""

    def __init__(self):
        # Vector DB
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_db = Chroma(persist_directory='./chroma_db', embedding_function=self.embeddings)

        # LLM
        self.llm = HuggingFacePipeline.from_model_id(
            model_id="meta-llama/Llama-2-7b-chat",
            device=0,
            pipeline_kwargs={"max_new_tokens": 512}
        )

        # Monitoring
        self.langsmith = LangSmithClient()

        # Prompt cache
        self.cache = PromptCache()

    def query(self, question: str):
        """RAG query with monitoring."""

        # Check cache
        cached = self.cache.get(question)
        if cached:
            return cached

        # Retrieve context
        docs = self.vector_db.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        # Build prompt
        prompt = f"""Answer the question based on context.

Context: {context}

Question: {question}

Answer:"""

        # LLM call (traced by LangSmith)
        answer = self.llm(prompt)

        # Cache
        self.cache.set(question, answer)

        # Track cost
        tokens = len(prompt.split()) + len(answer.split())
        cost = tokens * 0.00001  # $0.01 per 1K tokens

        return {
            'answer': answer,
            'sources': [doc.metadata for doc in docs],
            'tokens': tokens,
            'cost': cost
        }
```
