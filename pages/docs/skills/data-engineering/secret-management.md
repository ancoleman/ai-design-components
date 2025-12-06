---
sidebar_position: 5
title: Secret Management
description: Secure storage, rotation, and delivery of secrets with Vault and Kubernetes
tags: [data-engineering, security, vault, kubernetes, secrets, credentials, rotation]
---

# Secret Management

Secure storage, rotation, and delivery of secrets (API keys, database credentials, TLS certificates) for applications and infrastructure using HashiCorp Vault, cloud providers, and Kubernetes.

## When to Use

Use when:
- Storing API keys, database credentials, or encryption keys
- Implementing secret rotation (manual or automatic)
- Syncing secrets from external stores to Kubernetes
- Setting up dynamic secrets (database, cloud providers)
- Scanning code for leaked secrets
- Implementing zero-knowledge patterns
- Meeting compliance requirements (SOC 2, ISO 27001, PCI DSS)

## Key Features

### Static vs. Dynamic Secrets

| Secret Type | Use Dynamic? | TTL | Solution |
|-------------|-------------|-----|----------|
| Database credentials | YES | 1 hour | Vault DB engine |
| Cloud IAM (AWS/GCP) | YES | 15 min | Vault cloud engine |
| SSH/RDP access | YES | 5 min | Vault SSH engine |
| TLS certificates | YES | 24 hours | Vault PKI / cert-manager |
| Third-party API keys | NO | Quarterly | Vault KV v2 (manual rotation) |

### Kubernetes Secret Delivery

| Method | Use Case | Rotation | Restart Required |
|--------|----------|----------|------------------|
| **External Secrets Operator** | Static secrets, periodic sync | Polling (1h) | Yes |
| **Secrets Store CSI Driver** | File-based, watch rotation | inotify | No |
| **Vault Secrets Operator** | Vault-specific, dynamic | Automatic renewal | Optional |

## Quick Start

### HashiCorp Vault: Static Secrets (KV v2)

```bash
# Create secret
vault kv put secret/myapp/config api_key=sk_live_EXAMPLE

# Read secret
vault kv get secret/myapp/config

# List versions
vault kv metadata get secret/myapp/config
```

### Vault: Dynamic Database Credentials

```bash
# Configure PostgreSQL
vault write database/config/postgres \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb"

# Create role
vault write database/roles/app-role \
  db_name=postgres \
  creation_statements="CREATE ROLE \"{{name}}\"..." \
  default_ttl="1h"

# Generate credentials (auto-rotated)
vault read database/creds/app-role
```

### Kubernetes: External Secrets Operator (ESO)

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      auth:
        kubernetes:
          role: "app-role"
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: secret/data/database/config
```

### Python: Vault Integration (hvac)

```python
import hvac

client = hvac.Client(url='https://vault.example.com')
client.auth.kubernetes(role='app-role', jwt=jwt)

# Fetch dynamic credentials
response = client.secrets.database.generate_credentials(name='postgres-role')
username = response['data']['username']
password = response['data']['password']
```

## Decision Frameworks

### Choosing a Secret Store

| Scenario | Primary Choice | Alternative |
|----------|----------------|-------------|
| Kubernetes + Multi-Cloud | Vault + ESO | Cloud Secret Manager + ESO |
| Kubernetes + Single Cloud | Cloud Secret Manager + ESO | Vault + ESO |
| Serverless (AWS Lambda) | AWS Secrets Manager | AWS Parameter Store |
| Multi-Cloud Enterprise | HashiCorp Vault | Doppler (SaaS) |
| Small Team (&lt;10 apps) | Doppler, Infisical | 1Password Secrets Automation |
| GitOps-Centric | SOPS (git-encrypted) | Sealed Secrets (K8s-only) |

**Decision Tree**:
- Kubernetes? → External Secrets Operator (ESO) with chosen backend
- Single cloud? → Cloud-native (AWS/GCP/Azure)
- Multi-cloud/on-prem? → HashiCorp Vault
- GitOps? → SOPS or Sealed Secrets

## Secret Rotation Patterns

### Pattern 1: Versioned Static Secrets (Blue/Green)

1. Create new secret version in Vault
2. Update staging environment
3. Monitor for errors (24-48 hours)
4. Gradual production rollout (10% → 50% → 100%)
5. Revoke old secret (after 7 days)

### Pattern 2: Dynamic Database Credentials

Vault auto-generates credentials with short TTL:
- App fetches credentials from Vault
- Vault automatically renews lease (at 67% of TTL)
- On expiration, Vault revokes access
- On renewal failure, app requests new credentials

### Pattern 3: TLS Certificate Rotation

Using cert-manager + Vault PKI:
- cert-manager requests certificate from Vault
- Automatically renews before expiration (default: 67% of duration)
- Updates Kubernetes Secret on renewal
- Optional pod restart (via Reloader)

## Secret Scanning

### Pre-Commit Hooks (Gitleaks)

```bash
# Install Gitleaks
brew install gitleaks

# Run on staged files
gitleaks protect --staged --verbose
```

### CI/CD Integration (GitHub Actions)

```yaml
- name: Run Gitleaks
  uses: gitleaks/gitleaks-action@v2
```

### Remediation Workflow

When a secret is leaked:
1. **Rotate immediately** (within 1 hour)
2. **Revoke at provider**
3. **Remove from Git history** (BFG Repo-Cleaner)
4. **Force push** (notify team)
5. **Audit access** (who had access during leak window)
6. **Document incident**

## Library Recommendations (2025)

### Secret Stores

| Library | Use Case | Trust Score |
|---------|----------|-------------|
| HashiCorp Vault | Enterprise, multi-cloud | High (73.3/100) |
| External Secrets Operator | Kubernetes integration | High (85.0/100) |
| AWS Secrets Manager | AWS workloads | High |
| GCP Secret Manager | GCP workloads | High |
| Azure Key Vault | Azure workloads | High |

### Secret Scanning

| Library | Use Case | Trust Score |
|---------|----------|-------------|
| Gitleaks | Pre-commit, CI/CD | High (89.9/100) |
| TruffleHog | Git history scanning | Medium |

### Client Libraries

| Language | Library | Version |
|----------|---------|---------|
| Python | `hvac` | 2.2.0+ |
| Go | `vault/api` | Latest |
| TypeScript | `node-vault` | 0.10.2+ |
| Rust | `vaultrs` | 0.7+ |

## Security Best Practices

1. Never commit secrets to Git (use Gitleaks pre-commit hook)
2. Use dynamic secrets where possible
3. Rotate secrets regularly (quarterly for static, hourly for dynamic)
4. Implement least privilege (Vault policies, RBAC)
5. Enable audit logging
6. Encrypt at rest (Vault storage, etcd encryption)
7. Use short TTLs (< 24 hours for dynamic secrets)
8. Monitor failed access attempts

## Common Pitfalls

### Secrets in Environment Variables

Environment variables visible in process lists.

**Solution**: Use file-based secrets (Kubernetes volumes, CSI driver).

### Hardcoded Secrets in Manifests

Base64 is not encryption.

**Solution**: Use External Secrets Operator.

### No Secret Rotation

Stale credentials increase breach risk.

**Solution**: Use dynamic secrets or automate rotation.

### Root Token in Production

Unlimited permissions.

**Solution**: Use auth methods with least privilege policies.

## Related Skills

- [Data Architecture](./architecting-data) - Database credentials management
- [Streaming Data](./streaming-data) - Kafka authentication secrets
- [Performance Engineering](./performance-engineering) - API keys for monitoring tools

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/secret-management)
- [HashiCorp Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [External Secrets Operator](https://external-secrets.io/)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
