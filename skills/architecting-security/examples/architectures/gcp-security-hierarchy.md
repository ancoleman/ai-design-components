# GCP Security Hierarchy Architecture

## Overview

Google Cloud Platform (GCP) security architecture uses resource hierarchy for organizational structure and governance. Apply security controls through IAM policies, Organization Policies, and VPC Service Controls to enforce defense-in-depth.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ORGANIZATION (example.com)                            │
│                     Organization ID: 123456789                           │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Organization Policies:                                           │   │
│  │ - Require OS Login on all VMs                                    │   │
│  │ - Disable service account key creation                           │   │
│  │ - Restrict public IP on Cloud SQL                                │   │
│  │ - Require encryption with CMEK                                   │   │
│  │ - Domain restricted sharing (example.com only)                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
           │
           ├───────────────────┬──────────────────┬──────────────────┐
           │                   │                  │                  │
           ▼                   ▼                  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │Infrastructure│    │  Workloads  │    │   Sandbox   │    │ Deprecated  │
    │   Folder    │    │   Folder    │    │   Folder    │    │   Folder    │
    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
           │                   │                │                  │
           │                   │                │                  │
    ┌──────┴──────┐     ┌──────┴──────┐        │                  │
    ▼             ▼     ▼             ▼        ▼                  ▼
┌────────┐  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐      ┌────────┐
│Security│  │Network │ │ Prod   │ │  Dev   │ │Sandbox │      │Quarant.│
│Project │  │Project │ │Project │ │Project │ │Project │      │Project │
│        │  │        │ │        │ │        │ │        │      │        │
│SCC     │  │Shared  │ │App     │ │App     │ │Testing │      │Isolated│
│Cloud   │  │VPC     │ │Data    │ │Data    │ │Budget  │      │        │
│Logging │  │Cloud   │ │        │ │        │ │30-day  │      │        │
│        │  │Armor   │ │        │ │        │ │cleanup │      │        │
└────────┘  └────────┘ └────────┘ └────────┘ └────────┘      └────────┘
                │           │
                │           │
                └───────────┴──────────────┐
                                           ▼
                                 ┌──────────────────┐
                                 │ Shared VPC       │
                                 │ (Host Project)   │
                                 │                  │
                                 │ - Firewall Rules │
                                 │ - Cloud NAT      │
                                 │ - Cloud Router   │
                                 │ - Private Google │
                                 │   Access         │
                                 └──────────────────┘
```

## Resource Hierarchy Design

### Organization Level

Root node containing all GCP resources for the domain.

**Organization Policies Applied:**

```yaml
# Require OS Login
constraints/compute.requireOsLogin:
  enforce: true

# Disable service account key creation
constraints/iam.disableServiceAccountKeyCreation:
  enforce: true

# Restrict VM external IPs
constraints/compute.vmExternalIpAccess:
  listPolicy:
    deniedValues:
      - "*"
    allowedValues:
      - "projects/network-project/zones/us-central1-a/instances/bastion"

# Domain restricted sharing
constraints/iam.allowedPolicyMemberDomains:
  listPolicy:
    allowedValues:
      - "C01234567"  # example.com organization ID

# Require CMEK encryption
constraints/gcp.restrictNonCmekServices:
  listPolicy:
    deniedValues:
      - "compute.googleapis.com"
      - "storage.googleapis.com"

# Skip default network creation
constraints/compute.skipDefaultNetworkCreation:
  enforce: true

# Disable automatic IAM grants for default service accounts
constraints/iam.automaticIamGrantsForDefaultServiceAccounts:
  enforce: true
```

**Organization IAM Bindings:**

```yaml
bindings:
  - role: roles/resourcemanager.organizationAdmin
    members:
      - group:gcp-organization-admins@example.com
    condition:
      title: "Require context-aware access"
      expression: |
        device.is_corp_managed &&
        device.encryption_status == "ENCRYPTED"

  - role: roles/securitycenter.admin
    members:
      - group:security-team@example.com

  - role: roles/logging.configWriter
    members:
      - serviceAccount:logging-sa@security-project.iam.gserviceaccount.com

  - role: roles/viewer
    members:
      - group:all-employees@example.com
    condition:
      title: "Read-only during business hours"
      expression: |
        request.time.getHours("America/Los_Angeles") >= 8 &&
        request.time.getHours("America/Los_Angeles") < 18
