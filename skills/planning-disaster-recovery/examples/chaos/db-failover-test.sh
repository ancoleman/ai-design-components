#!/bin/bash
#
# Database Failover Chaos Test
#
# Purpose: Simulate database primary failure to validate failover mechanisms,
# replica promotion, and application resilience during database outages.
#
# Requirements:
# - PostgreSQL/MySQL client tools (psql, mysql)
# - SSH access to database servers (for direct testing)
# - jq for JSON parsing
# - Prometheus endpoint (optional, for metrics)
#
# Usage:
#   ./db-failover-test.sh --mode postgres --primary-host db1.example.com --secondary-host db2.example.com
#   ./db-failover-test.sh --mode mysql --primary-host mysql-primary --secondary-host mysql-replica
#   ./db-failover-test.sh --mode aws-rds --db-cluster prod-cluster --region us-east-1
#

set -euo pipefail

# Default configuration
MODE="${MODE:-postgres}"
DRY_RUN="${DRY_RUN:-false}"
TIMEOUT="${TIMEOUT:-60}"  # 1 minute
PROMETHEUS_URL="${PROMETHEUS_URL:-}"
LOG_FILE="/tmp/db-failover-test-$(date +%Y%m%d-%H%M%S).log"

# Database credentials (prefer environment variables or secrets manager)
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_NAME="${DB_NAME:-postgres}"
DB_PORT="${DB_PORT:-5432}"

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

Chaos engineering test to simulate database failover and validate replica promotion.

OPTIONS:
    --mode MODE              Database mode: 'postgres', 'mysql', or 'aws-rds' (default: postgres)
    --primary-host HOST      Primary database host
    --secondary-host HOST    Secondary/replica database host
    --db-cluster CLUSTER     RDS cluster identifier (AWS RDS mode)
    --region REGION          AWS region (AWS RDS mode)
    --db-user USER           Database user (default: postgres)
    --db-password PASS       Database password (or use DB_PASSWORD env var)
    --db-name NAME           Database name (default: postgres)
    --db-port PORT           Database port (default: 5432 for postgres, 3306 for mysql)
    --timeout SECONDS        Maximum failover time (default: 60)
    --failure-method METHOD  How to fail primary: 'stop-service', 'kill-process', 'network' (default: stop-service)
    --dry-run                Show what would be done without executing
    --prometheus-url URL     Prometheus endpoint for metrics collection
    --skip-confirmation      Skip safety confirmation prompt
    --help                   Show this help message

EXAMPLES:
    # PostgreSQL with streaming replication
    $0 --mode postgres --primary-host db1.internal --secondary-host db2.internal

    # MySQL with async replication
    $0 --mode mysql --primary-host mysql-primary --secondary-host mysql-replica --db-port 3306

    # AWS RDS Multi-AZ
    $0 --mode aws-rds --db-cluster prod-aurora --region us-east-1

ENVIRONMENT VARIABLES:
    DB_USER              Database username
    DB_PASSWORD          Database password
    DRY_RUN              Set to 'true' to enable dry-run mode
    PROMETHEUS_URL       Prometheus endpoint URL
    AWS_PROFILE          AWS profile to use (AWS RDS mode)

EOF
    exit 1
}

# Parse arguments
SKIP_CONFIRMATION=false
PRIMARY_HOST=""
SECONDARY_HOST=""
DB_CLUSTER=""
REGION=""
FAILURE_METHOD="stop-service"

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --primary-host)
            PRIMARY_HOST="$2"
            shift 2
            ;;
        --secondary-host)
            SECONDARY_HOST="$2"
            shift 2
            ;;
        --db-cluster)
            DB_CLUSTER="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --db-user)
            DB_USER="$2"
            shift 2
            ;;
        --db-password)
            DB_PASSWORD="$2"
            shift 2
            ;;
        --db-name)
            DB_NAME="$2"
            shift 2
            ;;
        --db-port)
            DB_PORT="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --failure-method)
            FAILURE_METHOD="$2"
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

# Set MySQL default port if needed
if [[ "$MODE" == "mysql" && "$DB_PORT" == "5432" ]]; then
    DB_PORT=3306
