# Message Queues - Master Plan

> **Skill Purpose**: Implement async communication patterns using message brokers and task queues for event-driven architectures, background job processing, and service decoupling across Python, Rust, Go, and TypeScript ecosystems.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Context7 research), Anthropic Skills best practices

---

## Strategic Positioning

### The Asynchronous Communication Gap

Modern applications require decoupled, scalable communication patterns:

```
Synchronous World (Request-Response):
User → API → Database → API → User
= Tight coupling, scaling bottlenecks, timeout risks

Asynchronous World (Event-Driven):
User → API → Queue → Worker Pool → Database → Notification
= Loose coupling, horizontal scaling, resilience
```

### Why This Skill Matters

| Problem | Message Queue Solution | Impact |
|---------|----------------------|--------|
| Long-running operations block requests | Background job processing (Celery, BullMQ) | Better UX, timeout prevention |
| Service coupling creates cascading failures | Event streaming (Kafka) | Resilience, fault isolation |
| Microservices coordination complexity | Workflow orchestration (Temporal) | Durable execution, saga patterns |
| Real-time data pipelines need reliable delivery | Message brokers (NATS, RabbitMQ) | Guaranteed delivery, replay |

### Integration with Other Skills

| Frontend Skill | Backend Integration | Message Queue Use Case |
|----------------|---------------------|------------------------|
| **forms** → | api-patterns → message-queues | Form submission triggers async validation/processing |
| **feedback** → | message-queues → realtime-sync | Job status updates via WebSocket/SSE |
| **ai-chat** → | model-serving → message-queues | LLM inference via worker queues |
| **media** → | api-patterns → message-queues | Image processing, video transcoding |
| **dashboards** → | databases-timeseries → message-queues | Metrics aggregation pipelines |

---

## Component Taxonomy

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Message Queue System Tiers                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TIER 1: MESSAGE BROKERS (Infrastructure)                   │
│  ├── Apache Kafka          Event streaming, log aggregation │
│  ├── NATS JetStream        Cloud-native, IoT, edge          │
│  ├── RabbitMQ              Complex routing, task queues     │
│  └── Redis Streams         Simple queues, caching layer     │
│                                                              │
│  TIER 2: TASK QUEUES (Application Layer)                    │
│  ├── Celery (Python)       Background jobs, periodic tasks  │
│  ├── BullMQ (TypeScript)   Node.js job processing           │
│  ├── Temporal              Workflow orchestration, sagas    │
│  └── Tokio (Rust)          In-process async tasks           │
│                                                              │
│  TIER 3: CLIENT LIBRARIES (Language Bindings)               │
│  ├── Python: confluent-kafka, celery, temporalio            │
│  ├── TypeScript: kafkajs, bullmq, @temporalio/client        │
│  ├── Rust: rdkafka, lapin (RabbitMQ)                        │
│  └── Go: confluent-kafka-go, asynq, temporal-go             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Context7 Library Research

### Kafka Ecosystem (Event Streaming)

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Confluent Kafka Python** | `/confluentinc/confluent-kafka-python` | High | 192 | 68.8 | Python Kafka client |
| Confluent Kafka Go | `/confluentinc/confluent-kafka-go` | High | 305 | - | Go Kafka client |
| Confluent Platform | `/websites/confluent_io-platform-current` | High | 18,627 | - | Full platform docs |

**Key Insights:**
- Confluent's Python client is production-ready with extensive documentation
- Platform documentation (18,627 snippets) provides comprehensive ecosystem coverage
- Go client equally mature for high-performance services

### Temporal (Workflow Orchestration)

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Temporal** | `/websites/temporal_io` | High | 3,769 | 80.9 | Workflow orchestration |
| Temporal Python | `/temporalio/samples-python` | High | 196 | - | Python examples |
| Temporal Go | `/temporalio/samples-go` | High | 79 | - | Go examples |

**Critical for AI Agents:**
- Durable execution survives service restarts
- Saga patterns for distributed transactions
- OpenAI Agents integration for LLM workflows
- Event sourcing native support

---

## Message Broker Comparison

### Performance & Latency Matrix

