# GCP Data Analytics Services Reference

Patterns for BigQuery, Pub/Sub, Dataflow, Dataproc, and Cloud Composer.

## Table of Contents

1. [BigQuery](#bigquery)
2. [Pub/Sub](#pubsub)
3. [Dataflow](#dataflow)
4. [Dataproc](#dataproc)
5. [Cloud Composer](#cloud-composer)

---

## BigQuery

### Optimized Table Configuration

```hcl
resource "google_bigquery_dataset" "analytics" {
  dataset_id    = "analytics"
  location      = "US"
  description   = "Analytics dataset"

  default_table_expiration_ms = 7776000000  # 90 days

  access {
    role          = "OWNER"
    user_by_email = google_service_account.analytics.email
  }
}

resource "google_bigquery_table" "events" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "events"

  # Partitioning by day (reduces query cost)
  time_partitioning {
    type  = "DAY"
    field = "event_timestamp"
    expiration_ms = 7776000000  # 90 days
  }

  # Clustering (further reduces query cost)
  clustering = ["user_id", "event_type", "country"]

  schema = jsonencode([
    {
      name = "event_id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "event_timestamp"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    },
    {
      name = "user_id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "event_type"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "country"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "properties"
      type = "JSON"
      mode = "NULLABLE"
    }
  ])
}
```

### Query Optimization

```python
from google.cloud import bigquery

client = bigquery.Client()

# Use parameterized queries
query = """
    SELECT
        event_type,
        COUNT(*) as event_count,
        COUNT(DISTINCT user_id) as unique_users
    FROM `project.analytics.events`
    WHERE event_timestamp >= @start_time
        AND event_timestamp < @end_time
        AND country = @country
    GROUP BY event_type
    ORDER BY event_count DESC
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", "2025-01-01"),
        bigquery.ScalarQueryParameter("end_time", "TIMESTAMP", "2025-01-31"),
        bigquery.ScalarQueryParameter("country", "STRING", "US"),
    ]
)

# Use query caching (24 hours by default)
query_job = client.query(query, job_config=job_config)
results = query_job.result()

# BigQuery ML
ml_query = """
    CREATE OR REPLACE MODEL `project.analytics.user_churn_model`
    OPTIONS(
      model_type='LOGISTIC_REG',
      input_label_cols=['churned']
    ) AS
    SELECT
      user_id,
      activity_count,
      last_active_days_ago,
      churned
    FROM `project.analytics.user_features`
"""
```

---

## Pub/Sub

### Topic and Subscription Configuration

```hcl
# Pub/Sub topic with schema
resource "google_pubsub_schema" "events" {
  name = "events-schema"
  type = "AVRO"
  definition = jsonencode({
    type = "record"
    name = "Event"
    fields = [
      { name = "event_id", type = "string" },
      { name = "timestamp", type = "long" },
      { name = "user_id", type = "string" },
      { name = "event_type", type = "string" }
    ]
  })
}

resource "google_pubsub_topic" "events" {
  name = "events-topic"

  schema_settings {
    schema   = google_pubsub_schema.events.id
    encoding = "JSON"
  }

  message_retention_duration = "604800s"  # 7 days
}

# Pull subscription
resource "google_pubsub_subscription" "events_pull" {
  name  = "events-pull"
  topic = google_pubsub_topic.events.name

  ack_deadline_seconds = 20
  message_retention_duration = "604800s"

  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dead_letter.id
    max_delivery_attempts = 5
  }

  expiration_policy {
    ttl = ""  # Never expire
  }
}

# Push subscription
resource "google_pubsub_subscription" "events_push" {
  name  = "events-push"
  topic = google_pubsub_topic.events.name

  push_config {
    push_endpoint = "https://example.com/webhook"

    oidc_token {
      service_account_email = google_service_account.pubsub.email
    }

    attributes = {
      x-goog-version = "v1"
    }
  }
}
```

### Python Publisher/Subscriber

```python
from google.cloud import pubsub_v1
import json

# Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'events-topic')

def publish_message(event_data):
    message_json = json.dumps(event_data).encode('utf-8')
    future = publisher.publish(
        topic_path,
        message_json,
        event_type=event_data['event_type']  # Custom attribute
    )
    return future.result()

# Subscriber (pull)
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('project-id', 'events-pull')

def callback(message):
    print(f'Received: {message.data}')
    message.ack()  # Acknowledge receipt

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
```

---

## Dataflow

### Terraform Configuration

```hcl
resource "google_dataflow_job" "stream_to_bq" {
  name              = "stream-events-to-bigquery"
  template_gcs_path = "gs://dataflow-templates-us-central1/latest/PubSub_to_BigQuery"
  temp_gcs_location = google_storage_bucket.dataflow_temp.url

  parameters = {
    inputTopic      = google_pubsub_topic.events.id
    outputTableSpec = "${var.project_id}:${google_bigquery_dataset.analytics.dataset_id}.${google_bigquery_table.events.table_id}"
  }

  on_delete = "cancel"
}
```

### Apache Beam Pipeline (Python)

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_pipeline():
    options = PipelineOptions(
        project='project-id',
        runner='DataflowRunner',
        region='us-central1',
        temp_location='gs://bucket/temp',
        staging_location='gs://bucket/staging',
        streaming=True
    )

    with beam.Pipeline(options=options) as pipeline:
        (pipeline
         | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
             topic='projects/project-id/topics/events-topic')
         | 'Parse JSON' >> beam.Map(lambda msg: json.loads(msg))
         | 'Transform' >> beam.Map(transform_event)
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
             'project-id:analytics.events',
             schema='event_id:STRING,timestamp:TIMESTAMP,user_id:STRING',
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
        )

def transform_event(event):
    return {
        'event_id': event['id'],
        'timestamp': event['timestamp'],
        'user_id': event['user']
    }
```

---

## Dataproc

### Cluster Configuration

```hcl
resource "google_dataproc_cluster" "spark" {
  name   = "spark-cluster"
  region = "us-central1"

  cluster_config {
    staging_bucket = google_storage_bucket.dataproc.name

    master_config {
      num_instances = 1
      machine_type  = "n2-standard-4"
      disk_config {
        boot_disk_type    = "pd-ssd"
        boot_disk_size_gb = 100
      }
    }

    worker_config {
      num_instances = 3
      machine_type  = "n2-standard-4"
      disk_config {
        boot_disk_size_gb = 100
      }
    }

    preemptible_worker_config {
      num_instances = 5
    }

    software_config {
      image_version = "2.1-debian11"
      properties = {
        "spark:spark.executor.memory" = "4g"
      }
    }

    gce_cluster_config {
      zone = "us-central1-a"
      service_account_scopes = ["cloud-platform"]
    }

    autoscaling_config {
      policy_uri = google_dataproc_autoscaling_policy.policy.name
    }
  }
}

resource "google_dataproc_autoscaling_policy" "policy" {
  policy_id = "dataproc-policy"
  location  = "us-central1"

  worker_config {
    max_instances = 10
    min_instances = 2
  }

  basic_algorithm {
    yarn_config {
      graceful_decommission_timeout = "30s"
      scale_up_factor               = 0.05
      scale_down_factor             = 1.0
    }
  }
}
```

---

## Cloud Composer

### Airflow Environment

```hcl
resource "google_composer_environment" "airflow" {
  name   = "production-airflow"
  region = "us-central1"

  config {
    software_config {
      airflow_config_overrides = {
        core-dags_are_paused_at_creation = "True"
        webserver-rbac                   = "True"
      }

      pypi_packages = {
        pandas    = ""
        numpy     = ""
        requests  = ">=2.28.0"
      }

      env_variables = {
        ENVIRONMENT = "production"
      }
    }

    node_config {
      zone         = "us-central1-a"
      machine_type = "n1-standard-4"
      disk_size_gb = 100

      service_account = google_service_account.composer.email
    }

    workloads_config {
      scheduler {
        cpu        = 2
        memory_gb  = 7.5
        storage_gb = 5
        count      = 2
      }
      web_server {
        cpu        = 2
        memory_gb  = 7.5
        storage_gb = 5
      }
      worker {
        cpu        = 2
        memory_gb  = 7.5
        storage_gb = 5
        min_count  = 2
        max_count  = 6
      }
    }
  }
}
```

### Sample DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_analytics_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # Daily at 2am
    catchup=False,
) as dag:

    load_data = GCSToBigQueryOperator(
        task_id='load_data_from_gcs',
        bucket='data-bucket',
        source_objects=['data/*.csv'],
        destination_project_dataset_table='project.analytics.raw_events',
        write_disposition='WRITE_TRUNCATE',
    )

    transform = BigQueryInsertJobOperator(
        task_id='transform_data',
        configuration={
            'query': {
                'query': """
                    INSERT INTO `project.analytics.events`
                    SELECT * FROM `project.analytics.raw_events`
                    WHERE timestamp >= CURRENT_DATE()
                """,
                'useLegacySql': False,
            }
        },
    )

    load_data >> transform
```

## Best Practices

### BigQuery
- Use partitioned and clustered tables
- Query only needed columns (avoid SELECT *)
- Use LIMIT for exploratory queries
- Cache results (24 hours)
- Use BI Engine for dashboards

### Pub/Sub
- Use dead letter topics
- Set appropriate ack deadlines
- Implement exponential backoff
- Use message ordering when needed
- Monitor subscription backlog

### Dataflow
- Use windowing for streaming
- Implement exactly-once processing
- Monitor pipeline metrics
- Use Flex templates for custom pipelines
- Enable autoscaling

### Dataproc
- Use preemptible workers (60-91% cheaper)
- Enable autoscaling
- Store data in Cloud Storage (ephemeral clusters)
- Use initialization actions
- Monitor YARN metrics

### Composer
- Use Workload Identity
- Set appropriate resource limits
- Monitor DAG performance
- Use XCom for small data only
- Implement alerting
