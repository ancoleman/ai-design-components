# Subcommand Design Guide

Comprehensive guide to structuring CLI command hierarchies with subcommands, nesting strategies, and organization patterns.

## Table of Contents

- [Command Structure Patterns](#command-structure-patterns)
- [Organization Strategies](#organization-strategies)
- [Naming Conventions](#naming-conventions)
- [Language-Specific Implementation](#language-specific-implementation)
- [Best Practices](#best-practices)

## Command Structure Patterns

### Pattern 1: Flat Structure (Single Level)

**Structure:**
```
app command1 [args]
app command2 [args]
app command3 [args]
```

**When to Use:**
- Small CLIs with 5-10 distinct operations
- Commands are independent (no natural groupings)
- Simplicity is priority

**Example:**
```bash
myapp deploy
myapp logs
myapp status
myapp restart
myapp rollback
```

**Advantages:**
- Simple to understand and use
- Low cognitive load
- Easy to implement

**Disadvantages:**
- Doesn't scale beyond 10-15 commands
- No logical grouping of related operations

### Pattern 2: Grouped Structure (Two Levels)

**Structure:**
```
app group1 subcommand [args]
app group2 subcommand [args]
```

**When to Use:**
- Medium CLIs with logical groupings (10-30 commands)
- Commands naturally cluster by resource or action
- Need organization without overwhelming complexity

**Example (Resource-Based Grouping):**
```bash
kubectl get pods
kubectl get services
kubectl create deployment
kubectl create service
kubectl delete pod
kubectl delete deployment
```

**Example (Action-Based Grouping):**
```bash
docker container start
docker container stop
docker container list
docker image build
docker image push
docker image pull
```

**Advantages:**
- Logical organization
- Scalable to 30-40 commands
- Discoverable via help

**Disadvantages:**
- Slightly more typing
- Requires choosing between resource-based or action-based grouping

### Pattern 3: Nested Structure (Three+ Levels)

**Structure:**
```
app group subgroup command [args]
```

**When to Use:**
- Large CLIs with deep hierarchies (30+ commands)
- Complex domains with multiple dimensions of organization
- Cloud provider CLIs, infrastructure tools

**Example:**
```bash
gcloud compute instances create
gcloud compute instances delete
gcloud compute disks create
gcloud container clusters create
aws ec2 describe-instances
aws s3 cp
```

**Advantages:**
- Handles very large command sets
- Precise organization

**Disadvantages:**
- Can become unwieldy (typing overhead)
- Difficult to remember deep paths
- Risk of over-nesting

**⚠️ Warning:** Avoid nesting beyond 3 levels. Beyond this, consider:
- Flattening hierarchy
- Splitting into multiple CLI tools
- Using aliases for common paths

## Organization Strategies

### Strategy 1: Resource-Based (CRUD Pattern)

**Organization:** Group by resource type (nouns)

**Structure:**
```
app resource action [args]
```

**Example:**
```bash
# Kubernetes-style
kubectl get pods
kubectl get services
kubectl create deployment
kubectl delete pod

# Database CLI
dbcli users list
dbcli users create
dbcli tables describe
dbcli tables drop
```

**When to Use:**
- Managing resources (infrastructure, databases)
- CRUD operations are primary use case
- Users think in terms of "what" they're managing

**Advantages:**
- Natural for resource management
- Clear resource boundaries
- Easy to add new resources

**Implementation:**

**Python (Typer):**
```python
import typer

app = typer.Typer()

# Create subapps for each resource
pods_app = typer.Typer()
services_app = typer.Typer()

@pods_app.command("list")
def list_pods():
    """List all pods."""
    pass

@pods_app.command("create")
def create_pod(name: str):
    """Create a pod."""
    pass

# Mount subapps
app.add_typer(pods_app, name="pods")
app.add_typer(services_app, name="services")
```

**Go (Cobra):**
```go
var rootCmd = &cobra.Command{Use: "myapp"}

var podsCmd = &cobra.Command{Use: "pods"}
var listPodsCmd = &cobra.Command{
    Use:   "list",
    Run: func(cmd *cobra.Command, args []string) {
        // List pods
    },
}

podsCmd.AddCommand(listPodsCmd)
rootCmd.AddCommand(podsCmd)
```

### Strategy 2: Action-Based (Verb-First Pattern)

**Organization:** Group by action type (verbs)

**Structure:**
```
app action resource [args]
```

**Example:**
```bash
# Git-style
git add file.txt
git commit -m "message"
git push origin main

# Build tool
build compile src/
build test unit
build package dist/
```

**When to Use:**
- Actions are the primary mental model
- Workflows are action-centric
- Consistent actions across different resources

**Advantages:**
- Natural for workflow-oriented CLIs
- Actions are prominent
- Good for task-based thinking

**Implementation:**

**Python (Typer):**
```python
app = typer.Typer()

create_app = typer.Typer()
delete_app = typer.Typer()

@create_app.command("pod")
def create_pod(name: str):
    pass

@create_app.command("service")
def create_service(name: str):
    pass

app.add_typer(create_app, name="create")
app.add_typer(delete_app, name="delete")
```

### Strategy 3: Hybrid (Context-Dependent)

**Organization:** Mix resource-based and action-based as appropriate

**Structure:**
```
app [context] action [resource] [args]
```

**Example:**
```bash
# Docker uses hybrid approach
docker container run    # resource-based
docker build           # action-based
docker image ls        # resource-based
docker login           # action-based

# AWS CLI
aws s3 cp              # action on resource
aws ec2 describe-instances  # action on resource
aws configure          # standalone action
```

**When to Use:**
- Some commands are clearly resource-bound
- Other commands are standalone actions
- Pragmatic balance between consistency and usability

**Best Practice:** Be consistent within each command group, even if different groups use different patterns.

## Naming Conventions

### Command Naming

**Use Verbs for Actions:**
- `create`, `delete`, `update`, `list`, `get`, `show`
- `deploy`, `rollback`, `restart`, `stop`, `start`
- `build`, `test`, `run`, `clean`

**Use Nouns for Resources:**
- `pod`, `service`, `deployment`, `node`
- `user`, `database`, `table`, `index`
- `instance`, `volume`, `snapshot`, `image`

**Avoid Ambiguity:**
- ✅ `list` or `ls` (clear)
- ❌ `l` (too short, unclear)
- ✅ `delete` or `remove` or `rm` (pick one, be consistent)
- ❌ Mix of `delete`, `remove`, `del`, `rm` (inconsistent)

### Consistency Rules

**Verb Consistency:**
- Choose one verb per action and stick to it
- ✅ Always use `create` (not mix of `create`, `new`, `add`)
- ✅ Always use `list` (not mix of `list`, `ls`, `show`)

**Noun Consistency:**
- Use singular or plural consistently
- ✅ `pod`, `service` (singular)
- ✅ `pods`, `services` (plural)
- ❌ Mix of `pod` and `services` (inconsistent)

**Abbreviations:**
- Support both full and short forms where appropriate
- `list` and `ls`, `delete` and `rm`
- Document abbreviations in help text

### Alias Support

**Common Aliases:**
```bash
# kubectl supports aliases
kubectl get pods  # full
kubectl get po    # abbreviated

# git supports aliases
git checkout      # full
git co            # alias
```

**Implementation:**

**Python (Typer):**
```python
@app.command("list", help="List resources")
@app.command("ls", help="List resources (alias)")
def list_resources():
    pass
```

**Go (Cobra):**
```go
var listCmd = &cobra.Command{
    Use:     "list",
    Aliases: []string{"ls"},
    Short:   "List resources",
}
```

**Rust (clap):**
```rust
#[derive(Subcommand)]
enum Commands {
    #[command(alias = "ls")]
    List,
}
```

## Language-Specific Implementation

### Python: Nested Typer Apps

**Pattern:**
```python
import typer

# Root app
app = typer.Typer()

# Resource group apps
pods_app = typer.Typer()
services_app = typer.Typer()

# Commands within resource groups
@pods_app.command("list")
def list_pods():
    """List all pods."""
    typer.echo("Listing pods...")

@pods_app.command("create")
def create_pod(name: str):
    """Create a pod."""
    typer.echo(f"Creating pod: {name}")

@services_app.command("list")
def list_services():
    """List all services."""
    typer.echo("Listing services...")

# Mount resource groups to root
app.add_typer(pods_app, name="pods", help="Manage pods")
app.add_typer(services_app, name="services", help="Manage services")

if __name__ == "__main__":
    app()
```

**Usage:**
```bash
python app.py pods list
python app.py pods create my-pod
python app.py services list
```

### Go: Nested Cobra Commands

**Pattern:**
```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My application",
}

// Resource group commands
var podsCmd = &cobra.Command{
    Use:   "pods",
    Short: "Manage pods",
}

var servicesCmd = &cobra.Command{
    Use:   "services",
    Short: "Manage services",
}

// Subcommands
var listPodsCmd = &cobra.Command{
    Use:   "list",
    Short: "List pods",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("Listing pods...")
    },
}

var createPodCmd = &cobra.Command{
    Use:   "create [name]",
    Short: "Create pod",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Printf("Creating pod: %s\n", args[0])
    },
}

func init() {
    // Build hierarchy
    podsCmd.AddCommand(listPodsCmd, createPodCmd)
    servicesCmd.AddCommand(/* service commands */)
    rootCmd.AddCommand(podsCmd, servicesCmd)
}

func main() {
    rootCmd.Execute()
}
```

### Rust: Nested clap Subcommands

**Pattern:**
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "myapp")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Manage pods
    Pods {
        #[command(subcommand)]
        subcommand: PodCommands,
    },
    /// Manage services
    Services {
        #[command(subcommand)]
        subcommand: ServiceCommands,
    },
}

#[derive(Subcommand)]
enum PodCommands {
    /// List all pods
    List,
    /// Create a pod
    Create {
        /// Pod name
        name: String,
    },
}

#[derive(Subcommand)]
enum ServiceCommands {
    /// List all services
    List,
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Pods { subcommand } => match subcommand {
            PodCommands::List => println!("Listing pods..."),
            PodCommands::Create { name } => println!("Creating pod: {}", name),
        },
        Commands::Services { subcommand } => match subcommand {
            ServiceCommands::List => println!("Listing services..."),
        },
    }
}
```

## Best Practices

### 1. Keep Command Paths Short

**Good:**
```bash
docker run nginx
kubectl get pods
git commit -m "message"
```

**Too Deep:**
```bash
myapp infrastructure cloud aws ec2 instances list region us-west-2
# 7 levels deep - too much!
```

**Better:**
```bash
myapp aws ec2 list --region us-west-2
# Flatten hierarchy, use flags for details
```

### 2. Group Logically

**Resource-Based (Good for CRUD):**
```bash
myapp users list
myapp users create
myapp users delete
```

**Action-Based (Good for Workflows):**
```bash
myapp deploy prod
myapp deploy staging
myapp rollback
```

### 3. Provide Clear Help at Each Level

**Root Level Help:**
```bash
$ myapp --help
Usage: myapp <COMMAND>

Commands:
  pods      Manage pods
  services  Manage services
  deploy    Deploy application
  logs      View logs
```

**Subcommand Level Help:**
```bash
$ myapp pods --help
Usage: myapp pods <COMMAND>

Commands:
  list    List all pods
  create  Create a pod
  delete  Delete a pod
  get     Get pod details
```

### 4. Support Common Patterns

**CRUD Operations:**
```bash
app resource create
app resource list
app resource get <id>
app resource update <id>
app resource delete <id>
```

**Lifecycle Operations:**
```bash
app resource start
app resource stop
app resource restart
app resource status
```

### 5. Design for Discoverability

**Use `--help` liberally:**
```bash
myapp --help           # Root help
myapp pods --help      # Group help
myapp pods list --help # Command help
```

**Show examples in help:**
```python
@app.command(help="""
List all pods.

Examples:
  myapp pods list
  myapp pods list --namespace default
  myapp pods list --output json
""")
def list_pods():
    pass
```

### 6. Handle Global Flags

**Persistent Flags (Go Cobra):**
```go
// Available to all subcommands
rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "Verbose")
rootCmd.PersistentFlags().StringVar(&config, "config", "", "Config file")
```

**Global Options (Python Typer):**
```python
app = typer.Typer()

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    config: str = typer.Option("config.yaml", "--config")
):
    """Global options available to all commands."""
    # Store in context or global state
    pass
```

## Anti-Patterns to Avoid

### ❌ Inconsistent Naming
```bash
myapp create user
myapp new-database  # Should be: myapp create database
myapp add-role      # Should be: myapp create role
```

### ❌ Over-Nesting
```bash
myapp infrastructure cloud provider aws region us-west-2 ec2 instances list
# Too deep! Simplify to:
myapp aws ec2 list --region us-west-2
```

### ❌ Ambiguous Commands
```bash
myapp run      # Run what? Tests? Server? Script?
myapp process  # Process what?

# Better:
myapp server run
myapp tests run
```

### ❌ Mixing Patterns Randomly
```bash
myapp user create   # resource-based
myapp create role   # action-based
myapp delete user   # action-based
# Pick one pattern and stick to it!
```

## Command Hierarchy Checklist

- [ ] Commands grouped logically (resource or action based)
- [ ] Maximum nesting depth of 3 levels
- [ ] Consistent verb usage (create, list, delete)
- [ ] Consistent noun usage (singular or plural)
- [ ] Help available at each level
- [ ] Common aliases provided (ls, rm)
- [ ] Global flags available to all subcommands
- [ ] Examples in help text
- [ ] Clear, descriptive command names
