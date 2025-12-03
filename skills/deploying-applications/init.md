# Deploying Applications - Master Plan

> **Skill Purpose**: Production deployment patterns from Kubernetes to serverless and edge functions. Bridges the gap from assembled applications to production infrastructure.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Skill 13), Context7 Library Research, Anthropic Skills Best Practices

---

## Strategic Positioning

### The Deployment Gap

Current skill chain workflow:
```
assembling-components → ??? → production deployment
```

With this skill:
```
assembling-components → deploying-applications → production infrastructure
```

**Problem Statement**: After assembling a complete application with `assembling-components`, developers face critical deployment decisions:
1. **Infrastructure as Code (IaC)**: Which tool to use (Pulumi, OpenTofu, SST)?
2. **Deployment Strategy**: Kubernetes, serverless, containers, or edge?
3. **GitOps Setup**: ArgoCD vs Flux for continuous deployment
4. **Service Mesh**: When to use Linkerd vs Istio
5. **Serverless Databases**: Scale-to-zero options (Neon, Turso, PlanetScale)
6. **Edge Functions**: Cloudflare Workers vs Deno Deploy vs Vercel Edge

### Unique Value Proposition

| Capability | Why It Matters |
|------------|----------------|
| TypeScript-first IaC | Pulumi provides type safety and familiar syntax |
| Deployment decision trees | Clear guidance for choosing Kubernetes vs serverless vs edge |
| Multi-cloud patterns | Works across AWS, GCP, Azure, Cloudflare |
| GitOps automation | ArgoCD/Flux for continuous deployment |
| Cost optimization | Serverless databases with scale-to-zero |

---

## Strategic Integration

### Frontend → Deployment Flow

```
┌──────────────────────────────────────────────────────────────┐
│            Deployment Flow from Frontend Skills              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  assembling-components (React/Next.js/Vite)                  │
│           ↓                                                   │
│  deploying-applications (IaC + Deployment)                   │
│           ↓                                                   │
│  Production Infrastructure:                                   │
│  ├─ Vercel (Next.js, zero-config)                           │
│  ├─ Cloudflare Workers (edge, <5ms cold start)              │
│  ├─ AWS Lambda + CloudFront (serverless)                     │
│  ├─ Google Cloud Run (containers, auto-scale)               │
│  └─ Kubernetes + ArgoCD (complex microservices)             │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Backend → Deployment Flow

```
┌──────────────────────────────────────────────────────────────┐
│            Backend Deployment Integration                     │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  api-patterns (FastAPI/Axum/Hono/Gin)                        │
│           ↓                                                   │
│  databases-* (relational/vector/timeseries)                  │
│           ↓                                                   │
│  deploying-applications (IaC + Deployment)                   │
│           ↓                                                   │
│  Production Infrastructure:                                   │
│  ├─ Kubernetes + Helm 4.0 + ArgoCD                          │
│  ├─ ECS Fargate (AWS containers)                            │
│  ├─ Cloud Run (GCP containers)                              │
│  ├─ Fly.io (global edge containers)                         │
│  └─ Docker Compose (development/small deployments)          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Taxonomy

### Tier 1: Deployment Strategies (Core Patterns)

#### 1.1 Kubernetes Orchestration
- **Helm 4.0** - Package manager (November 2025 release with architectural changes)
- **ArgoCD** - GitOps continuous deployment (declarative, self-healing)
- **Flux** - GitOps alternative (CNCF project, Kubernetes-native)
- **Service Mesh**: Linkerd (5-10% overhead) vs Istio (25-35% overhead)

#### 1.2 Serverless Platforms
- **Vercel** - Zero-config Next.js hosting (Edge Functions, 300+ edge locations)
- **AWS Lambda** - Event-driven compute (15-minute max, 10GB memory)
- **Google Cloud Functions** - HTTP/event triggers (Gen 2 with Cloud Run underneath)
- **Cloudflare Workers** - Edge compute (<5ms cold starts, V8 isolates, 200+ locations)
- **Deno Deploy** - TypeScript-native edge runtime