| Broker | Throughput (msg/s) | Latency (p99) | Persistence | Replay | Best For |
|--------|-------------------|---------------|-------------|--------|----------|
| **Apache Kafka** | 500K-1M+ | 10-50ms | Disk (log) | Yes | Event streaming, log aggregation, analytics |
| **NATS JetStream** | 200K-400K | Sub-ms to 5ms | Memory/Disk | Yes | Cloud-native microservices, IoT, edge |
| **RabbitMQ** | 50K-100K | 5-20ms | Disk/Memory | Limited | Complex routing, task queues, RPC |
| **Redis Streams** | 100K+ | Sub-ms | Memory (AOF) | Yes | Simple queues, already using Redis |

### Operational Characteristics

| Broker | Clustering | Delivery Guarantees | Protocol | Management UI |
|--------|-----------|---------------------|----------|---------------|
| **Kafka** | Yes (Zookeeper/KRaft) | At-least-once, exactly-once | Binary | Confluent Control Center |
| **NATS JetStream** | Yes (RAFT) | At-least-once, exactly-once | Text | NATS CLI, nats-box |
| **RabbitMQ** | Yes (Erlang) | At-least-once | AMQP 0.9.1 | Web UI (built-in) |
| **Redis Streams** | Sentinel/Cluster | At-least-once | RESP | RedisInsight |

---

## Task Queue Comparison

### By Language Ecosystem

| Queue | Language | Backend | Scheduling | Retries | Monitoring | Best For |
|-------|----------|---------|------------|---------|------------|----------|
| **Celery 5.4** | Python | Redis/RabbitMQ/SQS | Cron-like | Exponential backoff | Flower | Background jobs, periodic tasks |
| **BullMQ 5.x** | TypeScript | Redis | Repeat jobs | Automatic | Bull Board | Node.js job processing |
| **Temporal** | Multi | PostgreSQL | Workflows | Built-in | Web UI | Workflow orchestration, sagas |
| **Asynq** | Go | Redis | Periodic tasks | Retry with delay | Asynqmon | Go job queues |
| **Tokio** | Rust | In-process | Manual | Manual | - | In-process async tasks |

### Advanced Features Comparison

| Feature | Celery | BullMQ | Temporal | Asynq |
|---------|--------|--------|----------|-------|
| **Priority Queues** | ✅ | ✅ | ✅ | ✅ |
| **Rate Limiting** | ✅ (Redis) | ✅ | ✅ | ✅ |
| **Job Chaining** | ✅ (canvas) | ✅ (flows) | ✅ (workflows) | ✅ |
| **Delayed Execution** | ✅ (eta/countdown) | ✅ (delay) | ✅ (timers) | ✅ (schedule) |
| **Result Backend** | ✅ | ✅ | ✅ | ✅ |
| **Dead Letter Queue** | ⚠️ (manual) | ✅ | ✅ | ✅ |
| **Observability** | ⚠️ (Flower) | ✅ (Bull Board) | ✅ (Web UI) | ✅ (Asynqmon) |

---

## Decision Framework

