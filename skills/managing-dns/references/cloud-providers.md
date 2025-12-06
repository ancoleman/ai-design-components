# Cloud DNS Providers - Detailed Reference

Complete comparison of major cloud DNS providers with features, pricing, and configuration examples.

## Table of Contents

1. [AWS Route53](#aws-route53)
2. [Google Cloud DNS](#google-cloud-dns)
3. [Azure DNS](#azure-dns)
4. [Cloudflare](#cloudflare)
5. [Provider Comparison Matrix](#provider-comparison-matrix)
6. [Selection Guide](#selection-guide)

---

## AWS Route53

### Overview

AWS Route53 is Amazon's highly available and scalable DNS service with advanced routing policies and tight AWS integration.

**Key Strengths:**
- Advanced routing policies (7 types)
- Health checks with automatic failover
- ALIAS records for AWS resources (free queries)
- Traffic Flow visual policy editor
- Tight integration with AWS services

**Best For:**
- AWS-heavy infrastructure
- Complex routing requirements
- Need for health checks and failover
- Organizations using AWS ecosystem

### Features

**Routing Policies:**
1. **Simple**: Standard DNS routing
2. **Weighted**: Percentage-based traffic distribution
3. **Latency-based**: Route to lowest latency endpoint
4. **Geolocation**: Route based on user location
5. **Geoproximity**: Route based on resource and user location
6. **Failover**: Active-passive failover with health checks
7. **Multivalue**: Return multiple IPs with health checks

**Health Checks:**
- HTTP/HTTPS/TCP endpoint monitoring
- Calculated health checks (combine multiple checks)
- CloudWatch alarm integration
- String matching on response
- Latency measurements

**ALIAS Records:**
- CNAME-like functionality at zone apex
- Free queries (no charge for ALIAS to AWS resources)
- Automatic IP update when target changes
- Supported targets: ELB, CloudFront, S3, API Gateway, VPC endpoints

**DNSSEC:**
- Supported for both domain registration and hosted zones
- Key signing key (KSK) management
- Integration with domain registrars

### Pricing (2025)

**Hosted Zones:**
- $0.50/month per hosted zone
- First 25 zones: $0.50/month each
- Additional zones: pricing decreases with volume

**Queries:**
- Standard queries: $0.40 per million (first 1 billion)
- Latency-based: $0.60 per million
- Geo/Geoproximity: $0.70 per million
- ALIAS queries to AWS resources: Free

**Health Checks:**
- Basic (HTTP/HTTPS/TCP): $0.50/month per endpoint
- Calculated: $1.00/month per health check
- Optional features (HTTPS, string matching, fast interval): Additional cost

**Traffic Flow:**
- $50/month per policy record
- Includes unlimited policy configurations

### Configuration Examples

**Basic A Record:**
```hcl
resource "aws_route53_zone" "main" {
  name = "example.com"
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.example.com"
  type    = "A"
  ttl     = 300
  records = ["192.0.2.1"]
}
```

**ALIAS Record (CloudFront):**
```hcl
resource "aws_route53_record" "apex" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}
```

**Weighted Routing (Canary):**
```hcl
# 90% to stable
resource "aws_route53_record" "stable" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "api.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "stable"

  weighted_routing_policy {
    weight = 90
  }

  records = ["192.0.2.1"]
}

# 10% to canary
resource "aws_route53_record" "canary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "api.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "canary"

  weighted_routing_policy {
    weight = 10
  }

  records = ["192.0.2.2"]
}
```

**Geolocation Routing:**
```hcl
# North America users
resource "aws_route53_record" "na" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 300
  set_identifier = "north-america"

  geolocation_routing_policy {
    continent = "NA"
  }

  records = ["192.0.2.1"]
}

# Europe users
resource "aws_route53_record" "eu" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 300
  set_identifier = "europe"

  geolocation_routing_policy {
    continent = "EU"
  }

  records = ["192.0.2.10"]
}

# Default fallback
resource "aws_route53_record" "default" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 300
  set_identifier = "default"

  geolocation_routing_policy {
    location = "*"
  }

  records = ["192.0.2.100"]
}
```

**Health Check with Failover:**
```hcl
# Health check
resource "aws_route53_health_check" "primary" {
  fqdn              = "primary.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "primary-health-check"
  }
}

# Primary record
resource "aws_route53_record" "primary" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = "api.example.com"
  type            = "A"
  ttl             = 60
  set_identifier  = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.primary.id
  records         = ["192.0.2.1"]
}

# Secondary record
resource "aws_route53_record" "secondary" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = "api.example.com"
  type            = "A"
  ttl             = 60
  set_identifier  = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  records = ["192.0.2.2"]
}
```

### When to Choose Route53

**Choose Route53 if:**
- Already using AWS services (EC2, ELB, CloudFront, S3)
- Need advanced routing policies (geolocation, latency, weighted)
- Require health checks with automatic failover
- Want ALIAS records to AWS resources (free queries)
- Using Terraform or CloudFormation for infrastructure
- Need Traffic Flow for complex routing scenarios

**Skip Route53 if:**
- Not using AWS (no ALIAS benefit)
- Need lowest DNS costs (Cloud DNS is cheaper per zone)
- Want simplest setup (Cloudflare easier for beginners)
- Need fastest global DNS (Cloudflare typically faster)

---

## Google Cloud DNS

### Overview

Google Cloud DNS is a high-performance, scalable DNS service running on Google's infrastructure with strong DNSSEC support.

**Key Strengths:**
- Google's global anycast network
- Strong DNSSEC support with automatic key rotation
- Private DNS zones for VPC internal resolution
- Split-horizon DNS (different answers for internal/external)
- Lowest hosted zone cost among major providers

**Best For:**
- GCP-native applications
- DNSSEC requirements
- Private/internal DNS zones
- Organizations using Google Cloud

### Features

**DNS Zones:**
- Public zones (internet-accessible)
- Private zones (VPC-only, internal DNS)
- Managed zones with automatic backups
- Zone transfers (AXFR) supported

**DNSSEC:**
- One-click enablement
- Automatic key rotation
- Support for custom signing algorithms
- DS record management at registrar

**Routing Policies:**
- Weighted round robin
- Geolocation routing (GeoIP)
- Private zone resolution for VPCs

**Cloud DNS Features:**
- 100% SLA
- Fast global propagation
- Logging to Cloud Logging
- Integration with Cloud Monitoring

### Pricing (2025)

**Hosted Zones:**
- $0.20/month per managed zone (cheapest among major providers)
- First 25 zones: $0.20/month each

**Queries:**
- $0.40 per million queries (first 1 billion/month)
- Reduced pricing for higher volumes

**Note:** Cloud DNS pricing is the lowest for hosted zones among AWS, GCP, and Azure.

### Configuration Examples

**Basic Zone and Records:**
```hcl
resource "google_dns_managed_zone" "main" {
  name        = "example-com"
  dns_name    = "example.com."
  description = "Production DNS zone"

  dnssec_config {
    state = "on"
  }
}

resource "google_dns_record_set" "a" {
  name         = "example.com."
  managed_zone = google_dns_managed_zone.main.name
  type         = "A"
  ttl          = 300
  rrdatas      = ["192.0.2.1", "192.0.2.2"]
}

resource "google_dns_record_set" "www" {
  name         = "www.example.com."
  managed_zone = google_dns_managed_zone.main.name
  type         = "CNAME"
  ttl          = 3600
  rrdatas      = ["example.com."]
}
```

**Private DNS Zone:**
```hcl
resource "google_dns_managed_zone" "private" {
  name        = "internal-example"
  dns_name    = "internal.example.com."
  description = "Private DNS zone for VPC"
  visibility  = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.main.id
    }
    networks {
      network_url = google_compute_network.staging.id
    }
  }
}

resource "google_dns_record_set" "internal_db" {
  name         = "db.internal.example.com."
  managed_zone = google_dns_managed_zone.private.name
  type         = "A"
  ttl          = 300
  rrdatas      = ["10.0.1.10"]
}
```

**Geolocation Routing:**
```hcl
resource "google_dns_record_set" "geo" {
  name         = "app.example.com."
  managed_zone = google_dns_managed_zone.main.name
  type         = "A"
  ttl          = 300

  routing_policy {
    geo {
      location = "us-central1"
      rrdatas  = ["192.0.2.1"]
    }
    geo {
      location = "europe-west1"
      rrdatas  = ["192.0.2.10"]
    }
  }
}
```

### When to Choose Cloud DNS

**Choose Cloud DNS if:**
- Using Google Cloud Platform (GKE, GCE, Cloud Run)
- Need DNSSEC with automatic management
- Require private DNS zones for VPC
- Want split-horizon DNS (different internal/external records)
- Need lowest hosted zone cost
- Using Terraform for GCP infrastructure

**Skip Cloud DNS if:**
- Not using GCP (no private zone benefit)
- Need advanced routing policies (Route53 has more)
- Want built-in DDoS protection (Cloudflare better)
- Need health checks with failover (Route53 better)

---

## Azure DNS

### Overview

Azure DNS is Microsoft's cloud DNS service with tight Azure integration and support for both public and private DNS zones.

**Key Strengths:**
- Seamless Azure integration
- Azure Private DNS zones for VNets
- Azure role-based access control (RBAC)
- Traffic Manager integration
- Anycast network (Microsoft's global infrastructure)

**Best For:**
- Azure-native applications
- Integration with Azure Traffic Manager
- Organizations using Microsoft Azure
- Hybrid cloud scenarios

### Features

**Public DNS:**
- Internet-facing DNS zones
- Standard record types
- Anycast DNS for fast resolution
- Azure RBAC for access control

**Private DNS:**
- Private DNS zones for Azure Virtual Networks
- Auto-registration of VM hostnames
- Cross-region resolution
- Hybrid cloud DNS resolution

**Integration:**
- Azure Traffic Manager (global load balancing)
- Azure Front Door (CDN + WAF)
- Azure Private Link
- Azure Active Directory (authentication)

**ALIAS Records:**
- Point zone apex to Azure resources
- Traffic Manager profiles
- Azure CDN endpoints
- Azure Front Door

### Pricing (2025)

**Public Hosted Zones:**
- $0.50/month per zone (first 25 zones)
- $0.10/month per zone (additional zones)

**Private DNS Zones:**
- $0.50/month per private zone
- $0.10/month per VNet link

**Queries:**
- $0.40 per million queries (first 1 billion/month)

### Configuration Examples

**Public DNS Zone:**
```hcl
resource "azurerm_dns_zone" "main" {
  name                = "example.com"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_dns_a_record" "www" {
  name                = "www"
  zone_name           = azurerm_dns_zone.main.name
  resource_group_name = azurerm_resource_group.main.name
  ttl                 = 300
  records             = ["192.0.2.1"]
}

resource "azurerm_dns_cname_record" "blog" {
  name                = "blog"
  zone_name           = azurerm_dns_zone.main.name
  resource_group_name = azurerm_resource_group.main.name
  ttl                 = 3600
  record              = "example.com"
}
```

**Private DNS Zone:**
```hcl
resource "azurerm_private_dns_zone" "internal" {
  name                = "internal.example.com"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "main" {
  name                  = "main-vnet-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.internal.name
  virtual_network_id    = azurerm_virtual_network.main.id
  registration_enabled  = true  # Auto-register VM hostnames
}

resource "azurerm_private_dns_a_record" "db" {
  name                = "db"
  zone_name           = azurerm_private_dns_zone.internal.name
  resource_group_name = azurerm_resource_group.main.name
  ttl                 = 300
  records             = ["10.0.1.10"]
}
```

**Traffic Manager Integration:**
```hcl
resource "azurerm_traffic_manager_profile" "main" {
  name                = "app-traffic-manager"
  resource_group_name = azurerm_resource_group.main.name

  traffic_routing_method = "Performance"  # or "Weighted", "Priority", "Geographic"

  dns_config {
    relative_name = "app"
    ttl           = 60
  }

  monitor_config {
    protocol = "HTTPS"
    port     = 443
    path     = "/health"
  }
}

# DNS record pointing to Traffic Manager
resource "azurerm_dns_cname_record" "app" {
  name                = "app"
  zone_name           = azurerm_dns_zone.main.name
  resource_group_name = azurerm_resource_group.main.name
  ttl                 = 300
  record              = azurerm_traffic_manager_profile.main.fqdn
}
```

### When to Choose Azure DNS

**Choose Azure DNS if:**
- Using Microsoft Azure (App Service, VMs, AKS)
- Need Azure Private DNS for VNet resolution
- Want integration with Traffic Manager
- Using Azure Private Link
- Prefer ARM templates or Bicep for infrastructure
- Require Azure RBAC for DNS management

**Skip Azure DNS if:**
- Not using Azure (no private zone benefit)
- Need advanced routing (Route53 has more options)
- Want lowest zone cost (Cloud DNS cheaper)
- Need fastest DNS globally (Cloudflare typically faster)

---

## Cloudflare

### Overview

Cloudflare DNS is one of the world's fastest DNS services with built-in DDoS protection and generous free tier.

**Key Strengths:**
- Fastest DNS query times globally (consistently)
- Built-in DDoS protection (always-on)
- Free tier with unlimited queries
- Tight CDN integration
- Simplest setup and management
- CNAME flattening (works at zone apex)

**Best For:**
- Multi-cloud or cloud-agnostic infrastructure
- Performance-focused applications
- Budget-conscious organizations
- DDoS protection requirements
- Global user base

### Features

**Performance:**
- Global anycast network (200+ data centers)
- Fastest average DNS query time
- Automatic IPv6 support
- Edge-optimized resolution

**Security:**
- Built-in DDoS protection (all plans)
- DNSSEC (one-click enable)
- CAA record support
- Rate limiting and access control

**Load Balancing (Business/Enterprise):**
- Geo-steering
- Health checks (HTTP/HTTPS/TCP)
- Session affinity
- Weighted pools
- Active-active or active-passive

**CDN Integration:**
- Proxied records (orange cloud)
- Automatic SSL/TLS
- WAF (Web Application Firewall)
- Caching and optimization

**CNAME Flattening:**
- CNAME works at zone apex
- Automatically resolved to A record
- Transparent to clients

### Pricing (2025)

**Free Tier:**
- Unlimited DNS queries
- Basic DDoS protection
- DNSSEC
- SSL/TLS
- CDN caching
- IPv6 support

**Pro ($20/month per zone):**
- All free features
- Enhanced DDoS protection
- Page rules
- Image optimization
- Mobile optimization

**Business ($200/month per zone):**
- All Pro features
- Load balancing (geo-steering)
- Advanced DDoS protection
- 100% uptime SLA
- Enhanced support

**Enterprise (Custom pricing):**
- Custom SLA
- Dedicated support
- Advanced security features
- Custom SSL certificates

### Configuration Examples

**Basic Records:**
```hcl
resource "cloudflare_zone" "main" {
  account_id = var.cloudflare_account_id
  zone       = "example.com"
}

resource "cloudflare_record" "apex" {
  zone_id = cloudflare_zone.main.id
  name    = "example.com"
  type    = "A"
  value   = "192.0.2.1"
  ttl     = 300
  proxied = true  # Route through Cloudflare CDN (orange cloud)
}

resource "cloudflare_record" "www" {
  zone_id = cloudflare_zone.main.id
  name    = "www"
  type    = "CNAME"
  value   = "example.com"
  ttl     = 3600
  proxied = true
}
```

**Load Balancer with Geo-Steering:**
```hcl
# US pool
resource "cloudflare_load_balancer_pool" "us" {
  account_id = var.cloudflare_account_id
  name       = "us-pool"

  origins {
    name    = "us-east-1"
    address = "192.0.2.1"
    enabled = true
  }

  check_regions = ["WNAM", "ENAM"]

  monitor = cloudflare_load_balancer_monitor.https.id
}

# Europe pool
resource "cloudflare_load_balancer_pool" "eu" {
  account_id = var.cloudflare_account_id
  name       = "eu-pool"

  origins {
    name    = "eu-west-1"
    address = "192.0.2.10"
    enabled = true
  }

  check_regions = ["WEU", "EEU"]

  monitor = cloudflare_load_balancer_monitor.https.id
}

# Health check
resource "cloudflare_load_balancer_monitor" "https" {
  account_id = var.cloudflare_account_id
  type       = "https"
  port       = 443
  path       = "/health"
  interval   = 60
  timeout    = 5
  retries    = 2
}

# Load balancer with geo-steering
resource "cloudflare_load_balancer" "app" {
  zone_id          = cloudflare_zone.main.id
  name             = "app.example.com"
  default_pool_ids = [cloudflare_load_balancer_pool.us.id]
  fallback_pool_id = cloudflare_load_balancer_pool.us.id
  ttl              = 30
  proxied          = true

  region_pools {
    region   = "WNAM"
    pool_ids = [cloudflare_load_balancer_pool.us.id]
  }

  region_pools {
    region   = "WEU"
    pool_ids = [cloudflare_load_balancer_pool.eu.id]
  }
}
```

### When to Choose Cloudflare

**Choose Cloudflare if:**
- Need fastest DNS query times globally
- Want built-in DDoS protection
- Budget-conscious (free tier very generous)
- Multi-cloud or cloud-agnostic
- Need CDN + DNS combo
- Want simplest management interface
- Global user base

**Skip Cloudflare if:**
- Already heavily invested in cloud provider (AWS/GCP/Azure)
- Need advanced routing beyond geo-steering (Route53 better)
- Require integration with cloud-specific features
- Need private DNS zones (cloud providers better)

---

## Provider Comparison Matrix

### Feature Comparison

| Feature | Route53 | Cloud DNS | Azure DNS | Cloudflare |
|---------|---------|-----------|-----------|------------|
| **Routing Policies** | 7 types | 2 types | Via Traffic Mgr | Geo-steering |
| **Health Checks** | ✅ Native | ❌ | ✅ Traffic Mgr | ✅ Business+ |
| **DNSSEC** | ✅ | ✅ Auto rotation | ✅ | ✅ One-click |
| **Private Zones** | ❌ | ✅ VPC | ✅ VNet | ❌ |
| **ALIAS/CNAME Apex** | ✅ ALIAS | ❌ | ✅ | ✅ Flattening |
| **DDoS Protection** | Via Shield | Via Cloud Armor | Via DDoS Prot | ✅ Built-in |
| **CDN Integration** | CloudFront | Cloud CDN | Front Door | ✅ Native |
| **Free Tier** | ❌ | ❌ | ❌ | ✅ Generous |
| **Global Anycast** | ✅ | ✅ | ✅ | ✅ 200+ DCs |

### Pricing Comparison

| Item | Route53 | Cloud DNS | Azure DNS | Cloudflare |
|------|---------|-----------|-----------|------------|
| **Hosted Zone** | $0.50/mo | $0.20/mo | $0.50/mo | Free |
| **Queries (per M)** | $0.40 | $0.40 | $0.40 | Free |
| **Health Checks** | $0.50/mo | N/A | Via TM | $200/mo (Business+) |
| **Free Tier** | ❌ | ❌ | ❌ | ✅ Unlimited queries |

### Performance Comparison (Average Query Time)

Based on independent benchmarks (2025):

1. **Cloudflare**: ~10-15ms (consistently fastest)
2. **Cloud DNS**: ~15-20ms
3. **Route53**: ~15-25ms
4. **Azure DNS**: ~20-30ms

*Note: Actual performance varies by client location and network conditions*

---

## Selection Guide

### Decision Tree

```
Primary Cloud Platform?
├─ AWS → Route53 (ALIAS, tight integration)
├─ GCP → Cloud DNS (private zones, DNSSEC)
├─ Azure → Azure DNS (Traffic Manager, VNet)
└─ Multi-cloud/None → Continue...

Need Advanced Routing?
├─ Yes → Route53 (7 routing policies)
└─ No → Continue...

Need Fastest Global DNS?
├─ Yes → Cloudflare (consistently fastest)
└─ No → Continue...

Need Private/Internal DNS?
├─ Yes → Cloud DNS or Azure DNS (VPC/VNet zones)
└─ No → Continue...

Budget Consideration?
├─ Lowest zone cost → Cloud DNS ($0.20/mo)
├─ Free tier → Cloudflare (unlimited)
└─ Standard → Any (similar query pricing)

Need DDoS Protection?
├─ Yes → Cloudflare (built-in all plans)
└─ No → Any provider
```

### By Use Case

**E-commerce Website (Global):**
- Primary: Cloudflare (speed + DDoS + CDN)
- Alternative: Route53 (if AWS-based)

**Enterprise SaaS (AWS-based):**
- Primary: Route53 (ALIAS, health checks, AWS integration)
- Alternative: Cloudflare + Route53 (multi-provider)

**Startup (Budget-conscious):**
- Primary: Cloudflare (free tier)
- Alternative: Cloud DNS (lowest zone cost)

**Internal Corporate DNS:**
- Primary: Cloud DNS or Azure DNS (private zones)
- Alternative: Route53 + VPN (if AWS)

**API Platform with Failover:**
- Primary: Route53 (health checks, weighted routing)
- Alternative: Cloudflare Business (load balancing)

**Multi-cloud Architecture:**
- Primary: Cloudflare (cloud-agnostic)
- Alternative: OctoDNS or DNSControl (sync multiple providers)

### Multi-Provider Strategies

**Strategy 1: Primary + Secondary DNS**
```
Primary:   Cloudflare (fastest, DDoS protection)
Secondary: Route53 (AWS resources, health checks)

Use OctoDNS to sync records between providers
```

**Strategy 2: Regional Split**
```
Global:    Cloudflare (CDN + DNS)
AWS:       Route53 (internal AWS resources)
GCP:       Cloud DNS (GCP-specific services)

Use Terraform modules to manage all providers
```

**Strategy 3: Failover Redundancy**
```
Primary:   Route53 (primary authoritative)
Backup:    Cloudflare (NS backup)
Sync:      OctoDNS (automatic sync)

Configure both as NS records at registrar
```

---

## Summary

### Quick Recommendations

**Choose AWS Route53 for:**
- AWS-heavy infrastructure
- Advanced routing policies
- Health checks and automatic failover
- ALIAS records to AWS resources

**Choose Google Cloud DNS for:**
- GCP-native applications
- Strong DNSSEC requirements
- Private VPC DNS zones
- Lowest hosted zone cost

**Choose Azure DNS for:**
- Azure-native applications
- Traffic Manager integration
- Private VNet DNS zones
- Azure RBAC requirements

**Choose Cloudflare for:**
- Fastest global DNS performance
- Built-in DDoS protection
- Budget-conscious (free tier)
- Multi-cloud or cloud-agnostic
- CDN + DNS combo

### No Wrong Choice

All four providers offer:
- 100% uptime SLAs
- Global anycast networks
- DNSSEC support
- Similar query pricing ($0.40/M)
- Terraform/IaC support

The "best" provider depends on your specific requirements, existing infrastructure, and priorities.
