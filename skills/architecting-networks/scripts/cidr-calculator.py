#!/usr/bin/env python3
"""
CIDR Calculator for Network Architecture Planning

Calculate subnet details, available IPs, and plan CIDR blocks for VPC design.

Usage:
    python cidr-calculator.py --cidr 10.0.0.0/16
    python cidr-calculator.py --cidr 10.0.0.0/16 --subnets 3
"""

import ipaddress
import argparse
import sys
from typing import List, Dict


def calculate_cidr_details(cidr: str) -> Dict:
    """Calculate details for a given CIDR block"""
    try:
        network = ipaddress.ip_network(cidr, strict=False)

        # AWS reserves 5 IPs per subnet (first 4 and last 1)
        aws_reserved = 5
        usable_ips = network.num_addresses - aws_reserved if network.num_addresses > 5 else 0

        return {
            'cidr': str(network),
            'network_address': str(network.network_address),
            'broadcast_address': str(network.broadcast_address),
            'netmask': str(network.netmask),
            'prefix_length': network.prefixlen,
            'total_ips': network.num_addresses,
            'usable_ips_aws': usable_ips,
            'first_usable': str(network.network_address + 1),
            'last_usable': str(network.broadcast_address - 1),
            'aws_reserved_ips': [
                f"{network.network_address} (network address)",
                f"{network.network_address + 1} (VPC router)",
                f"{network.network_address + 2} (DNS server)",
                f"{network.network_address + 3} (reserved for future use)",
                f"{network.broadcast_address} (broadcast address)"
            ]
        }
    except ValueError as e:
        print(f"Error: Invalid CIDR notation - {e}", file=sys.stderr)
        sys.exit(1)


def suggest_subnet_sizes(total_ips: int) -> List[Dict]:
    """Suggest appropriate subnet sizes based on total IPs needed"""
    suggestions = []

    # Common subnet sizes
    sizes = {
        '/28': 16,
        '/27': 32,
        '/26': 64,
        '/25': 128,
        '/24': 256,
        '/23': 512,
        '/22': 1024,
        '/21': 2048,
        '/20': 4096,
        '/19': 8192,
        '/18': 16384,
        '/17': 32768,
        '/16': 65536
    }

    for prefix, ips in sizes.items():
        if ips >= total_ips:
            usable_aws = ips - 5
            suggestions.append({
                'prefix': prefix,
                'total_ips': ips,
                'usable_ips_aws': usable_aws,
                'capacity_utilization': f"{(total_ips / usable_aws * 100):.1f}%"
            })

    return suggestions


def split_cidr_into_subnets(cidr: str, num_subnets: int) -> List[str]:
    """Split a CIDR block into equal-sized subnets"""
    try:
        network = ipaddress.ip_network(cidr, strict=False)

        # Calculate new prefix length
        import math
        additional_bits = math.ceil(math.log2(num_subnets))
        new_prefix = network.prefixlen + additional_bits

        if new_prefix > 32:
            print(f"Error: Cannot split {cidr} into {num_subnets} subnets (would require /{new_prefix})",
                  file=sys.stderr)
            sys.exit(1)

        # Generate subnets
        subnets = list(network.subnets(new_prefix=new_prefix))
        return [str(subnet) for subnet in subnets[:num_subnets]]

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def print_cidr_details(details: Dict):
    """Print formatted CIDR details"""
    print("\n" + "=" * 60)
    print("CIDR Block Details")
    print("=" * 60)
    print(f"CIDR:              {details['cidr']}")
    print(f"Network Address:   {details['network_address']}")
    print(f"Broadcast Address: {details['broadcast_address']}")
    print(f"Netmask:           {details['netmask']}")
    print(f"Prefix Length:     /{details['prefix_length']}")
    print(f"Total IPs:         {details['total_ips']:,}")
    print(f"Usable IPs (AWS):  {details['usable_ips_aws']:,}")
    print(f"First Usable:      {details['first_usable']}")
    print(f"Last Usable:       {details['last_usable']}")

    print("\nAWS Reserved IPs:")
    for reserved in details['aws_reserved_ips']:
        print(f"  - {reserved}")


def print_subnet_suggestions(ips_needed: int):
    """Print subnet size suggestions"""
    suggestions = suggest_subnet_sizes(ips_needed)

    if not suggestions:
        print(f"\nNo suitable subnet size for {ips_needed} IPs")
        return

    print("\n" + "=" * 60)
    print(f"Subnet Size Suggestions for {ips_needed} IPs")
    print("=" * 60)
    print(f"{'Prefix':<10} {'Total IPs':<12} {'Usable (AWS)':<15} {'Utilization':<15}")
    print("-" * 60)

    for s in suggestions[:5]:  # Show top 5 suggestions
        print(f"{s['prefix']:<10} {s['total_ips']:<12,} {s['usable_ips_aws']:<15,} {s['capacity_utilization']:<15}")


def print_subnet_split(cidr: str, subnets: List[str]):
    """Print subnet split results"""
    print("\n" + "=" * 60)
    print(f"Splitting {cidr} into {len(subnets)} subnets")
    print("=" * 60)

    for i, subnet in enumerate(subnets, 1):
        details = calculate_cidr_details(subnet)
        print(f"\nSubnet {i}: {subnet}")
        print(f"  - Usable IPs (AWS): {details['usable_ips_aws']:,}")
        print(f"  - Range: {details['network_address']} - {details['broadcast_address']}")


def main():
    parser = argparse.ArgumentParser(
        description='CIDR Calculator for Network Architecture Planning',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  Calculate details for a CIDR block:
    %(prog)s --cidr 10.0.0.0/16

  Split CIDR into subnets:
    %(prog)s --cidr 10.0.0.0/16 --subnets 3

  Suggest subnet sizes for required IPs:
    %(prog)s --suggest 1000
        '''
    )

    parser.add_argument('--cidr', type=str, help='CIDR block to analyze (e.g., 10.0.0.0/16)')
    parser.add_argument('--subnets', type=int, help='Number of equal-sized subnets to create')
    parser.add_argument('--suggest', type=int, help='Suggest subnet sizes for N IPs needed')

    args = parser.parse_args()

    if not any([args.cidr, args.suggest]):
        parser.print_help()
        sys.exit(1)

    # Calculate CIDR details
    if args.cidr:
        details = calculate_cidr_details(args.cidr)
        print_cidr_details(details)

        # Split into subnets if requested
        if args.subnets:
            subnets = split_cidr_into_subnets(args.cidr, args.subnets)
            print_subnet_split(args.cidr, subnets)

    # Suggest subnet sizes
    if args.suggest:
        print_subnet_suggestions(args.suggest)

    print("\n")


if __name__ == '__main__':
    main()
