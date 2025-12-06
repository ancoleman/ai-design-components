# Zero Trust Networking

Comprehensive guide to implementing zero trust network architecture principles in cloud environments.

## Table of Contents

1. [Zero Trust Principles](#zero-trust-principles)
2. [Microsegmentation](#microsegmentation)
3. [Identity-Based Access](#identity-based-access)
4. [Continuous Verification](#continuous-verification)
5. [Implementation Roadmap](#implementation-roadmap)

---

## Zero Trust Principles

### Core Tenets (2025)

#### 1. Never Trust, Always Verify

**Traditional Approach:**
```
Inside Network = Trusted
Outside Network = Untrusted
```

**Zero Trust Approach:**
```
Every Request = Verify
Every User = Authenticate
Every Device = Validate
```

**Implementation:**
- Authenticate every request regardless of source
- Verify identity AND device health
- No implicit trust based on network location

#### 2. Least Privilege Access

**Traditional Approach:**
```
VPC = Full Access
Subnet = Full Access within subnet
```

**Zero Trust Approach:**
```
Service A → Service B: Port 8080 only
Service C → Database: Port 5432 only
```

**Implementation:**
- Grant minimum necessary permissions
- Time-bound access (just-in-time)
- Continuous authorization
- Revoke unused permissions

#### 3. Assume Breach

**Traditional Approach:**
```
Perimeter = Secure
Inside = Trusted
```

**Zero Trust Approach:**
```
Attackers Inside = Assume
Lateral Movement = Block
Segment Everything = Required
```

**Implementation:**
- Segment network aggressively
- Monitor all traffic
- Rapid detection and response
- Limit blast radius

---

## Microsegmentation

### Traditional Network vs Zero Trust

#### Traditional (Large Blast Radius)

```
┌────────────────────────────────────────────────┐
│              DMZ (0.0.0.0/0 allowed)           │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │ App1│ │ App2│ │ App3│ │ App4│ │ App5│     │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘     │
│   All apps can talk to each other              │
└────────────────────────────────────────────────┘

Problem: If one app compromised, all apps at risk
```

#### Zero Trust (Microsegmentation)

```
┌────────────────────────────────────────────────┐
│         Microsegmented Environment             │
│  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐       │
│  │App1 │──►│App2 │   │App3 │──►│App4 │       │
│  │[SG1]│   │[SG2]│   │[SG3]│   │[SG4]│       │
│  └─────┘   └─────┘   └─────┘   └─────┘       │
│    Only App1→App2 and App3→App4 allowed       │
└────────────────────────────────────────────────┘

Benefit: Compromise of App1 doesn't affect App3/App4
```

### Implementing Microsegmentation with Security Groups

#### Pattern 1: Service-to-Service Security Groups

**Architecture:**
```
┌───────────────────────────────────────────────────┐
│                  VPC                              │
│                                                   │
│  ┌─────────────────────────────────────────┐    │
│  │  ALB Security Group (alb-sg)            │    │
│  │  Ingress: 0.0.0.0/0:443 (HTTPS)         │    │
│  └─────────────────────────────────────────┘    │
│                      │                           │
│                      ▼                           │
│  ┌─────────────────────────────────────────┐    │
│  │  Backend Security Group (backend-sg)    │    │
│  │  Ingress: [alb-sg]:8080 (from ALB only) │    │
│  └─────────────────────────────────────────┘    │
│                      │                           │
│                      ▼                           │
│  ┌─────────────────────────────────────────┐    │
│  │  Database Security Group (db-sg)        │    │
│  │  Ingress: [backend-sg]:5432 (from BE)   │    │
│  └─────────────────────────────────────────┘    │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Implementation (AWS):**
```hcl
# ALB Security Group
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "ALB security group"
  vpc_id      = module.vpc.vpc_id

  # Public HTTPS access
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS from internet"
  }

  # Outbound to backend only
  egress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
    description     = "To backend service"
  }

  tags = {
    Name      = "alb-sg"
    ZeroTrust = "true"
  }
}

# Backend Service Security Group
resource "aws_security_group" "backend" {
  name        = "backend-sg"
  description = "Backend service security group"
  vpc_id      = module.vpc.vpc_id

  # Only accept traffic from ALB
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "From ALB only"
  }

  # Only send traffic to database
  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.database.id]
    description     = "To database only"
  }

  tags = {
    Name      = "backend-sg"
    ZeroTrust = "true"
  }
}

