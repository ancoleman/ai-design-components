# RabbitMQ - Advanced Message Routing

RabbitMQ is a robust message broker with sophisticated routing capabilities through exchanges and bindings. Best for complex pub/sub patterns and task queues.

## When to Use RabbitMQ

**Best for:**
- Complex routing patterns (topic, fanout, headers exchanges)
- Task queues with priority and TTL
- Dead letter exchanges (DLQ)
- Multi-consumer pub/sub
- AMQP 0.9.1 protocol compatibility

**Not ideal for:**
- Event streaming (use Kafka)
- Ultra-high throughput (use Kafka/NATS)
- Simple job queues (use Redis Streams)

## Core Concepts

### Exchanges and Bindings

**Exchange:** Routes messages to queues based on routing rules
**Binding:** Connection between exchange and queue with routing key

```
Producer → Exchange → Binding → Queue → Consumer
```

### Exchange Types

| Type | Routing Logic | Use Case |
|------|---------------|----------|
| **Direct** | Exact routing key match | Task distribution to specific workers |
| **Topic** | Pattern matching (wildcards) | Pub/sub with topic filtering |
| **Fanout** | Broadcast to all queues | Event broadcasting |
| **Headers** | Header attribute matching | Complex routing rules |

## Python Implementation

### Basic Producer/Consumer

```python
import pika
import json

# Connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Declare queue (idempotent)
channel.queue_declare(queue='tasks', durable=True)

# Producer: Publish message
message = {'task': 'process_image', 'url': 'image.jpg'}
channel.basic_publish(
    exchange='',
    routing_key='tasks',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2,  # Make message persistent
    )
)

print("Message sent")
connection.close()

# Consumer
def callback(ch, method, properties, body):
    """Process message"""
    message = json.loads(body)
    print(f"Processing: {message}")

    # Simulate work
    process_task(message)

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)  # Fair dispatch
channel.basic_consume(queue='tasks', on_message_callback=callback)

print("Waiting for messages...")
channel.start_consuming()
```

### Async Python with aio-pika

```python
import asyncio
import aio_pika
import json

async def main():
    # Connection
    connection = await aio_pika.connect_robust("amqp://localhost/")

    async with connection:
        channel = await connection.channel()

        # Declare queue
        queue = await channel.declare_queue("tasks", durable=True)

        # Consumer
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body.decode())
                    print(f"Processing: {body}")
                    await process_task(body)

asyncio.run(main())
```

## Exchange Patterns

### Direct Exchange (Task Distribution)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare direct exchange
channel.exchange_declare(exchange='tasks', exchange_type='direct')

# Declare queues
channel.queue_declare(queue='high_priority')
channel.queue_declare(queue='low_priority')

# Bind queues to exchange
channel.queue_bind(exchange='tasks', queue='high_priority', routing_key='high')
channel.queue_bind(exchange='tasks', queue='low_priority', routing_key='low')

# Publish to high priority
channel.basic_publish(
    exchange='tasks',
    routing_key='high',
    body='urgent task'
)

# Publish to low priority
channel.basic_publish(
    exchange='tasks',
    routing_key='low',
    body='normal task'
)
```

### Topic Exchange (Pattern Matching)

```python
# Declare topic exchange
channel.exchange_declare(exchange='logs', exchange_type='topic')

# Declare queues
channel.queue_declare(queue='critical_logs')
channel.queue_declare(queue='app_logs')
channel.queue_declare(queue='all_logs')

# Bindings with wildcards
# * matches one word, # matches zero or more words
channel.queue_bind(exchange='logs', queue='critical_logs', routing_key='*.critical')
channel.queue_bind(exchange='logs', queue='app_logs', routing_key='app.*')
channel.queue_bind(exchange='logs', queue='all_logs', routing_key='#')

# Publish messages
channel.basic_publish(exchange='logs', routing_key='app.error', body='App error')
channel.basic_publish(exchange='logs', routing_key='db.critical', body='DB failure')
channel.basic_publish(exchange='logs', routing_key='system.info', body='System info')

# Routing:
# app.error → app_logs, all_logs
# db.critical → critical_logs, all_logs
# system.info → all_logs
```

### Fanout Exchange (Broadcast)

```python
# Declare fanout exchange
channel.exchange_declare(exchange='notifications', exchange_type='fanout')

# Declare queues
channel.queue_declare(queue='email_service')
channel.queue_declare(queue='sms_service')
channel.queue_declare(queue='push_service')

