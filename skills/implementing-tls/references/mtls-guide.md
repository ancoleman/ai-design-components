# Mutual TLS (mTLS) Implementation Guide

Comprehensive guide to implementing mutual TLS for service-to-service authentication.

## Table of Contents

1. [Understanding mTLS](#understanding-mtls)
2. [Use Cases and Architecture](#use-cases-and-architecture)
3. [mTLS with Nginx](#mtls-with-nginx)
4. [mTLS with Application Code](#mtls-with-application-code)
5. [Certificate Distribution](#certificate-distribution)
6. [Service Mesh Integration](#service-mesh-integration)

## Understanding mTLS

### Standard TLS vs Mutual TLS

**Standard TLS (Server Authentication Only):**
- Client verifies server identity via certificate
- Server does not verify client
- Common for HTTPS websites

**Mutual TLS (Both Authenticate):**
- Both client and server present certificates
- Bidirectional authentication
- Used for service-to-service communication

### mTLS Handshake Flow

```
Client                          Server
  |                               |
  |--- ClientHello -------------->|
  |<-- ServerHello ---------------|
  |<-- Certificate ---------------|  Server proves identity
  |<-- CertificateRequest --------|  Server requests client cert
  |<-- ServerHelloDone ----------|
  |                               |
  |--- Certificate -------------->|  Client proves identity
  |--- ClientKeyExchange -------->|
  |--- CertificateVerify -------->|  Client signs with private key
  |--- ChangeCipherSpec --------->|
  |--- Finished ----------------->|
  |<-- ChangeCipherSpec ----------|
  |<-- Finished ------------------|
  |                               |
  |=== Encrypted Communication ===|
```

## Use Cases and Architecture

### Service-to-Service Authentication

**Microservices architecture:**

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ API Gateway │◄──mTLS──►│ User Service│◄──mTLS──►│ DB Service  │
└─────────────┘         └─────────────┘         └─────────────┘
                              ▲
                            mTLS
                              ▼
                        ┌─────────────┐
                        │Order Service│
                        └─────────────┘
```

**Benefits:**
- No shared secrets or passwords
- Certificate-based authorization (CN, O, OU fields)
- Automatic rotation via short-lived certificates
- Audit trail (certificate serial numbers in logs)

### Zero-Trust Networks

All services require mTLS, even on internal networks:

```
Principle: Never trust, always verify
├─ Every connection authenticated
├─ Certificate-based service identity
├─ Network location irrelevant
└─ Defense in depth
```

### API Authentication

External partners authenticate via client certificates:

```
Partner System ──[client cert]──► API Gateway ──► Internal Services
```

**Advantages over API keys:**
- Stronger cryptographic authentication
- Non-repudiation (signed requests)
- Automatic expiry (time-bound access)
- Harder to steal (requires private key + certificate)

## mTLS with Nginx

### Server Configuration (Require Client Certificates)

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    # Server certificate
    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;

    # CA certificate to verify client certificates
    ssl_client_certificate /etc/ssl/certs/ca.crt;

    # Require client certificate
    ssl_verify_client on;

    # Certificate verification depth
    ssl_verify_depth 2;

    # TLS protocol and ciphers
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;

    # Pass client certificate information to backend
    location / {
        proxy_pass http://backend;

        # Certificate in PEM format
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;

        # Subject Distinguished Name
        proxy_set_header X-SSL-Client-S-DN $ssl_client_s_dn;

        # Issuer Distinguished Name
        proxy_set_header X-SSL-Client-I-DN $ssl_client_i_dn;

        # Verification status (SUCCESS, FAILED:reason, NONE)
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;

        # Certificate serial number
        proxy_set_header X-SSL-Client-Serial $ssl_client_serial;
    }
}
```

### Optional Client Certificate

Make client certificate optional, fallback to other authentication:

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;
    ssl_client_certificate /etc/ssl/certs/ca.crt;

    # Optional client certificate
    ssl_verify_client optional;
    ssl_verify_depth 2;

    location / {
        # Allow if client cert valid OR has API key
        set $auth_pass 0;

        if ($ssl_client_verify = "SUCCESS") {
            set $auth_pass 1;
        }

        if ($http_x_api_key != "") {
            set $auth_pass 1;
        }

        if ($auth_pass = 0) {
            return 401;
        }

        proxy_pass http://backend;
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;
        proxy_set_header X-SSL-Client-S-DN $ssl_client_s_dn;
    }
}
```

### Certificate-Based Authorization

Route based on client certificate attributes:

```nginx
# Extract organization from client cert
map $ssl_client_s_dn $client_org {
    ~O=PartnerA $client_org "partnera";
    ~O=PartnerB $client_org "partnerb";
    default "unknown";
}

server {
    listen 443 ssl;
    ssl_verify_client on;
    ssl_client_certificate /etc/ssl/certs/ca.crt;

    location /api/partnera/ {
        if ($client_org != "partnera") {
            return 403;
        }
        proxy_pass http://partnera-backend;
    }

    location /api/partnerb/ {
        if ($client_org != "partnerb") {
            return 403;
        }
        proxy_pass http://partnerb-backend;
    }
}
```

### Testing with curl

**Basic mTLS request:**

```bash
curl https://api.example.com/endpoint \
  --cert client.crt \
  --key client.key \
  --cacert ca.crt
```

**With verbose output:**

```bash
curl -v https://api.example.com/endpoint \
  --cert client.crt \
  --key client.key \
  --cacert ca.crt
```

**Using PKCS#12 format:**

```bash
# Combine cert and key into PKCS#12
openssl pkcs12 -export -out client.p12 \
  -inkey client.key -in client.crt

# Use with curl
curl https://api.example.com/endpoint \
  --cert-type P12 \
  --cert client.p12:password \
  --cacert ca.crt
```

## mTLS with Application Code

### Go Example

```go
package main

import (
    "crypto/tls"
    "crypto/x509"
    "io/ioutil"
    "log"
    "net/http"
)

func main() {
    // Load CA certificate
    caCert, err := ioutil.ReadFile("ca.crt")
    if err != nil {
        log.Fatal(err)
    }
    caCertPool := x509.NewCertPool()
    caCertPool.AppendCertsFromPEM(caCert)

    // Load client certificate and key
    clientCert, err := tls.LoadX509KeyPair("client.crt", "client.key")
    if err != nil {
        log.Fatal(err)
    }

    // Configure TLS
    tlsConfig := &tls.Config{
        Certificates: []tls.Certificate{clientCert},
        RootCAs:      caCertPool,
        MinVersion:   tls.VersionTLS13,
    }

    // Create HTTP client with mTLS
    client := &http.Client{
        Transport: &http.Transport{
            TLSClientConfig: tlsConfig,
        },
    }

    // Make request
    resp, err := client.Get("https://api.example.com/endpoint")
    if err != nil {
        log.Fatal(err)
    }
    defer resp.Body.Close()

    log.Printf("Response status: %s", resp.Status)
}
```

### Python Example

```python
import requests

# Make mTLS request
response = requests.get(
    'https://api.example.com/endpoint',
    cert=('client.crt', 'client.key'),
    verify='ca.crt'
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

### Node.js Example

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  hostname: 'api.example.com',
  port: 443,
  path: '/endpoint',
  method: 'GET',
  cert: fs.readFileSync('client.crt'),
  key: fs.readFileSync('client.key'),
  ca: fs.readFileSync('ca.crt')
};

const req = https.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  res.on('data', (d) => {
    process.stdout.write(d);
  });
});

req.on('error', (e) => {
  console.error(e);
});

req.end();
```

## Certificate Distribution

### Pattern 1: Manual Distribution (Small Scale)

Suitable for <10 services:

```bash
# 1. Generate CA
cfssl genkey -initca ca-csr.json | cfssljson -bare ca

# 2. Distribute CA to all services (trust store)
# Services must trust this CA to verify peers

# 3. Generate certificates for each service
for service in api user order; do
  cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
    -config=ca-config.json -profile=peer \
    ${service}-csr.json | cfssljson -bare ${service}
done

# 4. Deploy certificates to services
# service.crt, service.key → /etc/ssl/
```

### Pattern 2: cert-manager (Kubernetes)

Automated certificate issuance for pods:

```yaml
# Internal CA
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: internal-ca
  namespace: cert-manager
spec:
  isCA: true
  commonName: Internal CA
  secretName: internal-ca-key-pair
  duration: 87600h
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer

---
# CA Issuer
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: internal-ca-issuer
spec:
  ca:
    secretName: internal-ca-key-pair

---
# Service certificate (automatic)
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-service-cert
  namespace: production
spec:
  secretName: api-service-tls
  issuerRef:
    name: internal-ca-issuer
    kind: ClusterIssuer
  dnsNames:
  - api-service
  - api-service.production.svc.cluster.local
  duration: 2160h  # 90 days
  renewBefore: 720h  # Renew 30 days before expiry
  usages:
  - server auth
  - client auth
```

**Mount certificate in pod:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    spec:
      containers:
      - name: api
        volumeMounts:
        - name: tls
          mountPath: /etc/tls
          readOnly: true
      volumes:
      - name: tls
        secret:
          secretName: api-service-tls
```

### Pattern 3: HashiCorp Vault PKI (Dynamic)

Short-lived certificates issued on demand:

```bash
# Service requests certificate on startup
vault write pki_int/issue/service-role \
  common_name="api-service.internal" \
  ttl="24h"

# Vault Agent auto-renews before expiry
# Service reloads certificate without restart
```

**Vault Agent sidecar in Kubernetes:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "api-service"
        vault.hashicorp.com/agent-inject-secret-cert: "pki_int/issue/service-role"
        vault.hashicorp.com/agent-inject-template-cert: |
          {{- with secret "pki_int/issue/service-role" "common_name=api-service.internal" "ttl=24h" }}
          {{ .Data.certificate }}
          {{ .Data.ca_chain }}
          {{- end }}
    spec:
      containers:
      - name: api
        # Application reads cert from /vault/secrets/cert
```

### Pattern 4: Service Mesh (Istio/Linkerd)

Automatic mTLS via sidecar proxies:

```yaml
# Istio PeerAuthentication (require mTLS)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

**How it works:**
1. Sidecar proxy intercepts all traffic
2. Certificates issued by mesh CA (automatically)
3. mTLS negotiation handled by proxy (transparent to app)
4. Automatic rotation (short TTL, typically 24h)
5. Policy-based access control (which services can communicate)

## Service Mesh Integration

### Istio mTLS

**Enable strict mTLS for namespace:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

**Authorization policy (certificate-based):**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-service-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/user-service"]
    to:
    - operation:
        methods: ["GET", "POST"]
```

### Linkerd mTLS

mTLS enabled by default in Linkerd:

```bash
# Install Linkerd
linkerd install | kubectl apply -f -

# Inject sidecar into deployment
kubectl get deploy api-service -o yaml | \
  linkerd inject - | \
  kubectl apply -f -

# Verify mTLS
linkerd viz stat deploy/api-service
# Shows secured/unsecured connection ratio
```

### Consul Connect

```hcl
# Service definition with Connect
service {
  name = "api-service"
  port = 8080

  connect {
    sidecar_service {
      proxy {
        upstreams {
          destination_name = "database"
          local_bind_port  = 5432
        }
      }
    }
  }
}
```

## Best Practices

1. **Short-lived certificates**: 24 hours to 90 days maximum
2. **Automatic rotation**: Never rely on manual renewal
3. **Certificate monitoring**: Alert before expiry
4. **Least privilege**: Issue certificates with minimal permissions
5. **Certificate revocation**: Have revocation process ready (CRL, OCSP)
6. **Audit logging**: Log certificate serial numbers for non-repudiation
7. **Separate CAs**: Different CAs for server and client certificates
8. **Service mesh for scale**: Use Istio/Linkerd for 50+ services
9. **Test certificate validation**: Ensure services reject invalid certs
10. **Emergency access**: Have break-glass procedure if certificates fail

## Troubleshooting

### Common mTLS Errors

**"peer did not return a certificate"**
- Client not sending certificate
- Verify client has cert/key files
- Check curl command includes --cert and --key

**"certificate verify failed: unable to get local issuer certificate"**
- CA certificate not in trust store
- Server: Add CA to ssl_client_certificate
- Client: Add CA to --cacert or system trust store

**"tlsv1 alert unknown ca"**
- Server doesn't trust client's CA
- Verify ssl_client_certificate contains correct CA

**"tlsv1 alert certificate required"**
- Server requires client certificate (ssl_verify_client on)
- Client must provide certificate

**"tlsv1 alert access denied"**
- Certificate verification succeeded but authorization failed
- Check Nginx location rules or application logic

### Debug mTLS with OpenSSL

```bash
# Test server mTLS requirement
openssl s_client -connect api.example.com:443

# Verify server requests client certificate
# Look for "Acceptable client certificate CA names"

# Test with client certificate
openssl s_client -connect api.example.com:443 \
  -cert client.crt -key client.key -CAfile ca.crt \
  -showcerts

# Verify handshake successful:
# "Verify return code: 0 (ok)"
```

### Verify Certificate Chain

```bash
# Verify server certificate against CA
openssl verify -CAfile ca.crt server.crt

# Verify client certificate against CA
openssl verify -CAfile ca.crt client.crt

# Check certificate purpose
openssl x509 -in server.crt -noout -purpose
# Should include: "SSL server : Yes"

openssl x509 -in client.crt -noout -purpose
# Should include: "SSL client : Yes"
```

For additional debugging, see `debugging-tls.md`.
