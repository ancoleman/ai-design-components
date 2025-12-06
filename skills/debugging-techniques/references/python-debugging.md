# Python Debugging Reference

## Table of Contents

1. [pdb - Built-in Python Debugger](#pdb---built-in-python-debugger)
2. [ipdb - Enhanced Debugger](#ipdb---enhanced-debugger)
3. [pudb - Visual Terminal Debugger](#pudb---visual-terminal-debugger)
4. [debugpy - VS Code Integration](#debugpy---vs-code-integration)
5. [Remote Debugging](#remote-debugging)
6. [Debugging Tests](#debugging-tests)
7. [Post-Mortem Debugging](#post-mortem-debugging)
8. [Advanced Techniques](#advanced-techniques)
9. [Best Practices](#best-practices)

## pdb - Built-in Python Debugger

### Basic Usage

**Insert breakpoint (Python 3.7+):**
```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    breakpoint()  # Execution stops here
    return total / count
```

**Older Python versions:**
```python
import pdb
pdb.set_trace()  # Execution stops here
```

### Essential Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `list` | `l` | Show 11 lines around current line |
| `list 10, 20` | `l 10, 20` | Show lines 10 to 20 |
| `longlist` | `ll` | Show entire current function |
| `next` | `n` | Execute current line, step over functions |
| `step` | `s` | Execute current line, step into functions |
| `continue` | `c` | Continue until next breakpoint |
| `return` | `r` | Continue until current function returns |
| `break <line>` | `b` | Set breakpoint at line number |
| `break <function>` | `b` | Set breakpoint at function |
| `tbreak <line>` | | Set temporary breakpoint (removed after hit) |
| `clear <number>` | `cl` | Clear breakpoint by number |
| `disable <number>` | | Disable breakpoint (keep it but don't stop) |
| `enable <number>` | | Re-enable breakpoint |
| `ignore <number> <count>` | | Ignore breakpoint N times |
| `print <expr>` | `p` | Print expression value |
| `pp <expr>` | | Pretty-print expression value |
| `display <expr>` | | Auto-display expression on each step |
| `undisplay <expr>` | | Stop auto-displaying expression |
| `where` | `w` | Show stack trace (call stack) |
| `up` | `u` | Move up one stack frame |
| `down` | `d` | Move down one stack frame |
| `args` | `a` | Show arguments of current function |
| `locals()` | | Show local variables (use with print) |
| `globals()` | | Show global variables (use with print) |
| `whatis <expr>` | | Show type of expression |
| `source <expr>` | | Show source code for expression |
| `help` | `h` | Show help |
| `help <command>` | `h <cmd>` | Show help for command |
| `quit` | `q` | Exit debugger |

### Conditional Breakpoints

**Break only when condition is true:**
```python
# Set breakpoint at line 10, only if x > 5
(Pdb) break 10, x > 5

# Or set breakpoint first, then add condition
(Pdb) break 10
(Pdb) condition 1 x > 5
```

### Example Session

```python
# bug.py
def calculate_discount(price, discount_percent):
    discount = price * discount_percent
    final_price = price - discount
    breakpoint()
    return final_price

result = calculate_discount(100, 0.2)
print(f"Final price: ${result}")
```

**Debugging session:**
```
$ python bug.py
> /path/to/bug.py(4)calculate_discount()
-> return final_price
(Pdb) list
  1     def calculate_discount(price, discount_percent):
  2         discount = price * discount_percent
  3         final_price = price - discount
  4  ->     breakpoint()
  5         return final_price
  6
  7     result = calculate_discount(100, 0.2)
(Pdb) print price
100
(Pdb) print discount_percent
0.2
(Pdb) print discount
20.0
(Pdb) print final_price
80.0
(Pdb) continue
Final price: $80.0
```

## ipdb - Enhanced Debugger

### Why ipdb?

- Tab completion for variables and methods
- Syntax highlighting
- Better introspection (dir(), help() more useful)
- IPython magic commands available
- Persistent command history

### Installation

```bash
pip install ipdb
```

### Usage

```python
import ipdb
ipdb.set_trace()

# Or use environment variable to use ipdb for breakpoint()
# export PYTHONBREAKPOINT=ipdb.set_trace
# Then breakpoint() will use ipdb
```

### Enhanced Features

**Tab completion:**
```
(Pdb) my_var.<TAB>
# Shows available methods/attributes

(Pdb) my_va<TAB>
# Completes variable name
```

**Syntax highlighting:**
- Code listings are colorized
- Variable values are highlighted

**IPython integration:**
```
(Pdb) %timeit expensive_function()  # IPython magic
(Pdb) !ls -la  # Shell commands
```

## pudb - Visual Terminal Debugger

### Why pudb?

- Visual interface in terminal (TUI)
- Sidebar with variables
- Breakpoint manager
- Stack viewer
- Navigation with arrow keys
- No need for X server or GUI

### Installation

```bash
pip install pudb
```

### Usage

```python
import pudb
pudb.set_trace()

# Or from command line
python -m pudb script.py
```

### Navigation

- **Arrow keys** - Navigate code
- **n** - Next line
- **s** - Step into
- **c** - Continue
- **b** - Set/clear breakpoint at current line
- **t** - Go to current line
- **u/d** - Up/down stack frame
- **q** - Quit

### Interface Layout

```
┌─────────────────────────────────────────┐
│ Variables                               │
│  price: 100                            │
│  discount_percent: 0.2                 │
│  discount: 20.0                        │
├─────────────────────────────────────────┤
│ Stack                                   │
│  calculate_discount()                  │
│  <module>                              │
├─────────────────────────────────────────┤
│ Breakpoints                            │
│  bug.py:4                              │
└─────────────────────────────────────────┘
```

## debugpy - VS Code Integration

### Setup

**Install VS Code Python extension** - includes debugpy automatically.

### launch.json Configuration

**Debug current file:**
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
    }
  ]
}
```

**Debug with arguments:**
```json
{
  "name": "Python: With Arguments",
  "type": "python",
  "request": "launch",
  "program": "${file}",
  "args": ["--config", "prod.yaml"],
  "console": "integratedTerminal"
}
```

**Debug module:**
```json
{
  "name": "Python: Module",
  "type": "python",
  "request": "launch",
  "module": "myapp.main",
  "console": "integratedTerminal"
}
```

## Remote Debugging

### debugpy Remote Attach

**On remote server:**
```python
import debugpy

# Start debug server on port 5678
debugpy.listen(("0.0.0.0", 5678))
print("Waiting for debugger to attach...")
debugpy.wait_for_client()  # Blocks until debugger connects
print("Debugger attached!")

# Your code here
breakpoint()
```

**VS Code launch.json (on local machine):**
```json
{
  "name": "Python: Remote Attach",
  "type": "python",
  "request": "attach",
  "connect": {
    "host": "remote-server.com",
    "port": 5678
  },
  "pathMappings": [
    {
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app"
    }
  ]
}
```

**SSH tunnel (if firewall blocks port):**
```bash
# Forward remote port 5678 to local port 5678
ssh -L 5678:localhost:5678 user@remote-server.com

# In launch.json, connect to localhost:5678
```

### Remote Debugging in Docker

**docker-compose.yml:**
```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "5678:5678"  # Debugging port
    environment:
      - PYTHONBREAKPOINT=debugpy.set_trace
```

**In application code:**
```python
import debugpy
debugpy.listen(("0.0.0.0", 5678))
# Don't wait for client in production!
# debugpy.wait_for_client()  # Comment out or use env var
```

## Debugging Tests

### pytest Integration

**Drop into debugger on failure:**
```bash
pytest --pdb
```

**Drop into debugger on first failure, then exit:**
```bash
pytest --pdb -x
```

**Drop into debugger immediately (before test runs):**
```bash
pytest --trace
```

**Debug specific test:**
```bash
pytest tests/test_module.py::test_function --pdb
```

### Debugging in Test Code

```python
def test_calculate_discount():
    price = 100
    discount = 0.2
    breakpoint()  # Drop into debugger during test
    result = calculate_discount(price, discount)
    assert result == 80
```

### unittest Integration

```python
import unittest
import pdb

class TestCalculator(unittest.TestCase):
    def test_discount(self):
        price = 100
        discount = 0.2
        pdb.set_trace()  # Drop into debugger
        result = calculate_discount(price, discount)
        self.assertEqual(result, 80)
```

## Post-Mortem Debugging

### Debugging After Crash

**From command line:**
```bash
python -m pdb script.py
# If script crashes, pdb drops into post-mortem mode
```

**In code:**
```python
import pdb
import sys

def main():
    try:
        # Your code here
        risky_operation()
    except Exception:
        # Drop into debugger at exception point
        pdb.post_mortem(sys.exc_info()[2])
        raise

if __name__ == "__main__":
    main()
```

### Automatic Post-Mortem

**Environment variable:**
```bash
# Automatically drop into pdb on uncaught exception
export PYTHONBREAKPOINT=pdb.set_trace
python -m pdb script.py
```

**IPython integration:**
```python
# In IPython/Jupyter
%pdb on  # Enable automatic post-mortem debugging
# Now any exception drops into ipdb
```

## Advanced Techniques

### Debugging Decorators

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        breakpoint()  # Debug decorator logic
        result = func(*args, **kwargs)
        return result
    return wrapper

@my_decorator
def my_function():
    pass
```

### Debugging Lambda Functions

```python
# Lambda with debugging
result = map(lambda x: (breakpoint(), x * 2)[1], numbers)
```

### Debugging Comprehensions

```python
# Break before comprehension
breakpoint()
result = [x * 2 for x in numbers if x > 5]

# Or convert to loop for easier debugging
result = []
for x in numbers:
    if x > 5:
        breakpoint()  # Debug inside loop
        result.append(x * 2)
```

### Debugging Async Code

```python
async def async_function():
    breakpoint()  # Works in async functions
    await some_async_operation()
```

### Custom pdb Commands

```python
import pdb

class CustomPdb(pdb.Pdb):
    def do_info(self, arg):
        """Custom command: info - Show all local variables"""
        frame = self.curframe
        print(frame.f_locals)

# Use custom debugger
CustomPdb().set_trace()
```

## Best Practices

### 1. Use breakpoint() over pdb.set_trace()

**Why:**
- Respects PYTHONBREAKPOINT environment variable
- Can switch debuggers without code changes
- Python 3.7+ standard

```python
# Good
breakpoint()

# Old style
import pdb; pdb.set_trace()
```

### 2. Leverage pp for Complex Data Structures

```python
(Pdb) pp large_dict
{
    'key1': 'value1',
    'key2': {
        'nested': 'data'
    }
}
```

### 3. Use Conditional Breakpoints

**Instead of:**
```python
for i in range(1000):
    breakpoint()  # Stops 1000 times!
    if i == 500:
        process(i)
```

**Do this:**
```python
for i in range(1000):
    if i == 500:
        breakpoint()  # Stops once
    process(i)
```

**Or use pdb condition:**
```
(Pdb) break 10, i == 500
```

### 4. Remove Breakpoints Before Commit

**Add to .gitignore or use pre-commit hook:**
```bash
# Check for breakpoint() calls
git diff --cached | grep -n "breakpoint()"
```

### 5. Use Post-Mortem for Crashes

**Instead of re-running:**
```bash
python -m pdb script.py
# Automatically drops into debugger on crash
```

### 6. Debugging in Production (Carefully)

**Use logging instead of breakpoints:**
```python
import logging
logging.debug(f"Variable value: {x}")
```

**If must use debugger:**
- Use debugpy remote attach (doesn't block other requests)
- Never use breakpoint() in production (blocks all execution)
- Consider snapshot debugging tools (Lightrun, Rookout)

### 7. Clean Debugger State

**Reset if state gets confusing:**
```
(Pdb) restart  # Restart program from beginning
```

### 8. Use IDE Integration When Available

**VS Code, PyCharm provide:**
- Visual breakpoint management
- Variable inspection sidebar
- Easier navigation
- Better user experience

### 9. Debugging Multi-threaded Code

```python
import threading
import pdb

def worker():
    breakpoint()  # Works, but only one thread can be in debugger
    process_data()

threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
```

**Note:** pdb is not thread-safe. Consider logging for multi-threaded debugging.

### 10. Environment-Specific Debugging

```python
import os

if os.getenv("DEBUG") == "1":
    breakpoint()
```

```bash
DEBUG=1 python script.py  # Enables debugging
python script.py          # Skips debugging
```
