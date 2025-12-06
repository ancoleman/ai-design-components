# vLLM - High-Performance LLM Serving


## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [PagedAttention Architecture](#pagedattention-architecture)
  - [The Memory Problem](#the-memory-problem)
  - [PagedAttention Solution](#pagedattention-solution)
- [Basic Usage](#basic-usage)
  - [Starting the Server](#starting-the-server)
  - [Key Parameters Explained](#key-parameters-explained)
- [Advanced Configuration](#advanced-configuration)
  - [Quantization](#quantization)
  - [Multi-GPU Deployment](#multi-gpu-deployment)
- [Python API](#python-api)
- [OpenAI-Compatible API](#openai-compatible-api)
- [Performance Tuning](#performance-tuning)
  - [Maximizing Throughput](#maximizing-throughput)
  - [Minimizing Latency](#minimizing-latency)
- [Monitoring](#monitoring)
  - [Built-in Metrics](#built-in-metrics)
  - [Health Checks](#health-checks)
- [Troubleshooting](#troubleshooting)
  - [Out of Memory (OOM)](#out-of-memory-oom)
  - [Low Throughput](#low-throughput)
  - [High Latency](#high-latency)
- [Model Compatibility](#model-compatibility)
- [Production Best Practices](#production-best-practices)
- [Resources](#resources)

## Overview

vLLM (Versatile LLM) is a high-throughput and memory-efficient inference engine for LLMs featuring PagedAttention memory management and continuous batching.

**Key Advantages:**
- 20-30x higher throughput vs naive PyTorch implementation
- Eliminates memory fragmentation with PagedAttention
- OpenAI-compatible API for easy migration
- Supports 100+ HuggingFace models out-of-the-box

## Installation

```bash
# Standard installation
pip install vllm

# For specific GPU architectures
pip install vllm --extra-index-url https://download.pytorch.org/whl/cu121  # CUDA 12.1

# From source (for latest features)
git clone https://github.com/vllm-project/vllm.git
cd vllm
pip install -e .
```

**System Requirements:**
- NVIDIA GPU with compute capability 7.0+ (V100, A100, H100, RTX 3090+)
- CUDA 11.8 or 12.1+
- Python 3.8+
- 16GB+ GPU memory for 7B models

## PagedAttention Architecture

### The Memory Problem

Traditional LLM serving wastes GPU memory:

```
Traditional KV Cache (static allocation):
┌─────────────────────────────────────┐
│ Request 1 [████░░░░] 50% utilized  │ ← Fragmentation
│ Request 2 [██████░░] 75% utilized  │ ← Fragmentation
│ Request 3 [████████] 100% utilized │ ← No waste
└─────────────────────────────────────┘
Total Memory Utilization: ~50-60%
```

### PagedAttention Solution

Inspired by OS virtual memory paging:

```
PagedAttention (dynamic allocation):
┌─────────────────────────────────────┐
│ Shared Pool: [████████████████████] │
│                                      │
│ Request 1 → Pages [0,1,2,3]        │
│ Request 2 → Pages [4,5,6,7,8,9]    │
│ Request 3 → Pages [10,11,12,13]    │
└─────────────────────────────────────┘
Total Memory Utilization: ~90%+
```

**Benefits:**
- Near-zero memory fragmentation
- 2-4x memory efficiency vs static allocation
- Enables larger batch sizes
- 20-30x throughput improvement

## Basic Usage

### Starting the Server

```bash
# Basic server
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --dtype auto \
  --port 8000

# Production configuration
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --dtype float16 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9 \
  --max-num-seqs 256 \
  --host 0.0.0.0 \
  --port 8000
```

### Key Parameters Explained

**Model Loading:**
- `--dtype`: Precision (auto, float16, bfloat16, float32)
  - `auto`: Let vLLM choose (usually float16)
  - `float16`: Standard half precision
  - `bfloat16`: Better numerical stability, slightly slower

**Memory Management:**
- `--gpu-memory-utilization`: Fraction of GPU memory to use (0.8-0.95)
  - Too low: Underutilized GPU
  - Too high: Risk of OOM errors
  - Recommended: Start with 0.9

- `--max-model-len`: Maximum sequence length (context window)
  - Default: Model's max (e.g., 8192 for Llama-3.1-8B)
  - Reduce to fit larger batches

**Throughput:**
- `--max-num-seqs`: Maximum concurrent sequences
  - Higher = more throughput
  - Limited by GPU memory
  - Default: 256

**Parallelism:**
- `--tensor-parallel-size`: Number of GPUs for model parallelism
  - Use for models that don't fit on single GPU
  - Must divide model evenly

## Advanced Configuration

### Quantization

Reduce memory usage with quantization:

```bash
# AWQ (4-bit quantization)
vllm serve TheBloke/Llama-3.1-8B-AWQ \
  --quantization awq \
  --dtype auto

# GPTQ (another 4-bit method)
vllm serve TheBloke/Llama-3.1-8B-GPTQ \
  --quantization gptq

# FP8 quantization (H100 optimized)
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --quantization fp8 \
  --dtype auto
```

**Quantization Comparison:**
- **FP16** (baseline): 2 bytes/param, best accuracy
- **AWQ** (4-bit): 0.5 bytes/param, 4x memory reduction, ~2% accuracy loss
- **GPTQ** (4-bit): 0.5 bytes/param, similar to AWQ
- **FP8**: 1 byte/param, 2x memory reduction, minimal accuracy loss (H100 only)

### Multi-GPU Deployment

**Tensor Parallelism (single model across GPUs):**
```bash
# Llama-3.1-70B on 4x A100 (40GB each)
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9
```

**Pipeline Parallelism:**
```bash
# Split model layers across GPUs
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --pipeline-parallel-size 2 \
  --tensor-parallel-size 2  # Total 4 GPUs
```

## Python API

For programmatic use without HTTP server:

```python
from vllm import LLM, SamplingParams

# Initialize model
llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    tensor_parallel_size=1,
    gpu_memory_utilization=0.9,
    max_model_len=4096,
    dtype="auto"
)

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.7,    # Randomness (0 = deterministic, 1 = creative)
    top_p=0.9,         # Nucleus sampling
    max_tokens=256,    # Maximum response length
    stop=["</s>", "\n\n"]  # Stop sequences
)

# Generate (batched automatically)
prompts = [
    "Explain quantum computing",
    "Write a Python function for Fibonacci"
]

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Prompt: {output.prompt}")
    print(f"Response: {output.outputs[0].text}")
    print(f"Tokens: {len(output.outputs[0].token_ids)}")
```

## OpenAI-Compatible API

vLLM exposes OpenAI-compatible endpoints:

**Endpoints:**
- `/v1/chat/completions` - Chat format
- `/v1/completions` - Raw completion
- `/v1/embeddings` - Text embeddings (if model supports)
- `/v1/models` - List available models

**Example:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # vLLM doesn't require auth by default
)

# Chat completion
response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain PagedAttention"}
    ],
    temperature=0.7,
    max_tokens=512
)

print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Count to 10"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Performance Tuning

### Maximizing Throughput

**1. Tune GPU Memory Utilization:**
```bash
# Conservative (safe)
--gpu-memory-utilization 0.85

# Aggressive (maximum throughput)
--gpu-memory-utilization 0.95
```

**2. Adjust Sequence Length:**
```bash
# Shorter context = more concurrent requests
--max-model-len 2048  # Instead of default 8192
```

**3. Enable Continuous Batching:**
Already enabled by default in vLLM. No configuration needed.

### Minimizing Latency

**1. Reduce Batch Size:**
```bash
--max-num-seqs 16  # Lower than default 256
```

**2. Use Faster Precision:**
```bash
--dtype float16  # Faster than bfloat16
```

**3. Smaller Model:**
Use Llama-3.1-8B instead of Llama-3.1-70B for latency-sensitive applications.

## Monitoring

### Built-in Metrics

vLLM exposes Prometheus metrics at `/metrics`:

**Key Metrics:**
- `vllm:num_requests_running` - Current active requests
- `vllm:num_requests_waiting` - Queue depth
- `vllm:gpu_cache_usage_perc` - KV cache utilization
- `vllm:time_to_first_token_seconds` - TTFT latency
- `vllm:time_per_output_token_seconds` - Inter-token latency

**Prometheus scrape config:**
```yaml
scrape_configs:
  - job_name: 'vllm'
    static_configs:
      - targets: ['localhost:8000']
```

### Health Checks

```bash
# Health endpoint
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/v1/models
```

## Troubleshooting

### Out of Memory (OOM)

**Symptoms:** `CUDA out of memory` errors

**Solutions:**
1. Reduce `--gpu-memory-utilization` to 0.85
2. Decrease `--max-model-len`
3. Lower `--max-num-seqs`
4. Enable quantization (AWQ, GPTQ)
5. Use smaller model variant

**Example fix:**
```bash
# Before (OOM)
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.95

# After (fixed)
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.85 \
  --quantization awq  # If using quantized model
```

### Low Throughput

**Symptoms:** Low requests/sec, high queue depth

**Solutions:**
1. Increase `--gpu-memory-utilization` to 0.9-0.95
2. Increase `--max-num-seqs`
3. Check GPU utilization (should be >80%)
4. Use tensor parallelism if memory allows

### High Latency

**Symptoms:** Slow time to first token

**Solutions:**
1. Reduce batch size (`--max-num-seqs`)
2. Use smaller model
3. Check network latency
4. Profile with `nvidia-smi` during inference

## Model Compatibility

vLLM supports 100+ models from HuggingFace. Common families:

**LLMs:**
- Llama 2, Llama 3, Llama 3.1
- Mistral, Mixtral
- Qwen 2, Qwen 2.5
- Gemma, Gemma 2
- Phi-2, Phi-3

**Embedding Models:**
- BERT variants
- sentence-transformers models

**Check compatibility:**
```bash
# List supported architectures
python -c "from vllm import ModelRegistry; print(ModelRegistry.get_supported_archs())"
```

## Production Best Practices

1. **Use float16 dtype** for best performance/quality balance
2. **Set gpu-memory-utilization to 0.9** for production
3. **Enable monitoring** with Prometheus metrics
4. **Add health checks** in load balancer
5. **Use quantization** (AWQ) for GPU memory constrained deployments
6. **Deploy behind API gateway** (Kong, Nginx) for auth and rate limiting
7. **Monitor queue depth** - scale if consistently >10

## Resources

- vLLM Documentation: https://docs.vllm.ai/
- PagedAttention Paper: https://arxiv.org/abs/2309.06180
- GitHub: https://github.com/vllm-project/vllm
- Model Hub: https://huggingface.co/models?library=vllm