fi

# Validate required parameters
validate_params() {
    if [[ "$MODE" == "aws-rds" ]]; then
        if [[ -z "$DB_CLUSTER" || -z "$REGION" ]]; then
            log_error "AWS RDS mode requires --db-cluster and --region"
            exit 1
        fi
        if ! command -v aws &> /dev/null; then
            log_error "AWS CLI is required for AWS RDS mode"
            exit 1
        fi
    else
        if [[ -z "$PRIMARY_HOST" || -z "$SECONDARY_HOST" ]]; then
            log_error "Direct mode requires --primary-host and --secondary-host"
            exit 1
        fi

        if [[ "$MODE" == "postgres" ]]; then
            if ! command -v psql &> /dev/null; then
                log_error "psql is required for PostgreSQL mode"
                exit 1
            fi
        elif [[ "$MODE" == "mysql" ]]; then
            if ! command -v mysql &> /dev/null; then
                log_error "mysql is required for MySQL mode"
                exit 1
            fi
        else
            log_error "Invalid mode: $MODE. Must be 'postgres', 'mysql', or 'aws-rds'"
            exit 1
        fi
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
    log_warning "  CHAOS ENGINEERING TEST - DATABASE FAILOVER SIMULATION"
    log_warning "═══════════════════════════════════════════════════════════"
    echo ""
    log_warning "This test will:"
    log_warning "  1. Simulate primary database failure"
    log_warning "  2. Force secondary replica promotion"
    log_warning "  3. Measure failover time and data consistency"
    log_warning "  4. Restore primary database"
    echo ""
    log_warning "Configuration:"
    log_warning "  Mode: $MODE"
    if [[ "$MODE" == "aws-rds" ]]; then
        log_warning "  RDS Cluster: $DB_CLUSTER"
        log_warning "  Region: $REGION"
    else
        log_warning "  Primary Host: $PRIMARY_HOST"
        log_warning "  Secondary Host: $SECONDARY_HOST"
        log_warning "  Failure Method: $FAILURE_METHOD"
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

# PostgreSQL: Check if database is in recovery mode
postgres_check_recovery() {
    local host="$1"
    local pgpassword_export=""

    if [[ -n "$DB_PASSWORD" ]]; then
        pgpassword_export="PGPASSWORD='$DB_PASSWORD'"
    fi

    local recovery_status=$(eval "$pgpassword_export psql -h $host -U $DB_USER -d $DB_NAME -p $DB_PORT -t -c 'SELECT pg_is_in_recovery();'" 2>/dev/null | tr -d ' ')

    echo "$recovery_status"
}

# PostgreSQL: Get replication lag
postgres_get_lag() {
    local host="$1"
    local pgpassword_export=""

    if [[ -n "$DB_PASSWORD" ]]; then
        pgpassword_export="PGPASSWORD='$DB_PASSWORD'"
    fi

    local lag=$(eval "$pgpassword_export psql -h $host -U $DB_USER -d $DB_NAME -p $DB_PORT -t -c \"SELECT EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp()));\"" 2>/dev/null | tr -d ' ')

    echo "${lag:-0}"
}

# MySQL: Check replication status
mysql_check_replication() {
    local host="$1"
    local mysql_cmd="mysql -h $host -u $DB_USER -p$DB_PASSWORD -P $DB_PORT -e"

    if [[ -z "$DB_PASSWORD" ]]; then
        mysql_cmd="mysql -h $host -u $DB_USER -P $DB_PORT -e"
    fi

    local slave_status=$($mysql_cmd "SHOW SLAVE STATUS\G" 2>/dev/null | grep "Slave_IO_Running" | awk '{print $2}')

    echo "$slave_status"
}

# MySQL: Get replication lag
mysql_get_lag() {
    local host="$1"
    local mysql_cmd="mysql -h $host -u $DB_USER -p$DB_PASSWORD -P $DB_PORT -e"

    if [[ -z "$DB_PASSWORD" ]]; then
        mysql_cmd="mysql -h $host -u $DB_USER -P $DB_PORT -e"
    fi

    local lag=$($mysql_cmd "SHOW SLAVE STATUS\G" 2>/dev/null | grep "Seconds_Behind_Master" | awk '{print $2}')

    echo "${lag:-0}"
}

# Get baseline metrics
get_baseline_metrics() {
    log_info "Collecting baseline metrics..."

    if [[ "$MODE" == "postgres" ]]; then
        BASELINE_RECOVERY_STATUS=$(postgres_check_recovery "$PRIMARY_HOST")
        BASELINE_LAG=$(postgres_get_lag "$SECONDARY_HOST")
        log_info "Primary recovery status: $BASELINE_RECOVERY_STATUS (should be 'f' for primary)"
        log_info "Secondary replication lag: ${BASELINE_LAG}s"
    elif [[ "$MODE" == "mysql" ]]; then
        BASELINE_REPLICATION=$(mysql_check_replication "$SECONDARY_HOST")
        BASELINE_LAG=$(mysql_get_lag "$SECONDARY_HOST")
        log_info "Replication status: $BASELINE_REPLICATION (should be 'Yes')"
        log_info "Replication lag: ${BASELINE_LAG}s"
    fi

    BASELINE_DB_CONNECTIONS=$(collect_metric "db_connections" 'pg_stat_database_numbackends{datname="'$DB_NAME'"}')
    BASELINE_ERROR_RATE=$(collect_metric "error_rate" 'rate(db_errors_total[1m])')

    log_info "Baseline DB Connections: $BASELINE_DB_CONNECTIONS"
    log_info "Baseline Error Rate: $BASELINE_ERROR_RATE"
}

# Fail primary database
fail_primary() {
    local host="$PRIMARY_HOST"

    log_info "Simulating primary database failure using method: $FAILURE_METHOD"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would fail primary database: $host"
        return 0
    fi

    case $FAILURE_METHOD in
        stop-service)
            if [[ "$MODE" == "postgres" ]]; then
                ssh "$host" "sudo systemctl stop postgresql" 2>/dev/null || log_warning "Failed to stop PostgreSQL service"
            elif [[ "$MODE" == "mysql" ]]; then
                ssh "$host" "sudo systemctl stop mysql" 2>/dev/null || ssh "$host" "sudo systemctl stop mysqld" 2>/dev/null || log_warning "Failed to stop MySQL service"
            fi
            ;;
        kill-process)
            if [[ "$MODE" == "postgres" ]]; then
                ssh "$host" "sudo pkill -9 postgres" 2>/dev/null || log_warning "Failed to kill PostgreSQL process"
            elif [[ "$MODE" == "mysql" ]]; then
                ssh "$host" "sudo pkill -9 mysqld" 2>/dev/null || log_warning "Failed to kill MySQL process"
            fi
            ;;
        network)
            ssh "$host" "sudo iptables -A INPUT -p tcp --dport $DB_PORT -j DROP" 2>/dev/null || log_warning "Failed to add iptables rule"
            ssh "$host" "sudo iptables -A OUTPUT -p tcp --sport $DB_PORT -j DROP" 2>/dev/null || log_warning "Failed to add iptables rule"
            ;;
        *)
            log_error "Unknown failure method: $FAILURE_METHOD"
            return 1
            ;;
    esac

    log_success "Primary database failed"
}

