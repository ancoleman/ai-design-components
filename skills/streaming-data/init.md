# Streaming Data - Master Plan

**Skill Name:** streaming-data
**Skill Level:** Mid (Implementation Patterns)
**Status:** Planning Phase
**Last Updated:** December 2025
**Target Lines:** 500-800 lines (Mid-level skill with multi-language coverage)

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Component Taxonomy](#component-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Multi-Language Implementations](#multi-language-implementations)
7. [Tool Recommendations](#tool-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Streaming Data Matters in 2025

Stream processing has evolved from a specialized technology to a **fundamental architectural pattern** for modern applications. In 2025, streaming data systems power:

- **Real-time AI/ML Pipelines**: Feature engineering, model inference, and continuous learning
- **Event-Driven Architectures**: Microservices communication, CQRS, event sourcing
- **Real-Time Analytics**: Business intelligence, fraud detection, monitoring dashboards
- **IoT and Edge Computing**: Processing billions of sensor events per day
- **Data Integration**: CDC (Change Data Capture), ETL/ELT pipelines, data synchronization

### Market Trends (2025)

1. **Apache Kafka remains dominant** but faces competition from lighter-weight alternatives
2. **Redpanda** gaining traction for performance-critical deployments (C++ implementation, Kafka-compatible)
3. **Apache Pulsar** established for multi-tenancy and geo-replication use cases
4. **Apache Flink** leads true stream processing (sub-millisecond latency)
5. **Spark Streaming** still preferred for batch + stream hybrid workloads
6. **Cloud-native streaming**: AWS Kinesis, Google Dataflow, Confluent Cloud

### Strategic Value of This Skill

This skill provides **language-agnostic streaming patterns** across TypeScript, Python, Go, and Java/Scala - the four dominant languages in streaming ecosystems:

- **TypeScript/Node.js**: Web services, real-time dashboards, API gateways
- **Python**: Data science, ML pipelines, analytics
- **Go**: High-performance microservices, infrastructure tools
- **Java/Scala**: Enterprise systems, big data processing, Flink/Spark jobs

---

## Skill Purpose and Scope

### Core Competencies

This skill teaches:

1. **Message Broker Selection**: When to use Kafka vs Pulsar vs Redpanda vs RabbitMQ
2. **Stream Processing Patterns**: Event time vs processing time, windowing, stateful operations
3. **Producer/Consumer Patterns**: At-least-once, at-most-once, exactly-once semantics
4. **Event Sourcing & CDC**: Capturing database changes, event-driven architectures
5. **Multi-Language Implementations**: Production-ready code in TypeScript, Python, Go, Java

### What This Skill Covers

- **Message Brokers**: Kafka, Pulsar, Redpanda, RabbitMQ (comparison and selection)
- **Stream Processors**: Flink, Spark Streaming, Kafka Streams, ksqlDB
- **Client Libraries**: KafkaJS, confluent-kafka-python, kafka-go, Apache Kafka Java
- **Delivery Guarantees**: At-least-once, at-most-once, exactly-once semantics
- **Advanced Patterns**: Event sourcing, CQRS, saga patterns, outbox pattern
- **Operational Concerns**: Partitioning, rebalancing, backpressure, dead-letter queues

### What This Skill Does NOT Cover

- **Infrastructure deployment**: Kubernetes operators, cloud provider setup (see infrastructure-as-code skill)
- **Monitoring/observability**: Metrics, logging, tracing (see observability skill)
- **Data modeling**: Schema design, serialization formats (covered briefly, not in-depth)
- **Message queues for job processing**: Use message-queues skill for RabbitMQ/SQS-style workloads

### Key Differentiators

- **Multi-language focus**: Working examples in 4 languages (not just conceptual)
- **Decision frameworks**: Clear guidance on technology selection
- **Production patterns**: Error handling, retries, dead-letter queues, monitoring hooks
- **2025 landscape**: Recent research on Kafka vs Redpanda vs Pulsar performance

---

## Research Findings

### Research Methodology

Research conducted December 2025 using:
1. **Google Search Grounding**: Stream processing frameworks, broker comparisons, architecture patterns
2. **Context7 Library Research**: Documentation quality, code examples, trust scores

### Stream Processing Frameworks (2025)

**Landscape Overview:**

- **Apache Kafka**: Industry standard for event streaming, massive ecosystem
- **Apache Flink**: Best-in-class for real-time stream processing (millisecond latency)
- **Apache Spark Streaming**: Mature micro-batch processing, strong ML integration
- **Apache Pulsar**: Multi-tenant architecture, tiered storage, geo-replication
- **Redpanda**: Kafka-compatible, C++ implementation, lower latency
- **Apache Samza**: LinkedIn's framework, high throughput
- **ksqlDB**: SQL interface for Kafka streams
- **RisingWave**: S3-native stream processing (emerging)

### Apache Kafka vs Pulsar vs Redpanda (2025 Analysis)

#### Architecture Comparison

| Feature | Kafka | Pulsar | Redpanda |
|---------|-------|--------|----------|
| **Language** | Java/Scala | Java | C++ |
| **Architecture** | Monolithic brokers | Layered (compute/storage) | Single-binary |
| **Dependencies** | ZooKeeper (KRaft available) | ZooKeeper + BookKeeper | None (Raft consensus) |
| **Deployment** | Moderate complexity | High complexity | Low complexity |
| **Multi-tenancy** | Manual | Native | Manual |
| **Tiered Storage** | Yes (via Confluent) | Native | Yes |

#### Performance Characteristics

**Kafka:**
- High throughput (millions of messages/sec)
- Good for batch workloads
- Higher tail latency under load
- Mature ecosystem, battle-tested

**Pulsar:**
- Horizontal scaling via layered architecture
- Better for multi-tenant scenarios
- Independent compute/storage scaling
- Higher operational complexity

**Redpanda:**
- **Lower latency** than Kafka (C++ efficiency)
- Better core utilization
- Kafka API compatible (drop-in replacement)
- Fewer nodes needed (cost savings)
- Simpler operations (no ZooKeeper/JVM)

**Source**: Research indicates Redpanda offers **better tail latency performance** than Kafka in single-node scenarios due to C++ implementation and better CPU utilization. NATS dominates in pure latency, Redpanda comes next.

#### When to Choose Which

**Choose Kafka when:**
- Need mature ecosystem and tooling
- Require bulletproof persistence and event replay
- Team has Kafka expertise
- Enterprise features via Confluent Platform
- High-throughput batch workloads (fintech, analytics pipelines)

**Choose Pulsar when:**
- Multi-tenancy is critical
- Need tiered storage (hot/cold data separation)
- Geo-replication and cross-datacenter sync
- Dynamic scaling requirements
- Schema evolution and message routing built-in

**Choose Redpanda when:**
- Low latency is paramount
- Want Kafka compatibility without operational overhead
- Limited infrastructure (edge, resource-constrained environments)
- Cost optimization (fewer nodes)
- Greenfield projects with performance requirements

### Apache Flink vs Spark Streaming (2025 Analysis)

#### Processing Model

**Flink:**
- **True stream processing**: Events processed individually as they arrive
- Event-time processing with watermarks
- Low latency (millisecond-level)
- Superior state management
- Better for real-time analytics

**Spark Streaming:**
- **Micro-batch processing**: Groups events into small batches
- Higher latency (seconds)
- Better for batch + streaming hybrid
- Mature ecosystem (MLlib, GraphX, Delta Lake)
- Easier integration with data warehouses

#### Performance Comparison

**Latency Requirements:**
- **Flink**: Millisecond-level responsiveness (fraud detection, monitoring, CEP)
- **Spark**: Near real-time (seconds acceptable) - ETL, aggregations, analytics

**Scalability:**
- **Flink**: Fine-grained resource management, millions of events/sec, sub-millisecond latency
- **Spark**: Better for large-scale batch transformations

**Ecosystem:**
- **Flink**: Superior for event-driven microservices, CEP systems
- **Spark**: Better for machine learning (MLlib), interactive SQL, Databricks/Delta Lake

**State Management:**
- **Flink**: Distributed checkpointing, efficient for long-running jobs
- **Spark**: Less versatile for stateful streaming

**Python Support:**
- **Flink**: Limited Python support
- **Spark**: Excellent PySpark support

#### When to Choose Which

**Choose Flink when:**
- Real-time analytics with millisecond SLAs
- Complex Event Processing (CEP)
- Event-driven microservices
- Exactly-once processing guarantees critical
- High-frequency event streams

**Choose Spark when:**
- Batch ETL + streaming in same pipeline
- Machine learning model training/inference
- Team already uses Databricks/Delta Lake
- Interactive SQL analytics
- Python-first data science teams

### Context7 Library Research Results

#### TypeScript: KafkaJS

**Library ID**: `/tulios/kafkajs`
**Code Snippets**: 827
**Source Reputation**: High
**Benchmark Score**: N/A

**Key Findings:**
- Modern, promise-based API
- Excellent TypeScript support
- Well-documented producer/consumer patterns
- Built-in support for GZIP compression, graceful shutdown
- Good for Node.js microservices, API gateways, real-time web apps

**Example Quality**: Comprehensive examples with error handling, signal traps, async/await patterns

#### Python: confluent-kafka-python

**Library ID**: `/confluentinc/confluent-kafka-python`
**Code Snippets**: 192
**Source Reputation**: High
**Benchmark Score**: 68.8

**Key Findings:**
- Official Confluent client (wrapper around librdkafka)
- High performance (C bindings)
- Supports Avro/JSON serialization via Schema Registry
- AsyncIO support (AIOProducer)
- Good for data engineering, ML pipelines, analytics

**Alternative**: `kafka-python` (86 snippets, score 89.8) - pure Python, easier for simple use cases

#### Go: kafka-go (Segment)

**Library ID**: `/segmentio/kafka-go`
**Code Snippets**: 42
**Source Reputation**: High
**Benchmark Score**: N/A

**Key Findings:**
- Idiomatic Go API (mirrors standard library)
- Zero external dependencies
- Both low-level and high-level APIs
- Good balancer compatibility (Sarama, librdkafka, Java client)
- Good for high-performance microservices

**Alternative**: `confluent-kafka-go` (305 snippets) - official Confluent client with more examples

#### Java: Apache Kafka (Native)

**Library ID**: `/apache/kafka`
**Code Snippets**: 683
**Source Reputation**: High
**Benchmark Score**: 76.9

**Key Findings:**
- The original, most feature-complete implementation
- Supports exactly-once semantics (transactions, idempotence)
- Best for enterprise Java/Scala applications
- Required for Kafka Streams, ksqlDB development

**Related**: Spring Kafka (406 snippets, score 95.8) - excellent for Spring Boot applications

#### Apache Flink

**Library ID**: `/apache/flink`
**Code Snippets**: 3,491
**Source Reputation**: High
**Benchmark Score**: 92.7

**Key Findings:**
- Extensive documentation (153k+ code snippets in master docs)
- Excellent Java/Scala support
- Stream processing + batch APIs unified
- State management, event-time processing, windowing

### Event-Driven Architecture Patterns (2025)

Research attempted for "event-driven architecture patterns" but encountered errors. Key patterns from domain knowledge:

1. **Event Sourcing**: Store all changes as events, rebuild state from event log
2. **CQRS**: Separate read/write models, often paired with event sourcing
3. **Saga Pattern**: Distributed transactions via event choreography
4. **Outbox Pattern**: Reliable event publishing from databases
5. **Event Notification**: Lightweight events triggering downstream actions
6. **Event-Carried State Transfer**: Events contain full state (reduce coupling)

---

## Component Taxonomy

### 1. Message Brokers

#### Apache Kafka
- **Purpose**: Distributed event streaming platform
- **Architecture**: Partitioned log, consumer groups, offset management
- **Strengths**: Durability, replay, massive ecosystem, exactly-once semantics
- **Use Cases**: Event sourcing, data pipelines, metrics aggregation, log aggregation
- **Ecosystem**: Kafka Connect (150+ connectors), Kafka Streams, ksqlDB, Schema Registry

#### Apache Pulsar
- **Purpose**: Multi-tenant messaging and streaming
- **Architecture**: Layered (brokers + BookKeeper storage), topic-based routing
- **Strengths**: Multi-tenancy, geo-replication, tiered storage, schema evolution
- **Use Cases**: Multi-tenant SaaS, cross-region data sync, IoT platforms
- **Ecosystem**: Pulsar Functions, Pulsar SQL, tiered storage (S3/GCS)

#### Redpanda
- **Purpose**: Kafka-compatible streaming platform (performance-optimized)
- **Architecture**: Single-binary, Raft consensus (no ZooKeeper)
- **Strengths**: Low latency, Kafka API compatibility, simple operations, resource efficiency
- **Use Cases**: Performance-critical streams, edge computing, cost-optimized deployments
- **Ecosystem**: Kafka-compatible (works with Kafka tools)

#### RabbitMQ
- **Purpose**: General-purpose message broker
- **Architecture**: Queue-based (vs log-based), AMQP/MQTT/STOMP protocols
- **Strengths**: Flexible routing, message acknowledgements, priority queues
- **Use Cases**: Task queues, RPC patterns, microservices async communication
- **Ecosystem**: Plugins for MQTT, STOMP, management UI

### 2. Stream Processors

#### Apache Flink
- **Purpose**: True stream processing framework
- **Architecture**: Distributed dataflow engine, stateful operators
- **Strengths**: Low latency, event-time processing, exactly-once state, complex event processing
- **Use Cases**: Real-time analytics, fraud detection, monitoring/alerting, CEP systems
- **APIs**: DataStream API (Java/Scala), Table API, SQL, PyFlink (limited)

#### Apache Spark Streaming
- **Purpose**: Micro-batch stream processing
- **Architecture**: RDD-based micro-batches (Structured Streaming uses DataFrames)
- **Strengths**: Unified batch/stream, ML integration (MLlib), SQL support, mature ecosystem
- **Use Cases**: ETL pipelines, batch + stream analytics, ML feature engineering
- **APIs**: DStream API (legacy), Structured Streaming (modern), PySpark

#### Kafka Streams
- **Purpose**: Stream processing library (embedded in applications)
- **Architecture**: Client library (not separate cluster), stateful processing
- **Strengths**: Simple deployment, exactly-once, integrates with Kafka
- **Use Cases**: Microservices stream processing, real-time aggregations
- **APIs**: Java/Scala DSL, Processor API (low-level)

#### ksqlDB
- **Purpose**: SQL interface for Kafka streams
- **Architecture**: Server-based SQL engine on top of Kafka Streams
- **Strengths**: SQL familiarity, materialized views, push queries
- **Use Cases**: Real-time dashboards, analytics, data transformations
- **APIs**: SQL statements (CREATE STREAM, CREATE TABLE, SELECT)

### 3. Event Sourcing & CDC

#### Event Sourcing
- **Pattern**: Store state changes as immutable events
- **Benefits**: Audit trail, temporal queries, event replay
- **Challenges**: Event schema evolution, event versioning, snapshot management
- **Tools**: Kafka as event store, EventStoreDB, Axon Framework

#### Change Data Capture (CDC)
- **Pattern**: Capture database changes as events
- **Benefits**: Real-time data synchronization, microservices data integration
- **Tools**: Debezium (Kafka Connect), Maxwell (MySQL → Kafka), Flink CDC
- **Databases**: MySQL, PostgreSQL, MongoDB, SQL Server, Oracle

### 4. Client Libraries by Language

#### TypeScript/Node.js
- **KafkaJS**: Modern, promise-based, excellent docs
- **Confluent Kafka JavaScript**: High-performance (librdkafka wrapper), KafkaJS-compatible
- **Platformatic Kafka**: Type-safe, pluggable serialization

#### Python
- **confluent-kafka-python**: High-performance (librdkafka), official Confluent
- **kafka-python**: Pure Python, easier for simple cases
- **aiokafka**: AsyncIO support
- **Faust**: Stream processing framework (Kafka Streams for Python)

#### Go
- **kafka-go (Segment)**: Idiomatic Go, zero dependencies
- **confluent-kafka-go**: Official Confluent, high performance
- **sarama (IBM)**: Popular pure-Go client

#### Java/Scala
- **Apache Kafka Java Client**: Official, most feature-complete
- **Spring Kafka**: Excellent Spring Boot integration
- **Kafka Streams**: Embedded stream processing

---

## Decision Frameworks

### Framework 1: Message Broker Selection

```
START → What are your requirements?

1. Do you need Kafka API compatibility?
   YES → Consider Kafka or Redpanda
   NO → Consider Pulsar or RabbitMQ

2. Is multi-tenancy critical?
   YES → Apache Pulsar
   NO → Continue

3. Is operational simplicity a priority?
   YES → Redpanda (no ZooKeeper, single binary)
   NO → Continue

4. Do you need mature ecosystem and tooling?
   YES → Apache Kafka
   NO → Consider Redpanda for better performance

5. Is this for task queues (not event streams)?
   YES → RabbitMQ or see message-queues skill
   NO → Kafka/Redpanda/Pulsar
```

**Decision Matrix:**

| Requirement | Kafka | Pulsar | Redpanda | RabbitMQ |
|-------------|-------|--------|----------|----------|
| High throughput | ✓✓✓ | ✓✓ | ✓✓✓ | ✓ |
| Low latency | ✓ | ✓ | ✓✓✓ | ✓✓ |
| Event replay | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✗ |
| Multi-tenancy | ✓ | ✓✓✓ | ✓ | ✓ |
| Operational simplicity | ✓ | ✗ | ✓✓✓ | ✓✓ |
| Ecosystem maturity | ✓✓✓ | ✓✓ | ✓✓ | ✓✓✓ |
| Cost efficiency | ✓ | ✓ | ✓✓✓ | ✓✓ |

### Framework 2: Stream Processor Selection

```
START → What is your latency requirement?

1. Need millisecond-level latency?
   YES → Apache Flink
   NO → Continue

2. Need batch + stream in same pipeline?
   YES → Apache Spark Streaming
   NO → Continue

3. Is this embedded in a microservice?
   YES → Kafka Streams
   NO → Continue

4. Need SQL interface for analysts?
   YES → ksqlDB
   NO → Apache Flink or Spark

5. Is Python your primary language?
   YES → Spark (PySpark) or Faust
   NO → Flink (Java/Scala)
```

### Framework 3: Delivery Guarantees

**At-Most-Once:**
- Messages may be lost
- No duplicates
- Lowest overhead
- **Use case**: Metrics, logs (loss acceptable)

**At-Least-Once:**
- Messages never lost
- May have duplicates
- Moderate overhead
- **Use case**: Most applications (idempotent consumers)

**Exactly-Once:**
- Messages never lost or duplicated
- Highest overhead
- **Use case**: Financial transactions, critical state updates

**Implementation:**

| Language | Library | Exactly-Once Support |
|----------|---------|---------------------|
| TypeScript | KafkaJS | Idempotent producer, transactions |
| Python | confluent-kafka-python | Idempotent producer, transactions |
| Go | kafka-go | Idempotent producer |
| Java | Kafka Java Client | Full support (transactions, idempotence) |

### Framework 4: Language Selection for Streaming

**Choose TypeScript/Node.js when:**
- Building API gateways, web services
- Real-time dashboards, websocket backends
- Team is JavaScript-first
- Need rapid development

**Choose Python when:**
- Data science, ML pipelines
- Analytics, data engineering
- Team is Python-first (data scientists)
- Integration with NumPy/Pandas/TensorFlow

**Choose Go when:**
- High-performance microservices
- Infrastructure tools
- Low resource usage critical
- Team values simplicity and performance

**Choose Java/Scala when:**
- Enterprise applications
- Using Kafka Streams, Flink, Spark
- Need exactly-once semantics
- Large-scale stream processing

---

## Multi-Language Implementations

### TypeScript (Node.js) - KafkaJS

#### Producer Example

```typescript
import { Kafka, CompressionTypes, Partitioners } from 'kafkajs';

interface MessagePayload {
  userId: string;
  action: string;
  timestamp: number;
}

class EventProducer {
  private kafka: Kafka;
  private producer: Producer;

  constructor(brokers: string[]) {
    this.kafka = new Kafka({
      clientId: 'my-app-producer',
      brokers: brokers,
    });

    this.producer = this.kafka.producer({
      createPartitioner: Partitioners.LegacyPartitioner,
    });
  }

  async connect(): Promise<void> {
    await this.producer.connect();
    console.log('Producer connected');
  }

  async sendEvent(topic: string, event: MessagePayload): Promise<void> {
    try {
      await this.producer.send({
        topic,
        compression: CompressionTypes.GZIP,
        messages: [
          {
            key: event.userId,
            value: JSON.stringify(event),
            headers: {
              'correlation-id': generateCorrelationId(),
            },
          },
        ],
      });
    } catch (error) {
      console.error('Failed to send event:', error);
      throw error;
    }
  }

  async sendBatch(topic: string, events: MessagePayload[]): Promise<void> {
    const messages = events.map(event => ({
      key: event.userId,
      value: JSON.stringify(event),
    }));

    await this.producer.send({
      topic,
      messages,
    });
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
  }
}

// Usage
const producer = new EventProducer(['localhost:9092']);
await producer.connect();
await producer.sendEvent('user-actions', {
  userId: 'user-123',
  action: 'login',
  timestamp: Date.now(),
});
```

#### Consumer Example

```typescript
import { Kafka, EachMessagePayload } from 'kafkajs';

class EventConsumer {
  private kafka: Kafka;
  private consumer: Consumer;

  constructor(brokers: string[], groupId: string) {
    this.kafka = new Kafka({
      clientId: 'my-app-consumer',
      brokers,
    });

    this.consumer = this.kafka.consumer({ groupId });
  }

  async connect(): Promise<void> {
    await this.consumer.connect();
  }

  async subscribe(topics: string[]): Promise<void> {
    await this.consumer.subscribe({
      topics,
      fromBeginning: false,
    });
  }

  async startConsuming(handler: (message: any) => Promise<void>): Promise<void> {
    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }: EachMessagePayload) => {
        const value = message.value?.toString();
        if (!value) return;

        try {
          const parsed = JSON.parse(value);
          await handler(parsed);

          // Message processing successful - offset committed automatically
        } catch (error) {
          console.error('Message processing failed:', error);
          // Implement dead-letter queue logic here
          await this.sendToDeadLetterQueue(topic, message);
        }
      },
    });
  }

  private async sendToDeadLetterQueue(topic: string, message: Message): Promise<void> {
    // Send to DLQ topic for later analysis
    const dlqTopic = `${topic}.dlq`;
    // Implementation depends on your DLQ strategy
  }

  async disconnect(): Promise<void> {
    await this.consumer.disconnect();
  }
}

// Usage
const consumer = new EventConsumer(['localhost:9092'], 'my-consumer-group');
await consumer.connect();
await consumer.subscribe(['user-actions']);
await consumer.startConsuming(async (event) => {
  console.log('Processing event:', event);
  // Your business logic here
});
```

### Python - confluent-kafka-python

#### Producer Example

```python
from confluent_kafka import Producer, KafkaException
from typing import Dict, Any, Optional
import json
import uuid

class EventProducer:
    def __init__(self, bootstrap_servers: str):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'my-app-producer',
            'acks': 'all',  # Wait for all replicas
            'retries': 3,
            'enable.idempotence': True,  # Exactly-once semantics
        }
        self.producer = Producer(self.config)

    def delivery_report(self, err, msg):
        """Callback for delivery reports."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

    def send_event(self, topic: str, event: Dict[str, Any], key: Optional[str] = None) -> None:
        """Send a single event to Kafka."""
        try:
            self.producer.produce(
                topic=topic,
                key=key.encode('utf-8') if key else None,
                value=json.dumps(event).encode('utf-8'),
                callback=self.delivery_report,
                headers={
                    'correlation-id': str(uuid.uuid4()),
                }
            )
            # Trigger delivery callbacks
            self.producer.poll(0)
        except KafkaException as e:
            print(f'Failed to send event: {e}')
            raise

    def flush(self) -> None:
        """Wait for all messages to be delivered."""
        self.producer.flush()

    def close(self) -> None:
        """Close the producer."""
        self.producer.flush()

# Usage
producer = EventProducer('localhost:9092')
producer.send_event('user-actions', {
    'user_id': 'user-123',
    'action': 'login',
    'timestamp': int(time.time())
}, key='user-123')
producer.flush()
```

#### Consumer Example

```python
from confluent_kafka import Consumer, KafkaException
from typing import Callable, List
import json

class EventConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,  # Manual commit for error handling
        }
        self.consumer = Consumer(self.config)

    def subscribe(self, topics: List[str]) -> None:
        """Subscribe to topics."""
        self.consumer.subscribe(topics)

    def consume(self, handler: Callable[[dict], None], batch_size: int = 1) -> None:
        """Start consuming messages."""
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                try:
                    # Decode message
                    value = json.loads(msg.value().decode('utf-8'))

                    # Process message
                    handler(value)

                    # Commit offset after successful processing
                    self.consumer.commit(message=msg)

                except json.JSONDecodeError as e:
                    print(f"Failed to decode message: {e}")
                    # Send to dead-letter queue
                    self._send_to_dlq(msg)
                    self.consumer.commit(message=msg)

                except Exception as e:
                    print(f"Error processing message: {e}")
                    # Don't commit - message will be reprocessed

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()

    def _send_to_dlq(self, msg):
        """Send failed message to dead-letter queue."""
        # Implementation depends on your DLQ strategy
        pass

    def close(self) -> None:
        """Close the consumer."""
        self.consumer.close()

# Usage
consumer = EventConsumer('localhost:9092', 'my-consumer-group')
consumer.subscribe(['user-actions'])

def handle_event(event: dict):
    print(f"Processing event: {event}")
    # Your business logic here

consumer.consume(handle_event)
```

### Go - kafka-go

#### Producer Example

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "time"

    "github.com/segmentio/kafka-go"
)

type Event struct {
    UserID    string `json:"user_id"`
    Action    string `json:"action"`
    Timestamp int64  `json:"timestamp"`
}

type EventProducer struct {
    writer *kafka.Writer
}

func NewEventProducer(brokers []string, topic string) *EventProducer {
    return &EventProducer{
        writer: &kafka.Writer{
            Addr:     kafka.TCP(brokers...),
            Topic:    topic,
            Balancer: &kafka.LeastBytes{},
            // Idempotent writes
            RequiredAcks: kafka.RequireAll,
            MaxAttempts:  3,
            // Compression
            Compression: kafka.Gzip,
        },
    }
}

func (p *EventProducer) SendEvent(ctx context.Context, event Event) error {
    value, err := json.Marshal(event)
    if err != nil {
        return fmt.Errorf("failed to marshal event: %w", err)
    }

    err = p.writer.WriteMessages(ctx, kafka.Message{
        Key:   []byte(event.UserID),
        Value: value,
        Headers: []kafka.Header{
            {Key: "correlation-id", Value: []byte(generateCorrelationID())},
        },
    })

    if err != nil {
        return fmt.Errorf("failed to write message: %w", err)
    }

    return nil
}

func (p *EventProducer) SendBatch(ctx context.Context, events []Event) error {
    messages := make([]kafka.Message, len(events))
    for i, event := range events {
        value, err := json.Marshal(event)
        if err != nil {
            return fmt.Errorf("failed to marshal event %d: %w", i, err)
        }
        messages[i] = kafka.Message{
            Key:   []byte(event.UserID),
            Value: value,
        }
    }

    return p.writer.WriteMessages(ctx, messages...)
}

func (p *EventProducer) Close() error {
    return p.writer.Close()
}

// Usage
func main() {
    producer := NewEventProducer([]string{"localhost:9092"}, "user-actions")
    defer producer.Close()

    event := Event{
        UserID:    "user-123",
        Action:    "login",
        Timestamp: time.Now().Unix(),
    }

    if err := producer.SendEvent(context.Background(), event); err != nil {
        fmt.Printf("Failed to send event: %v\n", err)
    }
}
```

#### Consumer Example

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "github.com/segmentio/kafka-go"
)

type EventConsumer struct {
    reader *kafka.Reader
}

func NewEventConsumer(brokers []string, topic string, groupID string) *EventConsumer {
    return &EventConsumer{
        reader: kafka.NewReader(kafka.ReaderConfig{
            Brokers:  brokers,
            Topic:    topic,
            GroupID:  groupID,
            MaxBytes: 10e6, // 10MB
            // Manual commit for error handling
            CommitInterval: 0,
        }),
    }
}

func (c *EventConsumer) Consume(ctx context.Context, handler func(Event) error) error {
    for {
        msg, err := c.reader.FetchMessage(ctx)
        if err != nil {
            if err == context.Canceled {
                break
            }
            log.Printf("Error fetching message: %v", err)
            continue
        }

        var event Event
        if err := json.Unmarshal(msg.Value, &event); err != nil {
            log.Printf("Failed to unmarshal message: %v", err)
            // Send to DLQ
            c.sendToDLQ(msg)
            // Commit to move forward
            c.reader.CommitMessages(ctx, msg)
            continue
        }

        // Process message
        if err := handler(event); err != nil {
            log.Printf("Error processing event: %v", err)
            // Don't commit - message will be reprocessed
            continue
        }

        // Commit offset after successful processing
        if err := c.reader.CommitMessages(ctx, msg); err != nil {
            log.Printf("Failed to commit offset: %v", err)
        }
    }

    return nil
}

func (c *EventConsumer) sendToDLQ(msg kafka.Message) {
    // Implementation depends on your DLQ strategy
}

func (c *EventConsumer) Close() error {
    return c.reader.Close()
}

// Usage
func main() {
    consumer := NewEventConsumer(
        []string{"localhost:9092"},
        "user-actions",
        "my-consumer-group",
    )
    defer consumer.Close()

    handler := func(event Event) error {
        fmt.Printf("Processing event: %+v\n", event)
        // Your business logic here
        return nil
    }

    if err := consumer.Consume(context.Background(), handler); err != nil {
        log.Fatalf("Consumer error: %v", err)
    }
}
```

### Java - Apache Kafka

#### Producer Example

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Properties;
import java.util.UUID;
import java.util.concurrent.Future;

public class EventProducer {
    private final KafkaProducer<String, String> producer;
    private final ObjectMapper objectMapper;
    private final String topic;

    public EventProducer(String bootstrapServers, String topic) {
        this.topic = topic;
        this.objectMapper = new ObjectMapper();

        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.CLIENT_ID_CONFIG, "my-app-producer");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // Exactly-once semantics
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);

        // Compression
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "gzip");

        this.producer = new KafkaProducer<>(props);
    }

    public void sendEvent(Event event) throws Exception {
        String key = event.getUserId();
        String value = objectMapper.writeValueAsString(event);

        ProducerRecord<String, String> record = new ProducerRecord<>(
            topic,
            key,
            value
        );

        // Add headers
        record.headers().add("correlation-id", UUID.randomUUID().toString().getBytes());

        // Asynchronous send with callback
        producer.send(record, new Callback() {
            @Override
            public void onCompletion(RecordMetadata metadata, Exception exception) {
                if (exception != null) {
                    System.err.println("Failed to send event: " + exception.getMessage());
                } else {
                    System.out.printf("Event sent to partition %d with offset %d%n",
                        metadata.partition(), metadata.offset());
                }
            }
        });
    }

    public RecordMetadata sendEventSync(Event event) throws Exception {
        String key = event.getUserId();
        String value = objectMapper.writeValueAsString(event);

        ProducerRecord<String, String> record = new ProducerRecord<>(topic, key, value);

        // Synchronous send (blocks until complete)
        Future<RecordMetadata> future = producer.send(record);
        return future.get();
    }

    public void close() {
        producer.flush();
        producer.close();
    }
}

