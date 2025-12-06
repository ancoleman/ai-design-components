#!/bin/bash
#
# Basic getopts Example
#
# Demonstrates simple argument parsing using getopts (POSIX-compliant).
# Supports short options: -h, -v, -f FILE, -o OUTPUT

set -euo pipefail

#============================================================================
# Usage
#============================================================================

usage() {
    cat <<EOF
Usage: $(basename "$0") [-h] [-v] [-f FILE] [-o OUTPUT]

Basic getopts example for parsing command-line arguments.

Options:
    -h          Show this help message
    -v          Enable verbose mode
    -f FILE     Input file (required)
    -o OUTPUT   Output file (optional, default: stdout)

Examples:
    # Basic usage
    $(basename "$0") -f input.txt

    # With output file
    $(basename "$0") -f input.txt -o output.txt

    # Verbose mode
    $(basename "$0") -v -f input.txt

    # Option bundling (combine -v and -f)
    $(basename "$0") -vf input.txt
EOF
    exit "${1:-0}"
}

#============================================================================
# Main Script
#============================================================================

# Default values
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""

# Parse options
while getopts "hvf:o:" opt; do
    case "$opt" in
        h)
            usage 0
            ;;
        v)
            VERBOSE=true
            ;;
        f)
            INPUT_FILE="$OPTARG"
            ;;
        o)
            OUTPUT_FILE="$OPTARG"
            ;;
        \?)
            echo "Error: Invalid option -$OPTARG" >&2
            usage 1
            ;;
        :)
            echo "Error: Option -$OPTARG requires an argument" >&2
            usage 1
            ;;
    esac
done

# Shift past parsed options
shift $((OPTIND - 1))

# Validate required arguments
if [ -z "$INPUT_FILE" ]; then
    echo "Error: -f FILE is required" >&2
    usage 1
fi

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
    echo "  Verbose: $VERBOSE"
    echo
fi

# Process file
echo "Processing file: $INPUT_FILE"

if [ -n "$OUTPUT_FILE" ]; then
    # Write to output file
    cat "$INPUT_FILE" > "$OUTPUT_FILE"
    echo "Output written to: $OUTPUT_FILE"
else
    # Write to stdout
    cat "$INPUT_FILE"
fi

echo "Processing complete"
