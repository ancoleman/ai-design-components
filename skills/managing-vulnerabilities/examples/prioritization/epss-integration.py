#!/usr/bin/env python3
"""
EPSS (Exploit Prediction Scoring System) Integration

Fetch EPSS scores for vulnerabilities and prioritize based on exploitation probability.

Usage:
    python epss-integration.py CVE-2021-44228
    python epss-integration.py --scan-results trivy-results.json
"""

import argparse
import json
import requests
import sys
from datetime import datetime
from typing import Dict, List, Optional


class EPSSClient:
    """Client for FIRST.org EPSS API"""

    BASE_URL = "https://api.first.org/data/v1/epss"

    def __init__(self):
        self.session = requests.Session()

    def get_score(self, cve_id: str) -> Optional[Dict]:
        """
        Fetch EPSS score for a single CVE

        Returns:
            {
                'cve': 'CVE-2021-44228',
                'epss': 0.97505,
                'percentile': 0.99999,
                'date': '2025-12-04'
            }
        """
        url = f"{self.BASE_URL}?cve={cve_id}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'OK' and data['data']:
                result = data['data'][0]
                return {
                    'cve': result['cve'],
                    'epss': float(result['epss']),
                    'percentile': float(result['percentile']),
                    'date': result['date']
                }
        except Exception as e:
            print(f"Error fetching EPSS for {cve_id}: {e}", file=sys.stderr)

        return None

    def get_scores_bulk(self, cve_ids: List[str]) -> Dict[str, Dict]:
        """
        Fetch EPSS scores for multiple CVEs

        Returns:
            {
                'CVE-2021-44228': {'epss': 0.97505, 'percentile': 0.99999},
                'CVE-2023-12345': {'epss': 0.001, 'percentile': 0.25},
                ...
            }
        """
        # API supports comma-separated CVE list
        cve_list = ','.join(cve_ids[:100])  # Limit to 100 per request
        url = f"{self.BASE_URL}?cve={cve_list}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            results = {}
            if data['status'] == 'OK':
                for item in data['data']:
                    results[item['cve']] = {
                        'epss': float(item['epss']),
                        'percentile': float(item['percentile']),
                        'date': item['date']
                    }
            return results
        except Exception as e:
            print(f"Error fetching bulk EPSS: {e}", file=sys.stderr)
            return {}


def enrich_scan_results(scan_file: str, output_file: str = None):
    """
    Enrich Trivy scan results with EPSS scores

    Args:
        scan_file: Path to Trivy JSON scan results
        output_file: Optional path for enriched output
    """
    # Load scan results
    with open(scan_file) as f:
        scan_data = json.load(f)

    # Extract CVEs
    cves = set()
    for result in scan_data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            cve_id = vuln.get('VulnerabilityID')
            if cve_id and cve_id.startswith('CVE-'):
                cves.add(cve_id)

    print(f"Found {len(cves)} unique CVEs in scan results")

    # Fetch EPSS scores
    epss_client = EPSSClient()
    epss_scores = epss_client.get_scores_bulk(list(cves))

    print(f"Retrieved EPSS scores for {len(epss_scores)} CVEs")

    # Enrich vulnerabilities with EPSS
    for result in scan_data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            cve_id = vuln.get('VulnerabilityID')
            if cve_id in epss_scores:
                vuln['EPSS'] = epss_scores[cve_id]

    # Save enriched results
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(scan_data, f, indent=2)
        print(f"Enriched results saved to {output_file}")

    # Print summary
    print("\n=== EPSS Analysis ===")

    # High EPSS vulnerabilities (> 10% probability)
    high_epss = []
    for result in scan_data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            epss_data = vuln.get('EPSS', {})
            epss_score = epss_data.get('epss', 0)
            if epss_score >= 0.1:
                high_epss.append({
                    'cve': vuln['VulnerabilityID'],
                    'epss': epss_score,
                    'cvss': vuln.get('CVSS', {}).get('nvd', {}).get('V3Score', 0),
                    'package': vuln.get('PkgName'),
                    'severity': vuln.get('Severity')
                })

    # Sort by EPSS descending
    high_epss.sort(key=lambda x: x['epss'], reverse=True)

    print(f"\nHigh Exploitation Probability (EPSS >= 10%): {len(high_epss)}")
    print("\nTop 10 by EPSS:")
    print(f"{'CVE':<20} {'EPSS':<8} {'CVSS':<6} {'Severity':<10} {'Package'}")
    print("-" * 80)

    for vuln in high_epss[:10]:
        print(f"{vuln['cve']:<20} {vuln['epss']:.4f}   {vuln['cvss']:<6.1f} {vuln['severity']:<10} {vuln['package']}")

    # Recommended priority
    print("\n=== Recommended Priority ===")
    p1_count = sum(1 for v in high_epss if v['epss'] >= 0.5)
    p2_count = sum(1 for v in high_epss if 0.1 <= v['epss'] < 0.5)

    print(f"P1 (EPSS >= 50%): {p1_count} vulnerabilities - Fix within 7 days")
    print(f"P2 (EPSS 10-50%): {p2_count} vulnerabilities - Fix within 30 days")


def analyze_single_cve(cve_id: str):
    """Analyze a single CVE and display EPSS information"""
    epss_client = EPSSClient()
    result = epss_client.get_score(cve_id)

    if result:
        print(f"\n=== EPSS Analysis for {cve_id} ===")
        print(f"EPSS Score: {result['epss']:.4f} ({result['epss']*100:.2f}%)")
        print(f"Percentile: {result['percentile']:.4f}")
        print(f"Date: {result['date']}")

        # Interpretation
        epss = result['epss']
        if epss >= 0.9:
            priority = "P0/P1"
            action = "IMMEDIATE - Very high exploitation probability"
        elif epss >= 0.5:
            priority = "P1"
            action = "High priority - Likely to be exploited"
        elif epss >= 0.1:
            priority = "P2"
            action = "Moderate priority - Monitor closely"
        else:
            priority = "P3/P4"
            action = "Low priority - Unlikely to be exploited"

        print(f"\nRecommended Priority: {priority}")
        print(f"Action: {action}")
    else:
        print(f"Could not retrieve EPSS data for {cve_id}")


def main():
    parser = argparse.ArgumentParser(description='EPSS Integration Tool')
    parser.add_argument('cve', nargs='?', help='Single CVE to analyze (e.g., CVE-2021-44228)')
    parser.add_argument('--scan-results', help='Path to Trivy JSON scan results')
    parser.add_argument('--output', help='Output file for enriched results')

    args = parser.parse_args()

    if args.scan_results:
        enrich_scan_results(args.scan_results, args.output)
    elif args.cve:
        analyze_single_cve(args.cve)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
