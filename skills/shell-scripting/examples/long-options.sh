#!/bin/bash
#
# Long Options Example
#
# Demonstrates manual parsing of long options (--help, --file, etc.)
# Supports both --option value and --option=value formats

set -euo pipefail

#============================================================================
# Usage
#============================================================================

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Long options example demonstrating manual argument parsing.

Options:
    --help              Show this help message
    --verbose           Enable verbose mode
    --file FILE         Input file (required)
    --output FILE       Output file (optional)
    --format FORMAT     Output format: text|json|yaml (default: text)
    --dry-run           Show what would be done without executing

Both formats are supported:
    --file input.txt    (space-separated)
    --file=input.txt    (equals sign)

Examples:
    # Basic usage
    $(basename "$0") --file input.txt

    # With equals sign
    $(basename "$0") --file=input.txt --output=output.txt

    # With format specification
    $(basename "$0") --file input.json --format json

    # Dry run mode
    $(basename "$0") --file input.txt --dry-run
EOF
    exit "${1:-0}"
}

#============================================================================
# Main Script
#============================================================================

# Default values
VERBOSE=false
DRY_RUN=false
INPUT_FILE=""
OUTPUT_FILE=""
FORMAT="text"

# Parse long options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            usage 0
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --file)
            if [ -z "${2:-}" ]; then
                echo "Error: --file requires an argument" >&2
                usage 1
            fi
            INPUT_FILE="$2"
            shift 2
            ;;
        --file=*)
            INPUT_FILE="${1#*=}"
            shift
            ;;
        --output)
            if [ -z "${2:-}" ]; then
                echo "Error: --output requires an argument" >&2
                usage 1
            fi
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --output=*)
            OUTPUT_FILE="${1#*=}"
            shift
            ;;
        --format)
            if [ -z "${2:-}" ]; then
                echo "Error: --format requires an argument" >&2
                usage 1
            fi
            FORMAT="$2"
            shift 2
            ;;
        --format=*)
            FORMAT="${1#*=}"
            shift
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            usage 1
            ;;
        *)
            # Positional argument
            echo "Error: Unexpected positional argument: $1" >&2
            usage 1
            ;;
    esac
done

# Validate required arguments
if [ -z "$INPUT_FILE" ]; then
    echo "Error: --file is required" >&2
    usage 1
fi

# Validate format
case "$FORMAT" in
    text|json|yaml)
        ;;
    *)
        echo "Error: Invalid format: $FORMAT (must be text, json, or yaml)" >&2
        usage 1
        ;;
esac

# Check input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file not found: $INPUT_FILE" >&2
    exit 1
fi

# Display configuration
if [ "$VERBOSE" = "true" ]; then
    echo "Configuration:"
    echo "  Input file: $INPUT_FILE"
    echo "  Output file: ${OUTPUT_FILE:-stdout}"
    echo "  Format: $FORMAT"
    echo "  Dry run: $DRY_RUN"
    echo
fi

# Process file
echo "Processing file: $INPUT_FILE"

if [ "$DRY_RUN" = "true" ]; then
    echo "[DRY RUN] Would process $INPUT_FILE with format $FORMAT"
    if [ -n "$OUTPUT_FILE" ]; then
        echo "[DRY RUN] Would write output to: $OUTPUT_FILE"
    fi
else
    # Actual processing
    if [ -n "$OUTPUT_FILE" ]; then
        cat "$INPUT_FILE" > "$OUTPUT_FILE"
        echo "Output written to: $OUTPUT_FILE"
    else
        cat "$INPUT_FILE"
    fi
fi

echo "Processing complete"
