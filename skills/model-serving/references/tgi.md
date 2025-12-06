# Text Generation Inference (TGI) - HuggingFace LLM Serving


## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Docker Deployment](#docker-deployment)
  - [Key Parameters](#key-parameters)
- [API Usage](#api-usage)
  - [HTTP Endpoints](#http-endpoints)
  - [Python Client](#python-client)
- [Quantization](#quantization)
  - [GPTQ (4-bit)](#gptq-4-bit)
  - [AWQ (4-bit)](#awq-4-bit)
  - [bitsandbytes (8-bit/4-bit)](#bitsandbytes-8-bit4-bit)
- [Multi-GPU Deployment](#multi-gpu-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Monitoring](#monitoring)
  - [Health Check](#health-check)
  - [Metrics](#metrics)
- [Comparison: TGI vs vLLM](#comparison-tgi-vs-vllm)
- [Resources](#resources)

## Overview

Text Generation Inference (TGI) is HuggingFace's production-ready LLM serving solution with continuous batching, tensor parallelism, and optimized kernels.

**When to use TGI instead of vLLM:**
- Deep HuggingFace ecosystem integration required
- Want official HuggingFace support
- Prefer opinionated, simpler deployment
- Need HuggingFace Hub integration

**vLLM is generally preferred for:**
- Maximum throughput (PagedAttention)
- More flexible configuration
- Better community support

## Installation

```bash
# Docker (recommended)
docker pull ghcr.io/huggingface/text-generation-inference:latest

# From source
cargo install --path router
cargo install --path launcher
```

## Quick Start

### Docker Deployment

```bash
# Basic deployment
docker run --gpus all --shm-size 1g -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct

# Production configuration
docker run --gpus all --shm-size 1g -p 8080:80 \
  -e HF_TOKEN=your_token_here \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct \
  --max-total-tokens 4096 \
  --max-input-length 2048 \
  --max-batch-prefill-tokens 8192 \
  --max-batch-total-tokens 16384
```

### Key Parameters

**Model Loading:**
- `--model-id`: HuggingFace model ID or local path
- `--revision`: Model revision (branch, tag, or commit)
- `--dtype`: Data type (float16, bfloat16, auto)

**Performance:**
- `--max-total-tokens`: Maximum sequence length
- `--max-input-length`: Maximum input tokens
- `--max-batch-prefill-tokens`: Max tokens for prefill stage
- `--max-batch-total-tokens`: Total tokens in batch

**Multi-GPU:**
- `--num-shard`: Number of GPUs for tensor parallelism
- `--quantize`: Quantization method (bitsandbytes, gptq, awq)

## API Usage

### HTTP Endpoints

**Generate (synchronous):**
```bash
curl http://localhost:8080/generate \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": "What is machine learning?",
    "parameters": {
      "max_new_tokens": 256,
      "temperature": 0.7,
      "top_p": 0.9
    }
  }'
```

**Generate Stream (SSE):**
```bash
curl http://localhost:8080/generate_stream \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": "Write a poem about AI",
    "parameters": {
      "max_new_tokens": 256
    }
  }'
```

**Chat Completions (OpenAI-compatible):**
```bash
curl http://localhost:8080/v1/chat/completions \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [
      {"role": "user", "content": "Explain quantum computing"}
    ],
    "max_tokens": 256,
    "temperature": 0.7
  }'
```

### Python Client

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    base_url="http://localhost:8080",
    token=None  # No token for local TGI
)

# Generate
response = client.text_generation(
    "Explain PagedAttention in simple terms",
    max_new_tokens=256,
    temperature=0.7,
    top_p=0.9
)
print(response)

# Stream
for token in client.text_generation(
    "Count to 10",
    max_new_tokens=50,
    stream=True
):
    print(token, end="")
```

## Quantization

### GPTQ (4-bit)

```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id TheBloke/Llama-3.1-8B-GPTQ \
  --quantize gptq
```

### AWQ (4-bit)

```bash
docker run --gpus all --shm-size 1g -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id TheBloke/Llama-3.1-8B-AWQ \
  --quantize awq
```

### bitsandbytes (8-bit/4-bit)

```bash
# 8-bit
docker run --gpus all --shm-size 1g -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct \
  --quantize bitsandbytes

# 4-bit
docker run --gpus all --shm-size 1g -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct \
  --quantize bitsandbytes-nf4
```

## Multi-GPU Deployment

```bash
# Llama-3.1-70B on 4 GPUs
docker run --gpus all --shm-size 1g -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-70B-Instruct \
  --num-shard 4
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tgi-llama
spec:
  replicas: 2
  selector:
    matchLabels:
      app: tgi-llama
  template:
    metadata:
      labels:
        app: tgi-llama
    spec:
      containers:
      - name: tgi
        image: ghcr.io/huggingface/text-generation-inference:latest
        args:
          - --model-id
          - meta-llama/Llama-3.1-8B-Instruct
          - --max-total-tokens
          - "4096"
        ports:
        - containerPort: 80
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 32Gi
          requests:
            nvidia.com/gpu: 1
            memory: 16Gi
        env:
        - name: HF_TOKEN
          valueFrom:
            secretKeyRef:
              name: hf-token
              key: token
```

## Monitoring

### Health Check

```bash
curl http://localhost:8080/health
```

### Metrics

TGI exposes Prometheus metrics at `/metrics`:

**Key metrics:**
- `tgi_request_duration_seconds` - Request latency
- `tgi_queue_size` - Current queue depth
- `tgi_request_success_total` - Successful requests
- `tgi_request_failure_total` - Failed requests

## Comparison: TGI vs vLLM

| Feature | TGI | vLLM |
|---------|-----|------|
| **Throughput** | Good | Excellent (PagedAttention) |
| **Memory Efficiency** | Good | Excellent |
| **Setup Complexity** | Simple (opinionated) | Moderate (flexible) |
| **HuggingFace Integration** | Native | Good |
| **Community Support** | Official HF | Large community |
| **OpenAI API** | Yes | Yes |
| **Multi-GPU** | Tensor parallelism | Tensor + pipeline |

**Choose TGI if:**
- Want official HuggingFace support
- Prefer simpler, opinionated deployment
- Deep HuggingFace Hub integration needed

**Choose vLLM if:**
- Need maximum throughput
- Want flexible configuration
- PagedAttention benefits important

## Resources

- TGI Documentation: https://huggingface.co/docs/text-generation-inference
- GitHub: https://github.com/huggingface/text-generation-inference
- Supported Models: https://huggingface.co/docs/text-generation-inference/supported_models
