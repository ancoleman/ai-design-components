# Building CLIs Skill - Master Plan

**Skill Name:** `building-clis`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [CLI Framework Taxonomy](#cli-framework-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Multi-Language Implementations](#multi-language-implementations)
7. [Cross-Cutting Patterns](#cross-cutting-patterns)
8. [Library Recommendations](#library-recommendations)
9. [Skill Structure Design](#skill-structure-design)
10. [Integration Points](#integration-points)
11. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Command-line interfaces (CLIs) remain the foundation of developer tools, automation, and infrastructure management in 2025. Despite the rise of web UIs and AI assistants, CLIs offer unmatched composability, automation potential, and scriptability.

**Market Drivers:**
- **DevOps/Infrastructure Automation:** CLIs are essential for CI/CD, deployment, and infrastructure management
- **Developer Tooling:** Every major framework (Next.js, Vite, Cargo, Go) ships powerful CLI tools
- **AI-Powered CLIs:** 2025 sees integration of AI assistants directly into terminal workflows (ShellGPT, Continue)
- **Cross-Platform Development:** Modern CLIs must work seamlessly on Windows, macOS, and Linux
- **Container/Kubernetes Era:** CLIs for Docker, kubectl, and cloud platforms are daily-use tools

**Strategic Value:**
1. **Universal Skill:** Every developer interacts with CLIs daily (git, npm, docker, etc.)
2. **Automation Foundation:** CLIs enable scripting, CI/CD integration, and infrastructure-as-code
3. **Framework-Agnostic:** CLI skills apply across Python, Go, Rust, and TypeScript ecosystems
4. **Career-Relevant:** Building robust CLIs is a valued skill for tooling engineers and DevOps

### How This Differs from Existing Solutions

**Existing CLI Documentation:**
- **Framework-Specific:** Most docs focus on single frameworks (argparse docs, Cobra docs, clap docs)
- **Language-Siloed:** Python OR Go OR Rust, not unified patterns
- **Feature-Focused:** "How to add a flag" vs. "When to use arguments vs. options"

**Our Approach:**
- **Multi-Language Unified:** Consistent patterns across Python, Go, and Rust
- **Decision-Driven:** When to use which framework, how to structure commands
- **Best Practices:** Configuration management, output formatting, error handling
- **Modern Patterns:** Shell completion, interactive prompts, progress bars, colored output
- **Distribution-Focused:** How to package and distribute CLIs (PyPI, Homebrew, binary releases)

### Target Audience

**Primary Users:**
- Backend developers building tooling and automation
- DevOps engineers creating deployment and management CLIs
- Open-source maintainers building developer tools
- Full-stack developers adding CLI capabilities to projects

**Skill Level Assumptions:**
- Proficient in at least one of: Python, Go, or Rust
- Understands basic CLI concepts (arguments, flags, options)
- Has used CLIs extensively but wants to build professional-grade tools

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Framework Selection**
   - When to use Click vs. Typer (Python)
   - When to use Cobra vs. urfave/cli (Go)
   - When to use clap derive vs. builder API (Rust)

2. **Argument Parsing Patterns**
   - Positional arguments vs. flags vs. options
   - Required vs. optional parameters
   - Multi-value arguments and variadic parameters
   - Subcommand organization and nesting

3. **Interactive CLI Features**
   - Prompts and confirmations
   - Progress bars and spinners
   - Interactive selections and menus
   - Color and styling for output

4. **Configuration Management**
   - Config files (YAML, TOML, JSON)
   - Environment variables
   - Configuration precedence (CLI args > env vars > config file > defaults)
   - XDG Base Directory specification

5. **Output Formatting**
   - Human-readable text output
   - Structured output (JSON, YAML)
   - Tables and aligned columns
   - Error messages and exit codes

6. **Shell Integration**
   - Shell completion (bash, zsh, fish, PowerShell)
   - Environment variable integration
   - Pipe-friendly output
   - Signal handling (SIGINT, SIGTERM)

7. **Distribution and Installation**
   - PyPI packaging (Python)
   - Homebrew formulas (macOS/Linux)
   - Binary releases with GitHub Actions
   - Cargo install (Rust)

### What This Skill Does NOT Cover

**Out of Scope:**
- **TUI Applications:** Full terminal UIs (use Textual for Python, Bubble Tea for Go, Ratatui for Rust)
- **Shell Scripting:** Bash/Zsh scripting (separate skill: `shell-scripting`)
- **API Client Implementation:** How to build SDKs (separate skill: `sdk-design`)
- **GUI Applications:** Desktop applications with graphical interfaces
- **Web Servers/APIs:** Building HTTP services (covered by `api-patterns`)

### Success Criteria

**A user successfully uses this skill when they can:**
1. Select the appropriate CLI framework for their language and use case
2. Design command hierarchies with subcommands and flags
3. Implement robust argument parsing and validation
4. Add interactive features (prompts, progress bars)
5. Manage configuration from multiple sources
6. Format output for both humans and machines
7. Generate shell completions for major shells
8. Package and distribute CLIs across platforms

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- Google Search Grounding (Vertex AI) - 2 successful queries
- Context7 for library documentation (Typer, Cobra, clap)
- Official framework documentation

### Key Trends for 2025

**1. Modern CLI Frameworks Dominate**
- **Python:** Typer has overtaken Click for new projects (type hints, modern ergonomics)
- **Go:** Cobra remains industry standard (Kubernetes, Docker, GitHub CLI)
- **Rust:** clap v4 with derive API is production-ready and highly ergonomic

**2. AI Integration in Terminal Workflows**
- **ShellGPT:** ChatGPT embedded in terminal for script writing and debugging
- **Continue:** VS Code plugin with AI suggestions for commands
- **Devika:** Autonomous software agent using shell, browser, and editor

**3. Modern Terminal Tooling**
- **Replacements for Classic Commands:**
  - `ls` → `lsd`/`exa` (colorful, tree views, icons)
  - `grep` → `ripgrep` (`rg`) (faster, better regex)
  - `cd` → `zoxide` (intelligent jumping, fuzzy matching)
  - `top` → `btm`/`htop` (interactive monitoring)
  - `curl` → `httpie` (user-friendly, color-coded)
  - `cat` → `bat` (syntax highlighting, Git integration)

**4. Configuration Best Practices**
- **Separate files per environment** (dev, test, prod)
- **Secret management:** Encrypted or behind secret managers
- **Configuration validation:** `--check-config` flag in CI/CD
- **Consistent format:** Stick to one format (YAML/TOML/JSON) per project
- **Schema validation:** Linting in pull request workflows

**5. Argument Parsing Standards**
- **GNU Coding Conventions:** Follow POSIX utilities guidelines
- **`--help` and `--version`:** Always handle these flags
- **Argument separator:** Use `--` to separate options from positional args
- **Short and long forms:** Support both `-v` and `--verbose`
- **Input validation:** Sanitize and validate all inputs

### CLI Framework Evolution (2025)

**Python:**
- **Typer** is the modern choice (built by FastAPI creator)
  - Type hints for automatic documentation
  - Fast development with minimal boilerplate
  - Automatic shell completion
  - Click-based under the hood (stability)

- **Click** still widely used (mature, battle-tested)
  - Decorator-based API
  - Flexible and composable
  - Large ecosystem of plugins

**Go:**
- **Cobra** is the industry standard
  - Used by Kubernetes, Docker, GitHub CLI, Hugo
  - Subcommand-based architecture
  - Integrates with Viper for configuration
  - POSIX-compliant flags

- **urfave/cli** as lighter alternative
  - Simpler API for smaller tools
  - Less opinionated than Cobra

**Rust:**
- **clap v4** is production-ready
  - Derive API (declarative, type-safe)
  - Builder API (programmatic, flexible)
  - Fast compilation times (improved in v4)
  - Comprehensive validation and error messages

### Framework Comparison Summary

| Framework | Language | Maturity | Best For | Ecosystem |
|-----------|----------|----------|----------|-----------|
| **Typer** | Python | Modern (2019+) | New projects, type-safe CLIs | Growing |
| **Click** | Python | Mature (2014+) | Existing projects, complex CLIs | Large |
| **Cobra** | Go | Mature (2013+) | Enterprise tools, subcommands | Very Large |
| **urfave/cli** | Go | Mature (2013+) | Simple tools, quick CLIs | Medium |
| **clap** | Rust | Mature (2015+, v4 2022) | Performance-critical, robust CLIs | Large |

---

## CLI Framework Taxonomy

### Taxonomy by Complexity Level

#### Tier 1: Simple Single-Command CLIs

**Characteristics:**
- No subcommands, flat command structure
- Few arguments and options (<10)
- Straightforward input/output
- Minimal configuration

**Use Cases:**
- Utility scripts (file conversion, data processing)
- Simple automation tools
- One-off developer tools

**Best Frameworks:**
- **Python:** Typer (simplest), Click
- **Go:** urfave/cli, Cobra (overkill but fine)
- **Rust:** clap derive

**Example:** `convert-image input.jpg output.png --quality 90`

---

#### Tier 2: Multi-Command CLIs with Subcommands

**Characteristics:**
- Organized into subcommands (like `git`, `docker`)
- Moderate complexity (10-50 total commands/flags)
- Configuration file support
- Structured output options

**Use Cases:**
- Developer tooling (build tools, test runners)
- DevOps tools (deployment, monitoring)
- API clients with multiple operations

**Best Frameworks:**
- **Python:** Typer (with app.add_typer), Click
- **Go:** Cobra (designed for this)
- **Rust:** clap with subcommands

**Example:** `myapp deploy --env prod`, `myapp logs --follow`

---

#### Tier 3: Complex Multi-Level CLIs

**Characteristics:**
- Nested subcommands (3+ levels deep)
- Extensive configuration management
- Plugins and extensions
- Interactive modes

**Use Cases:**
- Infrastructure management (kubectl, terraform)
- Cloud provider CLIs (aws, gcloud, az)
- Package managers (cargo, npm)

**Best Frameworks:**
- **Python:** Click (most flexible)
- **Go:** Cobra (industry standard for this)
- **Rust:** clap (performant, robust)

**Example:** `kubectl get pods --namespace production --selector app=web`

---

### Taxonomy by Interaction Pattern

#### A. Batch/Non-Interactive CLIs

**Characteristics:**
- All input via arguments/flags
- No user interaction during execution
- Suitable for scripting and automation

**Design Pattern:**
```
command [OPTIONS] [ARGUMENTS]
```

**Best Practices:**
- Accept input from stdin for pipe-friendly workflows
- Use exit codes for success/failure (0 = success, non-zero = error)
- Output to stdout (data) and stderr (errors/logs)

---

#### B. Interactive CLIs

**Characteristics:**
- Prompts for user input
- Confirmations for destructive actions
- Progress indicators for long operations

**Design Pattern:**
```
command [initial-args]
  → prompt for additional info
  → show progress
  → confirm actions
```

**Best Practices:**
- Support `--yes` or `--force` flags to skip prompts (for automation)
- Use colored output to highlight important info
- Show progress bars for operations >2 seconds

---

#### C. Hybrid CLIs

**Characteristics:**
- Can run non-interactively (all args provided)
- Falls back to interactive mode for missing inputs
- Best of both worlds

**Design Pattern:**
```
command --name value    # Non-interactive
command                 # Interactive (prompts for name)
```

**Best Practices:**
- Detect if stdin is a TTY (interactive) or pipe (non-interactive)
- Use sensible defaults to minimize prompts
- Document both usage modes

---

## Decision Frameworks

### Framework 1: Which Language and Framework Should I Use?

**Decision Tree:**

```
START: I need to build a CLI

Q1: What language is my project already using?
  ├─ Python → Q2
  ├─ Go → Q3
  ├─ Rust → Q4
  └─ Other/New Project → Q5

Q2 (Python): Do I need type safety and modern ergonomics?
  ├─ YES → Use Typer (type hints, auto-completion)
  └─ NO → Use Click (mature, flexible)

Q3 (Go): Do I have complex subcommands (like git/docker)?
  ├─ YES → Use Cobra (industry standard)
  └─ NO → Use urfave/cli (simpler)

Q4 (Rust): Do I need declarative API (derive) or programmatic (builder)?
  ├─ Derive (type-safe, compile-time validation) → clap derive
  └─ Builder (runtime flexibility) → clap builder

Q5 (New Project): What's most important?
  ├─ Fast development, Python-friendly → Typer (Python)
  ├─ Performance, low memory → clap (Rust)
  ├─ Enterprise tooling, Go ecosystem → Cobra (Go)
  └─ Simple, quick script → Typer (Python)
```

---

### Framework 2: Arguments vs. Options vs. Flags?

**Definitions:**

- **Positional Argument:** Required or optional, identified by position
  - Example: `git commit -m "message"` → "message" is an argument to `-m`

- **Option:** Named parameter with a value
  - Example: `--output file.txt`, `-o file.txt`

- **Flag:** Boolean option (presence = true)
  - Example: `--verbose`, `--dry-run`, `-v`

**Decision Matrix:**

| Use Case | Type | Example | Rationale |
|----------|------|---------|-----------|
| Primary input (required) | Positional Argument | `convert input.jpg` | Clear, minimal typing |
| Primary input (optional) | Option with default | `--input file.txt` | Explicit, self-documenting |
| Output destination | Option | `--output result.json` | Flexible, can default to stdout |
| Boolean setting | Flag | `--verbose`, `--force` | Clear intent, no value needed |
| Multiple values | Variadic argument | `files...` | Natural for multiple items |
| Configuration | Option | `--config app.yaml` | Explicit, discoverable |

**Best Practices:**

1. **Limit positional arguments:** Max 2-3 (more gets confusing)
2. **Use long-form options:** `--output` not `-o` (except for very common flags)
3. **Boolean options default to false:** `--verbose` (not present = false)
4. **Provide short forms for common options:** `-v` for `--verbose`, `-h` for `--help`

---

### Framework 3: How Should I Structure Subcommands?

**Patterns:**

#### A. Flat Subcommands (1 Level)
```
app command1 [args]
app command2 [args]
app command3 [args]
```

**When to Use:** Small CLIs with 5-10 distinct operations

**Example:** `myapp deploy`, `myapp logs`, `myapp status`

---

#### B. Grouped Subcommands (2 Levels)
```
app group1 subcommand [args]
app group2 subcommand [args]
```

**When to Use:** Medium CLIs with logical groupings (10-30 commands)

**Example:**
- `kubectl get pods`
- `kubectl create deployment`
- `kubectl delete service`

---

#### C. Nested Subcommands (3+ Levels)
```
app group subgroup command [args]
```

**When to Use:** Large CLIs with deep hierarchies (30+ commands)

**Example:**
- `gcloud compute instances create`
- `gcloud container clusters list`

**⚠️ Warning:** Avoid excessive nesting (>3 levels becomes unwieldy)

---

### Framework 4: Configuration Precedence Strategy

**Standard Precedence (Highest to Lowest):**

1. **CLI Arguments/Flags:** Explicitly provided by user
2. **Environment Variables:** Session-specific overrides
3. **Config File (Local):** Project-specific settings (`./config.yaml`)
4. **Config File (User):** User-specific settings (`~/.config/app/config.yaml`)
5. **Config File (System):** System-wide defaults (`/etc/app/config.yaml`)
6. **Built-in Defaults:** Hardcoded in application

**Implementation Pattern:**

```python
# Python (Typer) example
def get_config_value(cli_arg, env_var, config_key, default):
    return cli_arg or os.getenv(env_var) or config.get(config_key) or default
```

**Best Practices:**

- **Document precedence:** Show in `--help` which sources are checked
- **Validate early:** Check config file validity before CLI execution
- **Provide `--print-config`:** Show effective configuration (after merging)
- **Use XDG Base Directory:** `~/.config/app/` for Linux/macOS config files

---

### Framework 5: Output Formatting Strategy

**Decision Matrix:**

| Use Case | Format | When to Use |
|----------|--------|-------------|
| **Human consumption** | Colored text, tables | Default mode, interactive use |
| **Machine consumption** | JSON, YAML | `--output json`, piping to other tools |
| **Logging/debugging** | Plain text | `--verbose`, error messages to stderr |
| **Progress tracking** | Progress bars, spinners | Long-running operations |

**Implementation Pattern:**

```bash
# Human-readable (default)
$ myapp list
NAME        STATUS    AGE
web-server  running   2d
database    stopped   5d

# Machine-readable (JSON)
$ myapp list --output json
[{"name":"web-server","status":"running","age":"2d"}]

# Verbose (for debugging)
$ myapp list --verbose
[DEBUG] Loading configuration from ~/.config/myapp/config.yaml
[DEBUG] Connecting to API at https://api.example.com
[INFO] Found 2 items
NAME        STATUS    AGE
web-server  running   2d
database    stopped   5d
```

**Best Practices:**

1. **Default to human-readable:** Assume interactive use
2. **Provide `--output` flag:** `json`, `yaml`, `table`, `plain`
3. **Use stderr for logs:** Keep stdout clean for data
4. **Color detection:** Disable colors if output is not a TTY
5. **Exit codes:** 0 = success, 1 = error, 2 = usage error

---

## Multi-Language Implementations

### Python Implementation (Typer - Primary)

**Why Typer?**
- **Modern:** Type hints for automatic validation and documentation
- **Fast Development:** Minimal boilerplate, decorator-based
- **Built on Click:** Inherits stability and ecosystem
- **Auto-completion:** Shell completion out-of-the-box
- **Created by FastAPI author:** Same quality standards

**Installation:**
```bash
pip install typer[all]  # Includes rich for colored output
```

**Basic Example (Single Command):**
```python
import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def greet(
    name: Annotated[str, typer.Argument(help="Name to greet")],
    formal: Annotated[bool, typer.Option("--formal", help="Use formal greeting")] = False
):
    """Greet someone with a friendly message."""
    if formal:
        typer.echo(f"Good day, {name}.")
    else:
        typer.echo(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

**Run:**
```bash
$ python greet.py Alice
Hello, Alice!

$ python greet.py Bob --formal
Good day, Bob.

$ python greet.py --help
Usage: greet.py [OPTIONS] NAME

  Greet someone with a friendly message.

Arguments:
  NAME  Name to greet  [required]

Options:
  --formal / --no-formal  Use formal greeting  [default: no-formal]
  --help                  Show this message and exit.
```

---

**Subcommands Example:**
```python
import typer

app = typer.Typer()

@app.command()
def deploy(
    env: str = typer.Option(..., "--env", help="Environment (dev/staging/prod)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate deployment")
):
    """Deploy the application."""
    if dry_run:
        typer.echo(f"[DRY RUN] Would deploy to {env}")
    else:
        typer.echo(f"Deploying to {env}...")

@app.command()
def logs(
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs"),
    lines: int = typer.Option(10, "--lines", "-n", help="Number of lines")
):
    """View application logs."""
    typer.echo(f"Showing last {lines} lines...")
    if follow:
        typer.echo("Following logs... (Ctrl+C to stop)")

if __name__ == "__main__":
    app()
```

**Run:**
```bash
$ python app.py deploy --env prod
Deploying to prod...

$ python app.py logs --follow --lines 20
Showing last 20 lines...
Following logs... (Ctrl+C to stop)

$ python app.py --help
Usage: app.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  deploy  Deploy the application.
  logs    View application logs.
```

---

**Interactive Prompts:**
```python
import typer

app = typer.Typer()

@app.command()
def delete(
    resource_name: str = typer.Argument(..., help="Resource to delete"),
    force: bool = typer.Option(False, "--force", help="Skip confirmation")
):
    """Delete a resource."""
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete '{resource_name}'?")
        if not confirm:
            typer.echo("Deletion cancelled.")
            raise typer.Abort()

    typer.echo(f"Deleting {resource_name}...")
    # Perform deletion

if __name__ == "__main__":
    app()
```

**Run:**
```bash
$ python delete.py my-database
Are you sure you want to delete 'my-database'? [y/N]: y
Deleting my-database...

$ python delete.py my-database --force
Deleting my-database...
```

---

**Progress Bars (with rich):**
```python
import typer
import time
from rich.progress import track

app = typer.Typer()

@app.command()
def process(count: int = typer.Option(10, help="Number of items to process")):
    """Process items with progress bar."""
    for _ in track(range(count), description="Processing..."):
        time.sleep(0.5)  # Simulate work
    typer.echo("✓ All items processed!")

if __name__ == "__main__":
    app()
```

---

### Go Implementation (Cobra - Primary)

**Why Cobra?**
- **Industry Standard:** Used by Kubernetes, Docker, GitHub CLI, Hugo
- **Subcommand-Focused:** Designed for complex multi-command CLIs
- **POSIX Compliant:** Follows GNU conventions for flags
- **Viper Integration:** Seamless configuration management
- **Active Development:** Well-maintained by spf13

**Installation:**
```bash
go get -u github.com/spf13/cobra@latest
```

**Basic Example (Single Command):**
```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
    "os"
)

func main() {
    var name string
    var formal bool

    var rootCmd = &cobra.Command{
        Use:   "greet [name]",
        Short: "Greet someone with a friendly message",
        Args:  cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            name = args[0]
            if formal {
                fmt.Printf("Good day, %s.\n", name)
            } else {
                fmt.Printf("Hello, %s!\n", name)
            }
        },
    }

    rootCmd.Flags().BoolVar(&formal, "formal", false, "Use formal greeting")

    if err := rootCmd.Execute(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
```

**Run:**
```bash
$ go run greet.go Alice
Hello, Alice!

$ go run greet.go Bob --formal
Good day, Bob.
```

---

**Subcommands Example:**
```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
    "os"
)

func main() {
    var rootCmd = &cobra.Command{
        Use:   "app",
        Short: "A CLI application",
    }

    // Deploy subcommand
    var deployEnv string
    var dryRun bool

    var deployCmd = &cobra.Command{
        Use:   "deploy",
        Short: "Deploy the application",
        Run: func(cmd *cobra.Command, args []string) {
            if dryRun {
                fmt.Printf("[DRY RUN] Would deploy to %s\n", deployEnv)
            } else {
                fmt.Printf("Deploying to %s...\n", deployEnv)
            }
        },
    }
    deployCmd.Flags().StringVar(&deployEnv, "env", "", "Environment (dev/staging/prod)")
    deployCmd.MarkFlagRequired("env")
    deployCmd.Flags().BoolVar(&dryRun, "dry-run", false, "Simulate deployment")

    // Logs subcommand
    var follow bool
    var lines int

    var logsCmd = &cobra.Command{
        Use:   "logs",
        Short: "View application logs",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Printf("Showing last %d lines...\n", lines)
            if follow {
                fmt.Println("Following logs... (Ctrl+C to stop)")
            }
        },
    }
    logsCmd.Flags().BoolVarP(&follow, "follow", "f", false, "Follow logs")
    logsCmd.Flags().IntVarP(&lines, "lines", "n", 10, "Number of lines")

    rootCmd.AddCommand(deployCmd, logsCmd)

    if err := rootCmd.Execute(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
```

**Run:**
```bash
$ go run app.go deploy --env prod
Deploying to prod...

$ go run app.go logs --follow --lines 20
Showing last 20 lines...
Following logs... (Ctrl+C to stop)
```

---

**Persistent Flags (Global Flags):**
```go
var verbose bool

var rootCmd = &cobra.Command{
    Use:   "app",
    Short: "A CLI application",
}

// Persistent flags are available to all subcommands
rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "Verbose output")
```

---

### Rust Implementation (clap - Primary)

**Why clap?**
- **Performance:** Compiled to native binary, minimal overhead
- **Type Safety:** Compile-time validation via derive API
- **Modern Ergonomics:** clap v4 improved compile times and usability
- **Comprehensive Validation:** Rich error messages with suggestions
- **Two APIs:** Derive (declarative) and Builder (programmatic)

**Installation:**
```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
```

**Basic Example (Derive API):**
```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "greet")]
#[command(about = "Greet someone with a friendly message", long_about = None)]
struct Cli {
    /// Name to greet
    name: String,

    /// Use formal greeting
    #[arg(long)]
    formal: bool,
}

fn main() {
    let cli = Cli::parse();

    if cli.formal {
        println!("Good day, {}.", cli.name);
    } else {
        println!("Hello, {}!", cli.name);
    }
}
```

**Run:**
```bash
$ cargo run -- Alice
Hello, Alice!

$ cargo run -- Bob --formal
Good day, Bob.

$ cargo run -- --help
Greet someone with a friendly message

Usage: greet [OPTIONS] <NAME>

Arguments:
  <NAME>  Name to greet

Options:
      --formal  Use formal greeting
  -h, --help    Print help
```

---

**Subcommands Example (Derive API):**
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "app")]
#[command(about = "A CLI application", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Deploy the application
    Deploy {
        /// Environment (dev/staging/prod)
        #[arg(long)]
        env: String,

        /// Simulate deployment
        #[arg(long)]
        dry_run: bool,
    },
    /// View application logs
    Logs {
        /// Follow logs
        #[arg(short, long)]
        follow: bool,

        /// Number of lines
        #[arg(short = 'n', long, default_value_t = 10)]
        lines: u32,
    },
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Deploy { env, dry_run } => {
            if *dry_run {
                println!("[DRY RUN] Would deploy to {}", env);
            } else {
                println!("Deploying to {}...", env);
            }
        }
        Commands::Logs { follow, lines } => {
            println!("Showing last {} lines...", lines);
            if *follow {
                println!("Following logs... (Ctrl+C to stop)");
            }
        }
    }
}
```

**Run:**
```bash
$ cargo run -- deploy --env prod
Deploying to prod...

$ cargo run -- logs --follow --lines 20
Showing last 20 lines...
Following logs... (Ctrl+C to stop)
```

---

**Builder API (Programmatic):**
```rust
use clap::{Arg, Command};

fn main() {
    let matches = Command::new("greet")
        .about("Greet someone")
        .arg(Arg::new("name")
            .help("Name to greet")
            .required(true)
            .index(1))
        .arg(Arg::new("formal")
            .long("formal")
            .help("Use formal greeting")
            .action(clap::ArgAction::SetTrue))
        .get_matches();

    let name = matches.get_one::<String>("name").unwrap();
    let formal = matches.get_flag("formal");

    if formal {
        println!("Good day, {}.", name);
    } else {
        println!("Hello, {}!", name);
    }
}
```

**When to Use Builder API:**
- Runtime command generation
- Dynamic subcommands
- Plugin systems
- Complex conditional logic

---

## Cross-Cutting Patterns

### Pattern 1: Configuration Management

**Multi-Source Configuration Pattern:**

**Python (Typer + YAML):**
```python
import typer
import yaml
from pathlib import Path
from typing import Optional

def load_config():
    """Load config from multiple sources with precedence."""
    config = {}

    # 1. System-wide config
    system_config = Path("/etc/myapp/config.yaml")
    if system_config.exists():
        config.update(yaml.safe_load(system_config.read_text()))

    # 2. User config
    user_config = Path.home() / ".config" / "myapp" / "config.yaml"
    if user_config.exists():
        config.update(yaml.safe_load(user_config.read_text()))

    # 3. Project config
    project_config = Path("./myapp.yaml")
    if project_config.exists():
        config.update(yaml.safe_load(project_config.read_text()))

    return config

app = typer.Typer()

@app.command()
def run(
    host: Optional[str] = typer.Option(None, "--host", help="Server host"),
    port: Optional[int] = typer.Option(None, "--port", help="Server port"),
):
    """Run the server with merged configuration."""
    config = load_config()

    # CLI args override config file
    final_host = host or os.getenv("MYAPP_HOST") or config.get("host") or "localhost"
    final_port = port or os.getenv("MYAPP_PORT") or config.get("port") or 8000

    typer.echo(f"Starting server at {final_host}:{final_port}")
```

---

**Go (Cobra + Viper):**
```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

func initConfig() {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")

    // Search paths
    viper.AddConfigPath("/etc/myapp/")
    viper.AddConfigPath("$HOME/.config/myapp")
    viper.AddConfigPath(".")

    // Environment variables
    viper.SetEnvPrefix("MYAPP")
    viper.AutomaticEnv()

    // Read config
    if err := viper.ReadInConfig(); err == nil {
        fmt.Println("Using config file:", viper.ConfigFileUsed())
    }
}

func main() {
    cobra.OnInitialize(initConfig)

    var host string
    var port int

    var rootCmd = &cobra.Command{
        Use:   "myapp",
        Short: "My application",
        Run: func(cmd *cobra.Command, args []string) {
            // Viper binds flags to config
            host = viper.GetString("host")
            port = viper.GetInt("port")

            fmt.Printf("Starting server at %s:%d\n", host, port)
        },
    }

    rootCmd.Flags().StringVar(&host, "host", "localhost", "Server host")
    rootCmd.Flags().IntVar(&port, "port", 8000, "Server port")

    // Bind flags to viper
    viper.BindPFlag("host", rootCmd.Flags().Lookup("host"))
    viper.BindPFlag("port", rootCmd.Flags().Lookup("port"))

    rootCmd.Execute()
}
```

---

**Rust (clap + config crate):**
```rust
use clap::Parser;
use config::{Config, File, Environment};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct AppConfig {
    host: String,
    port: u16,
}

#[derive(Parser)]
struct Cli {
    /// Server host
    #[arg(long)]
    host: Option<String>,

    /// Server port
    #[arg(long)]
    port: Option<u16>,
}

fn load_config() -> AppConfig {
    Config::builder()
        // System config
        .add_source(File::with_name("/etc/myapp/config").required(false))
        // User config
        .add_source(File::with_name("~/.config/myapp/config").required(false))
        // Project config
        .add_source(File::with_name("./myapp").required(false))
        // Environment variables (MYAPP_HOST, MYAPP_PORT)
        .add_source(Environment::with_prefix("MYAPP"))
        // Defaults
        .set_default("host", "localhost").unwrap()
        .set_default("port", 8000).unwrap()
        .build()
        .unwrap()
        .try_deserialize()
        .unwrap()
}

fn main() {
    let cli = Cli::parse();
    let mut config = load_config();

    // CLI args override config
    if let Some(host) = cli.host {
        config.host = host;
    }
    if let Some(port) = cli.port {
        config.port = port;
    }

    println!("Starting server at {}:{}", config.host, config.port);
}
```

---

### Pattern 2: Output Formatting

**Structured Output (JSON/YAML) Pattern:**

**Python (Typer + rich):**
```python
import typer
import json
from rich.console import Console
from rich.table import Table
from enum import Enum

console = Console()

class OutputFormat(str, Enum):
    table = "table"
    json = "json"
    yaml = "yaml"

app = typer.Typer()

@app.command()
def list_items(
    output: OutputFormat = typer.Option(OutputFormat.table, "--output", "-o")
):
    """List items with different output formats."""
    items = [
        {"name": "web-server", "status": "running", "age": "2d"},
        {"name": "database", "status": "stopped", "age": "5d"},
    ]

    if output == OutputFormat.table:
        table = Table(title="Items")
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Age", style="green")

        for item in items:
            table.add_row(item["name"], item["status"], item["age"])

        console.print(table)

    elif output == OutputFormat.json:
        typer.echo(json.dumps(items, indent=2))

    elif output == OutputFormat.yaml:
        import yaml
        typer.echo(yaml.dump(items))
```

---

**Go (Cobra + encoding/json):**
```go
package main

import (
    "encoding/json"
    "fmt"
    "github.com/spf13/cobra"
    "github.com/olekukonko/tablewriter"
    "os"
)

type Item struct {
    Name   string `json:"name"`
    Status string `json:"status"`
    Age    string `json:"age"`
}

func main() {
    var outputFormat string

    var listCmd = &cobra.Command{
        Use:   "list",
        Short: "List items",
        Run: func(cmd *cobra.Command, args []string) {
            items := []Item{
                {"web-server", "running", "2d"},
                {"database", "stopped", "5d"},
            }

            switch outputFormat {
            case "table":
                table := tablewriter.NewWriter(os.Stdout)
                table.SetHeader([]string{"Name", "Status", "Age"})
                for _, item := range items {
                    table.Append([]string{item.Name, item.Status, item.Age})
                }
                table.Render()

            case "json":
                data, _ := json.MarshalIndent(items, "", "  ")
                fmt.Println(string(data))
            }
        },
    }

    listCmd.Flags().StringVarP(&outputFormat, "output", "o", "table", "Output format (table|json)")
    listCmd.Execute()
}
```

---

### Pattern 3: Shell Completion

**Python (Typer):**
```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    typer.echo(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

**Generate completion:**
```bash
# Bash
_MYAPP_COMPLETE=bash_source myapp > ~/.myapp-complete.bash
echo ". ~/.myapp-complete.bash" >> ~/.bashrc

# Zsh
_MYAPP_COMPLETE=zsh_source myapp > ~/.myapp-complete.zsh
echo ". ~/.myapp-complete.zsh" >> ~/.zshrc

# Fish
_MYAPP_COMPLETE=fish_source myapp > ~/.config/fish/completions/myapp.fish
```

---

**Go (Cobra):**
```go
package main

import (
    "github.com/spf13/cobra"
)

func main() {
    var rootCmd = &cobra.Command{Use: "app"}

    // Add completion command
    rootCmd.AddCommand(&cobra.Command{
        Use:   "completion [bash|zsh|fish|powershell]",
        Short: "Generate shell completion",
        Args:  cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            switch args[0] {
            case "bash":
                rootCmd.GenBashCompletion(os.Stdout)
            case "zsh":
                rootCmd.GenZshCompletion(os.Stdout)
            case "fish":
                rootCmd.GenFishCompletion(os.Stdout, true)
            case "powershell":
                rootCmd.GenPowerShellCompletionWithDesc(os.Stdout)
            }
        },
    })

    rootCmd.Execute()
}
```

**Install:**
```bash
# Bash
app completion bash > /etc/bash_completion.d/app

# Zsh
app completion zsh > "${fpath[1]}/_app"

# Fish
app completion fish > ~/.config/fish/completions/app.fish
```

---

**Rust (clap):**
```rust
use clap::{CommandFactory, Parser};
use clap_complete::{generate, shells::Bash};

#[derive(Parser)]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    /// Generate shell completion
    Completion {
        #[arg(value_enum)]
        shell: Shell,
    },
}

