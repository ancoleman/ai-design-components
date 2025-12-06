---
sidebar_position: 2
title: Building CLIs
description: Build professional command-line interfaces in Python, Go, and Rust with modern frameworks
tags: [developer-productivity, cli, python, go, rust, typer, cobra, clap]
---

# Building CLIs

Build professional command-line interfaces across Python, Go, and Rust using modern frameworks like Typer, Cobra, and clap with robust argument parsing, interactive features, configuration management, and multi-platform distribution.

## When to Use

Use when:
- Building developer tooling or automation CLIs
- Creating infrastructure management tools (deployment, monitoring)
- Implementing API client command-line tools
- Adding CLI capabilities to existing projects
- Packaging utilities for distribution (PyPI, Homebrew, binary releases)

Common triggers: "create a CLI tool", "build a command-line interface", "add CLI arguments", "parse command-line options", "generate shell completions"

## Key Features

- **Multi-Language Support**: Python (Typer), Go (Cobra), Rust (clap)
- **Argument Parsing**: Positional arguments, options, flags, and subcommands
- **Configuration Management**: Config files, environment variables, precedence handling
- **Interactive Features**: Progress bars, prompts, confirmations, colored output
- **Shell Completion**: Auto-generate completions for bash, zsh, fish, PowerShell
- **Distribution**: PyPI, Homebrew, Cargo, binary releases

## Quick Start

### Python with Typer

```python
import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def greet(
    name: Annotated[str, typer.Argument(help="Name to greet")],
    formal: Annotated[bool, typer.Option(help="Use formal greeting")] = False
):
    """Greet someone with a message."""
    greeting = "Good day" if formal else "Hello"
    typer.echo(f"{greeting}, {name}!")

if __name__ == "__main__":
    app()
```

### Go with Cobra

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "greet [name]",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        formal, _ := cmd.Flags().GetBool("formal")
        greeting := "Hello"
        if formal {
            greeting = "Good day"
        }
        fmt.Printf("%s, %s!\n", greeting, args[0])
    },
}

func init() {
    rootCmd.Flags().Bool("formal", false, "Use formal greeting")
}

func main() {
    rootCmd.Execute()
}
```

### Rust with clap

```rust
use clap::Parser;

#[derive(Parser)]
#[command(about = "Greet someone")]
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

## Framework Selection

### Quick Decision Guide

**Python Projects:**
- **Typer** (recommended): Modern type-safe CLIs with minimal boilerplate
- **Click**: Mature, flexible CLIs for complex command hierarchies

**Go Projects:**
- **Cobra** (recommended): Industry standard for enterprise tools (Kubernetes, Docker, GitHub CLI)
- **urfave/cli**: Lightweight alternative for simple CLIs

**Rust Projects:**
- **clap v4** (recommended): Type-safe with derive API or builder API for runtime flexibility

## Core Patterns

### Arguments vs. Options vs. Flags

| Use Case | Type | Example |
|----------|------|---------|
| Primary required input | Positional Argument | `git commit -m "message"` |
| Optional configuration | Option | `--config app.yaml` |
| Boolean setting | Flag | `--verbose`, `--force` |
| Multiple values | Variadic Argument | `files...` |

### Configuration Precedence (Highest to Lowest)

1. CLI Arguments/Flags (explicit user input)
2. Environment Variables (session overrides)
3. Config File - Local (`./config.yaml`)
4. Config File - User (`~/.config/app/config.yaml`)
5. Config File - System (`/etc/app/config.yaml`)
6. Built-in Defaults (hardcoded)

### Output Formatting

| Use Case | Format | When |
|----------|--------|------|
| Human consumption | Colored text, tables | Default interactive mode |
| Machine consumption | JSON, YAML | `--output json`, piping |
| Logging/debugging | Plain text | `--verbose`, stderr |
| Progress tracking | Progress bars, spinners | Long operations |

## Best Practices

**Universal CLI Conventions:**
- Always provide `--help` and `-h` for usage information
- Always provide `--version` and `-V` for version display
- Clear error messages with actionable suggestions
- Exit code 0 for success, 1 for errors, 2 for usage errors
- Write errors to stderr, data to stdout

**Interactivity:**
- Detect TTY (interactive vs. piped input)
- Provide `--yes`/`--force` to skip prompts for automation
- Show progress for operations longer than 2 seconds

## Related Skills

- [Designing APIs](./designing-apis) - Building API client CLIs
- [Debugging Techniques](./debugging-techniques) - CLI testing and debugging
- [Writing GitHub Actions](./writing-github-actions) - Automated releases via GitHub Actions
- [Managing Git Workflows](./managing-git-workflows) - Git automation tools

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/building-clis)
