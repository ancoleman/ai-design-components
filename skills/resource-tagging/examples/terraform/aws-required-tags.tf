# AWS Required Tags Example
#
# Demonstrates provider-level default tags and AWS Config enforcement
#
# Dependencies:
#   terraform >= 1.0
#   AWS provider >= 4.0
#
# Usage:
#   terraform init
#   terraform plan
#   terraform apply

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables for required tags
variable "environment" {
  type        = string
  description = "Environment (prod, staging, dev)"
  validation {
    condition     = contains(["prod", "staging", "dev", "test"], var.environment)
    error_message = "Environment must be prod, staging, dev, or test"
  }
}

variable "owner" {
  type        = string
  description = "Team email address"
  validation {
    condition     = can(regex("^[a-z0-9._%+-]+@company\\.com$", var.owner))
    error_message = "Owner must be a valid @company.com email"
  }
}

variable "cost_center" {
  type        = string
  description = "Finance cost center code"
  validation {
    condition     = can(regex("^CC-[0-9]{4}$", var.cost_center))
    error_message = "CostCenter must match format CC-####"
  }
}

variable "project" {
  type        = string
  description = "Project name"
}

# Provider with default tags (applies to ALL resources)
provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Environment = var.environment
      Owner       = var.owner
      CostCenter  = var.cost_center
      Project     = var.project
      ManagedBy   = "terraform"
      CreatedDate = timestamp()
    }
  }
}

# Example: EC2 instance with resource-specific tags merged with defaults
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"

  # Resource-specific tags (merged with provider default_tags)
  tags = {
    Name      = "${var.environment}-app-server-01"
    Component = "web"
    Backup    = "daily"
    SLA       = "high"
  }
}

# Example: RDS instance with additional tags
resource "aws_db_instance" "database" {
  identifier           = "${var.environment}-postgres-db"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t3.medium"
  allocated_storage    = 100
  username             = "admin"
  password             = random_password.db_password.result
  skip_final_snapshot  = true

  tags = {
    Name            = "${var.environment}-postgres-db"
    Component       = "database"
    Backup          = "continuous"
    DataClassification = "tier1"
  }
}

resource "random_password" "db_password" {
  length  = 16
  special = true
}

# Example: S3 bucket with compliance tags
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project}-${var.environment}-data-lake"

  tags = {
    Name               = "${var.project}-${var.environment}-data-lake"
    Component          = "storage"
    Compliance         = "SOC2"
    Confidentiality    = "confidential"
    DataClassification = "tier2"
  }
}

# AWS Config: Enable configuration recorder
resource "aws_config_configuration_recorder" "main" {
  name     = "tag-compliance-recorder"
  role_arn = aws_iam_role.config_role.arn

  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

resource "aws_config_delivery_channel" "main" {
  name           = "tag-compliance-channel"
  s3_bucket_name = aws_s3_bucket.config_logs.id
  depends_on     = [aws_config_configuration_recorder.main]
}

resource "aws_config_configuration_recorder_status" "main" {
  name       = aws_config_configuration_recorder.main.name
  is_enabled = true
  depends_on = [aws_config_delivery_channel.main]
}

# S3 bucket for AWS Config logs
resource "aws_s3_bucket" "config_logs" {
  bucket = "${var.project}-config-logs-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name      = "config-logs"
    Component = "compliance"
  }
}

resource "aws_s3_bucket_versioning" "config_logs" {
  bucket = aws_s3_bucket.config_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

# IAM role for AWS Config
resource "aws_iam_role" "config_role" {
  name = "aws-config-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "config.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "config_policy" {
  role       = aws_iam_role.config_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/ConfigRole"
}

# AWS Config Rule: Require tags on resources
resource "aws_config_config_rule" "required_tags" {
  name = "required-tags-check"

  source {
    owner             = "AWS"
    source_identifier = "REQUIRED_TAGS"
  }

  input_parameters = jsonencode({
    tag1Key = "Environment"
    tag2Key = "Owner"
    tag3Key = "CostCenter"
    tag4Key = "Project"
    tag5Key = "ManagedBy"
    tag6Key = "Name"
  })

  scope {
    compliance_resource_types = [
      "AWS::EC2::Instance",
      "AWS::RDS::DBInstance",
      "AWS::S3::Bucket",
      "AWS::Lambda::Function",
      "AWS::DynamoDB::Table",
    ]
  }

  depends_on = [aws_config_configuration_recorder.main]
}

# SNS topic for compliance alerts
resource "aws_sns_topic" "compliance_alerts" {
  name = "tag-compliance-alerts"

  tags = {
    Name      = "compliance-alerts"
    Component = "monitoring"
  }
}

resource "aws_sns_topic_subscription" "compliance_email" {
  topic_arn = aws_sns_topic.compliance_alerts.arn
  protocol  = "email"
  endpoint  = var.owner
}

# EventBridge rule to notify on non-compliance
resource "aws_cloudwatch_event_rule" "config_non_compliant" {
  name        = "tag-compliance-violations"
  description = "Trigger when resources are non-compliant with tag policies"

  event_pattern = jsonencode({
    source      = ["aws.config"]
    detail-type = ["Config Rules Compliance Change"]
    detail = {
      configRuleName = [aws_config_config_rule.required_tags.name]
      newEvaluationResult = {
        complianceType = ["NON_COMPLIANT"]
      }
    }
  })
}

resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.config_non_compliant.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.compliance_alerts.arn
}

resource "aws_sns_topic_policy" "compliance_alerts" {
  arn = aws_sns_topic.compliance_alerts.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "events.amazonaws.com"
      }
      Action   = "SNS:Publish"
      Resource = aws_sns_topic.compliance_alerts.arn
    }]
  })
}

# Enable cost allocation tags
resource "aws_ce_cost_allocation_tag" "environment" {
  tag_key = "Environment"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "project" {
  tag_key = "Project"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "costcenter" {
  tag_key = "CostCenter"
  status  = "Active"
}

# Data sources
data "aws_caller_identity" "current" {}

# Outputs
output "config_rule_arn" {
  description = "AWS Config rule ARN for tag compliance"
  value       = aws_config_config_rule.required_tags.arn
}

output "sns_topic_arn" {
  description = "SNS topic ARN for compliance alerts"
  value       = aws_sns_topic.compliance_alerts.arn
}

output "example_resources" {
  description = "Example resources with tags applied"
  value = {
    ec2_instance = aws_instance.app_server.id
    rds_instance = aws_db_instance.database.id
    s3_bucket    = aws_s3_bucket.data_lake.id
  }
}
