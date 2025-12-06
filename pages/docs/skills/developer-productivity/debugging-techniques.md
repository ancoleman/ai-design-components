---
sidebar_position: 5
title: Debugging Techniques
description: Systematic debugging workflows for Python, Go, Rust, Node.js, containers, and production environments
tags: [developer-productivity, debugging, pdb, delve, lldb, kubernetes, production]
---

# Debugging Techniques

Systematic debugging workflows for local, remote, container, and production environments across Python, Go, Rust, and Node.js. Covers interactive debuggers, container debugging with ephemeral containers, and production-safe techniques using correlation IDs and distributed tracing.

## When to Use

Use when:
- Setting breakpoints in Python, Go, Rust, or Node.js code
- Debugging running containers or Kubernetes pods
- Setting up remote debugging connections
- Safely debugging production issues
- Inspecting goroutines, threads, or async tasks
- Analyzing core dumps or stack traces
- Choosing the right debugging tool for a scenario

## Key Features

- **Multi-Language Debuggers**: pdb/debugpy (Python), delve (Go), lldb (Rust), node --inspect (Node.js)
- **Container Debugging**: kubectl debug with ephemeral containers, Docker exec
- **Production Debugging**: Structured logging, correlation IDs, distributed tracing
- **Goroutine Inspection**: Debug concurrent Go programs
- **Remote Debugging**: SSH tunnels, VS Code remote debugging
- **Interactive Tools**: Progress indicators, step-through debugging, variable inspection

## Quick Start

### Python Debugging

```python
def buggy_function(x, y):
    breakpoint()  # Python 3.7+ - stops execution here
    return x / y

# Older Python
import pdb
pdb.set_trace()
```

**Essential pdb commands:**
- `list` (l) - Show code around current line
- `next` (n) - Execute current line, step over functions
- `step` (s) - Execute current line, step into functions
- `print var` (p) - Print variable value
- `continue` (c) - Continue until next breakpoint
- `where` (w) - Show stack trace

**Debugging tests:**
```bash
pytest --pdb  # Drop into debugger on test failure
```

### Go Debugging with Delve

```bash
# Installation
go install github.com/go-delve/delve/cmd/dlv@latest

# Usage
dlv debug main.go              # Debug main package
dlv test github.com/me/pkg     # Debug test suite
dlv attach <pid>               # Attach to running process
```

**Essential commands:**
- `break main.main` (b) - Set breakpoint at function
- `break file.go:10` - Set breakpoint at line
- `continue` (c) - Continue execution
- `print x` (p) - Print variable
- `goroutines` (grs) - List all goroutines
- `goroutines -t` - Show goroutine stacktraces

**Goroutine debugging:**
```bash
(dlv) goroutines                 # List all goroutines
(dlv) goroutines -t              # Show stacktraces
(dlv) goroutine 5                # Switch to goroutine 5
```

### Rust Debugging with LLDB

```bash
# Compilation (debug build includes symbols)
cargo build

# Usage
rust-lldb target/debug/myapp   # LLDB wrapper for Rust
rust-gdb target/debug/myapp    # GDB wrapper (alternative)
```

**Essential LLDB commands:**
- `breakpoint set -f main.rs -l 10` - Set breakpoint at line
- `run` (r) - Start program
- `next` (n) - Step over
- `print variable` (p) - Print variable
- `backtrace` (bt) - Show stack trace

### Node.js Debugging

```bash
# Start with debugger
node --inspect-brk app.js       # Start and pause immediately
node --inspect app.js           # Start and run
node --inspect=0.0.0.0:9229 app.js  # Specify host/port
```

**Chrome DevTools:**
1. Open `chrome://inspect`
2. Click "Open dedicated DevTools for Node"
3. Set breakpoints, inspect variables

## Container & Kubernetes Debugging

### kubectl debug with Ephemeral Containers

