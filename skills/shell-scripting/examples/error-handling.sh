#!/bin/bash
#
# Error Handling Examples
#
# Demonstrates various error handling patterns in shell scripts.

#============================================================================
# Example 1: Fail-Fast with set -euo pipefail
#============================================================================

example_fail_fast() {
    echo "=== Example 1: Fail-Fast Pattern ==="

    (
        set -euo pipefail

        echo "Step 1: Success"
        true

        echo "Step 2: Success"
        true

        echo "Step 3: This will fail"
        false

        echo "This line will never execute"
    )

    echo "Script continued (fail-fast in subshell)"
    echo
}

#============================================================================
# Example 2: Explicit Exit Code Checking
#============================================================================

example_explicit_checking() {
    echo "=== Example 2: Explicit Exit Code Checking ==="

    # Method 1: if ! command
    if ! grep -q "pattern" /dev/null; then
        echo "Pattern not found (expected)"
    fi

    # Method 2: Capture and check exit code
    grep -q "pattern" /dev/null
    exit_code=$?
    if [ "$exit_code" -ne 0 ]; then
        echo "Exit code: $exit_code (expected)"
    fi

    # Method 3: Different handling per exit code
    curl -sSL --max-time 1 http://localhost:99999 2>/dev/null
    exit_code=$?

    case "$exit_code" in
        0)
            echo "Success"
            ;;
        6)
            echo "Could not resolve host (expected for this example)"
            ;;
        7)
            echo "Failed to connect (expected for this example)"
            ;;
        28)
            echo "Operation timeout"
            ;;
        *)
            echo "Curl failed with exit code: $exit_code"
            ;;
    esac

    echo
}

#============================================================================
# Example 3: Trap Handlers
#============================================================================

example_trap_handlers() {
    echo "=== Example 3: Trap Handlers ==="

    (
        # Create temporary file
        TEMP_FILE=$(mktemp)
        echo "Created temp file: $TEMP_FILE"

        # Cleanup function
        cleanup() {
            echo "Cleanup: Removing $TEMP_FILE"
            rm -f "$TEMP_FILE"
        }

        # Register cleanup on EXIT
        trap cleanup EXIT

        # Do some work
        echo "data" > "$TEMP_FILE"
        echo "Working with temp file..."

        # Cleanup runs automatically when subshell exits
    )

    echo "Temp file cleaned up automatically"
    echo
}

#============================================================================
# Example 4: Error Handler with Line Number
#============================================================================

example_error_handler() {
    echo "=== Example 4: Error Handler with Line Number ==="

    (
        set -Eeuo pipefail

        error_handler() {
            local line=$1
            local command=$2
            echo "Error on line $line: $command" >&2
        }

        trap 'error_handler $LINENO "$BASH_COMMAND"' ERR

        echo "Step 1: Success"
        true

        echo "Step 2: About to fail"
        false  # This triggers error handler

        echo "This won't execute"
    )

    echo "Error handler demonstrated"
    echo
}

#============================================================================
# Example 5: Defensive Programming
#============================================================================

example_defensive_programming() {
    echo "=== Example 5: Defensive Programming ==="

    # Check required commands
    check_command() {
        local cmd=$1
        if command -v "$cmd" >/dev/null 2>&1; then
            echo "✓ $cmd is available"
        else
            echo "✗ $cmd is not available"
        fi
    }

    check_command "bash"
    check_command "grep"
    check_command "nonexistent_command"

    # Check required environment variables
    export REQUIRED_VAR="value"
    : "${REQUIRED_VAR:?Error: REQUIRED_VAR must be set}"
    echo "✓ REQUIRED_VAR is set: $REQUIRED_VAR"

    # Check optional environment variable with default
    echo "Optional var: ${OPTIONAL_VAR:-default_value}"

    # Check file exists
    if [ -f "/etc/hosts" ]; then
        echo "✓ /etc/hosts exists"
    fi

    if [ ! -f "/nonexistent/file" ]; then
        echo "✓ Correctly detected missing file"
    fi

    echo
}

#============================================================================
# Example 6: Retry Logic
#============================================================================

example_retry_logic() {
    echo "=== Example 6: Retry Logic ==="

    retry_command() {
        local max_attempts=3
        local attempt=1
        local sleep_time=1

        while [ "$attempt" -le "$max_attempts" ]; do
            echo "Attempt $attempt of $max_attempts"

            # Simulate command that fails first 2 times
            if [ "$attempt" -eq 3 ]; then
                echo "Success on attempt $attempt"
                return 0
            else
                echo "Failed, retrying in ${sleep_time}s..."
                sleep "$sleep_time"
                attempt=$((attempt + 1))
            fi
        done

        echo "Failed after $max_attempts attempts"
        return 1
    }

    if retry_command; then
        echo "Command succeeded with retry logic"
    else
        echo "Command failed after retries"
    fi

    echo
}

#============================================================================
# Example 7: Timeout Handling
#============================================================================

example_timeout() {
    echo "=== Example 7: Timeout Handling ==="

    # Run command with timeout
    if timeout 2s sleep 1; then
        echo "✓ Command completed within timeout"
    else
        echo "✗ Command timed out or failed"
    fi

    if timeout 1s sleep 2; then
        echo "✓ Command completed within timeout"
    else
        local exit_code=$?
        if [ "$exit_code" -eq 124 ]; then
            echo "✗ Command timed out (expected)"
        else
            echo "✗ Command failed with exit code: $exit_code"
        fi
    fi

    echo
}

#============================================================================
# Example 8: Pipeline Error Handling
#============================================================================

example_pipeline_errors() {
    echo "=== Example 8: Pipeline Error Handling ==="

    # Without pipefail: exit code is from last command
    echo "Without pipefail:"
    false | true
    echo "Exit code: $? (from last command: true)"

    # With pipefail: exit code is from failed command
    echo "With pipefail:"
    (
        set -o pipefail
        false | true
        echo "Exit code: $? (from failed command: false)"
    ) || echo "Pipeline failed (expected)"

    echo
}

#============================================================================
# Main
#============================================================================

main() {
    echo "Shell Error Handling Examples"
    echo "=============================="
    echo

    example_fail_fast
    example_explicit_checking
    example_trap_handlers
    example_error_handler
    example_defensive_programming
    example_retry_logic
    example_timeout
    example_pipeline_errors

    echo "All examples completed"
}

main "$@"
