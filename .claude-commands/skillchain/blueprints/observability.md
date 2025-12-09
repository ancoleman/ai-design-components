# Observability Blueprint

**Version:** 1.0.0
**Last Updated:** 2024-12-06
**Category:** DevOps/Infrastructure

---

## Overview

Pre-configured skill chain optimized for implementing comprehensive observability solutions including metrics collection, distributed tracing, log aggregation, alerting, and visualization. This blueprint provides production-ready defaults for the most common observability patterns, minimizing configuration while maximizing system visibility.

---

## Trigger Keywords

**Primary (high confidence):**
- observability
- monitoring
- logging
- tracing
- metrics
- telemetry

**Secondary (medium confidence):**
- prometheus
- grafana
- opentelemetry
- datadog
- alerting
- sli/slo
- apm
- distributed tracing
- log aggregation
- instrumentation

**Example goals that match:**
- "observability stack with prometheus and grafana"
- "distributed tracing for microservices"
- "monitoring and alerting for kubernetes"
- "log aggregation with elasticsearch"
- "SLO tracking dashboard"
- "application performance monitoring setup"
- "opentelemetry instrumentation"
- "metrics collection and visualization"

---

## Skill Chain (Pre-configured)

This blueprint invokes 5 skills in the following order:

```
1. implementing-observability     (core - metrics, logs, traces)
2. creating-dashboards            (visualization and alerting UI)
3. implementing-siem              (log analysis and security)
4. building-ci-pipelines          (instrumentation in CI/CD)
5. configuring-kubernetes         (optional - k8s-specific monitoring)
```

**Total estimated time:** 30-45 minutes
**Total estimated questions:** 10-15 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. implementing-observability
```yaml
stack: "prometheus-grafana-loki"
  # Prometheus: Metrics collection and storage (pull-based)
  # Grafana: Visualization and dashboards
  # Loki: Log aggregation (Prometheus for logs)
  # OpenTelemetry: Instrumentation library (vendor-neutral)

metrics_collection:
  scrape_interval: "15s"
    # Balance between data granularity and storage cost
    # 15s is industry standard for most workloads

  retention: "15d"
    # 15 days of high-resolution data
    # Aggregate to longer-term storage after 15d

  exporters: ["prometheus", "opentelemetry"]
    # Prometheus exposition format (pull-based)
    # OTLP for vendor-neutral instrumentation

log_aggregation:
  format: "json"
    # Structured logging for better parsing
    # Includes: timestamp, level, service, trace_id, message, metadata

  levels: ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
    # Standard log levels
    # Production: INFO and above
    # Development: DEBUG and above

  retention: "30d"
    # 30 days of log retention
    # Archive to cold storage (S3) after 30d

distributed_tracing:
  library: "opentelemetry"
    # Vendor-neutral, CNCF standard
    # Supports Jaeger, Zipkin, Datadog backends

  sampling_rate: 0.1
    # Sample 10% of traces in production
    # 100% sampling for errors and high-latency requests
    # Reduces storage cost while maintaining visibility

  propagation: "w3c-trace-context"
    # W3C standard for trace context propagation
    # Works across service boundaries

alerting:
  notification_channels: ["slack", "pagerduty"]
    # Slack for low-priority alerts
    # PagerDuty for critical incidents

  rules_included: true
    # Pre-configured alert rules:
    # - High error rate (>5% for 5m)
    # - High latency (p95 >500ms for 5m)
    # - Service down (no heartbeat for 1m)
    # - Disk space low (<10% free)
    # - Memory pressure (>90% for 5m)
```

### 2. creating-dashboards
```yaml
platform: "grafana"
  # Industry-standard visualization platform
  # Supports Prometheus, Loki, Jaeger, and 100+ data sources
  # Open-source with enterprise options

dashboards_included:
  - "golden-signals"
      # The Four Golden Signals (Google SRE):
      # 1. Latency (request duration)
      # 2. Traffic (requests per second)
      # 3. Errors (error rate)
      # 4. Saturation (resource utilization)

  - "red-method"
      # For microservices:
      # - Rate (requests per second)
      # - Errors (error rate)
      # - Duration (latency percentiles)

  - "use-method"
      # For infrastructure:
      # - Utilization (CPU, memory, disk, network %)
      # - Saturation (queue depth, wait times)
      # - Errors (hardware/kernel errors)

  - "service-overview"
      # Per-service dashboard:
      # - Request rate and latency
      # - Error rate and top errors
      # - Resource usage (CPU, memory)
      # - Dependencies and external calls

  - "slo-tracking"
      # Service Level Objective monitoring:
      # - SLI (Service Level Indicator) graphs
      # - Error budget remaining
      # - Burn rate alerts

panel_types: ["time-series", "stat", "gauge", "heatmap", "table"]
  # Time-series: Metrics over time (primary)
  # Stat: Single value with threshold colors
  # Gauge: Progress toward limit (e.g., disk usage)
  # Heatmap: Latency distribution
  # Table: Top N errors, slowest endpoints

refresh_interval: "5s"
  # Auto-refresh for real-time monitoring
  # Configurable per dashboard

templating: true
  # Variables for filtering:
  # - Environment (prod, staging, dev)
  # - Service name
  # - Namespace (for k8s)
  # - Time range

annotations: true
  # Mark deployments, incidents, config changes
  # Correlate events with metric changes
```

### 3. implementing-siem
```yaml
log_analysis: "loki"
  # Loki for log aggregation (Prometheus-like for logs)
  # Lightweight, horizontally scalable
  # Uses LogQL (similar to PromQL)

indexing_strategy: "label-based"
  # Index by labels (service, env, level)
  # Full-text search on demand (not pre-indexed)
  # Cost-effective for high-volume logs

query_language: "logql"
  # Prometheus-style query language for logs
  # Example: {service="api"} |= "error" | json | level="ERROR"
  # Filters, parsers, aggregations

security_patterns:
  - "failed-login-attempts"
      # Alert on >5 failed logins in 1m from same IP

  - "unauthorized-access"
      # Alert on 401/403 status codes

  - "anomalous-traffic"
      # Detect unusual request patterns

  - "privilege-escalation"
      # Alert on sudo/admin operations

log_parsing: "auto"
  # Automatically detect JSON, logfmt, regex patterns
  # Extract fields for filtering and aggregation
```

### 4. building-ci-pipelines
```yaml
instrumentation_step: "test-and-validate"
  # Add observability checks to CI/CD:
  # - Validate metric endpoints are reachable
  # - Check log format compliance (JSON, required fields)
  # - Verify trace context propagation
  # - Test alert rules syntax

smoke_tests: true
  # Post-deployment health checks:
  # - /health endpoint responds 200
  # - Metrics endpoint (/metrics) is scrapable
  # - Logs are being ingested
  # - Traces appear in backend

deployment_annotations: true
  # Automatically annotate Grafana dashboards on deploy
  # Include: version, commit SHA, deployer, timestamp
  # Correlate deployments with metrics changes

canary_monitoring: true
  # Monitor canary deployments:
  # - Compare error rate: canary vs stable
  # - Compare latency: canary vs stable
  # - Auto-rollback if metrics degrade
```

