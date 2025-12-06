# AWS Database Services - Deep Dive

## Table of Contents

1. [RDS (Relational Database Service)](#rds-relational-database-service)
2. [Aurora (AWS-Native Relational)](#aurora-aws-native-relational)
3. [DynamoDB (NoSQL)](#dynamodb-nosql)
4. [DocumentDB (MongoDB Compatible)](#documentdb-mongodb-compatible)
5. [ElastiCache and MemoryDB](#elasticache-and-memorydb)
6. [Database Selection Decision Tree](#database-selection-decision-tree)
7. [Migration Strategies](#migration-strategies)

---

## RDS (Relational Database Service)

### Supported Engines

| Engine | Latest Version | Best For |
|--------|---------------|----------|
| PostgreSQL | 15.x | Modern apps, JSON support |
| MySQL | 8.0.x | Legacy compatibility |
| MariaDB | 10.11.x | MySQL fork, enhanced |
| Oracle | 19c, 21c | Enterprise apps, BYOL |
| SQL Server | 2019, 2022 | Microsoft ecosystem |

### Instance Classes

**General Purpose (db.t3, db.m5):**
- Balanced CPU, memory
- t3: Burstable, cost-effective
- m5: Consistent performance

**Memory Optimized (db.r5, db.x2):**
- High memory-to-CPU ratio
- Large datasets, caching
- r5: Latest generation

**Burstable (db.t4g - Graviton):**
- ARM-based processors
- 40% better price-performance
- Sustainable performance

### Cost Model (PostgreSQL db.t3.medium, us-east-1)

**Instance:** $0.068/hour = $49.64/month
**Storage (gp3):** $0.115/GB-month
**Backup Storage:** Free (automated backups = DB size)

**Example Configuration:**
- db.t3.medium instance: $49.64/month
- 100GB gp3 storage: $11.50/month
- **Total: $61.14/month**

### Multi-AZ Deployments

**How it Works:**
- Synchronous replication to standby in different AZ
- Automatic failover (60-120 seconds)
- Same endpoint (no app changes)

**Cost:** 2x instance cost + storage in both AZs

**Use When:**
- Production workloads
- High availability required (99.95% SLA)
- Automatic failover needed

### Read Replicas

**Purpose:**
- Offload read traffic
- Scale horizontally
- Analytics on replica (no impact on primary)

**Limitations:**
- Up to 15 replicas per instance
- Asynchronous replication (eventual consistency)
- Cross-region supported

**Cost:** Standard instance pricing per replica

### Blue/Green Deployments (2025 Feature)

**Purpose:**
- Zero-downtime version upgrades
- Test changes in production clone

**How it Works:**
1. Create green environment (clone)
2. Test in green environment
3. Switch traffic (blue → green)
4. Rollback if issues detected

**Use Cases:**
- Major version upgrades
- Schema changes
- Performance testing

### Best Practices

1. **Enable Automated Backups:**
   - Retention: 7-35 days
   - Point-in-time recovery
   - No performance impact (uses snapshots)

2. **Use Parameter Groups:**
   - Customize DB engine settings
   - Apply best practices per workload
   - Version control parameter changes

3. **Monitor Performance:**
   - Enable Performance Insights (free for 7 days)
   - Track slow queries
   - Set up CloudWatch alarms

4. **Security:**
   - Enable encryption at rest (KMS)
   - Use TLS for connections
   - Store credentials in Secrets Manager
   - Apply security group restrictions

---

## Aurora (AWS-Native Relational)

### Overview

AWS-designed database compatible with MySQL and PostgreSQL. Higher performance, availability, and durability than standard RDS.

### Architecture

**Storage:**
- Automatically scales 10GB to 128TB
- 6 copies across 3 AZs
- Self-healing storage
- Continuous backup to S3

**Compute:**
- Primary instance (read-write)
- Up to 15 read replicas
- Sub-10ms replica lag

### Performance Improvements

**vs. MySQL:**
- 5x throughput improvement
- Same applications, drivers

**vs. PostgreSQL:**
- 3x throughput improvement
- PostgreSQL 11-15 compatibility

### Aurora Serverless v2

**Use Cases:**
- Variable workloads (dev/test, seasonal)
- Unpredictable traffic
- Multi-tenant applications

**Scaling:**
- Minimum: 0.5 ACU (1 ACU = 2GB RAM, ~2 vCPU)
- Maximum: 128 ACU
- Scales in 0.5 ACU increments
- Sub-second scaling

**Cost Model:**
- $0.12 per ACU-hour (us-east-1)
- Storage: $0.10/GB-month
- I/O: $0.20 per 1M requests

**Example Calculation:**
```
Workload: 8 hours/day active, 2 ACU baseline, 10 ACU peak

ACU-hours/month: (2 × 16hr + 10 × 8hr) × 30 days = 3,360
Cost: 3,360 × $0.12 = $403.20/month
Storage (100GB): $10/month
Total: ~$413/month
```

### Aurora Limitless Database (2024+)

**Purpose:**
- Horizontal write scaling
- Sharding managed by Aurora
- Millions of transactions per second

**Use Cases:**
- Highest-scale OLTP workloads
- Multi-tenant SaaS applications
- Gaming leaderboards

**How it Works:**
- Data automatically sharded
- Distributed SQL processing
- Appears as single database to applications

### Aurora Global Database

**Purpose:**
- Cross-region replication (<1 second lag)
- Disaster recovery
- Low-latency global reads

**Architecture:**
- Primary region (read-write)
- Up to 5 secondary regions (read-only)
- Dedicated infrastructure for replication

**Cost:**
- Replication: $0.10 per GB transferred
- Instances in secondary regions charged normally

### Cost Comparison: Aurora vs. RDS

**Aurora Advantages:**
- No manual backups needed (continuous to S3)
- Faster replication (sub-10ms vs. seconds)
- Higher availability (99.99% vs. 99.95%)
- Automatic failover to replicas

**Aurora Premium:**
- 20% more expensive than RDS for equivalent instance
- Worth it for production workloads

**Example:**
- RDS PostgreSQL db.r5.large: $0.24/hour = $175/month
- Aurora PostgreSQL r5.large: $0.29/hour = $212/month
- Difference: $37/month (20% premium)

### Best Practices

1. **Use Aurora for Production:**
   - Better availability than RDS
   - Automatic storage scaling
   - Fast failover

2. **Leverage Read Replicas:**
   - Create reader endpoint (automatic load balancing)
   - Offload analytics to replicas
   - Use custom endpoints for workload isolation

3. **Enable Backtrack (MySQL):**
   - Rewind DB to specific point in time
   - No restore from backup needed
   - Minutes instead of hours

---

## DynamoDB (NoSQL)

### Overview

Fully managed NoSQL database. Single-digit millisecond latency. Infinite horizontal scaling.

### Data Model

**Primary Key Options:**

1. **Partition Key Only:**
   - Unique identifier
   - Example: UserID

2. **Partition Key + Sort Key:**
   - Composite primary key
   - Example: UserID (partition) + Timestamp (sort)
   - Enables range queries

**Attributes:**
- Flexible schema (no predefined columns)
- Supports strings, numbers, binary, lists, maps, sets

### Capacity Modes

**On-Demand:**
- Pay per request
- No capacity planning
- Automatic scaling

**Pricing (us-east-1):**
- Write: $1.25 per million write request units
- Read: $0.25 per million read request units
- Storage: $0.25/GB-month

**Provisioned:**
- Specify read/write capacity units
- Predictable cost
- Auto-scaling available

**Pricing (us-east-1):**
- Write: $0.00065 per WCU-hour
- Read: $0.00013 per RCU-hour
- Storage: $0.25/GB-month

### Storage Classes (2024+)

**Standard:**
- Default storage class
- $0.25/GB-month

**Standard-IA (Infrequent Access):**
- 60% cheaper storage
- $0.10/GB-month
- Higher per-request cost
- Use for tables accessed <2 times/month

### Global Tables

**Purpose:**
- Multi-region, active-active replication
- Sub-second replication lag
- Automatic conflict resolution

**Use Cases:**
- Global applications
- Disaster recovery
- Low-latency global access

**Cost:**
- Replication: $0.000002 per replicated write
- Full instance cost in each region

### DynamoDB Streams

**Purpose:**
- Real-time change data capture
- Trigger Lambda on insert/update/delete
- Audit logging, analytics pipelines

**Retention:**
- 24 hours of change data

**Use Cases:**
- Event-driven architectures
- Data replication
- Aggregation pipelines

### DynamoDB Accelerator (DAX)

**Purpose:**
- In-memory caching layer
- Microsecond latency
- Fully managed

**Performance:**
- Cache hit: <1ms latency
- Cache miss: ~10ms (DynamoDB read)

**Cost (dax.t3.small):**
- $0.04/hour = $29/month per node
- Minimum 3 nodes (HA) = $87/month

**Use When:**
- Need <1ms latency
- Read-heavy workload
- Can afford caching cost

### Best Practices

1. **Design Partition Keys:**
   - Distribute access evenly
   - Avoid hot partitions
   - Use high-cardinality attributes (UserID, not Country)

2. **Use Global Secondary Indexes (GSI):**
   - Query alternate access patterns
   - Different partition/sort keys
   - Eventually consistent reads
   - Plan for 20 GSIs limit

3. **Use Local Secondary Indexes (LSI):**
   - Same partition key, different sort key
   - Strongly consistent reads
   - Must create at table creation
   - 5 LSI limit

4. **Enable Point-in-Time Recovery:**
   - Restore to any second in last 35 days
   - $0.20/GB-month (20% of table size)

5. **Use PartiQL:**
   - SQL-like query language
   - Easier than low-level API
   - Supports SELECT, INSERT, UPDATE, DELETE

---

## DocumentDB (MongoDB Compatible)

### Overview

Managed document database compatible with MongoDB 4.0+. Scales to millions of requests per second.

### Architecture

**Storage:**
- Automatically scales to 128TB
- 6 copies across 3 AZs (like Aurora)
- Continuous backup to S3

**Compute:**
- Primary instance (read-write)
- Up to 15 read replicas

### MongoDB Compatibility

**Supported:**
- MongoDB 4.0, 4.2, 5.0 APIs
- Drivers and tools (Compass, mongosh)
- Most MongoDB queries and aggregations

**Not Supported:**
- Some advanced MongoDB features
- Check compatibility guide for specifics

### Cost Model (db.t3.medium)

**Instance:** $0.073/hour = $53/month
**Storage:** $0.10/GB-month
**I/O:** $0.20 per 1M requests

**Example:**
- Instance: $53/month
- 100GB storage: $10/month
- 10M I/O requests: $2/month
- **Total: $65/month**

### Use Cases

**Ideal:**
- Existing MongoDB workloads
- Document-oriented data
- JSON data storage
- Flexible schemas

**Consider Alternatives:**
- Simple key-value: Use DynamoDB (cheaper)
- Need native MongoDB: Use MongoDB Atlas
- Complex transactions: Use Aurora PostgreSQL

---

## ElastiCache and MemoryDB

### ElastiCache for Redis

**Purpose:**
- In-memory caching
- Session storage
- Real-time analytics

**Cost (cache.t3.medium):**
- $0.068/hour = $49.64/month per node

**Use Cases:**
- Database query caching
- Session store
- Leaderboards
- Rate limiting
- Pub/sub messaging

**Limitations:**
- No persistence (data lost on restart)
- Use MemoryDB for durability

### ElastiCache for Memcached

**Purpose:**
- Simple caching layer
- Horizontal scaling via sharding

**vs. Redis:**
- Simpler (no advanced data structures)
- Multi-threaded (better CPU utilization)
- No persistence

**Use When:**
- Simple caching needed
- Horizontal scaling priority
- Don't need Redis features

### MemoryDB for Redis (2024+)

**Purpose:**
- Redis-compatible with Multi-AZ durability
- Primary database (not just cache)

**Performance:**
- Microsecond read latency
- Single-digit millisecond write latency
- Durable across AZ failures

**Cost (db.t4g.small):**
- $0.061/hour = $44.53/month per node

**vs. ElastiCache Redis:**
- 20% more expensive
- Durable (survives restarts)
- Use as primary database

**Use Cases:**
- Real-time applications needing persistence
- Gaming leaderboards with durability
- Session stores with HA requirements

---

## Database Selection Decision Tree

```
Q1: What is the data model?
  ├─ Relational (tables with joins) → Q2
  ├─ Document (JSON/BSON) → Q5
  ├─ Key-Value → DynamoDB
  ├─ Graph → Neptune
  └─ Time-Series → Timestream

Q2: What is the scale requirement?
  ├─ <64TB, standard RDS features → RDS
  └─ >64TB or need highest performance → Aurora

Q3: What engine do you need?
  ├─ PostgreSQL → RDS PostgreSQL or Aurora PostgreSQL
  ├─ MySQL → RDS MySQL or Aurora MySQL
  ├─ Oracle/SQL Server → RDS (Aurora not available)

Q4: What availability do you need?
  ├─ Dev/Test → RDS Single-AZ
  ├─ Production → RDS Multi-AZ or Aurora
  └─ Global → Aurora Global Database

Q5: Document database specifics:
  ├─ Simple key-value with JSON → DynamoDB
  ├─ MongoDB compatibility required → DocumentDB
  └─ Complex MongoDB features → MongoDB Atlas

Q6: Caching needs:
  ├─ Simple cache, no persistence → ElastiCache (Redis or Memcached)
  ├─ Cache with durability → MemoryDB
  └─ Microsecond latency for DynamoDB → DAX
```

---

## Migration Strategies

### On-Premises to AWS

**Relational Databases:**

1. **AWS Database Migration Service (DMS):**
   - Minimal downtime
   - Continuous replication
   - Supports heterogeneous migrations (Oracle → PostgreSQL)

2. **Native Tools:**
   - MySQL: mysqldump, binlog replication
   - PostgreSQL: pg_dump, logical replication
   - Oracle: Data Pump, GoldenGate

**NoSQL Databases:**

1. **MongoDB to DocumentDB:**
   - Use AWS DMS
   - mongodump/mongorestore for smaller DBs

2. **Self-Managed to DynamoDB:**
   - Application-level migration
   - Dual-write pattern (old + new)
   - Validate and cutover

### RDS to Aurora

**Zero-Downtime Migration:**

1. Create Aurora read replica from RDS instance
2. Promote replica to standalone Aurora cluster
3. Update application endpoints
4. Decommission RDS instance

**Timeframe:** 1-2 hours depending on size

### DynamoDB to Aurora (or vice versa)

**Strategy:**
- Application-level migration
- Dual-write pattern
- Gradually shift reads
- Validate data consistency

**Tooling:**
- AWS DMS (limited support)
- Custom scripts

### Self-Managed to Managed

**Benefits:**
- Automated backups
- Automatic failover
- Managed upgrades
- Built-in monitoring

**Considerations:**
- Test performance (might differ)
- Validate feature compatibility
- Plan rollback strategy
