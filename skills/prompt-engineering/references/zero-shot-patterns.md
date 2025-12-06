# Zero-Shot Prompting Patterns

Zero-shot prompting involves providing clear instructions without examples, relying on the model's pre-trained knowledge to complete tasks.

## Table of Contents

- [When to Use Zero-Shot](#when-to-use-zero-shot)
- [Core Pattern Structure](#core-pattern-structure)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [Anti-Patterns](#anti-patterns)
- [Temperature Settings](#temperature-settings)
- [Multi-Language Examples](#multi-language-examples)

## When to Use Zero-Shot

**Ideal for:**
- Simple, well-defined tasks with clear outputs
- Tasks the model has likely seen during training (translation, summarization)
- Minimizing token usage and API costs
- Quick prototyping before investing in few-shot examples

**Not suitable for:**
- Complex reasoning requiring intermediate steps (use Chain-of-Thought)
- Tasks requiring specific formatting not easily described (use Few-Shot)
- Domain-specific styles or conventions (use Few-Shot with examples)

## Core Pattern Structure

```
[Clear instruction]
[Optional context/constraints]
[Input data]
[Output format specification]
```

### Minimal Pattern

```python
prompt = """
Translate the following text to Spanish:

"{text}"
"""
```

### Detailed Pattern

```python
prompt = """
Task: Summarize customer reviews for product analysis.

Requirements:
- Extract key themes (positive and negative)
- Identify mentioned features
- Note any recurring issues
- Length: 3-5 bullet points

Input:
{customer_reviews}

Summary:
"""
```

## Best Practices

### 1. Be Explicit About Constraints

**BAD:**
```python
"Summarize this article."
```

**GOOD:**
```python
"Summarize this article in exactly 3 sentences, focusing on: 1) Main argument, 2) Supporting evidence, 3) Conclusion."
```

### 2. Use Imperative Voice

**BAD:**
```python
"Can you please translate this to French?"
"I would like you to analyze this data."
```

**GOOD:**
```python
"Translate to French:"
"Analyze this data for trends:"
```

### 3. Specify Output Format Upfront

**BAD:**
```python
"List the ingredients in this recipe."
```

**GOOD:**
```python
"List the ingredients in this recipe. Format as JSON array of objects with 'name' and 'quantity' fields."
```

### 4. Provide Context When Necessary

**Without context (unclear):**
```python
"Is this good or bad?"
```

**With context (clear):**
```python
"Classify the sentiment of this product review as 'positive', 'negative', or 'neutral':

Review: {review_text}
Sentiment:"
```

### 5. Set Appropriate Temperature

```python
# Deterministic tasks (classification, extraction)
response = client.create(temperature=0, ...)

# Slightly varied outputs (summarization)
response = client.create(temperature=0.3, ...)

# Creative tasks (NOT zero-shot territory)
response = client.create(temperature=0.7, ...)
```

## Common Use Cases

### Translation

```python
from openai import OpenAI
client = OpenAI()

prompt = """
Translate the following English text to French. Maintain the original tone and formality.

English: "{text}"

French:
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)
```

### Summarization

```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Summarize this research paper abstract in 2 sentences for a general audience. Avoid technical jargon.

Abstract:
{abstract_text}

Summary:
"""

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)
```

### Classification

```python
prompt = """
Classify the following customer support ticket into one of these categories:
- billing
- technical_issue
- feature_request
- general_inquiry

Ticket: "{ticket_text}"

Category:
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,  # Deterministic classification
    max_tokens=10
)
```

### Entity Extraction

```python
prompt = """
Extract all person names and locations from the following text. Return as JSON with arrays "people" and "locations".

Text: "{input_text}"

JSON:
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"},
    temperature=0
)
```

### Code Generation

```python
prompt = """
Write a Python function that calculates the factorial of a number using recursion.

Requirements:
- Include type hints
- Add docstring
- Handle edge case of n=0
- Raise ValueError for negative inputs

Function:
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)
```

## Anti-Patterns

### 1. Overly Vague Instructions

**BAD:**
```python
"Tell me about this."
```

**GOOD:**
```python
"Explain what this Python code does, focusing on: 1) Purpose, 2) Inputs/outputs, 3) Key algorithms used."
```

### 2. Implicit Assumptions

**BAD:**
```python
"Rewrite this better."  # Better how?
```

**GOOD:**
```python
"Rewrite this text to be more concise while preserving key information. Target 50% reduction in word count."
```

### 3. Asking Questions Instead of Giving Instructions

**BAD:**
```python
"Can you help me understand this concept?"
"Would you be able to translate this?"
```

**GOOD:**
```python
"Explain this concept in simple terms with an analogy."
"Translate this text to Spanish."
```

### 4. Not Specifying Edge Cases

**BAD:**
```python
"Extract email addresses from this text."
```

**GOOD:**
```python
"Extract all email addresses from this text. If no emails found, return empty array. Return as JSON array of strings."
```

### 5. Mixing Multiple Tasks

**BAD:**
```python
"Translate this to French and also summarize it and extract key entities."
```

**GOOD (separate prompts or structured approach):**
```python
# Step 1: Translate
translation = translate(text)

# Step 2: Summarize
summary = summarize(translation)

# Step 3: Extract entities
entities = extract_entities(translation)
```

## Temperature Settings

### Temperature = 0 (Deterministic)

**Use for:**
- Classification tasks
- Data extraction
- Formatting and parsing
- Any task requiring consistency across runs

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Classify sentiment: {text}"}],
    temperature=0
)
```

### Temperature = 0.3-0.5 (Slightly Varied)

**Use for:**
- Summarization
- Explanations
- Translations
- Tasks where minor variation is acceptable

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Summarize: {text}"}],
    temperature=0.3
)
```

### Temperature > 0.7 (Creative)

**Generally avoid for zero-shot** - high variance can lead to inconsistent outputs. Use few-shot or structured prompts instead if creativity is needed.

## Multi-Language Examples

### Python + OpenAI

```python
from openai import OpenAI

client = OpenAI()

def zero_shot_classify(text: str) -> str:
    """Classify text sentiment using zero-shot prompting."""
    prompt = f"""
    Classify the sentiment of this text as 'positive', 'negative', or 'neutral'.

    Text: "{text}"

    Sentiment:
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10
    )

    return response.choices[0].message.content.strip().lower()

# Usage
result = zero_shot_classify("This product exceeded my expectations!")
print(result)  # "positive"
```

### Python + Anthropic

```python
import anthropic

client = anthropic.Anthropic()

def zero_shot_summarize(text: str, max_sentences: int = 3) -> str:
    """Summarize text using zero-shot prompting."""
    prompt = f"""
    Summarize the following text in exactly {max_sentences} sentences.

    Text:
    {text}

    Summary:
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return message.content[0].text

# Usage
summary = zero_shot_summarize(long_article, max_sentences=3)
```

### TypeScript + Vercel AI SDK

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

async function zeroShotExtract(text: string): Promise<string[]> {
  const prompt = `
Extract all email addresses from the following text.
Return as comma-separated list.

Text: "${text}"

Emails:
  `;

  const { text: result } = await generateText({
    model: openai('gpt-4'),
    prompt,
    temperature: 0,
  });

  return result.split(',').map(email => email.trim());
}

// Usage
const emails = await zeroShotExtract(
  "Contact us at support@example.com or sales@example.com"
);
console.log(emails); // ["support@example.com", "sales@example.com"]
```

### TypeScript + Anthropic SDK

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

async function zeroShotClassify(text: string): Promise<string> {
  const prompt = `
Classify this customer inquiry into one category:
- billing
- technical_support
- sales
- general

Inquiry: "${text}"

Category:
  `;

  const message = await client.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 20,
    messages: [{ role: 'user', content: prompt }],
    temperature: 0,
  });

  return message.content[0].text.trim().toLowerCase();
}
```

## When to Upgrade from Zero-Shot

Upgrade to more advanced techniques when experiencing:

1. **Inconsistent outputs** → Add few-shot examples
2. **Poor reasoning** → Use Chain-of-Thought
3. **Format issues** → Use structured outputs (JSON mode)
4. **Domain-specific requirements** → Add few-shot examples or fine-tuning
5. **Complex multi-step tasks** → Use prompt chaining

## Cost Optimization Tips

1. **Minimize prompt length** - Remove unnecessary words while maintaining clarity
2. **Use shorter models for simple tasks** - GPT-3.5 or Claude Haiku vs GPT-4/Opus
3. **Cache common prefixes** - Use Anthropic's prompt caching for repeated context
4. **Batch similar requests** - Process multiple items in single prompt when possible
5. **Set appropriate max_tokens** - Don't request more tokens than needed

## Testing Zero-Shot Prompts

```python
import pytest

test_cases = [
    {"input": "I love this product!", "expected": "positive"},
    {"input": "Terrible experience.", "expected": "negative"},
    {"input": "It's okay.", "expected": "neutral"},
]

@pytest.mark.parametrize("case", test_cases)
def test_sentiment_classification(case):
    result = zero_shot_classify(case["input"])
    assert result == case["expected"]
```

## Summary

Zero-shot prompting is the foundation of prompt engineering - master clear, explicit instructions before moving to advanced techniques. The key is specificity: define the task, constraints, format, and expected output without ambiguity.

**Key takeaways:**
- Be explicit about requirements and constraints
- Use imperative voice
- Specify output format upfront
- Set temperature=0 for deterministic tasks
- Test on diverse inputs to identify when to upgrade techniques
