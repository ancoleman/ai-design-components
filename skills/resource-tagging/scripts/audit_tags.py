#!/usr/bin/env python3
"""
Multi-Cloud Tag Compliance Audit Script

Audits resource tagging compliance across AWS, Azure, and GCP.

Dependencies:
    pip install boto3 azure-mgmt-resource google-cloud-asset tabulate

Usage:
    # Audit AWS only
    python audit_tags.py --cloud aws

    # Audit all clouds
    python audit_tags.py --cloud all

    # Export to CSV
    python audit_tags.py --cloud aws --output aws_audit.csv

    # Specify custom required tags
    python audit_tags.py --cloud aws --tags Environment Owner CostCenter
"""

import argparse
import csv
import sys
from datetime import datetime
from typing import List, Dict, Optional
from tabulate import tabulate

# Required tags (default)
DEFAULT_REQUIRED_TAGS = ['Environment', 'Owner', 'CostCenter', 'Project', 'ManagedBy']

# Cloud-specific imports (optional - install as needed)
try:
    import boto3
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

try:
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

try:
    from google.cloud import asset_v1
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False


class TagAuditor:
    """Base class for tag auditing."""

    def __init__(self, required_tags: List[str]):
        self.required_tags = required_tags
        self.non_compliant_resources = []

    def audit(self) -> List[Dict]:
        """Run audit and return non-compliant resources."""
        raise NotImplementedError

    def calculate_compliance(self, total: int, compliant: int) -> float:
        """Calculate compliance percentage."""
        if total == 0:
            return 100.0
        return (compliant / total) * 100


class AWSTagAuditor(TagAuditor):
    """AWS tag compliance auditor."""

    RESOURCE_TYPES = [
        'ec2:instance',
        'rds:db',
        's3:bucket',
        'lambda:function',
        'dynamodb:table',
    ]

    def audit(self) -> List[Dict]:
        """Audit AWS resources for tag compliance."""
        if not AWS_AVAILABLE:
            print("ERROR: boto3 not installed. Run: pip install boto3")
            return []

        client = boto3.client('resourcegroupstaggingapi')
        non_compliant = []

        for resource_type in self.RESOURCE_TYPES:
            try:
                paginator = client.get_paginator('get_resources')
                page_iterator = paginator.paginate(
                    ResourceTypeFilters=[resource_type]
                )

                for page in page_iterator:
                    for resource in page['ResourceTagMappingList']:
                        arn = resource['ResourceARN']
                        tags = {tag['Key']: tag['Value'] for tag in resource.get('Tags', [])}

                        # Check which required tags are missing
                        missing_tags = [tag for tag in self.required_tags if tag not in tags]

                        if missing_tags:
                            non_compliant.append({
                                'Cloud': 'AWS',
                                'ResourceARN': arn,
                                'ResourceType': resource_type,
                                'MissingTags': ', '.join(missing_tags),
                                'ExistingTags': str(tags)
                            })

            except Exception as e:
                print(f"Warning: Error auditing {resource_type}: {e}")

        self.non_compliant_resources = non_compliant
        return non_compliant


class AzureTagAuditor(TagAuditor):
    """Azure tag compliance auditor."""

    def __init__(self, required_tags: List[str], subscription_id: str):
        super().__init__(required_tags)
        self.subscription_id = subscription_id

    def audit(self) -> List[Dict]:
        """Audit Azure resources for tag compliance."""
        if not AZURE_AVAILABLE:
            print("ERROR: azure-mgmt-resource not installed. Run: pip install azure-mgmt-resource azure-identity")
            return []

        credential = DefaultAzureCredential()
        client = ResourceManagementClient(credential, self.subscription_id)
        non_compliant = []

        try:
            resources = client.resources.list()

            for resource in resources:
                tags = resource.tags or {}

                # Check which required tags are missing (case-insensitive for Azure)
                missing_tags = [tag for tag in self.required_tags if tag not in tags]

                if missing_tags:
                    non_compliant.append({
                        'Cloud': 'Azure',
                        'ResourceARN': resource.id,
                        'ResourceType': resource.type,
                        'MissingTags': ', '.join(missing_tags),
                        'ExistingTags': str(tags)
                    })

        except Exception as e:
            print(f"ERROR: Failed to audit Azure resources: {e}")

        self.non_compliant_resources = non_compliant
        return non_compliant


class GCPLabelAuditor(TagAuditor):
    """GCP label compliance auditor."""

    def __init__(self, required_tags: List[str], organization_id: Optional[str] = None, project_id: Optional[str] = None):
        # GCP labels are lowercase
        super().__init__([tag.lower() for tag in required_tags])
        self.organization_id = organization_id
        self.project_id = project_id

    def audit(self) -> List[Dict]:
        """Audit GCP resources for label compliance."""
        if not GCP_AVAILABLE:
            print("ERROR: google-cloud-asset not installed. Run: pip install google-cloud-asset")
            return []

        client = asset_v1.AssetServiceClient()
        non_compliant = []

        scope = f"organizations/{self.organization_id}" if self.organization_id else f"projects/{self.project_id}"

        try:
            # Search for resources
            request = asset_v1.SearchAllResourcesRequest(
                scope=scope,
                asset_types=[
                    "compute.googleapis.com/Instance",
                    "storage.googleapis.com/Bucket",
                ]
            )

            page_result = client.search_all_resources(request=request)

            for resource in page_result:
                labels = resource.labels or {}

                # Check which required labels are missing
                missing_labels = [label for label in self.required_tags if label not in labels]

                if missing_labels:
                    non_compliant.append({
                        'Cloud': 'GCP',
                        'ResourceARN': resource.name,
                        'ResourceType': resource.asset_type,
                        'MissingTags': ', '.join(missing_labels),
                        'ExistingTags': str(labels)
                    })

        except Exception as e:
            print(f"ERROR: Failed to audit GCP resources: {e}")

        self.non_compliant_resources = non_compliant
        return non_compliant


