# SOC 2 Trust Services Criteria


## Table of Contents

- [Overview](#overview)
- [Trust Services Criteria](#trust-services-criteria)
  - [Common Criteria (CC) - All SOC 2 Reports](#common-criteria-cc-all-soc-2-reports)
  - [Additional Trust Services Criteria (Optional)](#additional-trust-services-criteria-optional)
- [Evidence Collection for SOC 2](#evidence-collection-for-soc-2)
  - [Monthly Testing Requirements (2025)](#monthly-testing-requirements-2025)
  - [AI Governance Controls (2025)](#ai-governance-controls-2025)
- [SOC 2 Implementation Timeline](#soc-2-implementation-timeline)
- [Common SOC 2 Audit Findings](#common-soc-2-audit-findings)
- [Control Implementation Priority](#control-implementation-priority)
- [Tool Recommendations](#tool-recommendations)

## Overview

SOC 2 is an auditing procedure that ensures service providers securely manage data to protect the interests and privacy of their clients. Reports are issued by certified public accountants (CPAs) following an audit.

**Report Types:**
- **Type I:** Point-in-time assessment of control design
- **Type II:** 6-12 month assessment of control effectiveness (required for enterprise sales)

**2025 Updates:**
- Monthly control testing (previously annual) for Type II
- AI governance controls for ML systems handling customer data
- 72-hour breach notification requirement
- Enhanced third-party risk management

## Trust Services Criteria

### Common Criteria (CC) - All SOC 2 Reports

#### CC1: Control Environment

**CC1.1** - Organization demonstrates commitment to integrity and ethical values
**CC1.2** - Board of directors demonstrates independence and oversight
**CC1.3** - Management establishes structures, reporting lines, authorities, and responsibilities
**CC1.4** - Organization demonstrates commitment to attract, develop, and retain competent individuals
**CC1.5** - Organization holds individuals accountable for internal control responsibilities

**Implementation:**
- Documented code of conduct
- Board charter and meeting minutes
- Organizational chart with reporting structure
- Security awareness training program
- Performance reviews including security responsibilities

#### CC2: Communication and Information

**CC2.1** - Organization obtains or generates relevant, quality information
**CC2.2** - Organization internally communicates information necessary to support functioning of internal control
**CC2.3** - Organization communicates with external parties regarding matters affecting internal control

**Implementation:**
- Security policies and procedures documented
- Internal security newsletters and announcements
- Customer security documentation and incident communication
- Vendor management communications

#### CC3: Risk Assessment

**CC3.1** - Organization specifies objectives with sufficient clarity
**CC3.2** - Organization identifies risks to achievement of objectives
**CC3.3** - Organization considers potential for fraud in risk assessment
**CC3.4** - Organization identifies and assesses changes that could significantly impact internal control

**Implementation:**
- Annual risk assessments
- Risk register with mitigation plans
- Change management process
- Fraud risk assessment procedures

#### CC4: Monitoring Activities

**CC4.1** - Organization selects, develops, and performs ongoing/separate evaluations
**CC4.2** - Organization evaluates and communicates internal control deficiencies

**Implementation:**
- Continuous security monitoring
- Annual internal audits
- Penetration testing (annual minimum)
- Executive security reporting

#### CC5: Control Activities

**CC5.1** - Organization selects and develops control activities that contribute to mitigation of risks
**CC5.2** - Organization selects and develops general control activities over technology
**CC5.3** - Organization deploys control activities through policies and procedures

**Implementation:**
- Security control framework (mapped to TSC)
- IT general controls (change management, access controls)
- Standard operating procedures

#### CC6: Logical and Physical Access Controls

**CC6.1** - Organization implements logical access security software, infrastructure, and architectures
- Multi-factor authentication for privileged access
- Role-based access control (RBAC)
- Encryption at rest (AES-256) and in transit (TLS 1.3)
- Network segmentation and firewalls

**CC6.2** - Organization restricts logical access (least privilege)
- Access provisioning and deprovisioning procedures
- Quarterly access reviews
- Separation of duties enforcement

**CC6.3** - Organization manages identification and authentication
- Password complexity requirements (12+ characters)
- Account lockout policies
- Session timeout enforcement

**CC6.4** - Organization restricts access to programs and data
- Application-level access controls
- Data classification and handling
- Secure software development lifecycle

**CC6.5** - Organization terminates access when appropriate
- Immediate access revocation upon termination
- Regular review of inactive accounts
- Contractor access expiration

**CC6.6** - Organization implements security measures to protect against threats
- Intrusion detection/prevention systems
- DDoS protection
- Web application firewall (WAF)

**CC6.7** - Organization restricts transmission, movement, and removal of information
- Data loss prevention (DLP)
- Encrypted backups
- Secure data disposal procedures

**CC6.8** - Organization implements controls to prevent or detect malicious software
- Endpoint detection and response (EDR)
- Anti-malware on all systems
- Email security gateway

#### CC7: System Operations

**CC7.1** - Organization ensures systems are current and can continue operating
- Patch management with defined SLAs
- Vulnerability scanning (weekly minimum)
- Configuration management

**CC7.2** - Organization monitors system components and operation
- Centralized logging and SIEM
- Security information and event monitoring
- Log retention (7 years minimum)

**CC7.3** - Organization evaluates security events and responds
- Incident response plan
- Security operations center (SOC) or equivalent
- Threat intelligence integration

**CC7.4** - Organization identifies, develops, and implements activities to recover from disruptions
- Disaster recovery plan
- Regular backup procedures (automated daily)
- Annual DR testing

**CC7.5** - Organization deploys detection and monitoring procedures to identify anomalies
- Anomaly detection systems
- User behavior analytics
- Automated alerting for suspicious activity

#### CC8: Change Management

**CC8.1** - Organization authorizes, designs, develops, tests, approves, and implements changes
- Change advisory board (CAB)
- Code review requirements
- Testing in non-production environments
- Rollback procedures

#### CC9: Risk Mitigation

**CC9.1** - Organization establishes requirements for vendor and business partner agreements
- Vendor risk assessment process
- Security requirements in vendor contracts
- Right-to-audit clauses

**CC9.2** - Organization assesses vendor and business partner services
- Annual vendor reviews
- SOC 2 report collection (≤90 days old)
- Vendor incident notification requirements

### Additional Trust Services Criteria (Optional)

#### Availability

Measures system uptime and accessibility.

**Implementation:**
- SLA definitions (e.g., 99.99% uptime)
- Redundancy and failover mechanisms
- Performance monitoring
- Capacity planning

#### Processing Integrity

Ensures system processing is complete, valid, accurate, timely, and authorized.

**Implementation:**
- Input validation
- Error handling and logging
- Data reconciliation procedures
- Processing controls and audits

#### Confidentiality

Protects confidential information as agreed with clients.

**Implementation:**
- Data classification scheme
- Confidentiality agreements (NDAs)
- Confidential data encryption
- Access controls specific to confidential data

#### Privacy

Addresses collection, use, retention, disclosure, and disposal of personal information.

**Implementation:**
- Privacy policy
- Consent management
- Data subject rights procedures (access, deletion)
- Privacy impact assessments

## Evidence Collection for SOC 2

### Monthly Testing Requirements (2025)

All controls must be tested monthly for Type II reports:

**Automated Evidence:**
- Access logs (authentication, authorization)
- Encryption status (AWS Config, Cloud Custodian)
- Vulnerability scan results
- Backup success/failure logs
- Change management tickets
- Security monitoring alerts

**Manual Evidence:**
- Access review documentation (quarterly)
- Board meeting minutes (quarterly minimum)
- Security awareness training completion (annual)
- Vendor SOC 2 reports (annual)
- Penetration test reports (annual)
- Business continuity test results (annual)

### AI Governance Controls (2025)

New requirements for systems using AI/ML on customer data:

**Required Controls:**
- AI model logging and monitoring
- Algorithmic transparency documentation
- Bias mitigation procedures
- Model versioning and rollback capabilities
- AI-specific risk assessments
- Third-party AI service vendor assessments

**Evidence:**
- Model training logs
- Bias testing results
- Model performance monitoring
- AI incident response procedures
- AI ethics policy

## SOC 2 Implementation Timeline

**Phase 1: Gap Assessment (Month 1-2)**
- Compare current controls against TSC requirements
- Document existing controls
- Identify gaps and remediation plan

**Phase 2: Control Implementation (Month 3-6)**
- Implement missing controls
- Document policies and procedures
- Configure automated evidence collection

**Phase 3: Observation Period (Month 7-12)**
- Collect evidence continuously
- Monthly control testing
- Address any control failures
- Prepare for audit

**Phase 4: Audit (Month 13)**
- CPA audit firm engagement
- Provide evidence package
- Remediate audit findings
- Receive SOC 2 Type II report

## Common SOC 2 Audit Findings

**Most Frequent Deficiencies:**

1. **Access Reviews Not Performed:** Quarterly access reviews not completed or documented
   - **Remediation:** Automate access review reminders, track completion

2. **Insufficient Logging:** Not logging all required events or inadequate retention
   - **Remediation:** Implement comprehensive audit logging, 7-year retention

3. **MFA Gaps:** MFA not enforced for all privileged access
   - **Remediation:** Implement MFA enforcement policies (IAM, conditional access)

4. **Vendor SOC 2 Reports Expired:** Vendor reports older than 90 days
   - **Remediation:** Quarterly vendor report collection process

5. **Incomplete Change Documentation:** Changes deployed without proper approval/testing
   - **Remediation:** Enforce change management workflow in ticketing system

6. **Backup Testing Not Performed:** Backup success logged but restoration not tested
   - **Remediation:** Quarterly backup restoration tests

7. **Security Training Incomplete:** Not all employees completed training
   - **Remediation:** Mandatory training with tracking, escalation for non-completion

8. **Patch Management SLA Violations:** Critical patches not deployed within 30 days
   - **Remediation:** Automated patch deployment, exception tracking

## Control Implementation Priority

**Week 1-4: Foundation**
1. Encryption (CC6.1, CC6.7)
2. MFA enforcement (CC6.1)
3. Centralized logging (CC7.2)

**Week 5-8: Access Controls**
4. RBAC implementation (CC6.2)
5. Access review process (CC6.2)
6. Password policies (CC6.3)

**Week 9-12: Monitoring & Response**
7. Security monitoring/SIEM (CC7.2, CC7.3)
8. Incident response plan (CC7.3)
9. Vulnerability management (CC7.1)

**Month 4-6: Governance & Documentation**
10. Policy documentation (CC1, CC2)
11. Security awareness training (CC1.4)
12. Risk assessment process (CC3)
13. Vendor management (CC9)

**Month 7-12: Observation Period**
14. Monthly testing and evidence collection
15. Continuous monitoring and improvement
16. Audit preparation

## Tool Recommendations

**Automated Compliance Platforms:**
- Drata
- Vanta
- Secureframe
- TrustCloud

**Manual Alternative:**
- AWS Config + Lambda for evidence collection
- Spreadsheet-based control tracking
- Manual evidence package preparation

**Investment:**
- Automated platform: $20K-40K annually
- Manual approach: Significant staff time (200+ hours annually)
- Audit fees: $15K-50K depending on company size

This guide provides the framework for SOC 2 compliance. Consult with qualified auditors for organization-specific requirements.
