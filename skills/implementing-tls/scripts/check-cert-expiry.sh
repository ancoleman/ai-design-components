#!/bin/bash
# Check certificate expiration for local files or remote servers

set -e

usage() {
    cat <<EOF
Usage: $0 [OPTIONS] <certificate-file or hostname:port>

Check certificate expiration and alert if expiring soon.

Options:
    -w DAYS    Warning threshold (default: 30 days)
    -c DAYS    Critical threshold (default: 7 days)
    -h         Show this help

Examples:
    $0 cert.pem
    $0 example.com:443
    $0 -w 60 -c 14 example.com:443
EOF
    exit 1
}

# Defaults
WARN_DAYS=30
CRIT_DAYS=7

# Parse options
while getopts "w:c:h" opt; do
    case $opt in
        w) WARN_DAYS=$OPTARG ;;
        c) CRIT_DAYS=$OPTARG ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND-1))

if [ $# -eq 0 ]; then
    usage
fi

TARGET=$1

# Determine if file or remote
if [ -f "$TARGET" ]; then
    # Local file
    EXPIRY=$(openssl x509 -in "$TARGET" -noout -enddate | cut -d= -f2)
    SUBJECT=$(openssl x509 -in "$TARGET" -noout -subject | cut -d= -f2-)
else
    # Remote server (hostname:port)
    if [[ ! $TARGET =~ : ]]; then
        TARGET="${TARGET}:443"
    fi
    EXPIRY=$(echo | openssl s_client -connect "$TARGET" 2>/dev/null | \
             openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    SUBJECT=$(echo | openssl s_client -connect "$TARGET" 2>/dev/null | \
              openssl x509 -noout -subject 2>/dev/null | cut -d= -f2-)
fi

if [ -z "$EXPIRY" ]; then
    echo "ERROR: Could not get certificate expiration"
    exit 3
fi

# Calculate days remaining
EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$EXPIRY" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_EPOCH - $NOW_EPOCH) / 86400 ))

# Output
echo "Certificate: $TARGET"
echo "Subject: $SUBJECT"
echo "Expires: $EXPIRY"
echo "Days remaining: $DAYS_LEFT"

# Check thresholds
if [ $DAYS_LEFT -le 0 ]; then
    echo "STATUS: EXPIRED"
    exit 2
elif [ $DAYS_LEFT -le $CRIT_DAYS ]; then
    echo "STATUS: CRITICAL (expires in $DAYS_LEFT days)"
    exit 2
elif [ $DAYS_LEFT -le $WARN_DAYS ]; then
    echo "STATUS: WARNING (expires in $DAYS_LEFT days)"
    exit 1
else
    echo "STATUS: OK"
    exit 0
fi
