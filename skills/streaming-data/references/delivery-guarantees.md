# Delivery Guarantees in Stream Processing

## Table of Contents
- [Overview](#overview)
- [At-Most-Once Delivery](#at-most-once-delivery)
- [At-Least-Once Delivery](#at-least-once-delivery)
- [Exactly-Once Delivery](#exactly-once-delivery)
- [Comparison Matrix](#comparison-matrix)
- [Configuration Summary](#configuration-summary)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)

## Overview

Stream processing systems offer three delivery semantics: at-most-once, at-least-once, and exactly-once. Choose based on use case requirements and acceptable trade-offs.

## At-Most-Once Delivery

### Characteristics
- Messages may be lost
- No duplicates
- Lowest overhead and complexity
- Best performance

### Implementation
- Consumer commits offset before processing message
- Producer sends without acknowledgement (acks=0)

### Use Cases
- Metrics and monitoring (loss acceptable)
- Log aggregation (sampling OK)
- Best-effort notifications

### Example (Python)
```python
# Consumer commits before processing
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'enable.auto.commit': True,  # Auto-commit before processing
    'auto.commit.interval.ms': 1000,
})

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue

    # Message may be lost if processing fails
    try:
        process_message(msg.value())
    except Exception as e:
        # Offset already committed - message lost
        logging.error(f"Message lost: {e}")
```

## At-Least-Once Delivery

### Characteristics
- Messages never lost (guaranteed delivery)
- May have duplicates (redelivery on failure)
- Moderate overhead
- **Most common choice** for production systems

### Implementation
- Consumer commits offset after processing message
- Producer waits for acknowledgement (acks=all)
- Idempotent message processing required

### Use Cases
- Most production applications
- Order processing (with idempotency)
- Database synchronization
- Event-driven architectures

### Example (TypeScript)
```typescript
// Producer: acks=all
const producer = kafka.producer({
  idempotent: true,  // Prevents duplicates from retries
});

await producer.send({
  topic: 'orders',
  acks: -1,  // Wait for all replicas
  messages: [{ value: JSON.stringify(order) }],
});

// Consumer: manual commit after processing
await consumer.run({
  autoCommit: false,
  eachMessage: async ({ topic, partition, message }) => {
    try {
      // Process message idempotently
      await processMessageIdempotently(message);

      // Commit offset only after successful processing
      await consumer.commitOffsets([{
        topic,
        partition,
        offset: (parseInt(message.offset) + 1).toString(),
      }]);
    } catch (error) {
      // Don't commit - message will be reprocessed
      console.error('Processing failed, will retry:', error);
    }
  },
});
```

### Idempotency Strategies

**1. Deduplication by Message ID**
```typescript
const processedIds = new Set<string>();

async function processMessageIdempotently(message: any) {
  const messageId = message.headers['message-id'];

  if (processedIds.has(messageId)) {
    console.log('Duplicate message, skipping');
    return;
  }

  await processMessage(message);
  processedIds.add(messageId);
}
```

**2. Database Unique Constraints**
```sql
CREATE TABLE orders (
  order_id VARCHAR(36) PRIMARY KEY,
  -- other fields
);

-- Insert will fail silently if duplicate
INSERT INTO orders (order_id, ...)
VALUES (?, ...)
ON DUPLICATE KEY UPDATE order_id = order_id;
```

**3. Check-then-Set Pattern**
```typescript
async function processOrderIdempotently(order: Order) {
  const existing = await db.orders.findOne({ orderId: order.id });

  if (existing) {
    console.log('Order already processed');
    return;
  }

  await db.orders.insert(order);
}
```

## Exactly-Once Delivery

### Characteristics
- Messages never lost and never duplicated
- Highest overhead and complexity
- Requires transactional support
- End-to-end exactly-once (source to sink)

### Implementation
- Producer uses transactions
- Consumer processes and commits offset in same transaction
- Idempotent producers (enable.idempotence=true)

### Use Cases
- Financial transactions
- Payment processing
- Critical state updates
- Compliance-sensitive data

### Example (Java)
```java
// Producer with transactions
Properties props = new Properties();
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "my-transactional-id");
props.put(ProducerConfig.ACKS_CONFIG, "all");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);

// Initialize transactions
producer.initTransactions();

try {
    producer.beginTransaction();

    // Send messages
    producer.send(new ProducerRecord<>("topic1", "key", "value"));
    producer.send(new ProducerRecord<>("topic2", "key", "value"));

    // Commit transaction
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
    throw e;
}
```

### Exactly-Once with Consumer + Producer

```java
// Consumer with exactly-once processing
Properties consumerProps = new Properties();
consumerProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
consumerProps.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps);

Properties producerProps = new Properties();
producerProps.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "consumer-producer-tx");
producerProps.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps);
producer.initTransactions();

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

    if (!records.isEmpty()) {
        producer.beginTransaction();

        try {
            for (ConsumerRecord<String, String> record : records) {
                // Process message
                String result = processMessage(record.value());

                // Send output
                producer.send(new ProducerRecord<>("output", result));
            }

            // Commit consumer offsets in same transaction
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

## Comparison Matrix

| Guarantee | Message Loss | Duplicates | Overhead | Use Case |
|-----------|--------------|------------|----------|----------|
| **At-Most-Once** | Possible | No | Low | Metrics, logs |
| **At-Least-Once** | No | Possible | Medium | Most applications |
| **Exactly-Once** | No | No | High | Financial, critical |

## Configuration Summary

### At-Most-Once Configuration

**Producer**:
```properties
acks=0                          # No acknowledgement
enable.idempotence=false
```

**Consumer**:
```properties
enable.auto.commit=true         # Commit before processing
auto.commit.interval.ms=1000
```

### At-Least-Once Configuration

**Producer**:
```properties
acks=all                        # Wait for all replicas
retries=Integer.MAX_VALUE
enable.idempotence=true         # Prevent duplicates from retries
max.in.flight.requests.per.connection=5
```

**Consumer**:
```properties
enable.auto.commit=false        # Manual commit after processing
```

### Exactly-Once Configuration

**Producer**:
```properties
enable.idempotence=true
transactional.id=unique-tx-id
acks=all
max.in.flight.requests.per.connection=5
```

**Consumer**:
```properties
enable.auto.commit=false
isolation.level=read_committed  # Read only committed transactions
```

## Best Practices

### 1. Start with At-Least-Once

Most applications should use at-least-once delivery with idempotent processing. It provides good reliability without the complexity of exactly-once.

### 2. Design for Idempotency

Even with at-least-once, design message processing to be idempotent:
- Use unique message IDs
- Leverage database constraints
- Implement check-then-set patterns

### 3. Use Exactly-Once Sparingly

Only use exactly-once when absolutely required (financial transactions, compliance). The added complexity and overhead are significant.

### 4. Monitor Delivery Metrics

Track metrics for:
- Message loss (at-most-once)
- Duplicate processing rate (at-least-once)
- Transaction abort rate (exactly-once)

### 5. Test Failure Scenarios

Test behavior under:
- Network partitions
- Consumer crashes
- Broker failures
- Slow processing

## Conclusion

**Default recommendation**: Use at-least-once delivery with idempotent message processing for most applications. Reserve exactly-once for critical use cases where duplicates are unacceptable.
