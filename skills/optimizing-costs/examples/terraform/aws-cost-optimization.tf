# AWS Cost Optimization Infrastructure
#
# This Terraform configuration sets up:
# - Cost allocation tags
# - Monthly budgets with cascading alerts
# - Cost anomaly detection
# - SNS topic for notifications
#
# Usage:
#   terraform init
#   terraform plan -var="monthly_budget=10000" -var="team_email=team@company.com"
#   terraform apply

variable "monthly_budget" {
  description = "Monthly cloud budget in USD"
  type        = number
  default     = 10000
}

variable "team_email" {
  description = "Email for budget notifications"
  type        = string
}

variable "oncall_email" {
  description = "Email for critical cost alerts"
  type        = string
}

variable "finops_team_email" {
  description = "FinOps team email for anomaly alerts"
  type        = string
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for cost alerts"
  type        = string
  sensitive   = true
}

# Enable Cost Allocation Tags
resource "aws_ce_cost_allocation_tag" "environment" {
  tag_key = "Environment"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "project" {
  tag_key = "Project"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "owner" {
  tag_key = "Owner"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "cost_center" {
  tag_key = "CostCenter"
  status  = "Active"
}

# Monthly Budget with Cascading Alerts
resource "aws_budgets_budget" "monthly_cost" {
  name              = "monthly-cloud-budget"
  budget_type       = "COST"
  limit_amount      = var.monthly_budget
  limit_unit        = "USD"
  time_period_start = "2025-12-01_00:00"
  time_unit         = "MONTHLY"

  cost_filter {
    name = "LinkedAccount"
    values = [
      data.aws_caller_identity.current.account_id
    ]
  }

  # 50% threshold - Informational
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.team_email]
  }

  # 75% threshold - Warning
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 75
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.team_email]
    subscriber_sns_topic_arns  = [aws_sns_topic.cost_alerts.arn]
  }

  # 90% threshold - Urgent
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.oncall_email]
    subscriber_sns_topic_arns  = [aws_sns_topic.cost_alerts.arn]
  }

  # 100% threshold - Critical
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.oncall_email]
    subscriber_sns_topic_arns  = [aws_sns_topic.cost_alerts.arn]
  }
}

# Cost Anomaly Detection
resource "aws_ce_anomaly_monitor" "service_monitor" {
  name              = "service-cost-anomaly-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_monitor" "account_monitor" {
  name         = "account-cost-anomaly-monitor"
  monitor_type = "DIMENSIONAL"
  monitor_dimension = "LINKED_ACCOUNT"
}

resource "aws_ce_anomaly_subscription" "anomaly_alerts" {
  name      = "cost-anomaly-alerts"
  frequency = "IMMEDIATE"  # or "DAILY" or "WEEKLY"

  monitor_arn_list = [
    aws_ce_anomaly_monitor.service_monitor.arn,
    aws_ce_anomaly_monitor.account_monitor.arn
  ]

  subscriber {
    type    = "SNS"
    address = aws_sns_topic.cost_alerts.arn
  }

  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_PERCENTAGE"
      values        = ["20"]  # Alert if anomaly >20% cost increase
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
}

# SNS Topic for Cost Alerts
resource "aws_sns_topic" "cost_alerts" {
  name = "cloud-cost-alerts"

  tags = {
    Environment = "shared"
    ManagedBy   = "Terraform"
    Purpose     = "cost-optimization"
  }
}

# Email Subscription
resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.cost_alerts.arn
  protocol  = "email"
  endpoint  = var.finops_team_email
}

# Slack Subscription (via Lambda function)
resource "aws_sns_topic_subscription" "slack" {
  topic_arn = aws_sns_topic.cost_alerts.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.slack_notifier.arn
}

# Lambda Function for Slack Notifications
resource "aws_lambda_function" "slack_notifier" {
  filename         = "slack_notifier.zip"
  function_name    = "cost-alert-slack-notifier"
  role             = aws_iam_role.lambda_role.arn
  handler          = "index.handler"
  runtime          = "python3.11"
  timeout          = 60
  source_code_hash = filebase64sha256("slack_notifier.zip")

  environment {
    variables = {
      SLACK_WEBHOOK_URL = var.slack_webhook_url
    }
  }

  tags = {
    Environment = "shared"
    ManagedBy   = "Terraform"
  }
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_role" {
  name = "cost-alert-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Permission for SNS
resource "aws_lambda_permission" "sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slack_notifier.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.cost_alerts.arn
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}

# Outputs
output "budget_name" {
  description = "Name of the created budget"
  value       = aws_budgets_budget.monthly_cost.name
}

output "anomaly_monitor_arns" {
  description = "ARNs of anomaly monitors"
  value = [
    aws_ce_anomaly_monitor.service_monitor.arn,
    aws_ce_anomaly_monitor.account_monitor.arn
  ]
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for cost alerts"
  value       = aws_sns_topic.cost_alerts.arn
}
