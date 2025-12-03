# Redis Streams - Simple Message Queues

Redis Streams provide lightweight message queue functionality with consumer groups. Best when already using Redis for caching.

## When to Use Redis Streams

**Best for:**
- Simple job queues (already using Redis)
- Notification queues
- Activity feeds
- Moderate throughput (100K+ msg/s)
- Minimal infrastructure (no separate broker)

**Not ideal for:**
- High-throughput event streaming (use Kafka)
- Complex routing (use RabbitMQ)
- Workflow orchestration (use Temporal)

## Core Concepts

### Streams

**Stream:** Append-only log of messages
- Each message has unique ID (timestamp-sequence)
- Supports range queries
- Automatic trimming by count or time

### Consumer Groups

**Consumer group:** Coordinates message consumption across consumers
- Each message delivered to one consumer
- Acknowledgments track processed messages
- Pending entries list (PEL) tracks unacked messages

## Python Implementation

### Basic Producer/Consumer

```python
import redis
import json
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Producer: Add message to stream
message = {
    'order_id': 'ord_123',
    'customer_id': 'cus_456',
    'total': 99.99
}

message_id = r.xadd(
    'orders',  # Stream name
    message,  # Message data (dict)
    maxlen=10000  # Keep last 10K messages
)

print(f"Message ID: {message_id}")

# Consumer: Read from stream
last_id = '0'  # Start from beginning
while True:
    messages = r.xread(
        {'orders': last_id},
        count=10,  # Batch size
        block=5000  # Block for 5 seconds
    )

    for stream_name, stream_messages in messages:
        for message_id, message_data in stream_messages:
            print(f"Processing: {message_data}")
            process_order(message_data)
            last_id = message_id  # Update position
```

### Consumer Group Pattern

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Create consumer group (once)
try:
    r.xgroup_create(
        'orders',  # Stream name
        'order-processors',  # Group name
        id='0',  # Start from beginning
        mkstream=True  # Create stream if not exists
    )
except redis.exceptions.ResponseError:
    pass  # Group already exists

# Consumer: Read from group
consumer_name = 'worker-1'

while True:
    # Read new messages
    messages = r.xreadgroup(
        'order-processors',  # Group name
        consumer_name,  # Consumer name
        {'orders': '>'},  # '>' means new messages
        count=10,  # Batch size
        block=5000  # Block for 5 seconds
    )

    for stream_name, stream_messages in messages:
        for message_id, message_data in stream_messages:
            try:
                process_order(message_data)

                # Acknowledge message
                r.xack('orders', 'order-processors', message_id)

            except Exception as e:
                print(f"Error processing {message_id}: {e}")
                # Message stays in pending entries list
```

## Advanced Patterns

### Claiming Stale Messages

```python
# Claim messages pending for > 60 seconds
stale_messages = r.xautoclaim(
    'orders',
    'order-processors',
    consumer_name,
    min_idle_time=60000,  # 60 seconds in milliseconds
    start='0-0',
    count=10
)

for message_id, message_data in stale_messages[1]:
    print(f"Reclaiming stale message: {message_id}")
    try:
        process_order(message_data)
        r.xack('orders', 'order-processors', message_id)
    except Exception as e:
        print(f"Failed again: {e}")
```

### Dead Letter Queue Pattern

```python
def process_with_dlq(stream, group, consumer, message_id, message_data):
    """Process with retry tracking and DLQ"""
    try:
        # Check retry count
        retry_count = int(message_data.get('retry_count', 0))

        if retry_count >= 3:
            # Max retries reached, move to DLQ
            r.xadd('orders_dlq', {
                **message_data,
                'failed_at': time.time(),
                'reason': 'max_retries_exceeded'
            })
            r.xack(stream, group, message_id)
            return

        # Process message
        process_order(message_data)
        r.xack(stream, group, message_id)

    except RecoverableError as e:
        # Increment retry count and requeue
        r.xadd(stream, {
            **message_data,
            'retry_count': retry_count + 1
        })
        r.xack(stream, group, message_id)  # Ack original

    except UnrecoverableError as e:
        # Move to DLQ immediately
        r.xadd('orders_dlq', {
            **message_data,
            'failed_at': time.time(),
            'reason': str(e)
        })
        r.xack(stream, group, message_id)