#[derive(ValueEnum, Clone)]
enum Shell {
    Bash,
    Zsh,
    Fish,
}

fn main() {
    let cli = Cli::parse();

    if let Some(Commands::Completion { shell }) = cli.command {
        let mut cmd = Cli::command();
        match shell {
            Shell::Bash => generate(Bash, &mut cmd, "app", &mut io::stdout()),
            // ... other shells
        }
    }
}
```

---

### Pattern 4: Progress Indicators

**Python (rich):**
```python
import typer
import time
from rich.progress import Progress

app = typer.Typer()

@app.command()
def process(count: int = 100):
    """Process items with progress bar."""
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing...", total=count)

        for i in range(count):
            time.sleep(0.01)  # Simulate work
            progress.update(task, advance=1)

    typer.echo("✓ Complete!")
```

---

**Go (progressbar):**
```go
package main

import (
    "time"
    "github.com/schollz/progressbar/v3"
)

func main() {
    count := 100
    bar := progressbar.Default(int64(count))

    for i := 0; i < count; i++ {
        bar.Add(1)
        time.Sleep(10 * time.Millisecond)
    }

    fmt.Println("\n✓ Complete!")
}
```

---

**Rust (indicatif):**
```rust
use indicatif::ProgressBar;
use std::time::Duration;
use std::thread;