### Primary Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│              Message Queue Selection Tree                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WHAT IS YOUR PRIMARY NEED?                                  │
│                                                              │
│  ├── EVENT STREAMING / LOG AGGREGATION                       │
│  │   └─ Apache Kafka                                         │
│  │       ✓ Replay events (event sourcing)                   │
│  │       ✓ Partitioning for parallelism                     │
│  │       ✓ Exactly-once semantics                           │
│  │       ✓ Long-term retention (days/weeks)                 │
│  │       Use: Analytics, CQRS, event sourcing               │
│  │                                                          │
│  ├── SIMPLE BACKGROUND JOBS                                  │
│  │   ├─ Python → Celery + Redis                             │
│  │   │   ✓ Mature (15+ years)                               │
│  │   │   ✓ Rich ecosystem                                   │
│  │   │   ✓ Periodic tasks (cron)                            │
│  │   │   Use: Email sending, report generation              │
│  │   │                                                      │
│  │   ├─ TypeScript → BullMQ + Redis                         │
│  │   │   ✓ Modern API                                       │
│  │   │   ✓ Excellent observability                          │
│  │   │   ✓ Job prioritization                               │
│  │   │   Use: Image processing, webhooks                    │
│  │   │                                                      │
│  │   └─ Go → Asynq + Redis                                  │
│  │       ✓ High performance                                 │
│  │       ✓ Simple API                                       │
│  │       Use: Go microservices                              │
│  │                                                          │
│  ├── COMPLEX WORKFLOWS / SAGAS                               │
│  │   └─ Temporal                                             │
│  │       ✓ Durable execution (survives restarts)            │
│  │       ✓ Saga pattern support                             │
│  │       ✓ Human-in-the-loop workflows                      │
│  │       ✓ Child workflows, signals, queries                │
│  │       Use: Order processing, AI agent orchestration      │
│  │                                                          │
│  ├── REQUEST-REPLY / RPC PATTERNS                            │
│  │   └─ NATS (with request-reply)                           │
│  │       ✓ Built-in request-reply                           │
│  │       ✓ Sub-millisecond latency                          │
│  │       ✓ No persistence overhead                          │
│  │       Use: Microservices RPC, IoT command/control        │
│  │                                                          │
│  ├── COMPLEX MESSAGE ROUTING                                 │
│  │   └─ RabbitMQ                                             │
│  │       ✓ Exchanges (direct, topic, fanout, headers)       │
│  │       ✓ Dead letter exchanges                            │
│  │       ✓ Message TTL, priorities                          │
│  │       Use: Multi-consumer patterns, pub/sub              │
│  │                                                          │
│  └── ALREADY USING REDIS                                     │
│      └─ Redis Streams                                        │
│          ✓ No new infrastructure                             │
│          ✓ Simple consumer groups                            │
│          ✓ Good for moderate throughput                     │
│          Use: Notification queues, simple job queues        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Secondary Considerations

```
┌─────────────────────────────────────────────────────────────┐
│              Operational Trade-offs                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  KAFKA                                                       │
│  ✓ Highest throughput, best for analytics                   │
│  ✗ Operational complexity (ZooKeeper/KRaft)                 │
│  ✗ Steeper learning curve                                   │
│  ✗ Overkill for simple job queues                           │
│                                                              │
│  NATS JetStream                                              │
│  ✓ Cloud-native, easiest operations                         │
│  ✓ Excellent performance                                    │
│  ✗ Smaller ecosystem than Kafka/RabbitMQ                    │
│  ✗ Less tooling                                             │
│                                                              │
│  RabbitMQ                                                    │
│  ✓ Mature, extensive plugin ecosystem                       │
│  ✓ Excellent routing flexibility                            │
│  ✗ Lower throughput than Kafka                              │
│  ✗ Memory-heavy                                             │
│                                                              │
│  Redis Streams                                               │
│  ✓ Simplest if already using Redis                          │
│  ✓ Lowest latency                                           │
│  ✗ Memory-bound (not for large volumes)                     │
│  ✗ Limited routing capabilities                             │
│                                                              │
│  Temporal                                                    │
│  ✓ Solves complex orchestration problems                    │
│  ✓ Incredible reliability guarantees                        │
│  ✗ Additional infrastructure (Temporal Server)              │
│  ✗ Learning curve for workflow concepts                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Temporal Workflows: Deep Dive

### Why Temporal is Critical for AI Agents

Temporal provides **durable execution** - workflows survive:
- Service crashes and restarts
- Network partitions
- Database outages
- Code deployments

This is **essential** for:
- Long-running AI agent workflows (hours/days)
- Multi-step LLM orchestration with retries
- Human-in-the-loop approval workflows
- Distributed transactions (saga pattern)

### Saga Pattern for Distributed Transactions

```python
# Temporal workflow for order processing with compensation
from temporalio import workflow, activity
from datetime import timedelta

@workflow.defn
class OrderSagaWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        try:
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

            # Step 3: Ship order
            shipping_id = await workflow.execute_activity(
                ship_order,
                order_id,
                start_to_close_timeout=timedelta(minutes=5),
            )

            return f"Order {order_id} completed"

        except Exception as e:
            # COMPENSATION LOGIC (rollback in reverse order)
            if 'payment_id' in locals():
                await workflow.execute_activity(
                    refund_payment,
                    payment_id,
                    start_to_close_timeout=timedelta(seconds=30),
                )

            if 'inventory_id' in locals():
                await workflow.execute_activity(
                    release_inventory,
                    inventory_id,
                    start_to_close_timeout=timedelta(seconds=10),
                )

            raise
