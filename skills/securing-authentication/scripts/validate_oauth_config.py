#!/usr/bin/env python3
"""
OAuth 2.1 Configuration Validator

Validates OAuth 2.1 configuration compliance according to RFC 9449 (2025 standard).

OAuth 2.1 Mandatory Requirements:
- PKCE (Proof Key for Code Exchange) for ALL authorization code flows
- Exact redirect URI matching (no wildcards)
- NO implicit grant flow (removed in OAuth 2.1)
- NO resource owner password credentials grant (removed in OAuth 2.1)

Usage:
    python validate_oauth_config.py --config oauth_config.json
    python validate_oauth_config.py --config oauth_config.yaml
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

try:
    import yaml
except ImportError:
    yaml = None


def validate_pkce_requirement(config: Dict[str, Any]) -> List[str]:
    """Validate PKCE is mandatory for authorization code flows."""
    errors = []

    flows = config.get("flows", {})
    auth_code = flows.get("authorization_code", {})

    if auth_code:
        pkce_required = auth_code.get("pkce_required", False)
        if not pkce_required:
            errors.append(
                "❌ OAuth 2.1: PKCE MUST be required for authorization code flow"
            )

    return errors


def validate_forbidden_grants(config: Dict[str, Any]) -> List[str]:
    """Validate forbidden grant types are not used."""
    errors = []

    flows = config.get("flows", {})

    # Implicit grant is FORBIDDEN in OAuth 2.1
    if "implicit" in flows:
        errors.append(
            "❌ OAuth 2.1: Implicit grant is FORBIDDEN (security vulnerability)"
        )

    # Resource owner password credentials is FORBIDDEN
    if "password" in flows or "resource_owner_password" in flows:
        errors.append(
            "❌ OAuth 2.1: Password grant is FORBIDDEN (use authorization code + PKCE)"
        )

    return errors


def validate_redirect_uris(config: Dict[str, Any]) -> List[str]:
    """Validate redirect URIs use exact matching."""
    errors = []

    redirect_uris = config.get("redirect_uris", [])

    for uri in redirect_uris:
        # Check for wildcards
        if "*" in uri:
            errors.append(
                f"❌ OAuth 2.1: Redirect URI '{uri}' uses wildcards (must be exact match)"
            )

        # Check for http:// in production
        if uri.startswith("http://") and "localhost" not in uri:
            errors.append(
                f"⚠️  Warning: Redirect URI '{uri}' uses http:// (https:// recommended for production)"
            )

    if not redirect_uris:
        errors.append(
            "⚠️  Warning: No redirect URIs configured"
        )

    return errors


def validate_token_lifetimes(config: Dict[str, Any]) -> List[str]:
    """Validate token lifetimes follow best practices."""
    errors = []

    tokens = config.get("tokens", {})

    # Access token lifetime (recommended: 5-15 minutes)
    access_ttl = tokens.get("access_token_ttl", 0)
    if access_ttl == 0:
        errors.append("⚠️  Warning: access_token_ttl not configured")
    elif access_ttl > 900:  # 15 minutes
        errors.append(
            f"⚠️  Warning: access_token_ttl is {access_ttl}s (>15 minutes). Recommended: 300-900s (5-15 min)"
        )

    # Refresh token lifetime (recommended: 1-7 days)
    refresh_ttl = tokens.get("refresh_token_ttl", 0)
    if refresh_ttl > 0:
        if refresh_ttl < 86400:  # 1 day
            errors.append(
                f"⚠️  Warning: refresh_token_ttl is {refresh_ttl}s (<1 day). Recommended: 86400-604800s (1-7 days)"
            )
        elif refresh_ttl > 604800:  # 7 days
            errors.append(
                f"⚠️  Warning: refresh_token_ttl is {refresh_ttl}s (>7 days). Recommended: 86400-604800s"
            )

    # Refresh token rotation
    rotation = tokens.get("refresh_token_rotation", False)
    if not rotation and refresh_ttl > 0:
        errors.append(
            "⚠️  Warning: Refresh token rotation not enabled (recommended for security)"
        )

    return errors


def validate_jwt_algorithm(config: Dict[str, Any]) -> List[str]:
    """Validate JWT algorithm is OAuth 2.1 compliant."""
    errors = []

    jwt_config = config.get("jwt", {})
    algorithm = jwt_config.get("algorithm", "")

    # OAuth 2.1 recommended algorithms
    recommended = ["EdDSA", "ES256", "ES384", "ES512"]
    deprecated = ["RS256", "HS256", "none"]

    if not algorithm:
        errors.append("⚠️  Warning: JWT algorithm not specified")
    elif algorithm in deprecated:
        if algorithm == "none":
            errors.append(
                f"❌ CRITICAL: JWT algorithm 'none' is a SECURITY VULNERABILITY"
            )
        else:
            errors.append(
                f"⚠️  Warning: Algorithm '{algorithm}' is not recommended. Use EdDSA or ES256"
            )
    elif algorithm not in recommended:
        errors.append(
            f"⚠️  Warning: Unknown algorithm '{algorithm}'. Recommended: {', '.join(recommended)}"
        )

    # Check for algorithm switching prevention
    verify_alg = jwt_config.get("verify_algorithm", True)
    if not verify_alg:
        errors.append(
            "❌ CRITICAL: Algorithm verification disabled (enables alg: none attacks)"
        )

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate OAuth 2.1 configuration compliance"
    )
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to OAuth configuration file (JSON or YAML)"
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config_data = args.config.read_text()

        if args.config.suffix == ".json":
            config = json.loads(config_data)
        elif args.config.suffix in [".yaml", ".yml"]:
            if yaml is None:
                print("❌ Error: PyYAML not installed for YAML support")
                print("Install with: pip install pyyaml")
                sys.exit(1)
            config = yaml.safe_load(config_data)
        else:
            print(f"❌ Error: Unsupported file format: {args.config.suffix}")
            print("   Supported: .json, .yaml, .yml")
            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ Error: Config file not found: {args.config}")
        sys.exit(1)
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        print(f"❌ Error: Invalid config file format: {e}")
        sys.exit(1)

    # Run validation checks
    print(f"🔍 Validating OAuth 2.1 configuration: {args.config}")
    print("")

    all_errors = []

    # Check PKCE requirement
    all_errors.extend(validate_pkce_requirement(config))

    # Check forbidden grants
    all_errors.extend(validate_forbidden_grants(config))

    # Check redirect URIs
    all_errors.extend(validate_redirect_uris(config))

    # Check token lifetimes
    all_errors.extend(validate_token_lifetimes(config))

    # Check JWT algorithm
    all_errors.extend(validate_jwt_algorithm(config))

    # Print results
    if all_errors:
        print("Validation Issues Found:")
        print("")
        for error in all_errors:
            print(f"  {error}")
        print("")

        # Count critical vs warnings
        critical = sum(1 for e in all_errors if "❌" in e)
        warnings = sum(1 for e in all_errors if "⚠️" in e)

        print(f"Summary: {critical} critical errors, {warnings} warnings")

        if critical > 0:
            print("")
            print("❌ VALIDATION FAILED (critical errors must be fixed)")
            sys.exit(1)
        else:
            print("")
            print("⚠️  VALIDATION PASSED WITH WARNINGS")
            sys.exit(0)
    else:
        print("✅ All OAuth 2.1 compliance checks passed!")
        print("")
        print("Configuration is compliant with:")
        print("  - PKCE requirement for authorization code flows")
        print("  - No forbidden grant types (implicit, password)")
        print("  - Exact redirect URI matching")
        print("  - Secure JWT algorithms (EdDSA or ES256)")
        print("  - Recommended token lifetimes")
        sys.exit(0)


if __name__ == "__main__":
    main()
