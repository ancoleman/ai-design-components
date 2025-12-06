# Shell Completion Guide

Guide to generating and installing shell completions for bash, zsh, fish, and PowerShell.

## Table of Contents

- [Python (Typer)](#python-typer)
- [Go (Cobra)](#go-cobra)
- [Rust (clap)](#rust-clap)
- [Installation Instructions](#installation-instructions)

## Python (Typer)

### Generating Completions

Typer supports automatic completion generation via environment variables:

```bash
# Bash
_MYAPP_COMPLETE=bash_source myapp > ~/.myapp-complete.bash

# Zsh
_MYAPP_COMPLETE=zsh_source myapp > ~/.myapp-complete.zsh

# Fish
_MYAPP_COMPLETE=fish_source myapp > ~/.config/fish/completions/myapp.fish

# PowerShell
_MYAPP_COMPLETE=powershell_source myapp > ~/.myapp-complete.ps1
```

### Implementation

No special code required - Typer handles completion automatically via Click.

### Installation

**Bash:**
```bash
echo "source ~/.myapp-complete.bash" >> ~/.bashrc
source ~/.bashrc
```

**Zsh:**
```bash
echo "source ~/.myapp-complete.zsh" >> ~/.zshrc
source ~/.zshrc
```

**Fish:**
```bash
# Completion file already in correct location
# Restart fish shell
```

**PowerShell:**
```powershell
Add-Content $PROFILE ". ~/.myapp-complete.ps1"
```

## Go (Cobra)

### Generating Completions

Add completion command to your CLI:

```go
package main

import (
    "github.com/spf13/cobra"
    "os"
)

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My application",
}

var completionCmd = &cobra.Command{
    Use:   "completion [bash|zsh|fish|powershell]",
    Short: "Generate shell completion scripts",
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
}

func init() {
    rootCmd.AddCommand(completionCmd)
}

func main() {
    rootCmd.Execute()
}
```

### Usage

```bash
# Generate completion
myapp completion bash > /etc/bash_completion.d/myapp
myapp completion zsh > "${fpath[1]}/_myapp"
myapp completion fish > ~/.config/fish/completions/myapp.fish
myapp completion powershell > ~/.myapp-complete.ps1
```

### Custom Completions

For dynamic completions (e.g., resource names from API):

```go
var getCmd = &cobra.Command{
    Use:   "get [resource]",
    Short: "Get a resource",
    ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
        if len(args) == 0 {
            // Complete resource types
            return []string{"pods", "services", "deployments"}, cobra.ShellCompDirectiveNoFileComp
        }
        return nil, cobra.ShellCompDirectiveNoFileComp
    },
}
```

## Rust (clap)

### Dependencies

Add to `Cargo.toml`:
```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
clap_complete = "4.5"
```

### Implementation

```rust
use clap::{CommandFactory, Parser, Subcommand};
use clap_complete::{generate, shells::{Bash, Zsh, Fish, PowerShell}};
use std::io;

#[derive(Parser)]
#[command(name = "myapp")]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    /// Generate shell completion scripts
    Completion {
        #[arg(value_enum)]
        shell: Shell,
    },
}

#[derive(clap::ValueEnum, Clone)]
enum Shell {
    Bash,
    Zsh,
    Fish,
    PowerShell,
}

fn main() {
    let cli = Cli::parse();

    if let Some(Commands::Completion { shell }) = cli.command {
        let mut cmd = Cli::command();
        match shell {
            Shell::Bash => generate(Bash, &mut cmd, "myapp", &mut io::stdout()),
            Shell::Zsh => generate(Zsh, &mut cmd, "myapp", &mut io::stdout()),
            Shell::Fish => generate(Fish, &mut cmd, "myapp", &mut io::stdout()),
            Shell::PowerShell => generate(PowerShell, &mut cmd, "myapp", &mut io::stdout()),
        }
    }
}
```

### Usage

```bash
myapp completion bash > /etc/bash_completion.d/myapp
myapp completion zsh > "${fpath[1]}/_myapp"
myapp completion fish > ~/.config/fish/completions/myapp.fish
```

## Installation Instructions

### Bash

**System-wide:**
```bash
sudo myapp completion bash > /etc/bash_completion.d/myapp
```

**User-level:**
```bash
myapp completion bash > ~/.myapp-complete.bash
echo "source ~/.myapp-complete.bash" >> ~/.bashrc
```

### Zsh

**System-wide:**
```bash
sudo myapp completion zsh > /usr/local/share/zsh/site-functions/_myapp
```

**User-level:**
```bash
mkdir -p ~/.zsh/completion
myapp completion zsh > ~/.zsh/completion/_myapp
echo 'fpath=(~/.zsh/completion $fpath)' >> ~/.zshrc
echo 'autoload -Uz compinit && compinit' >> ~/.zshrc
```

### Fish

**User-level (standard location):**
```bash
myapp completion fish > ~/.config/fish/completions/myapp.fish
```

### PowerShell

**User-level:**
```powershell
myapp completion powershell > ~/.myapp-complete.ps1
Add-Content $PROFILE ". ~/.myapp-complete.ps1"
```

## Testing Completions

**Bash:**
```bash
# Type command and press TAB twice
myapp <TAB><TAB>

# Should show available subcommands
```

**Zsh:**
```zsh
# Type command and press TAB
myapp <TAB>

# Should show completions with descriptions
```

**Fish:**
```fish
# Type command and press TAB
myapp <TAB>

# Should show completions with descriptions
```

## Best Practices

- Add completion command to CLI (`myapp completion bash`)
- Include installation instructions in README
- Test completions in all supported shells
- Document completion in `--help` output
- Provide installation script for ease of use