#### 1.3 Container Platforms
- **ECS Fargate** - AWS serverless containers (no EC2 management)
- **Google Cloud Run** - Fully managed containers (auto-scale to zero)
- **Fly.io** - Global edge containers (anycast, multi-region)
- **Railway** - Developer-friendly container platform

#### 1.4 Edge Functions
- **Cloudflare Workers** - <5ms cold starts, V8 isolates, 200+ locations
- **Deno Deploy** - TypeScript-first, global edge
- **Vercel Edge Functions** - Next.js integration
- **Hono** - Universal framework (runs on all edge runtimes)

### Tier 2: Infrastructure as Code (IaC Tools)

#### 2.1 TypeScript-First IaC
- **Pulumi** - Multi-language IaC (TypeScript primary, Apache 2.0)
- **SST v3** - Serverless Stack (built on Pulumi, TypeScript-native)
- **CDK for Terraform** - TypeScript with Terraform providers

#### 2.2 HCL-Based IaC
- **OpenTofu** - CNCF Terraform fork (open governance, MPL-2.0)
- **Terraform** - HashiCorp original (BSL 1.1 license since August 2023)

#### 2.3 Cloud-Native Tools
- **AWS CDK** - TypeScript/Python IaC for AWS
- **Azure Bicep** - Declarative IaC for Azure
- **Google Deployment Manager** - GCP-native IaC

### Tier 3: GitOps & Service Mesh

#### 3.1 GitOps Platforms
- **ArgoCD** - Kubernetes GitOps (CNCF graduated, declarative)
- **Flux** - GitOps toolkit (CNCF graduated, Kubernetes-native)
- **Rancher Fleet** - Multi-cluster GitOps

#### 3.2 Service Mesh
- **Linkerd** - Lightweight (5-10% overhead, Rust-based)
- **Istio** - Feature-rich (25-35% overhead, Envoy-based)
- **Cilium** - eBPF-based networking and security

#### 3.3 Serverless Databases (Scale-to-Zero)
- **Neon** - Serverless PostgreSQL (database branching, scale-to-zero)
- **PlanetScale** - Serverless MySQL (Vitess, non-blocking migrations)
- **Turso** - Edge SQLite (libSQL, microsecond latency)

---

## Context7 Library Research

### Primary IaC Recommendation: Pulumi

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Pulumi** | `/websites/pulumi` | High | 6,034 | 86.4 | TypeScript-first IaC |
| **Pulumi Docs** | `/pulumi/docs` | High | 9,525 | **94.6** | Comprehensive documentation |
| Pulumi Kubernetes | `/pulumi/pulumi-kubernetes` | High | 462 | - | K8s provider |
| Pulumi AWS | `/pulumi/pulumi-aws` | High | 125 | 35.4 | AWS provider |
| Pulumi Examples | `/pulumi/examples` | High | 1,667 | - | Production examples |

**Why Pulumi (Primary Recommendation)**:
- **TypeScript-first**: Same language as frontend (React, Next.js, Vite)
- **Apache 2.0**: Fully open source (no license restrictions)
- **94.6 Context7 score**: Highest-quality documentation (9,525 snippets)
- **Multi-cloud**: Supports AWS, GCP, Azure, Cloudflare, Kubernetes
- **Type safety**: Compile-time validation of infrastructure
- **Component model**: Reusable infrastructure components

### Alternative IaC: OpenTofu

**OpenTofu** (CNCF project, Terraform fork):
- **License**: MPL-2.0 (open governance, community-driven)
- **HCL syntax**: Familiar to Terraform users
- **Compatibility**: Drop-in Terraform replacement
- **Use when**: Team has existing HCL expertise or Terraform codebase

### Serverless TypeScript: SST v3

**SST (Serverless Stack)**:
- **Built on Pulumi**: TypeScript-native, inherits Pulumi benefits
- **Serverless-focused**: Optimized for AWS Lambda, API Gateway, S3
- **Live Lambda**: Local development with AWS services
- **Use when**: Building serverless applications on AWS

---

## Deployment Strategy Decision Framework

