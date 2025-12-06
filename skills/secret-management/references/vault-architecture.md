# HashiCorp Vault Architecture

Comprehensive guide to Vault internals, high availability setup, policies, and production deployment patterns.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Secrets Engines](#secrets-engines)
3. [Authentication Methods](#authentication-methods)
4. [Policies and Access Control](#policies-and-access-control)
5. [Storage Backends](#storage-backends)
6. [High Availability Setup](#high-availability-setup)
7. [Audit Logging](#audit-logging)
8. [Production Deployment](#production-deployment)
9. [Common Pitfalls](#common-pitfalls)

## Architecture Overview

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│              HashiCorp Vault Architecture                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────┐         │
│  │         API Layer (HTTP/HTTPS)             │         │
│  │  ├── RESTful API                           │         │
│  │  ├── CLI (vault command)                   │         │
│  │  └── UI (Web interface)                    │         │
│  └────────────────┬───────────────────────────┘         │
│                   │                                      │
│                   ▼                                      │
│  ┌────────────────────────────────────────────┐         │
│  │      Authentication Methods                │         │
│  │  ├── Kubernetes (service accounts)         │         │
│  │  ├── JWT/OIDC (external identity)          │         │
│  │  ├── AppRole (machines, CI/CD)             │         │
│  │  ├── LDAP/Active Directory                 │         │
│  │  └── Token (direct auth)                   │         │
│  └────────────────┬───────────────────────────┘         │
│                   │                                      │
│                   ▼                                      │
│  ┌────────────────────────────────────────────┐         │
│  │         Core (Policy Engine)               │         │
│  │  ├── Request routing                       │         │
│  │  ├── Policy evaluation (HCL)               │         │
│  │  ├── Lease management                      │         │
│  │  └── Token generation                      │         │
│  └────────────────┬───────────────────────────┘         │
│                   │                                      │
│                   ▼                                      │
│  ┌────────────────────────────────────────────┐         │
│  │         Secrets Engines                    │         │
│  │  ├── KV v2 (versioned key-value)           │         │
│  │  ├── Database (dynamic credentials)        │         │
│  │  ├── AWS (dynamic IAM)                     │         │
│  │  ├── PKI (TLS certificates)                │         │
│  │  └── SSH (dynamic certificates)            │         │
│  └────────────────┬───────────────────────────┘         │
│                   │                                      │
│                   ▼                                      │
│  ┌────────────────────────────────────────────┐         │
│  │      Barrier (Encryption Layer)            │         │
│  │  ├── AES-256-GCM encryption                │         │
│  │  ├── Unsealing mechanism                   │         │
│  │  └── Master key protection                 │         │
│  └────────────────┬───────────────────────────┘         │
│                   │                                      │
│                   ▼                                      │
│  ┌────────────────────────────────────────────┐         │
│  │      Storage Backend                       │         │
│  │  ├── Consul (HA, recommended)              │         │
│  │  ├── etcd (Kubernetes native)              │         │
│  │  ├── S3 (cost-effective, no HA)            │         │
│  │  └── PostgreSQL (relational)               │         │
│  └────────────────────────────────────────────┘         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Request**: Client sends request (CLI, API, SDK)
2. **Authentication**: Vault validates identity (token, K8s SA, etc.)
3. **Authorization**: Policy engine evaluates permissions
4. **Secrets Engine**: Generates or retrieves secret
5. **Encryption**: Barrier encrypts data
6. **Storage**: Encrypted data written to backend
7. **Response**: Decrypted secret returned to client

## Secrets Engines

### KV v2 (Versioned Key-Value)

Static secrets with versioning and soft deletes.

**Enable:**
```bash
vault secrets enable -path=secret kv-v2
```

**Write Secret:**
```bash
vault kv put secret/myapp/config \
  api_key=sk_live_123 \
  database_url=postgresql://localhost/mydb
```

**Read Secret:**
```bash
vault kv get secret/myapp/config
vault kv get -version=2 secret/myapp/config  # Specific version
```

**Versioning:**
```bash
vault kv metadata get secret/myapp/config  # View all versions
vault kv undelete -versions=2 secret/myapp/config  # Restore deleted version
vault kv destroy -versions=1 secret/myapp/config  # Permanently delete
```

**Use Cases:**
- API keys (third-party services)
- OAuth client secrets
- Encryption keys (KEK)
- Configuration values

### Database Secrets Engine (Dynamic Credentials)

Auto-generates database credentials with TTL.

**Enable:**
```bash
vault secrets enable database
```

**Configure PostgreSQL:**
```bash
vault write database/config/postgres \
  plugin_name=postgresql-database-plugin \
  allowed_roles="app-role,readonly-role" \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb?sslmode=require" \
  username="vault-admin" \
  password="vault-admin-password"
```

**Create Role:**
```bash
vault write database/roles/app-role \
  db_name=postgres \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"
```

**Generate Credentials:**
```bash
vault read database/creds/app-role
# Output:
# Key                Value
# ---                -----
# lease_id           database/creds/app-role/abc123
# lease_duration     1h
# username           v-k8s-app-role-xyz789
# password           A1b2C3d4E5f6
```

**Rotation:**
```bash
# Rotate root credentials (Vault admin password)
vault write -force database/rotate-root/postgres
```

**Supported Databases:**
- PostgreSQL, MySQL, MongoDB
- MSSQL, Oracle, Cassandra
- Elasticsearch, InfluxDB
- Redshift, Snowflake

### AWS Secrets Engine (Dynamic IAM)

Auto-generates AWS IAM credentials.

**Enable:**
```bash
vault secrets enable aws
```

**Configure:**
```bash
vault write aws/config/root \
  access_key=AKIAIOSFODNN7EXAMPLE \
  secret_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
  region=us-east-1
```

**Create Role:**
```bash
vault write aws/roles/app-role \
  credential_type=iam_user \
  policy_document=-<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
EOF
```

**Generate Credentials:**
```bash
vault read aws/creds/app-role
# Output:
# Key                Value
# ---                -----
# lease_id           aws/creds/app-role/def456
# lease_duration     15m
# access_key         AKIAI44QH8DHBEXAMPLE
# secret_key         je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
```

**TTL:** Default 15 minutes, auto-revoked on expiration.

### PKI Secrets Engine (TLS Certificates)

Issues TLS certificates with automatic renewal.

**Enable:**
```bash
vault secrets enable pki
vault secrets tune -max-lease-ttl=8760h pki
```

**Generate Root CA:**
```bash
vault write pki/root/generate/internal \
  common_name=example.com \
  ttl=8760h
```

**Configure URLs:**
```bash
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com/v1/pki/crl"
```

**Create Role:**
```bash
vault write pki/roles/web-server \
  allowed_domains=example.com \
  allow_subdomains=true \
  max_ttl=72h
```

**Issue Certificate:**
```bash
vault write pki/issue/web-server \
  common_name=app.example.com \
  ttl=24h
# Returns: certificate, issuing_ca, private_key
```

## Authentication Methods

### Kubernetes Auth

Authenticate using Kubernetes service account tokens.

**Enable:**
```bash
vault auth enable kubernetes
```

**Configure:**
```bash
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc" \
  token_reviewer_jwt="<service-account-jwt>" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
```

**Create Role:**
```bash
vault write auth/kubernetes/role/app-role \
  bound_service_account_names=app-sa \
  bound_service_account_namespaces=production \
  policies=app-policy \
  ttl=1h
```

**Login (from pod):**
```bash
vault write auth/kubernetes/login \
  role=app-role \
  jwt=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
```

### JWT/OIDC Auth

Authenticate using external identity providers (Okta, Auth0, Google).

**Enable:**
```bash
vault auth enable oidc
```

**Configure:**
```bash
vault write auth/oidc/config \
  oidc_discovery_url="https://accounts.google.com" \
  oidc_client_id="<client-id>" \
  oidc_client_secret="<client-secret>" \
  default_role="default"
```

**Create Role:**
```bash
vault write auth/oidc/role/default \
  bound_audiences="<client-id>" \
  allowed_redirect_uris="https://vault.example.com/ui/vault/auth/oidc/oidc/callback" \
  user_claim="email" \
  policies=default
```

### AppRole Auth

Machine authentication for CI/CD, applications.

**Enable:**
```bash
vault auth enable approle
```

**Create Role:**
```bash
vault write auth/approle/role/ci-role \
  secret_id_ttl=10m \
  token_num_uses=10 \
  token_ttl=20m \
  token_max_ttl=30m \
  secret_id_num_uses=40 \
  policies=ci-policy
```

**Get RoleID:**
```bash
vault read auth/approle/role/ci-role/role-id
# role_id: 12345678-1234-1234-1234-123456789012
```

**Generate SecretID:**
```bash
vault write -f auth/approle/role/ci-role/secret-id
# secret_id: 87654321-4321-4321-4321-210987654321
```

**Login:**
```bash
vault write auth/approle/login \
  role_id=12345678-1234-1234-1234-123456789012 \
  secret_id=87654321-4321-4321-4321-210987654321
```

## Policies and Access Control

### Policy Syntax (HCL)

```hcl
# Read access to KV v2 secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Write access to specific secret
path "secret/data/myapp/config" {
  capabilities = ["create", "update", "read"]
}

# Dynamic database credentials
path "database/creds/app-role" {
  capabilities = ["read"]
}

# Deny all other paths
path "*" {
  capabilities = ["deny"]
}
```

**Capabilities:**
- `create`: Create new secrets
- `read`: Read existing secrets
- `update`: Update existing secrets
- `delete`: Delete secrets
- `list`: List secret paths
- `sudo`: Admin operations
- `deny`: Explicitly deny access

### Policy Templates

Dynamic policies using templates:

```hcl
# Policy for service accounts in specific namespace
path "secret/data/{{identity.entity.aliases.auth_kubernetes_abc123.metadata.service_account_namespace}}/*" {
  capabilities = ["read"]
}
```

### Writing Policies

```bash
# Write policy from file
vault policy write app-policy app-policy.hcl

# Write policy inline
vault policy write readonly-policy - <<EOF
path "secret/data/*" {
  capabilities = ["read", "list"]
}
EOF

# List policies
vault policy list

# Read policy
vault policy read app-policy
```

### Least Privilege Example

```hcl
# Application policy (minimal permissions)
path "secret/data/myapp/config" {
  capabilities = ["read"]
}

path "database/creds/app-role" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
```

## Storage Backends

### Consul (Recommended for HA)

**Pros:**
- High availability
- Automatic failover
- Service discovery
- Health checking

**Cons:**
- Requires separate Consul cluster
- More complex setup

**Configuration:**
```hcl
storage "consul" {
  address = "consul.example.com:8500"
  path    = "vault/"
  token   = "<consul-token>"
}
```

### etcd (Kubernetes Native)

**Pros:**
- Kubernetes native
- HA support
- Widely deployed

**Cons:**
- Performance at scale
- Requires etcd cluster

**Configuration:**
```hcl
storage "etcd" {
  address  = "https://etcd.example.com:2379"
  etcd_api = "v3"
  path     = "vault/"
  ha_enabled = "true"
}
```

### S3 (Cost-Effective)

**Pros:**
- Low cost
- Managed service
- Unlimited storage

**Cons:**
- No HA support
- Higher latency

**Configuration:**
```hcl
storage "s3" {
  bucket     = "vault-storage"
  region     = "us-east-1"
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG"
}
```

### PostgreSQL

**Pros:**
- Relational database
- Familiar tooling
- HA with replication

**Cons:**
- Not officially recommended
- Performance tuning needed

**Configuration:**
```hcl
storage "postgresql" {
  connection_url = "postgres://vault:password@postgres:5432/vault?sslmode=require"
  ha_enabled     = "true"
}
```

## High Availability Setup

### HA Architecture

```
┌────────────────────────────────────────────────┐
│         Vault HA Cluster (3 nodes)             │
├────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────┐ │
│  │   vault-0    │  │   vault-1    │  │vault-│ │
│  │   (Active)   │  │  (Standby)   │  │  2   │ │
│  │              │  │              │  │(Stand│ │
│  └──────┬───────┘  └──────┬───────┘  └──┬───┘ │
│         │                 │              │     │
│         └─────────────────┼──────────────┘     │
│                           │                    │
│                           ▼                    │
│              ┌─────────────────────┐           │
│              │   Storage Backend   │           │
│              │   (Consul/etcd)     │           │
│              └─────────────────────┘           │
│                                                 │
└────────────────────────────────────────────────┘
```

**Key Concepts:**
- One active node (handles requests)
- Multiple standby nodes (ready for failover)
- Automatic leader election
- Storage backend coordinates HA

### Kubernetes Deployment (HA)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vault
spec:
  serviceName: vault
  replicas: 3
  selector:
    matchLabels:
      app: vault
  template:
    metadata:
      labels:
        app: vault
    spec:
      containers:
      - name: vault
        image: hashicorp/vault:1.15
        args:
        - "server"
        - "-config=/vault/config/vault.hcl"
        ports:
        - containerPort: 8200
          name: api
        - containerPort: 8201
          name: cluster
        volumeMounts:
        - name: config
          mountPath: /vault/config
        - name: data
          mountPath: /vault/data
      volumes:
      - name: config
        configMap:
          name: vault-config
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

**vault.hcl:**
```hcl
storage "raft" {
  path    = "/vault/data"
  node_id = "vault-0"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 0
  tls_cert_file = "/vault/tls/tls.crt"
  tls_key_file  = "/vault/tls/tls.key"
}

api_addr = "https://vault-0.vault:8200"
cluster_addr = "https://vault-0.vault:8201"

ui = true
```

### Unsealing in HA

All nodes must be unsealed independently:

```bash
# Unseal each node (requires 3 of 5 key shares)
kubectl exec vault-0 -- vault operator unseal <KEY_SHARE_1>
kubectl exec vault-0 -- vault operator unseal <KEY_SHARE_2>
kubectl exec vault-0 -- vault operator unseal <KEY_SHARE_3>

kubectl exec vault-1 -- vault operator unseal <KEY_SHARE_1>
kubectl exec vault-1 -- vault operator unseal <KEY_SHARE_2>
kubectl exec vault-1 -- vault operator unseal <KEY_SHARE_3>

kubectl exec vault-2 -- vault operator unseal <KEY_SHARE_1>
kubectl exec vault-2 -- vault operator unseal <KEY_SHARE_2>
kubectl exec vault-2 -- vault operator unseal <KEY_SHARE_3>
```

**Auto-Unseal (Recommended for Production):**

Using cloud KMS (AWS, GCP, Azure):

```hcl
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/abc-def-ghi"
}
```

## Audit Logging

### Enable Audit Device

```bash
# File audit device
vault audit enable file file_path=/vault/logs/audit.log

# Syslog audit device
vault audit enable syslog tag="vault" facility="AUTH"

# Socket audit device
vault audit enable socket address="logstash.example.com:9090" socket_type="tcp"
```

### Audit Log Format

JSON format with request and response details:

```json
{
  "time": "2025-12-03T10:15:30Z",
  "type": "response",
  "auth": {
    "client_token": "hmac-sha256:abc123...",
    "accessor": "hmac-sha256:def456...",
    "display_name": "kubernetes-production-app-sa",
    "policies": ["app-policy", "default"]
  },
  "request": {
    "operation": "read",
    "path": "database/creds/app-role",
    "remote_address": "10.244.1.5"
  },
  "response": {
    "secret": {
      "lease_id": "database/creds/app-role/xyz789"
    }
  }
}
```

**Logged Information:**
- Authentication details
- Request path and operation
- Response (secrets are HMAC-hashed)
- Remote IP address
- Timestamp

## Production Deployment

### Checklist

- [ ] **TLS enabled** (never run Vault without TLS in production)
- [ ] **HA setup** (3+ nodes with Consul/etcd/Raft storage)
- [ ] **Auto-unseal** (AWS KMS, GCP KMS, Azure Key Vault)
- [ ] **Audit logging** (multiple devices for redundancy)
- [ ] **Backup strategy** (storage backend snapshots)
- [ ] **Monitoring** (Prometheus metrics, health checks)
- [ ] **Policies reviewed** (least privilege, no root tokens)
- [ ] **Secrets rotation** (quarterly for static, automatic for dynamic)
- [ ] **Disaster recovery** (tested restore procedure)

### Resource Requirements

**Development:**
- 1 CPU, 512 MB RAM
- Single node
- File storage backend

**Production (Small - <1000 secrets):**
- 2 CPU, 2 GB RAM per node
- 3 nodes (HA)
- Consul/etcd storage

**Production (Large - >10,000 secrets):**
- 4 CPU, 8 GB RAM per node
- 5+ nodes (HA)
- Dedicated storage cluster
- Load balancer

### Monitoring

**Prometheus Metrics:**
```yaml
# vault.hcl
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname = true
}
```

**Key Metrics:**
- `vault_core_unsealed`: Vault seal status (1 = unsealed)
- `vault_core_active`: Active node (1 = active, 0 = standby)
- `vault_token_count`: Total active tokens
- `vault_secret_lease_creation`: Secret lease generation rate
- `vault_runtime_alloc_bytes`: Memory usage

## Common Pitfalls

### Pitfall 1: Running Without TLS

**Problem:** Secrets transmitted in plaintext.

**Solution:**
```hcl
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 0  # NEVER set to 1 in production
  tls_cert_file = "/vault/tls/tls.crt"
  tls_key_file  = "/vault/tls/tls.key"
}
```

### Pitfall 2: Using Root Token

**Problem:** Unlimited permissions, no audit trail.

**Solution:** Delete root token after initial setup, use auth methods.

```bash
# Revoke root token
vault token revoke <ROOT_TOKEN>
```

### Pitfall 3: No Backup Strategy

**Problem:** Data loss on storage backend failure.

**Solution:** Regular snapshots of storage backend.

```bash
# Consul snapshot
consul snapshot save backup.snap

# etcd snapshot
ETCDCTL_API=3 etcdctl snapshot save backup.db
```

### Pitfall 4: Unsealing Delays

**Problem:** Manual unsealing after restart delays recovery.

**Solution:** Use auto-unseal with cloud KMS.

### Pitfall 5: Single Audit Device

**Problem:** Audit log failure blocks all requests.

**Solution:** Configure multiple audit devices (file + syslog).

```bash
vault audit enable file file_path=/vault/logs/audit.log
vault audit enable syslog tag="vault"
```

### Pitfall 6: No Lease Renewal

**Problem:** Dynamic secrets expire, causing app failures.

**Solution:** Implement lease renewal in application code.

```python
import time
import threading

def renew_lease(client, lease_id, lease_duration):
    renewal_time = lease_duration * 0.67  # Renew at 67% of TTL
    time.sleep(renewal_time)
    client.sys.renew_lease(lease_id)
```

### Pitfall 7: Hardcoded Policies in Code

**Problem:** Policy changes require code deployment.

**Solution:** Store policies as files, reference in Vault.

```bash
vault policy write app-policy /path/to/app-policy.hcl
```
