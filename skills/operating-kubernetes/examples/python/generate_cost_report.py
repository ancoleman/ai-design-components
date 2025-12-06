#!/usr/bin/env python3
"""
Generate Kubernetes Cost Report

Demonstrates: Calculate namespace-level resource costs based on requests

Dependencies:
    pip install kubernetes

Usage:
    python generate_cost_report.py
"""

from kubernetes import client, config

# Cost per resource (example pricing)
COST_PER_CPU_HOUR = 0.03  # $0.03 per CPU core per hour
COST_PER_GB_HOUR = 0.004  # $0.004 per GB memory per hour

def parse_cpu(cpu_str):
    """Convert CPU string to cores (e.g., '500m' -> 0.5)"""
    if not cpu_str:
        return 0
    if cpu_str.endswith('m'):
        return float(cpu_str[:-1]) / 1000
    return float(cpu_str)

def parse_memory(mem_str):
    """Convert memory string to GB (e.g., '512Mi' -> 0.5)"""
    if not mem_str:
        return 0

    units = {
        'Ki': 1024,
        'Mi': 1024**2,
        'Gi': 1024**3,
        'Ti': 1024**4,
    }

    for unit, multiplier in units.items():
        if mem_str.endswith(unit):
            return float(mem_str[:-len(unit)]) * multiplier / (1024**3)

    # Assume bytes if no unit
    return float(mem_str) / (1024**3)

def main():
    # Load kubeconfig
    config.load_kube_config()
    v1 = client.CoreV1Api()

    # Get all pods
    pods = v1.list_pod_for_all_namespaces()

    # Calculate costs by namespace
    namespace_costs = {}

    for pod in pods.items:
        ns = pod.metadata.namespace

        if ns not in namespace_costs:
            namespace_costs[ns] = {
                'cpu_cores': 0,
                'memory_gb': 0,
                'pod_count': 0
            }

        namespace_costs[ns]['pod_count'] += 1

        for container in pod.spec.containers:
            if container.resources.requests:
                cpu = parse_cpu(container.resources.requests.get('cpu'))
                memory = parse_memory(container.resources.requests.get('memory'))

                namespace_costs[ns]['cpu_cores'] += cpu
                namespace_costs[ns]['memory_gb'] += memory

    # Calculate costs
    print("=== Kubernetes Resource Cost Report ===\n")
    print(f"{'Namespace':<30} {'Pods':<8} {'CPU Cores':<12} {'Memory (GB)':<14} {'Cost/Hour':<12} {'Cost/Month'}")
    print("-" * 100)

    total_cpu = 0
    total_memory = 0
    total_cost_hour = 0

    for ns, resources in sorted(namespace_costs.items(), key=lambda x: x[1]['cpu_cores'], reverse=True):
        cpu = resources['cpu_cores']
        memory = resources['memory_gb']
        pods = resources['pod_count']

        cost_hour = (cpu * COST_PER_CPU_HOUR) + (memory * COST_PER_GB_HOUR)
        cost_month = cost_hour * 24 * 30

        total_cpu += cpu
        total_memory += memory
        total_cost_hour += cost_hour

        print(f"{ns:<30} {pods:<8} {cpu:<12.2f} {memory:<14.2f} ${cost_hour:<11.2f} ${cost_month:.2f}")

    # Totals
    print("-" * 100)
    total_cost_month = total_cost_hour * 24 * 30
    print(f"{'TOTAL':<30} {sum(c['pod_count'] for c in namespace_costs.values()):<8} {total_cpu:<12.2f} {total_memory:<14.2f} ${total_cost_hour:<11.2f} ${total_cost_month:.2f}")

    print(f"\n* Costs based on: CPU ${COST_PER_CPU_HOUR}/core/hr, Memory ${COST_PER_GB_HOUR}/GB/hr")
    print("* Actual cloud costs may vary based on instance types and commitments")

if __name__ == "__main__":
    main()
