# Error Handling Patterns for Shell Scripts

Comprehensive guide to error handling patterns in shell scripts, covering fail-fast behaviors, explicit checking, cleanup handlers, and defensive programming.

## Table of Contents

- [Set Options for Fail-Fast Behavior](#set-options-for-fail-fast-behavior)
- [Explicit Exit Code Checking](#explicit-exit-code-checking)
- [Trap Handlers for Cleanup](#trap-handlers-for-cleanup)
- [Defensive Programming Patterns](#defensive-programming-patterns)
- [Error Reporting Best Practices](#error-reporting-best-practices)
- [Common Error Scenarios](#common-error-scenarios)

---

## Set Options for Fail-Fast Behavior

### The Standard Pattern: set -euo pipefail

```bash
#!/bin/bash
set -euo pipefail

# -e: Exit immediately if any command exits with non-zero status
# -u: Treat unset variables as an error
# -o pipefail: Return exit code of rightmost failed command in pipeline
```

### Individual Option Behaviors

#### -e (errexit)

Exits immediately if any command returns non-zero:

```bash
#!/bin/bash
set -e

false  # Script exits here with exit code 1
echo "This will never execute"
```

**Exceptions where -e does NOT exit:**
- Commands in conditional tests: `if command; then`
- Commands with `||` or `&&`: `command || true`
- Commands in pipelines (without -o pipefail)

#### -u (nounset)

Exits if an undefined variable is referenced:

```bash
#!/bin/bash
set -u

echo "$UNDEFINED_VAR"  # Script exits with error
```

**Common issue:**
```bash
# ❌ Fails with set -u if variable is empty
if [ -z "$OPTIONAL_VAR" ]; then
    echo "Variable is empty"
fi

# ✅ Use parameter expansion
if [ -z "${OPTIONAL_VAR:-}" ]; then
    echo "Variable is empty"
fi
```

#### -o pipefail

Returns exit code of rightmost failed command in pipeline:

```bash
#!/bin/bash
set -o pipefail

# Without pipefail: exit code is from 'wc' (0), even if grep fails
grep "pattern" file.txt | wc -l

# With pipefail: exit code is from 'grep' if it fails
```

### When to Use set -euo pipefail

**✅ Use for:**
- Production automation scripts
- CI/CD build scripts
- Deployment scripts
- Scripts where partial execution is dangerous
- Cron jobs and scheduled tasks

**❌ Do NOT use for:**
- Interactive scripts where user can recover
- Scripts that intentionally handle failures
- Scripts using commands that may fail normally (e.g., grep returning no matches)

### Alternative: set -Eeuo pipefail

```bash
#!/bin/bash
set -Eeuo pipefail

# -E: ERR trap is inherited by functions and command substitutions
```

Enables more comprehensive error handling with trap:

```bash
#!/bin/bash
set -Eeuo pipefail

error_handler() {
    local line=$1
    echo "Error on line $line" >&2
    exit 1
}

trap 'error_handler $LINENO' ERR

# Error will trigger trap with line number
false
```

---

## Explicit Exit Code Checking

### Basic Pattern

```bash
#!/bin/bash

if ! command_that_might_fail; then
    echo "Error: Command failed" >&2
    exit 1
fi
```

### Capturing and Checking Exit Codes

```bash
#!/bin/bash

command_that_might_fail
exit_code=$?

if [ "$exit_code" -ne 0 ]; then
    echo "Error: Command failed with exit code $exit_code" >&2
    exit 1
fi
```

### Different Handling per Exit Code

```bash
#!/bin/bash

curl -sSL https://example.com/api
exit_code=$?

case "$exit_code" in
    0)
        echo "Success"
        ;;
    6)
        echo "Error: Could not resolve host" >&2
        exit 1
        ;;
    7)
        echo "Error: Failed to connect" >&2
        exit 1
        ;;
    22)
        echo "Error: HTTP error (4xx/5xx)" >&2
        exit 1
        ;;
    *)
        echo "Error: curl failed with exit code $exit_code" >&2
        exit 1
        ;;
esac
```

### Conditional Execution with Exit Codes

```bash
#!/bin/bash

# Execute command2 only if command1 succeeds
command1 && command2

# Execute command2 only if command1 fails
command1 || command2

# Chain multiple commands (all must succeed)
command1 && command2 && command3

# Fallback pattern
command_that_might_fail || {
    echo "Error: Command failed, attempting recovery" >&2
    recovery_command
}
```

### Ignoring Expected Failures

```bash
#!/bin/bash
set -e

# Explicitly ignore failure (when failure is acceptable)
grep "pattern" file.txt || true

# Or disable -e temporarily
set +e
command_that_may_fail
exit_code=$?
set -e

if [ "$exit_code" -ne 0 ]; then
    # Handle failure
    echo "Command failed (expected)" >&2
fi
```

---

## Trap Handlers for Cleanup

### Basic Cleanup Pattern

```bash
#!/bin/bash
set -euo pipefail

# Create temporary file
TEMP_FILE=$(mktemp)

# Cleanup function
cleanup() {
    echo "Cleaning up..." >&2
    rm -f "$TEMP_FILE"
}

# Register cleanup on EXIT
trap cleanup EXIT

# Script logic
echo "data" > "$TEMP_FILE"
# Cleanup runs automatically on exit (success or failure)
```

### Preserving Exit Code in Cleanup

```bash
#!/bin/bash
set -euo pipefail

cleanup() {
    local exit_code=$?
    echo "Cleaning up..." >&2
    rm -f "$TEMP_FILE"
    # Exit with original exit code
    exit "$exit_code"
}

trap cleanup EXIT
```

### Multiple Trap Signals

```bash
#!/bin/bash

cleanup() {
    echo "Cleanup triggered by: $1" >&2
    rm -f "$LOCK_FILE"
}

# Trap multiple signals
trap 'cleanup EXIT' EXIT
trap 'cleanup SIGINT' INT
trap 'cleanup SIGTERM' TERM
```

### Advanced: Error Handler with Line Number

```bash
#!/bin/bash
set -Eeuo pipefail

error_handler() {
    local line=$1
    local command=$2
    echo "Error on line $line: $command" >&2
    cleanup
    exit 1
}

cleanup() {
    echo "Performing cleanup..." >&2
    rm -f "$TEMP_FILE"
}

trap 'error_handler $LINENO "$BASH_COMMAND"' ERR
trap cleanup EXIT

# Script logic
TEMP_FILE=$(mktemp)
false  # Triggers error handler with line number
```

### Nested Trap Handlers

```bash
#!/bin/bash
set -euo pipefail

# Global cleanup
global_cleanup() {
    echo "Global cleanup" >&2
    rm -f /tmp/global_resource
}

trap global_cleanup EXIT

# Function-specific cleanup
process_file() {
    local temp_file=$(mktemp)

    # Local cleanup
    local_cleanup() {
        echo "Local cleanup" >&2
        rm -f "$temp_file"
    }

    trap local_cleanup RETURN

    # Process file
    echo "Processing..." > "$temp_file"
}

process_file
# Local cleanup runs when function returns
# Global cleanup runs when script exits
```

---

## Defensive Programming Patterns

### Check Required Commands

```bash
#!/bin/bash

# Method 1: Using command -v
command -v jq >/dev/null 2>&1 || {
    echo "Error: jq is required but not installed" >&2
    exit 1
}

# Method 2: Using type
type jq >/dev/null 2>&1 || {
    echo "Error: jq is required but not installed" >&2
    exit 1
}

# Method 3: Using which (less portable)
which jq >/dev/null 2>&1 || {
    echo "Error: jq is required but not installed" >&2
    exit 1
}
```

**Preferred:** `command -v` (most portable, POSIX-compliant)

### Check Required Environment Variables

```bash
#!/bin/bash

# Method 1: Parameter expansion with error
: "${API_KEY:?Error: API_KEY environment variable is required}"

# Method 2: Explicit check
if [ -z "${API_KEY:-}" ]; then
    echo "Error: API_KEY environment variable is required" >&2
    exit 1
fi

# Method 3: Check multiple variables
for var in API_KEY API_SECRET DATABASE_URL; do
    if [ -z "${!var:-}" ]; then
        echo "Error: $var environment variable is required" >&2
        exit 1
    fi
done
```

### Check File Existence and Permissions

```bash
#!/bin/bash

CONFIG_FILE="config.yaml"

# Check file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE" >&2
    exit 1
fi

# Check file is readable
if [ ! -r "$CONFIG_FILE" ]; then
    echo "Error: Cannot read config file: $CONFIG_FILE" >&2
    exit 1
fi

# Check file is writable
if [ ! -w "$CONFIG_FILE" ]; then
    echo "Error: Cannot write to config file: $CONFIG_FILE" >&2
    exit 1
fi

# Check directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Data directory not found: $DATA_DIR" >&2
    exit 1
fi
```

### Validate Input Arguments

```bash
#!/bin/bash

validate_input() {
    local input=$1

    # Check not empty
    if [ -z "$input" ]; then
        echo "Error: Input cannot be empty" >&2
        return 1
    fi

    # Check format (e.g., email)
    if ! echo "$input" | grep -qE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'; then
        echo "Error: Invalid email format: $input" >&2
        return 1
    fi

    return 0
}

# Usage
if ! validate_input "$USER_EMAIL"; then
    exit 1
fi
```

### Defensive Variable Quoting

```bash
#!/bin/bash

# ❌ BAD: Unquoted variables (word splitting, glob expansion)
echo $file
cp $source $dest
for item in $list; do

# ✅ GOOD: Quoted variables
echo "$file"
cp "$source" "$dest"
for item in "$list"; do

# ❌ BAD: Unquoted command substitution
files=$(ls *.txt)
for file in $files; do

# ✅ GOOD: Use array (Bash)
files=(*.txt)
for file in "${files[@]}"; do
```

---

## Error Reporting Best Practices

### Structured Logging

```bash
#!/bin/bash

# Logging functions
log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*" >&2
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
}

log_warning() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $*" >&2
}

# Usage
log_info "Starting script"
log_error "Failed to connect to database"
log_warning "Retrying in 5 seconds"
```

### Error Messages to stderr

```bash
#!/bin/bash

# ❌ BAD: Error to stdout
echo "Error: Something went wrong"

# ✅ GOOD: Error to stderr
echo "Error: Something went wrong" >&2

# ✅ GOOD: Using printf
printf "Error: %s\n" "Something went wrong" >&2
```

### Contextual Error Messages

```bash
#!/bin/bash

# ❌ BAD: Generic error
echo "Error: Command failed" >&2

# ✅ GOOD: Contextual error
echo "Error: Failed to download file from https://example.com/data.json" >&2
echo "Error: Database connection failed (host: $DB_HOST, port: $DB_PORT)" >&2
echo "Error: Invalid configuration in $CONFIG_FILE at line $line_number" >&2
```

### Notification on Critical Errors

```bash
#!/bin/bash

notify_error() {
    local message=$1

    # Log to syslog
    logger -t "$SCRIPT_NAME" -p user.err "$message"

    # Send email (if configured)
    if [ -n "${ADMIN_EMAIL:-}" ]; then
        echo "$message" | mail -s "[$HOSTNAME] Script Error" "$ADMIN_EMAIL"
    fi

    # Send to Slack (if webhook configured)
    if [ -n "${SLACK_WEBHOOK:-}" ]; then
        curl -X POST "$SLACK_WEBHOOK" \
            -H 'Content-Type: application/json' \
            -d "{\"text\": \"$message\"}"
    fi
}

# Usage
critical_operation || {
    notify_error "Critical operation failed on $HOSTNAME"
    exit 1
}
```

---

## Common Error Scenarios

### Network Requests

```bash
#!/bin/bash
set -euo pipefail

# Download with retry
download_with_retry() {
    local url=$1
    local output=$2
    local max_attempts=3
    local attempt=1

    while [ "$attempt" -le "$max_attempts" ]; do
        echo "Attempt $attempt of $max_attempts..." >&2

        if curl -sSL -o "$output" "$url"; then
            echo "Download successful" >&2
            return 0
        fi

        echo "Download failed, retrying in 5 seconds..." >&2
        sleep 5
        attempt=$((attempt + 1))
    done

    echo "Error: Failed to download after $max_attempts attempts" >&2
    return 1
}

# Usage
download_with_retry "https://example.com/data.json" "data.json" || exit 1
```

### File Operations

```bash
#!/bin/bash
set -euo pipefail

# Safe file operations with error handling
safe_copy() {
    local source=$1
    local dest=$2

    # Check source exists
    if [ ! -f "$source" ]; then
        echo "Error: Source file not found: $source" >&2
        return 1
    fi

    # Check destination directory exists
    local dest_dir=$(dirname "$dest")
    if [ ! -d "$dest_dir" ]; then
        echo "Error: Destination directory not found: $dest_dir" >&2
        return 1
    fi

    # Perform copy with error handling
    if ! cp "$source" "$dest"; then
        echo "Error: Failed to copy $source to $dest" >&2
        return 1
    fi

    echo "Successfully copied $source to $dest" >&2
    return 0
}

# Usage
safe_copy "source.txt" "destination.txt" || exit 1
```

### Command Execution

```bash
#!/bin/bash
set -euo pipefail

# Execute command with timeout
execute_with_timeout() {
    local timeout=$1
    shift
    local command=("$@")

    # Run command with timeout
    if ! timeout "$timeout" "${command[@]}"; then
        local exit_code=$?

        if [ "$exit_code" -eq 124 ]; then
            echo "Error: Command timed out after ${timeout}s: ${command[*]}" >&2
        else
            echo "Error: Command failed with exit code $exit_code: ${command[*]}" >&2
        fi

        return 1
    fi

    return 0
}

# Usage
execute_with_timeout 30 curl -sSL https://example.com/api || exit 1
```

### Process Management

```bash
#!/bin/bash
set -euo pipefail

# Start background process with PID tracking
start_background_process() {
    local command=$1
    local pid_file=$2

    # Start process in background
    $command &
    local pid=$!

    # Save PID
    echo "$pid" > "$pid_file"

    # Wait briefly and check if process is running
    sleep 1
    if ! kill -0 "$pid" 2>/dev/null; then
        echo "Error: Background process failed to start" >&2
        rm -f "$pid_file"
        return 1
    fi

    echo "Started background process with PID $pid" >&2
    return 0
}

# Stop background process
stop_background_process() {
    local pid_file=$1

    if [ ! -f "$pid_file" ]; then
        echo "Error: PID file not found: $pid_file" >&2
        return 1
    fi

    local pid=$(cat "$pid_file")

    if kill -0 "$pid" 2>/dev/null; then
        echo "Stopping process $pid..." >&2
        kill "$pid"

        # Wait for graceful shutdown
        local timeout=10
        while [ "$timeout" -gt 0 ] && kill -0 "$pid" 2>/dev/null; do
            sleep 1
            timeout=$((timeout - 1))
        done

        # Force kill if still running
        if kill -0 "$pid" 2>/dev/null; then
            echo "Force killing process $pid..." >&2
            kill -9 "$pid"
        fi
    fi

    rm -f "$pid_file"
    return 0
}
```

---

## Summary

**Key Principles:**
1. Use `set -euo pipefail` for production scripts
2. Always check exit codes of critical commands explicitly
3. Use trap handlers for guaranteed cleanup
4. Perform defensive checks early (commands, variables, files)
5. Report errors to stderr with context
6. Quote all variables and command substitutions

**Anti-Patterns to Avoid:**
- Ignoring exit codes
- Using unquoted variables
- Missing cleanup handlers
- Generic error messages
- Errors to stdout instead of stderr
