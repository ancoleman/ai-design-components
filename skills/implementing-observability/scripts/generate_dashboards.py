#!/usr/bin/env python3
"""
Generate Grafana Dashboards from Templates

Creates Grafana dashboard JSON from templates for common observability patterns.

Usage:
    python scripts/generate_dashboards.py --type api --service my-api --output dashboard.json
    python scripts/generate_dashboards.py --type database --service postgres --output db-dashboard.json
"""

import argparse
import json
import sys
from typing import Dict, Any


DASHBOARD_TEMPLATES = {
    "api": {
        "title": "{service} API Metrics",
        "panels": [
            {
                "title": "Request Rate",
                "targets": [
                    {
                        "expr": 'rate(http_requests_total{{service="{service}"}}[5m])',
                        "legendFormat": "{{method}} {{route}}",
                    }
                ],
                "type": "graph",
            },
            {
                "title": "Error Rate",
                "targets": [
                    {
                        "expr": 'rate(http_requests_total{{service="{service}",status=~"5.."}}[5m])',
                        "legendFormat": "{{status}} {{route}}",
                    }
                ],
                "type": "graph",
            },
            {
                "title": "Latency (p50, p95, p99)",
                "targets": [
                    {
                        "expr": 'histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{{service="{service}"}}[5m]))',
                        "legendFormat": "p50",
                    },
                    {
                        "expr": 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{service="{service}"}}[5m]))',
                        "legendFormat": "p95",
                    },
                    {
                        "expr": 'histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{{service="{service}"}}[5m]))',
                        "legendFormat": "p99",
                    },
                ],
                "type": "graph",
            },
        ],
    },
    "database": {
        "title": "{service} Database Metrics",
        "panels": [
            {
                "title": "Active Connections",
                "targets": [
                    {
                        "expr": 'pg_stat_activity_count{{service="{service}"}}',
                        "legendFormat": "{{state}}",
                    }
                ],
                "type": "graph",
            },
            {
                "title": "Query Duration",
                "targets": [
                    {
                        "expr": 'rate(pg_stat_statements_mean_exec_time{{service="{service}"}}[5m])',
                        "legendFormat": "{{query}}",
                    }
                ],
                "type": "graph",
            },
        ],
    },
    "llm": {
        "title": "{service} LLM Serving Metrics",
        "panels": [
            {
                "title": "Tokens per Second",
                "targets": [
                    {
                        "expr": 'rate(llm_tokens_generated_total{{service="{service}"}}[5m])',
                        "legendFormat": "{{model}}",
                    }
                ],
                "type": "graph",
            },
            {
                "title": "Time to First Token (TTFT)",
                "targets": [
                    {
                        "expr": 'histogram_quantile(0.95, rate(llm_time_to_first_token_seconds_bucket{{service="{service}"}}[5m]))',
                        "legendFormat": "p95 TTFT",
                    }
                ],
                "type": "graph",
            },
            {
                "title": "GPU Utilization",
                "targets": [
                    {
                        "expr": 'nvidia_gpu_duty_cycle{{service="{service}"}}',
                        "legendFormat": "GPU {{gpu}}",
                    }
                ],
                "type": "graph",
            },
        ],
    },
}


def generate_dashboard(dashboard_type: str, service: str) -> Dict[str, Any]:
    """Generate Grafana dashboard JSON"""

    if dashboard_type not in DASHBOARD_TEMPLATES:
        raise ValueError(f"Unknown dashboard type: {dashboard_type}. Valid: {list(DASHBOARD_TEMPLATES.keys())}")

    template = DASHBOARD_TEMPLATES[dashboard_type]

    # Build panels with service name
    panels = []
    for i, panel_template in enumerate(template["panels"]):
        panel = {
            "id": i + 1,
            "title": panel_template["title"],
            "type": panel_template["type"],
            "gridPos": {"x": 0, "y": i * 8, "w": 24, "h": 8},
            "targets": [],
        }

        # Substitute service name in queries
        for target in panel_template["targets"]:
            panel["targets"].append({
                "expr": target["expr"].format(service=service),
                "legendFormat": target["legendFormat"],
                "refId": f"A{i}",
            })

        panels.append(panel)

    # Build complete dashboard
    dashboard = {
        "dashboard": {
            "title": template["title"].format(service=service),
            "panels": panels,
            "editable": True,
            "timezone": "browser",
            "schemaVersion": 36,
            "version": 1,
            "refresh": "30s",
        },
        "overwrite": True,
    }

    return dashboard


def main():
    parser = argparse.ArgumentParser(description="Generate Grafana dashboards")
    parser.add_argument(
        "--type",
        required=True,
        choices=["api", "database", "llm"],
        help="Dashboard type"
    )
    parser.add_argument(
        "--service",
        required=True,
        help="Service name (used in metric labels)"
    )
    parser.add_argument(
        "--output",
        default="dashboard.json",
        help="Output file path"
    )

    args = parser.parse_args()

    try:
        dashboard = generate_dashboard(args.type, args.service)

        with open(args.output, 'w') as f:
            json.dump(dashboard, f, indent=2)

        print(f"✓ Dashboard generated: {args.output}")
        print(f"  Type: {args.type}")
        print(f"  Service: {args.service}")
        print(f"  Panels: {len(dashboard['dashboard']['panels'])}")
        print(f"\nImport to Grafana:")
        print(f"  curl -X POST http://localhost:3000/api/dashboards/db \\")
        print(f"    -H 'Content-Type: application/json' \\")
        print(f"    -d @{args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
