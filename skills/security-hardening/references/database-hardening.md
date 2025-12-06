# Database Hardening Reference

Comprehensive guide to hardening PostgreSQL, MySQL, MongoDB, and Redis databases.

## Table of Contents

1. [PostgreSQL Hardening](#postgresql-hardening)
2. [MySQL Hardening](#mysql-hardening)
3. [MongoDB Hardening](#mongodb-hardening)
4. [Redis Hardening](#redis-hardening)
5. [General Database Security](#general-database-security)

---

## PostgreSQL Hardening

### Authentication and Authorization

```sql
-- Revoke public schema permissions
REVOKE ALL ON DATABASE mydb FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM PUBLIC;

-- Create application role with minimal permissions
CREATE ROLE app_user WITH LOGIN PASSWORD 'use_vault_for_this';
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA app TO app_user;

-- Grant specific table permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA app GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- Read-only user
CREATE ROLE readonly WITH LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO readonly;
GRANT USAGE ON SCHEMA app TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA app TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA app GRANT SELECT ON TABLES TO readonly;

-- Revoke dangerous privileges
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON pg_catalog.pg_authid FROM PUBLIC;
```

### Connection Security (pg_hba.conf)

```conf
# /var/lib/postgresql/data/pg_hba.conf

# Local connections
local   all   postgres   peer
local   all   all        scram-sha-256

# Remote connections: require SSL
hostssl all   all   0.0.0.0/0   scram-sha-256
hostnossl all   all   0.0.0.0/0   reject

# Specific networks only
hostssl mydb   app_user   10.0.0.0/8   scram-sha-256

# Reject all other connections
host    all   all   0.0.0.0/0   reject
```

### postgresql.conf Hardening

```conf
# /var/lib/postgresql/data/postgresql.conf

# Connection settings
listen_addresses = '10.0.1.10'  # Specific IP, not '*'
port = 5432
max_connections = 100
superuser_reserved_connections = 3

# SSL/TLS
ssl = on
ssl_cert_file = '/var/lib/postgresql/data/server.crt'
ssl_key_file = '/var/lib/postgresql/data/server.key'
ssl_ca_file = '/var/lib/postgresql/data/root.crt'
ssl_min_protocol_version = 'TLSv1.2'
ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'
ssl_prefer_server_ciphers = on

# Logging
logging_collector = on
log_destination = 'stderr'
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_min_duration_statement = 1000  # Log slow queries (1s+)
log_connections = on
log_disconnections = on
log_duration = off
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_statement = 'ddl'  # Log DDL statements
log_timezone = 'UTC'

# Security settings
password_encryption = scram-sha-256
row_security = on

# Statement timeout (prevent runaway queries)
statement_timeout = 300000  # 5 minutes

# Lock timeout
lock_timeout = 30000  # 30 seconds

# Disable trust authentication (enforce password)
# (configured in pg_hba.conf)
```

### Encryption at Rest

```bash
# Using LUKS for filesystem encryption
cryptsetup luksFormat /dev/sdb
cryptsetup luksOpen /dev/sdb pgdata
mkfs.ext4 /dev/mapper/pgdata
mount /dev/mapper/pgdata /var/lib/postgresql

# Or use PostgreSQL's pgcrypto extension
psql -d mydb -c "CREATE EXTENSION pgcrypto;"

# Encrypt specific columns
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    ssn BYTEA  -- Encrypted column
);

INSERT INTO users (username, email, ssn)
VALUES ('john', 'john@example.com', pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Retrieve decrypted data
SELECT username, pgp_sym_decrypt(ssn, 'encryption_key') as ssn FROM users;
```

### Backup Security

```bash
#!/bin/bash
# /usr/local/bin/secure-pg-backup.sh

BACKUP_DIR="/backup/postgresql"
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
ENCRYPTION_KEY="/secure/backup.key"

# Dump database
pg_dump -U postgres mydb | \
  gzip | \
  openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:$ENCRYPTION_KEY \
  > "$BACKUP_DIR/mydb_$BACKUP_DATE.sql.gz.enc"

# Set secure permissions
chmod 600 "$BACKUP_DIR/mydb_$BACKUP_DATE.sql.gz.enc"

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "*.enc" -mtime +30 -delete
```

---

## MySQL Hardening

### User Management

```sql
-- Remove anonymous users
DELETE FROM mysql.user WHERE User='';

-- Remove remote root access
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');

-- Create application user
CREATE USER 'app_user'@'10.0.0.%' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app_user'@'10.0.0.%';

-- Require SSL
ALTER USER 'app_user'@'10.0.0.%' REQUIRE SSL;

-- Set password expiration
ALTER USER 'app_user'@'10.0.0.%' PASSWORD EXPIRE INTERVAL 90 DAY;

-- Flush privileges
FLUSH PRIVILEGES;
```

### my.cnf Hardening

```ini
# /etc/mysql/my.cnf

[mysqld]
# Network
bind-address = 10.0.1.10  # Specific IP, not 0.0.0.0
port = 3306
skip-networking = 0
skip-name-resolve = 1

# SSL/TLS
require_secure_transport = ON
ssl-ca = /etc/mysql/ssl/ca.pem
ssl-cert = /etc/mysql/ssl/server-cert.pem
ssl-key = /etc/mysql/ssl/server-key.pem
tls_version = TLSv1.2,TLSv1.3

# Security
local-infile = 0  # Disable LOAD DATA LOCAL INFILE
secure-file-priv = /var/lib/mysql-files/  # Restrict file operations
symbolic-links = 0  # Disable symbolic links

# Logging
log-error = /var/log/mysql/error.log
general_log = 1
general_log_file = /var/log/mysql/general.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2

# Performance and limits
max_connections = 100
max_connect_errors = 10
connect_timeout = 10
wait_timeout = 600
max_allowed_packet = 64M
```

### Remove Test Database

```sql
-- Remove test database
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
```

---

## MongoDB Hardening

### Enable Authentication

```javascript
// Create admin user
use admin
db.createUser({
  user: "admin",
  pwd: "strongAdminPassword",
  roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
})

// Create application user
use mydb
db.createUser({
  user: "app_user",
  pwd: "strongAppPassword",
  roles: [ { role: "readWrite", db: "mydb" } ]
})

// Create read-only user
use mydb
db.createUser({
  user: "readonly",
  pwd: "strongReadPassword",
  roles: [ { role: "read", db: "mydb" } ]
})
```

### mongod.conf Hardening

```yaml
# /etc/mongod.conf

# Network interfaces
net:
  port: 27017
  bindIp: 10.0.1.10  # Specific IP, not 0.0.0.0
  ssl:
    mode: requireSSL
    PEMKeyFile: /etc/ssl/mongodb.pem
    CAFile: /etc/ssl/ca.pem
    allowConnectionsWithoutCertificates: false

# Security
security:
  authorization: enabled
  clusterAuthMode: x509

# Auditing
auditLog:
  destination: file
  format: JSON
  path: /var/log/mongodb/audit.log

# Storage
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2
    collectionConfig:
      blockCompressor: snappy

# Encryption at rest
security:
  enableEncryption: true
  encryptionCipherMode: AES256-CBC
  encryptionKeyFile: /etc/mongodb-keyfile

# Logging
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  verbosity: 1

# Operations profiling
operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100
```

### Disable HTTP Interface

```yaml
# mongod.conf
net:
  http:
    enabled: false
    JSONPEnabled: false
    RESTInterfaceEnabled: false
```

---

## Redis Hardening

### redis.conf Hardening

```conf
# /etc/redis/redis.conf

# Network
bind 127.0.0.1 10.0.1.10  # Specific IPs
port 6379
protected-mode yes
tcp-backlog 511

# TLS/SSL
tls-port 6380
tls-cert-file /etc/redis/ssl/redis.crt
tls-key-file /etc/redis/ssl/redis.key
tls-ca-cert-file /etc/redis/ssl/ca.crt
tls-protocols "TLSv1.2 TLSv1.3"
tls-ciphers HIGH:!aNULL:!MD5
tls-prefer-server-ciphers yes

# Authentication
requirepass veryStrongPasswordHere
masterauth veryStrongPasswordHere

# ACL (Redis 6+)
aclfile /etc/redis/users.acl

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""
rename-command CONFIG "CONFIG_SECRET_NAME"
rename-command SHUTDOWN ""
rename-command DEBUG ""

# Limits
maxclients 10000
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /var/lib/redis

# Logging
loglevel notice
logfile /var/log/redis/redis-server.log
syslog-enabled no

# Security
supervised systemd
user redis
```

### Redis ACL (Access Control Lists)

```conf
# /etc/redis/users.acl

# Admin user (full access)
user admin on >strongAdminPassword ~* &* +@all

# Application user (limited commands)
user app_user on >strongAppPassword ~myapp:* &* +get +set +del +expire

# Read-only user
user readonly on >strongReadPassword ~* &* +get +scan +keys

# Default user (disabled)
user default off
```

---

## General Database Security

### 1. Network Isolation

```yaml
# Docker Compose example
version: '3.9'
services:
  db:
    image: postgres:15
    networks:
      - db-network
    # No ports exposed to host

  app:
    image: myapp:latest
    networks:
      - db-network
    depends_on:
      - db

networks:
  db-network:
    driver: bridge
    internal: true  # No external access
```

### 2. Least Privilege Principle

```sql
-- PostgreSQL: Grant only required permissions
CREATE ROLE app_user WITH LOGIN;
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA app TO app_user;
GRANT SELECT, INSERT, UPDATE ON specific_tables TO app_user;
-- NO DELETE, NO DDL permissions
```

### 3. Regular Backups with Encryption

```bash
#!/bin/bash
# Automated encrypted backup

# PostgreSQL
pg_dump mydb | gzip | openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:/secure/key > backup.sql.gz.enc

# MySQL
mysqldump mydb | gzip | openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:/secure/key > backup.sql.gz.enc

# MongoDB
mongodump --archive | gzip | openssl enc -aes-256-cbc -salt -pbkdf2 -pass file:/secure/key > backup.archive.gz.enc
```

### 4. Audit Logging

Enable comprehensive logging for all database access:

**PostgreSQL:** `log_statement = 'all'`
**MySQL:** `general_log = 1`
**MongoDB:** Enable auditing
**Redis:** `slowlog` and command logging

### 5. Connection Pooling

Use connection pooling to limit database connections:

```python
# Python with psycopg2 and connection pooling
from psycopg2 import pool

db_pool = pool.SimpleConnectionPool(
    1,  # minconn
    10,  # maxconn
    user='app_user',
    password='from_vault',
    host='db.internal',
    port='5432',
    database='mydb',
    sslmode='require'
)

# Get connection from pool
conn = db_pool.getconn()
# ... use connection ...
db_pool.putconn(conn)
```

### 6. Parameterized Queries

Prevent SQL injection:

```python
# Bad: Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE username = '{username}'"

# Good: Parameterized query
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

### 7. Rate Limiting

Implement rate limiting for database access:

```python
from redis import Redis
from ratelimit import limits, RateLimitException

redis_client = Redis(host='localhost', port=6379)

@limits(calls=10, period=60)  # 10 calls per minute
def query_database(user_id):
    # Database query
    pass
```

---

## Additional Resources

- PostgreSQL Security: https://www.postgresql.org/docs/current/security.html
- MySQL Security Guide: https://dev.mysql.com/doc/refman/8.0/en/security.html
- MongoDB Security Checklist: https://www.mongodb.com/docs/manual/administration/security-checklist/
- Redis Security: https://redis.io/docs/management/security/
- CIS Database Benchmarks: https://www.cisecurity.org/cis-benchmarks
