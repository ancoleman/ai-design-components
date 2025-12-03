# Alerting Rules and Notification Patterns

Complete guide for creating alerting rules in Prometheus, Loki, and Grafana with notification routing.

## Table of Contents

- [Alerting Architecture](#alerting-architecture)
- [Prometheus Alert Rules](#prometheus-alert-rules)
- [Loki Alert Rules](#loki-alert-rules)
- [Grafana Alerting](#grafana-alerting)
- [Notification Channels](#notification-channels)
- [Best Practices](#best-practices)

---

## Alerting Architecture

```
┌────────────────────────────────────────────────────────┐
│                 Alerting Data Flow                      │
├────────────────────────────────────────────────────────┤
│                                                         │
│  Metrics/Logs Sources                                   │
│  ├── Prometheus (metrics)                               │
│  ├── Loki (logs)                                        │
│  └── Tempo (traces - no native alerting)               │
│           │                                             │
│           ▼                                             │
│  ┌─────────────────────┐                               │
│  │   Alert Rules       │                               │
│  │  (PromQL/LogQL)     │                               │
│  └──────────┬──────────┘                               │
│             │                                           │
│             ▼                                           │
│  ┌─────────────────────┐                               │
│  │  Alertmanager /     │                               │
│  │  Grafana Alerting   │                               │
│  └──────────┬──────────┘                               │
│             │                                           │
│             ├──────────┬────────────┬──────────┐       │
│             ▼          ▼            ▼          ▼       │
│         Slack    PagerDuty    Email     Webhook        │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## Prometheus Alert Rules

### Rule File Format

**alerts.yaml**:

```yaml
groups:
  - name: http_alerts
    interval: 30s  # Evaluation interval
    rules:
      - alert: HighHTTPErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          ) > 0.05
        for: 5m  # Alert fires after condition is true for 5 minutes
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High HTTP error rate on {{ $labels.service }}"
          description: |
            Service {{ $labels.service }} has {{ $value | humanizePercentage }} error rate.
            Current error rate: {{ $value | humanize }}
          runbook_url: "https://wiki.example.com/runbooks/high-error-rate"
```

### Common Metric Alerts

#### 1. High Error Rate

```yaml
- alert: HighHTTPErrorRate
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
    ) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "{{ $labels.service }} error rate above 5%"
```

#### 2. High Latency (P95)

```yaml
- alert: HighP95Latency
  expr: |
    histogram_quantile(0.95,
      rate(http_request_duration_seconds_bucket[5m])
    ) > 0.5
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "P95 latency above 500ms on {{ $labels.service }}"
    description: "Current P95: {{ $value }}s"
```

#### 3. High Memory Usage

```yaml
- alert: HighMemoryUsage
  expr: |
    (
      container_memory_usage_bytes{container!=""}
      /
      container_spec_memory_limit_bytes{container!=""}
    ) > 0.9
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Container {{ $labels.container }} memory usage above 90%"
```

#### 4. High CPU Usage

```yaml
- alert: HighCPUUsage
  expr: |
    rate(container_cpu_usage_seconds_total{container!=""}[5m]) > 0.8
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Container {{ $labels.container }} CPU usage above 80%"
```

#### 5. Service Down (No Metrics)

```yaml
- alert: ServiceDown
  expr: |
    up{job="my-service"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Service {{ $labels.job }} is down"
    description: "No metrics received from {{ $labels.instance }}"
```

#### 6. High Request Rate

```yaml
- alert: HighRequestRate
  expr: |
    sum(rate(http_requests_total[1m])) by (service) > 1000
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High request rate on {{ $labels.service }}"
    description: "Current rate: {{ $value }} req/s"
```

#### 7. Disk Usage

```yaml
- alert: HighDiskUsage
  expr: |
    (
      node_filesystem_avail_bytes{mountpoint="/"}
      /
      node_filesystem_size_bytes{mountpoint="/"}
    ) < 0.1
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Disk usage above 90% on {{ $labels.instance }}"
```

---

## Loki Alert Rules

### Rule File Format

**loki-alerts.yaml**:

```yaml
groups:
  - name: log_alerts
    interval: 1m
    rules:
      - alert: HighLogErrorRate
        expr: |
          sum(rate({job="api-service"} | json | level="error" [5m])) by (service)
          /
          sum(rate({job="api-service"}[5m])) by (service)
          > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error log rate for {{ $labels.service }}"
          description: "{{ $value | humanizePercentage }} of logs are errors"
```

### Common Log Alerts

#### 1. Error Log Spike

```yaml
- alert: ErrorLogSpike
  expr: |
    sum(rate({job=~".+"} | json | level="error" [5m])) by (service)
    > 10
  for: 2m
  labels:
    severity: warning
  annotations:
    summary: "Error log spike on {{ $labels.service }}"
    description: "{{ $value }} errors/second"
```

#### 2. Application Crash Detected

```yaml
- alert: ApplicationCrashDetected
  expr: |
    sum(count_over_time({job=~".+"} |~ "(?i)(panic|fatal|crashed|exception)" [1m])) by (service)
    > 0
  for: 0m  # Immediate alert
  labels:
    severity: critical
  annotations:
    summary: "Application crash detected on {{ $labels.service }}"
```

#### 3. Authentication Failures

```yaml
- alert: HighAuthFailureRate
  expr: |
    sum(rate({job="auth-service"} | json | message="authentication_failed" [5m]))
    > 5
  for: 3m
  labels:
    severity: warning
  annotations:
    summary: "High authentication failure rate"
    description: "{{ $value }} failed auth attempts per second"
```

#### 4. Slow Query Logs

```yaml
- alert: SlowQueriesDetected
  expr: |
    sum(count_over_time({job="api-service"} | json | duration_ms > 1000 [5m]))
    > 10
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Slow queries detected on {{ $labels.service }}"
```

#### 5. Database Connection Errors

```yaml
- alert: DatabaseConnectionErrors
  expr: |
    sum(rate({job=~".+"} |~ "(?i)(connection refused|connection timeout|database unavailable)" [5m]))
    > 1
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Database connection errors on {{ $labels.service }}"
```

---

## Grafana Alerting

### Contact Points

**Slack Integration**:

```yaml
apiVersion: 1
contactPoints:
  - orgId: 1
    name: slack-critical
    receivers:
      - uid: slack-critical
        type: slack
        settings:
          url: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
          recipient: '#alerts-critical'
          username: Grafana
          text: |
            {{ range .Alerts }}
            *Alert:* {{ .Labels.alertname }}
            *Severity:* {{ .Labels.severity }}
            *Summary:* {{ .Annotations.summary }}
            *Description:* {{ .Annotations.description }}
            {{ end }}
```

**Email Integration**:

```yaml
- name: email-team
  receivers:
    - uid: email-team
      type: email
      settings:
        addresses: team@example.com
        subject: "[{{ .Status }}] {{ .Labels.alertname }}"
```

**PagerDuty Integration**:

```yaml
- name: pagerduty-oncall
  receivers:
    - uid: pagerduty
      type: pagerduty
      settings:
        integrationKey: YOUR_INTEGRATION_KEY
        severity: critical
```

**Webhook Integration**:

```yaml
- name: custom-webhook
  receivers:
    - uid: webhook
      type: webhook
      settings:
        url: https://api.example.com/alerts
        httpMethod: POST
```

### Notification Policies

```yaml
apiVersion: 1
policies:
  - orgId: 1
    receiver: default-email
    group_by: ['alertname', 'service']
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
      - receiver: slack-critical
        matchers:
          - severity = critical
        continue: true
        group_wait: 10s
        repeat_interval: 1h

      - receiver: pagerduty-oncall
        matchers:
          - severity = critical
          - team = backend
        continue: false

      - receiver: email-team
        matchers:
          - severity = warning
        repeat_interval: 12h
```

### Alert Rule (Grafana UI Format)

```yaml
apiVersion: 1
groups:
  - orgId: 1
    name: performance_alerts
    folder: Production
    interval: 1m
    rules:
      - uid: high_p99_latency
        title: High P99 Latency
        condition: C
        data:
          - refId: A
            datasourceUid: mimir
            model:
              expr: |
                histogram_quantile(0.99,
                  rate(http_request_duration_seconds_bucket[5m])
                )
              range: true
              intervalMs: 1000

          - refId: B
            datasourceUid: __expr__
            model:
              type: reduce
              expression: A
              reducer: last

          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              expression: B
              conditions:
                - evaluator:
                    params: [1.0]
                    type: gt

        noDataState: NoData
        execErrState: Error
        for: 5m
        annotations:
          summary: P99 latency above 1 second
        labels:
          severity: warning
```

---

## Notification Channels

### Slack Message Template

```json
{
  "channel": "#alerts",
  "username": "Grafana",
  "icon_emoji": ":warning:",
  "attachments": [
    {
      "color": "{{ if eq .Status \"firing\" }}danger{{ else }}good{{ end }}",
      "title": "{{ .Labels.alertname }}",
      "text": "{{ .Annotations.summary }}",
      "fields": [
        {
          "title": "Service",
          "value": "{{ .Labels.service }}",
          "short": true
        },
        {
          "title": "Severity",
          "value": "{{ .Labels.severity }}",
          "short": true
        },
        {
          "title": "Description",
          "value": "{{ .Annotations.description }}",
          "short": false
        }
      ],
      "footer": "Grafana",
      "footer_icon": "https://grafana.com/static/img/about/grafana_icon.svg",
      "ts": {{ .StartsAt.Unix }}
    }
  ]
}
```

### Email Template

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .alert { padding: 20px; border-left: 5px solid #f44336; }
    .warning { border-left-color: #ff9800; }
    .resolved { border-left-color: #4caf50; }
  </style>
</head>
<body>
  <div class="alert {{ .Status }}">
    <h2>{{ .Labels.alertname }}</h2>
    <p><strong>Status:</strong> {{ .Status }}</p>
    <p><strong>Severity:</strong> {{ .Labels.severity }}</p>
    <p><strong>Summary:</strong> {{ .Annotations.summary }}</p>
    <p><strong>Description:</strong> {{ .Annotations.description }}</p>
    <p><strong>Started:</strong> {{ .StartsAt }}</p>
    {{ if .EndsAt }}
    <p><strong>Ended:</strong> {{ .EndsAt }}</p>
    {{ end }}
  </div>
</body>
</html>
```

### PagerDuty Payload

```json
{
  "routing_key": "YOUR_INTEGRATION_KEY",
  "event_action": "{{ if eq .Status \"firing\" }}trigger{{ else }}resolve{{ end }}",
  "dedup_key": "{{ .GroupLabels.alertname }}-{{ .GroupLabels.service }}",
  "payload": {
    "summary": "{{ .Annotations.summary }}",
    "source": "{{ .Labels.instance }}",
    "severity": "{{ .Labels.severity }}",
    "custom_details": {
      "alert_name": "{{ .Labels.alertname }}",
      "service": "{{ .Labels.service }}",
      "description": "{{ .Annotations.description }}",
      "runbook_url": "{{ .Annotations.runbook_url }}"
    }
  }
}
```

---

## Best Practices

### 1. Alert Severity Levels

```
CRITICAL: Service down, data loss, security breach
  - Page on-call engineer immediately
  - Example: 100% error rate, database unavailable

WARNING: Degraded performance, high resource usage
  - Notify during business hours
  - Example: High latency, 80% CPU

INFO: Informational events
  - Log only, no notification
  - Example: Deployment completed, scaling event
```

### 2. Alert Naming Convention

```
[Component][Metric][Condition]

Good:
- APIHighErrorRate
- DatabaseHighLatency
- CacheMemoryExhausted

Bad:
- Alert1
- Problem
- IssueDetected
```

### 3. Alert Grouping

**Group related alerts**:

```yaml
group_by: ['alertname', 'service', 'region']
group_wait: 30s       # Wait to batch initial alerts
group_interval: 5m    # Wait before sending additional grouped alerts
repeat_interval: 4h   # Resend if still firing
```

### 4. Runbook Links

**Always include runbook URL**:

```yaml
annotations:
  runbook_url: "https://wiki.example.com/runbooks/{{ $labels.alertname }}"
```

### 5. Alert Inhibition

**Suppress dependent alerts**:

```yaml
inhibit_rules:
  - source_match:
      severity: critical
      alertname: ServiceDown
    target_match:
      severity: warning
    equal: ['service', 'instance']
# If service is down, don't alert on high latency/errors
```

### 6. Alert Thresholds

**Use appropriate thresholds**:

```yaml
# Error rate: > 5% for 5 minutes
# Latency: P95 > 500ms for 10 minutes
# Memory: > 90% for 5 minutes
# CPU: > 80% for 10 minutes
```

**Avoid flapping**:
- Use `for: <duration>` to require sustained condition
- Set reasonable repeat intervals
- Use hysteresis (different thresholds for firing vs resolving)

### 7. Alert Fatigue Prevention

**Reduce noise**:
- Start with higher thresholds, tune down based on false positives
- Use alert inhibition for cascading failures
- Group related alerts
- Set appropriate repeat intervals
- Auto-resolve when condition clears

---

## Testing Alerts

### Test Prometheus Alert

**Create test metric**:

```bash
# Send high error rate
curl -X POST http://localhost:9090/api/v1/admin/tsdb/delete_series \
  -d 'match[]={__name__="http_requests_total"}'

# Push test metrics
cat <<EOF | curl --data-binary @- http://localhost:9091/metrics/job/test
http_requests_total{status="500"} 100
http_requests_total{status="200"} 10
EOF
```

**Verify alert fires**:

```bash
# Check pending/firing alerts
curl http://localhost:9090/api/v1/alerts | jq .
```

### Test Loki Alert

**Generate error logs**:

```bash
# Send error logs to Loki
curl -X POST http://localhost:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  -d '{
    "streams": [{
      "stream": {"job": "test-service", "level": "error"},
      "values": [
        ["'$(date +%s%N)'", "error: test alert"]
      ]
    }]
  }'
```

### Test Notification

**Test Slack webhook**:

```bash
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Test alert from Grafana",
    "attachments": [{
      "color": "danger",
      "title": "Test Alert",
      "text": "This is a test notification"
    }]
  }'
```

---

## Auto-Generated Alerts

**Use script to generate alerts**:

```bash
python scripts/generate_dashboards.py --alerts \
  --metrics http_request_duration_seconds \
  --thresholds p95:0.5,p99:1.0 \
  --output alerts.yaml
```

**Generated output**:

```yaml
groups:
  - name: http_request_duration_seconds_alerts
    rules:
      - alert: HighP95Latency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency above 500ms"

      - alert: HighP99Latency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "P99 latency above 1s"
```

---

## Troubleshooting

**Alerts not firing**:
- Check PromQL/LogQL query returns data
- Verify `for:` duration hasn't been met yet
- Check alert rule evaluation interval
- Verify data source is connected

**Notifications not sent**:
- Test webhook URL manually
- Check notification policy routing
- Verify contact point configuration
- Check Alertmanager/Grafana logs

**Too many alerts (alert fatigue)**:
- Increase thresholds
- Add inhibit rules
- Increase repeat interval
- Group related alerts
- Use more specific matchers