// Event class
class Event {
    private String userId;
    private String action;
    private long timestamp;

    // Constructors, getters, setters
    public Event(String userId, String action, long timestamp) {
        this.userId = userId;
        this.action = action;
        this.timestamp = timestamp;
    }

    public String getUserId() { return userId; }
    public String getAction() { return action; }
    public long getTimestamp() { return timestamp; }
}

// Usage
public class Main {
    public static void main(String[] args) throws Exception {
        EventProducer producer = new EventProducer("localhost:9092", "user-actions");

        Event event = new Event("user-123", "login", System.currentTimeMillis());
        producer.sendEvent(event);

        producer.close();
    }
}
```

#### Consumer Example

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class EventConsumer {
    private final KafkaConsumer<String, String> consumer;
    private final ObjectMapper objectMapper;

    public EventConsumer(String bootstrapServers, String groupId, String topic) {
        this.objectMapper = new ObjectMapper();

        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        // Manual offset commit for error handling
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

        this.consumer = new KafkaConsumer<>(props);
        this.consumer.subscribe(Collections.singletonList(topic));
    }

    public void consume(EventHandler handler) {
        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));

                for (ConsumerRecord<String, String> record : records) {
                    try {
                        Event event = objectMapper.readValue(record.value(), Event.class);

                        // Process event
                        handler.handle(event);

                        // Commit offset after successful processing
                        consumer.commitSync();

                    } catch (Exception e) {
                        System.err.println("Error processing event: " + e.getMessage());
                        // Send to DLQ
                        sendToDLQ(record);
                        // Commit to move forward
                        consumer.commitSync();
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Consumer error: " + e.getMessage());
        } finally {
            consumer.close();
        }
    }

    private void sendToDLQ(ConsumerRecord<String, String> record) {
        // Implementation depends on your DLQ strategy
    }

    public void close() {
        consumer.close();
    }
}

// Event handler interface
interface EventHandler {
    void handle(Event event) throws Exception;
}

// Usage
public class Main {
    public static void main(String[] args) {
        EventConsumer consumer = new EventConsumer(
            "localhost:9092",
            "my-consumer-group",
            "user-actions"
        );

        consumer.consume(event -> {
            System.out.println("Processing event: " + event.getUserId());
            // Your business logic here
        });
    }
}
```

