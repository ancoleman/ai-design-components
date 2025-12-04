---
sidebar_position: 5
---

# Secret Management

Master plan for secure handling of secrets, credentials, and sensitive configuration. Covers secret storage solutions, rotation strategies, least-privilege access patterns, and integration with CI/CD pipelines and application runtime environments.

## Key Topics

- **Secret Storage Solutions**: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager
- **Secret Rotation**: Automated rotation strategies, zero-downtime updates, and grace periods
- **Access Control**: RBAC, policy-based access, service identity management, and audit logging
- **Encryption at Rest**: Key encryption keys (KEK), data encryption keys (DEK), and envelope encryption
- **Encryption in Transit**: TLS/mTLS, certificate management, and secure key exchange
- **Secret Injection**: Environment variables, mounted volumes, sidecar containers, and init containers
- **Development Workflows**: Local development secrets, .env files, and git-secret/git-crypt
- **CI/CD Integration**: Pipeline secret handling, ephemeral credentials, and OIDC token exchange
- **Secret Scanning**: Pre-commit hooks, GitHub secret scanning, and leaked credential detection
- **Compliance**: SOC 2, PCI-DSS, HIPAA requirements for secret handling and audit trails

## Primary Tools & Technologies

**Secret Management Platforms:**
- HashiCorp Vault (self-hosted, dynamic secrets)
- AWS Secrets Manager (managed, AWS-native)
- Azure Key Vault (managed, Azure-native)
- Google Secret Manager (managed, GCP-native)
- Doppler, 1Password Secrets Automation (developer-focused)

**Kubernetes Secret Management:**
- External Secrets Operator (sync from external sources)
- Sealed Secrets (encrypted secrets in Git)
- SOPS (encrypted secrets with age/PGP)
- Vault Agent Injector (Vault integration)

**CI/CD Integration:**
- GitHub Actions secrets, GitLab CI/CD variables
- OIDC federation (GitHub → AWS, Azure, GCP)
- Vault agent for ephemeral credentials

**Secret Scanning:**
- TruffleHog, GitLeaks (pre-commit hooks)
- GitHub secret scanning (automated detection)
- SpectralOps (real-time secret detection)

**Development Tools:**
- direnv (environment variable management)
- git-secret, git-crypt (encrypted secrets in repos)
- .env files with validation (dotenv, python-decouple)

## Integration Points

**Upstream Dependencies:**
- **Infrastructure as Code**: Secrets referenced in Terraform, CloudFormation, Pulumi
- **Container Orchestration**: Kubernetes Secret objects and CSI drivers

**Downstream Consumers:**
- **Data Architecture**: Database connection strings and credentials
- **Streaming Data**: Kafka broker credentials, schema registry authentication
- **Data Transformation**: Pipeline secrets for source/destination connections
- **SQL Optimization**: Secure credential passing for query execution

**Cross-Functional:**
- **Application Security**: API keys, OAuth tokens, JWT signing keys
- **Monitoring & Alerting**: Secret access logging and anomaly detection
- **Compliance & Audit**: Secret access trails and rotation evidence

## Status

**Master Plan Available** - Comprehensive guidance for secure secret management, covering Vault, cloud-native secret stores, rotation strategies, and CI/CD integration.

---

*Part of the Data Engineering skill collection focused on securing sensitive credentials and configuration data.*
