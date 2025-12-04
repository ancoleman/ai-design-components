# Temporal Order Saga Example

Distributed saga pattern for order processing using Temporal workflow orchestration.

## Use Case

E-commerce order processing with multiple steps that need coordination:
1. Reserve inventory
2. Charge payment
3. Create shipment
4. Send confirmation

If any step fails, compensating transactions rollback previous steps.

## What is Temporal?

Durable workflow engine that persists execution state. If worker crashes, workflow resumes from last checkpoint.

## Files

```
temporal-order-saga/
├── workflows/
│   └── orderWorkflow.ts     # Order saga workflow
├── activities/
│   ├── inventory.ts         # Inventory operations
│   ├── payment.ts           # Payment operations
│   └── shipping.ts          # Shipping operations
├── worker.ts                # Temporal worker
├── client.ts                # Start workflow
└── package.json
```

## Quick Start

```bash
# Install Temporal CLI
brew install temporal

# Start Temporal server
temporal server start-dev

# Install dependencies
npm install

# Run worker
npm run worker

# Execute workflow (separate terminal)
npm run start-order
```

## Workflow Implementation

```typescript
// workflows/orderWorkflow.ts
import { proxyActivities } from '@temporalio/workflow';
import * as activities from '../activities';

const { reserveInventory, chargePayment, createShipment, sendConfirmation } =
  proxyActivities<typeof activities>({
    startToCloseTimeout: '1 minute',
  });

export async function orderWorkflow(orderId: string): Promise<string> {
  let inventoryReserved = false;
  let paymentCharged = false;
  let shipmentCreated = false;

  try {
    // Step 1: Reserve inventory
    await reserveInventory(orderId);
    inventoryReserved = true;

    // Step 2: Charge payment
    await chargePayment(orderId);
    paymentCharged = true;

    // Step 3: Create shipment
    await createShipment(orderId);
    shipmentCreated = true;

    // Step 4: Send confirmation
    await sendConfirmation(orderId);

    return 'Order completed successfully';

  } catch (error) {
    // Compensating transactions (rollback)
    if (shipmentCreated) {
      await cancelShipment(orderId);
    }
    if (paymentCharged) {
      await refundPayment(orderId);
    }
    if (inventoryReserved) {
      await releaseInventory(orderId);
    }

    throw error;
  }
}
```

## Activities (Actual Work)

```typescript
// activities/inventory.ts
export async function reserveInventory(orderId: string): Promise<void> {
  const order = await db.order.findUnique({ where: { id: orderId } });

  for (const item of order.items) {
    const updated = await db.product.update({
      where: { id: item.productId, stock: { gte: item.quantity } },
      data: { stock: { decrement: item.quantity } },
    });

    if (!updated) {
      throw new Error(`Insufficient stock for product ${item.productId}`);
    }
  }
}

export async function releaseInventory(orderId: string): Promise<void> {
  const order = await db.order.findUnique({ where: { id: orderId } });

  for (const item of order.items) {
    await db.product.update({
      where: { id: item.productId },
      data: { stock: { increment: item.quantity } },
    });
  }
}

// activities/payment.ts
export async function chargePayment(orderId: string): Promise<void> {
  const order = await db.order.findUnique({ where: { id: orderId } });

  const charge = await stripe.charges.create({
    amount: order.total * 100,
    currency: 'usd',
    source: order.paymentMethodId,
  });

  await db.order.update({
    where: { id: orderId },
    data: { stripeChargeId: charge.id },
  });
}

export async function refundPayment(orderId: string): Promise<void> {
  const order = await db.order.findUnique({ where: { id: orderId } });

  await stripe.refunds.create({
    charge: order.stripeChargeId,
  });
}
```

## Starting Workflow

```typescript
// client.ts
import { Client } from '@temporalio/client';
import { orderWorkflow } from './workflows/orderWorkflow';

const client = new Client();

async function processOrder(orderId: string) {
  const handle = await client.workflow.start(orderWorkflow, {
    taskQueue: 'orders',
    workflowId: `order-${orderId}`,  // Unique workflow ID
    args: [orderId],
  });

  console.log(`Started workflow: ${handle.workflowId}`);

  // Wait for result
  const result = await handle.result();
  console.log('Workflow result:', result);
}

processOrder('order-123');
```

## Error Handling Benefits

**Without Temporal (fragile):**
- Worker crashes mid-process → orphaned payment charge
- Network error → need manual cleanup
- Hard to track saga state

**With Temporal:**
- Automatic retry on failures
- Guaranteed compensation execution
- Full workflow history
- Crash recovery (resume from checkpoint)

## Monitoring

Access Temporal Web UI: http://localhost:8233

View:
- Workflow execution history
- Failed workflows
- Retry attempts
- Execution timeline
- Event history

## When to Use Temporal vs Celery

**Use Temporal when:**
- Multi-step workflows with rollback logic
- Long-running processes (hours/days)
- Need execution history and replay
- Critical workflows requiring guarantees

**Use Celery when:**
- Simple background jobs
- No complex orchestration needed
- Python-only ecosystem
- Lower infrastructure complexity
