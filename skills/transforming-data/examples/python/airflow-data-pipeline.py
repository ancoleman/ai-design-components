"""
Airflow Data Pipeline Example

Complete ETL pipeline with dbt, data quality checks, and notifications.

Usage:
    Place in airflow/dags/ directory
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.slack.operators.slack import SlackWebhookOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

def extract_sales_data(**context):
    """Extract sales data from source"""
    df = pd.read_csv('s3://raw-data/sales.csv')
    assert len(df) > 0, "No data extracted"

    # Push metadata to XCom
    context['ti'].xcom_push(key='row_count', value=len(df))
    df.to_parquet('s3://staging/sales.parquet', index=False)

def validate_transformations(**context):
    """Validate dbt transformations"""
    row_count = context['ti'].xcom_pull(key='row_count', task_ids='extract_sales')
    df = pd.read_parquet('s3://transformed/fct_orders.parquet')

    assert len(df) >= row_count * 0.9, "Lost >10% of records"
    assert df['total_revenue'].min() >= 0, "Negative revenue"

with DAG(
    dag_id='daily_sales_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['sales', 'production']
) as dag:

    extract = PythonOperator(task_id='extract_sales', python_callable=extract_sales_data)
    dbt_run = DbtCloudRunJobOperator(task_id='dbt_transform', job_id=12345)
    validate = PythonOperator(task_id='validate', python_callable=validate_transformations)
    notify = SlackWebhookOperator(
        task_id='notify_success',
        http_conn_id='slack_webhook',
        message='Pipeline completed!',
        channel='#data-engineering'
    )

    extract >> dbt_run >> validate >> notify
