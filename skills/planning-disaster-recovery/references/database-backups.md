# Database Backup Patterns

## Table of Contents

1. [PostgreSQL Backup Strategies](#postgresql-backup-strategies)
2. [MySQL Backup Strategies](#mysql-backup-strategies)
3. [MongoDB Backup Strategies](#mongodb-backup-strategies)
4. [Backup Type Selection](#backup-type-selection)
5. [Point-in-Time Recovery](#point-in-time-recovery)

## PostgreSQL Backup Strategies

### pgBackRest Production Setup

**Architecture:**
```
PostgreSQL Primary
    ├─► WAL Archive (continuous) → S3/GCS/Azure
    ├─► Full Backup (weekly) → Multi-repo support
    ├─► Differential Backup (daily) → Based on last full
    └─► Incremental Backup (optional hourly) → Based on last backup

PostgreSQL Standby (optional)
    └─► Backup from standby (zero impact on primary)
```

**Complete Configuration:**

`/etc/pgbackrest/pgbackrest.conf`:
```ini
[global]
# Repository 1: S3 primary
repo1-type=s3
repo1-s3-bucket=prod-pg-backups
repo1-s3-region=us-east-1
repo1-s3-key=<access-key>
repo1-s3-key-secret=<secret-key>
repo1-path=/pgbackrest
repo1-retention-full=2
repo1-retention-diff=6
repo1-retention-archive=4
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=<strong-passphrase>

# Repository 2: S3 secondary region (disaster recovery)
repo2-type=s3
repo2-s3-bucket=dr-pg-backups
repo2-s3-region=us-west-2
repo2-s3-key=<access-key>
repo2-s3-key-secret=<secret-key>
repo2-path=/pgbackrest
repo2-retention-full=4
repo2-cipher-type=aes-256-cbc
repo2-cipher-pass=<strong-passphrase>

# Performance
process-max=4
compress-type=lz4
compress-level=3

# Logging
log-level-console=info
log-level-file=debug
log-path=/var/log/pgbackrest

[main]
pg1-path=/var/lib/postgresql/14/main
pg1-port=5432
pg1-socket-path=/var/run/postgresql
pg1-user=postgres

# Backup from standby to reduce primary load
backup-standby=y

# Archive settings
archive-async=y
archive-push-queue-max=128MB

# Backup settings
start-fast=y
stop-auto=y
delta=y
