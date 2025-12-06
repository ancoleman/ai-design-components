#!/bin/bash

# Security Architecture Checklist
# Automated checklist for security architecture review

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "Security Architecture Checklist"
echo "========================================="
echo ""

# Function to check with user
check_item() {
    local category="$1"
    local item="$2"
    echo -e "${YELLOW}[$category]${NC} $item"
    read -p "  Implemented? (y/n): " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "  ${GREEN}✓ Complete${NC}"
        return 0
    else
        echo -e "  ${RED}✗ Not Implemented${NC}"
        return 1
    fi
}

total=0
complete=0

echo "=== DEFENSE IN DEPTH LAYERS ==="
echo ""

# Layer 2: Network Perimeter
((total++))
if check_item "Layer 2" "Next-gen firewall (NGFW) deployed?"; then ((complete++)); fi
((total++))
if check_item "Layer 2" "Web Application Firewall (WAF) configured?"; then ((complete++)); fi
((total++))
if check_item "Layer 2" "DDoS protection enabled?"; then ((complete++)); fi

echo ""

# Layer 3: Network Segmentation
((total++))
if check_item "Layer 3" "Network segmented into zones (DMZ, Web, App, Data)?"; then ((complete++)); fi
((total++))
if check_item "Layer 3" "Security groups/NACLs configured with least privilege?"; then ((complete++)); fi

echo ""

# Layer 4: Endpoint Protection
((total++))
if check_item "Layer 4" "Endpoint Detection & Response (EDR) deployed?"; then ((complete++)); fi
((total++))
if check_item "Layer 4" "Patch management automated?"; then ((complete++)); fi
((total++))
if check_item "Layer 4" "Full-disk encryption enabled on endpoints?"; then ((complete++)); fi

echo ""

# Layer 5: Application Security
((total++))
if check_item "Layer 5" "SAST/DAST integrated in CI/CD?"; then ((complete++)); fi
((total++))
if check_item "Layer 5" "Input validation on all user inputs?"; then ((complete++)); fi
((total++))
if check_item "Layer 5" "Parameterized queries used (no raw SQL)?"; then ((complete++)); fi
((total++))
if check_item "Layer 5" "Dependency scanning enabled (SCA)?"; then ((complete++)); fi

echo ""

# Layer 6: Data Security
((total++))
if check_item "Layer 6" "Data encrypted at rest (AES-256)?"; then ((complete++)); fi
((total++))
if check_item "Layer 6" "Data encrypted in transit (TLS 1.3)?"; then ((complete++)); fi
((total++))
if check_item "Layer 6" "Key management system deployed (KMS/HSM)?"; then ((complete++)); fi
((total++))
if check_item "Layer 6" "Backup and recovery tested (3-2-1 rule)?"; then ((complete++)); fi

echo ""

# Layer 7: Identity & Access Management
((total++))
if check_item "Layer 7" "Multi-factor authentication (MFA) enforced for all users?"; then ((complete++)); fi
((total++))
if check_item "Layer 7" "Single Sign-On (SSO) deployed?"; then ((complete++)); fi
((total++))
if check_item "Layer 7" "Role-based access control (RBAC) implemented?"; then ((complete++)); fi
((total++))
if check_item "Layer 7" "Privileged access management (PAM) with JIT access?"; then ((complete++)); fi
((total++))
if check_item "Layer 7" "Standing admin credentials removed?"; then ((complete++)); fi

echo ""

# Layer 8: Behavioral Analytics
((total++))
if check_item "Layer 8" "User & Entity Behavior Analytics (UEBA) deployed?"; then ((complete++)); fi
((total++))
if check_item "Layer 8" "Anomaly detection configured?"; then ((complete++)); fi

echo ""

# Layer 9: Security Operations
((total++))
if check_item "Layer 9" "SIEM deployed and collecting logs?"; then ((complete++)); fi
((total++))
if check_item "Layer 9" "Incident response plan documented and tested?"; then ((complete++)); fi
((total++))
if check_item "Layer 9" "Security monitoring 24/7 or managed SOC?"; then ((complete++)); fi

echo ""
echo "=== ZERO TRUST ARCHITECTURE ==="
echo ""

((total++))
if check_item "ZTA" "Identity provider (IdP) with SSO deployed?"; then ((complete++)); fi
((total++))
if check_item "ZTA" "Device posture checks before access?"; then ((complete++)); fi
((total++))
if check_item "ZTA" "Micro-segmentation implemented for critical assets?"; then ((complete++)); fi
((total++))
if check_item "ZTA" "ZTNA deployed (replacing VPN)?"; then ((complete++)); fi
((total++))
if check_item "ZTA" "Continuous verification and monitoring?"; then ((complete++)); fi

echo ""
echo "=== THREAT MODELING ==="
echo ""

((total++))
if check_item "Threat Model" "Threat model created for critical applications?"; then ((complete++)); fi
((total++))
if check_item "Threat Model" "STRIDE or PASTA methodology used?"; then ((complete++)); fi
((total++))
if check_item "Threat Model" "Threats prioritized by risk (DREAD scoring)?"; then ((complete++)); fi
((total++))
if check_item "Threat Model" "Mitigations designed and implemented?"; then ((complete++)); fi

echo ""
echo "=== SUPPLY CHAIN SECURITY ==="
echo ""

((total++))
if check_item "Supply Chain" "SBOM generated for all applications?"; then ((complete++)); fi
((total++))
if check_item "Supply Chain" "Dependency scanning in CI/CD?"; then ((complete++)); fi
((total++))
if check_item "Supply Chain" "SLSA Level 2+ achieved (hosted build platform)?"; then ((complete++)); fi
((total++))
if check_item "Supply Chain" "Automated dependency updates (security patches)?"; then ((complete++)); fi

echo ""
echo "=== COMPLIANCE FRAMEWORKS ==="
echo ""

((total++))
if check_item "Compliance" "Controls mapped to framework (NIST CSF, CIS Controls, ISO 27001)?"; then ((complete++)); fi
((total++))
if check_item "Compliance" "Security policies documented and approved?"; then ((complete++)); fi
((total++))
if check_item "Compliance" "Regular security audits conducted?"; then ((complete++)); fi

echo ""
echo "========================================="
echo "RESULTS"
echo "========================================="

percentage=$((complete * 100 / total))

echo ""
echo "Total Items: $total"
echo "Completed: $complete"
echo "Percentage: ${percentage}%"
echo ""

if [ $percentage -ge 90 ]; then
    echo -e "${GREEN}✓ Excellent security posture!${NC}"
elif [ $percentage -ge 70 ]; then
    echo -e "${YELLOW}⚠ Good security posture, some improvements needed.${NC}"
elif [ $percentage -ge 50 ]; then
    echo -e "${YELLOW}⚠ Moderate security posture, significant gaps exist.${NC}"
else
    echo -e "${RED}✗ Poor security posture, immediate action required!${NC}"
fi

echo ""
echo "========================================="
