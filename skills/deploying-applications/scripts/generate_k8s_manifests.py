#!/usr/bin/env python3
"""
Generate Kubernetes manifests from templates.

This script is executed WITHOUT loading into context (token-free).

Usage:
    python scripts/generate_k8s_manifests.py --app-name my-app --replicas 3 --namespace production

Features:
    - Generates Deployment, Service, ConfigMap, Ingress
    - Configurable replicas, namespace, resources
    - Outputs valid YAML to stdout or file
"""

import argparse
import sys
from typing import Dict, Any


def generate_deployment(app_name: str, replicas: int, namespace: str, image: str, port: int, resources: Dict[str, Any]) -> str:
    """Generate Kubernetes Deployment manifest."""
    return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  namespace: {namespace}
  labels:
    app: {app_name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {image}
        ports:
        - containerPort: {port}
          name: http
        env:
        - name: PORT
          value: "{port}"
        resources:
          requests:
            cpu: {resources['requests']['cpu']}
            memory: {resources['requests']['memory']}
          limits:
            cpu: {resources['limits']['cpu']}
            memory: {resources['limits']['memory']}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
"""


def generate_service(app_name: str, namespace: str, port: int) -> str:
    """Generate Kubernetes Service manifest."""
    return f"""apiVersion: v1
kind: Service
metadata:
  name: {app_name}
  namespace: {namespace}
  labels:
    app: {app_name}
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: {port}
    protocol: TCP
    name: http
  selector:
    app: {app_name}
"""


def generate_configmap(app_name: str, namespace: str, environment: str) -> str:
    """Generate Kubernetes ConfigMap manifest."""
    return f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {app_name}-config
  namespace: {namespace}
data:
  environment: {environment}
  log_level: info
"""


def generate_ingress(app_name: str, namespace: str, host: str) -> str:
    """Generate Kubernetes Ingress manifest."""
    return f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {app_name}
  namespace: {namespace}
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - {host}
    secretName: {app_name}-tls
  rules:
  - host: {host}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {app_name}
            port:
              number: 80
"""


def generate_hpa(app_name: str, namespace: str, min_replicas: int, max_replicas: int, target_cpu: int) -> str:
    """Generate Horizontal Pod Autoscaler manifest."""
    return f"""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {app_name}
  namespace: {namespace}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {app_name}
  minReplicas: {min_replicas}
  maxReplicas: {max_replicas}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {target_cpu}
"""


def main():
    parser = argparse.ArgumentParser(description="Generate Kubernetes manifests")
    parser.add_argument("--app-name", required=True, help="Application name")
    parser.add_argument("--namespace", default="default", help="Kubernetes namespace")
    parser.add_argument("--replicas", type=int, default=2, help="Number of replicas")
    parser.add_argument("--image", default="my-app:latest", help="Container image")
    parser.add_argument("--port", type=int, default=3000, help="Container port")
    parser.add_argument("--cpu-request", default="100m", help="CPU request")
    parser.add_argument("--memory-request", default="128Mi", help="Memory request")
    parser.add_argument("--cpu-limit", default="500m", help="CPU limit")
    parser.add_argument("--memory-limit", default="512Mi", help="Memory limit")
    parser.add_argument("--environment", default="production", help="Environment (dev/staging/production)")
    parser.add_argument("--host", help="Ingress host (optional)")
    parser.add_argument("--enable-hpa", action="store_true", help="Enable Horizontal Pod Autoscaler")
    parser.add_argument("--min-replicas", type=int, default=2, help="HPA min replicas")
    parser.add_argument("--max-replicas", type=int, default=10, help="HPA max replicas")
    parser.add_argument("--target-cpu", type=int, default=70, help="HPA target CPU utilization")
    parser.add_argument("--output", help="Output file (default: stdout)")

    args = parser.parse_args()

    resources = {
        "requests": {
            "cpu": args.cpu_request,
            "memory": args.memory_request,
        },
        "limits": {
            "cpu": args.cpu_limit,
            "memory": args.memory_limit,
        },
    }

    manifests = []

    # Generate manifests
    manifests.append(generate_deployment(
        args.app_name,
        args.replicas,
        args.namespace,
        args.image,
        args.port,
        resources
    ))

    manifests.append(generate_service(args.app_name, args.namespace, args.port))
    manifests.append(generate_configmap(args.app_name, args.namespace, args.environment))

    if args.host:
        manifests.append(generate_ingress(args.app_name, args.namespace, args.host))

    if args.enable_hpa:
        manifests.append(generate_hpa(
            args.app_name,
            args.namespace,
            args.min_replicas,
            args.max_replicas,
            args.target_cpu
        ))

    # Join manifests with separator
    output = "---\n".join(manifests)

    # Write to file or stdout
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"✅ Manifests written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
