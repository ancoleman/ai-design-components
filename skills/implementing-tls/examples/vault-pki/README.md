# HashiCorp Vault PKI Examples

Examples for dynamic certificate issuance with Vault PKI.

## Setup PKI Engine

```bash
# Enable PKI secrets engine
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write -field=certificate pki/root/generate/internal \
  common_name="Example Corp Root CA" \
  ttl=87600h > root_ca.crt

# Configure URLs
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com:8200/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"
```

## Create Role

```bash
# Role for web servers
vault write pki/roles/example-dot-com \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl="720h" \
  key_usage="DigitalSignature,KeyEncipherment" \
  ext_key_usage="ServerAuth"
```

## Issue Certificate

```bash
# Issue certificate
vault write pki/issue/example-dot-com \
  common_name="api.example.com" \
  ttl="24h"

# Returns: certificate, private_key, ca_chain, serial_number
```

## Automatic Renewal with Vault Agent

See Vault Agent configuration in `vault-agent.hcl` for automatic certificate renewal.

Reference: `../../references/automation-patterns.md` for complete Vault PKI setup.
