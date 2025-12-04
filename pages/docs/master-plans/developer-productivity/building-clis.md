---
sidebar_position: 2
---

# Building CLIs

Master plan for creating professional command-line interfaces with excellent user experience. This skill covers CLI design patterns, argument parsing, interactive prompts, output formatting, and distribution strategies for building tools that developers love to use.

## Status

<span class="badge badge--primary">Master Plan Available</span>

## Key Topics

- **CLI Architecture**
  - Command structure and subcommand patterns
  - Argument and option parsing
  - Configuration file management (JSON, YAML, TOML)
  - Environment variable handling
  - Plugin and extension systems

- **User Experience**
  - Interactive prompts and wizards
  - Progress indicators and spinners
  - Colorized output and formatting
  - Error messages and help text
  - Tab completion and shell integration

- **Input/Output Handling**
  - STDIN/STDOUT/STDERR usage
  - Pipe and redirection support
  - Output formats (JSON, YAML, table, plain text)
  - Verbose and quiet modes
  - Log levels and debugging output

- **Testing & Quality**
  - Unit testing CLI commands
  - Integration testing with subprocess
  - Snapshot testing for output
  - Cross-platform compatibility
  - Error handling and exit codes

- **Distribution & Updates**
  - Package managers (npm, pip, cargo, homebrew)
  - Binary compilation and distribution
  - Auto-update mechanisms
  - Version checking and migration

## Primary Tools & Technologies

- **Node.js**: Commander.js, Yargs, Inquirer, Chalk, Ora
- **Python**: Click, Typer, argparse, Rich, Typer
- **Go**: Cobra, Viper, urfave/cli
- **Rust**: Clap, structopt
- **Testing**: Jest, pytest, Go testing, Rust testing frameworks

## Integration Points

- **API Design Principles**: CLIs consume APIs
- **SDK Design**: CLIs can wrap SDK functionality
- **Git Workflows**: Git is a CLI tool pattern to emulate
- **Documentation Generation**: Generate CLI help from code
- **Debugging Techniques**: CLI debugging strategies

## Related Skills

- Shell scripting and automation
- DevOps and deployment tools
- Terminal UI/TUI development
- Package management
- Cross-platform development

## Implementation Approach

The skill will provide:
- CLI project templates for multiple languages
- Command structure design patterns
- Interactive prompt examples
- Output formatting utilities
- Testing strategy templates
- Distribution checklists