```
┌──────────────────────────────────────────────────────────────┐
│              Deployment Strategy Selection                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  WORKLOAD TYPE?                                               │
│  ├── COMPLEX MICROSERVICES (10+ services)                    │
│  │   └─ Kubernetes + ArgoCD/Flux (GitOps)                   │
│  │       ├─ Service mesh: Linkerd (5-10% overhead)          │
│  │       │   └─ Use when: Multi-team, security boundaries   │
│  │       ├─ Istio (25-35% overhead)                         │
│  │       │   └─ Use when: Advanced routing, observability   │
│  │       └─ Helm 4.0 for packaging                          │
│  │                                                           │
│  ├── VARIABLE TRAFFIC / COST-SENSITIVE                       │
│  │   └─ Serverless                                           │
│  │       ├─ Database: Neon, Turso (scale-to-zero)           │
│  │       │   └─ Neon: PostgreSQL with branching             │
│  │       │   └─ Turso: Edge SQLite (<1ms read latency)      │
│  │       ├─ Compute: Vercel, AWS Lambda, Cloud Functions    │
│  │       │   └─ Vercel: Next.js (zero-config)               │
│  │       │   └─ Lambda: Event-driven (15min max)            │
│  │       └─ Edge: Cloudflare Workers (<5ms cold start)      │
│  │           └─ 200+ locations, V8 isolates                 │
│  │                                                           │
│  ├── CONSISTENT LOAD / PREDICTABLE TRAFFIC                   │
│  │   └─ Containers (ECS, Cloud Run, Fly.io)                 │
│  │       ├─ ECS Fargate: AWS-native, serverless containers  │
│  │       ├─ Cloud Run: GCP, scale-to-zero containers        │
│  │       └─ Fly.io: Global edge, multi-region               │
│  │                                                           │
│  ├── GLOBAL LOW-LATENCY (<50ms)                              │
│  │   └─ Edge Functions + Edge Database                       │
│  │       ├─ Cloudflare Workers + D1 (SQLite)                │
│  │       └─ Deno Deploy + Turso (libSQL)                    │
│  │                                                           │
│  └── RAPID PROTOTYPING / STARTUP MVP                         │
│      └─ Managed Platform as a Service                        │
│          ├─ Vercel (Next.js, zero-config)                   │
│          ├─ Railway (any framework, simple DX)              │
│          └─ Render (auto-deploy from Git)                   │
│                                                               │
│  IaC CHOICE?                                                  │
│  ├─ TypeScript-first → Pulumi (Apache 2.0, multi-cloud)     │
│  ├─ HCL-based → OpenTofu (CNCF, Terraform-compatible)       │
│  └─ Serverless TypeScript → SST v3 (built on Pulumi)        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Kubernetes Deployment Patterns

### Helm 4.0 (November 2025 Release)

**Key Changes in Helm 4.0**:
- Enhanced security model
- Improved dependency management
- Better OCI registry support
- Breaking changes from Helm 3.x (review migration guide)

**Helm Chart Structure**:
```
my-app-chart/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration
├── values-production.yaml  # Production overrides
├── values-staging.yaml     # Staging overrides
├── templates/
│   ├── deployment.yaml     # Kubernetes Deployment
│   ├── service.yaml        # Kubernetes Service
│   ├── ingress.yaml        # Ingress configuration
│   ├── configmap.yaml      # ConfigMap
│   ├── secret.yaml         # Secrets (use sealed-secrets)
│   └── hpa.yaml            # Horizontal Pod Autoscaler
└── charts/                 # Dependency charts
```

### GitOps: ArgoCD vs Flux

| Feature | ArgoCD | Flux |
|---------|--------|------|
| **Maturity** | CNCF Graduated | CNCF Graduated |
| **UI** | Rich web UI | CLI-focused |
| **Multi-tenancy** | Built-in RBAC | Requires setup |
| **Complexity** | Higher learning curve | Simpler, Kubernetes-native |
| **Best for** | Platform teams, multi-cluster | DevOps automation, single cluster |

**ArgoCD Pattern** (Recommended for multi-team platforms):
```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: main
    path: k8s/manifests
    helm:
      valueFiles:
        - values-production.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**Flux Pattern** (Recommended for GitOps automation):
```yaml
# flux-kustomization.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./k8s/overlays/production
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-app-repo
```

### Service Mesh: Linkerd vs Istio

