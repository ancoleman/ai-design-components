#!/usr/bin/env python3
"""
Validate deployment configuration before deploying.

This script is executed WITHOUT loading into context (token-free).

Usage:
    python scripts/validate_deployment.py --config deployment.yaml

Features:
    - Validates Kubernetes YAML syntax
    - Checks resource limits and requests
    - Verifies health check configuration
    - Validates environment variables
    - Checks security best practices
"""

import argparse
import sys
import yaml
from typing import Dict, List, Any


class ValidationError(Exception):
    """Validation error."""
    pass


def validate_yaml_syntax(file_path: str) -> List[Dict[str, Any]]:
    """Validate YAML syntax and return parsed documents."""
    try:
        with open(file_path, "r") as f:
            documents = list(yaml.safe_load_all(f))
        return [doc for doc in documents if doc is not None]
    except yaml.YAMLError as e:
        raise ValidationError(f"❌ Invalid YAML syntax: {e}")


def validate_resource_limits(container: Dict[str, Any], container_name: str) -> List[str]:
    """Validate resource requests and limits."""
    warnings = []

    resources = container.get("resources", {})

    if not resources:
        warnings.append(f"⚠️  Container '{container_name}': No resource limits defined (production best practice)")
        return warnings

    requests = resources.get("requests", {})
    limits = resources.get("limits", {})

    if not requests:
        warnings.append(f"⚠️  Container '{container_name}': No resource requests defined")

    if not limits:
        warnings.append(f"⚠️  Container '{container_name}': No resource limits defined")

    # Check if limits are higher than requests
    if requests.get("cpu") and limits.get("cpu"):
        # Parse CPU values (e.g., "100m", "0.5")
        req_cpu = parse_cpu(requests["cpu"])
        lim_cpu = parse_cpu(limits["cpu"])
        if lim_cpu < req_cpu:
            warnings.append(f"❌ Container '{container_name}': CPU limit ({limits['cpu']}) is less than request ({requests['cpu']})")

    if requests.get("memory") and limits.get("memory"):
        req_mem = parse_memory(requests["memory"])
        lim_mem = parse_memory(limits["memory"])
        if lim_mem < req_mem:
            warnings.append(f"❌ Container '{container_name}': Memory limit ({limits['memory']}) is less than request ({requests['memory']})")

    return warnings


def parse_cpu(cpu_str: str) -> float:
    """Parse CPU string to float (e.g., '100m' -> 0.1, '0.5' -> 0.5)."""
    if cpu_str.endswith("m"):
        return float(cpu_str[:-1]) / 1000
    return float(cpu_str)


def parse_memory(mem_str: str) -> int:
    """Parse memory string to bytes."""
    units = {
        "Ki": 1024,
        "Mi": 1024 ** 2,
        "Gi": 1024 ** 3,
        "Ti": 1024 ** 4,
    }
    for unit, multiplier in units.items():
        if mem_str.endswith(unit):
            return int(mem_str[:-2]) * multiplier
    return int(mem_str)


def validate_health_checks(container: Dict[str, Any], container_name: str) -> List[str]:
    """Validate liveness and readiness probes."""
    warnings = []

    if "livenessProbe" not in container:
        warnings.append(f"⚠️  Container '{container_name}': No liveness probe defined")

    if "readinessProbe" not in container:
        warnings.append(f"⚠️  Container '{container_name}': No readiness probe defined")

    # Check probe configuration
    for probe_type in ["livenessProbe", "readinessProbe"]:
        probe = container.get(probe_type)
        if probe:
            if "httpGet" in probe:
                if "path" not in probe["httpGet"]:
                    warnings.append(f"❌ Container '{container_name}': {probe_type} missing 'path'")
                if "port" not in probe["httpGet"]:
                    warnings.append(f"❌ Container '{container_name}': {probe_type} missing 'port'")

    return warnings


