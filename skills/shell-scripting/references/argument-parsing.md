# Argument Parsing in Shell Scripts

Comprehensive guide to parsing command-line arguments in shell scripts, covering getopts, manual parsing, and hybrid approaches.

## Table of Contents

- [getopts for Short Options](#getopts-for-short-options)
- [Manual Parsing for Long Options](#manual-parsing-for-long-options)
- [Hybrid Approach (Short + Long)](#hybrid-approach-short--long)
- [Positional Arguments](#positional-arguments)
- [Required vs Optional Arguments](#required-vs-optional-arguments)
- [Validation Patterns](#validation-patterns)
- [Usage Documentation](#usage-documentation)

---

## getopts for Short Options

### Basic Pattern

```bash
#!/bin/bash

usage() {
    cat <<EOF
Usage: $0 [-h] [-v] [-f FILE]

Options:
    -h          Show this help message
    -v          Enable verbose mode
    -f FILE     Input file (required)
EOF
    exit 1
}

# Default values
VERBOSE=false
INPUT_FILE=""

# Parse options
while getopts "hvf:" opt; do
    case "$opt" in
        h) usage ;;
        v) VERBOSE=true ;;
        f) INPUT_FILE="$OPTARG" ;;
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
echo "Input file: $INPUT_FILE"
echo "Remaining args: $*"
```

### Option Types

```bash
#!/bin/bash

# Option string: "ab:c::"
# a   - Boolean flag (no argument)
# b:  - Required argument
# c:: - Optional argument (non-POSIX, Bash only)

while getopts "ab:c::" opt; do
    case "$opt" in
        a)
            FLAG_A=true
            ;;
        b)
            VALUE_B="$OPTARG"
            ;;
        c)
            VALUE_C="${OPTARG:-default}"
            ;;
        *)
            usage
            ;;
    esac
done
```

### Option Bundling

getopts supports option bundling (-abc equivalent to -a -b -c):

```bash
#!/bin/bash

# Parse bundled options
while getopts "vdf:" opt; do
    case "$opt" in
        v) VERBOSE=true ;;
        d) DEBUG=true ;;
        f) FILE="$OPTARG" ;;
        *) usage ;;
    esac
done

# All of these work:
# ./script.sh -v -d -f file.txt
# ./script.sh -vd -f file.txt
# ./script.sh -vdf file.txt
```

### Multiple Values for Same Option

```bash
#!/bin/bash

# Collect multiple values in array
FILES=()

while getopts "f:" opt; do
    case "$opt" in
        f)
            FILES+=("$OPTARG")
            ;;
        *)
            usage
            ;;
    esac
done

# Usage: ./script.sh -f file1.txt -f file2.txt -f file3.txt
echo "Files: ${FILES[@]}"
```

### Error Handling in getopts

```bash
#!/bin/bash

# Silent error reporting (handle errors manually)
while getopts ":hvf:" opt; do
    case "$opt" in
        h) usage ;;
        v) VERBOSE=true ;;
        f) INPUT_FILE="$OPTARG" ;;
        \?)
            echo "Error: Invalid option -$OPTARG" >&2
            usage
            ;;
        :)
            echo "Error: Option -$OPTARG requires an argument" >&2
            usage
            ;;
    esac
done

# Note: Leading ':' in ":hvf:" enables silent error reporting
```

---

## Manual Parsing for Long Options

### Basic Pattern

```bash
#!/bin/bash

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Options:
    --help              Show this help
    --verbose           Enable verbose mode
    --file FILE         Input file (required)
    --output OUTPUT     Output file (optional)
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

# Check required
if [ -z "$INPUT_FILE" ]; then
    echo "Error: --file is required" >&2
    usage
fi
```

### With Equals Sign (--file=value)

```bash
#!/bin/bash

while [[ $# -gt 0 ]]; do
    case "$1" in
        --file=*)
            INPUT_FILE="${1#*=}"
            shift
            ;;
        --file)
            INPUT_FILE="$2"
            shift 2
            ;;
        --output=*)
            OUTPUT_FILE="${1#*=}"
            shift
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        *)
            break
            ;;
    esac
done

# Supports both:
# ./script.sh --file=input.txt --output=output.txt
# ./script.sh --file input.txt --output output.txt
```

### Error Handling for Long Options

```bash
#!/bin/bash

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --file)
                if [ -z "${2:-}" ]; then
                    echo "Error: --file requires an argument" >&2
                    return 1
                fi
                INPUT_FILE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            -*)
                echo "Error: Unknown option: $1" >&2
                return 1
                ;;
            *)
                # Positional argument
                POSITIONAL_ARGS+=("$1")
                shift
                ;;
        esac
    done
    return 0
}

# Usage
if ! parse_arguments "$@"; then
    usage
fi
```

---

## Hybrid Approach (Short + Long)

### Supporting Both Short and Long Options

```bash
#!/bin/bash

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Options:
    -h, --help              Show this help
    -v, --verbose           Enable verbose mode
    -f, --file FILE         Input file (required)
    -o, --output OUTPUT     Output file
    -d, --dry-run           Show what would be done
EOF
    exit 1
}

# Defaults
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""
DRY_RUN=false

# Parse options
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
        --file=*)
            INPUT_FILE="${1#*=}"
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --output=*)
            OUTPUT_FILE="${1#*=}"
            shift
            ;;
        -d|--dry-run)
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

# Check required
if [ -z "$INPUT_FILE" ]; then
    echo "Error: --file is required" >&2
    usage
fi
```

### Using getopt (GNU Enhanced Version)

**Note:** GNU getopt is not POSIX, not available on all systems (especially macOS).

```bash
#!/bin/bash

# Parse options with GNU getopt
PARSED=$(getopt -o hvf:o: --long help,verbose,file:,output: -n "$0" -- "$@")
eval set -- "$PARSED"

# Defaults
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""

# Process options
while true; do
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
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Error: Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Remaining arguments in "$@"
```

**Portability Warning:** GNU getopt is not available on BSD/macOS by default. Use manual parsing for portability.

---

## Positional Arguments

### Basic Positional Arguments

```bash
#!/bin/bash

# Access positional arguments
FIRST_ARG="$1"
SECOND_ARG="$2"
THIRD_ARG="$3"

# All arguments as array
ALL_ARGS=("$@")

# Number of arguments
ARG_COUNT=$#

echo "First: $FIRST_ARG"
echo "Second: $SECOND_ARG"
echo "Count: $ARG_COUNT"
```

### After Option Parsing

```bash
#!/bin/bash

# Parse options first
while getopts "v" opt; do
    case "$opt" in
        v) VERBOSE=true ;;
        *) usage ;;
    esac
done

# Shift past options
shift $((OPTIND - 1))

# Now "$@" contains only positional arguments
if [ $# -lt 1 ]; then
    echo "Error: At least one positional argument required" >&2
    usage
fi

COMMAND="$1"
shift

# Remaining arguments
ARGS=("$@")

echo "Command: $COMMAND"
echo "Args: ${ARGS[@]}"
```

### Variable Number of Positional Arguments

```bash
#!/bin/bash

# Accept variable number of files
FILES=("$@")

if [ ${#FILES[@]} -eq 0 ]; then
    echo "Error: At least one file required" >&2
    exit 1
fi

for file in "${FILES[@]}"; do
    echo "Processing: $file"
done
```

### Subcommand Pattern

```bash
#!/bin/bash

usage() {
    cat <<EOF
Usage: $0 <command> [options]

Commands:
    start       Start the service
    stop        Stop the service
    restart     Restart the service
    status      Show service status
EOF
    exit 1
}

# Check for command
if [ $# -lt 1 ]; then
    echo "Error: Command required" >&2
    usage
fi

COMMAND="$1"
shift

# Process subcommand
case "$COMMAND" in
    start)
        # Parse start-specific options
        while getopts "p:" opt; do
            case "$opt" in
                p) PORT="$OPTARG" ;;
                *) usage ;;
            esac
        done
        echo "Starting service on port ${PORT:-8080}"
        ;;
    stop)
        echo "Stopping service"
        ;;
    restart)
        echo "Restarting service"
        ;;
    status)
        echo "Service status"
        ;;
    *)
        echo "Error: Unknown command: $COMMAND" >&2
        usage
        ;;
esac
```

---

## Required vs Optional Arguments

### Validation Pattern

```bash
#!/bin/bash

# Parse options
while getopts "f:o:v" opt; do
    case "$opt" in
        f) INPUT_FILE="$OPTARG" ;;
        o) OUTPUT_FILE="$OPTARG" ;;
        v) VERBOSE=true ;;
        *) usage ;;
    esac
done

shift $((OPTIND - 1))

# Check required options
MISSING=()

if [ -z "${INPUT_FILE:-}" ]; then
    MISSING+=("-f FILE")
fi

if [ -z "${OUTPUT_FILE:-}" ]; then
    MISSING+=("-o OUTPUT")
fi

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Error: Missing required options: ${MISSING[*]}" >&2
    usage
fi
```

### Default Values for Optional Arguments

```bash
#!/bin/bash

# Parse with defaults
while getopts "f:o:p:" opt; do
    case "$opt" in
        f) INPUT_FILE="$OPTARG" ;;
        o) OUTPUT_FILE="$OPTARG" ;;
        p) PORT="$OPTARG" ;;
        *) usage ;;
    esac
done

# Apply defaults for optional arguments
: "${OUTPUT_FILE:=output.txt}"
: "${PORT:=8080}"

# Check required (no default)
if [ -z "${INPUT_FILE:-}" ]; then
    echo "Error: -f FILE is required" >&2
    usage
fi

echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE (default: output.txt)"
echo "Port: $PORT (default: 8080)"
```

### Environment Variables as Defaults

```bash
#!/bin/bash

# Parse options
while getopts "k:h:" opt; do
    case "$opt" in
        k) API_KEY="$OPTARG" ;;
        h) API_HOST="$OPTARG" ;;
        *) usage ;;
    esac
done

# Use environment variables as defaults
: "${API_KEY:=${API_KEY_ENV}}"
: "${API_HOST:=${API_HOST_ENV:-https://api.example.com}}"

# Check required
if [ -z "${API_KEY:-}" ]; then
    echo "Error: API key required (use -k or set API_KEY_ENV)" >&2
    usage
fi

echo "Using API host: $API_HOST"
```

---

## Validation Patterns

### Type Validation

```bash
#!/bin/bash

# Validate integer
validate_integer() {
    local value=$1
    local name=$2

    if ! [[ "$value" =~ ^[0-9]+$ ]]; then
        echo "Error: $name must be an integer: $value" >&2
        return 1
    fi
    return 0
}

# Validate range
validate_range() {
    local value=$1
    local min=$2
    local max=$3
    local name=$4

    if [ "$value" -lt "$min" ] || [ "$value" -gt "$max" ]; then
        echo "Error: $name must be between $min and $max: $value" >&2
        return 1
    fi
    return 0
}

# Parse and validate
while getopts "p:" opt; do
    case "$opt" in
        p)
            PORT="$OPTARG"
            validate_integer "$PORT" "port" || exit 1
            validate_range "$PORT" 1 65535 "port" || exit 1
            ;;
        *) usage ;;
    esac
done
```

### File Validation

```bash
#!/bin/bash

# Validate file exists and is readable
validate_input_file() {
    local file=$1

    if [ ! -f "$file" ]; then
        echo "Error: File not found: $file" >&2
        return 1
    fi

    if [ ! -r "$file" ]; then
        echo "Error: File not readable: $file" >&2
        return 1
    fi

    return 0
}

# Validate output path
validate_output_path() {
    local file=$1
    local dir=$(dirname "$file")

    if [ ! -d "$dir" ]; then
        echo "Error: Output directory does not exist: $dir" >&2
        return 1
    fi

    if [ ! -w "$dir" ]; then
        echo "Error: Output directory not writable: $dir" >&2
        return 1
    fi

    return 0
}

# Parse and validate
while getopts "f:o:" opt; do
    case "$opt" in
        f)
            INPUT_FILE="$OPTARG"
            validate_input_file "$INPUT_FILE" || exit 1
            ;;
        o)
            OUTPUT_FILE="$OPTARG"
            validate_output_path "$OUTPUT_FILE" || exit 1
            ;;
        *) usage ;;
    esac
done
```

### Format Validation

```bash
#!/bin/bash

# Validate email format
validate_email() {
    local email=$1

    if ! echo "$email" | grep -qE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'; then
        echo "Error: Invalid email format: $email" >&2
        return 1
    fi
    return 0
}

# Validate URL format
validate_url() {
    local url=$1

    if ! echo "$url" | grep -qE '^https?://[A-Za-z0-9.-]+'; then
        echo "Error: Invalid URL format: $url" >&2
        return 1
    fi
    return 0
}

# Parse and validate
while getopts "e:u:" opt; do
    case "$opt" in
        e)
            EMAIL="$OPTARG"
            validate_email "$EMAIL" || exit 1
            ;;
        u)
            URL="$OPTARG"
            validate_url "$URL" || exit 1
            ;;
        *) usage ;;
    esac
done
```

---

## Usage Documentation

### Comprehensive Help Message

```bash
#!/bin/bash

usage() {
    cat <<EOF
$(basename "$0") - Process data files

Usage:
    $(basename "$0") [OPTIONS] [FILES...]

Description:
    Process one or more data files with optional transformations.

Options:
    -h, --help              Show this help message
    -v, --verbose           Enable verbose output
    -f, --file FILE         Input file (required)
    -o, --output FILE       Output file (default: stdout)
    -t, --type TYPE         Processing type: json|yaml|csv (default: json)
    -d, --dry-run           Show what would be done without executing

Examples:
    # Process single file
    $(basename "$0") --file input.json --output output.json

    # Process with type specification
    $(basename "$0") -f data.csv -t csv -o results.csv

    # Dry run to preview changes
    $(basename "$0") --file input.yaml --dry-run

    # Verbose mode for debugging
    $(basename "$0") -v -f input.json

Environment Variables:
    API_KEY                 API key for authentication (optional)
    LOG_LEVEL              Logging level: debug|info|warn|error (default: info)

Exit Codes:
    0                      Success
    1                      General error
    2                      Invalid arguments
    3                      File not found

For more information, see: https://example.com/docs
EOF
    exit "${1:-0}"
}
```

### Auto-Generated Help from Comments

```bash
#!/bin/bash

# USAGE: script.sh [OPTIONS]
# DESCRIPTION: Process data files with transformations
# OPTIONS:
#   -h, --help      Show help
#   -f, --file      Input file (required)
#   -o, --output    Output file (optional)

usage() {
    # Extract usage from comments
    grep "^# " "$0" | sed 's/^# //'
    exit 0
}

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) usage ;;
        # ... other options
    esac
done
```

### Version Information

```bash
#!/bin/bash

VERSION="1.2.3"

show_version() {
    cat <<EOF
$(basename "$0") version $VERSION
Copyright (C) 2025 Your Organization
License: MIT
EOF
    exit 0
}

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
    -h, --help      Show help
    -V, --version   Show version
    # ... other options
EOF
    exit 0
}

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) usage ;;
        -V|--version) show_version ;;
        # ... other options
    esac
done
```

---

## Summary

**Best Practices:**
1. Use getopts for POSIX-compliant short options
2. Use manual parsing for long options (requires Bash)
3. Support both short and long options for user convenience
4. Always provide --help with examples
5. Validate arguments early before processing
6. Provide clear error messages for invalid input
7. Use defaults for optional arguments
8. Document environment variable alternatives

**Anti-Patterns to Avoid:**
- Relying on GNU getopt (not portable)
- Missing validation for required arguments
- Poor error messages ("Invalid argument")
- No help/usage documentation
- Modifying "$@" before option parsing
