# Certificate Generation Guide

Comprehensive examples for generating TLS certificates across different tools and use cases.

## Table of Contents

1. [Self-Signed Certificates with OpenSSL](#self-signed-certificates-with-openssl)
2. [Internal CA with CFSSL](#internal-ca-with-cfssl)
3. [Local Development with mkcert](#local-development-with-mkcert)
4. [Subject Alternative Names (SANs)](#subject-alternative-names-sans)

## Self-Signed Certificates with OpenSSL

### Quick Single-Line Generation

```bash
# Generate self-signed certificate + key (valid 365 days)
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout server-key.pem -out server-cert.pem \
  -days 365 -subj "/CN=example.com"
```

### Production-Quality with SANs

Create configuration file with Subject Alternative Names:

```bash
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
```

Generate certificate:

```bash
# Generate private key
openssl genrsa -out server-key.pem 2048

# Generate CSR
openssl req -new -key server-key.pem -out server.csr -config san.cnf

# Self-sign the certificate
openssl x509 -req -in server.csr -signkey server-key.pem \
  -out server-cert.pem -days 365 -extensions v3_req -extfile san.cnf

# Verify SANs
openssl x509 -in server-cert.pem -noout -text | grep -A 3 "Subject Alternative Name"
```

## Internal CA with CFSSL

### Installation

```bash
# Linux/macOS
curl -L https://github.com/cloudflare/cfssl/releases/download/v1.6.4/cfssl_1.6.4_linux_amd64 -o /usr/local/bin/cfssl
curl -L https://github.com/cloudflare/cfssl/releases/download/v1.6.4/cfssljson_1.6.4_linux_amd64 -o /usr/local/bin/cfssljson
chmod +x /usr/local/bin/cfssl /usr/local/bin/cfssljson

# Package managers
# Ubuntu: apt install golang-cfssl
# macOS: brew install cfssl
```

### Create CA Configuration

**ca-config.json** - Signing profiles:

```json
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
```

**ca-csr.json** - CA certificate request:

```json
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
```

### Generate CA Certificate

```bash
cfssl genkey -initca ca-csr.json | cfssljson -bare ca
# Produces: ca.pem (cert), ca-key.pem (private key), ca.csr
```

### Generate Server Certificate

**server-csr.json**:

```json
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
```

Generate and sign:

```bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=server \
  server-csr.json | cfssljson -bare server
# Produces: server.pem (cert), server-key.pem (private key)
```

### Generate Client Certificate (mTLS)

**client-csr.json**:

```json
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
```

Generate and sign:

```bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=client \
  client-csr.json | cfssljson -bare client
# Produces: client.pem (cert), client-key.pem (private key)
```

## Local Development with mkcert

### Installation

```bash
# macOS
brew install mkcert
brew install nss  # For Firefox support

# Linux (Debian/Ubuntu)
sudo apt install libnss3-tools
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64
sudo mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert
sudo chmod +x /usr/local/bin/mkcert

# Windows (via Chocolatey)
choco install mkcert
```

### Generate Trusted Local Certificates

```bash
# Install local CA in system trust store
mkcert -install

# Generate certificate for local domains
mkcert example.com "*.example.com" localhost 127.0.0.1 ::1
# Produces: example.com+4.pem (cert) and example.com+4-key.pem (key)
# Already trusted by browser and system!

# Use with web server
nginx -c nginx.conf  # Reference the generated .pem files
```

### View CA Location

```bash
# Show CA certificate location
mkcert -CAROOT
# Example: /Users/username/Library/Application Support/mkcert
```

## Subject Alternative Names (SANs)

### Why SANs Matter

Modern browsers ignore the Common Name (CN) field and require SANs. Without SANs, certificate validation fails even if CN matches.

### SAN Configuration Examples

**For multiple domains:**

```ini
[alt_names]
DNS.1 = example.com
DNS.2 = www.example.com
DNS.3 = api.example.com
DNS.4 = app.example.com
```

**For wildcard + specific domains:**

```ini
[alt_names]
DNS.1 = example.com
DNS.2 = *.example.com
DNS.3 = *.internal.example.com
```

**For IP addresses:**

```ini
[alt_names]
IP.1 = 192.168.1.100
IP.2 = 10.0.0.5
```

**Combined (domains + IPs):**

```ini
[alt_names]
DNS.1 = example.com
DNS.2 = localhost
IP.1 = 127.0.0.1
IP.2 = ::1
```

### Verify SANs in Certificate

```bash
# View SANs
openssl x509 -in cert.pem -noout -text | grep -A 3 "Subject Alternative Name"

# Or with verbose output
openssl x509 -in cert.pem -noout -text | grep -A 10 "X509v3 extensions"
```

## Certificate Verification

### Verify Certificate Contents

```bash
# View all certificate details
openssl x509 -in cert.pem -noout -text

# Check expiration dates
openssl x509 -in cert.pem -noout -dates

# Check issuer
openssl x509 -in cert.pem -noout -issuer

# Check subject
openssl x509 -in cert.pem -noout -subject

# Check fingerprint
openssl x509 -in cert.pem -noout -fingerprint -sha256
```

### Verify Certificate Chain

```bash
# Verify against CA
openssl verify -CAfile ca.crt cert.pem

# Verify with intermediate certificates
openssl verify -CAfile root-ca.crt -untrusted intermediate.crt cert.pem
```

### Verify Key and Certificate Match

```bash
# Certificate modulus
cert_modulus=$(openssl x509 -in cert.pem -noout -modulus | md5sum)

# Key modulus
key_modulus=$(openssl rsa -in key.pem -noout -modulus | md5sum)

# Compare (must match)
if [ "$cert_modulus" = "$key_modulus" ]; then
  echo "Certificate and key match"
else
  echo "Mismatch - cert and key do not pair"
fi
```

## Advanced: Certificate Signing Request (CSR)

### Generate CSR for Commercial CA

```bash
# Generate private key
openssl genrsa -out server-key.pem 2048

# Create CSR config
cat > csr.cnf <<EOF
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
emailAddress = admin@example.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com
DNS.2 = www.example.com
EOF

# Generate CSR
openssl req -new -key server-key.pem -out server.csr -config csr.cnf

# Verify CSR
openssl req -in server.csr -noout -text

# Submit CSR to CA (DigiCert, GlobalSign, etc.)
# CA will return signed certificate
```

## Best Practices

1. **Key Size**: Use RSA 2048-bit minimum (4096-bit for CAs)
2. **Validity Period**:
   - Development: 1-5 years
   - Production public: 90 days (Let's Encrypt standard)
   - Internal: 1-2 years
3. **Always Include SANs**: Required by modern browsers
4. **Protect Private Keys**:
   - File permissions: 600 (owner read/write only)
   - Never commit to version control
   - Use secret management tools (Vault, Sealed Secrets)
5. **Certificate Transparency**: Public certificates are logged
6. **Hash Algorithm**: Use SHA-256 minimum (SHA-1 deprecated)

## Troubleshooting

### Common Generation Errors

**"unable to write random state"**
- Solution: Ensure write permissions to home directory

**"No subject given"**
- Solution: Provide -subj flag or configuration file

**"req_extensions not found"**
- Solution: Verify [v3_req] section in config file

**"SANs not present in certificate"**
- Solution: Ensure -extensions v3_req -extfile san.cnf in signing command

For runtime certificate issues, see `debugging-tls.md`.