```

### OpenAI Agents Integration

```python
# Temporal + OpenAI for durable AI workflows
from temporalio import workflow, activity
from openai import OpenAI
from datetime import timedelta

@activity.defn
async def call_llm(prompt: str) -> str:
    """LLM call as activity - automatically retried on failure"""
    client = OpenAI()
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@workflow.defn
class AIResearchWorkflow:
    @workflow.run
    async def run(self, topic: str) -> dict:
        # Step 1: Generate research questions (retried on failure)
        questions = await workflow.execute_activity(
            call_llm,
            f"Generate 5 research questions about {topic}",
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy={"maximum_attempts": 3}
        )

        # Step 2: Signal for human approval (workflow pauses here)
        approved = await workflow.wait_condition(
            lambda: self.approval_received,
            timeout=timedelta(hours=24)
        )

        if not approved:
            return {"status": "timeout"}

        # Step 3: Research each question (parallel activities)
        answers = []
        for q in questions.split("\n"):
            answer = await workflow.execute_activity(
                call_llm,
                f"Research and answer: {q}",
                start_to_close_timeout=timedelta(minutes=5),
            )
            answers.append(answer)

        # Step 4: Synthesize final report
        report = await workflow.execute_activity(
            call_llm,
            f"Synthesize answers into report: {answers}",
            start_to_close_timeout=timedelta(minutes=10),
        )

        return {"status": "complete", "report": report}

    @workflow.signal
    def approve(self):
        self.approval_received = True
```

### Event Sourcing with Temporal

```python
# Event-sourced aggregate pattern
from temporalio import workflow
from dataclasses import dataclass
from typing import List

@dataclass
class OrderCreated:
    order_id: str
    customer_id: str

@dataclass
class ItemAdded:
    order_id: str
    item_id: str
    quantity: int

@dataclass
class OrderSubmitted:
    order_id: str

@workflow.defn
class OrderAggregateWorkflow:
    def __init__(self):
        self.events: List = []
        self.state = "draft"
        self.items = []

    @workflow.run
    async def run(self, order_id: str):
        # Workflow runs indefinitely, processing signals
        await workflow.wait_condition(lambda: False)

    @workflow.signal
    def create_order(self, customer_id: str, order_id: str):
        event = OrderCreated(order_id, customer_id)
        self.events.append(event)
        self.apply(event)

    @workflow.signal
    def add_item(self, order_id: str, item_id: str, quantity: int):
        if self.state != "draft":
            raise ValueError("Can only add items to draft orders")
        event = ItemAdded(order_id, item_id, quantity)
        self.events.append(event)
        self.apply(event)

    @workflow.signal
    def submit_order(self, order_id: str):
        event = OrderSubmitted(order_id)
        self.events.append(event)
        self.apply(event)

    @workflow.query
    def get_state(self) -> dict:
        return {
            "state": self.state,
            "items": self.items,
            "event_count": len(self.events)
        }

    def apply(self, event):
        """Apply event to aggregate state"""
        if isinstance(event, OrderCreated):
            self.state = "draft"
        elif isinstance(event, ItemAdded):
            self.items.append({"id": event.item_id, "qty": event.quantity})
        elif isinstance(event, OrderSubmitted):
            self.state = "submitted"
```

---

## Frontend Integration Patterns

### Forms → Async Processing

```typescript
// React form submission with BullMQ job tracking
import { useState } from 'react'
import { useToast } from '@/hooks/use-toast'

