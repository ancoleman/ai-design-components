# Model Serving - Master Plan

> **Skill Purpose**: Production deployment of LLM and ML models with optimized inference engines, serving platforms, and orchestration frameworks.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Skill 12), vLLM documentation, BentoML patterns, LangChain orchestration guides

---

## Strategic Positioning

### The Model Serving Challenge

The AI/ML model serving landscape is fragmented:

**LLM Serving Engines:**
- vLLM (PagedAttention, continuous batching)
- TensorRT-LLM (maximum GPU efficiency)
- TGI (HuggingFace ecosystem)
- Ollama (local development)

**ML Model Serving:**
- BentoML (microservices-friendly)
- Triton (multi-model, multi-framework)
- TorchServe (PyTorch-specific)
- TFServing (TensorFlow-specific)

**LLM Orchestration:**
- LangChain (general workflows)
- LlamaIndex (RAG-focused)
- Haystack (enterprise search)
- Semantic Kernel (Microsoft ecosystem)

### What This Skill Provides

| Capability | Value |
|------------|-------|
| **Unified Guidance** | Single source for LLM vs ML model serving decisions |
| **Performance Optimization** | PagedAttention, continuous batching, GPU efficiency patterns |
- **Integration Patterns** | Frontend (ai-chat) ↔ Backend (model serving) ↔ Vector DB |
| **Streaming Responses** | SSE pattern for LLM token streaming |
| **Production Deployment** | Rate limiting, auth, model routing, horizontal scaling |

### Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│              Model Serving Integration Map                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (ai-chat) ──────> Model Serving APIs              │
│                              │                               │
│                              ├─> vLLM (LLM inference)       │
│                              ├─> BentoML (ML models)        │
│                              └─> LangChain (orchestration)  │
│                                                              │
│  Model Serving ──────────> databases-vector                 │
│   (RAG retrieval)            (Qdrant, pgvector)             │
│                                                              │
│  Model Serving ──────────> message-queues                   │
│   (async inference)          (Celery, BullMQ)               │
│                                                              │
│  Model Serving ──────────> observability                    │
│   (inference metrics)        (OpenTelemetry, Prometheus)    │
│                                                              │
│  Model Serving ──────────> deploying-applications           │
│   (K8s deployment)           (Helm charts, ArgoCD)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Taxonomy (3-Tier Architecture)

### Tier 1: LLM Serving Engines

Specialized inference servers for large language models with advanced optimization techniques.

| Engine | Best Use Case | Key Feature | Performance |
|--------|---------------|-------------|-------------|
| **vLLM** | Flexible OSS model serving | PagedAttention memory management | High (20-30x throughput vs naive) |
| **TensorRT-LLM** | Maximum NVIDIA GPU efficiency | Kernel fusion, FP8 quantization | Highest (2-8x faster than vLLM) |
| **TGI** | HuggingFace ecosystem integration | Native transformers compatibility | Good (similar to vLLM) |
| **Ollama** | Local development, prototyping | Simple CLI, no GPU required | Moderate (CPU-friendly) |

**When to Use:**
- Self-hosting open-source LLMs (Llama, Mistral, Qwen, etc.)
- Need control over inference parameters
- Cost optimization vs managed APIs
- Low-latency requirements (<100ms)

### Tier 2: ML Model Serving Platforms

General-purpose ML model deployment for traditional ML models (scikit-learn, XGBoost, PyTorch, TensorFlow).

| Platform | Best Use Case | Key Feature | Deployment |
|----------|---------------|-------------|------------|
| **BentoML** | Easy deployment, microservices | Python-native, adaptive batching | Docker, K8s, serverless |
| **Triton** | Multi-model, multi-framework | Dynamic batching, model ensemble | NVIDIA-optimized, K8s |
| **TorchServe** | PyTorch models | Native PyTorch integration | AWS SageMaker compatible |
| **TFServing** | TensorFlow models | SavedModel format | Google Cloud optimized |

