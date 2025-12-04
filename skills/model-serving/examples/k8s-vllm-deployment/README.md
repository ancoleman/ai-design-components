# vLLM Kubernetes Deployment

Complete Kubernetes deployment for vLLM model serving with autoscaling, GPU support, and production best practices.

## Files

- `deployment.yaml` - vLLM deployment with GPU resources
- `service.yaml` - LoadBalancer service
- `hpa.yaml` - Horizontal Pod Autoscaler
- `configmap.yaml` - Model configuration
- `ingress.yaml` - Ingress with TLS

## Quick Start

```bash
# 1. Create namespace
kubectl create namespace model-serving

# 2. Apply all manifests
kubectl apply -f . -n model-serving

# 3. Check deployment
kubectl get pods -n model-serving
kubectl logs -f deployment/vllm-llama -n model-serving

# 4. Test endpoint
kubectl port-forward service/vllm-llama 8000:8000 -n model-serving
curl http://localhost:8000/v1/models
```

## Requirements

- Kubernetes cluster with GPU nodes (NVIDIA)
- nvidia-device-plugin installed
- 1x A100 (40GB) or 2x A10 GPUs per pod
- 50GB persistent volume for model cache

## Scaling

```bash
# Manual scale
kubectl scale deployment vllm-llama --replicas=3 -n model-serving

# Autoscaling (HPA configured)
# Scales based on request queue depth
```

See individual YAML files for detailed configuration.
