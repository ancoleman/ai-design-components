# Go Streaming Patterns (kafka-go)

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Basic Producer](#basic-producer)
- [Basic Consumer](#basic-consumer)
- [Concurrent Consumer](#concurrent-consumer)
- [Graceful Shutdown](#graceful-shutdown)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)

## Overview

kafka-go (Segment) provides an idiomatic Go API for Kafka with zero external dependencies. It mirrors Go's standard library design patterns.

**Library**: kafka-go (segmentio/kafka-go)
**Code Snippets**: 42+
**Trust Score**: High
**Best For**: High-performance microservices, infrastructure tools

## Installation

```bash
go get github.com/segmentio/kafka-go
```

## Basic Producer

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "time"

    "github.com/segmentio/kafka-go"
)

type Event struct {
    UserID    string `json:"user_id"`
    Action    string `json:"action"`
    Timestamp int64  `json:"timestamp"`
}

type EventProducer struct {
    writer *kafka.Writer
}

func NewEventProducer(brokers []string, topic string) *EventProducer {
    return &EventProducer{
        writer: &kafka.Writer{
            Addr:     kafka.TCP(brokers...),
            Topic:    topic,
            Balancer: &kafka.LeastBytes{},
            // At-least-once semantics
            RequiredAcks: kafka.RequireAll,
            MaxAttempts:  3,
            // Performance
            Compression: kafka.Gzip,
            BatchSize:   100,
            BatchTimeout: 10 * time.Millisecond,
        },
    }
}

func (p *EventProducer) SendEvent(ctx context.Context, event Event) error {
    value, err := json.Marshal(event)
    if err != nil {
        return fmt.Errorf("marshal event: %w", err)
    }

    err = p.writer.WriteMessages(ctx, kafka.Message{
        Key:   []byte(event.UserID),
        Value: value,
        Headers: []kafka.Header{
            {Key: "event-type", Value: []byte(event.Action)},
        },
    })

    if err != nil {
        return fmt.Errorf("write message: %w", err)
    }

    return nil
}

func (p *EventProducer) Close() error {
    return p.writer.Close()
}

// Usage
func main() {
    producer := NewEventProducer([]string{"localhost:9092"}, "user-actions")
    defer producer.Close()

    event := Event{
        UserID:    "user-123",
        Action:    "login",
        Timestamp: time.Now().Unix(),
    }

    if err := producer.SendEvent(context.Background(), event); err != nil {
        fmt.Printf("Failed: %v\n", err)
    }
}
```

## Basic Consumer

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "github.com/segmentio/kafka-go"
)

type EventConsumer struct {
    reader *kafka.Reader
}

func NewEventConsumer(brokers []string, topic string, groupID string) *EventConsumer {
    return &EventConsumer{
        reader: kafka.NewReader(kafka.ReaderConfig{
            Brokers:  brokers,
            Topic:    topic,
            GroupID:  groupID,
            MaxBytes: 10e6, // 10MB
            // Manual commit
            CommitInterval: 0,
        }),
    }
}

func (c *EventConsumer) Consume(ctx context.Context, handler func(Event) error) error {
    for {
        msg, err := c.reader.FetchMessage(ctx)
        if err != nil {
            if err == context.Canceled {
                break
            }
            log.Printf("Fetch error: %v", err)
            continue
        }

        var event Event
        if err := json.Unmarshal(msg.Value, &event); err != nil {
            log.Printf("Unmarshal error: %v", err)
            // Send to DLQ
            c.sendToDLQ(msg)
            c.reader.CommitMessages(ctx, msg)
            continue
        }

        // Process message
        if err := handler(event); err != nil {
            log.Printf("Handler error: %v", err)
            // Don't commit - will be reprocessed
            continue
        }

        // Commit after successful processing
        if err := c.reader.CommitMessages(ctx, msg); err != nil {
            log.Printf("Commit error: %v", err)
        }
    }

    return nil
}

func (c *EventConsumer) sendToDLQ(msg kafka.Message) {
    // DLQ implementation
}

func (c *EventConsumer) Close() error {
    return c.reader.Close()
}

// Usage
func main() {
    consumer := NewEventConsumer(
        []string{"localhost:9092"},
        "user-actions",
        "my-consumer-group",
    )
    defer consumer.Close()

    handler := func(event Event) error {
        fmt.Printf("Processing: %+v\n", event)
        return nil
    }

    if err := consumer.Consume(context.Background(), handler); err != nil {
        log.Fatal(err)
    }
}
```

## Concurrent Consumer

```go
type ConcurrentConsumer struct {
    reader  *kafka.Reader
    workers int
}

func NewConcurrentConsumer(brokers []string, topic, groupID string, workers int) *ConcurrentConsumer {
    return &ConcurrentConsumer{
        reader: kafka.NewReader(kafka.ReaderConfig{
            Brokers: brokers,
            Topic:   topic,
            GroupID: groupID,
        }),
        workers: workers,
    }
}

func (c *ConcurrentConsumer) Consume(ctx context.Context, handler func(Event) error) error {
    messageChan := make(chan kafka.Message, c.workers*2)
    errorChan := make(chan error, c.workers)

    // Start worker pool
    for i := 0; i < c.workers; i++ {
        go c.worker(ctx, messageChan, errorChan, handler)
    }

    // Fetch messages
    for {
        msg, err := c.reader.FetchMessage(ctx)
        if err != nil {
            if err == context.Canceled {
                break
            }
            log.Printf("Fetch error: %v", err)
            continue
        }

        select {
        case messageChan <- msg:
        case err := <-errorChan:
            log.Printf("Worker error: %v", err)
        case <-ctx.Done():
            close(messageChan)
            return ctx.Err()
        }
    }

    close(messageChan)
    return nil
}

func (c *ConcurrentConsumer) worker(
    ctx context.Context,
    messages <-chan kafka.Message,
    errors chan<- error,
    handler func(Event) error,
) {
    for msg := range messages {
        var event Event
        if err := json.Unmarshal(msg.Value, &event); err != nil {
            errors <- err
            c.reader.CommitMessages(ctx, msg)
            continue
        }

        if err := handler(event); err != nil {
            errors <- err
            continue
        }

        c.reader.CommitMessages(ctx, msg)
    }
}
```

## Graceful Shutdown

```go
package main

import (
    "context"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Handle signals
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

    consumer := NewEventConsumer(
        []string{"localhost:9092"},
        "events",
        "my-group",
    )
    defer consumer.Close()

    go func() {
        <-sigChan
        fmt.Println("Shutting down...")
        cancel()
    }()

    handler := func(event Event) error {
        fmt.Printf("Processing: %+v\n", event)
        return nil
    }

    if err := consumer.Consume(ctx, handler); err != nil && err != context.Canceled {
        fmt.Printf("Error: %v\n", err)
    }

    fmt.Println("Shutdown complete")
}
```

## Best Practices

### 1. Use Context for Cancellation

```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()

err := producer.SendEvent(ctx, event)
```

### 2. Handle Errors Explicitly

```go
if err := writer.WriteMessages(ctx, messages...); err != nil {
    if errors.Is(err, context.DeadlineExceeded) {
        // Timeout handling
    } else if errors.Is(err, kafka.LeaderNotAvailable) {
        // Retry
    } else {
        // Fatal error
    }
}
```

### 3. Batch Messages for Performance

```go
messages := make([]kafka.Message, 0, 100)
for _, event := range events {
    value, _ := json.Marshal(event)
    messages = append(messages, kafka.Message{Value: value})
}

writer.WriteMessages(ctx, messages...)
```

## Conclusion

kafka-go provides a performant, idiomatic Go client for Kafka. Use it for high-throughput microservices and infrastructure tools.
