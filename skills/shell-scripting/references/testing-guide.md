# Testing and Linting Shell Scripts

Comprehensive guide to testing shell scripts with Bats and linting with ShellCheck.

## Table of Contents

- [ShellCheck: Static Analysis](#shellcheck-static-analysis)
- [Bats: Automated Testing](#bats-automated-testing)
- [Integration Testing](#integration-testing)
- [CI/CD Integration](#cicd-integration)
- [Debugging Techniques](#debugging-techniques)

---

## ShellCheck: Static Analysis

### Installation

```bash
# macOS
brew install shellcheck

# Ubuntu/Debian
apt-get install shellcheck

# Fedora/RHEL
dnf install ShellCheck

# Docker
docker pull koalaman/shellcheck:stable
```

### Basic Usage

```bash
# Check single script
shellcheck script.sh

# Check multiple scripts
shellcheck *.sh

# Check with specific shell
shellcheck --shell=sh script.sh     # POSIX sh
shellcheck --shell=bash script.sh   # Bash

# Output formats
shellcheck --format=gcc script.sh   # GCC-style
shellcheck --format=json script.sh  # JSON
shellcheck --format=tty script.sh   # Terminal (default)
```

### Common Warnings

#### SC2086: Quote variables to prevent word splitting

```bash
# ❌ Problematic
echo $var
cp $source $dest

# ✅ Fixed
echo "$var"
cp "$source" "$dest"
```

#### SC2006: Use $(...) instead of backticks

```bash
# ❌ Problematic
result=`command`

# ✅ Fixed
result=$(command)
```

#### SC2046: Quote command substitution

```bash
# ❌ Problematic
for file in $(ls *.txt); do

# ✅ Fixed
for file in *.txt; do
```

#### SC2039: POSIX sh doesn't support arrays

```bash
# ❌ Problematic (in #!/bin/sh)
#!/bin/sh
files=("file1" "file2")

# ✅ Fixed (use Bash)
#!/bin/bash
files=("file1" "file2")

# Or use POSIX alternative
#!/bin/sh
files="file1 file2"
```

#### SC2155: Declare and assign separately

```bash
# ❌ Problematic
local result=$(command)

# ✅ Fixed
local result
result=$(command)
```

### Excluding Warnings

```bash
# Exclude specific warning
shellcheck --exclude=SC2086 script.sh

# Exclude multiple warnings
shellcheck --exclude=SC2086,SC2046 script.sh

# In-file exclusion
#!/bin/bash
# shellcheck disable=SC2086
echo $var

# Disable for single line
echo $var  # shellcheck disable=line
```

### Severity Levels

```bash
# Show only errors
shellcheck --severity=error script.sh

# Show errors and warnings
shellcheck --severity=warning script.sh

# Show errors, warnings, and info
shellcheck --severity=info script.sh

# Show everything (including style)
shellcheck --severity=style script.sh
```

### CI Integration

```bash
# Exit with non-zero on any issue
shellcheck script.sh
if [ $? -ne 0 ]; then
    echo "ShellCheck failed"
    exit 1
fi

# Or use in CI pipeline
shellcheck *.sh || exit 1
```

### Docker Usage

```bash
# Run ShellCheck in container
docker run --rm -v "$PWD:/mnt" koalaman/shellcheck:stable script.sh

# Check all scripts
docker run --rm -v "$PWD:/mnt" koalaman/shellcheck:stable /mnt/*.sh

# With specific options
docker run --rm -v "$PWD:/mnt" koalaman/shellcheck:stable \
    --shell=sh --severity=error /mnt/script.sh
```

---

## Bats: Automated Testing

### Installation

```bash
# macOS
brew install bats-core

# Git submodule
git submodule add https://github.com/bats-core/bats-core.git test/bats
git submodule add https://github.com/bats-core/bats-support.git test/test_helper/bats-support
git submodule add https://github.com/bats-core/bats-assert.git test/test_helper/bats-assert

# npm
npm install -g bats
```

### Basic Test Structure

```bash
#!/usr/bin/env bats

# test/example.bats

@test "addition using bc" {
    result="$(echo 2+2 | bc)"
    [ "$result" -eq 4 ]
}

@test "script exists and is executable" {
    [ -f "script.sh" ]
    [ -x "script.sh" ]
}
```

### Running Tests

```bash
# Run all tests in directory
bats test/

# Run specific test file
bats test/example.bats

# Verbose output
bats --tap test/

# Count only
bats --count test/

# Pretty output (default)
bats --pretty test/
```

### Test Assertions

```bash
#!/usr/bin/env bats

@test "string comparison" {
    result="hello"
    [ "$result" = "hello" ]
}

@test "numeric comparison" {
    result=42
    [ "$result" -eq 42 ]
}

@test "file exists" {
    [ -f "README.md" ]
}

@test "directory exists" {
    [ -d "src/" ]
}

@test "command succeeds" {
    true
}

@test "command fails" {
    run false
    [ "$status" -ne 0 ]
}
```

### Using run Command

```bash
#!/usr/bin/env bats

@test "script runs successfully" {
    run ./script.sh --help

    # Check exit code
    [ "$status" -eq 0 ]

    # Check output (entire output)
    [ "$output" = "Usage: script.sh [OPTIONS]" ]

    # Check specific line
    [ "${lines[0]}" = "Usage: script.sh [OPTIONS]" ]
    [ "${lines[1]}" = "" ]
}

@test "script handles error" {
    run ./script.sh --invalid-option

    # Should fail
    [ "$status" -eq 1 ]

    # Should print error
    [[ "$output" =~ "Error" ]]
}
```

### Setup and Teardown

```bash
#!/usr/bin/env bats

setup() {
    # Run before each test
    export TEST_VAR="test_value"
    mkdir -p tmp/
}

teardown() {
    # Run after each test
    rm -rf tmp/
}

@test "uses setup variables" {
    [ "$TEST_VAR" = "test_value" ]
}

@test "uses setup directory" {
    [ -d "tmp/" ]
}
```

### setup_file and teardown_file

```bash
#!/usr/bin/env bats

setup_file() {
    # Run once before all tests in file
    export GLOBAL_VAR="global"
}

teardown_file() {
    # Run once after all tests in file
    unset GLOBAL_VAR
}

setup() {
    # Run before each test
    export TEST_VAR="test"
}

teardown() {
    # Run after each test
    unset TEST_VAR
}
```

### Skipping Tests

```bash
#!/usr/bin/env bats

@test "this test is skipped" {
    skip "Not implemented yet"
    # Test code here won't run
}

@test "conditional skip" {
    if [ ! -f "required_file.txt" ]; then
        skip "required_file.txt not found"
    fi

    # Test code
}
```

### Using bats-support and bats-assert

```bash
#!/usr/bin/env bats

load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

@test "assert_success" {
    run echo "hello"
    assert_success
}

@test "assert_failure" {
    run false
    assert_failure
}

@test "assert_output" {
    run echo "hello world"
    assert_output "hello world"
}

@test "assert_output with pattern" {
    run echo "hello world"
    assert_output --partial "world"
}

@test "assert_line" {
    run echo -e "line1\nline2\nline3"
    assert_line --index 0 "line1"
    assert_line --index 2 "line3"
}

@test "refute_output" {
    run echo ""
    refute_output
}
```

### Testing Functions

```bash
#!/usr/bin/env bats

# Load script being tested
load '../script.sh'

@test "function returns correct value" {
    run my_function "arg1" "arg2"

    assert_success
    assert_output "expected_result"
}

@test "function handles error" {
    run my_function "invalid_arg"

    assert_failure
    assert_output --partial "Error"
}
```

### Testing with Fixtures

```bash
#!/usr/bin/env bats

setup() {
    # Create fixture files
    mkdir -p test/fixtures
    echo "test data" > test/fixtures/input.txt
}

teardown() {
    # Clean up fixtures
    rm -rf test/fixtures
}

@test "processes fixture file" {
    run ./script.sh test/fixtures/input.txt

    assert_success
    assert_output "test data processed"
}
```

---

## Integration Testing

### Testing Complete Workflows

```bash
#!/usr/bin/env bats

@test "end-to-end workflow" {
    # Setup
    mkdir -p tmp/input tmp/output

    # Create input
    echo "data" > tmp/input/file.txt

    # Run script
    run ./script.sh --input tmp/input --output tmp/output

    # Verify exit code
    assert_success

    # Verify output file created
    [ -f tmp/output/file.txt ]

    # Verify output content
    result=$(cat tmp/output/file.txt)
    [ "$result" = "processed data" ]

    # Cleanup
    rm -rf tmp/
}
```

### Testing External Dependencies

```bash
#!/usr/bin/env bats

@test "requires jq" {
    # Skip if jq not installed
    if ! command -v jq >/dev/null 2>&1; then
        skip "jq not installed"
    fi

    run ./script.sh --format json

    assert_success
}

@test "handles missing dependency gracefully" {
    # Temporarily hide command
    PATH="/tmp/empty:$PATH" run ./script.sh

    assert_failure
    assert_output --partial "Error: jq required"
}
```

### Testing with Mock Data

```bash
#!/usr/bin/env bats

setup() {
    # Create mock API response
    export MOCK_API_RESPONSE='{"status": "success", "data": []}'

    # Mock curl command
    curl() {
        echo "$MOCK_API_RESPONSE"
    }
    export -f curl
}

@test "handles API response" {
    run ./script.sh --api-endpoint https://example.com/api

    assert_success
    assert_output --partial "success"
}
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Shell Script Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y shellcheck
          npm install -g bats

      - name: Run ShellCheck
        run: shellcheck *.sh

      - name: Run Bats tests
        run: bats test/
```

### GitLab CI

```yaml
shellcheck:
  image: koalaman/shellcheck-alpine:stable
  script:
    - shellcheck *.sh

bats:
  image: bats/bats:latest
  script:
    - bats test/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running ShellCheck..."
shellcheck *.sh || {
    echo "ShellCheck failed. Commit aborted."
    exit 1
}

echo "Running Bats tests..."
bats test/ || {
    echo "Tests failed. Commit aborted."
    exit 1
}

echo "All checks passed."
```

### Makefile for Testing

```makefile
.PHONY: test lint check

# Run all tests
test:
	bats test/

# Run ShellCheck
lint:
	shellcheck *.sh

# Run both
check: lint test

# Watch mode (requires entr)
watch:
	find . -name "*.sh" | entr make check
```

---

## Debugging Techniques

### Verbose Execution

```bash
#!/bin/bash

# Print each command before execution
set -x

# Your script logic
echo "Hello"

# Disable verbose mode
set +x
```

### Trace Execution

```bash
# Run script with trace
bash -x script.sh

# Or use set -x in script
#!/bin/bash
set -x  # Enable trace
# ... script logic
```

### Debug Output

```bash
#!/bin/bash

DEBUG=${DEBUG:-false}

debug() {
    if [ "$DEBUG" = "true" ]; then
        echo "[DEBUG] $*" >&2
    fi
}

# Usage
debug "Variable value: $var"
debug "About to execute command"

# Run with: DEBUG=true ./script.sh
```

### Dry Run Mode

```bash
#!/bin/bash

DRY_RUN=${DRY_RUN:-false}

execute() {
    if [ "$DRY_RUN" = "true" ]; then
        echo "[DRY RUN] Would execute: $*" >&2
    else
        "$@"
    fi
}

# Usage
execute rm -f /tmp/file.txt

# Run with: DRY_RUN=true ./script.sh
```

### Logging

```bash
#!/bin/bash

LOG_FILE=${LOG_FILE:-/tmp/script.log}

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE" >&2
}

log "Script started"
log "Processing file: $file"
log "Script completed"
```

### Interactive Debugging

```bash
#!/bin/bash

# Break into debugger
read -p "Press Enter to continue..." _

# Inspect variables
read -p "DEBUG: var=$var. Press Enter..." _
```

---

## Summary

**ShellCheck:**
- Static analysis for shell scripts
- Catches common bugs and portability issues
- Integrates easily into CI/CD
- Use `--shell=sh` for POSIX compliance

**Bats:**
- Automated testing framework for shell scripts
- Simple test syntax
- Good for integration tests
- Use with bats-support and bats-assert for better assertions

**CI/CD:**
- Run ShellCheck and Bats in pipelines
- Use Docker images for consistent environment
- Pre-commit hooks prevent broken code

**Debugging:**
- `set -x` for trace execution
- Debug functions for conditional output
- Dry run mode for safety
- Logging for production scripts

**Best Practices:**
- Write tests first (TDD)
- Test on target platforms
- Use ShellCheck in editor
- Run tests before commit
- Maintain test coverage
