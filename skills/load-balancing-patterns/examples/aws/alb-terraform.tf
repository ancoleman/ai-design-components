# AWS Application Load Balancer (ALB) - Layer 7 HTTP Load Balancing
#
# This example demonstrates:
# - ALB with HTTPS listener
# - Path-based routing to multiple target groups
# - Health checks with custom endpoints
# - Cookie-based sticky sessions
# - SSL/TLS termination
#
# Dependencies:
# - terraform >= 1.0
# - AWS provider configured
# - VPC and subnets created
# - ACM certificate for SSL

# Application Load Balancer
resource "aws_lb" "application" {
  name               = "app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = true
  enable_http2              = true
  enable_cross_zone_load_balancing = true

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.id
    prefix  = "alb"
    enabled = true
  }

  tags = {
    Name        = "app-alb"
    Environment = "production"
  }
}

# Target Group: Web Application
resource "aws_lb_target_group" "web" {
  name     = "web-targets"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
    protocol            = "HTTP"
  }

  deregistration_delay = 30

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400  # 24 hours
    enabled         = true
  }

  tags = {
    Name = "web-targets"
  }
}

# Target Group: API
resource "aws_lb_target_group" "api" {
  name     = "api-targets"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 15  # More frequent for API
    path                = "/api/health"
    matcher             = "200,204"
    protocol            = "HTTP"
  }

  deregistration_delay = 10  # Faster for stateless API

  # Slow start for gradual traffic ramp-up
  slow_start = 30

  tags = {
    Name = "api-targets"
  }
}

# HTTPS Listener (primary)
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.application.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# HTTP Listener (redirect to HTTPS)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.application.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# Listener Rule: API path-based routing
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}

# Listener Rule: Admin host-based routing
resource "aws_lb_listener_rule" "admin" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 90

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.admin.arn
  }

  condition {
    host_header {
      values = ["admin.example.com"]
    }
  }
}

# Listener Rule: Header-based routing (API versioning)
resource "aws_lb_listener_rule" "api_v2" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 80

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api_v2.arn
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }

  condition {
    http_header {
      http_header_name = "X-API-Version"
      values           = ["v2"]
    }
  }
}

# Security Group for ALB
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP from internet (redirect to HTTPS)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-sg"
  }
}

# Outputs
output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.application.dns_name
}

output "alb_zone_id" {
  description = "Route 53 zone ID for ALB"
  value       = aws_lb.application.zone_id
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer"
  value       = aws_lb.application.arn
}
