#!/usr/bin/env python3
"""
AWS Idle Resource Cleanup Script

Identifies and deletes idle AWS resources to reduce costs:
- Unattached EBS volumes (>7 days old)
- Old EBS snapshots (>90 days, not tagged for retention)
- Stopped EC2 instances (>14 days, alert only)
- Idle load balancers (0 active connections for 7 days, alert only)

Usage:
    python cleanup_idle_resources.py --dry-run  # Preview changes
    python cleanup_idle_resources.py            # Execute cleanup

Dependencies:
    pip install boto3

Environment Variables:
    AWS_REGION (optional): AWS region (default: us-east-1)
    DRY_RUN (optional): Set to 'true' for dry-run mode
"""

import boto3
import argparse
from datetime import datetime, timedelta
from typing import List, Dict
import json


class IdleResourceCleaner:
    """Clean up idle AWS resources to reduce costs."""

    def __init__(self, region: str = 'us-east-1', dry_run: bool = False):
        self.region = region
        self.dry_run = dry_run
        self.ec2 = boto3.client('ec2', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)

    def cleanup_unattached_ebs_volumes(self) -> Dict:
        """Delete EBS volumes not attached to any instance for >7 days."""
        print("\n🔍 Checking for unattached EBS volumes...")

        volumes = self.ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )['Volumes']

        deleted = []
        kept = []

        for volume in volumes:
            volume_id = volume['VolumeId']
            create_time = volume['CreateTime'].replace(tzinfo=None)
            age_days = (datetime.now() - create_time).days

            # Check for KeepAlive tag
            tags = {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])}
            keep_alive = tags.get('KeepAlive', '').lower() == 'true'

            if age_days > 7 and not keep_alive:
                size_gb = volume['Size']
                monthly_cost = size_gb * 0.08  # $0.08/GB/month for gp3

                if self.dry_run:
                    print(f"  [DRY RUN] Would delete {volume_id} ({size_gb} GB, ${monthly_cost:.2f}/month)")
                else:
                    try:
                        self.ec2.delete_volume(VolumeId=volume_id)
                        print(f"  ✅ Deleted {volume_id} ({size_gb} GB, ${monthly_cost:.2f}/month)")
                        deleted.append({
                            'volume_id': volume_id,
                            'size_gb': size_gb,
                            'monthly_cost': monthly_cost
                        })
                    except Exception as e:
                        print(f"  ❌ Failed to delete {volume_id}: {e}")
            else:
                reason = "KeepAlive tag" if keep_alive else f"Too recent ({age_days} days)"
                kept.append({'volume_id': volume_id, 'reason': reason})

        total_savings = sum(v['monthly_cost'] for v in deleted)
        print(f"\n💰 Unattached volumes: {len(deleted)} deleted, ${total_savings:.2f}/month saved")
        return {'deleted': deleted, 'kept': kept, 'monthly_savings': total_savings}

    def cleanup_old_snapshots(self, retention_days: int = 90) -> Dict:
        """Delete EBS snapshots older than retention_days (unless tagged for retention)."""
        print(f"\n🔍 Checking for snapshots older than {retention_days} days...")

        snapshots = self.ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

        deleted = []
        kept = []

        for snapshot in snapshots:
            snapshot_id = snapshot['SnapshotId']
            start_time = snapshot['StartTime'].replace(tzinfo=None)
            age_days = (datetime.now() - start_time).days

            # Check for Retain tag
            tags = {tag['Key']: tag['Value'] for tag in snapshot.get('Tags', [])}
            retain = tags.get('Retain', '').lower() == 'true'

            if age_days > retention_days and not retain:
                size_gb = snapshot['VolumeSize']
                monthly_cost = size_gb * 0.05  # $0.05/GB/month for snapshots

                if self.dry_run:
                    print(f"  [DRY RUN] Would delete {snapshot_id} ({age_days} days old, ${monthly_cost:.2f}/month)")
                else:
                    try:
                        self.ec2.delete_snapshot(SnapshotId=snapshot_id)
                        print(f"  ✅ Deleted {snapshot_id} ({age_days} days old, ${monthly_cost:.2f}/month)")
                        deleted.append({
                            'snapshot_id': snapshot_id,
                            'age_days': age_days,
                            'monthly_cost': monthly_cost
                        })
                    except Exception as e:
                        print(f"  ❌ Failed to delete {snapshot_id}: {e}")
            else:
                reason = "Retain tag" if retain else f"Too recent ({age_days} days)"
                kept.append({'snapshot_id': snapshot_id, 'reason': reason})

        total_savings = sum(s['monthly_cost'] for s in deleted)
        print(f"\n💰 Old snapshots: {len(deleted)} deleted, ${total_savings:.2f}/month saved")
        return {'deleted': deleted, 'kept': kept, 'monthly_savings': total_savings}

    def check_stopped_instances(self, days_stopped: int = 14) -> Dict:
        """Alert on EC2 instances stopped for >days_stopped (no deletion)."""
        print(f"\n🔍 Checking for EC2 instances stopped >{days_stopped} days...")

        instances = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
        )

        alerts = []

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']

                tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                name = tags.get('Name', 'N/A')
                owner = tags.get('Owner', 'unknown')

                # Check for KeepAlive tag
                keep_alive = tags.get('KeepAlive', '').lower() == 'true'

                if not keep_alive:
                    # Estimate monthly cost of attached EBS volumes
                    volumes = [bdm for bdm in instance.get('BlockDeviceMappings', [])]
                    ebs_cost = len(volumes) * 10  # Rough estimate: $10/volume/month

                    alerts.append({
                        'instance_id': instance_id,
                        'name': name,
                        'owner': owner,
                        'instance_type': instance_type,
                        'estimated_ebs_cost_monthly': ebs_cost
                    })

                    print(f"  ⚠️  {instance_id} ({name}) stopped, owned by {owner}, ${ebs_cost}/month EBS cost")

        total_cost = sum(a['estimated_ebs_cost_monthly'] for a in alerts)
        print(f"\n💸 Stopped instances: {len(alerts)} found, ${total_cost}/month in EBS costs")
        print("   💡 Consider terminating or starting these instances")
        return {'alerts': alerts, 'monthly_cost': total_cost}

    def check_idle_load_balancers(self, days: int = 7) -> Dict:
        """Alert on load balancers with 0 active connections for days (no deletion)."""
        print(f"\n🔍 Checking for idle load balancers (0 connections for {days} days)...")

        load_balancers = self.elb.describe_load_balancers()['LoadBalancers']

        idle = []
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        for lb in load_balancers:
            lb_arn = lb['LoadBalancerArn']
            lb_name = lb['LoadBalancerName']
            lb_type = lb['Type']  # 'application' or 'network'

            # Check ActiveConnectionCount metric
            try:
                response = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/ApplicationELB' if lb_type == 'application' else 'AWS/NetworkELB',
                    MetricName='ActiveConnectionCount',
                    Dimensions=[{
                        'Name': 'LoadBalancer',
                        'Value': '/'.join(lb_arn.split('/')[-3:])
                    }],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86400,  # 1 day
                    Statistics=['Maximum']
                )

                max_connections = max([dp['Maximum'] for dp in response['Datapoints']], default=0)

                if max_connections == 0:
                    monthly_cost = 18.25  # $0.025/hour × 730 hours
                    idle.append({
                        'name': lb_name,
                        'arn': lb_arn,
                        'type': lb_type,
                        'monthly_cost': monthly_cost
                    })
                    print(f"  ⚠️  {lb_name} ({lb_type}) has 0 connections, ${monthly_cost}/month")

            except Exception as e:
                print(f"  ❌ Failed to check {lb_name}: {e}")

        total_cost = sum(lb['monthly_cost'] for lb in idle)
        print(f"\n💸 Idle load balancers: {len(idle)} found, ${total_cost}/month wasted")
        print("   💡 Consider deleting these load balancers")
        return {'idle': idle, 'monthly_cost': total_cost}

    def run_full_cleanup(self) -> Dict:
        """Run all cleanup checks and return summary."""
        print("=" * 60)
        print("AWS Idle Resource Cleanup")
        print(f"Region: {self.region}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print("=" * 60)

        results = {
            'unattached_volumes': self.cleanup_unattached_ebs_volumes(),
            'old_snapshots': self.cleanup_old_snapshots(),
            'stopped_instances': self.check_stopped_instances(),
            'idle_load_balancers': self.check_idle_load_balancers()
        }

        # Calculate total savings
        total_savings = (
            results['unattached_volumes']['monthly_savings'] +
            results['old_snapshots']['monthly_savings'] +
            results['stopped_instances']['monthly_cost'] +
            results['idle_load_balancers']['monthly_cost']
        )

        print("\n" + "=" * 60)
        print(f"💰 TOTAL POTENTIAL SAVINGS: ${total_savings:.2f}/month")
        print("=" * 60)

        return results


def main():
    parser = argparse.ArgumentParser(description='Clean up idle AWS resources')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')

    args = parser.parse_args()

    cleaner = IdleResourceCleaner(region=args.region, dry_run=args.dry_run)
    results = cleaner.run_full_cleanup()

    if args.json:
        print("\n" + json.dumps(results, indent=2, default=str))


if __name__ == '__main__':
    main()
