# TypeScript Streaming Patterns (KafkaJS)

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Basic Producer](#basic-producer)
- [Basic Consumer](#basic-consumer)
- [Error Handling](#error-handling)
- [Exactly-Once Semantics](#exactly-once-semantics)
- [Production Patterns](#production-patterns)

## Overview

KafkaJS is the recommended TypeScript/Node.js client for Apache Kafka. It provides a modern, promise-based API with excellent TypeScript support.

**Library**: KafkaJS
**Repository**: https://github.com/tulios/kafkajs
**Trust Score**: High
**Code Snippets**: 827+
**Best For**: Web services, API gateways, real-time dashboards

## Installation

```bash
npm install kafkajs
# or
yarn add kafkajs
```

**TypeScript types**: Included in package (no @types needed)

## Basic Producer

### Simple Producer

```typescript
import { Kafka, CompressionTypes, Partitioners } from 'kafkajs';

interface UserEvent {
  userId: string;
  action: string;
  timestamp: number;
}

class EventProducer {
  private kafka: Kafka;
  private producer: Producer;

  constructor(brokers: string[]) {
    this.kafka = new Kafka({
      clientId: 'my-app-producer',
      brokers: brokers,
      // Optional: SSL/SASL configuration
      // ssl: true,
      // sasl: {
      //   mechanism: 'plain',
      //   username: 'user',
      //   password: 'pass',
      // },
    });

    this.producer = this.kafka.producer({
      createPartitioner: Partitioners.LegacyPartitioner,
      // Exactly-once semantics
      idempotent: true,
      maxInFlightRequests: 5,
      transactionalId: 'my-transactional-producer', // For transactions
    });
  }

  async connect(): Promise<void> {
    await this.producer.connect();
    console.log('Producer connected');
  }

  async sendEvent(topic: string, event: UserEvent): Promise<void> {
    try {
      const metadata = await this.producer.send({
        topic,
        compression: CompressionTypes.GZIP,
        messages: [
          {
            key: event.userId, // Partition by user ID
            value: JSON.stringify(event),
            headers: {
              'correlation-id': generateCorrelationId(),
              'event-type': event.action,
            },
          },
        ],
      });

      console.log(`Event sent to partition ${metadata[0].partition}`);
    } catch (error) {
      console.error('Failed to send event:', error);
      throw error;
    }
  }

  async sendBatch(topic: string, events: UserEvent[]): Promise<void> {
    const messages = events.map(event => ({
      key: event.userId,
      value: JSON.stringify(event),
    }));

    await this.producer.send({
      topic,
      messages,
    });
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
  }
}

// Helper function
function generateCorrelationId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(7)}`;
}

// Usage
const producer = new EventProducer(['localhost:9092']);
await producer.connect();
await producer.sendEvent('user-actions', {
  userId: 'user-123',
  action: 'login',
  timestamp: Date.now(),
});
await producer.disconnect();
```

### Producer with Graceful Shutdown

```typescript
import { Kafka, Producer } from 'kafkajs';

class GracefulProducer {
  private producer: Producer;
  private isShuttingDown = false;

  constructor(brokers: string[]) {
    const kafka = new Kafka({
      clientId: 'my-app',
      brokers,
    });
    this.producer = kafka.producer();
  }

  async connect(): Promise<void> {
    await this.producer.connect();

    // Handle process signals
    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());
  }

  async send(topic: string, message: any): Promise<void> {
    if (this.isShuttingDown) {
      throw new Error('Producer is shutting down');
    }

    await this.producer.send({
      topic,
      messages: [{ value: JSON.stringify(message) }],
    });
  }

  private async shutdown(): Promise<void> {
    if (this.isShuttingDown) return;

    console.log('Shutting down producer...');
    this.isShuttingDown = true;

    await this.producer.disconnect();
    console.log('Producer disconnected');
    process.exit(0);
  }
}
```

## Basic Consumer

### Simple Consumer

```typescript
import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';

class EventConsumer {
  private kafka: Kafka;
  private consumer: Consumer;

  constructor(brokers: string[], groupId: string) {
    this.kafka = new Kafka({
      clientId: 'my-app-consumer',
      brokers,
    });

    this.consumer = this.kafka.consumer({
      groupId,
      // Start from earliest if no offset committed
      sessionTimeout: 30000,
      heartbeatInterval: 3000,
    });
  }

  async connect(): Promise<void> {
    await this.consumer.connect();
  }

  async subscribe(topics: string[]): Promise<void> {
    await this.consumer.subscribe({
      topics,
      fromBeginning: false, // Set true to replay from start
    });
  }

  async startConsuming(handler: (message: any) => Promise<void>): Promise<void> {
    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }: EachMessagePayload) => {
        const value = message.value?.toString();
        if (!value) return;

        try {
          const parsed = JSON.parse(value);
          await handler(parsed);
          // Offset committed automatically by default
        } catch (error) {
          console.error('Message processing failed:', error);
          // Implement error handling strategy
        }
      },
    });
  }

  async disconnect(): Promise<void> {
    await this.consumer.disconnect();
  }
}

