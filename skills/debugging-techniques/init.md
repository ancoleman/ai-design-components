# Debugging Techniques Skill - Master Plan

**Skill Name:** `debugging-techniques`
**Level:** Low Level (2,000-5,000 tokens, 300-500 lines)
**Status:** Planning Phase
**Created:** December 3, 2025
**Multi-Language:** Python, Go, Rust, Node.js

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Debugging Taxonomy](#debugging-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Python Debugging](#python-debugging)
7. [Go Debugging](#go-debugging)
8. [Rust Debugging](#rust-debugging)
9. [Node.js Debugging](#nodejs-debugging)
10. [Container & Kubernetes Debugging](#container--kubernetes-debugging)
11. [Production Debugging](#production-debugging)
12. [Tool Recommendations](#tool-recommendations)
13. [Skill Structure Design](#skill-structure-design)
14. [Integration Points](#integration-points)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Debugging is a universal engineering activity that directly impacts:
- **Development velocity** - Faster bug resolution = faster feature delivery
- **System reliability** - Better debugging = better understanding = fewer bugs
- **Developer experience** - Confidence in debugging tooling reduces stress
- **Production safety** - Safe debugging practices prevent outages

### Key Insights from Research

**General Principles (2025):**
- Debugging is about understanding code, not just fixing faults
- Systematic workflows prevent, find, and resolve issues collaboratively
- Testing and logging are proactive debugging techniques
- Version control (Git) is essential for safe debugging

**Language-Specific Trends:**
- **Python:** `pdb` remains standard, `debugpy` for IDE integration, `ipdb`/`pudb` for enhanced experiences
- **Go:** Delve is the official debugger, first-class goroutine support
- **Rust:** LLDB is preferred over GDB, ownership/borrowing requires special understanding
- **Node.js:** Chrome DevTools integration is standard, `node --inspect` is universal

**Container/K8s Evolution:**
- Ephemeral containers (`kubectl debug`) are now standard (GA in K8s 1.23+)
- Distroless images require external debugging containers
- Process namespace sharing enables non-invasive debugging

**Production Debugging:**
- Snapshot debugging (non-breaking breakpoints) is emerging
- Event-driven thinking (correlation IDs) supersedes service-oriented debugging
- Real-time error tracking platforms (Sentry, New Relic) are essential
- CI/CD integration for continuous debugging

---

## Skill Purpose and Scope

### What This Skill Covers

**Core Debugging Workflows:**
1. **Local debugging** - Interactive debuggers (pdb, delve, lldb, Chrome DevTools)
2. **Remote debugging** - SSH tunnels, IDE remote attach, container debugging
3. **Production debugging** - Safe, non-intrusive techniques with observability
4. **Container debugging** - Kubernetes ephemeral containers, `kubectl debug`
5. **Distributed systems** - Trace-based debugging with correlation IDs

**Language Coverage:**
- Python: `pdb`, `ipdb`, `debugpy` (VS Code)
- Go: `delve` (CLI and IDE integration)
- Rust: `rust-lldb`, `rust-gdb`
- Node.js: `node --inspect`, Chrome DevTools

**Specialized Techniques:**
- Goroutine debugging (Go-specific)
- Memory profiling basics
- Core dump analysis
- Log-based debugging patterns

### What This Skill Does NOT Cover

**Out of Scope:**
- **Performance profiling** - See `performance-engineering` skill
- **Full observability setup** - See `observability` skill (if exists)
- **Testing strategies** - See `testing-strategies` skill
- **IDE-specific tutorials** - Focus on tool-agnostic techniques

### When to Use This Skill

**Trigger Phrases:**
- "How do I debug this [language] code?"
- "Set a breakpoint in [language]"
- "Debug a running container/pod"
- "Remote debugging setup"
- "Production debugging safely"
- "Inspect goroutines/threads"
- "Core dump analysis"

---

## Research Findings

### Research Summary

**Research Date:** December 3, 2025
**Research Tools Used:** Google Search Grounding, Context7
**Libraries/Tools Evaluated:** 8+

### Google Search Grounding Insights

**Query 1: "debugging best practices 2025 Python pdb Go delve Rust gdb production debugging"**

Key Findings:
- **Systematic workflow adoption** - Modern debugging emphasizes structured approaches
- **Testing as debugging** - Unit tests and CI/CD integration prevent bugs
- **Structured logging** - Essential for distributed systems and production
- **IDE integration** - VS Code and JetBrains IDEs provide comprehensive debugging experiences
- **Language-specific tools:**
  - Python: `pdb` (built-in), `ipdb` (enhanced), `pudb` (visual), `py-spy` (profiling)
  - Go: Delve is official, install via `go install github.com/go-delve/delve/cmd/dlv@latest`
  - Rust: LLDB is default, GDB supported, compile with `cargo build` for debug symbols
  - Node.js: `--inspect` flag, Chrome DevTools integration

**Query 2: "remote debugging containers Kubernetes 2025 kubectl debug ephemeral containers"**

Key Findings:
- **Ephemeral containers are GA** - Standard in Kubernetes 1.23+
- **kubectl debug workflow:**
  - Add debugging tools without modifying pod definition
  - No restarts required
  - Process namespace sharing with `--share-processes` flag
  - Automatically attach with `-i/--interactive`
- **Distroless image debugging** - Ephemeral containers essential for minimal images
- **Security considerations:**
  - Non-root containers complicate debugging (permission restrictions)
  - Use Kubernetes policy engines (OPA/Gatekeeper) for security
- **Remote debugging patterns:**
  - SSH as secure tunnel (encrypts communications)
  - IDE integration (JetBrains Rider, Visual Studio support SSH)
  - Java applications: Enable via `JAVA_OPTS`, expose via `NodePort`

**Query 3: "production debugging observability traces distributed systems logging 2025"**

Status: Query failed (TaskGroup errors). Fallback to existing knowledge and Query 1/2 insights.

Key Production Debugging Principles (from Query 1):
- **Minimal performance impact** - Don't disrupt users
- **No blocking operations** - Non-breaking breakpoints
- **Security-aware** - No exposure of sensitive data
- **Snapshot debugging** - Capture variable state without restarting
- **Event-driven thinking** - Track correlation IDs across systems
- **Real-time error tracking** - Sentry, New Relic, etc.
- **Continuous debugging** - Integrate into CI/CD pipelines

### Context7 Documentation Research

**Delve (Go Debugger):**
- **Library:** `/go-delve/delve`
- **Trust Score:** High
- **Code Snippets:** 267+
- **Key Features:**
  - Built specifically for Go (goroutines, interfaces)
  - CLI commands: `break`, `continue`, `next`, `print`, `goroutine`, `goroutines`
  - Stacktrace support with `-t` flag
  - Conditional breakpoints with `on` command
  - Tracepoints for non-breaking breakpoints
  - Starlark scripting for custom commands
  - IDE integration (VS Code Go extension, GoLand)

**Installation:**
```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

**Basic Usage:**
```bash
dlv debug main.go              # Debug main package
dlv test github.com/me/pkg     # Debug test suite
dlv attach <pid>               # Attach to running process
```

**Key Commands:**
- `break main.main` - Set breakpoint
- `continue` (alias `c`) - Continue execution
- `next` (alias `n`) - Step over
- `step` (alias `s`) - Step into
- `print <var>` - Inspect variable
- `goroutine` - Show current goroutine
- `goroutines` - List all goroutines
- `goroutines -t` - Show stacktraces

**Python Debuggers:**
- **Note:** Context7 search for "pdb" returned PDB file format parsers (Rust library), not Python debugger
- **Fallback:** Use official Python documentation and Google Search findings
- Python `pdb` is built-in, no external library needed
- `ipdb` and `pudb` are enhanced versions available via pip

**Rust Debuggers:**
- **Note:** Context7 search for "rust-lldb" did not return LLDB directly
- **Fallback:** Use official Rust documentation
- LLDB and GDB are system-level debuggers, not Rust-specific packages
- Rust provides wrappers: `rust-lldb` and `rust-gdb` scripts

### Key Takeaways

1. **Language-specific debuggers are essential** - Each language has optimal tooling
2. **Container debugging has evolved** - Ephemeral containers are standard practice
3. **Production debugging requires safety** - Non-breaking techniques, observability
4. **IDE integration matters** - VS Code and JetBrains provide best experiences
5. **Systematic workflows beat ad-hoc debugging** - Structure prevents mistakes

---

## Debugging Taxonomy

### By Environment

```
Debugging Environments
│
├── Local Development
│   ├── Interactive Debugger (pdb, delve, lldb, node --inspect)
│   ├── IDE Integration (VS Code, JetBrains, vim/nvim)
│   └── Print/Log Statements (quick investigations)
│
├── Remote Development
│   ├── SSH Tunnel Debugging (secure, encrypted)
│   ├── IDE Remote Attach (VS Code Remote, JetBrains Gateway)
│   └── Container Exec (kubectl exec, docker exec)
│
├── Container/Kubernetes
│   ├── Ephemeral Containers (kubectl debug --image=<debug-image>)
│   ├── Process Namespace Sharing (--share-processes)
│   └── Node Debugging (kubectl debug node/<node-name>)
│
└── Production
    ├── Snapshot Debugging (non-breaking breakpoints)
    ├── Log-Based Debugging (structured logging, correlation IDs)
    ├── Trace-Based Debugging (distributed tracing, OpenTelemetry)
    └── Error Tracking (Sentry, New Relic, Datadog)
```

### By Technique

**1. Breakpoint Debugging**
- Stop execution at specific line/function
- Inspect variables, call stack, memory
- Step through code (over, into, out)
- Conditional breakpoints (break only if condition true)
- Tracepoints (log without stopping)

**2. Post-Mortem Debugging**
- Core dump analysis (crashed processes)
- Stack trace analysis (from logs/error reports)
- Memory dump inspection

**3. Live Debugging**
- Attach to running process (local or remote)
- Non-breaking observation (production-safe)
- Real-time variable inspection

**4. Log-Based Debugging**
- Structured logging (JSON, key-value pairs)
- Correlation IDs (trace requests across services)
- Log levels (DEBUG, INFO, WARN, ERROR)

**5. Trace-Based Debugging**
- Distributed tracing (Jaeger, Zipkin, OpenTelemetry)
- Span analysis (timing, dependencies)
- Request flow visualization

### By Problem Type

**1. Logical Errors**
- Wrong algorithm, incorrect condition
- **Tools:** Breakpoints, variable inspection, step debugging

**2. Runtime Errors**
- Exceptions, panics, crashes
- **Tools:** Stack traces, core dumps, error tracking

**3. Concurrency Issues**
- Race conditions, deadlocks
- **Tools:** Goroutine inspection (Go), thread inspection, race detector

**4. Performance Issues**
- Slowness, memory leaks
- **Tools:** Profilers (out of scope - see performance-engineering)

**5. Integration Issues**
- API failures, network problems
- **Tools:** Distributed tracing, correlation IDs, request/response logging

---

## Decision Framework

### Which Debugger for Which Language?

```
Language → Debugger Decision Tree

Python:
  ├── Simple script? → pdb (built-in, `breakpoint()`)
  ├── Need better UX? → ipdb (enhanced pdb with IPython)
  ├── Want visual UI? → pudb (terminal-based GUI)
  ├── VS Code user? → debugpy (built into Python extension)
  └── PyCharm user? → Built-in debugger

Go:
  ├── CLI debugging? → delve (dlv debug, dlv test)
  ├── VS Code user? → delve (via Go extension)
  ├── GoLand user? → Built-in debugger (uses delve)
  └── Goroutine debugging? → delve (first-class support)

Rust:
  ├── Mac/Linux? → rust-lldb (default choice)
  ├── Windows/prefer GDB? → rust-gdb
  ├── VS Code user? → CodeLLDB extension
  ├── IntelliJ Rust? → Built-in debugger
  └── Compile with: cargo build (debug symbols default)

Node.js:
  ├── CLI debugging? → node --inspect or node --inspect-brk
  ├── VS Code user? → Built-in debugger (attach mode)
  ├── Chrome user? → chrome://inspect (DevTools)
  └── Need remote? → node --inspect=0.0.0.0:9229
```

### Which Technique for Which Scenario?

| Scenario | Recommended Technique | Tools |
|----------|----------------------|-------|
| **Local development** | Interactive debugger | pdb, delve, lldb, node --inspect |
| **Bug in test** | Test-specific debugging | dlv test, pdb in pytest, lldb with cargo test |
| **Remote server** | SSH tunnel + remote attach | VS Code Remote, JetBrains Gateway |
| **Container (local)** | docker exec -it | sh/bash + debugger |
| **Kubernetes pod** | Ephemeral container | kubectl debug --image=nicolaka/netshoot |
| **Distroless image** | Ephemeral container (required) | kubectl debug with busybox/alpine |
| **Production issue** | Log analysis + error tracking | Structured logs, Sentry, correlation IDs |
| **Goroutine deadlock** | Goroutine inspection | delve goroutines, GODEBUG=gctrace=1 |
| **Crashed process** | Core dump analysis | gdb core, lldb -c core |
| **Distributed failure** | Distributed tracing | OpenTelemetry, Jaeger, correlation IDs |
| **Race condition** | Race detector + debugger | go run -race, cargo test --release (ThreadSanitizer) |
| **Memory issue** | Memory profiler (not debugger) | See performance-engineering skill |

### When to Use Ephemeral Containers?

```
Use kubectl debug with ephemeral containers when:
✅ Container has crashed (kubectl exec won't work)
✅ Using distroless/minimal image (no shell, no tools)
✅ Need debugging tools (curl, netstat, tcpdump) without rebuilding image
✅ Want to inspect running process without restart
✅ Debugging network issues (DNS, connectivity)

Do NOT use ephemeral containers when:
❌ kubectl exec works (simpler, faster)
❌ Debugging simple apps (logs may be sufficient)
❌ Performance testing (ephemeral containers add overhead)
```

### Production Debugging Safety Checklist

Before debugging in production:
- [ ] Will this impact performance? (Profile overhead)
- [ ] Will this block users? (Use non-breaking techniques)
- [ ] Could this expose secrets? (Avoid variable dumps)
- [ ] Is there a rollback plan? (Git branch, feature flag)
- [ ] Have we tried logs first? (Less invasive)
- [ ] Do we have correlation IDs? (Trace requests)
- [ ] Is error tracking enabled? (Sentry, New Relic)
- [ ] Can we reproduce in staging? (Safer environment)

---

## Python Debugging

### Built-in: pdb (Python Debugger)

**When to Use:**
- Quick debugging without extra dependencies
- Server environments (no IDE available)
- Understanding Python debugging fundamentals

**Basic Usage:**

```python
# Method 1: Insert breakpoint (Python 3.7+)
def buggy_function(x, y):
    breakpoint()  # Execution stops here
    return x / y

# Method 2: Import pdb (older Python)
import pdb
pdb.set_trace()  # Execution stops here
```

**Essential pdb Commands:**

| Command | Alias | Description |
|---------|-------|-------------|
| `list` | `l` | Show code around current line |
| `next` | `n` | Execute current line, step over functions |
| `step` | `s` | Execute current line, step into functions |
| `continue` | `c` | Continue execution until next breakpoint |
| `break <line>` | `b` | Set breakpoint at line number |
| `print <var>` | `p` | Print variable value |
| `pp <var>` | | Pretty-print variable value |
| `where` | `w` | Show stack trace |
| `up` | `u` | Move up stack frame |
| `down` | `d` | Move down stack frame |
| `quit` | `q` | Exit debugger |

**Example Workflow:**

```python
# bug.py
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    breakpoint()  # Inspect variables here
    return total / count

# At breakpoint:
# (Pdb) p total
# 15
# (Pdb) p count
# 3
# (Pdb) n  # Step to next line
# (Pdb) c  # Continue
```

### Enhanced: ipdb (IPython Debugger)

**Installation:**
```bash
pip install ipdb
```

**Why ipdb?**
- Tab completion
- Syntax highlighting
- Better introspection
- IPython magic commands

**Usage:**
```python
import ipdb
ipdb.set_trace()
```

### Visual: pudb (Terminal GUI Debugger)

**Installation:**
```bash
pip install pudb
```

**Why pudb?**
- Visual interface in terminal
- Sidebar variable inspector
- Breakpoint manager
- Navigation with arrow keys

**Usage:**
```python
import pudb
pudb.set_trace()
```

### IDE Integration: debugpy (VS Code)

**VS Code Python Extension** includes debugpy automatically.

**launch.json configuration:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Remote Attach",
      "type": "python",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      }
    }
  ]
}
```

**Remote debugging with debugpy:**
```python
# On remote server
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()  # Blocks until debugger attaches
breakpoint()
```

### Python Debugging Best Practices

1. **Use `breakpoint()` over `pdb.set_trace()`** (Python 3.7+)
2. **Leverage `pp` for complex data structures** (pretty-print)
3. **Use conditional breakpoints:** `b 10, x > 5` (break at line 10 if x > 5)
4. **Post-mortem debugging:** `python -m pdb script.py` (start pdb on crash)
5. **Debugging tests:** `pytest --pdb` (drop into debugger on failure)

---

## Go Debugging

### Delve: The Official Go Debugger

**Why Delve?**
- Built specifically for Go (goroutines, interfaces, channels)
- First-class goroutine support
- Handles Go's concurrency primitives
- IDE integration (VS Code, GoLand)

**Installation:**
```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

**Verify installation:**
```bash
dlv version
```

### Delve CLI Usage

**Debug main package:**
```bash
# From package directory
dlv debug

# Or specify package path
dlv debug github.com/user/project/cmd/app

# Pass arguments to program
dlv debug -- --config prod.yaml
```

**Debug tests:**
```bash
dlv test github.com/user/project/pkg/module
```

**Attach to running process:**
```bash
# Find PID
ps aux | grep myapp

# Attach
dlv attach <pid>
```

### Essential Delve Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `break main.main` | `b` | Set breakpoint at function |
| `break file.go:10` | `b` | Set breakpoint at line |
| `continue` | `c` | Continue execution |
| `next` | `n` | Step over |
| `step` | `s` | Step into |
| `stepout` | `so` | Step out of function |
| `print x` | `p` | Print variable |
| `locals` | | Show local variables |
| `args` | | Show function arguments |
| `goroutine` | `gr` | Show current goroutine |
| `goroutines` | `grs` | List all goroutines |
| `goroutines -t` | | Show goroutine stacktraces |
| `stack` | `bt` | Show stack trace |
| `list` | `l` | Show source code |
| `funcs` | | List functions (supports regex) |
| `on <bp> <cmd>` | | Execute command on breakpoint hit |

### Delve Workflow Example

```bash
$ dlv debug main.go
Type 'help' for list of commands.
(dlv) break main.main
Breakpoint 1 set at 0x49ecf3 for main.main() ./main.go:10
(dlv) continue
> main.main() ./main.go:10 (hits goroutine(1):1 total:1) (PC: 0x49ecf3)
     5:	package main
     6:
     7:	import "fmt"
     8:
     9:	func main() {
=>  10:		fmt.Println("Hello")
    11:	}
(dlv) print "Breakpoint hit!"
"Breakpoint hit!"
(dlv) next
Hello
(dlv) quit
```

### Goroutine Debugging

**List all goroutines:**
```bash
(dlv) goroutines
[9 goroutines]
  Goroutine 1 - User: ./main.go:10 main.main (0x49ecf3) (thread 12345)
  Goroutine 2 - Runtime: /usr/local/go/src/runtime/proc.go:242 runtime.forcegchelper (0x...)
  ...
```

**Show goroutine stacktraces:**
```bash
(dlv) goroutines -t
* Goroutine 1 - User: ./main.go:10 main.main (0x49ecf3)
    0  0x000000000049ecf3 in main.main
       at ./main.go:10
    1  0x0000000000438c93 in runtime.main
       at /usr/local/go/src/runtime/proc.go:250
```

**Filter goroutines:**
```bash
# Show only user goroutines (exclude runtime)
(dlv) goroutines -with user

# Show goroutines with location containing "handler"
(dlv) goroutines -with userloc handler

# Show goroutines running on OS thread
(dlv) goroutines -with running
```

**Switch to specific goroutine:**
```bash
(dlv) goroutine 5
Switched from 1 to 5 (thread 12345)
```

**Execute command on all goroutines:**
```bash
(dlv) goroutines -exec stack
```

### Conditional Breakpoints & Tracepoints

**Conditional breakpoint:**
```bash
(dlv) break main.go:20
(dlv) on <bp-id> cond x > 10
# Now breaks only when x > 10
```

**Tracepoint (log without stopping):**
```bash
(dlv) break main.go:20
(dlv) on <bp-id> trace
# Prints log when hit, continues execution
```

**Execute command on breakpoint:**
```bash
(dlv) break main.go:20
(dlv) on 1 print x
# Prints x every time breakpoint 1 is hit
```

### VS Code Integration

**Install Go extension** (includes Delve integration).

**launch.json configuration:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Package",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${fileDirname}"
    },
    {
      "name": "Attach to Process",
      "type": "go",
      "request": "attach",
      "mode": "local",
      "processId": "${command:pickProcess}"
    }
  ]
}
```

### Go Debugging Best Practices

1. **Always check goroutines** when debugging concurrent code
2. **Use tracepoints for frequent code paths** (avoid stopping repeatedly)
3. **Filter goroutines** to focus on relevant ones (`-with user`)
4. **Use `funcs` with regex** to find functions: `funcs test.Test*`
5. **Conditional breakpoints save time** (break only when needed)
6. **Enable race detector:** `go run -race` or `go test -race`

---

## Rust Debugging

### LLDB vs GDB for Rust

**Recommendation: Use LLDB**
- Default choice for Rust
- Better support for Rust types
- Cross-platform (Mac, Linux, Windows via MSVC)

**GDB is acceptable:**
- Linux standard
- More familiar to some developers
- Works with Rust via `rust-gdb` wrapper

### Compilation for Debugging

**Debug build (default):**
```bash
cargo build
# Produces target/debug/binary with debug symbols
```

**Release build with debug symbols:**
```bash
cargo build --release --config "profile.release.debug=true"
```

**Run with debugger:**
```bash
# LLDB
rust-lldb target/debug/myapp

# GDB
rust-gdb target/debug/myapp
```

### Essential LLDB Commands for Rust

| Command | Description |
|---------|-------------|
| `breakpoint set -f main.rs -l 10` | Set breakpoint at line |
| `breakpoint set -n main` | Set breakpoint at function |
| `run` | Start program |
| `continue` (or `c`) | Continue execution |
| `next` (or `n`) | Step over |
| `step` (or `s`) | Step into |
| `finish` | Step out of function |
| `print variable` (or `p`) | Print variable |
| `frame variable` (or `fr v`) | Show local variables |
| `backtrace` (or `bt`) | Show stack trace |
| `thread list` | List all threads |
| `quit` | Exit debugger |

### LLDB Workflow Example

```bash
$ rust-lldb target/debug/myapp
(lldb) breakpoint set -f main.rs -l 10
Breakpoint 1: where = myapp`myapp::main::h1234abcd + 42 at main.rs:10
(lldb) run
Process 12345 launched
* thread #1, name = 'main', stop reason = breakpoint 1.1
    frame #0: 0x000055555556789a myapp`myapp::main::h1234abcd at main.rs:10
   7   	fn main() {
   8   	    let x = 5;
   9   	    let y = 10;
-> 10  	    println!("x + y = {}", x + y);
   11  	}
(lldb) print x
(i32) $0 = 5
(lldb) continue
x + y = 15
Process 12345 exited with status = 0
```

### VS Code Integration: CodeLLDB

**Install extension:**
- Extension ID: `vadimcn.vscode-lldb`

**launch.json configuration:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug",
      "program": "${workspaceFolder}/target/debug/${workspaceFolderBasename}",
      "args": [],
      "cwd": "${workspaceFolder}"
    },
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug Tests",
      "program": "${workspaceFolder}/target/debug/deps/${workspaceFolderBasename}-<test-hash>",
      "args": [],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### Rust-Specific Debugging Challenges

**1. Ownership and Borrowing:**
- Variables may be moved/borrowed, making them unavailable in debugger
- Use `clone()` temporarily for debugging (remove in production)

**2. Name Mangling:**
- Rust mangles function names for uniqueness
- Use `#[no_mangle]` attribute for C FFI debugging
- `rust-lldb` and `rust-gdb` wrappers handle demangling

**3. Optimizations:**
- Release builds inline aggressively
- Variables may be optimized out
- Use debug builds for debugging (cargo build)

**4. Macros:**
- Macro expansions can be confusing
- Use `cargo expand` to see macro output before debugging

### Debugging Rust Tests

```bash
# Run tests with debugger
cargo test --no-run  # Build test binary
rust-lldb target/debug/deps/myapp-<hash>

# Or debug single test
cargo test --test integration_test --no-run
rust-lldb target/debug/deps/integration_test-<hash>

# Run specific test in debugger
(lldb) breakpoint set -n test_name
(lldb) run test_name
```

### Rust Debugging Best Practices

1. **Always compile with debug symbols** (`cargo build`)
2. **Use LLDB over GDB** (better Rust support)
3. **Install rust-lldb/rust-gdb wrappers** (handle name mangling)
4. **Understand ownership** (moved variables unavailable)
5. **Use `cargo expand`** to debug macros
6. **Debug builds only** (release optimizes out variables)
7. **CodeLLDB for VS Code** (best IDE experience)

---

## Node.js Debugging

### Built-in: node --inspect

**Start Node.js with debugger:**
```bash
# Start and pause immediately
node --inspect-brk app.js

# Start and run (attach debugger later)
node --inspect app.js

# Specify host and port
node --inspect=0.0.0.0:9229 app.js
```

**Chrome DevTools:**
1. Open Chrome: `chrome://inspect`
2. Click "Open dedicated DevTools for Node"
3. Set breakpoints, inspect variables

### VS Code Integration

**launch.json configuration:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Program",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/app.js"
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Process",
      "port": 9229,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

### Debugging Node.js in Docker

**Dockerfile:**
```dockerfile
# Expose debugging port
EXPOSE 9229

# Start with inspector
CMD ["node", "--inspect=0.0.0.0:9229", "app.js"]
```

**docker-compose.yml:**
```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
      - "9229:9229"  # Debugging port
```

**Attach VS Code:**
```json
{
  "type": "node",
  "request": "attach",
  "name": "Attach to Docker",
  "address": "localhost",
  "port": 9229,
  "localRoot": "${workspaceFolder}",
  "remoteRoot": "/app"
}
```

### Node.js Debugging Best Practices

1. **Use `--inspect-brk`** to pause immediately at startup
2. **Skip node_internals** to focus on your code
3. **Chrome DevTools for quick debugging** (no IDE needed)
4. **VS Code for project debugging** (better integration)
5. **Remote debugging in containers** (expose port 9229)

---

## Container & Kubernetes Debugging

### kubectl debug with Ephemeral Containers

**When to use:**
- Container has crashed (`kubectl exec` won't work)
- Distroless/minimal image (no shell, no debugging tools)
- Need network debugging tools (curl, netstat, tcpdump)

**Basic usage:**
```bash
# Add ephemeral debugging container
kubectl debug -it <pod-name> --image=nicolaka/netshoot

# Specify container name
kubectl debug -it <pod-name> --image=busybox --container=debug

# Share process namespace (see processes from other containers)
kubectl debug -it <pod-name> --image=busybox --share-processes --container=debugger
```

**Useful debugging images:**
- `nicolaka/netshoot` - Network debugging (curl, dig, netstat, tcpdump)
- `busybox` - Minimal shell and tools
- `alpine` - Lightweight Linux with package manager
- `ubuntu` - Full-featured environment

### Debugging Distroless Images

**Problem:** Distroless images have no shell.

**Solution:** Ephemeral container with debugging tools.

```bash
# Add busybox to inspect distroless container
kubectl debug -it my-distroless-pod --image=busybox --target=app

# --target=app shares process namespace with "app" container
# Now you can see app's processes: ps aux
```

### Node Debugging

**Debug on specific node:**
```bash
kubectl debug node/<node-name> -it --image=ubuntu
```

**What this does:**
- Creates privileged pod on the node
- Mounts node's root filesystem at `/host`
- Useful for node-level issues (disk, network, kernel)

**Example workflow:**
```bash
kubectl debug node/worker-1 -it --image=ubuntu

# Inside debug container
root@debug-pod:/# chroot /host
root@worker-1:/# systemctl status kubelet
root@worker-1:/# journalctl -u kubelet
```

### Docker Container Debugging

**Exec into running container:**
```bash
docker exec -it <container-id> sh
```

**If no shell available:**
```bash
# Create debug container sharing namespaces
docker run -it --pid=container:<container-id> \
           --net=container:<container-id> \
           busybox sh
```

### Container Debugging Best Practices

1. **Use ephemeral containers for K8s** (standard practice)
2. **Prefer netshoot for network issues** (comprehensive tooling)
3. **Share process namespace** to inspect other containers
4. **Clean up debug pods** after debugging
5. **Don't modify images for debugging** (use ephemeral approach)

---

## Production Debugging

### Production Debugging Principles

**Golden Rules:**
1. **Minimal performance impact** - Profile overhead, limit breakpoints
2. **No blocking operations** - Use non-breaking techniques (tracepoints, logs)
3. **Security-aware** - Avoid logging secrets, PII
4. **Reversible** - Can roll back changes quickly (feature flags, Git)
5. **Observable** - Structured logging, correlation IDs, distributed tracing

### Safe Production Debugging Techniques

**1. Structured Logging**

```python
# Bad: Unstructured
print("User login failed")

# Good: Structured (JSON)
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
// Generate correlation ID
func handleRequest(w http.ResponseWriter, r *http.Request) {
    correlationID := r.Header.Get("X-Correlation-ID")
    if correlationID == "" {
        correlationID = generateUUID()
    }

    // Pass to all downstream calls
    ctx := context.WithValue(r.Context(), "correlationID", correlationID)

    // Log with correlation ID
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
        # ... processing
        span.add_event("Order validated")
```

**4. Error Tracking Platforms**

- **Sentry:** Captures exceptions with context
- **New Relic:** APM with error tracking
- **Datadog:** Logs, metrics, traces
- **Rollbar:** Error monitoring

**Example: Sentry integration**

```python
import sentry_sdk

sentry_sdk.init(dsn="https://...")

try:
    risky_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)
```

**5. Snapshot Debugging (Non-Breaking Breakpoints)**

**Concept:** Capture variable state without stopping execution.

**Tools:**
- Lightrun (JVM, Node.js, Python)
- Rookout (Multi-language)

**How it works:**
- Set "non-breaking breakpoint" in IDE/UI
- Tool captures variable values when line is hit
- Logs sent to dashboard (doesn't pause execution)

### Production Debugging Workflow

**Step 1: Detect (Monitoring)**
- Error tracking platform alerts
- Log aggregation (ELK, Splunk)
- Metrics spike (Prometheus, Grafana)

**Step 2: Locate (Correlation)**
- Find correlation ID from error report
- Search logs for correlation ID
- View distributed trace for request

**Step 3: Reproduce (Staging)**
- Try to reproduce in staging environment
- Use production data (sanitized) if needed
- Avoid debugging directly in production if possible

**Step 4: Fix (Safe Changes)**
- Create feature flag for fix (gradual rollout)
- Deploy to canary environment first
- Monitor error rates closely

**Step 5: Verify (Observability)**
- Check error tracking platform (errors resolved?)
- Review logs for correlation ID (successful requests?)
- Monitor distributed traces (latency improved?)

### Production Debugging Anti-Patterns

**❌ DON'T:**
- Use interactive debuggers on production (blocks threads)
- Log sensitive data (passwords, tokens, PII)
- Add excessive logging (performance impact)
- Deploy untested fixes (test in staging first)
- Debug without correlation IDs (can't trace requests)

**✅ DO:**
- Use structured logging with correlation IDs
- Enable distributed tracing (OpenTelemetry)
- Use error tracking platforms (Sentry)
- Test fixes in staging first
- Implement gradual rollouts (feature flags, canary)
- Monitor after changes (metrics, logs, traces)

---

## Tool Recommendations

### Debuggers by Language (2025)

#### **Python**

**Primary: pdb (Built-in)**
- **Why:** No dependencies, universally available
- **When:** Quick debugging, server environments, learning
- **Installation:** Built into Python
- **Usage:** `breakpoint()` or `import pdb; pdb.set_trace()`

**Enhanced: ipdb**
- **Why:** Better UX (tab completion, syntax highlighting)
- **When:** Interactive debugging sessions, IPython users
- **Installation:** `pip install ipdb`
- **Usage:** `import ipdb; ipdb.set_trace()`

**Visual: pudb**
- **Why:** Terminal GUI, visual variable inspection
- **When:** Prefer visual debugging without IDE
- **Installation:** `pip install pudb`
- **Usage:** `import pudb; pudb.set_trace()`

**IDE Integration: debugpy (VS Code)**
- **Why:** Best IDE experience, remote debugging
- **When:** VS Code users, remote debugging needs
- **Installation:** Included with VS Code Python extension
- **Usage:** Configure `launch.json`

---

#### **Go**

**Primary: Delve**
- **Library:** `/go-delve/delve`
- **Trust Score:** High
- **Code Snippets:** 267+
- **Why:** Official Go debugger, first-class goroutine support
- **When:** All Go debugging (local, remote, test)
- **Installation:** `go install github.com/go-delve/delve/cmd/dlv@latest`
- **Usage:** `dlv debug`, `dlv test`, `dlv attach`

**IDE Integration:**
- **VS Code:** Go extension (uses delve)
- **GoLand:** Built-in debugger (uses delve)

---

#### **Rust**

**Primary: LLDB**
- **Why:** Default Rust debugger, best type support
- **When:** Mac, Linux, MSVC Windows
- **Installation:** System package (`brew install llvm`, `apt install lldb`)
- **Usage:** `rust-lldb target/debug/app`

**Alternative: GDB**
- **Why:** Familiar to Linux developers
- **When:** Linux, prefer GDB
- **Installation:** System package (`apt install gdb`)
- **Usage:** `rust-gdb target/debug/app`

**IDE Integration: CodeLLDB (VS Code)**
- **Extension ID:** `vadimcn.vscode-lldb`
- **Why:** Best VS Code Rust debugging experience
- **When:** VS Code users
- **Usage:** Configure `launch.json`

---

#### **Node.js**

**Primary: node --inspect**
- **Why:** Built-in, Chrome DevTools integration
- **When:** All Node.js debugging
- **Installation:** Built into Node.js
- **Usage:** `node --inspect-brk app.js`, then `chrome://inspect`

**IDE Integration:**
- **VS Code:** Built-in Node.js debugger
- **Chrome DevTools:** `chrome://inspect`

---

### Container Debugging Tools

**Primary: kubectl debug**
- **Why:** Standard K8s debugging (GA in 1.23+)
- **When:** K8s pod debugging, distroless images
- **Usage:** `kubectl debug -it <pod> --image=nicolaka/netshoot`

**Debugging Images:**

| Image | Size | Best For | Tools Included |
|-------|------|----------|----------------|
| **nicolaka/netshoot** | ~380MB | Network debugging | curl, dig, netstat, tcpdump, iperf |
| **busybox** | ~1MB | Minimal debugging | sh, basic utilities |
| **alpine** | ~5MB | Lightweight with packages | sh, apk package manager |
| **ubuntu** | ~70MB | Full environment | bash, apt, comprehensive tools |

---

### Production Debugging Tools

**Error Tracking:**
- **Sentry** - Exception tracking, breadcrumbs, release tracking
- **New Relic** - APM, error tracking, distributed tracing
- **Datadog** - Logs, metrics, traces, error tracking
- **Rollbar** - Error monitoring, deploy tracking

**Distributed Tracing:**
- **OpenTelemetry** - Open standard, vendor-neutral
- **Jaeger** - Open-source, distributed tracing
- **Zipkin** - Open-source, lightweight
- **Datadog APM** - Commercial, full observability

**Log Aggregation:**
- **ELK Stack** - Elasticsearch, Logstash, Kibana
- **Splunk** - Enterprise log management
- **Grafana Loki** - Log aggregation, integrates with Prometheus
- **Datadog Logs** - Centralized logging

---

## Skill Structure Design

### SKILL.md Structure (Main File)

**Estimated Length:** 300-400 lines

```markdown
---
name: debugging-techniques
description: Debugging workflows for Python (pdb, debugpy), Go (delve), Rust (lldb), and Node.js, including container debugging (kubectl debug, ephemeral containers) and production-safe debugging techniques with distributed tracing and correlation IDs
---

# Debugging Techniques

## Purpose
Provides debugging workflows for local, remote, container, and production environments across Python, Go, Rust, and Node.js.

## When to Use This Skill
- Setting breakpoints in [language]
- Debugging running containers/pods
- Remote debugging setup
- Production debugging safely
- Goroutine/thread inspection

## Quick Reference

### Python Debugging
[pdb commands, breakpoint() usage, debugpy remote attach]

### Go Debugging
[delve commands, goroutine inspection, dlv debug/test/attach]

### Rust Debugging
[LLDB commands, cargo build, rust-lldb usage]

### Node.js Debugging
[node --inspect, Chrome DevTools, VS Code attach]

### Container Debugging
[kubectl debug, ephemeral containers, process namespace sharing]

### Production Debugging
[Structured logging, correlation IDs, distributed tracing, error tracking]

## Decision Framework
[Which debugger? Which technique? When to use what?]

## Common Workflows
[Step-by-step debugging scenarios]

## Additional Resources
- See language-specific guides in reference/
- See container debugging patterns in reference/containers.md
- See production debugging guide in reference/production.md
```

### Bundled Resources Structure

```
debugging-techniques/
├── SKILL.md                          # Main skill file (300-400 lines)
├── reference/
│   ├── python-debugging.md           # Detailed Python debugging guide
│   ├── go-debugging.md               # Detailed Go/delve guide
│   ├── rust-debugging.md             # Detailed Rust/LLDB guide
│   ├── nodejs-debugging.md           # Detailed Node.js guide
│   ├── container-debugging.md        # K8s ephemeral containers, docker
│   ├── production-debugging.md       # Safe production techniques
│   └── decision-trees.md             # Debugging decision frameworks
├── examples/
│   ├── python-pdb-session.md         # Example pdb session
│   ├── go-delve-goroutines.md        # Example goroutine debugging
│   ├── rust-lldb-session.md          # Example LLDB session
│   ├── kubectl-debug-example.md      # Example K8s debugging
│   └── correlation-id-example.md     # Example distributed tracing
└── scripts/
    └── setup-remote-debug.sh         # Script to configure remote debugging
```

### Progressive Disclosure Strategy

**Level 1: SKILL.md (Always loaded when skill triggers)**
- Quick reference for all languages
- Common commands (pdb, delve, lldb, node --inspect)
- Decision framework (which tool when)
- Links to detailed references

**Level 2: Reference files (Loaded when Claude needs details)**
- `python-debugging.md` - When debugging Python specifically
- `go-debugging.md` - When debugging Go, goroutines
- `container-debugging.md` - When debugging in K8s/Docker
- `production-debugging.md` - When debugging production issues

**Level 3: Examples and scripts (Loaded on demand)**
- Example sessions for learning
- Setup scripts for automation

### File Descriptions

**reference/python-debugging.md:**
- pdb, ipdb, pudb detailed commands
- debugpy remote debugging setup
- pytest debugging integration
- Django/Flask debugging patterns

**reference/go-debugging.md:**
- Delve CLI deep dive
- Goroutine debugging techniques
- Conditional breakpoints, tracepoints
- Debugging concurrent code

**reference/rust-debugging.md:**
- LLDB vs GDB comparison
- Debugging ownership/borrowing issues
- Macro debugging with cargo expand
- FFI boundary debugging

**reference/nodejs-debugging.md:**
- node --inspect deep dive
- Chrome DevTools usage
- VS Code configuration
- Docker container debugging

**reference/container-debugging.md:**
- kubectl debug comprehensive guide
- Ephemeral container patterns
- Distroless image debugging
- Node debugging workflows

**reference/production-debugging.md:**
- Structured logging patterns
- Correlation ID implementation
- Distributed tracing setup (OpenTelemetry)
- Error tracking integration (Sentry)
- Safe debugging checklist

---

## Integration Points

### Related Skills

**1. testing-strategies**
- Debugging failed tests (pytest --pdb, dlv test)
- Test-driven debugging (write test, debug test)
- Integration test debugging

**2. performance-engineering**
- Profiling complements debugging (different tools)
- Memory debugging overlaps (but profilers are primary)
- Performance bottleneck identification

**3. kubernetes-operations**
- kubectl debug is core K8s operation
- Pod debugging workflows
- Node debugging for infrastructure issues

**4. security-hardening**
- Avoiding security issues during debugging (no secret logging)
- Non-root container debugging challenges
- Production debugging without exposing vulnerabilities

**5. observability** (if exists)
- Structured logging for debugging
- Distributed tracing for debugging distributed systems
- Metrics for identifying issues before debugging

### Workflow Integration

**Development Workflow:**
```
Write Code → Run → Error Occurs
  ↓
Use debugging-techniques skill:
  ├── Local: Interactive debugger (pdb, delve, lldb)
  ├── Test: Test-specific debugging (pytest --pdb, dlv test)
  └── Container: kubectl debug (if in K8s)
  ↓
Understand Issue → Fix → Test
  ↓
See testing-strategies skill for test debugging
```

**Production Workflow:**
```
Error Alert (Sentry, New Relic)
  ↓
Use debugging-techniques skill (production section):
  ├── Find correlation ID
  ├── Search logs
  ├── View distributed trace
  ↓
Reproduce in Staging
  ↓
Use interactive debugger (if needed)
  ↓
Fix → Gradual Rollout → Monitor
```

---

## Implementation Roadmap

### Phase 1: Core SKILL.md (Week 1)

**Tasks:**
- [ ] Create SKILL.md with YAML frontmatter
- [ ] Write "Quick Reference" section (all languages)
- [ ] Create decision framework table
- [ ] Add common commands reference
- [ ] Document kubectl debug basics
- [ ] Write production debugging safety checklist
- [ ] Add links to reference files (even if not created yet)

**Success Criteria:**
- SKILL.md under 400 lines
- Covers all 4 languages at basic level
- Includes container debugging
- Includes production debugging principles
- Clear "when to use what" guidance

---

### Phase 2: Language-Specific References (Week 2)

**Tasks:**
- [ ] Write reference/python-debugging.md (pdb, ipdb, debugpy)
- [ ] Write reference/go-debugging.md (delve, goroutines)
- [ ] Write reference/rust-debugging.md (LLDB, GDB)
- [ ] Write reference/nodejs-debugging.md (--inspect, DevTools)

**Success Criteria:**
- Each reference file 100-200 lines
- Comprehensive command reference
- IDE integration examples
- Common pitfalls documented

---

### Phase 3: Container & Production (Week 3)

**Tasks:**
- [ ] Write reference/container-debugging.md (kubectl debug, ephemeral containers)
- [ ] Write reference/production-debugging.md (structured logging, tracing)
- [ ] Write reference/decision-trees.md (expanded decision frameworks)

**Success Criteria:**
- Container debugging covers K8s and Docker
- Production debugging includes OpenTelemetry example
- Decision trees cover all scenarios from init.md

---

### Phase 4: Examples (Week 4)

**Tasks:**
- [ ] Write examples/python-pdb-session.md
- [ ] Write examples/go-delve-goroutines.md
- [ ] Write examples/rust-lldb-session.md
- [ ] Write examples/kubectl-debug-example.md
- [ ] Write examples/correlation-id-example.md

**Success Criteria:**
- Each example is complete, copy-pasteable
- Examples show realistic debugging scenarios
- Step-by-step walkthroughs

---

### Phase 5: Scripts & Automation (Week 5)

**Tasks:**
- [ ] Write scripts/setup-remote-debug.sh (SSH tunnel setup)
- [ ] Document script usage in SKILL.md
- [ ] Test scripts on Mac, Linux

**Success Criteria:**
- Scripts are executable without modification
- Clear error messages
- Documentation in SKILL.md

---

### Phase 6: Testing & Refinement (Week 6)

**Tasks:**
- [ ] Test skill with real debugging scenarios
- [ ] Create at least 3 evaluations:
  - Evaluation 1: "Debug Python function with pdb"
  - Evaluation 2: "Debug Go goroutine deadlock with delve"
  - Evaluation 3: "Debug distroless container in K8s with kubectl debug"
- [ ] Refine based on evaluation results
- [ ] Test across models (Haiku, Sonnet, Opus)
- [ ] Validate all commands work (pdb, delve, lldb)

**Success Criteria:**
- All evaluations pass
- Skill triggers appropriately
- Commands are accurate and tested
- Token usage reasonable

---

### Evaluation Plan

**Evaluation 1: Python pdb Debugging**
```
Scenario: Debug a Python function that raises ZeroDivisionError
Task: Use pdb to set breakpoint, inspect variables, step through code
Success: Correct pdb commands, identifies issue, suggests fix
```

**Evaluation 2: Go Goroutine Debugging**
```
Scenario: Go program with goroutine deadlock
Task: Use delve to list goroutines, show stacktraces, identify deadlock
Success: Correct delve commands (goroutines -t), identifies blocking goroutines
```

**Evaluation 3: Kubernetes Container Debugging**
```
Scenario: Distroless container in K8s with networking issue
Task: Use kubectl debug with ephemeral container to diagnose
Success: Correct kubectl debug command, suggests appropriate debug image (netshoot)
```

**Evaluation 4: Production Debugging**
```
Scenario: Production API error, need to trace request
Task: Explain how to use correlation IDs and distributed tracing
Success: Explains structured logging, correlation ID pattern, OpenTelemetry setup
```

**Evaluation 5: Multi-Language Decision**
```
Scenario: Given different debugging scenarios, choose appropriate tool
Task: Which debugger for which language/scenario?
Success: Recommends correct debugger (pdb for Python, delve for Go, etc.)
```

---

## Appendix: Research Sources

### Google Search Grounding Sources (December 3, 2025)

**Query 1: "debugging best practices 2025 Python pdb Go delve Rust gdb production debugging"**
- General debugging principles (systematic workflows, testing, logging)
- Python: pdb commands, ipdb, pudb, debugpy for VS Code
- Go: Delve installation, basic commands, goroutine debugging
- Rust: LLDB vs GDB, compilation with debug symbols, common challenges
- Production: Snapshot debugging, continuous debugging, error tracking platforms

**Query 2: "remote debugging containers Kubernetes 2025 kubectl debug ephemeral containers"**
- Ephemeral containers are GA in Kubernetes 1.23+
- kubectl debug workflow: Add debugging tools without pod restart
- Process namespace sharing with --share-processes
- Distroless image debugging requires ephemeral containers
- Security considerations: Non-root containers, policy engines
- Remote debugging via SSH tunnels

### Context7 Documentation Research

**Delve (/go-delve/delve):**
- Trust Score: High
- Code Snippets: 267+
- Comprehensive command documentation
- Goroutine debugging examples
- Starlark scripting support
- IDE integration guidance

---

## Version History

**v0.1 (December 3, 2025):**
- Initial planning document
- Multi-language scope: Python, Go, Rust, Node.js
- Container and production debugging included
- Research completed via Google Search Grounding and Context7
- Skill structure designed (SKILL.md + 7 reference files + 5 examples)

---

**Next Steps:** Proceed to implementation Phase 1 (Core SKILL.md creation).
