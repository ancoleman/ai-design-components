# Zero Trust Architecture Reference

## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [Reference Architecture](#reference-architecture)
4. [Implementation Roadmap](#implementation-roadmap)
5. [Technology Components](#technology-components)
6. [Common Patterns](#common-patterns)

## Overview

Zero Trust Architecture (ZTA) implements the principle "never trust, always verify" where every access request is authenticated, authorized, and continuously validated regardless of network location.

**Key Shift:** Traditional security assumes trust inside the network perimeter. Zero Trust assumes breach and verifies explicitly at every access request.

**Primary Standard:** NIST Special Publication 800-207 - Zero Trust Architecture

## Core Principles

### 1. Never Trust, Always Verify

**Traditional Model:**
- Trust based on network location (inside corporate network = trusted)
- VPN grants broad network access

**Zero Trust Model:**
- No implicit trust based on location
- Every access request authenticated and authorized
- Continuous verification throughout session

**Implementation:**
- Authenticate users with MFA at every access request
- Validate device posture before granting access
- Re-authenticate periodically during session
- Monitor session for anomalies

---

### 2. Assume Breach

**Design Philosophy:**
- Assume attackers are already inside the network
- Limit blast radius of any compromise
- Detect and contain breaches quickly

**Implementation:**
- Micro-segmentation: Isolate workloads to prevent lateral movement
- Least privilege: Minimize permissions granted
- Continuous monitoring: Detect anomalous behavior
- Automated response: Contain threats immediately

---

### 3. Explicit Verification

Verify multiple signals before granting access:

**User Identity:**
- Multi-factor authentication (MFA)
- Biometric verification
- Risk-based authentication

**Device Health:**
- Operating system version and patch level
- Endpoint protection status (EDR running, up-to-date)
- Encryption status (disk encryption enabled)
- Compliance with security policies

**Application Integrity:**
- Code signing verification
- Runtime integrity checks
- Vulnerability status

**Context:**
- Location (geolocation, IP address)
- Time of access (business hours vs. unusual times)
- Behavior (normal vs. anomalous patterns)
- Threat intelligence (known malicious IPs, IOCs)

---

### 4. Least Privilege Access

Grant minimum permissions required to complete tasks.

**Just-in-Time (JIT) Access:**
- Elevate privileges only when needed
- Time-bound access (e.g., 4 hours)
- Automated de-provisioning after time expires

**Just-Enough-Access (JEA):**
- Minimal permissions for specific tasks
- No standing admin privileges
- Role-based or attribute-based access control

**Access Recertification:**
- Periodic review of user permissions
- Automated removal of unused permissions
- Manager attestation for critical access

---

### 5. Micro-Segmentation

Divide network into small, isolated zones with granular access controls.

**Traditional Segmentation:**
- Coarse-grained: DMZ, internal network, database tier
- Network-based: VLANs, subnets

**Micro-Segmentation:**
- Fine-grained: Per-application, per-workload isolation
- Identity-based: Access based on user/service identity, not network location
- Dynamic: Policies follow workloads (cloud-native, containers)

**Technologies:**
- Zero Trust Network Access (ZTNA)
- Service mesh (Istio, Linkerd)
- Cloud security groups with identity-based rules
- Software-defined perimeter (SDP)

---

## Reference Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    POLICY DECISION POINT                         │
│                  (Policy Engine + Policy Administrator)          │
│                                                                  │
│  Input: User ID, Device Health, Resource, Context               │
│  Output: ALLOW / DENY access decision                           │
└──────────────────────┬───────────────────────────────────────────┘
                       │ Policy Decision
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────▼────┐   ┌────▼────┐   ┌───▼────┐
    │ Identity│   │ Device  │   │Context │
    │ Provider│   │ Posture │   │ & Risk │
    │ (IdP)   │   │ Service │   │ Engine │
    │         │   │         │   │        │
    │ - Users │   │ - OS    │   │ - Geo  │
    │ - MFA   │   │ - EDR   │   │ - Time │
    │ - SSO   │   │ - Patch │   │ - UEBA │
    └─────────┘   └─────────┘   └────────┘
         │             │             │
         └─────────────┼─────────────┘
                       │ Trust Signals
         ┌─────────────▼─────────────┐
         │  POLICY ENFORCEMENT POINT │
         │    (PEP - Gateways)       │
         │                           │
         │  - ZTNA Gateway           │
         │  - API Gateway            │
         │  - Reverse Proxy          │
         └─────────────┬─────────────┘
                       │ Enforced Access
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼───┐         ┌────▼────┐        ┌───▼────┐
│ User  │         │  App    │        │  Data  │
│Access │         │ Access  │        │ Access │
│(SaaS, │         │ (APIs,  │        │ (DBs,  │
│ Apps) │         │ Services)│        │ S3)    │
└───┬───┘         └────┬────┘        └───┬────┘
    │                  │                 │
┌───▼────────┐    ┌────▼─────────┐  ┌───▼─────────┐
│  End Users │    │ Applications │  │  Data Stores│
│  (Humans)  │    │ (Workloads)  │  │  (Storage)  │
└────────────┘    └──────────────┘  └─────────────┘
```

### Architecture Components

**1. Policy Decision Point (PDP):**
- **Policy Engine:** Makes access decisions (allow/deny) based on policies and trust signals
- **Policy Administrator:** Establishes/shuts down communication paths between subjects and resources

**2. Trust Signal Sources:**
- **Identity Provider (IdP):** Azure AD, Okta, Auth0, Ping Identity
  - User/service identity verification
  - MFA enforcement
  - SSO integration
- **Device Posture Service:** Microsoft Intune, Jamf, VMware Workspace ONE
  - Device inventory and health checks
  - Compliance verification
  - Integration with MDM/UEM platforms
- **Context & Risk Engine:** Microsoft Sentinel, Splunk, UEBA platforms
  - Behavioral analytics
  - Geolocation and time-based risk
  - Threat intelligence integration
  - Adaptive risk scoring

**3. Policy Enforcement Point (PEP):**
- **ZTNA Gateways:** Zscaler Private Access, Palo Alto Prisma Access, Cloudflare Access
  - Enforce policy decisions
  - Terminate connections if trust changes
  - No direct network access granted
- **API Gateways:** Kong, Apigee, AWS API Gateway
  - Enforce API-level policies
  - Rate limiting and throttling
  - JWT validation
- **Reverse Proxies:** NGINX, Envoy, Traefik
  - Application-level access control
  - TLS termination
  - Request filtering

---

## Implementation Roadmap

### Phase 1: Foundation (Months 1-3)

**Objective:** Establish identity and visibility foundation

**Tasks:**
1. **Asset Inventory:**
   - Inventory all users (employees, contractors, partners)
   - Inventory all devices (workstations, mobile, servers, IoT)
   - Inventory all applications (SaaS, on-premises, cloud)
   - Inventory all data stores and classification

2. **Identity Provider Deployment:**
   - Deploy centralized IdP (Azure AD, Okta)
   - Implement SSO for all applications
   - Enforce MFA for all users (prioritize privileged accounts)
   - Integrate on-premises AD with cloud IdP (hybrid identity)

3. **Device Management:**
   - Deploy MDM/UEM platform (Intune, Jamf, Workspace ONE)
   - Enroll all devices
   - Establish device compliance policies (encryption, patch level, EDR)
   - Enable device posture checks

4. **Visibility:**
   - Deploy SIEM for centralized logging
   - Enable cloud audit logs (CloudTrail, Azure Monitor, GCP Cloud Logging)
   - Establish baseline network traffic patterns
   - Map data flows between applications

**Success Metrics:**
- 100% user MFA enrollment
- 95%+ device enrollment in MDM
- Centralized logging operational
- Asset inventory complete

---

### Phase 2: Access Controls (Months 4-6)

**Objective:** Implement least privilege access and strong authentication

**Tasks:**
1. **Least Privilege Access:**
   - Review and document all user roles and permissions
   - Implement RBAC (role-based access control)
   - Remove excessive permissions (principle of least privilege)
   - Document and approve all privileged access

2. **Privileged Access Management (PAM):**
   - Deploy PAM solution (CyberArk, BeyondTrust, HashiCorp Vault)
   - Implement JIT (just-in-time) access for admins
   - Remove standing privileged credentials
   - Enable session recording for all privileged access

3. **Conditional Access Policies:**
   - Implement risk-based authentication
   - Require MFA for high-risk scenarios (new device, unusual location)
   - Block access from known malicious IPs
   - Enforce device compliance before granting access

4. **Identity Governance:**
   - Establish user lifecycle processes (joiner/mover/leaver)
   - Implement access certification (quarterly reviews)
   - Automate access revocation on termination
   - Segregation of duties (SoD) enforcement

**Success Metrics:**
- 0 standing admin credentials
- 100% privileged access via JIT
- Conditional access policies active
- Access certification process operational

---

### Phase 3: Micro-Segmentation (Months 7-9)

**Objective:** Limit lateral movement through network segmentation

**Tasks:**
1. **Application Dependency Mapping:**
   - Map all application dependencies and data flows
   - Document north-south traffic (user → application)
   - Document east-west traffic (application → application)
   - Identify critical assets requiring isolation

2. **Design Segmentation Zones:**
   - Define micro-segmentation zones (per-application, per-tier)
   - Create security policies for each zone
   - Plan migration sequence (critical apps first)

3. **ZTNA Deployment:**
   - Deploy ZTNA solution for remote access (replace VPN)
   - Configure application connectors/gateways
   - Migrate users from VPN to ZTNA (phased rollout)
   - Decommission VPN infrastructure

4. **Service Mesh (Cloud-Native):**
   - Deploy service mesh (Istio, Linkerd) for Kubernetes
   - Implement mutual TLS (mTLS) between services
   - Define service-to-service authorization policies
   - Monitor east-west traffic

5. **Network Policy Enforcement:**
   - Implement network policies (Kubernetes Network Policies, security groups)
   - Default deny all traffic, allow explicitly
   - Log all blocked traffic for tuning

**Success Metrics:**
- ZTNA replaces VPN for remote access
- Critical applications micro-segmented
- East-west traffic controlled by policies
- Lateral movement significantly reduced

---

### Phase 4: Monitoring & Automation (Months 10-12)

**Objective:** Continuous verification and automated response

**Tasks:**
1. **Behavioral Analytics (UEBA):**
   - Deploy UEBA platform (Microsoft Sentinel, Splunk)
   - Establish baseline behavior for users and entities
   - Configure anomaly detection rules
   - Integrate with SIEM for correlation

2. **Continuous Compliance Monitoring:**
   - Deploy CSPM for cloud security posture (Wiz, Orca, Prisma Cloud)
   - Monitor configuration drift from security baselines
   - Automate remediation of common misconfigurations
   - Track compliance against frameworks (CIS, NIST)

3. **Automated Incident Response (SOAR):**
   - Deploy SOAR platform (Splunk SOAR, Cortex XSOAR)
   - Create playbooks for common incidents:
     - Compromised credential → Revoke tokens, force re-auth
     - Malware detection → Isolate endpoint, block IOCs
     - Unusual data access → Alert SOC, increase monitoring
   - Test and refine playbooks

4. **Continuous Verification:**
   - Implement continuous device posture checks
   - Re-authenticate users periodically during long sessions
   - Adjust access based on real-time risk scores
   - Terminate sessions on trust degradation

**Success Metrics:**
- UEBA operational with baseline established
- 80%+ incidents automated response
- Mean time to respond (MTTR) reduced by 50%
- Continuous compliance monitoring active

---

## Technology Components

### Identity Providers (IdP)

| Provider | Strengths | Use Case |
|----------|-----------|----------|
| **Azure AD (Entra ID)** | Microsoft ecosystem integration, Conditional Access | Microsoft-centric organizations |
| **Okta** | Broad SaaS integration, strong MFA | Multi-cloud, SaaS-heavy |
| **Auth0** | Developer-friendly, CIAM focus | Customer identity (B2C) |
| **Ping Identity** | Enterprise scale, legacy integration | Large enterprises, hybrid |

**Key Features:**
- SSO (SAML, OAuth 2.0, OpenID Connect)
- MFA (TOTP, push, biometric, FIDO2)
- Conditional access policies
- User lifecycle management
- API access management

---

### Zero Trust Network Access (ZTNA)

| Provider | Approach | Strengths |
|----------|----------|-----------|
| **Zscaler Private Access** | Cloud-native proxy | Global PoPs, scalability |
| **Palo Alto Prisma Access** | SASE (converged ZTNA + CASB + FWaaS) | Comprehensive security |
| **Cloudflare Access** | Cloudflare network integration | Performance, global reach |
| **Perimeter 81** | Simplified deployment | SMB-friendly, easy setup |

**ZTNA vs. VPN:**

| Aspect | VPN | ZTNA |
|--------|-----|------|
| **Access Model** | Network-level (broad access) | Application-level (granular) |
| **Trust Model** | Implicit (inside = trusted) | Explicit (verify every request) |
| **Lateral Movement** | Easy (full network access) | Difficult (app-specific access) |
| **Device Posture** | Rarely checked | Continuously verified |
| **User Experience** | VPN client, latency | Transparent, faster |

---

### Micro-Segmentation Tools

**Cloud-Native:**
- **AWS Security Groups:** Stateful firewall rules for EC2 instances
- **GCP Firewall Rules:** VPC-level network policies
- **Azure Network Security Groups:** Subnet and NIC-level firewalls
- **Kubernetes Network Policies:** Pod-to-pod communication control

**Service Mesh:**
- **Istio:** Full-featured, complex, sidecar-based
- **Linkerd:** Lightweight, simple, sidecar-based
- **Consul Connect:** HashiCorp ecosystem, service registry integration

**Software-Defined Perimeter (SDP):**
- **Appgate SDP:** Enterprise SDP solution
- **Cyxtera AppGate:** Cloud and on-premises SDP
- **Google BeyondCorp:** Google's zero trust implementation

---

### UEBA & Risk Engines

| Platform | Strengths | Integration |
|----------|-----------|-------------|
| **Microsoft Sentinel** | Azure ecosystem, AI-driven | Azure AD, Microsoft 365 |
| **Splunk UEBA** | Advanced ML, customizable | Splunk SIEM |
| **Exabeam** | Automated threat detection | Multi-SIEM integration |
| **Securonix** | Big data analytics | Large-scale environments |

**UEBA Use Cases:**
- Account compromise detection (unusual login patterns)
- Insider threat detection (data exfiltration, privilege abuse)
- Lateral movement detection (unusual network connections)
- Risk scoring for adaptive authentication

---

## Common Patterns

### Pattern 1: ZTNA for Remote Workforce

**Problem:** VPN provides broad network access, enabling lateral movement if compromised.

**Solution:** Replace VPN with ZTNA for application-specific access.

**Implementation:**
1. Deploy ZTNA gateway (Zscaler, Palo Alto, Cloudflare)
2. Configure application connectors for each internal application
3. Define access policies (user roles → specific applications)
4. Enforce device posture checks before access
5. Migrate users from VPN to ZTNA (pilot → full rollout)
6. Decommission VPN

**Benefits:**
- No network-level access granted
- Per-application access control
- Device posture verification
- Improved user experience (no VPN client)

---

### Pattern 2: Zero Trust for Cloud Workloads

**Problem:** Cloud workloads communicate over network, enabling lateral movement.

**Solution:** Implement service mesh with mutual TLS and policy-based authorization.

**Implementation (Kubernetes + Istio):**
1. Deploy Istio service mesh to Kubernetes cluster
2. Enable automatic sidecar injection for all pods
3. Configure mTLS for all service-to-service communication
4. Define authorization policies using Istio AuthorizationPolicy:
   ```yaml
   apiVersion: security.istio.io/v1beta1
   kind: AuthorizationPolicy
   metadata:
     name: frontend-to-backend
   spec:
     selector:
       matchLabels:
         app: backend
     action: ALLOW
     rules:
     - from:
       - source:
           principals: ["cluster.local/ns/default/sa/frontend"]
       to:
       - operation:
           methods: ["GET", "POST"]
   ```
5. Monitor service mesh traffic with Kiali or Grafana

**Benefits:**
- Encrypted service-to-service communication
- Identity-based authorization (service accounts)
- Zero trust between microservices
- Visibility into east-west traffic

---

### Pattern 3: Adaptive Authentication Based on Risk

**Problem:** Static MFA requirements frustrate users in low-risk scenarios, but weak authentication enables breaches.

**Solution:** Adaptive authentication with risk-based MFA requirements.

**Implementation (Azure AD Conditional Access):**
1. Define risk signals:
   - High risk: New device, unusual location, known malicious IP
   - Medium risk: After-hours access, risky sign-in
   - Low risk: Known device, typical location, business hours

2. Configure Conditional Access policies:
   - **High risk:** Require MFA + compliant device + block if very high risk
   - **Medium risk:** Require MFA
   - **Low risk:** Allow access (SSO only)

3. Integrate UEBA for behavioral risk scoring

4. Continuously adjust risk scores based on session behavior

**Benefits:**
- Strong authentication when needed
- Minimal friction for low-risk access
- Dynamic security posture
- Reduced successful attacks

---

### Pattern 4: Just-in-Time (JIT) Privileged Access

**Problem:** Standing admin credentials are high-value targets and increase breach risk.

**Solution:** JIT access with time-bound privilege elevation.

**Implementation (Azure AD Privileged Identity Management):**
1. Remove all standing admin role assignments
2. Configure eligible roles (users can activate when needed)
3. Define activation requirements:
   - MFA required
   - Justification required (ticket number)
   - Approval required for critical roles
   - Time-bound (e.g., 4 hours)

4. Enable session recording for all privileged sessions

5. Alert on all privilege activations

6. Review and audit activation logs regularly

**Benefits:**
- Reduced attack surface (no standing admin creds)
- Audit trail of all privileged access
- Time-limited exposure
- Justification for compliance

---

## Benefits of Zero Trust Architecture

**Security Benefits:**
- **Reduced Attack Surface:** No broad network access, application-specific only
- **Limited Lateral Movement:** Micro-segmentation prevents attackers from spreading
- **Breach Detection:** Continuous monitoring detects anomalies quickly
- **Compliance:** Strong access controls and audit trails for regulatory requirements

**Cost Benefits (IBM 2024 Cost of Data Breach Report):**
- Average savings: $1.76M per breach for organizations with mature Zero Trust
- Reduced breach detection time (27% faster detection)
- Reduced breach containment time (33% faster containment)

**Operational Benefits:**
- **Improved User Experience:** ZTNA eliminates VPN latency and client issues
- **Cloud-Native:** Aligns with cloud and container architectures
- **Automation:** Policy-based access reduces manual administration
- **Visibility:** Comprehensive logging and monitoring across all access

---

## Challenges and Mitigations

### Challenge 1: Complexity of Implementation

**Issue:** Zero Trust requires integrating multiple technologies (IdP, ZTNA, UEBA, SIEM, PAM).

**Mitigation:**
- Phased approach (12-month roadmap, not "big bang")
- Start with identity foundation (Phase 1)
- Use cloud-native solutions where possible (reduce on-premises complexity)
- Consider SASE platforms for converged security (Zscaler, Palo Alto Prisma)

---

### Challenge 2: Legacy System Integration

**Issue:** Legacy applications may not support modern authentication (SAML, OAuth).

**Mitigation:**
- Use reverse proxies with authentication injection (NGINX, Envoy)
- Deploy privileged access gateways for legacy protocols (RDP, SSH)
- Plan modernization or replacement of unsupportable legacy systems
- Segment legacy systems with strict network policies

---

### Challenge 3: User Experience Impact

**Issue:** Frequent authentication and access checks can frustrate users.

**Mitigation:**
- Implement adaptive authentication (MFA only when risk warrants)
- Use SSO to minimize authentication prompts
- Deploy passwordless authentication (FIDO2, biometrics)
- Transparent ZTNA (no VPN client, seamless access)

---

### Challenge 4: Cultural Resistance

**Issue:** Users and IT staff may resist change from traditional VPN/perimeter model.

**Mitigation:**
- Executive sponsorship and communication of security benefits
- Pilot programs with early adopters
- Training and documentation for IT staff and users
- Demonstrate improved user experience (faster access, no VPN)

---

## Summary

Zero Trust Architecture shifts from perimeter-based security to identity-based continuous verification. Implement in phases over 12 months: Foundation (identity, visibility) → Access Controls (least privilege, PAM) → Micro-Segmentation (ZTNA, service mesh) → Monitoring & Automation (UEBA, SOAR).

Key technologies: IdP (Azure AD, Okta), ZTNA (Zscaler, Palo Alto, Cloudflare), Service Mesh (Istio, Linkerd), UEBA (Microsoft Sentinel, Splunk), PAM (CyberArk, HashiCorp Vault).

Primary benefit: Reduced breach impact through limited lateral movement, continuous verification, and rapid detection.
