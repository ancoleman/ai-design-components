#!/bin/bash
#
# Region Failure Chaos Test
#
# Purpose: Simulate a complete region failure to validate cross-region failover
# mechanisms, DNS updates, and application resilience.
#
# Requirements:
# - AWS CLI (for AWS mode) or generic HTTP monitoring
# - jq for JSON parsing
# - curl for health checks
# - Prometheus endpoint (optional, for metrics)
#
# Usage:
#   ./region-failure-test.sh --mode aws --primary-region us-east-1 --secondary-region us-west-2
#   ./region-failure-test.sh --mode generic --primary-url https://api.example.com --secondary-url https://api-backup.example.com
#

set -euo pipefail

# Default configuration
MODE="${MODE:-aws}"
DRY_RUN="${DRY_RUN:-false}"
TIMEOUT="${TIMEOUT:-300}"  # 5 minutes
PROMETHEUS_URL="${PROMETHEUS_URL:-}"
LOG_FILE="/tmp/region-failure-test-$(date +%Y%m%d-%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE"
}

log_info() { log "${BLUE}INFO${NC}" "$@"; }
log_success() { log "${GREEN}SUCCESS${NC}" "$@"; }
log_warning() { log "${YELLOW}WARNING${NC}" "$@"; }
log_error() { log "${RED}ERROR${NC}" "$@"; }

# Usage information
usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Chaos engineering test to simulate region failure and validate failover.

OPTIONS:
    --mode MODE              Test mode: 'aws' or 'generic' (default: aws)
    --primary-region REGION  Primary AWS region (AWS mode)
    --secondary-region REGION Secondary AWS region (AWS mode)
    --primary-url URL        Primary endpoint URL (generic mode)
    --secondary-url URL      Secondary endpoint URL (generic mode)
    --vpc-id VPC_ID          VPC ID to isolate (AWS mode)
    --timeout SECONDS        Maximum test duration (default: 300)
    --dry-run                Show what would be done without executing
    --prometheus-url URL     Prometheus endpoint for metrics collection
    --skip-confirmation      Skip safety confirmation prompt
    --help                   Show this help message

EXAMPLES:
    # AWS mode - simulate region failure via NACL
    $0 --mode aws --primary-region us-east-1 --secondary-region us-west-2 --vpc-id vpc-12345

    # Generic mode - block traffic via firewall/routing
    $0 --mode generic --primary-url https://api.example.com --secondary-url https://backup-api.example.com

ENVIRONMENT VARIABLES:
    DRY_RUN              Set to 'true' to enable dry-run mode
    PROMETHEUS_URL       Prometheus endpoint URL
    AWS_PROFILE          AWS profile to use (AWS mode)

EOF
    exit 1
}

# Parse arguments
SKIP_CONFIRMATION=false
PRIMARY_REGION=""
SECONDARY_REGION=""
PRIMARY_URL=""
SECONDARY_URL=""
VPC_ID=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --primary-region)
            PRIMARY_REGION="$2"
            shift 2
            ;;
        --secondary-region)
            SECONDARY_REGION="$2"
            shift 2
            ;;
        --primary-url)
            PRIMARY_URL="$2"
            shift 2
            ;;
        --secondary-url)
            SECONDARY_URL="$2"
            shift 2
            ;;
        --vpc-id)
            VPC_ID="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --prometheus-url)
            PROMETHEUS_URL="$2"
            shift 2
            ;;
        --skip-confirmation)
            SKIP_CONFIRMATION=true
            shift
            ;;
        --help)
            usage
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate required parameters
validate_params() {
    if [[ "$MODE" == "aws" ]]; then
        if [[ -z "$PRIMARY_REGION" || -z "$SECONDARY_REGION" ]]; then
            log_error "AWS mode requires --primary-region and --secondary-region"
            exit 1
        fi
        if ! command -v aws &> /dev/null; then
            log_error "AWS CLI is required for AWS mode"
            exit 1
        fi
    elif [[ "$MODE" == "generic" ]]; then
        if [[ -z "$PRIMARY_URL" || -z "$SECONDARY_URL" ]]; then
            log_error "Generic mode requires --primary-url and --secondary-url"
            exit 1
        fi
    else
        log_error "Invalid mode: $MODE. Must be 'aws' or 'generic'"
        exit 1
    fi

    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed"
        exit 1
    fi
}