export function UploadForm() {
  const [jobId, setJobId] = useState<string | null>(null)
  const { toast } = useToast()

  const handleSubmit = async (data: FormData) => {
    // Submit to API, which enqueues job
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: data,
    })

    const { jobId } = await response.json()
    setJobId(jobId)

    // Poll for job status (or use WebSocket)
    const interval = setInterval(async () => {
      const status = await fetch(`/api/jobs/${jobId}`)
      const { state, progress, result } = await status.json()

      if (state === 'completed') {
        clearInterval(interval)
        toast({
          title: 'Upload complete',
          description: result.message,
        })
      } else if (state === 'failed') {
        clearInterval(interval)
        toast({
          title: 'Upload failed',
          variant: 'destructive',
        })
      }
    }, 1000)
  }

  return <form onSubmit={handleSubmit}>{/* form fields */}</form>
}
```

### Feedback → Notifications

```python
# FastAPI + Celery + SSE for job status updates
from fastapi import FastAPI, BackgroundTasks
from celery import Celery
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()
celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task(bind=True)
def process_image(self, image_url: str):
    """Long-running image processing task"""
    self.update_state(state='PROGRESS', meta={'progress': 0})

    # Simulate processing steps
    for i in range(1, 6):
        time.sleep(2)  # Processing step
        self.update_state(
            state='PROGRESS',
            meta={'progress': i * 20, 'step': f'Processing step {i}'}
        )

    return {'status': 'complete', 'url': 'processed_image.jpg'}

@app.post("/process")
async def start_processing(image_url: str):
    task = process_image.delay(image_url)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def task_status_stream(task_id: str):
    """SSE endpoint for real-time job status"""
    async def event_generator():
        while True:
            task = celery_app.AsyncResult(task_id)

            if task.state == 'PROGRESS':
                yield {
                    "event": "progress",
                    "data": task.info.get('progress', 0)
                }
            elif task.state == 'SUCCESS':
                yield {
                    "event": "complete",
                    "data": task.result
                }
                break
            elif task.state == 'FAILURE':
                yield {
                    "event": "error",
                    "data": str(task.info)
                }
                break

            await asyncio.sleep(0.5)

    return EventSourceResponse(event_generator())
```

### AI Chat → Worker Processing

```python
# Temporal workflow for multi-turn AI conversations
from temporalio import workflow, activity
from datetime import timedelta
from typing import List, Dict

@activity.defn
async def call_llm(messages: List[Dict], model: str) -> str:
    """Activity: Call LLM API with retry logic"""
    # Automatically retried by Temporal on transient failures
    response = await openai_client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

@activity.defn
async def search_knowledge_base(query: str) -> List[str]:
    """Activity: RAG retrieval from vector DB"""
    # Qdrant search here
    results = await qdrant_client.search(...)
    return [hit.payload['text'] for hit in results]

@workflow.defn
class ConversationWorkflow:
    def __init__(self):
        self.messages: List[Dict] = []
        self.context: List[str] = []

    @workflow.run
    async def run(self):
        # Conversation runs indefinitely
        await workflow.wait_condition(lambda: False)

    @workflow.signal
    async def user_message(self, content: str):
        """Signal: User sends message"""
        self.messages.append({"role": "user", "content": content})

        # RAG: Search knowledge base
        relevant_docs = await workflow.execute_activity(
            search_knowledge_base,
            content,
            start_to_close_timeout=timedelta(seconds=10),
        )
        self.context = relevant_docs

        # Build prompt with context
        messages_with_context = [
            {"role": "system", "content": f"Context: {self.context}"},
            *self.messages
        ]

        # Call LLM
        response = await workflow.execute_activity(
            call_llm,
            args=[messages_with_context, "gpt-4"],
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy={"maximum_attempts": 3}
        )

        self.messages.append({"role": "assistant", "content": response})

    @workflow.query
    def get_messages(self) -> List[Dict]:
        return self.messages
```

---

## Event Patterns & Best Practices

### Event Naming Conventions

```
Domain.Entity.Action.Version

Examples:
- order.created.v1
- user.profile.updated.v2
- payment.failed.v1
- inventory.reserved.v1
```

### Event Schema Evolution

```json
{
  "event_type": "order.created.v2",
  "event_id": "uuid-here",
  "timestamp": "2025-12-02T10:00:00Z",
  "version": "2.0",
  "data": {
    "order_id": "ord_123",
    "customer_id": "cus_456",
    "items": [...],
    "total": 99.99,
    "currency": "USD"
  },
  "metadata": {
    "producer": "order-service",
    "trace_id": "abc123",
    "correlation_id": "xyz789"
  }
}
```

### Dead Letter Queue Pattern

```python
# Celery task with automatic DLQ on repeated failures
from celery import Celery
from celery.exceptions import Reject

