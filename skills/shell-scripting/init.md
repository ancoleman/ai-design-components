# Shell Scripting Skill - Master Plan

**Skill Name:** `shell-scripting`
**Skill Level:** Low Level (2,000-5,000 tokens, 300-500 lines init.md)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Shell Scripting Taxonomy](#shell-scripting-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Error Handling Patterns](#error-handling-patterns)
7. [Argument Parsing Patterns](#argument-parsing-patterns)
8. [Parameter Expansion and String Manipulation](#parameter-expansion-and-string-manipulation)
9. [Common Utilities Integration](#common-utilities-integration)
10. [Testing and Validation](#testing-and-validation)
11. [Tool Recommendations](#tool-recommendations)
12. [Skill Structure Design](#skill-structure-design)
13. [Integration Points](#integration-points)
14. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Shell Scripting Matters in 2025

Despite the rise of Python, Go, and other scripting languages, **shell scripting remains indispensable** for system administration, CI/CD pipelines, and automation tasks.

**Key Value Propositions:**

1. **Universal Availability:** Shell is guaranteed to be present on every Unix-like system
2. **Zero Dependencies:** No need to install interpreters, libraries, or runtime environments
3. **System Integration:** Direct access to OS utilities and system commands
4. **Startup Speed:** Instant execution without compilation or runtime initialization
5. **Pipeline Efficiency:** Native support for command composition and data streams

**2025 Use Cases:**

- **CI/CD Pipelines:** GitHub Actions, GitLab CI, Jenkins build scripts
- **Container Entrypoints:** Docker ENTRYPOINT and startup scripts
- **System Administration:** Cron jobs, log rotation, backup scripts
- **Development Tooling:** Build scripts, test runners, deployment automation
- **Infrastructure as Code:** Terraform/Pulumi wrapper scripts, cloud-init

### How This Differs from Related Skills

**This Skill Covers:**
- Writing robust bash/sh scripts with proper error handling
- Portable scripting practices (POSIX sh vs Bash)
- Argument parsing and parameter expansion
- Integration with common utilities (jq, yq, awk, sed)
- Testing and linting shell scripts

**NOT Covered (See Other Skills):**
- **Linux Administration:** System management, service configuration (see `linux-administration`)
- **CI/CD Pipelines:** GitHub Actions, GitLab CI YAML (see `building-ci-pipelines`)
- **Configuration Management:** Ansible, Puppet, Chef (see `configuration-management`)

**Complementary Relationship:**
```
Shell Scripting → Write maintainable automation scripts
Linux Administration → Understand what you're automating
Building CI Pipelines → Use scripts in automated workflows
```

### Target Audience

**Primary Users:**
- DevOps engineers automating infrastructure tasks
- Backend developers writing build and deployment scripts
- Site Reliability Engineers (SREs) creating runbooks
- Platform engineers building internal tooling

**Skill Level Assumptions:**
- Familiar with command line basics
- Understands pipes, redirection, and exit codes
- Needs guidance on error handling, argument parsing, and best practices
- May not know portability concerns (sh vs bash)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Error Handling and Defensive Scripting**
   - Using `set -euo pipefail` for fail-fast behavior
   - Checking command exit codes explicitly
   - Trap handlers for cleanup on exit/error
   - Defensive programming patterns

2. **Argument Parsing**
   - Using `getopts` for short options (-h, -v, -f FILE)
   - Manual parsing for long options (--help, --verbose)
   - Positional argument handling
   - Required vs optional arguments

3. **Functions and Modularity**
   - Function declaration and scoping
   - Returning values from functions
   - Creating reusable script libraries
   - Function naming conventions

4. **Parameter Expansion and String Manipulation**
   - Variable expansion patterns (${var:-default})
   - Substring extraction and replacement
   - Array handling in Bash
   - String comparison and pattern matching

5. **Portable Scripting (POSIX sh vs Bash)**
   - POSIX-compliant patterns for maximum portability
   - Bash-specific features and when to use them
   - Cross-platform considerations (Linux vs macOS)
   - Avoiding Bashisms when portability matters

6. **Common Utilities Integration**
   - JSON parsing with jq
   - YAML parsing with yq
   - Text processing with awk and sed
   - Process substitution patterns

7. **Testing and Validation**
   - Linting with ShellCheck
   - Testing with Bats (Bash Automated Testing System)
   - Continuous integration patterns
   - Debugging techniques

### What This Skill Does NOT Cover

- **Complex Application Logic:** Use Python, Go, or Ruby for complex logic
- **System Administration:** Covered in `linux-administration` skill
- **CI/CD Platform Specifics:** Covered in `building-ci-pipelines` skill
- **Security Hardening:** Covered in `security-hardening` skill

---

## Research Findings

### Research Methodology

**Research conducted:** December 3, 2025

**Tools Used:**
- Google Search Grounding (mcp__litellm__gs-google_search_grounding)
- Shell scripting best practices from 2025 sources

### Key Findings (2025)

#### 1. Error Handling Best Practices

**Fail-Fast with Set Options:**
```bash
#!/bin/bash
set -euo pipefail
# -e: Exit on error
# -u: Exit on undefined variable
# -o pipefail: Return exit code of failed pipe command
```

**Sources:**
- dev.to: Error handling patterns are now standard practice
- jsdev.space: Explicit exit code checking remains critical
- medium.com: Trap handlers for cleanup operations

**Key Insights:**
- `set -e` alone is insufficient; combine with `-u` and `-o pipefail`
- Always check exit codes of critical commands explicitly
- Use trap handlers for cleanup (temporary files, locks)

#### 2. POSIX Portability (sh vs bash)

**POSIX Compliance for Maximum Portability:**

**Source:** Reddit, StackOverflow, Columbia.edu

**Guidelines:**
- Use `#!/bin/sh` for portable scripts (works on all Unix-like systems)
- Avoid Bashisms: `[[`, arrays, `local`, process substitution
- Use `test` or `[` instead of `[[` for conditionals
- Use `printf` instead of `echo` for consistent output
- Stick to POSIX command options (avoid GNU long options like `--long`)

**When to Use Bash:**
- Controlled environments (Docker containers with specific base images)
- Complex scripts where Bash features simplify logic significantly
- Arrays, associative arrays, advanced parameter expansion needed

**Portability Testing:**
- Test with `dash` (strict POSIX shell) to ensure compliance
- Use ShellCheck with `--shell=sh` to detect Bashisms

#### 3. Parameter Expansion Patterns

**Source:** dev.to, gnu.org, opensource.com

**Common Patterns:**
```bash
# Default values
${var:-default}        # Use default if var is unset or null
${var:=default}        # Assign default if var is unset or null

# Substring extraction
${var:offset:length}   # Extract substring

# Pattern replacement
${var/pattern/string}  # Replace first match
${var//pattern/string} # Replace all matches

# String length
${#var}                # Length of variable

# Array handling (Bash only)
${array[@]}            # All array elements
${#array[@]}           # Array length
```

### Research Gaps and Mitigation

**Limited 2025 Data on:**
- Bats testing framework (some Google Search queries failed)
- ShellCheck latest features (queries returned errors)

**Mitigation:**
- Bats remains the standard for Bash testing (GitHub: bats-core/bats-core)
- ShellCheck is mature and stable (GitHub: koalaman/shellcheck)
- Will document core patterns that remain consistent

---

## Shell Scripting Taxonomy

### Script Categories

#### 1. System Administration Scripts
**Purpose:** Automate system maintenance tasks
**Characteristics:**
- Run as cron jobs or systemd timers
- Require root/sudo privileges
- Handle system resources (disk, processes, logs)

**Examples:**
- Log rotation and cleanup
- Backup automation
- System health checks
- User account management

#### 2. Build and Deployment Scripts
**Purpose:** Automate software build and deployment
**Characteristics:**
- Run in CI/CD pipelines
- Handle artifacts, dependencies, deployment targets
- Integrate with build tools (npm, cargo, maven)

**Examples:**
- Pre-commit hooks
- Build orchestration
- Docker image building
- Application deployment

#### 3. Development Tooling Scripts
**Purpose:** Improve developer workflow
**Characteristics:**
- Run locally by developers
- Interactive or non-interactive
- Integrate with development tools

**Examples:**
- Project initialization scripts
- Test runners
- Code generators
- Environment setup

#### 4. Container Entrypoint Scripts
**Purpose:** Initialize containerized applications
**Characteristics:**
- Run as PID 1 in containers
- Handle signal propagation
- Configure application at startup

**Examples:**
- Environment variable processing
- Configuration file generation
- Health checks
- Graceful shutdown handling

---

## Decision Frameworks

### Framework 1: POSIX sh vs Bash

```
NEED MAXIMUM PORTABILITY?
├── YES → Use POSIX sh (#!/bin/sh)
│   ✅ Works on all Unix-like systems (Linux, macOS, BSD)
│   ✅ Minimal container images (Alpine, Distroless)
│   ✅ Embedded systems
│   ❌ No arrays, no [[ ]], no process substitution
│   ❌ More verbose
│
└── NO → Use Bash (#!/bin/bash)
    ✅ Arrays and associative arrays
    ✅ [[ ]] for safer conditionals
    ✅ Advanced parameter expansion
    ✅ Process substitution <(cmd)
    ❌ Must ensure Bash is installed

PORTABILITY CHECKLIST:
- Runs on Linux AND macOS? → POSIX sh
- Runs in minimal containers (Alpine)? → POSIX sh
- Only runs in controlled environment? → Bash OK
- Complex data structures needed? → Consider Python
```

### Framework 2: When to Use Shell vs Other Languages

```
USE SHELL WHEN:
✅ Orchestrating existing commands
✅ Simple text processing (grep, sed, awk)
✅ File system operations
✅ Pipeline-heavy workflows
✅ System administration tasks

USE PYTHON/GO/RUBY WHEN:
❌ Complex business logic
❌ Error handling needs structured exceptions
❌ Data structures (maps, trees, graphs)
❌ API integration (REST, gRPC)
❌ Cross-platform GUI needed

DECISION THRESHOLD:
- Script < 100 lines, mostly commands → Shell
- Script > 200 lines, complex logic → Python/Go
- Script 100-200 lines → Evaluate complexity
```

### Framework 3: Error Handling Strategy

```
SCRIPT TYPE?

├── PRODUCTION AUTOMATION
│   ✅ set -euo pipefail (fail fast)
│   ✅ Trap handlers for cleanup
│   ✅ Explicit exit code checking for critical commands
│   ✅ Structured logging with timestamps
│   ✅ Email/Slack notifications on failure
│
├── INTERACTIVE TOOL
│   ⚠️  set -e may be too aggressive
│   ✅ Explicit error checking with user-friendly messages
│   ✅ Prompt for retry on recoverable errors
│   ✅ --dry-run flag for safety
│
└── BUILD SCRIPT (CI/CD)
    ✅ set -euo pipefail (fail fast for CI)
    ✅ Verbose output (set -x for debugging)
    ✅ Exit codes for CI failure detection
    ✅ Artifacts preserved on failure
```

---

## Error Handling Patterns

### Pattern 1: Fail-Fast with Set Options

```bash
#!/bin/bash
set -euo pipefail

# -e: Exit immediately if any command exits with non-zero status
# -u: Exit if undefined variable is used
# -o pipefail: Pipeline fails if any command in pipeline fails

# Example: This will exit immediately on curl failure
curl -sSL https://example.com/data.json | jq '.items'
```

**When to Use:**
- Production automation scripts
- CI/CD build scripts
- Scripts where partial execution is dangerous

**When NOT to Use:**
- Interactive scripts where user can recover from errors
- Scripts that intentionally use commands that may fail

### Pattern 2: Explicit Exit Code Checking

```bash
#!/bin/bash

# Check exit code explicitly
if ! command_that_might_fail; then
    echo "Error: Command failed" >&2
    exit 1
fi

# Or capture exit code
command_that_might_fail
exit_code=$?
if [ "$exit_code" -ne 0 ]; then
    echo "Error: Command failed with exit code $exit_code" >&2
    exit 1
fi
```

**When to Use:**
- When you need custom error messages
- When different exit codes require different handling
- When `set -e` is not used (interactive scripts)

### Pattern 3: Trap Handlers for Cleanup

```bash
#!/bin/bash
set -euo pipefail

# Temporary file
TEMP_FILE=$(mktemp)

# Cleanup function
cleanup() {
    local exit_code=$?
    echo "Cleaning up..."
    rm -f "$TEMP_FILE"
    exit "$exit_code"
}

# Register cleanup on EXIT
trap cleanup EXIT

# Script logic
echo "Processing..." > "$TEMP_FILE"
# If script fails here, cleanup() still runs
```

**When to Use:**
- Scripts creating temporary files
- Scripts acquiring locks or resources
- Scripts needing guaranteed cleanup

### Pattern 4: Defensive Checks

```bash
#!/bin/bash
set -euo pipefail

# Check required commands exist
command -v jq >/dev/null 2>&1 || {
    echo "Error: jq is required but not installed" >&2
    exit 1
}

# Check required environment variables
: "${API_KEY:?Error: API_KEY environment variable is required}"

# Check file exists before processing
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE" >&2
    exit 1
fi
```

**When to Use:**
- All production scripts (defensive programming)
- Scripts with external dependencies
- Scripts requiring specific environment

---

## Argument Parsing Patterns

### Pattern 1: getopts for Short Options

```bash
#!/bin/bash

usage() {
    cat <<EOF
Usage: $0 [-h] [-v] [-f FILE] [-o OUTPUT]

Options:
    -h          Show this help message
    -v          Enable verbose mode
    -f FILE     Input file (required)
    -o OUTPUT   Output file (default: stdout)
EOF
    exit 1
}

# Defaults
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""

# Parse options
while getopts "hvf:o:" opt; do
    case "$opt" in
        h) usage ;;
        v) VERBOSE=true ;;
        f) INPUT_FILE="$OPTARG" ;;
        o) OUTPUT_FILE="$OPTARG" ;;
        *) usage ;;
    esac
done

# Shift past parsed options
shift $((OPTIND - 1))

# Check required arguments
if [ -z "$INPUT_FILE" ]; then
    echo "Error: -f FILE is required" >&2
    usage
fi

# Remaining positional arguments in "$@"
```

**Advantages:**
- POSIX-compliant
- Handles option bundling (-vf file.txt)
- Standard pattern, widely recognized

**Limitations:**
- Short options only (-f, not --file)
- No automatic help generation

### Pattern 2: Manual Parsing for Long Options

```bash
#!/bin/bash

usage() {
    cat <<EOF
Usage: $0 [OPTIONS] [ARGS]

Options:
    --help              Show this help message
    --verbose           Enable verbose mode
    --file FILE         Input file (required)
    --output OUTPUT     Output file
    --dry-run           Show what would be done
EOF
    exit 1
}

# Defaults
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""
DRY_RUN=false

# Parse long options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            usage
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --file)
            INPUT_FILE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            usage
            ;;
        *)
            # Positional argument
            break
            ;;
    esac
done

# Check required arguments
if [ -z "$INPUT_FILE" ]; then
    echo "Error: --file is required" >&2
    usage
fi
```

**Advantages:**
- Supports long options (--file, --verbose)
- Clear and readable
- Easy to extend

**Limitations:**
- Not POSIX-compliant (uses `[[` and `[[ $# -gt 0 ]]`)
- Manual parsing is more verbose

### Pattern 3: Hybrid (Short + Long Options)

```bash
#!/bin/bash

# Support both -f and --file
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--file)
            INPUT_FILE="$2"
            shift 2
            ;;
        *)
            break
            ;;
    esac
done
```

---

## Parameter Expansion and String Manipulation

### Common Parameter Expansion Patterns

```bash
#!/bin/bash

# Default values
FILE="${1:-default.txt}"           # Use default.txt if $1 is unset
PORT="${PORT:-8080}"                # Use 8080 if PORT is unset

# Required variables (error if unset)
: "${API_KEY:?Error: API_KEY is required}"

# Assign default if unset
: "${CONFIG_DIR:=/etc/myapp}"

# String length
name="Alice"
echo "${#name}"  # Output: 5

# Substring extraction
path="/usr/local/bin/myapp"
echo "${path:0:4}"     # Output: /usr
echo "${path:5}"       # Output: local/bin/myapp

# Remove prefix/suffix
filename="report.csv.gz"
echo "${filename%.gz}"       # Output: report.csv (remove shortest suffix)
echo "${filename%%.*}"       # Output: report (remove longest suffix)
echo "${filename#*.}"        # Output: csv.gz (remove shortest prefix)
echo "${filename##*.}"       # Output: gz (remove longest prefix)

# Pattern replacement
text="hello world world"
echo "${text/world/universe}"   # Output: hello universe world (first)
echo "${text//world/universe}"  # Output: hello universe universe (all)

# Case conversion (Bash 4+)
name="Alice"
echo "${name^^}"  # Output: ALICE (uppercase)
echo "${name,,}"  # Output: alice (lowercase)
```

### Array Handling (Bash Only)

```bash
#!/bin/bash

# Declare array
files=("file1.txt" "file2.txt" "file3.txt")

# Access elements
echo "${files[0]}"      # First element
echo "${files[@]}"      # All elements
echo "${#files[@]}"     # Array length

# Iterate over array
for file in "${files[@]}"; do
    echo "Processing: $file"
done

# Associative arrays (Bash 4+)
declare -A config
config[host]="localhost"
config[port]="8080"

echo "${config[host]}"  # Output: localhost

# Iterate over associative array
for key in "${!config[@]}"; do
    echo "$key = ${config[$key]}"
done
```

---

## Common Utilities Integration

### JSON Parsing with jq

```bash
#!/bin/bash

# Parse JSON from API
response=$(curl -sSL https://api.example.com/users)

# Extract field
name=$(echo "$response" | jq -r '.name')

# Extract array elements
ids=$(echo "$response" | jq -r '.users[].id')

# Filter and transform
active_users=$(echo "$response" | jq -r '.users[] | select(.active == true) | .name')

# Check jq exit code
if ! echo "$response" | jq -e '.success' >/dev/null; then
    echo "Error: API request failed" >&2
    exit 1
fi
```

### YAML Parsing with yq

```bash
#!/bin/bash

# Parse YAML config
config_file="config.yaml"

# Extract field (yq v4 syntax, mimics jq)
database=$(yq eval '.database.host' "$config_file")

# Update YAML in place
yq eval '.database.port = 5432' -i "$config_file"

# Convert YAML to JSON
yq eval -o=json "$config_file" > config.json
```

### Text Processing with awk

```bash
#!/bin/bash

# Extract column from CSV
awk -F',' '{print $2}' data.csv

# Sum column values
total=$(awk '{sum += $1} END {print sum}' numbers.txt)

# Filter rows
awk '$3 > 100' data.txt  # Print rows where 3rd column > 100
```

### Pattern Matching with sed

```bash
#!/bin/bash

# Replace text in file
sed 's/old/new/g' file.txt

# In-place editing
sed -i 's/old/new/g' file.txt  # Linux
sed -i '' 's/old/new/g' file.txt  # macOS (note empty string after -i)

# Delete lines
sed '/pattern/d' file.txt  # Delete lines matching pattern
```

---

## Testing and Validation

### ShellCheck: Static Analysis

**Purpose:** Detect bugs, portability issues, and bad practices

**Installation:**
```bash
# macOS
brew install shellcheck

# Ubuntu/Debian
apt-get install shellcheck

# Docker
docker run --rm -v "$PWD:/mnt" koalaman/shellcheck:stable script.sh
```

**Usage:**
```bash
# Check script
shellcheck script.sh

# Check for POSIX compliance
shellcheck --shell=sh script.sh

# Exclude specific warnings
shellcheck --exclude=SC2086 script.sh
```

**Common Warnings:**
- SC2086: Quote variables to prevent word splitting
- SC2046: Quote command substitution to prevent word splitting
- SC2004: Arithmetic expansion doesn't need $ on variables

### Bats: Bash Automated Testing System

**Purpose:** Write automated tests for shell scripts

**Installation:**
```bash
# macOS
brew install bats-core

# Git submodule
git submodule add https://github.com/bats-core/bats-core.git test/bats
```

**Example Test:**
```bash
# test/example.bats
#!/usr/bin/env bats

@test "addition using bc" {
    result="$(echo 2+2 | bc)"
    [ "$result" -eq 4 ]
}

@test "script runs successfully" {
    run ./script.sh --help
    [ "$status" -eq 0 ]
    [ "${lines[0]}" = "Usage: script.sh [OPTIONS]" ]
}

@test "script fails on missing argument" {
    run ./script.sh
    [ "$status" -eq 1 ]
    [[ "$output" =~ "Error" ]]
}
```

**Running Tests:**
```bash
# Run all tests
bats test/

# Run specific test file
bats test/example.bats

# Verbose output
bats --tap test/
```

---

## Tool Recommendations

### Core Shell Tools (Always Available)

**POSIX Shell (sh):**
- Guaranteed on all Unix-like systems
- Minimal footprint
- Use for maximum portability

**Bash:**
- Default on most Linux distributions
- Rich feature set (arrays, parameter expansion)
- Use in controlled environments

### Essential Utilities

**jq** (JSON processor)
- **Purpose:** Parse and transform JSON
- **Installation:** `brew install jq` (macOS), `apt-get install jq` (Ubuntu)
- **Use Case:** API responses, config files

**yq** (YAML processor)
- **Purpose:** Parse and transform YAML
- **Installation:** `brew install yq` (macOS)
- **Use Case:** Kubernetes manifests, CI/CD configs

**ShellCheck** (linter)
- **Purpose:** Static analysis for shell scripts
- **Installation:** `brew install shellcheck` (macOS)
- **Use Case:** CI/CD linting, pre-commit hooks

**Bats** (testing framework)
- **Purpose:** Automated testing for shell scripts
- **Installation:** `brew install bats-core` (macOS)
- **Use Case:** Test-driven development, CI/CD

### Platform-Specific Considerations

**macOS vs Linux Differences:**
- `sed -i`: macOS requires empty string (`sed -i ''`), Linux doesn't
- `readlink`: macOS doesn't support `-f` flag (use `greadlink` from coreutils)
- `date`: Different flags for date arithmetic
- `grep`: macOS has BSD grep (use `ggrep` for GNU grep features)

**Mitigation:**
- Use POSIX-compliant patterns where possible
- Detect platform and adjust: `if [[ "$OSTYPE" == "darwin"* ]]; then`
- Use Docker/containers for consistent environment

---

## Skill Structure Design

### Progressive Disclosure Architecture

**Tier 1: SKILL.md (Core Guidance)**
- When to use shell scripts vs other languages
- Essential error handling patterns
- Argument parsing decision tree
- Quick reference for common patterns
- Links to detailed references

**Tier 2: Reference Files**
- `references/error-handling.md`: Comprehensive error handling patterns
- `references/argument-parsing.md`: Detailed parsing examples
- `references/parameter-expansion.md`: All expansion patterns
- `references/portability-guide.md`: POSIX vs Bash differences
- `references/testing-guide.md`: ShellCheck and Bats usage

**Tier 3: Scripts and Examples**
- `scripts/template.sh`: Production-ready script template
- `scripts/shellcheck-wrapper.sh`: CI/CD integration helper
- `examples/getopts-example.sh`: Argument parsing examples
- `examples/error-handling-example.sh`: Error handling examples

### File Structure

```
shell-scripting/
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── error-handling.md             # Comprehensive error patterns
│   ├── argument-parsing.md           # Parsing techniques
│   ├── parameter-expansion.md        # All expansion patterns
│   ├── portability-guide.md          # POSIX vs Bash
│   ├── testing-guide.md              # ShellCheck + Bats
│   └── common-utilities.md           # jq, yq, awk, sed
├── examples/
│   ├── production-template.sh        # Complete script template
│   ├── getopts-basic.sh              # Simple getopts usage
│   ├── getopts-advanced.sh           # Complex option handling
│   ├── long-options.sh               # Manual long option parsing
│   ├── error-handling.sh             # Error handling patterns
│   └── json-yaml-processing.sh       # jq/yq examples
├── scripts/
│   ├── lint-script.sh                # ShellCheck wrapper for CI
│   └── test-script.sh                # Bats wrapper for CI
└── assets/
    └── decision-trees.md             # Visual decision frameworks
```

---

## Integration Points

### Upstream Dependencies

**Skills that feed into shell-scripting:**

1. **`linux-administration`**
   - System commands and utilities
   - File system operations
   - Process management

2. **`building-ci-pipelines`**
   - CI/CD context for script usage
   - Pipeline-specific patterns

### Downstream Consumers

**Skills that use shell-scripting:**

1. **`building-ci-pipelines`**
   - Build scripts in GitHub Actions, GitLab CI
   - Pre-commit hooks
   - Deployment automation

2. **`infrastructure-as-code`**
   - Terraform/Pulumi wrapper scripts
   - Cloud-init scripts
   - Bootstrap scripts

3. **`kubernetes-operations`**
   - Kubectl wrapper scripts
   - Helm hooks
   - Init containers

4. **`linux-administration`**
   - Cron jobs
   - System maintenance scripts
   - Log processing

### Cross-Skill Patterns

**Shell scripting as glue:**
```
Configuration Management → Shell Scripts → System Commands
Infrastructure as Code → Shell Scripts → Cloud APIs
CI/CD Pipelines → Shell Scripts → Build Tools
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**SKILL.md Core Content:**
- [ ] Overview and when to use shell scripting
- [ ] Decision framework: sh vs bash vs other languages
- [ ] Essential error handling patterns (set -euo pipefail)
- [ ] Basic argument parsing (getopts)
- [ ] Quick reference for common patterns

**Deliverable:** SKILL.md under 500 lines with progressive disclosure

### Phase 2: Reference Documentation (Week 1-2)

**Create Reference Files:**
- [ ] `references/error-handling.md`: All error handling patterns
- [ ] `references/argument-parsing.md`: getopts and manual parsing
- [ ] `references/parameter-expansion.md`: Complete expansion guide
- [ ] `references/portability-guide.md`: POSIX vs Bash
- [ ] `references/testing-guide.md`: ShellCheck and Bats

**Deliverable:** Comprehensive references linked from SKILL.md

### Phase 3: Examples and Scripts (Week 2)

**Create Practical Examples:**
- [ ] `examples/production-template.sh`: Complete script template
- [ ] `examples/getopts-basic.sh`: Simple option parsing
- [ ] `examples/error-handling.sh`: Error patterns in action
- [ ] `examples/json-yaml-processing.sh`: jq/yq integration
- [ ] `scripts/lint-script.sh`: ShellCheck CI wrapper
- [ ] `scripts/test-script.sh`: Bats CI wrapper

**Deliverable:** Working examples for common use cases

### Phase 4: Testing and Validation (Week 3)

**Quality Assurance:**
- [ ] All examples pass ShellCheck
- [ ] Bats tests for example scripts
- [ ] Cross-platform testing (Linux + macOS)
- [ ] CI/CD integration example (GitHub Actions)

**Deliverable:** Battle-tested, production-ready skill

### Phase 5: Integration and Documentation (Week 3-4)

**Integration:**
- [ ] Cross-reference with `building-ci-pipelines` skill
- [ ] Cross-reference with `linux-administration` skill
- [ ] Add to skill discovery index
- [ ] Update CHANGELOG.md

**Deliverable:** Integrated skill ready for use

---

## Key Takeaways

### Critical Success Factors

1. **Error Handling is Non-Negotiable**
   - Always use `set -euo pipefail` for automation scripts
   - Explicit exit code checking for critical commands
   - Trap handlers for cleanup operations

2. **Portability Matters**
   - POSIX sh for maximum portability
   - Bash for controlled environments where features justify it
   - Test on target platforms (Linux, macOS, Alpine)

3. **Argument Parsing Clarity**
   - Use `getopts` for POSIX compliance (short options)
   - Manual parsing for long options (requires bash/[[]])
   - Always provide `--help` and usage examples

4. **Testing and Linting are Essential**
   - ShellCheck catches 90% of common bugs
   - Bats enables test-driven development
   - CI/CD integration prevents broken scripts

5. **Know When NOT to Use Shell**
   - Complex business logic → Python/Go
   - Cross-platform GUI → Not shell's strength
   - Heavy data processing → Use proper programming language

### Anti-Patterns to Avoid

❌ **Don't:**
- Use shell for complex logic (>200 lines without structure)
- Ignore exit codes or errors
- Use unquoted variables (`$var` instead of `"$var"`)
- Assume Bash is available (if portability matters)
- Skip ShellCheck (it catches real bugs)

✅ **Do:**
- Keep scripts focused and modular
- Use functions for reusability
- Quote all variables and command substitutions
- Test on target platforms
- Lint with ShellCheck and test with Bats

---

## Appendix: Quick Reference

### Common Pitfalls

```bash
# ❌ BAD: Unquoted variable (word splitting)
for file in $FILES; do

# ✅ GOOD: Quoted variable
for file in "$FILES"; do

# ❌ BAD: Unquoted command substitution
files=$(ls *.txt)

# ✅ GOOD: Use arrays in Bash or proper quoting
files=(*.txt)

# ❌ BAD: Using [ ] with && or ||
if [ "$x" -gt 0 ] && [ "$y" -lt 10 ]; then

# ✅ GOOD: Use [[ ]] in Bash (or separate if statements in POSIX)
if [[ "$x" -gt 0 && "$y" -lt 10 ]]; then

# ❌ BAD: Parsing ls output
for file in $(ls *.txt); do

# ✅ GOOD: Use glob directly
for file in *.txt; do
```

### Must-Know Commands

```bash
# Check if command exists
command -v jq >/dev/null 2>&1

# Get script directory (POSIX)
script_dir="$(cd "$(dirname "$0")" && pwd)"

# Get script directory (Bash)
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read file line by line
while IFS= read -r line; do
    echo "$line"
done < file.txt

# Create temporary file
temp_file=$(mktemp)
trap "rm -f '$temp_file'" EXIT
```

---

**End of Master Plan**

This init.md provides the foundation for implementing the `shell-scripting` skill. The next phase is to create SKILL.md following Anthropic's progressive disclosure patterns and the structure outlined in this document.
