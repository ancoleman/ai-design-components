---
sidebar_position: 4
title: Implementing TLS
description: Configure TLS certificates and encryption for secure communications
tags: [security, tls, ssl, certificates, encryption, mtls, lets-encrypt]
---

# Implementing TLS

Implement Transport Layer Security (TLS) for encrypting network communications and authenticating services. Generate certificates, automate certificate lifecycle management, configure TLS 1.3, implement mutual TLS, and debug certificate issues.

## When to Use

Trigger this skill when:
- Setting up HTTPS for web applications or APIs
- Securing service-to-service communication in microservices
- Implementing mutual TLS (mTLS) for zero-trust networks
- Generating certificates for development or production
- Automating certificate renewal and rotation
- Debugging certificate validation errors
- Configuring TLS termination at load balancers
- Setting up internal PKI for corporate networks

## Key Features

**Certificate Types:**
- **Public HTTPS**: Let's Encrypt with HTTP-01 (single domain) or DNS-01 (wildcard)
- **Internal Services**: Internal CA with CFSSL or HashiCorp Vault PKI
- **Development**: mkcert for trusted local certificates
- **mTLS**: Mutual authentication for service-to-service communication

**TLS 1.3 Best Practices:**
- Enable TLS 1.3 and 1.2 only (disable SSLv3, TLS 1.0, TLS 1.1)
- Recommended cipher suites: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256
- Perfect Forward Secrecy (PFS) with ephemeral key exchanges (ECDHE)
- OCSP Stapling for performance and privacy
- HSTS (Strict-Transport-Security) to force HTTPS

**Automation Tools:**
- **Kubernetes**: cert-manager with Let's Encrypt, Vault, or internal CA
- **Traditional Servers**: Certbot with nginx/apache plugins or DNS providers
- **Microservices**: HashiCorp Vault PKI for dynamic, short-lived certificates
- **Development**: mkcert for browser-trusted local certificates

**Certificate Lifecycle:**
1. Generate (mkcert, Let's Encrypt, CFSSL, Vault)
2. Deploy (Kubernetes Secrets, /etc/ssl/, Docker volumes)
3. Monitor (openssl x509, Prometheus blackbox_exporter)
4. Renew (30 days before expiry, automated via certbot/cert-manager/Vault)
5. Rotate (zero-downtime reload, rolling restarts)

## Quick Start

```bash
# Development: Local HTTPS with mkcert
brew install mkcert
mkcert -install
mkcert example.com localhost 127.0.0.1
# Creates: example.com+2.pem and example.com+2-key.pem

# Production: Let's Encrypt with Certbot
sudo apt install certbot
sudo certbot certonly --standalone -d example.com -d www.example.com
# Certificates saved to /etc/letsencrypt/live/example.com/

# Kubernetes: cert-manager with Let's Encrypt
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true
```

**Kubernetes Ingress with Automatic TLS:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - example.com
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

**Nginx TLS 1.3 Configuration:**

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_prefer_server_ciphers off;
    ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256';

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

**Debug TLS Issues:**

```bash
# Test TLS connection
openssl s_client -connect example.com:443

# Show certificate chain
openssl s_client -connect example.com:443 -showcerts

# Check certificate expiration
openssl x509 -in cert.pem -noout -dates

# Verify certificate chain
openssl verify -CAfile ca.crt cert.pem

# Test mTLS with client certificate
openssl s_client -connect api.example.com:443 \
  -cert client.crt -key client.key -CAfile ca.crt
```

**Common Errors and Solutions:**

| Error | Cause | Solution |
|-------|-------|----------|
| `certificate has expired` | Certificate validity passed | Renew certificate, check system clock |
| `unable to get local issuer certificate` | CA not in trust store | Add CA cert to system trust store |
| `Hostname mismatch` | CN/SAN doesn't match hostname | Regenerate cert with correct SANs |
| `handshake failure` | TLS version/cipher mismatch | Enable TLS 1.2+, check cipher suites |
| `certificate signed by unknown authority` | Missing intermediate certs | Include full chain in server config |

## Related Skills

- [Security Architecture](./architecting-security.md) - Strategic security design including PKI architecture
- [Configuring Firewalls](./configuring-firewalls.md) - Network security layer for TLS traffic
- [Secret Management](#) - Store private keys securely (Vault, Kubernetes Secrets, HSM)
- [Security Hardening](./security-hardening.md) - System security configuration including TLS hardening

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-tls)
- [Master Plan](../../master-plans/security/implementing-tls.md)
