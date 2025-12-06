# Database Migration & CDC


## Table of Contents

- [Schema Migration Tools](#schema-migration-tools)
  - [Python (Alembic)](#python-alembic)
  - [TypeScript (Drizzle)](#typescript-drizzle)
- [Bulk Data Migration](#bulk-data-migration)
  - [Python - Table to Table](#python-table-to-table)
  - [With Transformation](#with-transformation)
- [Change Data Capture (CDC)](#change-data-capture-cdc)
  - [PostgreSQL Logical Replication](#postgresql-logical-replication)
  - [Debezium (Docker)](#debezium-docker)
- [Initial Load + CDC Pattern](#initial-load-cdc-pattern)
- [Data Validation](#data-validation)

## Schema Migration Tools

### Python (Alembic)
```python
# alembic/versions/001_initial.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')
```

### TypeScript (Drizzle)
```typescript
// drizzle/0001_initial.ts
import { pgTable, serial, varchar, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  createdAt: timestamp("created_at").defaultNow()
});

// Run migration
import { migrate } from "drizzle-orm/node-postgres/migrator";
await migrate(db, { migrationsFolder: "./drizzle" });
```

## Bulk Data Migration

### Python - Table to Table
```python
import polars as pl
from sqlalchemy import create_engine

source = create_engine("postgresql://source_db")
target = create_engine("postgresql://target_db")

def migrate_table(table_name: str, batch_size: int = 10000):
    """Migrate table in batches."""
    offset = 0

    while True:
        # Read batch from source
        query = f"SELECT * FROM {table_name} ORDER BY id LIMIT {batch_size} OFFSET {offset}"
        df = pl.read_database(query, source)

        if len(df) == 0:
            break

        # Write to target
        df.write_database(
            table_name=table_name,
            connection=target,
            if_table_exists="append"
        )

        offset += batch_size
        print(f"Migrated {offset} rows...")
```

### With Transformation
```python
def migrate_with_transform(source_table: str, target_table: str):
    """Migrate with schema transformation."""
    df = pl.read_database(f"SELECT * FROM {source_table}", source)

    # Transform
    df = df.rename({"old_column": "new_column"})
    df = df.with_columns([
        pl.col("amount").cast(pl.Decimal(10, 2)),
        pl.col("created_at").str.to_datetime()
    ])
    df = df.drop("deprecated_field")

    # Write
    df.write_database(target_table, target, if_table_exists="replace")
```

## Change Data Capture (CDC)

### PostgreSQL Logical Replication
```python
import psycopg2
from psycopg2.extras import LogicalReplicationConnection

def consume_changes(slot_name: str = "my_slot"):
    conn = psycopg2.connect(
        connection_factory=LogicalReplicationConnection,
        dsn="postgresql://localhost/mydb"
    )
    cursor = conn.cursor()

    # Create replication slot
    cursor.create_replication_slot(slot_name, output_plugin='pgoutput')

    # Start replication
    cursor.start_replication(slot_name=slot_name)

    def consume(msg):
        # Parse logical replication message
        change = parse_pgoutput(msg.payload)
        process_change(change)
        msg.cursor.send_feedback(flush_lsn=msg.data_start)

    cursor.consume_stream(consume)
```

### Debezium (Docker)
```yaml
# docker-compose.yml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [zookeeper]
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092

  debezium:
    image: debezium/connect:2.4
    depends_on: [kafka]
    environment:
      BOOTSTRAP_SERVERS: kafka:9092
      GROUP_ID: 1
      CONFIG_STORAGE_TOPIC: debezium_config
      OFFSET_STORAGE_TOPIC: debezium_offsets
      STATUS_STORAGE_TOPIC: debezium_status
```

```python
# Register Debezium connector
import requests

connector_config = {
    "name": "postgres-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "postgres",
        "database.port": "5432",
        "database.user": "debezium",
        "database.password": "secret",
        "database.dbname": "mydb",
        "topic.prefix": "mydb",
        "table.include.list": "public.users,public.orders",
        "plugin.name": "pgoutput"
    }
}

requests.post(
    "http://localhost:8083/connectors",
    json=connector_config
)
```

## Initial Load + CDC Pattern

```python
async def initial_load_with_cdc(table: str):
    """
    1. Start CDC capture
    2. Take snapshot
    3. Apply CDC changes after snapshot
    """
    # Mark CDC start position
    cdc_start = await get_current_lsn()

    # Full table snapshot
    snapshot_df = pl.read_database(f"SELECT * FROM {table}", source)
    await write_to_target(snapshot_df, table)

    # Apply buffered CDC changes
    changes = await get_changes_since(cdc_start)
    for change in changes:
        await apply_change(change)

    # Continue with live CDC
    await consume_cdc_stream()
```

## Data Validation

```python
def validate_migration(source_table: str, target_table: str) -> dict:
    """Validate migration completeness."""
    source_count = pl.read_database(
        f"SELECT COUNT(*) as cnt FROM {source_table}", source
    )["cnt"][0]

    target_count = pl.read_database(
        f"SELECT COUNT(*) as cnt FROM {target_table}", target
    )["cnt"][0]

    # Sample comparison
    source_sample = pl.read_database(
        f"SELECT * FROM {source_table} ORDER BY RANDOM() LIMIT 100", source
    )
    target_sample = pl.read_database(
        f"SELECT * FROM {target_table} WHERE id IN ({','.join(map(str, source_sample['id']))})", target
    )

    return {
        "source_count": source_count,
        "target_count": target_count,
        "count_match": source_count == target_count,
        "sample_match": source_sample.equals(target_sample)
    }
```