fn main() {
    let count = 100;
    let bar = ProgressBar::new(count);

    for _ in 0..count {
        bar.inc(1);
        thread::sleep(Duration::from_millis(10));
    }

    bar.finish_with_message("✓ Complete!");
}
```

---

## Library Recommendations

### Research Summary

**Research Date:** December 3, 2025
**Libraries Evaluated:** 8 (Typer, Click, Cobra, urfave/cli, clap, argparse, docopt, fire)
**Research Tools:** Google Search Grounding (Vertex AI), Context7

---

### Python CLI Libraries (2025)

#### **Primary: Typer** (Modern, Type-Safe)

**Library:** `/fastapi/typer`
**Trust Score:** 86.7/100 (Context7)
**Code Snippets:** 558+
**Benchmark Score:** 86.7

**Why Typer?**
- **Modern Python:** Leverages type hints (Python 3.6+)
- **Auto-Documentation:** Help text generated from type hints and docstrings
- **Minimal Boilerplate:** Decorator-based API, clean syntax
- **Built on Click:** Inherits stability, can drop down to Click when needed
- **Rich Integration:** Works seamlessly with `rich` for beautiful output
- **Created by FastAPI Author:** Same quality standards and ergonomics

**When to Use:**
- New Python CLI projects (2025 recommendation)
- Type-safe applications with Python 3.7+
- Projects using FastAPI (consistent tooling)
- Need auto-completion and validation

**Installation:**
```bash
pip install "typer[all]"  # Includes rich, shellingham for auto-detection
```

**Example:**
```python
import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def hello(
    name: Annotated[str, typer.Argument(help="Name to greet")],
    formal: Annotated[bool, typer.Option(help="Use formal greeting")] = False
):
    """Greet someone."""
    greeting = "Good day" if formal else "Hello"
    typer.echo(f"{greeting}, {name}!")

