# Streaming Data Ingestion


## Table of Contents

- [Apache Kafka](#apache-kafka)
  - [Python (confluent-kafka)](#python-confluent-kafka)
  - [TypeScript (kafkajs)](#typescript-kafkajs)
  - [Rust (rdkafka)](#rust-rdkafka)
- [AWS Kinesis](#aws-kinesis)
  - [Python (boto3)](#python-boto3)
- [Google Pub/Sub](#google-pubsub)
  - [Python](#python)
- [Exactly-Once Semantics](#exactly-once-semantics)
  - [Pattern: Idempotent Processing](#pattern-idempotent-processing)
  - [Pattern: Outbox for Reliability](#pattern-outbox-for-reliability)
- [Dead Letter Queues](#dead-letter-queues)
- [Backpressure Handling](#backpressure-handling)

## Apache Kafka

### Python (confluent-kafka)
```python
from confluent_kafka import Consumer, KafkaError
import json

def create_consumer(group_id: str, topics: list[str]) -> Consumer:
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False  # Manual commit for exactly-once
    }
    consumer = Consumer(conf)
    consumer.subscribe(topics)
    return consumer

def consume_messages(consumer: Consumer, batch_size: int = 100):
    """Consume messages with manual commit."""
    messages = []

    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise Exception(msg.error())

        messages.append(json.loads(msg.value().decode()))

        if len(messages) >= batch_size:
            yield messages
            consumer.commit()
            messages = []

# Usage
consumer = create_consumer("my-group", ["events"])
for batch in consume_messages(consumer):
    process_batch(batch)
```

### TypeScript (kafkajs)
```typescript
import { Kafka, Consumer, EachBatchPayload } from "kafkajs";

const kafka = new Kafka({
  clientId: "my-app",
  brokers: ["localhost:9092"]
});

const consumer = kafka.consumer({ groupId: "my-group" });

async function startConsumer() {
  await consumer.connect();
  await consumer.subscribe({ topic: "events", fromBeginning: true });

  await consumer.run({
    eachBatch: async ({ batch, resolveOffset, heartbeat }: EachBatchPayload) => {
      for (const message of batch.messages) {
        const event = JSON.parse(message.value!.toString());
        await processEvent(event);
        resolveOffset(message.offset);
        await heartbeat();
      }
    }
  });
}
```

### Rust (rdkafka)
```rust
use rdkafka::consumer::{Consumer, StreamConsumer};
use rdkafka::Message;

async fn consume_events(consumer: StreamConsumer) -> Result<()> {
    loop {
        match consumer.recv().await {
            Ok(msg) => {
                if let Some(payload) = msg.payload() {
                    let event: Event = serde_json::from_slice(payload)?;
                    process_event(event).await?;
                }
                consumer.commit_message(&msg, CommitMode::Async)?;
            }
            Err(e) => eprintln!("Kafka error: {}", e),
        }
    }
}
```

## AWS Kinesis

### Python (boto3)
```python
import boto3
import json

kinesis = boto3.client('kinesis')

def consume_kinesis(stream_name: str, shard_id: str):
    # Get shard iterator
    response = kinesis.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType='LATEST'
    )
    shard_iterator = response['ShardIterator']

    while True:
        response = kinesis.get_records(
            ShardIterator=shard_iterator,
            Limit=100
        )

        for record in response['Records']:
            data = json.loads(record['Data'])
            yield data

        shard_iterator = response['NextShardIterator']
```

## Google Pub/Sub

### Python
```python
from google.cloud import pubsub_v1
import json

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("project", "subscription")

def callback(message):
    data = json.loads(message.data.decode())
    process_message(data)
    message.ack()

streaming_pull = subscriber.subscribe(subscription_path, callback=callback)

# Run forever
streaming_pull.result()
```

## Exactly-Once Semantics

### Pattern: Idempotent Processing
```python
async def process_with_idempotency(event: dict):
    event_id = event["id"]

    # Check if already processed
    existing = await db.execute(
        "SELECT 1 FROM processed_events WHERE event_id = ?",
        (event_id,)
    )
    if existing:
        return  # Skip duplicate

    # Process in transaction
    async with db.transaction():
        await process_event(event)
        await db.execute(
            "INSERT INTO processed_events (event_id, processed_at) VALUES (?, ?)",
            (event_id, datetime.utcnow())
        )
```

### Pattern: Outbox for Reliability
```python
async def process_with_outbox(event: dict):
    async with db.transaction():
        # 1. Write to outbox
        await db.execute(
            "INSERT INTO outbox (event_id, payload, status) VALUES (?, ?, 'pending')",
            (event["id"], json.dumps(event))
        )

        # 2. Process event
        result = await process_event(event)

        # 3. Mark complete
        await db.execute(
            "UPDATE outbox SET status = 'complete' WHERE event_id = ?",
            (event["id"],)
        )

    return result
```

## Dead Letter Queues

```python
async def consume_with_dlq(consumer, dlq_producer):
    for msg in consumer:
        try:
            await process_message(msg)
            consumer.commit()
        except Exception as e:
            # Send to DLQ after max retries
            if msg.retry_count >= 3:
                await dlq_producer.send(
                    topic="events-dlq",
                    value={
                        "original": msg.value,
                        "error": str(e),
                        "failed_at": datetime.utcnow().isoformat()
                    }
                )
                consumer.commit()
            else:
                # Re-queue for retry
                raise
```

## Backpressure Handling

```python
import asyncio
from asyncio import Semaphore

class BackpressureConsumer:
    def __init__(self, max_concurrent: int = 100):
        self.semaphore = Semaphore(max_concurrent)

    async def process_with_backpressure(self, message):
        async with self.semaphore:
            await process_message(message)

    async def consume(self, consumer):
        tasks = []
        async for msg in consumer:
            task = asyncio.create_task(self.process_with_backpressure(msg))
            tasks.append(task)

            # Periodically clean completed tasks
            if len(tasks) > 1000:
                tasks = [t for t in tasks if not t.done()]
```
