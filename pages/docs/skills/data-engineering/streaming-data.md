---
sidebar_position: 2
title: Streaming Data
description: Build event streaming and real-time data pipelines with Kafka, Pulsar, Flink, and Spark
tags: [data-engineering, kafka, streaming, event-sourcing, real-time, flink, spark-streaming]
---

# Streaming Data

Build production-ready event streaming systems and real-time data pipelines using modern message brokers (Kafka, Pulsar, Redpanda) and stream processors (Flink, Spark, Kafka Streams).

## When to Use

Use when:
- Building event-driven architectures and microservices communication
- Processing real-time analytics, monitoring, or alerting systems
- Implementing data integration pipelines (CDC, ETL/ELT)
- Creating log or metrics aggregation systems
- Developing IoT platforms or high-frequency trading systems

## Key Features

### Message Brokers vs Stream Processors

**Message Brokers** (Kafka, Pulsar, Redpanda):
- Store and distribute event streams
- Provide durability, replay capability, partitioning
- Handle producer/consumer coordination

**Stream Processors** (Flink, Spark, Kafka Streams):
- Transform and aggregate streaming data
- Provide windowing, joins, stateful operations
- Execute complex event processing (CEP)

### Delivery Guarantees

- **At-Most-Once**: Messages may be lost, no duplicates (lowest overhead)
- **At-Least-Once**: Messages never lost, may duplicate (requires idempotent consumers)
- **Exactly-Once**: Messages never lost or duplicated (highest overhead, transactional)

## Quick Start

### Choose a Message Broker

**Quick decision**:
- **Apache Kafka**: Mature ecosystem, enterprise features, event sourcing
- **Redpanda**: Low latency, Kafka-compatible, simpler operations (no ZooKeeper)
- **Apache Pulsar**: Multi-tenancy, geo-replication, tiered storage

### TypeScript Producer (KafkaJS)

```typescript
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['kafka1:9092', 'kafka2:9092']
});

const producer = kafka.producer();

await producer.connect();
await producer.send({
  topic: 'events',
  messages: [
    {
      key: 'user-123',
      value: JSON.stringify({ action: 'login', timestamp: Date.now() })
    }
  ]
});
```

### Python Consumer (confluent-kafka-python)

```python
from confluent_kafka import Consumer

consumer = Consumer({
    'bootstrap.servers': 'kafka1:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['events'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Error: {msg.error()}")
    else:
        print(f"Received: {msg.value().decode('utf-8')}")
        consumer.commit(msg)
```

### Stream Processing (Apache Flink)

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStream<Event> events = env
    .addSource(new FlinkKafkaConsumer<>("events", new EventSchema(), properties))
    .keyBy(Event::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new EventCounter());

events.addSink(new FlinkKafkaProducer<>("aggregated-events", new EventSchema(), properties));
env.execute("Event Aggregation");
```

## Decision Frameworks

### Message Broker Selection

```
Need Kafka API compatibility?
├─ YES → Kafka or Redpanda
└─ NO
   ├─ Multi-tenancy critical? → Apache Pulsar
   ├─ Operational simplicity? → Redpanda
   ├─ Mature ecosystem? → Apache Kafka
   └─ Task queues? → RabbitMQ
```

### Stream Processor Selection

```
Millisecond-level latency needed?
├─ YES → Apache Flink
└─ NO
   ├─ Batch + stream hybrid? → Apache Spark
   ├─ Embedded in microservice? → Kafka Streams
   ├─ SQL interface? → ksqlDB
   └─ Python primary? → Spark (PySpark) or Faust
```

### Language Selection

- **TypeScript/Node.js**: API gateways, web services (KafkaJS - 827 code snippets)
- **Python**: Data science, ML pipelines (confluent-kafka-python - 192 snippets)
- **Go**: High-performance microservices (kafka-go - 42 snippets)
- **Java/Scala**: Enterprise applications, Flink, Spark (Kafka Java Client - 683 snippets)

## Common Patterns

### Error Handling Strategy

For production systems, implement:
- **Dead Letter Queue (DLQ)**: Send failed messages to separate topic
- **Retry Logic**: Configurable retry attempts with backoff
- **Graceful Shutdown**: Finish processing, commit offsets, close connections
- **Monitoring**: Track consumer lag, error rates, throughput

### Event Sourcing

Store state changes as immutable events:
- Event store design patterns
- Event schema evolution
- Snapshot strategies
- Temporal queries and audit trails

### Change Data Capture (CDC)

Capture database changes as events using Debezium:
- Real-time data synchronization
- Microservices data integration patterns
- Support for MySQL, PostgreSQL, MongoDB

## Technology Comparison

### Message Broker Comparison

| Feature | Kafka | Pulsar | Redpanda | RabbitMQ |
|---------|-------|--------|----------|----------|
| Throughput | Very High | High | Very High | Medium |
| Latency | Medium | Medium | Low | Low |
| Event Replay | Yes | Yes | Yes | No |
| Multi-Tenancy | Manual | Native | Manual | Manual |
| Operational Complexity | Medium | High | Low | Low |

### Stream Processor Comparison

| Feature | Flink | Spark | Kafka Streams | ksqlDB |
|---------|-------|-------|---------------|--------|
| Processing Model | True streaming | Micro-batch | Library | SQL engine |
| Latency | Millisecond | Second | Millisecond | Second |
| Deployment | Cluster | Cluster | Embedded | Server |

## Troubleshooting

### Consumer Lag Issues
- Check partition count vs consumer count (match for parallelism)
- Increase consumer instances or reduce processing time
- Monitor with Kafka consumer lag metrics

### Message Loss
- Verify producer acks=all configuration
- Check broker replication factor (>1)
- Ensure consumers commit offsets after processing

### Duplicate Messages
- Implement idempotent consumers (track message IDs)
- Use exactly-once semantics (transactions)
- Design for at-least-once delivery

## Related Skills

- [Data Architecture](./architecting-data) - Data platform design and lakehouse patterns
- [Data Transformation](./transforming-data) - Stream processing with Spark and Flink
- [Performance Engineering](./performance-engineering) - Load testing streaming systems

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/streaming-data)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Flink Documentation](https://flink.apache.org/)
- [KafkaJS Documentation](https://kafka.js.org/)
