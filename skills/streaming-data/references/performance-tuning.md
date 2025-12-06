# Stream Processing Performance Tuning

## Table of Contents
- [Producer Performance](#producer-performance)
- [Consumer Performance](#consumer-performance)
- [Kafka Broker Tuning](#kafka-broker-tuning)
- [Partitioning Strategy](#partitioning-strategy)
- [Monitoring Metrics](#monitoring-metrics)
- [Conclusion](#conclusion)

## Producer Performance

### Batching

```properties
# Increase batch size for throughput
batch.size=32768              # 32KB (default: 16KB)
linger.ms=10                  # Wait 10ms for batch
buffer.memory=67108864        # 64MB buffer
```

### Compression

```properties
# LZ4: Best balance of speed/compression
compression.type=lz4

# GZIP: Better compression, slower
# compression.type=gzip

# Snappy: Fast, moderate compression
# compression.type=snappy
```

### Partitioning

```typescript
// Custom partitioner for even distribution
class CustomPartitioner {
  partition(topic: string, key: any, partitions: number): number {
    // Hash key to partition
    const hash = murmurhash(key);
    return hash % partitions;
  }
}
```

## Consumer Performance

### Parallelism

Match consumer instances to partition count:

```
Partitions: 10
Consumers: 10 (optimal)
Consumers: 5  (under-utilized)
Consumers: 15 (5 idle)
```

### Fetch Settings

```properties
# Increase fetch size for throughput
fetch.min.bytes=10240         # 10KB
fetch.max.wait.ms=500         # Wait 500ms
max.partition.fetch.bytes=1048576  # 1MB per partition
```

### Commit Frequency

```properties
# Less frequent commits = better performance
auto.commit.interval.ms=5000  # Commit every 5 seconds
```

## Kafka Broker Tuning

### Replica Settings

```properties
# Replication for fault tolerance
default.replication.factor=3
min.insync.replicas=2
```

### Log Settings

```properties
# Segment size and retention
log.segment.bytes=1073741824  # 1GB segments
log.retention.hours=168       # 7 days
log.retention.bytes=-1        # No size limit
```

### Network Threads

```properties
num.network.threads=8
num.io.threads=8
socket.send.buffer.bytes=1048576
socket.receive.buffer.bytes=1048576
```

## Partitioning Strategy

### Rule of Thumb

```
Partitions = (Target Throughput / Consumer Throughput)

Example:
Target: 1M msg/s
Consumer: 50k msg/s
Partitions = 1M / 50k = 20
```

### Repartitioning

Too few partitions → add partitions (can't reduce):

```bash
kafka-topics.sh --alter --topic my-topic --partitions 20 \
  --bootstrap-server localhost:9092
```

## Monitoring Metrics

### Producer Metrics

- `record-send-rate`: Messages/sec
- `record-error-rate`: Errors/sec
- `request-latency-avg`: Avg latency
- `batch-size-avg`: Avg batch size

### Consumer Metrics

- `records-consumed-rate`: Messages/sec
- `fetch-latency-avg`: Fetch latency
- `records-lag-max`: Max lag
- `commit-latency-avg`: Commit latency

### Broker Metrics

- `BytesInPerSec`: Inbound throughput
- `BytesOutPerSec`: Outbound throughput
- `MessagesInPerSec`: Message rate
- `UnderReplicatedPartitions`: Replication lag

## Conclusion

Tune batch size, compression, partitioning, and parallelism for optimal performance. Monitor key metrics and adjust based on workload patterns.
