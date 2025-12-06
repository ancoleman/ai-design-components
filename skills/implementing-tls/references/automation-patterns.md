# TLS Automation Patterns

Comprehensive guide to automating certificate lifecycle management across different platforms.

## Table of Contents

1. [Let's Encrypt with Certbot](#lets-encrypt-with-certbot)
2. [cert-manager in Kubernetes](#cert-manager-in-kubernetes)
3. [HashiCorp Vault PKI](#hashicorp-vault-pki)
4. [Renewal Strategies](#renewal-strategies)

## Let's Encrypt with Certbot

### Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot

# RHEL/CentOS/Fedora
sudo yum install certbot
# or
sudo dnf install certbot

# macOS
brew install certbot

# Verify installation
certbot --version
```

### Standalone Mode

Requires port 80 to be free (no web server running):

```bash
# Obtain certificate
sudo certbot certonly --standalone \
  -d example.com \
  -d www.example.com \
  --email admin@example.com \
  --agree-tos \
  --no-eff-email

# Certificates saved to:
# /etc/letsencrypt/live/example.com/fullchain.pem
# /etc/letsencrypt/live/example.com/privkey.pem
# /etc/letsencrypt/live/example.com/chain.pem
# /etc/letsencrypt/live/example.com/cert.pem
```

### Webroot Mode

Web server keeps running, validation files served from document root:

```bash
# Obtain certificate
sudo certbot certonly --webroot \
  -w /var/www/html \
  -d example.com \
  -d www.example.com \
  --email admin@example.com \
  --agree-tos

# Certbot writes challenge files to:
# /var/www/html/.well-known/acme-challenge/
```

### Nginx Plugin

Automatically configures Nginx:

```bash
# Install nginx plugin
sudo apt install python3-certbot-nginx

# Obtain certificate AND configure Nginx
sudo certbot --nginx -d example.com -d www.example.com

# Certbot modifies nginx config automatically
# Adds ssl_certificate and ssl_certificate_key directives
# Creates redirect from HTTP to HTTPS
```

### Apache Plugin

Automatically configures Apache:

```bash
# Install apache plugin
sudo apt install python3-certbot-apache

# Obtain certificate AND configure Apache
sudo certbot --apache -d example.com -d www.example.com
```

### DNS Challenge (Wildcard Support)

Required for wildcard certificates:

```bash
# Manual DNS challenge
sudo certbot certonly --manual \
  --preferred-challenges dns \
  -d example.com \
  -d "*.example.com"

# Certbot prompts to add TXT record:
# _acme-challenge.example.com TXT "abc123..."

# Verify DNS propagation before continuing:
dig _acme-challenge.example.com TXT
```

**Automated DNS with plugins:**

```bash
# Cloudflare
sudo apt install python3-certbot-dns-cloudflare
cat > ~/.secrets/cloudflare.ini <<EOF
dns_cloudflare_api_token = YOUR_API_TOKEN
EOF
chmod 600 ~/.secrets/cloudflare.ini

sudo certbot certonly --dns-cloudflare \
  --dns-cloudflare-credentials ~/.secrets/cloudflare.ini \
  -d example.com -d "*.example.com"

# Other DNS providers: Route53, Google Cloud DNS, Digital Ocean, etc.
# See: https://eff-certbot.readthedocs.io/en/stable/using.html#dns-plugins
```

### Automatic Renewal

**Cron job (traditional):**

```bash
# Certbot package usually installs cron job automatically
# Check: cat /etc/cron.d/certbot

# Manual cron entry (runs twice daily):
0 0,12 * * * root certbot renew --quiet

# Test renewal without actually renewing:
sudo certbot renew --dry-run
```

**Systemd timer (modern systems):**

```bash
# Check timer status
systemctl status certbot.timer

# Enable timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# View timer schedule
systemctl list-timers certbot.timer
```

**Post-renewal hooks:**

```bash
# Reload web server after renewal
sudo certbot renew --deploy-hook "systemctl reload nginx"

# Or create hook script
sudo mkdir -p /etc/letsencrypt/renewal-hooks/deploy
sudo tee /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh <<'EOF'
#!/bin/bash
systemctl reload nginx
EOF
sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
```

### Staging Environment

Test with Let's Encrypt staging to avoid rate limits:

```bash
# Use staging server
sudo certbot certonly --standalone \
  --staging \
  -d example.com \
  -d www.example.com

# Staging certificates are NOT trusted by browsers
# Use for testing only
```

**Rate Limits:**
- 50 certificates per registered domain per week
- 5 duplicate certificates per week
- Staging has much higher limits

## cert-manager in Kubernetes

### Installation via Helm

```bash
# Add Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager with CRDs
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0 \
  --set installCRDs=true

# Verify installation
kubectl get pods -n cert-manager
kubectl get crd | grep cert-manager
```

### ClusterIssuer (Let's Encrypt)

**Production issuer:**

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
      name: letsencrypt-prod-account-key
    solvers:
    # HTTP-01 solver
    - http01:
        ingress:
          class: nginx
```

**Staging issuer (for testing):**

```yaml
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

**DNS-01 solver (wildcard support):**

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-dns
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-dns-account-key
    solvers:
    - dns01:
        cloudflare:
          apiTokenSecretRef:
            name: cloudflare-api-token
            key: api-token
      selector:
        dnsZones:
        - example.com
```

### Ingress with Automatic Certificates

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - example.com
    - www.example.com
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

cert-manager automatically:
1. Detects Ingress with cert-manager.io/cluster-issuer annotation
2. Creates Certificate resource
3. Solves ACME challenge (HTTP-01)
4. Stores certificate in Secret (example-com-tls)
5. Renews before expiry

### Manual Certificate Resource

For non-Ingress use cases:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-cert
  namespace: production
spec:
  secretName: api-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - api.example.com
  - api.internal.example.com
  duration: 2160h  # 90 days
  renewBefore: 720h  # 30 days before expiry
```

### Internal CA with cert-manager

**Create self-signed CA:**

```yaml
# Self-signed issuer (bootstrap)
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}

---
# CA certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: internal-ca
  namespace: cert-manager
spec:
  isCA: true
  commonName: Internal CA
  secretName: internal-ca-key-pair
  duration: 87600h  # 10 years
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer

---
# CA issuer (uses CA cert above)
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: internal-ca-issuer
spec:
  ca:
    secretName: internal-ca-key-pair
```

**Issue certificates from internal CA:**

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: service-cert
  namespace: production
spec:
  secretName: service-tls
  issuerRef:
    name: internal-ca-issuer
    kind: ClusterIssuer
  dnsNames:
  - service.production.svc.cluster.local
  duration: 8760h  # 1 year
  renewBefore: 2160h  # 90 days
  usages:
  - server auth
  - client auth
```

### Monitor Certificates

```bash
# List all certificates
kubectl get certificate -A

# Check certificate status
kubectl describe certificate example-com-cert -n production

# Check certificate request
kubectl get certificaterequest -A

# View certificate secret
kubectl get secret example-com-tls -n production -o yaml

# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager
```

## HashiCorp Vault PKI

### Enable PKI Secrets Engine

```bash
# Enable PKI at pki/
vault secrets enable pki

# Set max TTL to 10 years
vault secrets tune -max-lease-ttl=87600h pki

# Enable intermediate CA (best practice)
vault secrets enable -path=pki_int pki
vault secrets tune -max-lease-ttl=43800h pki_int
```

### Generate Root CA

```bash
# Generate internal root CA
vault write -field=certificate pki/root/generate/internal \
  common_name="Example Corp Root CA" \
  issuer_name="root-2025" \
  ttl=87600h > root_ca.crt

# Configure CA and CRL URLs
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com:8200/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"
```

### Generate Intermediate CA

```bash
# Generate intermediate CSR
vault write -format=json pki_int/intermediate/generate/internal \
  common_name="Example Corp Intermediate CA" \
  issuer_name="example-intermediate" \
  | jq -r '.data.csr' > pki_intermediate.csr

# Sign intermediate with root CA
vault write -format=json pki/root/sign-intermediate \
  issuer_ref="root-2025" \
  csr=@pki_intermediate.csr \
  format=pem_bundle \
  ttl="43800h" \
  | jq -r '.data.certificate' > intermediate.cert.pem

# Import signed intermediate
vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
```

### Create Role for Certificate Issuance

```bash
# Create role for web servers
vault write pki_int/roles/example-dot-com \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl="720h" \
  key_usage="DigitalSignature,KeyEncipherment" \
  ext_key_usage="ServerAuth"

# Create role for client certificates (mTLS)
vault write pki_int/roles/client-cert \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl="24h" \
  key_usage="DigitalSignature,KeyEncipherment" \
  ext_key_usage="ClientAuth"
```

### Issue Certificate

```bash
# Issue server certificate
vault write pki_int/issue/example-dot-com \
  common_name="api.example.com" \
  ttl="24h"

# Returns: certificate, private_key, ca_chain, serial_number

# Issue with explicit SANs
vault write pki_int/issue/example-dot-com \
  common_name="api.example.com" \
  alt_names="api.internal.example.com,api.prod.example.com" \
  ip_sans="192.168.1.100" \
  ttl="24h"
```

### Vault Agent Auto-Renewal

**vault-agent.hcl:**

```hcl
pid_file = "/var/run/vault-agent.pid"

vault {
  address = "https://vault.example.com:8200"
}

auto_auth {
  method {
    type = "kubernetes"
    config = {
      role = "web-service"
    }
  }

  sink {
    type = "file"
    config = {
      path = "/var/run/secrets/vault-token"
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
  perms       = 0600
  command     = "systemctl reload nginx"
}
```

**cert.tpl:**

```
{{- with secret "pki_int/issue/example-dot-com" "common_name=api.example.com" "ttl=24h" }}
{{ .Data.certificate }}
{{ .Data.ca_chain }}
{{- end }}
```

**key.tpl:**

```
{{- with secret "pki_int/issue/example-dot-com" "common_name=api.example.com" "ttl=24h" }}
{{ .Data.private_key }}
{{- end }}
```

### Revoke Certificate

```bash
# Revoke by serial number
vault write pki_int/revoke serial_number="39:dd:2e:90:b7:23..."

# Check CRL
curl https://vault.example.com:8200/v1/pki_int/crl | openssl crl -inform DER -text
```

## Renewal Strategies

### Renewal Timing

**Best practice:** Renew at 2/3 of certificate lifetime

| Validity | Renew After | Example |
|----------|-------------|---------|
| 90 days | 60 days | Let's Encrypt (30 days before expiry) |
| 30 days | 20 days | Short-lived internal certs |
| 1 year | 8 months | Long-lived internal certs |
| 24 hours | 16 hours | Dynamic secrets (Vault) |

### Zero-Downtime Renewal

**Load new certificate without restart:**

```bash
# Nginx (reload config)
nginx -s reload

# Apache
apachectl graceful

# HAProxy
systemctl reload haproxy
```

**Kubernetes rolling restart:**

```bash
# Update Secret (cert-manager does this automatically)
kubectl create secret tls example-tls \
  --cert=new-cert.pem --key=new-key.pem \
  --dry-run=client -o yaml | kubectl apply -f -

# Rolling restart deployment
kubectl rollout restart deployment web-app -n production
```

### Monitoring Certificate Expiry

**Check expiry with OpenSSL:**

```bash
# Local certificate
openssl x509 -in cert.pem -noout -enddate

# Remote server
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -enddate

# Check if expires within 30 days
openssl x509 -in cert.pem -noout -checkend 2592000
# Exit 0: valid for 30+ days, Exit 1: expires within 30 days
```

**Prometheus monitoring:**

```yaml
# blackbox_exporter config
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      preferred_ip_protocol: ip4

# Prometheus scrape config
scrape_configs:
  - job_name: 'ssl_expiry'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - https://example.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: blackbox-exporter:9115

# Alert rule
groups:
  - name: ssl_expiry
    rules:
    - alert: SSLCertExpiring
      expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7
      for: 1h
      annotations:
        summary: "SSL certificate expiring in <7 days: {{ $labels.instance }}"
```

### Renewal Failure Handling

**Certbot renewal failure:**

```bash
# Check renewal logs
cat /var/log/letsencrypt/letsencrypt.log

# Manual renewal attempt
sudo certbot renew --force-renewal -d example.com

# Common issues:
# - Port 80 blocked (firewall)
# - DNS not pointing to server
# - Rate limit exceeded (use staging)
```

**cert-manager renewal failure:**

```bash
# Check Certificate status
kubectl describe certificate example-cert -n production

# Common issues in status:
# - ACME challenge failed (Ingress misconfigured)
# - DNS propagation timeout (DNS-01)
# - Rate limit (use staging ClusterIssuer)

# Check CertificateRequest
kubectl get certificaterequest -n production
kubectl describe certificaterequest <name> -n production

# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager --tail=100
```

## Best Practices

1. **Use staging environment** for testing (avoid rate limits)
2. **Automate from day one** - manual renewal will be forgotten
3. **Monitor expiry** with alerting (7-30 days before expiry)
4. **Test renewal process** regularly (dry-run)
5. **Short-lived certificates** are more secure (90 days or less)
6. **Separate concerns**: Certificate automation ≠ key storage (use secret management)
7. **Log renewal events** for audit trail
8. **Plan for failure**: What happens if renewal fails?
