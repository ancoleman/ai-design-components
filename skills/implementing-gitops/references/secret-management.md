# Secret Management Integration

Secure secret handling in GitOps workflows.


## Table of Contents

- [Sealed Secrets](#sealed-secrets)
  - [Installation](#installation)
  - [Create Sealed Secret](#create-sealed-secret)
  - [Sealed Secret Manifest](#sealed-secret-manifest)
- [External Secrets Operator](#external-secrets-operator)
  - [Installation](#installation)
  - [Vault SecretStore](#vault-secretstore)
  - [ExternalSecret](#externalsecret)
- [SOPS Encryption](#sops-encryption)
  - [Installation](#installation)
  - [Encrypt File with SOPS](#encrypt-file-with-sops)
  - [Flux SOPS Integration](#flux-sops-integration)

## Sealed Secrets

### Installation

```bash
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Install kubeseal CLI
brew install kubeseal
```

### Create Sealed Secret

```bash
# Create secret
kubectl create secret generic mysecret \
  --from-literal=password=mypassword \
  --dry-run=client -o yaml > secret.yaml

# Seal the secret
kubeseal -f secret.yaml -w sealedsecret.yaml

# Commit sealed secret to Git
git add sealedsecret.yaml
git commit -m "Add sealed secret"
```

### Sealed Secret Manifest

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: myapp
spec:
  encryptedData:
    password: AgBy3i4OJSWK+PiTySY...
```

## External Secrets Operator

### Installation

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets-system --create-namespace
```

### Vault SecretStore

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: myapp
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp"
```

### ExternalSecret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
  namespace: myapp
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-password
    remoteRef:
      key: secret/myapp/database
      property: password
  - secretKey: api-key
    remoteRef:
      key: secret/myapp/api
      property: key
```

## SOPS Encryption

### Installation

```bash
# Install SOPS
brew install sops

# Install age for encryption
brew install age

# Generate age key
age-keygen -o key.txt
```

### Encrypt File with SOPS

```yaml
# secrets/prod-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
stringData:
  database-url: postgresql://prod-db:5432/myapp
  api-key: sk_prod_abc123xyz
```

```bash
# Encrypt with age
sops --encrypt --age $(cat key.txt.pub) secrets/prod-secrets.yaml > secrets/prod-secrets.enc.yaml

# Commit encrypted file
git add secrets/prod-secrets.enc.yaml
```

### Flux SOPS Integration

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-secrets
  namespace: flux-system
spec:
  interval: 10m
  path: ./secrets
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
  decryption:
    provider: sops
    secretRef:
      name: sops-age
---
apiVersion: v1
kind: Secret
metadata:
  name: sops-age
  namespace: flux-system
stringData:
  age.agekey: |
    # created: 2025-01-01T00:00:00Z
    # public key: age1...
    AGE-SECRET-KEY-1...
```