---

## Tool Recommendations

### Message Brokers

| Tool | Trust Score | Code Snippets | Recommendation |
|------|-------------|---------------|----------------|
| **Apache Kafka** | High (76.9) | 683 | Primary choice for event streaming |
| **Redpanda** | N/A | N/A | Best for performance-critical, low-latency use cases |
| **Apache Pulsar** | N/A | N/A | Best for multi-tenancy, geo-replication |
| **RabbitMQ** | N/A | N/A | Best for traditional message queues, RPC |

### Stream Processors

| Tool | Trust Score | Code Snippets | Recommendation |
|------|-------------|---------------|----------------|
| **Apache Flink** | High (92.7) | 3,491 | Best for real-time, low-latency stream processing |
| **Apache Spark** | High (77.1) | 2,949 | Best for batch + stream, ML integration |
| **Kafka Streams** | Included in Kafka | N/A | Best for embedded stream processing |
| **ksqlDB** | N/A | N/A | Best for SQL-based stream processing |

### Client Libraries

#### TypeScript/Node.js
- **KafkaJS** (High reputation, 827 snippets) - **RECOMMENDED**
- Confluent Kafka JavaScript (High, 91 snippets, score 70.8) - Alternative for performance

#### Python
- **confluent-kafka-python** (High, 192 snippets, score 68.8) - **RECOMMENDED**
- kafka-python (High, 86 snippets, score 89.8) - Good for simple use cases
- aiokafka (High, 59 snippets) - For async/await