| Feature | Linkerd | Istio |
|---------|---------|-------|
| **Performance** | 5-10% overhead | 25-35% overhead |
| **Language** | Rust | C++ (Envoy) |
| **Complexity** | Simple, opinionated | Feature-rich, complex |
| **mTLS** | Automatic | Automatic |
| **Traffic Splitting** | Yes | Yes (more advanced) |
| **Best for** | Performance-critical, simplicity | Advanced routing, observability |

**When to Use Service Mesh**:
- ✅ Multi-team microservices (security boundaries)
- ✅ Zero-trust networking (mTLS required)
- ✅ Advanced traffic management (canary, blue-green)
- ❌ Simple monolith or 2-3 services (overhead not justified)
- ❌ Serverless architectures (incompatible)

---

## Serverless Databases (Scale-to-Zero)

### Database Comparison

| Database | Type | Key Feature | Cold Start | Pricing |
|----------|------|-------------|------------|---------|
| **Neon** | PostgreSQL | Database branching | <1s | Compute + storage separate |
| **PlanetScale** | MySQL (Vitess) | Non-blocking schema changes | <1s | Per-row pricing |
| **Turso** | SQLite (libSQL) | Edge deployment | Sub-ms | Per-request pricing |

### Neon PostgreSQL

**Key Features**:
- **Database Branching**: Create instant copies for testing (like Git branches)
- **Scale-to-Zero**: Automatically pause after inactivity, resume on first query
- **Separate Compute/Storage**: Pay only for what you use
- **PostgreSQL Compatibility**: Full Postgres 15/16 features

**Use Cases**:
- Development environments (branch per PR)
- Variable traffic applications
- Cost-sensitive projects

**Example Pulumi Integration**:
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as neon from "@pulumiverse/neon";

const project = new neon.Project("my-app", {
    name: "my-app-production",
    regionId: "aws-us-east-1",
});

const branch = new neon.Branch("main-branch", {
    projectId: project.id,
    name: "main",
});

export const connectionString = branch.connectionString;
```

### Turso (Edge SQLite)

**Key Features**:
- **Edge Deployment**: Deploy SQLite to 200+ locations
- **Sub-millisecond Reads**: <1ms read latency from edge
- **libSQL**: SQLite fork with improved replication
- **Multi-region Replication**: Automatic data replication

**Use Cases**:
- Edge functions (Cloudflare Workers, Deno Deploy)
- Global applications requiring low latency
- Read-heavy workloads

**Example with Cloudflare Workers**:
```typescript
import { createClient } from '@libsql/client/web';

export default {
  async fetch(request: Request, env: Env) {
    const client = createClient({
      url: env.TURSO_DATABASE_URL,
      authToken: env.TURSO_AUTH_TOKEN,
    });

    const result = await client.execute('SELECT * FROM users LIMIT 10');
    return new Response(JSON.stringify(result.rows));
  },
};
```

### PlanetScale MySQL

**Key Features**:
- **Non-blocking Schema Changes**: Deploy schema changes without downtime
- **Vitess-powered**: Google-scale MySQL (YouTube infrastructure)
- **Branching**: Database branches for development
- **Per-row Pricing**: Pay only for rows read/written

**Use Cases**:
- MySQL-dependent applications
- Frequent schema changes
- Predictable per-query pricing

---

## Edge Functions Deep Dive

### Cloudflare Workers

**Performance Characteristics**:
- **Cold Start**: <5ms (V8 isolates, not containers)
- **Locations**: 200+ global edge locations
- **Memory**: 128MB per request
- **CPU Time**: 50ms (free), 15s (paid)

**When to Use**:
- Global content delivery
- API gateway/middleware
- HTML rewriting (HTMLRewriter API)
- Edge authentication

**Example with Hono**:
```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.json({ message: 'Hello from Cloudflare Workers!' }))

app.get('/api/users/:id', async (c) => {
  const id = c.req.param('id')
  // Query Turso edge database
  const user = await db.query('SELECT * FROM users WHERE id = ?', [id])
  return c.json(user)
})

