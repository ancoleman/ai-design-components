# vLLM + FastAPI Streaming Example

Complete implementation of streaming LLM responses using vLLM and FastAPI with Server-Sent Events (SSE).

## Features

- Server-Sent Events (SSE) streaming
- OpenAI-compatible API
- CORS support for frontend integration
- Health checks for load balancers
- Production-ready error handling
- Logging and monitoring

## Prerequisites

1. **GPU with CUDA support** (16GB+ VRAM for Llama-3.1-8B)
2. **Python 3.8+**
3. **vLLM installed separately**

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install vLLM (separate installation)
pip install vllm
```

## Usage

### 1. Start vLLM Server

```bash
# Basic
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000

# Production
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --dtype float16 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9 \
  --port 8000
```

### 2. Start FastAPI Server

```bash
# Development
python main.py

# Production (with Gunicorn)
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:3000
```

### 3. Test Endpoints

**Health check:**
```bash
curl http://localhost:3000/health
```

**Non-streaming chat:**
```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum computing in simple terms",
    "temperature": 0.7,
    "max_tokens": 256
  }'
```

**Streaming chat:**
```bash
curl -X POST http://localhost:3000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a poem about AI",
    "temperature": 0.9,
    "max_tokens": 512
  }'
```

**List models:**
```bash
curl http://localhost:3000/models
```

## Frontend Integration

### React Example

```typescript
import { useState } from 'react'

export function useStreamingChat() {
  const [response, setResponse] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)

  const sendMessage = async (message: string) => {
    setIsStreaming(true)
    setResponse('')

    const res = await fetch('http://localhost:3000/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    })

    const reader = res.body!.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6))

          if (data.done) {
            setIsStreaming(false)
          } else if (data.token) {
            setResponse(prev => prev + data.token)
          }
        }
      }
    }
  }

  return { response, isStreaming, sendMessage }
}
```

### Next.js API Route

```typescript
// app/api/chat/route.ts
export async function POST(request: Request) {
  const { message } = await request.json()

  const response = await fetch('http://localhost:3000/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })

  // Forward SSE stream
  return new Response(response.body, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  })
}
```

## Production Deployment

### Docker Compose

```yaml
version: '3.8'

services:
  vllm:
    image: vllm/vllm-openai:latest
    command:
      - --model
      - meta-llama/Llama-3.1-8B-Instruct
      - --dtype
      - float16
      - --gpu-memory-utilization
      - "0.9"
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - VLLM_URL=http://vllm:8000
    depends_on:
      - vllm
```

### Kubernetes

See `../k8s-vllm-deployment/` for complete Kubernetes manifests.

## Performance Tuning

**Optimize vLLM:**
- Increase `--gpu-memory-utilization` to 0.95 for maximum throughput
- Use quantization for memory-constrained GPUs: `--quantization awq`
- Enable tensor parallelism for multi-GPU: `--tensor-parallel-size 2`

**Optimize FastAPI:**
- Use Gunicorn with multiple workers
- Add response caching for repeated queries
- Implement request queuing for rate limiting

## Monitoring

### Prometheus Metrics

Add to `main.py`:

```python
from prometheus_client import Counter, Histogram, make_asgi_app

requests_total = Counter('api_requests_total', 'Total requests')
request_duration = Histogram('api_request_duration_seconds', 'Request duration')

# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

### Grafana Dashboard

Monitor:
- Requests per second
- P50/P95/P99 latency
- Error rate
- Active connections
- Token generation rate

## Troubleshooting

**vLLM connection failed:**
- Verify vLLM is running: `curl http://localhost:8000/health`
- Check vLLM logs for errors
- Ensure correct port (default: 8000)

**Streaming not working:**
- Disable nginx buffering: `proxy_buffering off;`
- Check browser console for CORS errors
- Verify SSE format with `curl`

**Out of memory:**
- Reduce `--max-model-len` in vLLM
- Lower `--gpu-memory-utilization` to 0.85
- Use quantization (AWQ, GPTQ)

## Resources

- vLLM Docs: https://docs.vllm.ai/
- FastAPI Docs: https://fastapi.tiangolo.com/
- SSE Spec: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
