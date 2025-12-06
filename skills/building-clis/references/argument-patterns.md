# Argument Parsing Patterns

Comprehensive guide to arguments, options, and flags with decision frameworks and multi-language implementations.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Argument Types](#argument-types)
- [Decision Matrix](#decision-matrix)
- [Validation Patterns](#validation-patterns)
- [Multi-Value Arguments](#multi-value-arguments)
- [Language-Specific Patterns](#language-specific-patterns)

## Core Concepts

### Definitions

**Positional Argument:**
- Value identified by position, not name
- Can be required or optional
- Order matters
- Example: `git commit -m "message"` (message is argument to `-m`)

**Option (Named Parameter):**
- Named parameter with a value
- Identified by flag name (short or long form)
- Example: `--output file.txt`, `-o file.txt`

**Flag (Boolean Option):**
- Boolean parameter (presence = true, absence = false)
- No value required
- Example: `--verbose`, `--dry-run`, `-v`

### GNU Conventions

Follow POSIX and GNU standards:

**Short Form:**
- Single dash + single character: `-v`, `-o file.txt`
- Can be combined: `-vf` = `-v -f`

**Long Form:**
- Double dash + descriptive name: `--verbose`, `--output file.txt`
- More readable, self-documenting

**Mixed Usage:**
```bash
command -v --output file.txt input.txt
# -v: short flag
# --output file.txt: long option
# input.txt: positional argument
```

**Argument Separator:**
```bash
command --option value -- --file-starting-with-dash.txt
# -- separates options from positional arguments
# Allows files/args that start with dashes
```

## Argument Types

### 1. Required Positional Arguments

**Use Case:** Primary input that is always needed

**Example:**
```bash
convert input.jpg output.png
# input.jpg and output.png are required positional args
```

**Implementation:**

**Python (Typer):**
```python
def convert(
    input_file: Annotated[str, typer.Argument(help="Input file")],
    output_file: Annotated[str, typer.Argument(help="Output file")]
):
    pass
```

**Go (Cobra):**
```go
var convertCmd = &cobra.Command{
    Use:   "convert <input> <output>",
    Args:  cobra.ExactArgs(2),  // Exactly 2 required
    Run: func(cmd *cobra.Command, args []string) {
        inputFile := args[0]
        outputFile := args[1]
    },
}
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Input file
    input_file: String,
    /// Output file
    output_file: String,
}
```

### 2. Optional Positional Arguments

**Use Case:** Input that has a sensible default

**Example:**
```bash
log show error.log  # Use error.log
log show            # Use default log file
```

**Implementation:**

**Python (Typer):**
```python
def show(
    log_file: Annotated[str, typer.Argument()] = "app.log"
):
    pass
```

**Go (Cobra):**
```go
var showCmd = &cobra.Command{
    Use:   "show [log_file]",
    Args:  cobra.MaximumNArgs(1),  // 0 or 1 arg
    Run: func(cmd *cobra.Command, args []string) {
        logFile := "app.log"
        if len(args) > 0 {
            logFile = args[0]
        }
    },
}
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Log file to show
    #[arg(default_value = "app.log")]
    log_file: String,
}
```

### 3. Required Options

**Use Case:** Configuration that must be explicitly set

**Example:**
```bash
deploy --env production
# --env is required, no default
```

**Implementation:**

**Python (Typer):**
```python
def deploy(
    env: Annotated[str, typer.Option("--env", help="Environment")] = ...
    # ... means required
):
    pass
```

**Go (Cobra):**
```go
var env string

var deployCmd = &cobra.Command{
    Use: "deploy",
    Run: func(cmd *cobra.Command, args []string) {
        // env is populated
    },
}

deployCmd.Flags().StringVar(&env, "env", "", "Environment")
deployCmd.MarkFlagRequired("env")
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Environment (required)
    #[arg(long)]
    env: String,  // No Option<> = required
}
```

### 4. Optional Options with Defaults

**Use Case:** Configuration with sensible defaults

**Example:**
```bash
serve --port 8080  # Use 8080
serve              # Use default port 3000
```

**Implementation:**

**Python (Typer):**
```python
def serve(
    port: Annotated[int, typer.Option("--port")] = 3000
):
    pass
```

**Go (Cobra):**
```go
var port int

rootCmd.Flags().IntVar(&port, "port", 3000, "Server port")
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Server port
    #[arg(long, default_value_t = 3000)]
    port: u16,
}
```

### 5. Boolean Flags

**Use Case:** Toggle behaviors on/off

**Example:**
```bash
build --verbose --dry-run
# Both flags are present = true
```

**Implementation:**

**Python (Typer):**
```python
def build(
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False
):
    pass
```

**Go (Cobra):**
```go
var verbose bool
var dryRun bool

rootCmd.Flags().BoolVarP(&verbose, "verbose", "v", false, "Verbose output")
rootCmd.Flags().BoolVar(&dryRun, "dry-run", false, "Dry run mode")
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Verbose output
    #[arg(short, long)]
    verbose: bool,

    /// Dry run mode
    #[arg(long)]
    dry_run: bool,
}
```

### 6. Counting Flags

**Use Case:** Increase level by repetition (e.g., verbosity)

**Example:**
```bash
command -v      # verbosity level 1
command -vv     # verbosity level 2
command -vvv    # verbosity level 3
```

**Implementation:**

**Python (Typer):**
```python
def command(
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0
):
    # verbose = number of -v flags
    pass
```

**Go (Cobra):**
```go
var verbose int

rootCmd.Flags().CountVarP(&verbose, "verbose", "v", "Increase verbosity")
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Increase verbosity (-v, -vv, -vvv)
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,
}
```

## Decision Matrix

### When to Use Each Type

| Use Case | Type | Example | Rationale |
|----------|------|---------|-----------|
| **Primary required input** | Positional Argument | `convert input.jpg` | Clear, minimal typing |
| **Primary optional input** | Positional or Option | `show [logfile]` | Explicit when needed |
| **Output destination** | Option | `--output file.txt` | Flexible, can default to stdout |
| **Configuration value** | Option | `--config app.yaml` | Explicit, discoverable |
| **Boolean toggle** | Flag | `--verbose`, `--force` | Clear intent, no value |
| **Multiple values** | Variadic Argument | `files...` | Natural for lists |
| **Incremental setting** | Counting Flag | `-vvv` | Concise for levels |
| **Mutually exclusive** | Enum/Choice Option | `--mode [dev\|prod]` | Constrained choices |

### Argument Limits

**Best Practices:**
- **Max 2-3 positional arguments:** More becomes confusing
- **Use options for 3+ parameters:** Named params are clearer
- **Limit flags to 10-15:** Too many options overwhelm users

**Example of Too Many Positional Args (BAD):**
```bash
deploy production us-west-2 blue-green v1.2.3 true false
# What do these mean? Use options instead!
```

**Better Approach:**
```bash
deploy \
  --env production \
  --region us-west-2 \
  --strategy blue-green \
  --version v1.2.3 \
  --verbose \
  --no-backup
```

## Validation Patterns

### Type Validation

**Python (Typer with Pydantic):**
```python
from typing import Annotated
from pydantic import validator

def deploy(
    port: Annotated[int, typer.Option(min=1, max=65535)] = 8080
):
    # Automatic validation: port must be 1-65535
    pass
```

**Go (Cobra with Custom Validation):**
```go
var port int

deployCmd.Flags().IntVar(&port, "port", 8080, "Port number")

deployCmd.PreRunE = func(cmd *cobra.Command, args []string) error {
    if port < 1 || port > 65535 {
        return fmt.Errorf("port must be between 1 and 65535")
    }
    return nil
}
```

**Rust (clap with value_parser):**
```rust
use clap::{Parser, value_parser};

#[derive(Parser)]
struct Cli {
    /// Port number (1-65535)
    #[arg(long, value_parser = value_parser!(u16).range(1..=65535))]
    port: u16,
}
```

### Choice/Enum Validation

**Python (Typer with Enum):**
```python
from enum import Enum

class Environment(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"

def deploy(env: Annotated[Environment, typer.Option()]):
    # env is automatically validated
    pass
```

**Go (Cobra with ValidArgs):**
```go
var deployCmd = &cobra.Command{
    Use:       "deploy [env]",
    ValidArgs: []string{"dev", "staging", "prod"},
    Args:      cobra.OnlyValidArgs,
}
```

**Rust (clap with value_enum):**
```rust
use clap::{Parser, ValueEnum};

#[derive(ValueEnum, Clone)]
enum Environment {
    Dev,
    Staging,
    Prod,
}

#[derive(Parser)]
struct Cli {
    #[arg(long, value_enum)]
    env: Environment,
}
```

### Path Validation

**Python (Typer with Path):**
```python
from pathlib import Path

def process(
    input_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)]
):
    # Validates file exists and is not a directory
    pass
```

**Go (Cobra with Custom Validation):**
```go
deployCmd.PreRunE = func(cmd *cobra.Command, args []string) error {
    if _, err := os.Stat(configFile); os.IsNotExist(err) {
        return fmt.Errorf("config file %s does not exist", configFile)
    }
    return nil
}
```

**Rust (clap with value_parser):**
```rust
use std::path::PathBuf;

#[derive(Parser)]
struct Cli {
    /// Input file (must exist)
    #[arg(value_parser = validate_file_exists)]
    input_file: PathBuf,
}

fn validate_file_exists(s: &str) -> Result<PathBuf, String> {
    let path = PathBuf::from(s);
    if path.exists() {
        Ok(path)
    } else {
        Err(format!("File {} does not exist", s))
    }
}
```

## Multi-Value Arguments

### Variadic Positional Arguments

**Use Case:** Accept multiple files or values

**Example:**
```bash
process file1.txt file2.txt file3.txt
```

**Python (Typer):**
```python
def process(
    files: Annotated[list[str], typer.Argument()]
):
    for file in files:
        # Process each file
        pass
```

**Go (Cobra):**
```go
var processCmd = &cobra.Command{
    Use:   "process <files...>",
    Args:  cobra.MinimumNArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        for _, file := range args {
            // Process each file
        }
    },
}
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Files to process
    #[arg(required = true)]
    files: Vec<String>,
}
```

### Multi-Value Options

**Use Case:** Accept multiple values for an option

**Example:**
```bash
deploy --tag v1.0.0 --tag latest --tag stable
```

**Python (Typer):**
```python
def deploy(
    tags: Annotated[list[str], typer.Option("--tag")] = []
):
    pass
```

**Go (Cobra):**
```go
var tags []string

deployCmd.Flags().StringSliceVar(&tags, "tag", []string{}, "Tags to apply")
```

**Rust (clap):**
```rust
#[derive(Parser)]
struct Cli {
    /// Tags to apply
    #[arg(long)]
    tags: Vec<String>,
}
```

## Language-Specific Patterns

### Python: Type Hint Patterns

**Optional Values:**
```python
from typing import Optional

def command(
    value: Annotated[Optional[str], typer.Option()] = None
):
    if value is not None:
        # Use value
        pass
```

**Union Types (Multiple Allowed Types):**
```python
from typing import Union

def command(
    value: Annotated[Union[str, int], typer.Option()]
):
    # value can be string or int
    pass
```

**Literal Types (Specific Values):**
```python
from typing import Literal

def deploy(
    env: Annotated[Literal["dev", "staging", "prod"], typer.Option()]
):
    pass
```

### Go: Persistent vs. Local Flags

**Persistent Flags (Available to All Subcommands):**
```go
var verbose bool

rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "Verbose")

// Available in all subcommands
```

**Local Flags (Specific to Command):**
```go
var dryRun bool

deployCmd.Flags().BoolVar(&dryRun, "dry-run", false, "Dry run")

// Only available for 'deploy' command
```

### Rust: Derive vs. Builder API

**Derive API (Declarative):**
```rust
#[derive(Parser)]
struct Cli {
    #[arg(short, long)]
    verbose: bool,
}
```

**Builder API (Programmatic):**
```rust
use clap::{Arg, Command};

let matches = Command::new("myapp")
    .arg(Arg::new("verbose")
        .short('v')
        .long("verbose")
        .action(clap::ArgAction::SetTrue))
    .get_matches();

let verbose = matches.get_flag("verbose");
```

## Best Practices Summary

**Argument Design:**
- Limit positional arguments to 2-3
- Use options for most parameters
- Provide both short and long forms for common flags
- Use descriptive long-form names

**Validation:**
- Validate early (before processing)
- Provide helpful error messages with suggestions
- Use type system for automatic validation when possible

**Defaults:**
- Provide sensible defaults
- Document all defaults in help text
- Allow environment variables to override defaults

**Help Text:**
- Write clear, concise help for each parameter
- Include examples in command help
- Document valid ranges and choices