**When to use:**
- Container has crashed (kubectl exec won't work)
- Using distroless/minimal image (no shell, no tools)
- Need debugging tools without rebuilding image
- Debugging network issues

**Basic usage:**
```bash
# Add ephemeral debugging container
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Share process namespace (see other container processes)
kubectl debug -it <pod-name> --image=busybox --share-processes

# Target specific container
kubectl debug -it <pod-name> --image=busybox --target=app
```

**Recommended debugging images:**
- `nicolaka/netshoot` (~380MB) - Network debugging (curl, dig, tcpdump, netstat)
- `busybox` (~1MB) - Minimal shell and utilities
- `alpine` (~5MB) - Lightweight with package manager
- `ubuntu` (~70MB) - Full environment

**Example workflow:**
```bash
# Step 1: Check pod status
kubectl get pod my-app-pod -o wide

# Step 2: Check logs first
kubectl logs my-app-pod

# Step 3: Add ephemeral container if logs insufficient
kubectl debug -it my-app-pod --image=nicolaka/netshoot

# Step 4: Inside debug container, investigate
curl localhost:8080
netstat -tuln
nslookup api.example.com
```

## Production Debugging

### Production Debugging Principles

**Golden rules:**
1. **Minimal performance impact** - Profile overhead, limit scope
2. **No blocking operations** - Use non-breaking techniques
3. **Security-aware** - Avoid logging secrets, PII
4. **Reversible** - Can roll back quickly (feature flags, Git)
5. **Observable** - Structured logging, correlation IDs, tracing

### Safe Production Techniques

**1. Structured Logging**
```python
import logging
import json

logger = logging.getLogger(__name__)
logger.info(json.dumps({
    "event": "user_login_failed",
    "user_id": user_id,
    "error": str(e),
    "correlation_id": request_id
}))
```

**2. Correlation IDs (Request Tracing)**
```go
func handleRequest(w http.ResponseWriter, r *http.Request) {
    correlationID := r.Header.Get("X-Correlation-ID")
    if correlationID == "" {
        correlationID = generateUUID()
    }
    ctx := context.WithValue(r.Context(), "correlationID", correlationID)
    log.Printf("[%s] Processing request", correlationID)
}
```

**3. Distributed Tracing (OpenTelemetry)**
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        span.add_event("Order validated")
```

**Production debugging workflow:**
1. **Detect** - Error tracking alert, log spike, metric anomaly
2. **Locate** - Find correlation ID, search logs, view distributed trace
3. **Reproduce** - Try to reproduce in staging with production data (sanitized)
4. **Fix** - Create feature flag, deploy to canary first
5. **Verify** - Check error rates, review logs, monitor traces

## Decision Framework

### Which Debugger for Which Language?

| Language | Primary Tool | Installation | Best For |
|----------|-------------|--------------|----------|
| **Python** | pdb | Built-in | Simple scripts, server environments |
| | ipdb | `pip install ipdb` | Enhanced UX, IPython users |
| | debugpy | VS Code extension | IDE integration, remote debugging |
| **Go** | delve | `go install github.com/go-delve/delve/cmd/dlv@latest` | All Go debugging, goroutines |
| **Rust** | rust-lldb | System package | Mac, Linux, MSVC Windows |
| **Node.js** | node --inspect | Built-in | All Node.js debugging, Chrome DevTools |

### Which Technique for Which Scenario?

| Scenario | Recommended Technique | Tools |
|----------|----------------------|-------|
| Local development | Interactive debugger | pdb, delve, lldb, node --inspect |
| Bug in test | Test-specific debugging | pytest --pdb, dlv test |
| Kubernetes pod | Ephemeral container | kubectl debug --image=nicolaka/netshoot |
| Distroless image | Ephemeral container (required) | kubectl debug with busybox/alpine |
| Production issue | Log analysis + error tracking | Structured logs, Sentry, correlation IDs |
| Goroutine deadlock | Goroutine inspection | delve goroutines -t |
| Distributed failure | Distributed tracing | OpenTelemetry, Jaeger |

## Related Skills

- [Building CLIs](./building-clis) - CLI testing and debugging
- [Designing APIs](./designing-apis) - API debugging and tracing
- [Managing Git Workflows](./managing-git-workflows) - Git bisect for debugging
- [Writing GitHub Actions](./writing-github-actions) - CI/CD debugging

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/debugging-techniques)
