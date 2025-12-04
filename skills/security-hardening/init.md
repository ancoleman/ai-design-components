# Security Hardening Skill - Master Plan

**Skill Name:** `security-hardening`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Hardening Taxonomy](#hardening-taxonomy)
5. [CIS Benchmark Mapping](#cis-benchmark-mapping)
6. [Decision Frameworks](#decision-frameworks)
7. [Multi-Language Implementations](#multi-language-implementations)
8. [Verification and Auditing](#verification-and-auditing)
9. [Tool Recommendations](#tool-recommendations)
10. [Skill Structure Design](#skill-structure-design)
11. [Integration Points](#integration-points)
12. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Security hardening is the proactive reduction of attack surface across all infrastructure layers. In 2025, with zero-trust architectures, supply chain attacks, and regulatory pressures, systematic hardening is essential.

**Market Drivers:**
- **Zero Trust Adoption:** Assume breach, verify everything
- **Supply Chain Security:** SBOM requirements, container scanning
- **Compliance Mandates:** SOC2, PCI-DSS, HIPAA require hardening evidence
- **Container Proliferation:** 80%+ production workloads in containers
- **Cloud Misconfigurations:** #1 cause of cloud breaches

**Strategic Value:**
1. **Preventive Security:** Reduce attack surface before incidents
2. **Compliance Enabler:** Meet regulatory requirements systematically
3. **Automation Focus:** Codified, repeatable hardening
4. **Multi-Layer:** OS, container, cloud, network, database

### How This Differs from Existing Solutions

**Existing Security Documentation:**
- **Vendor-Specific:** AWS hardening OR Linux hardening, not unified
- **Checklist-Oriented:** "Do these 100 things" without prioritization
- **Manual Focus:** Assumes human execution, not automation

**Our Approach:**
- **Layer-Based Taxonomy:** OS → Container → Cloud → Network → Database
- **CIS Benchmark Mapping:** Industry-standard controls
- **Automation-First:** Scripts and tools for every hardening action
- **Verification Built-In:** How to prove hardening is applied

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **OS Hardening**
   - Linux kernel parameters
   - User and group management
   - File permissions and ownership
   - Service minimization
   - SSH hardening

2. **Container Hardening**
   - Minimal base images
   - Non-root containers
   - Read-only filesystems
   - Resource limits
   - Seccomp and AppArmor profiles

3. **Cloud Configuration Hardening**
   - IAM policies and least privilege
   - Network security groups
   - Encryption at rest and in transit
   - Logging and monitoring
   - Public exposure prevention

4. **Network Hardening**
   - Firewall configuration
   - Network segmentation
   - TLS/mTLS enforcement
   - DNS security

5. **Database Hardening**
   - Authentication and authorization
   - Encryption configuration
   - Audit logging
   - Network isolation

### What This Skill Does NOT Cover

- Authentication/authorization patterns (use auth-security skill)
- Secret management (use secret-management skill)
- Incident response (different skill domain)
- Penetration testing (offensive security)

---

## Research Findings

### Google Search Grounding (December 2025)

**Key 2025 Trends:**
- Zero Trust architecture is now baseline expectation
- Container security shifting left into CI/CD
- SBOM (Software Bill of Materials) becoming mandatory
- AI-driven threat detection supplementing hardening
- CIS Benchmarks v8 widely adopted

**Container Security Focus:**
- Image scanning in CI/CD pipeline
- Runtime security with Falco
- Network policies by default
- Supply chain security (Sigstore, SLSA)

**Linux Hardening Focus:**
- SELinux/AppArmor enforcement
- Kernel hardening (sysctl)
- Minimal installations
- Automated patching

**Cloud Hardening Focus:**
- CSPM (Cloud Security Posture Management) tools
- Infrastructure as Code security scanning
- Workload identity (no long-lived credentials)
- Default encryption everywhere

---

## Hardening Taxonomy

### Layer 1: Operating System (Linux)

**1.1 Kernel Hardening**
```bash
# /etc/sysctl.d/99-hardening.conf

# Disable IP forwarding (unless router)
net.ipv4.ip_forward = 0

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Enable TCP SYN cookies
net.ipv4.tcp_syncookies = 1

# Disable source routing
net.ipv4.conf.all.accept_source_route = 0

# Enable ASLR
kernel.randomize_va_space = 2

# Restrict kernel pointer exposure
kernel.kptr_restrict = 2

# Restrict dmesg access
kernel.dmesg_restrict = 1

# Restrict ptrace
kernel.yama.ptrace_scope = 2
```

**1.2 SSH Hardening**
```bash
# /etc/ssh/sshd_config.d/hardening.conf

# Disable root login
PermitRootLogin no

# Disable password authentication
PasswordAuthentication no

# Use only SSH Protocol 2
Protocol 2

# Limit authentication attempts
MaxAuthTries 3

# Disable empty passwords
PermitEmptyPasswords no

# Disable X11 forwarding
X11Forwarding no

# Set idle timeout
ClientAliveInterval 300
ClientAliveCountMax 2

# Limit users
AllowGroups ssh-users
```

**1.3 User and Group Management**
```bash
#!/bin/bash
# scripts/harden-users.sh

# Set password policies
sed -i 's/PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/' /etc/login.defs
sed -i 's/PASS_MIN_DAYS.*/PASS_MIN_DAYS 7/' /etc/login.defs
sed -i 's/PASS_MIN_LEN.*/PASS_MIN_LEN 14/' /etc/login.defs

# Lock system accounts
for user in bin daemon adm lp sync shutdown halt mail news uucp operator games gopher ftp nobody; do
  passwd -l $user 2>/dev/null
  usermod -s /sbin/nologin $user 2>/dev/null
done

# Set umask
echo "umask 027" >> /etc/profile.d/hardening.sh
```

**1.4 File System Hardening**
```bash
# /etc/fstab additions

# /tmp with noexec, nosuid, nodev
tmpfs /tmp tmpfs defaults,noexec,nosuid,nodev,size=2G 0 0

# /var/tmp bind mount to /tmp
/tmp /var/tmp none bind 0 0

# /home with nosuid, nodev
/dev/mapper/vg-home /home ext4 defaults,nosuid,nodev 0 2
```

### Layer 2: Container Hardening

**2.1 Dockerfile Best Practices**
```dockerfile
# Use minimal base image
FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/app/deps

# Production image
FROM cgr.dev/chainguard/python:latest

# Run as non-root
USER nonroot

WORKDIR /app
COPY --from=builder /app/deps /app/deps
COPY --chown=nonroot:nonroot . .

ENV PYTHONPATH=/app/deps

# Read-only filesystem compatible
ENTRYPOINT ["python", "-m", "app"]
```

**2.2 Kubernetes Pod Security**
```yaml
# Hardened pod security context
apiVersion: v1
kind: Pod
metadata:
  name: hardened-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65534
    runAsGroup: 65534
    fsGroup: 65534
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    resources:
      limits:
        memory: "256Mi"
        cpu: "500m"
      requests:
        memory: "128Mi"
        cpu: "100m"
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```

**2.3 Pod Security Standards**
```yaml
# Enforce restricted pod security standard
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Layer 3: Cloud Configuration Hardening

**3.1 AWS IAM Hardening**
```hcl
# Least privilege IAM policy
resource "aws_iam_policy" "app_policy" {
  name = "app-least-privilege"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3ReadOnly"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.app_data.arn,
          "${aws_s3_bucket.app_data.arn}/*"
        ]
      }
    ]
  })
}

# Deny all by default, require MFA for sensitive actions
resource "aws_iam_policy" "mfa_required" {
  name = "mfa-required-sensitive"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyWithoutMFA"
        Effect = "Deny"
        Action = [
          "iam:*",
          "organizations:*",
          "account:*"
        ]
        Resource = "*"
        Condition = {
          BoolIfExists = {
            "aws:MultiFactorAuthPresent" = "false"
          }
        }
      }
    ]
  })
}
```

**3.2 S3 Bucket Hardening**
```hcl
resource "aws_s3_bucket" "secure" {
  bucket = "company-secure-bucket"
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.secure.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
    bucket_key_enabled = true
  }
}

