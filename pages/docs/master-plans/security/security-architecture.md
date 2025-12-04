---
sidebar_position: 1
title: Security Architecture
description: Master plan for security architecture including defense in depth, zero trust, threat modeling, and security controls
tags: [master-plan, security, architecture, zero-trust, threat-modeling]
---

# Security Architecture

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Security architecture provides the foundational framework for protecting systems and data. This skill covers defense in depth strategies, zero trust architecture, threat modeling methodologies, and security controls mapping across infrastructure layers.

## Scope

This skill teaches:

- **Defense in Depth** - Multi-layered security strategy across network, host, application layers
- **Zero Trust Architecture** - Never trust, always verify principles
- **Threat Modeling** - STRIDE, DREAD, attack trees for risk assessment
- **Security Controls** - Preventive, detective, corrective controls mapping
- **Identity and Access Management** - Authentication, authorization, least privilege
- **Secure Development** - Security by design, DevSecOps integration
- **Incident Response** - Preparation, detection, containment, recovery

## Key Components

### Defense in Depth Layers

**Network Security:**
- Firewalls, security groups, network segmentation
- Intrusion detection/prevention systems (IDS/IPS)
- DDoS protection, WAF (Web Application Firewall)

**Host Security:**
- OS hardening (CIS benchmarks, security updates)
- Endpoint protection (antivirus, EDR)
- Host-based firewalls

**Application Security:**
- Input validation, output encoding
- Authentication and authorization
- Secure coding practices (OWASP Top 10)

**Data Security:**
- Encryption at rest and in transit
- Data loss prevention (DLP)
- Backup and disaster recovery

### Zero Trust Principles

1. **Verify Explicitly** - Always authenticate and authorize based on all available data
2. **Least Privilege Access** - Limit user access with Just-In-Time and Just-Enough-Access
3. **Assume Breach** - Minimize blast radius, segment access, verify end-to-end encryption

**Implementation:**
- Identity-based access (not network-based)
- Micro-segmentation (service-to-service isolation)
- Continuous monitoring and validation
- Strong authentication (MFA, biometrics)

### Threat Modeling (STRIDE)

| Threat | Description | Mitigation |
|--------|-------------|------------|
| **Spoofing** | Identity impersonation | Strong authentication, certificates |
| **Tampering** | Data modification | Integrity checks, signing |
| **Repudiation** | Deny actions | Audit logging, non-repudiation |
| **Information Disclosure** | Data exposure | Encryption, access controls |
| **Denial of Service** | Service unavailability | Rate limiting, redundancy |
| **Elevation of Privilege** | Unauthorized access | Least privilege, input validation |

### Security Controls Mapping

**Preventive Controls:**
- Firewalls, encryption, access controls
- Input validation, secure configurations

**Detective Controls:**
- Logging, monitoring, alerting
- Intrusion detection, vulnerability scanning

**Corrective Controls:**
- Incident response, patch management
- Backup and recovery procedures

## Decision Framework

**Which Security Architecture Pattern?**

```
Perimeter-based (legacy)?
  NO → Zero Trust Architecture
        → Identity-based access
        → Micro-segmentation
        → Continuous verification

Cloud-native application?
  YES → Zero Trust + Defense in Depth
        → Service mesh (mTLS)
        → IAM policies (least privilege)
        → Network policies (K8s)

Multi-cloud deployment?
  YES → Unified IAM (Okta, Azure AD)
        → Cross-cloud security policies
        → Centralized logging (SIEM)
```

**Threat Modeling Approach:**

```
New application design?
  YES → STRIDE threat modeling
        → Identify threats per component
        → Design mitigations

Existing system risk assessment?
  YES → Attack tree analysis
        → Identify attack paths
        → Prioritize by impact (DREAD)

Compliance required (PCI-DSS, HIPAA)?
  YES → Control-based approach
        → Map to compliance requirements
        → Document evidence
```

## Tool Recommendations

### Security Architecture

**Threat Modeling:**
- Microsoft Threat Modeling Tool
- OWASP Threat Dragon
- ThreatSpec (threat modeling as code)

**IAM/Access Management:**
- Okta, Auth0 (identity providers)
- AWS IAM, Azure AD, GCP IAM (cloud-native)
- HashiCorp Boundary (access proxy)

**Network Security:**
- AWS Security Groups, Azure NSGs, GCP Firewall Rules
- Palo Alto Networks, Fortinet (enterprise firewalls)
- Cloudflare, AWS WAF (web application firewalls)

### Monitoring and Detection

**SIEM:**
- Splunk, Elastic Security, Azure Sentinel
- Chronicle Security (Google)

**Vulnerability Scanning:**
- Trivy, Grype, Snyk (container/dependency scanning)
- Nessus, OpenVAS (network scanning)

## Integration Points

**With Other Skills:**
- `compliance-frameworks` - Map security controls to compliance requirements
- `vulnerability-management` - Identify and remediate security weaknesses
- `siem-logging` - Aggregate security logs for detection
- `implementing-tls` - Encrypt data in transit
- `configuring-firewalls` - Implement network security controls
- `network-architecture` - Zero trust networking patterns

**Workflow Example:**
```
Threat Model → Security Controls → Implementation → Monitoring
      │              │                  │              │
      ▼              ▼                  ▼              ▼
   STRIDE      Firewalls +        Deploy via      SIEM alerts
   analysis    encryption +       IaC/config      + incident
               IAM policies       management      response
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/security-architecture/init.md)
- Related: `compliance-frameworks`, `vulnerability-management`, `siem-logging`
