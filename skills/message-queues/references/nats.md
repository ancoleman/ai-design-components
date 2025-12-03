# NATS - Cloud-Native Messaging

NATS is a high-performance, cloud-native messaging system with built-in request-reply patterns and JetStream for persistence.

## When to Use NATS

**Best for:**
- Cloud-native microservices (Kubernetes-friendly)
- Request-reply / RPC patterns
- Low-latency messaging (sub-millisecond)
- IoT and edge computing
- Lightweight pub/sub

**Not ideal for:**
- Event sourcing with long retention (use Kafka)
- Complex routing (use RabbitMQ)
- Transaction processing (use Temporal)

## Core Concepts

### Core NATS (At-Most-Once)

**Pub/Sub:** Fire-and-forget messaging
- No persistence
- No delivery guarantees
- Ultra-low latency

### JetStream (At-Least-Once, Exactly-Once)

**Stream:** Durable log of messages (like Kafka)
- Persistence (file/memory)
- Replay capability
- Acknowledgments

**Consumer:** Reads from stream
- Push (messages sent to subscriber)
- Pull (subscriber requests messages)

## Python Implementation

### Basic Pub/Sub

```python
import asyncio
import nats

async def main():
    # Connect to NATS
    nc = await nats.connect("nats://localhost:4222")

    # Publisher
    await nc.publish("orders", b"order_123")

    # Subscriber
    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received: {data} on {subject}")

    await nc.subscribe("orders", cb=message_handler)

    # Keep connection alive
    await asyncio.sleep(60)
    await nc.close()

asyncio.run(main())
```

### Request-Reply Pattern

```python
import asyncio
import nats
import json

async def main():
    nc = await nats.connect("nats://localhost:4222")

    # Responder (service)
    async def request_handler(msg):
        request = json.loads(msg.data.decode())
        user_id = request['user_id']

        # Fetch user profile
        profile = get_user_profile(user_id)

        # Send reply
        await msg.respond(json.dumps(profile).encode())

    await nc.subscribe("user.profile", cb=request_handler)

    # Requester (client)
    request = {"user_id": "123"}
    response = await nc.request(
        "user.profile",
        json.dumps(request).encode(),
        timeout=1.0  # 1 second timeout
    )

    profile = json.loads(response.data.decode())
    print(f"Profile: {profile}")

    await nc.close()

asyncio.run(main())
```

### JetStream Producer/Consumer

```python
import asyncio
import nats
from nats.js import api

async def main():
    nc = await nats.connect("nats://localhost:4222")

    # Get JetStream context
    js = nc.jetstream()

    # Create stream (if not exists)
    stream_config = api.StreamConfig(
        name="ORDERS",
        subjects=["orders.*"],
        retention=api.RetentionPolicy.LIMITS,
        max_age=86400 * 7,  # 7 days retention
        storage=api.StorageType.FILE,
    )

    try:
        await js.add_stream(stream_config)
    except nats.js.errors.StreamNameAlreadyInUseError:
        pass  # Stream exists

    # Publisher
    ack = await js.publish(
        "orders.created",
        b"order_123",
        timeout=1.0
    )
    print(f"Published: seq={ack.seq}")

    # Consumer (durable)
    consumer_config = api.ConsumerConfig(
        durable_name="order-processor",
        ack_policy=api.AckPolicy.EXPLICIT,
        deliver_policy=api.DeliverPolicy.ALL,
    )

    psub = await js.pull_subscribe(
        "orders.created",
        "order-processor",
        config=consumer_config
    )

    # Fetch messages
    msgs = await psub.fetch(batch=10, timeout=1.0)
    for msg in msgs:
        print(f"Processing: {msg.data.decode()}")
        await msg.ack()

    await nc.close()

asyncio.run(main())
```

## JetStream Patterns

### At-Least-Once Delivery