export default app
```

### Deno Deploy

**Key Features**:
- **TypeScript-native**: No build step required
- **Global Edge**: Fast cold starts (<50ms)
- **Web Standard APIs**: Fetch, WebSockets, WebCrypto
- **KV Store**: Integrated edge key-value store

**Use Cases**:
- TypeScript APIs
- Real-time applications (WebSockets)
- Edge rendering

**Example**:
```typescript
import { serve } from "https://deno.land/std/http/server.ts";

serve(async (req: Request) => {
  const url = new URL(req.url);

  if (url.pathname === "/api/hello") {
    return new Response(JSON.stringify({ message: "Hello from Deno Deploy" }), {
      headers: { "content-type": "application/json" },
    });
  }

  return new Response("Not Found", { status: 404 });
});
```

### Hono Universal Framework

**Why Hono**:
- **Runs Everywhere**: Cloudflare Workers, Deno, Bun, Node.js, Vercel Edge
- **Fast**: 3-4x faster than Express
- **Small**: 14KB bundle size
- **TypeScript-first**: Full type safety

**Example Portable API**:
```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'

const app = new Hono()

app.use('*', cors())
app.use('*', logger())

app.get('/health', (c) => c.json({ status: 'ok' }))

// Works on Cloudflare Workers, Deno, Node.js, Bun
export default app
```

---

## Infrastructure as Code Patterns

### Pulumi TypeScript Patterns

#### Multi-Stack Architecture

```typescript
// Pulumi.yaml
name: my-app
runtime: nodejs
description: My application infrastructure

// Pulumi.dev.yaml (development stack)
config:
  aws:region: us-east-1
  my-app:environment: development
  my-app:dbSize: small

// Pulumi.prod.yaml (production stack)
config:
  aws:region: us-east-1
  my-app:environment: production
  my-app:dbSize: large
```

#### Component Pattern

```typescript
// components/web-service.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

interface WebServiceArgs {
  imageTag: string;
  environment: pulumi.Input<{ [key: string]: pulumi.Input<string> }>;
  cpu: number;
  memory: number;
}

export class WebService extends pulumi.ComponentResource {
  public readonly url: pulumi.Output<string>;

  constructor(name: string, args: WebServiceArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:WebService", name, {}, opts);

    // Create ALB
    const alb = new awsx.lb.ApplicationLoadBalancer(`${name}-alb`, {
      listener: {
        port: 443,
        protocol: "HTTPS",
      },
    }, { parent: this });

    // Create ECS Cluster
    const cluster = new aws.ecs.Cluster(`${name}-cluster`, {}, { parent: this });

    // Create Fargate Service
    const service = new awsx.ecs.FargateService(`${name}-service`, {
      cluster: cluster.arn,
      taskDefinitionArgs: {
        container: {
          image: `my-repo:${args.imageTag}`,
          cpu: args.cpu,
          memory: args.memory,
          environment: args.environment,
          portMappings: [{
            containerPort: 3000,
            targetGroup: alb.defaultTargetGroup,
          }],
        },
      },
      desiredCount: 2,
    }, { parent: this });

    this.url = alb.loadBalancer.dnsName;
    this.registerOutputs({
      url: this.url,
    });
  }
}
```

#### Usage

```typescript
// index.ts
import * as pulumi from "@pulumi/pulumi";
import { WebService } from "./components/web-service";

const config = new pulumi.Config();
const environment = config.require("environment");
const dbUrl = config.requireSecret("dbUrl");

const webService = new WebService("my-app", {
  imageTag: "v1.2.3",
  environment: {
    NODE_ENV: environment,
    DATABASE_URL: dbUrl,
  },
  cpu: 512,
  memory: 1024,
});

export const appUrl = webService.url;
```

### OpenTofu Patterns

**When to Use OpenTofu**:
- Existing Terraform codebase (drop-in replacement)
- Team has HCL expertise
- Prefer CNCF governance model
- Avoid HashiCorp BSL license

**Migration from Terraform**:
```bash
# Install OpenTofu
brew install opentofu

# Replace terraform commands with tofu
tofu init
tofu plan
tofu apply