### 5. configuring-kubernetes (optional)
```yaml
k8s_monitoring: "kube-prometheus-stack"
  # Helm chart with Prometheus Operator
  # Pre-configured dashboards for k8s components
  # ServiceMonitor CRDs for automatic scraping

metrics_collected:
  - "node-metrics"
      # CPU, memory, disk, network per node
      # kube-state-metrics for k8s object states

  - "pod-metrics"
      # Per-pod resource usage
      # Container restart counts
      # OOMKills and evictions

  - "apiserver-metrics"
      # API server request rate and latency
      # etcd performance

  - "custom-app-metrics"
      # Application-specific metrics via ServiceMonitor

log_collection: "fluent-bit"
  # Lightweight log forwarder (lower resource usage than Fluentd)
  # Runs as DaemonSet (one per node)
  # Forwards to Loki

tracing_backend: "jaeger"
  # Distributed tracing for k8s services
  # OpenTelemetry Collector as intermediary
  # Query UI for trace visualization

service_mesh_integration: false
  # Set to true if using Istio/Linkerd
  # Automatic metric collection from sidecars
  # No app instrumentation needed for basic metrics
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: Observability Focus
```
What aspects of observability are most important? (select one)

Options:
1. All three pillars (metrics, logs, traces) - comprehensive solution
2. Metrics-focused - performance and resource monitoring
3. Logs-focused - debugging and security analysis
4. Traces-focused - distributed systems and latency analysis

Your answer: _______________
```

**Why this matters:**
- Determines which components to prioritize
- Affects storage and infrastructure requirements
- Influences skill chain execution order

**Default if skipped:** "1 - All three pillars (comprehensive)"

---

### Question 2: Stack Preference
```
Which observability stack do you prefer?

Options:
1. Open-source (Prometheus/Grafana/Loki/Jaeger) - self-hosted, full control
2. Commercial SaaS (Datadog, New Relic, Dynatrace) - managed, turnkey
3. Cloud-native (AWS CloudWatch, GCP Operations, Azure Monitor) - native integration
4. Hybrid (open-source + commercial for specific needs)

Your answer: _______________
```

**Why this matters:**
- Determines configuration files and integrations
- Affects cost model (self-hosted vs SaaS)
- Influences deployment complexity

**Default if skipped:** "1 - Open-source (Prometheus/Grafana/Loki)"

---

### Question 3: Primary Use Case
```
What is your primary monitoring use case?

Options:
1. Application monitoring (APIs, services, user-facing apps)
2. Infrastructure monitoring (servers, containers, kubernetes)
3. SLO tracking (reliability engineering, error budgets)
4. Security monitoring (intrusion detection, audit logs)

Your answer: _______________
```

**Why this matters:**
- Determines default dashboard layouts
- Affects alert rule priorities
- Influences metric collection configuration

**Default if skipped:** "1 - Application monitoring"

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_observability_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "observability",
        "monitoring",
        "prometheus",
        "grafana",
        "tracing",
        "distributed tracing",
        "opentelemetry",
        "metrics collection",
        "log aggregation"
    ])

    # Secondary keywords + infrastructure
    secondary_match = (
        any(keyword in goal_lower for keyword in ["logging", "alerting", "apm", "telemetry"]) and
        any(keyword in goal_lower for keyword in ["setup", "stack", "platform", "system", "infrastructure"])
    )

    # SRE/reliability keywords
    sre_match = any(keyword in goal_lower for keyword in [
        "sli/slo",
        "slo tracking",
        "error budget",
        "golden signals",
        "reliability"
    ])

    return primary_match or secondary_match or sre_match
```

