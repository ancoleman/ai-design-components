---
sidebar_position: 2
---

# Streaming Data

Master plan for building real-time data streaming pipelines and event-driven architectures. Covers message brokers, stream processing frameworks, event sourcing patterns, and operational best practices for high-throughput data systems.

## Key Topics

- **Message Broker Architectures**: Kafka, Pulsar, RabbitMQ, NATS, and when to use each
- **Stream Processing Frameworks**: Apache Flink, Kafka Streams, Apache Spark Streaming, Apache Storm
- **Event Sourcing Patterns**: Command sourcing, event stores, projections, and replay mechanisms
- **Exactly-Once Semantics**: Idempotency, transactional outbox pattern, and distributed transactions
- **Schema Management**: Schema Registry (Avro, Protobuf, JSON Schema), evolution, and compatibility
- **Partitioning Strategies**: Key-based partitioning, sticky partitioning, and consumer group management
- **Backpressure Handling**: Flow control, buffering strategies, and rate limiting
- **Windowing and Aggregations**: Tumbling, sliding, session windows, and watermarks
- **Change Data Capture (CDC)**: Debezium, database log tailing, and sync strategies
- **Real-Time Analytics**: Streaming SQL, materialized views, and time-series aggregations

## Primary Tools & Technologies

**Message Brokers:**
- Apache Kafka (industry standard for event streaming)
- Apache Pulsar (cloud-native alternative with built-in multi-tenancy)
- RabbitMQ (traditional message queue patterns)
- AWS Kinesis, Azure Event Hubs, Google Pub/Sub (managed services)

**Stream Processing:**
- Apache Flink (stateful stream processing)
- Kafka Streams (lightweight, embedded processing)
- Apache Spark Streaming (micro-batch processing)
- ksqlDB (SQL-based stream processing)

**Schema Management:**
- Confluent Schema Registry
- Pulsar Schema Registry
- AWS Glue Schema Registry

**Change Data Capture:**
- Debezium (Kafka Connect-based CDC)
- Maxwell's Daemon (MySQL CDC)
- Airbyte (data integration with CDC support)

**Monitoring & Operations:**
- Kafka UI, Kafdrop, Conduktor
- Prometheus + Grafana for metrics
- Datadog, New Relic for observability

## Integration Points

**Upstream Dependencies:**
- **Data Architecture**: Event schema design and versioning strategies
- **API Design**: Async API specifications for event-driven systems
- **Secret Management**: Broker credentials and TLS certificate handling

**Downstream Consumers:**
- **Data Transformation**: Real-time ETL consuming streaming data
- **Performance Engineering**: Throughput optimization and latency tuning
- **SQL Optimization**: Materialized views and streaming analytics

**Cross-Functional:**
- **Microservices**: Event-driven communication and saga patterns
- **Monitoring & Alerting**: Stream lag monitoring and data quality checks
- **Disaster Recovery**: Replication strategies and backup/restore

## Status

**Master Plan Available** - Comprehensive guidance for real-time data streaming architectures, covering Kafka, Pulsar, Flink, and event-driven design patterns.

---

*Part of the Data Engineering skill collection focused on building scalable, real-time data pipelines.*
