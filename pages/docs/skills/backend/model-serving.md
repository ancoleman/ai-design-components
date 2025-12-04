---
sidebar_position: 13
title: Model Serving
description: LLM and ML model deployment for inference
tags: [backend, ai, ml, llm, inference, vllm]
---

# Model Serving

Deploy LLM and ML models for production inference with optimized serving engines, streaming response patterns, and orchestration frameworks. Focuses on self-hosted model serving, GPU optimization, and integration with frontend applications.

## When to Use

Use when:
- Deploying LLMs for production (self-hosted Llama, Mistral, Qwen)
- Building AI APIs with streaming responses
- Serving traditional ML models (scikit-learn, XGBoost, PyTorch)
- Implementing RAG pipelines with vector databases
- Optimizing inference throughput and latency
- Integrating LLM serving with frontend chat interfaces

## Multi-Language Support

This skill provides patterns for:
- **Python**: vLLM, BentoML, LangChain (primary for model serving)
- **Rust**: Candle (Hugging Face), optimized inference
- **Go**: High-performance API gateways
- **TypeScript**: Frontend integration, API consumption

## Model Serving Selection

### LLM Serving Engines

**vLLM (Recommended Primary)**
- PagedAttention memory management (20-30x throughput improvement)
- Continuous batching for dynamic request handling
- OpenAI-compatible API endpoints
- Use for: Most self-hosted LLM deployments

**TensorRT-LLM**
- Maximum GPU efficiency (2-8x faster than vLLM)
- Requires model conversion and optimization
- Use for: Production workloads needing absolute maximum throughput

**Ollama**
- Local development without GPUs
- Simple CLI interface
- Use for: Prototyping, laptop development, educational purposes

**Decision Framework:**
```
Self-hosted LLM deployment needed?
├─ Yes, need maximum throughput → vLLM
├─ Yes, need absolute max GPU efficiency → TensorRT-LLM
├─ Yes, local development only → Ollama
└─ No, use managed API (OpenAI, Anthropic) → No serving layer needed
```

### ML Model Serving (Non-LLM)

**BentoML (Recommended)**
- Python-native, easy deployment
- Adaptive batching for throughput
- Multi-framework support (scikit-learn, PyTorch, XGBoost)
- Use for: Most traditional ML model deployments

**Triton Inference Server**
- Multi-model serving on same GPU
- Model ensembles (chain multiple models)
- Use for: NVIDIA GPU optimization, serving 10+ models

## Quick Start: vLLM Server

```bash
# Install
pip install vllm

# Serve a model (OpenAI-compatible API)
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --dtype auto \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9 \
  --port 8000
```

**Key Parameters:**
- `--dtype`: Model precision (auto, float16, bfloat16)
- `--max-model-len`: Context window size
- `--gpu-memory-utilization`: GPU memory fraction (0.8-0.95)
- `--tensor-parallel-size`: Number of GPUs for model parallelism

## Streaming Responses (SSE Pattern)

**Backend (FastAPI):**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import json

app = FastAPI()
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

@app.post("/chat/stream")
async def chat_stream(message: str):
    async def generate():
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": message}],
            stream=True,
            max_tokens=512
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'token': token})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )
```

**Frontend (React):**
```typescript
const sendMessage = async (message: string) => {
  const response = await fetch('/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })

  const reader = response.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value)
    const lines = chunk.split('\n\n')

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6))
        if (data.token) {
          setResponse(prev => prev + data.token)
        }
      }
    }
  }
}
```

## BentoML Service

```python
import bentoml
from bentoml.io import JSON
import numpy as np

@bentoml.service(
    resources={"cpu": "2", "memory": "4Gi"},
    traffic={"timeout": 10}
)
class IrisClassifier:
    model_ref = bentoml.models.get("iris_classifier:latest")

    def __init__(self):
        self.model = bentoml.sklearn.load_model(self.model_ref)

    @bentoml.api(batchable=True, max_batch_size=32)
    def classify(self, features: list[dict]) -> list[str]:
        X = np.array([[f['sepal_length'], f['sepal_width'],
                       f['petal_length'], f['petal_width']] for f in features])
        predictions = self.model.predict(X)
        return ['setosa', 'versicolor', 'virginica'][predictions]