# Bind all queues (routing key ignored)
channel.queue_bind(exchange='notifications', queue='email_service')
channel.queue_bind(exchange='notifications', queue='sms_service')
channel.queue_bind(exchange='notifications', queue='push_service')

# Publish once, all queues receive
channel.basic_publish(
    exchange='notifications',
    routing_key='',  # Ignored for fanout
    body='New order #123'
)
```

### Headers Exchange (Attribute Matching)

```python
# Declare headers exchange
channel.exchange_declare(exchange='events', exchange_type='headers')

# Declare queues
channel.queue_declare(queue='order_events')
channel.queue_declare(queue='payment_events')

# Bind with header matching
channel.queue_bind(
    exchange='events',
    queue='order_events',
    arguments={
        'x-match': 'all',  # Match all headers
        'type': 'order',
        'priority': 'high'
    }
)

channel.queue_bind(
    exchange='events',
    queue='payment_events',
    arguments={
        'x-match': 'any',  # Match any header
        'type': 'payment',
        'source': 'stripe'
    }
)

# Publish with headers
channel.basic_publish(
    exchange='events',
    routing_key='',  # Ignored for headers
    body='Order created',
    properties=pika.BasicProperties(
        headers={'type': 'order', 'priority': 'high'}
    )
)
```

## Advanced Features

### Dead Letter Exchange (DLQ)

```python
# Declare DLQ
channel.exchange_declare(exchange='dlx', exchange_type='direct')
channel.queue_declare(queue='failed_tasks')
channel.queue_bind(exchange='dlx', queue='failed_tasks', routing_key='failed')

# Declare main queue with DLX
channel.queue_declare(
    queue='tasks',
    durable=True,
    arguments={
        'x-dead-letter-exchange': 'dlx',
        'x-dead-letter-routing-key': 'failed',
        'x-message-ttl': 60000,  # 1 minute TTL
    }
)

