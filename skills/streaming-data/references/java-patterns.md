# Java Streaming Patterns (Apache Kafka Java Client)

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Basic Producer](#basic-producer)
- [Basic Consumer](#basic-consumer)
- [Transactional Producer (Exactly-Once)](#transactional-producer-exactly-once)
- [Spring Kafka Integration](#spring-kafka-integration)
- [Best Practices](#best-practices)
- [Conclusion](#conclusion)

## Overview

The Apache Kafka Java Client is the most feature-complete Kafka client, offering full support for exactly-once semantics, transactions, and all advanced features.

**Library**: Apache Kafka Java Client
**Code Snippets**: 683+
**Trust Score**: High (76.9)
**Best For**: Enterprise applications, Kafka Streams, Flink, Spark

## Installation

Maven:
```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>3.6.0</version>
</dependency>
```

Gradle:
```gradle
implementation 'org.apache.kafka:kafka-clients:3.6.0'
```

## Basic Producer

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Properties;
import java.util.concurrent.Future;

public class EventProducer {
    private final KafkaProducer<String, String> producer;
    private final ObjectMapper objectMapper;
    private final String topic;

    public EventProducer(String bootstrapServers, String topic) {
        this.topic = topic;
        this.objectMapper = new ObjectMapper();

        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        // At-least-once delivery
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);

        // Performance tuning
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4");
        props.put(ProducerConfig.BATCH_SIZE_CONFIG, 32768);
        props.put(ProducerConfig.LINGER_MS_CONFIG, 10);

        this.producer = new KafkaProducer<>(props);
    }

    public void sendAsync(Event event) throws Exception {
        String key = event.getUserId();
        String value = objectMapper.writeValueAsString(event);

        ProducerRecord<String, String> record = new ProducerRecord<>(topic, key, value);

        producer.send(record, new Callback() {
            @Override
            public void onCompletion(RecordMetadata metadata, Exception exception) {
                if (exception != null) {
                    System.err.println("Send failed: " + exception.getMessage());
                } else {
                    System.out.printf("Sent to partition %d offset %d%n",
                        metadata.partition(), metadata.offset());
                }
            }
        });
    }

    public RecordMetadata sendSync(Event event) throws Exception {
        String key = event.getUserId();
        String value = objectMapper.writeValueAsString(event);

        ProducerRecord<String, String> record = new ProducerRecord<>(topic, key, value);

        Future<RecordMetadata> future = producer.send(record);
        return future.get(); // Block until complete
    }

    public void close() {
        producer.flush();
        producer.close();
    }
}

class Event {
    private String userId;
    private String action;
    private long timestamp;

    // Constructors, getters, setters
}
```

## Basic Consumer

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class EventConsumer {
    private final KafkaConsumer<String, String> consumer;
    private final ObjectMapper objectMapper;

    public EventConsumer(String bootstrapServers, String groupId, String topic) {
        this.objectMapper = new ObjectMapper();

        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        // Manual offset management
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

        this.consumer = new KafkaConsumer<>(props);
        this.consumer.subscribe(Collections.singletonList(topic));
    }

    public void consume(EventHandler handler) {
        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));

                for (ConsumerRecord<String, String> record : records) {
                    try {
                        Event event = objectMapper.readValue(record.value(), Event.class);

                        // Process event
                        handler.handle(event);

                        // Commit offset after successful processing
                        consumer.commitSync();

                    } catch (Exception e) {
                        System.err.println("Processing error: " + e.getMessage());
                        sendToDLQ(record);
                        consumer.commitSync();
                    }
                }
            }
        } finally {
            consumer.close();
        }
    }

    private void sendToDLQ(ConsumerRecord<String, String> record) {
        // DLQ implementation
    }
}

interface EventHandler {
    void handle(Event event) throws Exception;
}
```

## Transactional Producer (Exactly-Once)

```java
import org.apache.kafka.clients.producer.*;

public class TransactionalProducer {
    private final KafkaProducer<String, String> producer;

    public TransactionalProducer(String bootstrapServers, String transactionalId) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        // Exactly-once configuration
        props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, transactionalId);
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        props.put(ProducerConfig.ACKS_CONFIG, "all");

        this.producer = new KafkaProducer<>(props);
        this.producer.initTransactions();
    }

    public void sendInTransaction(String topic, String key, String value) {
        producer.beginTransaction();

        try {
            ProducerRecord<String, String> record = new ProducerRecord<>(topic, key, value);
            producer.send(record);

            // Can send to multiple topics in same transaction
            producer.send(new ProducerRecord<>("audit-log", key, "processed"));

            producer.commitTransaction();
        } catch (Exception e) {
            producer.abortTransaction();
            throw e;
        }
    }

    public void close() {
        producer.close();
    }
}
```

## Spring Kafka Integration

```java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class KafkaService {
    private final KafkaTemplate<String, Event> kafkaTemplate;

    public KafkaService(KafkaTemplate<String, Event> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendEvent(String topic, Event event) {
        kafkaTemplate.send(topic, event.getUserId(), event)
            .addCallback(
                result -> System.out.println("Sent: " + event),
                ex -> System.err.println("Failed: " + ex)
            );
    }

    @KafkaListener(topics = "user-actions", groupId = "my-group")
    public void listen(Event event) {
        System.out.println("Received: " + event);
        // Process event
    }
}
```

## Best Practices

### 1. Use Try-With-Resources

```java
try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
    producer.send(record).get();
}
```

### 2. Batch Processing

```java
List<ProducerRecord<String, String>> batch = new ArrayList<>();
for (Event event : events) {
    batch.add(new ProducerRecord<>(topic, serialize(event)));
}

for (ProducerRecord<String, String> record : batch) {
    producer.send(record);
}
producer.flush();
```

### 3. Error Handling

```java
try {
    producer.send(record).get();
} catch (ExecutionException e) {
    if (e.getCause() instanceof RetriableException) {
        // Retry
    } else {
        // Fatal error
    }
}
```

## Conclusion

The Apache Kafka Java Client provides the most complete feature set for Kafka, including full transaction support for exactly-once semantics. Essential for enterprise Java applications.
