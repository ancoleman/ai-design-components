#!/usr/bin/env python3
"""
JWT Key Pair Generation Tool

Generates cryptographic key pairs for JWT signing following OAuth 2.1 best practices.
Supports EdDSA (Ed25519 - recommended) and ES256 (ECDSA P-256) algorithms.

OAuth 2.1 Requirements:
- EdDSA (Ed25519) or ES256 algorithms
- Never allow algorithm switching (alg: none attacks)
- Rotate keys periodically

Usage:
    python generate_jwt_keys.py --algorithm EdDSA --output-dir ./keys
    python generate_jwt_keys.py --algorithm ES256 --output-dir ./keys
"""

import argparse
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519, ec
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("❌ Error: cryptography library not installed")
    print("Install with: pip install cryptography")
    sys.exit(1)


def generate_ed25519_keys(output_dir: Path):
    """Generate EdDSA (Ed25519) key pair - OAuth 2.1 recommended."""

    print("🔐 Generating EdDSA (Ed25519) key pair...")
    print("   Algorithm: EdDSA (Ed25519)")
    print("   Security: 128-bit (equivalent to RSA 3072-bit)")
    print("   Performance: Fastest signature generation")
    print("")

    # Generate private key
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize private key (PEM format)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key (PEM format)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write to files
    private_path = output_dir / "jwt_private_key_ed25519.pem"
    public_path = output_dir / "jwt_public_key_ed25519.pem"

    private_path.write_bytes(private_pem)
    public_path.write_bytes(public_pem)

    # Set restrictive permissions (owner read/write only)
    private_path.chmod(0o600)
    public_path.chmod(0o644)

    print(f"✅ Private key saved: {private_path}")
    print(f"   Permissions: 600 (owner read/write only)")
    print(f"✅ Public key saved: {public_path}")
    print(f"   Permissions: 644 (world readable)")

    return private_path, public_path


def generate_es256_keys(output_dir: Path):
    """Generate ES256 (ECDSA P-256) key pair - OAuth 2.1 alternative."""

    print("🔐 Generating ES256 (ECDSA P-256) key pair...")
    print("   Algorithm: ES256 (ECDSA with P-256 curve)")
    print("   Security: 128-bit (equivalent to RSA 3072-bit)")
    print("   Performance: Fast signature generation")
    print("")

    # Generate private key
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # Serialize private key (PEM format)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key (PEM format)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write to files
    private_path = output_dir / "jwt_private_key_es256.pem"
    public_path = output_dir / "jwt_public_key_es256.pem"

    private_path.write_bytes(private_pem)
    public_path.write_bytes(public_pem)

    # Set restrictive permissions
    private_path.chmod(0o600)
    public_path.chmod(0o644)

    print(f"✅ Private key saved: {private_path}")
    print(f"   Permissions: 600 (owner read/write only)")
    print(f"✅ Public key saved: {public_path}")
    print(f"   Permissions: 644 (world readable)")

    return private_path, public_path


def print_usage_examples(algorithm: str, private_path: Path, public_path: Path):
    """Print usage examples for the generated keys."""

    print("")
    print("📝 Usage Examples:")
    print("")

    if algorithm == "EdDSA":
        print("**Python (joserfc):**")
        print("```python")
        print("from joserfc import jwt")
        print("from joserfc.jwk import OctKey")
        print("")
        print(f"with open('{private_path}', 'rb') as f:")
        print("    private_key = f.read()")
        print("")
        print("# Sign JWT")
        print("token = jwt.encode(")
        print("    {'alg': 'EdDSA'},")
        print("    {'sub': 'user123', 'exp': 1234567890},")
        print("    private_key")
        print(")")
        print("```")
        print("")
        print("**TypeScript (jose):**")
        print("```typescript")
        print("import * as jose from 'jose'")
        print("import fs from 'fs'")
        print("")
        print(f"const privateKey = await jose.importPKCS8(")
        print(f"  fs.readFileSync('{private_path}', 'utf8'),")
        print("  'EdDSA'")
        print(")")
        print("")
        print("const jwt = await new jose.SignJWT({ sub: 'user123' })")
        print("  .setProtectedHeader({ alg: 'EdDSA' })")
        print("  .setExpirationTime('15m')")
        print("  .sign(privateKey)")
        print("```")

    else:  # ES256
        print("**Python (joserfc):**")
        print("```python")
        print("from joserfc import jwt")
        print("")
        print(f"with open('{private_path}', 'rb') as f:")
        print("    private_key = f.read()")
        print("")
        print("token = jwt.encode(")
        print("    {'alg': 'ES256'},")
        print("    {'sub': 'user123', 'exp': 1234567890},")
        print("    private_key")
        print(")")
        print("```")

    print("")
    print("⚠️  Security Notes:")
    print("   1. NEVER commit private keys to version control")
    print("   2. Use environment variables or secret management (AWS Secrets Manager, Vault)")
    print("   3. Rotate keys periodically (e.g., every 90 days)")
    print("   4. Access tokens: 5-15 minutes")
    print("   5. Refresh tokens: 1-7 days with rotation")


def main():
    parser = argparse.ArgumentParser(
        description="Generate JWT key pairs for OAuth 2.1 compliant systems"
    )
    parser.add_argument(
        "--algorithm",
        choices=["EdDSA", "ES256"],
        default="EdDSA",
        help="Key algorithm (EdDSA recommended, ES256 alternative)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for keys (default: current directory)"
    )

    args = parser.parse_args()

    # Create output directory if needed
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Generate keys
    if args.algorithm == "EdDSA":
        private_path, public_path = generate_ed25519_keys(args.output_dir)
    else:
        private_path, public_path = generate_es256_keys(args.output_dir)

    # Print usage examples
    print_usage_examples(args.algorithm, private_path, public_path)

    print("")
    print("✅ Key generation complete!")


if __name__ == "__main__":
    main()
