# Event Sourcing and CQRS

## Table of Contents

1. [Event Sourcing](#event-sourcing)
2. [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
3. [Benefits and Trade-offs](#benefits-and-trade-offs)

## Event Sourcing

### Concept

Store state changes as immutable events rather than current state.

### Event Store Implementation

```python
from datetime import datetime
from typing import List, Dict

class Event:
    def __init__(self, aggregate_id, event_type, data, version):
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.data = data
        self.version = version
        self.timestamp = datetime.utcnow()

class EventStore:
    def __init__(self):
        self.events = {}  # aggregate_id -> [events]
    
    def append(self, aggregate_id, event):
        if aggregate_id not in self.events:
            self.events[aggregate_id] = []
        self.events[aggregate_id].append(event)
    
    def get_events(self, aggregate_id, from_version=0):
        events = self.events.get(aggregate_id, [])
        return [e for e in events if e.version >= from_version]
    
    def replay(self, aggregate_id):
        events = self.get_events(aggregate_id)
        state = {}
        for event in events:
            state = self.apply_event(state, event)
        return state
    
    def apply_event(self, state, event):
        if event.event_type == 'AccountCreated':
            state['balance'] = event.data['initial_balance']
        elif event.event_type == 'MoneyDeposited':
            state['balance'] += event.data['amount']
        elif event.event_type == 'MoneyWithdrawn':
            state['balance'] -= event.data['amount']
        return state

# Usage
event_store = EventStore()

# Create account
event_store.append('account-123', Event(
    aggregate_id='account-123',
    event_type='AccountCreated',
    data={'initial_balance': 1000},
    version=1
))

# Deposit
event_store.append('account-123', Event(
    aggregate_id='account-123',
    event_type='MoneyDeposited',
    data={'amount': 500},
    version=2
))

# Get current state by replaying events
current_state = event_store.replay('account-123')
print(current_state)  # {'balance': 1500}
```

### Snapshots

```python
class EventStoreWithSnapshots:
    def __init__(self, snapshot_interval=100):
        self.events = {}
        self.snapshots = {}
        self.snapshot_interval = snapshot_interval
    
    def append(self, aggregate_id, event):
        if aggregate_id not in self.events:
            self.events[aggregate_id] = []
        
        self.events[aggregate_id].append(event)
        
        # Create snapshot every N events
        if len(self.events[aggregate_id]) % self.snapshot_interval == 0:
            self.create_snapshot(aggregate_id)
    
    def create_snapshot(self, aggregate_id):
        state = self.replay(aggregate_id)
        version = len(self.events[aggregate_id])
        self.snapshots[aggregate_id] = {
            'state': state,
            'version': version
        }
    
    def replay(self, aggregate_id):
        snapshot = self.snapshots.get(aggregate_id)
        
        if snapshot:
            state = snapshot['state']
            from_version = snapshot['version']
        else:
            state = {}
            from_version = 0
        
        events = self.get_events(aggregate_id, from_version)
        for event in events:
            state = self.apply_event(state, event)
        
        return state
```

## CQRS (Command Query Responsibility Segregation)

### Concept

Separate read and write models for optimized performance.

### Write Model

```python
class OrderWriteModel:
    def __init__(self, db, event_bus):
        self.db = db
        self.event_bus = event_bus
    
    def create_order(self, command):
        # Validate
        if self.db.order_exists(command['order_id']):
            raise ValueError("Order already exists")
        
        # Write to normalized tables
        self.db.insert_order({
            'order_id': command['order_id'],
            'customer_id': command['customer_id'],
            'status': 'pending'
        })
        
        for item in command['items']:
            self.db.insert_order_item({
                'order_id': command['order_id'],
                'item_id': item['id'],
                'quantity': item['qty']
            })
        
        # Publish event
        self.event_bus.publish({
            'type': 'OrderCreated',
            'order_id': command['order_id'],
            'customer_id': command['customer_id'],
            'items': command['items']
        })
```

### Read Model

```python
class OrderReadModel:
    def __init__(self, cache, search_index):
        self.cache = cache  # Redis
        self.search_index = search_index  # Elasticsearch
    
    def get_order(self, order_id):
        # Try cache
        cached = self.cache.get(f"order:{order_id}")
        if cached:
            return cached
        
        # Fallback to search index
        result = self.search_index.get('orders', order_id)
        self.cache.set(f"order:{order_id}", result, expire=3600)
        return result
    
    def search_orders(self, customer_id):
        return self.search_index.search('orders', {
            'query': {'term': {'customer_id': customer_id}},
            'sort': [{'created_at': 'desc'}]
        })
```

### Event Handler (Update Read Model)

```python
class OrderReadModelUpdater:
    def __init__(self, read_model):
        self.read_model = read_model
    
    def handle_order_created(self, event):
        # Update Elasticsearch
        order_doc = {
            'order_id': event['order_id'],
            'customer_id': event['customer_id'],
            'items': event['items'],
            'total_items': len(event['items']),
            'created_at': datetime.utcnow()
        }
        self.read_model.search_index.index('orders', event['order_id'], order_doc)
        
        # Update cache
        self.read_model.cache.set(
            f"order:{event['order_id']}",
            order_doc,
            expire=3600
        )
```

## Benefits and Trade-offs

**Event Sourcing Benefits:**
- Complete audit trail
- Time travel (replay to any point)
- Debugging (replay events)
- Event-driven architecture

**Event Sourcing Trade-offs:**
- Query complexity (must replay)
- Snapshot management
- Event schema evolution

**CQRS Benefits:**
- Optimized read/write models
- Independent scaling
- Multiple read models

**CQRS Trade-offs:**
- Eventual consistency (lag between write and read)
- Complexity (two models)
- Data synchronization
