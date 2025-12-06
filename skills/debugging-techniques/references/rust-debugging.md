# Rust Debugging Reference

## Table of Contents

1. [LLDB vs GDB](#lldb-vs-gdb)
2. [Compilation for Debugging](#compilation-for-debugging)
3. [LLDB Commands](#lldb-commands)
4. [GDB Commands](#gdb-commands)
5. [VS Code Integration](#vs-code-integration)
6. [Debugging Tests](#debugging-tests)
7. [Rust-Specific Challenges](#rust-specific-challenges)
8. [Best Practices](#best-practices)

## LLDB vs GDB

### LLDB (Recommended)

**Pros:**
- Default Rust debugger
- Better Rust type support
- Cross-platform (Mac, Linux, Windows MSVC)
- Active development

**Installation:**
```bash
# Mac
brew install llvm

# Ubuntu/Debian
sudo apt install lldb

# Fedora
sudo dnf install lldb
```

### GDB (Alternative)

**Pros:**
- Familiar to Linux developers
- Wide documentation
- Works well on Linux

**Installation:**
```bash
# Ubuntu/Debian
sudo apt install gdb

# Fedora
sudo dnf install gdb
```

### Recommendation

Use LLDB unless you have specific reasons to prefer GDB.

## Compilation for Debugging

### Debug Build (Default)

```bash
cargo build
# Produces target/debug/binary with full debug symbols
```

### Release Build with Debug Symbols

```bash
# Option 1: Command flag
cargo build --release --config "profile.release.debug=true"

# Option 2: Cargo.toml
[profile.release]
debug = true
```

### Optimization Levels

```toml
[profile.dev]
opt-level = 0  # No optimization (default for debug)

[profile.release]
opt-level = 3  # Maximum optimization (default for release)
```

## LLDB Commands

### Starting LLDB

```bash
# Debug binary
rust-lldb target/debug/myapp

# With arguments
rust-lldb target/debug/myapp -- --config prod.yaml

# Attach to running process
rust-lldb -p <pid>
```

### Essential Commands

| Command | Description |
|---------|-------------|
| `breakpoint set -f main.rs -l 10` | Set breakpoint at line |
| `breakpoint set -n main` | Set breakpoint at function |
| `breakpoint list` | List all breakpoints |
| `breakpoint delete <num>` | Delete breakpoint |
| `run` (r) | Start program |
| `continue` (c) | Continue execution |
| `next` (n) | Step over |
| `step` (s) | Step into |
| `finish` | Step out of function |
| `print variable` (p) | Print variable |
| `frame variable` (fr v) | Show local variables |
| `backtrace` (bt) | Show stack trace |
| `thread list` | List all threads |
| `frame select <num>` | Switch to frame |
| `up` | Move up stack frame |
| `down` | Move down stack frame |
| `quit` | Exit debugger |

### Example Session

```bash
$ rust-lldb target/debug/myapp
(lldb) breakpoint set -f main.rs -l 10
Breakpoint 1: where = myapp`myapp::main + 42 at main.rs:10

(lldb) run
Process 12345 launched
* thread #1, name = 'main', stop reason = breakpoint 1.1
    frame #0: 0x55555556789a myapp`myapp::main at main.rs:10
   7   	fn main() {
   8   	    let x = 5;
   9   	    let y = 10;
-> 10  	    println!("x + y = {}", x + y);
   11  	}

(lldb) print x
(i32) $0 = 5

(lldb) print y
(i32) $1 = 10

(lldb) continue
x + y = 15
Process 12345 exited with status = 0
```

### Conditional Breakpoints

```bash
(lldb) breakpoint set -f main.rs -l 10 -c 'x > 5'
# Breaks only when x > 5
```

## GDB Commands

### Starting GDB

```bash
# Debug binary
rust-gdb target/debug/myapp

# With arguments
rust-gdb --args target/debug/myapp --config prod.yaml

# Attach to running process
rust-gdb -p <pid>
```

### Essential Commands

| Command | Description |
|---------|-------------|
| `break main.rs:10` (b) | Set breakpoint at line |
| `break main` (b) | Set breakpoint at function |
| `info breakpoints` | List breakpoints |
| `delete <num>` (d) | Delete breakpoint |
| `run` (r) | Start program |
| `continue` (c) | Continue execution |
| `next` (n) | Step over |
| `step` (s) | Step into |
| `finish` | Step out of function |
| `print variable` (p) | Print variable |
| `info locals` | Show local variables |
| `backtrace` (bt) | Show stack trace |
| `info threads` | List threads |
| `frame <num>` (f) | Switch to frame |
| `up` | Move up stack frame |
| `down` | Move down stack frame |
| `quit` (q) | Exit debugger |

## VS Code Integration

### CodeLLDB Extension

**Install extension:**
- Extension ID: `vadimcn.vscode-lldb`
- Search "CodeLLDB" in VS Code extensions

### launch.json Configuration

**Debug main binary:**
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
    }
  ]
}
```

**Debug with arguments:**
```json
{
  "type": "lldb",
  "request": "launch",
  "name": "Debug with Args",
  "program": "${workspaceFolder}/target/debug/myapp",
  "args": ["--config", "prod.yaml"],
  "cwd": "${workspaceFolder}"
}
```

**Debug tests:**
```json
{
  "type": "lldb",
  "request": "launch",
  "name": "Debug Test",
  "program": "${workspaceFolder}/target/debug/deps/myapp-<hash>",
  "args": ["test_name"],
  "cwd": "${workspaceFolder}"
}
```

**Pre-launch task (build before debug):**
```json
{
  "type": "lldb",
  "request": "launch",
  "name": "Debug",
  "program": "${workspaceFolder}/target/debug/${workspaceFolderBasename}",
  "preLaunchTask": "cargo build",
  "cwd": "${workspaceFolder}"
}
```

### tasks.json for Build Task

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "cargo build",
      "type": "shell",
      "command": "cargo",
      "args": ["build"],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

## Debugging Tests

### Building Test Binary

```bash
# Build test binary without running
cargo test --no-run

# Binary location
ls target/debug/deps/myapp-*
```

### Debugging with LLDB

```bash
# Find test binary
cargo test --no-run
# Note the binary path in output

# Debug test binary
rust-lldb target/debug/deps/myapp-<hash>

(lldb) breakpoint set -n test_function
(lldb) run test_function
```

### Debugging Specific Test

```bash
# Build specific test
cargo test --test integration_test --no-run

# Debug it
rust-lldb target/debug/deps/integration_test-<hash>

(lldb) breakpoint set -n my_test
(lldb) run my_test
```

### VS Code Test Debugging

**launch.json:**
```json
{
  "type": "lldb",
  "request": "launch",
  "name": "Debug Current Test",
  "program": "${workspaceFolder}/target/debug/deps/${workspaceFolderBasename}-<hash>",
  "args": ["${selectedText}"],
  "preLaunchTask": "cargo test --no-run"
}
```

## Rust-Specific Challenges

### 1. Ownership and Borrowing

**Problem:** Variables may be moved, making them unavailable.

```rust
let x = String::from("hello");
let y = x;  // x is moved
// Cannot inspect x anymore in debugger
```

**Solution:** Use clone() temporarily for debugging:
```rust
let x = String::from("hello");
let y = x.clone();  // x still available
// Now can inspect both x and y
```

### 2. Name Mangling

**Problem:** Function names are mangled for uniqueness.

**Solution:**
- `rust-lldb` and `rust-gdb` wrappers handle demangling automatically
- For C FFI, use `#[no_mangle]` attribute

```rust
#[no_mangle]
pub extern "C" fn my_function() {
    // Can set breakpoint as "my_function" instead of mangled name
}
```

### 3. Optimizations

**Problem:** Release builds inline and optimize out variables.

**Solution:**
- Always use debug builds for debugging (`cargo build`)
- If must debug release, add debug symbols:

```toml
[profile.release]
debug = true
opt-level = 1  # Reduce optimization
```

### 4. Macros

**Problem:** Macro expansions can be confusing in debugger.

**Solution:** Use `cargo expand` to see macro output:

```bash
# Install cargo-expand
cargo install cargo-expand

# Expand macros
cargo expand

# Expand specific module
cargo expand module_name
```

### 5. Generic Functions

**Problem:** Generic functions are monomorphized, creating multiple copies.

**Solution:** Set breakpoints on specific instantiations:
```bash
(lldb) breakpoint set -n 'process<i32>'
(lldb) breakpoint set -n 'process<String>'
```

### 6. Async Code

**Problem:** Async functions are transformed into state machines.

**Solution:**
- Debug at state machine level (complex)
- Or use println! debugging for async code
- Consider using tokio-console for async debugging

### 7. Trait Objects

**Problem:** Dynamic dispatch makes it hard to see concrete type.

**Solution:**
```bash
(lldb) print *object
# Shows vtable and data
```

## Best Practices

### 1. Always Use Debug Builds

```bash
cargo build  # Not cargo build --release
```

**Why:** Release builds optimize out variables and inline code.

### 2. Use rust-lldb / rust-gdb Wrappers

```bash
# Good
rust-lldb target/debug/myapp

# Bad (misses Rust-specific pretty-printing)
lldb target/debug/myapp
```

### 3. Install Pretty Printers

**For GDB:**
```bash
# Add to ~/.gdbinit
python
import sys
sys.path.insert(0, '/path/to/rust-src/etc')
import gdb_rust_pretty_printing
gdb_rust_pretty_printing.register_printers(gdb)
end
```

**For LLDB:**
- `rust-lldb` includes pretty printers automatically

### 4. Use cargo expand for Macros

```bash
cargo expand | less
# Understand what macros generate before debugging
```

### 5. Understand Ownership

**If variable is unavailable:**
- It may have been moved
- Use clone() temporarily
- Check borrow checker rules

### 6. Debug Builds Only

**Don't debug release builds:**
- Variables are optimized out
- Code is inlined and reordered
- Confusing experience

### 7. Use VS Code for Better Experience

**CodeLLDB provides:**
- Visual breakpoint management
- Variable inspection
- Watch expressions
- Better navigation

### 8. Check Thread State

```bash
(lldb) thread list
# Identify panicked or blocked threads
```

### 9. Use backtrace for Panics

```rust
// In Cargo.toml
[profile.dev]
panic = 'unwind'  # Default, allows backtrace

// Or set environment variable
RUST_BACKTRACE=1 cargo run
```

### 10. Consider println! Debugging

**For complex async code or tight loops:**
```rust
println!("Debug: x = {:?}", x);
```

**Why:** Sometimes simpler than debugger for certain scenarios.

### 11. Use #[track_caller]

```rust
#[track_caller]
fn expect_value(val: Option<i32>) -> i32 {
    val.unwrap()  // Panic shows caller location
}
```

### 12. Enable Debug Logging

```rust
use log::{debug, info};

debug!("Processing item: {:?}", item);
```

### 13. Use cargo test --nocapture

```bash
cargo test --nocapture
# See println! output during tests
```

### 14. Debugging Panics

```bash
# Set RUST_BACKTRACE
RUST_BACKTRACE=full cargo run

# Or in debugger
(lldb) breakpoint set -n rust_panic
(lldb) run
```

### 15. Remote Debugging

**If debugging on remote server:**
```bash
# On server
lldb-server platform --listen 0.0.0.0:1234 --server

# On local machine
(lldb) platform select remote-linux
(lldb) platform connect connect://remote:1234
(lldb) target create target/debug/myapp
(lldb) run
```
