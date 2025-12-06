# Azure Database Selection Reference

Comprehensive guide to selecting and configuring Azure database services.

## Table of Contents

1. [Azure SQL Database](#azure-sql-database)
2. [Cosmos DB](#cosmos-db)
3. [PostgreSQL Flexible Server](#postgresql-flexible-server)
4. [MySQL Flexible Server](#mysql-flexible-server)
5. [Azure Cache for Redis](#azure-cache-for-redis)

---

## Azure SQL Database

Managed relational database service with elastic scalability and built-in high availability.

### Service Tiers

| Tier | vCores | RAM | Max Storage | Use Case |
|------|--------|-----|-------------|----------|
| **Serverless** | 0.5-40 | Auto | 4 TB | Variable workloads |
| **Provisioned (General Purpose)** | 2-80 | 5-415 GB | 4 TB | Most workloads |
| **Hyperscale** | 2-80 | 5-415 GB | 100 TB | Large databases |
| **Business Critical** | 2-80 | 5-415 GB | 4 TB | Low latency, HA |

---

## Cosmos DB

Globally distributed, multi-model NoSQL database with multiple consistency models and APIs.

### API Selection

| API | Data Model | Use Case |
|-----|------------|----------|
| **NoSQL** | Document (JSON) | General purpose, new apps |
| **MongoDB** | Document (BSON) | MongoDB compatibility |
| **Cassandra** | Wide-column | Time-series, IoT |
| **Gremlin** | Graph | Social networks, recommendations |
| **Table** | Key-value | Simple key-value storage |

---

## PostgreSQL Flexible Server

Azure-managed PostgreSQL with flexible configuration options.

**Advantages:**
- Zone-redundant HA
- Flexible maintenance windows
- Built-in connection pooling (PgBouncer)
- Point-in-time restore

---

## MySQL Flexible Server

Azure-managed MySQL with enterprise features.

**Advantages:**
- Zone-redundant HA
- Read replicas
- Automatic backups
- Burstable tier for dev/test

---

## Azure Cache for Redis

In-memory cache for session state, caching, and real-time analytics.

### Tiers

| Tier | Clustering | Persistence | Use Case |
|------|------------|-------------|----------|
| **Basic** | No | No | Dev/test |
| **Standard** | No | No | Production cache |
| **Premium** | Yes | Yes | Enterprise, HA |
| **Enterprise** | Yes | Yes | Active geo-replication |
