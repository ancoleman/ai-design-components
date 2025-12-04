# Self-Hosted Authentication Solutions

Setup guides and comparisons for self-hosted authentication systems that provide full control over user data and infrastructure.

## Solution Comparison

| Solution | Language | License | Best For | Complexity |
|----------|----------|---------|----------|------------|
| **Keycloak** | Java | Apache 2.0 | Enterprise, SAML/OIDC | High |
| **Ory** | Go | Apache 2.0 | Cloud-native, microservices | Medium |
| **Authentik** | Python | MIT | Modern UI, flexibility | Medium |
| **Authelia** | Go | Apache 2.0 | Reverse proxy SSO | Low-Medium |
| **SuperTokens** | TypeScript/Python | Apache 2.0 | Developer-friendly APIs | Low |

---

## Keycloak

**Best for:** Enterprise deployments, on-premises installations, comprehensive SAML/OIDC requirements

### Overview

Mature, battle-tested identity and access management solution. Industry standard for self-hosted authentication.

**Key Features:**
- SAML 2.0 and OpenID Connect support
- User federation (LDAP, Active Directory)
- Identity brokering (Google, Facebook, GitHub, etc.)
- Admin console for user management
- Fine-grained authorization (RBAC, ABAC)
- Multi-tenancy (realms)
- Themes and customization

**Requirements:**
- Java 11+
- PostgreSQL/MySQL (production)
- 2GB RAM minimum
- Reverse proxy (nginx/Apache recommended)

### Quick Setup (Docker)

```bash
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:23.0.1 \
  start-dev
```

Access admin console: http://localhost:8080

### Production Setup (Kubernetes + PostgreSQL)

```yaml
# keycloak-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keycloak
spec:
  replicas: 2
  selector:
    matchLabels:
      app: keycloak
  template:
    metadata:
      labels:
        app: keycloak
    spec:
      containers:
      - name: keycloak
        image: quay.io/keycloak/keycloak:23.0.1
        args: ["start", "--optimized"]
        env:
        - name: KC_DB
          value: postgres
        - name: KC_DB_URL
          value: jdbc:postgresql://postgres:5432/keycloak
        - name: KC_DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: keycloak-db
              key: username
        - name: KC_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: keycloak-db
              key: password
        - name: KC_HOSTNAME
          value: auth.example.com
        - name: KC_PROXY
          value: edge
        - name: KEYCLOAK_ADMIN
          valueFrom:
            secretKeyRef:
              name: keycloak-admin
              key: username
        - name: KEYCLOAK_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: keycloak-admin
              key: password
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 120
          periodSeconds: 10
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

### Client Integration (Next.js)

```typescript
// auth.ts
import NextAuth from 'next-auth';
import KeycloakProvider from 'next-auth/providers/keycloak';

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    KeycloakProvider({
      clientId: process.env.KEYCLOAK_CLIENT_ID!,
      clientSecret: process.env.KEYCLOAK_CLIENT_SECRET!,
      issuer: process.env.KEYCLOAK_ISSUER, // https://auth.example.com/realms/myrealm
    }),
  ],
});
```

### FastAPI Integration (Python)

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import requests

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://auth.example.com/realms/myrealm/protocol/openid-connect/auth",
    tokenUrl="https://auth.example.com/realms/myrealm/protocol/openid-connect/token"
)

# Fetch JWKS for token verification
JWKS_URL = "https://auth.example.com/realms/myrealm/protocol/openid-connect/certs"
jwks_client = jwt.PyJWKClient(JWKS_URL)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="account"
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
def protected_route(user: dict = Depends(verify_token)):
    return {"message": f"Hello {user['preferred_username']}"}
```

---

## Ory

**Best for:** Cloud-native applications, microservices, Kubernetes-first deployments

### Overview

Modern, cloud-native authentication and authorization platform built for Kubernetes.

**Key Features:**
- Ory Hydra (OAuth 2.0 and OpenID Connect server)
- Ory Kratos (Identity management)
- Ory Oathkeeper (Identity & Access Proxy)
- Ory Keto (Authorization server - Zanzibar-style)
- API-first design
- Headless (bring your own UI)

**Requirements:**
- Go 1.21+
- PostgreSQL/CockroachDB (production)
- Kubernetes recommended

### Quick Setup (Docker Compose)

