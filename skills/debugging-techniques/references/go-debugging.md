# Go Debugging Reference

## Table of Contents

1. [Delve Overview](#delve-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Basic Commands](#basic-commands)
4. [Goroutine Debugging](#goroutine-debugging)
5. [Advanced Features](#advanced-features)
6. [IDE Integration](#ide-integration)
7. [Remote Debugging](#remote-debugging)
8. [Debugging Tests](#debugging-tests)
9. [Best Practices](#best-practices)

## Delve Overview

Delve is the official debugger for Go, designed specifically for Go's unique features:
- Goroutines and channels
- Interfaces and reflection
- Deferred functions
- Built-in concurrency primitives

### Why Delve Over GDB?

- **Goroutine awareness** - First-class goroutine inspection
- **Go type system** - Understands interfaces, slices, maps
- **Better experience** - Commands designed for Go idioms
- **Active development** - Maintained by Go community

## Installation and Setup

### Installation

```bash
# Install latest version
go install github.com/go-delve/delve/cmd/dlv@latest

# Verify installation
dlv version
```

### Configuration

**Optional: Create alias:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias dlv='/path/to/go/bin/dlv'
```

**Disable optimizations for better debugging:**
```bash
# Compile without optimizations
go build -gcflags="all=-N -l" -o myapp
dlv exec ./myapp
```

## Basic Commands

### Starting Delve

```bash
# Debug main package
dlv debug

# Debug specific package
dlv debug github.com/user/project/cmd/app

# Debug with arguments
dlv debug -- --config prod.yaml --verbose

# Debug compiled binary
dlv exec ./myapp

# Attach to running process
dlv attach <pid>

# Debug tests
dlv test
dlv test github.com/user/project/pkg/module
```

### Essential Commands Reference

| Command | Alias | Description |
|---------|-------|-------------|
| `break <location>` | `b` | Set breakpoint |
| `breakpoints` | `bp` | List all breakpoints |
| `clear <number>` | | Clear breakpoint by number |
| `clearall` | | Clear all breakpoints |
| `condition <number> <expr>` | `cond` | Set breakpoint condition |
| `continue` | `c` | Continue execution |
| `next` | `n` | Step over (next line) |
| `step` | `s` | Step into function |
| `stepout` | `so` | Step out of function |
| `restart` | `r` | Restart program |
| `print <expr>` | `p` | Print expression |
| `locals` | | Show local variables |
| `args` | | Show function arguments |
| `vars` | | Show package variables |
| `whatis <expr>` | | Show type of expression |
| `set <var> = <value>` | | Change variable value |
| `stack` | `bt` | Show stack trace |
| `frame <number>` | | Switch to stack frame |
| `up` | | Move up one frame |
| `down` | | Move down one frame |
| `goroutine <id>` | `gr` | Switch to goroutine |
| `goroutines` | `grs` | List all goroutines |
| `list` | `l` | Show source code |
| `funcs <pattern>` | | List functions matching pattern |
| `types <pattern>` | | List types matching pattern |
| `help` | `h` | Show help |
| `quit` | `q` | Exit debugger |

### Setting Breakpoints

**By function:**
```bash
(dlv) break main.main
(dlv) break main.processRequest
```

**By file and line:**
```bash
(dlv) break main.go:42
(dlv) break pkg/handler/http.go:100
```

**By package and function:**
```bash
(dlv) break github.com/user/project/pkg/handler.HandleRequest
```

**With condition:**
```bash
(dlv) break main.go:42
(dlv) condition 1 x > 100
```

### Inspecting Variables

**Print variable:**
```bash
(dlv) print myVar
(dlv) p myVar.Field
(dlv) p myVar.Field.NestedField
```

**Print local variables:**
```bash
(dlv) locals
```

**Print function arguments:**
```bash
(dlv) args
```

**Print package-level variables:**
```bash
(dlv) vars myPackageVar
```

**Pretty print structs:**
```bash
(dlv) print myStruct
main.MyStruct {
    Field1: "value",
    Field2: 42,
}
```

## Goroutine Debugging

### Listing Goroutines

**List all goroutines:**
```bash
(dlv) goroutines
[50 goroutines]
* Goroutine 1 - User: ./main.go:42 main.main (0x109a2f0)
  Goroutine 2 - Runtime: /usr/local/go/src/runtime/proc.go:242 runtime.forcegchelper (0x...)
  Goroutine 5 - User: ./worker.go:15 main.worker (0x109b120)
  ...
```

**Show goroutine stacktraces:**
```bash
(dlv) goroutines -t
* Goroutine 1 - User: ./main.go:42 main.main (0x109a2f0)
    0  0x000000000109a2f0 in main.main
       at ./main.go:42
    1  0x0000000001037e93 in runtime.main
       at /usr/local/go/src/runtime/proc.go:250

  Goroutine 5 - User: ./worker.go:15 main.worker (0x109b120)
    0  0x000000000109b120 in main.worker
       at ./worker.go:15
    1  0x0000000001062d21 in runtime.goexit
       at /usr/local/go/src/runtime/asm_amd64.s:1571
```

### Filtering Goroutines

**Show only user goroutines (exclude runtime):**
```bash
(dlv) goroutines -with user
```

**Show goroutines with location containing "handler":**
```bash
(dlv) goroutines -with userloc handler
```

**Show goroutines currently running:**
```bash
(dlv) goroutines -with running
```

**Show goroutines in specific state:**
```bash
(dlv) goroutines -with waiting  # Waiting for channel, lock, etc.
```

### Switching Between Goroutines

**Switch to specific goroutine:**
```bash
(dlv) goroutine 5
Switched from 1 to 5 (thread 12345)

# Now all commands (print, stack, etc.) operate on goroutine 5
(dlv) stack
(dlv) print localVar
```

**Execute command on all goroutines:**
```bash
(dlv) goroutines -exec stack
# Shows stack trace for every goroutine
```

### Debugging Goroutine Issues

**Deadlock detection:**
```bash
(dlv) goroutines -t
# Look for goroutines blocked on chan send/recv
# Check for circular waits
```

**Example: Debugging channel deadlock:**
```go
// deadlock.go
package main

import "time"

func worker(ch chan int) {
    time.Sleep(1 * time.Second)
    ch <- 42  // Blocks if no receiver
}

func main() {
    ch := make(chan int)
    go worker(ch)
    time.Sleep(5 * time.Second)  // Main doesn't receive
}
```

**Debug session:**
```bash
$ dlv debug deadlock.go
(dlv) break main.main
(dlv) continue
(dlv) next  # Step through to where deadlock occurs
(dlv) goroutines -t
* Goroutine 1 - User: ./deadlock.go:13 main.main (0x...)
  Goroutine 5 - User: ./deadlock.go:8 main.worker (0x...)
      [blocked on channel send]
```

## Advanced Features

### Conditional Breakpoints

**Set condition on existing breakpoint:**
```bash
(dlv) break main.go:42
Breakpoint 1 set at 0x109a2f0 for main.processItem() ./main.go:42

(dlv) condition 1 item.Price > 100
# Now breaks only when item.Price > 100
```

**Complex conditions:**
```bash
(dlv) condition 1 len(items) > 10 && totalPrice > 1000
```

### Tracepoints (Non-Breaking Breakpoints)

**Set tracepoint:**
```bash
(dlv) break main.go:42
(dlv) on 1 trace
# Now logs when line is hit, but doesn't stop execution
```

**Trace with custom message:**
```bash
(dlv) break main.go:42
(dlv) on 1 print "Processing item:", item.ID
# Prints message every time breakpoint is hit
```

### Watchpoints (Data Breakpoints)

**Break when variable changes:**
```bash
(dlv) break main.go:42
(dlv) on 1 cond myVar != oldValue
```

**Note:** Delve doesn't have true hardware watchpoints yet, but conditions can approximate this.

### Function Call Interception

**Break on all calls to function:**
```bash
(dlv) break main.processItem
# Breaks every time processItem is called
```

**Break on specific method calls:**
```bash
(dlv) break (*MyStruct).MyMethod
```

### Starlark Scripting

**Execute Starlark script:**
```bash
(dlv) source script.star
```

**Example script (script.star):**
```python
# Starlark script for Delve
def on_breakpoint(event):
    if event.bp.id == 1:
        print("Breakpoint 1 hit at", event.bp.location)
        vars = Command("locals")
        print("Local variables:", vars)

# Register callback
dlv.on("breakpoint", on_breakpoint)
```

## IDE Integration

### VS Code

**Install Go extension** (includes Delve integration).

**launch.json configuration:**

**Debug main package:**
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
    }
  ]
}
```

**Debug with arguments:**
```json
{
  "name": "Launch with Args",
  "type": "go",
  "request": "launch",
  "mode": "debug",
  "program": "${fileDirname}",
  "args": ["--config", "prod.yaml"]
}
```

**Attach to running process:**
```json
{
  "name": "Attach to Process",
  "type": "go",
  "request": "attach",
  "mode": "local",
  "processId": "${command:pickProcess}"
}
```

**Debug tests:**
```json
{
  "name": "Debug Tests",
  "type": "go",
  "request": "launch",
  "mode": "test",
  "program": "${workspaceFolder}/pkg/mypackage"
}
```

### GoLand / IntelliJ IDEA

GoLand uses Delve internally. Built-in debugger provides:
- Visual breakpoint management
- Goroutine viewer
- Variable inspection
- Step debugging controls

**To use:**
1. Right-click on `main.go` → Debug
2. Or use Debug toolbar button
3. GoLand automatically uses Delve backend

## Remote Debugging

### Delve in Server Mode

**On remote server:**
```bash
# Start Delve in headless mode
dlv debug --headless --listen=:2345 --api-version=2 --accept-multiclient
```

**On local machine:**
```bash
dlv connect remote-server:2345
```

### VS Code Remote Debugging

**launch.json:**
```json
{
  "name": "Connect to Remote",
  "type": "go",
  "request": "attach",
  "mode": "remote",
  "remotePath": "/app",
  "port": 2345,
  "host": "remote-server.com"
}
```

### Debugging in Docker

**Dockerfile:**
```dockerfile
FROM golang:1.21

WORKDIR /app
COPY . .

# Install Delve
RUN go install github.com/go-delve/delve/cmd/dlv@latest

# Compile without optimizations
RUN go build -gcflags="all=-N -l" -o myapp

# Expose debugging port
EXPOSE 2345

# Start with Delve
CMD ["dlv", "--listen=:2345", "--headless=true", "--api-version=2", "--accept-multiclient", "exec", "./myapp"]
```

**docker-compose.yml:**
```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"
      - "2345:2345"  # Delve port
```

**Connect from VS Code:** Use remote attach configuration above.

## Debugging Tests

### Basic Test Debugging

```bash
# Debug all tests in package
dlv test

# Debug specific package
dlv test github.com/user/project/pkg/module

# Debug with test flags
dlv test -- -test.v -test.run TestMyFunction
```

### Debugging Inside Delve

```bash
$ dlv test
Type 'help' for list of commands.
(dlv) break TestMyFunction
(dlv) continue
> github.com/user/project/pkg.TestMyFunction() ./module_test.go:15
(dlv) print testVar
```

### VS Code Test Debugging

**launch.json:**
```json
{
  "name": "Debug Test",
  "type": "go",
  "request": "launch",
  "mode": "test",
  "program": "${workspaceFolder}/pkg/mypackage",
  "args": ["-test.run", "TestMyFunction"]
}
```

## Best Practices

### 1. Use Delve for All Go Debugging

**Why:**
- Designed for Go (goroutines, interfaces)
- Better than GDB for Go code
- Active development and support

### 2. Always Check Goroutines First

**When debugging concurrent code:**
```bash
(dlv) goroutines -t
# Identify blocked/waiting goroutines
# Look for deadlocks, channel issues
```

### 3. Use Tracepoints for Hot Paths

**Instead of breakpoints that stop execution:**
```bash
(dlv) break main.go:42
(dlv) on 1 trace  # Log without stopping
```

### 4. Filter Goroutines to Reduce Noise

```bash
# Exclude runtime goroutines
(dlv) goroutines -with user

# Focus on specific code
(dlv) goroutines -with userloc handler
```

### 5. Compile Without Optimizations

```bash
go build -gcflags="all=-N -l" -o myapp
dlv exec ./myapp
```

**Why:** Optimizations can make variables unavailable or code jump unexpectedly.

### 6. Use Conditional Breakpoints

**Instead of manual stepping:**
```bash
(dlv) break main.go:100
(dlv) condition 1 requestID == "abc-123"
```

### 7. Leverage funcs for Function Discovery

```bash
(dlv) funcs Test*  # Find all test functions
(dlv) funcs handler.*  # Find all handler functions
```

### 8. Use list to Orient Yourself

```bash
(dlv) list
# Shows 10 lines around current position
# Helps understand context
```

### 9. Save Debugging Sessions with restart

```bash
(dlv) restart
# Start over without exiting debugger
# Keeps breakpoints and settings
```

### 10. Remote Debugging for Containers

**For Docker/K8s:**
```bash
# Expose port 2345
# Run Delve in headless mode
# Connect from local machine
```

**Why:** Safer than debugging in production directly.

### 11. Enable Race Detector

```bash
go run -race main.go
# Detects race conditions
# Use Delve after race is found to debug
```

### 12. Use IDE Integration When Possible

**VS Code or GoLand provide:**
- Visual breakpoint management
- Goroutine viewer (GoLand especially)
- Variable inspection sidebar
- Better user experience

### 13. Document Debugging Workflows

**Create runbook for common issues:**
```bash
# Debugging deadlock:
# 1. dlv attach <pid>
# 2. goroutines -t
# 3. Look for blocked goroutines
# 4. Check channel send/recv
```

### 14. Clean Up Breakpoints

```bash
(dlv) breakpoints  # List all
(dlv) clear 1      # Remove specific
(dlv) clearall     # Remove all
```

### 15. Use set to Test Fixes

```bash
(dlv) print myVar
42
(dlv) set myVar = 100  # Test fix without recompiling
(dlv) continue
```