```

### Infrastructure Folder

Contains shared infrastructure and platform services.

**Security Project:**
- Security Command Center (SCC)
- Cloud Asset Inventory
- Access Transparency logs
- Cloud Audit Logs (organization sink)
- Cloud KMS for CMEK
- Certificate Authority Service
- Security Health Analytics

**Network Project (Shared VPC Host):**
- Shared VPC network
- Cloud Armor policies
- Cloud CDN
- Cloud Load Balancing
- Cloud NAT
- Cloud Interconnect
- Private Service Connect

**Folder Policies:**

```yaml
# Require VPC Service Controls
constraints/compute.restrictVpcPeering:
  listPolicy:
    allowedValues:
      - "under:organizations/123456789/folders/infrastructure"

# Require uniform bucket-level access
constraints/storage.uniformBucketLevelAccess:
  enforce: true
```

### Workloads Folder

Contains production and non-production application projects.

**Production Environment:**
- Service projects (Shared VPC)
- Binary Authorization required
- Enhanced audit logging
- Change approval required
- High availability SLA

**Development/Staging:**
- Service projects (Shared VPC)
- Relaxed deployment policies
- Cost controls via budgets
- Automatic resource cleanup (dev)

**Folder Policies:**

```yaml
# Restrict public IPs on Cloud SQL
constraints/sql.restrictPublicIp:
  enforce: true

# Require Binary Authorization
constraints/binaryauthorization.requireAttestations:
  listPolicy:
    allowedValues:
      - "projects/security-project/attestors/production-attestor"

# Disable default service account usage
constraints/iam.disableServiceAccountKeyUpload:
  enforce: true

# Require labels
constraints/gcp.resourceLocations:
  listPolicy:
    allowedValues:
      - "in:us-locations"
      - "in:eu-locations"
```

### Sandbox Folder

Provides innovation space with relaxed controls.

**Sandbox Projects:**
- Full API access
- Budget limits enforced
- No production data
- No connectivity to corporate network
- Automatic deletion after 90 days

**Folder Policies:**

```yaml
# Budget enforcement
constraints/compute.vmExternalIpAccess:
  listPolicy:
    allowedValues:
      - "*"

# Restrict expensive VM types
constraints/compute.vmMachineTypes:
  listPolicy:
    deniedValues:
      - "n2-*"
      - "c2-*"
      - "m1-*"
    allowedValues:
      - "e2-*"
      - "n1-standard-1"
      - "n1-standard-2"
```

### Deprecated Folder

Contains projects being decommissioned or quarantined.

**Quarantine Project:**
- All APIs disabled except logging
- No external connectivity
- Read-only access for security team
- Forensics tooling enabled

**Folder Policies:**

```yaml
# Deny all API usage except logging
constraints/serviceuser.services:
  listPolicy:
    deniedValues:
      - "*"
    allowedValues:
      - "logging.googleapis.com"
      - "cloudresourcemanager.googleapis.com"
```

## VPC Service Controls

### Security Perimeter Design

```
┌─────────────────────────────────────────────────────────────┐
│              VPC SERVICE CONTROL PERIMETER                   │
│                   (Production Perimeter)                     │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Prod Project │  │ Data Project │  │ ML Project   │      │
│  │              │  │              │  │              │      │
│  │ - Compute    │  │ - BigQuery   │  │ - Vertex AI  │      │
│  │ - GKE        │  │ - Cloud SQL  │  │ - AI Platform│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  Restricted Services:                                        │
│  - storage.googleapis.com                                    │
│  - bigquery.googleapis.com                                   │
│  - compute.googleapis.com                                    │
│                                                               │
│  Ingress Rules:                                              │
│  - Allow from corporate IP ranges                            │
│  - Allow from Cloud Identity (via Access Levels)            │
│                                                               │
│  Egress Rules:                                               │
│  - Allow to Google APIs only                                 │
│  - Deny to internet                                          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Perimeter Configuration:**

