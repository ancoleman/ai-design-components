# Kubernetes Disaster Recovery

## Table of Contents

1. [Velero Patterns](#velero-patterns)
2. [Monitoring Velero](#monitoring-velero)

## Velero Patterns

### Installation and Configuration

**AWS Setup:**
```bash
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0 \
  --bucket my-velero-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./credentials-velero \
  --use-node-agent \
  --uploader-type restic
```

**GCP Setup:**
```bash
velero install \
  --provider gcp \
  --plugins velero/velero-plugin-for-gcp:v1.9.0 \
  --bucket my-velero-backups \
  --secret-file ./credentials-velero
```

### Backup Schedules

**Production Namespace (Hourly):**
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: hourly-prod-backup
  namespace: velero
spec:
  schedule: "0 * * * *"
  template:
    ttl: 168h  # 7 days
    includedNamespaces: [production]
    labelSelector:
      matchLabels:
        backup: enabled
    snapshotVolumes: true
    hooks:
      resources:
        - name: postgres-backup-hook
          includedNamespaces: [production]
          labelSelector:
            matchLabels:
              app: postgres
          pre:
            - exec:
                container: postgres
                command: ["/bin/bash", "-c", "pg_dump > /tmp/backup.sql"]
          post:
            - exec:
                container: postgres
                command: ["/bin/bash", "-c", "rm /tmp/backup.sql"]
```

### Restic Integration

**Opt-in Volumes for File-Level Backup:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    metadata:
      annotations:
        backup.velero.io/backup-volumes: data,config
    spec:
      containers:
        - name: app
          volumeMounts:
            - name: data
              mountPath: /data
            - name: config
              mountPath: /config
```

### etcd Backup

**Automated Snapshot Script:**
```bash
#!/bin/bash
ETCDCTL_API=3 etcdctl snapshot save \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  /backups/etcd/snapshot-$(date +%Y%m%d-%H%M%S).db
```

## Monitoring Velero

### Prometheus Metrics

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: velero
  namespace: velero
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: velero
  endpoints:
    - port: monitoring
      interval: 30s
```

### Alert Rules

```yaml
groups:
  - name: velero-backup-alerts
    rules:
      - alert: VeleroBackupFailed
        expr: velero_backup_failure_total > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: Velero backup {{ $labels.schedule }} failed
      
      - alert: VeleroBackupTooOld
        expr: time() - velero_backup_last_successful_timestamp{schedule!=""} > 86400
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: No successful backup in 24 hours
```
