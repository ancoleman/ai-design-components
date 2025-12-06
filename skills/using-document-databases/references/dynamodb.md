# DynamoDB Complete Guide

AWS DynamoDB single-table design, GSI patterns, and serverless best practices.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Single-Table Design](#single-table-design)
- [Primary Keys](#primary-keys)
- [Global Secondary Indexes](#global-secondary-indexes)
- [Query Patterns](#query-patterns)
- [DynamoDB Streams](#dynamodb-streams)
- [Pricing Optimization](#pricing-optimization)
- [Performance Best Practices](#performance-best-practices)

---

## Core Concepts

### DynamoDB vs Traditional Databases

| Feature | DynamoDB | MongoDB/SQL |
|---------|----------|-------------|
| **Data Model** | Key-value, document | Document, relational |
| **Queries** | By primary key + GSI only | Flexible queries |
| **Scaling** | Automatic, unlimited | Manual sharding/replication |
| **Consistency** | Eventual (default), strong (optional) | Tunable |
| **Latency** | Single-digit ms guaranteed | Varies |
| **Pricing** | Per request or provisioned | Per instance/cluster |

### Key Terminology

- **Partition Key (PK)**: Hash key for data distribution
- **Sort Key (SK)**: Range key for sorting within partition
- **GSI**: Global Secondary Index (alternate query patterns)
- **LSI**: Local Secondary Index (different sort key, same PK)
- **WCU**: Write Capacity Unit (1 KB/sec)
- **RCU**: Read Capacity Unit (4 KB/sec for eventual, 4 KB/sec for strong)

---

## Single-Table Design

### Philosophy

Design for **access patterns**, not normalization. Store multiple entity types in one table using composite keys.

### Entity Types in One Table

```javascript
// Users table with multiple entity types

// User metadata
{
  PK: "USER#12345",
  SK: "METADATA",
  email: "user@example.com",
  name: "Jane Doe",
  createdAt: "2025-01-15T10:00:00Z"
}

// User's orders
{
  PK: "USER#12345",
  SK: "ORDER#2025-001234",
  orderNumber: "ORD-2025-001234",
  totalAmount: 249.97,
  status: "shipped",
  orderDate: "2025-11-25T14:30:00Z"
}

// Order detail (different access pattern)
{
  PK: "ORDER#2025-001234",
  SK: "METADATA",
  userId: "USER#12345",
  totalAmount: 249.97,
  status: "shipped"
}

// Order items
{
  PK: "ORDER#2025-001234",
  SK: "ITEM#001",
  productId: "PROD-456",
  quantity: 2,
  price: 49.99,
  name: "Widget Pro"
}

// Product catalog
{
  PK: "PRODUCT#456",
  SK: "METADATA",
  name: "Widget Pro",
  category: "widgets",
  price: 49.99,
  inventory: 245
}
```

### Access Patterns Enabled

```python
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AppData')

# 1. Get user metadata
response = table.query(
    KeyConditionExpression=Key('PK').eq('USER#12345') & Key('SK').eq('METADATA')
)

# 2. Get all orders for user
response = table.query(
    KeyConditionExpression=Key('PK').eq('USER#12345') & Key('SK').begins_with('ORDER#')
)

# 3. Get order with items
response = table.query(
    KeyConditionExpression=Key('PK').eq('ORDER#2025-001234')
)

# 4. Get specific order
response = table.query(
    KeyConditionExpression=Key('PK').eq('ORDER#2025-001234') & Key('SK').eq('METADATA')
)
```

### Composite Key Strategies

**Pattern 1: Entity Type Prefix**
```
PK: USER#12345
SK: METADATA
SK: ORDER#001
SK: ORDER#002
```

**Pattern 2: Hierarchical**
```
PK: TENANT#abc
SK: USER#12345
SK: USER#12345#ORDER#001
SK: USER#12345#ORDER#002
```

**Pattern 3: Reverse Relationship**
```
// Same item, two representations
PK: USER#12345,  SK: ORDER#001
PK: ORDER#001,   SK: USER#12345
```

---

## Primary Keys

### Partition Key Only

```python
# Create table with partition key only
dynamodb = boto3.client('dynamodb')

dynamodb.create_table(
    TableName='Users',
    KeySchema=[
        {'AttributeName': 'userId', 'KeyType': 'HASH'}  # PK only
    ],
    AttributeDefinitions=[
        {'AttributeName': 'userId', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)

# Put item
table.put_item(Item={
    'userId': 'user123',
    'email': 'user@example.com',
    'name': 'Jane Doe'
})

# Get item
response = table.get_item(Key={'userId': 'user123'})
```

### Partition Key + Sort Key

```python
# Create table with composite key
dynamodb.create_table(
    TableName='AppData',
    KeySchema=[
        {'AttributeName': 'PK', 'KeyType': 'HASH'},   # Partition Key
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}   # Sort Key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)
```

### Partition Key Design

**Good Partition Keys:**
- High cardinality (many unique values)
- Even access distribution
- No hot partitions

```python
# GOOD: User ID (unique per user)
PK: "USER#12345"

# GOOD: Composite (tenant + user)
PK: "TENANT#abc#USER#12345"

# BAD: Status (hot partition on "active")
PK: "STATUS#active"  # All active users in one partition!

# BAD: Date (hot partition for current date)
PK: "DATE#2025-11-28"  # All today's writes to one partition!
```

**Fix Hot Partitions:**
```python
# Add random suffix to distribute writes
import random
suffix = random.randint(0, 9)
PK: f"DATE#2025-11-28#{suffix}"
```

---

## Global Secondary Indexes (GSI)

### When to Use GSI

- Query by attributes other than primary key
- Different sort order
- Sparse indexes (not all items have attribute)

### GSI Example: Query Orders by Status

```python
# Base table: PK = userId, SK = timestamp
# GSI: PK = status, SK = timestamp (query all pending orders)

dynamodb.create_table(
    TableName='Orders',
    KeySchema=[
        {'AttributeName': 'userId', 'KeyType': 'HASH'},
        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'userId', 'AttributeType': 'S'},
        {'AttributeName': 'timestamp', 'AttributeType': 'S'},
        {'AttributeName': 'status', 'AttributeType': 'S'}
    ],
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'StatusIndex',
            'KeySchema': [
                {'AttributeName': 'status', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            'Projection': {'ProjectionType': 'ALL'},
            'BillingMode': 'PAY_PER_REQUEST'
        }
    ],
    BillingMode='PAY_PER_REQUEST'
)

# Query GSI
table = dynamodb.Table('Orders')
response = table.query(
    IndexName='StatusIndex',
    KeyConditionExpression=Key('status').eq('pending')
)
```

### GSI Projection Types

```python
# ALL: Project all attributes
'Projection': {'ProjectionType': 'ALL'}

# KEYS_ONLY: Project only keys (smallest index)
'Projection': {'ProjectionType': 'KEYS_ONLY'}

# INCLUDE: Project specific attributes
'Projection': {
    'ProjectionType': 'INCLUDE',
    'NonKeyAttributes': ['email', 'name', 'totalAmount']
}
```

### GSI Best Practices

1. **Use sparse indexes** (only items with attribute are indexed)
2. **Projection**: Use KEYS_ONLY or INCLUDE to reduce storage
3. **Limit GSIs**: Maximum 20 per table
4. **GSI writes**: Every item update may update multiple GSIs (cost!)

---

## Query Patterns

### Query vs Scan

```python
# GOOD: Query (efficient, uses index)
response = table.query(
    KeyConditionExpression=Key('PK').eq('USER#12345')
)

# BAD: Scan (reads entire table, expensive!)
response = table.scan(
    FilterExpression=Attr('email').eq('user@example.com')
)
```

### Query Operators

```python
from boto3.dynamodb.conditions import Key, Attr

# Equals
Key('PK').eq('USER#12345')

# Less than, greater than
Key('timestamp').lt('2025-11-01')
Key('timestamp').gte('2025-11-01')

# Between
Key('timestamp').between('2025-11-01', '2025-11-30')

# Begins with (sort key only)
Key('SK').begins_with('ORDER#')
```

### Filter Expressions (Post-Query Filtering)

```python
# Query + filter (filter after query, doesn't save RCUs)
response = table.query(
    KeyConditionExpression=Key('PK').eq('USER#12345'),
    FilterExpression=Attr('status').eq('active') & Attr('age').gte(18)
)
```

### Pagination

```python
# Paginate through large result sets
last_evaluated_key = None

while True:
    if last_evaluated_key:
        response = table.query(
            KeyConditionExpression=Key('PK').eq('USER#12345'),
            ExclusiveStartKey=last_evaluated_key
        )
    else:
        response = table.query(
            KeyConditionExpression=Key('PK').eq('USER#12345')
        )

    items = response['Items']
    # Process items

    last_evaluated_key = response.get('LastEvaluatedKey')
    if not last_evaluated_key:
        break
```

---

## Update Operations

### Update Expressions

```python
# Set attribute
table.update_item(
    Key={'userId': 'user123'},
    UpdateExpression='SET #name = :name',
    ExpressionAttributeNames={'#name': 'name'},
    ExpressionAttributeValues={':name': 'Jane Smith'}
)

# Increment counter
table.update_item(
    Key={'userId': 'user123'},
    UpdateExpression='SET loginCount = loginCount + :inc',
    ExpressionAttributeValues={':inc': 1}
)

# Add to list
table.update_item(
    Key={'userId': 'user123'},
    UpdateExpression='SET tags = list_append(tags, :tag)',
    ExpressionAttributeValues={':tag': ['new-tag']}
)

# Add to set
table.update_item(
    Key={'userId': 'user123'},
    UpdateExpression='ADD emailSet :email',
    ExpressionAttributeValues={':email': {'user@example.com'}}
)

# Remove attribute
table.update_item(
    Key={'userId': 'user123'},
    UpdateExpression='REMOVE deprecated_field'
)
```

### Conditional Updates

```python
# Update only if condition met
from botocore.exceptions import ClientError

try:
    table.update_item(
        Key={'userId': 'user123'},
        UpdateExpression='SET balance = balance - :amount',
        ConditionExpression='balance >= :amount',
        ExpressionAttributeValues={':amount': 100}
    )
except ClientError as e:
    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        print("Insufficient balance")
```

### Atomic Counters

```python
# Increment view count (atomic)
response = table.update_item(
    Key={'postId': 'post123'},
    UpdateExpression='SET viewCount = if_not_exists(viewCount, :start) + :inc',
    ExpressionAttributeValues={':start': 0, ':inc': 1},
    ReturnValues='UPDATED_NEW'
)
print(f"New count: {response['Attributes']['viewCount']}")
```

---

## DynamoDB Streams

### Enable Change Data Capture

```python
# Create table with streams enabled
dynamodb.create_table(
    TableName='Orders',
    # ... (key schema, attributes)
    StreamSpecification={
        'StreamEnabled': True,
        'StreamViewType': 'NEW_AND_OLD_IMAGES'  # Full document before/after
    }
)
```

### Stream View Types

- `KEYS_ONLY`: Only key attributes
- `NEW_IMAGE`: Entire item after update
- `OLD_IMAGE`: Entire item before update
- `NEW_AND_OLD_IMAGES`: Both before and after

### Process Streams with Lambda

```python
# Lambda function triggered by DynamoDB Stream
def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_item = record['dynamodb']['NewImage']
            print(f"New order: {new_item}")

            # Send notification
            send_email(new_item['email']['S'], "Order Confirmed")

        elif record['eventName'] == 'MODIFY':
            old_item = record['dynamodb']['OldImage']
            new_item = record['dynamodb']['NewImage']

            # Check if status changed
            if old_item['status']['S'] != new_item['status']['S']:
                print(f"Status changed: {old_item['status']['S']} -> {new_item['status']['S']}")

        elif record['eventName'] == 'REMOVE':
            old_item = record['dynamodb']['OldImage']
            print(f"Order deleted: {old_item}")
```

---

## Pricing Optimization

### Billing Modes

| Mode | Use Case | Cost |
|------|----------|------|
| **On-Demand** | Unpredictable traffic, dev/test | $1.25/million writes, $0.25/million reads |
| **Provisioned** | Predictable traffic | $0.47/WCU/month, $0.09/RCU/month |
| **Reserved** | Steady workloads (1-3 year) | Save up to 77% |

### Cost Optimization Strategies

```python
# 1. Use BatchGetItem (up to 100 items)
response = dynamodb.batch_get_item(
    RequestItems={
        'Users': {
            'Keys': [
                {'userId': 'user1'},
                {'userId': 'user2'},
                {'userId': 'user3'}
            ]
        }
    }
)

# 2. Use BatchWriteItem (up to 25 items)
dynamodb.batch_write_item(
    RequestItems={
        'Users': [
            {'PutRequest': {'Item': {'userId': 'user1', 'name': 'User 1'}}},
            {'PutRequest': {'Item': {'userId': 'user2', 'name': 'User 2'}}}
        ]
    }
)

# 3. Use projection expressions (fetch only needed attributes)
response = table.query(
    KeyConditionExpression=Key('PK').eq('USER#12345'),
    ProjectionExpression='email, #name, createdAt',
    ExpressionAttributeNames={'#name': 'name'}
)

# 4. Use eventually consistent reads (half the RCUs)
response = table.get_item(
    Key={'userId': 'user123'},
    ConsistentRead=False  # Default
)

# 5. Use TTL for auto-expiring data (free deletes!)
table.meta.client.update_time_to_live(
    TableName='Sessions',
    TimeToLiveSpecification={
        'Enabled': True,
        'AttributeName': 'ttl'
    }
)

# Add TTL to item (Unix timestamp)
import time
ttl_value = int(time.time()) + 86400  # Expire in 24 hours
table.put_item(Item={
    'sessionId': 'session123',
    'ttl': ttl_value
})
```

---

## Performance Best Practices

### Design for Even Distribution

```python
# GOOD: High cardinality partition key
PK: f"USER#{uuid.uuid4()}"

# GOOD: Composite key with multiple dimensions
PK: f"TENANT#{tenant_id}#USER#{user_id}"

# BAD: Low cardinality (hot partitions)
PK: f"STATUS#{status}"  # Only 3 values: active, pending, archived
```

### Use Sparse Indexes

```python
# Only index items with specific attribute (saves storage)
# GSI: PK = emailVerified, SK = timestamp
# Only items with emailVerified=true are indexed

table.put_item(Item={
    'userId': 'user123',
    'email': 'user@example.com',
    'emailVerified': True,  # This item appears in GSI
    'timestamp': '2025-11-28T10:00:00Z'
})

table.put_item(Item={
    'userId': 'user456',
    'email': 'other@example.com',
    # No emailVerified - this item NOT in GSI
    'timestamp': '2025-11-28T11:00:00Z'
})
```

### Adjacent Item Pattern (Reduce Queries)

```python
# Store related items with adjacent sort keys
# Query once, get all related data

# User metadata
PK: "USER#12345",  SK: "A#METADATA"

# User's addresses
PK: "USER#12345",  SK: "B#ADDRESS#001"
PK: "USER#12345",  SK: "B#ADDRESS#002"

# User's orders (most recent first)
PK: "USER#12345",  SK: "C#ORDER#2025-11-28#001"
PK: "USER#12345",  SK: "C#ORDER#2025-11-27#002"

# One query gets everything
response = table.query(
    KeyConditionExpression=Key('PK').eq('USER#12345')
)
```

### Composite Sort Keys

```python
# Hierarchical data in sort key
SK: "COUNTRY#USA#STATE#MA#CITY#Boston"

# Query all items in USA
Key('SK').begins_with('COUNTRY#USA')

# Query all items in Massachusetts
Key('SK').begins_with('COUNTRY#USA#STATE#MA')

# Query all items in Boston
Key('SK').begins_with('COUNTRY#USA#STATE#MA#CITY#Boston')
```

---

## TypeScript Examples (AWS SDK v3)

```typescript
import {
  DynamoDBClient,
  PutItemCommand,
  GetItemCommand,
  QueryCommand,
  UpdateItemCommand
} from '@aws-sdk/client-dynamodb'
import { marshall, unmarshall } from '@aws-sdk/util-dynamodb'

const client = new DynamoDBClient({ region: 'us-east-1' })

// Put item
await client.send(new PutItemCommand({
  TableName: 'Users',
  Item: marshall({
    userId: 'user123',
    email: 'user@example.com',
    name: 'Jane Doe',
    createdAt: new Date().toISOString()
  })
}))

// Get item
const response = await client.send(new GetItemCommand({
  TableName: 'Users',
  Key: marshall({ userId: 'user123' })
}))
const user = unmarshall(response.Item!)

// Query
const queryResponse = await client.send(new QueryCommand({
  TableName: 'Orders',
  KeyConditionExpression: 'PK = :pk',
  ExpressionAttributeValues: marshall({
    ':pk': 'USER#12345'
  })
}))
const items = queryResponse.Items!.map(item => unmarshall(item))

// Update
await client.send(new UpdateItemCommand({
  TableName: 'Users',
  Key: marshall({ userId: 'user123' }),
  UpdateExpression: 'SET #name = :name',
  ExpressionAttributeNames: { '#name': 'name' },
  ExpressionAttributeValues: marshall({ ':name': 'Jane Smith' })
}))
```

---

## Common Patterns

### Multi-Tenant Architecture

```python
# Partition by tenant
PK: "TENANT#abc#USER#12345"
SK: "METADATA"

# Query all users in tenant
response = table.query(
    KeyConditionExpression=Key('PK').begins_with('TENANT#abc#USER#')
)
```

### Time-Series Data

```python
# Partition by entity, sort by timestamp
PK: "SENSOR#sensor123"
SK: "2025-11-28T10:30:45.123Z"

# Query range
response = table.query(
    KeyConditionExpression=Key('PK').eq('SENSOR#sensor123') &
                          Key('SK').between('2025-11-28T00:00:00Z', '2025-11-28T23:59:59Z')
)

# Use GSI for cross-sensor queries
# GSI: PK = date, SK = sensorId
```

### Versioning

```python
# Store versions with sort key
PK: "DOC#doc123"
SK: "VERSION#001"
SK: "VERSION#002"
SK: "VERSION#003"

# Get latest version
response = table.query(
    KeyConditionExpression=Key('PK').eq('DOC#doc123'),
    ScanIndexForward=False,  # Descending order
    Limit=1
)
```

---

This guide covers DynamoDB single-table design and AWS-specific patterns. For Python FastAPI + MongoDB examples, see `../examples/dynamodb-serverless/`.
