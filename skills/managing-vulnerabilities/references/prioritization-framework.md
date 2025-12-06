# Vulnerability Prioritization Framework

Risk-based vulnerability prioritization using CVSS, EPSS, KEV, and business context.

## Table of Contents

1. [Overview](#overview)
2. [CVSS Scoring](#cvss-scoring)
3. [EPSS Integration](#epss-integration)
4. [KEV Catalog](#kev-catalog)
5. [Risk-Based Formula](#risk-based-formula)
6. [SLA Tiers](#sla-tiers)
7. [Automation Scripts](#automation-scripts)
8. [Examples](#examples)

---

## Overview

### The Problem with CVSS Alone

**CVSS Base Score limitations:**
- Treats all Critical CVEs equally (not all are exploited)
- Static score, doesn't reflect threat landscape
- No consideration of actual risk to your environment
- Results in "patch everything" approach (unsustainable)

### Modern Risk-Based Approach

Combine multiple data sources:

| Metric | Purpose | Source |
|--------|---------|--------|
| **CVSS** | Vulnerability severity | NVD, vendor advisories |
| **EPSS** | Exploitation probability | FIRST.org API |
| **KEV** | Actively exploited | CISA KEV Catalog |
| **Asset Criticality** | Business impact | Internal CMDB |
| **Exposure** | Attack surface | Network topology |

---

## CVSS Scoring

### CVSS v3.1 Overview

**Base Score Components:**

**Attack Vector (AV):**
- Network (N): Remotely exploitable
- Adjacent (A): Local network required
- Local (L): Local access required
- Physical (P): Physical access required

**Attack Complexity (AC):**
- Low (L): No special conditions
- High (H): Specific conditions required

**Privileges Required (PR):**
- None (N): Unauthenticated
- Low (L): Basic user privileges
- High (H): Administrator privileges

**User Interaction (UI):**
- None (N): No interaction needed
- Required (R): User action required

**Impact (CIA):**
- High (H): Total loss
- Low (L): Limited loss
- None (N): No impact

### Severity Ranges

| Range | Severity | Typical Response |
|-------|----------|------------------|
| 9.0 - 10.0 | Critical | Immediate action |
| 7.0 - 8.9 | High | Urgent, prioritize |
| 4.0 - 6.9 | Medium | Normal planning |
| 0.1 - 3.9 | Low | Backlog |
| 0.0 | None | Informational |

### Fetching CVSS Scores

```bash
# From NVD API
curl "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-44228" | \
  jq '.vulnerabilities[0].cve.metrics.cvssMetricV31[0].cvssData.baseScore'

# From Trivy scan
trivy image myapp:latest --format json | \
  jq '.Results[].Vulnerabilities[] | {cve: .VulnerabilityID, cvss: .CVSS.nvd.V3Score}'
```

---

## EPSS Integration

### What is EPSS?

Exploit Prediction Scoring System (EPSS) predicts the probability a vulnerability will be exploited within 30 days.

**Based On:**
- Exploit availability (PoC, Metasploit modules)
- Public discussions and mentions
- Vulnerability characteristics
- Historical exploitation patterns

### EPSS Score Interpretation

| Score Range | Probability | Action |
|-------------|-------------|--------|
| 0.9 - 1.0 | Very High (>90%) | Immediate priority |
| 0.5 - 0.9 | High (50-90%) | High priority |
| 0.1 - 0.5 | Moderate (10-50%) | Monitor closely |
| 0.0 - 0.1 | Low (<10%) | Normal priority |

### Using EPSS API

**Fetch EPSS Score:**

```bash
# Single CVE
curl "https://api.first.org/data/v1/epss?cve=CVE-2021-44228" | jq '.'

# Response:
{
  "status": "OK",
  "data": [{
    "cve": "CVE-2021-44228",
    "epss": "0.97505",
    "percentile": "0.99999"
  }]
}

# Multiple CVEs
curl "https://api.first.org/data/v1/epss?cve=CVE-2021-44228,CVE-2023-12345"

# All CVEs (large download)
curl "https://api.first.org/data/v1/epss" --output epss-all.csv
```

**Python Integration:**

```python
import requests

def get_epss_score(cve_id):
    """Fetch EPSS score for CVE"""
    url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK' and data['data']:
        return float(data['data'][0]['epss'])
    return 0.0

# Example
score = get_epss_score("CVE-2021-44228")
print(f"EPSS Score: {score:.4f} ({score*100:.2f}%)")
# Output: EPSS Score: 0.9751 (97.51%)
```

---

## KEV Catalog

### CISA Known Exploited Vulnerabilities

CVEs actively exploited in the wild. **If in KEV → Immediate action required.**

**KEV Catalog:** https://www.cisa.gov/known-exploited-vulnerabilities-catalog

### Using KEV Catalog

**Download KEV Data:**

```bash
# Download JSON
curl -o kev.json https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json

# Query specific CVE
jq '.vulnerabilities[] | select(.cveID == "CVE-2021-44228")' kev.json
```

**Check if CVE is in KEV:**

```python
import requests

def is_in_kev(cve_id):
    """Check if CVE is in CISA KEV catalog"""
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    response = requests.get(url)
    kev_data = response.json()

    for vuln in kev_data['vulnerabilities']:
        if vuln['cveID'] == cve_id:
            return True, vuln.get('dateAdded'), vuln.get('dueDate')
    return False, None, None

# Example
in_kev, added, due = is_in_kev("CVE-2021-44228")
if in_kev:
    print(f"P0 CRITICAL: In KEV catalog (added {added}, due {due})")
```

**KEV Response Fields:**

```json
{
  "cveID": "CVE-2021-44228",
  "vendorProject": "Apache",
  "product": "Log4j",
  "vulnerabilityName": "Log4j2 Remote Code Execution",
  "dateAdded": "2021-12-10",
  "shortDescription": "Apache Log4j2 ...",
  "requiredAction": "Apply updates per vendor instructions.",
  "dueDate": "2021-12-24"
}
```

---

## Risk-Based Formula

### Weighted Priority Score

```
Priority Score = (CVSS × 0.3) + (EPSS × 100 × 0.3) + (KEV × 50) + (Asset × 0.2) + (Exposure × 0.2)

Where:
- CVSS: Base score (0-10)
- EPSS: Probability (0-1), scaled to 0-100
- KEV: 1 if in KEV catalog, 0 otherwise (multiplied by 50)
- Asset: 1.0 (Critical), 0.7 (High), 0.4 (Medium), 0.1 (Low)
- Exposure: 1.0 (Internet-facing), 0.5 (Internal), 0.1 (Isolated)

Maximum Score: 10×0.3 + 100×0.3 + 50 + 1×0.2 + 1×0.2 = 83.4
```

### Asset Criticality Matrix

| Asset Type | Criticality | Weight | Examples |
|------------|-------------|--------|----------|
| Critical | 1.0 | Highest | Payment systems, PII databases, authentication |
| High | 0.7 | High | User-facing apps, APIs, internal services |
| Medium | 0.4 | Medium | Admin tools, internal dashboards |
| Low | 0.1 | Low | Dev/test environments, demos |

### Exposure Matrix

| Exposure Type | Weight | Examples |
|---------------|--------|----------|
| Internet-facing | 1.0 | Public websites, APIs, CDNs |
| Internal | 0.5 | Corporate network, VPN-only |
| Isolated | 0.1 | Air-gapped, development environments |

---

## SLA Tiers

### Priority Definitions

| Priority | Criteria | SLA | Action |
|----------|----------|-----|--------|
| **P0 - Critical** | KEV + Internet-facing + Critical asset | 24 hours | Emergency patch, all hands |
| **P1 - High** | CVSS ≥ 9.0 OR (CVSS ≥ 7.0 AND EPSS ≥ 0.1) | 7 days | Prioritize in current sprint |
| **P2 - Medium** | CVSS 7.0-8.9 OR EPSS ≥ 0.05 | 30 days | Plan in next sprint |
| **P3 - Low** | CVSS 4.0-6.9, EPSS < 0.05 | 90 days | Backlog, maintenance window |
| **P4 - Info** | CVSS < 4.0 | No SLA | Track, address opportunistically |

### SLA Escalation

```
Day 1-7:   Normal remediation
Day 8-14:  Manager notification
Day 15-21: Director escalation
Day 22+:   Executive escalation, risk acceptance required
```

---

## Automation Scripts

### Python Priority Calculator

```python
import requests

class VulnerabilityPrioritizer:
    def __init__(self):
        self.kev_cache = None

    def get_epss_score(self, cve_id):
        """Fetch EPSS score from API"""
        url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK' and data['data']:
            return float(data['data'][0]['epss'])
        return 0.0

    def is_in_kev(self, cve_id):
        """Check KEV catalog"""
        if not self.kev_cache:
            url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
            response = requests.get(url)
            self.kev_cache = response.json()

        for vuln in self.kev_cache['vulnerabilities']:
            if vuln['cveID'] == cve_id:
                return True
        return False

    def calculate_priority(self, cve_id, cvss_score, asset_criticality, exposure):
        """
        Calculate priority score

        Args:
            cve_id: CVE identifier
            cvss_score: CVSS base score (0-10)
            asset_criticality: 1.0 (Critical), 0.7 (High), 0.4 (Medium), 0.1 (Low)
            exposure: 1.0 (Internet), 0.5 (Internal), 0.1 (Isolated)
        """
        epss_score = self.get_epss_score(cve_id)
        kev_status = 1 if self.is_in_kev(cve_id) else 0

        priority_score = (
            (cvss_score * 0.3) +
            (epss_score * 100 * 0.3) +
            (kev_status * 50) +
            (asset_criticality * 0.2) +
            (exposure * 0.2)
        )

        # Determine priority tier
        if kev_status and exposure >= 0.5 and asset_criticality >= 0.7:
            tier = "P0"
            sla_hours = 24
        elif cvss_score >= 9.0 or (cvss_score >= 7.0 and epss_score >= 0.1):
            tier = "P1"
            sla_hours = 7 * 24
        elif cvss_score >= 7.0 or epss_score >= 0.05:
            tier = "P2"
            sla_hours = 30 * 24
        elif cvss_score >= 4.0:
            tier = "P3"
            sla_hours = 90 * 24
        else:
            tier = "P4"
            sla_hours = None

        return {
            'cve_id': cve_id,
            'cvss': cvss_score,
            'epss': epss_score,
            'kev': kev_status,
            'asset': asset_criticality,
            'exposure': exposure,
            'priority_score': round(priority_score, 2),
            'tier': tier,
            'sla_hours': sla_hours
        }

# Usage
prioritizer = VulnerabilityPrioritizer()

result = prioritizer.calculate_priority(
    cve_id="CVE-2021-44228",
    cvss_score=10.0,
    asset_criticality=1.0,  # Critical
    exposure=1.0  # Internet-facing
)

print(f"{result['tier']}: {result['cve_id']}")
print(f"  Priority Score: {result['priority_score']}")
print(f"  SLA: {result['sla_hours']} hours")
print(f"  CVSS: {result['cvss']}, EPSS: {result['epss']:.4f}, KEV: {bool(result['kev'])}")
```

---

## Examples

### Example 1: Log4Shell (Critical)

```
CVE: CVE-2021-44228 (Log4Shell)
CVSS: 10.0
EPSS: 0.97505 (97.5%)
KEV: Yes (CISA catalog)
Asset: Critical (payment API)
Exposure: Internet-facing

Calculation:
Priority Score = (10 × 0.3) + (97.5 × 0.3) + (1 × 50) + (1 × 0.2) + (1 × 0.2)
               = 3 + 29.25 + 50 + 0.2 + 0.2
               = 82.65

Result: P0 - Critical
SLA: 24 hours
Action: Emergency patch immediately, all hands on deck
```

---

### Example 2: High CVSS, Low EPSS

```
CVE: CVE-2023-99999 (Hypothetical)
CVSS: 9.0 (High)
EPSS: 0.001 (0.1%)
KEV: No
Asset: Medium (internal dashboard)
Exposure: Internal only

Calculation:
Priority Score = (9 × 0.3) + (0.1 × 0.3) + (0 × 50) + (0.4 × 0.2) + (0.5 × 0.2)
               = 2.7 + 0.03 + 0 + 0.08 + 0.1
               = 2.91

Result: P3 - Low
SLA: 90 days
Action: Backlog, address in maintenance window
Reasoning: High CVSS but very low exploitation probability, internal only, medium asset
```

---

### Example 3: Medium CVSS, High EPSS

```
CVE: CVE-2023-88888 (Hypothetical)
CVSS: 7.5 (High)
EPSS: 0.85 (85%)
KEV: No
Asset: High (user-facing API)
Exposure: Internet-facing

Calculation:
Priority Score = (7.5 × 0.3) + (85 × 0.3) + (0 × 50) + (0.7 × 0.2) + (1 × 0.2)
               = 2.25 + 25.5 + 0 + 0.14 + 0.2
               = 28.09

Result: P1 - High
SLA: 7 days
Action: Prioritize in current sprint
Reasoning: High exploitation probability + Internet-facing = high risk
```

---

## Summary

**Quick Reference:**

```
P0: KEV + Internet + Critical asset → 24 hours
P1: CVSS ≥ 9.0 OR (CVSS ≥ 7.0 AND EPSS ≥ 0.1) → 7 days
P2: CVSS 7.0-8.9 OR EPSS ≥ 0.05 → 30 days
P3: CVSS 4.0-6.9, EPSS < 0.05 → 90 days
P4: CVSS < 4.0 → No SLA
```

**Data Sources:**

```
CVSS: NVD API, Trivy scans, vendor advisories
EPSS: https://api.first.org/data/v1/epss
KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
```

**Automation:**
See `examples/prioritization/` for complete scripts.