# Safety confirmation
confirm_execution() {
    if [[ "$SKIP_CONFIRMATION" == "true" ]]; then
        return 0
    fi

    echo ""
    log_warning "═══════════════════════════════════════════════════════════"
    log_warning "  CHAOS ENGINEERING TEST - REGION FAILURE SIMULATION"
    log_warning "═══════════════════════════════════════════════════════════"
    echo ""
    log_warning "This test will:"
    log_warning "  1. Simulate a complete region failure"
    log_warning "  2. Block network traffic to primary region"
    log_warning "  3. Trigger failover to secondary region"
    log_warning "  4. Measure recovery time and application impact"
    echo ""
    log_warning "Configuration:"
    log_warning "  Mode: $MODE"
    if [[ "$MODE" == "aws" ]]; then
        log_warning "  Primary Region: $PRIMARY_REGION"
        log_warning "  Secondary Region: $SECONDARY_REGION"
        [[ -n "$VPC_ID" ]] && log_warning "  VPC ID: $VPC_ID"
    else
        log_warning "  Primary URL: $PRIMARY_URL"
        log_warning "  Secondary URL: $SECONDARY_URL"
    fi
    log_warning "  Timeout: ${TIMEOUT}s"
    log_warning "  Dry Run: $DRY_RUN"
    echo ""
    log_warning "═══════════════════════════════════════════════════════════"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "Running in DRY-RUN mode - no changes will be made"
        return 0
    fi

    read -p "Do you want to proceed? (yes/no): " -r
    echo
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log_info "Test cancelled by user"
        exit 0
    fi
}

# Collect Prometheus metrics
collect_metric() {
    local metric_name="$1"
    local query="$2"

    if [[ -z "$PROMETHEUS_URL" ]]; then
        return 0
    fi

    local result=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=${query}" | jq -r '.data.result[0].value[1]' 2>/dev/null || echo "0")
    echo "$result"
}

# Get baseline metrics
get_baseline_metrics() {
    log_info "Collecting baseline metrics..."

    BASELINE_ERROR_RATE=$(collect_metric "error_rate" 'rate(http_requests_total{status=~"5.."}[1m])')
    BASELINE_LATENCY=$(collect_metric "latency" 'histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[1m]))')
    BASELINE_THROUGHPUT=$(collect_metric "throughput" 'rate(http_requests_total[1m])')

    log_info "Baseline Error Rate: $BASELINE_ERROR_RATE"
    log_info "Baseline P99 Latency: ${BASELINE_LATENCY}s"
    log_info "Baseline Throughput: ${BASELINE_THROUGHPUT} req/s"
}

# Check endpoint health
check_endpoint_health() {
    local url="$1"
    local response_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")

    if [[ "$response_code" =~ ^2[0-9]{2}$ ]]; then
        return 0
    else
        return 1
    fi
}

# AWS: Block region traffic via NACL
aws_block_region() {
    log_info "Blocking traffic to primary region: $PRIMARY_REGION"

    if [[ -z "$VPC_ID" ]]; then
        log_warning "No VPC ID specified, discovering default VPC..."
        VPC_ID=$(aws ec2 describe-vpcs \
            --region "$PRIMARY_REGION" \
            --filters "Name=isDefault,Values=true" \
            --query 'Vpcs[0].VpcId' \
            --output text)

        if [[ "$VPC_ID" == "None" || -z "$VPC_ID" ]]; then
            log_error "Could not find VPC in region $PRIMARY_REGION"
            return 1
        fi
        log_info "Using VPC: $VPC_ID"
    fi

    # Get Network ACL ID
    NACL_ID=$(aws ec2 describe-network-acls \
        --region "$PRIMARY_REGION" \
        --filters "Name=vpc-id,Values=$VPC_ID" "Name=default,Values=true" \
        --query 'NetworkAcls[0].NetworkAclId' \
        --output text)

    if [[ "$NACL_ID" == "None" || -z "$NACL_ID" ]]; then
        log_error "Could not find Network ACL for VPC $VPC_ID"
        return 1
    fi

    log_info "Network ACL ID: $NACL_ID"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create DENY rule in NACL $NACL_ID"
        return 0
    fi

    # Create deny rule (rule number 1 to take precedence)
    aws ec2 create-network-acl-entry \
        --region "$PRIMARY_REGION" \
        --network-acl-id "$NACL_ID" \
        --rule-number 1 \
        --protocol -1 \
        --rule-action deny \
        --egress \
        --cidr-block 0.0.0.0/0

    aws ec2 create-network-acl-entry \
        --region "$PRIMARY_REGION" \
        --network-acl-id "$NACL_ID" \
        --rule-number 1 \
        --protocol -1 \
        --rule-action deny \
        --ingress \
        --cidr-block 0.0.0.0/0

    log_success "Successfully blocked traffic to $PRIMARY_REGION"

    # Store NACL ID for cleanup
    echo "$NACL_ID" > /tmp/chaos-nacl-id.txt
}

