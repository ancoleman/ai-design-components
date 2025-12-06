---
sidebar_position: 1
title: Security Architecture
description: Design comprehensive security architectures using defense-in-depth, zero trust, and threat modeling
tags: [security, architecture, zero-trust, threat-modeling, defense-in-depth]
---

# Security Architecture

Design and implement comprehensive security architectures that protect systems, data, and users through layered defense strategies, zero trust principles, and risk-based security controls.

## When to Use

Use security architecture when:
- Designing security for greenfield systems (new applications, cloud migrations)
- Conducting security audits or risk assessments of existing systems
- Implementing zero trust architecture across enterprise environments
- Establishing security governance programs and compliance frameworks
- Threat modeling applications, APIs, or microservices architectures
- Selecting and mapping security controls to regulatory requirements (SOC 2, HIPAA, PCI DSS)
- Designing cloud security architectures (AWS, GCP, Azure multi-account strategies)
- Addressing supply chain security (SLSA framework, SBOM implementation)

## Key Features

**Defense in Depth (9 Layers):**
- Physical security, network perimeter, network segmentation, endpoint protection
- Application layer security, data encryption, identity and access management
- Behavioral analytics, security operations (SIEM, SOAR)

**Zero Trust Architecture:**
- Continuous verification: Never trust, always verify
- Least privilege access with just-in-time permissions
- Assume breach: Design for compromise, limit blast radius
- Micro-segmentation: Divide networks into small isolated zones

**Threat Modeling Methodologies:**
- STRIDE: Threat identification for development teams
- PASTA: Risk-centric analysis for enterprise risk management
- DREAD: Risk scoring for prioritizing existing threats
- Attack Trees: Visual threat analysis for security architecture reviews

**Control Frameworks:**
- NIST Cybersecurity Framework 2.0: 6 core functions (GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER)
- CIS Critical Security Controls v8: 18 controls in 3 implementation groups
- OWASP Top 10 Risk Mitigation: Map application security risks to architectural controls

## Quick Start

```yaml
# Zero Trust Architecture Components

Policy Engine: Centralized authorization decision point
Identity Provider (IdP): User/machine identity verification (Azure AD, Okta)
Device Posture Service: Device health checks (MDM, EDR integration)
Context/Risk Engine: Behavioral analytics, location, time, threat intelligence
Policy Enforcement Points: ZTNA gateways, API gateways enforcing decisions
```

**STRIDE Threat Modeling Process:**

1. Model the system using data flow diagrams (DFDs)
2. Identify threats by applying STRIDE to each component/data flow
   - **S**poofing: Impersonation attacks → Mitigation: MFA, certificate validation
   - **T**ampering: Data modification → Mitigation: Encryption, digital signatures
   - **R**epudiation: Denying actions → Mitigation: Audit logs, non-repudiation
   - **I**nformation Disclosure: Data exposure → Mitigation: Encryption, access controls, DLP
   - **D**enial of Service: Unavailability → Mitigation: Rate limiting, DDoS protection
   - **E**levation of Privilege: Gaining higher privileges → Mitigation: Least privilege, patching
3. Document threats with STRIDE categories
4. Prioritize threats using DREAD scoring or business impact
5. Design mitigation controls

**Cloud Security Architecture (AWS Example):**

```hcl
# Multi-Account Security Strategy
# Use AWS Organizations with:
# - Security OU (Security Account, Logging Account, Audit Account)
# - Workload OUs (Production, Non-Production)
# - Service Control Policies (SCPs) for guardrails

# Key AWS Security Services:
# IAM: AWS IAM, IAM Identity Center (SSO), Cognito
# Detection: GuardDuty, Security Hub, Detective
# Network: AWS WAF, Shield (DDoS), Network Firewall
# Data: KMS, Secrets Manager, Macie
# Compute: Systems Manager, Inspector
```

## Related Skills

- [Security Hardening](./security-hardening.md) - Implement technical security controls from architecture design
- [Implementing Compliance](./implementing-compliance.md) - Map security architecture to compliance frameworks
- [Managing Vulnerabilities](./managing-vulnerabilities.md) - Integrate vulnerability scanning into security architecture
- [Implementing TLS](./implementing-tls.md) - Implement data encryption in transit
- [Configuring Firewalls](./configuring-firewalls.md) - Implement network perimeter layer
- [SIEM Logging](./siem-logging.md) - Implement security monitoring architecture

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/architecting-security)
- [Master Plan](../../master-plans/security/architecting-security.md)
