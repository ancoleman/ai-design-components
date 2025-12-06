# LGTM Stack Deployment Guide

Complete guide for deploying the LGTM stack (Loki, Grafana, Tempo, Mimir) in Docker Compose and Kubernetes.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Docker Compose (Development)](#docker-compose-development)
- [Kubernetes (Production)](#kubernetes-production)
- [Grafana Configuration](#grafana-configuration)
- [Scaling Considerations](#scaling-considerations)

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                      LGTM Stack Flow                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Application                                                    │
│  ├── OpenTelemetry SDK                                          │
│  └── Exports OTLP (gRPC port 4317 or HTTP port 4318)           │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────┐                                       │
│  │   Grafana Alloy     │  (Unified Collector)                  │
│  │  Receives: OTLP     │                                        │
│  │  Exports to:        │                                        │
│  │  ├─ Loki (logs)     │                                        │
│  │  ├─ Tempo (traces)  │                                        │
│  │  └─ Mimir (metrics) │                                        │
│  └─────────────────────┘                                       │
│           │                                                     │
│           ├────────────────┬──────────────────┐                │
│           ▼                ▼                  ▼                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │     Loki     │  │    Tempo     │  │    Mimir     │         │
│  │   (Logs)     │  │  (Traces)    │  │  (Metrics)   │         │
│  │  Port 3100   │  │  Port 3200   │  │  Port 9009   │         │
│  │  Storage:    │  │  Storage:    │  │  Storage:    │         │
│  │  Object/FS   │  │  Object/FS   │  │  Object/FS   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │                 │
│         └─────────────────┴──────────────────┘                 │
│                           │                                    │
│                  ┌────────▼────────┐                           │
│                  │     Grafana     │                           │
│                  │  Port 3000      │                           │
│                  │  Datasources:   │                           │
│                  │  ├─ Loki        │                           │
│                  │  ├─ Tempo       │                           │
│                  │  └─ Mimir       │                           │
│                  └─────────────────┘                           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Docker Compose (Development)

### Complete Stack (see examples/lgtm-docker-compose/)

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  # Grafana - Visualization
  grafana:
    image: grafana/grafana:10.2.3
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana/datasources.yaml:/etc/grafana/provisioning/datasources/datasources.yaml
      - grafana-data:/var/lib/grafana
    networks:
      - lgtm

  # Loki - Logs
  loki:
    image: grafana/loki:2.9.3
    container_name: loki
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - ./loki/loki-config.yaml:/etc/loki/local-config.yaml
      - loki-data:/loki
    networks:
      - lgtm

  # Tempo - Traces
  tempo:
    image: grafana/tempo:2.3.1
    container_name: tempo
    ports:
      - "3200:3200"   # Tempo
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
    command: -config.file=/etc/tempo/tempo.yaml
    volumes:
      - ./tempo/tempo-config.yaml:/etc/tempo/tempo.yaml
      - tempo-data:/var/tempo
    networks:
      - lgtm

  # Mimir - Metrics
  mimir:
    image: grafana/mimir:2.11.0
    container_name: mimir
    ports:
      - "9009:9009"
    command:
      - -config.file=/etc/mimir/mimir.yaml
    volumes:
      - ./mimir/mimir-config.yaml:/etc/mimir/mimir.yaml
      - mimir-data:/data
    networks:
      - lgtm

  # Grafana Alloy - Collector
  alloy:
    image: grafana/alloy:v1.0.0
    container_name: alloy
    ports:
      - "12345:12345"  # Alloy UI
      - "4317:4317"    # OTLP gRPC
      - "4318:4318"    # OTLP HTTP
    command:
      - run
      - /etc/alloy/config.alloy
      - --server.http.listen-addr=0.0.0.0:12345
    volumes:
      - ./alloy/config.alloy:/etc/alloy/config.alloy
    networks:
      - lgtm
    depends_on:
      - loki
      - tempo
      - mimir

volumes:
  grafana-data:
  loki-data:
  tempo-data:
  mimir-data:

networks:
  lgtm:
    driver: bridge
```

### Configuration Files

**grafana/datasources.yaml**:

```yaml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    uid: loki
    access: proxy
    url: http://loki:3100
    jsonData:
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "trace_id=(\\w+)"
          name: TraceID
          url: "$${__value.raw}"

  - name: Tempo
    type: tempo
    uid: tempo
    access: proxy
    url: http://tempo:3200
    jsonData:
      tracesToLogsV2:
        datasourceUid: loki
        filterByTraceID: true
        filterBySpanID: true
      tracesToMetrics:
        datasourceUid: mimir
      serviceMap:
        datasourceUid: tempo

  - name: Mimir
    type: prometheus
    uid: mimir
    access: proxy
    url: http://mimir:9009/prometheus
```

**loki/loki-config.yaml**:

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

limits_config:
  retention_period: 168h  # 7 days
```

**tempo/tempo-config.yaml**:

```yaml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

storage:
  trace:
    backend: local
    local:
      path: /var/tempo/traces
    wal:
      path: /var/tempo/wal
    pool:
      max_workers: 100
      queue_depth: 10000
```

**mimir/mimir-config.yaml**:

```yaml
target: all

server:
  http_listen_port: 9009
  grpc_listen_port: 9095

common:
  storage:
    backend: filesystem
    filesystem:
      dir: /data

blocks_storage:
  backend: filesystem
  filesystem:
    dir: /data/blocks

compactor:
  data_dir: /data/compactor

ingester:
  ring:
    kvstore:
      store: inmemory
    replication_factor: 1

limits:
  ingestion_rate: 50000
  ingestion_burst_size: 100000
```

**alloy/config.alloy**:

```hcl
otelcol.receiver.otlp "default" {
  grpc {
    endpoint = "0.0.0.0:4317"
  }

  http {
    endpoint = "0.0.0.0:4318"
  }

  output {
    metrics = [otelcol.processor.batch.default.input]
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.batch.default.input]
  }
}

otelcol.processor.batch "default" {
  output {
    metrics = [otelcol.exporter.prometheus.mimir.input]
    logs    = [otelcol.exporter.loki.default.input]
    traces  = [otelcol.exporter.otlp.tempo.input]
  }
}

otelcol.exporter.loki "default" {
  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}

otelcol.exporter.otlp "tempo" {
  client {
    endpoint = "tempo:4317"
    tls {
      insecure = true
    }
  }
}

otelcol.exporter.prometheus "mimir" {
  forward_to = [prometheus.remote_write.mimir.receiver]
}

prometheus.remote_write "mimir" {
  endpoint {
    url = "http://mimir:9009/api/v1/push"
  }
}
```

### Start Stack

```bash
cd examples/lgtm-docker-compose
docker-compose up -d

# Verify services
docker-compose ps

# Check logs
docker-compose logs -f

# Access Grafana: http://localhost:3000 (admin/admin)
# OTLP endpoint: localhost:4317 (gRPC) or localhost:4318 (HTTP)
```

---

## Kubernetes (Production)

### Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: implementing-observability
```

### Loki (StatefulSet)

```yaml
# loki-statefulset.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: loki-config
  namespace: observability
data:
  loki.yaml: |
    auth_enabled: false
    server:
      http_listen_port: 3100
    common:
      path_prefix: /loki
      storage:
        filesystem:
          chunks_directory: /loki/chunks
          rules_directory: /loki/rules
      replication_factor: 1
    schema_config:
      configs:
        - from: 2020-10-24
          store: boltdb-shipper
          object_store: filesystem
          schema: v11
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: loki
  namespace: observability
spec:
  serviceName: loki
  replicas: 1
  selector:
    matchLabels:
      app: loki
  template:
    metadata:
      labels:
        app: loki
    spec:
      containers:
      - name: loki
        image: grafana/loki:2.9.3
        args:
          - -config.file=/etc/loki/loki.yaml
        ports:
        - containerPort: 3100
          name: http
        volumeMounts:
        - name: config
          mountPath: /etc/loki
        - name: storage
          mountPath: /loki
      volumes:
      - name: config
        configMap:
          name: loki-config
  volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: loki
  namespace: observability
spec:
  ports:
  - port: 3100
    targetPort: 3100
    name: http
  selector:
    app: loki
```

### Tempo (StatefulSet)

```yaml
# tempo-statefulset.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tempo-config
  namespace: observability
data:
  tempo.yaml: |
    server:
      http_listen_port: 3200
    distributor:
      receivers:
        otlp:
          protocols:
            grpc:
              endpoint: 0.0.0.0:4317
    storage:
      trace:
        backend: local
        local:
          path: /var/tempo/traces
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: tempo
  namespace: observability
spec:
  serviceName: tempo
  replicas: 1
  selector:
    matchLabels:
      app: tempo
  template:
    metadata:
      labels:
        app: tempo
    spec:
      containers:
      - name: tempo
        image: grafana/tempo:2.3.1
        args:
          - -config.file=/etc/tempo/tempo.yaml
        ports:
        - containerPort: 3200
          name: http
        - containerPort: 4317
          name: otlp-grpc
        volumeMounts:
        - name: config
          mountPath: /etc/tempo
        - name: storage
          mountPath: /var/tempo
      volumes:
      - name: config
        configMap:
          name: tempo-config
  volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: tempo
  namespace: observability
spec:
  ports:
  - port: 3200
    targetPort: 3200
    name: http
  - port: 4317
    targetPort: 4317
    name: otlp-grpc
  selector:
    app: tempo
```

### Grafana (Deployment)

```yaml
# grafana-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: observability
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:10.2.3
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: grafana-admin
              key: password
        ports:
        - containerPort: 3000
          name: http
        volumeMounts:
        - name: datasources
          mountPath: /etc/grafana/provisioning/datasources
        - name: storage
          mountPath: /var/lib/grafana
      volumes:
      - name: datasources
        configMap:
          name: grafana-datasources
      - name: storage
        persistentVolumeClaim:
          claimName: grafana-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: observability
spec:
  type: LoadBalancer
  ports:
  - port: 3000
    targetPort: 3000
  selector:
    app: grafana
```

### Grafana Alloy (DaemonSet)

```yaml
# alloy-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: alloy
  namespace: observability
spec:
  selector:
    matchLabels:
      app: alloy
  template:
    metadata:
      labels:
        app: alloy
    spec:
      containers:
      - name: alloy
        image: grafana/alloy:v1.0.0
        args:
          - run
          - /etc/alloy/config.alloy
        ports:
        - containerPort: 4317
          name: otlp-grpc
        - containerPort: 4318
          name: otlp-http
        volumeMounts:
        - name: config
          mountPath: /etc/alloy
      volumes:
      - name: config
        configMap:
          name: alloy-config
---
apiVersion: v1
kind: Service
metadata:
  name: alloy
  namespace: observability
spec:
  type: ClusterIP
  ports:
  - port: 4317
    targetPort: 4317
    name: otlp-grpc
  - port: 4318
    targetPort: 4318
    name: otlp-http
  selector:
    app: alloy
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f namespace.yaml

# Deploy LGTM stack
kubectl apply -f loki-statefulset.yaml
kubectl apply -f tempo-statefulset.yaml
kubectl apply -f mimir-statefulset.yaml
kubectl apply -f grafana-deployment.yaml
kubectl apply -f alloy-daemonset.yaml

# Check status
kubectl get pods -n observability

# Get Grafana URL (if LoadBalancer)
kubectl get svc grafana -n observability
```

---

## Grafana Configuration

### Pre-configured Dashboards

**Create ConfigMap**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
  namespace: observability
data:
  dashboard-provider.yaml: |
    apiVersion: 1
    providers:
      - name: 'default'
        folder: 'General'
        type: file
        options:
          path: /var/lib/grafana/dashboards

  http-overview.json: |
    {
      "title": "HTTP Overview",
      "panels": [
        {
          "title": "Request Rate",
          "targets": [
            {
              "expr": "sum(rate(http_requests_total[5m]))"
            }
          ]
        }
      ]
    }
```

### Alerting

**Create Alert Rules**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-alerts
  namespace: observability
data:
  alerts.yaml: |
    groups:
      - name: http_alerts
        interval: 1m
        rules:
          - alert: HighErrorRate
            expr: |
              sum(rate(http_requests_total{status=~"5.."}[5m]))
              / sum(rate(http_requests_total[5m])) > 0.05
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: "High HTTP error rate"
              description: "Error rate is {{ $value | humanizePercentage }}"
```

---

## Scaling Considerations

### Horizontal Scaling

**Loki**:
- Read path: Scale queriers
- Write path: Scale ingesters
- Use object storage (S3, GCS) for long-term storage

**Tempo**:
- Scale distributors for ingestion
- Scale queriers for query performance
- Object storage is mandatory for production

**Mimir**:
- Distribute ingesters across AZs
- Scale compactors based on series count
- Use object storage for blocks

### Resource Requests (Production)

```yaml
# Loki
resources:
  requests:
    memory: "2Gi"
    cpu: "1"
  limits:
    memory: "4Gi"
    cpu: "2"

# Tempo
resources:
  requests:
    memory: "4Gi"
    cpu: "2"
  limits:
    memory: "8Gi"
    cpu: "4"

# Mimir
resources:
  requests:
    memory: "8Gi"
    cpu: "4"
  limits:
    memory: "16Gi"
    cpu: "8"
```

### High Availability

**3-replica setup**:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: loki
spec:
  replicas: 3
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: loki
            topologyKey: kubernetes.io/hostname
```

---

## Helm Charts (Alternative)

**Using official Grafana Helm charts**:

```bash
# Add Grafana Helm repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Loki
helm install loki grafana/loki -n observability

# Install Tempo
helm install tempo grafana/tempo -n observability

# Install Mimir
helm install mimir grafana/mimir-distributed -n observability

# Install Grafana
helm install grafana grafana/grafana -n observability
```

---

## Validation

**Test OTLP endpoint**:

```bash
# Test gRPC endpoint
grpcurl -plaintext localhost:4317 list

# Send test trace
curl -X POST http://localhost:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{
    "resourceSpans": [{
      "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": "test"}}]},
      "scopeSpans": [{
        "spans": [{
          "traceId": "5B8EFFF798038103D269B633813FC60C",
          "spanId": "EEE19B7EC3C1B174",
          "name": "test-span",
          "startTimeUnixNano": "1544712660000000000",
          "endTimeUnixNano": "1544712661000000000"
        }]
      }]
    }]
  }'
```

**Check Grafana**:
1. Navigate to http://localhost:3000
2. Explore → Tempo → Search for trace
3. Explore → Loki → Query logs
4. Explore → Mimir → Query metrics

---

## Troubleshooting

**Services not communicating**:
- Check network connectivity: `kubectl exec -it <pod> -- nc -zv loki 3100`
- Verify ConfigMaps are mounted correctly
- Check service DNS: `kubectl exec -it <pod> -- nslookup loki.observability.svc.cluster.local`

**High memory usage**:
- Reduce retention period in Loki config
- Enable compaction in Mimir
- Tune batch sizes in Alloy

**Missing data**:
- Verify OTLP endpoint is accessible from apps
- Check Alloy logs: `kubectl logs -n observability -l app=alloy`
- Validate data is reaching backends: `kubectl logs -n observability -l app=loki`
