# Error Handling Patterns for Stream Processing

## Table of Contents
- [Overview](#overview)
- [Dead Letter Queue (DLQ) Pattern](#dead-letter-queue-dlq-pattern)
- [Retry Strategies](#retry-strategies)
- [Backpressure Handling](#backpressure-handling)
- [Circuit Breaker Pattern](#circuit-breaker-pattern)
- [Graceful Shutdown](#graceful-shutdown)
- [Monitoring and Alerting](#monitoring-and-alerting)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)

## Overview

Production stream processing requires robust error handling strategies including dead-letter queues, retry logic, backpressure management, and circuit breakers.

## Dead Letter Queue (DLQ) Pattern

### Purpose
Send messages that fail processing to a separate topic for later analysis and manual intervention.

### When to Use
- Message cannot be parsed (schema mismatch)
- Processing fails after maximum retries
- Downstream service permanently unavailable
- Business logic validation failures

### Implementation (TypeScript)

```typescript
class ConsumerWithDLQ {
  private consumer: Consumer;
  private dlqProducer: Producer;

  async processWithDLQ(message: any): Promise<void> {
    try {
      await this.processMessage(message);
      await this.consumer.commitOffsets([...]);
    } catch (error) {
      await this.sendToDLQ(message, error);
      await this.consumer.commitOffsets([...]);
    }
  }

  private async sendToDLQ(message: any, error: Error): Promise<void> {
    const dlqTopic = `${message.topic}.dlq`;

    await this.dlqProducer.send({
      topic: dlqTopic,
      messages: [{
        key: message.key,
        value: message.value,
        headers: {
          'original-topic': message.topic,
          'error-message': error.message,
          'error-stack': error.stack,
          'failed-at': new Date().toISOString(),
          'retry-count': '3',
        },
      }],
    });
  }
}
```

## Retry Strategies

### Exponential Backoff

```python
import time

def process_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            process_message(message)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                # Exponential backoff: 1s, 2s, 4s
                sleep_time = 2 ** attempt
                time.sleep(sleep_time)
            else:
                # Final attempt failed
                send_to_dlq(message, e)
                return False
```

### Retry with Jitter

```go
func processWithRetry(msg kafka.Message, maxRetries int) error {
    for attempt := 0; attempt < maxRetries; attempt++ {
        err := processMessage(msg)
        if err == nil {
            return nil
        }

        if attempt < maxRetries-1 {
            // Exponential backoff with jitter
            baseDelay := time.Duration(math.Pow(2, float64(attempt))) * time.Second
            jitter := time.Duration(rand.Int63n(int64(baseDelay / 2)))
            time.Sleep(baseDelay + jitter)
        }
    }

    return sendToDLQ(msg)
}
```

## Backpressure Handling

### Consumer Backpressure

```java
public class BackpressureConsumer {
    private final Semaphore semaphore;
    private final int maxConcurrent = 100;

    public BackpressureConsumer() {
        this.semaphore = new Semaphore(maxConcurrent);
    }

    public void consume() {
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

            for (ConsumerRecord<String, String> record : records) {
                try {
                    // Acquire permit (blocks if maxConcurrent reached)
                    semaphore.acquire();

                    // Process asynchronously
                    executor.submit(() -> {
                        try {
                            processMessage(record);
                        } finally {
                            semaphore.release();
                        }
                    });
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
}
```

### Producer Backpressure

```typescript
class BackpressureProducer {
  private queue: any[] = [];
  private maxQueueSize = 10000;
  private processing = false;

  async send(message: any): Promise<void> {
    if (this.queue.length >= this.maxQueueSize) {
      throw new Error('Queue full - backpressure applied');
    }

    this.queue.push(message);

    if (!this.processing) {
      this.processBatch();
    }
  }

  private async processBatch(): Promise<void> {
    this.processing = true;

    while (this.queue.length > 0) {
      const batch = this.queue.splice(0, 100);

      try {
        await this.producer.sendBatch(batch);
      } catch (error) {
        // Re-queue on failure
        this.queue.unshift(...batch);
        await sleep(1000);
      }
    }

    this.processing = false;
  }
}
```

## Circuit Breaker Pattern

```typescript
enum CircuitState {
  CLOSED,
  OPEN,
  HALF_OPEN,
}

class CircuitBreaker {
  private state = CircuitState.CLOSED;
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime = 0;

  constructor(
    private threshold = 5,
    private timeout = 60000,
    private halfOpenAttempts = 3
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = CircuitState.HALF_OPEN;
        this.successCount = 0;
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

    if (this.state === CircuitState.HALF_OPEN) {
      this.successCount++;
      if (this.successCount >= this.halfOpenAttempts) {
        this.state = CircuitState.CLOSED;
      }
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.threshold) {
      this.state = CircuitState.OPEN;
    }
  }
}
```

## Graceful Shutdown

### TypeScript

```typescript
class GracefulConsumer {
  private isShuttingDown = false;

  async start(): Promise<void> {
    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());

    await this.consume();
  }

  private async shutdown(): Promise<void> {
    if (this.isShuttingDown) return;

    console.log('Shutting down gracefully...');
    this.isShuttingDown = true;

    // Stop accepting new messages
    await this.consumer.disconnect();

    // Wait for in-flight messages to complete
    await this.waitForInFlight();

    process.exit(0);
  }
}
```

### Go

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

    go func() {
        <-sigChan
        log.Println("Shutdown signal received")
        cancel()
    }()

    consumer.Consume(ctx, handler)
    log.Println("Shutdown complete")
}
```

## Monitoring and Alerting

### Metrics to Track

```python
from prometheus_client import Counter, Histogram, Gauge

# Message metrics
messages_processed = Counter('messages_processed_total', 'Total messages processed')
messages_failed = Counter('messages_failed_total', 'Total messages failed')
processing_duration = Histogram('processing_duration_seconds', 'Message processing duration')

# Consumer lag
consumer_lag = Gauge('consumer_lag', 'Consumer lag in messages', ['partition'])

# DLQ metrics
dlq_messages = Counter('dlq_messages_total', 'Messages sent to DLQ')

def process_message(msg):
    start_time = time.time()

    try:
        # Process message
        handle_message(msg)

        messages_processed.inc()
    except Exception as e:
        messages_failed.inc()
        send_to_dlq(msg, e)
        dlq_messages.inc()
    finally:
        duration = time.time() - start_time
        processing_duration.observe(duration)
```

## Best Practices

1. **Always implement DLQ**: Never silently drop failed messages
2. **Use exponential backoff**: Avoid thundering herd on retry
3. **Set max retries**: Prevent infinite retry loops
4. **Monitor consumer lag**: Alert on growing backlog
5. **Graceful shutdown**: Finish processing before exit
6. **Circuit breakers**: Protect downstream services
7. **Backpressure**: Prevent memory exhaustion

## Conclusion

Robust error handling is critical for production stream processing. Implement DLQ patterns, retry logic with backoff, backpressure management, and graceful shutdown to build reliable systems.
