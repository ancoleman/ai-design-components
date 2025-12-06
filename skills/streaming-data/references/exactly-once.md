# Exactly-Once Processing

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Idempotent Producer](#idempotent-producer)
- [Transactions](#transactions)
- [TypeScript Transactions (KafkaJS)](#typescript-transactions-kafkajs)
- [Performance Considerations](#performance-considerations)
- [When to Use](#when-to-use)
- [Alternatives to Transactions](#alternatives-to-transactions)
- [Monitoring](#monitoring)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)

## Overview

Exactly-once semantics guarantee that messages are processed exactly once - neither lost nor duplicated. Critical for financial transactions and stateful processing.

## Requirements

1. **Idempotent producers**: Prevent duplicate writes from retries
2. **Transactions**: Atomic writes to multiple topics
3. **Transactional reads**: Consumers read only committed data
4. **Offset commits in transactions**: Atomic processing + commit

## Idempotent Producer

### Configuration

```properties
enable.idempotence=true
acks=all
retries=Integer.MAX_VALUE
max.in.flight.requests.per.connection=5
```

### How It Works

Producer assigns sequence numbers to messages. Broker detects and deduplicates based on producer ID + sequence number.

### TypeScript

```typescript
const producer = kafka.producer({
  idempotent: true,
  maxInFlightRequests: 5,
});
```

## Transactions

### Producer-Only Transactions

Write to multiple topics atomically:

```java
Properties props = new Properties();
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "my-tx-id");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();

try {
    producer.beginTransaction();

    // Send to multiple topics
    producer.send(new ProducerRecord<>("topic1", "key", "value1"));
    producer.send(new ProducerRecord<>("topic2", "key", "value2"));

    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
    throw e;
}
```

### Consumer-Producer Transactions

Process message and produce output atomically:

```java
Properties consumerProps = new Properties();
consumerProps.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
consumerProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

Properties producerProps = new Properties();
producerProps.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "consumer-producer-tx");
producerProps.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps);
KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps);

producer.initTransactions();
consumer.subscribe(Arrays.asList("input-topic"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

    if (!records.isEmpty()) {
        producer.beginTransaction();

        try {
            // Process records
            for (ConsumerRecord<String, String> record : records) {
                String result = processMessage(record.value());

                // Send output
                producer.send(new ProducerRecord<>("output-topic", result));
            }

            // Commit consumer offsets in transaction
            Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();
            for (ConsumerRecord<String, String> record : records) {
                offsets.put(
                    new TopicPartition(record.topic(), record.partition()),
                    new OffsetAndMetadata(record.offset() + 1)
                );
            }

            producer.sendOffsetsToTransaction(offsets, consumer.groupMetadata());

            // Commit transaction
            producer.commitTransaction();

        } catch (Exception e) {
            producer.abortTransaction();
        }
    }
}
```

## TypeScript Transactions (KafkaJS)

```typescript
import { Kafka, Producer, Consumer } from 'kafkajs';

class ExactlyOnceProcessor {
  private producer: Producer;
  private consumer: Consumer;

  constructor(kafka: Kafka, transactionalId: string) {
    this.producer = kafka.producer({
      idempotent: true,
      maxInFlightRequests: 1,
      transactionalId,
    });

    this.consumer = kafka.consumer({
      groupId: 'my-group',
      readUncommitted: false, // Read only committed messages
    });
  }

  async process(): Promise<void> {
    await this.producer.connect();
    await this.consumer.connect();
    await this.consumer.subscribe({ topics: ['input'] });

    await this.consumer.run({
      autoCommit: false,
      eachMessage: async ({ topic, partition, message }) => {
        const transaction = await this.producer.transaction();

        try {
          const value = message.value?.toString();
          const result = await this.processMessage(value);

          // Send output in transaction
          await transaction.send({
            topic: 'output',
            messages: [{ value: result }],
          });

          // Commit consumer offset in same transaction
          await transaction.sendOffsets({
            consumerGroupId: this.consumer.groupId,
            topics: [{
              topic,
              partitions: [{
                partition,
                offset: (parseInt(message.offset) + 1).toString(),
              }],
            }],
          });

          await transaction.commit();

        } catch (error) {
          await transaction.abort();
          throw error;
        }
      },
    });
  }

  private async processMessage(input: string): Promise<string> {
    // Business logic
    return input.toUpperCase();
  }
}
```

## Performance Considerations

### Overhead

Exactly-once semantics add overhead:
- Latency: +20-50% vs at-least-once
- Throughput: -10-30% vs at-least-once
- Resource usage: Higher memory, CPU

### Tuning

```properties
# Reduce latency
transaction.timeout.ms=60000
transaction.state.log.min.isr=1

# Increase throughput
transaction.state.log.replication.factor=3
```

## When to Use

**Use exactly-once when**:
- Financial transactions
- Payment processing
- Inventory management
- Compliance requirements
- Stateful aggregations

**Avoid exactly-once when**:
- Metrics, logs (loss acceptable)
- High-volume, low-value events
- Performance is critical
- Idempotent consumers sufficient

## Alternatives to Transactions

### 1. Idempotent Processing

Design consumers to handle duplicates:

```python
processed_ids = set()

def process_idempotent(message):
    message_id = message.headers['message-id']

    if message_id in processed_ids:
        print('Duplicate, skipping')
        return

    process_message(message)
    processed_ids.add(message_id)
```

### 2. Database Constraints

Use unique constraints:

```sql
INSERT INTO orders (order_id, ...)
VALUES (?, ...)
ON DUPLICATE KEY UPDATE order_id = order_id;
```

### 3. External Transaction Coordinator

Use distributed transaction frameworks:
- Apache Flink state backend
- Apache Spark checkpointing
- Custom coordination service

## Monitoring

```python
from prometheus_client import Counter, Histogram

tx_commits = Counter('kafka_tx_commits_total', 'Transactions committed')
tx_aborts = Counter('kafka_tx_aborts_total', 'Transactions aborted')
tx_duration = Histogram('kafka_tx_duration_seconds', 'Transaction duration')

def process_with_tx():
    start = time.time()

    try:
        transaction.begin()
        # Processing logic
        transaction.commit()
        tx_commits.inc()
    except Exception:
        transaction.abort()
        tx_aborts.inc()
        raise
    finally:
        tx_duration.observe(time.time() - start)
```

## Best Practices

1. **Use unique transactional IDs**: One per producer instance
2. **Set appropriate timeouts**: Balance reliability vs performance
3. **Monitor abort rate**: High aborts indicate issues
4. **Test failure scenarios**: Crashes, network partitions
5. **Consider alternatives**: Idempotent processing often sufficient

## Conclusion

Exactly-once semantics provide strong guarantees but add complexity and overhead. Use for critical use cases like financial transactions. For most applications, at-least-once with idempotent processing is sufficient.