app = Celery('tasks', broker='redis://localhost:6379')

@app.task(bind=True, max_retries=3)
def process_order(self, order_id: str):
    try:
        # Processing logic
        result = perform_processing(order_id)
        return result
    except RecoverableError as e:
        # Retry for transient errors
        raise self.retry(exc=e, countdown=60)
    except UnrecoverableError as e:
        # Send to DLQ, don't retry
        send_to_dlq(order_id, str(e))
        raise Reject(e, requeue=False)
```

### Idempotency Pattern

```python
# Ensure exactly-once processing with idempotency keys
from fastapi import FastAPI, Header
from redis import Redis
import hashlib

app = FastAPI()
redis_client = Redis()

@app.post("/process")
async def process_payment(
    payment_data: dict,
    idempotency_key: str = Header(None)
):
    if not idempotency_key:
        raise ValueError("Idempotency-Key header required")

    # Check if already processed
    cached_result = redis_client.get(f"idempotency:{idempotency_key}")
    if cached_result:
        return {"status": "already_processed", "result": cached_result}

    # Process payment
    result = process_payment_logic(payment_data)

    # Cache result for 24 hours
    redis_client.setex(
        f"idempotency:{idempotency_key}",
        86400,
        result
    )

    return {"status": "processed", "result": result}
```

---

## Performance & Monitoring

### Kafka Performance Tuning

```properties
# Producer configuration for high throughput
acks=1                          # Wait for leader ACK only (not all replicas)
compression.type=lz4            # Fast compression
batch.size=32768                # 32KB batches
linger.ms=10                    # Wait 10ms for batching
buffer.memory=67108864          # 64MB send buffer

# Consumer configuration for low latency
fetch.min.bytes=1               # Don't wait for large batches
fetch.max.wait.ms=100           # Max 100ms wait
max.partition.fetch.bytes=1048576  # 1MB per partition
```

### Celery Monitoring with Prometheus

```python
# Celery metrics exporter
from celery.signals import task_prerun, task_postrun, task_failure
from prometheus_client import Counter, Histogram
import time

task_counter = Counter('celery_task_total', 'Total tasks', ['task', 'state'])
task_duration = Histogram('celery_task_duration_seconds', 'Task duration', ['task'])

@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    task.start_time = time.time()

@task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    duration = time.time() - task.start_time
    task_duration.labels(task=task.name).observe(duration)
    task_counter.labels(task=task.name, state='success').inc()

@task_failure.connect
def task_failure_handler(task_id, exception, *args, **kwargs):
    task_counter.labels(task=kwargs['sender'].name, state='failure').inc()
```

### Temporal Observability

```python
# Temporal with OpenTelemetry tracing
from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure OpenTelemetry
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Create Temporal client with tracing
client = await Client.connect(
    "localhost:7233",
    interceptors=[TracingInterceptor()],
)

