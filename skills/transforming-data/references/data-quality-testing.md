# Data Quality Testing


## Table of Contents

- [Overview](#overview)
- [dbt Testing](#dbt-testing)
  - [Generic Tests](#generic-tests)
  - [Singular Tests](#singular-tests)
  - [Custom Generic Tests (Macros)](#custom-generic-tests-macros)
- [Great Expectations](#great-expectations)
  - [Setup](#setup)
  - [Common Expectations](#common-expectations)
  - [Run Validation](#run-validation)
- [Integrating Tests into Pipelines](#integrating-tests-into-pipelines)
  - [Airflow Integration](#airflow-integration)
- [Best Practices](#best-practices)
  - [Test Severity Levels](#test-severity-levels)
  - [Common Quality Checks](#common-quality-checks)

## Overview

Data quality testing ensures transformations produce accurate, complete, and consistent data before consumption by downstream systems.

## dbt Testing

### Generic Tests

Built-in tests for common validations.

```yaml
# models/marts/schema.yml

models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null

      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
```

### Singular Tests

Custom SQL tests for complex validations.

```sql
-- tests/assert_positive_revenue.sql

select *
from {{ ref('fct_orders') }}
where total_revenue < 0
```

Test fails if any rows are returned.

### Custom Generic Tests (Macros)

```sql
-- macros/test_row_count_min.sql

{% test row_count_min(model, min_rows=1) %}

select count(*) as row_count
from {{ model }}
having count(*) < {{ min_rows }}

{% endtest %}
```

Usage:
```yaml
models:
  - name: fct_orders
    tests:
      - row_count_min:
          min_rows: 100
```

## Great Expectations

### Setup

```python
import great_expectations as gx

context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite(
    expectation_suite_name="orders_suite"
)
```

### Common Expectations

```python
# Column exists
suite.add_expectation(
    gx.expectations.ExpectColumnToExist(column="order_id")
)

# No nulls
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)

# Values in range
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="total_amount",
        min_value=0,
        max_value=100000
    )
)

# Unique values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
)

# Values in set
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="order_status",
        value_set=['pending', 'confirmed', 'shipped', 'delivered']
    )
)
```

### Run Validation

```python
# Validate DataFrame
validator = context.sources.pandas_default.read_dataframe(df)
results = validator.validate(expectation_suite_name="orders_suite")

if not results.success:
    raise ValueError("Data quality checks failed")
```

## Integrating Tests into Pipelines

### Airflow Integration

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator

def run_quality_checks(**context):
    # Great Expectations validation
    context_ge = gx.get_context()
    validator = context_ge.sources.pandas_default.read_dataframe(df)
    results = validator.validate(expectation_suite_name="orders_suite")

    if not results.success:
        raise ValueError("Quality checks failed")

with DAG('data_pipeline', ...) as dag:
    extract = PythonOperator(task_id='extract', ...)
    transform = DbtCloudRunJobOperator(task_id='dbt_run', ...)
    test = DbtCloudRunJobOperator(task_id='dbt_test', ...)  # Run dbt tests
    quality_check = PythonOperator(task_id='quality_check', python_callable=run_quality_checks)

    extract >> transform >> test >> quality_check
```

## Best Practices

1. **Test early**: Validate in staging layer before expensive transformations
2. **Test incrementally**: Run tests on each dbt run
3. **Fail fast**: Stop pipeline on critical test failures
4. **Monitor trends**: Track test pass rates over time
5. **Document expectations**: Explain why tests exist

### Test Severity Levels

```yaml
# dbt: Warn vs Error
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique:
              severity: error  # Fail pipeline
          - not_null:
              severity: warn   # Log but don't fail
```

### Common Quality Checks

1. **Completeness**: No missing required fields
2. **Uniqueness**: Primary keys are unique
3. **Consistency**: Values match reference data
4. **Accuracy**: Aggregations match source totals
5. **Timeliness**: Data freshness within SLA
6. **Validity**: Values in expected ranges/formats

```sql
-- Freshness check
select max(updated_at) as last_update
from {{ ref('fct_orders') }}
having max(updated_at) < current_timestamp - interval '24' hour
```