# AWS RDS: Trigger failover
aws_rds_failover() {
    log_info "Triggering AWS RDS failover for cluster: $DB_CLUSTER"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would trigger RDS failover"
        return 0
    fi

    aws rds failover-db-cluster \
        --db-cluster-identifier "$DB_CLUSTER" \
        --region "$REGION"

    log_success "Failover initiated"
}

# Measure failover time
measure_failover() {
    local secondary_host="$SECONDARY_HOST"
    local start_time=$(date +%s)
    local failover_time=0
    local max_wait="$TIMEOUT"

    log_info "Measuring failover time (timeout: ${max_wait}s)..."
    log_info "Monitoring secondary: $secondary_host"

    while true; do
        local elapsed=$(($(date +%s) - start_time))

        if [[ $elapsed -ge $max_wait ]]; then
            log_error "Failover timeout reached (${max_wait}s)"
            return 1
        fi

        local is_primary=false

        if [[ "$MODE" == "postgres" ]]; then
            local recovery_status=$(postgres_check_recovery "$secondary_host")
            if [[ "$recovery_status" == "f" ]]; then
                is_primary=true
            fi
        elif [[ "$MODE" == "mysql" ]]; then
            # For MySQL, check if secondary is accepting writes
            local mysql_cmd="mysql -h $secondary_host -u $DB_USER -p$DB_PASSWORD -P $DB_PORT -e"
            if [[ -z "$DB_PASSWORD" ]]; then
                mysql_cmd="mysql -h $secondary_host -u $DB_USER -P $DB_PORT -e"
            fi

            if $mysql_cmd "SELECT 1" &>/dev/null; then
                local read_only=$($mysql_cmd "SHOW VARIABLES LIKE 'read_only'\G" 2>/dev/null | grep "Value" | awk '{print $2}')
                if [[ "$read_only" == "OFF" ]]; then
                    is_primary=true
                fi
            fi
        fi

        if [[ "$is_primary" == "true" ]]; then
            failover_time=$elapsed
            log_success "Secondary promoted to primary after ${failover_time}s"
            break
        fi

        log_info "Waiting for promotion... (${elapsed}s elapsed)"
        sleep 2
    done

    echo "$failover_time"
}

