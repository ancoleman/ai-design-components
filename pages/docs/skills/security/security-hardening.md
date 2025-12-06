---
sidebar_position: 7
title: Security Hardening
description: Reduce attack surface across OS, container, cloud, network, and database layers
tags: [security, hardening, cis-benchmarks, containers, zero-trust, compliance]
---

# Security Hardening

Proactive reduction of attack surface across infrastructure layers through systematic configuration hardening, least-privilege enforcement, and automated security controls using CIS Benchmarks and zero-trust principles.

## When to Use

Invoke this skill when:
- Hardening production infrastructure before deployment
- Meeting compliance requirements (SOC 2, PCI-DSS, HIPAA, FedRAMP)
- Implementing zero-trust security architecture
- Reducing container or cloud misconfiguration risks
- Preparing for security audits or penetration tests
- Automating security baseline enforcement
- Responding to vulnerability scan findings

## Key Features

**Hardening Layers:**
- **OS (Linux)**: Kernel tuning, SSH hardening, SELinux/AppArmor, service minimization
- **Container**: Minimal base images, non-root execution, read-only filesystems, seccomp profiles
- **Cloud**: IAM least privilege, encryption, public access blocking, CSPM integration
- **Network**: Default-deny policies, segmentation, TLS/mTLS enforcement
- **Database**: Authentication hardening, connection encryption, audit logging, RBAC

**CIS Benchmark Integration:**
- Docker CIS Benchmark: docker-bench-security
- Kubernetes CIS Benchmark: kube-bench
- Linux CIS Benchmark: Lynis, OpenSCAP
- Automated scanning and compliance reporting

**Container Base Image Selection:**
- **Production**: Chainguard Images (~10MB, 0 CVEs) or Distroless (~20MB, minimal CVEs)
- **Development**: Alpine (~5MB, small attack surface)
- **Compatibility**: Debian slim (~80MB, debugging tools)
- **Legacy**: Ubuntu (~100MB, full compatibility)

**Automation Tools:**
- **Configuration Management**: Ansible, Puppet, Chef
- **IaC Security**: Terraform, Checkov, Terrascan
- **Policy Enforcement**: OPA/Gatekeeper, Kyverno
- **Scanning**: Trivy, Grype, Prowler, ScoutSuite, Lynis

## Quick Start

```bash
# Harden SSH Access
# Edit /etc/ssh/sshd_config.d/hardening.conf
PermitRootLogin no
PasswordAuthentication no
PermitEmptyPasswords no
MaxAuthTries 3
X11Forwarding no
ClientAliveInterval 300
ClientAliveCountMax 2

# Restart SSH
systemctl restart sshd
```

**Harden Container Image:**

```dockerfile
# Use minimal base
FROM cgr.dev/chainguard/python:latest

# Non-root user
USER nonroot

# Read-only filesystem
COPY --chown=nonroot:nonroot app /app
WORKDIR /app

# Drop all capabilities
ENTRYPOINT ["python", "-m", "app"]
```

**Harden Kubernetes Pod:**

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 65534
  seccompProfile:
    type: RuntimeDefault
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

**Harden AWS S3 Bucket:**

```hcl
resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
```

**Automated CIS Scanning:**

```bash
# Docker CIS Benchmark
docker run --rm -it \
  --net host \
  --pid host \
  --cap-add audit_control \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /etc:/etc:ro \
  docker/docker-bench-security

# Kubernetes CIS Benchmark
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs job/kube-bench

# Linux CIS Benchmark
lynis audit system --quick
```

**Continuous Verification Pipeline:**

```yaml
# GitHub Actions: Security Hardening Verification
name: Security Hardening Verification

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily scan

jobs:
  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t myapp:test .

      - name: Scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:test'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail on findings

  iac-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan IaC with Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          soft_fail: false
```

## Core Hardening Principles

1. **Default Deny, Explicit Allow**: Start with all access denied, permit only required operations
2. **Least Privilege Access**: Grant minimum permissions required for operation
3. **Defense in Depth**: Multiple overlapping security controls
4. **Minimal Attack Surface**: Remove unnecessary components, services, permissions
5. **Fail Securely**: Default to secure state on error or misconfiguration

## Hardening Priority Framework

**Critical Priority: Internet-Facing Systems**
- Container hardening (minimal images, non-root, read-only)
- Network segmentation (DMZ, WAF, DDoS protection)
- TLS termination and certificate management
- Rate limiting and authentication
- Real-time monitoring and alerting

**High Priority: Systems with Sensitive Data**
- Encryption at rest (AES-256, KMS-managed keys)
- Strict access controls (RBAC, least privilege)
- Comprehensive audit logging
- Database connection encryption
- Regular vulnerability scanning

**Standard Priority: Internal Systems**
- OS hardening (CIS Benchmarks)
- Service minimization
- Patch management automation
- Configuration management
- Basic monitoring

## Related Skills

- [Security Architecture](./architecting-security.md) - Strategic security design and defense-in-depth
- [Implementing Compliance](./implementing-compliance.md) - Map hardening to compliance frameworks
- [Managing Vulnerabilities](./managing-vulnerabilities.md) - Continuous vulnerability scanning
- [Configuring Firewalls](./configuring-firewalls.md) - Network layer hardening
- [Implementing TLS](./implementing-tls.md) - Encryption and certificate management

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/security-hardening)