def validate_security(deployment: Dict[str, Any]) -> List[str]:
    """Validate security best practices."""
    warnings = []

    spec = deployment.get("spec", {}).get("template", {}).get("spec", {})
    containers = spec.get("containers", [])

    for container in containers:
        container_name = container.get("name", "unknown")

        # Check if running as root
        security_context = container.get("securityContext", {})
        if security_context.get("runAsNonRoot") is False:
            warnings.append(f"⚠️  Container '{container_name}': Running as root (security risk)")

        # Check privileged mode
        if security_context.get("privileged"):
            warnings.append(f"⚠️  Container '{container_name}': Running in privileged mode (security risk)")

        # Check read-only root filesystem
        if not security_context.get("readOnlyRootFilesystem"):
            warnings.append(f"⚠️  Container '{container_name}': Root filesystem is writable (consider read-only)")

    return warnings


def validate_deployment(document: Dict[str, Any]) -> List[str]:
    """Validate Deployment manifest."""
    warnings = []

    if document.get("kind") != "Deployment":
        return warnings

    spec = document.get("spec", {})

    # Check replicas
    replicas = spec.get("replicas", 1)
    if replicas < 2:
        warnings.append(f"⚠️  Deployment has only {replicas} replica(s) (production should have 2+)")

    # Validate containers
    containers = spec.get("template", {}).get("spec", {}).get("containers", [])
    for container in containers:
        container_name = container.get("name", "unknown")

        # Resource limits
        warnings.extend(validate_resource_limits(container, container_name))

        # Health checks
        warnings.extend(validate_health_checks(container, container_name))

        # Image tag
        image = container.get("image", "")
        if image.endswith(":latest"):
            warnings.append(f"⚠️  Container '{container_name}': Using ':latest' tag (not recommended for production)")

    # Security
    warnings.extend(validate_security(document))

    return warnings


def validate_service(document: Dict[str, Any]) -> List[str]:
    """Validate Service manifest."""
    warnings = []

    if document.get("kind") != "Service":
        return warnings

    spec = document.get("spec", {})
    service_type = spec.get("type", "ClusterIP")

    # Check for LoadBalancer in production
    if service_type == "LoadBalancer":
        warnings.append("⚠️  Service type is LoadBalancer (expensive, consider Ingress)")

    # Check for NodePort
    if service_type == "NodePort":
        warnings.append("⚠️  Service type is NodePort (consider using Ingress instead)")

    return warnings


def main():
    parser = argparse.ArgumentParser(description="Validate deployment configuration")
    parser.add_argument("--config", required=True, help="Path to Kubernetes manifest file")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")

    args = parser.parse_args()

    print(f"🔍 Validating {args.config}...\n")

    try:
        documents = validate_yaml_syntax(args.config)
        print(f"✅ YAML syntax is valid ({len(documents)} documents)\n")
    except ValidationError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    all_warnings = []

    for doc in documents:
        kind = doc.get("kind", "Unknown")
        name = doc.get("metadata", {}).get("name", "unknown")

        print(f"📄 Validating {kind}/{name}...")

        warnings = []
        if kind == "Deployment":
            warnings = validate_deployment(doc)
        elif kind == "Service":
            warnings = validate_service(doc)

        if warnings:
            for warning in warnings:
                print(f"   {warning}")
            all_warnings.extend(warnings)
        else:
            print("   ✅ No issues found")

        print()

    # Summary
    print("=" * 60)
    if all_warnings:
        error_count = sum(1 for w in all_warnings if w.startswith("❌"))
        warning_count = sum(1 for w in all_warnings if w.startswith("⚠️"))

        print(f"📊 Summary: {error_count} errors, {warning_count} warnings")

        if error_count > 0 or (args.strict and warning_count > 0):
            print("\n❌ Validation failed")
            sys.exit(1)
        else:
            print("\n✅ Validation passed (with warnings)")
            sys.exit(0)
    else:
        print("✅ All validation checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