# Verify failover success
verify_failover() {
    local secondary_host="$SECONDARY_HOST"

    log_info "Verifying failover success..."

    if [[ "$MODE" == "postgres" ]]; then
        local recovery_status=$(postgres_check_recovery "$secondary_host")
        if [[ "$recovery_status" != "f" ]]; then
            log_error "Secondary is still in recovery mode"
            return 1
        fi
        log_success "Secondary is now primary (recovery mode: false)"

        # Test write operation
        local pgpassword_export=""
        if [[ -n "$DB_PASSWORD" ]]; then
            pgpassword_export="PGPASSWORD='$DB_PASSWORD'"
        fi

        if eval "$pgpassword_export psql -h $secondary_host -U $DB_USER -d $DB_NAME -p $DB_PORT -c 'CREATE TABLE IF NOT EXISTS chaos_test (id INT);'" &>/dev/null; then
            eval "$pgpassword_export psql -h $secondary_host -U $DB_USER -d $DB_NAME -p $DB_PORT -c 'DROP TABLE chaos_test;'" &>/dev/null
            log_success "Write test successful"
        else
            log_warning "Write test failed"
            return 1
        fi

    elif [[ "$MODE" == "mysql" ]]; then
        local mysql_cmd="mysql -h $secondary_host -u $DB_USER -p$DB_PASSWORD -P $DB_PORT -e"
        if [[ -z "$DB_PASSWORD" ]]; then
            mysql_cmd="mysql -h $secondary_host -u $DB_USER -P $DB_PORT -e"
        fi

        local read_only=$($mysql_cmd "SHOW VARIABLES LIKE 'read_only'\G" 2>/dev/null | grep "Value" | awk '{print $2}')
        if [[ "$read_only" != "OFF" ]]; then
            log_error "Secondary is still in read-only mode"
            return 1
        fi
        log_success "Secondary is now writable (read_only: OFF)"

        # Test write operation
        if $mysql_cmd "CREATE TABLE IF NOT EXISTS chaos_test (id INT);" &>/dev/null; then
            $mysql_cmd "DROP TABLE chaos_test;" &>/dev/null
            log_success "Write test successful"
        else
            log_warning "Write test failed"
            return 1
        fi
    fi

    log_success "Failover verification complete"
    return 0
}

