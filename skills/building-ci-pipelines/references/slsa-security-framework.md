# SLSA Security Framework

Supply-chain Levels for Software Artifacts (SLSA) is a security framework for ensuring the integrity of software artifacts throughout the software supply chain.

## Table of Contents

1. [SLSA Overview](#slsa-overview)
2. [SLSA Levels](#slsa-levels)
3. [Provenance Generation](#provenance-generation)
4. [Attestation Verification](#attestation-verification)
5. [GitHub Actions Integration](#github-actions-integration)
6. [GitLab CI Integration](#gitlab-ci-integration)
7. [Cosign Integration](#cosign-integration)

## SLSA Overview

SLSA (pronounced "salsa") prevents tampering and unauthorized modifications to software packages. It provides:

- **Provenance**: Record of how software was built
- **Integrity**: Cryptographic verification
- **Non-falsifiability**: Build system generates provenance, not developers
- **Auditability**: Complete build trail

### Why SLSA Matters

**Supply Chain Attacks Are Real:**
- SolarWinds (2020): Malicious code injected in build process
- Codecov (2021): Bash Uploader script compromised
- Log4Shell (2021): Vulnerability in widely-used library

**Compliance Requirements:**
- NIST SSDF (Secure Software Development Framework)
- PCI DSS 4.0 (Payment Card Industry Data Security Standard)
- Executive Order 14028 (Federal software procurement)

## SLSA Levels

### Level 1: Provenance Exists

**Requirements:**
- Build process generates provenance
- Provenance is available to artifact consumers

**Provides:**
- Basic record that artifact was built
- Minimal security assurance

**Example:**
```yaml
# GitHub Actions - Basic provenance
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - name: Generate build record
        run: |
          echo "{\"artifact\": \"myapp.tar.gz\", \"built_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > provenance.json
      - uses: actions/upload-artifact@v4
        with:
          name: provenance
          path: provenance.json
```

### Level 2: Hosted Build Service

**Requirements:**
- Build service (not local machine) generates provenance
- Service-generated provenance (tamper-resistant)
- Authenticated provenance

**Provides:**
- Provenance cannot be modified by developers
- Build environment is known

**Example:** GitHub Actions automatically satisfies Level 2 (hosted build service)

### Level 3: Hardened Build Platforms (RECOMMENDED)

**Requirements:**
- Hardened build environment
- Non-falsifiable provenance (cryptographically signed)
- Isolated build execution
- Parameterless build definition

**Provides:**
- High confidence in artifact integrity
- Verifiable chain of custody
- Industry standard for production

**Example:** See [GitHub Actions Integration](#github-actions-integration)

### Level 4: Two-Party Review + Hermetic Builds

**Requirements:**
- Two-person review for all changes
- Hermetic, reproducible builds
- Dependencies fetched only from trusted sources

**Provides:**
- Maximum supply chain security
- Fully reproducible builds

**Status:** Future state, limited tooling availability

## Provenance Generation

### SLSA Provenance Format

Provenance is a JSON document describing how an artifact was built:

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "subject": [
    {
      "name": "ghcr.io/myorg/myapp",
      "digest": {
        "sha256": "abcd1234..."
      }
    }
  ],
  "predicateType": "https://slsa.dev/provenance/v0.2",
  "predicate": {
    "builder": {
      "id": "https://github.com/slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@refs/tags/v1.10.0"
    },
    "buildType": "https://slsa.dev/container-based-build/v0.1",
    "invocation": {
      "configSource": {
        "uri": "git+https://github.com/myorg/myapp@refs/heads/main",
        "digest": {
          "sha1": "efgh5678..."
        },
        "entryPoint": ".github/workflows/release.yml"
      }
    },
    "metadata": {
      "buildStartedOn": "2025-12-04T10:30:00Z",
      "buildFinishedOn": "2025-12-04T10:35:00Z",
      "completeness": {
        "parameters": true,
        "environment": true,
        "materials": true
      }
    },
    "materials": [
      {
        "uri": "git+https://github.com/myorg/myapp",
        "digest": {
          "sha1": "efgh5678..."
        }
      }
    ]
  }
}
```

### Key Provenance Fields

**subject**: What was built
- name: Artifact identifier (image name, package name)
- digest: Content hash (sha256)

**builder.id**: Who built it
- URI identifying the build system
- Includes version/commit for reproducibility

**invocation.configSource**: Build instructions
- Repository URI
- Commit hash
- Workflow file path

**materials**: Build inputs
- Source code commit
- Base images
- Dependencies

## Attestation Verification

### Verification Process

1. **Download artifact and attestation**
2. **Verify attestation signature** (cryptographic)
3. **Check builder identity** (trusted build system)
4. **Verify subject matches artifact** (digest comparison)
5. **Validate materials** (expected source repo, commit)

### Manual Verification Example

```bash
# Download container image
docker pull ghcr.io/myorg/myapp@sha256:abcd1234...

# Verify SLSA provenance with cosign
cosign verify-attestation \
  --type slsaprovenance \
  --certificate-identity-regexp "^https://github.com/slsa-framework" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/myorg/myapp@sha256:abcd1234...

# Output shows verified provenance
```

### Automated Verification in Deployment

```yaml
# Kubernetes admission controller
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sImageProvenance
metadata:
  name: require-slsa-l3
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    minimumLevel: 3
    allowedBuilders:
      - "https://github.com/slsa-framework/slsa-github-generator"
```

## GitHub Actions Integration

### Container Image with SLSA Level 3

```yaml
name: SLSA Build
on:
  push:
    tags: ['v*']

permissions: read-all

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push container
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Extract digest
        run: |
          echo "digest=${{ steps.build.outputs.digest }}" >> $GITHUB_OUTPUT

  provenance:
    needs: build
    permissions:
      id-token: write  # For signing
      actions: read    # For reading workflow context
      packages: write  # For attaching attestation
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v1.10.0
    with:
      image: ghcr.io/${{ github.repository }}
      digest: ${{ needs.build.outputs.digest }}
      registry-username: ${{ github.actor }}
    secrets:
      registry-password: ${{ secrets.GITHUB_TOKEN }}
```

### Binary Artifacts with SLSA Level 3

```yaml
name: SLSA Binary Build
on:
  push:
    tags: ['v*']

permissions: read-all

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      hashes: ${{ steps.hash.outputs.hashes }}
    steps:
      - uses: actions/checkout@v4

      - name: Build binaries
        run: |
          make build-linux
          make build-windows
          make build-macos

      - name: Generate hashes
        id: hash
        run: |
          cd dist/
          sha256sum * > checksums.txt
          echo "hashes=$(cat checksums.txt | base64 -w0)" >> $GITHUB_OUTPUT

      - uses: actions/upload-artifact@v4
        with:
          name: binaries
          path: dist/*

  provenance:
    needs: build
    permissions:
      id-token: write
      actions: read
      contents: write  # For attaching to release
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.10.0
    with:
      base64-subjects: "${{ needs.build.outputs.hashes }}"
      upload-assets: true
```

### NPM Package with SLSA Level 3

```yaml
name: SLSA NPM Publish
on:
  release:
    types: [published]

permissions: read-all

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      package-name: ${{ steps.detect.outputs.package-name }}
      package-digest: ${{ steps.hash.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci
      - run: npm run build
      - run: npm pack

      - name: Detect package
        id: detect
        run: |
          PKG=$(ls *.tgz)
          echo "package-name=$PKG" >> $GITHUB_OUTPUT

      - name: Hash package
        id: hash
        run: |
          DIGEST=$(sha256sum ${{ steps.detect.outputs.package-name }} | awk '{print $1}')
          echo "digest=$DIGEST" >> $GITHUB_OUTPUT

      - uses: actions/upload-artifact@v4
        with:
          name: package
          path: "*.tgz"

  provenance:
    needs: build
    permissions:
      id-token: write
      actions: read
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.10.0
    with:
      base64-subjects: "${{ needs.build.outputs.package-digest }}"

  publish:
    needs: [build, provenance]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: package

      - uses: actions/download-artifact@v4
        with:
          name: provenance

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'

      - name: Publish to NPM
        run: npm publish ${{ needs.build.outputs.package-name }}
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## GitLab CI Integration

GitLab CI does not have native SLSA Level 3 support. Manual implementation required.

### Manual Provenance Generation

```yaml
# .gitlab-ci.yml
stages:
  - build
  - attest

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - echo "DIGEST=$(docker inspect --format='{{.Id}}' $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA)" >> build.env
  artifacts:
    reports:
      dotenv: build.env

attest:
  stage: attest
  image: gcr.io/projectsigstore/cosign:latest
  script:
    - |
      cat > provenance.json <<EOF
      {
        "_type": "https://in-toto.io/Statement/v0.1",
        "subject": [{
          "name": "$CI_REGISTRY_IMAGE",
          "digest": {"sha256": "$DIGEST"}
        }],
        "predicateType": "https://slsa.dev/provenance/v0.2",
        "predicate": {
          "builder": {"id": "https://gitlab.com/$CI_PROJECT_PATH"},
          "buildType": "https://gitlab.com/gitlab-ci",
          "invocation": {
            "configSource": {
              "uri": "git+$CI_PROJECT_URL",
              "digest": {"sha1": "$CI_COMMIT_SHA"}
            }
          }
        }
      }
      EOF
    - cosign attest --key cosign.key --predicate provenance.json $CI_REGISTRY_IMAGE@sha256:$DIGEST
```

## Cosign Integration

Cosign is a tool for signing and verifying container images and other artifacts.

### Signing with Cosign

```bash
# Generate key pair (one-time)
cosign generate-key-pair

# Sign container image
cosign sign --key cosign.key ghcr.io/myorg/myapp@sha256:abcd1234...

# Sign with OIDC (keyless)
cosign sign ghcr.io/myorg/myapp@sha256:abcd1234...
```

### Attaching Attestations

```bash
# Attach SLSA provenance
cosign attest --key cosign.key \
  --predicate provenance.json \
  --type slsaprovenance \
  ghcr.io/myorg/myapp@sha256:abcd1234...

# Attach SBOM
cosign attest --key cosign.key \
  --predicate sbom.spdx.json \
  --type spdx \
  ghcr.io/myorg/myapp@sha256:abcd1234...
```

### Verifying Signatures

```bash
# Verify with public key
cosign verify --key cosign.pub ghcr.io/myorg/myapp@sha256:abcd1234...

# Verify with OIDC (keyless)
cosign verify \
  --certificate-identity-regexp "^https://github.com/myorg" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/myorg/myapp@sha256:abcd1234...
```

### Policy Enforcement

```bash
# Verify attestation exists
cosign verify-attestation \
  --type slsaprovenance \
  --key cosign.pub \
  ghcr.io/myorg/myapp@sha256:abcd1234...

# Extract and validate provenance content
cosign verify-attestation \
  --type slsaprovenance \
  --key cosign.pub \
  ghcr.io/myorg/myapp@sha256:abcd1234... | jq '.payload | @base64d | fromjson'
```

### GitHub Actions with Cosign

```yaml
jobs:
  sign:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # For keyless signing
      packages: write
    steps:
      - name: Install Cosign
        uses: sigstore/cosign-installer@v3

      - name: Login to registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build image
        run: docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .

      - name: Push image
        run: docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Sign image (keyless)
        run: |
          cosign sign --yes \
            ghcr.io/${{ github.repository }}@$(docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/${{ github.repository }}:${{ github.sha }} | cut -d@ -f2)

      - name: Generate and attach SBOM
        run: |
          syft ghcr.io/${{ github.repository }}:${{ github.sha }} -o spdx-json > sbom.spdx.json
          cosign attest --yes --predicate sbom.spdx.json --type spdx \
            ghcr.io/${{ github.repository }}@$(docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/${{ github.repository }}:${{ github.sha }} | cut -d@ -f2)
```

## Best Practices

### DO:
- Achieve SLSA Level 3 for production artifacts
- Use OIDC (keyless signing) when possible
- Verify provenance before deployment
- Include SBOMs alongside provenance
- Store keys in hardware security modules (HSMs) if using key-based signing

### DON'T:
- Skip provenance generation for public releases
- Use developer-generated provenance (Level 1 only)
- Store signing keys in repositories
- Trust artifacts without verification
- Implement custom provenance formats (use SLSA standard)

## Resources

- SLSA Specification: https://slsa.dev
- GitHub SLSA Generator: https://github.com/slsa-framework/slsa-github-generator
- Cosign Documentation: https://docs.sigstore.dev/cosign/overview
- In-Toto: https://in-toto.io
- Sigstore: https://www.sigstore.dev