if __name__ == "__main__":
    app()
```

**Strengths:**
- ✅ Type hints for validation and docs
- ✅ Minimal code for full-featured CLIs
- ✅ Excellent error messages
- ✅ Auto-completion support
- ✅ Rich/colorful output built-in

**Considerations:**
- Requires Python 3.6+ (type hints)
- Less mature ecosystem than Click (but growing fast)

---

#### **Alternative: Click** (Mature, Flexible)

**Library:** `click` (Pallets Project)
**Maturity:** Very High (2014+)
**Ecosystem:** Very Large (many plugins)

**Why Click?**
- **Battle-Tested:** Used by Flask, AWS CLI, and thousands of projects
- **Flexible:** Decorator-based, highly composable
- **Ecosystem:** Large plugin library (click-plugins)
- **No Type Hints Required:** Works with older Python versions

**When to Use:**
- Existing projects already using Click
- Need for specific Click plugins
- Python <3.6 support required (though uncommon in 2025)
- Complex, nested command structures

**Installation:**
```bash
pip install click
```

**Example:**
```python
import click

@click.command()
@click.argument('name')
@click.option('--formal', is_flag=True, help='Use formal greeting')
def hello(name, formal):
    """Greet someone."""
    greeting = "Good day" if formal else "Hello"
    click.echo(f"{greeting}, {name}!")

