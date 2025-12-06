#!/bin/bash
# Generate self-signed certificate with Subject Alternative Names (SANs)

set -e

# Configuration
DOMAIN="${1:-example.com}"
DAYS="${2:-365}"

echo "Generating self-signed certificate for $DOMAIN (valid $DAYS days)"

# Create OpenSSL configuration
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
CN = $DOMAIN

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = www.$DOMAIN
DNS.3 = api.$DOMAIN
IP.1 = 127.0.0.1
IP.2 = 192.168.1.100
EOF

# Generate private key
echo "Generating private key..."
openssl genrsa -out server-key.pem 2048

# Generate certificate signing request (CSR)
echo "Generating CSR..."
openssl req -new -key server-key.pem -out server.csr -config san.cnf

# Self-sign the certificate
echo "Self-signing certificate..."
openssl x509 -req -in server.csr -signkey server-key.pem \
  -out server-cert.pem -days $DAYS -extensions v3_req -extfile san.cnf

# Verify SANs
echo ""
echo "Certificate generated successfully!"
echo ""
echo "Files created:"
echo "  - server-key.pem  (private key)"
echo "  - server-cert.pem (certificate)"
echo "  - server.csr      (CSR)"
echo ""
echo "Subject Alternative Names:"
openssl x509 -in server-cert.pem -noout -text | grep -A 3 "Subject Alternative Name"

echo ""
echo "Certificate expires:"
openssl x509 -in server-cert.pem -noout -enddate

# Cleanup
rm -f server.csr san.cnf

echo ""
echo "Usage with Nginx:"
echo "  ssl_certificate     /path/to/server-cert.pem;"
echo "  ssl_certificate_key /path/to/server-key.pem;"