// Usage
const consumer = new EventConsumer(['localhost:9092'], 'my-consumer-group');
await consumer.connect();
await consumer.subscribe(['user-actions']);
await consumer.startConsuming(async (event) => {
  console.log('Processing event:', event);
  // Your business logic here
});
```

### Consumer with Manual Offset Commits

```typescript
import { Kafka, Consumer } from 'kafkajs';

class ManualCommitConsumer {
  private consumer: Consumer;

  constructor(brokers: string[], groupId: string) {
    const kafka = new Kafka({ clientId: 'app', brokers });
    this.consumer = kafka.consumer({
      groupId,
      // Disable auto-commit for manual control
      maxWaitTimeInMs: 1000,
    });
  }

  async connect(): Promise<void> {
    await this.consumer.connect();
  }

  async subscribe(topics: string[]): Promise<void> {
    await this.consumer.subscribe({ topics });
  }

  async consume(handler: (message: any) => Promise<void>): Promise<void> {
    await this.consumer.run({
      autoCommit: false, // Manual offset management
      eachMessage: async ({ topic, partition, message }) => {
        const value = message.value?.toString();
        if (!value) return;

        try {
          const parsed = JSON.parse(value);

          // Process message
          await handler(parsed);

          // Commit offset only after successful processing
          await this.consumer.commitOffsets([
            {
              topic,
              partition,
              offset: (parseInt(message.offset) + 1).toString(),
            },
          ]);
        } catch (error) {
          console.error('Processing error:', error);
          // Don't commit - message will be reprocessed
        }
      },
    });
  }
}
```

## Error Handling

### Dead Letter Queue Pattern

```typescript
import { Kafka, Producer, Consumer, EachMessagePayload } from 'kafkajs';

class ConsumerWithDLQ {
  private consumer: Consumer;
  private dlqProducer: Producer;
  private maxRetries = 3;

  constructor(brokers: string[], groupId: string) {
    const kafka = new Kafka({ clientId: 'app', brokers });
    this.consumer = kafka.consumer({ groupId });
    this.dlqProducer = kafka.producer();
  }

  async connect(): Promise<void> {
    await this.consumer.connect();
    await this.dlqProducer.connect();
  }

  async subscribe(topics: string[]): Promise<void> {
    await this.consumer.subscribe({ topics });
  }

  async consume(handler: (message: any) => Promise<void>): Promise<void> {
    await this.consumer.run({
      autoCommit: false,
      eachMessage: async ({ topic, partition, message }: EachMessagePayload) => {
        const value = message.value?.toString();
        if (!value) return;

        let retries = 0;
        let success = false;

        while (retries < this.maxRetries && !success) {
          try {
            const parsed = JSON.parse(value);
            await handler(parsed);
            success = true;

            // Commit offset after successful processing
            await this.consumer.commitOffsets([
              {
                topic,
                partition,
                offset: (parseInt(message.offset) + 1).toString(),
              },
            ]);
          } catch (error) {
            retries++;
            console.error(`Retry ${retries}/${this.maxRetries}:`, error);

            if (retries < this.maxRetries) {
              // Exponential backoff
              await sleep(Math.pow(2, retries) * 1000);
            } else {
              // Send to DLQ after max retries
              await this.sendToDLQ(topic, message, error as Error);
              // Commit to move forward
              await this.consumer.commitOffsets([
                {
                  topic,
                  partition,
                  offset: (parseInt(message.offset) + 1).toString(),
                },
              ]);
            }
          }
        }
      },
    });
  }

