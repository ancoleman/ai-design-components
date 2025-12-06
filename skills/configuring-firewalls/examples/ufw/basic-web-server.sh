#!/bin/bash
# Basic Web Server UFW Configuration
#
# This script configures UFW for a typical web server with:
# - SSH access from specific IP range
# - HTTP and HTTPS access from anywhere
# - Rate limiting on SSH to prevent brute force
# - Logging enabled
#
# Usage: sudo ./basic-web-server.sh

set -e  # Exit on error

# Configuration
OFFICE_CIDR="203.0.113.0/24"  # Change to your office IP range

echo "=== Configuring UFW for Web Server ==="

# Set default policies
echo "Setting default policies..."
ufw default deny incoming
ufw default allow outgoing

# Allow SSH from office only (NOT 0.0.0.0/0 for security)
echo "Allowing SSH from ${OFFICE_CIDR}..."
ufw allow from ${OFFICE_CIDR} to any port 22

# Rate limit SSH to prevent brute force
echo "Enabling SSH rate limiting..."
ufw limit ssh

# Allow HTTP
echo "Allowing HTTP (port 80)..."
ufw allow http

# Allow HTTPS
echo "Allowing HTTPS (port 443)..."
ufw allow https

# Enable logging
echo "Enabling logging..."
ufw logging on

# Show rules before enabling
echo ""
echo "=== Rules to be applied ==="
ufw show added

# Confirm before enabling
read -p "Enable UFW with these rules? (yes/no): " confirm

if [ "$confirm" == "yes" ]; then
    echo "Enabling UFW..."
    ufw --force enable

    echo ""
    echo "=== UFW Status ==="
    ufw status verbose

    echo ""
    echo "✅ UFW configuration complete!"
    echo ""
    echo "Next steps:"
    echo "1. Test SSH access from office IP"
    echo "2. Test HTTP/HTTPS access from external IP"
    echo "3. Run: nmap -Pn <server-ip> (from external) to verify only 22, 80, 443 open"
    echo "4. Monitor logs: sudo tail -f /var/log/ufw.log"
else
    echo "UFW not enabled. Rules added but not active."
    echo "Run 'sudo ufw enable' when ready."
fi