```yaml
name: "accessPolicies/123456/servicePerimeters/production_perimeter"
title: "Production Perimeter"
description: "VPC SC perimeter for production workloads"
perimeterType: "PERIMETER_TYPE_REGULAR"

status:
  resources:
    - "projects/123456789"  # prod-project
    - "projects/234567890"  # data-project
    - "projects/345678901"  # ml-project

  restrictedServices:
    - "storage.googleapis.com"
    - "bigquery.googleapis.com"
    - "compute.googleapis.com"
    - "container.googleapis.com"
    - "sqladmin.googleapis.com"

  accessLevels:
    - "accessPolicies/123456/accessLevels/corp_access"
    - "accessPolicies/123456/accessLevels/secure_device_access"

  vpcAccessibleServices:
    enableRestriction: true
    allowedServices:
      - "RESTRICTED-SERVICES"
      - "logging.googleapis.com"
      - "monitoring.googleapis.com"

  ingressPolicies:
    - ingressFrom:
        sources:
          - accessLevel: "accessPolicies/123456/accessLevels/corp_access"
        identities:
          - "serviceAccount:ci-cd-sa@ci-cd-project.iam.gserviceaccount.com"
      ingressTo:
        operations:
          - serviceName: "storage.googleapis.com"
            methodSelectors:
              - method: "google.storage.objects.create"
              - method: "google.storage.objects.get"
        resources:
          - "*"

  egressPolicies:
    - egressFrom:
        identities:
          - "serviceAccount:app-sa@prod-project.iam.gserviceaccount.com"
      egressTo:
        operations:
          - serviceName: "bigquery.googleapis.com"
        resources:
          - "projects/234567890"
```

**Access Levels:**

```yaml
# Corporate network access
name: "accessPolicies/123456/accessLevels/corp_access"
title: "Corporate Access"
basic:
  conditions:
    - ipSubnetworks:
        - "203.0.113.0/24"  # Corporate office
        - "198.51.100.0/24"  # VPN range
      devicePolicy:
        requireCorpOwned: true
        requireScreenlock: true
      regions:
        - "US"
        - "EU"

# Secure device access (BeyondCorp)
name: "accessPolicies/123456/accessLevels/secure_device_access"
title: "Secure Device Access"
basic:
  conditions:
    - devicePolicy:
        requireCorpOwned: true
        requireAdminApproval: true
        requireScreenlock: true
        osConstraints:
          - osType: "DESKTOP_CHROME_OS"
            minimumVersion: "100.0.0"
          - osType: "DESKTOP_WINDOWS"
            minimumVersion: "10.0.19041"
      regions:
        - "US"
      members:
        - "user:alice@example.com"
        - "group:engineers@example.com"
```

## IAM Policy Inheritance

### Hierarchy Example

```
Organization
├── IAM: roles/viewer → group:all-employees@example.com
│
└── Folder: Infrastructure
    ├── IAM: roles/compute.networkAdmin → group:network-admins@example.com
    │
    └── Project: network-project
        ├── IAM (inherited): roles/viewer → group:all-employees@example.com
        ├── IAM (inherited): roles/compute.networkAdmin → group:network-admins@example.com
        └── IAM: roles/compute.instanceAdmin → serviceAccount:app-sa@app-project.iam.gserviceaccount.com
```

**Policy Inheritance Rules:**

1. Policies are inherited down the hierarchy
2. Child resources cannot remove inherited permissions
3. Child resources can add additional permissions
4. Most permissive policy wins
5. Deny policies (IAM Deny) override allow policies

### IAM Deny Policies

**Prevent Principal Deletion:**