```python
# Consumer with manual ack
psub = await js.pull_subscribe("orders.*", "processor")

while True:
    msgs = await psub.fetch(batch=10, timeout=1.0)

    for msg in msgs:
        try:
            process_order(msg.data)
            await msg.ack()  # Ack after successful processing
        except RecoverableError:
            await msg.nak()  # Negative ack, will redeliver
        except UnrecoverableError:
            await msg.term()  # Terminate, don't redeliver
```

### Exactly-Once Delivery

```python
import redis

redis_client = redis.Redis()

psub = await js.pull_subscribe("orders.*", "processor")

while True:
    msgs = await psub.fetch(batch=10, timeout=1.0)

    for msg in msgs:
        # Get message ID (JetStream sequence)
        msg_id = f"{msg.metadata.stream}:{msg.metadata.sequence.stream}"

        # Idempotency check
        if redis_client.exists(f"processed:{msg_id}"):
            await msg.ack()  # Already processed
            continue

        # Process
        try:
            process_order(msg.data)
            redis_client.setex(f"processed:{msg_id}", 86400, "1")
            await msg.ack()
        except Exception as e:
            await msg.nak()
```

### Consumer Groups (Work Queue)

```python
# Multiple consumers with same durable name share workload
consumer_config = api.ConsumerConfig(
    durable_name="order-processors",  # Same for all workers
    ack_policy=api.AckPolicy.EXPLICIT,
    max_ack_pending=100,  # Limit inflight messages
)

psub = await js.pull_subscribe(
    "orders.*",
    "order-processors",
    config=consumer_config
)

# Each message delivered to one consumer
while True:
    msgs = await psub.fetch(batch=10, timeout=1.0)
    for msg in msgs:
        process_order(msg.data)
        await msg.ack()
```

## Stream Configuration

### Retention Policies

```python
# LIMITS: Retain until max messages/age/size
stream_config = api.StreamConfig(
    name="LOGS",
    retention=api.RetentionPolicy.LIMITS,
    max_msgs=1000000,  # Max 1M messages
    max_age=86400 * 7,  # 7 days
    max_bytes=10 * 1024 * 1024 * 1024,  # 10GB
)

# INTEREST: Retain until all consumers ack
stream_config = api.StreamConfig(
    name="EVENTS",
    retention=api.RetentionPolicy.INTEREST,
)

# WORKQUEUE: Delete after first consumer ack
stream_config = api.StreamConfig(
    name="TASKS",
    retention=api.RetentionPolicy.WORKQUEUE,
)
```

### Deduplication

```python
# Deduplicate by message ID header
await js.publish(
    "orders.created",
    b"order_123",
    headers={"Nats-Msg-Id": "unique-id-123"}  # Dedupe key
)

# Stream deduplication window
stream_config = api.StreamConfig(
    name="ORDERS",
    duplicate_window=60,  # 60 seconds
)
```

## Monitoring

### Stream Status

```python
# Get stream info
info = await js.stream_info("ORDERS")

print(f"Messages: {info.state.messages}")
print(f"Bytes: {info.state.bytes}")
print(f"First seq: {info.state.first_seq}")
print(f"Last seq: {info.state.last_seq}")
print(f"Consumers: {info.state.consumer_count}")
```

### Consumer Status

```python
# Get consumer info
info = await js.consumer_info("ORDERS", "order-processor")

print(f"Pending: {info.num_pending}")
print(f"Ack pending: {info.num_ack_pending}")
print(f"Redelivered: {info.num_redelivered}")
print(f"Last delivered: {info.delivered.stream_seq}")
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Gauge

messages_processed = Counter('nats_messages_processed', 'Total', ['subject'])
pending_messages = Gauge('nats_pending_messages', 'Pending', ['consumer'])

async def monitored_consumer():
    while True:
        msgs = await psub.fetch(batch=10, timeout=1.0)

        for msg in msgs:
            process_order(msg.data)
            await msg.ack()
            messages_processed.labels(subject=msg.subject).inc()

        # Update pending count
        info = await js.consumer_info("ORDERS", "processor")
        pending_messages.labels(consumer="processor").set(info.num_pending)
```

