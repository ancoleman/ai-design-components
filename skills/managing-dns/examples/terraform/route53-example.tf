# AWS Route53 Terraform Example

# Hosted Zone
resource "aws_route53_zone" "main" {
  name = "example.com"

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

# A Record
resource "aws_route53_record" "apex" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "A"
  ttl     = 300
  records = ["192.0.2.1"]
}

# CNAME Record
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.example.com"
  type    = "CNAME"
  ttl     = 3600
  records = ["example.com"]
}

# ALIAS Record (CloudFront)
resource "aws_route53_record" "cdn" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "cdn.example.com"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}

# MX Records
resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "MX"
  ttl     = 3600
  records = [
    "10 mail1.example.com",
    "20 mail2.example.com"
  ]
}

# TXT Records (SPF)
resource "aws_route53_record" "spf" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "TXT"
  ttl     = 3600
  records = ["v=spf1 include:_spf.google.com ~all"]
}

# Health Check
resource "aws_route53_health_check" "primary" {
  fqdn              = "api.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "api-health-check"
  }
}

# Failover - Primary
resource "aws_route53_record" "api_primary" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = "api.example.com"
  type            = "A"
  ttl             = 60
  set_identifier  = "primary"
  health_check_id = aws_route53_health_check.primary.id

  failover_routing_policy {
    type = "PRIMARY"
  }

  records = ["192.0.2.1"]
}

# Failover - Secondary
resource "aws_route53_record" "api_secondary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "api.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  records = ["192.0.2.2"]
}

# Outputs
output "nameservers" {
  description = "Route53 nameservers for domain registration"
  value       = aws_route53_zone.main.name_servers
}
