# Secret Rotation Patterns

Detailed workflows for rotating static secrets, dynamic credentials, and TLS certificates.

## Table of Contents

1. [Why Rotate Secrets](#why-rotate-secrets)
2. [Versioned Static Secrets](#versioned-static-secrets)
3. [Dynamic Database Credentials](#dynamic-database-credentials)
4. [TLS Certificate Rotation](#tls-certificate-rotation)
5. [Cloud Provider Credentials](#cloud-provider-credentials)
6. [Automation Scripts](#automation-scripts)

## Why Rotate Secrets

**Security Benefits:**
- Limits blast radius of compromised credentials
- Reduces window of unauthorized access
- Meets compliance requirements (SOC 2, ISO 27001, PCI DSS)
- Detects dormant credential usage

**Industry Standards:**
- **PCI DSS**: Rotate passwords every 90 days
- **SOC 2**: Document rotation policy and evidence
- **ISO 27001**: Regular credential review and rotation
- **NIST**: Recommend rotation on suspicion of compromise

## Versioned Static Secrets

### Pattern: Blue/Green Rotation

For third-party API keys with no auto-rotation support.

**Steps:**

1. **Create New Secret Version**
```bash
# Vault KV v2 (versioned)
vault kv put secret/api-keys/stripe \
  key=sk_live_NEW_KEY_v2 \
  created_at="2025-12-03T10:00:00Z" \
  rotated_by="ops-team"

# Verify version created
vault kv metadata get secret/api-keys/stripe
# current_version: 2
```

2. **Update Staging Environment**
```bash
# Update Kubernetes Secret in staging
kubectl set env deployment/api-service -n staging \
  STRIPE_API_KEY=sk_live_NEW_KEY_v2

# Or update ExternalSecret to fetch version 2
kubectl patch externalsecret stripe-key -n staging --type merge -p '
spec:
  data:
  - secretKey: key
    remoteRef:
      key: secret/data/api-keys/stripe
      property: key
      version: 2
'
```

3. **Monitor for Errors (24-48 Hours)**
```bash
# Check application logs
kubectl logs -f deployment/api-service -n staging | grep -i "stripe\|error"

# Monitor error rates
curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~\"5..\"}[5m])"

# Verify API calls succeed
curl https://api.stripe.com/v1/charges \
  -u sk_live_NEW_KEY_v2: \
  -d amount=100 \
  -d currency=usd \
  -d source=tok_test
```

4. **Gradual Production Rollout**
```bash
# Update 10% of pods
kubectl patch deployment api-service -n production -p '
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
'
kubectl set env deployment/api-service -n production STRIPE_API_KEY=sk_live_NEW_KEY_v2

# Wait 1 hour, check metrics
sleep 3600
kubectl top pods -n production -l app=api-service

# Update remaining pods
kubectl rollout status deployment/api-service -n production
```

5. **Revoke Old Secret (After 7 Days)**
```bash
# Revoke at provider
# Stripe: Dashboard → API Keys → Revoke old key

# Delete old version from Vault
vault kv metadata delete secret/api-keys/stripe -versions=1

# Document rotation
vault kv put secret/rotation-log/stripe-2025-12 \
  old_key=sk_live_OLD_KEY_v1 \
  new_key=sk_live_NEW_KEY_v2 \
  rotated_at="2025-12-03T10:00:00Z" \
  revoked_at="2025-12-10T10:00:00Z"
```

### Automation Script

```bash
#!/bin/bash
# rotate-static-secret.sh

SECRET_PATH=$1  # e.g., "secret/api-keys/stripe"
NEW_VALUE=$2

echo "Rotating secret: $SECRET_PATH"

# Write new version
vault kv put "$SECRET_PATH" \
  key="$NEW_VALUE" \
  created_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  rotated_by="$(whoami)"

# Get new version number
NEW_VERSION=$(vault kv metadata get -format=json "$SECRET_PATH" | jq -r '.current_version')
echo "New version: $NEW_VERSION"

# Update staging
kubectl set env deployment/api-service -n staging \
  API_KEY="$NEW_VALUE"

echo "Secret rotated. Monitor staging for 24-48 hours before production rollout."
```

## Dynamic Database Credentials

### Pattern: Automatic Lease Renewal

Vault auto-generates credentials with short TTL (1 hour).

**Initial Setup:**

```bash
# 1. Enable database engine
vault secrets enable database

# 2. Configure PostgreSQL connection
vault write database/config/postgres \
  plugin_name=postgresql-database-plugin \
  allowed_roles="app-role" \
  connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb?sslmode=require" \
  username="vault-admin" \
  password="vault-admin-password"

# 3. Create role with TTL
vault write database/roles/app-role \
  db_name=postgres \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"
```

**Application Integration (Python):**

```python
import hvac
import time
import threading
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

class VaultDatabaseClient:
    def __init__(self, vault_url, role):
        self.client = hvac.Client(url=vault_url)
        self.role = role
        self.lease_id = None
        self.engine = None

        # Authenticate
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as f:
            jwt = f.read()
        self.client.auth.kubernetes(role='app-role', jwt=jwt)

        # Get initial credentials
        self._refresh_credentials()

        # Start renewal thread
        threading.Thread(target=self._renewal_loop, daemon=True).start()

    def _refresh_credentials(self):
        response = self.client.secrets.database.generate_credentials(name=self.role)
        username = response['data']['username']
        password = response['data']['password']
        self.lease_id = response['lease_id']
        self.lease_duration = response['lease_duration']

        # Create new database engine
        if self.engine:
            self.engine.dispose()
        self.engine = create_engine(
            f"postgresql://{username}:{password}@postgres:5432/mydb",
            poolclass=NullPool  # Don't pool connections (credentials rotate)
        )

        print(f"Credentials refreshed. Lease ID: {self.lease_id}, TTL: {self.lease_duration}s")

    def _renewal_loop(self):
        while True:
            # Renew at 67% of lease duration
            renewal_time = self.lease_duration * 0.67
            time.sleep(renewal_time)

            try:
                # Attempt renewal
                self.client.sys.renew_lease(self.lease_id)
                print(f"Lease renewed: {self.lease_id}")
            except Exception as e:
                print(f"Renewal failed: {e}. Requesting new credentials...")
                self._refresh_credentials()

    def query(self, sql):
        with self.engine.connect() as conn:
            return conn.execute(sql).fetchall()

# Usage
db_client = VaultDatabaseClient('https://vault.example.com', 'app-role')
users = db_client.query("SELECT * FROM users")
```

**Kubernetes with VSO:**

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: postgres-creds
  namespace: production
spec:
  vaultAuthRef: vault-auth
  mount: database
  path: creds/app-role
  renewalPercent: 67  # Renew at 67% of TTL
  destination:
    create: true
    name: dynamic-db-creds
  rolloutRestartTargets:
  - kind: Deployment
    name: app  # Auto-restart on credential change
```

**Monitoring:**

```bash
# Check active leases
vault list sys/leases/lookup/database/creds/app-role

# View lease details
vault lease lookup database/creds/app-role/<LEASE_ID>

# Force revoke (emergency)
vault lease revoke database/creds/app-role/<LEASE_ID>

# Revoke all leases for role
vault lease revoke -prefix database/creds/app-role
```

## TLS Certificate Rotation

### Pattern: cert-manager + Vault PKI

Automatic certificate issuance and renewal.

**Vault PKI Setup:**

```bash
# 1. Enable PKI engine
vault secrets enable pki
vault secrets tune -max-lease-ttl=8760h pki

# 2. Generate root CA
vault write pki/root/generate/internal \
  common_name=example.com \
  ttl=8760h

# 3. Configure URLs
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com/v1/pki/crl"

# 4. Create role
vault write pki/roles/web-server \
  allowed_domains=example.com \
  allow_subdomains=true \
  max_ttl=72h \
  key_type=rsa \
  key_bits=2048
```

**cert-manager Integration:**

```yaml
# 1. Issuer (Vault-backed)
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: vault-issuer
  namespace: production
spec:
  vault:
    server: https://vault.example.com
    path: pki/sign/web-server
    auth:
      kubernetes:
        role: cert-manager
        mountPath: /v1/auth/kubernetes
        secretRef:
          name: cert-manager-vault-token
          key: token

---
# 2. Certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: app-tls
  namespace: production
spec:
  secretName: app-tls-secret
  duration: 24h
  renewBefore: 8h  # Renew 8 hours before expiration (67% of 24h)
  issuerRef:
    name: vault-issuer
  dnsNames:
  - app.example.com
  - www.app.example.com
```

**Automatic Renewal:**

cert-manager automatically:
1. Monitors certificate expiration
2. Requests new certificate 8 hours before expiry
3. Updates Kubernetes Secret (app-tls-secret)
4. Triggers pod reload (via Reloader or similar)

**Pod Reload with Reloader:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  annotations:
    reloader.stakater.com/auto: "true"  # Auto-reload on Secret change
spec:
  template:
    spec:
      containers:
      - name: app
        volumeMounts:
        - name: tls
          mountPath: /etc/tls
      volumes:
      - name: tls
        secret:
          secretName: app-tls-secret
```

## Cloud Provider Credentials

### Pattern: AWS IAM with Vault

**Vault AWS Engine Setup:**

```bash
# 1. Enable AWS engine
vault secrets enable aws

# 2. Configure root credentials
vault write aws/config/root \
  access_key=AKIAIOSFODNN7EXAMPLE \
  secret_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
  region=us-east-1

# 3. Create role with inline policy
vault write aws/roles/s3-access \
  credential_type=iam_user \
  policy_document=-<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
EOF
  default_ttl=15m \
  max_ttl=1h
```

**Application Integration:**

```python
import boto3
import hvac
import time
import threading

class VaultAWSClient:
    def __init__(self, vault_url, aws_role):
        self.client = hvac.Client(url=vault_url)
        self.aws_role = aws_role
        self.lease_id = None

        # Authenticate with Vault
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as f:
            jwt = f.read()
        self.client.auth.kubernetes(role='app-role', jwt=jwt)

        # Get initial AWS credentials
        self._refresh_credentials()

        # Start renewal thread
        threading.Thread(target=self._renewal_loop, daemon=True).start()

    def _refresh_credentials(self):
        response = self.client.secrets.aws.generate_credentials(name=self.aws_role)
        self.access_key = response['data']['access_key']
        self.secret_key = response['data']['secret_key']
        self.lease_id = response['lease_id']
        self.lease_duration = response['lease_duration']

        # Update boto3 session
        self.session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
        self.s3 = self.session.client('s3')

        print(f"AWS credentials refreshed. Lease: {self.lease_id}, TTL: {self.lease_duration}s")

    def _renewal_loop(self):
        while True:
            renewal_time = self.lease_duration * 0.67
            time.sleep(renewal_time)

            try:
                self.client.sys.renew_lease(self.lease_id)
                print(f"Lease renewed: {self.lease_id}")
            except Exception as e:
                print(f"Renewal failed. Requesting new credentials...")
                self._refresh_credentials()

    def upload_file(self, bucket, key, file_path):
        self.s3.upload_file(file_path, bucket, key)

# Usage
aws_client = VaultAWSClient('https://vault.example.com', 's3-access')
aws_client.upload_file('my-bucket', 'data.csv', '/tmp/data.csv')
```

## Automation Scripts

### Comprehensive Rotation Script

```python
#!/usr/bin/env python3
"""
rotate_secrets.py

Automated secret rotation script for multiple secret types.

Usage:
  python rotate_secrets.py --type static --path secret/api-keys/stripe --value sk_live_NEW
  python rotate_secrets.py --type database --role app-role --ttl 1h
"""

import argparse
import hvac
import time
from datetime import datetime

class SecretRotator:
    def __init__(self, vault_url, vault_token):
        self.client = hvac.Client(url=vault_url, token=vault_token)

    def rotate_static(self, path, new_value):
        """Rotate static secret with versioning."""
        print(f"Rotating static secret: {path}")

        # Write new version
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path.replace('secret/data/', '').replace('secret/', ''),
            secret={'key': new_value},
            mount_point='secret'
        )

        # Get metadata
        metadata = self.client.secrets.kv.v2.read_secret_metadata(
            path=path.replace('secret/data/', '').replace('secret/', ''),
            mount_point='secret'
        )

        version = metadata['data']['current_version']
        print(f"✓ New version created: {version}")
        print(f"✓ Previous version available for rollback")

        return version

    def rotate_database(self, role, ttl='1h'):
        """Generate new dynamic database credentials."""
        print(f"Generating new database credentials for role: {role}")

        response = self.client.secrets.database.generate_credentials(name=role)

        print(f"✓ Username: {response['data']['username']}")
        print(f"✓ Lease ID: {response['lease_id']}")
        print(f"✓ TTL: {response['lease_duration']}s")

        return response

    def revoke_old_version(self, path, versions_to_keep=2):
        """Delete old versions of static secret."""
        print(f"Cleaning up old versions: {path}")

        metadata = self.client.secrets.kv.v2.read_secret_metadata(
            path=path.replace('secret/data/', '').replace('secret/', ''),
            mount_point='secret'
        )

        current_version = metadata['data']['current_version']
        versions_to_delete = list(range(1, current_version - versions_to_keep + 1))

        if versions_to_delete:
            self.client.secrets.kv.v2.delete_secret_versions(
                path=path.replace('secret/data/', '').replace('secret/', ''),
                versions=versions_to_delete,
                mount_point='secret'
            )
            print(f"✓ Deleted versions: {versions_to_delete}")
        else:
            print("✓ No old versions to delete")

def main():
    parser = argparse.ArgumentParser(description='Rotate secrets in Vault')
    parser.add_argument('--type', required=True, choices=['static', 'database'])
    parser.add_argument('--path', help='Secret path (for static secrets)')
    parser.add_argument('--value', help='New secret value (for static secrets)')
    parser.add_argument('--role', help='Database role name (for dynamic secrets)')
    parser.add_argument('--ttl', default='1h', help='TTL for dynamic secrets')
    parser.add_argument('--vault-url', default='https://vault.example.com')
    parser.add_argument('--vault-token', required=True)

    args = parser.parse_args()

    rotator = SecretRotator(args.vault_url, args.vault_token)

    if args.type == 'static':
        if not args.path or not args.value:
            parser.error("--path and --value required for static secrets")
        rotator.rotate_static(args.path, args.value)

        # Wait 7 days before cleanup (manual trigger)
        print("\nRun the following command in 7 days to clean up old versions:")
        print(f"  python rotate_secrets.py --type cleanup --path {args.path} --vault-token <TOKEN>")

    elif args.type == 'database':
        if not args.role:
            parser.error("--role required for database secrets")
        rotator.rotate_database(args.role, args.ttl)

if __name__ == '__main__':
    main()
```

### Validation Script

```bash
#!/bin/bash
# validate_rotation.sh

set -e

SECRET_PATH=$1
EXPECTED_VERSION=$2

echo "Validating secret rotation: $SECRET_PATH"

# Check Vault
CURRENT_VERSION=$(vault kv metadata get -format=json "$SECRET_PATH" | jq -r '.current_version')

if [ "$CURRENT_VERSION" -eq "$EXPECTED_VERSION" ]; then
  echo "✓ Vault version correct: $CURRENT_VERSION"
else
  echo "✗ Vault version mismatch. Expected: $EXPECTED_VERSION, Got: $CURRENT_VERSION"
  exit 1
fi

# Check Kubernetes Secret (if using ESO)
K8S_SECRET_NAME=$(echo "$SECRET_PATH" | sed 's/\//-/g')
K8S_VERSION=$(kubectl get secret "$K8S_SECRET_NAME" -o jsonpath='{.metadata.annotations.external-secrets\.io/secret-version}')

if [ "$K8S_VERSION" -eq "$EXPECTED_VERSION" ]; then
  echo "✓ Kubernetes Secret synced: $K8S_VERSION"
else
  echo "✗ Kubernetes Secret not synced. Expected: $EXPECTED_VERSION, Got: $K8S_VERSION"
  exit 1
fi

echo "✓ Rotation validated successfully"
```
