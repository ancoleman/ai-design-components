---
sidebar_position: 3
title: Security Hardening
description: Multi-layer security hardening across OS, containers, cloud, network, and database with CIS Benchmark mapping
tags: [master-plan, finops, security, hardening, cis-benchmark]
---

# Security Hardening

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Systematic security hardening across all infrastructure layers with automation-first approach and CIS Benchmark mapping.

## Scope

This skill provides layer-based hardening patterns:

- **OS Hardening** - Linux kernel parameters, SSH, user management, file permissions
- **Container Hardening** - Minimal base images, non-root, read-only filesystems, Seccomp/AppArmor
- **Cloud Configuration** - IAM least privilege, encryption, logging, private endpoints
- **Network Hardening** - Firewalls, segmentation, TLS enforcement, DNS security
- **Database Hardening** - Authentication, encryption, audit logging, network isolation
- **CIS Benchmark Mapping** - Industry-standard controls (v8)

## Key Components

- **Layer-Based Taxonomy** - OS → Container → Cloud → Network → Database
- **Automation-First** - Scripts and tools for every hardening action
- **CIS Benchmark Compliance** - Map to CIS Controls v8
- **Verification Built-In** - Prove hardening is applied (audit scripts)
- **Container Security** - Chainguard/Distroless images (0 CVEs), non-root, read-only
- **Zero Trust Principles** - Assume breach, verify everything

## Decision Framework

**Hardening Priority:**
```
CRITICAL: Internet-facing resources
- Container hardening
- Network segmentation
- WAF/DDoS protection

HIGH: Contains sensitive data
- Encryption at rest/in transit
- Access controls
- Audit logging

STANDARD: Internal resources
- OS hardening
- Least privilege IAM
```

**Container Base Image Selection:**
```
Production apps → Chainguard Images (~10MB, 0 CVEs)
Minimal Linux → Alpine (~5MB)
Compatibility → Distroless (~20MB)
Debugging → Debian slim (~80MB)
```

## Tool Recommendations

**Scanning Tools:**
- **Trivy** - Container & IaC vulnerability scanning
- **Checkov** - IaC security policy enforcement
- **Falco** - Kubernetes runtime security
- **OPA/Gatekeeper** - Policy-as-code enforcement
- **Prowler** - AWS security audit (CIS, PCI-DSS, HIPAA)

**Hardening Tools:**
- **Lynis** - Linux security auditing
- **Docker Bench Security** - Docker CIS benchmark
- **kube-bench** - Kubernetes CIS benchmark
- **OpenSCAP** - Compliance scanning (SCAP, STIG)

## Integration Points

- `securing-authentication` - Hardening complements authentication patterns
- `operating-kubernetes` - Pod security, RBAC, network policies
- `writing-infrastructure-code` - IaC security scanning with Checkov
- `building-ci-pipelines` - Security scanning in CI (shift-left)
- `secret-management` - Secure secret handling (no hardcoded credentials)
- `implementing-observability` - Security monitoring and alerting

## Learn More

- [Full Master Plan](https://github.com/ancoleman/ai-design-components/blob/main/skills/security-hardening/init.md)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
