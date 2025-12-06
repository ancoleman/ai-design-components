#!/usr/bin/env python3
"""
Validate RBAC Configuration

Demonstrates: Audit RBAC permissions for security compliance

Dependencies:
    pip install kubernetes

Usage:
    python validate_rbac.py
"""

from kubernetes import client, config

def check_overpermissive_roles(rbac_api):
    """Find roles with wildcard permissions"""
    print("=== Checking for Overpermissive Roles ===\n")

    overpermissive = []

    # Check Roles
    for namespace in ['default', 'production', 'staging']:
        try:
            roles = rbac_api.list_namespaced_role(namespace)
            for role in roles.items:
                for rule in role.rules:
                    if '*' in rule.verbs or '*' in rule.resources or '*' in (rule.api_groups or []):
                        overpermissive.append({
                            'type': 'Role',
                            'name': role.metadata.name,
                            'namespace': namespace,
                            'rule': rule
                        })
        except client.exceptions.ApiException:
            pass

    # Check ClusterRoles
    cluster_roles = rbac_api.list_cluster_role()
    for role in cluster_roles.items:
        for rule in role.rules:
            if '*' in rule.verbs or '*' in rule.resources or '*' in (rule.api_groups or []):
                overpermissive.append({
                    'type': 'ClusterRole',
                    'name': role.metadata.name,
                    'namespace': 'N/A',
                    'rule': rule
                })

    if overpermissive:
        print(f"Found {len(overpermissive)} overpermissive roles:\n")
        for item in overpermissive:
            print(f"  {item['type']}: {item['name']} (namespace: {item['namespace']})")
            print(f"    API Groups: {item['rule'].api_groups}")
            print(f"    Resources: {item['rule'].resources}")
            print(f"    Verbs: {item['rule'].verbs}\n")
    else:
        print("No overpermissive roles found.\n")

def check_default_sa_usage(v1):
    """Find pods using default ServiceAccount"""
    print("=== Checking for Default ServiceAccount Usage ===\n")

    pods = v1.list_pod_for_all_namespaces()
    default_sa_pods = []

    for pod in pods.items:
        if pod.spec.service_account_name in [None, 'default']:
            default_sa_pods.append({
                'namespace': pod.metadata.namespace,
                'pod': pod.metadata.name
            })

    if default_sa_pods:
        print(f"Found {len(default_sa_pods)} pods using default ServiceAccount:\n")
        for item in default_sa_pods[:10]:  # Show first 10
            print(f"  {item['namespace']}/{item['pod']}")
        if len(default_sa_pods) > 10:
            print(f"  ... and {len(default_sa_pods) - 10} more\n")
    else:
        print("All pods use dedicated ServiceAccounts. Good!\n")

def check_cluster_admin_bindings(rbac_api):
    """Find cluster-admin bindings"""
    print("=== Checking for cluster-admin Bindings ===\n")

    cluster_role_bindings = rbac_api.list_cluster_role_binding()
    admin_bindings = []

    for binding in cluster_role_bindings.items:
        if binding.role_ref.name == 'cluster-admin':
            for subject in binding.subjects or []:
                admin_bindings.append({
                    'binding': binding.metadata.name,
                    'subject_kind': subject.kind,
                    'subject_name': subject.name,
                    'namespace': getattr(subject, 'namespace', 'N/A')
                })

    if admin_bindings:
        print(f"Found {len(admin_bindings)} cluster-admin bindings:\n")
        for item in admin_bindings:
            print(f"  Binding: {item['binding']}")
            print(f"    Subject: {item['subject_kind']}/{item['subject_name']} (ns: {item['namespace']})\n")
    else:
        print("No cluster-admin bindings found.\n")

def main():
    # Load kubeconfig
    config.load_kube_config()
    v1 = client.CoreV1Api()
    rbac_api = client.RbacAuthorizationV1Api()

    print("=" * 60)
    print("Kubernetes RBAC Security Audit")
    print("=" * 60 + "\n")

    check_overpermissive_roles(rbac_api)
    check_default_sa_usage(v1)
    check_cluster_admin_bindings(rbac_api)

    print("=" * 60)
    print("Audit Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
