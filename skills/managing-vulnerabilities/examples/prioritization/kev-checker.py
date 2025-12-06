#!/usr/bin/env python3
"""
CISA KEV (Known Exploited Vulnerabilities) Checker

Check if CVEs are in the CISA KEV catalog (actively exploited in the wild).

Usage:
    python kev-checker.py CVE-2021-44228
    python kev-checker.py --scan-results trivy-results.json
    python kev-checker.py --update-cache
"""

import argparse
import json
import requests
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set


class KEVCatalog:
    """CISA Known Exploited Vulnerabilities Catalog"""

    CATALOG_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    CACHE_FILE = Path.home() / ".cache" / "kev-catalog.json"
    CACHE_DURATION = timedelta(days=1)

    def __init__(self):
        self.catalog = None
        self.kev_set: Set[str] = set()

    def update_cache(self):
        """Download latest KEV catalog"""
        print("Downloading latest KEV catalog from CISA...")

        try:
            response = requests.get(self.CATALOG_URL, timeout=30)
            response.raise_for_status()
            catalog_data = response.json()

            # Create cache directory if needed
            self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

            # Save to cache
            with open(self.CACHE_FILE, 'w') as f:
                json.dump({
                    'updated': datetime.now().isoformat(),
                    'catalog': catalog_data
                }, f, indent=2)

            print(f"KEV catalog updated: {len(catalog_data.get('vulnerabilities', []))} entries")
            self.catalog = catalog_data
            self._build_kev_set()

        except Exception as e:
            print(f"Error updating KEV catalog: {e}", file=sys.stderr)
            sys.exit(1)

    def load_catalog(self, force_update: bool = False):
        """Load KEV catalog from cache or download"""
        # Check if cache exists and is recent
        if not force_update and self.CACHE_FILE.exists():
            with open(self.CACHE_FILE) as f:
                cached = json.load(f)
                updated = datetime.fromisoformat(cached['updated'])

                # Use cache if less than 1 day old
                if datetime.now() - updated < self.CACHE_DURATION:
                    self.catalog = cached['catalog']
                    self._build_kev_set()
                    return

        # Cache missing, expired, or force update requested
        self.update_cache()

    def _build_kev_set(self):
        """Build set of CVE IDs for fast lookup"""
        if self.catalog:
            self.kev_set = {
                vuln['cveID']
                for vuln in self.catalog.get('vulnerabilities', [])
            }

    def is_kev(self, cve_id: str) -> bool:
        """Check if CVE is in KEV catalog"""
        if not self.catalog:
            self.load_catalog()
        return cve_id in self.kev_set

    def get_kev_details(self, cve_id: str) -> Optional[Dict]:
        """Get KEV catalog entry details"""
        if not self.catalog:
            self.load_catalog()

        for vuln in self.catalog.get('vulnerabilities', []):
            if vuln['cveID'] == cve_id:
                return vuln
        return None

    def get_all_kevs(self) -> List[Dict]:
        """Get all KEV entries"""
        if not self.catalog:
            self.load_catalog()
        return self.catalog.get('vulnerabilities', [])


def check_single_cve(cve_id: str):
    """Check if a single CVE is in KEV catalog"""
    kev = KEVCatalog()
    kev.load_catalog()

    print(f"\n=== KEV Status for {cve_id} ===")

    if kev.is_kev(cve_id):
        details = kev.get_kev_details(cve_id)
        print(f"⚠️  CRITICAL: {cve_id} is in CISA KEV catalog!")
        print(f"\nVendor/Project: {details.get('vendorProject')}")
        print(f"Product: {details.get('product')}")
        print(f"Vulnerability: {details.get('vulnerabilityName')}")
        print(f"Date Added: {details.get('dateAdded')}")
        print(f"Due Date: {details.get('dueDate')}")
        print(f"\nDescription: {details.get('shortDescription')}")
        print(f"Required Action: {details.get('requiredAction')}")
        print(f"\n🔴 PRIORITY: P0 - Immediate remediation required (24-hour SLA)")
    else:
        print(f"✓ {cve_id} is NOT in KEV catalog")
        print("No evidence of active exploitation (based on CISA data)")


