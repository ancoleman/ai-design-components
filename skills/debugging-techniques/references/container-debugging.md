# Container Debugging Reference

## Table of Contents

1. [kubectl debug with Ephemeral Containers](#kubectl-debug-with-ephemeral-containers)
2. [Node Debugging](#node-debugging)
3. [Docker Container Debugging](#docker-container-debugging)
4. [Common Debugging Scenarios](#common-debugging-scenarios)
5. [Advanced Techniques](#advanced-techniques)
6. [Best Practices](#best-practices)

## kubectl debug with Ephemeral Containers

### When to Use Ephemeral Containers

**Use ephemeral containers when:**
- Container has crashed (kubectl exec won't work)
- Using distroless/minimal image (no shell, no debugging tools)
- Need debugging tools without rebuilding image
- Debugging network issues (DNS, connectivity)
- Inspecting running process without restart

**Don't use ephemeral containers when:**
- kubectl exec works (simpler, faster)
- Debugging simple apps (logs may be sufficient)
- Performance testing (ephemeral containers add overhead)

### Basic Usage

```bash
# Add ephemeral debugging container
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Specify container name
kubectl debug -it <pod-name> --image=busybox --container=debugger

# Auto-attach with interactive terminal
kubectl debug -i <pod-name> --image=alpine
```

### Process Namespace Sharing

**Share process namespace with target container:**
```bash
kubectl debug -it <pod-name> \
  --image=busybox \
  --target=app \
  --share-processes

# Now can see app container's processes
ps aux
```

**Why share processes:**
- Inspect running processes from app container
- Send signals to app processes (SIGTERM, SIGUSR1)
- Use strace, gdb on app processes

### Debugging Distroless Images

**Problem:** Distroless images have no shell or debugging tools.

**Solution:** Add ephemeral container with tools.

```bash
# Step 1: Try kubectl exec (will fail for distroless)
kubectl exec -it my-distroless-pod -- sh
# Error: executable file not found

# Step 2: Add ephemeral container
kubectl debug -it my-distroless-pod \
  --image=busybox \
  --target=app \
  --share-processes

# Step 3: Inside debug container
ps aux  # See app processes
netstat -tuln  # Check network
```

### Recommended Debugging Images

| Image | Size | Best For | Tools Included |
|-------|------|----------|----------------|
| **nicolaka/netshoot** | ~380MB | Network debugging | curl, dig, netstat, tcpdump, iperf, nslookup, traceroute, netcat |
| **busybox** | ~1MB | Minimal debugging | sh, basic utilities (ls, ps, cat) |
| **alpine** | ~5MB | Lightweight + packages | sh, apk (package manager) |
| **ubuntu** | ~70MB | Full environment | bash, apt, comprehensive tools |
| **debian:slim** | ~50MB | Balanced | bash, apt-get, standard utilities |

### Network Debugging with netshoot

```bash
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Inside debug container:

# Test HTTP endpoint
curl http://api-service:8080/health

# DNS lookup
nslookup api-service
dig api-service.default.svc.cluster.local

# Check listening ports
netstat -tuln

# Capture packets
tcpdump -i eth0 port 8080

# Test bandwidth
iperf3 -c server-host

# Trace route
traceroute api-service
```

## Node Debugging

### Debug Specific Node

```bash
# Create privileged pod on node
kubectl debug node/<node-name> -it --image=ubuntu

# Mounts node's root filesystem at /host
```

**Example workflow:**
```bash
kubectl debug node/worker-1 -it --image=ubuntu

# Inside debug pod
chroot /host

# Now can access node's filesystem and processes
systemctl status kubelet
journalctl -u kubelet -n 100
dmesg | tail -50
df -h
top
```

**Use cases:**
- Node-level issues (disk full, high load)
- Kubelet not working
- Container runtime issues
- Kernel problems

## Docker Container Debugging

### Exec into Running Container

```bash
# Basic exec
docker exec -it <container-id> sh

# Run specific command
docker exec <container-id> ps aux
docker exec <container-id> netstat -tuln
```

### Debugging Containers Without Shell

**Create debug container sharing namespaces:**
```bash
# Share PID namespace
docker run -it --pid=container:<container-id> busybox sh

# Share network namespace
docker run -it --net=container:<container-id> nicolaka/netshoot

# Share both PID and network
docker run -it \
  --pid=container:<container-id> \
  --net=container:<container-id> \
  busybox sh
```

### Inspecting Stopped Container

```bash
# View logs
docker logs <container-id>

# Export filesystem
docker export <container-id> > container-fs.tar

# Inspect container config
docker inspect <container-id>
```

### Debugging at Build Time

```dockerfile
# Add debug tools temporarily
FROM myapp:latest
RUN apt-get update && apt-get install -y curl netcat

# Or use multi-stage build
FROM myapp:latest as debug
RUN apt-get update && apt-get install -y debugging-tools

FROM myapp:latest as production
# Minimal production image
```

## Common Debugging Scenarios

### Scenario 1: Pod CrashLoopBackOff

**Diagnosis:**
```bash
# Check pod status
kubectl get pod <pod-name> -o wide

# View logs (current container)
kubectl logs <pod-name>

# View logs (previous container)
kubectl logs <pod-name> --previous

# Describe pod for events
kubectl describe pod <pod-name>

# If container exits too fast, change entrypoint
kubectl debug <pod-name> -it --image=<same-image> \
  --copy-to=debug-pod \
  -- sh -c "while true; do sleep 1000; done"
```

### Scenario 2: Network Connectivity Issues

**Diagnosis:**
```bash
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Test DNS
nslookup kubernetes.default
nslookup <service-name>

# Test connectivity
curl http://<service-name>:<port>
telnet <service-name> <port>

# Check routes
route -n
ip route

# Capture traffic
tcpdump -i eth0 -w capture.pcap
```

### Scenario 3: Application Not Responding

**Diagnosis:**
```bash
kubectl debug -it <pod-name> \
  --image=busybox \
  --target=app \
  --share-processes

# Check if process is running
ps aux | grep myapp

# Check resource usage
top

# Check file handles
ls -la /proc/<pid>/fd

# Send signal to process
kill -SIGUSR1 <pid>  # Trigger heap dump, etc.
```

### Scenario 4: Distroless Image Investigation

**Diagnosis:**
```bash
kubectl debug -it <distroless-pod> \
  --image=busybox \
  --target=app \
  --share-processes

# Inspect process
ps aux

# Check environment
cat /proc/<pid>/environ | tr '\0' '\n'

# View open files
ls -la /proc/<pid>/fd

# Check network connections
netstat -tuln
```

### Scenario 5: Performance Issues

**Diagnosis:**
```bash
kubectl debug -it <pod-name> \
  --image=ubuntu \
  --target=app \
  --share-processes

# Install perf tools
apt-get update && apt-get install -y sysstat

# Check CPU usage
top
mpstat 1 10

# Check I/O
iostat -x 1 10

# Memory usage
free -m
cat /proc/<pid>/status | grep -i rss
```

## Advanced Techniques

### Copy Pod for Debugging

**Create copy with modified settings:**
```bash
kubectl debug <pod-name> \
  --copy-to=debug-pod \
  --image=myapp:debug \
  --set-image=app=myapp:debug
```

**Use cases:**
- Test different image version
- Change environment variables
- Modify command/args
- Debug without affecting running pod

### Debugging Init Containers

```bash
# View init container logs
kubectl logs <pod-name> -c <init-container-name>

# Debug pod with init container issue
kubectl debug <pod-name> --copy-to=debug-pod
kubectl describe pod debug-pod
```

### Profile Running Process

```bash
kubectl debug -it <pod-name> \
  --image=ubuntu \
  --target=app \
  --share-processes

# Install profiling tools
apt-get update && apt-get install -y linux-tools-generic

# Profile CPU (requires capabilities)
perf record -p <pid> -g -- sleep 30
perf report
```

### Capture Network Traffic

```bash
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Capture to file
tcpdump -i eth0 -w /tmp/capture.pcap

# Copy to local machine (from another terminal)
kubectl cp <pod-name>:/tmp/capture.pcap ./capture.pcap

# Analyze with Wireshark
wireshark capture.pcap
```

## Best Practices

### 1. Try kubectl exec First

```bash
# Simpler if it works
kubectl exec -it <pod-name> -- sh
```

### 2. Use Appropriate Debug Image

- **Network issues** → nicolaka/netshoot
- **Process inspection** → busybox (minimal)
- **Package installation needed** → ubuntu/alpine

### 3. Share Process Namespace When Needed

```bash
# To see target container processes
--target=app --share-processes
```

### 4. Clean Up Debug Pods

```bash
# Ephemeral containers are auto-removed
# But if using --copy-to:
kubectl delete pod debug-pod
```

### 5. Don't Modify Images for Debugging

**Bad:**
```dockerfile
# Adding debug tools to production image
RUN apt-get install -y curl tcpdump strace
```

**Good:**
```bash
# Use ephemeral containers instead
kubectl debug -it <pod> --image=nicolaka/netshoot
```

### 6. Check Logs Before Debugging

```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
```

### 7. Use describe for Events

```bash
kubectl describe pod <pod-name>
# Check Events section for errors
```

### 8. Security Considerations

**Don't expose debug capabilities in production:**
- Limit who can use kubectl debug
- Remove debug images after use
- Avoid leaving debug pods running
- Use RBAC to control access

### 9. Document Debugging Procedures

**Create runbooks:**
```markdown
## Network Issue Debugging

1. kubectl debug -it <pod> --image=nicolaka/netshoot
2. nslookup <service>
3. curl <service>:<port>
4. tcpdump if needed
```

### 10. Use Ephemeral Containers in CI/CD

**Test distroless images:**
```bash
# In CI pipeline
kubectl apply -f deployment.yaml
kubectl wait --for=condition=ready pod -l app=myapp
kubectl debug -it <pod> --image=busybox --target=app
# Run smoke tests from debug container
```
