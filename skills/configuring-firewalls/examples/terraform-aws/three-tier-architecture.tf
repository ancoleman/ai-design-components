# Three-Tier Architecture Security Groups
#
# This Terraform configuration creates security groups for a typical
# three-tier web application in AWS:
# - Web tier (public subnet, accessible from Internet)
# - App tier (private subnet, accessible from web tier)
# - Database tier (private subnet, accessible from app tier)
# - Bastion host (public subnet, for SSH access)
#
# Usage:
# 1. Update variables.tf with your VPC ID and CIDR ranges
# 2. terraform init
# 3. terraform plan
# 4. terraform apply

# Variables (create variables.tf)
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "office_cidr" {
  description = "Office IP range for SSH access"
  type        = string
  default     = "203.0.113.0/24"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# Bastion Security Group
resource "aws_security_group" "bastion" {
  name        = "bastion-sg"
  description = "Security group for bastion host"
  vpc_id      = var.vpc_id

  # Inbound: SSH from office only
  ingress {
    description = "SSH from office"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.office_cidr]
  }

  # Outbound: SSH to VPC instances
  egress {
    description = "SSH to VPC instances"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  # Outbound: HTTPS for package updates
  egress {
    description = "HTTPS for updates"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: DNS
  egress {
    description = "DNS"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "bastion-sg"
    Environment = var.environment
    Tier        = "bastion"
  }
}

# Web Tier Security Group (Public)
resource "aws_security_group" "web" {
  name        = "web-tier-sg"
  description = "Security group for web servers in public subnet"
  vpc_id      = var.vpc_id

  # Inbound: HTTP from Internet
  ingress {
    description = "HTTP from Internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound: HTTPS from Internet
  ingress {
    description = "HTTPS from Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound: SSH from bastion only
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Outbound: To app tier
  egress {
    description     = "HTTP to app tier"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # Outbound: HTTPS for external APIs
  egress {
    description = "HTTPS to Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: DNS
  egress {
    description = "DNS"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "web-tier-sg"
    Environment = var.environment
    Tier        = "web"
  }
}

# App Tier Security Group (Private)
resource "aws_security_group" "app" {
  name        = "app-tier-sg"
  description = "Security group for application servers in private subnet"
  vpc_id      = var.vpc_id

  # Inbound: HTTP from web tier
  ingress {
    description     = "HTTP from web tier"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  # Inbound: SSH from bastion
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Outbound: PostgreSQL to database
  egress {
    description     = "PostgreSQL to database"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.database.id]
  }

  # Outbound: HTTPS for external APIs
  egress {
    description = "HTTPS to Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: DNS
  egress {
    description = "DNS"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "app-tier-sg"
    Environment = var.environment
    Tier        = "app"
  }
}

# Database Tier Security Group (Private)
resource "aws_security_group" "database" {
  name        = "database-tier-sg"
  description = "Security group for RDS database in private subnet"
  vpc_id      = var.vpc_id

  # Inbound: PostgreSQL from app tier only
  ingress {
    description     = "PostgreSQL from app tier"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # Inbound: SSH from bastion (if using EC2, not RDS)
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Outbound: Minimal (VPC only, no Internet)
  egress {
    description = "Local VPC only"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Name        = "database-tier-sg"
    Environment = var.environment
    Tier        = "database"
  }
}

# Optional: Application Load Balancer Security Group
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = var.vpc_id

  # Inbound: HTTPS from Internet
  ingress {
    description = "HTTPS from Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound: HTTP from Internet (redirect to HTTPS)
  ingress {
    description = "HTTP from Internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: To web tier instances
  egress {
    description     = "HTTP to web tier"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  tags = {
    Name        = "alb-sg"
    Environment = var.environment
    Tier        = "load-balancer"
  }
}

# Outputs
output "bastion_sg_id" {
  description = "Bastion security group ID"
  value       = aws_security_group.bastion.id
}

output "web_sg_id" {
  description = "Web tier security group ID"
  value       = aws_security_group.web.id
}

output "app_sg_id" {
  description = "App tier security group ID"
  value       = aws_security_group.app.id
}

output "database_sg_id" {
  description = "Database tier security group ID"
  value       = aws_security_group.database.id
}

output "alb_sg_id" {
  description = "ALB security group ID"
  value       = aws_security_group.alb.id
}
