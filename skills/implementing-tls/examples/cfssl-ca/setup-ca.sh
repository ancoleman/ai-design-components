#!/bin/bash
# Setup internal Certificate Authority with CFSSL

set -e

echo "Setting up internal CA with CFSSL..."

# Create CA configuration
cat > ca-config.json <<'EOF'
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "server": {
        "expiry": "8760h",
        "usages": ["signing", "key encipherment", "server auth"]
      },
      "client": {
        "expiry": "8760h",
        "usages": ["signing", "key encipherment", "client auth"]
      },
      "peer": {
        "expiry": "8760h",
        "usages": ["signing", "key encipherment", "server auth", "client auth"]
      }
    }
  }
}
EOF

# Create CA CSR
cat > ca-csr.json <<'EOF'
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

# Generate CA
echo "Generating CA certificate..."
cfssl genkey -initca ca-csr.json | cfssljson -bare ca

echo ""
echo "CA created successfully!"
echo "Files:"
echo "  - ca.pem (CA certificate)"
echo "  - ca-key.pem (CA private key)"
echo "  - ca-config.json (signing profiles)"
echo ""
echo "To generate server certificate:"
echo "  cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \\"
echo "    -config=ca-config.json -profile=server \\"
echo "    server-csr.json | cfssljson -bare server"
