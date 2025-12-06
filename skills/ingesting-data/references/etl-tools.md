# ETL Tools Reference


## Table of Contents

- [dlt (data load tool) - Recommended](#dlt-data-load-tool-recommended)
  - [Installation](#installation)
  - [Basic Pipeline](#basic-pipeline)
  - [Incremental Loading](#incremental-loading)
  - [Transformations with dbt](#transformations-with-dbt)
- [Meltano (ELT Platform)](#meltano-elt-platform)
  - [Installation](#installation)
  - [Add Extractors/Loaders](#add-extractorsloaders)
  - [Configuration](#configuration)
  - [Run Pipeline](#run-pipeline)
- [Dagster (Orchestration + ELT)](#dagster-orchestration-elt)
  - [Assets-based Pipeline](#assets-based-pipeline)
- [Airbyte (Low-Code ELT)](#airbyte-low-code-elt)
  - [Docker Setup](#docker-setup)
  - [API Configuration](#api-configuration)
- [Tool Selection Guide](#tool-selection-guide)
- [Comparison Matrix](#comparison-matrix)

## dlt (data load tool) - Recommended

Modern Python-first ETL with automatic schema evolution.

### Installation
```bash
pip install dlt[postgres]  # or dlt[duckdb], dlt[bigquery], etc.
```

### Basic Pipeline
```python
import dlt

# Define source with resources
@dlt.source
def api_source(api_key: str):
    @dlt.resource(write_disposition="merge", primary_key="id")
    def users():
        response = requests.get(
            "https://api.example.com/users",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        yield response.json()

    @dlt.resource(write_disposition="append")
    def events():
        response = requests.get("https://api.example.com/events")
        yield response.json()

    return users, events

# Create pipeline
pipeline = dlt.pipeline(
    pipeline_name="api_pipeline",
    destination="postgres",
    dataset_name="raw_data"
)

# Run
load_info = pipeline.run(api_source(os.environ["API_KEY"]))
print(load_info)
```

### Incremental Loading
```python
@dlt.source
def incremental_source():
    @dlt.resource(primary_key="id")
    def orders(
        updated_at=dlt.sources.incremental("updated_at", initial_value="2024-01-01")
    ):
        # Only fetch records after last updated_at
        response = requests.get(
            f"https://api.example.com/orders?updated_after={updated_at.last_value}"
        )
        yield response.json()

    return orders
```

### Transformations with dbt
```python
# Run dbt models after loading
pipeline.run(source)
pipeline.run(
    dbt_package="./dbt_project",
    select=["staging", "marts"]
)
```

## Meltano (ELT Platform)

Singer-based with 500+ connectors.

### Installation
```bash
pip install meltano
meltano init my_project
cd my_project
```

### Add Extractors/Loaders
```bash
# Add extractors (sources)
meltano add extractor tap-github
meltano add extractor tap-salesforce

# Add loaders (destinations)
meltano add loader target-postgres
meltano add loader target-snowflake
```

### Configuration
```yaml
# meltano.yml
plugins:
  extractors:
    - name: tap-github
      config:
        repository: owner/repo
        start_date: '2024-01-01'

  loaders:
    - name: target-postgres
      config:
        host: localhost
        port: 5432
        database: warehouse
```

### Run Pipeline
```bash
meltano run tap-github target-postgres
```

## Dagster (Orchestration + ELT)

### Assets-based Pipeline
```python
from dagster import asset, Definitions
from dagster_duckdb import DuckDBResource

@asset
def raw_orders(duckdb: DuckDBResource):
    """Load orders from S3."""
    with duckdb.get_connection() as conn:
        conn.execute("""
            CREATE TABLE raw_orders AS
            SELECT * FROM read_parquet('s3://bucket/orders/*.parquet')
        """)

@asset(deps=[raw_orders])
def cleaned_orders(duckdb: DuckDBResource):
    """Clean and transform orders."""
    with duckdb.get_connection() as conn:
        conn.execute("""
            CREATE TABLE cleaned_orders AS
            SELECT
                id,
                customer_id,
                CAST(amount AS DECIMAL(10,2)) as amount,
                status
            FROM raw_orders
            WHERE status IS NOT NULL
        """)

defs = Definitions(
    assets=[raw_orders, cleaned_orders],
    resources={"duckdb": DuckDBResource(database="warehouse.db")}
)
```

## Airbyte (Low-Code ELT)

### Docker Setup
```bash
git clone https://github.com/airbytehq/airbyte.git
cd airbyte
./run-ab-platform.sh
```

### API Configuration
```python
import requests

# Create source
source = requests.post(
    "http://localhost:8000/api/v1/sources/create",
    json={
        "name": "My PostgreSQL",
        "sourceDefinitionId": "decd338e-5647-4c0b-adf4-da0e75f5a750",
        "workspaceId": "...",
        "connectionConfiguration": {
            "host": "localhost",
            "port": 5432,
            "database": "source_db"
        }
    }
)
```

## Tool Selection Guide

| Use Case | Tool | Why |
|----------|------|-----|
| **Python-first, flexible** | dlt | Pythonic, auto schema, fast |
| **Many connectors needed** | Meltano/Airbyte | 500+ pre-built |
| **Complex orchestration** | Dagster | Assets, observability |
| **Enterprise/managed** | Fivetran | SaaS, guaranteed |
| **Real-time streaming** | Custom + Kafka | Low latency |

## Comparison Matrix

| Feature | dlt | Meltano | Dagster | Airbyte |
|---------|-----|---------|---------|---------|
| **Setup** | pip install | CLI | pip install | Docker |
| **Connectors** | 50+ | 500+ | 50+ | 300+ |
| **Custom sources** | Python | Singer tap | Python | Java/Python |
| **Schema evolution** | Automatic | Manual | Manual | Automatic |
| **Orchestration** | Basic | Airflow | Built-in | Basic |
| **Incremental** | Yes | Yes | Yes | Yes |
| **Transformations** | dbt | dbt | Built-in | dbt |
| **Hosting** | Self | Self | Cloud/Self | Cloud/Self |
