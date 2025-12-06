# Deployment Strategies

Comprehensive guide to deployment strategies including blue-green, canary, rolling, recreate, and A/B testing patterns.

## Table of Contents

- [Strategy Overview](#strategy-overview)
- [Decision Matrix](#decision-matrix)
- [Rolling Deployment](#rolling-deployment)
- [Blue-Green Deployment](#blue-green-deployment)
- [Canary Deployment](#canary-deployment)
- [Recreate Deployment](#recreate-deployment)
- [A/B Testing](#ab-testing)
- [Implementation Patterns](#implementation-patterns)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Strategy Overview

Deployment strategies determine how application updates roll out to production.

### Quick Comparison

| Strategy | Downtime | Risk | Rollback Speed | Resource Cost | Complexity |
|----------|----------|------|----------------|---------------|------------|
| **Rolling** | None | Medium | Fast | Low (1x) | Low |
| **Blue-Green** | None | Low | Instant | High (2x) | Medium |
| **Canary** | None | Very Low | Fast | Medium (1.1-1.5x) | High |
| **Recreate** | Yes | High | Slow | Low (1x) | Very Low |
| **A/B Testing** | None | Low | Medium | Medium (1.5x) | High |

### Strategy Characteristics

**Rolling Deployment**:
- Gradual replacement of old version with new version
- No downtime, incremental updates
- Default strategy for most platforms

**Blue-Green Deployment**:
- Two identical environments (blue = current, green = new)
- Instant cutover via traffic switch
- Easy rollback, requires 2x resources

**Canary Deployment**:
- Small percentage of traffic to new version
- Gradual increase based on metrics
- Lowest risk, complex monitoring

**Recreate Deployment**:
- Stop all old instances, then start new ones
- Brief downtime, simplest approach
- Useful for stateful apps or dev environments

**A/B Testing**:
- Split traffic between versions based on criteria
- Long-running (days/weeks)
- Feature validation, not just deployment

## Decision Matrix

Select deployment strategy based on application characteristics and requirements.

### Decision Tree

```
DOWNTIME ACCEPTABLE?
├─ YES → Recreate
│   └─ Simplest, lowest resource cost
│
└─ NO → Continue...

ROLLBACK SPEED CRITICAL?
├─ YES (instant) → Blue-Green
│   └─ Requires 2x resources
│
└─ NO → Continue...

RISK TOLERANCE?
├─ VERY LOW (new feature/major change) → Canary
│   ├─ Complex monitoring required
│   └─ Gradual rollout (5% → 25% → 50% → 100%)
│
├─ LOW (validated change) → Blue-Green
│   └─ Instant rollback capability
│
├─ MEDIUM (incremental update) → Rolling
│   └─ Default for most deployments
│
└─ HIGH (dev/staging) → Recreate
    └─ Acceptable downtime

FEATURE VALIDATION NEEDED?
└─ YES → A/B Testing
    ├─ Split by user segment
    └─ Measure conversion metrics
```

### Selection Guidelines

**Use Rolling When**:
- Standard application updates
- Well-tested changes
- Cost optimization important
- Kubernetes default deployments

**Use Blue-Green When**:
- Zero-downtime mandatory
- Instant rollback required
- Database migrations (with backward compatibility)
- High-confidence releases

**Use Canary When**:
- Major version upgrades
- New features with unknown impact
- Complex distributed systems
- High-traffic production systems

**Use Recreate When**:
- Development/staging environments
- Stateful applications (single-instance databases)
- Downtime windows available
- Simple deployment pipeline

**Use A/B Testing When**:
- Feature flag validation
- UI/UX experiments
- Conversion optimization
- Long-running comparative analysis

## Rolling Deployment

Gradually replace old version pods with new version pods.

### How Rolling Works

```
Initial State: [v1] [v1] [v1] [v1]

Step 1: [v1] [v1] [v1] [v2]  (25% new)
Step 2: [v1] [v1] [v2] [v2]  (50% new)
Step 3: [v1] [v2] [v2] [v2]  (75% new)
Step 4: [v2] [v2] [v2] [v2]  (100% new)

Result: Zero downtime, gradual transition
```

### Kubernetes Implementation

**Deployment with Rolling Update**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max additional pods during update
      maxUnavailable: 1  # Max pods unavailable during update
  template:
    metadata:
      labels:
        app: my-app
        version: v2
    spec:
      containers:
      - name: my-app
        image: my-app:v2
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Update Command**:

```bash
# Update deployment image
kubectl set image deployment/my-app my-app=my-app:v2

# Monitor rollout status
kubectl rollout status deployment/my-app

# Pause rollout (if issues detected)
kubectl rollout pause deployment/my-app

# Resume rollout
kubectl rollout resume deployment/my-app

# Rollback to previous version
kubectl rollout undo deployment/my-app
```

### AWS ECS Rolling Deployment

```json
{
  "deploymentConfiguration": {
    "deploymentCircuitBreaker": {
      "enable": true,
      "rollback": true
    },
    "maximumPercent": 200,
    "minimumHealthyPercent": 100
  }
}
```

**Explanation**:
- `maximumPercent: 200` allows 2x tasks during deployment
- `minimumHealthyPercent: 100` ensures no capacity reduction
- Circuit breaker automatically rolls back on failure

### Configuration Parameters

**maxSurge**:
- Number of pods that can be created above desired count
- Value: number (e.g., `1`) or percentage (e.g., `25%`)
- Higher = faster rollout, more resources

**maxUnavailable**:
- Number of pods that can be unavailable during update
- Value: number (e.g., `1`) or percentage (e.g., `25%`)
- `0` = zero capacity reduction (safest)

**Common Configurations**:

```yaml
# Fast rollout (more resources)
maxSurge: 2
maxUnavailable: 1

# Conservative (minimal extra resources)
maxSurge: 1
maxUnavailable: 0

# Aggressive (faster, riskier)
maxSurge: 50%
maxUnavailable: 25%
```

## Blue-Green Deployment

Two identical environments with instant traffic cutover.

### How Blue-Green Works

```
Initial State:
  BLUE (v1) ← 100% traffic
  GREEN (idle)

Deploy New Version:
  BLUE (v1) ← 100% traffic
  GREEN (v2) ← 0% traffic (warming up)

Cutover:
  BLUE (v1) ← 0% traffic
  GREEN (v2) ← 100% traffic

Rollback (if needed):
  BLUE (v1) ← 100% traffic (instant switch back)
  GREEN (v2) ← 0% traffic
```

### Kubernetes Implementation

**Using Services and Labels**:

```yaml
# Service (routes traffic based on label)
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
    version: blue  # Switch to 'green' for cutover
  ports:
  - port: 80
    targetPort: 8080

---
# Blue Deployment (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: my-app:v1

---
# Green Deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app
        image: my-app:v2
```

**Cutover Process**:

```bash
# 1. Deploy green environment
kubectl apply -f my-app-green.yaml

# 2. Wait for green to be ready
kubectl wait --for=condition=available --timeout=300s deployment/my-app-green

# 3. Test green environment (port-forward for validation)
kubectl port-forward deployment/my-app-green 8080:8080

# 4. Switch traffic to green
kubectl patch service my-app -p '{"spec":{"selector":{"version":"green"}}}'

# 5. Monitor metrics (if issues, rollback)

# 6. If stable, delete blue deployment
kubectl delete deployment my-app-blue
```

### AWS CodeDeploy Blue-Green

```yaml
# appspec.yml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "arn:aws:ecs:region:account:task-definition/my-app:2"
        LoadBalancerInfo:
          ContainerName: "my-app"
          ContainerPort: 8080
        PlatformVersion: "LATEST"

Hooks:
  - BeforeInstall: "LambdaFunctionToValidateBeforeInstall"
  - AfterInstall: "LambdaFunctionToValidateAfterInstall"
  - BeforeAllowTraffic: "LambdaFunctionToValidateBeforeTrafficShift"
  - AfterAllowTraffic: "LambdaFunctionToValidateAfterTrafficShift"
```

### Pulumi Blue-Green (AWS)

```typescript
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

// Target group for blue environment
const blueTargetGroup = new aws.lb.TargetGroup("blue", {
    port: 8080,
    protocol: "HTTP",
    vpcId: vpcId,
    healthCheck: {
        path: "/health",
        interval: 30,
    },
});

// Target group for green environment
const greenTargetGroup = new aws.lb.TargetGroup("green", {
    port: 8080,
    protocol: "HTTP",
    vpcId: vpcId,
    healthCheck: {
        path: "/health",
        interval: 30,
    },
});

// Load balancer listener (switch target group for cutover)
const listener = new aws.lb.Listener("listener", {
    loadBalancerArn: loadBalancerArn,
    port: 80,
    defaultActions: [{
        type: "forward",
        targetGroupArn: blueTargetGroup.arn, // Change to greenTargetGroup.arn
    }],
});

// ECS Service (blue)
const blueService = new aws.ecs.Service("blue", {
    cluster: clusterArn,
    taskDefinition: blueTaskDefinition.arn,
    desiredCount: 3,
    loadBalancers: [{
        targetGroupArn: blueTargetGroup.arn,
        containerName: "my-app",
        containerPort: 8080,
    }],
});

// ECS Service (green)
const greenService = new aws.ecs.Service("green", {
    cluster: clusterArn,
    taskDefinition: greenTaskDefinition.arn,
    desiredCount: 3,
    loadBalancers: [{
        targetGroupArn: greenTargetGroup.arn,
        containerName: "my-app",
        containerPort: 8080,
    }],
});
```

## Canary Deployment

Gradual rollout to small percentage of traffic with monitoring.

### How Canary Works

```
Step 1: [v1] [v1] [v1] [v1] [v2]     5% canary
        ↓    ↓    ↓    ↓    ↓
        95%               5%

Step 2: [v1] [v1] [v1] [v2] [v2]     25% canary
        ↓    ↓    ↓    ↓    ↓
        75%          25%

Step 3: [v1] [v1] [v2] [v2] [v2]     50% canary
        ↓    ↓    ↓    ↓    ↓
        50%     50%

Step 4: [v2] [v2] [v2] [v2] [v2]     100% canary

Each step includes metrics monitoring and automatic rollback on failure.
```

### Kubernetes with Argo Rollouts

**Installation**:

```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

**Rollout Resource**:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  revisionHistoryLimit: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:v2
        ports:
        - containerPort: 8080
  strategy:
    canary:
      steps:
      - setWeight: 5       # 5% traffic to canary
      - pause: {duration: 2m}
      - setWeight: 25      # 25% traffic
      - pause: {duration: 5m}
      - setWeight: 50      # 50% traffic
      - pause: {duration: 5m}
      - setWeight: 75      # 75% traffic
      - pause: {duration: 5m}
      # Automatic promotion to 100% after final pause

      # Analysis for automatic rollback
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 1
        args:
        - name: service-name
          value: my-app
```

**Analysis Template (Prometheus)**:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 30s
    successCondition: result >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus.monitoring:9090
        query: |
          sum(rate(http_requests_total{
            service="{{args.service-name}}",
            status=~"2.."
          }[2m]))
          /
          sum(rate(http_requests_total{
            service="{{args.service-name}}"
          }[2m]))
```

**Rollout Commands**:

```bash
# Install kubectl plugin
brew install argoproj/tap/kubectl-argo-rollouts

# Watch rollout progress
kubectl argo rollouts get rollout my-app --watch

# Promote canary to next step
kubectl argo rollouts promote my-app

# Abort rollout (automatic rollback)
kubectl argo rollouts abort my-app

# List rollouts
kubectl argo rollouts list rollouts
```

### Istio Canary Deployment

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
  - my-app
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: my-app
        subset: v2
  - route:
    - destination:
        host: my-app
        subset: v1
      weight: 95
    - destination:
        host: my-app
        subset: v2
      weight: 5

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-app
spec:
  host: my-app
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### AWS Lambda Canary

```typescript
import * as aws from "@pulumi/aws";

const lambdaAlias = new aws.lambda.Alias("prod", {
    functionName: lambdaFunction.name,
    functionVersion: lambdaVersion.version,
    routingConfig: {
        additionalVersionWeights: {
            [newVersion.version]: 0.05, // 5% canary traffic
        },
    },
});

// Gradually increase weight in subsequent updates:
// 0.05 → 0.25 → 0.50 → 1.00
```

## Recreate Deployment

Stop all old instances before starting new ones.

### How Recreate Works

```
Step 1: [v1] [v1] [v1] [v1]  (running)
Step 2: [ ]  [ ]  [ ]  [ ]   (downtime)
Step 3: [v2] [v2] [v2] [v2]  (new version)

Downtime window: Time to stop old + start new
```

### Kubernetes Implementation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: Recreate  # All pods deleted before new ones created
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:v2
```

**Update Process**:

```bash
# Update deployment
kubectl apply -f deployment.yaml

# All v1 pods deleted immediately
# Then v2 pods created

# No gradual transition, brief downtime
```

### Use Cases for Recreate

**Stateful Single-Instance Applications**:
- Development databases
- Legacy monoliths
- Applications with file locks

**Scheduled Maintenance Windows**:
- Off-hours deployments
- Pre-announced downtime
- Coordinated with users

**Incompatible Version Transitions**:
- Breaking database schema changes
- Non-backward compatible APIs
- Major architecture changes

## A/B Testing

Long-running deployment with traffic split based on user attributes.

### How A/B Testing Works

```
Users arrive → Route by attribute → Version A or B
                                        ↓
                                    Measure metrics
                                        ↓
                                    Compare results
                                        ↓
                                    Choose winner
```

### A/B Testing vs Canary

| Aspect | Canary | A/B Testing |
|--------|--------|-------------|
| **Duration** | Hours/days | Days/weeks |
| **Goal** | Safe rollout | Feature validation |
| **Traffic Split** | Gradual increase | Fixed percentage |
| **Metrics** | Error rates, latency | Conversion, engagement |
| **Rollback** | Automatic | Manual decision |
| **Routing** | Random | User attribute (ID, region, etc.) |

### Kubernetes with Flagger

**Installation**:

```bash
kubectl apply -k github.com/fluxcd/flagger//kustomize/linkerd
```

**Canary Resource (A/B Mode)**:

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: my-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  service:
    port: 8080
  analysis:
    interval: 1h
    threshold: 10
    iterations: 10
    match:
      - headers:
          x-user-type:
            exact: "beta"  # Route beta users to canary
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: conversion-rate
      thresholdRange:
        min: 5.0
      interval: 1m
```

### Istio A/B Testing

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
  - my-app.example.com
  http:
  # Route by user ID (hash-based split)
  - match:
    - headers:
        user-id:
          regex: "^[0-4].*"  # User IDs starting 0-4 (50%)
    route:
    - destination:
        host: my-app
        subset: v2
  # Remaining traffic to v1
  - route:
    - destination:
        host: my-app
        subset: v1
```

### Feature Flag Integration

Combine deployment with feature flags for fine-grained control.

```typescript
// LaunchDarkly integration
import * as LaunchDarkly from 'launchdarkly-node-server-sdk';

const ldClient = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY);

app.get('/feature', async (req, res) => {
  const user = {
    key: req.user.id,
    custom: {
      region: req.user.region,
      plan: req.user.plan,
    },
  };

  const showNewFeature = await ldClient.variation(
    'new-feature-flag',
    user,
    false
  );

  if (showNewFeature) {
    // Serve new version
    res.json({ version: 'v2' });
  } else {
    // Serve old version
    res.json({ version: 'v1' });
  }
});
```

## Implementation Patterns

### Multi-Cloud Patterns

**Cloud Provider Services**:

| Provider | Rolling | Blue-Green | Canary |
|----------|---------|------------|--------|
| **AWS** | ECS/EKS | CodeDeploy, ALB | Lambda Aliases, App Mesh |
| **GCP** | GKE | Cloud Run Revisions | Traffic Splitting |
| **Azure** | AKS | Deployment Slots | Traffic Manager |
| **Cloudflare** | Workers Gradual Rollout | Workers Versions | Workers Routes |

### Serverless Deployments

**AWS Lambda with Canary**:

```yaml
# SAM template
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs20.x
      AutoPublishAlias: live
      DeploymentPreference:
        Type: Canary10Percent5Minutes
        Alarms:
          - !Ref ErrorAlarm
        Hooks:
          PreTraffic: !Ref PreTrafficHook
          PostTraffic: !Ref PostTrafficHook
```

**Available Deployment Types**:
- `Canary10Percent5Minutes` - 10% for 5 min, then 100%
- `Canary10Percent10Minutes` - 10% for 10 min, then 100%
- `Linear10PercentEvery1Minute` - +10% every minute
- `AllAtOnce` - Immediate 100%

### Edge Deployments

**Cloudflare Workers Gradual Rollout**:

```bash
# Deploy new version (0% traffic)
wrangler publish --new-version

# Route 10% traffic to new version
wrangler route --version=new --percentage=10

# Increase gradually
wrangler route --version=new --percentage=25
wrangler route --version=new --percentage=50
wrangler route --version=new --percentage=100
```

## Best Practices

### Pre-Deployment Validation

**Smoke Tests**:
```bash
# Test new version before cutover
curl -H "X-Canary: true" https://api.example.com/health
```

**Database Migrations**:
- Use backward-compatible migrations
- Deploy schema changes before code changes
- Test rollback procedures

**Dependency Checks**:
- Verify external service compatibility
- Check API version requirements
- Validate configuration changes

### Monitoring and Metrics

**Key Metrics to Monitor**:

```
Availability:
- Request success rate (target: >99.9%)
- Error rate by status code
- Uptime percentage

Performance:
- Response time (p50, p95, p99)
- Throughput (requests/second)
- Database query latency

Resources:
- CPU utilization
- Memory usage
- Network throughput
```

**Prometheus Queries**:

```promql
# Request success rate
sum(rate(http_requests_total{status=~"2.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))

# p95 latency
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)
```

### Automatic Rollback

**Conditions for Automatic Rollback**:
- Error rate exceeds threshold (e.g., 5%)
- Latency increases significantly (e.g., >2x baseline)
- Health check failures
- Memory/CPU saturation

**Kubernetes Example with Argo Rollouts**:

```yaml
strategy:
  canary:
    steps:
    - setWeight: 10
    - pause: {duration: 5m}
    analysis:
      templates:
      - templateName: error-rate
      args:
      - name: error-threshold
        value: "0.05"  # 5% error rate triggers rollback
```

### Communication and Documentation

**Deployment Checklist**:
1. Review changes and test coverage
2. Check database migration compatibility
3. Verify rollback procedure
4. Schedule deployment window
5. Notify stakeholders
6. Prepare incident response plan
7. Monitor metrics during deployment
8. Document any issues encountered

**Runbook Template**:
```markdown
# Deployment Runbook: [Feature Name]

## Pre-Deployment
- [ ] Schema migrations tested
- [ ] Rollback procedure verified
- [ ] Monitoring dashboards prepared

## Deployment Steps
1. Deploy green environment
2. Run smoke tests
3. Switch 5% traffic
4. Monitor for 10 minutes
5. Proceed to 25% if stable

## Rollback Procedure
1. Switch traffic back to blue
2. Investigate logs
3. Fix issues
4. Redeploy

## Stakeholders
- Team: @platform-team
- On-call: @sre-oncall
```

## Troubleshooting

### Common Issues

**Deployment Stuck in Progress**:

```bash
# Check pod status
kubectl get pods -l app=my-app

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check rollout status
kubectl rollout status deployment/my-app

# Describe deployment
kubectl describe deployment my-app
```

**Traffic Not Switching (Blue-Green)**:

```bash
# Verify service selector
kubectl get service my-app -o yaml | grep selector

# Check endpoint health
kubectl get endpoints my-app

# Verify pod labels
kubectl get pods --show-labels
```

**Canary Rollback Loop**:

```bash
# Check analysis results
kubectl argo rollouts get rollout my-app

# View analysis logs
kubectl logs -n argo-rollouts deployment/argo-rollouts

# Review metrics query
kubectl describe analysistemplate success-rate
```

### Performance Degradation

**Symptoms**:
- Increased latency during deployment
- Intermittent errors
- Resource exhaustion

**Diagnosis**:

```bash
# Check resource usage
kubectl top pods

# Review resource limits
kubectl describe pod <pod-name> | grep -A 5 "Limits:"

# Check readiness probe
kubectl describe pod <pod-name> | grep -A 10 "Readiness:"
```

**Solutions**:
- Adjust `maxSurge` and `maxUnavailable`
- Increase resource requests/limits
- Extend readiness probe initial delay
- Reduce deployment batch size

### Rollback Procedures

**Immediate Rollback (Kubernetes)**:

```bash
# Rollback to previous revision
kubectl rollout undo deployment/my-app

# Rollback to specific revision
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app --to-revision=3

# Verify rollback
kubectl rollout status deployment/my-app
```

**Blue-Green Rollback**:

```bash
# Switch traffic back to blue
kubectl patch service my-app -p '{"spec":{"selector":{"version":"blue"}}}'

# Verify traffic
kubectl get service my-app -o yaml | grep selector
```

**Canary Rollback**:

```bash
# Abort rollout (automatic rollback)
kubectl argo rollouts abort my-app

# Verify stable version
kubectl argo rollouts status my-app
```

## Additional Resources

- Argo Rollouts documentation: https://argoproj.github.io/argo-rollouts/
- Flagger documentation: https://flagger.app/
- Istio traffic management: https://istio.io/latest/docs/concepts/traffic-management/
- AWS deployment strategies: https://docs.aws.amazon.com/whitepapers/latest/overview-deployment-options/deployment-strategies.html