**Confidence levels:**
- **High (90%+):** Contains "observability" or "prometheus + grafana" or "opentelemetry"
- **Medium (70-89%):** Contains "monitoring" + infrastructure term, or "logging" + "aggregation"
- **Low (50-69%):** Contains "metrics" or "alerting" without clear context

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 📊 OBSERVABILITY BLUEPRINT DETECTED                        │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized Observability Blueprint!  │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ Prometheus metrics collection (15s scrape interval)   │
│  ✓ Grafana dashboards (Golden Signals, RED, USE)         │
│  ✓ Loki log aggregation (structured JSON logs)           │
│  ✓ OpenTelemetry distributed tracing (10% sampling)      │
│  ✓ Pre-built alert rules (error rate, latency, uptime)   │
│  ✓ SLO tracking and error budget monitoring              │
│  ✓ Kubernetes integration (optional)                      │
│  ✓ CI/CD instrumentation validation                       │
│                                                            │
│ Using blueprint reduces questions from 15 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~15 min)            │
│  2. Custom configuration (15 questions, ~40 min)          │
│  3. Skip all questions (use all defaults, ~10 min)        │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
observability-stack/
├── prometheus/
│   ├── prometheus.yml                 # Main Prometheus configuration
│   ├── alerts/
│   │   ├── application.rules.yml      # App-level alerts (error rate, latency)
│   │   ├── infrastructure.rules.yml   # Infra alerts (CPU, memory, disk)
│   │   └── slo.rules.yml              # SLO/SLI recording and alerting rules
│   ├── scrape_configs/
│   │   ├── kubernetes.yml             # K8s service discovery
│   │   ├── static_targets.yml         # Static scrape targets
│   │   └── federation.yml             # Prometheus federation (multi-cluster)
│   └── docker-compose.yml             # Prometheus + Alertmanager deployment
│
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   ├── prometheus.yml         # Prometheus data source config
│   │   │   ├── loki.yml               # Loki data source config
│   │   │   └── jaeger.yml             # Jaeger data source config
│   │   │
│   │   └── dashboards/
│   │       ├── dashboard.yml          # Dashboard provider config
│   │       └── dashboards/
│   │           ├── golden-signals.json     # Latency, traffic, errors, saturation
│   │           ├── red-method.json         # Rate, errors, duration (per service)
│   │           ├── use-method.json         # Utilization, saturation, errors (infra)
│   │           ├── service-overview.json   # Per-service detailed dashboard
│   │           ├── slo-tracking.json       # SLI graphs and error budget
│   │           ├── kubernetes-cluster.json # K8s cluster overview
│   │           └── logs-explorer.json      # Loki log exploration
│   │
│   ├── grafana.ini                    # Grafana configuration
│   └── docker-compose.yml             # Grafana deployment
│
├── loki/
│   ├── loki-config.yml                # Loki configuration
│   ├── promtail/
│   │   └── promtail-config.yml        # Log shipping agent config
│   └── docker-compose.yml             # Loki + Promtail deployment
│
├── opentelemetry/
│   ├── otel-collector-config.yml      # OpenTelemetry Collector config
│   │   # Receivers: OTLP, Jaeger, Zipkin
│   │   # Processors: Batch, sampling, attributes
│   │   # Exporters: Jaeger, Prometheus, Loki
│   │
│   ├── instrumentation/
│   │   ├── javascript/
│   │   │   ├── tracing.js             # Node.js auto-instrumentation
│   │   │   └── package.json           # @opentelemetry dependencies
│   │   │
│   │   ├── python/
│   │   │   ├── tracing.py             # Python auto-instrumentation
│   │   │   └── requirements.txt       # opentelemetry packages
│   │   │
│   │   ├── java/
│   │   │   └── README.md              # Java agent setup instructions
│   │   │
│   │   └── go/
│   │       ├── tracing.go             # Go manual instrumentation
│   │       └── go.mod                 # go.opentelemetry.io packages
│   │
│   └── docker-compose.yml             # OTel Collector deployment
│
├── jaeger/
│   ├── jaeger-config.yml              # Jaeger backend configuration
│   └── docker-compose.yml             # Jaeger all-in-one deployment
│
├── alertmanager/
│   ├── alertmanager.yml               # Alert routing and notification config
│   │   # Routes: severity-based routing
│   │   # Receivers: Slack, PagerDuty, email
│   │   # Inhibition: Suppress lower-priority alerts
│   │   # Grouping: Group related alerts
│   │
│   └── templates/
│       ├── slack.tmpl                 # Slack notification template
│       └── pagerduty.tmpl             # PagerDuty incident template
│
├── kubernetes/                        # Kubernetes manifests (if k8s enabled)
│   ├── namespace.yml                  # observability namespace
│   │
│   ├── prometheus/
│   │   ├── prometheus-operator.yml    # Prometheus Operator CRDs
│   │   ├── prometheus.yml             # Prometheus CR
│   │   ├── servicemonitor.yml         # ServiceMonitor for auto-discovery
│   │   └── prometheusrule.yml         # PrometheusRule for alerts
│   │
│   ├── grafana/
│   │   ├── deployment.yml             # Grafana deployment
│   │   ├── service.yml                # Grafana service (LoadBalancer/Ingress)
│   │   ├── configmap.yml              # Grafana configuration
│   │   └── secret.yml                 # Admin credentials
│   │
│   ├── loki/
│   │   ├── statefulset.yml            # Loki statefulset
│   │   ├── service.yml                # Loki service
│   │   └── fluent-bit-daemonset.yml   # Log forwarder on each node
│   │
│   └── opentelemetry/
│       ├── collector-deployment.yml   # OTel Collector deployment
│       ├── collector-configmap.yml    # OTel Collector config
│       └── instrumentation.yml        # Auto-instrumentation CR
│
├── scripts/
│   ├── setup.sh                       # One-command setup script
│   ├── validate-metrics.sh            # Check Prometheus targets are up
│   ├── validate-logs.sh               # Check Loki is receiving logs
│   ├── validate-traces.sh             # Check Jaeger has traces
│   ├── create-slo.sh                  # Generate SLO rules from config
│   └── backup-config.sh               # Backup Prometheus/Grafana data
│
├── ci-cd/
│   ├── github-actions/
│   │   └── observability-checks.yml   # CI checks for instrumentation
│   │
│   ├── gitlab-ci/
│   │   └── .gitlab-ci.yml             # GitLab CI observability pipeline
│   │
│   └── jenkins/
│       └── Jenkinsfile                # Jenkins pipeline with monitoring
│
├── examples/
│   ├── sample-app/                    # Example instrumented application
│   │   ├── app.py                     # Python Flask app with OTel
│   │   ├── Dockerfile                 # Containerized app
│   │   └── k8s-manifest.yml           # K8s deployment with ServiceMonitor
│   │
│   └── queries/
│       ├── promql-examples.md         # Common PromQL queries
│       ├── logql-examples.md          # Common LogQL queries
│       └── jaeger-queries.md          # Trace query examples
│
├── docs/
│   ├── SETUP.md                       # Step-by-step setup guide
│   ├── ARCHITECTURE.md                # System architecture diagram
│   ├── DASHBOARDS.md                  # Dashboard guide and screenshots
│   ├── ALERTS.md                      # Alert rule documentation
│   ├── SLO.md                         # SLO/SLI setup guide
│   ├── TROUBLESHOOTING.md             # Common issues and solutions
│   └── RUNBOOK.md                     # Incident response procedures
│
├── docker-compose.yml                 # Full stack deployment (all components)
├── .env.example                       # Environment variables template
├── README.md                          # Quick start guide
└── VERSION                            # Stack version tracking
```

---

## Component Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                            │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Instrumented Services (Node.js, Python, Go, Java)             │ │
│  │  - OpenTelemetry SDK embedded                                  │ │
│  │  - Exports: Metrics (OTLP), Logs (stdout), Traces (OTLP)     │ │
│  └────────────┬───────────────────┬────────────────┬──────────────┘ │
└───────────────┼───────────────────┼────────────────┼────────────────┘
                │                   │                │
                │ Metrics           │ Logs           │ Traces
                │ (OTLP)            │ (stdout/file)  │ (OTLP)
                │                   │                │
                ▼                   ▼                ▼
┌────────────────────────────────────────────────────────────────────┐
│                    COLLECTION LAYER                                │
├────────────────────┬───────────────────┬───────────────────────────┤
│  Prometheus        │  Promtail/        │  OpenTelemetry            │
│  (Pull Metrics)    │  Fluent Bit       │  Collector                │
│                    │  (Push Logs)      │  (Receive Traces)         │
│  - Scrapes /metrics│  - Tails logs     │  - Receives OTLP          │
│  - 15s interval    │  - Adds labels    │  - Samples traces (10%)   │
│  - Service         │  - Filters noise  │  - Batches and exports    │
│    discovery       │                   │                           │
└────────────────────┴───────────────────┴───────────────────────────┘
                │                   │                │
                │                   │                │
                ▼                   ▼                ▼
┌────────────────────────────────────────────────────────────────────┐
│                     STORAGE LAYER                                  │
├────────────────────┬───────────────────┬───────────────────────────┤
│  Prometheus        │  Loki             │  Jaeger                   │
│  (Time-Series DB)  │  (Log Aggregator) │  (Trace Storage)          │
│                    │                   │                           │
│  - 15d retention   │  - 30d retention  │  - 7d retention           │
│  - Block storage   │  - Label-indexed  │  - Cassandra/Badger       │
│  - PromQL API      │  - LogQL API      │  - Query UI               │
└────────────────────┴───────────────────┴───────────────────────────┘
                │                   │                │
                │                   │                │
                ▼                   ▼                ▼
┌────────────────────────────────────────────────────────────────────┐
│                   VISUALIZATION LAYER                              │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │                        Grafana                                 ││
│  │  ┌────────────────┬─────────────────┬─────────────────────┐   ││
│  │  │ Dashboards     │ Alerting        │ Explore             │   ││
│  │  │                │                 │                     │   ││
│  │  │ - Golden       │ - Alert rules   │ - Ad-hoc queries    │   ││
│  │  │   Signals      │ - Routing       │ - Metric/log/trace  │   ││
│  │  │ - RED Method   │ - Silencing     │   correlation       │   ││
│  │  │ - USE Method   │ - Annotations   │                     │   ││
│  │  │ - SLO Tracking │                 │                     │   ││
│  │  └────────────────┴─────────────────┴─────────────────────┘   ││
│  └────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ALERTING LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Alertmanager                              │   │
│  │  - Groups alerts                                            │   │
│  │  - Routes by severity                                       │   │
│  │  - Inhibits duplicates                                      │   │
│  │  - Sends to: Slack, PagerDuty, Email                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Integration Points

```
Application Instrumentation:
├── Metrics: /metrics endpoint (Prometheus exposition format)
├── Logs: stdout (JSON structured, captured by Promtail/Fluent Bit)
└── Traces: OTLP exporter → OpenTelemetry Collector → Jaeger

Service Discovery (Kubernetes):
├── Prometheus: ServiceMonitor CRDs → automatic scraping
├── Loki: Fluent Bit DaemonSet → automatic log collection
└── Jaeger: Sidecar injection (or SDK export) → trace collection

Correlation:
├── Trace ID in logs → correlate logs with traces
├── Service name label → correlate metrics with logs with traces
└── Grafana Explore → unified view across all data sources
```

---

## Default Metrics and Queries

### Golden Signals (Google SRE)

```yaml
# 1. LATENCY (request duration)
promql: |
  histogram_quantile(0.95,
    rate(http_request_duration_seconds_bucket[5m])
  )
