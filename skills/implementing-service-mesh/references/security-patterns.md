# Service Mesh Security Patterns

## Table of Contents

- [Zero-Trust Architecture](#zero-trust-architecture)
- [Mutual TLS Configuration](#mutual-tls-configuration)
- [Authorization Policies](#authorization-policies)
- [JWT Authentication](#jwt-authentication)
- [External Authorization](#external-authorization)
- [Certificate Management](#certificate-management)

## Zero-Trust Architecture

Implement security principle: never trust, always verify.

### Core Principles

1. **Default Deny:** Block all traffic unless explicitly allowed
2. **Identity-Based:** Use workload identities, not IP addresses
3. **Least Privilege:** Grant minimum required permissions
4. **Micro-Segmentation:** Isolate services at network level
5. **Continuous Verification:** Authenticate every request

### Implementation Steps (Istio)

**Step 1: Enable Strict mTLS**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default-strict-mtls
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

**Step 2: Default Deny All Traffic**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec: {}
```

**Step 3: Explicit Allow Rules**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/frontend
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

**Step 4: Namespace Isolation**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-cross-namespace
  namespace: production
spec:
  action: DENY
  rules:
  - from:
    - source:
        notNamespaces: ["production"]
```

### Zero-Trust Checklist

- [ ] Strict mTLS enabled mesh-wide
- [ ] Default-deny authorization policies
- [ ] Explicit allow rules for all required communication
- [ ] Service accounts properly configured
- [ ] Namespace isolation enforced
- [ ] Audit logging enabled
- [ ] Regular certificate rotation
- [ ] Policy validation in CI/CD

## Mutual TLS Configuration

Automatic encryption of service-to-service traffic.

### Istio mTLS Modes

**STRICT Mode (Production):**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: strict-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT
```

Rejects all plaintext connections. Use in production after migration.

**PERMISSIVE Mode (Migration):**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: permissive-mtls
  namespace: production
spec:
  mtls:
    mode: PERMISSIVE
```

Accepts both mTLS and plaintext. Use during migration.

**DISABLE Mode (Legacy):**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: disable-mtls
  namespace: production
spec:
  selector:
    matchLabels:
      app: legacy-service
  mtls:
    mode: DISABLE
```

Disables mTLS for specific workloads. Use sparingly.

### Per-Port mTLS

Configure mTLS for specific ports.

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: per-port-mtls
spec:
  selector:
    matchLabels:
      app: backend
  mtls:
    mode: STRICT
  portLevelMtls:
    8080:
      mode: PERMISSIVE
    9090:
      mode: DISABLE
```

### Verify mTLS Status

**Istio:**

```bash
# Check mTLS status for deployment
istioctl authn tls-check frontend.production.svc.cluster.local

# Verify proxy configuration
istioctl proxy-config secret deployment/frontend -n production
```

**Linkerd:**

```bash
# Check mTLS edges
linkerd edges deployment/frontend -n production

# Verify identity
linkerd identity list -n production
```

**Cilium:**

```bash
# List authenticated connections
cilium bpf auth list

# Check SPIRE status
kubectl exec -n spire spire-server-0 -- \
  /opt/spire/bin/spire-server entry show
```

### Migration Strategy

**Phase 1: Install Mesh with PERMISSIVE**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: PERMISSIVE
```

**Phase 2: Monitor mTLS Adoption**

```bash
# Check which services are using mTLS
kubectl get peerauthentication -A
istioctl authn tls-check <service>
```

**Phase 3: Switch to STRICT**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

**Phase 4: Validate**

```bash
# Ensure all traffic is encrypted
istioctl analyze
kubectl logs -n production deployment/frontend -c istio-proxy
```

## Authorization Policies

Control access to services based on identity and attributes.

### Service-to-Service Authorization

Allow specific service to call another.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: frontend-to-backend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/frontend
```

### HTTP Method and Path Restrictions

Allow only specific operations.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: read-only-api
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/frontend
    to:
    - operation:
        methods: ["GET", "HEAD"]
        paths: ["/api/users/*", "/api/products/*"]
```

### IP-Based Restrictions (Use Sparingly)

Allow traffic from specific IPs.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: ip-allowlist
spec:
  selector:
    matchLabels:
      app: admin-api
  action: ALLOW
  rules:
  - from:
    - source:
        ipBlocks:
        - 10.0.0.0/8
        - 192.168.1.100/32
```

**Note:** Prefer identity-based over IP-based for cloud environments.

### Time-Based Access Control

Restrict access during specific hours (requires custom attributes).

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: business-hours-only
spec:
  selector:
    matchLabels:
      app: reporting-service
  action: ALLOW
  rules:
  - when:
    - key: request.time
      values: ["09:00-17:00"]
```

### Deny Policies

Explicitly deny dangerous operations.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-delete
  namespace: production
spec:
  selector:
    matchLabels:
      app: database
  action: DENY
  rules:
  - to:
    - operation:
        methods: ["DELETE"]
```

### Namespace Isolation

Prevent cross-namespace communication.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: namespace-isolation
  namespace: production
spec:
  action: DENY
  rules:
  - from:
    - source:
        notNamespaces: ["production", "istio-system"]
```

## JWT Authentication

Validate JSON Web Tokens for API authentication.

### RequestAuthentication

Define JWT validation rules.

```yaml
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
    audiences:
    - "api.example.com"
    - "mobile.example.com"
    forwardOriginalToken: true
```

### Require Valid JWT

Enforce JWT presence with AuthorizationPolicy.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]
```

### Claims-Based Authorization

Authorize based on JWT claims.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: admin-only
  namespace: production
spec:
  selector:
    matchLabels:
      app: admin-api
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]
    when:
    - key: request.auth.claims[role]
      values: ["admin", "superuser"]
    - key: request.auth.claims[verified]
      values: ["true"]
```

### Per-Path JWT Requirements

Different paths, different auth requirements.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: public-private-paths
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
  # Public endpoints: no auth required
  - to:
    - operation:
        paths: ["/health", "/metrics", "/public/*"]
  # Private endpoints: JWT required
  - from:
    - source:
        requestPrincipals: ["*"]
    to:
    - operation:
        paths: ["/api/*"]
```

### Multiple JWT Issuers

Support tokens from multiple identity providers.

```yaml
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata:
  name: multi-issuer-jwt
spec:
  selector:
    matchLabels:
      app: api-gateway
  jwtRules:
  # Google OAuth
  - issuer: "https://accounts.google.com"
    jwksUri: "https://www.googleapis.com/oauth2/v3/certs"
    audiences: ["api.example.com"]
  # Auth0
  - issuer: "https://example.auth0.com/"
    jwksUri: "https://example.auth0.com/.well-known/jwks.json"
    audiences: ["https://api.example.com"]
  # Custom IDP
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/jwks"
    audiences: ["api.example.com"]
```

## External Authorization

Integrate with external authorization services.

### OPA (Open Policy Agent) Integration

**Step 1: Deploy OPA**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opa
  namespace: opa-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: opa
  template:
    metadata:
      labels:
        app: opa
    spec:
      containers:
      - name: opa
        image: openpolicyagent/opa:latest
        args:
        - "run"
        - "--server"
        - "--addr=0.0.0.0:9191"
        - "/policies"
        volumeMounts:
        - name: policies
          mountPath: /policies
      volumes:
      - name: policies
        configMap:
          name: opa-policies
```

**Step 2: Configure Istio Extension Provider**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio
  namespace: istio-system
data:
  mesh: |
    extensionProviders:
    - name: opa
      envoyExtAuthzGrpc:
        service: opa.opa-system.svc.cluster.local
        port: 9191
```

**Step 3: Apply Authorization Policy**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: ext-authz-opa
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: CUSTOM
  provider:
    name: opa
  rules:
  - to:
    - operation:
        paths: ["/api/*"]
```

**Step 4: Define OPA Policy**

```rego
package istio.authz

import input.attributes.request.http as http_request

default allow = false

# Allow GET requests to /api/users for authenticated users
allow {
    http_request.method == "GET"
    startswith(http_request.path, "/api/users")
    input.attributes.source.principal != ""
}

# Allow admins to access /api/admin
allow {
    startswith(http_request.path, "/api/admin")
    input.attributes.source.principal contains "admin"
}
```

### Custom External Authorizer

Implement custom authorization logic.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: custom-authz
spec:
  selector:
    matchLabels:
      app: payment-api
  action: CUSTOM
  provider:
    name: custom-authz-service
  rules:
  - to:
    - operation:
        paths: ["/payment/*"]
```

## Certificate Management

Manage TLS certificates for service mesh.

### Automatic Certificate Rotation (Istio)

Configure certificate TTL and rotation.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio
  namespace: istio-system
data:
  mesh: |
    certificates:
    - secretName: istio-ca-secret
      dnsNames:
      - istio-ca
    defaultConfig:
      workloadCertTtl: 24h
    meshConfig:
      trustDomain: cluster.local
```

### External CA Integration (cert-manager)

Use cert-manager for certificate issuance.

**Step 1: Create CA Issuer**

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: istio-ca
spec:
  ca:
    secretName: istio-ca-secret
```

**Step 2: Configure Istio to Use External CA**

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    caCertificates:
    - certSigners:
      - clusterissuers.cert-manager.io/istio-ca
```

### Certificate Monitoring

Monitor certificate expiration.

```bash
# Check certificate details (Istio)
istioctl proxy-config secret deployment/frontend -n production -o json | \
  jq '.dynamicActiveSecrets[] | select(.name=="default") | .secret.tlsCertificate.certificateChain.inlineBytes' | \
  base64 -d | openssl x509 -text -noout

# Alert on expiration
# Prometheus query:
certmanager_certificate_expiration_timestamp_seconds - time() < 86400
```

### Custom Root CA

Use enterprise PKI root CA.

```bash
# Generate root CA
openssl req -x509 -sha256 -nodes -days 3650 \
  -newkey rsa:4096 -keyout root-ca.key -out root-ca.crt

# Create Kubernetes secret
kubectl create secret generic istio-ca-secret \
  -n istio-system \
  --from-file=ca-cert.pem=root-ca.crt \
  --from-file=ca-key.pem=root-ca.key
```

## Security Best Practices

**mTLS:**
- Use STRICT mode in production
- Monitor mTLS adoption metrics
- Rotate certificates automatically
- Use short certificate lifetimes (24h)

**Authorization:**
- Start with default-deny policies
- Use identity-based controls (not IP-based)
- Apply least privilege principle
- Audit policy changes

**JWT:**
- Validate issuer and audience
- Use short token lifetimes
- Rotate signing keys regularly
- Validate claims in authorization policies

**External Authorization:**
- Use for complex business logic
- Monitor authorizer latency
- Implement fallback policies
- Cache authorization decisions when appropriate

**Certificate Management:**
- Automate rotation
- Monitor expiration
- Use separate CAs per environment
- Implement certificate revocation
