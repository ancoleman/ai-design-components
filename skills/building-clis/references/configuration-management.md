# Configuration Management Guide

Comprehensive guide to managing CLI configuration from multiple sources with proper precedence and validation.

## Table of Contents

- [Configuration Sources](#configuration-sources)
- [Precedence Strategy](#precedence-strategy)
- [File Formats](#file-formats)
- [Multi-Language Implementation](#multi-language-implementation)
- [Best Practices](#best-practices)

## Configuration Sources

### Standard Configuration Hierarchy

1. **CLI Arguments/Flags** (Highest Priority)
   - Explicitly provided by user
   - Always takes precedence
   - Example: `--port 8080`

2. **Environment Variables**
   - Session-specific overrides
   - Useful for CI/CD and containers
   - Example: `export MYAPP_PORT=8080`

3. **Config File - Local** (Project-Level)
   - Project-specific settings
   - Location: `./myapp.yaml` or `./.myapp.yaml`
   - Committed to version control (usually)

4. **Config File - User** (User-Level)
   - User-specific settings across projects
   - Location: `~/.config/myapp/config.yaml` (XDG)
   - Not committed to version control

5. **Config File - System** (System-Level)
   - System-wide defaults for all users
   - Location: `/etc/myapp/config.yaml` (Unix)
   - Managed by system administrators

6. **Built-in Defaults** (Lowest Priority)
   - Hardcoded in application
   - Fallback when nothing else is specified

## Precedence Strategy

### Implementation Pattern

**Merge Strategy:**
```
final_value = (
    cli_arg
    OR env_var
    OR local_config_value
    OR user_config_value
    OR system_config_value
    OR default_value
)
```

**Example:**
```bash
# System config: port = 3000
# User config: port = 4000
# Local config: port = 5000
# Environment: MYAPP_PORT=6000
# CLI arg: --port 8080

# Result: port = 8080 (CLI arg wins)
```

### Partial Override Strategy

Some configurations support partial overrides (merge, not replace):

**Example:**
```yaml
# System config
database:
  host: localhost
  port: 5432

# User config (merges with system)
database:
  port: 5433  # Overrides port only

# Result:
database:
  host: localhost  # From system
  port: 5433       # From user
```

## File Formats

### YAML (Recommended)

**Advantages:**
- Human-readable
- Supports comments
- Natural for nested data
- Wide ecosystem support

**Example (myapp.yaml):**
```yaml
# Server configuration
server:
  host: localhost
  port: 8080
  workers: 4

# Database configuration
database:
  host: db.example.com
  port: 5432
  name: myapp_db
  credentials:
    user: dbuser
    # password loaded from environment

# Feature flags
features:
  enable_cache: true
  enable_metrics: true
  log_level: info
```

### TOML (Alternative)

**Advantages:**
- Explicit types
- Good for flat or moderately nested data
- Popular in Rust ecosystem (Cargo.toml)

**Example (myapp.toml):**
```toml
[server]
host = "localhost"
port = 8080
workers = 4

[database]
host = "db.example.com"
port = 5432
name = "myapp_db"

[database.credentials]
user = "dbuser"

[features]
enable_cache = true
enable_metrics = true
log_level = "info"
```

### JSON (Machine-Friendly)

**Advantages:**
- Universal support
- Strict validation
- Good for programmatic generation

**Disadvantages:**
- No comments (limitation)
- Less human-friendly

**Example (myapp.json):**
```json
{
  "server": {
    "host": "localhost",
    "port": 8080,
    "workers": 4
  },
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "name": "myapp_db"
  }
}
```

**Recommendation:** Use YAML for user-facing configs, JSON for machine-generated configs.

## Multi-Language Implementation

### Python: YAML + Environment Variables

**Implementation:**
```python
import os
import yaml
from pathlib import Path
from typing import Any, Optional

class Config:
    def __init__(self):
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load configuration from multiple sources with precedence."""
        # 1. System config
        system_config = Path("/etc/myapp/config.yaml")
        if system_config.exists():
            self.config.update(yaml.safe_load(system_config.read_text()))

        # 2. User config (XDG)
        user_config = Path.home() / ".config" / "myapp" / "config.yaml"
        if user_config.exists():
            self.config.update(yaml.safe_load(user_config.read_text()))

        # 3. Local config
        local_config = Path("./myapp.yaml")
        if not local_config.exists():
            local_config = Path("./.myapp.yaml")
        if local_config.exists():
            self.config.update(yaml.safe_load(local_config.read_text()))

    def get(self, key: str, env_var: Optional[str] = None, default: Any = None) -> Any:
        """Get config value with environment variable override."""
        # 1. Check environment variable
        if env_var and (value := os.getenv(env_var)):
            return value

        # 2. Check config file
        if key in self.config:
            return self.config[key]

        # 3. Return default
        return default

# Usage in Typer app
import typer

app = typer.Typer()
config = Config()

@app.command()
def serve(
    host: Optional[str] = typer.Option(None, "--host", help="Server host"),
    port: Optional[int] = typer.Option(None, "--port", help="Server port"),
):
    """Start server with merged configuration."""
    # Precedence: CLI arg > env var > config file > default
    final_host = host or config.get("server.host", "MYAPP_HOST", "localhost")
    final_port = port or config.get("server.port", "MYAPP_PORT", 8080)

    typer.echo(f"Starting server at {final_host}:{final_port}")
```

**With Pydantic for Validation:**
```python
from pydantic import BaseSettings, Field

class ServerConfig(BaseSettings):
    host: str = Field(default="localhost", env="MYAPP_HOST")
    port: int = Field(default=8080, env="MYAPP_PORT")
    workers: int = Field(default=4, env="MYAPP_WORKERS")

    class Config:
        # Automatically load from environment variables
        case_sensitive = False
        env_prefix = "MYAPP_"

# Usage
server_config = ServerConfig()
print(f"Host: {server_config.host}, Port: {server_config.port}")
```

### Go: Viper for Configuration

**Implementation:**
```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

func initConfig() {
    // Set config file name and type
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")

    // Add config search paths (precedence: local > user > system)
    viper.AddConfigPath(".")                      // Local
    viper.AddConfigPath("$HOME/.config/myapp")   // User
    viper.AddConfigPath("/etc/myapp")            // System

    // Environment variable support
    viper.SetEnvPrefix("MYAPP")  // MYAPP_HOST, MYAPP_PORT
    viper.AutomaticEnv()         // Automatically bind env vars

    // Read config file
    if err := viper.ReadInConfig(); err == nil {
        fmt.Println("Using config file:", viper.ConfigFileUsed())
    }
}

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My application",
}

var serveCmd = &cobra.Command{
    Use:   "serve",
    Short: "Start server",
    Run: func(cmd *cobra.Command, args []string) {
        // Get values with precedence: flag > env > config > default
        host := viper.GetString("host")
        port := viper.GetInt("port")

        fmt.Printf("Starting server at %s:%d\n", host, port)
    },
}

func init() {
    // Initialize config before commands run
    cobra.OnInitialize(initConfig)

    // Define flags
    serveCmd.Flags().String("host", "localhost", "Server host")
    serveCmd.Flags().Int("port", 8080, "Server port")

    // Bind flags to viper
    viper.BindPFlag("host", serveCmd.Flags().Lookup("host"))
    viper.BindPFlag("port", serveCmd.Flags().Lookup("port"))

    rootCmd.AddCommand(serveCmd)
}

func main() {
    rootCmd.Execute()
}
```

**Viper Features:**
- Automatic precedence handling
- Environment variable binding
- Multiple config file formats (YAML, TOML, JSON)
- Live config reloading (optional)
- Default value management

### Rust: config crate + Environment

**Cargo.toml:**
```toml
[dependencies]
config = "0.13"
serde = { version = "1.0", features = ["derive"] }
```

**Implementation:**
```rust
use config::{Config, ConfigError, Environment, File};
use serde::Deserialize;
use std::env;

#[derive(Debug, Deserialize)]
struct ServerConfig {
    host: String,
    port: u16,
    workers: usize,
}

#[derive(Debug, Deserialize)]
struct AppConfig {
    server: ServerConfig,
}

fn load_config() -> Result<AppConfig, ConfigError> {
    let mut settings = Config::builder()
        // 1. System config
        .add_source(File::with_name("/etc/myapp/config").required(false))
        // 2. User config (XDG)
        .add_source(
            File::with_name(&format!(
                "{}/.config/myapp/config",
                env::var("HOME").unwrap_or_default()
            ))
            .required(false),
        )
        // 3. Local config
        .add_source(File::with_name("./myapp").required(false))
        .add_source(File::with_name("./.myapp").required(false))
        // 4. Environment variables (MYAPP_SERVER_HOST, MYAPP_SERVER_PORT)
        .add_source(Environment::with_prefix("MYAPP").separator("_"))
        // 5. Defaults
        .set_default("server.host", "localhost")?
        .set_default("server.port", 8080)?
        .set_default("server.workers", 4)?
        .build()?;

    settings.try_deserialize()
}

use clap::Parser;

#[derive(Parser)]
struct Cli {
    /// Server host
    #[arg(long)]
    host: Option<String>,

    /// Server port
    #[arg(long)]
    port: Option<u16>,
}

fn main() -> Result<(), ConfigError> {
    let cli = Cli::parse();
    let mut config = load_config()?;

    // CLI args override config
    if let Some(host) = cli.host {
        config.server.host = host;
    }
    if let Some(port) = cli.port {
        config.server.port = port;
    }

    println!(
        "Starting server at {}:{}",
        config.server.host, config.server.port
    );

    Ok(())
}
```

## Best Practices

### 1. Document Configuration Precedence

**In Help Text:**
```python
@app.command(help="""
Start the server.

Configuration precedence (highest to lowest):
1. CLI arguments (--host, --port)
2. Environment variables (MYAPP_HOST, MYAPP_PORT)
3. Local config file (./myapp.yaml)
4. User config file (~/.config/myapp/config.yaml)
5. System config file (/etc/myapp/config.yaml)
6. Built-in defaults
""")
def serve():
    pass
```

### 2. Provide Config Inspection

**Show Effective Configuration:**
```python
@app.command()
def config_show():
    """Show effective configuration (after merging all sources)."""
    config = load_config()
    print(yaml.dump(config, default_flow_style=False))
```

**Usage:**
```bash
$ myapp config show
server:
  host: localhost
  port: 8080
  workers: 4
database:
  host: db.example.com
  port: 5432
```

### 3. Validate Configuration Early

**Python (Pydantic):**
```python
from pydantic import BaseModel, Field, validator

class ServerConfig(BaseModel):
    host: str
    port: int = Field(ge=1, le=65535)  # Valid port range
    workers: int = Field(ge=1, le=100)

    @validator('host')
    def validate_host(cls, v):
        if not v or v.strip() == "":
            raise ValueError('host cannot be empty')
        return v

# Automatic validation on load
config = ServerConfig(**config_dict)  # Raises ValidationError if invalid
```

**Go (Validation):**
```go
func validateConfig() error {
    if port := viper.GetInt("port"); port < 1 || port > 65535 {
        return fmt.Errorf("invalid port: %d (must be 1-65535)", port)
    }
    if workers := viper.GetInt("workers"); workers < 1 {
        return fmt.Errorf("workers must be at least 1")
    }
    return nil
}
```

### 4. Support Config File Generation

**Generate Template:**
```python
@app.command()
def config_init(output: Path = typer.Option("./myapp.yaml")):
    """Generate a configuration file template."""
    template = """
# MyApp Configuration

server:
  host: localhost
  port: 8080
  workers: 4

database:
  host: localhost
  port: 5432
  name: myapp_db
"""
    output.write_text(template)
    typer.echo(f"Config template created at {output}")
```

### 5. Separate Secrets from Config

**Never commit secrets to config files!**

**Use environment variables for secrets:**
```yaml
# config.yaml (safe to commit)
database:
  host: db.example.com
  port: 5432
  name: myapp_db
  # password loaded from MYAPP_DB_PASSWORD environment variable
```

**Load secrets from environment:**
```python
import os

db_password = os.getenv("MYAPP_DB_PASSWORD")
if not db_password:
    raise ValueError("MYAPP_DB_PASSWORD environment variable required")
```

**Or use secrets management tools:**
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Kubernetes Secrets

### 6. Support Environment-Specific Configs

**Structure:**
```
config/
├── base.yaml           # Common settings
├── development.yaml    # Dev overrides
├── staging.yaml        # Staging overrides
└── production.yaml     # Prod overrides
```

**Load based on environment:**
```python
import os

env = os.getenv("APP_ENV", "development")
config_file = f"config/{env}.yaml"

config = yaml.safe_load(Path(config_file).read_text())
```

### 7. XDG Base Directory Specification (Linux/macOS)

**Follow XDG standards for config file locations:**

```python
from pathlib import Path
import os

# XDG_CONFIG_HOME defaults to ~/.config
xdg_config_home = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
user_config = xdg_config_home / "myapp" / "config.yaml"

# XDG_DATA_HOME defaults to ~/.local/share
xdg_data_home = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))
user_data = xdg_data_home / "myapp"

# XDG_CACHE_HOME defaults to ~/.cache
xdg_cache_home = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache"))
user_cache = xdg_cache_home / "myapp"
```

## Configuration Checklist

- [ ] Support multiple config sources (CLI, env, files)
- [ ] Implement clear precedence (CLI > env > local > user > system > default)
- [ ] Validate configuration on load
- [ ] Provide `config show` command to inspect effective config
- [ ] Provide `config init` to generate template
- [ ] Document precedence in help text
- [ ] Use environment variables for secrets
- [ ] Follow XDG Base Directory specification
- [ ] Support environment-specific configs (dev, staging, prod)
- [ ] Never commit secrets to version control
