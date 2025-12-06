# AWS Serverless Architecture Patterns

## Table of Contents

- [Lambda Function Patterns](#lambda-function-patterns)
- [API Gateway Patterns](#api-gateway-patterns)
- [Step Functions Orchestration](#step-functions-orchestration)
- [EventBridge Patterns](#eventbridge-patterns)
- [DynamoDB Integration](#dynamodb-integration)
- [Lambda SnapStart Configuration](#lambda-snapstart-configuration)
- [Response Streaming](#response-streaming)
- [Error Handling and Retry Logic](#error-handling-and-retry-logic)
- [Performance Optimization](#performance-optimization)
- [Anti-Patterns](#anti-patterns)

## Lambda Function Patterns

### Basic REST API Handler

**Pattern:** Single Lambda function handling HTTP requests through API Gateway.

**Use When:**
- Building CRUD APIs with predictable traffic
- Execution time under 15 minutes
- Need automatic scaling
- Cost optimization for variable workloads

**Architecture:**
```
API Gateway HTTP API → Lambda Function → DynamoDB/RDS
                                      → S3 (optional)
```

**Key Configuration:**
```yaml
# Lambda configuration
Runtime: python3.12 or nodejs20.x
Memory: 1024 MB (price-performance sweet spot)
Timeout: 30 seconds (API Gateway limit)
ReservedConcurrency: null (unlimited scaling)
ProvisionedConcurrency: 0 (avoid unless cold start critical)
```

**Cost Characteristics:**
- Free tier: 1M requests/month, 400,000 GB-seconds compute
- Beyond free tier: $0.20 per 1M requests + $0.0000166667 per GB-second
- 1M requests at 1GB memory, 500ms duration: ~$4.17/month

**Memory Allocation Guidance:**
- 128-256 MB: Simple data transformations, S3 processing
- 512-1024 MB: API handlers, moderate database queries
- 1536-3008 MB: Complex processing, ML inference, heavy I/O
- 10240 MB: Maximum, for CPU-intensive workloads

### Event-Driven Processing

**Pattern:** Lambda triggered by events from S3, DynamoDB Streams, or EventBridge.

**Architecture:**
```
S3 Upload → EventBridge Event → Lambda (transform) → DynamoDB (metadata)
                                                   → SQS (downstream)
```

**Configuration for Event Sources:**

**S3 Event:**
```yaml
EventSourceArn: !GetAtt MyBucket.Arn
Events:
  - s3:ObjectCreated:*
Filter:
  S3Key:
    Rules:
      - Name: prefix
        Value: uploads/
      - Name: suffix
        Value: .csv
```

**DynamoDB Stream:**
```yaml
EventSourceArn: !GetAtt MyTable.StreamArn
StartingPosition: LATEST
BatchSize: 100
MaximumBatchingWindowInSeconds: 10
ParallelizationFactor: 10  # Process 10 shards concurrently
```

**Batch Processing Configuration:**
- BatchSize: 1-10,000 for SQS/Kinesis
- MaximumBatchingWindowInSeconds: 0-300 (wait for batch to fill)
- ParallelizationFactor: 1-10 (concurrent executions per shard)

### Scheduled Task Pattern

**Pattern:** Lambda function running on schedule using EventBridge Rules.

**Use When:**
- Periodic data processing (ETL jobs)
- Cleanup tasks (delete expired records)
- Report generation
- Health checks and monitoring

**EventBridge Schedule Syntax:**
```
rate(5 minutes)                    # Every 5 minutes
rate(1 hour)                       # Every hour
rate(1 day)                        # Daily
cron(0 9 * * ? *)                 # 9 AM UTC daily
cron(0 0 ? * MON-FRI *)           # Midnight weekdays
cron(0/15 * * * ? *)              # Every 15 minutes
```

**Best Practices:**
- Use UTC timezone for cron expressions
- Set appropriate timeout (max 15 minutes)
- Implement idempotency (safe to retry)
- Use CloudWatch Logs for debugging

## API Gateway Patterns

### HTTP API vs REST API

**Decision Matrix:**

| Feature | HTTP API | REST API |
|---------|----------|----------|
| Cost | $1.00/million | $3.50/million |
| Latency | ~35% lower | Standard |
| JWT Authorization | Native | Custom authorizer needed |
| Request Validation | No | Yes |
| API Keys | No | Yes |
| Usage Plans | No | Yes |
| WebSocket | Separate | No |

**Recommendation:** Use HTTP API for 90% of use cases. Use REST API only when request validation, API keys, or usage plans required.

### Lambda Proxy Integration

**Pattern:** Pass entire request to Lambda, return entire response.

**Request Format Received:**
```json
{
  "version": "2.0",
  "routeKey": "POST /items",
  "rawPath": "/items",
  "headers": {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
  },
  "queryStringParameters": {
    "filter": "active"
  },
  "body": "{\"name\":\"item1\"}",
  "isBase64Encoded": false,
  "requestContext": {
    "requestId": "abc123",
    "http": {
      "method": "POST",
      "path": "/items"
    }
  }
}
```

**Required Response Format:**
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"message\":\"Success\"}"
}
```

**Common Errors:**
- Missing statusCode field (required)
- Body not stringified (must be string, not object)
- Incorrect header names (case-sensitive)

### CORS Configuration

**For HTTP API:**
```yaml
CorsConfiguration:
  AllowOrigins:
    - https://example.com
  AllowMethods:
    - GET
    - POST
    - PUT
    - DELETE
  AllowHeaders:
    - Content-Type
    - Authorization
  MaxAge: 300
  AllowCredentials: true
```

**For REST API:**
Must implement OPTIONS method with CORS headers in Lambda response.

### Custom Domain Names

**Pattern:** Map custom domain to API Gateway endpoint.

**Requirements:**
1. ACM certificate in us-east-1 (for edge-optimized) or same region (for regional)
2. Route 53 hosted zone or external DNS provider
3. API mapping configuration

**Configuration:**
```yaml
DomainName:
  DomainName: api.example.com
  CertificateArn: arn:aws:acm:us-east-1:123456789012:certificate/abc
  EndpointConfiguration:
    Types:
      - REGIONAL  # or EDGE for CloudFront distribution

ApiMapping:
  DomainName: api.example.com
  ApiId: !Ref HttpApi
  Stage: prod
  ApiMappingKey: v1  # results in api.example.com/v1
```

## Step Functions Orchestration

### Express Workflows vs Standard Workflows

**Decision Matrix:**

| Feature | Express Workflow | Standard Workflow |
|---------|-----------------|-------------------|
| Max Duration | 5 minutes | 1 year |
| Pricing Model | Per execution | Per state transition |
| Execution Guarantee | At-least-once | Exactly-once |
| Execution History | CloudWatch Logs | Built-in (90 days) |
| Cost (1M executions) | $1.00 | $25.00 |

**Use Cases:**
- **Express:** API response orchestration, real-time data processing
- **Standard:** Long-running workflows, ETL pipelines, human approval

### Common State Types

**Task State (Lambda Invocation):**
```json
{
  "ProcessData": {
    "Type": "Task",
    "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ProcessFunction",
    "TimeoutSeconds": 300,
    "Retry": [{
      "ErrorEquals": ["States.TaskFailed"],
      "IntervalSeconds": 2,
      "MaxAttempts": 3,
      "BackoffRate": 2.0
    }],
    "Catch": [{
      "ErrorEquals": ["States.ALL"],
      "Next": "HandleError"
    }],
    "Next": "NextState"
  }
}
```

**Choice State (Conditional Branching):**
```json
{
  "CheckStatus": {
    "Type": "Choice",
    "Choices": [{
      "Variable": "$.status",
      "StringEquals": "SUCCESS",
      "Next": "SuccessState"
    }, {
      "Variable": "$.status",
      "StringEquals": "FAILED",
      "Next": "FailureState"
    }],
    "Default": "DefaultState"
  }
}
```

**Map State (Parallel Processing):**
```json
{
  "ProcessItems": {
    "Type": "Map",
    "ItemsPath": "$.items",
    "MaxConcurrency": 10,
    "Iterator": {
      "StartAt": "ProcessItem",
      "States": {
        "ProcessItem": {
          "Type": "Task",
          "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ProcessItem",
          "End": true
        }
      }
    },
    "Next": "Aggregate"
  }
}
```

### Distributed Map (2024+ Feature)

**Use When:**
- Processing thousands to millions of items
- Items stored in S3 (JSON array or CSV)
- Need massive parallelism (10,000+ concurrent executions)

**Configuration:**
```json
{
  "ProcessLargeDataset": {
    "Type": "Map",
    "ItemReader": {
      "Resource": "arn:aws:states:::s3:getObject",
      "Parameters": {
        "Bucket": "my-bucket",
        "Key": "data.json"
      }
    },
    "ItemSelector": {
      "item.$": "$$.Map.Item.Value"
    },
    "MaxConcurrency": 10000,
    "ToleratedFailurePercentage": 5,
    "ResultWriter": {
      "Resource": "arn:aws:states:::s3:putObject",
      "Parameters": {
        "Bucket": "output-bucket",
        "Prefix": "results/"
      }
    },
    "Iterator": {
      "StartAt": "ProcessItem",
      "States": {
        "ProcessItem": {
          "Type": "Task",
          "Resource": "arn:aws:lambda:us-east-1:123456789012:function:Process",
          "End": true
        }
      }
    }
  }
}
```

**Performance:**
- Can process millions of items in minutes
- Automatic result aggregation to S3
- Built-in fault tolerance

## EventBridge Patterns

### Event-Driven Architecture

**Pattern:** Decouple producers and consumers using EventBridge.

**Architecture:**
```
Producer Service → EventBridge Event Bus → EventBridge Rule → Target (Lambda/SQS/Step Functions)
                                                            → Target (Additional consumers)
```

**Event Pattern Matching:**
```json
{
  "source": ["myapp.orders"],
  "detail-type": ["Order Placed"],
  "detail": {
    "amount": [{"numeric": [">=", 100]}],
    "status": ["confirmed"]
  }
}
```

**Advanced Filtering:**
```json
{
  "source": ["myapp.users"],
  "detail": {
    "location": {
      "state": [
        {"prefix": "US-"},
        "CA-BC",
        "CA-ON"
      ]
    },
    "metadata": {
      "plan": [
        {"anything-but": "free"}
      ]
    }
  }
}
```

### EventBridge Pipes (2023+ Feature)

**Pattern:** Simplified event processing with built-in filtering and enrichment.

**Architecture:**
```
Source (SQS/Kinesis/DynamoDB) → Filter → Enrichment (Lambda/API) → Target
```

**Use When:**
- Need to filter events before processing
- Require data enrichment from external API
- Want simpler configuration than Lambda + EventBridge

**Configuration:**
```yaml
Pipe:
  Source: !GetAtt SourceQueue.Arn
  SourceParameters:
    SqsQueueParameters:
      BatchSize: 10
      MaximumBatchingWindowInSeconds: 5

  Filter:
    Pattern: |
      {
        "body": {
          "amount": [{"numeric": [">", 100]}]
        }
      }

  Enrichment: !GetAtt EnrichmentFunction.Arn
  EnrichmentParameters:
    InputTemplate: |
      {
        "orderId": <$.body.orderId>,
        "customerId": <$.body.customerId>
      }

  Target: !GetAtt TargetFunction.Arn
  TargetParameters:
    InputTemplate: |
      {
        "enrichedData": <$.body>,
        "timestamp": <$.metadata.timestamp>
      }
```

**Benefits:**
- No custom Lambda code for routing
- Built-in transformation using JSONPath
- Automatic retries and DLQ support

### Schema Registry

**Pattern:** Define and version event schemas for type safety.

**Benefits:**
- Auto-generate code bindings (Java, Python, TypeScript)
- Schema validation
- Version management
- Discovery of available events

**Example Schema:**
```json
{
  "openapi": "3.0.0",
  "info": {
    "version": "1.0.0",
    "title": "OrderPlaced"
  },
  "paths": {},
  "components": {
    "schemas": {
      "OrderPlaced": {
        "type": "object",
        "required": ["orderId", "customerId", "amount"],
        "properties": {
          "orderId": {
            "type": "string",
            "format": "uuid"
          },
          "customerId": {
            "type": "string"
          },
          "amount": {
            "type": "number",
            "minimum": 0
          },
          "status": {
            "type": "string",
            "enum": ["pending", "confirmed", "shipped"]
          }
        }
      }
    }
  }
}
```

## DynamoDB Integration

### Single-Table Design

**Pattern:** Store multiple entity types in one table using GSIs.

**Primary Key Design:**
```
PK: CUSTOMER#123         SK: METADATA
PK: CUSTOMER#123         SK: ORDER#456
PK: CUSTOMER#123         SK: ORDER#789
PK: ORDER#456            SK: METADATA
PK: ORDER#456            SK: ITEM#1
```

**Access Patterns:**
1. Get customer: Query PK=CUSTOMER#123, SK begins_with METADATA
2. Get customer orders: Query PK=CUSTOMER#123, SK begins_with ORDER#
3. Get order details: Query PK=ORDER#456

**GSI for Inverted Access:**
```
GSI1PK: ORDER#456        GSI1SK: CUSTOMER#123
GSI1PK: ORDER#789        GSI1SK: CUSTOMER#123
```

Query orders by customer using GSI1PK=CUSTOMER#123.

### Lambda + DynamoDB Best Practices

**Batch Operations:**
```python
# Use batch_write_item for multiple puts (25 items max)
dynamodb.batch_write_item(
    RequestItems={
        'MyTable': [
            {'PutRequest': {'Item': item1}},
            {'PutRequest': {'Item': item2}},
        ]
    }
)

# Use batch_get_item for multiple reads (100 items max)
response = dynamodb.batch_get_item(
    RequestItems={
        'MyTable': {
            'Keys': [
                {'PK': 'CUSTOMER#123', 'SK': 'METADATA'},
                {'PK': 'CUSTOMER#456', 'SK': 'METADATA'},
            ]
        }
    }
)
```

**Connection Reuse:**
```python
# Initialize client OUTSIDE handler for reuse
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')

def lambda_handler(event, context):
    # Reuses existing connection
    response = table.get_item(Key={'PK': 'CUSTOMER#123', 'SK': 'METADATA'})
```

**DynamoDB Streams Processing:**
```python
def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_item = record['dynamodb']['NewImage']
            # Process new item
        elif record['eventName'] == 'MODIFY':
            old_item = record['dynamodb']['OldImage']
            new_item = record['dynamodb']['NewImage']
            # Process update
        elif record['eventName'] == 'REMOVE':
            old_item = record['dynamodb']['OldImage']
            # Process deletion
```

## Lambda SnapStart Configuration

### Java Cold Start Optimization

**Use When:**
- Using Java 11 or Java 17 runtime
- Cold start latency is critical (APIs, synchronous processing)
- Application initialization is expensive (framework startup, connection pools)

**Performance Improvement:**
- Cold start: 10-15 seconds → 200-500 milliseconds
- Warm start: No change (still fast)
- Cost: Same as regular Lambda

**Configuration:**
```yaml
Function:
  Runtime: java17
  SnapStart:
    ApplyOn: PublishedVersions
  AutoPublishAlias: live
```

**Requirements:**
1. Must use published versions (not $LATEST)
2. Must use alias pointing to version
3. Invoke alias ARN, not function ARN

**Code Considerations:**

**Avoid:**
```java
// Network connections in initialization
private static HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();  // Don't create in static initializer
```

**Prefer:**
```java
// Lazy initialization
private static HttpClient client;

private static HttpClient getClient() {
    if (client == null) {
        client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .build();
    }
    return client;
}
```

**Uniqueness Requirements:**
- Generate unique IDs in handler, not initialization
- Refresh credentials on each invocation
- Don't cache sensitive data in static variables

## Response Streaming

### Large Response Pattern (2023+ Feature)

**Use When:**
- Response size exceeds 6 MB (synchronous limit)
- Need to stream data to client incrementally
- Generating large reports or files

**Maximum Size:**
- Standard response: 6 MB
- Streaming response: 20 MB

**Configuration:**
```yaml
Function:
  Runtime: nodejs20.x or python3.12
  InvokeMode: RESPONSE_STREAM
```

**Python Implementation:**
```python
def lambda_handler(event, context):
    def generate_data():
        # Stream data in chunks
        for i in range(1000):
            yield json.dumps({'chunk': i}) + '\n'

    return generate_data()
```

**Node.js Implementation:**
```javascript
import { Readable } from 'stream';

export const handler = awslambda.streamifyResponse(
    async (event, responseStream, context) => {
        const stream = Readable.from(generateData());
        stream.pipe(responseStream);
    }
);

function* generateData() {
    for (let i = 0; i < 1000; i++) {
        yield JSON.stringify({ chunk: i }) + '\n';
    }
}
```

**API Gateway Integration:**
Not supported with API Gateway. Use Lambda Function URL.

**Function URL Configuration:**
```yaml
FunctionUrl:
  AuthType: AWS_IAM  # or NONE for public
  InvokeMode: RESPONSE_STREAM
  Cors:
    AllowOrigins:
      - '*'
    AllowMethods:
      - GET
      - POST
```

## Error Handling and Retry Logic

### Retry Configuration

**Automatic Retries by Invocation Type:**

| Invocation Type | Retries | Use Case |
|----------------|---------|----------|
| Synchronous (API Gateway) | 0 | Client should retry |
| Asynchronous (S3, EventBridge) | 2 | AWS retries automatically |
| Event Source (SQS, Kinesis) | Until success or TTL | Configurable |

**Custom Retry Configuration:**
```yaml
EventSourceMapping:
  FunctionName: !Ref ProcessFunction
  EventSourceArn: !GetAtt MyQueue.Arn
  MaximumRetryAttempts: 3
  MaximumRecordAgeInSeconds: 3600  # Discard after 1 hour
  BisectBatchOnFunctionError: true  # Split failed batch
```

**Asynchronous Retry Configuration:**
```yaml
Function:
  EventInvokeConfig:
    MaximumRetryAttempts: 1  # 0-2 retries
    MaximumEventAgeInSeconds: 3600  # Discard after 1 hour
    DestinationConfig:
      OnSuccess:
        Destination: !GetAtt SuccessQueue.Arn
      OnFailure:
        Destination: !GetAtt DLQ.Arn
```

### Dead Letter Queue (DLQ)

**Pattern:** Send failed events to SQS or SNS for manual processing.

**Configuration:**
```yaml
Function:
  DeadLetterConfig:
    TargetArn: !GetAtt DLQ.Arn

DLQ:
  Type: AWS::SQS::Queue
  Properties:
    MessageRetentionPeriod: 1209600  # 14 days
    VisibilityTimeout: 300
```

**DLQ Processing:**
```python
# Separate Lambda to process DLQ
def dlq_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        # Log to CloudWatch or external monitoring
        logger.error(f"Failed event: {body}")
        # Send alert to SNS/PagerDuty
        # Store in S3 for analysis
```

### Idempotency

**Pattern:** Ensure safe retries using idempotency keys.

**Implementation (Python):**
```python
import boto3
import hashlib
import json

dynamodb = boto3.resource('dynamodb')
idempotency_table = dynamodb.Table('IdempotencyTable')

def lambda_handler(event, context):
    # Generate idempotency key from event
    key = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # Check if already processed
    try:
        response = idempotency_table.get_item(Key={'RequestId': key})
        if 'Item' in response:
            # Already processed, return cached result
            return json.loads(response['Item']['Result'])
    except Exception as e:
        logger.error(f"Idempotency check failed: {e}")

    # Process event
    result = process_event(event)

    # Store result
    try:
        idempotency_table.put_item(
            Item={
                'RequestId': key,
                'Result': json.dumps(result),
                'TTL': int(time.time()) + 86400  # 24 hours
            }
        )
    except Exception as e:
        logger.error(f"Failed to store idempotency: {e}")

    return result
```

## Performance Optimization

### Memory vs CPU Tradeoff

**Key Insight:** CPU allocation scales linearly with memory.

| Memory | vCPU | Best For |
|--------|------|----------|
| 128 MB | 0.083 vCPU | Simple transformations |
| 512 MB | 0.33 vCPU | Light API handlers |
| 1024 MB | 0.67 vCPU | General purpose |
| 1769 MB | 1.0 vCPU | CPU-bound tasks |
| 3538 MB | 2.0 vCPU | Heavy processing |
| 10240 MB | 6.0 vCPU | Maximum performance |

**Cost vs Performance:**
- 128 MB, 1000ms = $0.0000002083 per invocation
- 1024 MB, 125ms = $0.0000002083 per invocation (8x faster, same cost!)

**Recommendation:** Use AWS Lambda Power Tuning to find optimal memory.

### Connection Pooling

**Pattern:** Reuse database connections across invocations.

**RDS Connection Pooling:**
```python
import pymysql

# Initialize OUTSIDE handler
connection = None

def get_connection():
    global connection
    if connection is None or not connection.open:
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor
        )
    return connection

def lambda_handler(event, context):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (event['userId'],))
        result = cursor.fetchone()
    return result
```

**RDS Proxy (Recommended):**
- Manages connection pooling automatically
- Reduces overhead by 66%+
- Built-in failover
- IAM authentication support

**Configuration:**
```yaml
DBProxy:
  Type: AWS::RDS::DBProxy
  Properties:
    EngineFamily: POSTGRESQL
    Auth:
      - AuthScheme: SECRETS
        SecretArn: !Ref DBSecret
    RoleArn: !GetAtt ProxyRole.Arn
    VpcSubnetIds:
      - !Ref PrivateSubnet1
      - !Ref PrivateSubnet2
```

### Provisioned Concurrency

**Use When:**
- Cold starts are unacceptable (<100ms p99 required)
- Predictable high traffic (not cost-effective for variable traffic)
- Cost is secondary to performance

**Cost Model:**
- Provisioned concurrency: $0.0000041667 per GB-second
- On-demand: $0.0000166667 per GB-second
- Provisioned is always running (charged even when idle)

**Configuration:**
```yaml
Function:
  ProvisionedConcurrencyConfig:
    ProvisionedConcurrentExecutions: 10
    AutoScalingConfig:
      MinCapacity: 5
      MaxCapacity: 100
      TargetValue: 0.70  # 70% utilization
```

**Application Auto Scaling:**
```yaml
ScalableTarget:
  ServiceNamespace: lambda
  ResourceId: !Sub "function:${FunctionName}:${Alias}"
  ScalableDimension: lambda:function:ProvisionedConcurrency
  MinCapacity: 5
  MaxCapacity: 100

ScalingPolicy:
  PolicyType: TargetTrackingScaling
  TargetTrackingScalingPolicyConfiguration:
    TargetValue: 0.70
    PredefinedMetricSpecification:
      PredefinedMetricType: LambdaProvisionedConcurrencyUtilization
```

## Anti-Patterns

### Don't: Run Long-Running Tasks

**Problem:** Lambda has 15-minute timeout limit.

**Solution:** Use Step Functions, ECS Fargate, or Batch.

### Don't: Store State in /tmp

**Problem:** /tmp is ephemeral and limited to 512 MB (10 GB in 2024+).

**Solution:** Use S3, EFS, or ElastiCache for persistent storage.

### Don't: Use Lambda for Predictable High Traffic

**Problem:** More expensive than Fargate/EC2 at constant utilization.

**Breakeven Analysis:**
- Lambda: $0.0000166667 per GB-second
- Fargate (1 vCPU, 2GB): $0.000011 per GB-second at 100% utilization

**Solution:** Use Fargate or EC2 for always-on workloads.

### Don't: Hardcode Configuration

**Problem:** Requires redeployment for configuration changes.

**Solution:** Use environment variables, Parameter Store, or AppConfig.

### Don't: Ignore Cold Start Impact

**Problem:** First invocation is slow (Java: 10-15s, Python: 200-500ms).

**Solutions:**
1. Use SnapStart (Java only)
2. Provision concurrency (expensive)
3. Keep functions warm (cron trigger)
4. Minimize dependencies
5. Use lighter runtimes (Node.js, Python over Java)

### Don't: Process Large Files in Lambda

**Problem:** 512 MB - 10 GB memory limit, 15-minute timeout.

**Solution:** Use S3 Select, Athena, or EMR for large data processing.

### Don't: Synchronous Step Functions for APIs

**Problem:** Express workflows have 5-minute limit, standard workflows are slow.

**Solution:** Use direct Lambda integration or asynchronous workflows.

### Don't: Ignore Concurrent Execution Limits

**Problem:** Account limit of 1,000 concurrent executions (can request increase).

**Solution:**
1. Request limit increase
2. Use reserved concurrency to prevent throttling
3. Implement backpressure (SQS rate limiting)
4. Use Provisioned Concurrency for critical functions

### Don't: Skip VPC Best Practices

**Problem:** Lambda in VPC requires ENIs (slow cold starts pre-2019).

**Modern Solution (Post-2019):**
- Hyperplane ENIs (shared across functions)
- No cold start penalty
- Use VPC for RDS/ElastiCache access
- Use VPC endpoints for AWS services (avoid NAT Gateway costs)

**Configuration:**
```yaml
Function:
  VpcConfig:
    SecurityGroupIds:
      - !Ref LambdaSecurityGroup
    SubnetIds:
      - !Ref PrivateSubnet1
      - !Ref PrivateSubnet2
```