```yaml
name: "policies/prevent-principal-deletion"
displayName: "Prevent deletion of critical service accounts"
rules:
  - denyRule:
      deniedPrincipals:
        - principalSet: "//iam.googleapis.com/projects/123456789/serviceAccounts/*"
      deniedPermissions:
        - "iam.serviceAccounts.delete"
      exceptionPrincipals:
        - "principal://goog/subject/security-admin@example.com"
```

**Prevent Data Exfiltration:**

```yaml
name: "policies/prevent-data-exfiltration"
displayName: "Prevent external bucket access"
rules:
  - denyRule:
      deniedPrincipals:
        - "principalSet://goog/public:all"
      deniedPermissions:
        - "storage.objects.get"
        - "storage.objects.list"
      denialCondition:
        expression: |
          resource.name.startsWith("projects/_/buckets/sensitive-") &&
          !principal.in(["domain:example.com"])
```

### Service Account Best Practices

**Workload Identity for GKE:**

```yaml
# Kubernetes Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-ksa
  namespace: production
  annotations:
    iam.gke.io/gcp-service-account: app-sa@prod-project.iam.gserviceaccount.com
```

```bash
# Bind KSA to GSA
gcloud iam service-accounts add-iam-policy-binding \
  app-sa@prod-project.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:prod-project.svc.id.goog[production/app-ksa]"
```

**Short-Lived Credentials:**

```python
from google.auth import impersonated_credentials
from google.auth.transport import requests

# Source credentials (user or SA)
source_credentials, project = google.auth.default()

# Impersonate target service account
target_scopes = ['https://www.googleapis.com/auth/cloud-platform']
target_credentials = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal='app-sa@prod-project.iam.gserviceaccount.com',
    target_scopes=target_scopes,
    lifetime=3600  # 1 hour max
)

# Use credentials
auth_request = requests.Request()
target_credentials.refresh(auth_request)
```

## Security Command Center

### Enable SCC Premium

```bash
# Enable Security Command Center API
gcloud services enable securitycenter.googleapis.com

# Configure SCC
gcloud scc settings update \
  --organization=123456789 \
  --enable-asset-discovery \
  --enable-security-health-analytics \
  --enable-event-threat-detection \
  --enable-container-threat-detection \
  --enable-web-security-scanner
```

### Security Health Analytics

**Custom Detectors:**

```yaml
# Detect public GCS buckets
name: "organizations/123456789/securityHealthAnalyticsSettings/customModules/public-bucket-detector"
displayName: "Public GCS Bucket Detector"
enablementState: ENABLED
customConfig:
  predicate:
    expression: |
      resource.type == "storage.googleapis.com/Bucket" &&
      resource.data.iamConfiguration.publicAccessPrevention == "UNSPECIFIED"
  resourceSelector:
    resourceTypes:
      - "storage.googleapis.com/Bucket"
  severity: HIGH
  description: "Detects Cloud Storage buckets without public access prevention"
  recommendation: "Enable Public Access Prevention on the bucket"
```

### Event Threat Detection

**Custom Threat Rules:**

```yaml
# Detect privilege escalation
name: "organizations/123456789/eventThreatDetectionSettings/customModules/privilege-escalation"
displayName: "Privilege Escalation Detection"
enablementState: ENABLED
customConfig:
  predicate:
    expression: |
      event.type == "google.iam.admin.v1.SetIamPolicy" &&
      event.data.policyDelta.bindingDeltas.exists(
        delta, delta.role.startsWith("roles/owner") ||
               delta.role.startsWith("roles/editor")
      )
  severity: CRITICAL
  description: "Detects IAM policy changes granting Owner or Editor roles"
```

### Continuous Exports to SIEM

```bash
# Create BigQuery export
gcloud scc bq-exports create prod-scc-export \
  --organization=123456789 \
  --dataset=projects/security-project/datasets/scc_findings \
  --description="Export SCC findings to BigQuery"

# Create Pub/Sub export
gcloud scc notifications create security-alerts \
  --organization=123456789 \
  --pubsub-topic=projects/security-project/topics/scc-findings \
  --description="Real-time SCC findings" \
  --filter="severity=\"HIGH\" OR severity=\"CRITICAL\""
```

