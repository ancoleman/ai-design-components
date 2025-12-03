#!/usr/bin/env python3
"""
S3 Connection Testing Tool

Tests S3 bucket connectivity, permissions, and file listing.
Useful for validating AWS credentials before ingestion.

Usage:
    python test_s3_connection.py --bucket my-bucket
    python test_s3_connection.py --bucket my-bucket --prefix data/2024/
    python test_s3_connection.py --bucket my-bucket --profile production
"""

import argparse
import sys
from datetime import datetime

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    print("Error: boto3 library not installed")
    print("Install with: pip install boto3")
    sys.exit(1)


def test_connection(bucket: str, prefix: str = "", profile: str = None) -> bool:
    """Test S3 bucket connection and permissions."""

    # Create session
    if profile:
        session = boto3.Session(profile_name=profile)
        print(f"Using AWS profile: {profile}")
    else:
        session = boto3.Session()
        print("Using default AWS credentials")

    s3 = session.client("s3")
    print(f"Bucket: {bucket}")
    print(f"Prefix: {prefix or '(root)'}")
    print("")

    # Test 1: Check bucket exists and is accessible
    print("1. Testing bucket access...")
    try:
        s3.head_bucket(Bucket=bucket)
        print("   Bucket exists and is accessible")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            print(f"   Bucket not found: {bucket}")
        elif error_code == "403":
            print(f"   Access denied to bucket: {bucket}")
        else:
            print(f"   Error: {e}")
        return False
    except NoCredentialsError:
        print("   No AWS credentials found")
        print("   Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return False

    # Test 2: List objects
    print("2. Testing list objects permission...")
    try:
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=10
        )
        count = response.get("KeyCount", 0)
        print(f"   Found {count} objects (showing up to 10)")

        if "Contents" in response:
            for obj in response["Contents"][:5]:
                size = obj["Size"]
                key = obj["Key"]
                print(f"     - {key} ({format_size(size)})")
            if count > 5:
                print(f"     ... and {count - 5} more")
    except ClientError as e:
        print(f"   List objects failed: {e}")
        return False

    # Test 3: Check read permission on first object
    print("3. Testing read permission...")
    if "Contents" in response and response["Contents"]:
        test_key = response["Contents"][0]["Key"]
        try:
            s3.head_object(Bucket=bucket, Key=test_key)
            print(f"   Can read: {test_key}")
        except ClientError as e:
            print(f"   Read permission denied: {e}")
            return False
    else:
        print("   No objects to test (bucket may be empty)")

    # Test 4: Check region
    print("4. Checking bucket region...")
    try:
        location = s3.get_bucket_location(Bucket=bucket)
        region = location.get("LocationConstraint") or "us-east-1"
        print(f"   Bucket region: {region}")
    except ClientError:
        print("   Could not determine region")

    print("")
    print("Connection test PASSED")
    return True


def format_size(size: int) -> str:
    """Format byte size to human readable."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def main():
    parser = argparse.ArgumentParser(
        description="Test S3 bucket connectivity"
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="S3 bucket name"
    )
    parser.add_argument(
        "--prefix",
        default="",
        help="Object prefix to filter (optional)"
    )
    parser.add_argument(
        "--profile",
        help="AWS profile name (optional)"
    )

    args = parser.parse_args()

    success = test_connection(
        bucket=args.bucket,
        prefix=args.prefix,
        profile=args.profile
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
