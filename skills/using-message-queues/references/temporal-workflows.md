# Temporal Workflows - Durable Execution

Temporal provides **durable execution** for workflows that survive service crashes, network partitions, and code deployments. Critical for complex orchestration and long-running processes.


## Table of Contents

- [When to Use Temporal](#when-to-use-temporal)
- [Core Concepts](#core-concepts)
  - [Workflows vs Activities](#workflows-vs-activities)
  - [Signals and Queries](#signals-and-queries)
- [Python Implementation](#python-implementation)
  - [Basic Workflow](#basic-workflow)
  - [Saga Pattern for Distributed Transactions](#saga-pattern-for-distributed-transactions)
  - [Human-in-the-Loop with Signals](#human-in-the-loop-with-signals)
  - [AI Agent Orchestration](#ai-agent-orchestration)
- [Running Workflows](#running-workflows)
  - [Start Temporal Server](#start-temporal-server)
  - [Worker Implementation](#worker-implementation)
  - [Execute Workflow](#execute-workflow)
  - [Send Signal](#send-signal)
- [Advanced Patterns](#advanced-patterns)
  - [Child Workflows](#child-workflows)
  - [Parallel Activities](#parallel-activities)
  - [Continue-as-New (Long-Running Workflows)](#continue-as-new-long-running-workflows)
- [Observability](#observability)
  - [OpenTelemetry Integration](#opentelemetry-integration)
  - [Workflow Logging](#workflow-logging)
- [Best Practices](#best-practices)
  - [1. Workflows Must Be Deterministic](#1-workflows-must-be-deterministic)
  - [2. Use Activities for Side Effects](#2-use-activities-for-side-effects)
  - [3. Set Appropriate Timeouts](#3-set-appropriate-timeouts)
  - [4. Use Queries for Status Checks](#4-use-queries-for-status-checks)
- [Troubleshooting](#troubleshooting)
  - [Workflow Stuck](#workflow-stuck)
  - [Non-Deterministic Error](#non-deterministic-error)
  - [Activity Retry Exhausted](#activity-retry-exhausted)
- [Related Patterns](#related-patterns)

## When to Use Temporal

**Best for:**
- **Saga patterns** (distributed transactions with compensation)
- **Long-running workflows** (hours/days/months)
- **Human-in-the-loop** (approval workflows, manual steps)
- **AI agent orchestration** (multi-step LLM workflows with retries)
- **Complex state machines** (order fulfillment, onboarding flows)

**Not ideal for:**
- Simple background jobs (use Celery/BullMQ)
- High-throughput event processing (use Kafka)
- Request-reply RPC (use NATS/gRPC)

## Core Concepts

### Workflows vs Activities

**Workflow:** Orchestration logic (deterministic, retryable, durable)
- Survives service restarts
- Replayed from event history
- Must be deterministic (no random(), datetime.now() directly)

**Activity:** External side effects (non-deterministic, can be retried)
- API calls, database writes, file I/O
- Can fail and be retried with backoff
- Can take hours/days with heartbeats

```
Workflow (Orchestrator)
├─ Activity: Reserve Inventory
├─ Activity: Charge Payment
├─ Activity: Ship Order
└─ Activity: Send Confirmation Email
```

### Signals and Queries

**Signal:** External event that modifies workflow state
- Async, fire-and-forget
- Use for: User actions, external triggers

**Query:** Read workflow state without modifying it
- Synchronous
- Use for: Status checks, progress updates

## Python Implementation

### Basic Workflow

```python
from temporalio import workflow, activity
from datetime import timedelta

@activity.defn
async def send_email(email: str, subject: str, body: str) -> str:
    """Activity: Send email (can fail, will be retried)"""
    import aiosmtplib
    # Send email via SMTP
    await aiosmtplib.send(...)
    return "email_sent"

@workflow.defn
class OnboardingWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> str:
        # Step 1: Send welcome email
        await workflow.execute_activity(
            send_email,
            args=["user@example.com", "Welcome!", "..."],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=workflow.RetryPolicy(
                maximum_attempts=3,
                backoff_coefficient=2.0,
            )
        )

        # Step 2: Wait 3 days (workflow sleeps, doesn't block)
        await workflow.async_sleep(timedelta(days=3))

        # Step 3: Send follow-up email
        await workflow.execute_activity(
            send_email,
            args=["user@example.com", "How's it going?", "..."],
            start_to_close_timeout=timedelta(seconds=30),
        )

        return f"Onboarding complete for {user_id}"
```

### Saga Pattern for Distributed Transactions

```python
from temporalio import workflow, activity
from datetime import timedelta
from typing import Optional

@activity.defn
async def reserve_inventory(order_id: str) -> str:
    """Reserve inventory, return reservation ID"""
    # Call inventory service
    reservation = await inventory_service.reserve(order_id)
    return reservation['reservation_id']

@activity.defn
async def release_inventory(reservation_id: str) -> None:
    """Compensation: Release inventory"""
    await inventory_service.release(reservation_id)

@activity.defn
async def charge_payment(order_id: str) -> str:
    """Charge payment, return payment ID"""
    payment = await payment_service.charge(order_id)
    return payment['payment_id']

@activity.defn
async def refund_payment(payment_id: str) -> None:
    """Compensation: Refund payment"""
    await payment_service.refund(payment_id)

@activity.defn
async def ship_order(order_id: str) -> str:
    """Ship order, return tracking number"""
    shipment = await shipping_service.create(order_id)
    return shipment['tracking_number']

@workflow.defn
class OrderSagaWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        reservation_id: Optional[str] = None
        payment_id: Optional[str] = None

        try:
            # Step 1: Reserve inventory
            workflow.logger.info(f"Reserving inventory for {order_id}")
            reservation_id = await workflow.execute_activity(
                reserve_inventory,
                order_id,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=workflow.RetryPolicy(maximum_attempts=3),
            )

            # Step 2: Charge payment
            workflow.logger.info(f"Charging payment for {order_id}")
            payment_id = await workflow.execute_activity(
                charge_payment,
                order_id,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=workflow.RetryPolicy(maximum_attempts=3),
            )

            # Step 3: Ship order
            workflow.logger.info(f"Shipping order {order_id}")
            tracking_number = await workflow.execute_activity(
                ship_order,
                order_id,
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=workflow.RetryPolicy(maximum_attempts=3),
            )

            return f"Order {order_id} completed. Tracking: {tracking_number}"

        except Exception as e:
            workflow.logger.error(f"Order {order_id} failed: {e}")

            # COMPENSATION LOGIC (rollback in reverse order)
            if payment_id:
                workflow.logger.info(f"Refunding payment {payment_id}")
                await workflow.execute_activity(
                    refund_payment,
                    payment_id,
                    start_to_close_timeout=timedelta(seconds=30),
                )

            if reservation_id:
                workflow.logger.info(f"Releasing inventory {reservation_id}")
                await workflow.execute_activity(
                    release_inventory,
                    reservation_id,
                    start_to_close_timeout=timedelta(seconds=10),
                )

            raise Exception(f"Order {order_id} failed and was compensated")
```

### Human-in-the-Loop with Signals

```python
from temporalio import workflow, activity
from datetime import timedelta

@workflow.defn
class ExpenseApprovalWorkflow:
    def __init__(self):
        self.approved = False
        self.rejected = False

    @workflow.run
    async def run(self, expense_id: str, amount: float) -> str:
        # Notify manager
        await workflow.execute_activity(
            notify_manager,
            args=[expense_id, amount],
            start_to_close_timeout=timedelta(seconds=10),
        )

        # Wait for approval (up to 7 days)
        workflow.logger.info(f"Waiting for approval of {expense_id}")
        approved = await workflow.wait_condition(
            lambda: self.approved or self.rejected,
            timeout=timedelta(days=7)
        )

        if not approved:
            # Timeout - auto-reject
            await workflow.execute_activity(
                notify_timeout,
                expense_id,
                start_to_close_timeout=timedelta(seconds=10),
            )
            return "timeout"

        if self.approved:
            # Process payment
            await workflow.execute_activity(
                process_payment,
                expense_id,
                start_to_close_timeout=timedelta(minutes=5),
            )
            return "approved"
        else:
            # Rejected
            await workflow.execute_activity(
                notify_rejection,
                expense_id,
                start_to_close_timeout=timedelta(seconds=10),
            )
            return "rejected"

    @workflow.signal
    def approve(self):
        """Signal: Manager approves expense"""
        self.approved = True

    @workflow.signal
    def reject(self):
        """Signal: Manager rejects expense"""
        self.rejected = True

    @workflow.query
    def get_status(self) -> dict:
        """Query: Get current approval status"""
        return {
            "approved": self.approved,
            "rejected": self.rejected,
            "pending": not (self.approved or self.rejected)
        }
```

### AI Agent Orchestration

```python
from temporalio import workflow, activity
from datetime import timedelta
from typing import List, Dict

@activity.defn
async def call_llm(prompt: str, model: str = "gpt-4") -> str:
    """Activity: Call LLM (automatically retried on transient failures)"""
    from openai import AsyncOpenAI
    client = AsyncOpenAI()

    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@activity.defn
async def search_knowledge_base(query: str) -> List[str]:
    """Activity: RAG retrieval from vector DB"""
    from qdrant_client import QdrantClient

    client = QdrantClient("localhost", port=6333)
    results = client.search(
        collection_name="documents",
        query_text=query,
        limit=5
    )
    return [hit.payload['text'] for hit in results]

@workflow.defn
class ResearchWorkflow:
    def __init__(self):
        self.messages: List[Dict] = []
        self.approved = False

    @workflow.run
    async def run(self, topic: str) -> Dict:
        # Step 1: Generate research questions
        workflow.logger.info(f"Generating questions for {topic}")
        questions = await workflow.execute_activity(
            call_llm,
            args=[f"Generate 5 research questions about {topic}"],
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=workflow.RetryPolicy(
                maximum_attempts=3,
                backoff_coefficient=2.0,
            )
        )

        self.messages.append({"role": "assistant", "content": questions})

        # Step 2: Wait for human approval
        workflow.logger.info("Waiting for approval")
        approved = await workflow.wait_condition(
            lambda: self.approved,
            timeout=timedelta(hours=24)
        )

        if not approved:
            return {"status": "timeout", "questions": questions}

        # Step 3: Research each question with RAG
        answers = []
        for question in questions.split("\n"):
            if not question.strip():
                continue

            # RAG: Search knowledge base
            context = await workflow.execute_activity(
                search_knowledge_base,
                question,
                start_to_close_timeout=timedelta(seconds=10),
            )

            # LLM: Answer with context
            prompt = f"Context: {context}\n\nQuestion: {question}"
            answer = await workflow.execute_activity(
                call_llm,
                args=[prompt],
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=workflow.RetryPolicy(maximum_attempts=3),
            )

            answers.append({"question": question, "answer": answer})

        # Step 4: Synthesize final report
        synthesis_prompt = f"Synthesize these Q&A into a report:\n{answers}"
        report = await workflow.execute_activity(
            call_llm,
            args=[synthesis_prompt],
            start_to_close_timeout=timedelta(minutes=10),
        )

        return {
            "status": "complete",
            "questions": questions,
            "answers": answers,
            "report": report
        }

    @workflow.signal
    def approve(self):
        """Signal: Human approves research questions"""
        self.approved = True

    @workflow.query
    def get_messages(self) -> List[Dict]:
        """Query: Get conversation history"""
        return self.messages
```

## Running Workflows

### Start Temporal Server

```bash
# Using Docker
docker run -p 7233:7233 -p 8233:8233 temporalio/auto-setup:latest

# Or using Temporal CLI
temporal server start-dev
```

### Worker Implementation

```python
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Create worker
    worker = Worker(
        client,
        task_queue="order-processing",
        workflows=[OrderSagaWorkflow],
        activities=[
            reserve_inventory,
            release_inventory,
            charge_payment,
            refund_payment,
            ship_order,
        ],
    )

    # Run worker
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Execute Workflow

```python
from temporalio.client import Client

async def execute_order():
    client = await Client.connect("localhost:7233")

    # Start workflow
    handle = await client.start_workflow(
        OrderSagaWorkflow.run,
        "order_123",
        id=f"order-saga-order_123",
        task_queue="order-processing",
    )

    print(f"Started workflow: {handle.id}")

    # Wait for result
    result = await handle.result()
    print(f"Result: {result}")

    # Or query status without waiting
    status = await handle.query(OrderSagaWorkflow.get_status)
    print(f"Status: {status}")

asyncio.run(execute_order())
```

### Send Signal

```python
# Approve expense from external system
async def approve_expense(workflow_id: str):
    client = await Client.connect("localhost:7233")

    handle = client.get_workflow_handle(workflow_id)

    # Send signal
    await handle.signal(ExpenseApprovalWorkflow.approve)

    print(f"Approved workflow {workflow_id}")
```

## Advanced Patterns

### Child Workflows

```python
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self) -> str:
        # Execute child workflow
        child_result = await workflow.execute_child_workflow(
            ChildWorkflow.run,
            args=["child_input"],
            id="child-workflow-123",
        )

        return f"Parent completed with child result: {child_result}"
```

### Parallel Activities

```python
@workflow.defn
class ParallelProcessingWorkflow:
    @workflow.run
    async def run(self, items: List[str]) -> List[str]:
        # Execute activities in parallel
        results = await asyncio.gather(*[
            workflow.execute_activity(
                process_item,
                item,
                start_to_close_timeout=timedelta(minutes=1),
            )
            for item in items
        ])

        return results
```

### Continue-as-New (Long-Running Workflows)

```python
@workflow.defn
class ContinuousWorkflow:
    @workflow.run
    async def run(self, iteration: int = 0) -> None:
        # Process batch
        await workflow.execute_activity(
            process_batch,
            iteration,
            start_to_close_timeout=timedelta(minutes=5),
        )

        # Wait for next batch
        await workflow.async_sleep(timedelta(hours=1))

        # Continue as new workflow (prevents history from growing unbounded)
        if iteration < 1000:
            workflow.continue_as_new(iteration + 1)
```

## Observability

### OpenTelemetry Integration

```python
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

# All workflow executions are now traced
```

### Workflow Logging

```python
@workflow.defn
class LoggingWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        workflow.logger.info(f"Starting workflow for {order_id}")
        workflow.logger.debug(f"Debug info: {order_id}")
        workflow.logger.warning(f"Warning: {order_id}")
        workflow.logger.error(f"Error: {order_id}")

        return "complete"
```

## Best Practices

### 1. Workflows Must Be Deterministic

```python
# ❌ BAD: Non-deterministic
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> str:
        if random.random() > 0.5:  # Non-deterministic!
            return "A"
        else:
            return "B"

# ✅ GOOD: Deterministic
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self, seed: int) -> str:
        # Use seed from input (deterministic)
        random.seed(seed)
        if random.random() > 0.5:
            return "A"
        else:
            return "B"
```

### 2. Use Activities for Side Effects

```python
# ❌ BAD: Side effects in workflow
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> str:
        # This will fail on replay!
        await aiohttp.get("https://api.example.com")
        return "done"

# ✅ GOOD: Side effects in activity
@activity.defn
async def call_api() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as resp:
            return await resp.text()

@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> str:
        result = await workflow.execute_activity(
            call_api,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return result
```

### 3. Set Appropriate Timeouts

```python
await workflow.execute_activity(
    long_running_task,
    start_to_close_timeout=timedelta(hours=2),  # Total execution time
    schedule_to_close_timeout=timedelta(hours=3),  # Including queue time
    heartbeat_timeout=timedelta(minutes=5),  # Activity must heartbeat
    retry_policy=workflow.RetryPolicy(
        maximum_attempts=3,
        backoff_coefficient=2.0,
        maximum_interval=timedelta(minutes=10),
    )
)
```

### 4. Use Queries for Status Checks

```python
@workflow.defn
class TrackableWorkflow:
    def __init__(self):
        self.progress = 0
        self.status = "pending"

    @workflow.run
    async def run(self) -> str:
        for i in range(10):
            self.progress = (i + 1) * 10
            self.status = f"step_{i+1}"
            await workflow.execute_activity(...)

        self.status = "complete"
        return "done"

    @workflow.query
    def get_progress(self) -> int:
        return self.progress

    @workflow.query
    def get_status(self) -> str:
        return self.status
```

## Troubleshooting

### Workflow Stuck

**Check:**
1. Activity timeouts configured?
2. Worker running and consuming from correct task queue?
3. Check Temporal Web UI for errors

### Non-Deterministic Error

**Cause:** Workflow behavior changed between executions (replay fails)

**Fix:**
1. Use workflow versioning
2. Avoid non-deterministic code
3. Use activities for external calls

### Activity Retry Exhausted

**Cause:** Activity failed too many times

**Fix:**
1. Check activity logs for errors
2. Increase `maximum_attempts` in retry policy
3. Implement DLQ for failed activities

## Related Patterns

- **Saga Pattern**: Distributed transactions with compensation
- **Event Sourcing**: Workflow events as immutable log
- **CQRS**: Separate command workflows from query models
- **Human-in-the-Loop**: Approval workflows with signals
