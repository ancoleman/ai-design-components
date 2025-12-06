/**
 * Flat (Single VPC) Architecture Example - AWS
 *
 * Demonstrates: Basic three-tier VPC with public, private, and database subnets
 *
 * Use Case: Small applications, single environment, simple security requirements
 *
 * Prerequisites:
 * - Terraform >= 1.0
 * - AWS provider configured
 *
 * Usage:
 * terraform init
 * terraform plan
 * terraform apply
 */

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.environment}-vpc"
  cidr = "10.0.0.0/16"

  # Availability Zones
  azs = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]

  # Public Subnets (for ALB, NAT Gateways)
  public_subnets = [
    "10.0.1.0/24",   # us-east-1a
    "10.0.2.0/24",   # us-east-1b
    "10.0.3.0/24"    # us-east-1c
  ]

  # Private Subnets (for application workloads)
  private_subnets = [
    "10.0.10.0/24",  # us-east-1a
    "10.0.11.0/24",  # us-east-1b
    "10.0.12.0/24"   # us-east-1c
  ]

  # Database Subnets (for RDS)
  database_subnets = [
    "10.0.20.0/24",  # us-east-1a
    "10.0.21.0/24",  # us-east-1b
    "10.0.22.0/24"   # us-east-1c
  ]

  # NAT Gateway Configuration
  # For production: one_nat_gateway_per_az = true (resilient, higher cost)
  # For dev/test: single_nat_gateway = true (cost-optimized, single point of failure)
  enable_nat_gateway     = true
  single_nat_gateway     = false  # NAT per AZ for resilience
  one_nat_gateway_per_az = true

  # DNS Configuration
  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Endpoints for cost optimization (avoid NAT charges)
  enable_s3_endpoint       = true  # Gateway endpoint (free)
  enable_dynamodb_endpoint = true  # Gateway endpoint (free)

  # Create database subnet group
  create_database_subnet_group = true

  # Tags
  tags = {
    Terraform   = "true"
    Environment = var.environment
    Pattern     = "flat-vpc"
  }

  public_subnet_tags = {
    Tier = "public"
  }

  private_subnet_tags = {
    Tier = "private"
  }

  database_subnet_tags = {
    Tier = "database"
  }
}

# VPC Flow Logs
resource "aws_cloudwatch_log_group" "vpc_flow_log" {
  name              = "/aws/vpc/${module.vpc.vpc_id}/flow-logs"
  retention_in_days = 7  # 7 days for dev, 30+ for production

  tags = {
    Name        = "${var.environment}-vpc-flow-logs"
    Environment = var.environment
  }
}

resource "aws_iam_role" "vpc_flow_log" {
  name = "${var.environment}-vpc-flow-log-role"

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

  tags = {
    Name = "${var.environment}-vpc-flow-log-role"
  }
}

resource "aws_iam_role_policy" "vpc_flow_log" {
  name = "${var.environment}-vpc-flow-log-policy"
  role = aws_iam_role.vpc_flow_log.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_flow_log" "vpc" {
  iam_role_arn    = aws_iam_role.vpc_flow_log.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log.arn
  traffic_type    = "ALL"  # Capture both accepted and rejected traffic
  vpc_id          = module.vpc.vpc_id

  tags = {
    Name        = "${var.environment}-vpc-flow-log"
    Environment = var.environment
  }
}

# Security Groups
resource "aws_security_group" "alb" {
  name        = "${var.environment}-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = module.vpc.vpc_id

  # Inbound HTTPS from internet
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS from internet"
  }

  # Inbound HTTP from internet (redirect to HTTPS)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP from internet"
  }

  # Outbound to backend
  egress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
    description     = "To backend service"
  }

  tags = {
    Name        = "${var.environment}-alb-sg"
    Environment = var.environment
  }
}

resource "aws_security_group" "backend" {
  name        = "${var.environment}-backend-sg"
  description = "Security group for backend application"
  vpc_id      = module.vpc.vpc_id

  # Inbound from ALB only
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "From ALB only"
  }

  # Outbound to database
  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.database.id]
    description     = "To PostgreSQL database"
  }

  # Outbound to internet (for package updates, API calls)
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to internet"
  }

  tags = {
    Name        = "${var.environment}-backend-sg"
    Environment = var.environment
  }
}

resource "aws_security_group" "database" {
  name        = "${var.environment}-database-sg"
  description = "Security group for database"
  vpc_id      = module.vpc.vpc_id

  # Inbound from backend only
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
    description     = "From backend only"
  }

  # No egress rules needed (database doesn't initiate connections)
  # Some egress required for AWS health checks
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Required for AWS health checks"
  }

  tags = {
    Name        = "${var.environment}-database-sg"
    Environment = var.environment
  }
}

# Outputs
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "database_subnets" {
  description = "Database subnet IDs"
  value       = module.vpc.database_subnets
}

output "nat_gateway_ids" {
  description = "NAT Gateway IDs"
  value       = module.vpc.natgw_ids
}

output "alb_security_group_id" {
  description = "ALB Security Group ID"
  value       = aws_security_group.alb.id
}

output "backend_security_group_id" {
  description = "Backend Security Group ID"
  value       = aws_security_group.backend.id
}

output "database_security_group_id" {
  description = "Database Security Group ID"
  value       = aws_security_group.database.id
}