#### Go
- **kafka-go (Segment)** (High, 42 snippets) - **RECOMMENDED** for idiomatic Go
- confluent-kafka-go (High, 305 snippets) - Alternative for official support

#### Java/Scala
- **Apache Kafka Java Client** (High, 683 snippets, score 76.9) - **RECOMMENDED**
- Spring Kafka (High, 406 snippets, score 95.8) - For Spring Boot applications

### Related Tools

- **Debezium** - CDC for MySQL, PostgreSQL, MongoDB (Kafka Connect)
- **Schema Registry** - Avro/Protobuf/JSON schema management
- **Kafka Connect** - 150+ connectors for data integration
- **Kafka UI** (provectus) - Web UI for managing Kafka clusters

---

## Skill Structure Design

### Proposed SKILL.md Structure

```markdown
---
name: streaming-data
description: Build event streaming and real-time data pipelines with Kafka, Pulsar, Redpanda, Flink, and Spark. Covers producer/consumer patterns, stream processing, event sourcing, and CDC across TypeScript, Python, Go, and Java. Choose brokers and processors based on latency, throughput, and operational requirements.
---

# Streaming Data Processing

## Purpose
Enable building production-ready event streaming systems and real-time data pipelines across multiple languages and frameworks.

## When to Use This Skill
- Building event-driven architectures
- Real-time analytics and monitoring
- Data integration pipelines (CDC, ETL)
- Microservices async communication
- Log/metrics aggregation

## Quick Start

### Decision: Choose a Message Broker
Reference: references/broker-selection.md

### Decision: Choose a Stream Processor
Reference: references/processor-selection.md

### Implementation Patterns
Reference language-specific guides:
- references/typescript-patterns.md
- references/python-patterns.md
- references/go-patterns.md
- references/java-patterns.md

### Advanced Patterns
- references/event-sourcing.md
- references/cdc-patterns.md
- references/exactly-once.md
- references/error-handling.md

## Scripts (Token-Free Execution)

### Validate Kafka Configuration
scripts/validate-kafka-config.py - Check producer/consumer configuration

### Generate Schema Registry Templates
scripts/generate-schema.py - Create Avro/Protobuf schemas

### Benchmark Throughput
scripts/benchmark-throughput.sh - Test producer/consumer performance
```

