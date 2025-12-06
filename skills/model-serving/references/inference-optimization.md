# Inference Optimization Guide


## Table of Contents

- [Overview](#overview)
- [Quantization Techniques](#quantization-techniques)
  - [LLM Quantization](#llm-quantization)
  - [AWQ (Activation-aware Weight Quantization)](#awq-activation-aware-weight-quantization)
  - [GPTQ](#gptq)
  - [FP8 Quantization (H100 GPUs)](#fp8-quantization-h100-gpus)
- [Batching Strategies](#batching-strategies)
  - [Continuous Batching (vLLM)](#continuous-batching-vllm)
  - [Adaptive Batching (BentoML)](#adaptive-batching-bentoml)
  - [Manual Batching](#manual-batching)
- [GPU Optimization](#gpu-optimization)
  - [Memory Management](#memory-management)
  - [Tensor Parallelism](#tensor-parallelism)
  - [Pipeline Parallelism](#pipeline-parallelism)
- [KV Cache Optimization](#kv-cache-optimization)
  - [PagedAttention (vLLM)](#pagedattention-vllm)
  - [KV Cache Quantization](#kv-cache-quantization)
- [Attention Optimization](#attention-optimization)
  - [Flash Attention](#flash-attention)
  - [Multi-Query Attention (MQA)](#multi-query-attention-mqa)
- [Kernel Optimization](#kernel-optimization)
  - [Custom CUDA Kernels (vLLM)](#custom-cuda-kernels-vllm)
  - [TensorRT-LLM](#tensorrt-llm)
- [Caching Strategies](#caching-strategies)
  - [Response Caching](#response-caching)
  - [Prefix Caching](#prefix-caching)
  - [Embedding Caching](#embedding-caching)
- [Profiling and Monitoring](#profiling-and-monitoring)
  - [GPU Monitoring](#gpu-monitoring)
  - [vLLM Metrics](#vllm-metrics)
  - [Profiling with PyTorch](#profiling-with-pytorch)
- [Benchmarking](#benchmarking)
  - [Throughput Benchmark](#throughput-benchmark)
  - [Latency Benchmark](#latency-benchmark)
- [Production Optimization Checklist](#production-optimization-checklist)
- [Resources](#resources)

## Overview

Optimize LLM and ML model inference for production through quantization, batching, caching, and GPU tuning.

## Quantization Techniques

### LLM Quantization

Reduce model size and memory usage with minimal accuracy loss.

**Quantization Methods:**

| Method | Bits | Memory Reduction | Accuracy Loss | Speed |
|--------|------|------------------|---------------|-------|
| FP16 (baseline) | 16 | - | 0% | 1x |
| INT8 | 8 | 2x | <1% | 1.2-1.5x |
| INT4 (AWQ) | 4 | 4x | 1-2% | 1.5-2x |
| INT4 (GPTQ) | 4 | 4x | 1-2% | 1.5-2x |
| FP8 | 8 | 2x | <0.5% | 1.8-2.5x (H100 only) |

### AWQ (Activation-aware Weight Quantization)

**How it works:** Protects important weights, quantizes less important ones more aggressively.

**Use with vLLM:**
```bash
# Use pre-quantized model
vllm serve TheBloke/Llama-3.1-8B-AWQ \
  --quantization awq \
  --dtype auto
```

**Quantize your own model:**
```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "meta-llama/Llama-3.1-8B-Instruct"
quant_path = "llama-3.1-8b-awq"

# Load model
model = AutoAWQForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Quantize (requires calibration data)
quant_config = {"zero_point": True, "q_group_size": 128, "w_bit": 4}

model.quantize(tokenizer, quant_config=quant_config)
model.save_quantized(quant_path)
tokenizer.save_pretrained(quant_path)
```

### GPTQ

Similar to AWQ, different algorithm:

```python
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

model_path = "meta-llama/Llama-3.1-8B-Instruct"

quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=False
)

model = AutoGPTQForCausalLM.from_pretrained(
    model_path,
    quantize_config=quantize_config
)

model.quantize(calibration_dataset)
model.save_quantized("llama-3.1-8b-gptq")
```

### FP8 Quantization (H100 GPUs)

Maximum performance on NVIDIA H100:

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --quantization fp8 \
  --dtype auto
```

**Performance:** 1.8-2.5x faster than FP16 with <0.5% accuracy loss.

## Batching Strategies

### Continuous Batching (vLLM)

**Default in vLLM.** No configuration needed.

**How it works:**
```
Static Batching (old way):
Batch 1: [Req1, Req2, Req3, Req4] → Generate until ALL finish
Batch 2: [Req5, Req6, Req7, Req8] → Wait for Batch 1

Continuous Batching (vLLM):
[Req1, Req2, Req3, Req4] → Req1 finishes → Add Req5
[Req2, Req3, Req4, Req5] → Req3 finishes → Add Req6
[Req2, Req4, Req5, Req6] → ...
```

**Throughput improvement:** 2-3x vs static batching

### Adaptive Batching (BentoML)

Automatically batches requests with configurable trade-offs:

```python
@bentoml.api(
    batchable=True,
    max_batch_size=32,      # Maximum batch size
    max_latency_ms=1000     # Maximum wait time
)
def predict(self, inputs: list[np.ndarray]) -> list[float]:
    # BentoML automatically batches
    batch = np.array(inputs)
    return self.model.predict(batch).tolist()
```

**Tuning:**
- High throughput: `max_batch_size=64, max_latency_ms=2000`
- Low latency: `max_batch_size=8, max_latency_ms=100`

### Manual Batching

For custom serving:

```python
import asyncio
from collections import deque
from typing import List

class BatchProcessor:
    def __init__(self, model, max_batch_size=32, max_wait_ms=100):
        self.model = model
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.queue = deque()

    async def add_request(self, input_data):
        future = asyncio.Future()
        self.queue.append((input_data, future))

        # Trigger batch processing
        asyncio.create_task(self.process_batch())

        return await future

    async def process_batch(self):
        # Wait for batch to fill or timeout
        await asyncio.sleep(self.max_wait_ms / 1000)

        if not self.queue:
            return

        # Collect batch
        batch_size = min(len(self.queue), self.max_batch_size)
        batch = [self.queue.popleft() for _ in range(batch_size)]

        inputs = [item[0] for item in batch]
        futures = [item[1] for item in batch]

        # Process batch
        results = self.model.predict(inputs)

        # Return results
        for future, result in zip(futures, results):
            future.set_result(result)
```

## GPU Optimization

### Memory Management

**Estimate GPU memory:**
```python
def estimate_gpu_memory(num_params_billions, precision="fp16"):
    """Estimate GPU memory for LLM.

    Args:
        num_params_billions: Model parameters in billions
        precision: fp32, fp16, int8, int4
    """
    bytes_per_param = {
        "fp32": 4,
        "fp16": 2,
        "int8": 1,
        "int4": 0.5
    }

    # Model weights
    model_memory_gb = num_params_billions * bytes_per_param[precision]

    # KV cache and activations (1.2x overhead)
    total_memory_gb = model_memory_gb * 1.2

    return total_memory_gb

# Llama-3.1-8B in FP16
print(estimate_gpu_memory(8, "fp16"))  # ~19.2 GB

# Llama-3.1-70B in INT4
print(estimate_gpu_memory(70, "int4"))  # ~42 GB
```

**vLLM GPU tuning:**
```bash
# Maximum utilization (throughput)
vllm serve model \
  --gpu-memory-utilization 0.95 \
  --max-num-seqs 256

# Conservative (stability)
vllm serve model \
  --gpu-memory-utilization 0.85 \
  --max-num-seqs 128

# Multi-GPU
vllm serve model \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9
```

### Tensor Parallelism

Split model across multiple GPUs:

```bash
# Llama-3.1-70B on 4x A100 (40GB each)
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 4

# Or 2x A100 (80GB each)
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 2
```

**When to use:**
- Model doesn't fit on single GPU
- Each GPU gets 1/N of model weights
- Linear scaling up to ~8 GPUs

### Pipeline Parallelism

Split model layers across GPUs:

```bash
# 70B model on 8 GPUs (4-way pipeline, 2-way tensor)
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --pipeline-parallel-size 4 \
  --tensor-parallel-size 2
```

**Trade-offs:**
- Better for very large models
- Pipeline bubbles reduce efficiency
- More complex than tensor parallelism

## KV Cache Optimization

### PagedAttention (vLLM)

**Automatically enabled.** No configuration needed.

**How it works:**
- Stores key-value cache in paged memory blocks
- Eliminates fragmentation
- Near-zero memory waste

**Impact:** 2-4x memory efficiency vs traditional caching

### KV Cache Quantization

Reduce cache memory usage:

```bash
# INT8 KV cache
vllm serve model --kv-cache-dtype int8

# FP8 KV cache (H100)
vllm serve model --kv-cache-dtype fp8
```

**Memory reduction:** 2x with minimal quality impact

## Attention Optimization

### Flash Attention

**Automatically used by vLLM** when available.

**Benefits:**
- 2-4x faster attention computation
- Lower memory usage
- Exact attention (not approximate)

**Requirements:**
- NVIDIA Ampere+ GPU (A100, H100, RTX 3090+)
- Installed automatically with vLLM

### Multi-Query Attention (MQA)

**Model architecture feature** (e.g., Falcon models).

**Benefits:**
- Reduced KV cache size
- Faster inference
- Minimal accuracy impact

## Kernel Optimization

### Custom CUDA Kernels (vLLM)

vLLM includes optimized kernels for:
- PagedAttention
- Rotary position embeddings
- Layer normalization
- Activation functions

**No configuration needed.** Automatically used.

### TensorRT-LLM

Maximum optimization (requires model conversion):

```bash
# 1. Convert model
python convert_checkpoint.py \
  --model_dir ./llama-3.1-8b \
  --output_dir ./trt-checkpoint \
  --dtype float16

# 2. Build TensorRT engine
trtllm-build \
  --checkpoint_dir ./trt-checkpoint \
  --output_dir ./trt-engine \
  --gemm_plugin float16 \
  --max_batch_size 256

# 3. Serve
tritonserver --model-repository=./model_repo
```

**Performance:** 2-8x faster than vLLM, but more complex setup.

## Caching Strategies

### Response Caching

Cache complete responses for repeated queries:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_inference(prompt: str, temperature: float = 0.0):
    """Cache responses for identical prompts."""
    return model.generate(prompt, temperature=temperature)
```

**Best for:**
- Temperature = 0 (deterministic)
- Repeated identical queries
- FAQ-style applications

### Prefix Caching

Cache common prompt prefixes:

```python
# Example: System prompt is constant
SYSTEM_PROMPT = "You are a helpful assistant..."

# vLLM automatically shares KV cache for common prefixes
# across requests with same system prompt
```

**Enabled automatically in vLLM.**

### Embedding Caching

Cache embeddings for RAG:

```python
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

store = LocalFileStore("./embeddings_cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    OpenAIEmbeddings(),
    store,
    namespace="docs-v1"
)
```

## Profiling and Monitoring

### GPU Monitoring

```bash
# Real-time GPU stats
nvidia-smi dmon -s pucvmet -d 1

# Watch specific GPU
nvidia-smi -i 0 dmon

# Log to file
nvidia-smi dmon -s pucvmet -d 5 -o T > gpu_metrics.log
```

**Key metrics:**
- GPU utilization (should be >80%)
- Memory usage
- Temperature
- Power consumption

### vLLM Metrics

```python
import requests

# Prometheus metrics
response = requests.get("http://localhost:8000/metrics")
metrics = response.text

# Parse key metrics
for line in metrics.split('\n'):
    if 'vllm:' in line and not line.startswith('#'):
        print(line)
```

**Important metrics:**
- `vllm:time_to_first_token_seconds` - TTFT latency
- `vllm:time_per_output_token_seconds` - Token generation speed
- `vllm:num_requests_waiting` - Queue depth
- `vllm:gpu_cache_usage_perc` - KV cache utilization

### Profiling with PyTorch

```python
import torch
from torch.profiler import profile, ProfilerActivity

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True,
    with_stack=True
) as prof:
    outputs = model.generate(inputs)

# Print summary
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))

# Export Chrome trace
prof.export_chrome_trace("trace.json")
```

## Benchmarking

### Throughput Benchmark

```python
import time
import asyncio

async def benchmark_throughput(endpoint, num_requests=100):
    """Measure requests per second."""
    start = time.time()

    tasks = [
        asyncio.create_task(
            send_request(endpoint, f"Test prompt {i}")
        )
        for i in range(num_requests)
    ]

    await asyncio.gather(*tasks)

    duration = time.time() - start
    rps = num_requests / duration

    print(f"Throughput: {rps:.2f} req/s")
    print(f"Duration: {duration:.2f}s")
```

### Latency Benchmark

```python
import numpy as np

def benchmark_latency(endpoint, num_requests=100):
    """Measure latency percentiles."""
    latencies = []

    for i in range(num_requests):
        start = time.time()
        send_request(endpoint, f"Test prompt {i}")
        latency = time.time() - start
        latencies.append(latency)

    latencies = np.array(latencies) * 1000  # Convert to ms

    print(f"P50 latency: {np.percentile(latencies, 50):.2f}ms")
    print(f"P95 latency: {np.percentile(latencies, 95):.2f}ms")
    print(f"P99 latency: {np.percentile(latencies, 99):.2f}ms")
    print(f"Mean latency: {np.mean(latencies):.2f}ms")
```

## Production Optimization Checklist

**LLM Serving (vLLM):**
- [ ] Use FP16 or quantization (AWQ, INT8)
- [ ] Set `--gpu-memory-utilization 0.9`
- [ ] Enable tensor parallelism for large models
- [ ] Monitor GPU utilization (>80%)
- [ ] Track queue depth (scale if >10)
- [ ] Cache common prompt prefixes

**ML Model Serving (BentoML):**
- [ ] Enable adaptive batching
- [ ] Tune `max_batch_size` and `max_latency_ms`
- [ ] Set resource limits (CPU, memory)
- [ ] Monitor batch sizes
- [ ] Use multiple workers

**General:**
- [ ] Add response caching for repeated queries
- [ ] Implement request queuing
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Profile with PyTorch profiler
- [ ] Benchmark before deploying
- [ ] Load test at expected RPS

## Resources

- vLLM Performance: https://docs.vllm.ai/en/latest/performance/
- PagedAttention Paper: https://arxiv.org/abs/2309.06180
- Flash Attention: https://github.com/Dao-AILab/flash-attention
- AWQ: https://github.com/mit-han-lab/llm-awq
- TensorRT-LLM: https://github.com/NVIDIA/TensorRT-LLM
