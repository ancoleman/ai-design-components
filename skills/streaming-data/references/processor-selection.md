# Stream Processor Selection Guide

## Table of Contents
- [Overview](#overview)
- [Apache Flink](#apache-flink)
- [Apache Spark Streaming](#apache-spark-streaming)
- [Kafka Streams](#kafka-streams)
- [ksqlDB](#ksqldb)
- [Comparison Matrix](#comparison-matrix)
- [Selection Flowchart](#selection-flowchart)

## Overview

Stream processors transform, aggregate, and analyze streaming data in real-time. Choose based on latency requirements, processing model, deployment constraints, and ecosystem integration.

## Apache Flink

### Architecture
- True stream processing (event-by-event)
- Distributed dataflow engine
- Stateful operators with checkpointing
- Event-time processing with watermarks

### Strengths
- Millisecond-level latency
- Superior state management (RocksDB backend)
- Event-time semantics (handles out-of-order events)
- Exactly-once processing guarantees
- Complex Event Processing (CEP) support
- Flexible windowing (tumbling, sliding, session)

### Weaknesses
- Steeper learning curve
- Requires separate cluster deployment
- Limited Python support (PyFlink improving but not mature)
- Smaller ecosystem than Spark

### Best Use Cases
- Real-time analytics dashboards
- Fraud detection (sub-second response)
- Monitoring and alerting systems
- Complex Event Processing (CEP)
- High-frequency trading
- IoT stream processing

### Code Example (Java)

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<Event> events = env
    .addSource(new FlinkKafkaConsumer<>("events", new EventSchema(), properties));

DataStream<Aggregation> aggregated = events
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new EventAggregator());

aggregated.addSink(new FlinkKafkaProducer<>("aggregated", new AggregationSchema(), properties));

env.execute("Real-Time Aggregation");
```

### Configuration Recommendations

```yaml
# flink-conf.yaml
taskmanager.memory.process.size: 4096m
taskmanager.numberOfTaskSlots: 4
state.backend: rocksdb
state.checkpoints.dir: s3://bucket/checkpoints
state.savepoints.dir: s3://bucket/savepoints
execution.checkpointing.interval: 60000
```

## Apache Spark Streaming

### Architecture
- Micro-batch processing model
- RDD-based (legacy) or DataFrame-based (Structured Streaming)
- Integration with Spark batch ecosystem
- Catalyst optimizer for SQL

### Strengths
- Unified batch and stream processing
- Excellent Python support (PySpark)
- Strong ML integration (MLlib, feature stores)
- Interactive SQL analytics
- Mature ecosystem (Delta Lake, Databricks)
- Good for complex transformations

### Weaknesses
- Higher latency (seconds vs milliseconds)
- Less suitable for real-time use cases
- Larger resource footprint

### Best Use Cases
- ETL pipelines (batch + streaming)
- Machine learning feature engineering
- Data lake ingestion and transformation
- Analytics with SQL (Structured Streaming)
- Hybrid batch/stream workloads
- Python-first data science teams

### Code Example (Python)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col

spark = SparkSession.builder \
    .appName("StreamingETL") \
    .getOrCreate()

# Read from Kafka
events = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "events") \
    .load()

# Parse JSON and aggregate
aggregated = events \
    .selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .groupBy(window("data.timestamp", "5 minutes"), "data.user_id") \
    .count()

# Write to data lake
query = aggregated.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://bucket/checkpoints") \
    .start("s3://bucket/aggregated")

query.awaitTermination()
```

### Configuration Recommendations

```python
# Spark configuration
spark.conf.set("spark.sql.streaming.checkpointLocation", "s3://bucket/checkpoints")
spark.conf.set("spark.sql.shuffle.partitions", "100")
spark.conf.set("spark.streaming.kafka.maxRatePerPartition", "1000")
spark.conf.set("spark.sql.streaming.stateStore.providerClass",
               "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider")
```

## Kafka Streams

### Architecture
- Client library (not separate cluster)
- Embedded in application JVM
- Stateful processing with RocksDB
- Exactly-once processing support

### Strengths
- Simple deployment (no cluster management)
- Exactly-once semantics
- Tight Kafka integration
- Automatic load balancing (consumer group protocol)
- Low operational overhead

### Weaknesses
- Kafka-only (cannot read from other sources)
- Java/Scala only
- Scales with application instances
- Limited ecosystem compared to Flink/Spark

### Best Use Cases
- Microservices stream processing
- Real-time aggregations
- Stateful transformations
- Event enrichment
- Stream-stream joins
- Applications already using Kafka

### Code Example (Java)

```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "aggregation-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

StreamsBuilder builder = new StreamsBuilder();

KStream<String, Event> events = builder.stream("events");

KTable<Windowed<String>, Long> aggregated = events
    .groupByKey()
    .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
    .count();

aggregated.toStream().to("aggregated");

KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

### Configuration Recommendations

```properties
# Kafka Streams config
processing.guarantee=exactly_once_v2
num.stream.threads=4
state.dir=/tmp/kafka-streams
cache.max.bytes.buffering=10485760
commit.interval.ms=1000
```

## ksqlDB

### Architecture
- Server-based SQL engine
- Built on Kafka Streams
- Push and pull queries
- Materialized views

### Strengths
- SQL interface (familiar to analysts)
- No code required for simple transformations
- Materialized views for serving queries
- Integration with Confluent Platform
- Good for rapid prototyping

### Weaknesses
- Limited to SQL expressiveness
- Performance overhead vs native Kafka Streams
- Smaller community than other options
- Confluent-specific ecosystem

### Best Use Cases
- Real-time dashboards (SQL queries)
- Simple transformations and aggregations
- Analyst self-service analytics
- Prototyping stream processing logic
- Materialized view serving

### Code Example (ksqlDB)

```sql
-- Create stream from Kafka topic
CREATE STREAM events (
  user_id VARCHAR,
  action VARCHAR,
  timestamp BIGINT
) WITH (
  KAFKA_TOPIC='events',
  VALUE_FORMAT='JSON'
);

-- Aggregate events in 5-minute windows
CREATE TABLE aggregated AS
SELECT
  user_id,
  WINDOWSTART AS window_start,
  COUNT(*) AS event_count
FROM events
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY user_id
EMIT CHANGES;

-- Push query (continuous)
SELECT * FROM aggregated EMIT CHANGES;

-- Pull query (point-in-time)
SELECT * FROM aggregated WHERE user_id = 'user-123';
```

## Comparison Matrix

### Processing Model

| Feature | Flink | Spark | Kafka Streams | ksqlDB |
|---------|-------|-------|---------------|--------|
| **Processing Model** | True streaming | Micro-batch | True streaming | True streaming |
| **Latency** | Millisecond | Second | Millisecond | Millisecond |
| **Throughput** | Very High | Very High | High | Medium |
| **Event Time** | Native | Supported | Native | Supported |
| **Watermarks** | Built-in | Manual | Built-in | Automatic |

### State Management

| Feature | Flink | Spark | Kafka Streams | ksqlDB |
|---------|-------|-------|---------------|--------|
| **State Backend** | RocksDB, In-Memory | RocksDB, HDFS | RocksDB | Kafka Streams |
| **Checkpointing** | Excellent | Good | Good | Automatic |
| **Fault Tolerance** | Exactly-once | Exactly-once | Exactly-once | Exactly-once |
| **State Size** | Large (TB+) | Large (TB+) | Medium (100s GB) | Medium |

### Deployment

| Feature | Flink | Spark | Kafka Streams | ksqlDB |
|---------|-------|-------|---------------|--------|
| **Deployment** | Cluster | Cluster | Embedded | Server |
| **Scaling** | Task slots | Executors | App instances | Server instances |
| **Operations** | Medium | Medium | Low | Low |
| **Resource Usage** | Medium | High | Low | Medium |

### Ecosystem

| Feature | Flink | Spark | Kafka Streams | ksqlDB |
|---------|-------|-------|---------------|--------|
| **Language Support** | Java, Scala, PyFlink | Java, Scala, Python, R | Java, Scala | SQL |
| **Connectors** | Many (Flink CDC) | Many (Spark connectors) | Kafka-only | Kafka-only |
| **ML Integration** | FlinkML | MLlib (Excellent) | None | None |
| **SQL Support** | Table API, SQL | Structured Streaming | None | Native |
| **Community** | Large | Very Large | Large | Medium |

## Selection Flowchart

### Primary Decision Path

```
START: What is primary requirement?

├─ Latency
│  ├─ Millisecond-level? → FLINK or KAFKA STREAMS
│  ├─ Sub-second? → FLINK
│  └─ Seconds OK? → SPARK
│
├─ Processing Model
│  ├─ True streaming? → FLINK or KAFKA STREAMS
│  ├─ Micro-batch OK? → SPARK
│  └─ SQL interface? → KSQLDB
│
├─ Deployment
│  ├─ Embedded in app? → KAFKA STREAMS
│  ├─ Separate cluster? → FLINK or SPARK
│  └─ Serverless? → KSQLDB
│
└─ Language
   ├─ Python required? → SPARK
   ├─ Java/Scala only? → FLINK or KAFKA STREAMS
   └─ SQL only? → KSQLDB
```

### Use Case Alignment

```
START: What is use case?

├─ Real-Time Analytics
│  ├─ Millisecond dashboards? → FLINK
│  ├─ SQL interface for analysts? → KSQLDB
│  └─ Complex aggregations? → SPARK
│
├─ ETL Pipelines
│  ├─ Batch + streaming? → SPARK
│  ├─ Streaming only? → FLINK
│  └─ Simple transformations? → KAFKA STREAMS
│
├─ Machine Learning
│  ├─ Feature engineering? → SPARK (MLlib)
│  ├─ Model inference? → FLINK or SPARK
│  └─ Training? → SPARK
│
├─ Complex Event Processing
│  ├─ Pattern matching? → FLINK (CEP)
│  ├─ Stateful operations? → FLINK
│  └─ Simple filters? → KAFKA STREAMS
│
└─ Microservices
   ├─ Embedded processing? → KAFKA STREAMS
   ├─ Shared infrastructure? → FLINK
   └─ SQL-based? → KSQLDB
```

### Operational Constraints

```
START: What are operational needs?

├─ Team Skills
│  ├─ Python expertise? → SPARK
│  ├─ Java/Scala expertise? → FLINK or KAFKA STREAMS
│  ├─ SQL-first team? → KSQLDB
│  └─ Mixed skills? → SPARK
│
├─ Infrastructure
│  ├─ Kubernetes? → FLINK or SPARK
│  ├─ Serverless? → KSQLDB or managed services
│  ├─ On-prem? → FLINK or SPARK
│  └─ Cloud-native? → Managed FLINK or SPARK
│
└─ Budget
   ├─ Cost-sensitive? → KAFKA STREAMS (no cluster)
   ├─ Enterprise support? → SPARK (Databricks)
   └─ Open source only? → FLINK or KAFKA STREAMS
```

## Technology-Specific Guidance

### When to Choose Flink

**Strong indicators**:
- Real-time analytics with millisecond SLAs
- Complex Event Processing (CEP) requirements
- Event-time processing critical (out-of-order events)
- Large state management (100s GB to TBs)
- High-frequency event streams

**Example scenarios**:
- Fraud detection (sub-second response)
- Real-time recommendation systems
- IoT sensor data processing
- Network monitoring and alerting
- Financial trading systems

**Code smell (avoid Flink)**:
- Python-first team with no Java/Scala expertise
- Simple transformations (overkill)
- Batch-heavy workloads

### When to Choose Spark Streaming

**Strong indicators**:
- Batch + streaming hybrid workloads
- Machine learning integration (MLlib, feature stores)
- Python-first data science teams
- Data lake ingestion and transformation
- Interactive SQL analytics

**Example scenarios**:
- ETL pipelines (ingest to data warehouse)
- ML feature engineering pipelines
- Log aggregation and analysis
- Batch reprocessing with streaming updates
- Data quality monitoring

**Code smell (avoid Spark)**:
- Real-time requirements (<1 second latency)
- Simple event routing (overkill)

### When to Choose Kafka Streams

**Strong indicators**:
- Microservices architecture
- No separate cluster desired
- Tight Kafka integration
- Stateful transformations
- Event enrichment

**Example scenarios**:
- Order processing pipeline
- User session aggregation
- Event enrichment from database
- Stream-stream joins
- Real-time inventory updates

**Code smell (avoid Kafka Streams)**:
- Need to process from multiple sources (not just Kafka)
- Python requirement
- Large-scale batch processing

### When to Choose ksqlDB

**Strong indicators**:
- SQL-first team (analysts, not engineers)
- Rapid prototyping
- Simple aggregations and transformations
- Materialized views for serving
- No custom code desired

**Example scenarios**:
- Real-time dashboard queries
- Simple aggregation pipelines
- Analyst self-service analytics
- Prototyping before coding
- Materialized view serving layer

**Code smell (avoid ksqlDB)**:
- Complex business logic (SQL limitations)
- Performance-critical paths
- Need for custom UDFs

## Performance Tuning

### Flink Tuning

```yaml
# Parallelism
parallelism.default: 4
taskmanager.numberOfTaskSlots: 4

# Memory
taskmanager.memory.process.size: 4096m
taskmanager.memory.managed.fraction: 0.4

# Checkpointing
execution.checkpointing.interval: 60000
execution.checkpointing.mode: EXACTLY_ONCE
state.backend.incremental: true

# RocksDB state backend
state.backend.rocksdb.block.cache-size: 256m
state.backend.rocksdb.write-buffer-size: 64m
```

### Spark Tuning

```python
# Shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Memory
spark.conf.set("spark.executor.memory", "4g")
spark.conf.set("spark.executor.memoryOverhead", "1g")

# Streaming
spark.conf.set("spark.sql.streaming.stateStore.providerClass",
               "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider")
spark.conf.set("spark.streaming.kafka.maxRatePerPartition", "1000")
```

### Kafka Streams Tuning

```properties
# Parallelism
num.stream.threads=4

# State store
state.dir=/mnt/kafka-streams
cache.max.bytes.buffering=10485760

# Processing
commit.interval.ms=1000
processing.guarantee=exactly_once_v2

# RocksDB
rocksdb.config.setter=CustomRocksDBConfig
```

## Migration Strategies

### From Spark to Flink

**Reasons to migrate**:
- Need lower latency (millisecond vs second)
- Event-time processing critical
- True streaming model required

**Migration approach**:
1. Identify Spark Streaming jobs
2. Rewrite using Flink DataStream API
3. Run both systems in parallel (shadow mode)
4. Compare results and performance
5. Cutover to Flink

### From Kafka Streams to Flink

**Reasons to migrate**:
- Need to process from multiple sources (not just Kafka)
- Large state exceeds Kafka Streams capacity
- Complex CEP patterns required

**Migration approach**:
1. Extract business logic to shared library
2. Implement Flink job with same logic
3. Dual-write results for validation
4. Cutover consumer to Flink results
5. Decommission Kafka Streams app

### From ksqlDB to Code

**Reasons to migrate**:
- SQL limitations (complex business logic)
- Performance requirements
- Need custom UDFs

**Migration approach**:
1. Export ksqlDB queries as reference
2. Implement equivalent logic in Flink/Kafka Streams
3. Test with same input data
4. Compare outputs
5. Cutover

## Conclusion

**Default recommendation**: Start with Kafka Streams for microservices, Flink for real-time analytics, Spark for batch+stream hybrid.

**Real-time requirements**: Choose Flink for millisecond latency and complex event processing.

**Python teams**: Choose Spark Streaming for excellent PySpark support and ML integration.

**Operational simplicity**: Choose Kafka Streams for embedded processing without cluster management.

**SQL interface**: Choose ksqlDB for analyst self-service and rapid prototyping.
