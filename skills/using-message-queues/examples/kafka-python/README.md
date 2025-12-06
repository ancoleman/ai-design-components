# Kafka Python Producer/Consumer Example

Production-ready Kafka producer and consumer implementations using confluent-kafka-python.

## Prerequisites

```bash
# Install confluent-kafka
pip install confluent-kafka

# Start Kafka (Docker)
docker run -d \
  --name kafka \
  -p 9092:9092 \
  apache/kafka:latest
```

## Files

- `producer.py` - Producer examples (simple, batching, partitioning, error handling)
- `consumer.py` - Consumer examples (manual commit, batching, multiple topics)

## Running Examples

### Producer

```bash
python producer.py
```

**Output:**
```
🚀 Kafka Producer Examples
==================================================

=== Example 1: Simple Message ===
✅ Message delivered to orders [0] @ offset 42

=== Example 2: Message with Headers ===
✅ Message delivered to payments [1] @ offset 15

=== Example 3: Batch Production ===
Produced 100 messages in 0.23 seconds (435 msg/s)
```

### Consumer

```bash
python consumer.py
```

**Output:**
```
🚀 Kafka Consumer Examples
==================================================

=== Example 1: Manual Commit ===
📦 Processing order: ord_123
✅ Committed offset 42
📦 Processing order: ord_456
✅ Committed offset 43
```

## Key Features

### Producer
- ✅ Idempotent producer (prevents duplicates)
- ✅ Batching for efficiency
- ✅ Custom partitioning
- ✅ Headers for metadata
- ✅ Error handling with retries

### Consumer
- ✅ Manual offset commits (exactly-once)
- ✅ Batch processing
- ✅ Error handling (recoverable vs unrecoverable)
- ✅ Dead letter queue pattern
- ✅ Multiple topic subscriptions

## Configuration

### Producer Config

```python
config = {
    'bootstrap.servers': 'localhost:9092',
    'acks': 'all',  # Wait for all replicas
    'enable.idempotence': True,  # Prevent duplicates
    'compression.type': 'lz4',  # Fast compression
}
```

### Consumer Config

```python
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python-consumer-group',
    'enable.auto.commit': False,  # Manual commit
    'auto.offset.reset': 'earliest',
}
```

## Topics Used

- `orders` - Order events
- `payments` - Payment events
- `logs` - Log messages
- `inventory` - Inventory updates
- `alerts` - Critical alerts

## Monitoring

### Check Topics

```bash
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Consumer Group Lag

```bash
docker exec kafka kafka-consumer-groups \
  --describe \
  --group python-consumer-group \
  --bootstrap-server localhost:9092
```

## References

- Confluent Kafka Python: `/confluentinc/confluent-kafka-python`
- Trust Score: 68.8/100
- Code Snippets: 192+