if __name__ == '__main__':
    hello()
```

**Strengths:**
- ✅ Very mature and stable
- ✅ Large ecosystem
- ✅ Flexible and composable
- ✅ Excellent documentation

**Considerations:**
- More verbose than Typer
- No type hint integration

---

### Go CLI Libraries (2025)

#### **Primary: Cobra** (Industry Standard)

**Library:** `/spf13/cobra`
**Trust Score:** 90.1/100 (Context7 - Benchmark)
**Code Snippets:** 1,126+ (pkg.go.dev documentation)
**Benchmark Score:** 90.1

**Why Cobra?**
- **Industry Standard:** Used by Kubernetes, Docker, GitHub CLI, Hugo, Terraform
- **Subcommand-Focused:** Designed for complex multi-command CLIs
- **POSIX Compliant:** Follows GNU conventions
- **Viper Integration:** Seamless configuration management
- **Shell Completion:** Automatic generation for all major shells
- **Generator Tool:** `cobra-cli` scaffolds projects

**When to Use:**
- Enterprise-grade CLI tools
- Complex subcommand hierarchies (like git, docker, kubectl)
- Go projects requiring configuration management (with Viper)
- Need for POSIX-compliant flags

**Installation:**
```bash
go get -u github.com/spf13/cobra@latest
```

**Example:**
```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
    "os"
)

