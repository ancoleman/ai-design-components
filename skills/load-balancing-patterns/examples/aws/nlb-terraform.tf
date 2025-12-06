# AWS Network Load Balancer (NLB) Configuration with Terraform
# This configuration demonstrates production-ready NLB setup with health checks and cross-zone load balancing

# Terraform and provider configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables for configuration
variable "vpc_id" {
  description = "VPC ID where the NLB will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the NLB (must be in different AZs)"
  type        = list(string)
}

variable "environment" {
  description = "Environment name (e.g., production, staging)"
  type        = string
  default     = "production"
}

# Data source to get VPC information
data "aws_vpc" "main" {
  id = var.vpc_id
}

#---------------------------------------------------------------------
# Network Load Balancer
#---------------------------------------------------------------------
resource "aws_lb" "main" {
  name               = "${var.environment}-app-nlb"
  internal           = false  # Set to true for internal NLB
  load_balancer_type = "network"

  # Enable cross-zone load balancing for even distribution
  enable_cross_zone_load_balancing = true

  # Enable deletion protection for production
  enable_deletion_protection = var.environment == "production" ? true : false

  # Subnet mappings (must span multiple AZs for high availability)
  # NLB requires at least 2 subnets in different availability zones
  dynamic "subnet_mapping" {
    for_each = var.subnet_ids
    content {
      subnet_id = subnet_mapping.value
      # Optional: Assign static IP per AZ
      # allocation_id = aws_eip.nlb[subnet_mapping.key].id
    }
  }

  # Enable access logs to S3 (optional but recommended)
  # access_logs {
  #   bucket  = aws_s3_bucket.nlb_logs.id
  #   prefix  = "nlb"
  #   enabled = true
  # }

  tags = {
    Name        = "${var.environment}-app-nlb"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Service     = "LoadBalancing"
  }
}

#---------------------------------------------------------------------
# Target Group: TCP (for general TCP traffic)
#---------------------------------------------------------------------
resource "aws_lb_target_group" "tcp" {
  name     = "${var.environment}-tcp-tg"
  port     = 8080
  protocol = "TCP"
  vpc_id   = var.vpc_id

  # Target type: instance | ip | alb | lambda
  target_type = "instance"

  # Deregistration delay (time to drain connections)
  deregistration_delay = 30

  # Health check configuration
  health_check {
    enabled             = true
    interval            = 30              # Check every 30 seconds
    port                = "traffic-port"  # Use same port as target
    protocol            = "TCP"           # TCP health check
    healthy_threshold   = 3               # 3 successful checks = healthy
    unhealthy_threshold = 3               # 3 failed checks = unhealthy
  }

  # Connection termination on deregistration
  connection_termination = true

  # Preserve client IP address
  preserve_client_ip = true

  tags = {
    Name        = "${var.environment}-tcp-target-group"
    Environment = var.environment
    Protocol    = "TCP"
  }
}

#---------------------------------------------------------------------
# Target Group: TLS (for encrypted TCP traffic)
#---------------------------------------------------------------------
resource "aws_lb_target_group" "tls" {
  name     = "${var.environment}-tls-tg"
  port     = 443
  protocol = "TLS"
  vpc_id   = var.vpc_id

  target_type = "instance"

  # TLS-specific settings
  # Proxy protocol v2 adds connection information to the TCP stream
  proxy_protocol_v2 = false

  health_check {
    enabled             = true
    interval            = 30
    port                = 443
    protocol            = "TCP"  # Can also use "HTTPS" for application-layer health checks
    healthy_threshold   = 3
    unhealthy_threshold = 3

    # Optional: HTTP/HTTPS health check parameters
    # protocol = "HTTPS"
    # path     = "/health"
    # matcher  = "200-299"
  }

  tags = {
    Name        = "${var.environment}-tls-target-group"
    Environment = var.environment
    Protocol    = "TLS"
  }
}

#---------------------------------------------------------------------
# Target Group: UDP (for UDP traffic like DNS, QUIC)
#---------------------------------------------------------------------
resource "aws_lb_target_group" "udp" {
  name     = "${var.environment}-udp-tg"
  port     = 53
  protocol = "UDP"
  vpc_id   = var.vpc_id

  target_type = "instance"

  health_check {
    enabled             = true
    interval            = 30
    port                = 53
    protocol            = "TCP"  # UDP health checks use TCP or HTTP(S)
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  tags = {
    Name        = "${var.environment}-udp-target-group"
    Environment = var.environment
    Protocol    = "UDP"
  }
}

#---------------------------------------------------------------------
# Listener: TCP on port 80
#---------------------------------------------------------------------
resource "aws_lb_listener" "tcp" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tcp.arn
  }

  tags = {
    Name = "${var.environment}-tcp-listener"
  }
}

