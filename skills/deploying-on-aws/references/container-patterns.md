# AWS Container Patterns

## Table of Contents

- [ECS Service Patterns](#ecs-service-patterns)
- [EKS Cluster Patterns](#eks-cluster-patterns)
- [Fargate vs EC2 Launch Types](#fargate-vs-ec2-launch-types)
- [Task Definition Best Practices](#task-definition-best-practices)
- [Service Discovery and Load Balancing](#service-discovery-and-load-balancing)
- [Auto Scaling Strategies](#auto-scaling-strategies)
- [Service Connect (Service Mesh)](#service-connect-service-mesh)
- [EKS Pod Identities](#eks-pod-identities)
- [Container Security](#container-security)
- [Logging and Monitoring](#logging-and-monitoring)
- [Cost Optimization](#cost-optimization)
- [Anti-Patterns](#anti-patterns)

## ECS Service Patterns

### Basic Web Application (Fargate + ALB)

**Pattern:** Containerized web service with auto-scaling and load balancing.

**Architecture:**
```
Internet → ALB (Application Load Balancer)
           → Target Group
             → ECS Service (Fargate tasks)
               → RDS or DynamoDB
               → ElastiCache (optional)
```

**Use When:**
- Building containerized web applications
- Need auto-scaling without managing servers
- Docker-based deployment workflow
- Team lacks Kubernetes expertise

**Task Definition Components:**
```yaml
TaskDefinition:
  Family: web-app
  NetworkMode: awsvpc  # Required for Fargate
  RequiresCompatibilities:
    - FARGATE
  Cpu: '512'  # 0.5 vCPU
  Memory: '1024'  # 1 GB
  ExecutionRoleArn: !GetAtt ExecutionRole.Arn  # Pull image, logs
  TaskRoleArn: !GetAtt TaskRole.Arn  # Container permissions

  ContainerDefinitions:
    - Name: web
      Image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/web-app:latest
      PortMappings:
        - ContainerPort: 80
          Protocol: tcp
      Environment:
        - Name: NODE_ENV
          Value: production
      Secrets:
        - Name: DB_PASSWORD
          ValueFrom: arn:aws:secretsmanager:us-east-1:123456789012:secret:db-pass
      LogConfiguration:
        LogDriver: awslogs
        Options:
          awslogs-group: /ecs/web-app
          awslogs-region: us-east-1
          awslogs-stream-prefix: web
      HealthCheck:
        Command:
          - CMD-SHELL
          - curl -f http://localhost/health || exit 1
        Interval: 30
        Timeout: 5
        Retries: 3
        StartPeriod: 60
```

**Service Configuration:**
```yaml
Service:
  ServiceName: web-service
  Cluster: !Ref ECSCluster
  TaskDefinition: !Ref TaskDefinition
  DesiredCount: 2
  LaunchType: FARGATE

  NetworkConfiguration:
    AwsvpcConfiguration:
      Subnets:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      SecurityGroups:
        - !Ref ServiceSecurityGroup
      AssignPublicIp: DISABLED

  LoadBalancers:
    - TargetGroupArn: !Ref TargetGroup
      ContainerName: web
      ContainerPort: 80

  HealthCheckGracePeriodSeconds: 60

  DeploymentConfiguration:
    MaximumPercent: 200
    MinimumHealthyPercent: 100
    DeploymentCircuitBreaker:
      Enable: true
      Rollback: true
```

**Cost Estimate (2 tasks, 24/7):**
- Fargate (0.5 vCPU, 1GB): ~$35/month
- ALB: ~$20/month
- Data transfer: ~$5/month
- **Total: ~$60/month**

### Background Worker Pattern

**Pattern:** Process asynchronous jobs from SQS queue.

**Architecture:**
```
SQS Queue → ECS Service (Fargate tasks)
             → DynamoDB (job status)
             → S3 (results)
```

**Use When:**
- Processing background jobs (image processing, report generation)
- Need auto-scaling based on queue depth
- Variable workload patterns
- Prefer containers over Lambda (>15 min runtime, >10GB memory)

**Task Definition Differences:**
```yaml
ContainerDefinitions:
  - Name: worker
    Image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/worker:latest
    # No PortMappings needed
    Environment:
      - Name: QUEUE_URL
        Value: !Ref WorkQueue
      - Name: BATCH_SIZE
        Value: '10'
    Essential: true
```

**Service Configuration:**
```yaml
Service:
  ServiceName: worker-service
  DesiredCount: 1  # Scale based on queue depth
  # No LoadBalancers configuration
```

**Auto Scaling by Queue Depth:**
```yaml
ScalableTarget:
  ServiceNamespace: ecs
  ResourceId: !Sub "service/${Cluster}/${ServiceName}"
  ScalableDimension: ecs:service:DesiredCount
  MinCapacity: 1
  MaxCapacity: 20

ScalingPolicy:
  PolicyType: TargetTrackingScaling
  TargetTrackingScalingPolicyConfiguration:
    CustomizedMetricSpecification:
      MetricName: ApproximateNumberOfMessagesVisible
      Namespace: AWS/SQS
      Statistic: Average
      Dimensions:
        - Name: QueueName
          Value: !GetAtt WorkQueue.QueueName
    TargetValue: 100  # Target 100 messages per task
    ScaleInCooldown: 300
    ScaleOutCooldown: 60
```

### Scheduled Task Pattern

**Pattern:** Run containerized cron jobs using EventBridge.

**Architecture:**
```
EventBridge Rule (schedule) → ECS Task (Fargate)
                               → Process data
                               → Store results in S3
```

**Use When:**
- Scheduled batch processing
- Need more than 15 minutes runtime (Lambda limit)
- Require more than 10 GB memory
- Complex dependencies or large Docker images

**EventBridge Rule:**
```yaml
ScheduledRule:
  ScheduleExpression: cron(0 2 * * ? *)  # 2 AM UTC daily
  State: ENABLED
  Targets:
    - Arn: !GetAtt ECSCluster.Arn
      RoleArn: !GetAtt EventsRole.Arn
      EcsParameters:
        TaskDefinitionArn: !Ref TaskDefinition
        LaunchType: FARGATE
        NetworkConfiguration:
          AwsVpcConfiguration:
            Subnets:
              - !Ref PrivateSubnet1
            SecurityGroups:
              - !Ref TaskSecurityGroup
            AssignPublicIp: DISABLED
        TaskCount: 1
```

**Benefits over Lambda:**
- No 15-minute timeout
- Up to 120 GB memory (Fargate)
- More familiar Docker ecosystem
- Can use same image as production service

## EKS Cluster Patterns

### Production-Ready EKS Cluster

**Pattern:** Managed Kubernetes cluster with best practices.

**Architecture:**
```
VPC (10.0.0.0/16)
├── Public Subnets (NAT Gateways, Load Balancers)
├── Private Subnets (EKS worker nodes)
└── Database Subnets (RDS, ElastiCache)

EKS Control Plane (AWS-managed)
└── Node Groups (EC2 or Fargate)
    └── Pods (application containers)
```

**Use When:**
- Team has Kubernetes expertise
- Need Kubernetes ecosystem (Helm, Operators, Istio)
- Multi-cloud or hybrid cloud strategy
- Complex orchestration requirements
- Migrating from on-premises Kubernetes

**Cluster Configuration:**
```yaml
EKSCluster:
  Name: production-cluster
  Version: '1.28'
  RoleArn: !GetAtt ClusterRole.Arn

  ResourcesVpcConfig:
    SubnetIds:
      - !Ref PrivateSubnet1
      - !Ref PrivateSubnet2
      - !Ref PrivateSubnet3
    EndpointPublicAccess: false  # Private cluster
    EndpointPrivateAccess: true
    SecurityGroupIds:
      - !Ref ClusterSecurityGroup

  Logging:
    ClusterLogging:
      EnabledTypes:
        - Type: api
        - Type: audit
        - Type: authenticator
        - Type: controllerManager
        - Type: scheduler

  EncryptionConfig:
    - Resources:
        - secrets
      Provider:
        KeyArn: !GetAtt KMSKey.Arn
```

**Managed Node Group (Recommended):**
```yaml
NodeGroup:
  ClusterName: !Ref EKSCluster
  NodegroupName: general-purpose
  NodeRole: !GetAtt NodeRole.Arn

  Subnets:
    - !Ref PrivateSubnet1
    - !Ref PrivateSubnet2

  ScalingConfig:
    MinSize: 2
    MaxSize: 10
    DesiredSize: 3

  InstanceTypes:
    - t3.medium
    - t3a.medium  # AMD alternative, 10% cheaper

  AmiType: AL2_x86_64  # Amazon Linux 2
  CapacityType: ON_DEMAND  # or SPOT for 70% savings

  UpdateConfig:
    MaxUnavailable: 1  # Rolling updates

  Labels:
    environment: production
    workload-type: general

  Taints:
    - Key: dedicated
      Value: general
      Effect: NoSchedule
```

**Fargate Profile (Serverless Nodes):**
```yaml
FargateProfile:
  ClusterName: !Ref EKSCluster
  FargateProfileName: serverless-workloads
  PodExecutionRoleArn: !GetAtt FargateRole.Arn

  Subnets:
    - !Ref PrivateSubnet1
    - !Ref PrivateSubnet2

  Selectors:
    - Namespace: serverless
      Labels:
        compute-type: fargate
    - Namespace: kube-system
      Labels:
        k8s-app: kube-dns  # CoreDNS on Fargate
```

**Cost Breakdown:**
- EKS control plane: $73/month
- Worker nodes (3x t3.medium, 24/7): ~$94/month
- NAT Gateways (2x): ~$65/month
- Data transfer: ~$10/month
- **Total: ~$242/month minimum**

### EKS Auto Mode (2024+ Feature)

**Pattern:** Fully managed node lifecycle, auto-scaling, and upgrades.

**Use When:**
- Want maximum automation
- Minimize operational overhead
- Acceptable with AWS-managed node pools
- Cost is less critical than simplicity

**Configuration:**
```yaml
EKSCluster:
  ComputeConfig:
    Enabled: true  # Enable Auto Mode
    NodePools:
      - general-purpose  # AWS-managed
    NodeRoleArn: !GetAtt AutoModeNodeRole.Arn
```

**Auto Mode Features:**
- Automatic node provisioning
- Auto-scaling without Cluster Autoscaler
- Automated OS patches and upgrades
- Built-in cost optimization

**Cost Impact:**
- ~10-15% higher than self-managed nodes
- Savings from reduced operational overhead
- Automatic spot instance usage

### Multi-Tenant EKS Pattern

**Pattern:** Isolated namespaces with resource quotas and network policies.

**Use When:**
- Multiple teams or applications sharing cluster
- Need cost efficiency (shared control plane)
- Strong isolation requirements
- Centralized cluster management

**Namespace Isolation:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
  labels:
    team: team-a
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "5"
    services.loadbalancers: "2"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-limits
  namespace: team-a
spec:
  limits:
    - max:
        cpu: "4"
        memory: 8Gi
      min:
        cpu: "100m"
        memory: 128Mi
      type: Container
```

**Network Policies (Deny by Default):**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: team-a
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-within-namespace
  namespace: team-a
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector: {}  # Allow from same namespace
```

**RBAC (Role-Based Access Control):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: team-a-developer
  namespace: team-a
rules:
  - apiGroups: ["", "apps", "batch"]
    resources: ["pods", "deployments", "jobs", "services"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: [""]
    resources: ["secrets", "configmaps"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-a-developers
  namespace: team-a
subjects:
  - kind: Group
    name: team-a
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: team-a-developer
  apiGroup: rbac.authorization.k8s.io
```

## Fargate vs EC2 Launch Types

### Decision Matrix

| Factor | Fargate | EC2 |
|--------|---------|-----|
| **Management** | AWS manages instances | Self-managed instances |
| **Pricing** | Per task-second | Per instance-hour |
| **Scaling** | Task-level (instant) | Instance-level (slower) |
| **Cost (predictable)** | Higher | Lower (RI/SP savings) |
| **Cost (variable)** | Lower | Higher (idle capacity) |
| **Start Time** | ~30 seconds | Instant (if capacity) |
| **Instance Access** | No SSH access | Full SSH access |
| **Customization** | Limited | Full control |
| **Spot Support** | Fargate Spot (70% off) | EC2 Spot (70% off) |

### Cost Comparison Example

**Workload:** Web service, 2 vCPU, 4 GB RAM, 24/7

**Fargate:**
- Pricing: $0.04048/hour (2 vCPU) + $0.004445/hour per GB = ~$0.0587/hour
- Monthly: $0.0587 × 730 hours = $42.85/month

**EC2 (t3.medium: 2 vCPU, 4 GB):**
- On-Demand: $0.0416/hour = $30.37/month
- 1-year Reserved Instance: $0.0208/hour = $15.18/month
- 3-year Reserved Instance: $0.0125/hour = $9.13/month

**Recommendation:**
- **Variable traffic:** Fargate (scale to zero)
- **Predictable 24/7:** EC2 with Reserved Instances
- **Development/Test:** Fargate (simpler, pay only when testing)
- **Production high-volume:** EC2 with RI (50-70% cost savings)

### Fargate Spot

**Pattern:** Run fault-tolerant tasks at 70% discount.

**Use When:**
- Batch processing jobs
- CI/CD build workers
- Data processing pipelines
- Development/test environments

**Configuration:**
```yaml
Service:
  CapacityProviderStrategy:
    - CapacityProvider: FARGATE_SPOT
      Weight: 4
      Base: 0
    - CapacityProvider: FARGATE
      Weight: 1
      Base: 2  # Always maintain 2 on-demand tasks
```

**Interruption Handling:**
- 2-minute warning before interruption
- Listen for SIGTERM signal
- Gracefully finish current work
- Task automatically restarted

**Python Example:**
```python
import signal
import sys

def sigterm_handler(signum, frame):
    print("SIGTERM received, gracefully shutting down")
    # Finish current work
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

# Main processing loop
while True:
    process_batch()
```

## Task Definition Best Practices

### Resource Allocation

**CPU and Memory Combinations (Fargate):**

| CPU (vCPU) | Memory Options (GB) |
|------------|---------------------|
| 0.25 | 0.5, 1, 2 |
| 0.5 | 1, 2, 3, 4 |
| 1 | 2, 3, 4, 5, 6, 7, 8 |
| 2 | 4-16 (1 GB increments) |
| 4 | 8-30 (1 GB increments) |
| 8 | 16-60 (4 GB increments) |
| 16 | 32-120 (8 GB increments) |

**Right-Sizing Approach:**
1. Start with 0.5 vCPU, 1 GB (common web apps)
2. Monitor CloudWatch metrics (CPUUtilization, MemoryUtilization)
3. Increase if consistently >70% utilization
4. Decrease if consistently <30% utilization

### Health Checks

**Container Health Check:**
```yaml
HealthCheck:
  Command:
    - CMD-SHELL
    - curl -f http://localhost:8080/health || exit 1
  Interval: 30  # Seconds between checks
  Timeout: 5  # Max time for check to complete
  Retries: 3  # Consecutive failures before unhealthy
  StartPeriod: 60  # Grace period for startup
```

**Load Balancer Health Check:**
```yaml
TargetGroup:
  HealthCheckPath: /health
  HealthCheckProtocol: HTTP
  HealthCheckIntervalSeconds: 30
  HealthCheckTimeoutSeconds: 5
  HealthyThresholdCount: 2  # Consecutive successes
  UnhealthyThresholdCount: 3  # Consecutive failures
  Matcher:
    HttpCode: 200  # or 200-299
```

**Best Practices:**
- Use dedicated health check endpoint
- Check critical dependencies (database connectivity)
- Return appropriate status codes
- Keep health checks fast (<1 second)
- Log health check failures

### Environment Variables vs Secrets

**Environment Variables (Plain Text):**
```yaml
Environment:
  - Name: NODE_ENV
    Value: production
  - Name: LOG_LEVEL
    Value: info
  - Name: API_ENDPOINT
    Value: https://api.example.com
```

**Use For:**
- Non-sensitive configuration
- Public endpoints
- Feature flags
- Environment names

**Secrets (Encrypted):**
```yaml
Secrets:
  - Name: DB_PASSWORD
    ValueFrom: arn:aws:secretsmanager:us-east-1:123456789012:secret:db-pass
  - Name: API_KEY
    ValueFrom: arn:aws:ssm:us-east-1:123456789012:parameter/api-key
```

**Use For:**
- Database credentials
- API keys
- OAuth tokens
- Private certificates

**IAM Permissions Required:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "secretsmanager:GetSecretValue",
      "ssm:GetParameters"
    ],
    "Resource": [
      "arn:aws:secretsmanager:us-east-1:123456789012:secret:*",
      "arn:aws:ssm:us-east-1:123456789012:parameter/*"
    ]
  }]
}
```

### Logging Configuration

**CloudWatch Logs (Default):**
```yaml
LogConfiguration:
  LogDriver: awslogs
  Options:
    awslogs-group: /ecs/my-service
    awslogs-region: us-east-1
    awslogs-stream-prefix: task
    awslogs-create-group: true
```

**FireLens (Advanced Routing):**
```yaml
LogConfiguration:
  LogDriver: awsfirelens
  Options:
    Name: datadog
    apikey: !Ref DatadogApiKey
    dd_service: my-service
    dd_source: ecs
    dd_tags: env:production,team:platform
```

**Supported Destinations:**
- CloudWatch Logs
- Datadog
- New Relic
- Splunk
- Elasticsearch
- S3 (via Kinesis Firehose)

## Service Discovery and Load Balancing

### AWS Cloud Map (Service Discovery)

**Pattern:** DNS-based service discovery for microservices.

**Use When:**
- Microservices architecture
- Service-to-service communication
- Dynamic service endpoints
- No load balancer needed (internal traffic)

**Configuration:**
```yaml
ServiceDiscoveryService:
  Name: backend-api
  DnsConfig:
    NamespaceId: !Ref PrivateNamespace
    DnsRecords:
      - Type: A
        TTL: 10
  HealthCheckCustomConfig:
    FailureThreshold: 1

PrivateNamespace:
  Name: internal.example.com
  Vpc: !Ref VPC
```

**Service Registration:**
```yaml
Service:
  ServiceRegistries:
    - RegistryArn: !GetAtt ServiceDiscoveryService.Arn
      ContainerName: backend
      ContainerPort: 8080
```

**Usage in Application:**
```python
# Resolve service using DNS
import socket
hostname = "backend-api.internal.example.com"
ip_address = socket.gethostbyname(hostname)

# Make request
response = requests.get(f"http://{ip_address}:8080/api")
```

**Benefits:**
- No load balancer cost
- Automatic registration/deregistration
- Health check integration
- Low latency (DNS caching)

### Application Load Balancer Integration

**Path-Based Routing:**
```yaml
ListenerRule1:
  Priority: 1
  Conditions:
    - Field: path-pattern
      Values:
        - /api/*
  Actions:
    - Type: forward
      TargetGroupArn: !Ref BackendTargetGroup

ListenerRule2:
  Priority: 2
  Conditions:
    - Field: path-pattern
      Values:
        - /admin/*
  Actions:
    - Type: forward
      TargetGroupArn: !Ref AdminTargetGroup
```

**Host-Based Routing:**
```yaml
ListenerRule:
  Conditions:
    - Field: host-header
      Values:
        - api.example.com
        - api-staging.example.com
  Actions:
    - Type: forward
      TargetGroupArn: !Ref ApiTargetGroup
```

**Header-Based Routing:**
```yaml
ListenerRule:
  Conditions:
    - Field: http-header
      HttpHeaderConfig:
        HttpHeaderName: X-API-Version
        Values:
          - v2
  Actions:
    - Type: forward
      TargetGroupArn: !Ref V2TargetGroup
```

## Auto Scaling Strategies

### Target Tracking (Recommended)

**CPU-Based Scaling:**
```yaml
ScalingPolicy:
  PolicyType: TargetTrackingScaling
  TargetTrackingScalingPolicyConfiguration:
    TargetValue: 70.0  # 70% CPU utilization
    PredefinedMetricSpecification:
      PredefinedMetricType: ECSServiceAverageCPUUtilization
    ScaleInCooldown: 300  # 5 minutes
    ScaleOutCooldown: 60  # 1 minute
```

**Memory-Based Scaling:**
```yaml
TargetTrackingScalingPolicyConfiguration:
  TargetValue: 80.0  # 80% memory utilization
  PredefinedMetricSpecification:
    PredefinedMetricType: ECSServiceAverageMemoryUtilization
```

**ALB Request Count Scaling:**
```yaml
TargetTrackingScalingPolicyConfiguration:
  TargetValue: 1000  # 1000 requests per target
  PredefinedMetricSpecification:
    PredefinedMetricType: ALBRequestCountPerTarget
    ResourceLabel: !Sub
      - ${LoadBalancerFullName}/${TargetGroupFullName}
      - LoadBalancerFullName: !GetAtt ALB.LoadBalancerFullName
        TargetGroupFullName: !GetAtt TargetGroup.TargetGroupFullName
```

### Step Scaling (Advanced)

**Use When:**
- Need different scaling behavior at different thresholds
- Complex scaling logic
- Multiple alarm thresholds

**Configuration:**
```yaml
ScalingPolicy:
  PolicyType: StepScaling
  StepScalingPolicyConfiguration:
    AdjustmentType: PercentChangeInCapacity
    Cooldown: 300
    MetricAggregationType: Average
    StepAdjustments:
      - MetricIntervalLowerBound: 0
        MetricIntervalUpperBound: 10
        ScalingAdjustment: 10  # Add 10% capacity
      - MetricIntervalLowerBound: 10
        MetricIntervalUpperBound: 20
        ScalingAdjustment: 20  # Add 20% capacity
      - MetricIntervalLowerBound: 20
        ScalingAdjustment: 30  # Add 30% capacity
```

### Scheduled Scaling

**Use When:**
- Predictable traffic patterns (business hours)
- Batch processing at specific times
- Cost optimization (scale down at night)

**Configuration:**
```yaml
ScheduledAction1:
  ScheduledActionName: scale-up-morning
  Schedule: cron(0 7 * * MON-FRI *)  # 7 AM weekdays
  ScalableTargetAction:
    MinCapacity: 5
    MaxCapacity: 20

ScheduledAction2:
  ScheduledActionName: scale-down-evening
  Schedule: cron(0 19 * * * *)  # 7 PM daily
  ScalableTargetAction:
    MinCapacity: 1
    MaxCapacity: 5
```

## Service Connect (Service Mesh)

### Built-In Service Mesh (2023+ Feature)

**Use When:**
- Need service-to-service communication
- Want observability without code changes
- Require retry logic and circuit breaking
- Avoid complexity of Istio or App Mesh

**Architecture:**
```
Service A → Envoy Proxy → Service B Endpoint
                        → Service B Load Balancing
                        → CloudMap Discovery
```

**Configuration:**
```yaml
Cluster:
  ServiceConnectDefaults:
    Namespace: internal.local

Service:
  ServiceConnectConfiguration:
    Enabled: true
    Namespace: internal.local
    Services:
      - PortName: http
        ClientAliases:
          - Port: 8080
            DnsName: backend-api
        IngressPortOverride: 8080
    LogConfiguration:
      LogDriver: awslogs
      Options:
        awslogs-group: /ecs/service-connect
        awslogs-stream-prefix: proxy
```

**Benefits:**
- Zero code changes
- Automatic retries
- Circuit breaking
- Connection pooling
- Metrics and tracing
- mTLS encryption (optional)

**Observability:**
- Request success/failure rates
- Latency percentiles (p50, p99)
- Active connections
- Retry counts
- All metrics in CloudWatch

## EKS Pod Identities

### Simplified IAM for Pods (2024+ Feature)

**Use When:**
- Running applications on EKS
- Need AWS service access from pods
- Want simpler configuration than IRSA

**Old Way (IRSA - IAM Roles for Service Accounts):**
```yaml
# Complex OIDC provider setup required
# Per-namespace service account annotations
# Trust relationship with OIDC provider
```

**New Way (Pod Identities):**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/MyAppRole
```

**IAM Role Configuration:**
```yaml
MyAppRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: pods.eks.amazonaws.com
          Action: sts:AssumeRole
          Condition:
            StringEquals:
              aws:SourceAccount: !Ref AWS::AccountId
            ArnEquals:
              aws:SourceArn: !Sub 'arn:aws:eks:${AWS::Region}:${AWS::AccountId}:cluster/${ClusterName}'
    Policies:
      - PolicyName: S3Access
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - s3:GetObject
                - s3:PutObject
              Resource: !Sub '${Bucket.Arn}/*'
```

**Pod Specification:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  namespace: default
spec:
  serviceAccountName: my-app
  containers:
    - name: app
      image: my-app:latest
      # AWS SDK automatically assumes role
```

**Benefits over IRSA:**
- Simpler setup (no OIDC provider)
- Works with any namespace
- Faster credential rotation
- Better audit logging

## Container Security

### Image Scanning

**ECR Image Scanning:**
```yaml
Repository:
  ImageScanningConfiguration:
    ScanOnPush: true
  ImageTagMutability: IMMUTABLE  # Prevent tag overwrites
```

**Scan Results Integration:**
- Automatic CVE detection
- Severity classification (Critical, High, Medium, Low)
- Integration with Security Hub
- Findings in ECR console

**Best Practices:**
- Scan all images before deployment
- Block deployments with critical vulnerabilities
- Regularly rebuild base images
- Use minimal base images (alpine, distroless)

### Runtime Security

**Read-Only Root Filesystem:**
```yaml
ContainerDefinitions:
  - Name: app
    ReadonlyRootFilesystem: true
    MountPoints:
      - SourceVolume: tmp
        ContainerPath: /tmp
        ReadOnly: false

Volumes:
  - Name: tmp
    Host:
      SourcePath: /tmp
```

**Drop Capabilities (Kubernetes):**
```yaml
securityContext:
  allowPrivilegeEscalation: false
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE  # Only if needed
```

**Network Segmentation:**
```yaml
SecurityGroup:
  Ingress:
    - IpProtocol: tcp
      FromPort: 80
      ToPort: 80
      SourceSecurityGroupId: !Ref ALBSecurityGroup
    # No SSH access
  Egress:
    - IpProtocol: tcp
      FromPort: 443
      ToPort: 443
      CidrIp: 0.0.0.0/0  # HTTPS only
    - IpProtocol: tcp
      FromPort: 5432
      ToPort: 5432
      DestinationSecurityGroupId: !Ref DBSecurityGroup
```

## Logging and Monitoring

### Container Insights

**Enable Container Insights:**
```yaml
Cluster:
  ClusterSettings:
    - Name: containerInsights
      Value: enabled
```

**Metrics Collected:**
- CPU utilization (cluster, service, task)
- Memory utilization
- Network throughput
- Disk I/O
- Task count

**Log Insights Queries:**
```sql
-- Find errors in last hour
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100

-- Slowest requests
fields @timestamp, duration, status
| filter path = "/api/users"
| stats avg(duration), max(duration), count() by bin(5m)
```

### X-Ray Tracing

**Enable X-Ray:**
```yaml
ContainerDefinitions:
  - Name: xray-daemon
    Image: amazon/aws-xray-daemon
    PortMappings:
      - ContainerPort: 2000
        Protocol: udp
  - Name: app
    Environment:
      - Name: AWS_XRAY_DAEMON_ADDRESS
        Value: localhost:2000
```

**Application Code (Python):**
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)
XRayMiddleware(app, xray_recorder)

@app.route('/api/users')
def get_users():
    # Automatically traced
    return jsonify(users)
```

## Cost Optimization

### EC2 Launch Type Optimization

**Spot Instances (70% Savings):**
```yaml
CapacityProvider:
  Name: spot-capacity
  AutoScalingGroupProvider:
    AutoScalingGroupArn: !Ref SpotASG
    ManagedScaling:
      Status: ENABLED
      TargetCapacity: 100
    ManagedTerminationProtection: ENABLED

Service:
  CapacityProviderStrategy:
    - CapacityProvider: spot-capacity
      Weight: 4
    - CapacityProvider: ondemand-capacity
      Weight: 1
      Base: 2  # Always maintain 2 on-demand
```

**Graviton Processors (20% Cost Savings):**
```yaml
LaunchTemplate:
  InstanceType: t4g.medium  # Graviton-based
  # 20% cheaper than t3.medium
  # 40% better price-performance
```

**Reserved Instances:**
- 1-year: 30-40% savings
- 3-year: 50-60% savings
- Use for predictable baseline capacity

### Task-Level Optimization

**Right-Sizing:**
- Monitor CloudWatch metrics weekly
- Reduce over-provisioned resources
- Use Compute Optimizer recommendations

**Reduce Data Transfer:**
- Use VPC endpoints (avoid NAT Gateway costs)
- Place services in same AZ when possible
- Use CloudFront for static assets

**Storage Optimization:**
- Use ephemeral storage (free)
- Avoid EBS volumes unless necessary
- Clean up unused ECR images

## Anti-Patterns

### Don't: Run Databases in Containers

**Problem:** Stateful data, performance overhead, operational complexity.

**Solution:** Use RDS, Aurora, or DynamoDB.

### Don't: Use Latest Tag

**Problem:** Unpredictable deployments, difficult rollbacks.

**Solution:** Use immutable tags (commit SHA, semantic versions).

```yaml
# Bad
Image: my-app:latest

# Good
Image: my-app:v1.2.3
Image: my-app:commit-abc123
```

### Don't: Store Secrets in Environment Variables

**Problem:** Exposed in logs, console, API responses.

**Solution:** Use Secrets Manager or Parameter Store.

### Don't: Run Single Replica

**Problem:** No high availability, downtime during deployments.

**Solution:** Run minimum 2 replicas across multiple AZs.

### Don't: Ignore Resource Limits

**Problem:** Resource starvation, OOM kills, cascading failures.

**Solution:** Set appropriate CPU and memory limits.

```yaml
# Kubernetes
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Don't: Use Default VPC

**Problem:** No subnet segmentation, poor security posture.

**Solution:** Create custom VPC with private subnets.

### Don't: Skip Health Checks

**Problem:** Traffic sent to unhealthy tasks, user-facing errors.

**Solution:** Implement comprehensive health checks.

### Don't: Ignore Deployment Circuit Breakers

**Problem:** Bad deployments can take down entire service.

**Solution:** Enable circuit breakers with automatic rollback.

```yaml
DeploymentConfiguration:
  DeploymentCircuitBreaker:
    Enable: true
    Rollback: true
```
