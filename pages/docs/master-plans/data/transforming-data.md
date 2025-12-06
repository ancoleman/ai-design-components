---
sidebar_position: 3
---

# Data Transformation

Master plan for building ETL/ELT pipelines and data transformation workflows. Covers pipeline orchestration, data quality frameworks, incremental processing strategies, and modern analytics engineering practices.

## Key Topics

- **ETL vs. ELT Patterns**: When to transform before or after loading, trade-offs and architecture
- **Pipeline Orchestration**: DAG design, dependency management, scheduling, and retries
- **Incremental Processing**: Change detection, watermark strategies, and upsert patterns
- **Data Quality Frameworks**: Validation rules, anomaly detection, and data profiling
- **Idempotency Patterns**: Ensuring safe pipeline re-runs and exactly-once processing
- **Error Handling**: Dead letter queues, poison pill detection, and graceful degradation
- **Batch vs. Micro-Batch**: Processing window selection and latency requirements
- **Data Lineage Tracking**: Capturing transformations, dependencies, and impact analysis
- **Testing Strategies**: Unit tests for transformations, integration tests, data diff testing
- **Analytics Engineering**: dbt workflows, model organization, and documentation practices

## Primary Tools & Technologies

**Orchestration Platforms:**
- Apache Airflow (Python-based DAG orchestration)
- Prefect (modern Python workflow engine)
- Dagster (data-aware orchestration)
- Temporal (durable execution engine)
- Azure Data Factory, AWS Glue, Google Cloud Composer (managed services)

**Transformation Frameworks:**
- dbt (SQL-based analytics engineering)
- Apache Spark (distributed batch/stream processing)
- Pandas, Polars (Python data manipulation)
- SQL stored procedures and views

**Data Quality:**
- Great Expectations (Python data validation)
- dbt tests (SQL-based quality checks)
- Soda Core (data quality checks as code)
- Monte Carlo, Datafold (automated data observability)

**Data Integration:**
- Airbyte (open-source ELT connector platform)
- Fivetran (managed ELT service)
- Singer taps (lightweight connectors)
- Apache NiFi (visual dataflow programming)

**Version Control & CI/CD:**
- Git for pipeline code
- dbt Cloud, Astronomer for CI/CD
- GitHub Actions, GitLab CI for automation

## Integration Points

**Upstream Dependencies:**
- **Data Architecture**: Schema design informing transformation logic
- **Streaming Data**: Real-time transformations and CDC integration
- **SQL Optimization**: Query tuning for transformation performance
- **Secret Management**: Secure handling of database and API credentials

**Downstream Consumers:**
- **Data Visualization**: Clean, modeled data ready for BI tools
- **Analytics**: Aggregated datasets for reporting and dashboards
- **Machine Learning**: Feature engineering and training dataset preparation

**Cross-Functional:**
- **Performance Engineering**: Pipeline optimization and resource tuning
- **Monitoring & Alerting**: Data pipeline health, SLA tracking, and failure alerts
- **Documentation**: Automated lineage diagrams and data dictionaries

## Status

**Master Plan Available** - Comprehensive guidance for data transformation pipelines, covering Airflow, dbt, Spark, and modern analytics engineering workflows.

---

*Part of the Data Engineering skill collection focused on building reliable, maintainable data transformation pipelines.*