# AWS: Restore region traffic
aws_restore_region() {
    log_info "Restoring traffic to primary region: $PRIMARY_REGION"

    if [[ ! -f /tmp/chaos-nacl-id.txt ]]; then
        log_warning "No NACL ID found, skipping restore"
        return 0
    fi

    NACL_ID=$(cat /tmp/chaos-nacl-id.txt)

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would remove DENY rules from NACL $NACL_ID"
        return 0
    fi

    # Remove deny rules
    aws ec2 delete-network-acl-entry \
        --region "$PRIMARY_REGION" \
        --network-acl-id "$NACL_ID" \
        --rule-number 1 \
        --egress \
        2>/dev/null || log_warning "Failed to delete egress rule"

    aws ec2 delete-network-acl-entry \
        --region "$PRIMARY_REGION" \
        --network-acl-id "$NACL_ID" \
        --rule-number 1 \
        --ingress \
        2>/dev/null || log_warning "Failed to delete ingress rule"

    rm -f /tmp/chaos-nacl-id.txt
    log_success "Traffic restored to $PRIMARY_REGION"
}

# Generic: Simulate region failure (requires manual intervention)
generic_block_region() {
    log_warning "Generic mode: Manual intervention required"
    log_info "Please block traffic to: $PRIMARY_URL"
    log_info "Suggested methods:"
    log_info "  - Update firewall rules to drop traffic"
    log_info "  - Update routing tables to blackhole traffic"
    log_info "  - Disable load balancer"
    log_info "  - Stop application servers"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would wait for manual failover"
        return 0
    fi

    read -p "Press ENTER when primary region is blocked..." -r
    log_info "Proceeding with test..."
}

# Generic: Restore region
generic_restore_region() {
    log_warning "Generic mode: Manual restoration required"
    log_info "Please restore traffic to: $PRIMARY_URL"
    log_info "Suggested methods:"
    log_info "  - Remove firewall rules"
    log_info "  - Restore routing tables"
    log_info "  - Enable load balancer"
    log_info "  - Start application servers"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would wait for manual restoration"
        return 0
    fi

    read -p "Press ENTER when primary region is restored..." -r
    log_info "Primary region restored"
}

# Measure recovery time
measure_recovery() {
    local secondary_endpoint="$1"
    local start_time=$(date +%s)
    local recovery_time=0
    local max_wait="$TIMEOUT"

    log_info "Measuring recovery time (timeout: ${max_wait}s)..."
    log_info "Monitoring secondary endpoint: $secondary_endpoint"

    while true; do
        local elapsed=$(($(date +%s) - start_time))

        if [[ $elapsed -ge $max_wait ]]; then
            log_error "Recovery timeout reached (${max_wait}s)"
            return 1
        fi

        if check_endpoint_health "$secondary_endpoint"; then
            recovery_time=$elapsed
            log_success "Secondary endpoint healthy after ${recovery_time}s"
            break
        fi

        log_info "Waiting for recovery... (${elapsed}s elapsed)"
        sleep 2
    done

    echo "$recovery_time"
}