#---------------------------------------------------------------------
# Listener: TLS on port 443 with certificate
#---------------------------------------------------------------------
resource "aws_lb_listener" "tls" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "TLS"
  certificate_arn   = aws_acm_certificate.main.arn

  # TLS security policy
  # Options: ELBSecurityPolicy-TLS13-1-2-2021-06, ELBSecurityPolicy-TLS-1-2-2017-01, etc.
  ssl_policy = "ELBSecurityPolicy-TLS13-1-2-2021-06"

  # ALPN policy for HTTP/2, HTTP/1.1
  alpn_policy = "HTTP2Preferred"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tls.arn
  }

  tags = {
    Name = "${var.environment}-tls-listener"
  }
}

#---------------------------------------------------------------------
# Listener: UDP on port 53 (DNS example)
#---------------------------------------------------------------------
resource "aws_lb_listener" "udp" {
  load_balancer_arn = aws_lb.main.arn
  port              = 53
  protocol          = "UDP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.udp.arn
  }

  tags = {
    Name = "${var.environment}-udp-listener"
  }
}

#---------------------------------------------------------------------
# Target Group Attachments (register EC2 instances)
#---------------------------------------------------------------------
# Example: Attach existing EC2 instances to target groups
# You would typically use auto-scaling groups instead

resource "aws_lb_target_group_attachment" "tcp_instance_1" {
  target_group_arn = aws_lb_target_group.tcp.arn
  target_id        = aws_instance.app_server_1.id
  port             = 8080
}

resource "aws_lb_target_group_attachment" "tcp_instance_2" {
  target_group_arn = aws_lb_target_group.tcp.arn
  target_id        = aws_instance.app_server_2.id
  port             = 8080
}

resource "aws_lb_target_group_attachment" "tls_instance_1" {
  target_group_arn = aws_lb_target_group.tls.arn
  target_id        = aws_instance.app_server_1.id
  port             = 443
}

resource "aws_lb_target_group_attachment" "tls_instance_2" {
  target_group_arn = aws_lb_target_group.tls.arn
  target_id        = aws_instance.app_server_2.id
  port             = 443
}

#---------------------------------------------------------------------
# ACM Certificate (for TLS listener)
#---------------------------------------------------------------------
resource "aws_acm_certificate" "main" {
  domain_name       = "example.com"
  validation_method = "DNS"

  subject_alternative_names = [
    "*.example.com",
  ]

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name        = "${var.environment}-certificate"
    Environment = var.environment
  }
}

#---------------------------------------------------------------------
# Security Group for NLB targets (EC2 instances)
#---------------------------------------------------------------------
resource "aws_security_group" "nlb_targets" {
  name        = "${var.environment}-nlb-targets-sg"
  description = "Security group for NLB target instances"
  vpc_id      = var.vpc_id

  # Allow TCP traffic on port 8080 from anywhere
  ingress {
    description = "HTTP from NLB"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow TLS traffic on port 443
  ingress {
    description = "HTTPS from NLB"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow UDP traffic on port 53
  ingress {
    description = "DNS from NLB"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-nlb-targets-sg"
    Environment = var.environment
  }
}

#---------------------------------------------------------------------
# Example EC2 Instances (target servers)
#---------------------------------------------------------------------
# These are placeholder instances - in production, use Auto Scaling Groups

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "app_server_1" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.medium"
  subnet_id     = var.subnet_ids[0]

  vpc_security_group_ids = [aws_security_group.nlb_targets.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "Server 1" > /var/www/html/index.html
              EOF

  tags = {
    Name        = "${var.environment}-app-server-1"
    Environment = var.environment
  }
}

resource "aws_instance" "app_server_2" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.medium"
  subnet_id     = var.subnet_ids[1]

  vpc_security_group_ids = [aws_security_group.nlb_targets.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "Server 2" > /var/www/html/index.html
              EOF

  tags = {
    Name        = "${var.environment}-app-server-2"
    Environment = var.environment
  }
}

#---------------------------------------------------------------------
# Outputs
#---------------------------------------------------------------------
output "nlb_dns_name" {
  description = "DNS name of the Network Load Balancer"
  value       = aws_lb.main.dns_name
}

output "nlb_arn" {
  description = "ARN of the Network Load Balancer"
  value       = aws_lb.main.arn
}

output "nlb_zone_id" {
  description = "Zone ID of the Network Load Balancer"
  value       = aws_lb.main.zone_id
}

output "tcp_target_group_arn" {
  description = "ARN of the TCP target group"
  value       = aws_lb_target_group.tcp.arn
}

output "tls_target_group_arn" {
  description = "ARN of the TLS target group"
  value       = aws_lb_target_group.tls.arn
}

output "udp_target_group_arn" {
  description = "ARN of the UDP target group"
  value       = aws_lb_target_group.udp.arn
}