description: "95th percentile latency over 5 minutes"
threshold: "<500ms for good user experience"

# 2. TRAFFIC (requests per second)
promql: |
  sum(rate(http_requests_total[1m])) by (service)
description: "Request rate per service"
threshold: "Baseline varies by service"

# 3. ERRORS (error rate)
promql: |
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
description: "Error rate (5xx / total requests)"
threshold: "<1% is typical SLO target"

# 4. SATURATION (resource utilization)
promql: |
  1 - (avg(node_memory_MemAvailable_bytes) / avg(node_memory_MemTotal_bytes))
description: "Memory utilization percentage"
threshold: "<90% to avoid performance degradation"
```

### RED Method (for microservices)

```yaml
# RATE
promql: |
  sum(rate(http_requests_total[5m])) by (service, method, route)
description: "Request rate per endpoint"

# ERRORS
promql: |
  sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
description: "Error count per service"

# DURATION
promql: |
  histogram_quantile(0.99,
    sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
  )
description: "99th percentile latency per service"
```

### USE Method (for infrastructure)

```yaml
# UTILIZATION
promql: |
  100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
description: "CPU utilization percentage"

# SATURATION
promql: |
  node_load15
description: "15-minute load average (queue depth indicator)"

# ERRORS
promql: |
  rate(node_network_receive_errs_total[5m])
description: "Network receive errors"
```

### Log Queries (LogQL)

```yaml
# Error logs from specific service
logql: |
  {service="api", env="prod"}
  |= "error"
  | json
  | level="ERROR"

# Slow requests (>1s)
logql: |
  {service="api"}
  | json
  | duration > 1000
  | line_format "{{.method}} {{.path}} took {{.duration}}ms"

# Count errors by endpoint
logql: |
  sum(rate({service="api"}
  | json
  | status >= 500 [5m])) by (path)
```

### Trace Queries (Jaeger)

```yaml
# Find slow traces (>500ms)
service: "api"
operation: "GET /users"
min_duration: "500ms"

# Find traces with errors
tags: "error=true"

# Find traces for specific user
tags: "user_id=12345"
```

---

## Alert Rules

### Application-Level Alerts

```yaml
# High Error Rate
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m])) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate detected"
    description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

# High Latency
- alert: HighLatency
  expr: |
    histogram_quantile(0.95,
      rate(http_request_duration_seconds_bucket[5m])
    ) > 0.5
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High latency detected"
    description: "95th percentile latency is {{ $value }}s (threshold: 500ms)"

# Service Down
- alert: ServiceDown
  expr: up == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Service {{ $labels.job }} is down"
    description: "No heartbeat received for 1 minute"
```

### Infrastructure-Level Alerts

```yaml
# High CPU
- alert: HighCPU
  expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High CPU usage"
    description: "CPU usage is {{ $value }}% (threshold: 90%)"

# High Memory
- alert: HighMemory
  expr: |
    (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) > 0.9
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High memory usage"
    description: "Memory usage is {{ $value | humanizePercentage }} (threshold: 90%)"

# Disk Space Low
- alert: DiskSpaceLow
  expr: |
    (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Disk space low on {{ $labels.device }}"
    description: "Only {{ $value | humanizePercentage }} free space remaining"
```

### SLO Alerts

```yaml
# Error Budget Burn Rate (fast burn)
- alert: FastErrorBudgetBurn
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status!~"5.."}[1h]))
        /
        sum(rate(http_requests_total[1h]))
      )
    ) > (1 - 0.999) * 14.4  # 14.4x burn rate
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Fast error budget burn detected"
    description: "At current rate, monthly error budget will be exhausted in <2 days"

# Error Budget Burn Rate (slow burn)
- alert: SlowErrorBudgetBurn
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status!~"5.."}[24h]))
        /
        sum(rate(http_requests_total[24h]))
      )
    ) > (1 - 0.999) * 3  # 3x burn rate
  for: 1h
  labels:
    severity: warning
  annotations:
    summary: "Slow error budget burn detected"
    description: "At current rate, monthly error budget will be exhausted in <10 days"
```

---

## Dependencies and Requirements

### Docker/Docker Compose Stack

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.48.0
    ports: ["9090:9090"]
    volumes: [./prometheus:/etc/prometheus]

  grafana:
    image: grafana/grafana:10.2.0
    ports: ["3000:3000"]
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}

  loki:
    image: grafana/loki:2.9.0
    ports: ["3100:3100"]

  promtail:
    image: grafana/promtail:2.9.0
    volumes: [/var/log:/var/log:ro]

  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.91.0
    ports: ["4317:4317", "4318:4318"]  # OTLP gRPC and HTTP

  jaeger:
    image: jaegertracing/all-in-one:1.52
    ports: ["16686:16686", "14268:14268"]

  alertmanager:
    image: prom/alertmanager:v0.26.0
    ports: ["9093:9093"]
```

### Kubernetes Stack (Helm Charts)

```yaml
# kube-prometheus-stack (all-in-one)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install kube-prometheus prometheus-community/kube-prometheus-stack \
  --version 54.0.0 \
  --namespace observability \
  --create-namespace

# Loki
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack \
  --version 2.9.11 \
  --namespace observability

# OpenTelemetry Operator
helm install opentelemetry-operator open-telemetry/opentelemetry-operator \
  --version 0.44.0 \
  --namespace observability
```

### Instrumentation Libraries

```yaml
# Node.js
npm install --save \
  @opentelemetry/sdk-node \
  @opentelemetry/auto-instrumentations-node \
  @opentelemetry/exporter-metrics-otlp-http \
  @opentelemetry/exporter-trace-otlp-http \
  pino pino-pretty  # Structured logging

# Python
pip install \
  opentelemetry-distro \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation-flask \
  opentelemetry-instrumentation-requests \
  structlog  # Structured logging

# Go
go get go.opentelemetry.io/otel \
  go.opentelemetry.io/otel/sdk \
  go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp \
  go.uber.org/zap  # Structured logging

# Java (agent-based, no code changes)
# Download: https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases
# Run: java -javaagent:opentelemetry-javaagent.jar -jar app.jar
```

---

## Accessibility and Usability

### Grafana Dashboard Best Practices

- **Color-blind friendly palettes:** Use Grafana's built-in accessible color schemes
- **Clear panel titles:** Descriptive names (not "Panel 1")
- **Thresholds with icons:** Red/yellow/green with ✗/!/✓ icons
- **Annotations for context:** Mark deployments, incidents, config changes
- **Template variables:** Filter by service, environment, time range
- **Panel descriptions:** Hover tooltips explaining each metric

### Alert Message Templates

```yaml
# Good alert message (actionable)
summary: "API error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
description: |
  Service: {{ $labels.service }}
  Environment: {{ $labels.env }}
  Current error rate: {{ $value | humanizePercentage }}
  Threshold: 5%
  Runbook: https://runbook.example.com/high-error-rate
  Graph: https://grafana.example.com/d/xyz

# Bad alert message (vague)
summary: "Something is wrong"
description: "Check the dashboard"
```

---

## Performance and Cost Optimization

### Metrics Retention Strategy

```yaml
# Tier 1: High resolution (15s scrape interval)
retention: 15 days
storage: "Local SSD (Prometheus TSDB)"
cost: "~1GB per million samples"

# Tier 2: Downsampled (5m aggregation)
retention: 90 days
storage: "Remote storage (Thanos, Cortex, Mimir)"
cost: "~10GB per million samples (compressed)"

# Tier 3: Long-term (1h aggregation)
retention: 1 year
storage: "Object storage (S3, GCS)"
cost: "~1GB per million samples (highly compressed)"
```

