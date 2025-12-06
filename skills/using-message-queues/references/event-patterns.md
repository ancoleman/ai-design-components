# Event Patterns - Event Sourcing, CQRS, Outbox

Advanced event-driven architecture patterns for building scalable, reliable systems.


## Table of Contents

- [Event Sourcing](#event-sourcing)
  - [Implementation](#implementation)
  - [Persistence with Kafka](#persistence-with-kafka)
- [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
  - [Implementation](#implementation)
- [Outbox Pattern](#outbox-pattern)
  - [Implementation](#implementation)
  - [Outbox Table Schema](#outbox-table-schema)
- [Event Versioning](#event-versioning)
  - [Upcasting Pattern](#upcasting-pattern)
- [Saga Pattern (Distributed Transactions)](#saga-pattern-distributed-transactions)
  - [Event-Based Saga (Choreography)](#event-based-saga-choreography)
- [Best Practices](#best-practices)
  - [1. Event Naming Convention](#1-event-naming-convention)
  - [2. Event Schema Evolution](#2-event-schema-evolution)
  - [3. Idempotent Event Handlers](#3-idempotent-event-handlers)
  - [4. Event Metadata](#4-event-metadata)
- [Related Patterns](#related-patterns)

## Event Sourcing

**Pattern:** Store state changes as immutable events instead of current state.

**Benefits:**
- Complete audit log (every change recorded)
- Time travel (replay to any point)
- Event replay for new projections
- Natural fit for event-driven systems

**Trade-offs:**
- More complex than CRUD
- Requires event versioning strategy
- Eventual consistency

### Implementation

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime
import json

@dataclass
class Event:
    """Base event"""
    event_id: str
    event_type: str
    aggregate_id: str
    timestamp: datetime
    version: int
    data: dict

@dataclass
class OrderCreated(Event):
    event_type: str = "order.created.v1"

@dataclass
class ItemAdded(Event):
    event_type: str = "item.added.v1"

@dataclass
class OrderSubmitted(Event):
    event_type: str = "order.submitted.v1"

class OrderAggregate:
    """Event-sourced aggregate"""
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.events: List[Event] = []
        self.version = 0

        # State (derived from events)
        self.status = "draft"
        self.items = []
        self.total = 0.0

    def create_order(self, customer_id: str):
        """Command: Create order"""
        event = OrderCreated(
            event_id=str(uuid.uuid4()),
            event_type="order.created.v1",
            aggregate_id=self.order_id,
            timestamp=datetime.utcnow(),
            version=self.version + 1,
            data={"customer_id": customer_id}
        )
        self.apply(event)
        self.events.append(event)

    def add_item(self, item_id: str, quantity: int, price: float):
        """Command: Add item"""
        if self.status != "draft":
            raise ValueError("Can only add items to draft orders")

        event = ItemAdded(
            event_id=str(uuid.uuid4()),
            event_type="item.added.v1",
            aggregate_id=self.order_id,
            timestamp=datetime.utcnow(),
            version=self.version + 1,
            data={"item_id": item_id, "quantity": quantity, "price": price}
        )
        self.apply(event)
        self.events.append(event)

    def submit_order(self):
        """Command: Submit order"""
        if not self.items:
            raise ValueError("Cannot submit empty order")

        event = OrderSubmitted(
            event_id=str(uuid.uuid4()),
            event_type="order.submitted.v1",
            aggregate_id=self.order_id,
            timestamp=datetime.utcnow(),
            version=self.version + 1,
            data={"total": self.total}
        )
        self.apply(event)
        self.events.append(event)

    def apply(self, event: Event):
        """Apply event to update state"""
        if event.event_type == "order.created.v1":
            self.status = "draft"
        elif event.event_type == "item.added.v1":
            self.items.append(event.data)
            self.total += event.data['price'] * event.data['quantity']
        elif event.event_type == "order.submitted.v1":
            self.status = "submitted"

        self.version = event.version

    @classmethod
    def from_events(cls, order_id: str, events: List[Event]):
        """Rebuild aggregate from events (event replay)"""
        aggregate = cls(order_id)
        for event in events:
            aggregate.apply(event)
            aggregate.events.append(event)
        return aggregate
```

### Persistence with Kafka

```python
from confluent_kafka import Producer, Consumer
import json
import uuid

class EventStore:
    """Kafka-based event store"""
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': f'event-replay-{uuid.uuid4()}',
            'auto.offset.reset': 'earliest'
        })

    def save_events(self, aggregate_id: str, events: List[Event]):
        """Append events to stream"""
        for event in events:
            self.producer.produce(
                topic='order-events',
                key=aggregate_id,  # All events for same aggregate in same partition
                value=json.dumps({
                    'event_id': event.event_id,
                    'event_type': event.event_type,
                    'aggregate_id': event.aggregate_id,
                    'timestamp': event.timestamp.isoformat(),
                    'version': event.version,
                    'data': event.data
                })
            )
        self.producer.flush()

    def load_events(self, aggregate_id: str) -> List[Event]:
        """Load all events for aggregate (event replay)"""
        self.consumer.subscribe(['order-events'])

        events = []
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                break

            if msg.key().decode() == aggregate_id:
                event_data = json.loads(msg.value().decode())
                events.append(Event(
                    event_id=event_data['event_id'],
                    event_type=event_data['event_type'],
                    aggregate_id=event_data['aggregate_id'],
                    timestamp=datetime.fromisoformat(event_data['timestamp']),
                    version=event_data['version'],
                    data=event_data['data']
                ))

        return sorted(events, key=lambda e: e.version)
```

## CQRS (Command Query Responsibility Segregation)

**Pattern:** Separate write model (commands) from read model (queries).

**Benefits:**
- Optimize read and write independently
- Scale read and write separately
- Multiple read models from same events
- Complex queries without impacting writes

**Trade-offs:**
- Eventual consistency between models
- More complex than single model
- Need to synchronize models

### Implementation

```python
# WRITE MODEL (Command Side)
class OrderCommandHandler:
    """Handle write operations"""
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def create_order(self, order_id: str, customer_id: str):
        """Command: Create order"""
        aggregate = OrderAggregate(order_id)
        aggregate.create_order(customer_id)

        # Save events
        self.event_store.save_events(order_id, aggregate.events)

    def add_item(self, order_id: str, item_id: str, quantity: int, price: float):
        """Command: Add item"""
        # Load events and rebuild aggregate
        events = self.event_store.load_events(order_id)
        aggregate = OrderAggregate.from_events(order_id, events)

        # Execute command
        aggregate.add_item(item_id, quantity, price)

        # Save new events
        self.event_store.save_events(order_id, aggregate.events[-1:])


# READ MODEL (Query Side)
class OrderReadModel:
    """Optimized for queries"""
    def __init__(self, db):
        self.db = db  # Could be PostgreSQL, MongoDB, etc.

    def get_order(self, order_id: str) -> dict:
        """Query: Get order details"""
        return self.db.query("SELECT * FROM orders WHERE id = ?", order_id)

    def get_customer_orders(self, customer_id: str) -> List[dict]:
        """Query: Get all orders for customer"""
        return self.db.query("SELECT * FROM orders WHERE customer_id = ?", customer_id)

    def get_order_summary(self, order_id: str) -> dict:
        """Query: Get order summary with items"""
        return self.db.query("""
            SELECT o.*, COUNT(i.id) as item_count, SUM(i.total) as total
            FROM orders o
            LEFT JOIN order_items i ON o.id = i.order_id
            WHERE o.id = ?
            GROUP BY o.id
        """, order_id)


# PROJECTOR (Sync write model → read model)
class OrderProjector:
    """Project events to read model"""
    def __init__(self, read_model: OrderReadModel):
        self.read_model = read_model

    def handle_event(self, event: Event):
        """Update read model based on event"""
        if event.event_type == "order.created.v1":
            self.read_model.db.execute(
                "INSERT INTO orders (id, customer_id, status) VALUES (?, ?, ?)",
                event.aggregate_id,
                event.data['customer_id'],
                'draft'
            )

        elif event.event_type == "item.added.v1":
            self.read_model.db.execute(
                "INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (?, ?, ?, ?)",
                event.aggregate_id,
                event.data['item_id'],
                event.data['quantity'],
                event.data['price']
            )

        elif event.event_type == "order.submitted.v1":
            self.read_model.db.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                'submitted',
                event.aggregate_id
            )

    def project_all_events(self, stream: str):
        """Rebuild read model from scratch (event replay)"""
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'projector',
            'auto.offset.reset': 'earliest'
        })
        consumer.subscribe([stream])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                break

            event_data = json.loads(msg.value().decode())
            event = Event(**event_data)
            self.handle_event(event)
```

## Outbox Pattern

**Pattern:** Ensure database writes and event publishing are atomic (no partial failures).

**Problem:**
```python
# ❌ NOT ATOMIC
db.insert_order(order)  # Succeeds
kafka.publish(event)     # FAILS → inconsistent state!
```

**Solution:** Write events to outbox table in same transaction, then publish asynchronously.

### Implementation

```python
import psycopg2
from psycopg2.extras import Json
from confluent_kafka import Producer
import json
import time

class OutboxPattern:
    """Transactional outbox pattern"""
    def __init__(self, db_conn, kafka_producer: Producer):
        self.db = db_conn
        self.producer = kafka_producer

    def create_order_with_event(self, order_id: str, customer_id: str):
        """Create order and event atomically"""
        cursor = self.db.cursor()

        try:
            # Begin transaction
            cursor.execute("BEGIN")

            # Insert order
            cursor.execute(
                "INSERT INTO orders (id, customer_id, status) VALUES (%s, %s, %s)",
                (order_id, customer_id, 'draft')
            )

            # Insert event to outbox (same transaction)
            event = {
                'event_type': 'order.created.v1',
                'aggregate_id': order_id,
                'timestamp': datetime.utcnow().isoformat(),
                'data': {'customer_id': customer_id}
            }

            cursor.execute(
                "INSERT INTO outbox (id, event_type, aggregate_id, payload) VALUES (%s, %s, %s, %s)",
                (str(uuid.uuid4()), event['event_type'], order_id, Json(event))
            )

            # Commit transaction (both writes succeed or both fail)
            cursor.execute("COMMIT")

        except Exception as e:
            cursor.execute("ROLLBACK")
            raise

    def publish_outbox_events(self):
        """Background worker: Publish events from outbox"""
        cursor = self.db.cursor()

        while True:
            # Fetch unpublished events
            cursor.execute(
                "SELECT id, aggregate_id, payload FROM outbox WHERE published = false ORDER BY created_at LIMIT 100"
            )

            events = cursor.fetchall()

            for event_id, aggregate_id, payload in events:
                try:
                    # Publish to Kafka
                    self.producer.produce(
                        topic='order-events',
                        key=aggregate_id,
                        value=json.dumps(payload)
                    )
                    self.producer.flush()

                    # Mark as published
                    cursor.execute(
                        "UPDATE outbox SET published = true WHERE id = %s",
                        (event_id,)
                    )
                    self.db.commit()

                except Exception as e:
                    print(f"Failed to publish {event_id}: {e}")
                    # Will retry on next iteration

            time.sleep(1)  # Poll every second
```

### Outbox Table Schema

```sql
CREATE TABLE outbox (
    id UUID PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    published BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    INDEX idx_unpublished (published, created_at)
);

-- Clean up old published events periodically
DELETE FROM outbox WHERE published = true AND published_at < NOW() - INTERVAL '7 days';
```

## Event Versioning

**Challenge:** Events are immutable but business logic evolves.

### Upcasting Pattern

```python
class EventUpcaster:
    """Convert old event versions to new versions"""
    def upcast(self, event: dict) -> dict:
        """Convert event to latest version"""
        event_type = event['event_type']

        if event_type == "order.created.v1":
            # v1 → v2: Add currency field
            return {
                **event,
                'event_type': 'order.created.v2',
                'data': {
                    **event['data'],
                    'currency': 'USD'  # Default for old events
                }
            }

        elif event_type == "item.added.v1":
            # v1 → v2: Add discount field
            return {
                **event,
                'event_type': 'item.added.v2',
                'data': {
                    **event['data'],
                    'discount': 0.0  # Default for old events
                }
            }

        return event  # Already latest version

    def load_events_with_upcasting(self, aggregate_id: str) -> List[Event]:
        """Load and upcast events"""
        raw_events = self.event_store.load_events(aggregate_id)
        upcasted = [self.upcast(e) for e in raw_events]
        return [Event(**e) for e in upcasted]
```

## Saga Pattern (Distributed Transactions)

**Pattern:** Coordinate transactions across services with compensation.

See `temporal-workflows.md` for comprehensive Temporal saga implementation.

### Event-Based Saga (Choreography)

```python
# Order Service: Emit event
kafka.publish('order-events', {
    'event_type': 'order.created',
    'order_id': 'ord_123',
    'customer_id': 'cus_456'
})

# Inventory Service: Listen and react
@kafka_consumer('order-events')
def handle_order_created(event):
    try:
        reserve_inventory(event['order_id'])
        kafka.publish('inventory-events', {
            'event_type': 'inventory.reserved',
            'order_id': event['order_id']
        })
    except InsufficientStockError:
        kafka.publish('inventory-events', {
            'event_type': 'inventory.reservation.failed',
            'order_id': event['order_id']
        })

# Payment Service: Listen and react
@kafka_consumer('inventory-events')
def handle_inventory_reserved(event):
    if event['event_type'] == 'inventory.reserved':
        charge_payment(event['order_id'])
        kafka.publish('payment-events', {
            'event_type': 'payment.charged',
            'order_id': event['order_id']
        })

# Order Service: Listen for completion or failure
@kafka_consumer('payment-events')
def handle_payment_charged(event):
    if event['event_type'] == 'payment.charged':
        complete_order(event['order_id'])
    elif event['event_type'] == 'payment.failed':
        # Compensate: Release inventory
        kafka.publish('compensation-events', {
            'event_type': 'inventory.release.requested',
            'order_id': event['order_id']
        })
```

## Best Practices

### 1. Event Naming Convention

```
Domain.Entity.Action.Version

Examples:
- order.created.v1
- order.item.added.v2
- payment.charged.v1
```

### 2. Event Schema Evolution

```python
# Include schema version in event
event = {
    'event_type': 'order.created.v2',
    'schema_version': 2,
    'data': {...}
}

# Handle multiple versions
def handle_order_created(event):
    if event['schema_version'] == 1:
        # Handle v1 schema
        pass
    elif event['schema_version'] == 2:
        # Handle v2 schema
        pass
```

### 3. Idempotent Event Handlers

```python
@event_handler('order.created')
def handle_order_created(event):
    event_id = event['event_id']

    # Check if already processed
    if redis.exists(f'processed:{event_id}'):
        return  # Already handled

    # Process event
    create_order_projection(event)

    # Mark as processed
    redis.setex(f'processed:{event_id}', 86400, '1')
```

### 4. Event Metadata

```python
event = {
    'event_type': 'order.created.v1',
    'event_id': str(uuid.uuid4()),
    'timestamp': datetime.utcnow().isoformat(),
    'data': {...},
    'metadata': {
        'correlation_id': 'request-123',  # Trace across services
        'causation_id': 'event-456',  # Which event caused this
        'user_id': 'user-789',  # Who triggered
        'service': 'order-service',  # Which service
        'version': '1.2.3'  # Service version
    }
}
```

## Related Patterns

- **Event Sourcing**: State as event log
- **CQRS**: Separate read/write models
- **Outbox**: Atomic writes + events
- **Saga**: Distributed transactions with compensation
- **Event Versioning**: Handle schema evolution
