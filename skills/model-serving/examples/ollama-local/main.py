"""
Ollama Local Development Example

Simple local LLM serving for development without GPU requirements.
Perfect for prototyping AI applications on laptops.
"""

import requests
import json

OLLAMA_URL = "http://localhost:11434"

def generate(prompt: str, model: str = "llama3.1:8b", stream: bool = False):
    """
    Generate response from Ollama.

    Args:
        prompt: User prompt
        model: Model name (use `ollama list` to see available)
        stream: Whether to stream response
    """
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    if stream:
        # Streaming response
        response = requests.post(url, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if not data.get("done"):
                    print(data["response"], end="", flush=True)
                else:
                    print()  # New line at end
    else:
        # Non-streaming response
        response = requests.post(url, json=payload)
        result = response.json()
        return result["response"]

def chat(messages: list[dict], model: str = "llama3.1:8b", stream: bool = False):
    """
    Chat with Ollama using conversation history.

    Args:
        messages: List of {"role": "user"|"assistant"|"system", "content": "..."}
        model: Model name
        stream: Whether to stream response
    """
    url = f"{OLLAMA_URL}/api/chat"

    payload = {
        "model": model,
        "messages": messages,
        "stream": stream
    }

    if stream:
        response = requests.post(url, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if not data.get("done"):
                    print(data["message"]["content"], end="", flush=True)
                else:
                    print()
    else:
        response = requests.post(url, json=payload)
        result = response.json()
        return result["message"]["content"]

def list_models():
    """List available models."""
    url = f"{OLLAMA_URL}/api/tags"
    response = requests.get(url)
    models = response.json()

    print("Available models:")
    for model in models["models"]:
        print(f"- {model['name']} (size: {model['size'] / 1e9:.1f}GB)")

if __name__ == "__main__":
    print("Ollama Local Development Example\n")

    # Example 1: Simple generation
    print("Example 1: Simple generation")
    print("-" * 50)
    prompt = "Explain PagedAttention in one paragraph."
    print(f"Prompt: {prompt}\n")
    response = generate(prompt, stream=False)
    print(f"Response: {response}\n")

    # Example 2: Streaming generation
    print("\nExample 2: Streaming generation")
    print("-" * 50)
    prompt = "Count to 5 slowly."
    print(f"Prompt: {prompt}\n")
    print("Response: ", end="")
    generate(prompt, stream=True)

    # Example 3: Conversational chat
    print("\nExample 3: Conversational chat")
    print("-" * 50)

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is vLLM?"}
    ]

    print("User: What is vLLM?")
    response = chat(messages, stream=False)
    print(f"Assistant: {response}\n")

    # Follow-up
    messages.append({"role": "assistant", "content": response})
    messages.append({"role": "user", "content": "How does it improve throughput?"})

    print("User: How does it improve throughput?")
    print("Assistant: ", end="")
    chat(messages, stream=True)

    # List available models
    print("\n")
    list_models()
