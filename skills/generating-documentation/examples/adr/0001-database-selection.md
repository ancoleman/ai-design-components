# Use PostgreSQL for Primary Database

* Status: accepted
* Deciders: Engineering Team, CTO, Platform Lead
* Date: 2025-01-15

Technical Story: We need to select a relational database for our new application that handles user data, transactions, and complex queries with high reliability.

## Context and Problem Statement

Our application requires a reliable, performant relational database that can handle complex queries with joins, ACID transactions, JSON data types for flexible schemas, full-text search capabilities, and potential for horizontal scaling in the future.

We need to choose between PostgreSQL, MySQL, and cloud-managed database solutions.

## Decision Drivers

* **Data Integrity**: ACID compliance is critical for financial transactions
* **Developer Experience**: Team has experience with SQL databases but needs good tooling
* **Cost**: Open-source preferred to minimize licensing costs
* **Performance**: Must handle 10,000+ queries per second at peak
* **Ecosystem**: Rich tooling, library support, and community resources
* **Scalability**: Ability to scale horizontally in the future as we grow
* **Features**: Advanced features like JSONB, full-text search, and window functions

## Considered Options

* PostgreSQL
* MySQL
* Amazon Aurora (PostgreSQL-compatible)
* Google Cloud SQL (PostgreSQL)

## Decision Outcome

Chosen option: "PostgreSQL", because it provides the best balance of features, performance, and cost for our use case. PostgreSQL's advanced features (JSONB, full-text search, advanced indexing, window functions) align perfectly with our requirements, our team has existing expertise, and it's open-source with no licensing costs.

### Positive Consequences

* Open-source with no licensing costs
* Excellent documentation and very active community support
* Advanced features (JSONB, CTEs, window functions, full-text search) available out of the box
* Strong ACID compliance and data integrity guarantees
* Can migrate to managed services (AWS RDS, Azure Database, Google Cloud SQL) later if needed
* Rich ecosystem of tools (pg_dump, pgAdmin, TimescaleDB, PostGIS)
* Superior performance for complex queries compared to alternatives

### Negative Consequences

* Slightly steeper learning curve than MySQL for some advanced features
* Self-hosting requires DevOps investment (backups, monitoring, updates)
* Horizontal scaling requires extensions (Citus) or architectural changes (sharding)
* Need to manage connection pooling (PgBouncer) for high concurrency

## Pros and Cons of the Options

### PostgreSQL

* Good, because it's open-source and free (no licensing costs)
* Good, because it has JSONB support for flexible schemas
* Good, because it has excellent full-text search capabilities
* Good, because team has 3 engineers with PostgreSQL experience
* Good, because it has strong ACID compliance
* Good, because advanced features like window functions and CTEs are available
* Good, because it has excellent performance for complex queries
* Bad, because horizontal scaling requires architectural changes or extensions
* Bad, because self-hosting requires DevOps investment (though we have this capability)

### MySQL

* Good, because it's open-source and free
* Good, because it has a simpler architecture for basic use cases
* Good, because it has slightly better read performance for very simple queries
* Good, because it's widely used and has large community
* Bad, because it lacks advanced features that we need (no JSONB until MySQL 8.0, and still limited)
* Bad, because full-text search is less powerful than PostgreSQL
* Bad, because historically weaker transaction support (though improved in recent versions)
* Bad, because window functions and CTEs were added later and are less mature

### Amazon Aurora (PostgreSQL-compatible)

* Good, because it's managed (less operational overhead)
* Good, because it offers PostgreSQL compatibility
* Good, because it has built-in replication and automated backups
* Good, because it can scale reads with read replicas
* Good, because it provides high availability out of the box
* Bad, because it's more expensive than self-hosted PostgreSQL (~$200-500/month vs ~$50/month for equivalent EC2)
* Bad, because it locks us into AWS ecosystem
* Bad, because it adds vendor dependency and potential for vendor lock-in
* Bad, because we lose some control over database configuration

### Google Cloud SQL (PostgreSQL)

* Good, because it's managed (less operational overhead)
* Good, because it supports PostgreSQL fully
* Good, because it provides automated backups and point-in-time recovery
* Good, because our infrastructure is already on Google Cloud
* Bad, because it's more expensive than self-hosted (~$150-400/month)
* Bad, because it locks us into Google Cloud
* Bad, because it adds vendor dependency
* Bad, because performance may be slightly lower than Aurora for write-heavy workloads

## Links

* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [Internal Wiki: Database Setup Guide](https://wiki.example.com/db-setup)
* [Performance Benchmarks Document](https://docs.example.com/benchmarks)
* Related: Future ADR needed for read replica strategy
