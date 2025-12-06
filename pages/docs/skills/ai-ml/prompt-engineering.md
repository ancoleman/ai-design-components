---
sidebar_position: 2
title: Prompt Engineering
description: Engineer effective LLM prompts using zero-shot, few-shot, chain-of-thought, and structured output techniques
tags: [ai-ml, prompt-engineering, llm, gpt, claude, langchain, rag]
---

# Prompt Engineering

Design and optimize prompts for large language models (LLMs) to achieve reliable, high-quality outputs across diverse tasks.

## When to Use

Use this skill when:

- Building LLM-powered applications requiring consistent outputs
- Model outputs are unreliable, inconsistent, or hallucinating
- Need structured data (JSON) from natural language inputs
- Implementing multi-step reasoning tasks (math, logic, analysis)
- Creating AI agents that use tools and external APIs
- Optimizing prompt costs or latency in production systems
- Migrating prompts across different model providers
- Establishing prompt versioning and testing workflows

## Key Features

### 1. Prompting Technique Decision Framework

**Choose the right technique based on task requirements:**

| Goal | Technique | Token Cost | Reliability | Use Case |
|------|-----------|------------|-------------|----------|
| Simple, well-defined task | Zero-Shot | Minimal | Medium | Translation, simple summarization |
| Specific format/style | Few-Shot | Medium | High | Classification, entity extraction |
| Complex reasoning | Chain-of-Thought | Higher | Very High | Math, logic, multi-hop QA |
| Structured data output | JSON Mode / Tools | Low-Med | Very High | API responses, data extraction |
| Multi-step workflows | Prompt Chaining | Medium | High | Pipelines, complex tasks |
| Knowledge retrieval | RAG | Higher | High | QA over documents |
| Agent behaviors | ReAct (Tool Use) | Highest | Medium | Multi-tool, complex tasks |

### 2. Zero-Shot Prompting

**Pattern:** Clear instruction + optional context + input + output format

**Best Practices:**
- Be specific about constraints and requirements
- Use imperative voice ("Summarize...", not "Can you summarize...")
- Specify output format upfront
- Set `temperature=0` for deterministic outputs

**Example:**
```python
prompt = """
Summarize the following customer review in 2 sentences, focusing on key concerns:

Review: [customer feedback text]

Summary:
"""
```

### 3. Chain-of-Thought (CoT)

**Pattern:** Task + "Let's think step by step" + reasoning steps → answer

**When to Use:** Complex reasoning tasks (math problems, multi-hop logic, analysis)

**Research Foundation:** Wei et al. (2022) demonstrated 20-50% accuracy improvements on reasoning benchmarks

**Zero-Shot CoT:**
```python
prompt = """
Solve this problem step by step:

A train leaves Station A at 2 PM going 60 mph.
Another leaves Station B at 3 PM going 80 mph.
Stations are 300 miles apart. When do they meet?

Let's think through this step by step:
"""
```

### 4. Few-Shot Learning

**Pattern:** Task description + 2-5 examples (input → output) + actual task

**Sweet Spot:** 2-5 examples (quality > quantity)

**Best Practices:**
- Use diverse, representative examples
- Maintain consistent formatting
- Randomize example order to avoid position bias
- Label edge cases explicitly

**Example:**
```python
prompt = """
Classify sentiment of movie reviews.

Examples:
Review: "Absolutely fantastic! Loved every minute."
Sentiment: positive

Review: "Waste of time. Terrible acting."
Sentiment: negative

Review: "It was okay, nothing special."
Sentiment: neutral

Review: "{new_review}"
Sentiment:
"""
```

### 5. Structured Output Generation

**Modern Approach (2025):** Use native JSON modes and tool calling

**OpenAI JSON Mode:**
```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Extract user data as JSON."},
        {"role": "user", "content": "From bio: 'Sarah, 28, sarah@example.com'"}
    ],
    response_format={"type": "json_object"}
)
```

**TypeScript with Zod:**
```typescript
import { generateObject } from 'ai';
import { z } from 'zod';

const schema = z.object({
  name: z.string(),
  age: z.number(),
});

const { object } = await generateObject({
  model: openai('gpt-4'),
  schema,
  prompt: 'Extract: "Sarah, 28"',
});
```

### 6. Tool Use and Function Calling

**Pattern:** Define functions → Model decides when to call → Execute → Return results → Model synthesizes

**OpenAI Function Calling:**
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
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

### 7. Prompt Chaining and Composition

**Pattern:** Break complex tasks into sequential prompts

**LangChain LCEL Example:**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

summarize_prompt = ChatPromptTemplate.from_template(
    "Summarize: {article}"
)
title_prompt = ChatPromptTemplate.from_template(
    "Create title for: {summary}"
)

llm = ChatOpenAI(model="gpt-4")
chain = summarize_prompt | llm | title_prompt | llm