**When to Use:**
- Traditional ML models (not LLMs)
- Multi-model serving (ensemble predictions)
- Framework-agnostic deployment
- Integration with existing ML pipelines

### Tier 3: LLM Orchestration Frameworks

High-level frameworks for building RAG systems, agents, and multi-step LLM workflows.

| Framework | Best Use Case | Key Feature | Ecosystem |
|-----------|---------------|-------------|-----------|
| **LangChain** | General workflows, agents | Extensive integrations (100+) | Python, TypeScript, Go, Java |
| **LlamaIndex** | RAG-focused applications | Data connectors, index structures | Python, TypeScript |
| **Haystack** | Enterprise search + generation | Production-ready, pipelines | Python, REST APIs |
| **Semantic Kernel** | Microsoft ecosystem | Azure integration, plugins | .NET, Python, Java |

**When to Use:**
- Building RAG pipelines (retrieval + generation)
- Multi-step agent workflows
- Need pre-built integrations (vector DBs, LLM providers)
- Rapid prototyping of AI applications

---

## LLM Serving Engines: Detailed Comparison

### vLLM (Recommended Primary)

**Why vLLM:**
- **PagedAttention**: Eliminates memory fragmentation, 20-30x throughput improvement
- **Continuous batching**: Dynamic request handling vs static batching
- **HuggingFace compatibility**: Works with 100+ models out-of-the-box
- **OpenAI-compatible API**: Drop-in replacement for OpenAI endpoints
- **Active development**: Backed by UC Berkeley, rapid iteration

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│                    vLLM Architecture                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  HTTP API (OpenAI-compatible)                                │
│       │                                                      │
│       ├─> /v1/completions                                   │
│       ├─> /v1/chat/completions                              │
│       └─> /v1/embeddings                                    │
│       │                                                      │
│  ┌────▼──────────────────────────────────────────────┐      │
│  │          AsyncEngine                             │      │
│  │  ├─ Request scheduling (continuous batching)    │      │
│  │  ├─ KV cache management (PagedAttention)        │      │
│  │  └─ Token streaming                             │      │
│  └──────────────────┬──────────────────────────────┘      │
│                     │                                       │
│  ┌─────────────────▼──────────────────────────────┐        │
│  │        Model Executor (GPU)                    │        │
│  │  ├─ Tensor parallelism (multi-GPU)            │        │
│  │  ├─ Quantization (AWQ, GPTQ, FP8)             │        │
│  │  └─ Custom CUDA kernels                       │        │
│  └───────────────────────────────────────────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Installation & Basic Setup:**
```bash
# Install vLLM
pip install vllm

# Serve a model (OpenAI-compatible API)
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --dtype auto \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9 \
  --host 0.0.0.0 \
  --port 8000
```

**Python API (programmatic):**
```python
from vllm import LLM, SamplingParams

# Initialize model
llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    tensor_parallel_size=2,  # Use 2 GPUs
    gpu_memory_utilization=0.9,
    max_model_len=4096
)

# Generate responses
prompts = [
    "Explain quantum computing in simple terms.",
    "Write a Python function to calculate Fibonacci."
]

sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=256
)

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Prompt: {output.prompt}")
    print(f"Response: {output.outputs[0].text}")
```

**Key Parameters:**
- `--dtype`: Model precision (auto, float16, bfloat16, float32)
- `--max-model-len`: Maximum sequence length (context window)
- `--gpu-memory-utilization`: GPU memory fraction (0.8-0.95 recommended)
- `--tensor-parallel-size`: Number of GPUs for tensor parallelism
- `--quantization`: Quantization method (awq, gptq, fp8)

### TensorRT-LLM (Maximum Performance)

**When to Use:**
- Need absolute maximum throughput (2-8x faster than vLLM)
- NVIDIA GPUs available (required)
- Willing to invest in model conversion/optimization
- Production workloads with high RPS

