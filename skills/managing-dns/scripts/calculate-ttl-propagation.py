#!/usr/bin/env python3
"""
DNS TTL Propagation Time Calculator
Calculates maximum propagation time based on TTL values

Usage:
    python3 calculate-ttl-propagation.py <old_ttl> <new_ttl>
    python3 calculate-ttl-propagation.py 3600 300
"""

import sys
from datetime import timedelta


def format_time(seconds):
    """Format seconds into human-readable time"""
    td = timedelta(seconds=seconds)
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    secs = td.seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if secs > 0 or not parts:
        parts.append(f"{secs} second{'s' if secs != 1 else ''}")

    return ", ".join(parts)


def calculate_propagation(old_ttl, new_ttl):
    """Calculate maximum DNS propagation time"""
    # Add buffer for DNS query time
    query_buffer = 5

    max_time = old_ttl + new_ttl + query_buffer

    print("=" * 60)
    print("DNS TTL Propagation Time Calculator")
    print("=" * 60)
    print()
    print(f"Old TTL:       {old_ttl}s ({format_time(old_ttl)})")
    print(f"New TTL:       {new_ttl}s ({format_time(new_ttl)})")
    print(f"Query Buffer:  {query_buffer}s")
    print()
    print("-" * 60)
    print(f"Maximum Propagation Time: {max_time}s ({format_time(max_time)})")
    print("-" * 60)
    print()
    print("Timeline:")
    print(f"  T+0:       Change made to DNS")
    print(f"  T+{old_ttl}:    Old TTL expires (worst case)")
    print(f"  T+{max_time}:    All resolvers have new record")
    print()
    print("=" * 60)

    # Recommendations
    print()
    print("Recommendations:")
    if old_ttl >= 3600:
        print(f"  ⚠️  High TTL ({format_time(old_ttl)}) - consider lowering 48h before changes")
        print(f"  💡 Lower to 300s (5min) for faster propagation (~10 minutes)")
    elif old_ttl <= 300:
        print(f"  ✅ Low TTL ({format_time(old_ttl)}) - fast propagation")
    else:
        print(f"  ℹ️  Moderate TTL ({format_time(old_ttl)}) - acceptable propagation time")
    print()


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 calculate-ttl-propagation.py <old_ttl> <new_ttl>")
        print("Example: python3 calculate-ttl-propagation.py 3600 300")
        sys.exit(1)

    try:
        old_ttl = int(sys.argv[1])
        new_ttl = int(sys.argv[2])

        if old_ttl < 0 or new_ttl < 0:
            raise ValueError("TTL values must be positive")

        calculate_propagation(old_ttl, new_ttl)

    except ValueError as e:
        print(f"Error: Invalid TTL value - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