```

## Performance Optimization

### GPU Memory Estimation

**Rule of thumb for LLMs:**
```
GPU Memory (GB) = Model Parameters (B) × Precision (bytes) × 1.2
```

**Examples:**
- Llama-3.1-8B (FP16): 8B × 2 bytes × 1.2 = 19.2 GB
- Llama-3.1-70B (FP16): 70B × 2 bytes × 1.2 = 168 GB (requires 2-4 A100s)

**Quantization reduces memory:**
- FP16: 2 bytes per parameter
- INT8: 1 byte per parameter (2x memory reduction)
- INT4: 0.5 bytes per parameter (4x memory reduction)

### vLLM Optimization

```bash
# Enable quantization (AWQ for 4-bit)
vllm serve TheBloke/Llama-3.1-8B-AWQ \
  --quantization awq \
  --gpu-memory-utilization 0.9

# Multi-GPU deployment (tensor parallelism)
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9
```

### Batching Strategies

**Continuous batching (vLLM default):**
- Dynamically adds/removes requests from batch
- Higher throughput than static batching
- No configuration needed

**Adaptive batching (BentoML):**
```python
@bentoml.api(
    batchable=True,
    max_batch_size=32,
    max_latency_ms=1000  # Wait max 1s to fill batch
)
def predict(self, inputs: list[np.ndarray]) -> list[float]:
    # BentoML automatically batches requests
    return self.model.predict(np.array(inputs))
```

## Production Deployment

### Monitoring Metrics

**Essential LLM metrics:**
- Tokens per second (throughput)
- Time to first token (TTFT)
- Inter-token latency
- GPU utilization and memory
- Queue depth

**Prometheus instrumentation:**
```python
from prometheus_client import Counter, Histogram

requests_total = Counter('llm_requests_total', 'Total requests')
tokens_generated = Counter('llm_tokens_generated', 'Total tokens')
request_duration = Histogram('llm_request_duration_seconds', 'Request duration')

@app.post("/chat")
async def chat(request):
    requests_total.inc()
    start = time.time()
    response = await generate(request)
    tokens_generated.inc(len(response.tokens))
    request_duration.observe(time.time() - start)
    return response
```

## Integration Patterns

### Frontend (ai-chat) Integration

This skill provides the backend serving layer for the `ai-chat` skill.

**Flow:**
```
Frontend (React) → API Gateway → vLLM Server → GPU Inference
     ↑                                                  ↓
     └─────────── SSE Stream (tokens) ─────────────────┘
```

### RAG with Vector Databases

**Architecture:**
```
User Query → LangChain
              ├─> Vector DB (Qdrant) for retrieval
              ├─> Combine context + query
              └─> LLM (vLLM) for generation
```

## Migration from OpenAI API

vLLM provides OpenAI-compatible endpoints for easy migration:

```python
# Before (OpenAI)
from openai import OpenAI
client = OpenAI(api_key="sk-...")

# After (vLLM)
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

# Same API calls work!
response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Multi-Model Serving

Route requests to different models based on task:

```python
MODEL_ROUTING = {
    "small": "meta-llama/Llama-3.1-8B-Instruct",  # Fast, cheap
    "large": "meta-llama/Llama-3.1-70B-Instruct", # Accurate, expensive
    "code": "codellama/CodeLlama-34b-Instruct"    # Code-specific
}

@app.post("/chat")
async def chat(message: str, task: str = "small"):
    model = MODEL_ROUTING[task]
    # Route to appropriate vLLM instance
```

## Cost Optimization

**Track token usage:**
```python
import tiktoken

def estimate_cost(text: str, model: str, price_per_1k: float):
    encoding = tiktoken.encoding_for_model(model)
    tokens = len(encoding.encode(text))
    return (tokens / 1000) * price_per_1k

# Compare costs
openai_cost = estimate_cost(text, "gpt-4o", 0.005)  # $5 per 1M tokens
self_hosted_cost = 0  # Fixed GPU cost, unlimited tokens
```

## Troubleshooting

**Out of GPU memory:**
- Reduce `--max-model-len`
- Lower `--gpu-memory-utilization` (try 0.8)
- Enable quantization (`--quantization awq`)
- Use smaller model variant

**Low throughput:**
- Increase `--gpu-memory-utilization` (try 0.95)
- Enable continuous batching (vLLM default)
- Check GPU utilization (should be >80%)
- Consider tensor parallelism for multi-GPU

**High latency:**
- Reduce batch size if using static batching
- Check network latency to GPU server
- Profile with benchmarking scripts

## Related Skills

- [AI Chat](../frontend/ai-chat) - Frontend chat interface
- [AI Data Engineering](./ai-data-engineering) - RAG pipeline orchestration
- [Vector Databases](./databases-vector) - Retrieval for RAG
- [Deploying Applications](./deploying-applications) - Deploy vLLM infrastructure

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/model-serving)
- vLLM: https://docs.vllm.ai/
- BentoML: https://docs.bentoml.com/
- LangChain: https://python.langchain.com/
- Ollama: https://ollama.com/