### Bundled Resources Structure

```
streaming-data/
├── SKILL.md (main skill file)
├── references/
│   ├── broker-selection.md          # Decision framework for Kafka vs Pulsar vs Redpanda
│   ├── processor-selection.md       # Flink vs Spark vs Kafka Streams
│   ├── delivery-guarantees.md       # At-least-once, exactly-once patterns
│   ├── typescript-patterns.md       # KafkaJS patterns
│   ├── python-patterns.md           # confluent-kafka-python patterns
│   ├── go-patterns.md               # kafka-go patterns
│   ├── java-patterns.md             # Kafka Java client patterns
│   ├── event-sourcing.md            # Event sourcing architecture
│   ├── cdc-patterns.md              # Change Data Capture with Debezium
│   ├── exactly-once.md              # Exactly-once semantics implementation
│   └── error-handling.md            # DLQ, retries, backpressure
├── scripts/
│   ├── validate-kafka-config.py     # Configuration validator
│   ├── generate-schema.py           # Schema Registry template generator
│   └── benchmark-throughput.sh      # Performance testing
└── examples/
    ├── typescript-microservice/     # Full TypeScript example
    ├── python-analytics/            # Full Python example
    ├── go-high-perf/                # Full Go example
    └── java-enterprise/             # Full Java example
```