# Messages rejected or expired go to DLQ
def callback(ch, method, properties, body):
    try:
        process_task(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except UnrecoverableError:
        # Reject → goes to DLQ
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```

### Message Priority

```python
# Declare priority queue
channel.queue_declare(
    queue='priority_tasks',
    arguments={'x-max-priority': 10}
)

# Publish with priority
channel.basic_publish(
    exchange='',
    routing_key='priority_tasks',
    body='high priority task',
    properties=pika.BasicProperties(
        priority=9,  # 0-10
        delivery_mode=2
    )
)

channel.basic_publish(
    exchange='',
    routing_key='priority_tasks',
    body='low priority task',
    properties=pika.BasicProperties(
        priority=1,
        delivery_mode=2
    )
)

# Consumer receives high priority first
```

### Message TTL (Time-To-Live)

```python
# Queue-level TTL (all messages expire)
channel.queue_declare(
    queue='temporary_tasks',
    arguments={'x-message-ttl': 60000}  # 60 seconds
)

# Message-level TTL
channel.basic_publish(
    exchange='',
    routing_key='tasks',
    body='expires soon',
    properties=pika.BasicProperties(
        expiration='30000'  # 30 seconds (string!)
    )
)
```

### Consumer Prefetch (Fair Dispatch)

```python
# Limit unacknowledged messages per consumer
channel.basic_qos(prefetch_count=1)

# Now consumers only get 1 message at a time
# Prevents one consumer from hogging all messages
channel.basic_consume(queue='tasks', on_message_callback=callback)
```

## Production Patterns

### Retry with Exponential Backoff

```python
def callback_with_retry(ch, method, properties, body):
    """Retry with exponential backoff using headers"""
    try:
        process_task(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except RecoverableError as e:
        # Get retry count from headers
        headers = properties.headers or {}
        retry_count = headers.get('x-retry-count', 0)

        if retry_count < 3:
            # Republish with incremented retry count
            delay_ms = 1000 * (2 ** retry_count)  # Exponential backoff

            ch.basic_publish(
                exchange='',
                routing_key='tasks_retry',
                body=body,
                properties=pika.BasicProperties(
                    headers={'x-retry-count': retry_count + 1},
                    expiration=str(delay_ms)
                )
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Max retries reached, send to DLQ
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```

### Idempotent Consumer

```python
import redis

redis_client = redis.Redis()

def idempotent_callback(ch, method, properties, body):
    """Ensure exactly-once processing"""
    message_id = properties.message_id

    # Check if already processed
    if redis_client.exists(f'processed:{message_id}'):
        print(f"Already processed {message_id}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Process message
    result = process_task(body)

    # Mark as processed (24h TTL)
    redis_client.setex(f'processed:{message_id}', 86400, '1')

    ch.basic_ack(delivery_tag=method.delivery_tag)
```

### Publisher Confirms

```python
# Enable publisher confirms
channel.confirm_delivery()

try:
    channel.basic_publish(
        exchange='',
        routing_key='tasks',
        body='important message',
        mandatory=True  # Require queue to exist
    )
    print("Message confirmed by broker")
except pika.exceptions.UnroutableError:
    print("Message could not be routed")
except pika.exceptions.NackError:
    print("Message was nacked by broker")
```

## Monitoring

### Management API

```python
import requests

# Get queue stats
response = requests.get(
    'http://localhost:15672/api/queues/%2F/tasks',  # %2F = default vhost /
    auth=('guest', 'guest')
)

stats = response.json()
print(f"Messages: {stats['messages']}")
print(f"Consumers: {stats['consumers']}")
print(f"Message rate: {stats['messages_details']['rate']}")
```

### Prometheus Exporter

```python
from prometheus_client import Counter, Gauge, Histogram
import time

messages_consumed = Counter('rabbitmq_messages_consumed_total', 'Total messages', ['queue'])
processing_duration = Histogram('rabbitmq_processing_seconds', 'Processing time', ['queue'])
queue_depth = Gauge('rabbitmq_queue_depth', 'Queue depth', ['queue'])

def monitored_callback(ch, method, properties, body):
    start_time = time.time()

    try:
        process_task(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        # Record metrics
        messages_consumed.labels(queue='tasks').inc()
        processing_duration.labels(queue='tasks').observe(time.time() - start_time)

        # Update queue depth
        info = ch.queue_declare(queue='tasks', passive=True)
        queue_depth.labels(queue='tasks').set(info.method.message_count)

    except Exception as e:
        print(f"Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```

## Clustering and High Availability

### Mirrored Queues (Classic Queues)

```python
# Declare mirrored queue (replicated across nodes)
channel.queue_declare(
    queue='ha_tasks',
    durable=True,
    arguments={
        'x-ha-policy': 'all',  # Mirror to all nodes
        # Or use 'exactly' with 'x-ha-params': 2
    }
)
```

### Quorum Queues (Recommended for HA)

```python
# Declare quorum queue (Raft-based replication)
channel.queue_declare(
    queue='quorum_tasks',
    durable=True,
    arguments={
        'x-queue-type': 'quorum',
        'x-quorum-initial-group-size': 3,  # 3 replicas
    }
)
```

## Configuration Best Practices

### Producer Config

```python
connection_params = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=pika.PlainCredentials('user', 'password'),
    heartbeat=600,  # 10 minutes
    blocked_connection_timeout=300,  # 5 minutes
    connection_attempts=3,
    retry_delay=2,
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Enable publisher confirms
channel.confirm_delivery()

# Publish with properties
channel.basic_publish(
    exchange='',
    routing_key='tasks',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # Persistent
        content_type='application/json',
        message_id=str(uuid.uuid4()),
        timestamp=int(time.time()),
    ),
    mandatory=True  # Return if unroutable
)
```

### Consumer Config

```python
# Prefetch for fair dispatch
channel.basic_qos(
    prefetch_count=1,  # Max unacknowledged messages
    prefetch_size=0,  # 0 = no byte limit
    global_qos=False  # Per-consumer (not per-channel)
)

# Consume with manual ack
channel.basic_consume(
    queue='tasks',
    on_message_callback=callback,
    auto_ack=False  # Manual acknowledgment
)
```

## Troubleshooting

### Messages Not Being Consumed

**Check:**
1. Queue declared correctly?
2. Consumer connected to same queue?
3. Prefetch limit too low?
4. Consumer crashed?

```bash
# Check queue in management UI or CLI
rabbitmqctl list_queues name messages consumers
```

### Messages Piling Up

**Causes:**
- Consumers too slow
- Not enough consumers
- Consumer crashes without ack

**Fix:**
```python
# Add more consumers (scale horizontally)
# Or increase prefetch
channel.basic_qos(prefetch_count=10)
```

### Connection Errors

**Check:**
- RabbitMQ running?
- Credentials correct?
- Firewall blocking port 5672?

```bash
# Check RabbitMQ status
rabbitmqctl status

# Check logs
tail -f /var/log/rabbitmq/rabbit@hostname.log
```

## Related Patterns

- **Work Queues**: Fair dispatch with prefetch
- **Pub/Sub**: Fanout exchange broadcasting
- **Routing**: Direct/topic exchanges for filtering
- **RPC**: Request-reply with correlation ID and reply-to queue
