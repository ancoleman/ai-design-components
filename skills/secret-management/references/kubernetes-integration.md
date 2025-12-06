# Kubernetes Secret Integration

Comprehensive guide to integrating secret management with Kubernetes using External Secrets Operator, Secrets Store CSI Driver, and Vault Secrets Operator.

## Table of Contents

1. [Integration Approaches](#integration-approaches)
2. [External Secrets Operator (ESO)](#external-secrets-operator-eso)
3. [Secrets Store CSI Driver](#secrets-store-csi-driver)
4. [Vault Secrets Operator (VSO)](#vault-secrets-operator-vso)
5. [Comparison Matrix](#comparison-matrix)
6. [Best Practices](#best-practices)

## Integration Approaches

### Native Kubernetes Secrets (Baseline)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  username: YWRtaW4=  # base64("admin")
  password: cGFzc3dvcmQ=  # base64("password")
```

**Problems:**
- Base64 is NOT encryption
- Secrets stored in etcd (encrypted at rest if enabled)
- Manual rotation required
- No audit trail
- Secrets in Git (if committed)

**Solution:** Use external secret stores + sync operators.

### External Secret Stores

```
┌─────────────────────────────────────────────────────┐
│         External Secret Store Integrations          │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────┐         │
│  │   External Secrets Operator (ESO)      │         │
│  │  ├── Syncs from 30+ providers          │         │
│  │  ├── Creates Kubernetes Secrets        │         │
│  │  └── Polling-based refresh             │         │
│  └────────────────────────────────────────┘         │
│                                                      │
│  ┌────────────────────────────────────────┐         │
│  │   Secrets Store CSI Driver             │         │
│  │  ├── Mounts secrets as files           │         │
│  │  ├── No Kubernetes Secret creation     │         │
│  │  └── Watch-based refresh               │         │
│  └────────────────────────────────────────┘         │
│                                                      │
│  ┌────────────────────────────────────────┐         │
│  │   Vault Secrets Operator (VSO)         │         │
│  │  ├── Vault-specific CRDs               │         │
│  │  ├── Dynamic secret renewal            │         │
│  │  └─ Kubernetes-native experience       │         │
│  └────────────────────────────────────────┘         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## External Secrets Operator (ESO)

### Installation

```bash
# Helm installation
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets-system \
  --create-namespace

# Verify installation
kubectl get pods -n external-secrets-system
```

### Core Resources

**SecretStore** (Namespace-scoped)
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "app-role"
          serviceAccountRef:
            name: app-sa
```

**ClusterSecretStore** (Cluster-wide)
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-global
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "cluster-admin-role"
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets-system
```

**ExternalSecret**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h  # Poll every hour
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: db-credentials  # Kubernetes Secret name
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: secret/data/database/config
      property: username
  - secretKey: password
    remoteRef:
      key: secret/data/database/config
      property: password
```

### Multi-Provider Examples

**AWS Secrets Manager**
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
```

**GCP Secret Manager**
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
```

**Azure Key Vault**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: azure-secrets
spec:
  provider:
    azurekv:
      vaultUrl: "https://my-vault.vault.azure.net"
      authType: WorkloadIdentity
      serviceAccountRef:
        name: app-sa
```

### Advanced Features

**Secret Templating**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-config
spec:
  secretStoreRef:
    name: vault-backend
  target:
    name: app-config
    template:
      type: Opaque
      data:
        config.yaml: |
          database:
            url: postgresql://{{ .username }}:{{ .password }}@postgres:5432/mydb
          api_key: {{ .api_key }}
  data:
  - secretKey: username
    remoteRef:
      key: secret/data/database/config
      property: username
  - secretKey: password
    remoteRef:
      key: secret/data/database/config
      property: password
  - secretKey: api_key
    remoteRef:
      key: secret/data/api/keys
      property: stripe_key
```

**DataFrom (Fetch All Keys)**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: all-secrets
spec:
  secretStoreRef:
    name: vault-backend
  target:
    name: all-secrets
  dataFrom:
  - extract:
      key: secret/data/myapp/config  # Fetch all keys from this path
```

**PushSecret (Sync TO External Store)**
```yaml
apiVersion: external-secrets.io/v1alpha1
kind: PushSecret
metadata:
  name: push-credentials
spec:
  refreshInterval: 10m
  secretStoreRefs:
  - name: vault-backend
    kind: SecretStore
  selector:
    secret:
      name: local-secret  # Kubernetes Secret to push
  data:
  - match:
      secretKey: username
      remoteRef:
        remoteKey: secret/data/synced/credentials
        property: username
```

## Secrets Store CSI Driver

### Installation

```bash
# Install CSI driver
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver \
  --namespace kube-system

# Install Vault provider
kubectl apply -f https://raw.githubusercontent.com/hashicorp/vault-csi-provider/main/deployment/vault-csi-provider.yaml
```

### SecretProviderClass (Vault)

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-database
  namespace: production
spec:
  provider: vault
  parameters:
    vaultAddress: "https://vault.example.com"
    roleName: "app-role"
    vaultSkipTLSVerify: "false"
    objects: |
      - objectName: "db-username"
        secretPath: "secret/data/database/config"
        secretKey: "username"
      - objectName: "db-password"
        secretPath: "secret/data/database/config"
        secretKey: "password"
```

### Pod with CSI Volume

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: production
spec:
  serviceAccountName: app-sa
  containers:
  - name: app
    image: myapp:latest
    volumeMounts:
    - name: secrets-store
      mountPath: "/mnt/secrets"
      readOnly: true
    env:
    - name: DB_USERNAME_FILE
      value: /mnt/secrets/db-username
    - name: DB_PASSWORD_FILE
      value: /mnt/secrets/db-password
  volumes:
  - name: secrets-store
    csi:
      driver: secrets-store.csi.k8s.io
      readOnly: true
      volumeAttributes:
        secretProviderClass: "vault-database"
```

### Sync to Kubernetes Secret (Optional)

```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-database
spec:
  provider: vault
  secretObjects:
  - secretName: db-credentials
    type: Opaque
    data:
    - objectName: db-username
      key: username
    - objectName: db-password
      key: password
  parameters:
    vaultAddress: "https://vault.example.com"
    roleName: "app-role"
    objects: |
      - objectName: "db-username"
        secretPath: "secret/data/database/config"
        secretKey: "username"
      - objectName: "db-password"
        secretPath: "secret/data/database/config"
        secretKey: "password"
```

### Auto-Rotation Detection

Application code to watch for file changes:

```python
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SecretReloader(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == "/mnt/secrets/db-password":
            print("Secret rotated, reloading database connection...")
            reload_database_connection()

observer = Observer()
observer.schedule(SecretReloader(), "/mnt/secrets", recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

## Vault Secrets Operator (VSO)

### Installation

```bash
# Helm installation
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault-secrets-operator hashicorp/vault-secrets-operator \
  --namespace vault-secrets-operator-system \
  --create-namespace
```

### VaultConnection

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultConnection
metadata:
  name: vault-connection
  namespace: production
spec:
  address: "https://vault.example.com:8200"
  skipTLSVerify: false
  caCertSecretRef: vault-ca-cert
```

### VaultAuth

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  name: vault-auth
  namespace: production
spec:
  vaultConnectionRef: vault-connection
  method: kubernetes
  mount: kubernetes
  kubernetes:
    role: app-role
    serviceAccount: app-sa
```

### VaultStaticSecret (KV v2)

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: api-keys
  namespace: production
spec:
  vaultAuthRef: vault-auth
  mount: secret
  path: myapp/api-keys
  type: kv-v2
  refreshAfter: 1h
  destination:
    create: true
    name: api-keys
```

### VaultDynamicSecret (Database)

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: postgres-creds
  namespace: production
spec:
  vaultAuthRef: vault-auth
  mount: database
  path: creds/postgres-role
  renewalPercent: 67  # Renew at 67% of TTL
  destination:
    create: true
    name: dynamic-db-creds
  rolloutRestartTargets:
  - kind: Deployment
    name: app
```

**Automatic Renewal:**
- VSO renews lease at 67% of TTL
- On renewal failure, requests new credentials
- Optionally triggers pod restart (rolloutRestartTargets)

### VaultPKISecret (TLS Certificates)

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultPKISecret
metadata:
  name: app-tls
  namespace: production
spec:
  vaultAuthRef: vault-auth
  mount: pki
  role: web-server
  commonName: app.example.com
  altNames:
  - www.app.example.com
  ttl: 24h
  destination:
    create: true
    name: app-tls-cert
  rolloutRestartTargets:
  - kind: Deployment
    name: app
```

## Comparison Matrix

| Feature | ESO | CSI Driver | VSO |
|---------|-----|------------|-----|
| **Multi-Provider** | Yes (30+) | Yes (AWS, GCP, Azure, Vault) | No (Vault only) |
| **Secret Type** | Kubernetes Secret | Files (volume mount) | Kubernetes Secret |
| **Rotation** | Polling (refresh interval) | Watch (inotify) | Lease renewal (automatic) |
| **Dynamic Secrets** | Limited | Yes | Yes (native support) |
| **Pod Restart** | Manual | Manual | Automatic (optional) |
| **Complexity** | Low | Medium | Low (for Vault users) |
| **Performance** | Polling overhead | Low overhead | Low overhead |
| **Maturity** | High (CNCF) | High (Kubernetes SIG) | Medium (HashiCorp) |

### When to Use Each

**External Secrets Operator (ESO):**
- Multi-cloud environments
- Need to support multiple secret stores
- Static secrets with hourly refresh acceptable
- Team familiar with Kubernetes operators

**Secrets Store CSI Driver:**
- Need file-based secret delivery
- Automatic rotation without pod restart
- TLS certificates (frequent rotation)
- Applications that watch files for changes

**Vault Secrets Operator (VSO):**
- Vault-centric infrastructure
- Dynamic secrets (database, cloud)
- Automatic lease renewal required
- Prefer Kubernetes-native CRDs

## Best Practices

### 1. Namespace Isolation

Use namespace-scoped SecretStores:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production  # Isolated to production namespace
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret/production"  # Namespace-specific path
      auth:
        kubernetes:
          role: "production-app-role"
          serviceAccountRef:
            name: app-sa
```

### 2. Least Privilege Service Accounts

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-secret-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["db-credentials"]  # Specific secret only
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-secret-reader-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: app-sa
roleRef:
  kind: Role
  name: app-secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### 3. Refresh Interval Tuning

```yaml
# Frequent rotation (TLS certs)
refreshInterval: 10m

# Moderate rotation (API keys)
refreshInterval: 1h

# Infrequent rotation (static configs)
refreshInterval: 6h
```

### 4. Monitoring and Alerting

**Prometheus Metrics (ESO):**
```yaml
- external_secrets_sync_calls_total
- external_secrets_sync_calls_error
- external_secrets_status_condition
```

**Alerts:**
```yaml
- alert: ExternalSecretSyncFailure
  expr: external_secrets_sync_calls_error > 0
  for: 5m
  annotations:
    summary: "ExternalSecret sync failing"
```

### 5. Encryption at Rest (etcd)

Enable etcd encryption for Kubernetes Secrets:

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <BASE64_ENCODED_SECRET>
  - identity: {}
```

```yaml
# kube-apiserver flag
--encryption-provider-config=/etc/kubernetes/encryption-config.yaml
```

### 6. Secret Versioning

Track secret versions for rollback:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: versioned-secret
  annotations:
    external-secrets.io/secret-version: "v2"
spec:
  secretStoreRef:
    name: vault-backend
  target:
    name: app-config
  data:
  - secretKey: api_key
    remoteRef:
      key: secret/data/api-keys
      version: 2  # Specific version
```

### 7. Testing Secret Rotation

```bash
# Update secret in Vault
vault kv put secret/myapp/config api_key=new_key_v2

# Wait for refresh interval
sleep 3600

# Verify Kubernetes Secret updated
kubectl get secret db-credentials -o jsonpath='{.data.api_key}' | base64 -d

# Check pod logs for reload
kubectl logs -f deployment/app
```

### 8. Disaster Recovery

Backup SecretStore configurations:

```bash
# Export all ExternalSecrets
kubectl get externalsecrets -A -o yaml > externalsecrets-backup.yaml

# Export all SecretStores
kubectl get secretstores -A -o yaml > secretstores-backup.yaml

# Restore
kubectl apply -f externalsecrets-backup.yaml
kubectl apply -f secretstores-backup.yaml
```