func main() {
    var formal bool

    var rootCmd = &cobra.Command{
        Use:   "greet [name]",
        Short: "Greet someone",
        Args:  cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            greeting := "Hello"
            if formal {
                greeting = "Good day"
            }
            fmt.Printf("%s, %s!\n", greeting, args[0])
        },
    }

    rootCmd.Flags().BoolVar(&formal, "formal", false, "Use formal greeting")

    if err := rootCmd.Execute(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
```

**Strengths:**
- ✅ Best-in-class for Go CLIs
- ✅ Used by major projects (proven at scale)
- ✅ Excellent subcommand support
- ✅ Viper integration for config
- ✅ Automatic help and usage generation

**Considerations:**
- Can be overkill for simple CLIs
- More boilerplate than alternatives

---

#### **Alternative: urfave/cli** (Lightweight)

**Library:** `github.com/urfave/cli`
**Maturity:** High (2013+)
**Use Case:** Simple CLIs, quick tools

**Why urfave/cli?**
- **Simpler API:** Less boilerplate for basic CLIs
- **Lightweight:** Smaller dependency footprint
- **Good Documentation:** Clear examples

**When to Use:**
- Simple CLI tools (5-10 commands max)
- Quick scripts and utilities
- Prefer minimal boilerplate

**Example:**
```go
package main

import (
    "fmt"
    "github.com/urfave/cli/v2"
    "os"
)

func main() {
    app := &cli.App{
        Name:  "greet",
        Usage: "Greet someone",
        Flags: []cli.Flag{
            &cli.BoolFlag{
                Name:  "formal",
                Usage: "Use formal greeting",
            },
        },
        Action: func(c *cli.Context) error {
            greeting := "Hello"
            if c.Bool("formal") {
                greeting = "Good day"
            }
            fmt.Printf("%s, %s!\n", greeting, c.Args().First())
            return nil
        },
    }

    app.Run(os.Args)
}
```

---

### Rust CLI Libraries (2025)

#### **Primary: clap v4** (Modern, Type-Safe)

**Library:** `/clap-rs/clap`
**Trust Score:** High (GitHub stars: 13k+)
**Code Snippets:** 213+
**Version:** v4.5+ (2025)

**Why clap v4?**
- **Two APIs:** Derive (declarative) and Builder (programmatic)
- **Compile-Time Validation:** Derive API catches errors at compile time
- **Improved v4:** Faster compile times, better error messages
- **Comprehensive:** Subcommands, validation, shell completion, colored help
- **Active Development:** Regular updates, modern Rust idioms

**When to Use:**
- All Rust CLI projects (default choice in 2025)
- Need compile-time safety (derive API)
- Performance-critical CLIs
- Want excellent error messages

**Installation:**
```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
```

**Example (Derive API):**
```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "greet", about = "Greet someone")]
struct Cli {
    /// Name to greet
    name: String,

    /// Use formal greeting
    #[arg(long)]
    formal: bool,
}

fn main() {
    let cli = Cli::parse();

    let greeting = if cli.formal { "Good day" } else { "Hello" };
    println!("{}, {}!", greeting, cli.name);
}
```

**Example (Builder API):**
```rust
use clap::{Arg, Command};

