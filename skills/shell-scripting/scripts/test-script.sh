#!/bin/bash
#
# Bats Testing Wrapper for CI/CD
#
# Runs Bats tests with configurable options.
# Designed for CI/CD pipelines.

set -euo pipefail

#============================================================================
# Configuration
#============================================================================

readonly SCRIPT_NAME="$(basename "$0")"

# Default test directory
TEST_DIR="test"

# Output format
FORMAT="pretty"

# Verbose mode
VERBOSE=false

# Count only
COUNT_ONLY=false

# Filter tests
FILTER=""

# Number of parallel jobs
JOBS=1

#============================================================================
# Usage
#============================================================================

usage() {
    cat <<EOF
$SCRIPT_NAME - Bats testing wrapper for CI/CD

Usage:
    $SCRIPT_NAME [OPTIONS] [TEST_FILES...]

Options:
    -h, --help              Show this help message
    -d, --dir DIR           Test directory (default: test/)
    -f, --format FORMAT     Output format: pretty|tap|junit (default: pretty)
    -v, --verbose           Verbose output
    -c, --count             Count tests only
    --filter PATTERN        Run only tests matching pattern
    -j, --jobs N            Number of parallel jobs (default: 1)

Arguments:
    TEST_FILES              Specific test files to run (default: all in test dir)

Examples:
    # Run all tests
    $SCRIPT_NAME

    # Run specific test file
    $SCRIPT_NAME test/example.bats

    # Run with TAP output
    $SCRIPT_NAME --format tap

    # Count tests
    $SCRIPT_NAME --count

    # Run tests matching pattern
    $SCRIPT_NAME --filter "argument parsing"

    # Run tests in parallel
    $SCRIPT_NAME --jobs 4
EOF
    exit "${1:-0}"
}

#============================================================================
# Logging
#============================================================================

log_info() {
    echo "[INFO] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

#============================================================================
# Argument Parsing
#============================================================================

parse_arguments() {
    TEST_FILES=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage 0
                ;;
            -d|--dir)
                TEST_DIR="$2"
                shift 2
                ;;
            -f|--format)
                FORMAT="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -c|--count)
                COUNT_ONLY=true
                shift
                ;;
            --filter)
                FILTER="$2"
                shift 2
                ;;
            -j|--jobs)
                JOBS="$2"
                shift 2
                ;;
            -*)
                log_error "Unknown option: $1"
                usage 1
                ;;
            *)
                TEST_FILES+=("$1")
                shift
                ;;
        esac
    done
}

#============================================================================
# Validation
#============================================================================

check_dependencies() {
    if ! command -v bats >/dev/null 2>&1; then
        log_error "bats is required but not installed"
        log_error "Install with: brew install bats-core (macOS) or npm install -g bats"
        exit 1
    fi
}

validate_format() {
    case "$FORMAT" in
        pretty|tap|junit)
            return 0
            ;;
        *)
            log_error "Invalid format: $FORMAT (must be pretty, tap, or junit)"
            return 1
            ;;
    esac
}

validate_test_dir() {
    if [ ! -d "$TEST_DIR" ]; then
        log_error "Test directory not found: $TEST_DIR"
        return 1
    fi
}

#============================================================================
# Test Discovery
#============================================================================

find_test_files() {
    if [ ${#TEST_FILES[@]} -gt 0 ]; then
        # Use specified files
        printf '%s\n' "${TEST_FILES[@]}"
    else
        # Find all .bats files in test directory
        find "$TEST_DIR" -type f -name "*.bats" | sort
    fi
}

#============================================================================
# Bats Execution
#============================================================================

run_bats() {
    local args=()

    # Build arguments
    if [ "$FORMAT" = "tap" ]; then
        args+=("--tap")
    elif [ "$FORMAT" = "junit" ]; then
        args+=("--formatter" "junit")
    else
        args+=("--pretty")
    fi

    if [ "$COUNT_ONLY" = "true" ]; then
        args+=("--count")
    fi

    if [ -n "$FILTER" ]; then
        args+=("--filter" "$FILTER")
    fi

    if [ "$JOBS" -gt 1 ]; then
        args+=("--jobs" "$JOBS")
    fi

    # Add test files
    while IFS= read -r test_file; do
        args+=("$test_file")
    done < <(find_test_files)

    # Check if we have test files
    if [ "${#args[@]}" -eq 0 ] || ! printf '%s\n' "${args[@]}" | grep -q '\.bats$'; then
        log_error "No test files found"
        exit 1
    fi

    # Run Bats
    log_info "Running Bats tests..."

    if [ "$VERBOSE" = "true" ]; then
        log_info "Command: bats ${args[*]}"
    fi

    if bats "${args[@]}"; then
        log_info "All tests passed"
        return 0
    else
        local exit_code=$?
        log_error "Tests failed (exit code: $exit_code)"
        return "$exit_code"
    fi
}

#============================================================================
# Main
#============================================================================

main() {
    parse_arguments "$@"

    # Validate configuration
    check_dependencies
    validate_format || exit 1

    if [ ${#TEST_FILES[@]} -eq 0 ]; then
        validate_test_dir || exit 1
    fi

    # Run tests
    if run_bats; then
        exit 0
    else
        exit 1
    fi
}

main "$@"