### Log Volume Reduction

```yaml
# Production logging levels
levels:
  - DEBUG: disabled (only in development)
  - INFO: enabled (structured, sampled 10% for high-volume)
  - WARN: enabled (always logged)
  - ERROR: enabled (always logged + alerted)
  - FATAL: enabled (always logged + paged)

# Sampling strategy
high_volume_endpoints:
  - path: "/health"
    sample_rate: 0.01  # 1% sampling (otherwise floods logs)
  - path: "/metrics"
    sample_rate: 0  # Never log (called every 15s by Prometheus)

normal_endpoints:
  sample_rate: 1.0  # 100% logging
```

### Trace Sampling

```yaml
# Head-based sampling (at instrumentation)
default_sample_rate: 0.1  # 10% of all traces

# Always sample these:
always_sample:
  - status_code: "5xx"  # All errors
  - duration: ">1s"     # Slow requests
  - endpoint: "/checkout"  # Critical user journeys

# Never sample these:
never_sample:
  - endpoint: "/health"
  - endpoint: "/metrics"

# Tail-based sampling (at collector - advanced)
# Requires stateful collector (more complex)
# Samples based on complete trace analysis
```

---

## Security Considerations

### Authentication and Authorization

```yaml
# Grafana
- Enable SSO (OAuth, SAML, LDAP)
- Role-based access control (Viewer, Editor, Admin)
- API key rotation (30-day expiry)

# Prometheus
- Basic auth for /metrics endpoints
- Network policies (only Prometheus can scrape)
- Read-only query API for Grafana

# Jaeger
- OAuth proxy for UI access
- Backend encryption at rest
- TLS for trace data in transit
```

### Sensitive Data Handling

```yaml
# Scrub sensitive data from logs
patterns_to_redact:
  - credit_card: '\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}'
  - ssn: '\d{3}-\d{2}-\d{4}'
  - api_key: 'api_key=[a-zA-Z0-9]+'
  - password: 'password=[^&\s]+'

replacement: "[REDACTED]"

# Scrub from metrics labels
# Never use high-cardinality labels (user_id, request_id)
# Good: {service="api", method="POST", route="/users"}
# Bad: {service="api", user_id="12345", request_id="abc-def"}
```

---

## Testing and Validation

### Smoke Tests (run post-deployment)

```bash
#!/bin/bash
# scripts/validate-observability.sh

echo "Testing Prometheus..."
curl -f http://prometheus:9090/-/healthy || exit 1
curl -f http://prometheus:9090/api/v1/targets | jq '.data.activeTargets | length'

echo "Testing Grafana..."
curl -f http://grafana:3000/api/health || exit 1

echo "Testing Loki..."
curl -f http://loki:3100/ready || exit 1
curl -f http://loki:3100/metrics | grep loki_build_info

echo "Testing Jaeger..."
curl -f http://jaeger:16686/ || exit 1

echo "Testing OpenTelemetry Collector..."
curl -f http://otel-collector:13133/ || exit 1

echo "All systems operational!"
```

### Load Testing (verify instrumentation doesn't impact performance)

```yaml
# Expected overhead:
# - Metrics: <1% CPU, <50MB memory
# - Logs: <2% CPU, <100MB memory
# - Traces (10% sampling): <3% CPU, <100MB memory
# - Total overhead: <5% CPU, <200MB memory

# Test with hey, k6, or locust
# Before: Baseline latency and throughput
# After: With full instrumentation
# Acceptable degradation: <5% latency increase
```

---

## Migration and Rollout Strategy

### Phased Rollout

```yaml
Phase 1: Pilot (Week 1-2)
  - Deploy observability stack (Prometheus, Grafana, Loki)
  - Instrument 1-2 non-critical services
  - Validate metrics, logs, and dashboards
  - Tune scrape intervals and retention

Phase 2: Core Services (Week 3-4)
  - Instrument critical user-facing services
  - Enable distributed tracing (10% sampling)
  - Configure alerts (error rate, latency, uptime)
  - Integrate with PagerDuty/Slack

Phase 3: Full Rollout (Week 5-6)
  - Instrument all services
  - Enable SLO tracking
  - Train team on dashboards and runbooks
  - Document incident response procedures

Phase 4: Optimization (Week 7-8)
  - Review alert noise and tune thresholds
  - Optimize storage and retention policies
  - Add advanced features (anomaly detection, forecasting)
  - Conduct game day exercises
```

---

## Troubleshooting Common Issues

### Prometheus Not Scraping Targets

```yaml
Symptom: Targets show "DOWN" in Prometheus UI
Causes:
  - Network policy blocking Prometheus → service
  - Incorrect service discovery configuration
  - /metrics endpoint not exposed
  - Firewall rules

Debug:
  - Check Prometheus logs: docker logs prometheus
  - Test scraping manually: curl http://service:8080/metrics
  - Verify service discovery: kubectl get servicemonitors
  - Check Prometheus targets page: http://prometheus:9090/targets
```

### Logs Not Appearing in Loki

```yaml
Symptom: No logs in Grafana Explore
Causes:
  - Promtail/Fluent Bit not running
  - Incorrect log path configuration
  - Loki rejecting logs (schema mismatch)
  - Label cardinality too high

Debug:
  - Check Promtail logs: docker logs promtail
  - Verify Promtail is reading files: promtail_read_lines_total metric
  - Test Loki ingestion: curl http://loki:3100/loki/api/v1/push
  - Check Loki logs for errors: docker logs loki
```

### Traces Not Appearing in Jaeger

```yaml
Symptom: No traces in Jaeger UI
Causes:
  - OpenTelemetry Collector not receiving spans
  - Incorrect OTLP endpoint in application
  - Sampling rate too low (or zero)
  - Trace context not propagating across services

Debug:
  - Check OTel Collector logs: docker logs otel-collector
  - Verify OTLP receiver metrics: otelcol_receiver_accepted_spans
  - Test span export: otel-cli span test --endpoint http://collector:4317
  - Check trace context headers: W3C traceparent header present
```

---

## Runbook Templates

### High Error Rate Incident

```markdown
## High Error Rate Runbook

**Alert:** HighErrorRate
**Severity:** Critical
**SLO Impact:** Yes (error budget burn)

### 1. Acknowledge
- Acknowledge alert in PagerDuty
- Announce in #incidents Slack channel

### 2. Assess
- Check Grafana dashboard: https://grafana/d/golden-signals
- Identify affected service(s)
- Check recent deployments (last 1 hour)
- Review error logs in Loki: {service="api"} | json | level="ERROR"

### 3. Mitigate
- If recent deployment: Rollback immediately
- If capacity issue: Scale up service replicas
- If dependency issue: Enable circuit breaker

### 4. Communicate
- Update incident status every 15 minutes
- Notify stakeholders if customer-facing

### 5. Resolve
- Verify error rate returns to <1%
- Monitor for 15 minutes before closing
- Document root cause in incident report

### 6. Follow-up
- Schedule postmortem within 48 hours
- Implement preventative measures
- Update runbook with lessons learned
```

---

## Related Blueprints

- **Dashboard Blueprint:** For creating custom monitoring dashboards
- **Kubernetes Blueprint:** For k8s-specific observability setup
- **CI/CD Blueprint:** For integrating observability into pipelines
- **Security Blueprint:** For SIEM and security-focused logging