```yaml
# docker-compose.yml
version: '3.7'

services:
  kratos-migrate:
    image: oryd/kratos:v1.1.0
    environment:
      DSN: postgres://kratos:secret@postgres:5432/kratos?sslmode=disable
    volumes:
      - type: bind
        source: ./kratos
        target: /etc/config/kratos
    command: migrate sql -e --yes
    restart: on-failure

  kratos:
    image: oryd/kratos:v1.1.0
    ports:
      - '4433:4433'  # public
      - '4434:4434'  # admin
    environment:
      DSN: postgres://kratos:secret@postgres:5432/kratos?sslmode=disable
    command: serve -c /etc/config/kratos/kratos.yml --dev --watch-courier
    volumes:
      - type: bind
        source: ./kratos
        target: /etc/config/kratos
    restart: unless-stopped

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: kratos
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: kratos
    volumes:
      - kratos-postgres:/var/lib/postgresql/data

volumes:
  kratos-postgres:
```

### Ory Kratos Configuration

```yaml
# kratos.yml
version: v1.1.0

dsn: postgres://kratos:secret@postgres:5432/kratos?sslmode=disable

serve:
  public:
    base_url: http://localhost:4433/
    cors:
      enabled: true
  admin:
    base_url: http://localhost:4434/

selfservice:
  default_browser_return_url: http://localhost:3000/
  allowed_return_urls:
    - http://localhost:3000

  methods:
    password:
      enabled: true
    oidc:
      enabled: true
      config:
        providers:
          - id: google
            provider: google
            client_id: YOUR_GOOGLE_CLIENT_ID
            client_secret: YOUR_GOOGLE_CLIENT_SECRET
            mapper_url: file:///etc/config/kratos/oidc.google.jsonnet
            scope:
              - email
              - profile

  flows:
    registration:
      enabled: true
      ui_url: http://localhost:3000/registration
    login:
      ui_url: http://localhost:3000/login

identity:
  default_schema_id: default
  schemas:
    - id: default
      url: file:///etc/config/kratos/identity.schema.json

courier:
  smtp:
    connection_uri: smtps://test:test@mailslurper:1025/?skip_ssl_verify=true
```

### Client Integration (React)

```typescript
import { Configuration, FrontendApi } from '@ory/client';

const ory = new FrontendApi(
  new Configuration({
    basePath: 'http://localhost:4433',
    baseOptions: {
      withCredentials: true,
    },
  })
);

// Initialize login flow
const { data: flow } = await ory.createBrowserLoginFlow();

// Submit login
await ory.updateLoginFlow({
  flow: flow.id,
  updateLoginFlowBody: {
    method: 'password',
    identifier: 'user@example.com',
    password: 'password',
  },
});
```

---

## Authentik

**Best for:** Modern UI requirements, flexible identity provider, developer-friendly setup

### Overview

Modern identity provider with beautiful UI and flexible configuration.

**Key Features:**
- Policies and property mappings (custom logic)
- Application wizard (simplifies integration)
- Built-in proxy provider
- LDAP provider (outbound)
- Radius provider
- SCIM provider
- Flow-based configuration

**Requirements:**
- Python 3.11+
- PostgreSQL/Redis
- Docker recommended

### Quick Setup (Docker Compose)

```yaml
# docker-compose.yml
version: '3.7'

services:
  postgresql:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: authentik
      POSTGRES_USER: authentik
      POSTGRES_DB: authentik
    volumes:
      - database:/var/lib/postgresql/data

  redis:
    image: redis:alpine

  server:
    image: ghcr.io/goauthentik/server:2024.2.1
    command: server
    environment:
      AUTHENTIK_SECRET_KEY: change-me-please
      AUTHENTIK_BOOTSTRAP_PASSWORD: change-me-please
      AUTHENTIK_BOOTSTRAP_TOKEN: change-me-please
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: authentik
      AUTHENTIK_POSTGRESQL__PASSWORD: authentik
      AUTHENTIK_POSTGRESQL__NAME: authentik
      AUTHENTIK_REDIS__HOST: redis
    ports:
      - '9000:9000'
      - '9443:9443'
    volumes:
      - ./media:/media
      - ./custom-templates:/templates

  worker:
    image: ghcr.io/goauthentik/server:2024.2.1
    command: worker
    environment:
      AUTHENTIK_SECRET_KEY: change-me-please
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: authentik
      AUTHENTIK_POSTGRESQL__PASSWORD: authentik
      AUTHENTIK_POSTGRESQL__NAME: authentik
      AUTHENTIK_REDIS__HOST: redis
    volumes:
      - ./media:/media
      - ./certs:/certs
      - ./custom-templates:/templates

volumes:
  database:
```

Access: https://localhost:9443

---

## SuperTokens

**Best for:** Developer-friendly APIs, embedded authentication, modern frameworks

### Overview

Open-source alternative to Auth0 with simple integration.

**Key Features:**
- Session management (access/refresh tokens)
- Social login (Google, GitHub, etc.)
- Email/password authentication
- Passwordless (magic links, OTP)
- Multi-tenancy
- Pre-built UI components
- Self-hosted or managed cloud

**Requirements:**
- Node.js 16+ or Python 3.7+
- PostgreSQL/MySQL
- Docker recommended