# Verify failover success
verify_failover() {
    local secondary_endpoint="$1"

    log_info "Verifying failover to secondary region..."

    # Check health
    if ! check_endpoint_health "$secondary_endpoint"; then
        log_error "Secondary endpoint is not healthy"
        return 1
    fi

    # Check error rate if Prometheus available
    if [[ -n "$PROMETHEUS_URL" ]]; then
        local current_error_rate=$(collect_metric "error_rate" 'rate(http_requests_total{status=~"5.."}[1m])')
        log_info "Current error rate: $current_error_rate"

        # Allow 10% increase in error rate
        local threshold=$(echo "$BASELINE_ERROR_RATE * 1.1" | bc -l)
        if (( $(echo "$current_error_rate > $threshold" | bc -l) )); then
            log_warning "Error rate increased beyond threshold"
        else
            log_success "Error rate within acceptable range"
        fi
    fi

    log_success "Failover verification complete"
    return 0
}

# Generate test report
generate_report() {
    local recovery_time="$1"
    local test_result="$2"

    local report_file="/tmp/region-failure-report-$(date +%Y%m%d-%H%M%S).json"

    cat > "$report_file" <<EOF
{
  "test": "region-failure",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "mode": "$MODE",
  "configuration": {
    "primary_region": "$PRIMARY_REGION",
    "secondary_region": "$SECONDARY_REGION",
    "primary_url": "$PRIMARY_URL",
    "secondary_url": "$SECONDARY_URL",
    "timeout": $TIMEOUT
  },
  "baseline_metrics": {
    "error_rate": "$BASELINE_ERROR_RATE",
    "latency_p99": "$BASELINE_LATENCY",
    "throughput": "$BASELINE_THROUGHPUT"
  },
  "results": {
    "recovery_time_seconds": $recovery_time,
    "test_result": "$test_result"
  }
}
EOF

    log_info "Report saved to: $report_file"
    cat "$report_file" | jq '.'
}

# Cleanup function
cleanup() {
    local exit_code=$?

    log_info "Running cleanup..."

    if [[ "$MODE" == "aws" ]]; then
        aws_restore_region
    else
        generic_restore_region
    fi

    log_info "Cleanup complete"
    log_info "Full log: $LOG_FILE"

    exit $exit_code
}

# Register cleanup trap
trap cleanup EXIT INT TERM

# Main execution
main() {
    log_info "Starting region failure chaos test"
    log_info "Log file: $LOG_FILE"

    # Validate parameters
    validate_params

    # Safety confirmation
    confirm_execution

    # Get baseline metrics
    get_baseline_metrics

    # Determine secondary endpoint
    local secondary_endpoint=""
    if [[ "$MODE" == "aws" ]]; then
        # For AWS mode, you would typically have a health check endpoint
        # This is a placeholder - adjust based on your architecture
        secondary_endpoint="${SECONDARY_URL:-https://api.${SECONDARY_REGION}.example.com/health}"
        log_warning "Secondary endpoint not specified, using: $secondary_endpoint"
        log_warning "Override with --secondary-url if different"
    else
        secondary_endpoint="$SECONDARY_URL"
    fi

    # Block primary region
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 1: Simulating region failure"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ "$MODE" == "aws" ]]; then
        aws_block_region
    else
        generic_block_region
    fi

    # Measure recovery time
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 2: Measuring recovery time"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    recovery_time=$(measure_recovery "$secondary_endpoint")
    recovery_status=$?

    # Verify failover
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 3: Verifying failover"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if verify_failover "$secondary_endpoint"; then
        test_result="PASS"
    else
        test_result="FAIL"
    fi

    # Generate report
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 4: Test results"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    generate_report "$recovery_time" "$test_result"

    # Final status
    echo ""
    if [[ "$test_result" == "PASS" ]]; then
        log_success "═══════════════════════════════════════════════════════════"
        log_success "  TEST PASSED"
        log_success "  Recovery Time: ${recovery_time}s"
        log_success "═══════════════════════════════════════════════════════════"
        return 0
    else
        log_error "═══════════════════════════════════════════════════════════"
        log_error "  TEST FAILED"
        log_error "═══════════════════════════════════════════════════════════"
        return 1
    fi
}

# Run main function
main "$@"
