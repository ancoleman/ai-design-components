# Detection Rules Guide

## Table of Contents

- [SIGMA Rule Format](#sigma-rule-format)
- [Elastic EQL](#elastic-eql)
- [Microsoft Sentinel KQL](#microsoft-sentinel-kql)
- [Splunk SPL](#splunk-spl)
- [Rule Development Workflow](#rule-development-workflow)
- [MITRE ATT&CK Mapping](#mitre-attck-mapping)
- [Testing and Validation](#testing-and-validation)

## SIGMA Rule Format

### What is SIGMA?

SIGMA is an open-source, generic signature format for SIEM systems. Write detection logic once, compile to any SIEM query language (Elastic EQL, Splunk SPL, Microsoft KQL, etc.).

### SIGMA Rule Structure

```yaml
title: [Detection Rule Title]
id: [UUID]
status: [stable|test|experimental]
description: [Detailed description of what this detects]
author: [Author name or team]
date: [YYYY/MM/DD]
modified: [YYYY/MM/DD]
references:
  - [URL to documentation, threat research]
tags:
  - attack.[tactic]
  - attack.[technique_id]
logsource:
  category: [process_creation|network_traffic|authentication]
  product: [windows|linux|aws|azure]
detection:
  selection:
    [field_name]: [value or pattern]
  condition: [selection logic]
falsepositives:
  - [Known false positive scenario]
level: [low|medium|high|critical]
```

### SIGMA Rule Examples

#### Brute Force Detection

```yaml
title: Multiple Failed Login Attempts from Single Source
id: 8a9e3c7f-4b2d-4e8a-9f1c-2d5e6f7a8b9c
status: stable
description: Detects potential brute force attacks (10+ failed logins in 10 minutes)
author: Security Team
date: 2025/12/03
references:
  - https://attack.mitre.org/techniques/T1110/
tags:
  - attack.credential_access
  - attack.t1110
logsource:
  category: authentication
  product: linux
detection:
  selection:
    event.type: authentication
    event.outcome: failure
  timeframe: 10m
  condition: selection | count() by source.ip > 10
falsepositives:
  - Misconfigured monitoring systems
  - Password reset attempts
level: high
```

#### Privilege Escalation (sudo)

```yaml
title: Suspicious Sudo Execution
id: 7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e
status: stable
description: Detects sudo execution by non-privileged users (web servers, service accounts)
author: Security Team
date: 2025/12/03
references:
  - https://attack.mitre.org/techniques/T1548/003/
tags:
  - attack.privilege_escalation
  - attack.t1548.003
logsource:
  category: process_creation
  product: linux
detection:
  selection:
    process.name: sudo
    user.name:
      - 'www-data'
      - 'nobody'
      - 'nginx'
      - 'apache'
  condition: selection
falsepositives:
  - Legitimate administrative scripts running as service accounts
level: high
```

#### Data Exfiltration

```yaml
title: Large Data Upload to External Domain
id: 9c0d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f
status: stable
description: Detects uploads >100MB to non-whitelisted external domains
author: Security Team
date: 2025/12/03
references:
  - https://attack.mitre.org/techniques/T1041/
tags:
  - attack.exfiltration
  - attack.t1041
logsource:
  category: network_traffic
  product: proxy
detection:
  selection:
    http.request.method: POST
    http.request.bytes: '>100000000'
  filter_whitelist:
    destination.domain:
      - 'backup.company.com'
      - 's3.amazonaws.com'
      - 'blob.core.windows.net'
  condition: selection and not filter_whitelist
falsepositives:
  - Large file uploads to legitimate cloud storage
  - Backup operations
level: critical
```

#### Mimikatz Detection

```yaml
title: Mimikatz Execution Detected
id: 0d1e2f3a-4b5c-6d7e-8f9a-0b1c2d3e4f5a
status: stable
description: Detects Mimikatz credential dumping tool execution
author: Security Team
date: 2025/12/03
references:
  - https://attack.mitre.org/techniques/T1003/001/
tags:
  - attack.credential_access
  - attack.t1003.001
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine|contains:
      - 'sekurlsa::logonpasswords'
      - 'sekurlsa::tickets'
      - 'lsadump::sam'
      - 'kerberos::golden'
  condition: selection
falsepositives:
  - Security testing (authorized penetration tests)
level: critical
```

### Compiling SIGMA Rules

```bash
# Install SIGMA compiler
pip install sigma-cli

# Compile to Elastic EQL
sigmac -t es-eql brute-force-detection.yml

# Compile to Splunk SPL
sigmac -t splunk brute-force-detection.yml

# Compile to Microsoft KQL
sigmac -t kusto brute-force-detection.yml

# Compile to all formats
sigmac -t es-eql,splunk,kusto brute-force-detection.yml
```

---

## Elastic EQL

### Event Query Language Overview

EQL (Event Query Language) is Elastic's native query language for sequence-based detection and complex event correlation.

### Advantages

- Native to Elastic SIEM
- Sequence-based detection (multi-event correlation)
- Time-based analysis with `maxspan`
- MITRE ATT&CK mapping built-in
- Efficient query execution

### Basic EQL Query

```eql
process where event.type == "start" and
  process.name == "powershell.exe" and
  process.args : ("Invoke-WebRequest", "iwr", "wget", "curl")
```

### Sequence Detection

```eql
sequence by user.name with maxspan=5m
  [process where event.type == "start" and process.name == "powershell.exe"]
  [library where dll.name == "kernel32.dll" and
    dll.code_signature.subject_name != "Microsoft Corporation"]
  [network where process.name == "powershell.exe"]
```

**Explanation:**
1. PowerShell starts
2. Loads non-Microsoft signed DLL (suspicious)
3. Makes network connection (potential C2)
4. All within 5 minutes, by same user

### Advanced Examples

**Credential Dumping (Registry Access):**

```eql
registry where registry.path : (
  "HKLM\\SAM\\SAM\\Domains\\Account\\Users\\*",
  "HKLM\\SECURITY\\Policy\\Secrets\\*"
) and not process.executable : (
  "C:\\Windows\\System32\\lsass.exe",
  "C:\\Windows\\System32\\svchost.exe"
)
```

**Ransomware Behavior:**

```eql
sequence by host.id with maxspan=1h
  [file where event.action == "modification" and file.extension : ("docx", "xlsx", "pdf")]
  [file where event.action == "modification" and file.extension : ("encrypted", "locked", "crypted")]
  [file where event.action == "creation" and file.name : ("*README*", "*DECRYPT*", "*RANSOM*")]
```

**Lateral Movement (RDP Chain):**

```eql
sequence by user.name with maxspan=10m
  [authentication where event.outcome == "success" and source.ip == "10.0.1.100"]
  [process where process.name == "mstsc.exe"]
  [authentication where event.outcome == "success" and source.ip != "10.0.1.100"]
```

---

## Microsoft Sentinel KQL

### Kusto Query Language Overview

KQL (Kusto Query Language) is Microsoft's query language for Azure Monitor, Log Analytics, and Sentinel.

### Advantages

- Native to Azure ecosystem
- Rich aggregation and summarization functions
- Powerful join and union operators
- Time-series analysis
- Integration with Azure Logic Apps for automation

### Basic KQL Query

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != 0  // Failed login
| where UserPrincipalName == "admin@company.com"
| project TimeGenerated, UserPrincipalName, IPAddress, Location
```

### Advanced Examples

**Failed Logins from Multiple Countries:**

```kql
let threshold = 3;
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != 0  // Failed login
| summarize FailedCountries=dcount(LocationDetails.countryOrRegion),
            FailedAttempts=count() by UserPrincipalName
| where FailedCountries >= threshold
| project UserPrincipalName, FailedCountries, FailedAttempts
```

**Suspicious Azure Resource Deletion:**

```kql
AzureActivity
| where TimeGenerated > ago(24h)
| where OperationNameValue endswith "DELETE"
| where ActivityStatusValue == "Success"
| where ResourceProvider in ("Microsoft.Compute", "Microsoft.Storage", "Microsoft.Sql")
| summarize DeletedResources=count() by Caller, ResourceProvider
| where DeletedResources > 5
```

**Office 365 Email Forwarding Rule Created:**

```kql
OfficeActivity
| where TimeGenerated > ago(7d)
| where Operation == "New-InboxRule"
| where Parameters has "ForwardTo" or Parameters has "RedirectTo"
| extend ForwardingAddress = extract("(ForwardTo|RedirectTo):([^;]+)", 2, Parameters)
| project TimeGenerated, UserId, ClientIP, ForwardingAddress
```

**Anomalous Sign-in Pattern:**

```kql
let historical_logins = SigninLogs
| where TimeGenerated between (ago(30d) .. ago(1d))
| where ResultType == 0
| summarize hist_countries = make_set(LocationDetails.countryOrRegion) by UserPrincipalName;

SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType == 0
| extend current_country = LocationDetails.countryOrRegion
| join kind=inner historical_logins on UserPrincipalName
| where not(current_country in (hist_countries))
| project TimeGenerated, UserPrincipalName, current_country, IPAddress
```

---

## Splunk SPL

### Search Processing Language Overview

SPL (Search Processing Language) is Splunk's query language for searching, filtering, and transforming security events.

### Advantages

- Powerful data transformation (eval, rex, stats)
- Pipeline-based query structure
- Rich statistical functions
- Extensive field extraction
- Mature ecosystem with thousands of searches

### Basic SPL Query

```spl
index=windows_logs sourcetype=WinEventLog:Security EventCode=4625
| stats count by src_ip, user
| where count > 5
```

### Advanced Examples

**SQL Injection Detection:**

```spl
index=web_logs sourcetype=access_combined
| rex field=uri "(?<sql_keywords>union|select|insert|update|delete|drop|exec|script)"
| where isnotnull(sql_keywords)
| stats count by src_ip, uri, sql_keywords
| where count > 5
```

**Unusual Process Parent-Child Relationship:**

```spl
index=windows_logs sourcetype=WinEventLog:Security EventCode=4688
| eval parent_child=parent_process_name + "->" + new_process_name
| search parent_child IN (
    "winword.exe->cmd.exe",
    "excel.exe->powershell.exe",
    "outlook.exe->wscript.exe"
)
| stats count by ComputerName, user, parent_child
```

**AWS CloudTrail Anomalous API Activity:**

```spl
index=aws_cloudtrail
| stats count by userName, eventName
| eventstats avg(count) as avg_count, stdev(count) as stdev_count by eventName
| eval threshold = avg_count + (2 * stdev_count)
| where count > threshold
| table userName, eventName, count, avg_count, threshold
```

**Successful Login After Multiple Failures:**

```spl
index=authentication
| transaction user maxspan=30m
| search failed_attempts>5 AND success_attempts>0
| table _time, user, src_ip, failed_attempts, success_attempts
```

---

## Rule Development Workflow

### 1. Threat Research

- Identify attack technique (MITRE ATT&CK framework)
- Research indicators of compromise (IOCs)
- Understand attacker TTPs (Tactics, Techniques, Procedures)
- Review public threat intelligence reports

### 2. Log Analysis

- Identify log sources containing relevant events
- Analyze log structure and fields
- Determine detection logic and thresholds
- Identify potential false positive scenarios

### 3. Rule Development

- Write SIGMA rule (universal format) OR platform-specific query
- Include MITRE ATT&CK mapping
- Document false positives
- Set appropriate severity level

### 4. Testing

- Test rule against historical data (2-4 weeks)
- Validate true positives (attack scenarios)
- Identify false positives
- Adjust thresholds and whitelisting

### 5. Deployment

- Deploy rule to production SIEM
- Monitor alert volume and quality
- Tune rule based on operational feedback
- Document any exceptions or whitelists

### 6. Maintenance

- Review rule effectiveness monthly
- Update based on new threat intelligence
- Adjust thresholds as environment changes
- Archive or deprecate ineffective rules

---

## MITRE ATT&CK Mapping

### Top 10 Techniques to Detect

| Technique ID | Technique Name | Detection Method |
|--------------|---------------|------------------|
| **T1078** | Valid Accounts | Unusual login patterns, impossible travel |
| **T1059.001** | PowerShell | Malicious PowerShell commands, script downloads |
| **T1003** | Credential Dumping | Mimikatz signatures, registry access |
| **T1021.001** | Remote Desktop | RDP from unusual sources, lateral movement |
| **T1071** | Application Layer Protocol | C2 communication via HTTP/DNS |
| **T1105** | Ingress Tool Transfer | File downloads from internet |
| **T1486** | Data Encrypted for Impact | Ransomware file encryption patterns |
| **T1087** | Account Discovery | Enumeration commands (net user, whoami) |
| **T1098** | Account Manipulation | Privilege escalation, role changes |
| **T1562.001** | Disable Security Tools | Stopping AV, SIEM agents, logging |

### Mapping SIGMA Rules to MITRE ATT&CK

```yaml
tags:
  - attack.credential_access      # Tactic
  - attack.t1110                  # Technique (Brute Force)
  - attack.t1110.001              # Sub-technique (Password Guessing)
```

**Tactics (14 total):**
- Initial Access, Execution, Persistence, Privilege Escalation
- Defense Evasion, Credential Access, Discovery, Lateral Movement
- Collection, Command and Control, Exfiltration, Impact

---

## Testing and Validation

### Unit Testing Detection Rules

**Test Data Creation:**

```bash
# Simulate brute force attack (for testing)
for i in {1..15}; do
  ssh user@target-host -p 22 2>&1 | logger -t sshd
done
```

**Rule Validation:**

```bash
# Elastic: Test EQL query
POST /_eql/search
{
  "query": "process where process.name == 'powershell.exe'",
  "size": 10
}

# Splunk: Test SPL query
index=test_data sourcetype=authentication
| stats count by src_ip
| where count > 10

# Sentinel: Test KQL query
SigninLogs
| where TimeGenerated > ago(1h)
| take 10
```

### False Positive Analysis

**Common False Positive Scenarios:**

1. **Monitoring Systems** - Health checks, scanners triggering rate-limit alerts
2. **Automated Processes** - Scripts, CI/CD pipelines triggering unusual process alerts
3. **Admin Operations** - Legitimate bulk operations (user creation, config changes)
4. **Known Tools** - Security tools (Nessus, Qualys) triggering vulnerability scan alerts

**Mitigation Strategies:**

- **Whitelisting** - Exclude known-safe IPs, users, processes
- **Threshold Tuning** - Adjust count/frequency thresholds
- **Context Enrichment** - Add business context (service accounts, admin users)
- **Time-Based Rules** - Suppress alerts during maintenance windows

### Continuous Improvement

**Metrics to Track:**

- **True Positive Rate** - % of alerts that are actual threats (target: >30%)
- **False Positive Rate** - % of alerts that are benign (target: <50%)
- **Mean Time to Investigate** - Average time to triage alert (target: <15 min)
- **Alert Volume** - Total alerts per day (target: <100)
- **Coverage** - % of MITRE ATT&CK techniques detected (target: >70%)

**Monthly Review:**

- Analyze alert metrics
- Review incidents detected by each rule
- Identify rules needing tuning or deprecation
- Update rules based on new threat intelligence
- Document improvements and lessons learned

---

## Summary

**Use SIGMA rules when:**
- Need to support multiple SIEM platforms
- Want vendor-agnostic detection logic
- Building reusable detection rule library
- Contributing to open-source security community

**Use Elastic EQL when:**
- Using Elastic SIEM exclusively
- Need sequence-based detection (multi-event correlation)
- Require time-based analysis with `maxspan`
- Want native Elastic performance optimizations

**Use Microsoft Sentinel KQL when:**
- Using Microsoft Sentinel/Azure
- Need rich aggregation and statistical analysis
- Want integration with Azure Logic Apps
- Require time-series analysis

**Use Splunk SPL when:**
- Using Splunk Enterprise Security
- Need powerful data transformation (eval, rex)
- Require complex field extraction
- Want pipeline-based query structure
