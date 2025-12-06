# Multi-Model Portability

Guide to writing prompts that work across different LLM providers (OpenAI, Anthropic, Google, Meta) and migrating prompts between models.

## Table of Contents

1. [Overview](#overview)
2. [Model Comparison](#model-comparison)
3. [System Prompt Compatibility](#system-prompt-compatibility)
4. [Token Limits and Context Windows](#token-limits-and-context-windows)
5. [Feature Parity Mapping](#feature-parity-mapping)
6. [Prompt Adaptation Strategies](#prompt-adaptation-strategies)
7. [Testing Across Models](#testing-across-models)
8. [Cost-Performance Tradeoffs](#cost-performance-tradeoffs)

## Overview

**Why Multi-Model Portability Matters:**
- Vendor lock-in avoidance
- Cost optimization (route to cheapest capable model)
- Reliability (fallback to alternative providers)
- Leverage model-specific strengths
- Future-proofing applications

**Portability challenges:**
- Different prompt formats and conventions
- Varying context window sizes
- Inconsistent feature support (JSON mode, tool calling)
- Model-specific behaviors and biases
- Different pricing structures

**Goal:** Write prompts that maintain quality across providers with minimal adaptation.

## Model Comparison

### Major LLM Providers (December 2024)

| Provider | Model | Context Window | Strengths | Best For |
|----------|-------|----------------|-----------|----------|
| **OpenAI** | GPT-4 Turbo | 128K | Fast, concise, strong reasoning | General tasks, quick responses |
| | GPT-4o | 128K | Multimodal, vision | Image analysis, multimodal tasks |
| | GPT-3.5 Turbo | 16K | Fast, cheap | Simple tasks, high volume |
| **Anthropic** | Claude 3.5 Sonnet | 200K | Long context, detailed, XML-friendly | Complex analysis, long documents |
| | Claude 3 Opus | 200K | Most capable, best quality | Critical tasks, research |
| | Claude 3 Haiku | 200K | Fast, cheap | Simple tasks, speed priority |
| **Google** | Gemini 1.5 Pro | 2M | Massive context, multimodal | Long documents, video analysis |
| | Gemini 1.5 Flash | 1M | Fast, efficient | Quick tasks, cost-sensitive |
| **Meta** | Llama 3.1 (70B) | 128K | Open source, self-hostable | Privacy, customization |
| | Llama 3.1 (8B) | 128K | Lightweight, fast | Edge deployment, low latency |

### Key Differences

**Instruction Following:**
- **GPT-4:** Excellent, prefers concise instructions
- **Claude 3:** Excellent, handles verbose/detailed instructions well
- **Gemini:** Good, sometimes over-cautious with safety
- **Llama 3:** Good, benefits from more explicit examples

**Formatting Preferences:**
- **GPT-4:** Markdown, JSON
- **Claude 3:** XML tags, Markdown
- **Gemini:** Markdown, structured text
- **Llama 3:** Simple formats, fewer special characters

**Reasoning Style:**
- **GPT-4:** Step-by-step, logical
- **Claude 3:** Thorough, considers edge cases
- **Gemini:** Factual, citation-focused
- **Llama 3:** Direct, less verbose

## System Prompt Compatibility

### Universal System Prompt Pattern

**Structure that works across all models:**
```python
UNIVERSAL_SYSTEM_PROMPT = """
Role: [Define the assistant's role clearly]

Capabilities:
- [Specific skill 1]
- [Specific skill 2]
- [Specific skill 3]

Guidelines:
- [Behavior guideline 1]
- [Behavior guideline 2]
- [Output format specification]

Constraints:
- [What NOT to do]
- [Boundaries and limitations]
"""
```

**Example: Customer Support Bot**
```python
# Works with OpenAI, Anthropic, Google, Meta
SUPPORT_SYSTEM_PROMPT = """
Role: Customer support assistant for TechCorp products.

Capabilities:
- Answer questions about product features
- Troubleshoot common technical issues
- Explain billing and subscription details
- Guide users through setup processes

Guidelines:
- Use friendly, professional tone
- Provide step-by-step instructions
- Ask clarifying questions when needed
- Cite specific documentation when available

Constraints:
- Do not promise refunds (escalate to human)
- Do not share customer data
- Do not diagnose hardware failures (escalate to tech support)
- Stay focused on TechCorp products only
"""
```

### Model-Specific System Prompt Adaptations

**OpenAI (System Message):**
```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": SUPPORT_SYSTEM_PROMPT},
        {"role": "user", "content": "How do I reset my password?"}
    ]
)
```

**Anthropic (System Parameter + XML):**
```python
from anthropic import Anthropic

client = Anthropic()

# Claude benefits from XML structure
CLAUDE_SYSTEM_PROMPT = """
<role>Customer support assistant for TechCorp products</role>

<capabilities>
- Answer questions about product features
- Troubleshoot common technical issues
- Explain billing and subscription details
- Guide users through setup processes
</capabilities>

<guidelines>
- Use friendly, professional tone
- Provide step-by-step instructions
- Ask clarifying questions when needed
- Cite specific documentation when available
</guidelines>

<constraints>
- Do not promise refunds (escalate to human)
- Do not share customer data
- Do not diagnose hardware failures (escalate to tech support)
- Stay focused on TechCorp products only
</constraints>
"""

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=CLAUDE_SYSTEM_PROMPT,
    messages=[
        {"role": "user", "content": "How do I reset my password?"}
    ]
)
```

**Google Gemini (System Instruction):**
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=SUPPORT_SYSTEM_PROMPT
)

response = model.generate_content("How do I reset my password?")
```

**Meta Llama (Prepended to First Message):**
```python
# Llama doesn't have separate system message in all implementations
# Prepend system prompt to first user message

def llama_format(system_prompt: str, user_message: str) -> str:
    return f"""<|system|>
{system_prompt}
<|end|>
<|user|>
{user_message}
<|end|>
<|assistant|>"""

prompt = llama_format(SUPPORT_SYSTEM_PROMPT, "How do I reset my password?")
```

## Token Limits and Context Windows

### Context Window Sizes (2024)

| Model | Input Limit | Output Limit | Total |
|-------|-------------|--------------|-------|
| GPT-4 Turbo | ~120K tokens | 4K tokens | 128K |
| GPT-4o | ~120K tokens | 16K tokens | 128K |
| Claude 3.5 Sonnet | ~180K tokens | 20K tokens | 200K |
| Gemini 1.5 Pro | ~2M tokens | 8K tokens | 2M |
| Llama 3.1 70B | ~120K tokens | 8K tokens | 128K |

### Adaptive Prompting for Token Limits

```python
def get_model_limits(model_name: str) -> dict:
    """Get token limits for different models."""
    limits = {
        "gpt-4": {"input": 120000, "output": 4096},
        "gpt-4o": {"input": 120000, "output": 16384},
        "claude-3-5-sonnet": {"input": 180000, "output": 20000},
        "gemini-1.5-pro": {"input": 2000000, "output": 8192},
        "llama-3.1-70b": {"input": 120000, "output": 8192},
    }
    return limits.get(model_name, {"input": 100000, "output": 4096})

def adapt_context_for_model(context: str, model_name: str) -> str:
    """Truncate context to fit model limits."""
    import tiktoken

    limits = get_model_limits(model_name)
    max_input = limits["input"]

    # Estimate tokens (rough approximation)
    enc = tiktoken.encoding_for_model("gpt-4")  # Use GPT-4 tokenizer as approximation
    tokens = enc.encode(context)

    if len(tokens) > max_input:
        # Truncate to fit
        truncated = enc.decode(tokens[:max_input])
        return truncated + "\n\n[Context truncated to fit model limits]"

    return context
```

### Smart Summarization for Large Context

```python
def smart_context_handling(long_context: str, query: str, model: str):
    """Use different strategies based on model capabilities."""

    limits = get_model_limits(model)

    if model == "gemini-1.5-pro":
        # Gemini can handle massive context, send everything
        return long_context

    elif model.startswith("claude"):
        # Claude has good context handling, can send most
        return adapt_context_for_model(long_context, model)

    elif model.startswith("gpt"):
        # GPT has smaller context, summarize first
        if len(long_context) > 50000:
            summary_prompt = f"Summarize this context for the query: {query}\n\n{long_context}"
            summary = summarize_with_llm(summary_prompt)
            return summary
        return long_context

    else:
        # For unknown models, be conservative
        return adapt_context_for_model(long_context, model)[:50000]
```

## Feature Parity Mapping

### JSON Mode / Structured Outputs

**OpenAI JSON Mode:**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Extract user data as JSON."},
        {"role": "user", "content": "Name: Sarah, Age: 28, Email: sarah@example.com"}
    ],
    response_format={"type": "json_object"}
)
```

**Anthropic Tool Use (for JSON):**
```python
tools = [{
    "name": "record_user_data",
    "description": "Record structured user information",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string"}
        },
        "required": ["name", "age", "email"]
    }
}]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Name: Sarah, Age: 28, Email: sarah@example.com"}]
)

# Extract tool input as JSON
json_data = response.content[0].input
```

**Gemini JSON Mode:**
```python
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content(
    "Extract: Name: Sarah, Age: 28",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
    )
)
```

**Llama (Prompt Engineering):**
```python
# Llama doesn't have native JSON mode, use strong prompting
prompt = """
Extract user data in JSON format. Output ONLY valid JSON, nothing else.

Input: Name: Sarah, Age: 28, Email: sarah@example.com

JSON Output:
"""
# Parse and validate manually
```

### Function Calling / Tool Use

**OpenAI Function Calling:**
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto"
)
```

**Anthropic Tool Use:**
```python
tools = [{
    "name": "get_weather",
    "description": "Get weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
}]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
```

**Gemini Function Calling:**
```python
tools = [genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="get_weather",
            description="Get weather for a location",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    'location': genai.protos.Schema(type=genai.protos.Type.STRING)
                },
                required=['location']
            )
        )
    ]
)]

model = genai.GenerativeModel('gemini-1.5-pro', tools=tools)
response = model.generate_content("What's the weather in Tokyo?")
```

**Feature Availability Matrix:**

| Feature | OpenAI | Anthropic | Google | Llama |
|---------|--------|-----------|--------|-------|
| JSON Mode | ✅ Native | ⚠️ Via Tools | ✅ Native | ❌ Prompt only |
| Function Calling | ✅ Native | ✅ Native | ✅ Native | ❌ Prompt only |
| Streaming | ✅ | ✅ | ✅ | ✅ |
| Vision (Images) | ✅ (GPT-4o) | ✅ (Claude 3+) | ✅ Native | ❌ |
| Prompt Caching | ❌ | ✅ | ✅ | ✅ (Impl. specific) |

## Prompt Adaptation Strategies

### Strategy 1: Abstract Prompt Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class PromptProvider(ABC):
    """Abstract interface for model-specific prompts."""

    @abstractmethod
    def format_system_prompt(self, content: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def format_user_message(self, content: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def format_json_request(self, prompt: str, schema: dict) -> Dict[str, Any]:
        pass

class OpenAIProvider(PromptProvider):
    def format_system_prompt(self, content: str) -> Dict[str, Any]:
        return {"role": "system", "content": content}

    def format_user_message(self, content: str) -> Dict[str, Any]:
        return {"role": "user", "content": content}

    def format_json_request(self, prompt: str, schema: dict) -> Dict[str, Any]:
        return {
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

class AnthropicProvider(PromptProvider):
    def format_system_prompt(self, content: str) -> Dict[str, Any]:
        # Add XML structure for Claude
        return {"system": self._add_xml_structure(content)}

    def format_user_message(self, content: str) -> Dict[str, Any]:
        return {"role": "user", "content": content}

    def format_json_request(self, prompt: str, schema: dict) -> Dict[str, Any]:
        # Convert to tool use
        tool = self._schema_to_tool(schema)
        return {
            "messages": [{"role": "user", "content": prompt}],
            "tools": [tool]
        }

    def _add_xml_structure(self, content: str) -> str:
        # Add XML tags for better Claude parsing
        if "<role>" not in content:
            # Wrap in basic XML
            return f"<instructions>\n{content}\n</instructions>"
        return content

    def _schema_to_tool(self, schema: dict) -> dict:
        return {
            "name": "extract_data",
            "description": "Extract structured data",
            "input_schema": schema
        }

# Usage
def generate_with_provider(prompt: str, provider: PromptProvider):
    system_msg = provider.format_system_prompt("You are a helpful assistant.")
    user_msg = provider.format_user_message(prompt)

    if isinstance(provider, OpenAIProvider):
        # Call OpenAI
        pass
    elif isinstance(provider, AnthropicProvider):
        # Call Anthropic
        pass
```

### Strategy 2: Prompt Translation Layer

```python
def translate_prompt_for_model(
    prompt: str,
    source_model: str,
    target_model: str
) -> str:
    """Translate prompt from one model's style to another."""

    if source_model.startswith("gpt") and target_model.startswith("claude"):
        # GPT → Claude: Add XML structure
        return add_xml_structure(prompt)

    elif source_model.startswith("claude") and target_model.startswith("gpt"):
        # Claude → GPT: Remove XML, make more concise
        return remove_xml_structure(prompt)

    elif target_model.startswith("llama"):
        # Any → Llama: Simplify, add more examples
        return simplify_for_llama(prompt)

    return prompt

def add_xml_structure(prompt: str) -> str:
    """Add XML tags for Claude."""
    if "<" not in prompt:
        sections = prompt.split("\n\n")
        xml_parts = []
        for section in sections:
            if section.startswith("Role:"):
                xml_parts.append(f"<role>{section[5:].strip()}</role>")
            elif section.startswith("Guidelines:"):
                xml_parts.append(f"<guidelines>\n{section[11:].strip()}\n</guidelines>")
            else:
                xml_parts.append(section)
        return "\n\n".join(xml_parts)
    return prompt

def remove_xml_structure(prompt: str) -> str:
    """Remove XML tags for GPT."""
    import re
    # Remove XML tags
    cleaned = re.sub(r'<[^>]+>', '', prompt)
    # Remove extra whitespace
    cleaned = re.sub(r'\n\n+', '\n\n', cleaned)
    return cleaned.strip()

def simplify_for_llama(prompt: str) -> str:
    """Simplify and add examples for Llama."""
    # Add explicit instruction markers
    simplified = "INSTRUCTION:\n" + prompt + "\n\nRESPONSE:"
    return simplified
```

### Strategy 3: Multi-Model Wrapper

```python
from typing import Union, Optional
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

class UniversalLLM:
    """Unified interface for multiple LLM providers."""

    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model

        if provider == "openai":
            self.client = OpenAI()
        elif provider == "anthropic":
            self.client = Anthropic()
        elif provider == "google":
            genai.configure()
            self.client = genai.GenerativeModel(model)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """Generate text using unified interface."""

        if self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

        elif self.provider == "anthropic":
            # Adapt system prompt for Claude
            if system_prompt:
                system_prompt = add_xml_structure(system_prompt)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif self.provider == "google":
            # Gemini
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = self.client.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            return response.text

# Usage
llm = UniversalLLM("anthropic", "claude-3-5-sonnet-20241022")
result = llm.generate(
    "Explain quantum computing",
    system_prompt="You are a physics teacher."
)
```

## Testing Across Models

### Test Suite for Prompt Portability

```python
import pytest
from typing import List, Dict

class PromptTest:
    """Test prompt across multiple models."""

    def __init__(self, prompt: str, expected_patterns: List[str]):
        self.prompt = prompt
        self.expected_patterns = expected_patterns

    def test_with_model(self, model: UniversalLLM) -> Dict[str, bool]:
        """Test if prompt produces expected output patterns."""
        response = model.generate(self.prompt)

        results = {}
        for pattern in self.expected_patterns:
            results[pattern] = pattern.lower() in response.lower()

        return results

# Example tests
def test_classification_prompt():
    """Test sentiment classification across models."""
    prompt = "Classify sentiment: 'This product is amazing!'"
    expected = ["positive"]

    models = [
        UniversalLLM("openai", "gpt-4"),
        UniversalLLM("anthropic", "claude-3-5-sonnet-20241022"),
    ]

    for model in models:
        test = PromptTest(prompt, expected)
        results = test.test_with_model(model)
        assert all(results.values()), f"Failed for {model.provider}: {results}"

def test_json_extraction():
    """Test JSON extraction across models."""
    prompt = "Extract name and age as JSON: 'John is 25 years old'"
    expected = ["john", "25", "{", "}"]

    models = [
        UniversalLLM("openai", "gpt-4"),
        UniversalLLM("anthropic", "claude-3-5-sonnet-20241022"),
    ]

    for model in models:
        test = PromptTest(prompt, expected)
        results = test.test_with_model(model)
        assert all(results.values()), f"Failed for {model.provider}"
```

### A/B Testing Framework

```python
import asyncio
from typing import List, Tuple

async def ab_test_models(
    prompt: str,
    models: List[Tuple[str, str]],  # [(provider, model_name), ...]
    num_runs: int = 5
) -> Dict[str, Dict]:
    """Compare prompt performance across models."""

    results = {}

    for provider, model_name in models:
        model = UniversalLLM(provider, model_name)
        outputs = []
        latencies = []

        for _ in range(num_runs):
            import time
            start = time.time()
            output = model.generate(prompt)
            latency = time.time() - start

            outputs.append(output)
            latencies.append(latency)

        results[f"{provider}/{model_name}"] = {
            "outputs": outputs,
            "avg_latency": sum(latencies) / len(latencies),
            "consistency": len(set(outputs)) / len(outputs)  # 1.0 = all unique, 0.x = some repeats
        }

    return results

# Usage
async def main():
    models = [
        ("openai", "gpt-4"),
        ("anthropic", "claude-3-5-sonnet-20241022"),
        ("google", "gemini-1.5-pro")
    ]

    results = await ab_test_models(
        "Explain the concept of recursion in programming.",
        models,
        num_runs=3
    )

    for model, metrics in results.items():
        print(f"\n{model}:")
        print(f"  Avg Latency: {metrics['avg_latency']:.2f}s")
        print(f"  Consistency: {metrics['consistency']:.2f}")
```

## Cost-Performance Tradeoffs

### Pricing Comparison (Approximate, 2024)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Best For |
|-------|----------------------|------------------------|----------|
| GPT-4 Turbo | $10 | $30 | Balanced performance |
| GPT-4o | $5 | $15 | Cost-effective GPT-4 |
| GPT-3.5 Turbo | $0.50 | $1.50 | High-volume, simple tasks |
| Claude 3.5 Sonnet | $3 | $15 | Long context, quality |
| Claude 3 Haiku | $0.25 | $1.25 | Fast, cheap |
| Gemini 1.5 Pro | $7 | $21 | Massive context |
| Gemini 1.5 Flash | $0.35 | $1.05 | Cost-effective |

### Intelligent Model Routing

```python
def route_to_optimal_model(
    prompt: str,
    requirements: Dict[str, Any]
) -> Tuple[str, str]:
    """Route to most cost-effective model that meets requirements."""

    prompt_length = len(prompt)
    needs_reasoning = requirements.get("reasoning", False)
    needs_vision = requirements.get("vision", False)
    budget = requirements.get("budget", "medium")

    # Vision required
    if needs_vision:
        if budget == "low":
            return ("google", "gemini-1.5-flash")
        else:
            return ("openai", "gpt-4o")

    # Very long context
    if prompt_length > 100000:
        return ("google", "gemini-1.5-pro")

    # Complex reasoning
    if needs_reasoning:
        if budget == "low":
            return ("anthropic", "claude-3-haiku")
        elif budget == "high":
            return ("anthropic", "claude-3-opus")
        else:
            return ("openai", "gpt-4")

    # Simple tasks
    if budget == "low":
        return ("openai", "gpt-3.5-turbo")

    # Default
    return ("anthropic", "claude-3-5-sonnet-20241022")

# Usage
provider, model = route_to_optimal_model(
    "Translate this to French: Hello world",
    {"reasoning": False, "budget": "low"}
)
# Returns: ("openai", "gpt-3.5-turbo")
```

---

**Related Files:**
- `rag-patterns.md` - Multi-model RAG implementations
- `tool-use-guide.md` - Tool calling across providers
- `examples/openai-examples.py` - OpenAI-specific patterns
- `examples/anthropic-examples.py` - Anthropic-specific patterns

**Key Takeaways:**
1. Write provider-agnostic prompts when possible
2. Use abstraction layers for multi-model support
3. Test prompts across target models
4. Adapt system prompts to model preferences (XML for Claude, concise for GPT)
5. Be aware of context window limits
6. Route intelligently based on task requirements and cost
7. Handle feature gaps gracefully (JSON mode, function calling)
