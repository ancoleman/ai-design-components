#!/bin/bash
#
# Advanced getopts Example
#
# Demonstrates advanced argument parsing with validation, multiple files,
# and comprehensive error handling.

set -euo pipefail

#============================================================================
# Logging
#============================================================================

log_info() {
    echo "[INFO] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_debug() {
    if [ "$VERBOSE" = "true" ]; then
        echo "[DEBUG] $*" >&2
    fi
}

#============================================================================
# Usage
#============================================================================

usage() {
    cat <<EOF
Usage: $(basename "$0") [-h] [-v] [-d] [-f FILE]... [-o OUTPUT] [-t TYPE] [FILES...]

Advanced getopts example with multiple options and validation.

Options:
    -h          Show this help message
    -v          Enable verbose mode
    -d          Enable dry-run mode
    -f FILE     Input file (can be specified multiple times)
    -o OUTPUT   Output directory (default: current directory)
    -t TYPE     Processing type: text|json|yaml (default: text)

Positional Arguments:
    FILES       Additional input files

Examples:
    # Single file
    $(basename "$0") -f input.txt

    # Multiple files using -f
    $(basename "$0") -f file1.txt -f file2.txt -f file3.txt

    # Multiple files using positional arguments
    $(basename "$0") file1.txt file2.txt file3.txt

    # Mixed -f options and positional arguments
    $(basename "$0") -f file1.txt file2.txt file3.txt

    # With output directory and type
    $(basename "$0") -f input.json -o output/ -t json

    # Dry run mode
    $(basename "$0") -d -f input.txt
EOF
    exit "${1:-0}"
}

#============================================================================
# Validation
#============================================================================

validate_type() {
    local type=$1

    case "$type" in
        text|json|yaml)
            return 0
            ;;
        *)
            log_error "Invalid type: $type (must be text, json, or yaml)"
            return 1
            ;;
    esac
}

validate_file() {
    local file=$1

    if [ ! -f "$file" ]; then
        log_error "File not found: $file"
        return 1
    fi

    if [ ! -r "$file" ]; then
        log_error "File not readable: $file"
        return 1
    fi

    return 0
}

validate_output_dir() {
    local dir=$1

    if [ ! -d "$dir" ]; then
        log_error "Output directory does not exist: $dir"
        return 1
    fi

    if [ ! -w "$dir" ]; then
        log_error "Output directory not writable: $dir"
        return 1
    fi

    return 0
}

#============================================================================
# Processing
#============================================================================

process_file() {
    local file=$1
    local type=$2
    local output_dir=$3

    log_info "Processing $file (type: $type)"

    if [ "$DRY_RUN" = "true" ]; then
        log_info "[DRY RUN] Would process: $file"
        return 0
    fi

    # Actual processing logic here
    local output_file="$output_dir/$(basename "$file")"

    log_debug "Input: $file"
    log_debug "Output: $output_file"

    # Example: Copy file to output directory
    cp "$file" "$output_file"

    log_info "Processed: $file -> $output_file"
}

#============================================================================
# Main Script
#============================================================================

# Default values
VERBOSE=false
DRY_RUN=false
OUTPUT_DIR="."
PROCESS_TYPE="text"
INPUT_FILES=()

# Parse options
while getopts "hvdf:o:t:" opt; do
    case "$opt" in
        h)
            usage 0
            ;;
        v)
            VERBOSE=true
            ;;
        d)
            DRY_RUN=true
            ;;
        f)
            INPUT_FILES+=("$OPTARG")
            ;;
        o)
            OUTPUT_DIR="$OPTARG"
            ;;
        t)
            PROCESS_TYPE="$OPTARG"
            ;;
        \?)
            log_error "Invalid option -$OPTARG"
            usage 1
            ;;
        :)
            log_error "Option -$OPTARG requires an argument"
            usage 1
            ;;
    esac
done

# Shift past parsed options
shift $((OPTIND - 1))

# Add positional arguments to input files
for arg in "$@"; do
    INPUT_FILES+=("$arg")
done

# Validate configuration
if ! validate_type "$PROCESS_TYPE"; then
    usage 1
fi

if ! validate_output_dir "$OUTPUT_DIR"; then
    exit 1
fi

# Check we have at least one input file
if [ ${#INPUT_FILES[@]} -eq 0 ]; then
    log_error "No input files specified"
    usage 1
fi

# Display configuration
log_debug "Configuration:"
log_debug "  Input files: ${INPUT_FILES[*]}"
log_debug "  Output directory: $OUTPUT_DIR"
log_debug "  Processing type: $PROCESS_TYPE"
log_debug "  Verbose: $VERBOSE"
log_debug "  Dry run: $DRY_RUN"
log_debug ""

# Validate all input files
for file in "${INPUT_FILES[@]}"; do
    if ! validate_file "$file"; then
        exit 1
    fi
done

# Process each file
processed_count=0
failed_count=0

for file in "${INPUT_FILES[@]}"; do
    if process_file "$file" "$PROCESS_TYPE" "$OUTPUT_DIR"; then
        ((processed_count++))
    else
        ((failed_count++))
        log_error "Failed to process: $file"
    fi
done

# Summary
log_info "Processing complete:"
log_info "  Processed: $processed_count"
log_info "  Failed: $failed_count"

if [ "$failed_count" -gt 0 ]; then
    exit 1
fi

exit 0