## Binary Authorization

### Attestation Policy

```yaml
name: "projects/prod-project/policy"
globalPolicyEvaluationMode: ENABLE
defaultAdmissionRule:
  evaluationMode: REQUIRE_ATTESTATION
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
  requireAttestationsBy:
    - "projects/security-project/attestors/vulnerability-scanner"
    - "projects/security-project/attestors/code-review"
kubernetesNamespaceAdmissionRules:
  production:
    evaluationMode: REQUIRE_ATTESTATION
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
    requireAttestationsBy:
      - "projects/security-project/attestors/vulnerability-scanner"
      - "projects/security-project/attestors/code-review"
      - "projects/security-project/attestors/qa-approval"
  development:
    evaluationMode: ALWAYS_ALLOW
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
```

### Attestor Configuration

```yaml
# Vulnerability scanner attestor
name: "projects/security-project/attestors/vulnerability-scanner"
description: "Container vulnerability scan approval"
userOwnedGrafeasNote:
  noteReference: "projects/security-project/notes/vulnerability-scan-note"
  publicKeys:
    - pkixPublicKey:
        publicKeyPem: |
          -----BEGIN PUBLIC KEY-----
          MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
          -----END PUBLIC KEY-----
        signatureAlgorithm: RSA_SIGN_PKCS1_4096_SHA512
```

### CI/CD Attestation

```python
import base64
from google.cloud import containeranalysis_v1
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def create_attestation(project_id, note_id, image_url, private_key_path):
    """
    Create Binary Authorization attestation after vulnerability scan.
    """
    client = containeranalysis_v1.ContainerAnalysisClient()
    grafeas_client = client.get_grafeas_client()

    note_name = f"projects/{project_id}/notes/{note_id}"
    artifact_url = f"https://{image_url}"

    # Create occurrence (attestation)
    occurrence = {
        "resource_uri": artifact_url,
        "note_name": note_name,
        "attestation": {
            "attestation": {
                "serialized_payload": base64.b64encode(
                    artifact_url.encode()
                ).decode(),
            }
        }
    }

    # Sign attestation
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    signature = private_key.sign(
        artifact_url.encode(),
        padding.PKCS1v15(),
        hashes.SHA512()
    )

    occurrence["attestation"]["attestation"]["signatures"] = [
        {
            "public_key_id": "vulnerability-scanner-key-1",
            "signature": base64.b64encode(signature).decode()
        }
    ]

    # Create occurrence
    created = grafeas_client.create_occurrence(
        parent=f"projects/{project_id}",
        occurrence=occurrence
    )

    print(f"Attestation created: {created.name}")
    return created
```

## Cloud Audit Logs

### Organization-Level Log Sink

```bash
# Create organization log sink to BigQuery
gcloud logging sinks create org-audit-logs-sink \
  bigquery.googleapis.com/projects/security-project/datasets/audit_logs \
  --organization=123456789 \
  --include-children \
  --log-filter='logName:"cloudaudit.googleapis.com"'

# Grant sink service account permissions
gcloud projects add-iam-policy-binding security-project \
  --member="serviceAccount:o123456789-XXXXXX@gcp-sa-logging.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"
```

### Data Access Audit Configuration

```yaml
auditConfigs:
  - service: "allServices"
    auditLogConfigs:
      - logType: "ADMIN_READ"
      - logType: "DATA_READ"
      - logType: "DATA_WRITE"

  - service: "storage.googleapis.com"
    auditLogConfigs:
      - logType: "ADMIN_READ"
      - logType: "DATA_READ"
      - logType: "DATA_WRITE"
        exemptedMembers:
          - "serviceAccount:logging-sa@security-project.iam.gserviceaccount.com"

  - service: "bigquery.googleapis.com"
    auditLogConfigs:
      - logType: "ADMIN_READ"
      - logType: "DATA_READ"
        logType: "DATA_WRITE"
```