def generate_csv_report(resources: List[Dict], output_file: str):
    """Generate CSV compliance report."""
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Cloud', 'ResourceARN', 'ResourceType', 'MissingTags', 'ExistingTags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for resource in resources:
            writer.writerow(resource)

    print(f"\nCompliance report generated: {output_file}")


def print_summary(auditors: List[TagAuditor]):
    """Print audit summary."""
    print("\n" + "="*70)
    print(" TAG COMPLIANCE AUDIT SUMMARY")
    print("="*70)

    for auditor in auditors:
        cloud = auditor.__class__.__name__.replace('TagAuditor', '').replace('LabelAuditor', '')
        non_compliant_count = len(auditor.non_compliant_resources)

        print(f"\n{cloud}:")
        print(f"  Non-compliant resources: {non_compliant_count}")

        if non_compliant_count > 0 and non_compliant_count <= 10:
            # Print sample of non-compliant resources
            print(f"\n  Sample non-compliant resources:")
            table_data = []
            for resource in auditor.non_compliant_resources[:10]:
                table_data.append([
                    resource['ResourceType'],
                    resource['ResourceARN'][:60] + '...' if len(resource['ResourceARN']) > 60 else resource['ResourceARN'],
                    resource['MissingTags']
                ])
            print(tabulate(table_data, headers=['Type', 'Resource', 'Missing Tags'], tablefmt='simple'))

    print("\n" + "="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Multi-cloud tag compliance auditor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit AWS only
  python audit_tags.py --cloud aws

  # Audit all clouds
  python audit_tags.py --cloud all

  # Export to CSV
  python audit_tags.py --cloud aws --output aws_audit.csv

  # Custom required tags
  python audit_tags.py --cloud aws --tags Environment Owner Project
        """
    )

    parser.add_argument('--cloud', choices=['aws', 'azure', 'gcp', 'all'], default='all',
                        help='Cloud provider to audit (default: all)')
    parser.add_argument('--tags', nargs='+', default=DEFAULT_REQUIRED_TAGS,
                        help=f'Required tags to check (default: {" ".join(DEFAULT_REQUIRED_TAGS)})')
    parser.add_argument('--output', type=str,
                        help='Output CSV file path')
    parser.add_argument('--azure-subscription', type=str,
                        help='Azure subscription ID (required for Azure audit)')
    parser.add_argument('--gcp-org', type=str,
                        help='GCP organization ID (format: 123456789)')
    parser.add_argument('--gcp-project', type=str,
                        help='GCP project ID (alternative to --gcp-org)')

    args = parser.parse_args()

    print("="*70)
    print(" MULTI-CLOUD TAG COMPLIANCE AUDIT")
    print("="*70)
    print(f"Required tags: {', '.join(args.tags)}")
    print(f"Clouds: {args.cloud}")
    print()

    auditors = []
    all_non_compliant = []

    # AWS audit
    if args.cloud in ['aws', 'all']:
        if not AWS_AVAILABLE:
            print("WARNING: boto3 not installed. Skipping AWS audit.")
        else:
            print("Auditing AWS resources...")
            aws_auditor = AWSTagAuditor(args.tags)
            non_compliant = aws_auditor.audit()
            auditors.append(aws_auditor)
            all_non_compliant.extend(non_compliant)
            print(f"  Found {len(non_compliant)} non-compliant AWS resources")

    # Azure audit
    if args.cloud in ['azure', 'all']:
        if not AZURE_AVAILABLE:
            print("WARNING: azure-mgmt-resource not installed. Skipping Azure audit.")
        elif not args.azure_subscription:
            print("WARNING: --azure-subscription required for Azure audit. Skipping.")
        else:
            print("Auditing Azure resources...")
            azure_auditor = AzureTagAuditor(args.tags, args.azure_subscription)
            non_compliant = azure_auditor.audit()
            auditors.append(azure_auditor)
            all_non_compliant.extend(non_compliant)
            print(f"  Found {len(non_compliant)} non-compliant Azure resources")

    # GCP audit
    if args.cloud in ['gcp', 'all']:
        if not GCP_AVAILABLE:
            print("WARNING: google-cloud-asset not installed. Skipping GCP audit.")
        elif not args.gcp_org and not args.gcp_project:
            print("WARNING: --gcp-org or --gcp-project required for GCP audit. Skipping.")
        else:
            print("Auditing GCP resources...")
            gcp_auditor = GCPLabelAuditor(args.tags, args.gcp_org, args.gcp_project)
            non_compliant = gcp_auditor.audit()
            auditors.append(gcp_auditor)
            all_non_compliant.extend(non_compliant)
            print(f"  Found {len(non_compliant)} non-compliant GCP resources")

    # Generate report
    if args.output and all_non_compliant:
        generate_csv_report(all_non_compliant, args.output)

    # Print summary
    if auditors:
        print_summary(auditors)
    else:
        print("\nERROR: No cloud providers were audited. Check dependencies and arguments.")
        sys.exit(1)

    # Exit code based on compliance
    if all_non_compliant:
        sys.exit(1)  # Non-zero exit for CI/CD pipelines
    else:
        print("\n✓ All resources are compliant!")
        sys.exit(0)


if __name__ == '__main__':
    main()
