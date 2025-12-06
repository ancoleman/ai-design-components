#!/bin/bash
#
# ShellCheck Linting Wrapper for CI/CD
#
# Runs ShellCheck on shell scripts with configurable options.
# Designed for CI/CD pipelines.

set -euo pipefail

#============================================================================
# Configuration
#============================================================================

readonly SCRIPT_NAME="$(basename "$0")"

# Default severity level
SEVERITY="warning"

# Default shell type
SHELL_TYPE="bash"

# Exclude warnings (comma-separated)
EXCLUDE=""

# Directories/files to check
CHECK_PATHS=()

# Exit with error on warnings
STRICT_MODE=false

# Output format
FORMAT="tty"

#============================================================================
# Usage
#============================================================================

usage() {
    cat <<EOF
$SCRIPT_NAME - ShellCheck wrapper for CI/CD

Usage:
    $SCRIPT_NAME [OPTIONS] [PATHS...]

Options:
    -h, --help              Show this help message
    -s, --severity LEVEL    Set severity: error|warning|info|style (default: warning)
    --shell TYPE            Set shell type: sh|bash|dash|ksh (default: bash)
    --exclude CODES         Exclude warning codes (comma-separated)
    --strict                Exit with error on any warnings
    --format FORMAT         Output format: tty|gcc|json|checkstyle (default: tty)

Arguments:
    PATHS                   Files or directories to check (default: current directory)

Examples:
    # Check all scripts in current directory
    $SCRIPT_NAME

    # Check specific file
    $SCRIPT_NAME script.sh

    # Check with strict mode (fail on warnings)
    $SCRIPT_NAME --strict *.sh

    # Check POSIX sh compliance
    $SCRIPT_NAME --shell sh script.sh

    # Exclude specific warnings
    $SCRIPT_NAME --exclude SC2086,SC2046 script.sh

    # JSON output for CI
    $SCRIPT_NAME --format json script.sh
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
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage 0
                ;;
            -s|--severity)
                SEVERITY="$2"
                shift 2
                ;;
            --shell)
                SHELL_TYPE="$2"
                shift 2
                ;;
            --exclude)
                EXCLUDE="$2"
                shift 2
                ;;
            --strict)
                STRICT_MODE=true
                shift
                ;;
            --format)
                FORMAT="$2"
                shift 2
                ;;
            -*)
                log_error "Unknown option: $1"
                usage 1
                ;;
            *)
                CHECK_PATHS+=("$1")
                shift
                ;;
        esac
    done

    # Default to current directory if no paths specified
    if [ ${#CHECK_PATHS[@]} -eq 0 ]; then
        CHECK_PATHS=(".")
    fi
}

#============================================================================
# Validation
#============================================================================

check_dependencies() {
    if ! command -v shellcheck >/dev/null 2>&1; then
        log_error "shellcheck is required but not installed"
        log_error "Install with: brew install shellcheck (macOS) or apt-get install shellcheck (Linux)"
        exit 1
    fi
}

validate_severity() {
    case "$SEVERITY" in
        error|warning|info|style)
            return 0
            ;;
        *)
            log_error "Invalid severity: $SEVERITY (must be error, warning, info, or style)"
            return 1
            ;;
    esac
}

validate_shell_type() {
    case "$SHELL_TYPE" in
        sh|bash|dash|ksh)
            return 0
            ;;
        *)
            log_error "Invalid shell type: $SHELL_TYPE (must be sh, bash, dash, or ksh)"
            return 1
            ;;
    esac
}

validate_format() {
    case "$FORMAT" in
        tty|gcc|json|checkstyle)
            return 0
            ;;
        *)
            log_error "Invalid format: $FORMAT (must be tty, gcc, json, or checkstyle)"
            return 1
            ;;
    esac
}

#============================================================================
# File Discovery
#============================================================================

find_shell_scripts() {
    local path=$1
    local scripts=()

    if [ -f "$path" ]; then
        # Single file
        scripts+=("$path")
    elif [ -d "$path" ]; then
        # Directory: find shell scripts
        while IFS= read -r -d '' file; do
            # Check if file has shell shebang
            if head -n 1 "$file" 2>/dev/null | grep -qE '^#!.*(sh|bash|dash|ksh)'; then
                scripts+=("$file")
            fi
        done < <(find "$path" -type f -executable -print0)

        # Also include *.sh files
        while IFS= read -r -d '' file; do
            scripts+=("$file")
        done < <(find "$path" -type f -name "*.sh" -print0)
    else
        log_error "Path not found: $path"
        return 1
    fi

    # Remove duplicates and print
    printf '%s\n' "${scripts[@]}" | sort -u
}

#============================================================================
# ShellCheck Execution
#============================================================================

run_shellcheck() {
    local file=$1
    local args=()

    # Build arguments
    args+=("--severity=$SEVERITY")
    args+=("--shell=$SHELL_TYPE")
    args+=("--format=$FORMAT")

    if [ -n "$EXCLUDE" ]; then
        args+=("--exclude=$EXCLUDE")
    fi

    # Run ShellCheck
    shellcheck "${args[@]}" "$file"
    return $?
}

#============================================================================
# Main
#============================================================================

main() {
    parse_arguments "$@"

    # Validate configuration
    check_dependencies
    validate_severity || exit 1
    validate_shell_type || exit 1
    validate_format || exit 1

    # Collect all files to check
    local all_files=()
    for path in "${CHECK_PATHS[@]}"; do
        while IFS= read -r file; do
            all_files+=("$file")
        done < <(find_shell_scripts "$path")
    done

    # Check if we found any files
    if [ ${#all_files[@]} -eq 0 ]; then
        log_error "No shell scripts found"
        exit 1
    fi

    log_info "Checking ${#all_files[@]} file(s) with ShellCheck"
    log_info "Severity: $SEVERITY, Shell: $SHELL_TYPE"

    # Run ShellCheck on each file
    local failed_count=0
    local warning_count=0

    for file in "${all_files[@]}"; do
        if run_shellcheck "$file"; then
            continue
        else
            local exit_code=$?

            if [ "$exit_code" -eq 1 ]; then
                # Errors found
                ((failed_count++))
            elif [ "$STRICT_MODE" = "true" ]; then
                # Warnings in strict mode
                ((warning_count++))
            fi
        fi
    done

    # Summary
    if [ "$FORMAT" = "tty" ]; then
        echo
        log_info "ShellCheck complete: ${#all_files[@]} file(s) checked"

        if [ "$failed_count" -gt 0 ]; then
            log_error "Files with errors: $failed_count"
        fi

        if [ "$warning_count" -gt 0 ]; then
            log_error "Files with warnings (strict mode): $warning_count"
        fi
    fi

    # Exit code
    if [ "$failed_count" -gt 0 ]; then
        exit 1
    fi

    if [ "$STRICT_MODE" = "true" ] && [ "$warning_count" -gt 0 ]; then
        exit 1
    fi

    exit 0
}

main "$@"
