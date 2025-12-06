# Output Formatting Guide

Guide to formatting CLI output for both human and machine consumption.

## Table of Contents

- [Output Modes](#output-modes)
- [Human-Readable Output](#human-readable-output)
- [Machine-Readable Output](#machine-readable-output)
- [Progress Indicators](#progress-indicators)
- [Error Handling](#error-handling)

## Output Modes

### Standard Output Streams

**stdout (Standard Output):**
- Use for data and results
- Pipe-friendly (can be piped to other commands)
- Example: `myapp list | jq '.'`

**stderr (Standard Error):**
- Use for errors, warnings, and log messages
- Not captured by pipes (unless explicitly redirected)
- Example: Progress bars, debug messages

**Exit Codes:**
- `0`: Success
- `1`: General error
- `2`: Usage error (invalid arguments)
- Custom codes: Document in help text

## Human-Readable Output

### Tables

**Python (rich):**
```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Deployments")
table.add_column("Name", style="cyan")
table.add_column("Status", style="magenta")
table.add_column("Age", style="green")

table.add_row("web-app", "Running", "2d")
table.add_row("api-server", "Stopped", "5h")

console.print(table)
```

**Go (tablewriter):**
```go
import "github.com/olekukonko/tablewriter"

table := tablewriter.NewWriter(os.Stdout)
table.SetHeader([]string{"Name", "Status", "Age"})
table.Append([]string{"web-app", "Running", "2d"})
table.Append([]string{"api-server", "Stopped", "5h"})
table.Render()
```

**Rust (comfy-table):**
```rust
use comfy_table::{Table, Row};

let mut table = Table::new();
table.set_header(vec!["Name", "Status", "Age"]);
table.add_row(vec!["web-app", "Running", "2d"]);
table.add_row(vec!["api-server", "Stopped", "5h"]);
println!("{table}");
```

### Colored Output

**Auto-detect TTY:**
```python
import sys

def supports_color():
    return sys.stdout.isatty()

if supports_color():
    # Use colors
    print("\033[32mSuccess!\033[0m")
else:
    # Plain text
    print("Success!")
```

**Python (rich):**
```python
from rich.console import Console

console = Console()
console.print("[green]Success![/green]")
console.print("[red]Error![/red]")
console.print("[yellow]Warning[/yellow]")
```

**Go (color):**
```go
import "github.com/fatih/color"

color.Green("Success!")
color.Red("Error!")
color.Yellow("Warning")
```

**Rust (colored):**
```rust
use colored::*;

println!("{}", "Success!".green());
println!("{}", "Error!".red());
println!("{}", "Warning".yellow());
```

## Machine-Readable Output

### JSON Output

**Python:**
```python
import json

@app.command()
def list_items(output: str = typer.Option("table", "--output", "-o")):
    items = [
        {"name": "web-app", "status": "running"},
        {"name": "api-server", "status": "stopped"},
    ]

    if output == "json":
        print(json.dumps(items, indent=2))
    elif output == "table":
        # ... table rendering
        pass
```

**Go:**
```go
import "encoding/json"

if outputFormat == "json" {
    data, _ := json.MarshalIndent(items, "", "  ")
    fmt.Println(string(data))
}
```

**Rust:**
```rust
use serde_json;

if output_format == "json" {
    println!("{}", serde_json::to_string_pretty(&items)?);
}
```

### YAML Output

**Python:**
```python
import yaml

print(yaml.dump(items, default_flow_style=False))
```

**Go:**
```go
import "gopkg.in/yaml.v3"

data, _ := yaml.Marshal(items)
fmt.Println(string(data))
```

**Rust:**
```rust
use serde_yaml;

println!("{}", serde_yaml::to_string(&items)?);
```

## Progress Indicators

### Progress Bars

**Python (rich):**
```python
from rich.progress import Progress
import time

with Progress() as progress:
    task = progress.add_task("[cyan]Processing...", total=100)
    for i in range(100):
        time.sleep(0.01)
        progress.update(task, advance=1)
```

**Go (progressbar):**
```go
import "github.com/schollz/progressbar/v3"

bar := progressbar.Default(100)
for i := 0; i < 100; i++ {
    bar.Add(1)
    time.Sleep(10 * time.Millisecond)
}
```

**Rust (indicatif):**
```rust
use indicatif::ProgressBar;

let bar = ProgressBar::new(100);
for _ in 0..100 {
    bar.inc(1);
    thread::sleep(Duration::from_millis(10));
}
bar.finish_with_message("Done!");
```

### Spinners

**Python (rich):**
```python
from rich.console import Console

console = Console()
with console.status("[bold green]Working..."):
    time.sleep(3)  # Do work
```

**Go (spinner):**
```go
import "github.com/briandowns/spinner"

s := spinner.New(spinner.CharSets[9], 100*time.Millisecond)
s.Start()
time.Sleep(3 * time.Second)
s.Stop()
```

**Rust (indicatif):**
```rust
use indicatif::ProgressBar;

let spinner = ProgressBar::new_spinner();
spinner.set_message("Working...");
thread::sleep(Duration::from_secs(3));
spinner.finish_with_message("Done!");
```

## Error Handling

### Error Messages

**Best Practices:**
- Write errors to stderr
- Provide actionable suggestions
- Include error codes for scripting
- Use colors for visibility (if TTY)

**Python:**
```python
import sys

def error(message: str, exit_code: int = 1):
    console.print(f"[red]Error:[/red] {message}", file=sys.stderr)
    raise typer.Exit(exit_code)

# Usage
if not file_exists:
    error("Config file not found. Run 'myapp config init' to create one.")
```

**Go:**
```go
import (
    "fmt"
    "os"
)

func error(message string, exitCode int) {
    fmt.Fprintf(os.Stderr, "Error: %s\n", message)
    os.Exit(exitCode)
}
```

**Rust:**
```rust
eprintln!("Error: {}", message);
std::process::exit(1);
```

### Warnings

**Python:**
```python
console.print("[yellow]Warning:[/yellow] Using default configuration", file=sys.stderr)
```

**Go:**
```go
fmt.Fprintf(os.Stderr, "Warning: %s\n", message)
```

**Rust:**
```rust
eprintln!("Warning: {}", message);
```

## Best Practices Summary

**Output Design:**
- Default to human-readable (tables, colors)
- Provide `--output` flag for JSON/YAML
- Write data to stdout, logs to stderr
- Disable colors when not a TTY

**Progress Indicators:**
- Use progress bars for operations >2 seconds
- Use spinners for indeterminate operations
- Write to stderr (keeps stdout clean)

**Error Handling:**
- Clear error messages with suggestions
- Use exit codes: 0 = success, 1 = error, 2 = usage
- Log errors to stderr
- Provide `--verbose` for debugging
