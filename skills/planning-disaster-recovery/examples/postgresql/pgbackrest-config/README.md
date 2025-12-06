# pgBackRest Configuration Example

This directory contains a complete pgBackRest setup for production PostgreSQL with S3 backup storage.

## Files

- `pgbackrest.conf` - Main pgBackRest configuration
- `postgresql.conf` - PostgreSQL settings for WAL archiving
- `backup.sh` - Automated backup script
- `restore.sh` - Point-in-time restore script

## Quick Start

1. Install pgBackRest:
```bash
sudo apt-get install pgbackrest
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Copy configuration:
```bash
sudo cp pgbackrest.conf /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

4. Update PostgreSQL configuration:
```bash
sudo -u postgres psql -c "ALTER SYSTEM SET archive_command = 'pgbackrest --stanza=main archive-push %p';"
sudo -u postgres psql -c "SELECT pg_reload_conf();"
```

5. Initialize stanza:
```bash
sudo -u postgres pgbackrest --stanza=main stanza-create
```

6. Run first backup:
```bash
sudo -u postgres pgbackrest --stanza=main --type=full backup
```

## Configuration Details

See `pgbackrest.conf` for complete configuration including:
- Dual S3 repositories (primary + DR region)
- AES-256 encryption
- LZ4 compression
- Parallel processing
- Retention policies
