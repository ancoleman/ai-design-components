# Pipeline Orchestration Patterns

## Table of Contents

1. [Airflow Patterns](#airflow-patterns)
2. [Dagster Patterns](#dagster-patterns)
3. [Prefect Patterns](#prefect-patterns)
4. [Tool Comparison](#tool-comparison)
5. [Common Orchestration Patterns](#common-orchestration-patterns)
6. [Best Practices](#best-practices)

---

## Airflow Patterns

### Basic DAG Structure

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1)
}

with DAG(
    dag_id='example_pipeline',
    default_args=default_args,
    description='Example data pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['production', 'etl']
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_function
    )

    transform_task = BashOperator(
        task_id='transform_data',
        bash_command='dbt run --models staging'
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_function
    )

    # Define dependencies
    extract_task >> transform_task >> load_task
```

### XCom for Task Communication

```python
def extract_data(**context):
    data = fetch_from_api()
    row_count = len(data)

    # Push to XCom
    context['ti'].xcom_push(key='row_count', value=row_count)
    context['ti'].xcom_push(key='max_timestamp', value=data['timestamp'].max())

    return row_count

def validate_data(**context):
    # Pull from XCom
    row_count = context['ti'].xcom_pull(key='row_count', task_ids='extract_data')

    if row_count < 100:
        raise ValueError(f"Insufficient data: only {row_count} rows")
```

### Dynamic Task Generation

```python
from airflow.models import DagBag

def create_processing_tasks():
    regions = ['us-east', 'us-west', 'eu-central', 'ap-southeast']

    for region in regions:
        PythonOperator(
            task_id=f'process_{region}',
            python_callable=process_region,
            op_kwargs={'region': region}
        )
```

### TaskFlow API (Airflow 2.0+)

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def etl_pipeline():

    @task
    def extract():
        return fetch_data_from_api()

    @task
    def transform(data: dict):
        return clean_and_transform(data)

    @task
    def load(data: dict):
        save_to_warehouse(data)

    # Automatic XCom handling
    data = extract()
    transformed = transform(data)
    load(transformed)

dag = etl_pipeline()
```

---

## Dagster Patterns

### Asset-Based Workflow

```python
from dagster import asset, AssetExecutionContext
import polars as pl

@asset
def raw_orders(context: AssetExecutionContext):
    """Extract raw orders from source system"""
    df = pl.read_csv('s3://bucket/raw/orders.csv')
    context.log.info(f"Extracted {len(df)} orders")
    return df

@asset
def clean_orders(context: AssetExecutionContext, raw_orders: pl.DataFrame):
    """Clean and standardize order data"""
    df = raw_orders.filter(pl.col('order_id').is_not_null())
    context.log.info(f"Cleaned {len(df)} orders")
    return df

@asset
def order_metrics(context: AssetExecutionContext, clean_orders: pl.DataFrame):
    """Calculate order-level metrics"""
    df = clean_orders.group_by('customer_id').agg([
        pl.col('order_amount').sum().alias('total_spent'),
        pl.col('order_id').count().alias('order_count')
    ])
    return df
```

### dbt Integration

```python
from dagster import Definitions
from dagster_dbt import DbtCliResource, dbt_assets

@dbt_assets(manifest=dbt_manifest_path)
def my_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(['build'], context=context).stream()

defs = Definitions(
    assets=[my_dbt_assets],
    resources={
        'dbt': DbtCliResource(project_dir='/path/to/dbt')
    }
)
```

### Asset Groups and Schedules

```python
from dagster import define_asset_job, ScheduleDefinition

# Define job for specific assets
daily_analytics_job = define_asset_job(
    name='daily_analytics',
    selection=['raw_orders', 'clean_orders', 'order_metrics']
)

# Schedule the job
daily_schedule = ScheduleDefinition(
    job=daily_analytics_job,
    cron_schedule='0 2 * * *'  # Daily at 2 AM
)
```

---

## Prefect Patterns

### Flow and Task Decorators

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def extract_data(source: str):
    """Extract data from source with caching"""
    return fetch_from_source(source)

@task(retries=3, retry_delay_seconds=60)
def transform_data(data: dict):
    """Transform data with automatic retries"""
    return apply_transformations(data)

@task
def load_data(data: dict, target: str):
    """Load data to target"""
    save_to_target(data, target)

@flow(name='etl-pipeline')
def etl_flow(source: str, target: str):
    """Main ETL flow"""
    raw_data = extract_data(source)
    transformed_data = transform_data(raw_data)
    load_data(transformed_data, target)

# Run flow
if __name__ == '__main__':
    etl_flow(source='api', target='warehouse')
```

### Dynamic Task Mapping

```python
from prefect import flow, task

@task
def process_file(file_path: str):
    """Process a single file"""
    return transform_file(file_path)

@flow
def batch_processing():
    """Process multiple files in parallel"""
    files = ['file1.csv', 'file2.csv', 'file3.csv']

    # Map task to multiple inputs (parallel execution)
    results = process_file.map(files)

    return results
```

### Subflows

```python
@flow
def staging_flow(table_name: str):
    """Subflow for staging a single table"""
    extract_task(table_name)
    validate_task(table_name)
    return f"{table_name} staged"

@flow
def main_pipeline():
    """Main flow calling multiple subflows"""
    tables = ['orders', 'customers', 'products']

    for table in tables:
        staging_flow(table)  # Call subflow

    aggregate_all_tables()
```

---

## Tool Comparison

### When to Choose Airflow

**Pros**:
- Battle-tested at massive scale (10,000+ DAGs)
- 5,000+ provider packages (integrations)
- Managed services (AWS MWAA, GCP Cloud Composer, Astronomer)
- Large community and extensive documentation

**Cons**:
- Complex setup and maintenance
- Dynamic workflows require custom code
- Heavier resource requirements

**Best for**:
- Enterprise production environments
- Complex static workflows
- Teams needing proven stability

### When to Choose Dagster

**Pros**:
- Asset-based paradigm (data-aware)
- Native dbt integration
- Built-in data lineage and testing
- Excellent developer experience

**Cons**:
- Smaller community than Airflow
- Fewer integrations
- Newer tool (less battle-tested)

**Best for**:
- dbt-heavy workflows
- ML pipelines
- Data quality focus
- Modern data teams

### When to Choose Prefect

**Pros**:
- Pythonic API (decorators, not classes)
- Dynamic workflows (runtime task generation)
- Cloud-native architecture
- Rich observability

**Cons**:
- Smallest community of the three
- Fewer integrations than Airflow
- Some features require Prefect Cloud

**Best for**:
- Dynamic workflows
- Cloud-first companies
- Teams preferring Python-native approach

---

## Common Orchestration Patterns

### Pattern 1: Linear Pipeline

```python
# Airflow
extract >> transform >> validate >> load

# Dagster (automatic from dependencies)
@asset
def step2(step1): pass

# Prefect
@flow
def pipeline():
    a = step1()
    b = step2(a)
    c = step3(b)
```

### Pattern 2: Fan-Out / Fan-In

```python
# Airflow
extract >> [transform_a, transform_b, transform_c] >> aggregate

# Dagster
@asset
def aggregate(transform_a, transform_b, transform_c):
    return combine_all([transform_a, transform_b, transform_c])

# Prefect
@flow
def fan_out_in():
    data = extract()
    results = [transform_a(data), transform_b(data), transform_c(data)]
    aggregate(results)
```

### Pattern 3: Conditional Execution

```python
# Airflow BranchOperator
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    if condition():
        return 'process_full'
    else:
        return 'process_incremental'

branch = BranchPythonOperator(
    task_id='branch',
    python_callable=choose_branch
)

# Prefect
@flow
def conditional_flow():
    data = extract()
    if len(data) > 1000:
        full_process(data)
    else:
        incremental_process(data)
```

### Pattern 4: Error Handling and Retries

```python
# Airflow
task = PythonOperator(
    task_id='task',
    python_callable=func,
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True
)

# Dagster
@asset(retry_policy=RetryPolicy(max_retries=3))
def my_asset():
    return process_data()

# Prefect
@task(retries=3, retry_delay_seconds=[60, 120, 300])
def my_task():
    return process_data()
```

---

## Best Practices

### 1. Idempotency

Ensure tasks produce the same result when run multiple times:

```python
# Good: Idempotent (truncate then insert)
def load_data():
    truncate_table('target_table')
    insert_data('target_table', data)

# Bad: Not idempotent (duplicates on retry)
def load_data():
    insert_data('target_table', data)  # Duplicates if run twice
```

### 2. Incremental Processing

Process only new/changed data:

```python
@task
def extract_incremental(**context):
    # Get last successful run timestamp
    last_run = context['prev_ds']

    # Extract only new data
    data = fetch_data(f"WHERE updated_at > '{last_run}'")
    return data
```

### 3. Data Quality Checks

Integrate validation into pipeline:

```python
@task
def validate_data(df):
    # Check row count
    assert len(df) > 0, "Empty dataset"

    # Check required columns
    required_cols = ['order_id', 'customer_id', 'amount']
    assert all(col in df.columns for col in required_cols)

    # Check data types
    assert df['amount'].dtype == 'float64'

    return df
```

### 4. Monitoring and Alerting

```python
# Airflow: Email/Slack on failure
from airflow.providers.slack.operators.slack import SlackWebhookOperator

notify_failure = SlackWebhookOperator(
    task_id='notify_failure',
    http_conn_id='slack_webhook',
    message='Pipeline failed!',
    trigger_rule='one_failed'
)

# Dagster: Asset checks
from dagster import asset_check

@asset_check(asset=my_asset)
def check_row_count(asset_df):
    if len(asset_df) < 100:
        return AssetCheckResult(passed=False, description="Too few rows")
    return AssetCheckResult(passed=True)
```

### 5. Backfill Strategies

```python
# Airflow: Catchup for historical runs
with DAG(
    dag_id='daily_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=True  # Run for all past dates
) as dag:
    pass

# Dagster: Backfill via CLI
# dagster asset backfill --from 2024-01-01 --to 2024-12-31
```

---

## Additional Resources

- Airflow documentation: https://airflow.apache.org/docs/
- Dagster documentation: https://docs.dagster.io/
- Prefect documentation: https://docs.prefect.io/
- Airflow best practices: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
