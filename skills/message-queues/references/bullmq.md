# BullMQ Reference Guide

Modern Node.js/TypeScript job queue built on Redis with advanced features like delayed jobs, rate limiting, and job prioritization.

## When to Use BullMQ

- TypeScript/Node.js ecosystem
- Need advanced scheduling (cron, delayed, repeatable jobs)
- Rate limiting per queue
- Job prioritization
- Horizontal scaling with workers

## Installation

```bash
npm install bullmq ioredis
```

## Core Concepts

### Queue, Worker, Job

```typescript
import { Queue, Worker } from 'bullmq';

// 1. Queue (producer)
const emailQueue = new Queue('emails', {
  connection: { host: 'localhost', port: 6379 }
});

// 2. Add job
await emailQueue.add('send-welcome', {
  to: 'user@example.com',
  template: 'welcome',
});

// 3. Worker (consumer)
const worker = new Worker('emails', async (job) => {
  console.log(`Processing job ${job.id}:`, job.data);

  // Simulate email sending
  await sendEmail(job.data.to, job.data.template);

  return { sent: true };
}, { connection: { host: 'localhost', port: 6379 } });
```

## Advanced Features

### Delayed Jobs

```typescript
// Process in 1 hour
await queue.add('reminder', { userId: 123 }, {
  delay: 3600000,  // 1 hour in ms
});

// Process at specific time
await queue.add('scheduled-report', { reportId: 456 }, {
  delay: new Date('2025-12-04T09:00:00').getTime() - Date.now(),
});
```

### Repeatable Jobs (Cron)

```typescript
import { Queue } from 'bullmq';

await queue.add('daily-report', {}, {
  repeat: {
    pattern: '0 9 * * *',  // Every day at 9 AM
    tz: 'America/New_York',
  },
});

// Every 5 minutes
await queue.add('health-check', {}, {
  repeat: { every: 300000 },  // 5 minutes
});
```

### Job Prioritization

```typescript
// High priority (processed first)
await queue.add('critical-alert', { ... }, { priority: 1 });

// Normal priority
await queue.add('email', { ... }, { priority: 5 });

// Low priority (processed last)
await queue.add('cleanup', { ... }, { priority: 10 });
```

### Rate Limiting

```typescript
const worker = new Worker('api-calls', async (job) => {
  await callExternalAPI(job.data);
}, {
  connection: { host: 'localhost', port: 6379 },
  limiter: {
    max: 100,       // Max 100 jobs
    duration: 60000 // Per 60 seconds
  },
});
```

## Retry and Error Handling

```typescript
await queue.add('flaky-api-call', { url: '...' }, {
  attempts: 5,              // Retry up to 5 times
  backoff: {
    type: 'exponential',
    delay: 2000,            // Start with 2s, then 4s, 8s, 16s, 32s
  },
});

// Worker error handling
const worker = new Worker('api-calls', async (job) => {
  try {
    await callAPI(job.data.url);
  } catch (error) {
    if (error.code === 'RATE_LIMIT') {
      throw error;  // Retry
    }
    // Don't retry for other errors
    await job.moveToFailed({ message: error.message }, token);
  }
});
```

## Job Events

```typescript
import { QueueEvents } from 'bullmq';

const queueEvents = new QueueEvents('emails');

queueEvents.on('completed', ({ jobId, returnvalue }) => {
  console.log(`Job ${jobId} completed:`, returnvalue);
});

queueEvents.on('failed', ({ jobId, failedReason }) => {
  console.error(`Job ${jobId} failed:`, failedReason);
});

queueEvents.on('progress', ({ jobId, data }) => {
  console.log(`Job ${jobId} progress:`, data);
});
```

## Horizontal Scaling

```typescript
// Run multiple workers (same queue, different processes)

// worker1.ts
const worker1 = new Worker('emails', processEmail, {
  connection: redis,
  concurrency: 5,  // Process 5 jobs concurrently
});

// worker2.ts (separate server)
const worker2 = new Worker('emails', processEmail, {
  connection: redis,
  concurrency: 5,
});

// Jobs automatically distributed across workers
```

## Monitoring with Bull Board

```typescript
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

createBullBoard({
  queues: [
    new BullMQAdapter(emailQueue),
    new BullMQAdapter(webhookQueue),
  ],
  serverAdapter,
});

app.use('/admin/queues', serverAdapter.getRouter());
```

Access dashboard: http://localhost:3000/admin/queues

## Job Patterns

### Fire-and-Forget

```typescript
await queue.add('send-email', { to: 'user@example.com' });
// Don't wait for completion
```

### Wait for Completion

```typescript
const job = await queue.add('generate-report', { userId: 123 });
const result = await job.waitUntilFinished(queueEvents);
console.log('Report:', result);
```

### Job Dependencies (Flow)

```typescript
import { FlowProducer } from 'bullmq';

const flow = new FlowProducer({ connection: redis });

await flow.add({
  name: 'process-video',
  queueName: 'videos',
  data: { videoId: 123 },
  children: [
    {
      name: 'extract-thumbnail',
      queueName: 'images',
      data: { videoId: 123 },
    },
    {
      name: 'generate-subtitles',
      queueName: 'transcription',
      data: { videoId: 123 },
    },
  ],
});
```

## Best Practices

1. **Use job IDs for idempotency** - Prevent duplicate processing
2. **Set reasonable timeouts** - Prevent stuck jobs
3. **Monitor failed jobs** - Set up alerting
4. **Use separate queues** - Different priorities/workers
5. **Clean completed jobs** - Prevent Redis memory growth
6. **Use concurrency wisely** - Based on I/O vs CPU
7. **Handle errors gracefully** - Distinguish retryable vs fatal errors

## Common Patterns

### Webhook Processing

```typescript
// Receive webhook
app.post('/webhooks/stripe', async (req, res) => {
  await webhookQueue.add('stripe-event', req.body, {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
  });

  res.json({ received: true });
});

// Process async
const worker = new Worker('stripe-webhooks', async (job) => {
  await processStripeEvent(job.data);
});
```

### Image Processing Pipeline

```typescript
// Upload endpoint
app.post('/upload', async (req, res) => {
  const jobId = await imageQueue.add('process-image', {
    imageUrl: req.file.url,
    userId: req.user.id,
  }, {
    priority: req.user.isPremium ? 1 : 5,
  });

  res.json({ jobId });
});

// Worker pipeline
const worker = new Worker('images', async (job) => {
  const { imageUrl } = job.data;

  // Update progress
  await job.updateProgress(10);

  const optimized = await optimizeImage(imageUrl);
  await job.updateProgress(50);

  const thumbnail = await generateThumbnail(optimized);
  await job.updateProgress(90);

  await uploadToS3(optimized, thumbnail);
  await job.updateProgress(100);

  return { optimized, thumbnail };
});
```

## Resources

- BullMQ Docs: https://docs.bullmq.io/
- Bull Board: https://github.com/felixmosh/bull-board
- GitHub: https://github.com/taskforcesh/bullmq