## Advanced Patterns

### Request-Reply with Timeout

```python
async def resilient_request(nc, subject, data, timeout=1.0, retries=3):
    """Request with retry logic"""
    for attempt in range(retries):
        try:
            response = await nc.request(subject, data, timeout=timeout)
            return response.data
        except asyncio.TimeoutError:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(0.1 * (2 ** attempt))  # Exponential backoff
```

### Multi-Subject Subscriptions

```python
# Subscribe to multiple subjects with wildcards
# * matches one token, > matches one or more tokens
await nc.subscribe("orders.*", cb=handler)  # orders.created, orders.updated
await nc.subscribe("logs.>", cb=handler)    # logs.app.error, logs.db.warning
```

### Queue Groups (Load Balancing)

```python
# Multiple subscribers with same queue group share load
await nc.subscribe("orders", queue="processors", cb=handler1)
await nc.subscribe("orders", queue="processors", cb=handler2)
await nc.subscribe("orders", queue="processors", cb=handler3)

# Each message delivered to one subscriber in queue group
```

## Clustering

### Connect to Cluster

```python
# Multiple servers for high availability
nc = await nats.connect(
    servers=[
        "nats://node1:4222",
        "nats://node2:4222",
        "nats://node3:4222"
    ],
    max_reconnect_attempts=-1,  # Infinite retries
    reconnect_time_wait=2,  # 2 seconds between retries
)
```

### JetStream Replication

```python
# Stream with 3 replicas (Raft consensus)
stream_config = api.StreamConfig(
    name="HA_ORDERS",
    subjects=["orders.*"],
    num_replicas=3,  # 3 nodes for fault tolerance
)
```

## Configuration Best Practices

### Producer Config

```python
nc = await nats.connect(
    servers=["nats://localhost:4222"],
    max_reconnect_attempts=-1,
    ping_interval=30,  # 30s ping
    max_outstanding_pings=3,
    name="order-producer",  # Client name
)

js = nc.jetstream()

# Publish with timeout and deduplication
await js.publish(
    "orders.created",
    data,
    timeout=5.0,
    headers={"Nats-Msg-Id": unique_id}
)
```

### Consumer Config

```python
consumer_config = api.ConsumerConfig(
    durable_name="processor",
    ack_policy=api.AckPolicy.EXPLICIT,
    ack_wait=30,  # 30s to ack before redelivery
    max_deliver=3,  # Max 3 delivery attempts
    max_ack_pending=1000,  # Max 1000 unacked messages
    deliver_policy=api.DeliverPolicy.ALL,
    filter_subject="orders.created",  # Only this subject
)
```

## Troubleshooting

### Messages Not Being Delivered

**Check:**
1. Stream exists? `nats stream list`
2. Consumer exists? `nats consumer list STREAM_NAME`
3. Subject matches? Check wildcards
4. Consumer ack pending limit reached?

```bash
# CLI tools
nats stream info ORDERS
nats consumer info ORDERS processor
```

### Consumer Lag Growing

**Check:**
- Processing too slow?
- Max ack pending limit?
- Network issues?

```python
# Monitor lag
info = await js.consumer_info("ORDERS", "processor")
lag = info.num_pending + info.num_ack_pending
print(f"Consumer lag: {lag}")
```

### Connection Issues

**Check:**
- NATS server running? `nats-server -v`
- Firewall blocking port 4222?
- Cluster connectivity?

```python
# Check connection status
if nc.is_connected:
    print("Connected")
else:
    print("Disconnected")
```

## Related Patterns

- **Request-Reply**: Built-in RPC pattern
- **Work Queue**: Queue groups for load balancing
- **Pub/Sub**: Core NATS pattern
- **Event Streaming**: JetStream for persistence