### Audit Log Analysis

```sql
-- Detect privilege escalation
SELECT
  timestamp,
  protoPayload.authenticationInfo.principalEmail,
  protoPayload.methodName,
  protoPayload.resourceName,
  JSON_EXTRACT(protoPayload.request, '$.policy.bindings') AS new_bindings
FROM
  `security-project.audit_logs.cloudaudit_googleapis_com_activity_*`
WHERE
  protoPayload.methodName = 'google.iam.admin.v1.SetIamPolicy'
  AND JSON_EXTRACT(protoPayload.request, '$.policy.bindings') LIKE '%roles/owner%'
  AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
ORDER BY timestamp DESC;

-- Detect data exfiltration attempts
SELECT
  timestamp,
  protoPayload.authenticationInfo.principalEmail,
  protoPayload.resourceName,
  COUNT(*) as access_count
FROM
  `security-project.audit_logs.cloudaudit_googleapis_com_data_access_*`
WHERE
  protoPayload.serviceName = 'storage.googleapis.com'
  AND protoPayload.methodName = 'storage.objects.get'
  AND protoPayload.resourceName LIKE '%sensitive-%'
  AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY 1, 2, 3
HAVING access_count > 100
ORDER BY access_count DESC;
```

## Network Security

### Firewall Rules Hierarchy

```yaml
# Deny all ingress (base rule)
name: "deny-all-ingress"
priority: 65535
direction: INGRESS
action: DENY
targetTags: []
sourceRanges:
  - "0.0.0.0/0"

# Allow SSH from IAP
name: "allow-ssh-iap"
priority: 1000
direction: INGRESS
action: ALLOW
sourceRanges:
  - "35.235.240.0/20"  # IAP range
allowed:
  - IPProtocol: tcp
    ports:
      - "22"
targetTags:
  - "allow-ssh"

# Allow internal traffic
name: "allow-internal"
priority: 1100
direction: INGRESS
action: ALLOW
sourceRanges:
  - "10.128.0.0/9"  # Internal VPC range
allowed:
  - IPProtocol: tcp
    ports:
      - "0-65535"
  - IPProtocol: udp
    ports:
      - "0-65535"
  - IPProtocol: icmp
```

### Cloud Armor Security Policies

```yaml
# DDoS and WAF protection
name: "cloud-armor-policy"
description: "WAF and DDoS protection for public endpoints"
rules:
  - priority: 0
    description: "Default rule"
    action: "allow"
    match:
      versionedExpr: "SRC_IPS_V1"
      config:
        srcIpRanges:
          - "*"

  - priority: 10
    description: "Block known bad IPs"
    action: "deny(403)"
    match:
      versionedExpr: "SRC_IPS_V1"
      config:
        srcIpRanges:
          - "192.0.2.0/24"

  - priority: 20
    description: "Rate limit per IP"
    action: "rate_based_ban"
    rateLimitOptions:
      conformAction: "allow"
      exceedAction: "deny(429)"
      enforceOnKey: "IP"
      rateLimitThreshold:
        count: 100
        intervalSec: 60
      banDurationSec: 600

  - priority: 30
    description: "Block SQL injection"
    action: "deny(403)"
    match:
      expr:
        expression: |
          evaluatePreconfiguredExpr('sqli-stable',
            ['owasp-crs-v030001-id942251-sqli',
             'owasp-crs-v030001-id942420-sqli',
             'owasp-crs-v030001-id942431-sqli'])

  - priority: 40
    description: "Block XSS"
    action: "deny(403)"
    match:
      expr:
        expression: |
          evaluatePreconfiguredExpr('xss-stable',
            ['owasp-crs-v030001-id941150-xss',
             'owasp-crs-v030001-id941320-xss'])
```

### Private Google Access

