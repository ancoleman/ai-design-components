# Implementing TLS Skill - Master Plan

**Skill Name:** `implementing-tls`
**Level:** Low Level (2,000-5,000 tokens)
**Target SKILL.md Size:** ~300-400 lines
**Research Date:** December 3, 2025
**Status:** Master Plan Complete → Ready for SKILL.md implementation

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [TLS Implementation Taxonomy](#tls-implementation-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Certificate Generation Examples](#certificate-generation-examples)
7. [Automation Patterns](#automation-patterns)
8. [mTLS Patterns](#mtls-patterns)
9. [Debugging Guide](#debugging-guide)
10. [Tool Recommendations](#tool-recommendations)
11. [Skill Structure Design](#skill-structure-design)
12. [Integration Points](#integration-points)
13. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why TLS Implementation Matters

TLS (Transport Layer Security) is the **foundational encryption layer** for all secure communications:

```
┌─────────────────────────────────────────────────────────┐
│         TLS: Secure Communication Foundation            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Protection Against:                                    │
│  ├── Man-in-the-Middle attacks (MITM)                   │
│  ├── Eavesdropping (network sniffing)                   │
│  ├── Data tampering (integrity protection)              │
│  ├── Impersonation (authentication via certificates)    │
│  └── Replay attacks (TLS 1.3 improvements)              │
│                                                          │
│  Critical Applications:                                 │
│  ├── HTTPS (web traffic encryption)                     │
│  ├── mTLS (service-to-service authentication)           │
│  ├── API security (encrypted payloads)                  │
│  ├── Database connections (encrypted channels)          │
│  └── Email (STARTTLS, SMTPS)                            │
│                                                          │
│  2025 Requirements:                                     │
│  ├── TLS 1.3 recommended (improved performance/security)│
│  ├── Automated certificate management (90-day certs)    │
│  ├── Perfect Forward Secrecy (PFS) mandatory            │
│  ├── OCSP stapling for performance                      │
│  └── Post-quantum cryptography preparation              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Why TLS 1.3 is Critical (2025):**
- **Faster handshakes**: 1-RTT vs 2-RTT in TLS 1.2 (50% faster)
- **Enhanced privacy**: Encrypts more of the handshake
- **Simplified cipher suites**: Removed weak algorithms
- **0-RTT resumption**: Zero round-trip time for repeat connections
- **Quantum-resistant**: Forward-looking for post-quantum migration

**The Cost of Poor TLS:**
- **Let's Encrypt issues 3.5M+ certs/day**: Manual management impossible
- **90-day validity**: Short lifespans require automation
- **Certificate transparency**: All certs publicly logged
- **Browser warnings**: Lost revenue, trust erosion
- **Compliance**: PCI DSS, HIPAA, SOC 2 require TLS

---

## Skill Purpose and Scope

### What This Skill Covers

**Core TLS Operations:**
1. **Certificate Generation**
   - Self-signed certificates (development)
   - Certificate Signing Requests (CSRs)
   - Certificate Authorities (internal CAs)
   - Wildcard vs single-domain certificates

2. **Automation & Lifecycle**
   - Let's Encrypt with ACME protocol
   - cert-manager for Kubernetes
   - Automatic renewal strategies
   - Certificate rotation patterns

3. **mTLS (Mutual TLS)**
   - Service-to-service authentication
   - Client certificate verification
   - Certificate-based RBAC
   - Service mesh integration

4. **TLS Configuration**
   - TLS 1.3 cipher suites
   - Protocol version selection
   - OCSP stapling
   - Certificate transparency

5. **Debugging & Troubleshooting**
   - openssl s_client debugging
   - Certificate chain validation
   - Common TLS errors
   - Monitoring certificate expiry

### What This Skill Does NOT Cover

**Out of Scope (See Related Skills):**
- **security-architecture**: Holistic security design, threat modeling
- **auth-security**: Application-level authentication (OAuth, OIDC, JWT)
- **secret-management**: Storing private keys, HSM integration
- **configuring-nginx**: Full web server TLS configuration
- **load-balancing-patterns**: TLS termination at load balancers
- **kubernetes-operations**: Kubernetes cluster TLS configuration

**Boundary Clarifications:**
- This skill focuses on **TLS certificate operations** (generation, automation, debugging)
- For **storing private keys securely**, see `secret-management`
- For **TLS as part of API design**, see `api-patterns`
- For **service mesh mTLS**, see integration patterns but detailed config elsewhere

---

## Research Findings

### Google Search Grounding Results (December 2025)

#### Query 1: "TLS 1.3 configuration best practices 2025"

**Key Findings:**

**1. Protocol and Cipher Suites:**
- **Enable TLS 1.3 and 1.2 only**: Disable SSLv3, TLS 1.0, TLS 1.1
- **Strong cipher suites**: AES-GCM, ChaCha20-Poly1305
- **Perfect Forward Secrecy (PFS)**: Ephemeral key exchanges mandatory
- **Disable weak ciphers**: RC4, DES, 3DES, AES-CBC, SHA-1, RSA key transport

**2. Certificate Management:**
- **Automated certificate lifecycle**: Issuance, renewal, revocation
- **Short certificate lifetimes**: 90 days maximum (Let's Encrypt standard)
- **Trusted Certificate Authorities**: Publicly trusted CAs or internal PKI
- **OCSP Stapling**: Improves performance, enhances privacy

**3. Security Best Practices:**
- **Regular updates**: Keep TLS libraries current (OpenSSL, BoringSSL)
- **Secure Renegotiation Protocol (SRP)**: Prevent downgrade attacks
- **HSTS (HTTP Strict Transport Security)**: Force HTTPS connections
- **Disable TLS compression**: Prevents CRIME attacks

**4. TLS 1.3 Specific:**
- **Encrypted handshake**: More of the handshake is encrypted
- **0-RTT mode**: Use with caution (replay attack risks)
- **Encrypted SNI (ESNI)**: Additional privacy (emerging standard)

**5. Monitoring and Compliance:**
- **Certificate transparency**: All public certs logged
- **Automated monitoring**: Track expiry, revocations
- **Vulnerability scanning**: Tools like SSL Labs
- **Post-quantum preparation**: Monitor quantum-resistant algorithm adoption

**Sources:**
- zenarmor.com: TLS 1.3 best practices
- securityboulevard.com: Enterprise TLS configuration
- NIST: Cryptographic standards and guidelines
- trustico.com: Certificate lifecycle management

#### Query 2: "Let's Encrypt cert-manager Kubernetes automation 2025"

**Key Components:**

**1. Let's Encrypt:**
- Free, automated Certificate Authority
- ACME protocol for automation
- 90-day certificate validity
- Rate limits: 50 certs/week per registered domain

**2. cert-manager:**
- Kubernetes native certificate management
- Automates certificate issuance and renewal
- Supports multiple issuers (Let's Encrypt, Vault, self-signed)
- Integrates with Ingress controllers

**3. Workflow:**
```
1. Install cert-manager (Helm recommended)
2. Create ClusterIssuer (Let's Encrypt config)
3. Define Ingress with TLS annotation
4. cert-manager creates Certificate resource
5. ACME challenge solved (HTTP-01 or DNS-01)
6. Certificate stored in Kubernetes Secret
7. Automatic renewal before expiry
```

**4. Challenge Types:**
- **HTTP-01**: Temporary web server serves token (port 80)
- **DNS-01**: TXT record proves domain control (supports wildcards)

**5. Best Practices:**
- Use staging environment for testing (avoid rate limits)
- Monitor Certificate resources for errors
- Configure DNS properly for domain validation
- Use ClusterIssuer for cluster-wide certificates

**Sources:**
- cert-manager.io: Official documentation
- dev.to, medium.com: Kubernetes TLS tutorials
- funkysi1701.com: Production deployment guides

#### Query 3: "mTLS mutual TLS implementation patterns microservices"

**Note:** This query encountered errors (ExceptionGroup), but general mTLS patterns are well-established:

**Mutual TLS (mTLS) Patterns:**

**1. What is mTLS:**
- Both client and server present certificates
- Bidirectional authentication
- Zero-trust network security
- Common in service meshes (Istio, Linkerd, Consul)

**2. Use Cases:**
- Service-to-service authentication (microservices)
- API security (client certificate validation)
- Database connections (PostgreSQL, MySQL with client certs)
- IoT device authentication

**3. Implementation Patterns:**
- **Service Mesh**: Automatic mTLS (sidecar proxies)
- **Manual**: Application-level certificate validation
- **API Gateway**: Terminate mTLS at gateway
- **Zero Trust**: Every connection requires mTLS

**4. Certificate Distribution:**
- **Centralized CA**: Internal CA issues all certs
- **SPIFFE/SPIRE**: Workload identity framework
- **cert-manager**: Kubernetes-native distribution
- **Vault PKI**: Dynamic certificate issuance

### Context7 Research Results

#### cert-manager (Kubernetes Certificate Management)

**Library:** `/cert-manager/cert-manager`
**Trust Score:** High (75.7/100)
**Code Snippets:** 151
**Source Reputation:** High

**Key Features:**
- Adds certificates as Kubernetes CRDs (Custom Resource Definitions)
- Supports multiple issuers: Let's Encrypt, Vault, Venafi, self-signed
- Automatic renewal before expiry
- Integration with Ingress annotations
- CA injection for webhooks and APIServices
- Keystore outputs (JKS, PKCS12) for Java applications

**Architecture:**
```
cert-manager Controller
  ├── Certificate CRD (desired state)
  ├── Issuer/ClusterIssuer (CA configuration)
  ├── CertificateRequest (internal tracking)
  └── Secret (certificate storage)

Supported Issuers:
  ├── ACME (Let's Encrypt, ZeroSSL)
  ├── CA (internal CA with key pair)
  ├── Vault (HashiCorp Vault PKI)
  ├── Venafi (enterprise PKI)
  └── SelfSigned (development)
```

**Installation:**
```bash
# Helm installation (recommended)
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0 \
  --set installCRDs=true
```

**Example: Let's Encrypt with HTTP-01:**
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
    - http01:
        ingress:
          class: nginx
```

#### CFSSL (CloudFlare PKI Toolkit)

**Library:** `/cloudflare/cfssl`
**Trust Score:** High
**Code Snippets:** 245
**Source Reputation:** High

**Key Features:**
- Command-line tool and HTTP API server
- Certificate signing, verification, bundling
- Internal CA operations
- JSON-based configuration
- Suitable for automation and scripting

**Core Commands:**
```bash
# Generate self-signed CA
cfssl genkey -initca csr.json | cfssljson -bare ca

# Generate certificate from CA
cfssl gencert -ca ca.pem -ca-key ca-key.pem \
  -config config.json -profile server \
  server.json | cfssljson -bare server

# Generate client certificate
cfssl gencert -ca ca.pem -ca-key ca-key.pem \
  -config config.json -profile client \
  client.json | cfssljson -bare client
```

**Use Cases:**
- Internal PKI for development/testing
- Microservice mTLS certificate generation
- Automated certificate pipelines
- Custom CA operations

#### Certbot (Let's Encrypt Client)

**Library:** `/certbot/certbot`
**Trust Score:** High
**Code Snippets:** 278
**Source Reputation:** High

**Key Features:**
- Official Let's Encrypt client (EFF maintained)
- ACME protocol implementation
- Automatic renewal via cron/systemd timers
- Plugin system (nginx, apache, DNS providers)
- Manual mode for custom setups

**Basic Usage:**
```bash
# Obtain certificate (standalone mode)
certbot certonly --standalone -d example.com -d www.example.com

# Obtain with webroot (no service interruption)
certbot certonly --webroot -w /var/www/html -d example.com

# Renew all certificates
certbot renew

# Test renewal (dry run)
certbot renew --dry-run
```

**Automatic Renewal:**
```bash
# Cron job (twice daily)
0 0,12 * * * certbot renew -q

# Systemd timer (systemctl status certbot.timer)
# Usually installed automatically on modern systems
```

**DNS Challenge (wildcard support):**
```bash
certbot certonly --manual --preferred-challenges dns \
  -d example.com -d *.example.com
```

#### Other Notable Tools

**OpenSSL:**
- Universal TLS toolkit (already known by Claude)
- Certificate generation, signing, verification
- Debugging with `s_client` and `x509`
- Widely available on all Unix systems

**mkcert:**
- Developer-friendly local CA
- Automatically trusts certificates in browser/system
- Perfect for local development
- Simple CLI: `mkcert example.com localhost`

**smallstep certificates:**
**Library:** `/smallstep/certificates`
**Benchmark Score:** 61.3/100
**Code Snippets:** 74

- Online certificate authority for DevOps
- ACME protocol support
- SSH certificate issuance
- Automated certificate management

**CertMagic (Go library):**
**Library:** `/caddyserver/certmagic`
**Trust Score:** High (91.6/100)
**Code Snippets:** 34

- Go library for automatic HTTPS
- Used by Caddy web server
- One-line HTTPS servers
- Automatic certificate issuance and renewal

---

## TLS Implementation Taxonomy

### Certificate Types

**1. Self-Signed Certificates**
- **Use Case**: Development, testing, internal services
- **Pros**: Instant generation, no CA dependency, free
- **Cons**: Browser warnings, no chain of trust, manual distribution
- **Tools**: openssl, cfssl, mkcert
- **Validity**: Any duration (typically 1-10 years for internal)

**2. CA-Signed Certificates (Public)**
- **Use Case**: Production websites, public APIs, customer-facing services
- **Pros**: Browser trust, no warnings, industry standard
- **Cons**: Cost (commercial CAs), manual renewal (traditional CAs)
- **Providers**: Let's Encrypt (free), DigiCert, GlobalSign, Sectigo
- **Validity**: 90 days (Let's Encrypt) to 1 year (commercial CAs)

**3. CA-Signed Certificates (Internal)**
- **Use Case**: Internal services, microservices, corporate networks
- **Pros**: Full control, custom policies, no external dependency
- **Cons**: Manual trust distribution, CA management overhead
- **Tools**: CFSSL, HashiCorp Vault PKI, Smallstep CA
- **Validity**: Any duration (typically 1-5 years)

**4. Wildcard Certificates**
- **Use Case**: Multiple subdomains (*.example.com)
- **Pros**: Single cert for all subdomains, simplified management
- **Cons**: Higher risk if compromised, DNS-01 challenge required
- **Format**: `*.example.com` (covers sub.example.com, not sub.sub.example.com)
- **Providers**: Let's Encrypt (via DNS challenge), commercial CAs

**5. Client Certificates (mTLS)**
- **Use Case**: Service-to-service auth, API authentication, device identity
- **Pros**: Strong authentication, no passwords, mutual trust
- **Cons**: Certificate distribution complexity, revocation challenges
- **Tools**: CFSSL, Vault PKI, cert-manager
- **Validity**: Short-lived (hours to days) for high security

### Certificate Formats

```
Format Landscape:
├── PEM (Privacy-Enhanced Mail) - Most common
│   ├── .pem, .crt, .cer, .key extensions
│   ├── Base64 encoded, ASCII text
│   ├── BEGIN/END delimiters
│   └── Used by: Apache, Nginx, most Unix tools
│
├── DER (Distinguished Encoding Rules) - Binary
│   ├── .der, .cer extensions
│   ├── Binary format
│   └── Used by: Java, Windows, some legacy systems
│
├── PKCS#12 / PFX - Container format
│   ├── .p12, .pfx extensions
│   ├── Contains certificate + private key (password protected)
│   └── Used by: Windows, Java keystores, browsers
│
└── JKS (Java KeyStore)
    ├── .jks extension
    ├── Java-specific format
    └── Used by: Java applications, Tomcat, JBoss
```

**Conversion Examples:**
```bash
# PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# PEM to PKCS#12
openssl pkcs12 -export -out cert.p12 -inkey key.pem -in cert.pem

# PKCS#12 to PEM
openssl pkcs12 -in cert.p12 -out cert.pem -nodes
```

### TLS 1.3 Cipher Suites (Recommended 2025)

**Supported in TLS 1.3 (5 cipher suites only):**
```
TLS_AES_256_GCM_SHA384           - AES-256 with GCM (AEAD)
TLS_CHACHA20_POLY1305_SHA256     - ChaCha20-Poly1305 (mobile-optimized)
TLS_AES_128_GCM_SHA256           - AES-128 with GCM (performance)
TLS_AES_128_CCM_SHA256           - AES-128 with CCM (constrained devices)
TLS_AES_128_CCM_8_SHA256         - AES-128 with CCM-8 (IoT)
```

**Configuration Strategy:**
1. **Default order**: Let client choose (modern clients prefer ChaCha20 on mobile)
2. **Server preference**: Enable if you want to enforce cipher order
3. **Minimum**: Support at least TLS_AES_256_GCM_SHA384 and TLS_CHACHA20_POLY1305_SHA256

**TLS 1.2 Cipher Suites (Fallback):**
```
# Recommended for TLS 1.2 compatibility
ECDHE-RSA-AES256-GCM-SHA384
ECDHE-RSA-AES128-GCM-SHA256
ECDHE-RSA-CHACHA20-POLY1305
```

**What to Disable:**
- All SSLv3, TLS 1.0, TLS 1.1
- RC4, DES, 3DES ciphers
- MD5, SHA-1 hashing
- CBC mode ciphers (BEAST, Lucky13 attacks)
- Export ciphers
- Anonymous ciphers (aNULL)
- RSA key transport (no PFS)

---

## Decision Framework

### Certificate Type Selection

```
Start: Need TLS certificate

Question 1: Public-facing or internal?
├─ Public-facing (internet users)
│  └─> Question 2: Single domain or multiple subdomains?
│     ├─ Single domain (example.com, www.example.com)
│     │  └─> Let's Encrypt (certbot or cert-manager)
│     │      HTTP-01 challenge, free, automated
│     │
│     └─ Multiple subdomains (*.example.com)
│        └─> Let's Encrypt with DNS-01 challenge
│            Wildcard cert, requires DNS API access
│
└─ Internal (corporate network, microservices)
   └─> Question 3: Development or production?
      ├─ Development (local testing)
      │  └─> mkcert or self-signed (openssl)
      │      Fast, no external dependency
      │
      └─ Production (internal services)
         └─> Question 4: Scale and automation?
            ├─ Small scale (<10 services)
            │  └─> CFSSL or self-signed CA
            │      Manual but simple
            │
            └─ Large scale (100+ services)
               └─> HashiCorp Vault PKI or cert-manager
                   Automated, dynamic secrets, rotation
```

### Automation Tool Selection

```
Environment: Where are you deploying?

Kubernetes:
  └─> cert-manager (native CRDs, Ingress integration)
      Supports: Let's Encrypt, Vault, CA, self-signed
      Best for: Cloud-native applications

Traditional Servers (VMs, bare metal):
  ├─ Public certs: Certbot (Let's Encrypt)
  │  └─> Plugins: nginx, apache, standalone, DNS
  │
  └─ Internal certs: CFSSL or Vault PKI
     └─> API-driven, scriptable

Microservices (any platform):
  └─> HashiCorp Vault PKI
      Dynamic secrets, short-lived certs, revocation
      Best for: Service mesh, mTLS at scale

Developer Workstation:
  └─> mkcert (local development)
      Trusted by browser/system automatically
      Best for: Local HTTPS testing
```

### mTLS vs Standard TLS

```
Decision: Do services need to authenticate each other?

Standard TLS (server-only authentication):
  Use when:
  ├─ Public websites (users trust server)
  ├─ APIs with bearer tokens (separate auth layer)
  ├─ Services behind API gateway (gateway handles auth)
  └─ Simple architectures (< 5 services)

  Benefits:
  ├─ Simpler configuration
  ├─ Standard browser/client support
  └─ Lower operational overhead

Mutual TLS (client + server authentication):
  Use when:
  ├─ Service-to-service (microservices, zero-trust)
  ├─ High security requirements (financial, healthcare)
  ├─ Machine-to-machine (APIs, IoT devices)
  └─ No shared network trust (public internet)

  Benefits:
  ├─ Strong authentication (certificate-based)
  ├─ No passwords to manage
  ├─ Works well with service mesh
  └─ Network-level authorization

  Challenges:
  ├─ Certificate distribution complexity
  ├─ Revocation and rotation at scale
  ├─ Client configuration required
  └─ Debugging complexity
```

---

## Certificate Generation Examples

### 1. Self-Signed Certificate (OpenSSL)

**Quick single-line generation:**
```bash
# Generate self-signed cert + key (valid 365 days)
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout server-key.pem -out server-cert.pem \
  -days 365 -subj "/CN=example.com"
```

**Production-quality self-signed with SAN (Subject Alternative Names):**
```bash
# Step 1: Create OpenSSL config with SANs
cat > san.cnf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C = US
ST = California
L = San Francisco
O = Example Corp
OU = IT Department
CN = example.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com
DNS.2 = www.example.com
DNS.3 = api.example.com
IP.1 = 192.168.1.100
EOF

# Step 2: Generate private key
openssl genrsa -out server-key.pem 2048

# Step 3: Generate certificate signing request (CSR)
openssl req -new -key server-key.pem -out server.csr -config san.cnf

# Step 4: Self-sign the certificate (365 days)
openssl x509 -req -in server.csr -signkey server-key.pem \
  -out server-cert.pem -days 365 -extensions v3_req -extfile san.cnf

# Verify SANs
openssl x509 -in server-cert.pem -noout -text | grep -A 3 "Subject Alternative Name"
```

### 2. Internal CA with CFSSL

**Step 1: Install CFSSL**
```bash
# Linux/macOS
curl -L https://github.com/cloudflare/cfssl/releases/download/v1.6.4/cfssl_1.6.4_linux_amd64 -o /usr/local/bin/cfssl
curl -L https://github.com/cloudflare/cfssl/releases/download/v1.6.4/cfssljson_1.6.4_linux_amd64 -o /usr/local/bin/cfssljson
chmod +x /usr/local/bin/cfssl /usr/local/bin/cfssljson

# Or via package manager
# Ubuntu: apt install golang-cfssl
# macOS: brew install cfssl
```

**Step 2: Create CA configuration**
```bash
# ca-config.json - Signing profiles
cat > ca-config.json <<EOF
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "server": {
        "expiry": "8760h",
        "usages": [
          "signing",
          "key encipherment",
          "server auth"
        ]
      },
      "client": {
        "expiry": "8760h",
        "usages": [
          "signing",
          "key encipherment",
          "client auth"
        ]
      },
      "peer": {
        "expiry": "8760h",
        "usages": [
          "signing",
          "key encipherment",
          "server auth",
          "client auth"
        ]
      }
    }
  }
}
EOF

# ca-csr.json - CA certificate request
cat > ca-csr.json <<EOF
{
  "CN": "Example Corp Internal CA",
  "key": {
    "algo": "rsa",
    "size": 4096
  },
  "names": [
    {
      "C": "US",
      "ST": "California",
      "L": "San Francisco",
      "O": "Example Corp",
      "OU": "IT Security"
    }
  ],
  "ca": {
    "expiry": "87600h"
  }
}
EOF
```

**Step 3: Generate CA certificate**
```bash
cfssl genkey -initca ca-csr.json | cfssljson -bare ca
# Produces: ca.pem (cert), ca-key.pem (private key), ca.csr
```

**Step 4: Generate server certificate**
```bash
# server-csr.json
cat > server-csr.json <<EOF
{
  "CN": "api.example.com",
  "hosts": [
    "api.example.com",
    "api.internal.example.com",
    "192.168.1.100"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "ST": "California",
      "L": "San Francisco",
      "O": "Example Corp",
      "OU": "Engineering"
    }
  ]
}
EOF

# Generate and sign server certificate
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=server \
  server-csr.json | cfssljson -bare server

# Produces: server.pem (cert), server-key.pem (private key)
```

**Step 5: Generate client certificate (for mTLS)**
```bash
# client-csr.json
cat > client-csr.json <<EOF
{
  "CN": "client.example.com",
  "hosts": [""],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "ST": "California",
      "O": "Example Corp",
      "OU": "Engineering"
    }
  ]
}
EOF

# Generate and sign client certificate
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=client \
  client-csr.json | cfssljson -bare client
```

### 3. Local Development with mkcert

**Install mkcert:**
```bash
# macOS
brew install mkcert
brew install nss  # For Firefox support

# Linux (Debian/Ubuntu)
sudo apt install libnss3-tools
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64
sudo mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert
sudo chmod +x /usr/local/bin/mkcert
```

**Generate trusted local certificates:**
```bash
# Install local CA in system trust store
mkcert -install

# Generate certificate for local domains
mkcert example.com "*.example.com" localhost 127.0.0.1 ::1

# Produces: example.com+4.pem (cert) and example.com+4-key.pem (key)
# Already trusted by browser and system!
```

---

## Automation Patterns

### 1. Let's Encrypt with Certbot (Traditional Servers)

**Installation:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot

# RHEL/CentOS
sudo yum install certbot

# macOS
brew install certbot
```

**Standalone Mode (Port 80 must be free):**
```bash
# Obtain certificate
sudo certbot certonly --standalone \
  -d example.com \
  -d www.example.com \
  --email admin@example.com \
  --agree-tos

# Certificates saved to:
# /etc/letsencrypt/live/example.com/fullchain.pem
# /etc/letsencrypt/live/example.com/privkey.pem
```

**Webroot Mode (No service interruption):**
```bash
# Obtain certificate (service keeps running)
sudo certbot certonly --webroot \
  -w /var/www/html \
  -d example.com \
  -d www.example.com \
  --email admin@example.com \
  --agree-tos
```

**Nginx Plugin (Automatic configuration):**
```bash
# Obtain certificate AND configure nginx
sudo certbot --nginx -d example.com -d www.example.com
```

**DNS Challenge (Wildcard certificates):**
```bash
# Manual DNS challenge
sudo certbot certonly --manual \
  --preferred-challenges dns \
  -d example.com \
  -d "*.example.com"

# Follow prompts to add TXT record to DNS
# Verify: dig _acme-challenge.example.com TXT
```

**Automatic Renewal Setup:**
```bash
# Test renewal (dry run)
sudo certbot renew --dry-run

# Cron job (automatically installed by certbot package)
# /etc/cron.d/certbot:
0 */12 * * * root certbot renew --quiet

# Systemd timer (modern systems)
systemctl status certbot.timer
systemctl enable certbot.timer
```

### 2. cert-manager in Kubernetes

**Installation via Helm:**
```bash
# Add Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager (includes CRDs)
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0 \
  --set installCRDs=true

# Verify installation
kubectl get pods -n cert-manager
kubectl get crd | grep cert-manager
```

**Create ClusterIssuer (Let's Encrypt):**
```yaml
# letsencrypt-prod.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # Production server (rate limited!)
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com

    # Secret to store ACME account key
    privateKeySecretRef:
      name: letsencrypt-prod-account-key

    # HTTP-01 challenge solver
    solvers:
    - http01:
        ingress:
          class: nginx

---
# letsencrypt-staging.yaml (for testing)
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-staging-account-key
    solvers:
    - http01:
        ingress:
          class: nginx
```

**Apply ClusterIssuer:**
```bash
kubectl apply -f letsencrypt-prod.yaml
kubectl apply -f letsencrypt-staging.yaml

# Verify
kubectl get clusterissuer
```

**Ingress with Automatic Certificate:**
```yaml
# ingress-tls.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  namespace: production
  annotations:
    # Enable cert-manager
    cert-manager.io/cluster-issuer: "letsencrypt-prod"

    # Ingress controller annotations
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - example.com
    - www.example.com
    # Secret will be created automatically by cert-manager
    secretName: example-com-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

**Manual Certificate Resource:**
```yaml
# certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-com-cert
  namespace: production
spec:
  secretName: example-com-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - example.com
  - www.example.com
  duration: 2160h  # 90 days
  renewBefore: 720h  # 30 days before expiry
```

**Monitor Certificates:**
```bash
# Check certificate status
kubectl get certificate -A
kubectl describe certificate example-com-cert -n production

# Check certificate request
kubectl get certificaterequest -A

# Check issued secret
kubectl get secret example-com-tls -n production -o yaml
```

### 3. HashiCorp Vault PKI (Dynamic Certificates)

**Enable PKI secrets engine:**
```bash
# Enable PKI at pki/
vault secrets enable pki

# Set max TTL to 10 years
vault secrets tune -max-lease-ttl=87600h pki
```

**Generate root CA:**
```bash
# Generate internal root CA
vault write pki/root/generate/internal \
  common_name="Example Corp Root CA" \
  ttl=87600h

# Configure CA and CRL URLs
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com:8200/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"
```

**Create role for certificate issuance:**
```bash
# Create role for web servers
vault write pki/roles/example-dot-com \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl="720h" \
  key_usage="DigitalSignature,KeyEncipherment" \
  ext_key_usage="ServerAuth"
```

**Issue certificate:**
```bash
# Request certificate for api.example.com
vault write pki/issue/example-dot-com \
  common_name="api.example.com" \
  ttl="24h"

# Returns: certificate, private_key, ca_chain, serial_number
```

**Vault Agent for Automatic Renewal:**
```hcl
# vault-agent.hcl
auto_auth {
  method "kubernetes" {
    mount_path = "auth/kubernetes"
    config = {
      role = "web-service"
    }
  }
}

template {
  source      = "/etc/vault/cert.tpl"
  destination = "/etc/ssl/certs/server.crt"
  command     = "systemctl reload nginx"
}

template {
  source      = "/etc/vault/key.tpl"
  destination = "/etc/ssl/private/server.key"
  command     = "systemctl reload nginx"
}
```

---

## mTLS Patterns

### What is Mutual TLS (mTLS)?

**Standard TLS (Server Authentication):**
```
Client                    Server
  |                         |
  |--- ClientHello -------->|
  |<-- ServerHello ---------|
  |<-- Certificate ---------|  (Server proves identity)
  |<-- ServerHelloDone -----|
  |                         |
  |--- ClientKeyExchange -->|
  |--- ChangeCipherSpec --->|
  |--- Finished ----------->|
  |<-- ChangeCipherSpec ----|
  |<-- Finished ------------|
  |                         |
  |=== Encrypted Data =====>|
```

**Mutual TLS (Both Authenticate):**
```
Client                    Server
  |                         |
  |--- ClientHello -------->|
  |<-- ServerHello ---------|
  |<-- Certificate ---------|  (Server proves identity)
  |<-- CertificateRequest --|  (Server requests client cert)
  |<-- ServerHelloDone -----|
  |                         |
  |--- Certificate -------->|  (Client proves identity)
  |--- ClientKeyExchange -->|
  |--- CertificateVerify -->|  (Client signs with private key)
  |--- ChangeCipherSpec --->|
  |--- Finished ----------->|
  |<-- ChangeCipherSpec ----|
  |<-- Finished ------------|
  |                         |
  |=== Encrypted Data =====>|
```

### mTLS Use Cases

**1. Service-to-Service Authentication (Microservices)**
```
API Gateway ←--mTLS--→ User Service ←--mTLS--→ Database Service
                         ↑
                       mTLS
                         ↓
                    Order Service
```

**Benefits:**
- No shared secrets or passwords
- Network-level authentication
- Works with service mesh (Istio, Linkerd)
- Certificate-based authorization

**2. API Authentication (Machine-to-Machine)**
```
External Partner ←--mTLS--→ API Gateway ←--→ Internal Services
```

**Benefits:**
- Stronger than API keys
- Non-repudiation (audit trail)
- Automatic rotation via short-lived certs

**3. Zero-Trust Networks**
```
All services require mTLS, even on internal network
└─> Assumes network is hostile (defense in depth)
```

### Implementing mTLS with Nginx

**Server Configuration (Require Client Certificates):**
```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    # Server certificate
    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;

    # CA certificate to verify client certs
    ssl_client_certificate /etc/ssl/certs/ca.crt;

    # Require client certificate
    ssl_verify_client on;

    # Certificate verification depth
    ssl_verify_depth 2;

    # TLS 1.3 only
    ssl_protocols TLSv1.3;

    location / {
        proxy_pass http://backend;

        # Pass client cert info to backend
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;
        proxy_set_header X-SSL-Client-S-DN $ssl_client_s_dn;
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;
    }
}
```

**Optional Client Certificate (Fallback to Other Auth):**
```nginx
# Make client cert optional
ssl_verify_client optional;

location / {
    # Allow if client cert is valid OR has valid API key
    if ($ssl_client_verify != "SUCCESS") {
        set $auth_required "1";
    }
    if ($http_x_api_key = "") {
        set $auth_required "${auth_required}1";
    }
    if ($auth_required = "11") {
        return 401;
    }

    proxy_pass http://backend;
}
```

### mTLS with curl (Client Side)

**Basic mTLS request:**
```bash
curl https://api.example.com/endpoint \
  --cert client.crt \
  --key client.key \
  --cacert ca.crt

# Or with PKCS#12
curl https://api.example.com/endpoint \
  --cert-type P12 \
  --cert client.p12:password
```

**Verify server certificate only:**
```bash
curl https://api.example.com/endpoint \
  --cacert ca.crt
```

**Skip certificate verification (INSECURE - testing only):**
```bash
curl https://api.example.com/endpoint \
  --insecure  # or -k
```

### mTLS Certificate Distribution Patterns

**Pattern 1: Manual Distribution (Small Scale)**
```
1. Generate CA certificate
2. Distribute CA to all services (trust store)
3. Generate client/server certs from CA
4. Manually deploy certs to each service
5. Configure services to use certs
```

**Pattern 2: cert-manager (Kubernetes)**
```yaml
# CA certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: internal-ca
spec:
  isCA: true
  commonName: Internal CA
  secretName: internal-ca-key-pair
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer

---
# Service certificate (automatic)
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: service-cert
spec:
  secretName: service-tls
  issuerRef:
    name: internal-ca
    kind: Issuer
  dnsNames:
  - service.namespace.svc.cluster.local
  usages:
  - server auth
  - client auth
```

**Pattern 3: Vault PKI (Dynamic, Short-Lived)**
```bash
# Service requests cert from Vault on startup
vault write pki/issue/service-role \
  common_name="service.internal" \
  ttl="24h"

# Vault Agent auto-renews before expiry
# Service reloads cert without restart
```

**Pattern 4: Service Mesh (Istio/Linkerd)**
```
Sidecar proxy handles mTLS automatically:
├─ Certificates issued by mesh CA
├─ Automatic rotation (short TTL)
├─ Transparent to application code
└─ Policy-based (which services can talk)
```

---

## Debugging Guide

### Essential TLS Debugging Commands

**1. Test TLS Connection (OpenSSL s_client)**
```bash
# Basic connection test
openssl s_client -connect example.com:443

# Show certificate chain
openssl s_client -connect example.com:443 -showcerts

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_3

# Test with SNI (Server Name Indication)
openssl s_client -connect example.com:443 -servername example.com

# Test mTLS (client certificate)
openssl s_client -connect api.example.com:443 \
  -cert client.crt -key client.key -CAfile ca.crt

# Save server certificate
openssl s_client -connect example.com:443 </dev/null 2>/dev/null | \
  openssl x509 -out server.crt
```

**Key Output Indicators:**
```
Verify return code: 0 (ok)              # Certificate valid
Verify return code: 20 (unable to get   # CA certificate not trusted
  local issuer certificate)
Verify return code: 10 (certificate     # Certificate expired
  has expired)
```

**2. Examine Certificate Details**
```bash
# View certificate contents
openssl x509 -in cert.pem -noout -text

# Check expiration date
openssl x509 -in cert.pem -noout -dates
# Output: notBefore=..., notAfter=...

# Check certificate subject
openssl x509 -in cert.pem -noout -subject

# Check certificate issuer
openssl x509 -in cert.pem -noout -issuer

# Check Subject Alternative Names (SANs)
openssl x509 -in cert.pem -noout -text | grep -A 1 "Subject Alternative Name"

# Check certificate fingerprint
openssl x509 -in cert.pem -noout -fingerprint -sha256

# Verify certificate chain
openssl verify -CAfile ca.crt cert.pem
```

**3. Verify Private Key and Certificate Match**
```bash
# Check certificate modulus
openssl x509 -in cert.pem -noout -modulus | md5sum

# Check private key modulus
openssl rsa -in key.pem -noout -modulus | md5sum

# If MD5 hashes match, cert and key are a pair
```

**4. Test with curl**
```bash
# Verbose TLS handshake
curl -v https://example.com

# Show TLS handshake details
curl -vvv https://example.com 2>&1 | grep -E "SSL|TLS"

# Test with specific CA
curl --cacert ca.crt https://example.com

# Test mTLS
curl --cert client.crt --key client.key --cacert ca.crt https://api.example.com

# Ignore certificate errors (testing only)
curl -k https://example.com
```

### Common TLS Errors and Solutions

**Error 1: "certificate has expired"**
```
Cause: Certificate validity period has passed
Solution:
- Renew certificate (certbot renew or cert-manager auto-renewal)
- Check system clock (ntpdate or chrony)
- Verify certificate dates: openssl x509 -in cert.pem -noout -dates
```

**Error 2: "unable to get local issuer certificate"**
```
Cause: CA certificate not in trust store
Solution:
- Add CA to system trust store:
  # Ubuntu/Debian
  sudo cp ca.crt /usr/local/share/ca-certificates/
  sudo update-ca-certificates

  # RHEL/CentOS
  sudo cp ca.crt /etc/pki/ca-trust/source/anchors/
  sudo update-ca-trust

- Or specify CA in application:
  curl --cacert ca.crt https://example.com
  openssl s_client -CAfile ca.crt -connect example.com:443
```

**Error 3: "certificate verify failed: Hostname mismatch"**
```
Cause: Certificate CN/SAN doesn't match requested hostname
Solution:
- Generate new certificate with correct hostname in SAN
- Check SANs: openssl x509 -in cert.pem -noout -text | grep -A 1 "Subject Alternative Name"
- Ensure SNI is sent: curl --resolve example.com:443:192.168.1.100 https://example.com
```

**Error 4: "SSL handshake failed: sslv3 alert handshake failure"**
```
Cause: TLS version or cipher suite mismatch
Solution:
- Check supported TLS versions on server
- Update client to support TLS 1.2+ (disable TLS 1.0/1.1)
- Check cipher suites: openssl s_client -connect example.com:443 -cipher 'ECDHE-RSA-AES256-GCM-SHA384'
- Enable compatible cipher suites on server
```

**Error 5: "certificate signed by unknown authority"**
```
Cause: Intermediate certificates missing from chain
Solution:
- Include full certificate chain in server config
- Verify chain: openssl s_client -connect example.com:443 -showcerts
- Build chain file: cat cert.pem intermediate.pem > fullchain.pem
```

### TLS Monitoring and Alerting

**Check Certificate Expiry:**
```bash
# Check expiry date
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Check days until expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -checkend 2592000
# Exit code 0: valid for 30+ days, 1: expires within 30 days

# Script to check multiple domains
cat domains.txt | while read domain; do
  expiry=$(echo | openssl s_client -connect $domain:443 2>/dev/null | \
    openssl x509 -noout -enddate | cut -d= -f2)
  echo "$domain: $expiry"
done
```

**Prometheus Exporter (blackbox_exporter):**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'ssl_expiry'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - https://example.com
        - https://api.example.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115

# Alert when certificate expires in < 7 days
groups:
  - name: ssl_expiry
    rules:
    - alert: SSLCertExpiring
      expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7
      for: 1h
      annotations:
        summary: "SSL certificate expiring soon: {{ $labels.instance }}"
```

---

## Tool Recommendations

### Primary Tools (Production)

**1. cert-manager (Kubernetes)**
- **Use Case**: Kubernetes native certificate management
- **Trust Score**: High (75.7/100)
- **Installation**: Helm chart
- **Best For**: Cloud-native applications, automated renewal
- **Supported Issuers**: Let's Encrypt, Vault, Venafi, CA, self-signed
- **Official Docs**: https://cert-manager.io/docs/

**2. Certbot (Traditional Servers)**
- **Use Case**: Let's Encrypt on VMs/bare metal
- **Trust Score**: High (278 code snippets)
- **Installation**: Package manager (apt, yum, brew)
- **Best For**: LAMP/LEMP stacks, Apache, Nginx
- **Plugins**: nginx, apache, standalone, DNS (50+ providers)
- **Official Docs**: https://certbot.eff.org/docs/

**3. HashiCorp Vault PKI**
- **Use Case**: Dynamic certificates, internal PKI, mTLS
- **Trust Score**: High
- **Best For**: Microservices, short-lived certs, service mesh
- **Features**: Automatic renewal, policy-based access, audit logs
- **Official Docs**: https://developer.hashicorp.com/vault/docs/secrets/pki

### Development Tools

**1. mkcert**
- **Use Case**: Local HTTPS development
- **Installation**: brew install mkcert (macOS), apt install (Linux)
- **Best For**: Trusted local certificates, no browser warnings
- **Platforms**: macOS, Linux, Windows
- **GitHub**: https://github.com/FiloSottile/mkcert

**2. OpenSSL**
- **Use Case**: Universal TLS toolkit (already available)
- **Best For**: Manual operations, debugging, testing
- **Commands**: genrsa, req, x509, s_client, verify

### Internal PKI Tools

**1. CFSSL (CloudFlare)**
- **Library**: /cloudflare/cfssl
- **Trust Score**: High (245 code snippets)
- **Use Case**: Internal CA operations, automation
- **Best For**: Scripting, API-driven certificate issuance
- **GitHub**: https://github.com/cloudflare/cfssl

**2. Smallstep Certificates**
- **Library**: /smallstep/certificates
- **Benchmark Score**: 61.3/100
- **Use Case**: Online CA for DevOps, ACME server
- **Best For**: Internal ACME, SSH certificates
- **GitHub**: https://github.com/smallstep/certificates

### Tool Selection Matrix

| Use Case | Environment | Recommended Tool | Alternative |
|----------|-------------|------------------|-------------|
| **Public HTTPS** | Kubernetes | cert-manager | External Secrets Operator |
| **Public HTTPS** | VMs/Bare Metal | Certbot | acme.sh |
| **Internal PKI** | Any | HashiCorp Vault | CFSSL, Smallstep |
| **mTLS (K8s)** | Kubernetes | cert-manager + Istio | Linkerd, Consul |
| **mTLS (VMs)** | Traditional | Vault PKI | CFSSL |
| **Local Dev** | Workstation | mkcert | Self-signed (OpenSSL) |
| **Debugging** | Any | OpenSSL s_client | curl -v |
| **Automation** | CI/CD | CFSSL API | Vault API |

---

## Skill Structure Design

### Proposed File Structure

```
implementing-tls/
├── SKILL.md                          # Main skill file (300-400 lines)
│   ├── Purpose and Scope
│   ├── When to Use This Skill
│   ├── Quick Start Guide
│   │   ├── Development (mkcert)
│   │   ├── Production (certbot or cert-manager)
│   │   └── Internal PKI (CFSSL)
│   ├── TLS 1.3 Configuration
│   ├── Decision Framework (cert type selection)
│   ├── Common Workflows
│   │   ├── Generate self-signed cert
│   │   ├── Setup Let's Encrypt
│   │   ├── Configure mTLS
│   │   └── Debug TLS issues
│   └── References to Detailed Guides
│
├── references/                       # Progressive disclosure
│   ├── certificate-generation.md    # Detailed generation examples
│   │   ├── OpenSSL recipes
│   │   ├── CFSSL workflows
│   │   ├── mkcert usage
│   │   └── SAN configuration
│   │
│   ├── automation-patterns.md       # Automation deep-dive
│   │   ├── Certbot setup and plugins
│   │   ├── cert-manager configuration
│   │   ├── Vault PKI integration
│   │   └── Renewal strategies
│   │
│   ├── mtls-guide.md               # mTLS implementation
│   │   ├── Architecture patterns
│   │   ├── Nginx configuration
│   │   ├── Certificate distribution
│   │   └── Service mesh integration
│   │
│   ├── debugging-tls.md            # Troubleshooting guide
│   │   ├── OpenSSL debugging commands
│   │   ├── Common errors and solutions
│   │   ├── Certificate validation
│   │   └── Monitoring expiry
│   │
│   └── tls13-best-practices.md    # TLS 1.3 configuration
│       ├── Protocol versions
│       ├── Cipher suite selection
│       ├── OCSP stapling
│       └── Performance tuning
│
├── examples/                        # Working examples
│   ├── self-signed/
│   │   ├── generate.sh
│   │   └── san.cnf
│   │
│   ├── cfssl-ca/
│   │   ├── setup-ca.sh
│   │   ├── ca-config.json
│   │   ├── ca-csr.json
│   │   ├── server-csr.json
│   │   └── client-csr.json
│   │
│   ├── certbot/
│   │   ├── standalone.sh
│   │   ├── webroot.sh
│   │   ├── dns-challenge.sh
│   │   └── renewal-hook.sh
│   │
│   ├── cert-manager/
│   │   ├── install.sh
│   │   ├── clusterissuer-letsencrypt.yaml
│   │   ├── clusterissuer-ca.yaml
│   │   ├── certificate.yaml
│   │   └── ingress-tls.yaml
│   │
│   ├── mtls-nginx/
│   │   ├── server.conf
│   │   ├── client-test.sh
│   │   └── README.md
│   │
│   └── vault-pki/
│       ├── setup-pki.sh
│       ├── issue-cert.sh
│       └── vault-agent.hcl
│
└── scripts/                         # Utility scripts (executable)
    ├── check-cert-expiry.sh        # Monitor certificate expiration
    ├── validate-chain.sh           # Verify certificate chain
    ├── test-tls-connection.sh      # Test TLS with various options
    └── convert-formats.sh          # Convert between PEM/DER/PKCS12
```

### SKILL.md Content Outline (300-400 lines)

```markdown
# Implementing TLS

## Purpose
[2-3 sentences: What this skill does]

## When to Use This Skill
[Specific trigger scenarios]

## Quick Start

### For Development (Local HTTPS)
[mkcert one-liner]

### For Production (Public HTTPS)
[certbot or cert-manager quick start]

### For Internal Services (Internal PKI)
[CFSSL quick start]

## TLS 1.3 Configuration Best Practices
[Protocol versions, cipher suites, security settings]

## Decision Framework
[Flowchart: Certificate type selection]

## Common Workflows

### Generate Self-Signed Certificate
[OpenSSL command with SANs]
[Reference: certificate-generation.md]

### Setup Let's Encrypt Automation
[Certbot or cert-manager basic config]
[Reference: automation-patterns.md]

### Configure mTLS
[Basic mTLS setup, client/server certs]
[Reference: mtls-guide.md]

### Debug TLS Issues
[Essential debugging commands]
[Reference: debugging-tls.md]

## Tool Selection Guide
[Table: Use case → Recommended tool]

## Certificate Lifecycle
[Generate → Deploy → Monitor → Renew → Rotate]

## References
- references/certificate-generation.md - Detailed generation examples
- references/automation-patterns.md - Automation deep-dive
- references/mtls-guide.md - mTLS implementation
- references/debugging-tls.md - Troubleshooting guide
- references/tls13-best-practices.md - TLS 1.3 configuration

## Examples
- examples/self-signed/ - Self-signed certificate generation
- examples/cfssl-ca/ - Internal CA setup
- examples/certbot/ - Let's Encrypt automation
- examples/cert-manager/ - Kubernetes certificate management
- examples/mtls-nginx/ - mTLS with Nginx
- examples/vault-pki/ - Vault PKI integration

## Scripts
- scripts/check-cert-expiry.sh - Monitor certificate expiration
- scripts/validate-chain.sh - Verify certificate chain
- scripts/test-tls-connection.sh - Test TLS connections
- scripts/convert-formats.sh - Convert certificate formats
```

### Progressive Disclosure Strategy

**Level 1: SKILL.md (Always Loaded)**
- Purpose and when to use
- Quick start guides (1-3 commands)
- Decision framework (visual)
- Common workflows (high-level)
- Tool selection guide
- References to detailed guides

**Level 2: references/ (Loaded on Demand)**
- certificate-generation.md: When user needs detailed generation
- automation-patterns.md: When setting up automation
- mtls-guide.md: When implementing mTLS
- debugging-tls.md: When troubleshooting
- tls13-best-practices.md: When configuring TLS 1.3

**Level 3: examples/ and scripts/ (Executed/Read as Needed)**
- examples/: Working code to copy/adapt
- scripts/: Utilities to run (zero tokens until executed)

---

## Integration Points

### Related Skills

**1. secret-management** (Store Private Keys)
```
implementing-tls generates certificates
  └─> secret-management stores private keys securely
      ├─ Vault KV for long-term storage
      ├─ Kubernetes Secrets with encryption at rest
      └─ HSM for high-security environments
```

**2. auth-security** (Combine TLS with Authentication)
```
implementing-tls provides transport security
  └─> auth-security handles application auth
      ├─ mTLS for machine-to-machine
      ├─ OAuth/OIDC for user authentication
      └─ JWT signing keys stored securely
```

**3. deploying-applications** (Inject Certificates)
```
implementing-tls generates certificates
  └─> deploying-applications injects at runtime
      ├─ Kubernetes: Mount Secrets as volumes
      ├─ Docker: Mount certs via volumes
      └─ VMs: Provision via configuration management
```

**4. load-balancing-patterns** (TLS Termination)
```
implementing-tls provides certificates
  └─> load-balancing-patterns terminates TLS
      ├─ Terminate at load balancer (offload)
      ├─ Pass through to backend (end-to-end)
      └─ Re-encrypt (terminate + re-establish)
```

**5. kubernetes-operations** (Cluster TLS)
```
implementing-tls focuses on application certs
  └─> kubernetes-operations handles cluster certs
      ├─ API server certificates
      ├─ etcd peer and client certificates
      └─ kubelet certificates
```

**6. observability** (Monitor Certificate Health)
```
implementing-tls provides debugging commands
  └─> observability monitors expiry and health
      ├─ Prometheus blackbox_exporter
      ├─ Grafana dashboards for cert expiry
      └─ Alertmanager notifications
```

**7. security-architecture** (Holistic Design)
```
security-architecture defines TLS requirements
  └─> implementing-tls implements those requirements
      ├─ TLS 1.3 mandatory (compliance)
      ├─ mTLS for zero-trust networks
      └─ Certificate rotation policies
```

### Workflow Examples

**Example 1: Deploying Secure Microservice**
```
1. security-architecture: Define mTLS requirement
2. implementing-tls: Generate CA and service certificates
3. secret-management: Store private keys in Vault
4. deploying-applications: Inject certs via Vault Agent
5. observability: Monitor certificate expiry
```

**Example 2: Setting Up Public HTTPS**
```
1. implementing-tls: Configure cert-manager with Let's Encrypt
2. deploying-applications: Deploy Ingress with TLS annotations
3. load-balancing-patterns: Configure Ingress controller
4. observability: Alert on certificate expiry < 7 days
```

**Example 3: Internal Service Communication**
```
1. implementing-tls: Setup internal CA with CFSSL
2. implementing-tls: Generate client/server certs (mTLS)
3. secret-management: Distribute certs via Kubernetes Secrets
4. auth-security: Configure service-to-service authorization
5. observability: Monitor TLS handshake failures
```

---

## Implementation Roadmap

### Phase 1: Core SKILL.md (Week 1)

**Deliverables:**
- [ ] SKILL.md frontmatter (name, description)
- [ ] Purpose and scope section
- [ ] Quick start guides (development, production, internal)
- [ ] Decision framework (visual flowchart)
- [ ] TLS 1.3 best practices summary
- [ ] Tool selection guide (table)
- [ ] References section (links to detailed guides)

**Token Budget:** ~2,000-2,500 tokens (150-200 lines)

### Phase 2: Reference Documents (Week 2)

**Deliverables:**
- [ ] references/certificate-generation.md
  - OpenSSL detailed recipes
  - CFSSL CA setup
  - mkcert usage
  - SAN configuration examples

- [ ] references/automation-patterns.md
  - Certbot complete guide (plugins, renewal)
  - cert-manager in-depth (all issuers)
  - Vault PKI integration
  - Renewal strategies

- [ ] references/mtls-guide.md
  - Architecture patterns
  - Nginx mTLS configuration
  - Certificate distribution strategies
  - Service mesh integration notes

**Token Budget:** ~1,500-2,000 tokens total (split across files)

### Phase 3: Examples and Scripts (Week 3)

**Deliverables:**
- [ ] examples/self-signed/generate.sh
- [ ] examples/cfssl-ca/ (complete CA setup)
- [ ] examples/certbot/ (all challenge types)
- [ ] examples/cert-manager/ (K8s manifests)
- [ ] examples/mtls-nginx/ (working config)
- [ ] scripts/check-cert-expiry.sh
- [ ] scripts/validate-chain.sh
- [ ] scripts/test-tls-connection.sh

**Token Budget:** ~500-1,000 tokens (comments in scripts)

### Phase 4: Debugging and Advanced Topics (Week 4)

**Deliverables:**
- [ ] references/debugging-tls.md
  - OpenSSL s_client comprehensive guide
  - Common errors and solutions
  - Certificate chain validation
  - Monitoring and alerting

- [ ] references/tls13-best-practices.md
  - Protocol configuration
  - Cipher suite selection
  - OCSP stapling setup
  - Performance tuning

**Token Budget:** ~1,000 tokens

### Total Estimated Token Count

```
Phase 1 (Core):        2,000-2,500 tokens
Phase 2 (References):  1,500-2,000 tokens
Phase 3 (Examples):      500-1,000 tokens
Phase 4 (Advanced):    1,000 tokens
─────────────────────────────────────────
Total:                 5,000-6,500 tokens
Target:                2,000-5,000 tokens (Low Level)
```

**Optimization Strategy:**
- Keep SKILL.md under 300 lines (core guidance only)
- Move detailed examples to references/ (progressive disclosure)
- Use scripts/ for repetitive commands (zero-token execution)
- Assume Claude knows OpenSSL basics (focus on TLS-specific operations)

### Testing and Validation

**Test Scenarios:**
1. **Generate self-signed cert for development**
   - User: "I need HTTPS for my local dev environment"
   - Expected: Skill triggers, provides mkcert quick start

2. **Setup Let's Encrypt for production**
   - User: "Setup HTTPS for example.com on Kubernetes"
   - Expected: Skill provides cert-manager + Ingress example

3. **Configure mTLS for microservices**
   - User: "How do I setup mutual TLS between services?"
   - Expected: Skill provides mTLS architecture and CFSSL example

4. **Debug certificate error**
   - User: "Getting 'certificate has expired' error"
   - Expected: Skill provides debugging commands and solution

5. **Rotate certificates**
   - User: "How do I rotate certificates without downtime?"
   - Expected: Skill provides rotation strategies for different tools

**Success Criteria:**
- [ ] Skill triggers on TLS-related queries
- [ ] Provides correct tool for environment (K8s vs VMs)
- [ ] Debugging commands work and solve common issues
- [ ] Examples are copy-paste ready
- [ ] References loaded only when needed (progressive disclosure)

---

## Summary

**This skill provides:**
- **Certificate generation** for all environments (dev, staging, production)
- **Automation patterns** (certbot, cert-manager, Vault PKI)
- **mTLS implementation** (service-to-service authentication)
- **TLS 1.3 configuration** (modern security best practices)
- **Debugging workflows** (OpenSSL, curl, common errors)

**Key differentiators:**
- **Environment-aware**: Different tools for K8s, VMs, local dev
- **Automation-first**: Emphasizes automatic renewal (90-day certs)
- **Modern standards**: TLS 1.3, short-lived certs, mTLS
- **Practical examples**: Working code, not just theory

**Integration:**
- Works with `secret-management` for key storage
- Complements `auth-security` for application auth
- Supports `deploying-applications` with cert injection
- Enables `load-balancing-patterns` with TLS termination

**Token efficiency:**
- Core guidance in SKILL.md (~2,500 tokens)
- Detailed references loaded on demand (~3,000 tokens)
- Scripts executed without loading (zero-token utilities)
- Total: 2,000-5,000 tokens (Low Level target achieved)

---

**Status:** Master Plan Complete ✅
**Next Step:** Implement SKILL.md using this plan
**Research Valid Until:** June 2026 (re-validate for TLS 1.4 or quantum-resistant standards)
