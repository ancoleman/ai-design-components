---
sidebar_position: 11
title: Deploying Applications
description: Deployment patterns from Kubernetes to serverless and edge functions
tags: [backend, deployment, kubernetes, serverless, iac, gitops]
---

# Deploying Applications

Production deployment patterns from Kubernetes to serverless and edge functions. Bridges the gap from application assembly to production infrastructure.

## When to Use

Use when:
- Deploying applications to production infrastructure
- Setting up CI/CD pipelines and GitOps workflows
- Choosing between Kubernetes, serverless, or edge deployment
- Implementing Infrastructure as Code (Pulumi, OpenTofu, SST)
- Migrating from manual deployment to automated infrastructure

## Multi-Language Support

This skill provides patterns for:
- **Infrastructure as Code**: Pulumi (TypeScript), OpenTofu (HCL), SST v3 (TypeScript)
- **GitOps**: ArgoCD, Flux (Kubernetes)
- **Serverless**: Vercel (Next.js), AWS Lambda, Cloud Functions
- **Edge**: Cloudflare Workers (Hono), Deno Deploy

## Deployment Strategy Decision Tree

```
WORKLOAD TYPE?

├── COMPLEX MICROSERVICES (10+ services)
│   └─ Kubernetes + ArgoCD/Flux (GitOps)
│       ├─ Helm 4.0 for packaging
│       ├─ Service mesh: Linkerd (5-10% overhead) or Istio (25-35%)
│       └─ See references/kubernetes-patterns.md

├── VARIABLE TRAFFIC / COST-SENSITIVE
│   └─ Serverless
│       ├─ Database: Neon/Turso (scale-to-zero)
│       ├─ Compute: Vercel, AWS Lambda, Cloud Functions
│       ├─ Edge: Cloudflare Workers (under 5ms cold start)
│       └─ See references/serverless-dbs.md

├── CONSISTENT LOAD / PREDICTABLE TRAFFIC
│   └─ Containers (ECS, Cloud Run, Fly.io)
│       ├─ ECS Fargate: AWS-native, serverless containers
│       ├─ Cloud Run: GCP, scale-to-zero containers
│       └─ Fly.io: Global edge, multi-region

├── GLOBAL LOW-LATENCY (under 50ms)
│   └─ Edge Functions + Edge Database
│       ├─ Cloudflare Workers + D1 (SQLite)
│       ├─ Deno Deploy + Turso (libSQL)
│       └─ See references/edge-functions.md

└── RAPID PROTOTYPING / STARTUP MVP
    └─ Managed Platform as a Service
        ├─ Vercel (Next.js, zero-config)
        ├─ Railway (any framework)
        └─ Render (auto-deploy from Git)
```

## Core Concepts

### Infrastructure as Code (IaC)

Define infrastructure using code instead of manual configuration.

**Primary: Pulumi (TypeScript)**
- TypeScript-first (same language as React/Next.js)
- Multi-cloud support (AWS, GCP, Azure, Cloudflare)
- Trust score: 94.6/100, 9,525 code snippets

**Alternative: OpenTofu (HCL)**
- CNCF project, Terraform-compatible
- MPL-2.0 license (open governance)
- Drop-in Terraform replacement

**Serverless: SST v3 (TypeScript)**
- Built on Pulumi
- Optimized for AWS Lambda, API Gateway
- Live Lambda development

### GitOps Deployment

Declarative infrastructure with Git as source of truth.

**ArgoCD** (Recommended for platform teams):
- Rich web UI
- Built-in RBAC and multi-tenancy
- Self-healing deployments

**Flux** (Recommended for DevOps automation):
- Kubernetes-native
- CLI-focused
- Simpler architecture

### Service Mesh

Optional layer for microservices communication, security, and observability.

**When to Use Service Mesh**:
- Multi-team microservices (security boundaries)
- Zero-trust networking (mTLS required)
- Advanced traffic management (canary, blue-green)

**When NOT to Use**:
- Simple monolith or 2-3 services (overhead not justified)
- Serverless architectures (incompatible)

**Linkerd** (Performance-focused):
- 5-10% overhead
- Rust-based
- Simple, opinionated

**Istio** (Feature-rich):
- 25-35% overhead
- C++ (Envoy)
- Advanced routing, observability

## Quick Start Workflows

### Workflow 1: Deploy Next.js to Vercel (Zero-Config)

```bash
# Install Vercel CLI
npm i -g vercel

# Link project
vercel link

# Deploy to production
vercel --prod
```

### Workflow 2: Deploy to Kubernetes with ArgoCD

1. Create Helm chart
2. Push chart to Git repository
3. Create ArgoCD Application
4. ArgoCD syncs automatically

### Workflow 3: Deploy Serverless with Pulumi

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Create Lambda function
const lambda = new aws.lambda.Function("api", {
    runtime: "nodejs20.x",
    handler: "index.handler",
    role: role.arn,
    code: new pulumi.asset.FileArchive("./dist"),
});

