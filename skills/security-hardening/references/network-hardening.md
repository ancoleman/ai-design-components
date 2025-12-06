# Network Hardening Reference

Comprehensive guide to hardening network configurations using firewalls, segmentation, TLS, and DNS security.

## Table of Contents

1. [Firewall Configuration](#firewall-configuration)
2. [Network Segmentation](#network-segmentation)
3. [TLS/mTLS Configuration](#tlsmtls-configuration)
4. [DNS Security](#dns-security)
5. [Network Monitoring](#network-monitoring)

---

## Firewall Configuration

### iptables (Linux)

```bash
#!/bin/bash
# /etc/scripts/firewall-hardening.sh

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Default policies: DROP
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from specific network
iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/8 -m state --state NEW -j ACCEPT

# Allow HTTPS outbound
iptables -A OUTPUT -p tcp --dport 443 -m state --state NEW -j ACCEPT

# Allow DNS outbound
iptables -A OUTPUT -p udp --dport 53 -m state --state NEW -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "iptables-INPUT-dropped: "
iptables -A OUTPUT -j LOG --log-prefix "iptables-OUTPUT-dropped: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### firewalld (Red Hat/CentOS)

```bash
# Set default zone to drop
firewall-cmd --set-default-zone=drop

# Create custom zone for trusted networks
firewall-cmd --permanent --new-zone=trusted-internal
firewall-cmd --permanent --zone=trusted-internal --add-source=10.0.0.0/8
firewall-cmd --permanent --zone=trusted-internal --add-service=ssh
firewall-cmd --permanent --zone=trusted-internal --add-service=http
firewall-cmd --permanent --zone=trusted-internal --add-service=https

# Allow specific ports
firewall-cmd --permanent --zone=public --add-port=8080/tcp

# Enable logging for denied packets
firewall-cmd --set-log-denied=all

# Reload
firewall-cmd --reload
```

### nftables (Modern replacement for iptables)

```bash
# /etc/nftables.conf
flush ruleset

table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;

    # Allow loopback
    iif lo accept

    # Allow established connections
    ct state established,related accept

    # Allow SSH from trusted network
    ip saddr 10.0.0.0/8 tcp dport 22 ct state new accept

    # Log dropped
    log prefix "nftables-input-dropped: " drop
  }

  chain forward {
    type filter hook forward priority 0; policy drop;
  }

  chain output {
    type filter hook output priority 0; policy drop;

    # Allow loopback
    oif lo accept

    # Allow established
    ct state established,related accept

    # Allow HTTPS outbound
    tcp dport 443 ct state new accept

    # Allow DNS
    udp dport 53 ct state new accept

    # Log dropped
    log prefix "nftables-output-dropped: " drop
  }
}
```

---

## Network Segmentation

### VLAN Segmentation

```
Network Architecture:
┌─────────────────────────────────────────┐
│             Internet                     │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │   Firewall     │
         └───────┬────────┘
                 │
     ┌───────────┴────────────┐
     │  Core Switch (VLANs)   │
     └─────┬──────┬──────┬────┘
           │      │      │
    VLAN 10│ VLAN 20│ VLAN 30
    DMZ    │ App   │ DB
    ───────┴───────┴─────────
    Public │ Internal│ Data
    Web    │ Apps   │ Storage
```

**Segmentation principles:**
- DMZ for internet-facing services
- Application tier (internal only)
- Database tier (most restricted)
- Management network (separate)

### Kubernetes NetworkPolicy

```yaml
# Default deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Allow frontend -> API
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: database
    ports:
    - protocol: TCP
      port: 5432
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53

---
# Allow database -> nowhere (only ingress)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: database
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: api
    ports:
    - protocol: TCP
      port: 5432
  egress: []  # No outbound allowed
```

### Service Mesh (Istio)

```yaml
# Strict mTLS for all workloads
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

---
# Authorization policy: deny all by default
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}

---
# Allow frontend to API
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

---

## TLS/mTLS Configuration

### NGINX TLS Hardening

```nginx
# /etc/nginx/conf.d/ssl-hardening.conf

server {
    listen 443 ssl http2;
    server_name example.com;

    # Certificates
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Protocols: TLS 1.2 and 1.3 only
    ssl_protocols TLSv1.2 TLSv1.3;

    # Strong cipher suites (ordered by preference)
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;

    # HSTS (force HTTPS for 1 year)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/nginx/ssl/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # Session cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;

    # DH parameters (generate with: openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096)
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    location / {
        proxy_pass http://backend;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Certificate Generation (Let's Encrypt)

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Generate certificate
certbot --nginx -d example.com -d www.example.com

# Auto-renewal (cron job)
0 0 * * * certbot renew --quiet --post-hook "systemctl reload nginx"
```

### mTLS with Client Certificates

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/nginx/ssl/server.pem;
    ssl_certificate_key /etc/nginx/ssl/server-key.pem;

    # Require client certificate
    ssl_verify_client on;
    ssl_client_certificate /etc/nginx/ssl/ca.pem;
    ssl_verify_depth 2;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';

    location / {
        # Pass client certificate info to backend
        proxy_set_header X-Client-Cert $ssl_client_cert;
        proxy_set_header X-Client-Verify $ssl_client_verify;
        proxy_set_header X-Client-DN $ssl_client_s_dn;
        proxy_pass http://backend;
    }
}
```

---

## DNS Security

### DNSSEC Configuration

```bash
# Install BIND9 with DNSSEC support
apt-get install bind9 bind9utils

# Generate DNSSEC keys
cd /etc/bind/keys
dnssec-keygen -a ECDSAP256SHA256 -n ZONE example.com
dnssec-keygen -f KSK -a ECDSAP256SHA256 -n ZONE example.com

# Sign zone
dnssec-signzone -A -3 $(head -c 1000 /dev/random | sha1sum | cut -b 1-16) \
  -N INCREMENT -o example.com -t /var/cache/bind/db.example.com

# Update named.conf
zone "example.com" {
    type master;
    file "/var/cache/bind/db.example.com.signed";
    allow-transfer { none; };
};
```

### DNS Filtering (Pi-hole style)

```bash
# Block malicious domains
# /etc/dnsmasq.d/blocklist.conf

# Block tracking
address=/doubleclick.net/0.0.0.0
address=/googleadservices.com/0.0.0.0

# Block malware
address=/malware-site.com/0.0.0.0

# Use upstream DNS with DoT (DNS over TLS)
server=1.1.1.1@853#cloudflare-dns.com
server=8.8.8.8@853#dns.google
```

### DNS over HTTPS (DoH) Client

```yaml
# dnscrypt-proxy.toml
server_names = ['cloudflare', 'google']

[sources]
  [sources.'public-resolvers']
  urls = ['https://raw.githubusercontent.com/DNSCrypt/dnscrypt-resolvers/master/v3/public-resolvers.md']
  cache_file = 'public-resolvers.md'
  minisign_key = 'RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3'
  refresh_delay = 72

[static]
  [static.'cloudflare']
  stamp = 'sdns://AgcAAAAAAAAABzEuMS4xLjEgPhoaD2xT8-l6SS1XCEtbmAcFnuBXqxUFh2_YP9o9uDgKZG5zLmNsb3VkZmxhcmUuY29tCi9kbnMtcXVlcnk'
```

---

## Network Monitoring

### Enable Flow Logging

**AWS VPC Flow Logs:**
```hcl
resource "aws_flow_log" "vpc" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_logs.arn
  log_destination = aws_cloudwatch_log_group.flow_logs.arn
}
```

**GCP VPC Flow Logs:**
```hcl
resource "google_compute_subnetwork" "main" {
  name          = "main-subnet"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.main.id

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 1.0
    metadata             = "INCLUDE_ALL_METADATA"
  }
}
```

### Intrusion Detection (Suricata)

```bash
# Install Suricata
apt-get install suricata

# Configure /etc/suricata/suricata.yaml
af-packet:
  - interface: eth0
    threads: auto
    cluster-id: 99
    cluster-type: cluster_flow

# Update rules
suricata-update

# Start Suricata
systemctl enable suricata
systemctl start suricata

# Monitor alerts
tail -f /var/log/suricata/fast.log
```

### Network Scanning Detection

```bash
# Configure fail2ban to block port scans
# /etc/fail2ban/filter.d/portscan.conf

[Definition]
failregex = ^.*kernel:.*IN=.* SRC=<HOST> DST=.* PROTO=(TCP|UDP).*$
ignoreregex =

# /etc/fail2ban/jail.local
[portscan]
enabled = true
filter = portscan
logpath = /var/log/kern.log
maxretry = 5
findtime = 300
bantime = 86400
```

---

## Additional Resources

- NIST Firewall Guide: https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final
- Mozilla SSL Configuration Generator: https://ssl-config.mozilla.org/
- Kubernetes Network Policies: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Istio Security: https://istio.io/latest/docs/concepts/security/
- DNSSEC Guide: https://www.dnssec.net/