### Progressive Disclosure Strategy

**SKILL.md** (main file, <500 lines):
- Quick decision frameworks
- When to use which broker/processor
- Links to language-specific guides
- Links to advanced patterns

**references/** (loaded on-demand):
- Detailed implementation guides
- Language-specific patterns
- Architecture patterns (event sourcing, CDC)

**scripts/** (executed, NOT loaded into context):
- Configuration validators
- Schema generators
- Performance benchmarks

**examples/** (optional reference):
- Full working applications
- Deployment configurations

---

## Integration Points

### Related Skills

1. **message-queues** (if exists)
   - Overlap: RabbitMQ, async communication
   - Distinction: message-queues focuses on task processing; streaming-data on event logs

2. **data-architecture** (if exists)
   - Integration: CDC feeds data warehouses, lake houses
   - Streaming as data integration layer

3. **microservices** (if exists)
   - Event-driven architecture patterns
   - Service-to-service async communication

4. **infrastructure-as-code** (exists)
   - Deployment: Kubernetes operators (Strimzi for Kafka)
   - Infrastructure: Terraform modules for Kafka/Pulsar

5. **observability/monitoring** (if exists)
   - Metrics: JMX, Prometheus exporters
   - Tracing: OpenTelemetry integration

### Technology Ecosystem

**Kafka Ecosystem:**
- Kafka Connect (data integration)
- Schema Registry (schema management)
- ksqlDB (stream SQL)
- Kafka Streams (embedded processing)

**Flink Ecosystem:**
- Flink CDC (change data capture)
- Flink SQL (stream SQL)
- Flink Kubernetes Operator

**Complementary Tools:**
- Debezium (CDC)
- Avro/Protobuf (serialization)
- Kubernetes (deployment)
- Prometheus (monitoring)

---

## Implementation Roadmap

### Phase 1: Core Skill (Week 1)

**Tasks:**
1. Create SKILL.md with frontmatter and quick start
2. Write broker-selection.md (Kafka vs Pulsar vs Redpanda)
3. Write processor-selection.md (Flink vs Spark)
4. Create delivery-guarantees.md (at-least-once, exactly-once)

**Deliverable:** Basic skill with decision frameworks

### Phase 2: Multi-Language Patterns (Week 2)

**Tasks:**
1. Write typescript-patterns.md (KafkaJS examples)
2. Write python-patterns.md (confluent-kafka-python)
3. Write go-patterns.md (kafka-go)
4. Write java-patterns.md (Kafka Java client)

**Deliverable:** Production-ready code examples in 4 languages

### Phase 3: Advanced Patterns (Week 3)

**Tasks:**
1. Write event-sourcing.md (architecture patterns)
2. Write cdc-patterns.md (Debezium integration)
3. Write exactly-once.md (transactional processing)
4. Write error-handling.md (DLQ, retries, backpressure)

**Deliverable:** Advanced architectural guidance

### Phase 4: Scripts & Examples (Week 4)

**Tasks:**
1. Create validate-kafka-config.py script
2. Create generate-schema.py script
3. Create benchmark-throughput.sh script
4. Build full examples/ directory

**Deliverable:** Executable tools and reference implementations

### Phase 5: Testing & Validation (Week 5)

**Tasks:**
1. Test skill with Claude B on real scenarios
2. Validate all code examples
3. Check progressive disclosure (token usage)
4. Peer review with other developers

**Deliverable:** Production-ready skill

### Phase 6: Documentation & Polish (Week 6)

**Tasks:**
1. Add ASCII diagrams to references/
2. Create troubleshooting guide
3. Add performance tuning guide
4. Final review and publish

**Deliverable:** Polished, comprehensive skill

---

## Evaluation Scenarios

### Scenario 1: TypeScript Microservice
**Task:** "Build a TypeScript microservice that consumes user events from Kafka and writes them to PostgreSQL"

**Expected Outcome:**
- Uses KafkaJS consumer
- Implements error handling with DLQ
- Shows manual offset commits
- Includes graceful shutdown

### Scenario 2: Python Analytics Pipeline
**Task:** "Create a Python consumer that reads click events, aggregates them in 5-minute windows, and writes to Redshift"

**Expected Outcome:**
- Uses confluent-kafka-python
- Shows batch processing pattern
- Implements exactly-once semantics
- Includes Schema Registry integration

### Scenario 3: Go High-Performance Service
**Task:** "Build a Go service that reads from Kafka and forwards events to multiple downstream systems with <10ms latency"

**Expected Outcome:**
- Uses kafka-go with manual commits
- Shows concurrent processing pattern
- Implements backpressure handling
- Includes performance metrics

### Scenario 4: Java Enterprise Application
**Task:** "Implement exactly-once processing with Kafka transactions for a financial transaction system"

**Expected Outcome:**
- Uses Kafka Java client with transactions
- Shows transactional producer/consumer
- Implements idempotent processing
- Includes error recovery patterns

---

## Success Metrics

1. **Code Quality**: All examples compile and run
2. **Token Efficiency**: SKILL.md under 500 lines, progressive disclosure working
3. **Language Coverage**: Working examples in TypeScript, Python, Go, Java
4. **Decision Clarity**: Clear frameworks for broker/processor selection
5. **Production Readiness**: Error handling, monitoring hooks, performance patterns

---

## References & Sources

### Research Sources (December 2025)

1. **Google Search Grounding**:
   - "stream processing frameworks 2025"
   - "Apache Kafka vs Pulsar vs Redpanda comparison"
   - "Apache Flink vs Spark Streaming 2025"

2. **Context7 Documentation**:
   - KafkaJS (/tulios/kafkajs) - 827 snippets
   - confluent-kafka-python (/confluentinc/confluent-kafka-python) - 192 snippets, score 68.8
   - kafka-go (/segmentio/kafka-go) - 42 snippets
   - Apache Kafka (/apache/kafka) - 683 snippets, score 76.9
   - Apache Flink (/apache/flink) - 3,491 snippets, score 92.7

### Key Insights

1. **Redpanda vs Kafka**: Redpanda offers better tail latency and operational simplicity (no ZooKeeper, C++ implementation)
2. **Flink vs Spark**: Flink for millisecond latency, Spark for batch + stream hybrid
3. **Exactly-Once**: Requires idempotent producers + transactions (well-supported in Kafka)
4. **Multi-Language**: Each language has mature Kafka clients with good documentation

---

## Appendix: Technology Comparison Tables

### Message Broker Comparison

| Feature | Kafka | Pulsar | Redpanda | RabbitMQ |
|---------|-------|--------|----------|----------|
| **Primary Use Case** | Event streaming | Multi-tenant streaming | High-perf streaming | Task queues |
| **Throughput** | Very High | High | Very High | Medium |
| **Latency** | Medium | Medium | Low | Low |
| **Event Replay** | Yes | Yes | Yes | No |
| **Operational Complexity** | Medium | High | Low | Low |
| **Multi-Tenancy** | Manual | Native | Manual | Manual |
| **Ecosystem Maturity** | Excellent | Good | Good | Excellent |
| **Best For** | Enterprise, big data | SaaS, IoT | Performance-critical | Simple queues |

### Stream Processor Comparison

| Feature | Flink | Spark Streaming | Kafka Streams | ksqlDB |
|---------|-------|----------------|---------------|--------|
| **Processing Model** | True streaming | Micro-batch | Library | SQL engine |
| **Latency** | Millisecond | Second | Millisecond | Second |
| **State Management** | Excellent | Good | Good | Good |
| **Deployment** | Cluster | Cluster | Embedded | Server |
| **SQL Support** | Yes (Table API) | Yes (Structured) | No | Yes (native) |
| **Best For** | Real-time analytics | Batch + stream | Microservices | Analysts |

### Language Client Comparison

| Language | Primary Library | Trust Score | Snippets | Best For |
|----------|----------------|-------------|----------|----------|
| **TypeScript** | KafkaJS | High | 827 | Web services, APIs |
| **Python** | confluent-kafka-python | High (68.8) | 192 | Data pipelines, ML |
| **Go** | kafka-go | High | 42 | High-performance services |
| **Java** | Kafka Java Client | High (76.9) | 683 | Enterprise, Flink/Spark |

---

**End of Master Plan**