```yaml
# Enable Private Google Access for subnet
name: "private-subnet"
network: "projects/network-project/global/networks/shared-vpc"
region: "us-central1"
ipCidrRange: "10.128.0.0/20"
privateIpGoogleAccess: true

# Configure Private Service Connect
pscConnection:
  network: "projects/network-project/global/networks/shared-vpc"
  serviceAttachments:
    - "projects/SERVICE_PROJECT/regions/us-central1/serviceAttachments/all-apis"
  ipAddress: "10.128.10.10"
```

## Cloud KMS and Encryption

### Key Hierarchy

```
Key Ring: production-keyring (us-central1)
├── Database Encryption Key
│   ├── Purpose: ENCRYPT_DECRYPT
│   ├── Rotation: 90 days
│   └── Versions: 3 active
│
├── Application Secrets Key
│   ├── Purpose: ENCRYPT_DECRYPT
│   ├── Rotation: 30 days
│   └── Versions: 5 active
│
└── Signing Key
    ├── Purpose: ASYMMETRIC_SIGN
    ├── Algorithm: RSA_SIGN_PKCS1_4096_SHA256
    └── Versions: 1 active
```

**Key Configuration:**

```yaml
# Create key ring
name: "projects/security-project/locations/us-central1/keyRings/production-keyring"

# Create crypto key
name: "projects/security-project/locations/us-central1/keyRings/production-keyring/cryptoKeys/database-key"
purpose: "ENCRYPT_DECRYPT"
versionTemplate:
  algorithm: "GOOGLE_SYMMETRIC_ENCRYPTION"
  protectionLevel: "HSM"
rotationPeriod: "7776000s"  # 90 days
nextRotationTime: "2024-04-01T00:00:00Z"
```

**CMEK for Cloud SQL:**

```bash
# Create Cloud SQL instance with CMEK
gcloud sql instances create prod-db \
  --tier=db-n1-standard-4 \
  --region=us-central1 \
  --disk-encryption-key=projects/security-project/locations/us-central1/keyRings/production-keyring/cryptoKeys/database-key \
  --disk-encryption-key-keyring=production-keyring \
  --disk-encryption-key-location=us-central1
```

## Key Security Metrics

Monitor these metrics across GCP:

1. **IAM Metrics:**
   - Service account key age
   - Overly permissive roles (Owner, Editor)
   - Unused service accounts
   - External members in IAM policies

2. **Compliance Metrics:**
   - Organization policy violations
   - SCC findings by severity
   - Asset inventory changes
   - Non-compliant resources

3. **Network Metrics:**
   - Firewall rule hits
   - Cloud Armor blocks
   - VPC SC perimeter violations
   - Public IP usage

4. **Threat Detection:**
   - Event Threat Detection findings
   - Anomalous API usage
   - Failed authentication attempts
   - Data exfiltration attempts

## Implementation Checklist

- [ ] Create organization and verify domain ownership
- [ ] Design folder hierarchy
- [ ] Apply organization policies
- [ ] Create infrastructure projects (security, network)
- [ ] Deploy Shared VPC network
- [ ] Configure firewall rules
- [ ] Enable Security Command Center Premium
- [ ] Configure VPC Service Controls perimeters
- [ ] Define access levels
- [ ] Create workload projects
- [ ] Attach service projects to Shared VPC
- [ ] Configure Cloud KMS and create keys
- [ ] Enable CMEK for data services
- [ ] Configure organization audit log sinks
- [ ] Deploy Binary Authorization
- [ ] Create attestors and policies
- [ ] Configure Cloud Armor policies
- [ ] Enable Private Google Access
- [ ] Establish security monitoring dashboard
- [ ] Configure alerting (Pub/Sub → Cloud Functions)
- [ ] Document architecture and procedures

## References

- [GCP Resource Hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)
- [Organization Policy Constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints)
- [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs)
- [Security Command Center](https://cloud.google.com/security-command-center/docs)
- [Binary Authorization](https://cloud.google.com/binary-authorization/docs)
- [CIS Google Cloud Platform Foundation Benchmark](https://www.cisecurity.org/benchmark/google_cloud_computing_platform)
