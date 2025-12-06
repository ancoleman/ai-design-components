# Azure Messaging Patterns Reference

Comprehensive guide to Azure messaging and event services.

## Table of Contents

1. [Azure Service Bus](#azure-service-bus)
2. [Azure Event Grid](#azure-event-grid)
3. [Azure Event Hubs](#azure-event-hubs)
4. [Storage Queues](#storage-queues)

---

## Azure Service Bus

Enterprise messaging service with queues and publish-subscribe topics.

### Queue vs. Topic

| Feature | Queue | Topic/Subscription |
|---------|-------|-------------------|
| **Pattern** | Point-to-point | Publish-subscribe |
| **Receivers** | Single consumer | Multiple subscribers |
| **Filtering** | No | Yes (SQL filters) |
| **Use Case** | Task distribution | Event broadcasting |

### Sessions for Ordered Processing

Enable sessions for FIFO (first-in-first-out) message processing within a session.

---

## Azure Event Grid

Event routing service for reactive programming.

### Event Domains

Group related topics for multi-tenant scenarios.

### Advanced Filtering

Filter events by subject, data fields, and event type before delivery.

---

## Azure Event Hubs

Big data streaming platform for telemetry and event ingestion.

### Partitioning Strategy

Partition by key (e.g., device ID) for ordered processing within partition.

### Capture Feature

Automatically archive events to Blob Storage or Data Lake.

---

## Storage Queues

Simple queue for asynchronous messaging.

**When to Use:**
- Simple task queues
- Cost-sensitive (<500k messages/sec)
- No advanced features needed (transactions, sessions)
