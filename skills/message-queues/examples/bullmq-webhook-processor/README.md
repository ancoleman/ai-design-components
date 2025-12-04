# BullMQ Webhook Processor Example

Resilient webhook processing system using BullMQ with retry logic, dead letter queue, and monitoring.

## Use Case

Process incoming webhooks asynchronously with:
- Immediate HTTP 200 response (webhook doesn't timeout)
- Retry failed webhooks with exponential backoff
- Dead letter queue for permanently failed webhooks
- Rate limiting to external APIs
- Monitoring dashboard

## Architecture

```
Webhook POST → Express API → BullMQ Queue → Worker → External API
                   ↓                              ↓
               200 OK (instant)            Process async
```

## Files

```
bullmq-webhook-processor/
├── src/
│   ├── server.ts            # Express API
│   ├── queues/
│   │   └── webhookQueue.ts  # Queue setup
│   ├── workers/
│   │   └── webhookWorker.ts # Job processor
│   └── processors/
│       └── stripeProcessor.ts
├── package.json
└── .env.example
```

## Quick Start

```bash
npm install
docker run -p 6379:6379 redis  # Start Redis
npm run dev
```

## Implementation

### Queue Setup

```typescript
// queues/webhookQueue.ts
import { Queue } from 'bullmq';

export const webhookQueue = new Queue('webhooks', {
  connection: { host: 'localhost', port: 6379 },
  defaultJobOptions: {
    attempts: 5,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: { age: 86400 },  // Keep 24 hours
    removeOnFail: { age: 604800 },     // Keep 7 days
  },
});
```

### Worker

```typescript
// workers/webhookWorker.ts
import { Worker } from 'bullmq';

const worker = new Worker('webhooks', async (job) => {
  const { provider, event } = job.data;

  console.log(`Processing ${provider} webhook:`, job.id);

  switch (provider) {
    case 'stripe':
      return await processStripeWebhook(event);
    case 'github':
      return await processGitHubWebhook(event);
    default:
      throw new Error(`Unknown provider: ${provider}`);
  }
}, {
  connection: { host: 'localhost', port: 6379 },
  concurrency: 10,
  limiter: { max: 100, duration: 60000 },  // 100 jobs/min
});

worker.on('completed', (job) => {
  console.log(`✓ Job ${job.id} completed`);
});

worker.on('failed', (job, err) => {
  console.error(`✗ Job ${job.id} failed:`, err.message);
});
```

### API Endpoint

```typescript
// server.ts
import express from 'express';
import { webhookQueue } from './queues/webhookQueue';

const app = express();
app.use(express.json());

app.post('/webhooks/stripe', async (req, res) => {
  // Validate webhook signature
  const signature = req.headers['stripe-signature'];
  // ... validation logic ...

  // Queue for async processing
  await webhookQueue.add('stripe-event', {
    provider: 'stripe',
    event: req.body,
    receivedAt: new Date().toISOString(),
  }, {
    jobId: req.body.id,  // Idempotency (prevent duplicates)
  });

  // Immediate response
  res.json({ received: true });
});

app.listen(3000);
```

## Features

- Automatic retries with exponential backoff
- Job deduplication via jobId
- Progress tracking
- Failed job monitoring
- Bull Board dashboard integration

## Monitoring

```typescript
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

createBullBoard({
  queues: [new BullMQAdapter(webhookQueue)],
  serverAdapter,
});

app.use('/admin/queues', serverAdapter.getRouter());
```

Access: http://localhost:3000/admin/queues
