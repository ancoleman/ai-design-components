# GCP Networking Reference

VPC, Load Balancing, CDN, and Cloud Armor patterns.


## Table of Contents

- [VPC Configuration](#vpc-configuration)
- [Global Load Balancing](#global-load-balancing)
- [Cloud Armor (WAF)](#cloud-armor-waf)
- [VPC Peering](#vpc-peering)
- [Private Service Connection](#private-service-connection)

## VPC Configuration

```hcl
resource "google_compute_network" "main" {
  name                    = "main-vpc"
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

resource "google_compute_subnetwork" "private" {
  name          = "private-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.main.id

  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "gke-pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "gke-services"
    ip_cidr_range = "10.2.0.0/20"
  }

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
  }
}

# Cloud NAT for private instances
resource "google_compute_router" "router" {
  name    = "nat-router"
  region  = "us-central1"
  network = google_compute_network.main.id
}

resource "google_compute_router_nat" "nat" {
  name                               = "nat-gateway"
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}
```

## Global Load Balancing

```hcl
# Global HTTP(S) Load Balancer
resource "google_compute_global_address" "lb_ip" {
  name = "global-lb-ip"
}

resource "google_compute_global_forwarding_rule" "https" {
  name       = "https-forwarding-rule"
  target     = google_compute_target_https_proxy.default.id
  port_range = "443"
  ip_address = google_compute_global_address.lb_ip.address
}

resource "google_compute_target_https_proxy" "default" {
  name             = "https-proxy"
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
}

resource "google_compute_managed_ssl_certificate" "default" {
  name = "ssl-cert"
  managed {
    domains = ["example.com", "www.example.com"]
  }
}

resource "google_compute_url_map" "default" {
  name            = "url-map"
  default_service = google_compute_backend_service.default.id

  host_rule {
    hosts        = ["example.com"]
    path_matcher = "allpaths"
  }

  path_matcher {
    name            = "allpaths"
    default_service = google_compute_backend_service.default.id

    path_rule {
      paths   = ["/api/*"]
      service = google_compute_backend_service.api.id
    }
  }
}

resource "google_compute_backend_service" "default" {
  name                  = "backend-service"
  protocol              = "HTTP"
  timeout_sec           = 30
  health_checks         = [google_compute_health_check.default.id]
  load_balancing_scheme = "EXTERNAL_MANAGED"

  backend {
    group           = google_compute_region_network_endpoint_group.cloudrun.id
    balancing_mode  = "UTILIZATION"
    capacity_scaler = 1.0
  }

  cdn_policy {
    cache_mode                   = "CACHE_ALL_STATIC"
    default_ttl                  = 3600
    client_ttl                   = 7200
    max_ttl                      = 86400
    negative_caching             = true
    serve_while_stale            = 86400

    cache_key_policy {
      include_protocol = true
      include_host     = true
    }
  }

  iap {
    oauth2_client_id     = google_iap_client.default.client_id
    oauth2_client_secret = google_iap_client.default.secret
  }
}
```

## Cloud Armor (WAF)

```hcl
resource "google_compute_security_policy" "policy" {
  name = "security-policy"

  # Default rule
  rule {
    action   = "allow"
    priority = "2147483647"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
  }

  # Block specific countries
  rule {
    action   = "deny(403)"
    priority = "1000"
    match {
      expr {
        expression = "origin.region_code == 'CN' || origin.region_code == 'RU'"
      }
    }
  }

  # Rate limiting
  rule {
    action   = "rate_based_ban"
    priority = "2000"
    match {
      versioned_expr = "SRC_IPS_V1"
      config {
        src_ip_ranges = ["*"]
      }
    }
    rate_limit_options {
      conform_action = "allow"
      exceed_action  = "deny(429)"

      rate_limit_threshold {
        count        = 100
        interval_sec = 60
      }

      ban_duration_sec = 600
    }
  }

  # SQL injection protection
  rule {
    action   = "deny(403)"
    priority = "3000"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('sqli-stable')"
      }
    }
  }

  # XSS protection
  rule {
    action   = "deny(403)"
    priority = "3001"
    match {
      expr {
        expression = "evaluatePreconfiguredExpr('xss-stable')"
      }
    }
  }

  adaptive_protection_config {
    layer_7_ddos_defense_config {
      enable = true
    }
  }
}

# Attach to backend service
resource "google_compute_backend_service_security_policy_attachment" "policy" {
  backend_service = google_compute_backend_service.default.id
  security_policy = google_compute_security_policy.policy.id
}
```

## VPC Peering

```hcl
resource "google_compute_network_peering" "peering1" {
  name         = "peering-to-network2"
  network      = google_compute_network.network1.id
  peer_network = google_compute_network.network2.id

  export_custom_routes = true
  import_custom_routes = true
}

resource "google_compute_network_peering" "peering2" {
  name         = "peering-to-network1"
  network      = google_compute_network.network2.id
  peer_network = google_compute_network.network1.id

  export_custom_routes = true
  import_custom_routes = true
}
```

## Private Service Connection

```hcl
resource "google_compute_global_address" "private_ip_alloc" {
  name          = "private-ip-alloc"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.main.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.main.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_alloc.name]
}
```