fn main() {
    let matches = Command::new("greet")
        .about("Greet someone")
        .arg(Arg::new("name").required(true).index(1))
        .arg(Arg::new("formal").long("formal").action(clap::ArgAction::SetTrue))
        .get_matches();

    let name = matches.get_one::<String>("name").unwrap();
    let formal = matches.get_flag("formal");

    let greeting = if formal { "Good day" } else { "Hello" };
    println!("{}, {}!", greeting, name);
}
```

**Strengths:**
- ✅ Type-safe (derive API)
- ✅ Excellent error messages
- ✅ Fast and lightweight
- ✅ Two APIs (derive + builder)
- ✅ Comprehensive feature set

**Considerations:**
- Derive API requires feature flag
- Learning curve for advanced features

---

### Comparison Matrix

| Framework | Language | API Style | Complexity | Type Safety | Maturity | Best For |
|-----------|----------|-----------|------------|-------------|----------|----------|
| **Typer** | Python | Decorator | Low | ⭐⭐⭐⭐⭐ (type hints) | Growing | Modern Python CLIs |
| **Click** | Python | Decorator | Medium | ⭐⭐⭐ | Very High | Mature Python CLIs |
| **Cobra** | Go | Struct-based | Medium-High | ⭐⭐⭐⭐ | Very High | Enterprise Go CLIs |
| **urfave/cli** | Go | Struct-based | Low-Medium | ⭐⭐⭐ | High | Simple Go CLIs |
| **clap** | Rust | Derive/Builder | Medium | ⭐⭐⭐⭐⭐ (derive) | High | All Rust CLIs |

---

### Supporting Libraries

#### Output Formatting

**Python:**
- **rich:** Beautiful terminal output (tables, progress, colors)
  - `pip install rich`
- **colorama:** Cross-platform colored output
  - `pip install colorama`

**Go:**
- **tablewriter:** ASCII tables
  - `github.com/olekukonko/tablewriter`
- **color:** ANSI colors
  - `github.com/fatih/color`
- **progressbar:** Progress bars
  - `github.com/schollz/progressbar/v3`

**Rust:**
- **indicatif:** Progress bars and spinners
  - `indicatif = "0.17"`
- **colored:** Colored output
  - `colored = "2.0"`
- **comfy-table:** Beautiful tables
  - `comfy-table = "7.0"`

#### Configuration Management

**Python:**
- **pydantic:** Type-safe config validation
  - `pip install pydantic`
- **python-dotenv:** Load .env files
  - `pip install python-dotenv`

**Go:**
- **viper:** Complete configuration solution
  - `github.com/spf13/viper`

**Rust:**
- **config:** Configuration management
  - `config = "0.13"`
- **serde:** Serialization/deserialization
  - `serde = { version = "1.0", features = ["derive"] }`

---

## Skill Structure Design

### Skill File Organization

**Proposed Structure:**

```
building-clis/
├── SKILL.md                          # Main skill file (<500 lines)
├── references/
│   ├── framework-selection.md        # Decision tree: Which framework?
│   ├── argument-patterns.md          # Args vs options vs flags
│   ├── subcommand-design.md          # Structuring command hierarchies
│   ├── configuration-management.md   # Config files, env vars, precedence
│   ├── output-formatting.md          # Human vs machine-readable
│   ├── shell-completion.md           # Generating completions
│   └── distribution.md               # Packaging and releasing CLIs
├── examples/
│   ├── python/
│   │   ├── typer_basic.py            # Simple single-command CLI
│   │   ├── typer_subcommands.py      # Multi-command structure
│   │   ├── typer_config.py           # Configuration management
│   │   ├── typer_interactive.py      # Prompts and confirmations
│   │   └── typer_progress.py         # Progress bars and formatting
│   ├── go/
│   │   ├── cobra_basic.go            # Simple Cobra CLI
│   │   ├── cobra_subcommands.go      # Multi-level subcommands
│   │   ├── cobra_viper.go            # Configuration with Viper
│   │   └── cobra_completion.go       # Shell completion
│   └── rust/
│       ├── clap_derive.rs            # Derive API examples
│       ├── clap_builder.rs           # Builder API examples
│       ├── clap_subcommands.rs       # Subcommand patterns
│       └── clap_config.rs            # Config file integration
├── scripts/
│   └── package-cli.sh                # Cross-platform packaging script
└── assets/
    └── cli-decision-tree.svg         # Visual decision framework
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~450-500 lines):**

1. **Frontmatter** (YAML)
   - name: `building-clis`
   - description: Build professional command-line interfaces in Python, Go, and Rust with modern frameworks like Typer, Cobra, and clap

2. **Purpose** (~50 lines)
   - What this skill teaches
   - When to use this skill
   - Multi-language coverage

3. **Quick Start Guide** (~100 lines)
   - Python (Typer): Basic example
   - Go (Cobra): Basic example
   - Rust (clap): Basic example
   - Framework selection flowchart

4. **Core Patterns** (~150 lines)
   - Arguments vs. options vs. flags
   - Subcommand organization
   - Configuration management (config files + env vars)
   - Output formatting (human vs. machine)
   - Interactive features (prompts, progress)

5. **Language-Specific Notes** (~100 lines)
   - Python: Typer features, rich integration
   - Go: Cobra + Viper patterns
   - Rust: Derive vs. builder API

6. **Distribution** (~50 lines)
   - PyPI (Python)
   - Homebrew (Go/Rust)
   - Binary releases (GitHub Actions)

7. **Reference Links** (~20 lines)
   - Links to detailed references/
   - Links to examples/
   - External resources

---

### Progressive Disclosure Strategy

**Main SKILL.md Contains:**
- Quick-start examples (copy-paste ready)
- High-level decision frameworks
- When to use which pattern
- Links to detailed references

**References/ Contains:**
- Detailed framework selection guide (references/framework-selection.md)
- Comprehensive argument parsing patterns (references/argument-patterns.md)
- Configuration management deep dive (references/configuration-management.md)
- Output formatting strategies (references/output-formatting.md)
- Distribution best practices (references/distribution.md)

**Examples/ Contains:**
- Working code examples (copy-paste ready, tested)
- Organized by language (python/, go/, rust/)
- Real-world patterns (not toy examples)

**Scripts/ Contains:**
- Cross-platform packaging script (scripts/package-cli.sh)
- Version management automation (optional)

---

## Integration Points

### Integration with Existing Skills

#### 1. **building-ci-pipelines** Skill
- **CLI Testing:** Running CLI tests in CI/CD
- **Binary Builds:** Compiling and releasing CLI binaries
- **Cross-Platform Testing:** Testing CLIs on Windows, macOS, Linux

**Example Integration (.github/workflows/cli-release.yml):**
```yaml
name: Release CLI

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Build CLI (Go)
        run: |
          go build -o myapp-${{ matrix.os }}

      - name: Upload Binary
        uses: actions/upload-artifact@v3
        with:
          name: myapp-${{ matrix.os }}
          path: myapp-${{ matrix.os }}
```

---

#### 2. **testing-strategies** Skill
- **CLI Testing:** Testing argument parsing, command execution
- **Integration Tests:** End-to-end CLI testing
- **Mocking:** Mocking external dependencies in CLI tests

**Example Integration (Python/pytest):**
```python
import pytest
from typer.testing import CliRunner
from myapp import app

runner = CliRunner()

def test_hello_command():
    result = runner.invoke(app, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.stdout

def test_hello_command_formal():
    result = runner.invoke(app, ["hello", "Bob", "--formal"])
    assert result.exit_code == 0
    assert "Good day, Bob" in result.stdout
```

---

#### 3. **api-patterns** Skill
- **API Client CLIs:** Building CLIs that interact with REST/GraphQL APIs
- **Authentication:** Handling API tokens and credentials
- **Output Formatting:** Displaying API responses