**Trade-offs:**
- More complex setup (model conversion required)
- Less flexible (optimized per model architecture)
- NVIDIA-only (no AMD/CPU fallback)

**Typical Workflow:**
```bash
# 1. Convert HuggingFace model to TensorRT-LLM format
python convert_checkpoint.py \
  --model_dir ./llama-3.1-8b \
  --output_dir ./llama-trt \
  --dtype float16

# 2. Build TensorRT engine
trtllm-build \
  --checkpoint_dir ./llama-trt \
  --output_dir ./llama-engine \
  --max_batch_size 256 \
  --max_input_len 2048 \
  --max_output_len 512

# 3. Serve with Triton Inference Server
tritonserver --model-repository=./model_repo
```

### TGI (Text Generation Inference)

**When to Use:**
- Deep HuggingFace integration required
- Want official HuggingFace support
- Simpler deployment than vLLM (opinionated)

**Quick Start:**
```bash
# Docker deployment
docker run --gpus all --shm-size 1g -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct \
  --max-total-tokens 4096 \
  --max-input-length 2048
```

### Ollama (Local Development)

**When to Use:**
- Local development without GPUs
- Quick prototyping
- Desktop/laptop deployment
- Educational purposes

**Installation:**
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull and run a model
ollama pull llama3.1:8b
ollama run llama3.1:8b
```

**REST API:**
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

---

## ML Model Serving: Detailed Comparison

### BentoML (Recommended Primary)

**Why BentoML:**
- **Python-native**: Natural fit for data science workflows
- **Adaptive batching**: Automatic request batching for throughput
- **Multi-framework**: scikit-learn, PyTorch, TensorFlow, XGBoost, LightGBM
- **Easy deployment**: Docker, Kubernetes, AWS Lambda, GCP Cloud Run
- **Production-ready**: Metrics, logging, health checks built-in

**Example Service:**
```python
import bentoml
from bentoml.io import JSON
import numpy as np
from pydantic import BaseModel

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Load model (assumes model is saved with bentoml.sklearn.save_model)
iris_model = bentoml.sklearn.get("iris_classifier:latest")

@bentoml.service(
    resources={"cpu": "2", "memory": "4Gi"},
    traffic={"timeout": 10},
)
class IrisClassifier:
    model_ref = bentoml.models.get("iris_classifier:latest")

    def __init__(self):
        self.model = bentoml.sklearn.load_model(self.model_ref)

    @bentoml.api(batchable=True, max_batch_size=32, max_latency_ms=1000)
    def classify(self, features: list[IrisFeatures]) -> list[str]:
        # Convert to numpy array
        X = np.array([[f.sepal_length, f.sepal_width,
                       f.petal_length, f.petal_width] for f in features])

        # Predict
        predictions = self.model.predict(X)

        # Map to class names
        class_names = ['setosa', 'versicolor', 'virginica']
        return [class_names[p] for p in predictions]
```

**Deployment:**
```bash
# Build Docker image
bentoml build

# Deploy to Kubernetes
bentoml containerize iris_classifier:latest
kubectl apply -f deployment.yaml

# Or deploy to BentoCloud (managed)
bentoml deploy iris_classifier:latest
```

### Triton Inference Server

**When to Use:**
- Multi-model serving (serve 10+ models on same GPU)
- Model ensembles (chain multiple models)
- NVIDIA GPU optimization critical
- TensorFlow, PyTorch, ONNX, TensorRT models

**Key Features:**
- **Dynamic batching**: Automatic request batching
- **Model ensemble**: Chain models (e.g., preprocessing → inference → postprocessing)
- **Concurrent model execution**: Run multiple models simultaneously
- **Backend support**: TensorFlow, PyTorch, ONNX, Python, TensorRT, OpenVINO

---

## LLM Orchestration: Detailed Comparison

### LangChain (Recommended General Purpose)

**Why LangChain:**
- **Largest ecosystem**: 100+ integrations (LLMs, vector DBs, tools)
- **Agent frameworks**: ReAct, Plan-and-Execute, Self-Ask
- **Multi-language**: Python, TypeScript, Go, Java
- **Active development**: Weekly releases, strong community

**Basic RAG Pipeline:**
```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 1. Load documents
loader = TextLoader("./data/documents.txt")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Qdrant.from_documents(
    chunks,
    embeddings,
    url="http://localhost:6333",
    collection_name="documents"
)

