---
sidebar_position: 7
title: Message Queues
description: Async communication patterns using message brokers and task queues
tags: [backend, messaging, kafka, rabbitmq, celery, async]
---

# Message Queues

Implement asynchronous communication patterns for event-driven architectures, background job processing, and service decoupling.

## When to Use

Use message queues when:
- **Long-running operations** block HTTP requests (report generation, video processing)
- **Service decoupling** required (microservices, event-driven architecture)
- **Guaranteed delivery** needed (payment processing, order fulfillment)
- **Event streaming** for analytics (log aggregation, metrics pipelines)
- **Workflow orchestration** for complex processes (multi-step sagas, human-in-the-loop)
- **Background job processing** (email sending, image resizing)

## Multi-Language Support

This skill provides patterns for:
- **Python**: Celery + Redis, confluent-kafka, Temporal
- **TypeScript**: BullMQ + Redis, kafkajs, @temporalio/client
- **Rust**: lapin (RabbitMQ), rdkafka
- **Go**: Asynq + Redis, franz-go (Kafka), Temporal SDK

## Broker Selection Decision Tree

### Event Streaming / Log Aggregation
**→ Apache Kafka**
- Throughput: 500K-1M msg/s
- Replay events (event sourcing)
- Exactly-once semantics
- Long-term retention
- Use: Analytics pipelines, CQRS, event sourcing

### Simple Background Jobs
**→ Task Queues**
- **Python** → Celery + Redis
- **TypeScript** → BullMQ + Redis
- **Go** → Asynq + Redis
- Use: Email sending, report generation, webhooks

### Complex Workflows / Sagas
**→ Temporal**
- Durable execution (survives restarts)
- Saga pattern support
- Human-in-the-loop workflows
- Use: Order processing, AI agent orchestration

### Request-Reply / RPC Patterns
**→ NATS**
- Built-in request-reply
- Sub-millisecond latency
- Cloud-native, simple operations
- Use: Microservices RPC, IoT command/control

### Complex Message Routing
**→ RabbitMQ**
- Exchanges (direct, topic, fanout, headers)
- Dead letter exchanges
- Message TTL, priorities
- Use: Multi-consumer patterns, pub/sub

### Already Using Redis
**→ Redis Streams**
- No new infrastructure
- Simple consumer groups
- Moderate throughput (100K+ msg/s)
- Use: Notification queues, simple job queues

## Performance Comparison

| Broker | Throughput | Latency (p99) | Best For |
|--------|-----------|---------------|----------|
| **Kafka** | 500K-1M msg/s | 10-50ms | Event streaming |
| **NATS JetStream** | 200K-400K msg/s | Sub-ms to 5ms | Cloud-native microservices |
| **RabbitMQ** | 50K-100K msg/s | 5-20ms | Task queues, complex routing |
| **Redis Streams** | 100K+ msg/s | Sub-ms | Simple queues, caching |

## Quick Start Examples

### Kafka Producer/Consumer (Python)

```python
from confluent_kafka import Producer, Consumer

# Producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})
producer.produce('orders', key='order_123', value='{"status": "created"}')
producer.flush()

# Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-processors',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['orders'])

while True:
    msg = consumer.poll(1.0)
    if msg is not None:
        process_order(msg.value())
```

### Celery Background Jobs (Python)

```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task(bind=True, max_retries=3)
def process_image(self, image_url: str):
    try:
        result = expensive_image_processing(image_url)
        return result
    except RecoverableError as e:
        raise self.retry(exc=e, countdown=60)
```

### BullMQ Job Processing (TypeScript)

```typescript
import { Queue, Worker } from 'bullmq'

const queue = new Queue('webhooks', {
  connection: { host: 'localhost', port: 6379 }
})

// Enqueue job
await queue.add('send-webhook', {
  url: 'https://example.com/webhook',
  payload: { event: 'order.created' }
})

// Process jobs
const worker = new Worker('webhooks', async job => {
  await fetch(job.data.url, {
    method: 'POST',
    body: JSON.stringify(job.data.payload)
  })
}, { connection: { host: 'localhost', port: 6379 } })
```

### Temporal Workflow Orchestration

