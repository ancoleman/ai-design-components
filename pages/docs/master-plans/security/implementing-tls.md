---
sidebar_position: 5
title: Implementing TLS
description: Master plan for TLS/SSL implementation including certificate generation, automation, mTLS, and modern cipher suites
tags: [master-plan, security, tls, ssl, certificates, encryption]
---

# Implementing TLS

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

TLS (Transport Layer Security) encrypts data in transit and is essential for modern applications. This skill covers certificate generation, automation with Let's Encrypt/cert-manager, mTLS (mutual TLS), and modern cipher suite configuration.

## Scope

This skill teaches:

- **Certificate Generation** - Self-signed, CA-signed, Let's Encrypt automation
- **TLS Termination** - Load balancer, reverse proxy, application-level
- **mTLS (Mutual TLS)** - Client certificate authentication
- **Certificate Management** - Rotation, renewal, revocation
- **Modern TLS Configuration** - TLS 1.3, cipher suites, HSTS
- **Automation** - cert-manager (Kubernetes), ACME protocol

## Key Components

### Certificate Types

**Self-Signed Certificates:**
- Used for: Development, testing, internal services
- Pros: Free, no CA dependency
- Cons: Browser warnings, not trusted by default

**Let's Encrypt (ACME):**
- Used for: Public-facing websites
- Pros: Free, automated, trusted by browsers
- Cons: 90-day expiry (requires automation)

**Commercial CA:**
- Used for: Enterprise, extended validation (EV)
- Pros: Longer validity, insurance, support
- Cons: Cost, manual processes

**Internal CA:**
- Used for: Internal services, mTLS
- Pros: Full control, custom policies
- Cons: PKI infrastructure maintenance

### TLS Termination Patterns

**Load Balancer Termination:**
```
Client → LB (HTTPS) → Backend (HTTP)
  │        │              │
  ▼        ▼              ▼
TLS     Decrypt       Plaintext
encrypted             (trusted network)
```
- Pros: Centralized certificate management, offload TLS
- Cons: Plaintext between LB and backend

**End-to-End TLS:**
```
Client → LB (HTTPS) → Backend (HTTPS)
  │        │              │
  ▼        ▼              ▼
TLS     TLS passthrough  TLS encrypted
encrypted  OR re-encrypt  (zero trust)
```
- Pros: Encrypted everywhere (zero trust)
- Cons: Certificate management on backends

### mTLS (Mutual TLS)

**Purpose:** Both client and server authenticate with certificates

**Use Cases:**
- Service-to-service communication (service mesh)
- API authentication (machine-to-machine)
- Zero trust networking

**mTLS Workflow:**
1. Client connects to server
2. Server presents certificate
3. Client validates server certificate
4. Server requests client certificate
5. Client presents certificate
6. Server validates client certificate
7. Encrypted communication established

**Example (NGINX mTLS):**
```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    ssl_client_certificate /etc/nginx/ssl/ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;

    location / {
        if ($ssl_client_verify != SUCCESS) {
            return 403;
        }
        proxy_pass http://backend;
    }
}
```

### Modern TLS Configuration (2025)

**TLS Protocol Versions:**
- **TLS 1.3** - Preferred (faster handshake, modern ciphers)
- **TLS 1.2** - Acceptable (for legacy clients)
- **TLS 1.0/1.1** - **Deprecated, disable**

**Cipher Suites (TLS 1.3):**
```
TLS_AES_256_GCM_SHA384
TLS_CHACHA20_POLY1305_SHA256
TLS_AES_128_GCM_SHA256
```

**HSTS (HTTP Strict Transport Security):**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

## Decision Framework

**Which Certificate Type?**

```
Public-facing website?
  YES → Let's Encrypt (free, automated)

Internal services only?
  YES → Self-signed OR Internal CA
        Need mTLS? → Internal CA (easier trust)

Enterprise/commercial?
  YES → Commercial CA (DigiCert, GlobalSign)

Kubernetes workloads?
  YES → cert-manager + Let's Encrypt
        OR cert-manager + Internal CA (Vault)
```

**TLS Termination Location?**

```
Cloud load balancer available?
  YES → Terminate at LB (simplest)

Zero trust / compliance required?
  YES → End-to-end TLS (encrypt everywhere)

Service mesh deployed?
  YES → mTLS via service mesh (Istio, Linkerd)

Legacy applications?
  YES → LB termination (offload TLS)
```

## Tool Recommendations

### Certificate Management

**Let's Encrypt + Certbot:**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal (cron)
0 12 * * * /usr/bin/certbot renew --quiet
```

**cert-manager (Kubernetes):**
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-com
spec:
  secretName: example-com-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - example.com
    - www.example.com
```

**HashiCorp Vault:**
- PKI secrets engine
- Automated certificate issuance
- Short-lived certificates (< 1 day)

### Testing and Validation

**OpenSSL:**
```bash
# Test TLS connection
openssl s_client -connect example.com:443 -servername example.com

# Check certificate expiry
openssl s_client -connect example.com:443 | openssl x509 -noout -dates

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt
```

**SSL Labs:**
- https://www.ssllabs.com/ssltest/
- Grade TLS configuration
- Identify vulnerabilities

## Integration Points

**With Other Skills:**
- `security-architecture` - Encryption as security control
- `kubernetes-operations` - cert-manager for automated certificates
- `service-mesh` - mTLS for service-to-service encryption
- `configuring-nginx` - NGINX TLS termination
- `load-balancing-patterns` - LB TLS termination

**Workflow Example:**
```
Domain → DNS → LB/Ingress → Certificate → HTTPS
   │       │        │           │            │
   ▼       ▼        ▼           ▼            ▼
Route53  CNAME  ALB/NGINX  cert-manager  Encrypted
record             OR      + Let's       traffic
                  Ingress   Encrypt
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/implementing-tls/init.md)
- Related: `security-architecture`, `service-mesh`, `configuring-nginx`