# 4. Create retrieval chain
llm = ChatOpenAI(model="gpt-4o", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 5. Query
result = qa_chain({"query": "What is PagedAttention?"})
print(result["result"])
print(result["source_documents"])
```

**Agent Pattern:**
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub

# Define tools
def search_vector_db(query: str) -> str:
    """Search the vector database for relevant information."""
    # Implementation: query Qdrant
    return "PagedAttention is a memory optimization technique..."

def calculate(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

tools = [
    Tool(
        name="VectorSearch",
        func=search_vector_db,
        description="Search documentation for technical information"
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Calculate mathematical expressions"
    )
]

# Create agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run agent
result = agent_executor.invoke({
    "input": "What is PagedAttention and calculate 2048 * 0.9"
})
print(result["output"])
```

### LlamaIndex (RAG-Focused)

**When to Use:**
- RAG is the primary use case
- Need advanced retrieval strategies (hybrid search, re-ranking)
- Data ingestion from multiple sources (PDF, web, databases)

**Key Advantages:**
- **Data connectors**: 100+ loaders (PDF, Notion, Google Drive, etc.)
- **Index structures**: Vector, tree, keyword, knowledge graph
- **Query engines**: Optimized for RAG workflows
- **Evaluation**: Built-in RAG evaluation metrics

**Example:**
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
llm = OpenAI(model="gpt-4o")
embed_model = OpenAIEmbedding()
index = VectorStoreIndex.from_documents(
    documents,
    llm=llm,
    embed_model=embed_model
)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Explain PagedAttention")
print(response)
```

### Haystack (Enterprise Search)

**When to Use:**
- Enterprise search + generation (hybrid systems)
- Production-ready pipelines with monitoring
- Need REST APIs out-of-the-box

---

## Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 Model Serving Selection Tree                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WHAT ARE YOU DEPLOYING?                                     │
│                                                              │
│  ├─ LLM (Large Language Model)                               │
│  │  │                                                       │
│  │  ├─ WHERE TO HOST?                                       │
│  │  │  ├─ Self-hosted OSS model                            │
│  │  │  │  ├─ Maximum throughput → vLLM                     │
│  │  │  │  ├─ Maximum GPU efficiency → TensorRT-LLM         │
│  │  │  │  ├─ HuggingFace ecosystem → TGI                   │
│  │  │  │  └─ Local development → Ollama                    │
│  │  │  │                                                   │
│  │  │  └─ Managed API (OpenAI, Anthropic, etc.)            │
│  │  │     └─ Use SDK directly (no serving layer needed)    │
│  │  │                                                       │
│  │  └─ NEED ORCHESTRATION? (RAG, agents, workflows)         │
│  │     ├─ General purpose → LangChain                      │
│  │     ├─ RAG-focused → LlamaIndex                         │
│  │     ├─ Enterprise search → Haystack                     │
│  │     └─ Microsoft ecosystem → Semantic Kernel            │
│  │                                                          │
│  ├─ TRADITIONAL ML MODEL (not LLM)                          │
│  │  │                                                       │
│  │  ├─ Simple deployment → BentoML                          │
│  │  ├─ Multi-model serving → Triton Inference Server       │
│  │  ├─ PyTorch specific → TorchServe                       │
│  │  └─ TensorFlow specific → TF Serving                    │
│  │                                                          │
│  └─ EMBEDDING MODEL                                          │
│     ├─ Small scale → FastAPI + sentence-transformers       │
│     ├─ Large scale → vLLM (supports embedding models)      │
│     └─ Managed → Voyage AI, OpenAI, Cohere                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Frontend Integration: ai-chat → LLM Serving

### Streaming Response Pattern (SSE)

**Backend (FastAPI + vLLM):**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import json

app = FastAPI()

# Connect to vLLM server (OpenAI-compatible)
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"  # vLLM doesn't require API key
)

@app.post("/chat/stream")
async def chat_stream(message: str):
    async def generate():
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": message}],
            stream=True,
            max_tokens=512,
            temperature=0.7
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                # SSE format
                yield f"data: {json.dumps({'token': token})}\n\n"

        # Signal completion
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

**Frontend (React):**
```typescript
// hooks/use-streaming-chat.ts
import { useState } from 'react'

export function useStreamingChat() {
  const [response, setResponse] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)

  const sendMessage = async (message: string) => {
    setIsStreaming(true)
    setResponse('')

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

---

## API Gateway Pattern for Production

### Requirements
- **Rate limiting**: Per-user, per-model
- **Authentication**: API key validation
- **Model routing**: Route requests to different models
- **Load balancing**: Distribute across replicas
- **Monitoring**: Track latency, tokens, costs

### Architecture with Kong/Nginx

```
┌─────────────────────────────────────────────────────────────┐
│              Production LLM API Gateway                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client Request                                              │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────────┐                                     │
│  │   API Gateway       │  (Kong, Nginx, Traefik)            │
│  │  ├─ Auth check      │                                     │
│  │  ├─ Rate limit      │                                     │
│  │  ├─ Route by model  │                                     │
│  │  └─ Metrics         │                                     │
│  └────────┬────────────┘                                     │
│           │                                                  │
│           ├──────> vLLM Instance 1 (Llama-3.1-8B)           │
│           ├──────> vLLM Instance 2 (Llama-3.1-70B)          │
│           └──────> vLLM Instance 3 (Mistral-7B)             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Kong Configuration Example:**
```yaml
services:
  - name: vllm-llama-8b
    url: http://vllm-llama-8b:8000
    routes:
      - name: chat-completions
        paths:
          - /v1/chat/completions
    plugins:
      - name: rate-limiting
        config:
          minute: 60
          policy: local
      - name: key-auth
      - name: prometheus
```

---

## Performance Benchmarks

### LLM Serving Throughput (Llama-3.1-8B, A100 GPU)

| Engine | Requests/sec | Latency (P50) | Latency (P99) | GPU Memory |
|--------|-------------|---------------|---------------|------------|
| **vLLM** | 150-200 | 50ms | 150ms | 14GB |
| **TensorRT-LLM** | 300-400 | 25ms | 80ms | 12GB |
| **TGI** | 120-180 | 60ms | 180ms | 15GB |
| **Naive PyTorch** | 5-10 | 500ms | 1000ms | 20GB |

**Test conditions:**
- Batch size: 32
- Input tokens: 512
- Output tokens: 128
- Concurrent requests: 64

### ML Model Serving (scikit-learn Random Forest)

| Platform | Requests/sec | Latency (P50) | CPU Usage |
|----------|-------------|---------------|-----------|
| **BentoML** | 5,000 | 2ms | 60% |
| **FastAPI (naive)** | 2,000 | 5ms | 80% |
| **Triton** | 8,000 | 1ms | 50% |

---

## Deployment Patterns

### Kubernetes Deployment (vLLM)

**Deployment YAML:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama-8b
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vllm-llama-8b
  template:
    metadata:
      labels:
        app: vllm-llama-8b
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        command:
          - python
          - -m
          - vllm.entrypoints.openai.api_server
          - --model
          - meta-llama/Llama-3.1-8B-Instruct
          - --dtype
          - auto
          - --max-model-len
          - "4096"
          - --gpu-memory-utilization
          - "0.9"
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 32Gi
          requests:
            nvidia.com/gpu: 1
            memory: 16Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: vllm-llama-8b
spec:
  selector:
    app: vllm-llama-8b
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-llama-8b
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

---

## Observability & Monitoring

### Key Metrics to Track

**LLM-Specific Metrics:**
- **Tokens per second** (throughput)
- **Time to first token** (TTFT)
- **Inter-token latency**
- **GPU utilization**
- **GPU memory usage**
- **KV cache hit rate**
- **Queue depth**

**General Metrics:**
- **Request rate** (req/s)
- **Error rate** (4xx, 5xx)
- **Latency** (P50, P95, P99)
- **Cost per request**

### Prometheus Metrics (vLLM)

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
requests_total = Counter('vllm_requests_total', 'Total requests')
tokens_generated = Counter('vllm_tokens_generated_total', 'Total tokens generated')
request_duration = Histogram('vllm_request_duration_seconds', 'Request duration')
gpu_memory_used = Gauge('vllm_gpu_memory_bytes', 'GPU memory used')

# Instrument endpoint
@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    requests_total.inc()
    start = time.time()

    try:
        response = await generate_response(request)
        tokens_generated.inc(len(response.tokens))
        return response
    finally:
        request_duration.observe(time.time() - start)
```

### Grafana Dashboard

**Essential Panels:**
1. **Throughput**: Requests/sec, tokens/sec
2. **Latency**: P50, P95, P99 latency over time
3. **GPU Metrics**: Utilization, memory, temperature
4. **Queue Depth**: Pending requests
5. **Error Rate**: 4xx/5xx over time
6. **Cost Tracking**: Tokens × cost per token

---

## Skill Structure

```
model-serving/
├── init.md                          # This file - master plan
├── SKILL.md                         # Main skill file (< 500 lines)
├── references/
│   ├── vllm-guide.md                # vLLM setup, configuration, optimization
│   ├── tensorrt-llm-guide.md        # TensorRT-LLM conversion, deployment
│   ├── bentoml-guide.md             # BentoML service patterns
│   ├── langchain-orchestration.md   # LangChain RAG, agents, chains
│   ├── llamaindex-patterns.md       # LlamaIndex data connectors, indices
│   ├── streaming-sse.md             # SSE streaming implementation
│   ├── api-gateway-patterns.md      # Kong, Nginx, rate limiting
│   └── inference-optimization.md    # Quantization, batching, caching
├── examples/
│   ├── vllm-fastapi-streaming/      # Complete SSE streaming example
│   │   ├── backend/
│   │   │   ├── main.py
│   │   │   └── requirements.txt
│   │   └── frontend/
│   │       └── use-streaming-chat.ts
│   ├── bentoml-sklearn/             # BentoML ML model serving
│   │   ├── service.py
│   │   ├── train.py
│   │   └── bentofile.yaml
│   ├── langchain-rag-qdrant/        # LangChain + Qdrant RAG
│   │   ├── ingest.py
│   │   ├── query.py
│   │   └── requirements.txt
│   └── k8s-vllm-deployment/         # Kubernetes deployment
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── hpa.yaml
│       └── prometheus-rules.yaml
├── scripts/
│   ├── benchmark_inference.py       # Throughput/latency benchmarking
│   ├── validate_deployment.py       # Health check, smoke tests
│   └── estimate_gpu_memory.py       # Estimate GPU requirements
└── assets/
    └── deployment-templates/
        ├── docker-compose.yaml      # Local development setup
        └── helm-chart/              # Helm chart for K8s
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: model-serving
description: LLM and ML model deployment for inference. Use when serving models in production, building AI APIs, or optimizing inference. Covers vLLM (LLM serving with PagedAttention), TensorRT-LLM (GPU optimization), Ollama (local development), BentoML (ML deployment), Triton (multi-model), LangChain (orchestration), LlamaIndex (RAG), streaming response patterns (SSE), API gateway setup, and Kubernetes deployment.
---
```

---

## Quality Checklist

Before finalizing this skill:

**Core Quality:**
- [ ] Clear scope: LLM + ML model serving, not training
- [ ] Decision framework: LLM vs ML, self-hosted vs managed, orchestration needs
- [ ] Performance benchmarks included (throughput, latency, GPU memory)
- [ ] Production patterns: API gateway, rate limiting, monitoring
- [ ] Integration examples: Frontend (ai-chat) ↔ Backend (model serving) ↔ Vector DB

**Technical Depth:**
- [ ] vLLM PagedAttention explained with architecture diagram
- [ ] Streaming SSE pattern with complete code examples
- [ ] Kubernetes deployment with HPA, GPU resource management
- [ ] Observability: Prometheus metrics, Grafana dashboards
- [ ] BentoML adaptive batching for ML models

**Progressive Disclosure:**
- [ ] SKILL.md < 500 lines (overview + framework selection)
- [ ] references/ for detailed guides (vLLM, BentoML, LangChain, etc.)
- [ ] examples/ with working code (streaming, RAG, deployment)
- [ ] scripts/ for benchmarking, validation (token-free execution)

**Cross-Skill Integration:**
- [ ] Frontend: ai-chat skill (streaming responses)
- [ ] Backend: databases-vector (RAG retrieval)
- [ ] Backend: message-queues (async inference)
- [ ] Backend: observability (inference metrics)
- [ ] Backend: deploying-applications (K8s deployment)

**Multi-Language Support:**
- [ ] Python (primary): FastAPI + vLLM, BentoML, LangChain
- [ ] TypeScript: Frontend streaming client, tRPC endpoints
- [ ] Rust (optional): Rust bindings for vLLM (future)

**Production Readiness:**
- [ ] Rate limiting patterns (Kong, Nginx)
- [ ] Authentication (API keys, OAuth)
- [ ] Cost tracking (tokens × pricing)
- [ ] Error handling (retry logic, fallbacks)
- [ ] Monitoring (Prometheus, Grafana)

**Documentation:**
- [ ] Installation instructions for each platform
- [ ] Configuration parameters explained
- [ ] Performance tuning guide
- [ ] Troubleshooting common issues
- [ ] Migration paths (e.g., OpenAI → self-hosted vLLM)

**Examples Completeness:**
- [ ] vLLM + FastAPI streaming (backend + frontend)
- [ ] BentoML scikit-learn deployment
- [ ] LangChain RAG with Qdrant
- [ ] Kubernetes deployment with GPU support
- [ ] Docker Compose for local development

**Scripts Utility:**
- [ ] `benchmark_inference.py`: Measure throughput/latency
- [ ] `validate_deployment.py`: Health checks, smoke tests
- [ ] `estimate_gpu_memory.py`: Calculate GPU requirements for models

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

## Research Sources

### LLM Serving Engines
- vLLM documentation: https://docs.vllm.ai/
- vLLM PagedAttention paper: https://arxiv.org/abs/2309.06180
- TensorRT-LLM: https://github.com/NVIDIA/TensorRT-LLM
- Text Generation Inference: https://huggingface.co/docs/text-generation-inference
- Ollama: https://ollama.com/

### ML Model Serving
- BentoML documentation: https://docs.bentoml.com/
- Triton Inference Server: https://github.com/triton-inference-server/server
- TorchServe: https://pytorch.org/serve/
- TensorFlow Serving: https://www.tensorflow.org/tfx/guide/serving

### LLM Orchestration
- LangChain documentation: https://python.langchain.com/
- LlamaIndex documentation: https://docs.llamaindex.ai/
- Haystack documentation: https://docs.haystack.deepset.ai/
- Semantic Kernel: https://learn.microsoft.com/en-us/semantic-kernel/

### Production Patterns
- Server-Sent Events (SSE): https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- Kong API Gateway: https://docs.konghq.com/
- Prometheus metrics: https://prometheus.io/docs/practices/instrumentation/
- Kubernetes GPU support: https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/

---

*Document status: Planning Phase - Ready for SKILL.md implementation*
