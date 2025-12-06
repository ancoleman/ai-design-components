# Data Orchestration Tools for AI Pipelines

Comparison of Dagster, Prefect, Airflow 3.0, and dbt for orchestrating AI/ML data workflows.


## Table of Contents

- [Quick Comparison](#quick-comparison)
- [Dagster (Recommended for AI Pipelines)](#dagster-recommended-for-ai-pipelines)
  - [Why Dagster for AI?](#why-dagster-for-ai)
  - [Basic Pipeline](#basic-pipeline)
  - [Run Pipeline](#run-pipeline)
- [Prefect (Developer-Friendly)](#prefect-developer-friendly)
  - [Basic Workflow](#basic-workflow)
  - [Deployments](#deployments)
- [Airflow 3.0](#airflow-30)
  - [DAG Definition](#dag-definition)
- [dbt (SQL Transformations Only)](#dbt-sql-transformations-only)
  - [Use in AI Pipelines](#use-in-ai-pipelines)
- [Decision Framework](#decision-framework)
- [Scheduling Patterns](#scheduling-patterns)
  - [Dagster Schedules](#dagster-schedules)
  - [Prefect Schedules](#prefect-schedules)
  - [Airflow Schedules](#airflow-schedules)
- [Monitoring and Alerting](#monitoring-and-alerting)
  - [Dagster Sensors](#dagster-sensors)
  - [Prefect Automations](#prefect-automations)
- [Performance Optimization](#performance-optimization)
  - [Parallel Task Execution](#parallel-task-execution)
- [Best Practices](#best-practices)
- [AI Pipeline Example Comparison](#ai-pipeline-example-comparison)
  - [Dagster (Asset-Centric)](#dagster-asset-centric)
  - [Prefect (Task-Centric)](#prefect-task-centric)
  - [Airflow (Operator-Centric)](#airflow-operator-centric)
- [Resources](#resources)

## Quick Comparison

| Tool | Best For | Language | Complexity | Learning Curve |
|------|----------|----------|------------|----------------|
| **Dagster** | ML/AI pipelines, data lineage | Python | Medium | Medium |
| **Prefect** | General workflows, developer UX | Python | Low-Medium | Low |
| **Airflow 3.0** | Enterprise, battle-tested | Python | High | High |
| **dbt** | SQL transformations only | SQL | Low | Low |

## Dagster (Recommended for AI Pipelines)

**Best for:** RAG pipelines, embedding generation, ML feature engineering

### Why Dagster for AI?

- **Asset-centric design** - Think in terms of data assets, not tasks
- **Best data lineage** - Visualize dependencies across pipeline
- **Type system** - Catch errors before runtime
- **Testing built-in** - Unit test pipelines easily
- **Partitions** - Process data in time windows or logical partitions

### Basic Pipeline

```python
from dagster import asset, Definitions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_voyageai import VoyageAIEmbeddings
from qdrant_client import QdrantClient

@asset
def raw_documents():
    """Load raw documents from S3"""
    return load_from_s3("s3://bucket/docs/")

@asset
def chunked_documents(raw_documents):
    """Split documents into 512-token chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )
    return splitter.split_documents(raw_documents)

@asset
def embeddings(chunked_documents):
    """Generate embeddings with Voyage AI"""
    embedder = VoyageAIEmbeddings(model="voyage-3")
    vectors = embedder.embed_documents([doc.page_content for doc in chunked_documents])
    return vectors

@asset
def vector_database(chunked_documents, embeddings):
    """Index into Qdrant"""
    client = QdrantClient("localhost", port=6333)

    client.upsert(
        collection_name="documents",
        points=[
            {"id": i, "vector": vec, "payload": {"text": doc.page_content}}
            for i, (doc, vec) in enumerate(zip(chunked_documents, embeddings))
        ]
    )

    return {"indexed": len(embeddings)}

defs = Definitions(assets=[raw_documents, chunked_documents, embeddings, vector_database])
```

### Run Pipeline

```bash
# Install
pip install dagster dagster-webserver

# Start UI
dagster dev

# Materialize assets
dagster asset materialize --select raw_documents+
```

Access UI: http://localhost:3000

---

## Prefect (Developer-Friendly)

**Best for:** General-purpose workflows, simpler setup than Airflow

### Basic Workflow

```python
from prefect import flow, task
from prefect.tasks import exponential_backoff
from typing import List

@task(retries=3, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def fetch_documents() -> List[str]:
    """Fetch documents with automatic retries"""
    return ["doc1", "doc2", "doc3"]

@task
def chunk_document(doc: str) -> List[str]:
    """Chunk single document"""
    return doc.split()  # Simplified

@task
def generate_embedding(chunk: str) -> List[float]:
    """Generate embedding for chunk"""
    return [0.1, 0.2, 0.3]  # Mock embedding

@flow(name="embedding-pipeline")
def embedding_pipeline():
    """Main embedding pipeline flow"""
    docs = fetch_documents()

    all_chunks = []
    for doc in docs:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)

    embeddings = [generate_embedding(chunk) for chunk in all_chunks]

    return {"total_embeddings": len(embeddings)}

# Run
if __name__ == "__main__":
    embedding_pipeline()
```

### Deployments

```bash
# Start Prefect server
prefect server start

# Deploy flow
prefect deploy
```

---

## Airflow 3.0

**Best for:** Enterprise deployments, existing Airflow users, complex dependencies

### DAG Definition

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def chunk_documents(**context):
    """Chunk documents task"""
    docs = context['ti'].xcom_pull(task_ids='fetch_documents')
    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc, chunk_size=512))
    return chunks

def generate_embeddings(**context):
    """Generate embeddings task"""
    chunks = context['ti'].xcom_pull(task_ids='chunk_documents')
    embeddings = voyage_ai.embed(chunks)
    return embeddings

with DAG(
    'rag_pipeline',
    default_args=default_args,
    description='RAG embedding pipeline',
    schedule_interval='@daily',
    start_date=datetime(2025, 12, 1),
    catchup=False,
) as dag:

    fetch = PythonOperator(
        task_id='fetch_documents',
        python_callable=fetch_documents,
    )

    chunk = PythonOperator(
        task_id='chunk_documents',
        python_callable=chunk_documents,
    )

    embed = PythonOperator(
        task_id='generate_embeddings',
        python_callable=generate_embeddings,
    )

    index = PythonOperator(
        task_id='index_to_qdrant',
        python_callable=index_to_qdrant,
    )

    fetch >> chunk >> embed >> index
```

---

## dbt (SQL Transformations Only)

**Best for:** Data warehouse transformations, NOT for embedding generation

### Use in AI Pipelines

dbt is best for pre-processing data BEFORE embedding generation:

```sql
-- models/cleaned_documents.sql
SELECT
  id,
  title,
  REGEXP_REPLACE(content, '[^a-zA-Z0-9\s]', '') AS cleaned_content,
  category,
  last_updated
FROM raw_documents
WHERE last_updated > CURRENT_DATE - INTERVAL '30 days'
  AND content IS NOT NULL
```

**Then:** Use Dagster/Prefect for embedding generation.

---

## Decision Framework

```
WORKFLOW COMPLEXITY?
├─ SIMPLE (10 steps, SQL + Python)
│  └─ Prefect (lowest overhead)
│
├─ AI/ML FOCUS (embeddings, features, model training)
│  └─ Dagster (asset-centric, best lineage)
│
├─ ENTERPRISE (100+ DAGs, complex dependencies)
│  └─ Airflow 3.0 (battle-tested, mature)
│
└─ SQL-ONLY (data warehouse transformations)
   └─ dbt (specialized tool)
```

## Scheduling Patterns

### Dagster Schedules

```python
from dagster import ScheduleDefinition

daily_embedding_schedule = ScheduleDefinition(
    name="daily_embeddings",
    cron_schedule="0 2 * * *",  # 2 AM daily
    job=embedding_job,
)
```

### Prefect Schedules

```python
from prefect.schedules import CronSchedule

schedule = CronSchedule(cron="0 2 * * *", timezone="UTC")

@flow(schedule=schedule)
def scheduled_pipeline():
    # Pipeline logic
    pass
```

### Airflow Schedules

```python
# schedule_interval in DAG definition
schedule_interval='@daily'  # or '0 2 * * *'
```

## Monitoring and Alerting

### Dagster Sensors

```python
from dagster import sensor, RunRequest

@sensor(job=embedding_job)
def s3_document_sensor():
    """Trigger pipeline when new documents uploaded to S3"""
    new_files = check_s3_for_new_files()

    if new_files:
        return RunRequest(
            run_config={"s3_files": new_files}
        )
```

### Prefect Automations

```python
from prefect.blocks.notifications import SlackWebhook

slack = SlackWebhook.load("my-slack-webhook")

@flow(on_failure=[slack.notify])
def pipeline_with_alerts():
    # Pipeline that alerts on failure
    pass
```

## Performance Optimization

### Parallel Task Execution

**Dagster:**
```python
from dagster import OpExecutionContext

@asset
def embeddings(context: OpExecutionContext, chunks):
    # Dagster automatically parallelizes across workers
    return [generate_embedding(chunk) for chunk in chunks]
```

**Prefect:**
```python
from prefect import flow, task

@task
def generate_embedding(chunk):
    return embed(chunk)

@flow
def parallel_embeddings(chunks):
    # Prefect automatically parallelizes
    futures = [generate_embedding.submit(chunk) for chunk in chunks]
    return [f.result() for f in futures]
```

## Best Practices

1. **Start simple** - Use Prefect for initial prototypes
2. **Idempotent tasks** - Safe to retry and re-run
3. **Partition large datasets** - Process in time windows
4. **Monitor failures** - Set up alerting
5. **Version pipeline code** - Git + semantic versioning
6. **Test locally** - Don't test in production
7. **Log metadata** - Track model versions, parameters
8. **Graceful degradation** - Handle missing/delayed data

## AI Pipeline Example Comparison

### Dagster (Asset-Centric)

```python
@asset
def cleaned_text(): ...

@asset(deps=[cleaned_text])
def chunks(): ...

@asset(deps=[chunks])
def embeddings(): ...
```

### Prefect (Task-Centric)

```python
@flow
def pipeline():
    text = clean_text()
    chunks = create_chunks(text)
    embeddings = generate_embeddings(chunks)
```

### Airflow (Operator-Centric)

```python
fetch >> clean >> chunk >> embed >> index
```

## Resources

- Dagster Docs: https://docs.dagster.io/
- Prefect Docs: https://docs.prefect.io/
- Airflow Docs: https://airflow.apache.org/docs/
- dbt Docs: https://docs.getdbt.com/
- LakeFS Docs: https://docs.lakefs.io/
