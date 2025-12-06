# Database Firewall Patterns

Firewall configurations for database servers with strict access control.


## Table of Contents

- [Core Principles](#core-principles)
- [UFW Configuration (PostgreSQL)](#ufw-configuration-postgresql)
- [nftables Configuration (PostgreSQL)](#nftables-configuration-postgresql)
- [AWS Security Group (RDS PostgreSQL)](#aws-security-group-rds-postgresql)
- [Database Types and Ports](#database-types-and-ports)
- [MySQL Example (nftables)](#mysql-example-nftables)
- [MongoDB Example (UFW)](#mongodb-example-ufw)
- [Connection Pooling Considerations](#connection-pooling-considerations)
- [Read Replicas](#read-replicas)
- [Database Monitoring Access](#database-monitoring-access)
- [Best Practices](#best-practices)
- [PostgreSQL SSL/TLS Enforcement](#postgresql-ssltls-enforcement)
- [Testing Database Firewall](#testing-database-firewall)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Core Principles

1. **Deny All by Default:** Database should not be accessible from Internet
2. **Application Tier Only:** Allow connections only from app servers
3. **SSH from Bastion:** Administrative access via bastion host
4. **No Direct Internet:** Database should not initiate outbound Internet connections
5. **Monitoring:** Enhanced logging for database access

## UFW Configuration (PostgreSQL)

```bash
# Database server (10.0.3.10)
# App servers: 10.0.2.10, 10.0.2.11, 10.0.2.12
# Bastion: 10.0.1.5

# Set defaults
sudo ufw default deny incoming
sudo ufw default deny outgoing  # Restrict outbound too

# Allow SSH from bastion only
sudo ufw allow from 10.0.1.5 to any port 22

# Allow PostgreSQL from app servers only
sudo ufw allow from 10.0.2.10 to any port 5432
sudo ufw allow from 10.0.2.11 to any port 5432
sudo ufw allow from 10.0.2.12 to any port 5432

# Or allow from entire app subnet
sudo ufw allow from 10.0.2.0/24 to any port 5432

# Allow outbound DNS (for name resolution)
sudo ufw allow out 53

# Allow outbound to VPC only (for responses)
sudo ufw allow out to 10.0.0.0/8

# Enable logging
sudo ufw logging on

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status verbose
```

## nftables Configuration (PostgreSQL)

```nftables
#!/usr/sbin/nft -f
# Database server firewall

flush ruleset

table inet filter {
    # App tier IPs
    set app_servers {
        type ipv4_addr
        elements = { 10.0.2.10, 10.0.2.11, 10.0.2.12 }
    }

    # Bastion IP
    set bastion {
        type ipv4_addr
        elements = { 10.0.1.5 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        iif "lo" accept
        ct state established,related accept
        ct state invalid drop

        # SSH from bastion only
        tcp dport 22 ip saddr @bastion accept

        # PostgreSQL from app servers only
        tcp dport 5432 ip saddr @app_servers ct state new limit rate 100/second accept

        # Log dropped connections
        log prefix "db-drop: " limit rate 5/minute level warn
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy drop;

        oif "lo" accept
        ct state established,related accept

        # DNS
        udp dport 53 accept
        tcp dport 53 accept

        # Internal network only (no Internet)
        ip daddr 10.0.0.0/8 accept

        # Log blocked egress
        log prefix "db-egress-block: " limit rate 2/minute level warn
    }
}
```

## AWS Security Group (RDS PostgreSQL)

```hcl
resource "aws_security_group" "database" {
  name        = "rds-postgresql-sg"
  description = "Security group for RDS PostgreSQL database"
  vpc_id      = aws_vpc.main.id

  # Inbound: PostgreSQL from app tier only
  ingress {
    description     = "PostgreSQL from app servers"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]  # Reference app SG
  }

  # Outbound: Minimal (local VPC only)
  egress {
    description = "Local VPC only"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  tags = {
    Name        = "rds-postgresql-sg"
    Environment = var.environment
    Tier        = "database"
  }
}

# RDS instance with security group
resource "aws_db_instance" "postgres" {
  identifier             = "myapp-postgres"
  engine                 = "postgres"
  engine_version         = "15.3"
  instance_class         = "db.t3.medium"
  allocated_storage      = 100
  db_name                = "myapp"
  username               = "dbadmin"
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.database.name

  # Network isolation
  publicly_accessible = false

  # Encryption
  storage_encrypted = true

  # Backups
  backup_retention_period = 7

  # Monitoring
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Name = "myapp-postgres"
  }
}
```

## Database Types and Ports

| Database | Default Port | Protocol |
|----------|-------------|----------|
| **PostgreSQL** | 5432 | TCP |
| **MySQL/MariaDB** | 3306 | TCP |
| **MongoDB** | 27017 | TCP |
| **Redis** | 6379 | TCP |
| **Cassandra** | 9042 | TCP |
| **Elasticsearch** | 9200 | TCP |
| **SQL Server** | 1433 | TCP |
| **Oracle** | 1521 | TCP |

## MySQL Example (nftables)

```nftables
table inet filter {
    set app_servers {
        type ipv4_addr
        elements = { 10.0.2.10, 10.0.2.11 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        iif "lo" accept
        ct state established,related accept

        # MySQL from app servers
        tcp dport 3306 ip saddr @app_servers accept

        # SSH from bastion
        tcp dport 22 ip saddr 10.0.1.5 accept
    }

    chain output {
        type filter hook output priority 0; policy drop;

        oif "lo" accept
        ct state established,related accept

        # DNS
        udp dport 53 accept

        # Internal only
        ip daddr 10.0.0.0/8 accept
    }
}
```

## MongoDB Example (UFW)

```bash
# MongoDB default port 27017
sudo ufw default deny incoming
sudo ufw default deny outgoing

# Allow from app servers
sudo ufw allow from 10.0.2.0/24 to any port 27017

# SSH from bastion
sudo ufw allow from 10.0.1.5 to any port 22

# Outbound DNS
sudo ufw allow out 53

# Outbound internal
sudo ufw allow out to 10.0.0.0/8

sudo ufw enable
```

## Connection Pooling Considerations

With connection poolers (PgBouncer, ProxySQL):

```bash
# Allow app servers to pooler
sudo ufw allow from 10.0.2.0/24 to any port 6432  # PgBouncer

# Allow pooler to database (localhost if on same host)
# Or if separate:
sudo ufw allow from <pooler-ip> to any port 5432
```

## Read Replicas

For database replication:

```bash
# On primary database
sudo ufw allow from <replica-ip> to any port 5432

# PostgreSQL replication (if using different port)
sudo ufw allow from <replica-ip> to any port 5433
```

## Database Monitoring Access

Allow monitoring tools:

```bash
# Prometheus postgres_exporter
sudo ufw allow from <monitoring-server> to any port 9187

# Or use localhost-only exporter
# postgres_exporter listens on 127.0.0.1:9187
# SSH tunnel from monitoring server
```

## Best Practices

1. **Never Expose to Internet:** Database should always be in private subnet
2. **Application Security Group Reference:** Use SG IDs, not IPs
3. **Egress Restrictions:** Prevent data exfiltration via outbound blocks
4. **Rate Limiting:** Limit connection attempts (nftables)
5. **Logging:** Enable comprehensive connection logging
6. **Encryption in Transit:** Require SSL/TLS connections
7. **No Root from Network:** Disable network root login (MySQL)
8. **VPC Peering:** Use VPC peering for cross-VPC database access
9. **PrivateLink:** Use AWS PrivateLink for secure cross-account access
10. **Backup Access:** Ensure backup tools can reach database

## PostgreSQL SSL/TLS Enforcement

In `/etc/postgresql/*/main/postgresql.conf`:

```
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
```

In `/etc/postgresql/*/main/pg_hba.conf`:

```
# Require SSL for all remote connections
hostssl all all 10.0.2.0/24 md5
```

## Testing Database Firewall

```bash
# From app server (should succeed)
psql -h 10.0.3.10 -U myapp -d mydb

# From bastion (should fail - database connection)
psql -h 10.0.3.10 -U myapp -d mydb

# From bastion (should succeed - SSH)
ssh admin@10.0.3.10

# From Internet (should timeout)
telnet <public-ip> 5432  # Should not be reachable
```

## Troubleshooting

**Can't connect from app server:**
- Check firewall allows app server IP: `sudo ufw status`
- Verify database listening: `ss -tuln | grep 5432`
- Check PostgreSQL config: `listen_addresses = '*'` in postgresql.conf
- Check pg_hba.conf allows app subnet

**Locked out of database server:**
- Use bastion to SSH: `ssh -J bastion admin@database`
- Check UFW status: `sudo ufw status`
- If needed, disable temporarily via console access

**Replication not working:**
- Ensure replica IP allowed on primary database
- Check firewall on both primary and replica
- Verify replication port (often same as main port)

## Resources

- PostgreSQL Security: https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
- MySQL Security: https://dev.mysql.com/doc/refman/8.0/en/security.html
- For AWS RDS Security Groups configuration, see the main SKILL.md
- For nftables and UFW patterns, see the main SKILL.md
