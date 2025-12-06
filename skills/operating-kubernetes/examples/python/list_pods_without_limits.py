#!/usr/bin/env python3
"""
List Pods Without Resource Limits

Demonstrates: Finding pods missing resource limits for cost optimization

Dependencies:
    pip install kubernetes

Usage:
    python list_pods_without_limits.py
"""

from kubernetes import client, config

def main():
    # Load kubeconfig
    config.load_kube_config()
    v1 = client.CoreV1Api()

    # Get all pods across all namespaces
    pods = v1.list_pod_for_all_namespaces()

    missing_limits = []

    for pod in pods.items:
        for container in pod.spec.containers:
            if not container.resources.limits:
                missing_limits.append({
                    'namespace': pod.metadata.namespace,
                    'pod': pod.metadata.name,
                    'container': container.name
                })

    # Print results
    print(f"Found {len(missing_limits)} containers without resource limits:\n")
    for item in missing_limits:
        print(f"  {item['namespace']}/{item['pod']}/{item['container']}")

    # Summary by namespace
    print("\n--- Summary by Namespace ---")
    namespaces = {}
    for item in missing_limits:
        ns = item['namespace']
        namespaces[ns] = namespaces.get(ns, 0) + 1

    for ns, count in sorted(namespaces.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ns}: {count} containers")

if __name__ == "__main__":
    main()
