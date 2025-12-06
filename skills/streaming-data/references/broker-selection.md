# Message Broker Selection Guide

## Table of Contents
- [Overview](#overview)
- [Apache Kafka](#apache-kafka)
- [Apache Pulsar](#apache-pulsar)
- [Redpanda](#redpanda)
- [RabbitMQ](#rabbitmq)
- [Comparison Matrix](#comparison-matrix)
- [Selection Flowchart](#selection-flowchart)

## Overview

Choose a message broker based on throughput requirements, latency constraints, operational complexity, and ecosystem maturity.

## Apache Kafka

### Architecture
- Partitioned log-based storage
- Consumer groups for load balancing
- ZooKeeper dependency (KRaft mode available)
- Distributed, fault-tolerant

### Strengths
- Very high throughput (millions of messages/sec)
- Durability and event replay capability
- Massive ecosystem (Kafka Connect, Schema Registry, ksqlDB)
- Exactly-once semantics support
- Battle-tested at scale

### Weaknesses
- Operational complexity (JVM tuning, ZooKeeper management)
- Higher tail latency under load vs alternatives
- Resource-intensive (memory, disk, network)

### Best Use Cases
- Event sourcing and CQRS architectures
- Data pipeline integration (150+ Kafka Connect connectors)
- High-throughput batch workloads (fintech, analytics)
- Enterprise systems with mature tooling requirements
- Log and metrics aggregation

### Configuration Recommendations

**Broker Settings**:
```properties
# Replication for fault tolerance
replication.factor=3
min.insync.replicas=2

# Performance tuning
num.network.threads=8
num.io.threads=8
socket.send.buffer.bytes=1048576
socket.receive.buffer.bytes=1048576
```

**Producer Settings**:
```properties
# Exactly-once
enable.idempotence=true
acks=all
retries=Integer.MAX_VALUE
max.in.flight.requests.per.connection=5

# Performance
compression.type=lz4
batch.size=32768
linger.ms=10
```

## Apache Pulsar

### Architecture
- Layered architecture (brokers + BookKeeper storage)
- Separate compute and storage layers
- Native multi-tenancy support
- Tiered storage (hot/cold data separation)

### Strengths
- Excellent multi-tenancy isolation
- Geo-replication and cross-datacenter sync
- Independent scaling of compute and storage
- Schema evolution built-in
- Pulsar Functions (lightweight stream processing)

### Weaknesses
- Higher operational complexity (ZooKeeper + BookKeeper)
- Smaller ecosystem compared to Kafka
- More moving parts (brokers, bookies, ZooKeeper)

### Best Use Cases
- Multi-tenant SaaS platforms
- IoT platforms with millions of topics
- Cross-region data synchronization
- Applications requiring tiered storage
- Dynamic scaling requirements

### Configuration Recommendations

**Broker Settings**:
```properties
# Multi-tenancy
numTenants=1000
maxTopicsPerNamespace=10000

# Tiered storage
managedLedgerOffloadDriver=aws-s3
s3ManagedLedgerOffloadBucket=pulsar-offload
```

**Producer Settings**:
```java
Producer<byte[]> producer = client.newProducer()
    .topic("persistent://tenant/namespace/topic")
    .batchingMaxMessages(1000)
    .compressionType(CompressionType.LZ4)
    .create();
```

## Redpanda

### Architecture
- Single-binary deployment (C++ implementation)
- Raft consensus (no ZooKeeper dependency)
- Kafka-compatible API
- Thread-per-core design for CPU efficiency

### Strengths
- Lower latency than Kafka (especially tail latency)
- Simpler operations (no JVM, no ZooKeeper)
- Better CPU and memory utilization
- Drop-in Kafka replacement (API compatible)
- Fewer nodes needed (cost savings)

### Weaknesses
- Smaller ecosystem than Kafka
- Less mature tooling
- Newer project (less battle-tested)

### Best Use Cases
- Performance-critical applications (low-latency requirements)
- Edge computing and resource-constrained environments
- Kafka replacements seeking operational simplicity
- Cost optimization (fewer nodes for same throughput)
- Greenfield projects with performance focus

### Configuration Recommendations

**Broker Settings**:
```yaml
# redpanda.yaml
redpanda:
  data_directory: /var/lib/redpanda/data
  node_id: 1
  rpc_server:
    address: 0.0.0.0
    port: 33145
  kafka_api:
    - address: 0.0.0.0
      port: 9092
  admin:
    - address: 0.0.0.0
      port: 9644

# Performance tuning
pandaproxy_client:
  retries: 10
  retry_base_backoff_ms: 100
```

## RabbitMQ

### Architecture
- Queue-based (not log-based)
- AMQP, MQTT, STOMP protocol support
- Flexible routing (exchanges, bindings)
- Message acknowledgements

### Strengths
- Flexible message routing patterns
- Priority queues and message TTL
- Easy to set up and operate
- Rich plugin ecosystem
- Good for RPC patterns

### Weaknesses
- No event replay capability
- Lower throughput than Kafka/Pulsar/Redpanda
- Not designed for event streaming use cases

### Best Use Cases
- Task queues and job processing
- RPC communication patterns
- Traditional message queue use cases
- Microservices async communication (non-streaming)

### Configuration Recommendations

**RabbitMQ Config**:
```erlang
# rabbitmq.conf
vm_memory_high_watermark.relative = 0.6
disk_free_limit.absolute = 50GB
consumer_timeout = 3600000

# Clustering
cluster_formation.peer_discovery_backend = rabbit_peer_discovery_k8s
```

## Comparison Matrix

### Performance Characteristics

| Feature | Kafka | Pulsar | Redpanda | RabbitMQ |
|---------|-------|--------|----------|----------|
| **Throughput** | Very High (100k+ msg/s) | High (50k+ msg/s) | Very High (100k+ msg/s) | Medium (10k-50k msg/s) |
| **Latency (p99)** | 20-100ms | 20-100ms | 5-50ms | 5-20ms |
| **Event Replay** | Yes | Yes | Yes | No |
| **Persistence** | Disk (log segments) | BookKeeper | Disk (log segments) | Disk/Memory |
| **Retention** | Time/Size-based | Time/Size-based | Time/Size-based | Queue-based |

### Operational Characteristics

| Feature | Kafka | Pulsar | Redpanda | RabbitMQ |
|---------|-------|--------|----------|----------|
| **Deployment Complexity** | Medium | High | Low | Low |
| **Dependencies** | ZooKeeper (or KRaft) | ZooKeeper + BookKeeper | None (Raft) | None |
| **Resource Usage** | High (JVM) | High | Low (C++) | Medium |
| **Scaling** | Add brokers | Independent compute/storage | Add brokers | Add nodes |
| **Monitoring** | JMX, Prometheus | Prometheus | Prometheus | Management UI |

### Ecosystem Maturity

| Feature | Kafka | Pulsar | Redpanda | RabbitMQ |
|---------|-------|--------|----------|----------|
| **Client Libraries** | Excellent | Good | Kafka-compatible | Excellent |
| **Connectors** | 150+ (Kafka Connect) | Good (Pulsar IO) | Kafka-compatible | Plugin-based |
| **Stream Processing** | Kafka Streams, ksqlDB | Pulsar Functions | Kafka-compatible | Limited |
| **Schema Registry** | Confluent Schema Registry | Built-in | Compatible | N/A |
| **Community Size** | Very Large | Medium | Growing | Large |

### Cost Considerations

| Factor | Kafka | Pulsar | Redpanda | RabbitMQ |
|--------|-------|--------|----------|----------|
| **Hardware Requirements** | High | High | Medium | Low-Medium |
| **Node Count** | 3-5+ brokers | 3+ brokers + bookies | 3+ brokers | 3+ nodes |
| **Operational Overhead** | Medium | High | Low | Low |
| **Cloud Pricing** | $$$ | $$$ | $$ | $ |

## Selection Flowchart

### Primary Decision Path

```
START: What is primary use case?

├─ Event Streaming & Event Sourcing
│  ├─ Need proven ecosystem? → KAFKA
│  ├─ Need lowest latency? → REDPANDA
│  └─ Need multi-tenancy? → PULSAR
│
├─ Real-Time Analytics
│  ├─ Millisecond latency? → REDPANDA
│  └─ Integration with big data? → KAFKA
│
├─ Data Integration Pipelines
│  ├─ Many source connectors? → KAFKA (Kafka Connect)
│  └─ Cross-region sync? → PULSAR
│
├─ Microservices Communication
│  ├─ Event-driven architecture? → KAFKA or REDPANDA
│  └─ Task queues? → RABBITMQ
│
└─ IoT / Edge Computing
   ├─ Resource-constrained? → REDPANDA
   └─ Millions of topics? → PULSAR
```

### Operational Considerations

```
START: What are operational constraints?

├─ Team Experience
│  ├─ Strong Kafka expertise? → KAFKA
│  ├─ Need simplicity? → REDPANDA or RABBITMQ
│  └─ Multi-cloud experience? → PULSAR
│
├─ Infrastructure
│  ├─ Kubernetes-native? → REDPANDA or PULSAR
│  ├─ Traditional VMs? → KAFKA or RABBITMQ
│  └─ Edge devices? → REDPANDA
│
└─ Budget
   ├─ Cost-sensitive? → REDPANDA (fewer nodes)
   ├─ Enterprise support needed? → KAFKA (Confluent)
   └─ Open source only? → KAFKA or REDPANDA
```

### Performance Requirements

```
START: What are performance needs?

├─ Throughput
│  ├─ >100k msg/s per node? → KAFKA or REDPANDA
│  ├─ 50k-100k msg/s? → PULSAR
│  └─ <50k msg/s? → RABBITMQ
│
├─ Latency
│  ├─ <10ms p99? → REDPANDA
│  ├─ <50ms p99? → KAFKA or PULSAR
│  └─ <100ms p99? → RABBITMQ
│
└─ Guarantees
   ├─ Exactly-once critical? → KAFKA
   ├─ At-least-once OK? → ANY
   └─ At-most-once OK? → RABBITMQ
```

## Technology-Specific Guidance

### When to Choose Kafka

**Strong indicators**:
- Need for battle-tested, mature ecosystem
- Requirement for event replay and time-travel debugging
- Large number of data source integrations (Kafka Connect)
- Enterprise support requirements (Confluent Platform)
- Team already has Kafka expertise

**Example scenarios**:
- Financial transaction processing (exactly-once semantics)
- E-commerce event sourcing (order events, inventory changes)
- Data lake ingestion (S3, HDFS, data warehouse)
- Microservices event-driven architecture

### When to Choose Pulsar

**Strong indicators**:
- Multi-tenant SaaS application
- Geo-replication across multiple regions
- Need to separate compute and storage scaling
- Tiered storage for hot/cold data
- Millions of topics (IoT scenarios)

**Example scenarios**:
- SaaS platform with tenant isolation
- IoT device telemetry (millions of devices)
- Cross-region data synchronization
- Message routing with complex topic hierarchies

### When to Choose Redpanda

**Strong indicators**:
- Low-latency requirements (<10ms p99)
- Operational simplicity priority
- Cost optimization (fewer nodes)
- Kafka compatibility needed (existing clients)
- Resource-constrained environments

**Example scenarios**:
- High-frequency trading systems
- Real-time fraud detection
- Edge computing applications
- Kafka replacement for cost/performance
- Gaming telemetry (low latency critical)

### When to Choose RabbitMQ

**Strong indicators**:
- Task queue processing (not event streaming)
- RPC communication patterns
- Need for flexible message routing
- Priority queues required
- Simpler use cases

**Example scenarios**:
- Background job processing
- Email sending queues
- Request-response patterns
- Notification delivery systems

## Migration Paths

### From RabbitMQ to Kafka/Redpanda

**Why migrate**:
- Need event replay capability
- Scaling beyond RabbitMQ throughput limits
- Event-driven architecture adoption

**Migration strategy**:
1. Run both systems in parallel (dual-write)
2. Migrate consumers first (read from Kafka)
3. Migrate producers (write to Kafka)
4. Decommission RabbitMQ

### From Kafka to Redpanda

**Why migrate**:
- Reduce operational complexity
- Lower latency requirements
- Cost optimization

**Migration strategy**:
1. Redpanda is Kafka API-compatible
2. Point clients to Redpanda brokers
3. Mirror topics using MirrorMaker 2
4. Cutover consumers and producers
5. Decommission Kafka cluster

### From Kafka to Pulsar

**Why migrate**:
- Multi-tenancy requirements
- Need tiered storage
- Geo-replication

**Migration strategy**:
1. Deploy Pulsar cluster
2. Use Pulsar Kafka-on-Pulsar adapter
3. Mirror topics with Kafka Connect
4. Migrate consumers to Pulsar client
5. Migrate producers
6. Decommission Kafka

## Conclusion

**Default recommendation**: Start with Apache Kafka unless specific requirements dictate otherwise. Kafka offers the best balance of features, maturity, and ecosystem.

**Performance-critical**: Choose Redpanda for low-latency requirements and operational simplicity.

**Multi-tenant SaaS**: Choose Pulsar for native multi-tenancy and geo-replication.

**Simple queues**: Choose RabbitMQ for traditional message queue use cases.
