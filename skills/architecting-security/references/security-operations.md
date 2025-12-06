# Security Operations Reference

## SIEM (Security Information & Event Management)

**Purpose:** Centralize log aggregation, correlation, and alerting

**Leading Platforms:**
- Splunk Enterprise Security
- Elastic Security
- Microsoft Sentinel
- Google Chronicle

**Architecture:**
1. Log Collection: Ingest from all sources
2. Normalization: Standardize log formats
3. Correlation: Apply rules to detect patterns
4. Alerting: Notify SOC team
5. Investigation: Search and visualization

## SOAR (Security Orchestration, Automation & Response)

**Purpose:** Automate incident response workflows

**Capabilities:**
- Playbooks: Automated response workflows
- Orchestration: Integrate security tools
- Case Management: Track incidents

**Leading Platforms:**
- Splunk SOAR
- Palo Alto Cortex XSOAR
- IBM Resilient

## Detection Strategies

### UEBA (User & Entity Behavior Analytics)

**Purpose:** ML-based anomaly detection

**Use Cases:**
- Account compromise detection
- Insider threat detection
- Data exfiltration detection
- Lateral movement detection

### Threat Intelligence

**Sources:**
- MISP (Malware Information Sharing Platform)
- ThreatConnect
- ISACs (Information Sharing and Analysis Centers)

**Integration:**
- Enrich SIEM alerts with threat context
- Block known malicious IPs/domains
- Proactive threat hunting
