# Profiling Guide

## Table of Contents

1. [Profiling Fundamentals](#profiling-fundamentals)
2. [CPU Profiling](#cpu-profiling)
3. [Memory Profiling](#memory-profiling)
4. [I/O Profiling](#io-profiling)
5. [Profiling Workflow](#profiling-workflow)
6. [Analyzing Flamegraphs](#analyzing-flamegraphs)
7. [Production Profiling](#production-profiling)
8. [Language-Specific Guides](#language-specific-guides)

---

## Profiling Fundamentals

### What is Profiling?

Profiling measures where a program spends time and resources. Unlike load testing (which tests system behavior under load), profiling provides detailed insights into code execution.

**Key questions profiling answers:**
- Which functions use the most CPU time?
- Where are memory allocations happening?
- What's causing slow I/O operations?
- Which code paths are hot (frequently executed)?

### Profiling vs. Load Testing

| Aspect | Load Testing | Profiling |
|--------|--------------|-----------|
| **Purpose** | Validate system capacity | Identify code-level bottlenecks |
| **Scope** | System-level (throughput, latency) | Function-level (CPU, memory, I/O) |
| **Output** | Metrics (RPS, p95 latency) | Flamegraphs, call stacks |
| **When** | Before launch, regression testing | After identifying slow performance |
| **Tool Examples** | k6, Locust | pprof, py-spy, Chrome DevTools |

**Workflow:** Load test identifies slow endpoints → Profiling identifies which functions cause slowness.

### Profiling Types

#### CPU Profiling
Measures where program spends CPU cycles.

**When to use:**
- High CPU usage (>70%)
- Slow response times with low I/O wait
- Hot path optimization

**Output:** Functions ranked by CPU time consumed.

#### Memory Profiling
Tracks memory allocations and heap usage.

**When to use:**
- Memory usage growing over time
- Out-of-memory errors
- High garbage collection overhead

**Output:** Allocation sites, heap snapshots, memory growth trends.

#### I/O Profiling
Identifies slow database queries, network calls, filesystem operations.

**When to use:**
- High I/O wait time
- Slow response times with low CPU usage
- Database connection exhaustion

**Output:** Query execution times, network latency, file I/O throughput.

### Sampling vs. Instrumentation Profiling

**Sampling Profiling (py-spy, pprof):**
- Periodically samples program state (every 10ms)
- Low overhead (~1-5%)
- Production-safe
- May miss short-lived functions

**Instrumentation Profiling (cProfile):**
- Records every function call
- High overhead (10-50%)
- More accurate
- Not recommended for production

**Recommendation:** Use sampling profilers (py-spy, pprof) in production, instrumentation profilers in development.

---

## CPU Profiling

### When to CPU Profile

**Symptoms:**
- High CPU usage (>70% sustained)
- Slow response times with low I/O wait
- High load average
- Users reporting slow application

**Not CPU-bound if:**
- CPU usage < 50%
- High I/O wait time
- Slow database queries

### CPU Profiling Process

1. **Reproduce slow behavior:** Load test or real traffic
2. **Start CPU profiler:** Capture profile for 30-60 seconds
3. **Analyze profile:** Identify hot functions (top 20% using 80% CPU)
4. **Optimize hot paths:** Focus on most expensive functions
5. **Re-profile:** Validate improvement

### Python CPU Profiling

#### py-spy (Recommended, Production-Safe)

**Installation:**
```bash
pip install py-spy
```

**Usage:**
```bash
# Profile running process (30 seconds)
py-spy record -o profile.svg --pid <PID> --duration 30

# Top-like view of functions
py-spy top --pid <PID>

# Profile command
py-spy record -o profile.svg -- python app.py

# Flamegraph output (open in browser)
py-spy record -o profile.svg --format speedscope --pid <PID>
```

**Interpreting output:**
- Flamegraph shows call stack (bottom = callers, top = callees)
- Wider bars = more CPU time
- Look for wide bars (hot functions)

#### cProfile (Instrumentation Profiler)

**Usage:**
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
my_function()

profiler.disable()

# Print stats (sorted by cumulative time)
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

**Output interpretation:**
```
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000    0.050    0.000    0.150    0.000 module.py:10(process_data)
```

- **ncalls:** Number of calls
- **tottime:** Total time in function (excluding subcalls)
- **cumtime:** Cumulative time (including subcalls)
- **percall:** Time per call

**Optimization priority:** Sort by `cumtime` (cumulative time).

### Go CPU Profiling

#### pprof (Built-in)

**Enable pprof HTTP server:**
```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()

    startApp()
}
```

**Capture CPU profile:**
```bash
# 30-second CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Interactive analysis
(pprof) top
(pprof) list functionName
(pprof) web  # Open flamegraph in browser
```

**Programmatic profiling:**
```go
import (
    "os"
    "runtime/pprof"
)

func profileCPU() {
    f, _ := os.Create("cpu.prof")
    defer f.Close()

    pprof.StartCPUProfile(f)
    defer pprof.StopCPUProfile()

    // Code to profile
    doWork()
}
```

**Analyze profile:**
```bash
go tool pprof cpu.prof

# Commands:
(pprof) top      # Top functions by CPU
(pprof) list fn  # Source code with CPU annotations
(pprof) web      # Flamegraph
```

### TypeScript/JavaScript CPU Profiling

#### Chrome DevTools (Browser/Node.js)

**Browser:**
1. Open Chrome DevTools (F12)
2. Performance tab → Record
3. Perform slow actions
4. Stop recording
5. Analyze flamegraph (bottom-up view)

**Node.js:**
```bash
# Start Node with inspector
node --inspect app.js

# Open chrome://inspect in Chrome
# Click "Open dedicated DevTools for Node"
# Go to Performance tab → Record
```

#### clinic.js (Node.js)

**Installation:**
```bash
npm install -g clinic
```

**Usage:**
```bash
# CPU profiling
clinic doctor -- node app.js

# Flamegraph
clinic flame -- node app.js

# Interactive HTML report generated
```

### CPU Profiling Best Practices

- Profile under realistic load (not idle)
- Profile for 30-60 seconds (capture representative sample)
- Focus on hot paths (top 20% of functions)
- Optimize biggest bottlenecks first (Amdahl's Law)
- Avoid premature optimization (profile before optimizing)
- Re-profile after changes (validate improvement)

---

## Memory Profiling

### When to Memory Profile

**Symptoms:**
- Memory usage growing over time
- Out-of-memory errors (OOM)
- High garbage collection (GC) overhead
- Swap usage increasing
- Application restarts due to memory

**Memory leak indicators:**
- Memory usage grows linearly with time
- Memory doesn't decrease after load reduction
- GC cannot reclaim memory

### Python Memory Profiling

#### memory_profiler (Line-by-Line)

**Installation:**
```bash
pip install memory-profiler
```

**Usage:**
```python
from memory_profiler import profile

@profile
def my_function():
    a = [1] * (10 ** 6)        # 1M integers
    b = [2] * (2 * 10 ** 7)    # 20M integers
    del b
    return a

# Run with: python -m memory_profiler script.py
```

**Output:**
```
Line #    Mem usage    Increment  Line Contents
================================================
     3     10.0 MiB     10.0 MiB   @profile
     4     17.6 MiB      7.6 MiB   a = [1] * (10 ** 6)
     5    165.2 MiB    147.6 MiB   b = [2] * (2 * 10 ** 7)
     6     17.6 MiB   -147.6 MiB   del b
     7     17.6 MiB      0.0 MiB   return a
```

#### tracemalloc (Built-in)

**Usage:**
```python
import tracemalloc

# Start tracking
tracemalloc.start()

# Code to profile
run_application()

# Get snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

# Print top 10 allocation sites
for stat in top_stats[:10]:
    print(stat)
```

#### Pympler (Detailed Object Tracking)

**Installation:**
```bash
pip install pympler
```

**Usage:**
```python
from pympler import asizeof, tracker

# Track memory allocations
tr = tracker.SummaryTracker()

# Code to profile
run_code()

# Print differences
tr.print_diff()

# Get object size
size = asizeof.asizeof(my_object)
```

### Go Memory Profiling

#### pprof Heap Profiling

**Capture heap profile:**
```bash
# Heap allocation profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Interactive analysis
(pprof) top
(pprof) list functionName
(pprof) web
```

**Programmatic heap profiling:**
```go
import (
    "os"
    "runtime/pprof"
)

func profileHeap() {
    f, _ := os.Create("heap.prof")
    defer f.Close()

    pprof.WriteHeapProfile(f)
}
```

**Memory statistics:**
```go
import "runtime"

var m runtime.MemStats
runtime.ReadMemStats(&m)

fmt.Printf("Alloc = %v MiB", m.Alloc / 1024 / 1024)
fmt.Printf("TotalAlloc = %v MiB", m.TotalAlloc / 1024 / 1024)
fmt.Printf("Sys = %v MiB", m.Sys / 1024 / 1024)
fmt.Printf("NumGC = %v\n", m.NumGC)
```

### TypeScript/JavaScript Memory Profiling

#### Chrome DevTools Heap Snapshot

**Browser:**
1. Open Chrome DevTools (F12)
2. Memory tab → Heap snapshot
3. Take snapshot
4. Perform actions (allocate memory)
5. Take another snapshot
6. Compare snapshots (identify retained objects)

**Node.js:**
```bash
node --inspect app.js

# Open chrome://inspect
# Memory tab → Heap snapshot
```

**Finding leaks:**
- Compare snapshots before/after operations
- Look for objects retained unexpectedly
- Check for event listeners not removed
- Identify closures holding references

#### clinic.js Heap Profiling

```bash
npm install -g clinic

# Memory profiling
clinic heapprofiler -- node app.js

# Interactive report
```

### Memory Profiling Best Practices

- Take snapshots at different times (compare growth)
- Run soak tests to detect leaks (24+ hours)
- Focus on objects retained unexpectedly
- Check for common leak patterns:
  - Event listeners not removed
  - Timers not cleared (setInterval)
  - Closures holding large references
  - Caches without eviction
  - Connection pools not closed
- Validate fixes with soak tests

---

## I/O Profiling

### When to I/O Profile

**Symptoms:**
- Slow response times with low CPU usage
- High I/O wait time
- Database connection pool exhaustion
- Slow database queries
- High network latency

**I/O bottleneck indicators:**
- CPU usage < 50%
- I/O wait time > 20%
- Slow queries in database logs
- High latency in APM traces

### Database Query Profiling

#### Python (Django Debug Toolbar)

**Installation:**
```bash
pip install django-debug-toolbar
```

**Configuration:**
```python
# settings.py
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
```

**Usage:**
- View SQL queries in web UI
- Identify N+1 queries
- Analyze query execution time
- View query EXPLAIN plans

#### Python (SQLAlchemy Query Logging)

```python
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Now see all queries in logs
```

#### Go (Database Query Logging)

```go
import (
    "database/sql"
    _ "github.com/lib/pq"
    "log"
)

// Log slow queries
func logSlowQuery(query string, duration time.Duration) {
    if duration > 100*time.Millisecond {
        log.Printf("SLOW QUERY (%v): %s", duration, query)
    }
}
```

### Network Profiling

#### Go (pprof Block Profile)

```bash
# Block profiling (I/O wait, mutex contention)
go tool pprof http://localhost:6060/debug/pprof/block

# Analyze goroutines waiting on I/O
(pprof) top
(pprof) list functionName
```

#### TypeScript/JavaScript (Chrome DevTools Network Tab)

**Browser:**
1. Open Chrome DevTools (F12)
2. Network tab
3. Perform actions
4. Analyze:
   - Request waterfall (dependencies)
   - Request timing (TTFB, download)
   - Large requests (>1MB)
   - Slow requests (>1s)

### Filesystem I/O Profiling

#### Python (asyncio Profiler)

```python
import asyncio

# Enable asyncio debug mode
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()
loop.set_debug(True)

# See slow callbacks in logs
```

#### Go (pprof Block Profile)

```bash
# Capture block profile (includes filesystem I/O)
curl http://localhost:6060/debug/pprof/block > block.prof
go tool pprof block.prof
```

### I/O Profiling Best Practices

- Profile under realistic load (I/O issues show under concurrency)
- Identify N+1 queries (common in ORMs)
- Use database query logs (enable slow query log)
- Analyze query EXPLAIN plans
- Check connection pool size (exhaustion = queuing)
- Monitor network latency (APM tools)
- Use distributed tracing (correlate service calls)

---

## Profiling Workflow

### Standard Process

1. **Observe Symptoms**
   - Metrics: High CPU, memory growth, slow response times
   - Logs: Errors, warnings, slow queries
   - User reports: Slow pages, timeouts

2. **Hypothesize Bottleneck**
   - High CPU → CPU profiling
   - Memory growth → Memory profiling
   - Slow response, low CPU → I/O profiling

3. **Choose Profiling Type**
   - CPU: py-spy, pprof, Chrome DevTools
   - Memory: memory_profiler, pprof heap, Chrome heap snapshot
   - I/O: Query logs, pprof block, network tab

4. **Run Profiler Under Load**
   - Reproduce production conditions
   - Use load testing tools (k6, Locust)
   - Capture profile for 30-60 seconds

5. **Analyze Profile**
   - Flamegraph: Identify hot paths
   - Call tree: Find expensive call chains
   - Top functions: Focus on biggest offenders

6. **Identify Hot Spots**
   - Top 20% functions using 80% resources
   - Unexpected allocations
   - N+1 queries
   - Slow external calls

7. **Optimize Bottlenecks**
   - Algorithmic improvements
   - Caching
   - Database query optimization
   - Connection pooling

8. **Re-Profile to Validate**
   - Measure improvement (before/after)
   - Ensure no regressions
   - Repeat if needed

---

## Analyzing Flamegraphs

### What is a Flamegraph?

Flamegraphs visualize profiling data:
- X-axis: Width represents time spent (wider = more time)
- Y-axis: Call stack depth (bottom = root, top = leaves)
- Color: Typically random (no meaning, just visual aid)

### Reading Flamegraphs

**Structure:**
```
┌─────────────────────────────────────┐
│        leaf_function (10ms)         │  ← Actual work
├─────────────────────────────────────┤
│       intermediate_function (50ms)  │  ← Calls leaf
├─────────────────────────────────────┤
│       root_function (100ms)         │  ← Entry point
└─────────────────────────────────────┘
```

**Key patterns:**

**Wide bar at top (hot function):**
```
┌────────────────────────────┐
│  expensive_function (80%)  │  ← OPTIMIZE THIS
├────────────────────────────┤
│      caller (100%)         │
└────────────────────────────┘
```

**Many small bars (many functions):**
```
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│ │ │ │ │ │ │ │ │ │ │ │ │ │ │  ← Many small functions
├─────────────────────────────┤
│      caller (100%)          │
└─────────────────────────────┘
```
- Indicates overhead (function call cost)
- Consider inlining or batching

**Tall tower (deep call stack):**
```
│  leaf  │
│   ↓    │
│  mid   │
│   ↓    │
│  mid   │
│   ↓    │
│  root  │
```
- Deep recursion or abstraction layers
- Consider flattening call stack

### Optimization Priority

1. **Widest bars:** Most CPU time, highest impact
2. **Unexpected functions:** Shouldn't be hot (caching?)
3. **Repeated patterns:** Same function called multiple times (batch?)
4. **External calls:** Database, network (can they be reduced?)

---

## Production Profiling

### Safety Considerations

**Safe in production:**
- Sampling profilers (py-spy, pprof) - Low overhead (~1-5%)
- Short profiling sessions (30-60 seconds)
- Profiling subset of instances (not all at once)

**Avoid in production:**
- Instrumentation profilers (cProfile) - High overhead
- Long profiling sessions (hours) - Resource usage
- Profiling all instances simultaneously

### Continuous Profiling

**Tools:**
- **Grafana Pyroscope** (multi-language, open-source)
- **Google Cloud Profiler** (GCP, low overhead)
- **Datadog Profiler** (commercial APM)

**Benefits:**
- Always-on profiling (no manual sessions)
- Historical comparison (before/after deployments)
- Correlate with incidents (what changed?)
- Low overhead (1-2%)

**Setup (Pyroscope):**
```python
# Python
import pyroscope

pyroscope.configure(
    application_name="my-app",
    server_address="http://pyroscope:4040",
)
```

```go
// Go
import "github.com/pyroscope-io/client/pyroscope"

pyroscope.Start(pyroscope.Config{
    ApplicationName: "my-app",
    ServerAddress:   "http://pyroscope:4040",
})
```

### Production Profiling Best Practices

- Use sampling profilers only (low overhead)
- Profile for short durations (30-60 seconds)
- Profile subset of instances (canary profiling)
- Correlate with monitoring (metrics, logs)
- Store profiles for historical analysis
- Compare profiles before/after deployments
- Set up alerts for performance regressions

---

## Language-Specific Guides

### Python Profiling Summary

| Tool | Type | Overhead | Production-Safe | Output |
|------|------|----------|-----------------|--------|
| py-spy | Sampling CPU | Very Low | ✅ | Flamegraph |
| cProfile | Instrumentation CPU | Medium | ⚠️ | Stats table |
| memory_profiler | Line-by-line Memory | High | ❌ | Line annotations |
| tracemalloc | Memory snapshot | Low | ✅ | Allocation sites |

**Recommendation:** py-spy (CPU), tracemalloc (memory) for production.

### Go Profiling Summary

| Tool | Type | Overhead | Production-Safe | Output |
|------|------|----------|-----------------|--------|
| pprof (CPU) | Sampling CPU | Low | ✅ | Flamegraph |
| pprof (heap) | Memory snapshot | Low | ✅ | Allocation sites |
| pprof (goroutine) | Goroutine trace | Low | ✅ | Goroutine stacks |
| pprof (block) | I/O wait | Low | ✅ | Blocking calls |

**Recommendation:** pprof for all profiling (built-in, excellent).

### TypeScript/JavaScript Profiling Summary

| Tool | Type | Overhead | Production-Safe | Output |
|------|------|----------|-----------------|--------|
| Chrome DevTools | CPU + Memory | Low | ✅ (Node) | Timeline, flamegraph |
| clinic.js | CPU + Memory | Low | ✅ | Interactive HTML |
| 0x | Sampling CPU | Low | ✅ | Flamegraph |

**Recommendation:** Chrome DevTools (development), clinic.js (Node.js production).

---

## Profiling Checklist

### Before Profiling

- [ ] Define hypothesis (CPU? Memory? I/O?)
- [ ] Reproduce slow behavior (load test or real traffic)
- [ ] Choose appropriate profiler
- [ ] Ensure safe for production (if profiling prod)

### During Profiling

- [ ] Profile under realistic load
- [ ] Capture 30-60 seconds
- [ ] Monitor overhead (CPU, memory impact)
- [ ] Save profile output

### After Profiling

- [ ] Analyze flamegraph or stats
- [ ] Identify hot spots (top 20% functions)
- [ ] Prioritize optimizations (biggest impact first)
- [ ] Document findings
- [ ] Re-profile after optimizations (validate improvement)
