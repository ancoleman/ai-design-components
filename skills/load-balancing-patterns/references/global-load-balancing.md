# Global Load Balancing

DNS-based global traffic management for multi-region deployments.


## Table of Contents

- [GeoDNS Routing](#geodns-routing)
  - [AWS Route 53 Geolocation Routing](#aws-route-53-geolocation-routing)
- [Latency-Based Routing](#latency-based-routing)
- [Multi-Region Failover](#multi-region-failover)
- [AWS Global Accelerator](#aws-global-accelerator)
- [CDN Integration](#cdn-integration)
- [Summary](#summary)

## GeoDNS Routing

Route users to nearest server based on geographic location.

### AWS Route 53 Geolocation Routing

```hcl
resource "aws_route53_record" "geo_us" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  geolocation_routing_policy {
    continent = "NA"
  }

  set_identifier = "US-East"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "geo_eu" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  geolocation_routing_policy {
    continent = "EU"
  }

  set_identifier = "EU-West"
  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }
}

# Default fallback
resource "aws_route53_record" "geo_default" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  geolocation_routing_policy {
    continent = "*"
  }

  set_identifier = "Default"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}
```

## Latency-Based Routing

DNS returns IP of lowest-latency endpoint.

```hcl
resource "aws_route53_record" "latency_us" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  latency_routing_policy {
    region = "us-east-1"
  }

  set_identifier = "US-East"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}
```

## Multi-Region Failover

Primary/secondary configuration with health checks.

```hcl
resource "aws_route53_record" "primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier = "Primary"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.primary.id
}

resource "aws_route53_record" "secondary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "Secondary"
  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_health_check" "primary" {
  fqdn              = aws_lb.us_east.dns_name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}
```

## AWS Global Accelerator

Global Layer 4 load balancer using AWS backbone.

```hcl
resource "aws_globalaccelerator_accelerator" "main" {
  name            = "app-accelerator"
  ip_address_type = "IPV4"
  enabled         = true
}

resource "aws_globalaccelerator_listener" "main" {
  accelerator_arn = aws_globalaccelerator_accelerator.main.id
  protocol        = "TCP"
  port_ranges {
    from_port = 443
    to_port   = 443
  }
}

resource "aws_globalaccelerator_endpoint_group" "us_east" {
  listener_arn = aws_globalaccelerator_listener.main.id
  endpoint_group_region = "us-east-1"

  endpoint_configuration {
    endpoint_id = aws_lb.us_east.arn
    weight      = 100
  }

  health_check_interval_seconds = 30
  health_check_path            = "/health"
  health_check_protocol        = "HTTPS"
  threshold_count              = 3
  traffic_dial_percentage      = 100
}
```

## CDN Integration

Combine load balancing with CDN for global content delivery.

**CloudFlare:**
- Global anycast network
- DDoS protection
- Edge caching
- Load balancing across origins

**AWS CloudFront + Route 53:**
- GeoDNS routes to CloudFront
- CloudFront caches at edge locations
- Origin load balancing with ALB/NLB

## Summary

Use GeoDNS for geographic routing, latency-based routing for performance, and failover routing for high availability. Combine with CDN for optimal global performance. Monitor DNS propagation times and TTLs carefully.
