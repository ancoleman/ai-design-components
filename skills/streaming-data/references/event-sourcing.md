# Event Sourcing Patterns

## Table of Contents
- [Overview](#overview)
- [Core Concepts](#core-concepts)
- [Benefits](#benefits)
- [Challenges](#challenges)
- [Implementation Pattern](#implementation-pattern)
- [Event Schema Evolution](#event-schema-evolution)
- [Snapshots](#snapshots)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)

## Overview

Event sourcing stores all changes to application state as a sequence of immutable events. Instead of storing current state, store the history of state changes.

## Core Concepts

### Event Store
Append-only log of all events (Kafka is ideal for this)

### Event
Immutable fact that something happened

### Aggregate
Entity whose state is derived from events

### Projection
Read model built from event stream

## Benefits

- Complete audit trail
- Temporal queries (state at any point in time)
- Event replay for debugging
- Easy to add new projections
- Natural fit for event-driven architecture

## Challenges

- Event schema evolution
- Eventual consistency
- Increased storage requirements
- Complexity in querying current state

## Implementation Pattern

### Define Events

```typescript
interface Event {
  eventId: string;
  eventType: string;
  aggregateId: string;
  timestamp: number;
  version: number;
  data: any;
}

interface OrderCreatedEvent extends Event {
  eventType: 'OrderCreated';
  data: {
    orderId: string;
    customerId: string;
    items: OrderItem[];
    total: number;
  };
}

interface OrderShippedEvent extends Event {
  eventType: 'OrderShipped';
  data: {
    orderId: string;
    trackingNumber: string;
    shippedAt: number;
  };
}
```

### Event Store (Kafka)

```typescript
class EventStore {
  private producer: Producer;
  private consumer: Consumer;

  async appendEvent(event: Event): Promise<void> {
    await this.producer.send({
      topic: 'events',
      messages: [{
        key: event.aggregateId,
        value: JSON.stringify(event),
        headers: {
          'event-type': event.eventType,
          'event-version': event.version.toString(),
        },
      }],
    });
  }

  async getEvents(aggregateId: string): Promise<Event[]> {
    // Read all events for aggregate from beginning
    const events: Event[] = [];

    await this.consumer.subscribe({
      topics: ['events'],
      fromBeginning: true,
    });

    await this.consumer.run({
      eachMessage: async ({ message }) => {
        const event = JSON.parse(message.value.toString());
        if (event.aggregateId === aggregateId) {
          events.push(event);
        }
      },
    });

    return events;
  }
}
```

### Aggregate

```typescript
class Order {
  private id: string;
  private customerId: string;
  private items: OrderItem[] = [];
  private status: OrderStatus = 'pending';
  private version = 0;
  private uncommittedEvents: Event[] = [];

  static async load(id: string, eventStore: EventStore): Promise<Order> {
    const events = await eventStore.getEvents(id);
    const order = new Order(id);

    for (const event of events) {
      order.applyEvent(event, false);
    }

    return order;
  }

  createOrder(customerId: string, items: OrderItem[]): void {
    const event: OrderCreatedEvent = {
      eventId: uuid(),
      eventType: 'OrderCreated',
      aggregateId: this.id,
      timestamp: Date.now(),
      version: ++this.version,
      data: { orderId: this.id, customerId, items, total: calculateTotal(items) },
    };

    this.applyEvent(event, true);
  }

  shipOrder(trackingNumber: string): void {
    if (this.status !== 'pending') {
      throw new Error('Order already shipped');
    }

    const event: OrderShippedEvent = {
      eventId: uuid(),
      eventType: 'OrderShipped',
      aggregateId: this.id,
      timestamp: Date.now(),
      version: ++this.version,
      data: { orderId: this.id, trackingNumber, shippedAt: Date.now() },
    };

    this.applyEvent(event, true);
  }

  private applyEvent(event: Event, isNew: boolean): void {
    switch (event.eventType) {
      case 'OrderCreated':
        this.customerId = event.data.customerId;
        this.items = event.data.items;
        break;
      case 'OrderShipped':
        this.status = 'shipped';
        break;
    }

    if (isNew) {
      this.uncommittedEvents.push(event);
    }
  }

  async save(eventStore: EventStore): Promise<void> {
    for (const event of this.uncommittedEvents) {
      await eventStore.appendEvent(event);
    }
    this.uncommittedEvents = [];
  }
}
```

### Projection (Read Model)

```typescript
class OrderProjection {
  private db: Database;

  async build(eventStream: EventStream): Promise<void> {
    await eventStream.subscribe(['events'], async (event: Event) => {
      switch (event.eventType) {
        case 'OrderCreated':
          await this.db.orders.insert({
            id: event.data.orderId,
            customerId: event.data.customerId,
            total: event.data.total,
            status: 'pending',
          });
          break;

        case 'OrderShipped':
          await this.db.orders.update(
            { id: event.data.orderId },
            { status: 'shipped', trackingNumber: event.data.trackingNumber }
          );
          break;
      }
    });
  }

  async getOrder(orderId: string): Promise<Order> {
    return await this.db.orders.findOne({ id: orderId });
  }
}
```

## Event Schema Evolution

### Versioning Strategy

```typescript
interface EventV1 {
  version: 1;
  eventType: 'OrderCreated';
  data: {
    orderId: string;
    customerId: string;
  };
}

interface EventV2 {
  version: 2;
  eventType: 'OrderCreated';
  data: {
    orderId: string;
    customerId: string;
    customerEmail: string; // New field
  };
}

function migrateEvent(event: Event): EventV2 {
  if (event.version === 1) {
    return {
      ...event,
      version: 2,
      data: {
        ...event.data,
        customerEmail: 'unknown@example.com', // Default value
      },
    };
  }
  return event;
}
```

## Snapshots

For aggregates with many events, use snapshots:

```typescript
class SnapshotStore {
  async saveSnapshot(aggregateId: string, state: any, version: number): Promise<void> {
    await this.db.snapshots.upsert({
      aggregateId,
      state: JSON.stringify(state),
      version,
      createdAt: Date.now(),
    });
  }

  async getSnapshot(aggregateId: string): Promise<Snapshot | null> {
    return await this.db.snapshots.findOne({ aggregateId });
  }
}

class Order {
  static async load(id: string, eventStore: EventStore, snapshotStore: SnapshotStore): Promise<Order> {
    const snapshot = await snapshotStore.getSnapshot(id);

    let order: Order;
    let fromVersion = 0;

    if (snapshot) {
      order = Order.fromSnapshot(snapshot);
      fromVersion = snapshot.version;
    } else {
      order = new Order(id);
    }

    // Load events after snapshot
    const events = await eventStore.getEvents(id, fromVersion);
    for (const event of events) {
      order.applyEvent(event, false);
    }

    return order;
  }
}
```

## Best Practices

1. **Immutable events**: Never modify published events
2. **Idempotent projections**: Handle duplicate events
3. **Event versioning**: Plan for schema evolution
4. **Snapshots**: Use for aggregates with many events
5. **Upcasting**: Convert old events to new schema
6. **Correlation IDs**: Track causation across events

## Conclusion

Event sourcing provides a complete audit trail and enables temporal queries. Use Kafka as the event store, design for schema evolution, and implement snapshots for performance.