# State migration (automatic)
terraform state pull > terraform.tfstate.backup
tofu init -migrate-state
```

---

## Frontend Deployment Integration

### Next.js Deployment

#### Vercel (Recommended for Next.js)

**Why Vercel for Next.js**:
- Zero-config deployment (git push = deploy)
- Edge Functions (300+ locations)
- Image optimization (next/image)
- ISR (Incremental Static Regeneration)

**Deployment Steps**:
```bash
# Install Vercel CLI
npm i -g vercel

# Link project
vercel link

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

**Environment Variables**:
```bash
# .env.local (development)
DATABASE_URL=postgresql://localhost:5432/mydb
NEXT_PUBLIC_API_URL=http://localhost:3000

# Vercel dashboard (production)
# Add secrets via UI or CLI
vercel env add DATABASE_URL production
```

#### Alternative: Cloudflare Pages + Workers

**When to Use**:
- Need Cloudflare Workers integration
- Prefer Cloudflare ecosystem (R2, D1, KV)
- Global edge deployment

**Deployment**:
```bash
# Install Wrangler
npm i -g wrangler

# Login
wrangler login

# Deploy
wrangler pages deploy out
```

### Vite/React SPA Deployment

**Static Hosting Options**:
- **Cloudflare Pages**: Free, global CDN, automatic HTTPS
- **Netlify**: Git-based deploys, preview URLs
- **Vercel**: Zero-config, edge network
- **AWS S3 + CloudFront**: DIY, full control

**Pulumi Example (S3 + CloudFront)**:
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// S3 bucket for static files
const bucket = new aws.s3.Bucket("my-app-bucket", {
  website: {
    indexDocument: "index.html",
    errorDocument: "index.html", // SPA routing
  },
});

// Upload Vite build output
const bucketFolder = new aws.s3.BucketObject("index.html", {
  bucket: bucket.id,
  source: new pulumi.asset.FileAsset("./dist/index.html"),
  contentType: "text/html",
});

// CloudFront distribution
const cdn = new aws.cloudfront.Distribution("cdn", {
  enabled: true,
  origins: [{
    originId: bucket.id,
    domainName: bucket.websiteEndpoint,
    customOriginConfig: {
      originProtocolPolicy: "http-only",
      httpPort: 80,
      httpsPort: 443,
      originSslProtocols: ["TLSv1.2"],
    },
  }],
  defaultCacheBehavior: {
    targetOriginId: bucket.id,
    viewerProtocolPolicy: "redirect-to-https",
    allowedMethods: ["GET", "HEAD"],
    cachedMethods: ["GET", "HEAD"],
    forwardedValues: {
      queryString: false,
      cookies: { forward: "none" },
    },
  },
});

export const cdnUrl = cdn.domainName;
```

---

## Backend Deployment Integration

### FastAPI Deployment

#### ECS Fargate (AWS)

**Pulumi Example**:
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as awsx from "@pulumi/awsx";

const cluster = new awsx.ecs.Cluster("fastapi-cluster");

const service = new awsx.ecs.FargateService("fastapi-service", {
  cluster: cluster.arn,
  taskDefinitionArgs: {
    container: {
      image: "my-fastapi-app:latest",
      cpu: 512,
      memory: 1024,
      essential: true,
      portMappings: [{
        containerPort: 8000,
        hostPort: 8000,
        protocol: "tcp",
      }],
      environment: [
        { name: "ENV", value: "production" },
      ],
      secrets: [
        {
          name: "DATABASE_URL",
          valueFrom: "arn:aws:secretsmanager:...",
        },
      ],
    },
  },
  desiredCount: 2,
});
```

#### Cloud Run (GCP)

**Pulumi Example**:
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

const service = new gcp.cloudrun.Service("fastapi-service", {
  location: "us-central1",
  template: {
    spec: {
      containers: [{
        image: "gcr.io/my-project/fastapi-app:latest",
        ports: [{ containerPort: 8000 }],
        envs: [
          { name: "ENV", value: "production" },
        ],
        resources: {
          limits: {
            memory: "1Gi",
            cpu: "1000m",
          },
        },
      }],
    },
  },
});

// Allow public access
const iamPolicy = new gcp.cloudrun.IamMember("public-access", {
  service: service.name,
  location: service.location,
  role: "roles/run.invoker",
  member: "allUsers",
});

