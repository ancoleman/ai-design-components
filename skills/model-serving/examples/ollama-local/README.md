# Ollama Local Development Example

Simple local LLM serving for development without GPU requirements. Perfect for prototyping AI applications on laptops.

## Features

- CPU-friendly (no GPU required)
- Simple REST API
- Streaming responses
- Conversational chat
- Multiple model support

## Prerequisites

1. **Ollama installed** (download from https://ollama.com)
2. **Python 3.8+**

## Installation

### 1. Install Ollama

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Pull a Model

```bash
# Llama 3.1 8B (recommended)
ollama pull llama3.1:8b

# Smaller model for testing (faster)
ollama pull llama3.1:7b

# Larger model (better quality)
ollama pull llama3.1:70b

# List available models
ollama list
```

### 2. Start Ollama Server

```bash
# Usually auto-started, but can manually start with:
ollama serve
```

### 3. Run Example

```bash
python main.py
```

## API Examples

### Simple Generation

```python
import requests

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.1:8b",
    "prompt": "Why is the sky blue?"
})

print(response.json()["response"])
```

### Streaming

```python
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.1:8b", "prompt": "Count to 10", "stream": True},
    stream=True
)

for line in response.iter_lines():
    if line:
        data = json.loads(line)
        if not data.get("done"):
            print(data["response"], end="", flush=True)
```

### Chat with History

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning?"}
]

response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.1:8b",
    "messages": messages
})

print(response.json()["message"]["content"])
```

## CLI Usage

Ollama also provides a CLI:

```bash
# Interactive chat
ollama run llama3.1:8b

# One-off generation
echo "Explain quantum computing" | ollama run llama3.1:8b

# List models
ollama list

# Remove model
ollama rm llama3.1:8b

# Show model info
ollama show llama3.1:8b
```

## Integration with LangChain

```python
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.1:8b")

# Simple generation
response = llm.invoke("Explain vLLM in simple terms")
print(response)

# With chains
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

template = """You are a technical expert.

Question: {question}

Answer:"""

prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(llm=llm, prompt=prompt)

response = chain.run(question="What is PagedAttention?")
print(response)
```

## Performance Tuning

### Model Selection

- **7B models**: Fast, good for testing (~4GB RAM)
- **8B models**: Balanced quality/speed (~6GB RAM)
- **13B models**: Better quality (~8GB RAM)
- **70B models**: Best quality, slow (~40GB RAM)

### Parameters

```python
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.1:8b",
    "prompt": "Your prompt",
    "options": {
        "temperature": 0.7,      # Randomness (0-1)
        "top_p": 0.9,           # Nucleus sampling
        "num_ctx": 2048,        # Context window
        "num_predict": 512,     # Max tokens to generate
    }
})
```

## Use Cases

**Perfect for:**
- Local development and testing
- Prototyping AI applications
- Learning LLM concepts
- Privacy-sensitive applications (data never leaves machine)
- Offline development

**Not suitable for:**
- Production high-throughput serving
- Multi-user applications (use vLLM instead)
- Maximum performance (no GPU optimization)

## Migration to vLLM

When ready for production, migrate to vLLM:

```python
# Before (Ollama)
import requests
response = requests.post("http://localhost:11434/api/generate", ...)

# After (vLLM with OpenAI API)
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
response = client.chat.completions.create(...)
```

## Troubleshooting

**Ollama not starting:**
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart
killall ollama
ollama serve
```

**Out of memory:**
- Use smaller model (7B instead of 70B)
- Reduce `num_ctx` parameter
- Close other applications

**Slow generation:**
- Expected for CPU inference
- Use smaller model
- Consider upgrading to vLLM with GPU

## Resources

- Ollama Website: https://ollama.com
- Ollama GitHub: https://github.com/ollama/ollama
- Model Library: https://ollama.com/library
- API Documentation: https://github.com/ollama/ollama/blob/main/docs/api.md
