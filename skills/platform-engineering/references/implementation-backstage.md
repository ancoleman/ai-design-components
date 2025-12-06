# Implementing a Backstage-Based Platform

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation and Setup](#installation-and-setup)
3. [Core Configuration](#core-configuration)
4. [Creating the First Golden Path](#creating-the-first-golden-path)
5. [Integration Examples](#integration-examples)
6. [Production Deployment](#production-deployment)

## Prerequisites

### Infrastructure Requirements

**Development Environment:**
- Node.js 18+ and Yarn
- Docker and Docker Compose
- Git
- Text editor / IDE

**Production Environment:**
- Kubernetes cluster (EKS, GKE, AKS, or self-managed)
- PostgreSQL database (managed or self-hosted)
- Object storage for TechDocs (S3, GCS, Azure Blob)
- Authentication provider (GitHub, GitLab, Okta, Azure AD)

### Team Requirements

**Minimum Team:**
- 1-2 platform engineers (Backstage setup and customization)
- 1 frontend engineer (optional, for custom plugins/UI)

**Recommended Team:**
- 1 platform lead (strategy, roadmap)
- 2-3 platform engineers (Backstage development, integrations)
- 1 SRE (production operations, monitoring)

## Installation and Setup

### Quick Start (Development)

```bash
# Create new Backstage app
npx @backstage/create-app@latest

# Follow prompts
App name: my-platform
# Choose GitHub authentication

cd my-platform

# Start development server
yarn dev
```

Access at `http://localhost:3000`

### Directory Structure

```
my-platform/
├── app-config.yaml              # Main configuration
├── app-config.production.yaml   # Production overrides
├── packages/
│   ├── app/                     # Frontend React app
│   │   ├── src/
│   │   │   ├── App.tsx          # Main app component
│   │   │   └── components/      # Custom components
│   ├── backend/                 # Backend Node.js app
│   │   ├── src/
│   │   │   ├── index.ts         # Backend entry point
│   │   │   └── plugins/         # Backend plugins
│   └── common/                  # Shared code
├── plugins/                     # Custom plugins
└── catalog-info.yaml            # Backstage itself in catalog
```

## Core Configuration

### app-config.yaml

```yaml
app:
  title: My Platform
  baseUrl: http://localhost:3000

organization:
  name: My Company

backend:
  baseUrl: http://localhost:7007
  listen:
    port: 7007
  database:
    client: pg
    connection:
      host: ${POSTGRES_HOST}
      port: ${POSTGRES_PORT}
      user: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}

auth:
  environment: development
  providers:
    github:
      development:
        clientId: ${GITHUB_CLIENT_ID}
        clientSecret: ${GITHUB_CLIENT_SECRET}

catalog:
  import:
    entityFilename: catalog-info.yaml
  rules:
    - allow: [Component, System, API, Resource, Location]
  locations:
    # Register components from Git repositories
    - type: url
      target: https://github.com/my-org/service-catalog/blob/main/all.yaml
      rules:
        - allow: [User, Group]

techdocs:
  builder: 'local'
  generator:
    runIn: 'local'
  publisher:
    type: 'local'
```

### Authentication Setup (GitHub)

1. Create GitHub OAuth App:
   - Go to GitHub Settings → Developer settings → OAuth Apps → New OAuth App
   - Homepage URL: `http://localhost:3000`
   - Callback URL: `http://localhost:7007/api/auth/github/handler/frame`

2. Add credentials to `app-config.local.yaml` (gitignored):

```yaml
auth:
  providers:
    github:
      development:
        clientId: your-client-id
        clientSecret: your-client-secret
```

### Database Setup

**Development (SQLite):**
```yaml
backend:
  database:
    client: better-sqlite3
    connection: ':memory:'
```

**Production (PostgreSQL):**
```bash
# Create database
createdb backstage

# Set environment variables
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=backstage
export POSTGRES_PASSWORD=secure-password
```

## Creating the First Golden Path

### Software Template Example: Node.js Microservice

Create `templates/nodejs-service/template.yaml`:

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: nodejs-service
  title: Node.js Microservice
  description: Create a new Node.js microservice with Express and TypeScript
  tags:
    - recommended
    - nodejs
    - api
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Information
      required:
        - name
        - owner
      properties:
        name:
          title: Name
          type: string
          description: Unique name for this service
          ui:autofocus: true
        description:
          title: Description
          type: string
          description: What does this service do?
        owner:
          title: Owner
          type: string
          description: Team or individual owner
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind: [Group, User]

    - title: Deployment Configuration
      required:
        - environment
      properties:
        environment:
          title: Initial Environment
          type: string
          enum:
            - development
            - staging
            - production
          default: development

  steps:
    - id: fetch-base
      name: Fetch Base Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          description: ${{ parameters.description }}
          owner: ${{ parameters.owner }}
          environment: ${{ parameters.environment }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: ${{ parameters.description }}
        repoUrl: github.com?owner=my-org&repo=${{ parameters.name }}
        defaultBranch: main

    - id: register
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  output:
    links:
      - title: Repository
        url: ${{ steps['publish'].output.remoteUrl }}
      - title: Open in catalog
        icon: catalog
        entityRef: ${{ steps['register'].output.entityRef }}
```

### Template Skeleton Structure

Create `templates/nodejs-service/skeleton/`:

```
skeleton/
├── catalog-info.yaml
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── app.ts
│   └── routes/
│       └── health.ts
├── .github/
│   └── workflows/
│       └── ci.yaml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── docs/
│   └── index.md
└── mkdocs.yml
```

**catalog-info.yaml:**
```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ${{values.name}}
  description: ${{values.description}}
  annotations:
    github.com/project-slug: my-org/${{values.name}}
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: experimental
  owner: ${{values.owner}}
  system: platform
```

**package.json:**
```json
{
  "name": "${{values.name}}",
  "version": "1.0.0",
  "description": "${{values.description}}",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "ts-node-dev src/index.ts",
    "build": "tsc",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.0",
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "ts-node-dev": "^2.0.0"
  }
}
```

## Integration Examples

### GitHub Actions Plugin

**Install plugin:**
```bash
yarn workspace app add @backstage/plugin-github-actions
```

**Configure in app/src/components/catalog/EntityPage.tsx:**
```typescript
import {
  EntityGithubActionsContent,
  isGithubActionsAvailable,
} from '@backstage/plugin-github-actions';

const cicdContent = (
  <EntitySwitch>
    <EntitySwitch.Case if={isGithubActionsAvailable}>
      <EntityGithubActionsContent />
    </EntitySwitch.Case>
  </EntitySwitch>
);
```

**Add to app-config.yaml:**
```yaml
integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}
```

### Kubernetes Plugin

**Install:**
```bash
yarn workspace app add @backstage/plugin-kubernetes
yarn workspace backend add @backstage/plugin-kubernetes-backend
```

**Configure backend (packages/backend/src/plugins/kubernetes.ts):**
```typescript
import { KubernetesBuilder } from '@backstage/plugin-kubernetes-backend';
import { Router } from 'express';
import { PluginEnvironment } from '../types';

export default async function createPlugin(
  env: PluginEnvironment,
): Promise<Router> {
  const { router } = await KubernetesBuilder.createBuilder({
    logger: env.logger,
    config: env.config,
  }).build();
  return router;
}
```

**app-config.yaml:**
```yaml
kubernetes:
  serviceLocatorMethod:
    type: 'multiTenant'
  clusterLocatorMethods:
    - type: 'config'
      clusters:
        - url: https://k8s-cluster.example.com
          name: production
          authProvider: 'serviceAccount'
          serviceAccountToken: ${K8S_TOKEN}
```

### Prometheus/Grafana Plugin

**Install:**
```bash
yarn workspace app add @backstage/plugin-prometheus
```

**Add annotation to catalog-info.yaml:**
```yaml
metadata:
  annotations:
    prometheus.io/rule: memUsage|component,|instance,|job
    prometheus.io/alert: all
```

## Production Deployment

### Kubernetes Deployment

**Create namespace:**
```bash
kubectl create namespace backstage
```

**Create PostgreSQL (using Helm):**
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql \
  --namespace backstage \
  --set auth.database=backstage \
  --set auth.username=backstage
```

**Build Docker image:**
```dockerfile
# packages/backend/Dockerfile
FROM node:18-bullseye-slim
WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./
COPY packages/backend/package.json ./packages/backend/

# Install dependencies
RUN yarn install --frozen-lockfile --production --network-timeout 300000

# Copy backend code
COPY packages/backend/dist ./packages/backend/dist

CMD ["node", "packages/backend"]
EXPOSE 7007
```

```bash
# Build
docker build -t my-registry/backstage:1.0.0 -f packages/backend/Dockerfile .

# Push
docker push my-registry/backstage:1.0.0
```

**Kubernetes manifests:**

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backstage
  namespace: backstage
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backstage
  template:
    metadata:
      labels:
        app: backstage
    spec:
      containers:
      - name: backstage
        image: my-registry/backstage:1.0.0
        ports:
        - containerPort: 7007
        env:
        - name: POSTGRES_HOST
          value: postgres-postgresql
        - name: POSTGRES_PORT
          value: "5432"
        - name: POSTGRES_USER
          value: backstage
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-postgresql
              key: password
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: backstage-secrets
              key: github-token
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

**service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backstage
  namespace: backstage
spec:
  selector:
    app: backstage
  ports:
  - port: 80
    targetPort: 7007
  type: ClusterIP
```

**ingress.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backstage
  namespace: backstage
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - platform.mycompany.com
    secretName: backstage-tls
  rules:
  - host: platform.mycompany.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backstage
            port:
              number: 80
```

**Deploy:**
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

### Monitoring and Observability

**Add Prometheus metrics:**
```typescript
// packages/backend/src/index.ts
import { useHotCleanup } from '@backstage/backend-common';
import { metricsHandler } from '@backstage/backend-defaults/prometheus';

async function main() {
  // ... existing code ...

  // Add metrics endpoint
  apiRouter.use('/metrics', metricsHandler());
}
```

**ServiceMonitor (for Prometheus Operator):**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backstage
  namespace: backstage
spec:
  selector:
    matchLabels:
      app: backstage
  endpoints:
  - port: http
    path: /metrics
```

### Scaling Considerations

**Horizontal Pod Autoscaling:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backstage
  namespace: backstage
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backstage
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Database Connection Pooling:**
```yaml
# app-config.production.yaml
backend:
  database:
    client: pg
    connection:
      host: ${POSTGRES_HOST}
      port: ${POSTGRES_PORT}
      user: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}
    pool:
      min: 5
      max: 20
```

### Backup and Disaster Recovery

**PostgreSQL Backups:**
```bash
# Automated backup script
pg_dump -h $POSTGRES_HOST -U backstage backstage | gzip > backstage-$(date +%Y%m%d).sql.gz

# Upload to S3
aws s3 cp backstage-$(date +%Y%m%d).sql.gz s3://backups/backstage/
```

**Restore:**
```bash
# Download from S3
aws s3 cp s3://backups/backstage/backstage-20250101.sql.gz .

# Restore
gunzip < backstage-20250101.sql.gz | psql -h $POSTGRES_HOST -U backstage backstage
```