### Quick Setup (Self-Hosted)

```bash
docker run -p 3567:3567 -d registry.supertokens.io/supertokens/supertokens-postgresql
```

### Integration (Next.js)

```typescript
// config/appInfo.ts
export const appInfo = {
  appName: 'MyApp',
  apiDomain: 'http://localhost:3000',
  websiteDomain: 'http://localhost:3000',
  apiBasePath: '/api/auth',
  websiteBasePath: '/auth',
};

// config/backend.ts
import SuperTokens from 'supertokens-node';
import EmailPassword from 'supertokens-node/recipe/emailpassword';
import Session from 'supertokens-node/recipe/session';

SuperTokens.init({
  framework: 'express',
  supertokens: {
    connectionURI: 'http://localhost:3567',
  },
  appInfo,
  recipeList: [
    EmailPassword.init(),
    Session.init(),
  ],
});
```

---

## Comparison Matrix

| Feature | Keycloak | Ory | Authentik | SuperTokens |
|---------|----------|-----|-----------|-------------|
| **SAML Support** | ✓✓✓ | ✗ | ✓✓ | ✗ |
| **OIDC Support** | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓ |
| **Built-in UI** | ✓✓✓ | ✗ | ✓✓✓ | ✓✓ |
| **Headless Option** | ✓ | ✓✓✓ | ✓ | ✓ |
| **Multi-tenancy** | ✓✓✓ | ✓ | ✓✓ | ✓✓ |
| **User Federation (LDAP)** | ✓✓✓ | ✗ | ✓✓✓ | ✗ |
| **API-first** | ✓ | ✓✓✓ | ✓✓ | ✓✓✓ |
| **Kubernetes-native** | ✓ | ✓✓✓ | ✓ | ✓ |
| **Setup Complexity** | High | Medium | Medium | Low |

## Decision Framework

### Choose Keycloak if:
- Enterprise deployment with SAML requirements
- Need LDAP/Active Directory integration
- Mature, battle-tested solution required
- Can manage Java infrastructure

### Choose Ory if:
- Building cloud-native microservices
- Kubernetes-first deployment
- Want headless, API-first architecture
- Need Zanzibar-style authorization (Ory Keto)

### Choose Authentik if:
- Want beautiful, modern admin UI
- Need flexible policy engine
- Require built-in proxy provider
- Python/Django familiarity

### Choose SuperTokens if:
- Want simplest integration
- Building with Next.js/Express
- Need pre-built UI components
- Want managed cloud option (fallback)

## Operational Considerations

### High Availability

**Keycloak:**
```yaml
# Multiple replicas + sticky sessions
replicas: 3
sessionAffinity: ClientIP
```

**Ory Kratos:**
```yaml
# Stateless design, scale horizontally
replicas: 5
```

### Backup and Recovery

**Database backups:**
```bash
# PostgreSQL backup (all solutions)
pg_dump -h localhost -U keycloak -d keycloak > keycloak-backup.sql

# Restore
psql -h localhost -U keycloak -d keycloak < keycloak-backup.sql
```

### Monitoring

**Key metrics to monitor:**
- Login success/failure rates
- Token generation latency
- Database connection pool utilization
- Memory/CPU usage
- Authentication endpoint response times

**Prometheus integration:**
- Keycloak: Built-in metrics endpoint
- Ory: Prometheus exporter available
- Authentik: Built-in Prometheus metrics

### Security Hardening

1. **Use HTTPS everywhere** (TLS 1.3+)
2. **Enable rate limiting** on auth endpoints
3. **Implement bot detection** (reCAPTCHA, Turnstile)
4. **Regular security updates** (subscribe to security mailing lists)
5. **Audit logging** (track authentication events)
6. **Secrets management** (Vault, Kubernetes secrets)

## Migration from Managed to Self-Hosted

**Steps:**
1. **Export user database** from managed provider
2. **Convert password hashes** (if supported)
3. **Set up self-hosted solution** in parallel
4. **Test with small user cohort**
5. **Gradual rollout** with feature flags
6. **Update OAuth redirect URIs**
7. **Monitor for authentication failures**

## Cost Analysis

**Self-hosted costs:**
- Infrastructure: $50-500/month (depending on scale)
- Maintenance: 10-20 hours/month developer time
- Monitoring/logging: $20-100/month

**Break-even point:**
- Typically 10K-50K MAU (compared to managed Auth0/Clerk)
- Factor in developer time for maintenance
- Consider compliance overhead (SOC 2, HIPAA)

## Resources

- Keycloak Docs: https://www.keycloak.org/documentation
- Ory Docs: https://www.ory.sh/docs
- Authentik Docs: https://goauthentik.io/docs/
- SuperTokens Docs: https://supertokens.com/docs/
