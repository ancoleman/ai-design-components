# Kafka - Event Streaming Platform

Apache Kafka is a distributed event streaming platform designed for high-throughput, fault-tolerant log aggregation and event sourcing.


## Table of Contents

- [When to Use Kafka](#when-to-use-kafka)
- [Core Concepts](#core-concepts)
  - [Topics and Partitions](#topics-and-partitions)
  - [Consumer Groups](#consumer-groups)
  - [Offsets](#offsets)
- [Python Implementation](#python-implementation)
  - [Producer with Confluent Kafka](#producer-with-confluent-kafka)
  - [Consumer with Confluent Kafka](#consumer-with-confluent-kafka)
- [Exactly-Once Semantics](#exactly-once-semantics)
  - [Idempotent Producer](#idempotent-producer)
  - [Transactional Producer](#transactional-producer)
- [Partitioning Strategies](#partitioning-strategies)
  - [Key-Based Partitioning (Default)](#key-based-partitioning-default)
  - [Custom Partitioner](#custom-partitioner)
- [Consumer Rebalancing](#consumer-rebalancing)
  - [Graceful Shutdown](#graceful-shutdown)
  - [Rebalance Listener](#rebalance-listener)
- [Performance Tuning](#performance-tuning)
  - [Producer Throughput Optimization](#producer-throughput-optimization)
  - [Consumer Throughput Optimization](#consumer-throughput-optimization)
- [Monitoring](#monitoring)
  - [Key Metrics](#key-metrics)
  - [Prometheus Metrics Exporter](#prometheus-metrics-exporter)
- [Common Patterns](#common-patterns)
  - [Dead Letter Queue](#dead-letter-queue)
  - [Event Sourcing](#event-sourcing)
- [Troubleshooting](#troubleshooting)
  - [Consumer Not Receiving Messages](#consumer-not-receiving-messages)
  - [Consumer Lag Growing](#consumer-lag-growing)
  - [Duplicate Messages](#duplicate-messages)
- [Configuration Best Practices](#configuration-best-practices)
  - [Production Producer Config](#production-producer-config)
  - [Production Consumer Config](#production-consumer-config)
- [Related Patterns](#related-patterns)

## When to Use Kafka

**Best for:**
- Event streaming (500K-1M+ msg/s)
- Log aggregation across microservices
- Event sourcing / CQRS architectures
- Real-time analytics pipelines
- Long-term event retention (days/weeks)

**Not ideal for:**
- Simple background job queues (use Celery/BullMQ)
- Request-reply patterns (use NATS)
- Low-latency RPC (use gRPC/HTTP)

## Core Concepts

### Topics and Partitions

**Topics** are categories for messages. **Partitions** enable parallelism.

```
Topic: "orders"
├─ Partition 0: [msg1, msg4, msg7, ...]
├─ Partition 1: [msg2, msg5, msg8, ...]
└─ Partition 2: [msg3, msg6, msg9, ...]
```

**Key points:**
- Messages with same key go to same partition (ordering guarantee)
- More partitions = more parallelism
- Partition count cannot decrease (only increase)
- Recommended: Start with partitions = max expected consumers

### Consumer Groups

**Consumer group** coordinates partition assignment across consumers.

```
Consumer Group: "order-processors"
├─ Consumer 1 → Partition 0, 1
├─ Consumer 2 → Partition 2, 3
└─ Consumer 3 → Partition 4, 5
```

**Key points:**
- One partition assigned to one consumer per group
- Adding consumers (up to partition count) increases parallelism
- Rebalancing occurs when consumers join/leave
- Different groups consume independently

### Offsets

**Offset** tracks position in partition for each consumer group.

```
Partition 0: [0] [1] [2] [3] [4] [5] [6] [7] [8] [9]
                                    ↑
                            Consumer offset: 5
```

**Commit strategies:**
- **Auto-commit** (default): Periodic background commit (may lose messages on crash)
- **Manual commit**: Commit after processing (exactly-once semantics)

## Python Implementation

### Producer with Confluent Kafka

```python
from confluent_kafka import Producer
import json
import uuid

# Producer configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'order-producer',
    'acks': 'all',  # Wait for all replicas (strongest guarantee)
    'compression.type': 'lz4',  # Fast compression
    'batch.size': 32768,  # 32KB batches
    'linger.ms': 10,  # Wait 10ms for batching
}

producer = Producer(config)

def delivery_callback(err, msg):
    """Called when message delivered or failed"""
    if err:
        print(f'Delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

# Produce message with key for partitioning
order = {
    'order_id': 'ord_123',
    'customer_id': 'cus_456',
    'total': 99.99
}

producer.produce(
    topic='orders',
    key='ord_123',  # Messages with same key go to same partition
    value=json.dumps(order).encode('utf-8'),
    on_delivery=delivery_callback
)

# Flush ensures all messages sent before program exits
producer.flush()
```

### Consumer with Confluent Kafka

```python
from confluent_kafka import Consumer, KafkaException, KafkaError
import json

# Consumer configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-processors',
    'auto.offset.reset': 'earliest',  # Start from beginning if no offset
    'enable.auto.commit': False,  # Manual commit for exactly-once
    'max.poll.interval.ms': 300000,  # 5 minutes max processing time
}

consumer = Consumer(config)
consumer.subscribe(['orders'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue  # No message within timeout

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f'End of partition {msg.partition()}')
            else:
                raise KafkaException(msg.error())
        else:
            # Process message
            order = json.loads(msg.value().decode('utf-8'))
            print(f'Processing order: {order}')

            try:
                process_order(order)

                # Manual commit after successful processing
                consumer.commit(message=msg)

            except Exception as e:
                print(f'Processing failed: {e}')
                # Don't commit - message will be redelivered

finally:
    consumer.close()
```

## Exactly-Once Semantics

Kafka supports exactly-once processing through **idempotent producers** and **transactional writes**.

### Idempotent Producer

```python
config = {
    'bootstrap.servers': 'localhost:9092',
    'enable.idempotence': True,  # Prevents duplicate messages
    'acks': 'all',
    'max.in.flight.requests.per.connection': 5,
}

producer = Producer(config)
```

**How it works:**
- Producer assigns sequence numbers to messages
- Broker detects and rejects duplicates
- Guarantees: No duplicates even on retries

### Transactional Producer

```python
from confluent_kafka import Producer

config = {
    'bootstrap.servers': 'localhost:9092',
    'transactional.id': 'order-processor-1',  # Unique per producer
    'enable.idempotence': True,
}

producer = Producer(config)
producer.init_transactions()

try:
    producer.begin_transaction()

    # Produce multiple messages atomically
    producer.produce('orders', key='ord_1', value='...')
    producer.produce('inventory', key='inv_1', value='...')
    producer.produce('notifications', key='ntf_1', value='...')

    # All messages committed together or none
    producer.commit_transaction()

except Exception as e:
    producer.abort_transaction()
    raise
```

**Use case:** Consuming from one topic, processing, producing to another (exactly-once end-to-end).

## Partitioning Strategies

### Key-Based Partitioning (Default)

```python
# Messages with same key go to same partition
producer.produce(
    'orders',
    key='customer_456',  # All orders for this customer in same partition
    value=order_data
)
```

**Guarantees:** Order preserved per key.

### Custom Partitioner

```python
from confluent_kafka import Producer

def custom_partitioner(key, num_partitions):
    """Route VIP customers to partition 0"""
    if key.startswith('VIP_'):
        return 0
    else:
        # Default hash-based partitioning for others
        return hash(key) % num_partitions

config = {
    'bootstrap.servers': 'localhost:9092',
    'partitioner': custom_partitioner,
}

producer = Producer(config)
```

## Consumer Rebalancing

When consumers join/leave, Kafka **rebalances** partition assignments.

### Graceful Shutdown

```python
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    consumer.close()  # Triggers rebalance, releases partitions
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

consumer = Consumer(config)
consumer.subscribe(['orders'])

while True:
    msg = consumer.poll(1.0)
    # Process messages...
```

### Rebalance Listener

```python
from confluent_kafka import Consumer

def on_assign(consumer, partitions):
    """Called when partitions assigned"""
    print(f'Assigned partitions: {[p.partition for p in partitions]}')

def on_revoke(consumer, partitions):
    """Called before partitions revoked"""
    print(f'Revoking partitions: {[p.partition for p in partitions]}')
    consumer.commit()  # Commit offsets before losing partitions

consumer = Consumer(config)
consumer.subscribe(['orders'], on_assign=on_assign, on_revoke=on_revoke)
```

## Performance Tuning

### Producer Throughput Optimization

```python
config = {
    'bootstrap.servers': 'localhost:9092',
    'acks': '1',  # Wait for leader ACK only (faster than 'all')
    'compression.type': 'lz4',  # Fast compression
    'batch.size': 65536,  # 64KB batches (larger = more efficient)
    'linger.ms': 20,  # Wait 20ms for batching
    'buffer.memory': 67108864,  # 64MB send buffer
    'max.in.flight.requests.per.connection': 5,
}
```

**Trade-offs:**
- `acks=1` faster but weaker durability than `acks=all`
- Larger batches = higher throughput, higher latency
- `linger.ms` adds latency but increases batching efficiency

### Consumer Throughput Optimization

```python
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'high-throughput-consumer',
    'fetch.min.bytes': 1048576,  # 1MB min fetch (reduce round trips)
    'fetch.max.wait.ms': 500,  # Max 500ms wait for fetch.min.bytes
    'max.partition.fetch.bytes': 2097152,  # 2MB per partition
    'session.timeout.ms': 30000,  # 30s session timeout
    'heartbeat.interval.ms': 10000,  # 10s heartbeat
}
```

**Trade-offs:**
- Larger `fetch.min.bytes` = fewer network calls but higher latency
- Increase `max.partition.fetch.bytes` for high-throughput topics
- Tune `session.timeout.ms` based on processing time per message

## Monitoring

### Key Metrics

```python
from confluent_kafka import Consumer, TopicPartition

consumer = Consumer(config)
consumer.subscribe(['orders'])

# Get consumer lag (messages behind)
def get_consumer_lag():
    """Calculate lag for all assigned partitions"""
    assigned = consumer.assignment()
    lag = {}

    for partition in assigned:
        # Get current committed offset
        committed = consumer.committed([partition])[0].offset

        # Get high watermark (latest offset in partition)
        low, high = consumer.get_watermark_offsets(partition)

        lag[partition.partition] = high - committed

    return lag

# Print lag every 10 seconds
import time
while True:
    msg = consumer.poll(1.0)
    # Process message...

    if time.time() % 10 == 0:
        print(f'Consumer lag: {get_consumer_lag()}')
```

### Prometheus Metrics Exporter

```python
from prometheus_client import Counter, Histogram, Gauge

messages_consumed = Counter('kafka_messages_consumed_total', 'Total messages consumed', ['topic'])
processing_duration = Histogram('kafka_message_processing_seconds', 'Processing duration', ['topic'])
consumer_lag = Gauge('kafka_consumer_lag', 'Consumer lag', ['topic', 'partition'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue

    start_time = time.time()

    # Process message
    process_order(msg.value())

    # Record metrics
    messages_consumed.labels(topic=msg.topic()).inc()
    processing_duration.labels(topic=msg.topic()).observe(time.time() - start_time)

    consumer.commit(message=msg)
```

## Common Patterns

### Dead Letter Queue

```python
def process_with_dlq(msg):
    """Process message with DLQ fallback"""
    try:
        process_order(msg.value())
        consumer.commit(message=msg)
    except RecoverableError as e:
        # Retry by not committing (message will be redelivered)
        print(f'Recoverable error, will retry: {e}')
    except UnrecoverableError as e:
        # Send to DLQ
        dlq_producer.produce(
            'orders-dlq',
            key=msg.key(),
            value=msg.value(),
            headers={'error': str(e)}
        )
        consumer.commit(message=msg)  # Don't reprocess
```

### Event Sourcing

```python
# Write events to Kafka as source of truth
def create_order(order_data):
    """Event sourcing: Append event to log"""
    event = {
        'event_type': 'order.created.v1',
        'event_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'data': order_data
    }

    producer.produce(
        'order-events',
        key=order_data['order_id'],
        value=json.dumps(event).encode('utf-8')
    )
    producer.flush()

# Rebuild state by replaying events
def rebuild_order_state(order_id):
    """Replay all events for an order"""
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': f'rebuild-{uuid.uuid4()}',  # Unique group
        'auto.offset.reset': 'earliest',
    })

    consumer.subscribe(['order-events'])

    order_state = {}
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            break

        if msg.key().decode('utf-8') == order_id:
            event = json.loads(msg.value().decode('utf-8'))
            apply_event(order_state, event)

    return order_state
```

## Troubleshooting

### Consumer Not Receiving Messages

**Check:**
1. Topic exists: `kafka-topics --list --bootstrap-server localhost:9092`
2. Messages in topic: `kafka-console-consumer --topic orders --from-beginning`
3. Consumer group offset: `kafka-consumer-groups --describe --group order-processors`

### Consumer Lag Growing

**Causes:**
- Processing too slow (scale horizontally by adding consumers)
- Too few partitions (repartition topic)
- Network issues (check broker health)

**Fix:**
```python
# Scale by adding more consumers (up to partition count)
# If already at partition limit, repartition topic:
# kafka-topics --alter --topic orders --partitions 10
```

### Duplicate Messages

**Causes:**
- Consumer crashed before committing offset
- Rebalancing occurred mid-processing

**Fix:** Implement idempotency:
```python
def process_order_idempotent(order_id, data):
    """Idempotent processing with deduplication"""
    if redis.exists(f'processed:{order_id}'):
        return 'already_processed'

    result = process_order(data)
    redis.setex(f'processed:{order_id}', 86400, '1')  # 24h TTL
    return result
```

## Configuration Best Practices

### Production Producer Config

```python
config = {
    'bootstrap.servers': 'broker1:9092,broker2:9092,broker3:9092',
    'client.id': 'order-producer',
    'acks': 'all',  # Strongest durability
    'retries': 2147483647,  # Max retries
    'max.in.flight.requests.per.connection': 5,
    'enable.idempotence': True,  # Prevent duplicates
    'compression.type': 'lz4',
    'batch.size': 32768,
    'linger.ms': 10,
}
```

### Production Consumer Config

```python
config = {
    'bootstrap.servers': 'broker1:9092,broker2:9092,broker3:9092',
    'group.id': 'order-processors',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Manual commit
    'max.poll.interval.ms': 300000,  # 5 minutes
    'session.timeout.ms': 30000,  # 30 seconds
    'heartbeat.interval.ms': 10000,  # 10 seconds
    'isolation.level': 'read_committed',  # For transactional producers
}
```

## Related Patterns

- **CQRS**: Command topics write events, query topics build read models
- **Event Sourcing**: Kafka as immutable event log
- **Outbox Pattern**: Ensure database writes and event publishing are atomic
- **Saga Pattern**: Coordinate distributed transactions via events (see Temporal integration)
