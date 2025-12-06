# mTLS with Nginx Examples

Mutual TLS (mTLS) configuration examples for Nginx.

## Prerequisites

Generate certificates using CFSSL (see `../cfssl-ca/`):

```bash
# CA certificate
cfssl genkey -initca ca-csr.json | cfssljson -bare ca

# Server certificate
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=server \
  server-csr.json | cfssljson -bare server

# Client certificate
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=client \
  client-csr.json | cfssljson -bare client
```

## Test with curl

```bash
# mTLS request
curl https://api.example.com/endpoint \
  --cert client.pem \
  --key client-key.pem \
  --cacert ca.pem

# Verbose output
curl -v https://api.example.com/endpoint \
  --cert client.pem \
  --key client-key.pem \
  --cacert ca.pem
```

## Test with OpenSSL

```bash
openssl s_client -connect api.example.com:443 \
  -cert client.pem \
  -key client-key.pem \
  -CAfile ca.pem
```

See `../../references/mtls-guide.md` for complete mTLS implementation guide.