---

## Version History

**1.0.0** (2024-12-06)
- Initial observability blueprint
- 5-skill chain with optimized defaults
- 3-question quick configuration
- Open-source stack (Prometheus/Grafana/Loki) as default
- Comprehensive dashboards (Golden Signals, RED, USE)
- OpenTelemetry instrumentation examples
- SLO tracking and error budget monitoring
- Kubernetes integration support

---

## Deliverables Specification

This section defines concrete validation checks for blueprint promises, ensuring skills produce what users expect.

### Deliverables

```yaml
deliverables:
  "OpenTelemetry collector configuration":
    primary_skill: implementing-observability
    required_files:
      - observability/otel-collector-config.yml
    content_checks:
      - pattern: "receivers:|otlp:"
        in: observability/otel-collector-config.yml
      - pattern: "processors:|batch:|sampling:"
        in: observability/otel-collector-config.yml
      - pattern: "exporters:|jaeger:|prometheus:"
        in: observability/otel-collector-config.yml
    maturity_required: [starter, intermediate, advanced]

  "Prometheus configuration":
    primary_skill: implementing-observability
    required_files:
      - prometheus/prometheus.yml
    content_checks:
      - pattern: "global:|scrape_interval:"
        in: prometheus/prometheus.yml
      - pattern: "scrape_configs:|job_name:"
        in: prometheus/prometheus.yml
    maturity_required: [starter, intermediate, advanced]

  "Prometheus alert rules":
    primary_skill: implementing-observability
    required_files:
      - prometheus/alerts/application.rules.yml
      - prometheus/alerts/infrastructure.rules.yml
    content_checks:
      - pattern: "groups:|alert:|expr:"
        in: prometheus/alerts/
      - pattern: "HighErrorRate|HighLatency|ServiceDown"
        in: prometheus/alerts/application.rules.yml
      - pattern: "HighCPU|HighMemory|DiskSpaceLow"
        in: prometheus/alerts/infrastructure.rules.yml
    maturity_required: [intermediate, advanced]

  "SLO alert rules":
    primary_skill: implementing-observability
    required_files:
      - prometheus/alerts/slo.rules.yml
    content_checks:
      - pattern: "record:|expr:|labels:"
        in: prometheus/alerts/slo.rules.yml
      - pattern: "ErrorBudgetBurn|slo:|sli:"
        in: prometheus/alerts/slo.rules.yml
    maturity_required: [intermediate, advanced]

  "Grafana data source configuration":
    primary_skill: creating-dashboards
    required_files:
      - grafana/provisioning/datasources/prometheus.yml
      - grafana/provisioning/datasources/loki.yml
      - grafana/provisioning/datasources/jaeger.yml
    content_checks:
      - pattern: "apiVersion:|datasources:|type: prometheus"
        in: grafana/provisioning/datasources/prometheus.yml
      - pattern: "type: loki"
        in: grafana/provisioning/datasources/loki.yml
      - pattern: "type: jaeger"
        in: grafana/provisioning/datasources/jaeger.yml
    maturity_required: [starter, intermediate, advanced]

  "Golden Signals dashboard":
    primary_skill: creating-dashboards
    required_files:
      - grafana/provisioning/dashboards/dashboards/golden-signals.json
    content_checks:
      - pattern: '"title".*Latency|"title".*Traffic|"title".*Errors|"title".*Saturation'
        in: grafana/provisioning/dashboards/dashboards/golden-signals.json
      - pattern: '"type":\\s*"graph"|"type":\\s*"gauge"'
        in: grafana/provisioning/dashboards/dashboards/golden-signals.json
    maturity_required: [starter, intermediate, advanced]

  "RED method dashboard":
    primary_skill: creating-dashboards
    required_files:
      - grafana/provisioning/dashboards/dashboards/red-method.json
    content_checks:
      - pattern: '"title".*Rate|"title".*Errors|"title".*Duration'
        in: grafana/provisioning/dashboards/dashboards/red-method.json
      - pattern: 'histogram_quantile|rate\\(http_requests'
        in: grafana/provisioning/dashboards/dashboards/red-method.json
    maturity_required: [intermediate, advanced]

  "USE method dashboard":
    primary_skill: creating-dashboards
    required_files:
      - grafana/provisioning/dashboards/dashboards/use-method.json
    content_checks:
      - pattern: '"title".*Utilization|"title".*Saturation|"title".*Errors'
        in: grafana/provisioning/dashboards/dashboards/use-method.json
      - pattern: 'node_cpu|node_memory|node_load'
        in: grafana/provisioning/dashboards/dashboards/use-method.json
    maturity_required: [intermediate, advanced]

  "SLO tracking dashboard":
    primary_skill: creating-dashboards
    required_files:
      - grafana/provisioning/dashboards/dashboards/slo-tracking.json
    content_checks:
      - pattern: '"title".*SLI|"title".*Error Budget|"title".*Burn Rate'
        in: grafana/provisioning/dashboards/dashboards/slo-tracking.json
      - pattern: 'slo:|error_budget|burn_rate'
        in: grafana/provisioning/dashboards/dashboards/slo-tracking.json
    maturity_required: [intermediate, advanced]

  "Loki configuration":
    primary_skill: implementing-siem
    required_files:
      - loki/loki-config.yml
    content_checks:
      - pattern: "auth_enabled:|server:|ingester:"
        in: loki/loki-config.yml
      - pattern: "schema_config:|storage_config:"
        in: loki/loki-config.yml
    maturity_required: [intermediate, advanced]

  "Promtail configuration":
    primary_skill: implementing-siem
    required_files:
      - loki/promtail/promtail-config.yml
    content_checks:
      - pattern: "server:|positions:|clients:"
        in: loki/promtail/promtail-config.yml
      - pattern: "scrape_configs:|job_name:"
        in: loki/promtail/promtail-config.yml
    maturity_required: [intermediate, advanced]

  "Log parsing rules":
    primary_skill: implementing-siem
    required_files:
      - loki/promtail/promtail-config.yml
    content_checks:
      - pattern: "pipeline_stages:|json:|regex:|labels:"
        in: loki/promtail/promtail-config.yml
    maturity_required: [intermediate, advanced]

  "Jaeger configuration":
    primary_skill: implementing-observability
    required_files:
      - jaeger/jaeger-config.yml
    content_checks:
      - pattern: "span-storage-type:|collector:|query:"
        in: jaeger/jaeger-config.yml
    maturity_required: [starter, intermediate, advanced]

  "OpenTelemetry instrumentation (Node.js)":
    primary_skill: implementing-observability
    required_files:
      - opentelemetry/instrumentation/javascript/tracing.js
    content_checks:
      - pattern: "@opentelemetry/sdk-node|NodeSDK"
        in: opentelemetry/instrumentation/javascript/tracing.js
      - pattern: "auto-instrumentations|trace|metrics"
        in: opentelemetry/instrumentation/javascript/tracing.js
    maturity_required: [starter, intermediate, advanced]

  "OpenTelemetry instrumentation (Python)":
    primary_skill: implementing-observability
    required_files:
      - opentelemetry/instrumentation/python/tracing.py
    content_checks:
      - pattern: "from opentelemetry|import.*opentelemetry"
        in: opentelemetry/instrumentation/python/tracing.py
      - pattern: "TracerProvider|MeterProvider|OTLPSpanExporter"
        in: opentelemetry/instrumentation/python/tracing.py
    maturity_required: [starter, intermediate, advanced]

  "Alertmanager configuration":
    primary_skill: implementing-observability
    required_files:
      - alertmanager/alertmanager.yml
    content_checks:
      - pattern: "route:|receivers:|inhibit_rules:"
        in: alertmanager/alertmanager.yml
      - pattern: "slack_configs|pagerduty_configs|email_configs"
        in: alertmanager/alertmanager.yml
    maturity_required: [intermediate, advanced]

  "Alert notification templates":
    primary_skill: implementing-observability
    required_files:
      - alertmanager/templates/slack.tmpl
    content_checks:
      - pattern: "{{.*}}|{{\\s*range|{{\\s*if"
        in: alertmanager/templates/slack.tmpl
      - pattern: "Status:|Alert:|Description:"
        in: alertmanager/templates/slack.tmpl
    maturity_required: [intermediate, advanced]

  "Docker Compose deployment":
    primary_skill: implementing-observability
    required_files:
      - docker-compose.yml
    content_checks:
      - pattern: "services:|prometheus:|grafana:|loki:"
        in: docker-compose.yml
      - pattern: "image:|ports:|volumes:"
        in: docker-compose.yml
    maturity_required: [starter]

  "Kubernetes namespace":
    primary_skill: configuring-kubernetes
    required_files:
      - kubernetes/namespace.yml
    content_checks:
      - pattern: "kind: Namespace"
        in: kubernetes/namespace.yml
      - pattern: "name: observability"
        in: kubernetes/namespace.yml
    maturity_required: [intermediate, advanced]

  "Prometheus Operator":
    primary_skill: configuring-kubernetes
    required_files:
      - kubernetes/prometheus/prometheus-operator.yml
      - kubernetes/prometheus/prometheus.yml
    content_checks:
      - pattern: "kind: Prometheus"
        in: kubernetes/prometheus/prometheus.yml
      - pattern: "serviceMonitorSelector:|ruleSelector:"
        in: kubernetes/prometheus/prometheus.yml
    maturity_required: [intermediate, advanced]

  "ServiceMonitor CRDs":
    primary_skill: configuring-kubernetes
    required_files:
      - kubernetes/prometheus/servicemonitor.yml
    content_checks:
      - pattern: "kind: ServiceMonitor"
        in: kubernetes/prometheus/servicemonitor.yml
      - pattern: "endpoints:|port:|path:"
        in: kubernetes/prometheus/servicemonitor.yml
    maturity_required: [intermediate, advanced]

  "Grafana Kubernetes deployment":
    primary_skill: configuring-kubernetes
    required_files:
      - kubernetes/grafana/deployment.yml
      - kubernetes/grafana/service.yml
    content_checks:
      - pattern: "kind: Deployment"
        in: kubernetes/grafana/deployment.yml
      - pattern: "kind: Service"
        in: kubernetes/grafana/service.yml
      - pattern: "grafana/grafana"
        in: kubernetes/grafana/deployment.yml
    maturity_required: [intermediate, advanced]

  "Loki StatefulSet":
    primary_skill: configuring-kubernetes
    required_files:
      - kubernetes/loki/statefulset.yml
    content_checks:
      - pattern: "kind: StatefulSet"
        in: kubernetes/loki/statefulset.yml
      - pattern: "grafana/loki"
        in: kubernetes/loki/statefulset.yml
    maturity_required: [advanced]

  "Fluent Bit DaemonSet":
    primary_skill: configuring-kubernetes
    required_files:
      - kubernetes/loki/fluent-bit-daemonset.yml
    content_checks:
      - pattern: "kind: DaemonSet"
        in: kubernetes/loki/fluent-bit-daemonset.yml
      - pattern: "fluent/fluent-bit"
        in: kubernetes/loki/fluent-bit-daemonset.yml
    maturity_required: [advanced]

  "OpenTelemetry Collector deployment":
    primary_skill: configuring-kubernetes
    required_files:
      - kubernetes/opentelemetry/collector-deployment.yml
      - kubernetes/opentelemetry/collector-configmap.yml
    content_checks:
      - pattern: "kind: Deployment|kind: ConfigMap"
        in: kubernetes/opentelemetry/
      - pattern: "otel/opentelemetry-collector"
        in: kubernetes/opentelemetry/collector-deployment.yml
    maturity_required: [intermediate, advanced]

  "CI/CD observability checks":
    primary_skill: building-ci-pipelines
    required_files:
      - ci-cd/github-actions/observability-checks.yml
    content_checks:
      - pattern: "on:|push:|pull_request:"
        in: ci-cd/github-actions/observability-checks.yml
      - pattern: "curl.*metrics|curl.*health"
        in: ci-cd/github-actions/observability-checks.yml
    maturity_required: [intermediate, advanced]

  "Metrics validation script":
    primary_skill: building-ci-pipelines
    required_files:
      - scripts/validate-metrics.sh
    content_checks:
      - pattern: "#!/bin/bash|curl.*prometheus"
        in: scripts/validate-metrics.sh
      - pattern: "activeTargets|up==1"
        in: scripts/validate-metrics.sh
    maturity_required: [intermediate, advanced]

  "Logs validation script":
    primary_skill: building-ci-pipelines
    required_files:
      - scripts/validate-logs.sh
    content_checks:
      - pattern: "#!/bin/bash|curl.*loki"
        in: scripts/validate-logs.sh
      - pattern: "ready|/metrics"
        in: scripts/validate-logs.sh
    maturity_required: [intermediate, advanced]

  "Traces validation script":
    primary_skill: building-ci-pipelines
    required_files:
      - scripts/validate-traces.sh
    content_checks:
      - pattern: "#!/bin/bash|curl.*jaeger"
        in: scripts/validate-traces.sh
      - pattern: "16686|/api/services"
        in: scripts/validate-traces.sh
    maturity_required: [intermediate, advanced]

  "Sample instrumented application":
    primary_skill: implementing-observability
    required_files:
      - examples/sample-app/app.py
    content_checks:
      - pattern: "import.*opentelemetry|from opentelemetry"
        in: examples/sample-app/app.py
      - pattern: "/metrics|prometheus|@app"
        in: examples/sample-app/app.py
    maturity_required: [starter]

  "PromQL query examples":
    primary_skill: implementing-observability
    required_files:
      - examples/queries/promql-examples.md
    content_checks:
      - pattern: "rate\\(|histogram_quantile|sum by"
        in: examples/queries/promql-examples.md
      - pattern: "http_requests_total|http_request_duration"
        in: examples/queries/promql-examples.md
    maturity_required: [starter, intermediate, advanced]

  "LogQL query examples":
    primary_skill: implementing-siem
    required_files:
      - examples/queries/logql-examples.md
    content_checks:
      - pattern: "\\{service=|\\|=|\\| json"
        in: examples/queries/logql-examples.md
      - pattern: "level=|rate\\(\\{|sum by"
        in: examples/queries/logql-examples.md
    maturity_required: [intermediate, advanced]

  "Setup documentation":
    primary_skill: implementing-observability
    required_files:
      - docs/SETUP.md
    content_checks:
      - pattern: "##|###|Step|Prerequisites"
        in: docs/SETUP.md
      - pattern: "docker-compose up|kubectl apply|helm install"
        in: docs/SETUP.md
    maturity_required: [starter, intermediate, advanced]

  "Architecture documentation":
    primary_skill: implementing-observability
    required_files:
      - docs/ARCHITECTURE.md
    content_checks:
      - pattern: "##|###|Component|Architecture"
        in: docs/ARCHITECTURE.md
      - pattern: "Prometheus|Grafana|Loki|OpenTelemetry"
        in: docs/ARCHITECTURE.md
    maturity_required: [intermediate, advanced]

  "Runbook documentation":
    primary_skill: implementing-observability
    required_files:
      - docs/RUNBOOK.md
    content_checks:
      - pattern: "##|###|Alert:|Incident|Runbook"
        in: docs/RUNBOOK.md
      - pattern: "HighErrorRate|HighLatency|Acknowledge|Mitigate"
        in: docs/RUNBOOK.md
    maturity_required: [intermediate, advanced]
```

