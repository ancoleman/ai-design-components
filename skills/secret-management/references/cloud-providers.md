# Cloud Provider Secret Managers

Quick reference for AWS Secrets Manager, GCP Secret Manager, and Azure Key Vault.

## Table of Contents

1. [Comparison Matrix](#comparison-matrix)
2. [AWS Secrets Manager](#aws-secrets-manager)
3. [GCP Secret Manager](#gcp-secret-manager)
4. [Azure Key Vault](#azure-key-vault)
5. [Kubernetes Integration (ESO)](#kubernetes-integration-eso)

## Comparison Matrix

| Feature | AWS Secrets Manager | GCP Secret Manager | Azure Key Vault |
|---------|--------------------|--------------------|-----------------|
| **Pricing** | $0.40/secret/month + $0.05/10k API calls | $0.06/secret version/month + $0.03/10k ops | $0.03/10k ops, Free tier |
| **Rotation** | Automatic (Lambda) | Manual (Cloud Functions) | Automatic (Event Grid) |
| **Versioning** | Yes (auto-versioned) | Yes (explicit versions) | Yes (versions) |
| **Replication** | Multi-region | Global | Multi-region |
| **IAM Integration** | Native (IAM policies) | Native (IAM policies) | Native (RBAC) |
| **Kubernetes** | ESO, CSI driver | ESO, CSI driver | ESO, CSI driver |

## AWS Secrets Manager

### CLI Commands

```bash
# Create secret
aws secretsmanager create-secret \
  --name prod/database/credentials \
  --secret-string '{"username":"admin","password":"secret123"}'

# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id prod/database/credentials \
  --query SecretString --output text

# Update secret
aws secretsmanager update-secret \
  --secret-id prod/database/credentials \
  --secret-string '{"username":"admin","password":"newsecret456"}'

# Enable automatic rotation
aws secretsmanager rotate-secret \
  --secret-id prod/database/credentials \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-secret
```

### IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/*"
    }
  ]
}
```

### Python SDK (boto3)

```python
import boto3
import json

client = boto3.client('secretsmanager', region_name='us-east-1')

# Get secret
response = client.get_secret_value(SecretId='prod/database/credentials')
secret = json.loads(response['SecretString'])

print(f"Username: {secret['username']}")
print(f"Password: {secret['password']}")
```

## GCP Secret Manager

### gcloud Commands

```bash
# Create secret
echo -n "secret-password" | gcloud secrets create db-password \
  --data-file=- \
  --replication-policy=automatic

# Add version
echo -n "new-password" | gcloud secrets versions add db-password \
  --data-file=-

# Access secret
gcloud secrets versions access latest --secret=db-password

# Delete secret
gcloud secrets delete db-password
```

### IAM Binding

```bash
gcloud secrets add-iam-policy-binding db-password \
  --member="serviceAccount:app@project.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Python SDK

```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()

# Access secret
name = "projects/my-project/secrets/db-password/versions/latest"
response = client.access_secret_version(request={"name": name})
secret = response.payload.data.decode('UTF-8')

print(f"Secret: {secret}")
```

## Azure Key Vault

### Azure CLI Commands

```bash
# Create Key Vault
az keyvault create \
  --name my-keyvault \
  --resource-group my-rg \
  --location eastus

# Set secret
az keyvault secret set \
  --vault-name my-keyvault \
  --name db-password \
  --value "secret123"

# Get secret
az keyvault secret show \
  --vault-name my-keyvault \
  --name db-password \
  --query value --output tsv

# Enable soft-delete
az keyvault update \
  --name my-keyvault \
  --enable-soft-delete true \
  --retention-days 90
```

### Access Policy

```bash
az keyvault set-policy \
  --name my-keyvault \
  --spn <service-principal-id> \
  --secret-permissions get list
```

### Python SDK

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://my-keyvault.vault.azure.net", credential=credential)

# Get secret
secret = client.get_secret("db-password")
print(f"Secret: {secret.value}")
```

## Kubernetes Integration (ESO)

### AWS Secrets Manager + ESO

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: app-sa
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
  target:
    name: db-credentials
  data:
  - secretKey: username
    remoteRef:
      key: prod/database/credentials
      property: username
  - secretKey: password
    remoteRef:
      key: prod/database/credentials
      property: password
```

### GCP Secret Manager + ESO

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: gcp-secrets
spec:
  provider:
    gcpsm:
      projectID: "my-project-123"
      auth:
        workloadIdentity:
          clusterLocation: us-central1
          clusterName: production-cluster
          serviceAccountRef:
            name: app-sa
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: gcp-secrets
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: db-password
      version: latest
```

### Azure Key Vault + ESO

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: azure-secrets
spec:
  provider:
    azurekv:
      vaultUrl: "https://my-keyvault.vault.azure.net"
      authType: WorkloadIdentity
      serviceAccountRef:
        name: app-sa
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: azure-secrets
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: db-password
```
