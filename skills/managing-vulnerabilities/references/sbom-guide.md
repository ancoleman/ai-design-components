# SBOM Generation and Management Guide

Complete patterns for Software Bill of Materials (SBOM) generation, storage, consumption, and compliance.

## Table of Contents

1. [SBOM Fundamentals](#sbom-fundamentals)
2. [CycloneDX vs SPDX](#cyclonedx-vs-spdx)
3. [Generation Tools](#generation-tools)
4. [Generation Patterns](#generation-patterns)
5. [SBOM Storage and Distribution](#sbom-storage-and-distribution)
6. [SBOM Consumption](#sbom-consumption)
7. [Compliance Requirements](#compliance-requirements)
8. [Best Practices](#best-practices)

---

## SBOM Fundamentals

### What is an SBOM?

A Software Bill of Materials (SBOM) is a formal, structured list of components, libraries, and modules required to build software. Think of it as an "ingredients label" for software.

**Core Elements (NTIA Minimum):**
- Supplier name
- Component name
- Version of component
- Unique identifier (PURL, CPE)
- Dependency relationships
- Author of SBOM data
- Timestamp

### Why SBOMs Matter

**Regulatory Drivers:**
- Executive Order 14028 (US Federal software procurement)
- NTIA minimum elements for SBOM
- Industry standards (OWASP, Linux Foundation)
- Customer security requirements

**Security Benefits:**
- Vulnerability tracking: Know what's affected by new CVEs
- Supply chain transparency: Understand dependency risks
- Incident response: Quickly identify affected systems
- License compliance: Track open-source licenses

**Operational Benefits:**
- Faster vulnerability remediation
- Automated security scanning
- Compliance evidence generation
- Supply chain risk management

---

## CycloneDX vs SPDX

### Format Comparison

| Aspect | CycloneDX | SPDX |
|--------|-----------|------|
| **Focus** | Security, vulnerability management | License compliance, legal |
| **Maintainer** | OWASP | Linux Foundation |
| **Status** | OWASP standard | ISO/IEC 5962:2021 |
| **Primary Use** | DevSecOps, security pipelines | Legal teams, compliance |
| **Formats** | JSON, XML, Protocol Buffers | JSON, XML, YAML, RDF, Tag/Value |
| **Vulnerability Data** | Native support (BOM-link, VEX) | External enrichment needed |
| **License Info** | Basic license identifiers | Comprehensive legal metadata |
| **Tool Support** | Trivy, Syft, cdxgen, Grype | Tern, Microsoft SBOM Tool, Syft |
| **Speed** | Fast (JSON optimized) | Slower (more comprehensive) |
| **Size** | Smaller files | Larger files (more metadata) |

### When to Use CycloneDX

**Best For:**
- DevSecOps and security-focused teams
- Vulnerability tracking and management
- Fast CI/CD pipelines (smaller files)
- Automated security scanning
- Container security workflows
- Agile development environments

**Example Use Cases:**
```
✓ Container image SBOM for vulnerability scanning
✓ CI/CD pipeline artifact generation
✓ Automated dependency tracking
✓ Security dashboard integration
✓ Rapid SBOM generation (< 1 minute)
```

### When to Use SPDX

**Best For:**
- Legal and compliance teams
- License compliance audits
- Government/defense contracts (ISO standard)
- Comprehensive legal metadata required
- Open-source license tracking
- Long-term archival

**Example Use Cases:**
```
✓ License compliance audits
✓ Federal contract requirements
✓ Open-source license tracking
✓ Legal risk assessment
✓ Export compliance documentation
```

### Recommendation by Scenario

**Scenario 1: DevSecOps Team**
```
Format: CycloneDX JSON
Reason: Security-focused, fast, native vulnerability references
Tools: Trivy, Syft, cdxgen
```

**Scenario 2: Legal/Compliance Team**
```
Format: SPDX 2.3
Reason: Comprehensive license data, ISO standard
Tools: Microsoft SBOM Tool, Syft
```

**Scenario 3: Dual Requirements**
```
Format: Both (generate both formats)
Reason: Security AND legal needs
Tools: Syft (supports both), or Trivy + Microsoft SBOM Tool
```

**Scenario 4: Federal/Government**
```
Format: SPDX (preferred) or CycloneDX (accepted)
Reason: ISO standard alignment, government preference
Tools: Microsoft SBOM Tool, Tern
```

---

## Generation Tools

### Multi-Format Tools

#### Trivy (Recommended - All-in-One)

**Supports:** CycloneDX, SPDX
**Best For:** Container images, fast CI/CD, comprehensive coverage

```bash
# CycloneDX JSON (recommended for security)
trivy image --format cyclonedx --output sbom.json alpine:latest

# SPDX JSON (for compliance)
trivy image --format spdx-json --output sbom-spdx.json alpine:latest

# Scan filesystem
trivy fs --format cyclonedx --output sbom.json .

# Include vulnerabilities in SBOM
trivy image --format cyclonedx --scanners vuln --output sbom-with-vulns.json alpine:latest
```

**Strengths:**
- All-in-one: Scan + SBOM generation
- Fast: Optimized for CI/CD
- Multiple targets: Containers, filesystems, Git repos
- Vulnerability integration: Include vulnerabilities in SBOM

---

#### Syft (Accuracy-Focused)

**Supports:** CycloneDX, SPDX, Syft JSON
**Best For:** High accuracy, SBOM-first workflows, Anchore ecosystem

```bash
# CycloneDX
syft alpine:latest -o cyclonedx-json=sbom.json

# SPDX
syft alpine:latest -o spdx-json=sbom-spdx.json

# Multiple formats at once
syft alpine:latest -o cyclonedx-json=sbom-cdx.json -o spdx-json=sbom-spdx.json

# Scan directory
syft dir:. -o cyclonedx-json=sbom.json

# Scan with cataloging options
syft packages alpine:latest --scope all-layers -o cyclonedx-json
```

**Strengths:**
- High accuracy: Precise package detection
- Multi-format: CycloneDX, SPDX, custom JSON
- Flexible: Many output formats and options
- Anchore integration: Works with Grype for scanning

---

#### cdxgen (Multi-Language)

**Supports:** CycloneDX only
**Best For:** Multi-language projects, Node.js/Python/Java focus

```bash
# Install
npm install -g @cyclonedx/cdxgen

# Generate SBOM
cdxgen -o sbom.json .

# Specific project type
cdxgen -t node -o sbom.json .

# With evidence (build info)
cdxgen --evidence -o sbom.json .

# Include dev dependencies
cdxgen --include-dev -o sbom.json .
```

**Strengths:**
- 20+ languages: Node.js, Python, Java, Go, PHP, .NET, etc.
- OWASP official: Maintained by CycloneDX team
- Evidence tracking: Build and deployment metadata
- Container support: Docker and OCI images

---

### Language-Specific Tools

#### Node.js

```bash
# CycloneDX BOM
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# SPDX
npm install -g spdx-sbom-generator
spdx-sbom-generator -p .
```

#### Python

```bash
# CycloneDX
pip install cyclonedx-bom
cyclonedx-py -o sbom.json

# Syft (recommended)
syft dir:. -o cyclonedx-json=sbom.json
```

#### Java (Maven)

```xml
<!-- pom.xml -->
<plugin>
  <groupId>org.cyclonedx</groupId>
  <artifactId>cyclonedx-maven-plugin</artifactId>
  <version>2.7.9</version>
  <executions>
    <execution>
      <goals>
        <goal>makeAggregateBom</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

```bash
# Generate SBOM
mvn cyclonedx:makeAggregateBom
```

#### Go

```bash
# Syft
syft packages dir:. -o cyclonedx-json=sbom.json

# cdxgen
cdxgen -t go -o sbom.json .
```

#### Rust

```bash
# cargo-sbom
cargo install cargo-sbom
cargo sbom --output-format cyclonedx_json_1_4 > sbom.json
```

---

## Generation Patterns

### Pattern 1: CI/CD Automatic Generation

**GitHub Actions:**

```yaml
name: Generate SBOM

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Generate CycloneDX SBOM (security)
        run: |
          trivy image --format cyclonedx \
            --output sbom-cyclonedx.json \
            myapp:${{ github.sha }}

      - name: Generate SPDX SBOM (compliance)
        run: |
          syft myapp:${{ github.sha }} \
            -o spdx-json=sbom-spdx.json

      - name: Upload SBOM artifacts
        uses: actions/upload-artifact@v3
        with:
          name: sboms
          path: |
            sbom-cyclonedx.json
            sbom-spdx.json
          retention-days: 90

      - name: Attach SBOM to release (if release event)
        if: github.event_name == 'release'
        run: |
          gh release upload ${{ github.event.release.tag_name }} \
            sbom-cyclonedx.json sbom-spdx.json
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**GitLab CI:**

```yaml
sbom-generation:
  stage: build
  image: aquasec/trivy:latest
  script:
    - trivy image --format cyclonedx --output sbom.json $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    paths:
      - sbom.json
    reports:
      cyclonedx: sbom.json
    expire_in: 90 days
```

---

### Pattern 2: Multi-Stage Docker Build with SBOM

**Dockerfile:**

```dockerfile
# Stage 1: Build application
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production

# Generate SBOM during build
RUN npx @cyclonedx/cyclonedx-npm \
    --output-file /tmp/sbom.json \
    --output-format JSON \
    --short-PURLs

# Stage 2: Runtime
FROM node:20-alpine AS runtime
WORKDIR /app

# Copy application
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Include SBOM in image
COPY --from=builder /tmp/sbom.json /app/sbom.json

# Label with SBOM location
LABEL org.opencontainers.image.sbom=/app/sbom.json

CMD ["node", "index.js"]
```

---

### Pattern 3: SBOM as OCI Artifact

Store SBOM alongside container image in registry:

```bash
# Install ORAS (OCI Registry As Storage)
brew install oras

# Generate SBOM
trivy image --format cyclonedx --output sbom.json myapp:latest

# Attach SBOM to image as OCI artifact
oras attach myregistry.io/myapp:latest \
  --artifact-type application/vnd.cyclonedx+json \
  sbom.json:application/vnd.cyclonedx+json

# Discover attached artifacts
oras discover myregistry.io/myapp:latest

# Pull SBOM
oras pull myregistry.io/myapp:latest --artifact-type application/vnd.cyclonedx+json
```

---

### Pattern 4: SBOM Enrichment with Vulnerabilities

Include vulnerability data in SBOM:

```bash
# Generate SBOM with vulnerabilities (CycloneDX VEX)
trivy image --format cyclonedx \
  --scanners vuln \
  --output sbom-with-vulns.json \
  myapp:latest

# Separate SBOM and vulnerability report
trivy image --format cyclonedx --output sbom.json myapp:latest
trivy image --format json --output vulns.json myapp:latest
```

---

## SBOM Storage and Distribution

### Storage Options

#### 1. Version Control (Git)

**Best For:** Tracking SBOM changes over time

```bash
# Store in repository
git add sbom.json
git commit -m "chore: Update SBOM for v1.2.0"
git tag v1.2.0
git push --tags
```

**Structure:**
```
project/
├── sbom/
│   ├── sbom-v1.0.0.json
│   ├── sbom-v1.1.0.json
│   └── sbom-latest.json
└── src/
```

---

#### 2. Artifact Repository

**Best For:** Enterprise artifact management

**Artifactory:**
```bash
# Upload to Artifactory
curl -H "X-JFrog-Art-Api:$API_KEY" \
  -T sbom.json \
  "https://artifactory.example.com/artifactory/sbom-repo/myapp/1.0.0/sbom.json"
```

**Nexus:**
```bash
# Upload to Nexus
curl -u admin:admin123 \
  --upload-file sbom.json \
  "https://nexus.example.com/repository/sbom-repo/myapp/1.0.0/sbom.json"
```

---

#### 3. SBOM Management Platforms

**Dependency Track:**

```bash
# Upload SBOM
curl -X PUT \
  "https://dtrack.example.com/api/v1/bom" \
  -H "X-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @sbom.json
```

**Kubernetes ConfigMap:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-sbom
  namespace: production
data:
  sbom.json: |
    {
      "bomFormat": "CycloneDX",
      "specVersion": "1.4",
      ...
    }
```

---

#### 4. Cloud Storage

**AWS S3:**

```bash
# Upload to S3
aws s3 cp sbom.json s3://company-sboms/myapp/v1.0.0/sbom.json

# Make public (if needed for customers)
aws s3api put-object-acl \
  --bucket company-sboms \
  --key myapp/v1.0.0/sbom.json \
  --acl public-read
```

**Google Cloud Storage:**

```bash
# Upload to GCS
gsutil cp sbom.json gs://company-sboms/myapp/v1.0.0/sbom.json
```

---

### Distribution Methods

#### 1. Include in Software Package

```bash
# Include SBOM in release tarball
tar -czf myapp-v1.0.0.tar.gz myapp/ sbom.json

# Include in installer
dpkg-deb --build --root-owner-group myapp_1.0.0_amd64
# (SBOM in /usr/share/doc/myapp/sbom.json)
```

---

#### 2. Publish with Release

**GitHub Releases:**

```bash
# Create release with SBOM
gh release create v1.0.0 \
  --title "Release v1.0.0" \
  --notes "See CHANGELOG.md" \
  myapp-v1.0.0.tar.gz \
  sbom-cyclonedx.json \
  sbom-spdx.json
```

---

#### 3. API Endpoint

Serve SBOM via API for automated consumption:

```javascript
// Express.js example
app.get('/sbom/:version', (req, res) => {
  const sbomPath = `./sboms/sbom-${req.params.version}.json`;
  res.sendFile(sbomPath);
});

// https://api.example.com/sbom/1.0.0
```

---

## SBOM Consumption

### Scanning SBOM Instead of Image

**Faster CI/CD:** Scan SBOM (seconds) vs. re-scan image (minutes)

```bash
# Generate SBOM once (build stage)
trivy image --format cyclonedx --output sbom.json myapp:latest

# Scan SBOM in subsequent stages (fast)
trivy sbom sbom.json --severity HIGH,CRITICAL

# With Grype
grype sbom:sbom.json --fail-on high
```

**GitHub Actions Pattern:**

```yaml
build:
  runs-on: ubuntu-latest
  steps:
    - run: docker build -t myapp:${{ github.sha }} .
    - run: trivy image --format cyclonedx --output sbom.json myapp:${{ github.sha }}
    - uses: actions/upload-artifact@v3
      with:
        name: sbom
        path: sbom.json

scan-pr:
  runs-on: ubuntu-latest
  needs: build
  steps:
    - uses: actions/download-artifact@v3
      with:
        name: sbom
    - run: trivy sbom sbom.json --severity HIGH,CRITICAL --exit-code 1
```

---

### SBOM Analysis and Queries

**Query SBOM with jq:**

```bash
# List all components
jq '.components[] | {name: .name, version: .version}' sbom.json

# Find specific dependency
jq '.components[] | select(.name == "lodash")' sbom.json

# Count dependencies
jq '.components | length' sbom.json

# List licenses
jq '.components[].licenses[].license.id' sbom.json | sort -u

# Find vulnerabilities (if included)
jq '.vulnerabilities[] | {id: .id, severity: .ratings[0].severity}' sbom.json
```

**Python Script Example:**

```python
import json

with open('sbom.json') as f:
    sbom = json.load(f)

# Extract components
components = sbom.get('components', [])

# Group by license
licenses = {}
for comp in components:
    for lic in comp.get('licenses', []):
        license_id = lic['license']['id']
        licenses.setdefault(license_id, []).append(comp['name'])

# Report
for license, packages in licenses.items():
    print(f"{license}: {len(packages)} packages")
```

---

### SBOM Diffing

Compare SBOMs between versions:

```bash
# Generate SBOMs for two versions
trivy image --format cyclonedx --output sbom-old.json myapp:v1.0.0
trivy image --format cyclonedx --output sbom-new.json myapp:v1.1.0

# Extract component lists
jq -r '.components[] | "\(.name)@\(.version)"' sbom-old.json | sort > old-deps.txt
jq -r '.components[] | "\(.name)@\(.version)"' sbom-new.json | sort > new-deps.txt

# Show differences
diff old-deps.txt new-deps.txt

# Added dependencies
comm -13 old-deps.txt new-deps.txt

# Removed dependencies
comm -23 old-deps.txt new-deps.txt
```

---

## Compliance Requirements

### NTIA Minimum Elements

Required fields for SBOM compliance:

1. **Supplier Name:** Who provides the component
2. **Component Name:** Name of the software component
3. **Version:** Version identifier
4. **Unique Identifier:** PURL, CPE, or similar
5. **Dependency Relationships:** Component graph
6. **Author of SBOM:** Who created the SBOM
7. **Timestamp:** When SBOM was created

**Validation:**

```bash
# Verify NTIA compliance
# Check for required fields in CycloneDX
jq '.metadata.timestamp, .metadata.authors, .components[0] | {name, version, purl}' sbom.json
```

---

### Executive Order 14028 (Federal)

**Requirements:**
- SBOM for all software sold to federal government
- Machine-readable format (CycloneDX or SPDX)
- NTIA minimum elements included
- Regular updates with vulnerability data

**Recommended Format:** SPDX (ISO standard preferred by government)

---

### Industry Standards

**OWASP CycloneDX:**
- Current version: 1.5
- Security-focused SBOM standard
- Used by: Trivy, Syft, cdxgen, Dependency Track

**SPDX:**
- Current version: 2.3
- ISO/IEC 5962:2021
- Used by: Linux Foundation, Microsoft SBOM Tool

---

## Best Practices

### 1. Generate SBOM on Every Build

```yaml
# Always generate SBOM
- name: Generate SBOM
  run: trivy image --format cyclonedx --output sbom.json $IMAGE
  if: always()  # Generate even if tests fail
```

### 2. Store with Artifacts

```yaml
# Upload SBOM with build artifacts
- uses: actions/upload-artifact@v3
  with:
    name: release-artifacts
    path: |
      myapp-binary
      sbom.json
      sbom-spdx.json
```

### 3. Version SBOMs

```bash
# Include version in filename
trivy image --format cyclonedx --output sbom-v${VERSION}.json myapp:${VERSION}

# Tag SBOMs in Git
git tag sbom-v1.0.0
```

### 4. Provide Multiple Formats

```bash
# Generate both CycloneDX (security) and SPDX (compliance)
trivy image --format cyclonedx --output sbom-cyclonedx.json myapp:latest
trivy image --format spdx-json --output sbom-spdx.json myapp:latest
```

### 5. Automate Distribution

```yaml
# Automatically attach to releases
- name: Upload to release
  if: github.event_name == 'release'
  run: gh release upload ${{ github.ref_name }} sbom*.json
```

### 6. Sign SBOMs

```bash
# Sign with cosign
cosign sign-blob --key cosign.key sbom.json > sbom.json.sig

# Verify
cosign verify-blob --key cosign.pub --signature sbom.json.sig sbom.json
```

### 7. Include in Documentation

```markdown
# README.md

## Security

Software Bill of Materials (SBOM) available:
- CycloneDX: [sbom-cyclonedx.json](./sbom-cyclonedx.json)
- SPDX: [sbom-spdx.json](./sbom-spdx.json)

Generated with: Trivy v0.48.0
Last updated: 2025-12-04
```

### 8. Continuous Monitoring

```bash
# Upload to Dependency Track for continuous monitoring
curl -X PUT "https://dtrack.example.com/api/v1/bom" \
  -H "X-Api-Key: $API_KEY" \
  -d @sbom.json

# Get notifications on new vulnerabilities
```

---

## Troubleshooting

### Common Issues

**1. Large SBOM Files**

```bash
# Problem: SBOM is 50MB+
# Solution: Exclude unnecessary components

# Exclude dev dependencies
trivy image --skip-dirs node_modules --format cyclonedx myapp:latest

# Syft: scope production only
syft myapp:latest --scope squashed -o cyclonedx-json
```

**2. Missing Dependencies**

```bash
# Problem: Not all dependencies detected
# Solution: Use multiple tools and merge

# Generate with multiple tools
trivy image --format cyclonedx --output sbom-trivy.json myapp:latest
syft myapp:latest -o cyclonedx-json=sbom-syft.json

# Manual merge or use cdx-merge tool
```

**3. Incompatible Format Versions**

```bash
# Problem: Tool doesn't support CycloneDX 1.5
# Solution: Specify older version

# Syft with specific version
syft myapp:latest --output cyclonedx-1.4-json=sbom.json
```

---

## Summary

**Quick Decision Guide:**

```
Security/DevSecOps → CycloneDX + Trivy/Syft
Legal/Compliance → SPDX + Microsoft SBOM Tool / Syft
Both requirements → Generate both formats
Federal/Government → SPDX (ISO standard)
Fast CI/CD → CycloneDX JSON
```

**Essential Commands:**

```bash
# Generate CycloneDX (security)
trivy image --format cyclonedx --output sbom.json myapp:latest

# Generate SPDX (compliance)
syft myapp:latest -o spdx-json=sbom-spdx.json

# Scan SBOM (fast)
trivy sbom sbom.json --severity HIGH,CRITICAL
```
