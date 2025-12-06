# Saga Pattern

## Table of Contents

1. [Overview](#overview)
2. [Choreography vs Orchestration](#choreography-vs-orchestration)
3. [Best Practices](#best-practices)

## Overview

Manage distributed transactions across microservices using compensating transactions instead of distributed 2PC.

## Choreography vs Orchestration

### Choreography (Event-Based)

Services react to events published by other services.

```
Order Service → OrderCreated event
   ↓
Payment Service listens → PaymentProcessed event
   ↓
Inventory Service listens → InventoryReserved event
   ↓
Shipping Service listens → OrderShipped event

If Payment fails:
   Payment Service → PaymentFailed event
   Order Service listens → CancelOrder (compensating action)
```

**Implementation:**

```python
# Event bus (Kafka, RabbitMQ, etc.)
class EventBus:
    def publish(self, event_type, data):
        # Publish event to message queue
        pass
    
    def subscribe(self, event_type, handler):
        # Subscribe handler to event type
        pass

# Order Service
class OrderService:
    def create_order(self, order_data):
        order = self.save_order(order_data)
        event_bus.publish('OrderCreated', {'order_id': order.id})
        return order
    
    def handle_payment_failed(self, event):
        order_id = event['order_id']
        self.cancel_order(order_id)
        event_bus.publish('OrderCancelled', {'order_id': order_id})

event_bus.subscribe('PaymentFailed', order_service.handle_payment_failed)

# Payment Service
class PaymentService:
    def handle_order_created(self, event):
        order_id = event['order_id']
        try:
            payment = self.process_payment(order_id)
            event_bus.publish('PaymentProcessed', {'order_id': order_id})
        except Exception:
            event_bus.publish('PaymentFailed', {'order_id': order_id})

event_bus.subscribe('OrderCreated', payment_service.handle_order_created)
```

### Orchestration (Coordinator-Based)

Central coordinator manages saga flow.

```
Saga Orchestrator:
1. Call Order Service → create order
2. Call Payment Service → process payment
3. Call Inventory Service → reserve inventory
4. Call Shipping Service → ship order

If step 3 fails:
  Compensate step 2: Refund payment
  Compensate step 1: Cancel order
```

**Implementation:**

```python
class SagaOrchestrator:
    def __init__(self):
        self.steps = []
        self.compensations = []
    
    def add_step(self, action, compensation):
        self.steps.append(action)
        self.compensations.append(compensation)
    
    def execute(self, context):
        executed_steps = []
        
        try:
            for step in self.steps:
                result = step(context)
                executed_steps.append(step)
                context.update(result)
            
            return {'status': 'success', 'context': context}
        
        except Exception as e:
            # Rollback executed steps
            for step in reversed(executed_steps):
                idx = self.steps.index(step)
                compensation = self.compensations[idx]
                try:
                    compensation(context)
                except Exception as comp_error:
                    # Log compensation failure
                    print(f"Compensation failed: {comp_error}")
            
            return {'status': 'failed', 'error': str(e)}

# Usage
saga = SagaOrchestrator()

saga.add_step(
    action=lambda ctx: order_service.create_order(ctx['order_data']),
    compensation=lambda ctx: order_service.cancel_order(ctx['order_id'])
)

saga.add_step(
    action=lambda ctx: payment_service.process_payment(ctx['order_id']),
    compensation=lambda ctx: payment_service.refund(ctx['payment_id'])
)

saga.add_step(
    action=lambda ctx: inventory_service.reserve(ctx['product_id']),
    compensation=lambda ctx: inventory_service.release(ctx['reservation_id'])
)

result = saga.execute({'order_data': {...}})
```

## Best Practices

**Idempotency:** Ensure steps can be safely retried
**Timeouts:** Set timeouts for each step
**Monitoring:** Track saga progress and failures
**Compensation Logic:** Design reversible operations
