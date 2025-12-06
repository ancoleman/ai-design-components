# Debugging Decision Trees

## Table of Contents

1. [Which Debugger to Use?](#which-debugger-to-use)
2. [Which Technique for Which Problem?](#which-technique-for-which-problem)
3. [Container Debugging Decision Tree](#container-debugging-decision-tree)
4. [Production Debugging Decision Tree](#production-debugging-decision-tree)
5. [Quick Reference Matrix](#quick-reference-matrix)

## Which Debugger to Use?

### By Language

```
Is the language...

├─ Python?
│  ├─ Simple script? → pdb (built-in, use breakpoint())
│  ├─ Need better UX? → ipdb (enhanced pdb with IPython)
│  ├─ Want visual UI? → pudb (terminal-based GUI)
│  ├─ VS Code user? → debugpy (built into Python extension)
│  └─ PyCharm user? → Built-in debugger
│
├─ Go?
│  ├─ CLI debugging? → delve (dlv debug, dlv test)
│  ├─ VS Code user? → delve (via Go extension)
│  ├─ GoLand user? → Built-in debugger (uses delve)
│  └─ Goroutine debugging? → delve (first-class support)
│
├─ Rust?
│  ├─ Mac/Linux? → rust-lldb (default choice)
│  ├─ Windows/prefer GDB? → rust-gdb
│  ├─ VS Code user? → CodeLLDB extension
│  ├─ IntelliJ Rust? → Built-in debugger
│  └─ Compile with: cargo build (debug symbols default)
│
└─ Node.js?
   ├─ CLI debugging? → node --inspect or node --inspect-brk
   ├─ VS Code user? → Built-in debugger (attach mode)
   ├─ Chrome user? → chrome://inspect (DevTools)
   └─ Need remote? → node --inspect=0.0.0.0:9229
```

### By Environment

```
Where is the code running?

├─ Local development?
│  └─ Use interactive debugger (pdb, delve, lldb, node --inspect)
│
├─ Remote server?
│  ├─ SSH available? → SSH tunnel + remote attach
│  │  └─ VS Code Remote, debugpy, delve headless
│  └─ No SSH? → Log-based debugging, error tracking
│
├─ Container (local)?
│  ├─ Has shell? → docker exec -it + debugger
│  └─ No shell? → docker run with shared namespaces + debugger
│
├─ Kubernetes pod?
│  ├─ kubectl exec works? → kubectl exec -it <pod> -- sh
│  ├─ Pod crashed? → kubectl debug with ephemeral container
│  ├─ Distroless image? → kubectl debug (required)
│  └─ Network issue? → kubectl debug --image=nicolaka/netshoot
│
└─ Production?
   ├─ Error tracking enabled? → Use Sentry/New Relic dashboard
   ├─ Have correlation ID? → Search logs, view distributed trace
   ├─ Can reproduce in staging? → Debug in staging (safer)
   └─ Must debug live? → Non-breaking techniques only
      ├─ Tracepoints (non-blocking)
      ├─ Additional logging (temporary)
      └─ Snapshot debugging (if available)
```

## Which Technique for Which Problem?

### By Problem Type

```
What kind of issue?

├─ Logical error (wrong result)?
│  └─ Interactive debugger
│     ├─ Set breakpoint before wrong calculation
│     ├─ Inspect variables
│     ├─ Step through logic
│     └─ Identify incorrect condition/algorithm
│
├─ Runtime error (exception/panic)?
│  ├─ Stack trace available? → Analyze stack trace
│  ├─ Post-mortem debugging? → Core dump analysis (gdb, lldb)
│  └─ Can reproduce? → Interactive debugger with breakpoint before error
│
├─ Concurrency issue?
│  ├─ Go goroutine? → delve goroutines -t
│  ├─ Rust thread? → lldb thread list
│  ├─ Race condition? → Race detector (go run -race, cargo test)
│  └─ Deadlock? → Inspect all threads/goroutines for blocking
│
├─ Performance issue (slowness)?
│  └─ See performance-engineering skill (profiling, not debugging)
│
├─ Integration issue (API/network)?
│  ├─ Container? → kubectl debug with netshoot
│  ├─ Distributed? → Distributed tracing (OpenTelemetry)
│  └─ Request failing? → Correlation ID + log search
│
└─ Intermittent issue (flaky)?
   ├─ Conditional breakpoint → Break only when condition met
   ├─ Tracepoint → Log without stopping (delve, lldb)
   └─ Comprehensive logging → Capture state over many runs
```

### By Debugging Goal

```
What do you want to do?

├─ Understand code flow?
│  └─ Step debugging (step into functions)
│
├─ Inspect variable values?
│  ├─ Breakpoint + print command
│  └─ Watch expressions (IDE)
│
├─ Find where error occurs?
│  ├─ Stack trace analysis
│  └─ Breakpoint on exception (Python: --pdb)
│
├─ Test hypothesis about bug?
│  ├─ Conditional breakpoint
│  └─ Modify variable (delve set, lldb expr)
│
├─ Track request across services?
│  ├─ Correlation ID + log search
│  └─ Distributed tracing (Jaeger)
│
└─ Debug without stopping execution?
   ├─ Tracepoints (delve, lldb)
   ├─ Non-breaking breakpoints
   └─ Additional logging
```

## Container Debugging Decision Tree

```
Container debugging scenario:

├─ Can use kubectl exec?
│  └─ YES: kubectl exec -it <pod> -- sh (simplest)
│
├─ Container crashed?
│  └─ YES: kubectl debug (kubectl exec won't work)
│
├─ Distroless/minimal image?
│  └─ YES: kubectl debug with full-featured image (required)
│
├─ Need debugging tools?
│  ├─ Network debugging? → nicolaka/netshoot (curl, tcpdump, dig)
│  ├─ Minimal inspection? → busybox (~1MB, basic tools)
│  ├─ Package installation? → alpine (~5MB, apk) or ubuntu (~70MB, apt)
│  └─ Process inspection? → Use --share-processes --target=<container>
│
├─ Node-level issue?
│  └─ YES: kubectl debug node/<node-name>
│     └─ Access node filesystem at /host
│
└─ Docker (not K8s)?
   ├─ Has shell? → docker exec -it <container> sh
   └─ No shell? → docker run --pid=container:<id> --net=container:<id>
```

## Production Debugging Decision Tree

```
Production debugging scenario:

├─ Have error alert?
│  ├─ From Sentry/New Relic? → Check error dashboard
│  │  └─ Copy correlation ID from error report
│  │
│  ├─ From logs? → Identify correlation ID
│  │  └─ Search for correlation ID in log aggregation
│  │
│  └─ From metrics? → Correlate with logs/traces
│
├─ Have correlation ID?
│  ├─ YES: Search logs for correlation ID
│  │  └─ View entire request flow
│  │     └─ View distributed trace (if available)
│  │
│  └─ NO: Use timestamp + approximate request
│     └─ Search logs by time range
│
├─ Can reproduce in staging?
│  ├─ YES: Reproduce in staging (safer)
│  │  ├─ Add additional logging if needed
│  │  ├─ Use interactive debugger
│  │  └─ Test fix before deploying
│  │
│  └─ NO: Production-specific issue
│     ├─ Add temporary logging (structured, no secrets)
│     ├─ Use tracepoints (non-breaking)
│     └─ Monitor error tracking for new info
│
├─ Need to deploy fix?
│  ├─ Use feature flag → Gradual rollout
│  │  └─ Enable for 1% → 10% → 50% → 100%
│  │
│  ├─ Use canary deployment → Deploy to subset
│  │  └─ Monitor error rates closely
│  │
│  └─ Have rollback plan?
│     └─ YES: Deploy and monitor
│
└─ After fix deployed:
   ├─ Check error tracking (errors resolved?)
   ├─ Review logs (successful requests?)
   ├─ Monitor distributed traces (latency OK?)
   └─ Watch metrics (error rate decreased?)
```

## Quick Reference Matrix

### Debugging Technique Selection

| Scenario | Recommended Technique | Tools | When to Use |
|----------|----------------------|-------|-------------|
| **Local development** | Interactive debugger | pdb, delve, lldb, node --inspect | Writing/testing code locally |
| **Bug in test** | Test-specific debugging | pytest --pdb, dlv test, cargo test | Test failure investigation |
| **Remote server** | SSH tunnel + remote attach | VS Code Remote, debugpy, delve headless | Debugging on dev/staging server |
| **Container (local)** | docker exec -it | sh/bash + debugger | Local Docker development |
| **Kubernetes pod** | Ephemeral container | kubectl debug --image=nicolaka/netshoot | Pod has no shell or tools |
| **Distroless image** | Ephemeral container (required) | kubectl debug with busybox/alpine | Cannot exec into distroless |
| **Production issue** | Log analysis + error tracking | Structured logs, Sentry, correlation IDs | User-reported production bug |
| **Goroutine deadlock** | Goroutine inspection | delve goroutines -t | Go concurrency issue |
| **Crashed process** | Core dump analysis | gdb core, lldb -c core | Post-mortem debugging |
| **Distributed failure** | Distributed tracing | OpenTelemetry, Jaeger, correlation IDs | Multi-service issue |
| **Race condition** | Race detector + debugger | go run -race, cargo test | Intermittent concurrency bug |
| **Network issue** | Network debugging tools | kubectl debug --image=netshoot | DNS, connectivity, latency |

### Problem Type → Primary Tool

| Problem Type | Primary Tool | Secondary Tool | Notes |
|--------------|-------------|----------------|-------|
| Logic error | Interactive debugger | Print debugging | Step through code, inspect variables |
| Exception/panic | Stack trace analysis | Post-mortem debugger | Analyze call stack first |
| Concurrency | Thread/goroutine inspector | Race detector | Check all threads/goroutines |
| Performance | Profiler (not debugger) | System monitoring | See performance-engineering skill |
| Integration | Distributed tracing | Log correlation | Track across services |
| Intermittent | Conditional breakpoint | Extensive logging | Break only when triggered |
| Container | kubectl debug | docker exec | Ephemeral containers for minimal images |
| Production | Log analysis | Error tracking platform | Never use blocking debuggers |

### Environment → Access Method

| Environment | Access Method | Prerequisites | Tools Available |
|-------------|--------------|---------------|-----------------|
| Local machine | Direct execution | None | All debuggers |
| Remote server (SSH) | SSH tunnel | SSH access | Remote debuggers |
| Docker container | docker exec / shared namespaces | Docker access | Shell + debuggers |
| K8s pod (with shell) | kubectl exec | kubectl access | Shell + debuggers |
| K8s pod (minimal) | Ephemeral container | kubectl debug access | Debugging image tools |
| K8s node | Node debugging | Admin kubectl access | Node filesystem + tools |
| Production | Logs + traces | Observability setup | No interactive debuggers |