  private async sendToDLQ(
    originalTopic: string,
    message: any,
    error: Error
  ): Promise<void> {
    const dlqTopic = `${originalTopic}.dlq`;

    await this.dlqProducer.send({
      topic: dlqTopic,
      messages: [
        {
          key: message.key,
          value: message.value,
          headers: {
            ...message.headers,
            'original-topic': originalTopic,
            'error-message': error.message,
            'failed-at': new Date().toISOString(),
          },
        },
      ],
    });

    console.log(`Message sent to DLQ: ${dlqTopic}`);
  }

  async disconnect(): Promise<void> {
    await this.consumer.disconnect();
    await this.dlqProducer.disconnect();
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### Circuit Breaker Pattern

```typescript
class CircuitBreaker {
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime: number = 0;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    this.successCount++;

    if (this.state === 'HALF_OPEN' && this.successCount >= 3) {
      this.state = 'CLOSED';
      this.successCount = 0;
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    this.successCount = 0;

    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }

  getState(): string {
    return this.state;
  }
}

// Usage
const breaker = new CircuitBreaker(5, 60000);

await consumer.run({
  eachMessage: async ({ message }) => {
    await breaker.execute(async () => {
      // Your processing logic
      await processMessage(message);
    });
  },
});
```

## Exactly-Once Semantics

### Transactional Producer

```typescript
import { Kafka, Producer } from 'kafkajs';

class TransactionalProducer {
  private producer: Producer;

  constructor(brokers: string[], transactionalId: string) {
    const kafka = new Kafka({ clientId: 'app', brokers });

    this.producer = kafka.producer({
      idempotent: true,
      maxInFlightRequests: 1,
      transactionalId, // Required for transactions
    });
  }

  async connect(): Promise<void> {
    await this.producer.connect();
  }

  async sendInTransaction(
    operations: Array<{ topic: string; messages: any[] }>
  ): Promise<void> {
    const transaction = await this.producer.transaction();

    try {
      // Send all messages in transaction
      for (const op of operations) {
        await transaction.send({
          topic: op.topic,
          messages: op.messages,
        });
      }

      // Commit transaction
      await transaction.commit();
    } catch (error) {
      // Rollback on error
      await transaction.abort();
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
  }
}

// Usage: Exactly-once processing
const txProducer = new TransactionalProducer(
  ['localhost:9092'],
  'my-tx-producer'
);

await txProducer.connect();
await txProducer.sendInTransaction([
  {
    topic: 'orders',
    messages: [{ value: JSON.stringify({ orderId: '123', status: 'created' }) }],
  },
  {
    topic: 'inventory',
    messages: [{ value: JSON.stringify({ productId: 'P1', quantity: -1 }) }],
  },
]);
```

### Consumer with Exactly-Once Processing

```typescript
import { Kafka, Consumer, Producer } from 'kafkajs';

class ExactlyOnceConsumer {
  private consumer: Consumer;
  private producer: Producer;

  constructor(brokers: string[], groupId: string, transactionalId: string) {
    const kafka = new Kafka({ clientId: 'app', brokers });
    this.consumer = kafka.consumer({ groupId });
    this.producer = kafka.producer({
      idempotent: true,
      transactionalId,
    });
  }

  async connect(): Promise<void> {
    await this.consumer.connect();
    await this.producer.connect();
  }

  async subscribe(topics: string[]): Promise<void> {
    await this.consumer.subscribe({ topics });
  }

  async consume(
    handler: (message: any) => Promise<{ topic: string; messages: any[] }>
  ): Promise<void> {
    await this.consumer.run({
      autoCommit: false,
      eachMessage: async ({ topic, partition, message }) => {
        const value = message.value?.toString();
        if (!value) return;

        const transaction = await this.producer.transaction();

        try {
          const parsed = JSON.parse(value);

          // Process message and get output
          const output = await handler(parsed);

          // Send output in transaction
          await transaction.send(output);

          // Commit consumer offset in same transaction
          await transaction.sendOffsets({
            consumerGroupId: this.consumer.groupId,
            topics: [
              {
                topic,
                partitions: [
                  {
                    partition,
                    offset: (parseInt(message.offset) + 1).toString(),
                  },
                ],
              },
            ],
          });

          // Commit transaction
          await transaction.commit();
        } catch (error) {
          await transaction.abort();
          throw error;
        }
      },
    });
  }
}
```

## Production Patterns

### Health Check Endpoint

```typescript
import express from 'express';
import { Kafka } from 'kafkajs';

const app = express();
const kafka = new Kafka({ clientId: 'app', brokers: ['localhost:9092'] });
const admin = kafka.admin();

app.get('/health', async (req, res) => {
  try {
    await admin.connect();
    const cluster = await admin.describeCluster();
    await admin.disconnect();

    res.json({
      status: 'healthy',
      brokers: cluster.brokers.length,
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: (error as Error).message,
    });
  }
});

app.listen(3000);
```

### Metrics Collection

```typescript
import { Kafka, Producer } from 'kafkajs';
import { Counter, Histogram } from 'prom-client';

const messagesSent = new Counter({
  name: 'kafka_messages_sent_total',
  help: 'Total messages sent',
  labelNames: ['topic'],
});

const sendDuration = new Histogram({
  name: 'kafka_send_duration_seconds',
  help: 'Duration of send operations',
  labelNames: ['topic'],
});

class MetricsProducer {
  private producer: Producer;

  constructor(brokers: string[]) {
    const kafka = new Kafka({ clientId: 'app', brokers });
    this.producer = kafka.producer();
  }

  async connect(): Promise<void> {
    await this.producer.connect();
  }

  async send(topic: string, message: any): Promise<void> {
    const timer = sendDuration.startTimer({ topic });

    try {
      await this.producer.send({
        topic,
        messages: [{ value: JSON.stringify(message) }],
      });

      messagesSent.inc({ topic });
    } finally {
      timer();
    }
  }
}
```

### Batch Processing

```typescript
class BatchConsumer {
  private consumer: Consumer;
  private batchSize = 100;
  private batchTimeout = 5000; // 5 seconds
  private batch: any[] = [];
  private batchTimer: NodeJS.Timeout | null = null;

  constructor(brokers: string[], groupId: string) {
    const kafka = new Kafka({ clientId: 'app', brokers });
    this.consumer = kafka.consumer({ groupId });
  }

  async connect(): Promise<void> {
    await this.consumer.connect();
  }

  async subscribe(topics: string[]): Promise<void> {
    await this.consumer.subscribe({ topics });
  }

  async consume(handler: (batch: any[]) => Promise<void>): Promise<void> {
    await this.consumer.run({
      eachMessage: async ({ message }) => {
        const value = message.value?.toString();
        if (!value) return;

        const parsed = JSON.parse(value);
        this.batch.push(parsed);

        // Process when batch is full
        if (this.batch.length >= this.batchSize) {
          await this.processBatch(handler);
        } else {
          // Set timer for batch timeout
          if (!this.batchTimer) {
            this.batchTimer = setTimeout(async () => {
              await this.processBatch(handler);
            }, this.batchTimeout);
          }
        }
      },
    });
  }

  private async processBatch(handler: (batch: any[]) => Promise<void>): Promise<void> {
    if (this.batch.length === 0) return;

    if (this.batchTimer) {
      clearTimeout(this.batchTimer);
      this.batchTimer = null;
    }

    const currentBatch = [...this.batch];
    this.batch = [];

    await handler(currentBatch);
  }
}
```

## Conclusion

KafkaJS provides a production-ready TypeScript client with excellent developer experience. Use idempotent producers and manual offset commits for at-least-once delivery, or transactions for exactly-once semantics.
