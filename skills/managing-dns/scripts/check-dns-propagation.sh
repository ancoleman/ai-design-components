#!/bin/bash
# DNS Propagation Checker
# Checks DNS resolution across multiple public resolvers
# Usage: ./check-dns-propagation.sh example.com [A|AAAA|MX|TXT|NS]

set -euo pipefail

DOMAIN="${1:-}"
RECORD_TYPE="${2:-A}"

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <domain> [record-type]"
    echo "Example: $0 example.com A"
    exit 1
fi

# List of public DNS resolvers
declare -a RESOLVERS=(
    "8.8.8.8:Google DNS Primary"
    "8.8.4.4:Google DNS Secondary"
    "1.1.1.1:Cloudflare DNS Primary"
    "1.0.0.1:Cloudflare DNS Secondary"
    "208.67.222.222:OpenDNS Primary"
    "208.67.220.220:OpenDNS Secondary"
    "9.9.9.9:Quad9 Primary"
    "149.112.112.112:Quad9 Secondary"
    "64.6.64.6:Verisign Primary"
    "64.6.65.6:Verisign Secondary"
)

echo "================================================================"
echo "DNS Propagation Check: $DOMAIN ($RECORD_TYPE)"
echo "================================================================"
echo ""

for resolver_info in "${RESOLVERS[@]}"; do
    IFS=':' read -r ip name <<< "$resolver_info"

    # Query DNS
    result=$(dig @"$ip" "$DOMAIN" "$RECORD_TYPE" +short 2>/dev/null | head -1)

    if [ -z "$result" ]; then
        result="(no record)"
    fi

    printf "%-30s %s\n" "$name:" "$result"
done

echo ""
echo "================================================================"
echo "Check complete. If results differ, wait for TTL to expire."
echo "================================================================"