# Enable versioning
resource "aws_s3_bucket_versioning" "secure" {
  bucket = aws_s3_bucket.secure.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable logging
resource "aws_s3_bucket_logging" "secure" {
  bucket = aws_s3_bucket.secure.id

  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3-access-logs/"
}
```

### Layer 4: Network Hardening

**4.1 Network Policy (Kubernetes)**
```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
# Allow only specific communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

**4.2 AWS Security Group Hardening**
```hcl
# Minimal security group
resource "aws_security_group" "web" {
  name        = "web-hardened"
  description = "Hardened web security group"
  vpc_id      = aws_vpc.main.id

  # Only allow HTTPS from ALB
  ingress {
    description     = "HTTPS from ALB"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  # Egress only to specific destinations
  egress {
    description     = "Database access"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.db.id]
  }

  egress {
    description = "HTTPS outbound"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-hardened"
  }
}
```

### Layer 5: Database Hardening

**5.1 PostgreSQL Hardening**
```sql
-- Revoke public permissions
REVOKE ALL ON DATABASE production FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM PUBLIC;

-- Create application role with minimal permissions
CREATE ROLE app_user WITH LOGIN PASSWORD 'use_vault_for_this';
GRANT CONNECT ON DATABASE production TO app_user;
GRANT USAGE ON SCHEMA app TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA app GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- Disable superuser connections except from trusted hosts
-- In pg_hba.conf:
-- local   all   postgres   peer
-- host    all   postgres   127.0.0.1/32   scram-sha-256
-- hostssl all   all        0.0.0.0/0      scram-sha-256

-- Enable audit logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
```

**5.2 RDS Hardening (Terraform)**
```hcl
resource "aws_db_instance" "hardened" {
  identifier = "hardened-postgres"

  # Encryption
  storage_encrypted   = true
  kms_key_id          = aws_kms_key.rds.arn

  # Network isolation
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.private.name
  vpc_security_group_ids = [aws_security_group.db.id]

  # Authentication
  iam_database_authentication_enabled = true

  # Logging
  enabled_cloudwatch_logs_exports = [
    "postgresql",
    "upgrade"
  ]

  # Backups
  backup_retention_period = 30
  backup_window          = "03:00-04:00"

  # Maintenance
  auto_minor_version_upgrade = true
  maintenance_window         = "Mon:04:00-Mon:05:00"

  # Deletion protection
  deletion_protection = true
  skip_final_snapshot = false
}
```

---

## CIS Benchmark Mapping

### CIS Controls v8 Mapping

| CIS Control | Hardening Action | Layer |
|-------------|------------------|-------|
| 1.1 | Asset inventory | All |
| 2.1 | Authorized software list | Container |
| 3.1 | Data protection | Cloud, DB |
| 4.1 | Secure configuration | OS, Container, Cloud |
| 5.1 | Account management | OS, Cloud |
| 6.1 | Access control | All |
| 7.1 | Vulnerability management | Container |
| 8.1 | Audit log management | All |
| 10.1 | Malware defenses | OS |
| 12.1 | Network monitoring | Network |
| 13.1 | Service provider management | Cloud |

### Automated CIS Scanning

```bash
# Docker CIS Benchmark
docker run --rm -it \
  --net host \
  --pid host \
  --userns host \
  --cap-add audit_control \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /etc:/etc:ro \
  docker/docker-bench-security

# Kubernetes CIS Benchmark
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs job/kube-bench
```

---

## Decision Frameworks

### Framework 1: Hardening Priority

```
START
  │
  ├─► Internet-facing?
  │     YES ──► CRITICAL PRIORITY
  │             - Container hardening
  │             - Network segmentation
  │             - WAF/DDoS protection
  │     NO ──► Contains sensitive data?
  │              YES ──► HIGH PRIORITY
  │                      - Encryption at rest
  │                      - Access controls
  │                      - Audit logging
  │              NO ──► STANDARD PRIORITY
  │                     - OS hardening
  │                     - Least privilege
```

### Framework 2: Container Base Image Selection

| Use Case | Recommended Base | Size | CVEs |
|----------|------------------|------|------|
| Production apps | Chainguard Images | ~10MB | 0 |
| Minimal Linux | Alpine | ~5MB | Few |
| Compatibility | Distroless | ~20MB | Few |
| Debugging | Debian slim | ~80MB | More |
| Legacy apps | Ubuntu | ~100MB | Many |

### Framework 3: Compliance Mapping

| Requirement | Controls | Tools |
|-------------|----------|-------|
| SOC 2 | CIS, encryption, logging | Checkov, Prowler |
| PCI DSS | Network seg, access, encrypt | Qualys, Nessus |
| HIPAA | Access control, audit, encrypt | Prowler, ScoutSuite |
| FedRAMP | CIS, STIG, encryption | OpenSCAP |

---

## Multi-Language Implementations

### Python: Hardening Automation

```python
# scripts/harden_linux.py
import subprocess
import os
from pathlib import Path

class LinuxHardener:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.changes = []

    def apply_sysctl(self, settings: dict[str, str]) -> None:
        """Apply kernel parameters."""
        sysctl_file = Path("/etc/sysctl.d/99-hardening.conf")

        content = "# Security hardening parameters\n"
        for key, value in settings.items():
            content += f"{key} = {value}\n"

        if not self.dry_run:
            sysctl_file.write_text(content)
            subprocess.run(["sysctl", "--system"], check=True)

        self.changes.append(f"Applied {len(settings)} sysctl settings")

    def harden_ssh(self) -> None:
        """Apply SSH hardening configuration."""
        ssh_config = """
# Hardening configuration
PermitRootLogin no
PasswordAuthentication no
PermitEmptyPasswords no
X11Forwarding no
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
"""
        config_file = Path("/etc/ssh/sshd_config.d/hardening.conf")

        if not self.dry_run:
            config_file.write_text(ssh_config)
            subprocess.run(["systemctl", "reload", "sshd"], check=True)

        self.changes.append("Applied SSH hardening")

    def audit(self) -> dict:
        """Audit current hardening status."""
        results = {}

        # Check SSH config
        results["ssh_root_login"] = self._check_ssh_setting("PermitRootLogin", "no")
        results["ssh_password_auth"] = self._check_ssh_setting("PasswordAuthentication", "no")

        # Check kernel params
        results["aslr_enabled"] = self._check_sysctl("kernel.randomize_va_space", "2")
        results["ip_forward_disabled"] = self._check_sysctl("net.ipv4.ip_forward", "0")

        return results

    def _check_sysctl(self, key: str, expected: str) -> bool:
        result = subprocess.run(
            ["sysctl", "-n", key],
            capture_output=True, text=True
        )
        return result.stdout.strip() == expected

    def _check_ssh_setting(self, key: str, expected: str) -> bool:
        result = subprocess.run(
            ["sshd", "-T"],
            capture_output=True, text=True
        )
        for line in result.stdout.lower().split("\n"):
            if line.startswith(key.lower()):
                return expected.lower() in line
        return False


if __name__ == "__main__":
    hardener = LinuxHardener(dry_run=True)

    hardener.apply_sysctl({
        "kernel.randomize_va_space": "2",
        "net.ipv4.ip_forward": "0",
        "net.ipv4.conf.all.accept_redirects": "0",
    })

    hardener.harden_ssh()

    print("Audit results:", hardener.audit())
    print("Changes:", hardener.changes)
```

### Bash: Hardening Scripts

```bash
#!/bin/bash
# scripts/harden-container-host.sh
set -euo pipefail

echo "=== Container Host Hardening ==="

# Ensure Docker daemon is hardened
cat > /etc/docker/daemon.json <<EOF
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "seccomp-profile": "/etc/docker/seccomp/default.json",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
EOF

# Restart Docker
systemctl restart docker

# Verify settings
docker info --format '{{.SecurityOptions}}'

echo "=== Container host hardening complete ==="
```

### Go: Security Scanner Integration

```go
// tools/scanner/main.go
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os/exec"
)

type ScanResult struct {
	Target          string          `json:"target"`
	Vulnerabilities []Vulnerability `json:"vulnerabilities"`
	Misconfigs      []Misconfig     `json:"misconfigurations"`
}

type Vulnerability struct {
	ID       string `json:"id"`
	Severity string `json:"severity"`
	Title    string `json:"title"`
}

type Misconfig struct {
	ID       string `json:"id"`
	Severity string `json:"severity"`
	Title    string `json:"title"`
}

func ScanImage(ctx context.Context, image string) (*ScanResult, error) {
	cmd := exec.CommandContext(ctx, "trivy", "image",
		"--format", "json",
		"--severity", "HIGH,CRITICAL",
		image,
	)

	output, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("trivy scan failed: %w", err)
	}

	var result ScanResult
	if err := json.Unmarshal(output, &result); err != nil {
		return nil, fmt.Errorf("parse result: %w", err)
	}

	return &result, nil
}

func ScanKubernetes(ctx context.Context, namespace string) (*ScanResult, error) {
	cmd := exec.CommandContext(ctx, "trivy", "k8s",
		"--format", "json",
		"--namespace", namespace,
		"--severity", "HIGH,CRITICAL",
	)

	output, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("trivy k8s scan failed: %w", err)
	}

	var result ScanResult
	if err := json.Unmarshal(output, &result); err != nil {
		return nil, fmt.Errorf("parse result: %w", err)
	}

	return &result, nil
}

func main() {
	ctx := context.Background()

	result, err := ScanImage(ctx, "myapp:latest")
	if err != nil {
		panic(err)
	}

	fmt.Printf("Found %d vulnerabilities\n", len(result.Vulnerabilities))
}
```

---

## Verification and Auditing

### Automated Verification Pipeline

```yaml
# .github/workflows/security-scan.yml
name: Security Hardening Verification

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  iac-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          soft_fail: false

  k8s-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Kubesec
        run: |
          docker run -i kubesec/kubesec:latest scan - < k8s/deployment.yaml
```

### Compliance Reporting

```python
# scripts/compliance_report.py
from datetime import datetime
import json

def generate_compliance_report(scan_results: dict) -> dict:
    """Generate compliance report from scan results."""

    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "framework": "CIS Kubernetes Benchmark v1.8",
        "summary": {
            "total_checks": 0,
            "passed": 0,
            "failed": 0,
            "score": 0.0
        },
        "controls": []
    }

    for control_id, result in scan_results.items():
        report["summary"]["total_checks"] += 1
        if result["status"] == "PASS":
            report["summary"]["passed"] += 1
        else:
            report["summary"]["failed"] += 1

        report["controls"].append({
            "id": control_id,
            "title": result["title"],
            "status": result["status"],
            "remediation": result.get("remediation", "")
        })

    total = report["summary"]["total_checks"]
    passed = report["summary"]["passed"]
    report["summary"]["score"] = round((passed / total) * 100, 2) if total > 0 else 0

    return report
```

---

## Tool Recommendations

### Scanning Tools

| Tool | Purpose | Languages |
|------|---------|-----------|
| **Trivy** | Container & IaC scanning | Go |
| **Checkov** | IaC security | Python |
| **Falco** | Runtime security | C++ |
| **OPA/Gatekeeper** | Policy enforcement | Rego |
| **Kyverno** | K8s policy | YAML |
| **Prowler** | AWS security | Python |
| **ScoutSuite** | Multi-cloud audit | Python |

### Hardening Tools

| Tool | Purpose |
|------|---------|
| **Lynis** | Linux auditing |
| **Docker Bench** | Docker CIS |
| **kube-bench** | K8s CIS |
| **OpenSCAP** | Compliance scanning |

---

## Skill Structure Design

```
security-hardening/
├── SKILL.md                         # Main skill (400-500 lines)
├── references/
│   ├── linux-hardening.md           # OS-level hardening
│   ├── container-hardening.md       # Docker/K8s hardening
│   ├── cloud-hardening.md           # AWS/GCP/Azure
│   ├── network-hardening.md         # Firewalls, segmentation
│   ├── database-hardening.md        # PostgreSQL, MySQL, etc.
│   └── cis-benchmark-mapping.md     # Control mapping
├── examples/
│   ├── linux/
│   │   ├── sysctl-hardening.conf
│   │   └── ssh-hardening.conf
│   ├── kubernetes/
│   │   ├── pod-security-policy.yaml
│   │   └── network-policy.yaml
│   └── terraform/
│       ├── s3-hardening/
│       └── iam-hardening/
└── scripts/
    ├── harden-linux.py
    ├── harden-container-host.sh
    ├── audit-compliance.py
    └── scan-infrastructure.sh
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `auth-security` | Hardening complements auth patterns |
| `kubernetes-operations` | Pod security, RBAC, network policies |
| `infrastructure-as-code` | IaC security scanning |
| `building-ci-pipelines` | Security scanning in CI |
| `secret-management` | Secure secret handling |
| `observability` | Security monitoring and alerting |

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Linux hardening patterns
- [ ] Container hardening best practices
- [ ] CIS benchmark mapping

### Phase 2: Cloud & Network (Week 3-4)
- [ ] AWS/GCP/Azure hardening
- [ ] Network security patterns
- [ ] Database hardening

### Phase 3: Automation (Week 5-6)
- [ ] Python automation scripts
- [ ] CI/CD integration
- [ ] Compliance reporting

### Phase 4: Verification (Week 7-8)
- [ ] Scanning tool integration
- [ ] Audit playbooks
- [ ] Polish and review

---

## Key Takeaways

1. **Layer-based approach** - OS → Container → Cloud → Network → Database
2. **Automation-first** - Every hardening action should be scripted
3. **Verification built-in** - Prove hardening is applied
4. **CIS Benchmarks** - Industry-standard baseline
5. **Continuous scanning** - Security is ongoing, not one-time
6. **Least privilege** - Default deny, explicit allow

---

**Progressive disclosure:** This init.md provides the master plan. Detailed documentation in `references/` directory.