export const url = service.statuses[0].url;
```

### Rust (Axum/Actix) Deployment

#### Fly.io (Global Edge Containers)

**fly.toml**:
```toml
app = "my-axum-app"

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/rust"]

[env]
  RUST_LOG = "info"

[[services]]
  internal_port = 3000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80
    force_https = true

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

[services.concurrency]
  hard_limit = 250
  soft_limit = 200
```

**Deployment**:
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Create app
flyctl launch

# Deploy
flyctl deploy
```

---

## Skill Structure

```
deploying-applications/
├── init.md                           # This file - master plan
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── kubernetes-helm.md            # Helm 4.0 patterns
│   ├── kubernetes-gitops.md          # ArgoCD vs Flux
│   ├── kubernetes-service-mesh.md    # Linkerd vs Istio
│   ├── serverless-databases.md       # Neon, Turso, PlanetScale
│   ├── edge-functions.md             # Cloudflare Workers, Deno Deploy
│   ├── pulumi-guide.md               # Pulumi TypeScript patterns
│   ├── opentofu-guide.md             # OpenTofu/Terraform patterns
│   ├── sst-guide.md                  # SST v3 serverless
│   ├── nextjs-deployment.md          # Next.js deployment options
│   ├── vite-deployment.md            # Vite/React SPA deployment
│   ├── fastapi-deployment.md         # FastAPI container deployment
│   └── rust-deployment.md            # Rust (Axum/Actix) deployment
├── scripts/
│   ├── generate_k8s_manifests.py     # Generate Kubernetes YAML
│   ├── validate_deployment.py        # Pre-deployment validation
│   ├── pulumi_helpers.py             # Pulumi utility functions
│   └── helm_template_generator.py    # Helm chart scaffolding
├── examples/
│   ├── pulumi-aws-fargate/           # Complete ECS Fargate example
│   ├── pulumi-gcp-cloudrun/          # Complete Cloud Run example
│   ├── pulumi-k8s-argocd/            # Kubernetes + ArgoCD example
│   ├── sst-serverless/               # SST v3 serverless example
│   ├── cloudflare-workers-hono/      # Edge functions example
│   └── fly-io-rust/                  # Fly.io Rust deployment
└── assets/
    ├── templates/
    │   ├── pulumi/                   # Pulumi project templates
    │   ├── helm/                     # Helm chart templates
    │   └── k8s/                      # Kubernetes manifest templates
    └── diagrams/
        └── deployment-decision-tree.svg
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: deploying-applications
description: Production deployment patterns from Kubernetes to serverless and edge functions. Use when deploying applications to production, setting up CI/CD pipelines, or managing infrastructure as code. Covers Kubernetes (Helm 4.0, ArgoCD, Flux, Linkerd, Istio), serverless platforms (Vercel, Lambda, Cloud Run), edge functions (Cloudflare Workers, Deno Deploy), IaC (Pulumi, OpenTofu, SST), serverless databases (Neon, Turso, PlanetScale), and GitOps automation. Integrates with assembling-components for complete frontend-to-production workflow.
---
```

**Key Points**:
- **Gerund form**: `deploying-applications` (verb + -ing)
- **What + When**: Describes both functionality and use cases
- **Comprehensive coverage**: Lists all major technologies
- **Integration context**: Links to `assembling-components`
- **Under 1024 chars**: 673 characters (leaves room for updates)

---

## Quality Checklist

### Before Implementation (init.md → SKILL.md)

**Core Quality:**
- [x] Clear scope definition (Kubernetes → serverless → edge)
- [x] Context7 library research (Pulumi with 94.6 score)
- [x] Decision framework (ASCII diagram for workload types)
- [x] Multi-cloud support (AWS, GCP, Azure, Cloudflare)
- [x] Integration points with frontend skills (assembling-components)
- [x] Security best practices (GitOps, secrets management)
- [x] Performance benchmarks (Linkerd 5-10%, Cloudflare <5ms)

**Naming and Structure:**
- [x] Name uses gerund form (`deploying-applications`)
- [x] Name: lowercase, hyphens only (`deploying-applications`)
- [x] Description includes WHAT and WHEN
- [x] Description under 1024 chars (673 characters)
- [x] File paths use forward slashes
- [x] Progressive disclosure structure planned