def check_scan_results(scan_file: str, output_file: str = None):
    """Check Trivy scan results against KEV catalog"""
    kev = KEVCatalog()
    kev.load_catalog()

    # Load scan results
    with open(scan_file) as f:
        scan_data = json.load(f)

    # Find KEV vulnerabilities
    kev_found = []
    all_cves = set()

    for result in scan_data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            cve_id = vuln.get('VulnerabilityID')
            if cve_id and cve_id.startswith('CVE-'):
                all_cves.add(cve_id)

                if kev.is_kev(cve_id):
                    kev_details = kev.get_kev_details(cve_id)
                    kev_found.append({
                        'cve': cve_id,
                        'package': vuln.get('PkgName'),
                        'severity': vuln.get('Severity'),
                        'fixed_version': vuln.get('FixedVersion'),
                        'kev_added': kev_details.get('dateAdded'),
                        'kev_due': kev_details.get('dueDate'),
                        'kev_action': kev_details.get('requiredAction')
                    })

                    # Mark in scan results
                    vuln['KEV'] = kev_details

    # Save enriched results
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(scan_data, f, indent=2)
        print(f"Enriched results saved to {output_file}")

    # Print summary
    print(f"\n=== KEV Analysis ===")
    print(f"Total unique CVEs scanned: {len(all_cves)}")
    print(f"CVEs in CISA KEV catalog: {len(kev_found)}")

    if kev_found:
        print(f"\n🔴 CRITICAL: {len(kev_found)} actively exploited vulnerabilities found!")
        print("\n" + "=" * 100)
        print(f"{'CVE':<20} {'Package':<25} {'Severity':<10} {'Fixed':<15} {'KEV Added'}")
        print("=" * 100)

        for vuln in kev_found:
            fixed = vuln['fixed_version'] or 'No fix'
            print(f"{vuln['cve']:<20} {vuln['package']:<25} {vuln['severity']:<10} {fixed:<15} {vuln['kev_added']}")

        print("\n⚠️  ACTION REQUIRED:")
        print("   - Priority: P0 (CRITICAL)")
        print("   - SLA: 24 hours")
        print("   - These CVEs are actively exploited in the wild")
        print("   - Immediate patching required")
        print("\nRemediation steps:")
        for vuln in kev_found:
            if vuln['fixed_version']:
                print(f"   - Update {vuln['package']} to {vuln['fixed_version']}")
            else:
                print(f"   - Apply mitigations for {vuln['cve']}: {vuln['kev_action']}")

        # Exit with error if KEV found
        sys.exit(1)
    else:
        print("\n✓ No KEV catalog vulnerabilities found")
        print("Continue with normal vulnerability prioritization")


def list_recent_kevs(days: int = 30):
    """List recently added KEV entries"""
    kev = KEVCatalog()
    kev.load_catalog()

    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    recent = [
        vuln for vuln in kev.get_all_kevs()
        if vuln.get('dateAdded', '') >= cutoff_date
    ]

    # Sort by date added (newest first)
    recent.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)

    print(f"\n=== KEV Entries Added in Last {days} Days ===")
    print(f"Total: {len(recent)} entries\n")

    print(f"{'Date Added':<12} {'CVE':<20} {'Vendor/Product':<40} {'Due Date'}")
    print("=" * 100)

    for vuln in recent[:50]:  # Show up to 50
        vendor_product = f"{vuln.get('vendorProject')} {vuln.get('product')}"
        print(f"{vuln.get('dateAdded'):<12} {vuln.get('cveID'):<20} {vendor_product:<40} {vuln.get('dueDate')}")


def main():
    parser = argparse.ArgumentParser(description='CISA KEV Catalog Checker')
    parser.add_argument('cve', nargs='?', help='Single CVE to check (e.g., CVE-2021-44228)')
    parser.add_argument('--scan-results', help='Path to Trivy JSON scan results')
    parser.add_argument('--output', help='Output file for enriched results')
    parser.add_argument('--update-cache', action='store_true', help='Force update KEV catalog cache')
    parser.add_argument('--list-recent', type=int, metavar='DAYS', help='List KEVs added in last N days')

    args = parser.parse_args()

    if args.update_cache:
        kev = KEVCatalog()
        kev.update_cache()
        print("KEV catalog cache updated successfully")

    elif args.list_recent:
        list_recent_kevs(args.list_recent)

    elif args.scan_results:
        check_scan_results(args.scan_results, args.output)

    elif args.cve:
        check_single_cve(args.cve)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