# All workflow executions are now traced in your observability backend
```

---

## Skill Structure

```
message-queues/
├── init.md                          # This file - master plan
├── SKILL.md                         # Main skill file (< 500 lines)
├── references/
│   ├── kafka-guide.md               # Kafka setup, patterns, tuning
│   ├── rabbitmq-guide.md            # RabbitMQ exchanges, routing
│   ├── nats-guide.md                # NATS JetStream patterns
│   ├── redis-streams-guide.md       # Redis Streams consumer groups
│   ├── temporal-workflows.md        # Workflow patterns, sagas
│   ├── celery-guide.md              # Celery tasks, periodic jobs
│   ├── bullmq-guide.md              # BullMQ job processing
│   ├── event-patterns.md            # Event sourcing, CQRS, DLQ
│   └── integration-patterns.md      # Frontend integration examples
├── scripts/
│   ├── setup_kafka.py               # Kafka cluster setup automation
│   ├── setup_temporal.py            # Temporal server setup
│   ├── validate_event_schema.py     # JSON schema validation
│   └── benchmark_throughput.py      # Performance testing
├── examples/
│   ├── kafka-python/
│   │   ├── producer.py
│   │   ├── consumer.py
│   │   └── README.md
│   ├── temporal-order-saga/
│   │   ├── workflow.py
│   │   ├── activities.py
│   │   └── worker.py
│   ├── celery-image-processing/
│   │   ├── tasks.py
│   │   ├── worker.py
│   │   └── api.py
│   ├── bullmq-webhook-processor/
│   │   ├── worker.ts
│   │   ├── queue.ts
│   │   └── api.ts
│   └── redis-streams-notifications/
│       ├── producer.py
│       └── consumer.py
└── assets/
    ├── diagrams/
    │   ├── kafka-architecture.svg
    │   ├── temporal-saga.svg
    │   └── event-driven-flow.svg
    └── schemas/
        └── event-schema.json         # JSON schema for events
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: message-queues
description: Async communication patterns using message brokers and task queues for event-driven architectures, background job processing, and service decoupling. Use when building systems requiring async processing, event streaming, workflow orchestration, or microservices communication. Covers Kafka (event streaming), RabbitMQ (complex routing), NATS (cloud-native), Redis Streams (simple queues), Celery (Python jobs), BullMQ (TypeScript jobs), Temporal (workflow orchestration), saga patterns, event sourcing, and frontend integration.
---
```

---

## Quality Checklist

### Pre-Implementation Validation

- [ ] Message broker selection matches use case (event streaming vs task queue vs RPC)
- [ ] Event schema versioning strategy defined
- [ ] Idempotency strategy implemented (for exactly-once semantics)
- [ ] Dead letter queue handling configured
- [ ] Monitoring and alerting set up (Prometheus, Grafana, or native UIs)
- [ ] Retry policies configured with exponential backoff
- [ ] Consumer group/partition strategy designed (for Kafka)

### Implementation Standards

- [ ] All events use consistent naming convention (Domain.Entity.Action.Version)
- [ ] Event schemas include metadata (trace_id, correlation_id, timestamp)
- [ ] Producers use batching for efficiency (where applicable)
- [ ] Consumers are idempotent (can handle duplicate messages)
- [ ] Error handling includes both transient and permanent failures
- [ ] Observability: all queue operations are traced/metered

### Operational Readiness

- [ ] Deployment automation scripts created (setup_kafka.py, etc.)
- [ ] Cluster configuration documented (replication factor, partitions)
- [ ] Backup and disaster recovery plan documented
- [ ] Performance benchmarks established
- [ ] Capacity planning calculations documented
- [ ] Runbook created for common issues

### Frontend Integration

- [ ] Job status polling or SSE/WebSocket updates implemented
- [ ] Progress indicators connected to queue state
- [ ] Error messages surfaced to users
- [ ] Retry mechanisms exposed (where appropriate)
- [ ] Integration with feedback skill (toasts, notifications)

---

## Integration Examples

### Example 1: E-Commerce Order Processing

```
User submits order (forms skill)
    ↓
API creates order (api-patterns skill)
    ↓
Publish OrderCreated event to Kafka
    ↓
Consumers:
├─ Inventory Service: Reserve stock → Kafka event
├─ Payment Service: Charge card → Kafka event
├─ Notification Service: Send confirmation email (Celery task)
└─ Analytics Service: Update dashboards (databases-timeseries)
    ↓
Temporal Saga coordinates compensation if any step fails
    ↓
WebSocket update to frontend (realtime-sync skill)
    ↓
Dashboard updates (dashboards skill)
```

### Example 2: AI-Powered Document Analysis

```
User uploads PDF (media skill + forms skill)
    ↓
API enqueues BullMQ job
    ↓
Worker:
├─ Extract text from PDF
├─ Chunk into sections
├─ Generate embeddings (ai-data-engineering skill)
└─ Store in Qdrant (databases-vector skill)
    ↓
Progress updates via SSE (realtime-sync skill)
    ↓
Completion notification (feedback skill)
    ↓
Results displayed in dashboard (dashboards + tables skills)
```

### Example 3: Real-Time Analytics Pipeline

```
IoT sensors publish data to NATS JetStream
    ↓
Stream processor:
├─ Aggregate per minute
├─ Write to TimescaleDB (databases-timeseries skill)
└─ Publish aggregated events to Kafka
    ↓
