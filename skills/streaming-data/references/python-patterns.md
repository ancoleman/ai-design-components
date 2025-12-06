# Python Streaming Patterns (confluent-kafka-python)

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Basic Producer](#basic-producer)
- [Basic Consumer](#basic-consumer)
- [Batch Processing](#batch-processing)
- [AsyncIO Support](#asyncio-support)
- [Schema Registry Integration](#schema-registry-integration)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)

## Overview

confluent-kafka-python is the recommended Python client for Apache Kafka. It wraps librdkafka (C library) for high performance while providing a Pythonic API.

**Library**: confluent-kafka-python
**Trust Score**: High (68.8)
**Code Snippets**: 192+
**Best For**: Data pipelines, ML feature engineering, analytics

## Installation

```bash
pip install confluent-kafka
# For Avro support
pip install confluent-kafka[avro]
```

## Basic Producer

```python
from confluent_kafka import Producer
import json
import time

class EventProducer:
    def __init__(self, bootstrap_servers: str):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'my-app-producer',
            # At-least-once guarantees
            'acks': 'all',
            'retries': 3,
            'enable.idempotence': True,
            # Performance tuning
            'compression.type': 'lz4',
            'batch.size': 32768,
            'linger.ms': 10,
        }
        self.producer = Producer(self.config)

    def delivery_callback(self, err, msg):
        """Callback for delivery reports."""
        if err:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

    def send_event(self, topic: str, event: dict, key: str = None):
        """Send a single event."""
        try:
            self.producer.produce(
                topic=topic,
                key=key.encode('utf-8') if key else None,
                value=json.dumps(event).encode('utf-8'),
                callback=self.delivery_callback,
                headers={
                    'event-type': event.get('type', ''),
                    'timestamp': str(int(time.time())),
                }
            )
            # Trigger callbacks (non-blocking)
            self.producer.poll(0)
        except BufferError:
            print('Local producer queue is full')
            self.producer.poll(1)  # Block until space available
            self.send_event(topic, event, key)  # Retry

    def flush(self):
        """Wait for all messages to be delivered."""
        remaining = self.producer.flush(timeout=30)
        if remaining > 0:
            print(f'Warning: {remaining} messages not delivered')

    def close(self):
        """Close the producer."""
        self.flush()

# Usage
producer = EventProducer('localhost:9092')
producer.send_event('user-actions', {
    'user_id': 'user-123',
    'action': 'login',
    'timestamp': int(time.time())
}, key='user-123')
producer.close()
```

## Basic Consumer

```python
from confluent_kafka import Consumer, KafkaException
import json

class EventConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            # Manual commit for error handling
            'enable.auto.commit': False,
            # Performance
            'fetch.min.bytes': 1024,
            'fetch.wait.max.ms': 500,
        }
        self.consumer = Consumer(self.config)

    def subscribe(self, topics: list):
        """Subscribe to topics."""
        self.consumer.subscribe(topics)

    def consume(self, handler, batch_size: int = 1):
        """Start consuming messages."""
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    raise KafkaException(msg.error())

                try:
                    # Decode message
                    value = json.loads(msg.value().decode('utf-8'))

                    # Process message
                    handler(value)

                    # Commit offset after successful processing
                    self.consumer.commit(message=msg)

                except json.JSONDecodeError as e:
                    print(f'Failed to decode message: {e}')
                    # Send to DLQ
                    self._send_to_dlq(msg)
                    self.consumer.commit(message=msg)

                except Exception as e:
                    print(f'Error processing message: {e}')
                    # Don't commit - message will be reprocessed

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()

    def _send_to_dlq(self, msg):
        """Send failed message to dead-letter queue."""
        # Implementation depends on your DLQ strategy
        pass

    def close(self):
        """Close the consumer."""
        self.consumer.close()

# Usage
consumer = EventConsumer('localhost:9092', 'my-consumer-group')
consumer.subscribe(['user-actions'])

def handle_event(event: dict):
    print(f'Processing event: {event}')
    # Your business logic here

consumer.consume(handle_event)
```

## Batch Processing

```python
from confluent_kafka import Consumer
from typing import List, Callable

class BatchConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'enable.auto.commit': False,
        }
        self.consumer = Consumer(self.config)

    def subscribe(self, topics: list):
        self.consumer.subscribe(topics)

    def consume_batch(self, handler: Callable[[List[dict]], None],
                      batch_size: int = 100, timeout: float = 5.0):
        """Consume messages in batches."""
        batch = []
        last_msg = None

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    # Timeout - process partial batch if exists
                    if batch:
                        handler(batch)
                        if last_msg:
                            self.consumer.commit(message=last_msg)
                        batch = []
                    continue

                if msg.error():
                    continue

                try:
                    value = json.loads(msg.value().decode('utf-8'))
                    batch.append(value)
                    last_msg = msg

                    # Process when batch is full
                    if len(batch) >= batch_size:
                        handler(batch)
                        self.consumer.commit(message=last_msg)
                        batch = []

                except Exception as e:
                    print(f'Error: {e}')

        finally:
            self.consumer.close()

# Usage
consumer = BatchConsumer('localhost:9092', 'batch-group')
consumer.subscribe(['events'])

def process_batch(events: List[dict]):
    print(f'Processing batch of {len(events)} events')
    # Batch insert to database, etc.

consumer.consume_batch(process_batch, batch_size=100)
```

## AsyncIO Support

```python
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json

async def async_produce():
    """Async producer example."""
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await producer.start()
    try:
        for i in range(100):
            await producer.send_and_wait('my-topic', {'count': i})
    finally:
        await producer.stop()

async def async_consume():
    """Async consumer example."""
    consumer = AIOKafkaConsumer(
        'my-topic',
        bootstrap_servers='localhost:9092',
        group_id='async-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Received: {msg.value}')
            # Process asynchronously
            await process_async(msg.value)
    finally:
        await consumer.stop()

async def process_async(data: dict):
    """Async processing logic."""
    await asyncio.sleep(0.1)  # Simulate async I/O
    print(f'Processed: {data}')

# Run
asyncio.run(async_consume())
```

## Schema Registry Integration

```python
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

# Schema definition
user_schema_str = """
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}
"""

class AvroProducer:
    def __init__(self, bootstrap_servers: str, schema_registry_url: str):
        schema_registry_client = SchemaRegistryClient({'url': schema_registry_url})

        avro_serializer = AvroSerializer(
            schema_registry_client,
            user_schema_str
        )

        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
        })

        self.avro_serializer = avro_serializer

    def send_user(self, topic: str, user: dict):
        """Send user with Avro serialization."""
        self.producer.produce(
            topic=topic,
            value=self.avro_serializer(
                user,
                SerializationContext(topic, MessageField.VALUE)
            ),
            on_delivery=lambda err, msg: print(f'Delivered: {err or msg}')
        )
        self.producer.poll(0)

    def flush(self):
        self.producer.flush()

# Usage
producer = AvroProducer('localhost:9092', 'http://localhost:8081')
producer.send_user('users', {
    'id': 'user-123',
    'name': 'Alice',
    'email': 'alice@example.com'
})
producer.flush()
```

## Best Practices

### 1. Use Callback for Async Produce

```python
def delivery_report(err, msg):
    if err:
        logging.error(f'Delivery failed: {err}')
    else:
        logging.info(f'Delivered to {msg.topic()} [{msg.partition()}]')

producer.produce(topic, value, callback=delivery_report)
producer.poll(0)  # Trigger callbacks
```

### 2. Manual Offset Management

```python
# Disable auto-commit
consumer = Consumer({'enable.auto.commit': False, ...})

# Commit after successful processing
msg = consumer.poll()
process(msg)
consumer.commit(message=msg)
```

### 3. Graceful Shutdown

```python
import signal

running = True

def signal_handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)

while running:
    msg = consumer.poll(timeout=1.0)
    if msg:
        process(msg)

consumer.close()
```

### 4. Error Handling

```python
from confluent_kafka import KafkaError

msg = consumer.poll()
if msg.error():
    if msg.error().code() == KafkaError._PARTITION_EOF:
        print('End of partition')
    else:
        raise KafkaException(msg.error())
```

## Conclusion

confluent-kafka-python provides high-performance Kafka integration for Python applications. Use it for data pipelines, ML feature engineering, and analytics workloads.