# Database Security Group
resource "aws_security_group" "database" {
  name        = "database-sg"
  description = "Database security group"
  vpc_id      = module.vpc.vpc_id

  # Only accept traffic from backend
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
    description     = "From backend only"
  }

  # No outbound (database doesn't initiate)
  # Note: Some egress required for health checks
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Required for AWS health checks"
  }

  tags = {
    Name      = "database-sg"
    ZeroTrust = "true"
  }
}
```

#### Pattern 2: Microservices Segmentation

**Scenario:** Multiple microservices with specific dependencies

```hcl
# Auth Service
resource "aws_security_group" "auth_service" {
  name        = "auth-service-sg"
  vpc_id      = module.vpc.vpc_id

  # Accept from API Gateway
  ingress {
    from_port       = 8081
    to_port         = 8081
    protocol        = "tcp"
    security_groups = [aws_security_group.api_gateway.id]
  }

  # Can talk to user database
  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.user_db.id]
  }

  tags = {
    Service = "auth"
  }
}

# Order Service
resource "aws_security_group" "order_service" {
  name        = "order-service-sg"
  vpc_id      = module.vpc.vpc_id

  # Accept from API Gateway
  ingress {
    from_port       = 8082
    to_port         = 8082
    protocol        = "tcp"
    security_groups = [aws_security_group.api_gateway.id]
  }

  # Can talk to order database
  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.order_db.id]
  }

  # Can talk to payment service
  egress {
    from_port       = 8083
    to_port         = 8083
    protocol        = "tcp"
    security_groups = [aws_security_group.payment_service.id]
  }

  tags = {
    Service = "order"
  }
}
```

### Microsegmentation Best Practices

1. **One Security Group Per Service**
   - Don't reuse security groups across services
   - Makes dependency tracking clear

2. **Reference Other Security Groups**
   - Use security group IDs instead of CIDR blocks
   - Example: `source_security_group_id = aws_security_group.backend.id`

3. **Explicit Deny Not Needed**
   - Security groups are deny-by-default
   - Only create allow rules

4. **Document Dependencies**
   ```hcl
   # Dependency: Frontend → Backend → Database
   # Frontend can only talk to Backend
   # Backend can only talk to Database
   ```

5. **Use Tags for Organization**
   ```hcl
   tags = {
     Service     = "backend"
     Environment = "production"
     ZeroTrust   = "true"
     Owner       = "platform-team"
   }
   ```

---

## Identity-Based Access

### Concept: Identity Over IP Address

**Traditional Approach:**
```
Allow: 10.0.1.0/24 (subnet) → S3
Problem: Any compromised instance in subnet can access S3
```

**Zero Trust Approach:**
```
Allow: IAM Role "app-role" → S3 bucket "app-bucket"
Benefit: Only instances with specific role can access
```

### Implementation Patterns

#### Pattern 1: VPC Endpoints with IAM Policies

**S3 VPC Endpoint with Role-Based Access:**
```hcl
# S3 VPC Endpoint with IAM Policy
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = module.vpc.private_route_table_ids

  # Only specific IAM role can use this endpoint
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.app.arn
        }
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.app.arn}/*"
      }
    ]
  })
}

# Application IAM Role
resource "aws_iam_role" "app" {
  name = "app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "ecs:cluster" = aws_ecs_cluster.main.arn
          }
        }
      }
    ]
  })
}
```

#### Pattern 2: Service Control Policies (SCPs)

**Prevent Public S3 Buckets:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "s3:PutBucketPublicAccessBlock",
        "s3:PutAccountPublicAccessBlock"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-acl": "private"
        }
      }
    }
  ]
}
```

#### Pattern 3: Attribute-Based Access Control (ABAC)

**Tag-Based Access:**
```hcl
# IAM Policy using tags
resource "aws_iam_policy" "tag_based_access" {
  name = "tag-based-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "ec2:*"
        Resource = "*"
        Condition = {
          StringEquals = {
            "ec2:ResourceTag/Environment" = "$${aws:PrincipalTag/Environment}"
          }
        }
      }
    ]
  })
}
```

---

## Continuous Verification

### VPC Flow Logs for Traffic Analysis

#### Enable Flow Logs

```hcl
# VPC Flow Logs to CloudWatch
resource "aws_flow_log" "vpc" {
  iam_role_arn             = aws_iam_role.flow_log.arn
  log_destination          = aws_cloudwatch_log_group.flow_log.arn
  traffic_type             = "ALL"  # Capture accepted and rejected
  vpc_id                   = module.vpc.vpc_id
  max_aggregation_interval = 60  # 1 minute

  tags = {
    Name      = "vpc-flow-logs"
    ZeroTrust = "true"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "flow_log" {
  name              = "/aws/vpc/flow-logs"
  retention_in_days = 30

  tags = {
    Purpose = "Security monitoring"
  }
}

# IAM Role for Flow Logs
resource "aws_iam_role" "flow_log" {
  name = "vpc-flow-log-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
```

### Monitoring Rejected Connections

#### CloudWatch Metric Filter

```hcl
# Detect rejected connections (potential attacks)
resource "aws_cloudwatch_log_metric_filter" "rejected_connections" {
  name           = "rejected-connections"
  log_group_name = aws_cloudwatch_log_group.flow_log.name

  # Flow log format: action="REJECT"
  pattern = "[version, account, eni, source, destination, srcport, destport, protocol, packets, bytes, windowstart, windowend, action=\"REJECT\", flowlogstatus]"

  metric_transformation {
    name      = "RejectedConnectionCount"
    namespace = "VPC/FlowLogs"
    value     = "1"
  }
}

# Alert on spike in rejected connections
resource "aws_cloudwatch_metric_alarm" "rejected_connections_spike" {
  alarm_name          = "rejected-connections-spike"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "RejectedConnectionCount"
  namespace           = "VPC/FlowLogs"
  period              = "300"  # 5 minutes
  statistic           = "Sum"
  threshold           = "100"  # Alert if >100 rejections in 5 min
  alarm_description   = "Potential attack: High rejected connection count"
  alarm_actions       = [aws_sns_topic.security_alerts.arn]

  tags = {
    Severity = "High"
    Type     = "Security"
  }
}
```

### Analyzing Flow Logs

#### Common Queries

**1. Top Talkers (Most Traffic):**
```sql
SELECT srcaddr, dstaddr, SUM(bytes) as total_bytes
FROM vpc_flow_logs
WHERE action = 'ACCEPT'
GROUP BY srcaddr, dstaddr
ORDER BY total_bytes DESC
LIMIT 20
```

**2. Rejected Connections by Source:**
```sql
SELECT srcaddr, COUNT(*) as rejected_count
FROM vpc_flow_logs
WHERE action = 'REJECT'
GROUP BY srcaddr
ORDER BY rejected_count DESC
LIMIT 20
```

**3. Unusual Ports:**
```sql
SELECT dstport, COUNT(*) as count
FROM vpc_flow_logs
WHERE dstport NOT IN (80, 443, 22, 3306, 5432)
GROUP BY dstport
ORDER BY count DESC
```

---

## Implementation Roadmap

### Phase 1: Assessment (Weeks 1-2)

**Activities:**
- [ ] Document current network architecture
- [ ] Inventory all services and dependencies
- [ ] Map data flows between services
- [ ] Identify sensitive data paths
- [ ] Assess current security posture

**Deliverables:**
- Network architecture diagram
- Service dependency map
- Risk assessment report

### Phase 2: Design (Weeks 3-4)

**Activities:**
- [ ] Design microsegmentation strategy
- [ ] Plan security group architecture
- [ ] Define IAM roles and policies
- [ ] Design monitoring and logging strategy
- [ ] Plan phased rollout

**Deliverables:**
- Zero trust architecture design
- Security group matrix
- IAM policy documents
- Monitoring plan

### Phase 3: Pilot (Weeks 5-6)

**Activities:**
- [ ] Implement in non-production environment
- [ ] Test microsegmentation rules
- [ ] Validate IAM policies
- [ ] Enable VPC flow logs
- [ ] Test monitoring and alerting

**Deliverables:**
- Working pilot environment
- Test results
- Lessons learned

### Phase 4: Production Rollout (Weeks 7-12)

**Activities:**
- [ ] Implement microsegmentation in production
- [ ] Enable VPC flow logs
- [ ] Configure CloudWatch alarms
- [ ] Train operations team
- [ ] Document procedures

**Phased Approach:**
1. Week 7-8: Implement security groups (audit mode)
2. Week 9-10: Enforce security group rules
3. Week 11-12: Continuous monitoring and tuning

### Phase 5: Continuous Improvement (Ongoing)

**Activities:**
- [ ] Review flow logs weekly
- [ ] Audit security group rules monthly
- [ ] Update microsegmentation as services change
- [ ] Conduct quarterly security reviews
- [ ] Respond to security incidents

**Metrics to Track:**
- Number of rejected connections
- Security group rule count
- IAM policy complexity
- Time to detect threats
- Time to remediate incidents
