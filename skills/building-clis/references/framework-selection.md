# CLI Framework Selection Guide

Comprehensive decision framework for choosing the appropriate CLI framework based on language, complexity, and requirements.

## Table of Contents

- [Decision Tree](#decision-tree)
- [Python Frameworks](#python-frameworks)
- [Go Frameworks](#go-frameworks)
- [Rust Frameworks](#rust-frameworks)
- [Comparison Matrix](#comparison-matrix)
- [Migration Paths](#migration-paths)

## Decision Tree

### Start: Choose Based on Existing Project

```
Q1: What language is the project using?
  ├─ Python → Go to Python Frameworks
  ├─ Go → Go to Go Frameworks
  ├─ Rust → Go to Rust Frameworks
  └─ New Project/Flexible → Go to Requirements-Based Selection
```

### Requirements-Based Selection (New Projects)

```
What is most important?

├─ Fast Development + Python Ecosystem
│  → Use Typer (Python)
│     - Type-safe, minimal boilerplate
│     - Rich ecosystem, easy distribution via PyPI
│     - 5-10 minutes to first working CLI
│
├─ Performance + Low Memory Footprint
│  → Use clap (Rust)
│     - Compile to native binary
│     - Minimal runtime overhead
│     - Type-safe at compile time
│
├─ Enterprise Integration + Go Ecosystem
│  → Use Cobra (Go)
│     - Industry standard (Kubernetes, Docker)
│     - Strong stdlib, easy cross-compilation
│     - Native binary distribution
│
└─ Quick Script (<100 lines)
   → Use Typer (Python)
      - Fastest time to working CLI
      - No compilation required
      - Easy to modify and iterate
```

## Python Frameworks

### Typer (Recommended for New Projects)

**When to Use:**
- New Python CLI projects (2025 standard)
- Type-safe applications with Python 3.7+
- Need auto-completion and validation
- Want minimal boilerplate with modern ergonomics
- Building CLI for FastAPI project (consistent tooling)

**Strengths:**
- Type hints for automatic validation and documentation
- Minimal code for full-featured CLIs
- Excellent error messages with suggestions
- Auto-completion support (bash, zsh, fish)
- Rich/colorful output built-in
- Built on Click (can drop down when needed)

**Considerations:**
- Requires Python 3.6+ (type hints)
- Younger ecosystem than Click
- Slightly slower than Click (minimal difference)

**Installation:**
```bash
pip install "typer[all]"  # Includes rich, shellingham
```

**Best For:**
- Developer tools and automation
- API client CLIs
- Modern Python projects
- Interactive CLIs with prompts/progress

### Click (Alternative for Complex/Legacy Projects)

**When to Use:**
- Existing projects already using Click
- Need specific Click plugins
- Complex nested command structures
- Python <3.6 support required (rare in 2025)
- Large existing Click codebase

**Strengths:**
- Very mature and stable (2014+)
- Large ecosystem of plugins
- Flexible and composable
- Excellent documentation
- Battle-tested in production

**Considerations:**
- More verbose than Typer
- No type hint integration
- Manual validation required

**Installation:**
```bash
pip install click
```

**Best For:**
- Complex multi-level command trees
- Legacy Python codebases
- Projects requiring specific Click plugins

### Comparison: Typer vs. Click

| Feature | Typer | Click |
|---------|-------|-------|
| Type Hints | ✅ Native | ❌ Manual |
| Boilerplate | Minimal | Medium |
| Auto-completion | ✅ Built-in | ⚠️ Via plugin |
| Ecosystem | Growing | Very Large |
| Maturity | Modern (2019+) | Very Mature (2014+) |
| Learning Curve | Easy | Easy |
| Documentation | Excellent | Excellent |
| Python Version | 3.6+ | 2.7+ |

**Decision:** Use Typer for new projects, Click for existing codebases or if specific plugins required.

## Go Frameworks

### Cobra (Recommended for Most Projects)

**When to Use:**
- Enterprise-grade CLI tools
- Complex subcommand hierarchies (like git, docker, kubectl)
- Go projects requiring configuration management (with Viper)
- Need POSIX-compliant flags
- Building developer tooling

**Strengths:**
- Industry standard (Kubernetes, Docker, GitHub CLI, Hugo, Terraform)
- Designed for complex multi-command CLIs
- Excellent subcommand support
- Viper integration for configuration
- Automatic help and usage generation
- Shell completion for all major shells
- Generator tool (`cobra-cli`) for scaffolding

**Considerations:**
- Can be overkill for simple CLIs (5-10 commands)
- More boilerplate than alternatives
- Steeper learning curve for beginners

**Installation:**
```bash
go get -u github.com/spf13/cobra@latest
```

**Best For:**
- Multi-command CLIs with 10+ commands
- Infrastructure tools (deployment, monitoring)
- Cloud provider CLIs
- Developer tooling (build systems, test runners)

### urfave/cli (Alternative for Simple CLIs)

**When to Use:**
- Simple CLI tools (5-10 commands max)
- Quick scripts and utilities
- Prefer minimal boilerplate
- Lightweight dependency footprint

**Strengths:**
- Simpler API than Cobra
- Less boilerplate for basic CLIs
- Good documentation with clear examples
- Lightweight (smaller binary size)

**Considerations:**
- Less powerful for complex command trees
- Smaller ecosystem than Cobra
- Less common in enterprise projects

**Installation:**
```bash
go get github.com/urfave/cli/v2
```

**Best For:**
- Single-purpose utilities
- Quick automation scripts
- Learning Go CLI development

### Comparison: Cobra vs. urfave/cli

| Feature | Cobra | urfave/cli |
|---------|-------|------------|
| Subcommand Support | Excellent | Good |
| Boilerplate | Medium | Low |
| Ecosystem | Very Large | Medium |
| Configuration | Viper Integration | Manual |
| Complexity Ceiling | High | Medium |
| Learning Curve | Medium | Easy |
| Industry Usage | Very High | Medium |
| Binary Size | Larger | Smaller |

**Decision:** Use Cobra for enterprise tools and complex CLIs, urfave/cli for simple utilities.

## Rust Frameworks

### clap v4 (Recommended for All Rust CLIs)

**When to Use:**
- All Rust CLI projects (default choice in 2025)
- Need compile-time safety (derive API)
- Performance-critical CLIs
- Want excellent error messages
- Building system utilities or developer tools

**Strengths:**
- Two APIs: Derive (declarative, type-safe) and Builder (programmatic, flexible)
- Compile-time validation (derive API catches errors before runtime)
- Improved v4: Faster compile times, better error messages
- Comprehensive feature set (subcommands, validation, shell completion, colored help)
- Active development with modern Rust idioms
- Performance: Minimal runtime overhead

**API Choice:**

**Derive API:**
- Type-safe at compile time
- Declarative (attributes on structs)
- Best for: Static command structures
- Example: Most CLIs with fixed commands

**Builder API:**
- Runtime flexibility
- Programmatic construction
- Best for: Dynamic commands, plugin systems
- Example: CLIs with runtime-loaded subcommands

**Considerations:**
- Derive API requires feature flag
- Learning curve for advanced features
- Compile times (improved in v4, still slower than interpreted languages)

**Installation:**
```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
```

**Best For:**
- Performance-critical tools
- System utilities (replacements for coreutils)
- Developer tools requiring fast startup
- Cross-platform binaries

### Alternative: structopt (Legacy)

**Note:** structopt is now deprecated. clap v3+ absorbed structopt's derive functionality. Migrate existing structopt projects to clap v4 derive API.

## Comparison Matrix

### Cross-Language Framework Comparison

| Framework | Language | API Style | Compile | Type Safety | Binary Size | Startup Time | Best Use Case |
|-----------|----------|-----------|---------|-------------|-------------|--------------|---------------|
| **Typer** | Python | Decorator | No | ⭐⭐⭐⭐⭐ | N/A | ~100ms | Modern Python CLIs |
| **Click** | Python | Decorator | No | ⭐⭐⭐ | N/A | ~100ms | Complex Python CLIs |
| **Cobra** | Go | Struct | Yes | ⭐⭐⭐⭐ | ~8-15MB | ~5ms | Enterprise Go CLIs |
| **urfave/cli** | Go | Struct | Yes | ⭐⭐⭐ | ~5-8MB | ~5ms | Simple Go CLIs |
| **clap** | Rust | Derive/Builder | Yes | ⭐⭐⭐⭐⭐ | ~2-5MB | ~1ms | Performance Rust CLIs |

### Feature Support Matrix

| Feature | Typer | Click | Cobra | urfave/cli | clap |
|---------|-------|-------|-------|------------|------|
| Subcommands | ✅ | ✅ | ✅ Excellent | ✅ Good | ✅ Excellent |
| Shell Completion | ✅ | ⚠️ Plugin | ✅ | ❌ | ✅ |
| Config Files | ⚠️ Manual | ⚠️ Manual | ✅ Viper | ⚠️ Manual | ⚠️ config crate |
| Type Safety | ✅ Type Hints | ❌ | ⚠️ Compile | ⚠️ Compile | ✅ Compile |
| Progress Bars | ✅ rich | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ indicatif |
| Colored Output | ✅ rich | ✅ | ⚠️ Manual | ⚠️ Manual | ✅ |
| Auto Help | ✅ | ✅ | ✅ | ✅ | ✅ |
| Validation | ✅ Type-based | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ✅ Derive |

## Migration Paths

### Python: Click → Typer

**Why Migrate:**
- Modern type safety with type hints
- Reduced boilerplate
- Better auto-completion support

**Migration Strategy:**
```python
# Click
import click

@click.command()
@click.argument('name')
@click.option('--count', default=1)
def hello(name, count):
    click.echo(f'Hello {name}!' * count)

# Typer equivalent
import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def hello(
    name: Annotated[str, typer.Argument()],
    count: Annotated[int, typer.Option()] = 1
):
    typer.echo(f'Hello {name}!' * count)
```

**Gradual Migration:**
- Typer is built on Click (can coexist)
- Migrate command by command
- Use Click's `@click.pass_context` for interop

### Go: urfave/cli → Cobra

**Why Migrate:**
- Better subcommand support
- Viper configuration integration
- Industry standard tooling

**Migration Strategy:**
```go
// urfave/cli
app := &cli.App{
    Name: "myapp",
    Action: func(c *cli.Context) error {
        fmt.Println("Hello")
        return nil
    },
}

// Cobra equivalent
var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My application",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("Hello")
    },
}
```

**Gradual Migration:**
- Start with root command
- Migrate subcommands one at a time
- Test thoroughly (API differences)

### Rust: structopt → clap v4

**Why Migrate:**
- structopt is deprecated
- clap v4 has better compile times
- More features and active development

**Migration Strategy:**
```rust
// Old structopt
use structopt::StructOpt;

#[derive(StructOpt)]
struct Cli {
    #[structopt(short, long)]
    verbose: bool,
}

// New clap v4
use clap::Parser;

#[derive(Parser)]
struct Cli {
    #[arg(short, long)]
    verbose: bool,
}
```

**Changes:**
- `#[structopt(...)]` → `#[arg(...)]`
- `#[derive(StructOpt)]` → `#[derive(Parser)]`
- Import from `clap` instead of `structopt`

## Decision Checklist

Use this checklist to select the appropriate framework:

**Project Context:**
- [ ] What language is the project using?
- [ ] Is this a new project or existing codebase?
- [ ] What is the expected complexity (simple, medium, complex)?

**Requirements:**
- [ ] Performance requirements (startup time, memory)?
- [ ] Type safety requirements?
- [ ] Distribution method (PyPI, Homebrew, binary)?
- [ ] Team expertise (language familiarity)?

**Features Needed:**
- [ ] Subcommand support?
- [ ] Configuration file management?
- [ ] Shell completion?
- [ ] Interactive features (prompts, progress)?

**Recommendations Based on Answers:**

**Python:**
- New project + type safety → Typer
- Existing Click project → Click (or migrate to Typer)
- Complex command trees → Click or Typer

**Go:**
- Enterprise tool + complex commands → Cobra
- Simple utility → urfave/cli
- Need configuration management → Cobra + Viper

**Rust:**
- Any Rust CLI → clap v4 (derive or builder)
- Static commands → derive API
- Dynamic commands → builder API
