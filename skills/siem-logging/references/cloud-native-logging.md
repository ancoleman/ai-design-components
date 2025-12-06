# Cloud-Native Logging

## Table of Contents

- [AWS Logging](#aws-logging)
- [Azure Logging](#azure-logging)
- [Kubernetes Logging](#kubernetes-logging)
- [Summary](#summary)

## AWS Logging

### Key Services

- **CloudTrail:** API activity logs
- **VPC Flow Logs:** Network traffic logs
- **CloudWatch Logs:** Application and system logs
- **GuardDuty:** Threat detection
- **Security Hub:** Aggregated security findings

### AWS Security Lake Setup

```bash
# Enable AWS Security Lake
aws securitylake create-data-lake \
  --region us-east-1 \
  --meta-store-manager-role-arn arn:aws:iam::123456789012:role/SecurityLakeRole

# Add CloudTrail as source
aws securitylake create-aws-log-source \
  --sources '[{"sourceName":"CLOUD_TRAIL_MGMT","sourceVersion":"2.0"}]'

# Add VPC Flow Logs
aws securitylake create-aws-log-source \
  --sources '[{"sourceName":"VPC_FLOW","sourceVersion":"2.0"}]'
```

## Azure Logging

### Key Services

- **Azure Monitor:** Centralized monitoring
- **Azure Activity Logs:** Subscription-level events
- **Azure AD Logs:** Authentication and authorization
- **Azure Security Center:** Security recommendations
- **Microsoft Sentinel:** Cloud-native SIEM

### Sentinel Setup

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group security-rg \
  --workspace-name security-sentinel \
  --location eastus

# Enable Microsoft Sentinel
az sentinel workspace create \
  --resource-group security-rg \
  --workspace-name security-sentinel

# Connect Azure AD
az sentinel data-connector create \
  --resource-group security-rg \
  --workspace-name security-sentinel \
  --name AzureActiveDirectory \
  --kind AzureActiveDirectory
```

## Kubernetes Logging

### Fluentd DaemonSet

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccountName: fluentd
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.kube-logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## Summary

- **AWS:** Use Security Lake for centralized security data lake
- **Azure:** Use Microsoft Sentinel for cloud-native SIEM
- **GCP:** Use Cloud Logging and Chronicle for security monitoring
- **Kubernetes:** Use Fluentd/Fluent Bit for container log aggregation