**Content Organization:**
- [x] No time-sensitive information (future-proof patterns)
- [x] Consistent terminology (Kubernetes, serverless, edge)
- [x] Concrete examples (Pulumi TypeScript, Helm charts)
- [x] References one level deep from SKILL.md
- [x] Scripts are token-free automation

**Research Quality:**
- [x] Context7 IDs included for all major libraries
- [x] Trust scores documented
- [x] Snippet counts provided
- [x] Use case clarity
- [x] Alternative options explained

### During Implementation (SKILL.md creation)

**SKILL.md Quality:**
- [ ] Under 500 lines
- [ ] YAML frontmatter correct
- [ ] Progressive disclosure to references
- [ ] Working code examples
- [ ] Token-free scripts for automation
- [ ] Clear decision trees
- [ ] Integration patterns documented

**Testing:**
- [ ] At least 3 evaluations created
- [ ] Tested with Haiku (more guidance needed?)
- [ ] Tested with Sonnet (balanced clarity?)
- [ ] Tested with Opus (avoid over-explaining?)
- [ ] Real deployment scenarios validated

---

## Integration with Existing Skills

### Frontend Skills → Deployment

| Frontend Skill | Deployment Pattern | IaC Tool | Platform |
|----------------|-------------------|----------|----------|
| **assembling-components (Next.js)** | Vercel (zero-config) | Vercel CLI | Edge (300+ locations) |
| **assembling-components (Vite)** | Static hosting | Pulumi | S3 + CloudFront |
| **ai-chat** | Edge functions | Pulumi | Cloudflare Workers |
| **dashboards** | SSR or static | Pulumi/SST | ECS or Vercel |

### Backend Skills → Deployment

| Backend Skill | Deployment Pattern | IaC Tool | Platform |
|---------------|-------------------|----------|----------|
| **api-patterns (FastAPI)** | Containers | Pulumi | ECS Fargate |
| **api-patterns (Axum)** | Containers | Fly.io | Global edge |
| **databases-relational** | Managed DB | Pulumi | RDS or Neon |
| **databases-vector (Qdrant)** | K8s Helm | ArgoCD | Kubernetes |
| **observability** | K8s + LGTM | Helm 4.0 | Kubernetes |

---

## Success Metrics

This skill is successful when:

1. **Clear Deployment Decisions**: Users can select the right deployment strategy in < 2 minutes
2. **Working Infrastructure**: Generated Pulumi/OpenTofu code deploys without errors
3. **Cost Optimization**: Serverless database recommendations reduce costs by 50%+
4. **GitOps Automation**: ArgoCD/Flux setups enable hands-off deployments
5. **Integration Speed**: < 5 minutes from `assembling-components` to production deployment

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

## Research Sources

### Context7 Library Research
- Pulumi: `/websites/pulumi` (86.4 score, 6,034 snippets)
- Pulumi Docs: `/pulumi/docs` (94.6 score, 9,525 snippets)
- Pulumi Kubernetes: `/pulumi/pulumi-kubernetes` (462 snippets)
- Pulumi AWS: `/pulumi/pulumi-aws` (125 snippets)
- Pulumi Examples: `/pulumi/examples` (1,667 snippets)

### Industry Best Practices (December 2025)
- Helm 4.0 release notes (November 2025)
- CNCF OpenTofu project documentation
- ArgoCD GitOps patterns (CNCF graduated)
- Flux GitOps toolkit (CNCF graduated)
- Linkerd vs Istio performance benchmarks
- Cloudflare Workers V8 isolate architecture
- Neon serverless PostgreSQL branching
- Turso edge SQLite deployment patterns

### Integration References
- `assembling-components/init.md` - Frontend assembly patterns
- `api-patterns/init.md` - Backend API deployment needs
- `databases-*/init.md` - Database deployment requirements
- `observability/init.md` - Monitoring stack deployment

---

*Document Status: Planning Phase - Ready for SKILL.md Implementation*
*Next Steps: Create SKILL.md with progressive disclosure to reference files*
