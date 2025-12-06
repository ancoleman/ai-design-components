# Troubleshooting

## Table of Contents

1. [Pod Issues](#pod-issues)
2. [Networking Issues](#networking-issues)
3. [Storage Issues](#storage-issues)
4. [Resource Issues](#resource-issues)
5. [Troubleshooting Toolkit](#troubleshooting-toolkit)

## Pod Issues

### Pod Stuck in Pending

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
my-app-6d5f8b9c4-xz7k2   0/1     Pending   0          5m
```

**Diagnosis:**
```bash
kubectl describe pod my-app-6d5f8b9c4-xz7k2
```

**Common Causes:**

**A. Insufficient CPU/Memory**
```
Events:
  Warning  FailedScheduling  0/3 nodes are available: 3 Insufficient cpu.
```
**Solution:**
- Reduce resource requests
- Add more nodes
- Check resource quotas

```bash
# Check node capacity
kubectl describe nodes | grep -A5 "Allocated resources"

# Check namespace quotas
kubectl describe resourcequota -n production
```

**B. Node Selector Mismatch**
```
Events:
  Warning  FailedScheduling  0/3 nodes are available: 3 node(s) didn't match node selector.
```
**Solution:**
- Fix nodeSelector in pod spec
- Add matching labels to nodes

```bash
# Check node labels
kubectl get nodes --show-labels

# Add label to node
kubectl label nodes node-1 workload=general
```

**C. PVC Not Bound**
```
Events:
  Warning  FailedScheduling  persistentvolumeclaim "data" not found
```
**Solution:**
- Create PVC
- Fix PVC name in pod spec
- Check StorageClass exists

```bash
# Check PVC status
kubectl get pvc -n production

# Describe PVC
kubectl describe pvc data -n production
```

**D. Taints Not Tolerated**
```
Events:
  Warning  FailedScheduling  0/3 nodes are available: 3 node(s) had taints that the pod didn't tolerate.
```
**Solution:**
- Add toleration to pod
- Remove taint from nodes

```bash
# Check node taints
kubectl describe nodes | grep Taints

# Remove taint
kubectl taint nodes node-1 key:NoSchedule-
```

### CrashLoopBackOff

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS             RESTARTS   AGE
my-app-6d5f8b9c4-abc12   0/1     CrashLoopBackOff   5          3m
```

**Diagnosis:**
```bash
# Check current logs
kubectl logs my-app-6d5f8b9c4-abc12

# Check previous container logs
kubectl logs my-app-6d5f8b9c4-abc12 --previous

# Check events
kubectl describe pod my-app-6d5f8b9c4-abc12
```

**Common Causes:**

**A. Application Crash on Startup**
```
$ kubectl logs my-app-6d5f8b9c4-abc12
Error: Cannot find module '/app/index.js'
```
**Solution:**
- Fix application code
- Ensure correct Docker image
- Check file paths in container

**B. Missing Environment Variables**
```
$ kubectl logs my-app-6d5f8b9c4-abc12
Error: DATABASE_URL environment variable not set
```
**Solution:**
```yaml
# Add environment variables
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: url
```

**C. Liveness Probe Failing Too Quickly**
```
Events:
  Warning  Unhealthy  Liveness probe failed: HTTP probe failed
```
**Solution:**
```yaml
# Increase initialDelaySeconds
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 60  # Give app time to start
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

**D. OOMKilled (Out of Memory)**
```
Events:
  Warning  BackOff  Back-off restarting failed container
State:
  Last State:     Terminated
    Reason:       OOMKilled
    Exit Code:    137
```
**Solution:**
- Increase memory limit
- Fix memory leak in application
- Profile memory usage

```yaml
resources:
  limits:
    memory: "1Gi"  # Increased from 512Mi
```

### ImagePullBackOff

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS              RESTARTS   AGE
my-app-6d5f8b9c4-def34   0/1     ImagePullBackOff    0          2m
```

**Diagnosis:**
```bash
kubectl describe pod my-app-6d5f8b9c4-def34
```

**Common Causes:**

**A. Image Doesn't Exist**
```
Events:
  Warning  Failed  Failed to pull image "myapp:v2.0": rpc error: code = Unknown desc = Error response from daemon: manifest for myapp:v2.0 not found
```
**Solution:**
- Fix image name/tag
- Push image to registry
- Check registry URL

**B. Authentication Required**
```
Events:
  Warning  Failed  Failed to pull image: rpc error: code = Unknown desc = Error response from daemon: pull access denied
```
**Solution:**
```bash
# Create image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.azurecr.io \
  --docker-username=myuser \
  --docker-password=mypassword \
  --docker-email=myemail@example.com \
  --namespace production

# Add to pod spec
spec:
  imagePullSecrets:
  - name: regcred
```

**C. Network Issues**
```
Events:
  Warning  Failed  Failed to pull image: rpc error: dial tcp: lookup myregistry.com: no such host
```
**Solution:**
- Check DNS resolution
- Check NetworkPolicies allow egress
- Check firewall rules

```bash
# Test DNS from node
kubectl run test --rm -it --image=busybox -- nslookup myregistry.com

# Check NetworkPolicies
kubectl get networkpolicies -n production
```

### Init Container Failures

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS     RESTARTS   AGE
my-app-6d5f8b9c4-ghi56   0/1     Init:0/1   0          2m
```

**Diagnosis:**
```bash
# Check init container logs
kubectl logs my-app-6d5f8b9c4-ghi56 -c init-container-name

# Describe pod
kubectl describe pod my-app-6d5f8b9c4-ghi56
```

**Solution:**
- Fix init container script
- Ensure init container can complete
- Check init container resource requests

### Pods Evicted

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
my-app-6d5f8b9c4-jkl78   0/1     Evicted   0          10m
```

**Diagnosis:**
```bash
kubectl describe pod my-app-6d5f8b9c4-jkl78

# Check eviction reason
kubectl get pod my-app-6d5f8b9c4-jkl78 -o jsonpath='{.status.reason}'
```

**Common Reasons:**

**A. Node Pressure (DiskPressure, MemoryPressure)**
```
Reason: NodeLost
Message: Node node-1 which was running pod my-app was not ready for more than 40s
```
**Solution:**
- Check node health
- Increase disk/memory on nodes
- Clean up unused images/volumes

```bash
# Check node conditions
kubectl describe node node-1 | grep Conditions -A10

# Clean up images on node
docker system prune -a

# Clean up volumes
docker volume prune
```

**B. Exceeding ResourceQuota**
```
Reason: QuotaExceeded
Message: exceeded quota: compute-resources
```
**Solution:**
- Increase quota
- Reduce resource requests
- Clean up unused resources

## Networking Issues

### Service Not Accessible

**Symptoms:**
```bash
$ curl http://backend-service:8080
curl: (7) Failed to connect to backend-service port 8080: Connection refused
```

**Diagnosis:**
```bash
# Check service exists
kubectl get svc backend-service -n production

# Check endpoints (should list pod IPs)
kubectl get endpoints backend-service -n production

# Describe service
kubectl describe svc backend-service -n production
```

**Common Causes:**

**A. Service Selector Doesn't Match Pod Labels**
```bash
# Check service selector
kubectl get svc backend-service -o yaml | grep -A3 selector

# Check pod labels
kubectl get pods -l app=backend -o wide

# If no pods match, fix selector or pod labels
```

**B. Pods Not Ready (Readiness Probe Failing)**
```bash
$ kubectl get pods
NAME                       READY   STATUS    RESTARTS   AGE
backend-6d5f8b9c4-abc12    0/1     Running   0          2m
```
**Solution:**
- Fix readiness probe
- Debug why probe is failing

```bash
# Check probe configuration
kubectl describe pod backend-6d5f8b9c4-abc12 | grep -A10 Readiness

# Test probe manually
kubectl exec -it backend-6d5f8b9c4-abc12 -- curl http://localhost:8080/health
```

**C. NetworkPolicy Blocking Traffic**
```bash
# List NetworkPolicies
kubectl get networkpolicies -n production

# Describe policy
kubectl describe networkpolicy default-deny-all -n production

# Test connectivity
kubectl run test --rm -it --image=busybox -- wget -O- http://backend-service:8080
```

**Solution:**
- Create NetworkPolicy to allow traffic
- Fix existing policy selectors

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### DNS Resolution Failures

**Symptoms:**
```bash
$ kubectl exec -it my-app -- nslookup backend-service
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

nslookup: can't resolve 'backend-service'
```

**Diagnosis:**
```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test DNS from pod
kubectl run test --rm -it --image=busybox -- nslookup kubernetes.default
```

**Solution:**
- Restart CoreDNS pods
- Check CoreDNS ConfigMap
- Verify NetworkPolicy allows DNS

```bash
# Restart CoreDNS
kubectl rollout restart deployment coredns -n kube-system

# Allow DNS in NetworkPolicy
egress:
- to:
  - namespaceSelector:
      matchLabels:
        name: kube-system
  - podSelector:
      matchLabels:
        k8s-app: kube-dns
  ports:
  - protocol: UDP
    port: 53
```

### Ingress Not Working

**Symptoms:**
```bash
$ curl https://myapp.example.com
curl: (7) Failed to connect to myapp.example.com port 443: Connection refused
```

**Diagnosis:**
```bash
# Check Ingress resource
kubectl get ingress -n production

# Describe Ingress
kubectl describe ingress app-ingress -n production

# Check Ingress controller pods
kubectl get pods -n ingress-nginx

# Check Ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

**Common Issues:**

**A. Ingress Controller Not Installed**
```bash
# Install Nginx Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

**B. Ingress Class Mismatch**
```yaml
# Fix ingressClassName
spec:
  ingressClassName: nginx  # Must match installed controller
```

**C. Backend Service Not Found**
```
Events:
  Warning  Sync  service "backend" not found
```
**Solution:**
- Create backend Service
- Fix service name in Ingress spec

## Storage Issues

### PVC Stuck in Pending

**Symptoms:**
```bash
$ kubectl get pvc
NAME            STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
postgres-data   Pending                                      gp3            5m
```

**Diagnosis:**
```bash
kubectl describe pvc postgres-data
```

**Common Causes:**

**A. StorageClass Not Found**
```
Events:
  Warning  ProvisioningFailed  storageclass.storage.k8s.io "gp3" not found
```
**Solution:**
```bash
# Check StorageClasses
kubectl get storageclass

# Create StorageClass (AWS EBS example)
kubectl apply -f storageclass-gp3.yaml
```

**B. Zone Mismatch (volumeBindingMode: Immediate)**
```
Events:
  Warning  ProvisioningFailed  volume.beta.kubernetes.io/zone not accessible from current zone
```
**Solution:**
```yaml
# Change to WaitForFirstConsumer
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer  # Wait for pod scheduling
```

**C. CSI Driver Not Installed**
```
Events:
  Warning  ProvisioningFailed  Failed to provision volume: CSI driver not installed
```
**Solution:**
```bash
# Install AWS EBS CSI Driver
helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
helm install aws-ebs-csi-driver aws-ebs-csi-driver/aws-ebs-csi-driver \
  --namespace kube-system
```

### Volume Mount Failures

**Symptoms:**
```bash
$ kubectl get pods
NAME                       READY   STATUS              RESTARTS   AGE
postgres-6d5f8b9c4-xyz     0/1     ContainerCreating   0          2m
```

**Diagnosis:**
```bash
kubectl describe pod postgres-6d5f8b9c4-xyz

# Look for mount errors
Events:
  Warning  FailedMount  Unable to attach or mount volumes
```

**Common Causes:**

**A. Multi-Attach Error**
```
Events:
  Warning  FailedAttachVolume  Multi-Attach error for volume "pvc-xxx": Volume is already exclusively attached to one node
```
**Solution:**
- Volume already attached to another node
- Delete old pod or wait for detachment

```bash
# Force delete old pod
kubectl delete pod old-pod --grace-period=0 --force

# AWS: Force detach volume
aws ec2 detach-volume --volume-id vol-xxx --force
```

**B. Filesystem Corruption**
```
Events:
  Warning  FailedMount  MountVolume.SetUp failed: mount failed: exit status 32
```
**Solution:**
- Check filesystem
- Restore from snapshot

## Resource Issues

### CPU Throttling

**Diagnosis:**
```bash
# Check CPU metrics
kubectl top pods -n production

# Check for throttling (Prometheus)
rate(container_cpu_cfs_throttled_seconds_total[5m]) > 0.1
```

**Solution:**
- Increase CPU limits
- Reduce CPU usage in application

```yaml
resources:
  limits:
    cpu: "1"  # Increased from 500m
```

### Memory Leaks

**Diagnosis:**
```bash
# Monitor memory usage
kubectl top pods -n production --containers

# Check for OOMKilled events
kubectl get events --field-selector reason=OOMKilled
```

**Solution:**
- Profile application for memory leaks
- Increase memory limits temporarily
- Fix memory leak in code

### Node Pressure

**Symptoms:**
```bash
$ kubectl describe node node-1
Conditions:
  Type             Status
  MemoryPressure   True
  DiskPressure     True
```

**Diagnosis:**
```bash
# Check node resources
kubectl describe node node-1 | grep -A10 "Allocated resources"

# SSH to node and check
ssh node-1
df -h  # Disk usage
free -h  # Memory usage
```

**Solution:**
- Clean up images: `docker system prune -a`
- Clean up volumes: `docker volume prune`
- Increase node disk/memory
- Evict non-critical pods

## Troubleshooting Toolkit

### Essential Commands

```bash
# Pod investigation
kubectl get pods -n production
kubectl describe pod <pod-name> -n production
kubectl logs <pod-name> -n production
kubectl logs <pod-name> -c <container-name> --previous
kubectl exec -it <pod-name> -n production -- /bin/sh

# Service debugging
kubectl get svc -n production
kubectl get endpoints <service-name> -n production
kubectl describe svc <service-name> -n production

# Events
kubectl get events -n production --sort-by='.lastTimestamp'
kubectl get events --field-selector involvedObject.name=<pod-name>

# Resource usage
kubectl top nodes
kubectl top pods -n production
kubectl top pods -n production --containers

# NetworkPolicy debugging
kubectl get networkpolicies -n production
kubectl describe networkpolicy <policy-name> -n production

# Storage debugging
kubectl get pvc -n production
kubectl describe pvc <pvc-name> -n production
kubectl get storageclass
```

### Debug Pods

```bash
# Run ephemeral debug pod
kubectl run debug --rm -it --image=busybox -- /bin/sh

# Debug specific pod
kubectl debug <pod-name> -it --image=busybox --target=<container-name>

# Copy pod for debugging (Kubernetes 1.20+)
kubectl debug <pod-name> -it --copy-to=<debug-pod-name> --container=<container-name>
```

### Network Debugging

```bash
# Test DNS
kubectl run test --rm -it --image=busybox -- nslookup kubernetes.default

# Test HTTP
kubectl run test --rm -it --image=curlimages/curl -- curl http://backend:8080

# Test connectivity
kubectl run test --rm -it --image=busybox -- wget -O- http://backend:8080

# Network tools pod
kubectl run nettools --rm -it --image=nicolaka/netshoot -- /bin/bash
# Inside pod: dig, nslookup, curl, tcpdump, nmap, etc.
```

### Node Investigation

```bash
# Node details
kubectl describe node <node-name>

# Node logs (SSH to node)
journalctl -u kubelet -f

# Container logs on node
docker ps -a
docker logs <container-id>

# Resource usage on node
top
free -h
df -h
```

### Prometheus Queries

```promql
# CPU throttling
rate(container_cpu_cfs_throttled_seconds_total[5m])

# Memory usage vs limit
container_memory_working_set_bytes / container_spec_memory_limit_bytes

# Pod restarts
kube_pod_container_status_restarts_total

# OOMKilled pods
kube_pod_container_status_terminated_reason{reason="OOMKilled"}

# Pending pods
kube_pod_status_phase{phase="Pending"}

# Failed scheduling
kube_pod_status_scheduled{condition="false"}
```

## Summary

**Troubleshooting Workflow:**

1. **Identify symptom** (Pending, CrashLoopBackOff, etc.)
2. **Gather information** (`kubectl describe`, `kubectl logs`)
3. **Check events** (`kubectl get events`)
4. **Test hypothesis** (DNS, connectivity, resources)
5. **Apply fix** (increase resources, fix config, etc.)
6. **Verify** (check pod status, test functionality)
7. **Monitor** (ensure issue doesn't recur)

**Common Root Causes:**
- Resource constraints (CPU, memory, disk)
- Configuration errors (wrong labels, selectors)
- Network policies blocking traffic
- Missing dependencies (images, volumes, secrets)
- Node issues (pressure, taints, failures)

**Best Practices:**
- Always check `kubectl describe` first
- Review events for clues
- Test hypotheses systematically
- Document fixes for future reference
- Set up monitoring and alerts
- Use PodDisruptionBudgets for critical workloads