result = chain.invoke({"article": "..."})
```

**Anthropic Prompt Caching:**
```python
# Cache large context (90% cost reduction on subsequent calls)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=[
        {"type": "text", "text": "You are a coding assistant."},
        {
            "type": "text",
            "text": f"Codebase:\n\n{large_codebase}",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Explain auth module"}]
)
```

## Quick Start

### Zero-Shot Prompt (Python + OpenAI)
```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize this article in 3 sentences: [text]"}
    ],
    temperature=0  # Deterministic output
)
print(response.choices[0].message.content)
```

### Structured Output (TypeScript + Vercel AI SDK)
```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const schema = z.object({
  name: z.string(),
  sentiment: z.enum(['positive', 'negative', 'neutral']),
});

const { object } = await generateObject({
  model: openai('gpt-4'),
  schema,
  prompt: 'Extract sentiment from: "This product is amazing!"',
});
```

## Library Recommendations

### Python Ecosystem
- **LangChain**: Complex RAG, agents, multi-step workflows
- **LlamaIndex**: Document indexing, knowledge base QA
- **DSPy**: Programmatic prompt optimization
- **OpenAI SDK**: Direct OpenAI access
- **Anthropic SDK**: Claude integration

### TypeScript Ecosystem
- **Vercel AI SDK**: Next.js/React AI apps (modern, type-safe)
- **LangChain.js**: JavaScript port
- **Provider SDKs**: openai, @anthropic-ai/sdk

| Library | Complexity | Multi-Provider | Best For |
|---------|------------|----------------|----------|
| LangChain | High | ✅ | Complex workflows, RAG |
| LlamaIndex | Medium | ✅ | Data-centric RAG |
| DSPy | High | ✅ | Research, optimization |
| Vercel AI SDK | Low-Medium | ✅ | React/Next.js apps |
| Provider SDKs | Low | ❌ | Single-provider apps |

## Production Best Practices

### 1. Prompt Versioning
```python
PROMPTS = {
    "v1.0": {
        "system": "You are a helpful assistant.",
        "version": "2025-01-15",
        "notes": "Initial version"
    },
    "v1.1": {
        "system": "You are a helpful assistant. Always cite sources.",
        "version": "2025-02-01",
        "notes": "Reduced hallucination"
    }
}
```

### 2. Cost and Token Monitoring
```python
def tracked_completion(prompt, model):
    response = client.messages.create(model=model, ...)
    usage = response.usage
    cost = calculate_cost(usage.input_tokens, usage.output_tokens, model)

    log_metrics({
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cost_usd": cost,
        "timestamp": datetime.now()
    })
    return response
```

### 3. Error Handling and Retries
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def robust_completion(prompt):
    try:
        return client.messages.create(...)
    except anthropic.RateLimitError:
        raise  # Retry
    except anthropic.APIError as e:
        return fallback_completion(prompt)
```

### 4. Input Sanitization
```python
def sanitize_user_input(text: str) -> str:
    dangerous = [
        "ignore previous instructions",
        "ignore all instructions",
        "you are now",
    ]

    cleaned = text.lower()
    for pattern in dangerous:
        if pattern in cleaned:
            raise ValueError("Potential injection detected")
    return text
```

## Multi-Model Portability

**OpenAI GPT-4:**
- Strong at complex instructions
- Use system messages for global behavior
- Prefers concise prompts

**Anthropic Claude:**
- Excels with XML-structured prompts
- Use `<thinking>` tags for chain-of-thought
- Prefers detailed instructions

**Google Gemini:**
- Multimodal by default (text + images)
- Strong at code generation
- More aggressive safety filters

**Meta Llama (Open Source):**
- Requires more explicit instructions
- Few-shot examples critical
- Self-hosted, full control

## Related Skills

- **building-ai-chat**: Conversational AI patterns and system messages
- **evaluating-llms**: Testing and validating prompt quality
- **model-serving**: Deploying prompt-based applications
- **designing-apis**: LLM API integration patterns
- **generating-documentation**: LLM-powered documentation tools

## References

- Full skill documentation: `/skills/prompt-engineering/SKILL.md`
- Zero-shot patterns: `/skills/prompt-engineering/references/zero-shot-patterns.md`
- Chain-of-thought: `/skills/prompt-engineering/references/chain-of-thought.md`
- Few-shot learning: `/skills/prompt-engineering/references/few-shot-learning.md`
- Structured outputs: `/skills/prompt-engineering/references/structured-outputs.md`
- Tool use guide: `/skills/prompt-engineering/references/tool-use-guide.md`
- Prompt chaining: `/skills/prompt-engineering/references/prompt-chaining.md`
- RAG patterns: `/skills/prompt-engineering/references/rag-patterns.md`
- Multi-model portability: `/skills/prompt-engineering/references/multi-model-portability.md`