```

### Priority Queue Simulation

```python
# Use multiple streams for priorities
HIGH_PRIORITY = 'tasks:high'
NORMAL_PRIORITY = 'tasks:normal'
LOW_PRIORITY = 'tasks:low'

# Consumer reads in priority order
while True:
    # Try high priority first
    messages = r.xreadgroup(
        'task-processors',
        consumer_name,
        {HIGH_PRIORITY: '>'},
        count=10,
        block=100  # Short timeout
    )

    if messages:
        process_messages(messages)
        continue

    # Then normal priority
    messages = r.xreadgroup(
        'task-processors',
        consumer_name,
        {NORMAL_PRIORITY: '>'},
        count=10,
        block=100
    )

    if messages:
        process_messages(messages)
        continue

    # Finally low priority
    messages = r.xreadgroup(
        'task-processors',
        consumer_name,
        {LOW_PRIORITY: '>'},
        count=10,
        block=5000
    )

    if messages:
        process_messages(messages)
```

## Monitoring

### Stream Info

```python
# Get stream length
length = r.xlen('orders')
print(f"Stream length: {length}")

# Get stream info
info = r.xinfo_stream('orders')
print(f"Length: {info['length']}")
print(f"First ID: {info['first-entry'][0]}")
print(f"Last ID: {info['last-entry'][0]}")
print(f"Consumer groups: {info['groups']}")
```

### Consumer Group Info

```python
# Get consumer group info
groups = r.xinfo_groups('orders')
for group in groups:
    print(f"Group: {group['name']}")
    print(f"Consumers: {group['consumers']}")
    print(f"Pending: {group['pending']}")
    print(f"Last delivered: {group['last-delivered-id']}")

# Get consumer info
consumers = r.xinfo_consumers('orders', 'order-processors')
for consumer in consumers:
    print(f"Consumer: {consumer['name']}")
    print(f"Pending: {consumer['pending']}")
    print(f"Idle: {consumer['idle']} ms")
```

### Pending Messages

```python
# Get pending messages for consumer
pending = r.xpending_range(
    'orders',
    'order-processors',
    min='-',
    max='+',
    count=100,
    consumername=consumer_name
)

for msg in pending:
    message_id = msg['message_id']
    consumer = msg['consumer']
    time_since_delivery = msg['time_since_delivered']
    delivery_count = msg['times_delivered']

    print(f"Pending: {message_id}, {time_since_delivery}ms, {delivery_count} deliveries")
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Gauge, Histogram
import time

messages_processed = Counter('redis_streams_processed', 'Total', ['stream'])
processing_duration = Histogram('redis_streams_duration_seconds', 'Duration', ['stream'])
stream_length = Gauge('redis_streams_length', 'Length', ['stream'])
pending_messages = Gauge('redis_streams_pending', 'Pending', ['stream', 'group', 'consumer'])

def monitored_consumer():
    while True:
        start_time = time.time()

        messages = r.xreadgroup(
            'order-processors',
            consumer_name,
            {'orders': '>'},
            count=10,
            block=5000
        )

        for stream_name, stream_messages in messages:
            for message_id, message_data in stream_messages:
                process_order(message_data)
                r.xack('orders', 'order-processors', message_id)

                # Metrics
                messages_processed.labels(stream='orders').inc()
                processing_duration.labels(stream='orders').observe(
                    time.time() - start_time
                )

        # Update stream length
        stream_length.labels(stream='orders').set(r.xlen('orders'))

        # Update pending count
        pending = r.xpending('orders', 'order-processors')
        pending_messages.labels(
            stream='orders',
            group='order-processors',
            consumer=consumer_name
        ).set(pending['pending'])
```

## Stream Trimming

### Approximate Trimming (Efficient)

```python
# Keep approximately last 10K messages
r.xadd(
    'orders',
    message,
    maxlen=10000,  # Approximate (more efficient)
)

# Or trim explicitly
r.xtrim('orders', maxlen=10000, approximate=True)
```

### Exact Trimming (Slower)

```python
# Keep exactly last 10K messages
r.xadd(
    'orders',
    message,
    maxlen=10000,
    approximate=False
)
```

### Time-Based Trimming

```python
# Keep messages from last 7 days
import time

seven_days_ago = int((time.time() - 7 * 24 * 3600) * 1000)
min_id = f"{seven_days_ago}-0"

r.xtrim('orders', minid=min_id, approximate=True)
```

## Configuration Best Practices

### Producer Config

```python
import redis
from redis.connection import ConnectionPool

