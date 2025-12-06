# Storage

## Table of Contents

1. [StorageClasses](#storageclasses)
2. [PersistentVolumes and PersistentVolumeClaims](#persistentvolumes-and-persistentvolumeclaims)
3. [CSI Drivers](#csi-drivers)
4. [Volume Snapshots](#volume-snapshots)
5. [StatefulSets with Storage](#statefulsets-with-storage)
6. [Storage Decision Framework](#storage-decision-framework)

## StorageClasses

### AWS EBS StorageClasses

**General Purpose SSD (gp3):**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iopsPerGB: "50"
  throughput: "125"  # MB/s
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123456789:key/..."
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

**Provisioned IOPS SSD (io2):**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: io2-high-iops
provisioner: ebs.csi.aws.com
parameters:
  type: io2
  iops: "10000"      # Fixed IOPS
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Retain  # Keep volume after PVC deletion
```

**HDD (st1) - Throughput Optimized:**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: st1
provisioner: ebs.csi.aws.com
parameters:
  type: st1  # Low cost, high throughput
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### GCP Persistent Disk

**SSD:**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: pd-ssd
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

**Balanced:**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: pd-balanced
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-balanced  # Cost-effective, good performance
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Azure Disk

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium
provisioner: disk.csi.azure.com
parameters:
  storageaccounttype: Premium_LRS
  kind: Managed
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### NFS StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: nfs.csi.k8s.io
parameters:
  server: nfs-server.example.com
  share: /exports/kubernetes
  mountOptions: "hard,nfsvers=4.1"
volumeBindingMode: Immediate
allowVolumeExpansion: true
reclaimPolicy: Retain
```

### StorageClass Parameters

**volumeBindingMode:**
- **WaitForFirstConsumer:** Delay binding until pod scheduled (topology-aware)
- **Immediate:** Bind immediately (may cause zone mismatch)

**reclaimPolicy:**
- **Delete:** Delete volume when PVC deleted
- **Retain:** Keep volume (manual cleanup required)

**allowVolumeExpansion:**
- **true:** Allow PVC resize
- **false:** Fixed size

## PersistentVolumes and PersistentVolumeClaims

### PVC Lifecycle

```yaml
# 1. Create PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
spec:
  storageClassName: gp3
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
```

```yaml
# 2. Use PVC in Pod
apiVersion: v1
kind: Pod
metadata:
  name: postgres
spec:
  containers:
  - name: postgres
    image: postgres:15
    volumeMounts:
    - name: data
      mountPath: /var/lib/postgresql/data
    env:
    - name: POSTGRES_PASSWORD
      valueFrom:
        secretKeyRef:
          name: postgres-secret
          key: password
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: postgres-data
```

### Access Modes

**ReadWriteOnce (RWO):**
- Single node read-write
- Most common (block storage)
- AWS EBS, GCP PD, Azure Disk

**ReadOnlyMany (ROX):**
- Multiple nodes read-only
- Use for shared static content

**ReadWriteMany (RWX):**
- Multiple nodes read-write
- Requires network storage (NFS, EFS, Azure Files)

**ReadWriteOncePod (RWOP):**
- Single pod read-write (Kubernetes 1.29+)
- Stricter than RWO

### Volume Expansion

```yaml
# 1. Ensure allowVolumeExpansion: true in StorageClass

# 2. Edit PVC
kubectl edit pvc postgres-data

# 3. Update storage size
spec:
  resources:
    requests:
      storage: 100Gi  # Increased from 50Gi

# 4. Check expansion status
kubectl describe pvc postgres-data

# 5. May require pod restart for filesystem resize
kubectl rollout restart deployment postgres
```

### Static Provisioning

```yaml
# 1. Create PV (manual)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: static-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  awsElasticBlockStore:
    volumeID: vol-0abc123456789def0
    fsType: ext4
---
# 2. Create PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: static-pvc
spec:
  storageClassName: manual
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
```

## CSI Drivers

### AWS EBS CSI Driver

**Installation (Helm):**
```bash
helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
helm install aws-ebs-csi-driver aws-ebs-csi-driver/aws-ebs-csi-driver \
  --namespace kube-system \
  --set enableVolumeScheduling=true \
  --set enableVolumeSnapshot=true
```

**IAM Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateVolume",
        "ec2:DeleteVolume",
        "ec2:AttachVolume",
        "ec2:DetachVolume",
        "ec2:DescribeVolumes",
        "ec2:CreateSnapshot",
        "ec2:DeleteSnapshot",
        "ec2:DescribeSnapshots"
      ],
      "Resource": "*"
    }
  ]
}
```

### AWS EFS CSI Driver

**Installation:**
```bash
helm repo add aws-efs-csi-driver https://kubernetes-sigs.github.io/aws-efs-csi-driver
helm install aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver \
  --namespace kube-system
```

**StorageClass (EFS):**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: efs-sc
provisioner: efs.csi.aws.com
parameters:
  provisioningMode: efs-ap
  fileSystemId: fs-0abc123456789def0
  directoryPerms: "700"
  gidRangeStart: "1000"
  gidRangeEnd: "2000"
  basePath: "/dynamic_provisioning"
volumeBindingMode: Immediate
reclaimPolicy: Delete
```

**PVC (RWX):**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: efs-claim
spec:
  storageClassName: efs-sc
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
```

### GCP Filestore CSI Driver

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: filestore
provisioner: filestore.csi.storage.gke.io
parameters:
  tier: standard
  network: default
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

## Volume Snapshots

### VolumeSnapshotClass

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: ebs-snapshot-class
driver: ebs.csi.aws.com
deletionPolicy: Delete
parameters:
  tagSpecification_1: "Name=CreatedBy,Value=kubernetes"
```

### Create Snapshot

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: postgres-snapshot
spec:
  volumeSnapshotClassName: ebs-snapshot-class
  source:
    persistentVolumeClaimName: postgres-data
```

### Restore from Snapshot

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-restore
spec:
  storageClassName: gp3
  dataSource:
    name: postgres-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
```

### Automated Backups

```yaml
# CronJob for daily snapshots
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-backup
spec:
  schedule: "0 2 * * *"  # 2 AM daily
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: snapshot-creator
          containers:
          - name: kubectl
            image: bitnami/kubectl:latest
            command:
            - /bin/sh
            - -c
            - |
              kubectl create -f - <<EOF
              apiVersion: snapshot.storage.k8s.io/v1
              kind: VolumeSnapshot
              metadata:
                name: postgres-backup-$(date +%Y%m%d-%H%M%S)
              spec:
                volumeSnapshotClassName: ebs-snapshot-class
                source:
                  persistentVolumeClaimName: postgres-data
              EOF
          restartPolicy: OnFailure
```

## StatefulSets with Storage

### Basic StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
          name: postgres
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: gp3
      resources:
        requests:
          storage: 50Gi
```

**Creates:**
- `postgres-0` with PVC `data-postgres-0`
- `postgres-1` with PVC `data-postgres-1`
- `postgres-2` with PVC `data-postgres-2`

### Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  clusterIP: None  # Headless
  selector:
    app: postgres
  ports:
  - protocol: TCP
    port: 5432
    targetPort: 5432
```

**DNS entries:**
- `postgres-0.postgres.default.svc.cluster.local`
- `postgres-1.postgres.default.svc.cluster.local`
- `postgres-2.postgres.default.svc.cluster.local`

### Persistent Identity

StatefulSet pods have stable:
- **Network identity:** `postgres-0`, `postgres-1`, `postgres-2`
- **Storage:** Each pod's PVC persists across restarts
- **Ordering:** Pods created/deleted in order (0→1→2)

## Storage Decision Framework

### Performance Tiers

| Use Case | Performance | IOPS | Throughput | AWS | GCP | Azure |
|----------|-------------|------|------------|-----|-----|-------|
| High-performance DB | High | 10,000+ | 250+ MB/s | io2 | pd-ssd | Premium_LRS |
| General DB/apps | Medium | 3,000-16,000 | 125-1000 MB/s | gp3 | pd-balanced | StandardSSD_LRS |
| Logs, backups | Low | < 500 | 40-90 MB/s | st1 | pd-standard | Standard_LRS |
| Shared files | Medium | N/A | 100+ MB/s | EFS | Filestore | Azure Files |

### Access Mode Selection

**Single-pod write:**
- Use ReadWriteOnce (RWO)
- Block storage (EBS, PD, Azure Disk)
- Most databases

**Multiple-pod write:**
- Use ReadWriteMany (RWX)
- Network storage (EFS, Filestore, Azure Files)
- Shared file systems

**Multiple-pod read-only:**
- Use ReadOnlyMany (ROX)
- Pre-populated static content
- ML model storage

### Cost Optimization

**Reclaim Policy:**
```yaml
# Production: Retain (safety)
reclaimPolicy: Retain

# Development: Delete (cost savings)
reclaimPolicy: Delete
```

**Right-size Storage:**
```bash
# Check actual usage
kubectl exec -it postgres-0 -- df -h /var/lib/postgresql/data

# If usage < 50%, consider downsizing
```

**Lifecycle Management:**
```yaml
# S3 lifecycle policy (EBS snapshots)
# Move to Glacier after 30 days
# Delete after 90 days
```

### Monitoring

```bash
# PVC usage
kubectl get pvc -A

# PVC status
kubectl describe pvc postgres-data

# Check mount inside pod
kubectl exec -it pod-name -- df -h

# View storage metrics
kubectl top pods --containers
```

## Troubleshooting

### PVC Stuck in Pending

```bash
kubectl describe pvc <pvc-name>

# Common causes:
# 1. No StorageClass found
# 2. Insufficient storage quota
# 3. Zone mismatch (volumeBindingMode: Immediate)
# 4. CSI driver not installed
```

**Fix:**
```bash
# Check StorageClass exists
kubectl get storageclass

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Switch to WaitForFirstConsumer
kubectl patch storageclass gp3 -p '{"volumeBindingMode":"WaitForFirstConsumer"}'
```

### Mount Failures

```bash
# Check pod events
kubectl describe pod <pod-name>

# Common errors:
# - "Multi-Attach error": Volume already attached to another node
# - "Unable to mount": Filesystem corruption or permissions
```

**Fix:**
```bash
# Force detach (AWS)
aws ec2 detach-volume --volume-id vol-xxx --force

# Delete pod to trigger reattach
kubectl delete pod <pod-name>
```

### Volume Expansion Failures

```bash
# Check expansion status
kubectl describe pvc <pvc-name>

# Common issues:
# - allowVolumeExpansion: false
# - Filesystem not resized
# - Pod not restarted
```

**Fix:**
```bash
# Enable expansion
kubectl patch storageclass gp3 -p '{"allowVolumeExpansion":true}'

# Restart pod
kubectl rollout restart deployment <name>
```

## Summary

**Storage Pattern Selection:**

| Workload | Storage Type | Access Mode | StorageClass |
|----------|--------------|-------------|--------------|
| PostgreSQL | Block | ReadWriteOnce | gp3/pd-ssd |
| MongoDB replica | Block | ReadWriteOnce | gp3/pd-balanced |
| Shared uploads | Network | ReadWriteMany | EFS/Filestore |
| ML models | Object/Network | ReadOnlyMany | S3/GCS |
| Logs | Block | ReadWriteOnce | st1/pd-standard |

**Best Practices:**
1. Use CSI drivers (not legacy in-tree provisioners)
2. Enable volume snapshots for stateful workloads
3. Set appropriate reclaim policies (Retain for production)
4. Use WaitForFirstConsumer for topology awareness
5. Monitor storage usage and right-size PVCs
6. Automate backup/restore procedures
7. Test volume expansion before production