export const apiUrl = lambda.invokeArn;
```

### Workflow 4: Deploy Edge Function to Cloudflare Workers

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/api/hello', (c) => {
  return c.json({ message: 'Hello from edge!' })
})

export default app
```

Deploy with Wrangler:
```bash
wrangler deploy
```

## Serverless Databases

| Database | Type | Key Feature | Best For |
|----------|------|-------------|----------|
| **Neon** | PostgreSQL | Database branching, scale-to-zero | Development workflows, preview environments |
| **PlanetScale** | MySQL | Non-blocking schema changes | MySQL apps, zero-downtime migrations |
| **Turso** | SQLite | Edge deployment, low latency | Edge functions, global distribution |

## Edge Functions

**Cloudflare Workers**:
- Under 5ms cold starts (V8 isolates)
- 200+ edge locations
- 128MB memory per request

**Deno Deploy**:
- TypeScript-native
- Web Standard APIs
- Global edge (under 50ms)

**Hono Framework**:
- Runs on all edge runtimes
- 14KB bundle size
- TypeScript-first

## Best Practices

### Security
- Use secrets management (AWS Secrets Manager, Vault)
- Enable mTLS for service-to-service communication
- Implement least-privilege IAM roles
- Scan container images for vulnerabilities

### Cost Optimization
- Use serverless databases for variable traffic (scale-to-zero)
- Enable horizontal pod autoscaling (HPA) in Kubernetes
- Right-size compute resources (CPU/memory)
- Use spot instances for non-critical workloads

### Performance
- Deploy close to users (edge functions for global apps)
- Use CDN for static assets (CloudFront, Cloudflare)
- Implement caching strategies (Redis, CloudFront)
- Monitor cold start times for serverless

### Reliability
- Implement health checks (Kubernetes liveness/readiness probes)
- Set up auto-scaling (HPA, Lambda concurrency)
- Use multi-region deployments for critical services
- Implement circuit breakers and retries

## Troubleshooting

### Deployment Failures

**Kubernetes pod fails to start**:
1. Check pod logs: `kubectl logs <pod-name>`
2. Describe pod: `kubectl describe pod <pod-name>`
3. Verify resource limits and requests
4. Check image pull errors (imagePullSecrets)

**Serverless cold starts too slow**:
1. Reduce bundle size (tree-shaking, code splitting)
2. Use provisioned concurrency (AWS Lambda)
3. Consider edge functions (Cloudflare Workers)
4. Optimize initialization code

**GitOps sync errors (ArgoCD/Flux)**:
1. Verify Git repository access
2. Check manifest validity (`kubectl apply --dry-run`)
3. Review sync policies (prune, selfHeal)
4. Check ArgoCD/Flux logs

## Migration Patterns

### From Manual to IaC

1. Inventory existing infrastructure
2. Start with non-critical environments (dev, staging)
3. Use Pulumi/OpenTofu to codify infrastructure
4. Test in staging before production
5. Gradual migration (one service at a time)

### From Terraform to OpenTofu

```bash
# Install OpenTofu
brew install opentofu

# Migrate state
terraform state pull > terraform.tfstate.backup
tofu init -migrate-state
tofu plan
tofu apply
```

### From EC2 to Containers

1. Containerize application (create Dockerfile)
2. Test locally (Docker Compose)
3. Deploy to staging (ECS/Cloud Run/Kubernetes)
4. Monitor performance and costs
5. Cutover production traffic (blue-green deployment)

### From Containers to Serverless

1. Identify stateless services
2. Refactor to serverless-friendly patterns
3. Use serverless databases (Neon/Turso)
4. Deploy to Lambda/Cloud Functions
5. Monitor cold starts and costs

## Integration with Other Skills

This skill provides deployment strategies for:
- **API Patterns**: Deploy REST/GraphQL APIs
- **Databases**: Deploy PostgreSQL, MongoDB, vector databases
- **Real-time Sync**: Deploy WebSocket/SSE servers
- **Observability**: Deploy LGTM stack (Loki, Grafana, Tempo, Mimir)
- **AI/ML**: Deploy vLLM model serving, RAG pipelines

## Related Skills

- [API Patterns](./implementing-api-patterns) - Deploy backend APIs
- [Observability](./implementing-observability) - Deploy monitoring infrastructure
- [Model Serving](./model-serving) - Deploy LLM serving infrastructure
- [Relational Databases](./using-relational-databases) - Deploy PostgreSQL/MySQL

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/deploying-applications)
- Pulumi: https://www.pulumi.com/
- OpenTofu: https://opentofu.org/
- ArgoCD: https://argo-cd.readthedocs.io/
- Cloudflare Workers: https://workers.cloudflare.com/
- Neon: https://neon.tech/