Consumers:
├─ Real-time dashboard updates (dashboards skill + realtime-sync)
├─ Anomaly detection ML model (model-serving skill)
└─ Long-term storage (databases-relational skill)
```

---

## Library Recommendations by Language

### Python

| Library | Use Case | Installation |
|---------|----------|--------------|
| **confluent-kafka** | Kafka client | `pip install confluent-kafka` |
| **celery[redis]** | Background jobs | `pip install celery[redis]` |
| **temporalio** | Workflow orchestration | `pip install temporalio` |
| **aio-pika** | RabbitMQ async | `pip install aio-pika` |
| **redis** | Redis Streams | `pip install redis` |

### TypeScript/Node.js

| Library | Use Case | Installation |
|---------|----------|--------------|
| **kafkajs** | Kafka client | `npm install kafkajs` |
| **bullmq** | Job queues | `npm install bullmq` |
| **@temporalio/client** | Temporal client | `npm install @temporalio/client` |
| **amqplib** | RabbitMQ | `npm install amqplib` |
| **ioredis** | Redis Streams | `npm install ioredis` |

### Rust

| Library | Use Case | Installation |
|---------|----------|--------------|
| **rdkafka** | Kafka client | `cargo add rdkafka` |
| **lapin** | RabbitMQ | `cargo add lapin` |
| **async-nats** | NATS client | `cargo add async-nats` |
| **redis** | Redis Streams | `cargo add redis` |

### Go

| Library | Use Case | Installation |
|---------|----------|--------------|
| **confluent-kafka-go** | Kafka client | `go get github.com/confluentinc/confluent-kafka-go` |
| **asynq** | Job queues | `go get github.com/hibiken/asynq` |
| **temporal-go** | Temporal SDK | `go get go.temporal.io/sdk` |
| **amqp091-go** | RabbitMQ | `go get github.com/rabbitmq/amqp091-go` |

---

## Success Metrics

This skill is successful when:

1. **Correct Pattern Selection**: Decision tree leads to appropriate queue choice 95%+ of time
2. **Zero Message Loss**: All production deployments achieve at-least-once delivery
3. **Performance Targets Met**: Throughput/latency meet documented broker specifications
4. **Operational Simplicity**: Setup scripts create working infrastructure without manual intervention
5. **Frontend Integration**: Background jobs surface status updates to users seamlessly
6. **Temporal Adoption**: Complex workflows use Temporal (not fragile manual coordination)

---

## Common Anti-Patterns to Avoid

### 1. Using Synchronous API Calls for Long Operations

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
    return {"task_id": task.id, "status_url": f"/tasks/{task.id}"}
```

### 2. Not Handling Duplicate Messages (Non-Idempotent Consumers)

```python
# ❌ BAD: Processes duplicates
@app.task
def send_email(user_id: str, email: str):
    send_email_service(user_id, email)  # Sends twice if retried!

# ✅ GOOD: Idempotent with deduplication
@app.task
def send_email(user_id: str, email: str, idempotency_key: str):
    if redis.exists(f"sent:{idempotency_key}"):
        return "already_sent"

    send_email_service(user_id, email)
    redis.setex(f"sent:{idempotency_key}", 86400, "1")
```

### 3. Ignoring Dead Letter Queues

```python
# ❌ BAD: Failed messages lost forever
@app.task(max_retries=3)
def risky_task(data):
    process(data)  # If all retries fail, data disappears

# ✅ GOOD: DLQ for manual inspection
@app.task(max_retries=3)
def risky_task(data):
    try:
        process(data)
    except Exception as e:
        if self.request.retries >= 3:
            send_to_dlq(data, str(e))
        raise
```

### 4. Using Kafka for RPC (Request-Reply)

```python
# ❌ BAD: Kafka is not designed for this
def get_user_profile(user_id: str):
    kafka_producer.send("user_requests", {"user_id": user_id})
    # Now what? Poll for response? Correlate messages?
    # This is painful and error-prone

# ✅ GOOD: Use NATS request-reply or HTTP/gRPC
response = await nats.request("user.profile", user_id.encode())
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

*Document Status: Planning Phase - Ready for SKILL.md Implementation*
*Research Sources: FULL_STACK_SKILLS_UNIFIED.md (Context7), Anthropic Skills Best Practices*
*Integration Points: api-patterns, databases-*, realtime-sync, observability, forms, feedback, ai-chat*