**Example Integration:**
```python
import typer
import httpx

app = typer.Typer()

@app.command()
def get_user(user_id: int, api_key: str = typer.Option(..., envvar="API_KEY")):
    """Fetch user from API."""
    response = httpx.get(
        f"https://api.example.com/users/{user_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    typer.echo(response.json())
```

---

#### 4. **infrastructure-as-code** Skill
- **Deployment CLIs:** Building tools for infrastructure deployment
- **Configuration Management:** Managing infrastructure config files
- **Terraform/Ansible Integration:** CLI wrappers for IaC tools

**Example Integration:**
```bash
# CLI wrapping Terraform
myapp deploy --env prod --plan    # terraform plan
myapp deploy --env prod --apply   # terraform apply
myapp destroy --env prod          # terraform destroy
```

---

#### 5. **secret-management** Skill
- **Secure Credentials:** Storing API keys, passwords securely
- **Environment Variables:** Loading secrets from env vars
- **Vault Integration:** Fetching secrets from HashiCorp Vault

**Example Integration:**
```python
import typer
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

app = typer.Typer()

@app.command()
def deploy(api_key: str = typer.Option(None, envvar="API_KEY")):
    """Deploy with secure API key."""
    if not api_key:
        typer.echo("Error: API_KEY not set", err=True)
        raise typer.Exit(1)

    # Use api_key for deployment
    typer.echo("Deploying...")
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Deliverables:**
- [x] Complete init.md (this document)
- [ ] Create SKILL.md main file
- [ ] Write references/framework-selection.md
- [ ] Write references/argument-patterns.md

**Content Focus:**
- Framework selection decision tree
- Basic argument parsing patterns
- When to use which framework

---

### Phase 2: Python Implementation (Week 2)

**Deliverables:**
- [ ] Complete Typer examples (basic, subcommands, config, interactive)
- [ ] Write references/configuration-management.md
- [ ] Document Click alternative patterns

**Files:**
- examples/python/typer_basic.py
- examples/python/typer_subcommands.py
- examples/python/typer_config.py
- examples/python/typer_interactive.py
- examples/python/typer_progress.py

---

### Phase 3: Go Implementation (Week 3)

**Deliverables:**
- [ ] Complete Cobra examples (basic, subcommands, Viper integration)
- [ ] Write references/subcommand-design.md
- [ ] Document urfave/cli alternative

**Files:**
- examples/go/cobra_basic.go
- examples/go/cobra_subcommands.go
- examples/go/cobra_viper.go
- examples/go/cobra_completion.go

---

### Phase 4: Rust Implementation (Week 4)

**Deliverables:**
- [ ] Complete clap examples (derive API, builder API, subcommands)
- [ ] Write references/output-formatting.md
- [ ] Document when to use derive vs. builder

**Files:**
- examples/rust/clap_derive.rs
- examples/rust/clap_builder.rs
- examples/rust/clap_subcommands.rs
- examples/rust/clap_config.rs

---

### Phase 5: Advanced Topics (Week 5)

**Deliverables:**
- [ ] Write references/shell-completion.md
- [ ] Write references/distribution.md
- [ ] Create scripts/package-cli.sh
- [ ] Document interactive features (prompts, progress bars)

---

### Phase 6: Integration & Polish (Week 6)

**Deliverables:**
- [ ] Cross-link with related skills (CI/CD, testing, API patterns)
- [ ] Create CLI decision tree visual (assets/cli-decision-tree.svg)
- [ ] Test all examples across platforms
- [ ] Finalize SKILL.md and references

---

## Validation Checklist

### Before Creating SKILL.md

- [x] Research complete (Google Search + Context7)
- [x] Library recommendations validated (trust scores, snippets)
- [x] Decision frameworks designed
- [x] Multi-language patterns identified (Python, Go, Rust)
- [x] Integration points with other skills mapped

### Before Finalizing Skill

- [ ] SKILL.md under 500 lines
- [ ] All references/ files created
- [ ] All examples/ files working and tested across platforms
- [ ] Progressive disclosure effective (main → references → examples)
- [ ] Tested with real CLI projects
- [ ] Cross-language consistency validated
- [ ] Integration with related skills verified

---

## Success Metrics

**This skill is successful if developers can:**

1. **Make Strategic Decisions:**
   - Choose appropriate framework (Typer vs. Click, Cobra vs. urfave/cli, clap derive vs. builder)
   - Decide when to use arguments vs. options vs. flags
   - Design effective command hierarchies with subcommands

2. **Build Professional CLIs:**
   - Parse arguments and validate input
   - Implement interactive features (prompts, confirmations, progress bars)
   - Format output for humans and machines (tables, JSON, YAML)
   - Manage configuration from multiple sources (files, env vars, CLI args)

3. **Deliver Production-Ready Tools:**
   - Generate shell completions (bash, zsh, fish, PowerShell)
   - Package and distribute CLIs (PyPI, Homebrew, binary releases)
   - Handle errors gracefully with helpful messages
   - Follow CLI best practices (exit codes, signal handling, pipe-friendly)

4. **Integrate with Workflows:**
   - CLIs work in CI/CD pipelines
   - Support automation (non-interactive modes)
   - Provide machine-readable output for scripting

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **TUI Integration**
   - When to use TUI frameworks (Textual, Bubble Tea, Ratatui)
   - Transitioning from CLI to TUI

2. **Plugin Systems**
   - Building extensible CLIs with plugins
   - Plugin discovery and loading

3. **Advanced Shell Integration**
   - Custom shell completions with dynamic suggestions
   - Shell aliases and functions

4. **Performance Optimization**
   - Lazy loading of subcommands
   - Caching strategies for CLI tools

5. **Security**
   - Handling sensitive data in CLIs
   - Secure credential storage
   - Audit logging

---

## Appendix: CLI Best Practices Summary

### Universal Best Practices (All Languages)

1. **Follow GNU Conventions:**
   - Always provide `--help` and `--version`
   - Use `--` to separate options from positional arguments
   - Support both short (`-v`) and long (`--verbose`) forms

2. **Error Handling:**
   - Use exit codes: 0 = success, 1 = error, 2 = usage error
   - Write errors to stderr, data to stdout
   - Provide helpful error messages with suggestions

3. **Output:**
   - Default to human-readable output
   - Provide `--output` flag for JSON/YAML
   - Disable colors when output is not a TTY

4. **Configuration:**
   - Support config files (YAML/TOML/JSON)
   - Support environment variables
   - CLI args override env vars override config files

5. **Interactivity:**
   - Detect if stdin is a TTY (interactive vs. pipe)
   - Provide `--yes` or `--force` to skip prompts
   - Show progress bars for operations >2 seconds

6. **Shell Integration:**
   - Generate completions for major shells
   - Support pipe-friendly workflows (stdin/stdout)
   - Handle signals gracefully (SIGINT, SIGTERM)

---

## References

**Research Sources:**
- Google Search Grounding (Vertex AI): CLI frameworks 2025, best practices
- Context7 Documentation: Typer (/fastapi/typer), Cobra (/spf13/cobra), clap (/clap-rs/clap)
- Official Documentation: typer.tiangolo.com, cobra.dev, docs.rs/clap

**Related Skills:**
- `testing-strategies` - CLI testing patterns
- `building-ci-pipelines` - Binary builds and releases
- `api-patterns` - Building API client CLIs
- `infrastructure-as-code` - Deployment CLIs
- `secret-management` - Secure credential handling

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
