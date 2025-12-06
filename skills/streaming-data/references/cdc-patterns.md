# Change Data Capture (CDC) Patterns

## Table of Contents
- [Overview](#overview)
- [Use Cases](#use-cases)
- [Debezium (Recommended)](#debezium-recommended)
- [MySQL CDC Example](#mysql-cdc-example)
- [PostgreSQL CDC Example](#postgresql-cdc-example)
- [Consuming CDC Events](#consuming-cdc-events)
- [Outbox Pattern](#outbox-pattern)
- [Best Practices](#best-practices)
- [Monitoring](#monitoring)
- [Conclusion](#conclusion)

## Overview

Change Data Capture captures changes from databases and publishes them as events to streaming platforms. Essential for real-time data synchronization and microservices data integration.

## Use Cases

- Real-time data replication
- Microservices data synchronization
- Event-driven architectures
- Data warehouse ingestion
- Cache invalidation

## Debezium (Recommended)

Debezium is the industry-standard CDC tool for Kafka. It captures row-level changes from databases and publishes them to Kafka topics.

### Supported Databases
- MySQL
- PostgreSQL
- MongoDB
- SQL Server
- Oracle
- Db2
- Cassandra

### Architecture

```
Database → Debezium Connector → Kafka → Consumers
```

## MySQL CDC Example

### 1. Enable Binary Logging

```sql
-- MySQL configuration (my.cnf)
server-id = 1
log_bin = mysql-bin
binlog_format = ROW
binlog_row_image = FULL
expire_logs_days = 10
```

### 2. Create Debezium User

```sql
CREATE USER 'debezium'@'%' IDENTIFIED BY 'password';
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT
ON *.* TO 'debezium'@'%';
FLUSH PRIVILEGES;
```

### 3. Deploy Debezium Connector

```json
{
  "name": "mysql-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "password",
    "database.server.id": "184054",
    "database.server.name": "mydb",
    "database.include.list": "inventory",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.inventory"
  }
}
```

### 4. Event Format

```json
{
  "before": {
    "id": 1,
    "name": "Old Name",
    "email": "old@example.com"
  },
  "after": {
    "id": 1,
    "name": "New Name",
    "email": "new@example.com"
  },
  "source": {
    "version": "1.9.0.Final",
    "connector": "mysql",
    "name": "mydb",
    "ts_ms": 1234567890,
    "snapshot": "false",
    "db": "inventory",
    "table": "users",
    "server_id": 1,
    "gtid": null,
    "file": "mysql-bin.000003",
    "pos": 154,
    "row": 0
  },
  "op": "u",
  "ts_ms": 1234567890
}
```

## PostgreSQL CDC Example

### 1. Enable Logical Replication

```sql
-- postgresql.conf
wal_level = logical
max_replication_slots = 4
max_wal_senders = 4
```

### 2. Create Replication User

```sql
CREATE USER debezium WITH REPLICATION PASSWORD 'password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO debezium;
```

### 3. Deploy Connector

```json
{
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "password",
    "database.dbname": "inventory",
    "database.server.name": "pgserver",
    "plugin.name": "pgoutput",
    "publication.name": "dbz_publication"
  }
}
```

## Consuming CDC Events

### TypeScript Consumer

```typescript
import { Kafka } from 'kafkajs';

interface CDCEvent {
  before: any;
  after: any;
  source: {
    db: string;
    table: string;
    ts_ms: number;
  };
  op: 'c' | 'u' | 'd' | 'r'; // create, update, delete, read
  ts_ms: number;
}

class CDCConsumer {
  private consumer: Consumer;

  async subscribe(tables: string[]): Promise<void> {
    const topics = tables.map(t => `mydb.inventory.${t}`);
    await this.consumer.subscribe({ topics });
  }

  async consume(): Promise<void> {
    await this.consumer.run({
      eachMessage: async ({ topic, message }) => {
        const event: CDCEvent = JSON.parse(message.value.toString());

        switch (event.op) {
          case 'c': // CREATE
            await this.handleInsert(event.after);
            break;
          case 'u': // UPDATE
            await this.handleUpdate(event.before, event.after);
            break;
          case 'd': // DELETE
            await this.handleDelete(event.before);
            break;
        }
      },
    });
  }

  private async handleInsert(record: any): Promise<void> {
    console.log('Insert:', record);
    // Sync to cache, search index, etc.
  }

  private async handleUpdate(before: any, after: any): Promise<void> {
    console.log('Update:', before, '->', after);
    // Invalidate cache, update search index
  }

  private async handleDelete(record: any): Promise<void> {
    console.log('Delete:', record);
    // Remove from cache, search index
  }
}
```

### Python Consumer

```python
from confluent_kafka import Consumer
import json

class CDCConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
        })

    def subscribe(self, tables: list):
        topics = [f'mydb.inventory.{table}' for table in tables]
        self.consumer.subscribe(topics)

    def consume(self):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue

            event = json.loads(msg.value().decode('utf-8'))

            if event['op'] == 'c':
                self.handle_insert(event['after'])
            elif event['op'] == 'u':
                self.handle_update(event['before'], event['after'])
            elif event['op'] == 'd':
                self.handle_delete(event['before'])

    def handle_insert(self, record):
        print(f'Insert: {record}')
        # Sync to Elasticsearch, Redis, etc.

    def handle_update(self, before, after):
        print(f'Update: {before} -> {after}')

    def handle_delete(self, record):
        print(f'Delete: {record}')

# Usage
consumer = CDCConsumer('localhost:9092', 'cdc-consumer')
consumer.subscribe(['users', 'orders'])
consumer.consume()
```

## Outbox Pattern

Combine CDC with outbox pattern for reliable event publishing:

### 1. Create Outbox Table

```sql
CREATE TABLE outbox (
  id UUID PRIMARY KEY,
  aggregate_id VARCHAR(255),
  event_type VARCHAR(255),
  payload JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 2. Transactional Write

```sql
BEGIN;
  -- Business logic
  UPDATE orders SET status = 'shipped' WHERE id = '123';

  -- Write to outbox
  INSERT INTO outbox (id, aggregate_id, event_type, payload)
  VALUES (
    gen_random_uuid(),
    '123',
    'OrderShipped',
    '{"orderId": "123", "trackingNumber": "TRACK123"}'::jsonb
  );
COMMIT;
```

### 3. CDC Captures Outbox

Debezium captures outbox changes and publishes to Kafka. Application consumes events from Kafka topic.

## Best Practices

1. **Use Debezium**: Industry-standard, battle-tested
2. **Monitor lag**: Track replication delay
3. **Handle schema changes**: Plan for column additions/removals
4. **Idempotent consumers**: CDC may deliver duplicates
5. **Filter events**: Use SMTs (Single Message Transforms)
6. **Tombstone events**: Handle deletes properly

## Monitoring

```python
from prometheus_client import Gauge

cdc_lag = Gauge('cdc_replication_lag_seconds', 'CDC replication lag')

def monitor_lag(event):
    current_time = time.time() * 1000
    event_time = event['ts_ms']
    lag_ms = current_time - event_time
    cdc_lag.set(lag_ms / 1000)
```

## Conclusion

CDC enables real-time data synchronization without application code changes. Use Debezium for production deployments, implement the outbox pattern for transactional guarantees.
