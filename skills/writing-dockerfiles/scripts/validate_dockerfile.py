#!/usr/bin/env python3
"""
Dockerfile Validation Script

Validates Dockerfiles against best practices:
- Multi-stage builds for production
- Non-root users
- Version pinning
- BuildKit syntax
- No secrets in ENV vars
- Minimal base images

Usage:
    python3 validate_dockerfile.py Dockerfile
    python3 validate_dockerfile.py --verbose Dockerfile
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class DockerfileValidator:
    def __init__(self, filepath: Path, verbose: bool = False):
        self.filepath = filepath
        self.verbose = verbose
        self.content = self.filepath.read_text()
        self.lines = self.content.splitlines()
        self.errors = []
        self.warnings = []
        self.suggestions = []

    def validate(self) -> Tuple[List[str], List[str], List[str]]:
        """Run all validations and return errors, warnings, suggestions."""
        self.check_buildkit_syntax()
        self.check_version_pinning()
        self.check_multistage_build()
        self.check_user_configuration()
        self.check_secrets()
        self.check_cache_mounts()
        self.check_layer_optimization()
        self.check_base_image()
        self.check_healthcheck()

        return self.errors, self.warnings, self.suggestions

    def check_buildkit_syntax(self):
        """Check for BuildKit syntax directive."""
        if not self.content.startswith("# syntax=docker/dockerfile:"):
            self.warnings.append(
                "Missing BuildKit syntax directive. Add: # syntax=docker/dockerfile:1"
            )

    def check_version_pinning(self):
        """Check if base images use version tags."""
        from_pattern = re.compile(r"^FROM\s+([^\s]+)", re.MULTILINE)
        matches = from_pattern.findall(self.content)

        for match in matches:
            if match.startswith("scratch") or match.startswith("gcr.io/distroless"):
                continue  # Scratch and distroless don't need version pinning

            if ":latest" in match:
                self.errors.append(f"Base image uses :latest tag: {match}")
            elif ":" not in match:
                self.errors.append(f"Base image missing version tag: {match}")

    def check_multistage_build(self):
        """Check for multi-stage builds."""
        from_count = len(re.findall(r"^FROM\s+", self.content, re.MULTILINE))

        if from_count == 1:
            self.suggestions.append(
                "Consider using multi-stage build for smaller images "
                "(separate build and runtime stages)"
            )

    def check_user_configuration(self):
        """Check for non-root user configuration."""
        has_user = re.search(r"^USER\s+", self.content, re.MULTILINE)

        if not has_user:
            self.warnings.append(
                "No USER directive found. Consider running as non-root user for security."
            )
        elif "USER root" in self.content or "USER 0" in self.content:
            self.errors.append("Running as root user (USER root or USER 0)")

    def check_secrets(self):
        """Check for secrets in ENV vars or build args."""
        # Check for suspicious ENV vars
        env_pattern = re.compile(
            r"ENV\s+.*(?:TOKEN|SECRET|PASSWORD|KEY|CREDENTIAL)", re.IGNORECASE
        )
        if env_pattern.search(self.content):
            self.errors.append(
                "Potential secret in ENV variable. Use BuildKit secret mounts instead."
            )

        # Check for suspicious ARG usage
        arg_pattern = re.compile(
            r"ARG\s+.*(?:TOKEN|SECRET|PASSWORD|KEY|CREDENTIAL)", re.IGNORECASE
        )
        if arg_pattern.search(self.content):
            self.warnings.append(
                "Potential secret in ARG. Consider using BuildKit secret mounts."
            )

    def check_cache_mounts(self):
        """Check for BuildKit cache mounts in package manager commands."""
        package_managers = {
            "pip install": "/root/.cache/pip",
            "npm ci": "/root/.npm",
            "pnpm install": "/root/.local/share/pnpm/store",
            "yarn install": "/usr/local/share/.cache/yarn",
            "go mod download": "/go/pkg/mod",
            "cargo build": "/usr/local/cargo/registry",
        }

        for cmd, cache_path in package_managers.items():
            if cmd in self.content:
                cache_mount = f"--mount=type=cache,target={cache_path}"
                if cache_mount not in self.content:
                    self.suggestions.append(
                        f"Consider adding cache mount for '{cmd}': "
                        f"RUN --mount=type=cache,target={cache_path} {cmd}"
                    )

    def check_layer_optimization(self):
        """Check for layer optimization patterns."""
        # Check if COPY . comes before package install
        copy_all = re.search(r"COPY\s+\.\s+", self.content)
        pip_install = re.search(r"pip install", self.content)
        npm_ci = re.search(r"npm ci", self.content)

        if copy_all and (pip_install or npm_ci):
            if copy_all.start() < (pip_install.start() if pip_install else npm_ci.start()):
                self.suggestions.append(
                    "Copy dependency manifests before source code for better layer caching. "
                    "Example: COPY requirements.txt . → RUN pip install → COPY . ."
                )

    def check_base_image(self):
        """Check base image choices."""
        # Check for full images in production
        full_images = re.findall(
            r"FROM\s+(python|node|golang|rust):\d+\.\d+\s*$", self.content, re.MULTILINE
        )
        if full_images:
            self.suggestions.append(
                f"Consider using slim/alpine variants for smaller images: "
                f"{', '.join(full_images)} → -slim or -alpine"
            )

        # Check Python alpine with compiled dependencies
        if "FROM python:" in self.content and "-alpine" in self.content:
            if any(
                pkg in self.content
                for pkg in ["numpy", "pandas", "scipy", "pillow", "psycopg2"]
            ):
                self.warnings.append(
                    "Python alpine with compiled dependencies detected. "
                    "Consider using -slim base to avoid compilation issues."
                )

    def check_healthcheck(self):
        """Check for health check configuration."""
        if "HEALTHCHECK" not in self.content:
            self.suggestions.append(
                "Consider adding HEALTHCHECK for container health monitoring"
            )

    def print_results(self):
        """Print validation results."""
        print(f"Validating: {self.filepath}")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if self.suggestions:
            print(f"\n💡 SUGGESTIONS ({len(self.suggestions)}):")
            for suggestion in self.suggestions:
                print(f"  - {suggestion}")

        print("\n" + "=" * 60)

        if not self.errors and not self.warnings:
            print("✅ Validation PASSED - No errors or warnings")
            return 0
        elif not self.errors:
            print(f"⚠️  Validation PASSED with {len(self.warnings)} warning(s)")
            return 0
        else:
            print(f"❌ Validation FAILED - {len(self.errors)} error(s) must be fixed")
            return 1


def main():
    parser = argparse.ArgumentParser(description="Validate Dockerfile against best practices")
    parser.add_argument("dockerfile", type=Path, help="Path to Dockerfile")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output"
    )

    args = parser.parse_args()

    if not args.dockerfile.exists():
        print(f"Error: Dockerfile not found: {args.dockerfile}")
        return 1

    validator = DockerfileValidator(args.dockerfile, args.verbose)
    errors, warnings, suggestions = validator.validate()

    exit_code = validator.print_results()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