```python
from temporalio import workflow, activity
from datetime import timedelta

@workflow.defn
class OrderSagaWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        # Step 1: Reserve inventory
        inventory_id = await workflow.execute_activity(
            reserve_inventory,
            order_id,
            start_to_close_timeout=timedelta(seconds=10),
        )

        # Step 2: Charge payment
        payment_id = await workflow.execute_activity(
            charge_payment,
            order_id,
            start_to_close_timeout=timedelta(seconds=30),
        )

        return f"Order {order_id} completed"
```

## Core Patterns

### Event Naming Convention
Use: `Domain.Entity.Action.Version`

Examples:
- `order.created.v1`
- `user.profile.updated.v2`
- `payment.failed.v1`

### Event Schema Structure
```json
{
  "event_type": "order.created.v2",
  "event_id": "uuid-here",
  "timestamp": "2025-12-02T10:00:00Z",
  "version": "2.0",
  "data": {
    "order_id": "ord_123",
    "customer_id": "cus_456"
  },
  "metadata": {
    "producer": "order-service",
    "trace_id": "abc123",
    "correlation_id": "xyz789"
  }
}
```

### Dead Letter Queue Pattern
Route failed messages to dead letter queue (DLQ) after max retries:

```python
@app.task(bind=True, max_retries=3)
def process_order(self, order_id: str):
    try:
        result = perform_processing(order_id)
        return result
    except UnrecoverableError as e:
        send_to_dlq(order_id, str(e))
        raise Reject(e, requeue=False)
```

### Idempotency for Exactly-Once Processing

```python
@app.post("/process")
async def process_payment(
    payment_data: dict,
    idempotency_key: str = Header(None)
):
    # Check if already processed
    cached_result = redis_client.get(f"idempotency:{idempotency_key}")
    if cached_result:
        return {"status": "already_processed"}

    result = process_payment_logic(payment_data)
    redis_client.setex(f"idempotency:{idempotency_key}", 86400, result)
    return {"status": "processed", "result": result}
```

## Frontend Integration

### Job Status Updates via SSE

```python
# FastAPI endpoint for real-time job status
@app.get("/status/{task_id}")
async def task_status_stream(task_id: str):
    async def event_generator():
        while True:
            task = celery_app.AsyncResult(task_id)

            if task.state == 'PROGRESS':
                yield {"event": "progress", "data": task.info.get('progress', 0)}
            elif task.state == 'SUCCESS':
                yield {"event": "complete", "data": task.result}
                break

            await asyncio.sleep(0.5)

    return EventSourceResponse(event_generator())
```

### React Component

```typescript
export function JobStatus({ jobId }: { jobId: string }) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const eventSource = new EventSource(`/api/status/${jobId}`)

    eventSource.addEventListener('progress', (e) => {
      setProgress(JSON.parse(e.data))
    })

    eventSource.addEventListener('complete', (e) => {
      toast({ title: 'Job complete', description: JSON.parse(e.data) })
      eventSource.close()
    })

    return () => eventSource.close()
  }, [jobId])

  return &lt;ProgressBar value={progress} />
}
```

## Common Anti-Patterns to Avoid

### 1. Synchronous API for Long Operations
```python
# ❌ BAD: Blocks request thread
@app.post("/generate-report")
def generate_report(user_id: str):
    report = expensive_computation(user_id)  # 5 minutes!
    return report

# ✅ GOOD: Enqueue background job
@app.post("/generate-report")
async def generate_report(user_id: str):
    task = generate_report_task.delay(user_id)
    return {"task_id": task.id}
```

### 2. Non-Idempotent Consumers
Always implement idempotency checks to prevent duplicate processing.

### 3. Ignoring Dead Letter Queues
Always configure DLQs for manual inspection of failed messages.

### 4. Using Kafka for Request-Reply
Kafka is asynchronous - use NATS or HTTP/gRPC for request-reply patterns.

## Related Skills

- [API Patterns](./implementing-api-patterns) - API design for async job submission
- [Real-time Sync](./implementing-realtime-sync) - WebSocket/SSE for job status updates
- [Feedback](../frontend/providing-feedback) - Toast notifications for job completion
- [Observability](./implementing-observability) - Tracing and metrics for queue operations

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/using-message-queues)
- Kafka: https://kafka.apache.org/
- Celery: https://docs.celeryq.dev/
- BullMQ: https://docs.bullmq.io/
- Temporal: https://temporal.io/
