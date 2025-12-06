# Security

## Table of Contents

1. [RBAC (Role-Based Access Control)](#rbac-role-based-access-control)
2. [Pod Security Standards](#pod-security-standards)
3. [Policy Enforcement](#policy-enforcement)
4. [Secrets Management](#secrets-management)
5. [Image Security](#image-security)
6. [Network Security](#network-security)

## RBAC (Role-Based Access Control)

### Roles and ClusterRoles

**Role (Namespace-scoped):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]  # Core API group
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]
```

**ClusterRole (Cluster-wide):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-admin
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch", "update", "patch"]
- apiGroups: [""]
  resources: ["persistentvolumes"]
  verbs: ["get", "list", "watch", "create", "delete"]
```

### RoleBindings and ClusterRoleBindings

**RoleBinding (Namespace-scoped):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: User
  name: jane@example.com
  apiGroup: rbac.authorization.k8s.io
- kind: Group
  name: developers
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: app-sa
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**ClusterRoleBinding (Cluster-wide):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-admins
subjects:
- kind: Group
  name: sre-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: node-admin
  apiGroup: rbac.authorization.k8s.io
```

### ServiceAccounts

**Create ServiceAccount:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: production
automountServiceAccountToken: false  # Don't auto-mount unless needed
```

**Use in Pod:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  namespace: production
spec:
  serviceAccountName: my-app-sa
  containers:
  - name: app
    image: myapp:latest
```

**Grant Permissions:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: configmap-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-configmap-access
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app-sa
  namespace: production
roleRef:
  kind: Role
  name: configmap-reader
  apiGroup: rbac.authorization.k8s.io
```

### Common RBAC Patterns

**Read-Only Access:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: readonly
  namespace: production
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
```

**Deployment Manager:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
```

**Debug Access (Exec into Pods):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: debug-access
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods/exec"]
  verbs: ["create"]
```

### RBAC Best Practices

**Least Privilege:**
```yaml
# Bad: Too permissive
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

# Good: Specific permissions
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
  resourceNames: ["app-config"]  # Further restrict to specific resource
```

**Avoid Default ServiceAccount:**
```yaml
# Bad: Using default ServiceAccount
spec:
  serviceAccountName: default

# Good: Dedicated ServiceAccount
spec:
  serviceAccountName: my-app-sa
```

**Audit RBAC:**
```bash
# Check user permissions
kubectl auth can-i create deployments --namespace production --as jane@example.com

# List all RoleBindings
kubectl get rolebindings -A

# Audit who can delete pods
kubectl get rolebindings,clusterrolebindings -A -o json | \
  jq -r '.items[] | select(.roleRef.name=="cluster-admin")'
```

## Pod Security Standards

### Namespace Enforcement

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Enforcement Modes:**
- **enforce:** Block pod creation if violates standard
- **audit:** Log violations but allow
- **warn:** Show warning but allow

**Security Levels:**
- **privileged:** Unrestricted (system workloads only)
- **baseline:** Minimally restrictive (prevents known escalations)
- **restricted:** Most secure (removes all privilege escalations)

### Restricted Pod Configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: production
spec:
  # Pod-level security context
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault

  containers:
  - name: app
    image: myapp:latest

    # Container-level security context
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
        - ALL
      seccompProfile:
        type: RuntimeDefault

    # Writable directories
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache

  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

### Security Context Options

**runAsNonRoot:**
```yaml
securityContext:
  runAsNonRoot: true  # Prevent root user
```

**readOnlyRootFilesystem:**
```yaml
securityContext:
  readOnlyRootFilesystem: true  # Immutable filesystem
```

**Capabilities:**
```yaml
securityContext:
  capabilities:
    drop:
    - ALL  # Drop all capabilities
    add:
    - NET_BIND_SERVICE  # Add only specific capability
```

**seccomp Profile:**
```yaml
securityContext:
  seccompProfile:
    type: RuntimeDefault  # Apply default seccomp profile
```

**AppArmor:**
```yaml
metadata:
  annotations:
    container.apparmor.security.beta.kubernetes.io/app: runtime/default
```

### Pod Security Standard Migration

```bash
# Audit current violations
kubectl label namespace production \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted

# Review warnings
kubectl get pods -n production

# Fix violations, then enforce
kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted
```

## Policy Enforcement

### Kyverno Policies

**Installation:**
```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno --namespace kyverno --create-namespace
```

**Require Resource Limits:**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resources
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: check-resources
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CPU and memory resource requests and limits are required"
      pattern:
        spec:
          containers:
          - resources:
              requests:
                memory: "?*"
                cpu: "?*"
              limits:
                memory: "?*"
                cpu: "?*"
```

**Block Latest Tag:**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: enforce
  rules:
  - name: require-image-tag
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Using 'latest' image tag is not allowed"
      pattern:
        spec:
          containers:
          - image: "!*:latest"
```

**Require Labels:**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: enforce
  rules:
  - name: check-labels
    match:
      any:
      - resources:
          kinds:
          - Deployment
    validate:
      message: "Deployments must have 'app' and 'team' labels"
      pattern:
        metadata:
          labels:
            app: "?*"
            team: "?*"
```

**Mutate (Add Default Resources):**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-resources
spec:
  background: true
  rules:
  - name: add-resources
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        spec:
          containers:
          - (name): "*"
            resources:
              requests:
                +(memory): "256Mi"
                +(cpu): "250m"
              limits:
                +(memory): "512Mi"
                +(cpu): "500m"
```

### OPA Gatekeeper

**Installation:**
```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml
```

**Constraint Template:**
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package k8srequiredlabels
      violation[{"msg": msg}] {
        provided := {label | input.review.object.metadata.labels[label]}
        required := {label | label := input.parameters.labels[_]}
        missing := required - provided
        count(missing) > 0
        msg := sprintf("Missing required labels: %v", [missing])
      }
```

**Constraint:**
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-app-team-labels
spec:
  match:
    kinds:
    - apiGroups: ["apps"]
      kinds: ["Deployment"]
  parameters:
    labels: ["app", "team"]
```

## Secrets Management

### Kubernetes Secrets

**Create Secret:**
```bash
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=securepassword \
  --namespace production
```

```yaml
# YAML definition
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: production
type: Opaque
stringData:
  username: admin
  password: securepassword
```

**Use in Pod:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
```

**Mount as Volume:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:latest
    volumeMounts:
    - name: secrets
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secrets
    secret:
      secretName: db-credentials
```

### Encryption at Rest

**Enable encryption (kube-apiserver flag):**
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-encoded-32-byte-key>
  - identity: {}
```

### External Secrets Operator

**Installation:**
```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets-system --create-namespace
```

**SecretStore (AWS Secrets Manager):**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets
  namespace: production
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets
```

**ExternalSecret:**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: db-secret
    creationPolicy: Owner
  data:
  - secretKey: password
    remoteRef:
      key: production/postgres/password
```

## Image Security

### Image Scanning

**Trivy (Open Source):**
```bash
# Scan image
trivy image myapp:latest

# Scan for HIGH/CRITICAL only
trivy image --severity HIGH,CRITICAL myapp:latest

# Output JSON
trivy image --format json -o results.json myapp:latest
```

**Admission Controller (Scan on Deploy):**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: scan-images
spec:
  validationFailureAction: enforce
  webhookTimeoutSeconds: 30
  rules:
  - name: scan-image
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Image has HIGH/CRITICAL vulnerabilities"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            any:
            - key: "{{ scan('{{ element.image }}').critical }}"
              operator: GreaterThan
              value: 0
```

### Image Pull Secrets

```bash
# Create registry secret
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.azurecr.io \
  --docker-username=myuser \
  --docker-password=mypassword \
  --docker-email=myemail@example.com \
  --namespace production
```

```yaml
# Use in Pod
spec:
  imagePullSecrets:
  - name: regcred
  containers:
  - name: app
    image: myregistry.azurecr.io/myapp:v1.0
```

### Image Signing (Sigstore/Cosign)

```bash
# Sign image
cosign sign --key cosign.key myregistry.io/myapp:v1.0

# Verify signature
cosign verify --key cosign.pub myregistry.io/myapp:v1.0
```

**Kyverno Verification:**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signature
spec:
  validationFailureAction: enforce
  rules:
  - name: verify-signature
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "myregistry.io/*"
      attestors:
      - entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
```

## Network Security

### TLS for In-Cluster Communication

**cert-manager Installation:**
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

**ClusterIssuer:**
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

**Certificate:**
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapp-tls
  namespace: production
spec:
  secretName: myapp-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - myapp.example.com
```

## Summary

**Security Checklist:**
- [ ] Enable RBAC and follow least-privilege principle
- [ ] Create dedicated ServiceAccounts (don't use default)
- [ ] Enforce Pod Security Standards (Restricted for apps)
- [ ] Implement policy enforcement (Kyverno or OPA)
- [ ] Use External Secrets Operator for sensitive data
- [ ] Enable encryption at rest for Secrets
- [ ] Scan images for vulnerabilities
- [ ] Use image pull secrets for private registries
- [ ] Implement NetworkPolicies (default-deny)
- [ ] Enable TLS for ingress traffic (cert-manager)
- [ ] Regularly audit RBAC permissions
- [ ] Monitor security events and policy violations

**Recommended Tools:**
- **RBAC:** Built-in Kubernetes
- **Pod Security:** Pod Security Standards (built-in)
- **Policy:** Kyverno (easier) or OPA Gatekeeper (more powerful)
- **Secrets:** External Secrets Operator + cloud provider
- **Image Scanning:** Trivy
- **TLS:** cert-manager
- **Audit:** Falco, kube-bench