### Maturity Profiles

```yaml
maturity_profiles:
  starter:
    description: "Learning-focused observability with Docker Compose, basic dashboards, and getting started guides"

    require_additionally:
      - "OpenTelemetry collector configuration"
      - "Prometheus configuration"
      - "Grafana data source configuration"
      - "Golden Signals dashboard"
      - "Jaeger configuration"
      - "OpenTelemetry instrumentation (Node.js)"
      - "OpenTelemetry instrumentation (Python)"
      - "Docker Compose deployment"
      - "Sample instrumented application"
      - "PromQL query examples"
      - "Setup documentation"

    skip_deliverables:
      - "Prometheus alert rules"
      - "SLO alert rules"
      - "RED method dashboard"
      - "USE method dashboard"
      - "SLO tracking dashboard"
      - "Loki configuration"
      - "Promtail configuration"
      - "Log parsing rules"
      - "Alertmanager configuration"
      - "Alert notification templates"
      - "Kubernetes namespace"
      - "Prometheus Operator"
      - "ServiceMonitor CRDs"
      - "Grafana Kubernetes deployment"
      - "Loki StatefulSet"
      - "Fluent Bit DaemonSet"
      - "OpenTelemetry Collector deployment"
      - "CI/CD observability checks"
      - "Metrics validation script"
      - "Logs validation script"
      - "Traces validation script"
      - "LogQL query examples"
      - "Architecture documentation"
      - "Runbook documentation"

    empty_dirs_allowed:
      - kubernetes/
      - prometheus/alerts/
      - loki/
      - alertmanager/
      - ci-cd/
      - monitoring/grafana/dashboards/advanced/

    generation_adjustments:
      - Use Docker Compose for all components (not Kubernetes)
      - Include comprehensive inline comments
      - Provide pre-configured docker-compose.yml with all services
      - Include working sample application with instrumentation
      - Add step-by-step setup guide in README
      - Focus on single-host deployment
      - Use all-in-one Jaeger (not distributed)
      - Skip advanced alerting and SLO tracking

  intermediate:
    description: "Production-ready observability with LGTM stack, alerting, SLO tracking, and Kubernetes support"

    require_additionally:
      - "OpenTelemetry collector configuration"
      - "Prometheus configuration"
      - "Prometheus alert rules"
      - "SLO alert rules"
      - "Grafana data source configuration"
      - "Golden Signals dashboard"
      - "RED method dashboard"
      - "USE method dashboard"
      - "SLO tracking dashboard"
      - "Loki configuration"
      - "Promtail configuration"
      - "Log parsing rules"
      - "Jaeger configuration"
      - "OpenTelemetry instrumentation (Node.js)"
      - "OpenTelemetry instrumentation (Python)"
      - "Alertmanager configuration"
      - "Alert notification templates"
      - "Kubernetes namespace"
      - "Prometheus Operator"
      - "ServiceMonitor CRDs"
      - "Grafana Kubernetes deployment"
      - "OpenTelemetry Collector deployment"
      - "CI/CD observability checks"
      - "Metrics validation script"
      - "Logs validation script"
      - "Traces validation script"
      - "PromQL query examples"
      - "LogQL query examples"
      - "Setup documentation"
      - "Architecture documentation"
      - "Runbook documentation"

    skip_deliverables:
      - "Docker Compose deployment"
      - "Sample instrumented application"
      - "Loki StatefulSet"
      - "Fluent Bit DaemonSet"

    empty_dirs_allowed:
      - examples/sample-app/

    generation_adjustments:
      - Use Kubernetes for orchestration
      - Include Prometheus Operator for dynamic discovery
      - Configure LGTM stack (Loki, Grafana, Tempo, Mimir)
      - Add comprehensive alert rules and SLO tracking
      - Include Alertmanager with Slack/PagerDuty integration
      - Provide CI/CD pipeline integration
      - Add validation scripts for smoke testing
      - Include runbooks for common incidents
      - Use distributed Jaeger (not all-in-one)

  advanced:
    description: "Enterprise-scale observability with distributed LGTM stack, advanced SLOs, comprehensive testing, and multi-cluster support"

    require_additionally:
      - "OpenTelemetry collector configuration"
      - "Prometheus configuration"
      - "Prometheus alert rules"
      - "SLO alert rules"
      - "Grafana data source configuration"
      - "Golden Signals dashboard"
      - "RED method dashboard"
      - "USE method dashboard"
      - "SLO tracking dashboard"
      - "Loki configuration"
      - "Promtail configuration"
      - "Log parsing rules"
      - "Jaeger configuration"
      - "OpenTelemetry instrumentation (Node.js)"
      - "OpenTelemetry instrumentation (Python)"
      - "Alertmanager configuration"
      - "Alert notification templates"
      - "Kubernetes namespace"
      - "Prometheus Operator"
      - "ServiceMonitor CRDs"
      - "Grafana Kubernetes deployment"
      - "Loki StatefulSet"
      - "Fluent Bit DaemonSet"
      - "OpenTelemetry Collector deployment"
      - "CI/CD observability checks"
      - "Metrics validation script"
      - "Logs validation script"
      - "Traces validation script"
      - "PromQL query examples"
      - "LogQL query examples"
      - "Setup documentation"
      - "Architecture documentation"
      - "Runbook documentation"

    skip_deliverables:
      - "Docker Compose deployment"
      - "Sample instrumented application"

    empty_dirs_allowed: []

    generation_adjustments:
      - Use distributed LGTM stack (Loki, Grafana, Tempo, Mimir)
      - Deploy Loki as StatefulSet with S3/GCS backend
      - Configure Tempo for distributed tracing at scale
      - Use Mimir for long-term metrics storage
      - Add multi-burn rate SLO alerts
      - Include advanced dashboards with anomaly detection
      - Configure high availability for all components
      - Add Fluent Bit DaemonSet for log collection
      - Include federation for multi-cluster monitoring
      - Add comprehensive integration tests
      - Configure retention policies and downsampling
      - Include cost optimization strategies
```

### Validation Process

After all skills complete, the skillchain orchestrator validates deliverables:

1. **File existence checks**: Verify all required_files exist for the selected maturity level
2. **Content validation**: Run regex pattern checks against file contents
3. **Structural checks**: Ensure proper YAML/JSON syntax for configuration files
4. **Integration validation**: Verify service connectivity (Prometheus can reach exporters, Grafana can query Prometheus/Loki/Tempo)
5. **Smoke tests**: Run validation scripts (validate-metrics.sh, validate-logs.sh, validate-traces.sh)

**Success criteria:**
- All required deliverables present
- All content_checks pass
- No errors in configuration file syntax
- Services can communicate (for intermediate/advanced)

**Failure handling:**
- Report missing deliverables with skill attribution
- Show which content_checks failed and in which files
- Provide remediation suggestions
- Optionally re-run failed skill with corrected parameters

---

**Blueprint Complete**
