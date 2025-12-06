#!/bin/bash
#
# Production Shell Script Template
#
# This template demonstrates best practices for production-ready shell scripts.
# Includes error handling, argument parsing, logging, and cleanup.

set -euo pipefail

#============================================================================
# Script Metadata
#============================================================================

readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
readonly VERSION="1.0.0"

#============================================================================
# Configuration
#============================================================================

# Defaults (can be overridden by command-line arguments or environment)
: "${LOG_LEVEL:=info}"
: "${DRY_RUN:=false}"
: "${VERBOSE:=false}"

#============================================================================
# Global Variables
#============================================================================

TEMP_DIR=""
EXIT_CODE=0

#============================================================================
# Cleanup Handler
#============================================================================

cleanup() {
    local exit_code=$?

    # Perform cleanup operations
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        log_debug "Removing temporary directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi

    # Additional cleanup operations
    # - Remove lock files
    # - Close connections
    # - Save state

    log_info "Cleanup completed"

    # Exit with original exit code
    exit "$exit_code"
}

# Register cleanup handler
trap cleanup EXIT
trap 'EXIT_CODE=$?; cleanup; exit $EXIT_CODE' INT TERM

#============================================================================
# Logging Functions
#============================================================================

log_debug() {
    if [ "$LOG_LEVEL" = "debug" ] || [ "$VERBOSE" = "true" ]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] [DEBUG] $*" >&2
    fi
}

log_info() {
    if [ "$LOG_LEVEL" = "debug" ] || [ "$LOG_LEVEL" = "info" ] || [ "$VERBOSE" = "true" ]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] $*" >&2
    fi
}

log_warning() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [WARNING] $*" >&2
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [ERROR] $*" >&2
}

#============================================================================
# Usage Documentation
#============================================================================

usage() {
    cat <<EOF
$SCRIPT_NAME - Production script template

Usage:
    $SCRIPT_NAME [OPTIONS] [ARGS]

Description:
    This script demonstrates production-ready patterns for shell scripting.

Options:
    -h, --help              Show this help message
    -v, --verbose           Enable verbose output
    -V, --version           Show version information
    -f, --file FILE         Input file (required)
    -o, --output FILE       Output file (default: stdout)
    -d, --dry-run           Show what would be done without executing
    --log-level LEVEL       Set log level: debug|info|warning|error (default: info)

Examples:
    # Basic usage
    $SCRIPT_NAME --file input.txt

    # With output file
    $SCRIPT_NAME -f input.txt -o output.txt

    # Dry run mode
    $SCRIPT_NAME --file input.txt --dry-run

    # Verbose mode with debug logging
    $SCRIPT_NAME -v --log-level debug --file input.txt

Environment Variables:
    LOG_LEVEL              Set default log level (default: info)
    DRY_RUN               Enable dry-run mode (default: false)
    VERBOSE               Enable verbose output (default: false)

Exit Codes:
    0                     Success
    1                     General error
    2                     Invalid arguments
    3                     Missing dependencies
    4                     File not found

EOF
    exit "${1:-0}"
}

show_version() {
    echo "$SCRIPT_NAME version $VERSION"
    exit 0
}

#============================================================================
# Dependency Checking
#============================================================================

check_dependencies() {
    local missing_deps=()

    # List required commands
    local required_commands=(
        # Add your required commands here
        # "jq"
        # "curl"
        # "git"
    )

    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            missing_deps+=("$cmd")
        fi
    done

    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install missing dependencies and try again"
        exit 3
    fi

    log_debug "All dependencies satisfied"
}

#============================================================================
# Argument Parsing
#============================================================================

parse_arguments() {
    # Initialize variables
    INPUT_FILE=""
    OUTPUT_FILE=""

    # Parse options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -V|--version)
                show_version
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
            --log-level)
                LOG_LEVEL="$2"
                shift 2
                ;;
            --log-level=*)
                LOG_LEVEL="${1#*=}"
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                usage 2
                ;;
            *)
                # Positional argument
                break
                ;;
        esac
    done

    # Validate required arguments
    if [ -z "$INPUT_FILE" ]; then
        log_error "Missing required argument: --file"
        usage 2
    fi

    # Validate log level
    case "$LOG_LEVEL" in
        debug|info|warning|error)
            ;;
        *)
            log_error "Invalid log level: $LOG_LEVEL"
            usage 2
            ;;
    esac
}

#============================================================================
# Validation Functions
#============================================================================

validate_input() {
    log_debug "Validating input parameters"

    # Check input file exists
    if [ ! -f "$INPUT_FILE" ]; then
        log_error "Input file not found: $INPUT_FILE"
        exit 4
    fi

    # Check input file is readable
    if [ ! -r "$INPUT_FILE" ]; then
        log_error "Input file not readable: $INPUT_FILE"
        exit 4
    fi

    # Validate output path
    if [ -n "$OUTPUT_FILE" ]; then
        local output_dir
        output_dir="$(dirname "$OUTPUT_FILE")"

        if [ ! -d "$output_dir" ]; then
            log_error "Output directory does not exist: $output_dir"
            exit 4
        fi

        if [ ! -w "$output_dir" ]; then
            log_error "Output directory not writable: $output_dir"
            exit 4
        fi
    fi

    log_debug "Input validation passed"
}

#============================================================================
# Core Functions
#============================================================================

execute_command() {
    local command=("$@")

    if [ "$DRY_RUN" = "true" ]; then
        log_info "[DRY RUN] Would execute: ${command[*]}"
        return 0
    fi

    log_debug "Executing: ${command[*]}"

    if "${command[@]}"; then
        log_debug "Command succeeded: ${command[*]}"
        return 0
    else
        local exit_code=$?
        log_error "Command failed (exit code $exit_code): ${command[*]}"
        return "$exit_code"
    fi
}

process_file() {
    local input_file=$1
    local output_file=${2:-}

    log_info "Processing file: $input_file"

    # Create temporary directory if needed
    if [ -z "$TEMP_DIR" ]; then
        TEMP_DIR=$(mktemp -d)
        log_debug "Created temporary directory: $TEMP_DIR"
    fi

    # Your processing logic here
    # Example: Read input, transform, write output

    if [ -n "$output_file" ]; then
        log_info "Writing output to: $output_file"
        # Write to output file
    else
        log_info "Writing output to stdout"
        # Write to stdout
    fi

    log_info "Processing completed successfully"
}

#============================================================================
# Main Function
#============================================================================

main() {
    log_info "Starting $SCRIPT_NAME v$VERSION"

    # Parse and validate arguments
    parse_arguments "$@"

    # Check dependencies
    check_dependencies

    # Validate input
    validate_input

    # Main processing logic
    process_file "$INPUT_FILE" "$OUTPUT_FILE"

    log_info "$SCRIPT_NAME completed successfully"
    exit 0
}

#============================================================================
# Script Entry Point
#============================================================================

main "$@"
