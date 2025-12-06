# TLS Debugging and Troubleshooting Guide

Comprehensive guide for debugging TLS issues and common certificate problems.

## Table of Contents

1. [Essential Debugging Commands](#essential-debugging-commands)
2. [Common TLS Errors](#common-tls-errors)
3. [Certificate Validation](#certificate-validation)
4. [TLS Handshake Analysis](#tls-handshake-analysis)
5. [Monitoring Certificate Expiry](#monitoring-certificate-expiry)

## Essential Debugging Commands

### OpenSSL s_client

**Basic connection test:**

```bash
# Test TLS connection
openssl s_client -connect example.com:443

# Key indicators in output:
# - "Verify return code: 0 (ok)" = certificate valid
# - "Verify return code: 20" = unable to get local issuer certificate
# - "Verify return code: 10" = certificate has expired
```

**Show certificate chain:**

```bash
openssl s_client -connect example.com:443 -showcerts

# Displays full certificate chain:
# - Server certificate (first)
# - Intermediate certificates
# - Root CA (usually not included)
```

**Test specific TLS version:**

```bash
# TLS 1.3
openssl s_client -connect example.com:443 -tls1_3

# TLS 1.2
openssl s_client -connect example.com:443 -tls1_2

# TLS 1.1 (should fail on modern servers)
openssl s_client -connect example.com:443 -tls1_1
```

**Test with SNI (Server Name Indication):**

```bash
# Required for shared hosting / multiple domains
openssl s_client -connect example.com:443 -servername example.com

# Without SNI, server may present wrong certificate
```

**Test specific cipher suite:**

```bash
# Test if server supports specific cipher
openssl s_client -connect example.com:443 \
  -cipher 'ECDHE-RSA-AES256-GCM-SHA384'

# Test TLS 1.3 cipher
openssl s_client -connect example.com:443 \
  -tls1_3 -ciphersuites 'TLS_AES_256_GCM_SHA384'
```

**Test mTLS (client certificate):**

```bash
openssl s_client -connect api.example.com:443 \
  -cert client.crt \
  -key client.key \
  -CAfile ca.crt

# Verify output includes:
# "Acceptable client certificate CA names" (server requests client cert)
# "Verify return code: 0 (ok)"
```

**Save server certificate:**

```bash
# Extract and save certificate
openssl s_client -connect example.com:443 </dev/null 2>/dev/null | \
  openssl x509 -out server.crt

# Verify saved certificate
openssl x509 -in server.crt -noout -text
```

### curl for TLS Testing

**Verbose TLS handshake:**

```bash
curl -v https://example.com

# Look for:
# * SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
# * Server certificate:
# *  subject: CN=example.com
# *  issuer: C=US; O=Let's Encrypt; CN=R3
```

**Very verbose (show all TLS details):**

```bash
curl -vvv https://example.com 2>&1 | grep -E "SSL|TLS"
```

**Test with specific CA:**

```bash
curl --cacert ca.crt https://example.com
```

**Test mTLS:**

```bash
curl --cert client.crt --key client.key --cacert ca.crt \
  https://api.example.com/endpoint
```

**Ignore certificate errors (INSECURE - testing only):**

```bash
curl -k https://example.com
# or
curl --insecure https://example.com
```

### Certificate Examination

**View certificate details:**

```bash
# Full certificate details
openssl x509 -in cert.pem -noout -text

# Specific fields only
openssl x509 -in cert.pem -noout -subject
openssl x509 -in cert.pem -noout -issuer
openssl x509 -in cert.pem -noout -dates
openssl x509 -in cert.pem -noout -serial
openssl x509 -in cert.pem -noout -fingerprint -sha256
```

**Check Subject Alternative Names (SANs):**

```bash
openssl x509 -in cert.pem -noout -text | grep -A 1 "Subject Alternative Name"

# Example output:
# X509v3 Subject Alternative Name:
#     DNS:example.com, DNS:www.example.com, IP Address:192.168.1.100
```

**Check certificate purpose:**

```bash
openssl x509 -in cert.pem -noout -purpose

# Shows allowed purposes:
# - SSL client : Yes/No
# - SSL server : Yes/No
# - S/MIME signing : Yes/No
```

**Check certificate expiration:**

```bash
# Show dates
openssl x509 -in cert.pem -noout -dates
# Output:
# notBefore=Jan  1 00:00:00 2025 GMT
# notAfter=Apr  1 00:00:00 2025 GMT

# Check if expired
openssl x509 -in cert.pem -noout -checkend 0
# Exit 0: not expired, Exit 1: expired

# Check if expires within 30 days (2592000 seconds)
openssl x509 -in cert.pem -noout -checkend 2592000
```

## Common TLS Errors

### Error: "certificate has expired"

**Cause:** Certificate validity period has passed.

**Diagnosis:**

```bash
# Check expiration date
openssl x509 -in cert.pem -noout -enddate

# Check system clock
date
timedatectl  # systemd systems
```

**Solution:**

```bash
# 1. Renew certificate
certbot renew  # Let's Encrypt
# or regenerate self-signed certificate

# 2. Verify system clock is correct
sudo ntpdate pool.ntp.org
# or
sudo timedatectl set-ntp true
```

### Error: "unable to get local issuer certificate"

**Cause:** CA certificate not in trust store.

**Diagnosis:**

```bash
# Check certificate chain
openssl s_client -connect example.com:443 -showcerts

# Verify issuer
openssl x509 -in cert.pem -noout -issuer
```

**Solution:**

Add CA certificate to system trust store:

```bash
# Ubuntu/Debian
sudo cp ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# RHEL/CentOS/Fedora
sudo cp ca.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust

# Or specify CA in application
curl --cacert ca.crt https://example.com
openssl s_client -CAfile ca.crt -connect example.com:443
```

### Error: "certificate verify failed: Hostname mismatch"

**Cause:** Certificate CN/SAN doesn't match requested hostname.

**Diagnosis:**

```bash
# Check certificate SANs
openssl x509 -in cert.pem -noout -text | grep -A 3 "Subject Alternative Name"

# Check what hostname you're requesting
curl -v https://example.com  # Look at "Host:" header
```

**Solution:**

```bash
# 1. Regenerate certificate with correct SANs
# See certificate-generation.md

# 2. Or use correct hostname
curl https://correct-hostname.com  # Match certificate

# 3. For testing with IP (if cert has IP in SAN)
curl --resolve example.com:443:192.168.1.100 https://example.com
```

### Error: "SSL handshake failed: sslv3 alert handshake failure"

**Cause:** TLS version or cipher suite mismatch.

**Diagnosis:**

```bash
# Test TLS versions
openssl s_client -connect example.com:443 -tls1_3
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_1

# Test cipher support
openssl s_client -connect example.com:443 \
  -cipher 'ECDHE-RSA-AES256-GCM-SHA384'
```

**Solution:**

Update configuration to support TLS 1.2+ and strong ciphers:

```nginx
# Nginx
ssl_protocols TLSv1.3 TLSv1.2;
ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256';
```

### Error: "certificate signed by unknown authority"

**Cause:** Intermediate certificates missing from chain.

**Diagnosis:**

```bash
# Check what server sends
openssl s_client -connect example.com:443 -showcerts

# Verify chain locally
openssl verify -CAfile ca.crt cert.pem
# If this fails, chain is incomplete
```

**Solution:**

Include full certificate chain in server configuration:

```bash
# Build full chain
cat cert.pem intermediate.pem root.pem > fullchain.pem

# Configure server
# Nginx
ssl_certificate /etc/ssl/certs/fullchain.pem;

# Apache
SSLCertificateFile /etc/ssl/certs/fullchain.pem
```

### Error: "tlsv1 alert unknown ca" (mTLS)

**Cause:** Server doesn't trust client certificate's CA.

**Diagnosis:**

```bash
# Verify client certificate issuer
openssl x509 -in client.crt -noout -issuer

# Check server's trusted CAs
# Nginx: ssl_client_certificate directive
# Check file contains correct CA
openssl x509 -in /etc/ssl/certs/ca.crt -noout -subject
```

**Solution:**

Add client CA to server trust store:

```nginx
# Nginx
ssl_client_certificate /etc/ssl/certs/client-ca.crt;
ssl_verify_client on;
```

### Error: "peer did not return a certificate" (mTLS)

**Cause:** Client not sending certificate when server requires it.

**Diagnosis:**

```bash
# Verify server requests client cert
openssl s_client -connect api.example.com:443
# Look for "Acceptable client certificate CA names"
```

**Solution:**

```bash
# Client must provide certificate
curl --cert client.crt --key client.key https://api.example.com

# Or in application code (Go example)
clientCert, _ := tls.LoadX509KeyPair("client.crt", "client.key")
tlsConfig := &tls.Config{Certificates: []tls.Certificate{clientCert}}
```

## Certificate Validation

### Verify Certificate Chain

```bash
# Verify certificate against CA
openssl verify -CAfile ca.crt cert.pem

# Verify with intermediate certificates
openssl verify -CAfile root-ca.crt -untrusted intermediate.crt cert.pem

# Verify full chain
cat intermediate.crt root.crt > chain.pem
openssl verify -CAfile chain.pem cert.pem
```

### Verify Private Key and Certificate Match

```bash
# Extract modulus from certificate
cert_modulus=$(openssl x509 -in cert.pem -noout -modulus | openssl md5)
echo "Certificate modulus: $cert_modulus"

# Extract modulus from private key
key_modulus=$(openssl rsa -in key.pem -noout -modulus | openssl md5)
echo "Private key modulus: $key_modulus"

# Compare (must match)
if [ "$cert_modulus" = "$key_modulus" ]; then
    echo "✓ Certificate and key match"
else
    echo "✗ Certificate and key DO NOT match"
fi
```

### Verify Certificate Purpose

```bash
# Check Extended Key Usage
openssl x509 -in cert.pem -noout -text | grep -A 1 "Extended Key Usage"

# Server certificates should have:
# TLS Web Server Authentication

# Client certificates should have:
# TLS Web Client Authentication
```

## TLS Handshake Analysis

### Capture TLS Handshake with tcpdump

```bash
# Capture traffic on port 443
sudo tcpdump -i any -w capture.pcap port 443

# Analyze with Wireshark or tshark
tshark -r capture.pcap -Y tls.handshake

# View certificate in handshake
tshark -r capture.pcap -Y tls.handshake.certificate -V
```

### Analyze TLS with ssllabs

```bash
# Online SSL/TLS testing
# Visit: https://www.ssllabs.com/ssltest/

# Or use testssl.sh (command-line)
git clone https://github.com/drwetter/testssl.sh.git
cd testssl.sh
./testssl.sh example.com
```

### Test OCSP Stapling

```bash
# Test if server supports OCSP stapling
openssl s_client -connect example.com:443 -status

# Look for "OCSP Response Status: successful"
```

## Monitoring Certificate Expiry

### Check Expiry for Single Domain

```bash
# Extract expiry date
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -enddate

# Human-readable time remaining
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -enddate | \
  awk -F'=' '{print $2}' | \
  xargs -I {} date -d {} +%s | \
  awk '{print "Days remaining: " int(($1 - systime()) / 86400)}'
```

### Check Multiple Domains

```bash
# domains.txt contains one domain per line
cat domains.txt | while read domain; do
    expiry=$(echo | openssl s_client -connect $domain:443 2>/dev/null | \
      openssl x509 -noout -enddate | cut -d= -f2)
    echo "$domain expires: $expiry"
done
```

### Prometheus Monitoring

**blackbox_exporter configuration:**

```yaml
# blackbox.yml
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      preferred_ip_protocol: ip4
      fail_if_ssl: false
      fail_if_not_ssl: true
```

**Prometheus scrape config:**

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
```

**Alert rule:**

```yaml
# alerts.yml
groups:
  - name: ssl_expiry
    rules:
    - alert: SSLCertExpiringSoon
      expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7
      for: 1h
      labels:
        severity: warning
      annotations:
        summary: "SSL certificate expiring in <7 days"
        description: "{{ $labels.instance }} certificate expires in {{ $value | humanizeDuration }}"

    - alert: SSLCertExpired
      expr: probe_ssl_earliest_cert_expiry - time() <= 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "SSL certificate expired"
        description: "{{ $labels.instance }} certificate has expired"
```

### Nagios/Icinga Check

```bash
#!/bin/bash
# check_ssl_cert.sh

DOMAIN=$1
WARN_DAYS=30
CRIT_DAYS=7

# Get expiry date
EXPIRY=$(echo | openssl s_client -connect $DOMAIN:443 2>/dev/null | \
         openssl x509 -noout -enddate | cut -d= -f2)

# Convert to epoch
EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_EPOCH - $NOW_EPOCH) / 86400 ))

# Check thresholds
if [ $DAYS_LEFT -le $CRIT_DAYS ]; then
    echo "CRITICAL: Certificate expires in $DAYS_LEFT days"
    exit 2
elif [ $DAYS_LEFT -le $WARN_DAYS ]; then
    echo "WARNING: Certificate expires in $DAYS_LEFT days"
    exit 1
else
    echo "OK: Certificate expires in $DAYS_LEFT days"
    exit 0
fi
```

## Advanced Debugging

### Debug TLS with strace

```bash
# Trace openssl command
strace -e trace=read,write,open,connect \
  openssl s_client -connect example.com:443

# Trace application
strace -e trace=network,read,write -p PID
```

### Enable TLS Debug Logging

**Nginx:**

```nginx
error_log /var/log/nginx/error.log debug;

# Generates verbose TLS handshake logs
```

**Apache:**

```apache
LogLevel ssl:trace6

# Logs to error_log with detailed TLS info
```

**Go application:**

```go
// Set GODEBUG environment variable
// GODEBUG=x509roots=1 ./app
// Shows certificate verification details
```

### Test Certificate Revocation

**Check CRL (Certificate Revocation List):**

```bash
# Extract CRL URL from certificate
openssl x509 -in cert.pem -noout -text | grep -A 4 "CRL Distribution"

# Download and check CRL
wget http://crl.example.com/ca.crl
openssl crl -in ca.crl -inform DER -text

# Check if certificate is revoked
openssl crl -in ca.crl -inform DER -noout -text | grep -A 2 "Serial Number: ABC123"
```

**Check OCSP (Online Certificate Status Protocol):**

```bash
# Extract OCSP URL
openssl x509 -in cert.pem -noout -ocsp_uri

# Check OCSP status
openssl ocsp -issuer ca.crt -cert cert.pem \
  -url http://ocsp.example.com -resp_text
```

## Troubleshooting Checklist

When debugging TLS issues, check:

- [ ] Certificate not expired (`openssl x509 -noout -dates`)
- [ ] Hostname matches certificate SANs
- [ ] Certificate chain complete (intermediate certs included)
- [ ] CA certificate in trust store
- [ ] Private key matches certificate
- [ ] TLS 1.2 or 1.3 enabled
- [ ] Strong cipher suites configured
- [ ] Firewall allows port 443
- [ ] SNI configured (shared hosting)
- [ ] Certificate not revoked (CRL/OCSP)
- [ ] System clock correct
- [ ] File permissions correct (key: 600, cert: 644)

For certificate generation issues, see `certificate-generation.md`.
For mTLS-specific debugging, see `mtls-guide.md`.