# Connection pool for better performance
pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=10,
    decode_responses=True
)

r = redis.Redis(connection_pool=pool)

# Publish with trimming
def publish_message(stream, message, maxlen=10000):
    """Publish with automatic trimming"""
    message_id = r.xadd(
        stream,
        message,
        maxlen=maxlen,
        approximate=True
    )
    return message_id
```

### Consumer Config

```python
# Consumer with error handling
def consume_messages(stream, group, consumer, batch_size=10, block_ms=5000):
    """Robust consumer implementation"""
    try:
        messages = r.xreadgroup(
            group,
            consumer,
            {stream: '>'},
            count=batch_size,
            block=block_ms
        )

        for stream_name, stream_messages in messages:
            for message_id, message_data in stream_messages:
                try:
                    process_message(message_data)
                    r.xack(stream, group, message_id)
                except Exception as e:
                    # Log error, message stays in PEL
                    print(f"Error: {e}")

    except redis.exceptions.ConnectionError:
        # Handle connection errors
        print("Connection error, reconnecting...")
        time.sleep(1)
```

## TypeScript/Node.js Implementation

```typescript
import Redis from 'ioredis'

const redis = new Redis({
  host: 'localhost',
  port: 6379,
})

// Producer
async function publishMessage(stream: string, message: object) {
  const messageId = await redis.xadd(
    stream,
    'MAXLEN',
    '~', // Approximate trimming
    '10000',
    '*', // Auto-generate ID
    ...Object.entries(message).flat()
  )
  return messageId
}

// Consumer with consumer group
async function consumeMessages(
  stream: string,
  group: string,
  consumer: string
) {
  while (true) {
    const messages = await redis.xreadgroup(
      'GROUP',
      group,
      consumer,
      'COUNT',
      '10',
      'BLOCK',
      '5000',
      'STREAMS',
      stream,
      '>'
    )

    if (messages) {
      for (const [streamName, streamMessages] of messages) {
        for (const [messageId, messageFields] of streamMessages) {
          try {
            // Convert array to object
            const message = {}
            for (let i = 0; i < messageFields.length; i += 2) {
              message[messageFields[i]] = messageFields[i + 1]
            }

            await processMessage(message)
            await redis.xack(stream, group, messageId)
          } catch (err) {
            console.error(`Error processing ${messageId}:`, err)
          }
        }
      }
    }
  }
}

// Create consumer group
try {
  await redis.xgroup('CREATE', 'orders', 'processors', '0', 'MKSTREAM')
} catch (err) {
  // Group already exists
}

await consumeMessages('orders', 'processors', 'worker-1')
```

## Troubleshooting

### Messages Not Being Consumed

**Check:**
1. Consumer group exists?
2. Consumer name unique per worker?
3. Using '>' for new messages?
4. Stream has messages?

```python
# Debug info
print(f"Stream length: {r.xlen('orders')}")
print(f"Groups: {r.xinfo_groups('orders')}")
print(f"Consumers: {r.xinfo_consumers('orders', 'order-processors')}")
```

### Messages Piling Up

**Check:**
- Consumer processing too slow?
- Consumer crashed with pending messages?
- Need more consumers?

```python
# Check pending messages
pending_summary = r.xpending('orders', 'order-processors')
print(f"Pending: {pending_summary['pending']}")

# Claim stale messages
stale = r.xautoclaim('orders', 'order-processors', consumer_name, 60000, '0-0')
```

### Memory Usage Growing

**Check:**
- Stream trimming enabled?
- Trimming maxlen too high?

```python
# Enable aggressive trimming
r.xadd('orders', message, maxlen=1000, approximate=True)

# Or trim periodically
r.xtrim('orders', maxlen=10000, approximate=True)
```

## Performance Tips

1. **Use approximate trimming** (`~` in Redis CLI) for better performance
2. **Batch reads** with `count` parameter
3. **Connection pooling** for multiple consumers
4. **Pipeline commands** for bulk operations
5. **Monitor memory** with `INFO memory`

## Related Patterns

- **Work Queue**: Consumer groups for load balancing
- **Pub/Sub**: Use Redis pub/sub for fanout, streams for persistence
- **Dead Letter Queue**: Custom implementation with retry tracking
- **Priority Queues**: Multiple streams for different priorities