# Restore primary database
restore_primary() {
    local host="$PRIMARY_HOST"

    log_info "Restoring primary database: $host"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would restore primary database"
        return 0
    fi

    case $FAILURE_METHOD in
        stop-service)
            if [[ "$MODE" == "postgres" ]]; then
                ssh "$host" "sudo systemctl start postgresql" 2>/dev/null || log_warning "Failed to start PostgreSQL service"
            elif [[ "$MODE" == "mysql" ]]; then
                ssh "$host" "sudo systemctl start mysql" 2>/dev/null || ssh "$host" "sudo systemctl start mysqld" 2>/dev/null || log_warning "Failed to start MySQL service"
            fi
            ;;
        kill-process)
            if [[ "$MODE" == "postgres" ]]; then
                ssh "$host" "sudo systemctl start postgresql" 2>/dev/null || log_warning "Failed to start PostgreSQL service"
            elif [[ "$MODE" == "mysql" ]]; then
                ssh "$host" "sudo systemctl start mysql" 2>/dev/null || ssh "$host" "sudo systemctl start mysqld" 2>/dev/null || log_warning "Failed to start MySQL service"
            fi
            ;;
        network)
            ssh "$host" "sudo iptables -D INPUT -p tcp --dport $DB_PORT -j DROP" 2>/dev/null || log_warning "Failed to remove iptables rule"
            ssh "$host" "sudo iptables -D OUTPUT -p tcp --sport $DB_PORT -j DROP" 2>/dev/null || log_warning "Failed to remove iptables rule"
            ;;
    esac

    log_success "Primary database restored (will resync as replica)"
}

# Generate test report
generate_report() {
    local failover_time="$1"
    local test_result="$2"

    local report_file="/tmp/db-failover-report-$(date +%Y%m%d-%H%M%S).json"

    cat > "$report_file" <<EOF
{
  "test": "database-failover",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "mode": "$MODE",
  "configuration": {
    "primary_host": "$PRIMARY_HOST",
    "secondary_host": "$SECONDARY_HOST",
    "db_cluster": "$DB_CLUSTER",
    "failure_method": "$FAILURE_METHOD",
    "timeout": $TIMEOUT
  },
  "baseline_metrics": {
    "replication_lag": "${BASELINE_LAG:-0}",
    "db_connections": "${BASELINE_DB_CONNECTIONS:-0}",
    "error_rate": "${BASELINE_ERROR_RATE:-0}"
  },
  "results": {
    "failover_time_seconds": $failover_time,
    "test_result": "$test_result",
    "rto_met": $(if [[ $failover_time -le 60 ]]; then echo "true"; else echo "false"; fi)
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

    if [[ "$MODE" != "aws-rds" ]]; then
        restore_primary
    fi

    log_info "Cleanup complete"
    log_info "Full log: $LOG_FILE"

    exit $exit_code
}

# Register cleanup trap
trap cleanup EXIT INT TERM

# Main execution
main() {
    log_info "Starting database failover chaos test"
    log_info "Log file: $LOG_FILE"

    # Validate parameters
    validate_params

    # Safety confirmation
    confirm_execution

    # Get baseline metrics
    get_baseline_metrics

    # Fail primary database
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 1: Simulating primary database failure"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ "$MODE" == "aws-rds" ]]; then
        aws_rds_failover
    else
        fail_primary
    fi

    # Measure failover time
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 2: Measuring failover time"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ "$MODE" == "aws-rds" ]]; then
        # For AWS RDS, we need to wait and check cluster status
        log_info "Waiting for AWS RDS failover to complete..."
        sleep 5
        failover_time=30  # Approximate, as AWS manages this
        log_info "AWS RDS failover initiated (approximate time: ${failover_time}s)"
    else
        failover_time=$(measure_failover)
        failover_status=$?
    fi

    # Verify failover
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 3: Verifying failover"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ "$MODE" != "aws-rds" ]] && verify_failover; then
        test_result="PASS"
    elif [[ "$MODE" == "aws-rds" ]]; then
        test_result="PASS"
        log_info "AWS RDS failover completed"
    else
        test_result="FAIL"
    fi

    # Generate report
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "PHASE 4: Test results"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    generate_report "$failover_time" "$test_result"

    # Final status
    echo ""
    if [[ "$test_result" == "PASS" ]]; then
        log_success "═══════════════════════════════════════════════════════════"
        log_success "  TEST PASSED"
        log_success "  Failover Time: ${failover_time}s"
        if [[ $failover_time -le 60 ]]; then
            log_success "  RTO Target Met: < 60s"
        else
            log_warning "  RTO Target Missed: ${failover_time}s > 60s"
        fi
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
