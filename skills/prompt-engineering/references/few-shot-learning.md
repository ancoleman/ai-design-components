# Few-Shot Learning

Few-shot learning provides 2-5 examples of desired input-output pairs to guide model behavior without fine-tuning.

## Table of Contents

- [When to Use Few-Shot](#when-to-use-few-shot)
- [Core Pattern](#core-pattern)
- [Example Selection Strategies](#example-selection-strategies)
- [Best Practices](#best-practices)
- [Implementation Examples](#implementation-examples)
- [Common Pitfalls](#common-pitfalls)

## When to Use Few-Shot

**Ideal for:**
- Tasks requiring specific formatting or style
- Classification with nuanced categories
- Entity extraction with custom schemas
- Style transfer or tone matching
- Domain-specific conventions

**Not necessary for:**
- Tasks model performs well zero-shot
- When clear instructions suffice
- High token cost sensitivity (examples add tokens)

## Core Pattern

```
{Task description}

Examples:
Input: {example_input_1}
Output: {example_output_1}

Input: {example_input_2}
Output: {example_output_2}

[Optional: 1-3 more examples]

Now complete:
Input: {actual_input}
Output:
```

## Example Selection Strategies

### 1. Diversity Over Quantity

```python
# BAD: 10 similar examples
examples = [
    {"input": "Great product!", "output": "positive"},
    {"input": "Love it!", "output": "positive"},
    {"input": "Amazing quality!", "output": "positive"},
    # ... 7 more positive examples
]

# GOOD: 3-5 diverse examples
examples = [
    {"input": "Great product!", "output": "positive"},
    {"input": "Terrible experience", "output": "negative"},
    {"input": "It's okay, nothing special", "output": "neutral"},
    {"input": "Love it but pricey", "output": "mixed"},  # Edge case
]
```

### 2. Include Edge Cases

```python
examples = [
    # Standard cases
    {"input": "john@example.com", "output": "valid"},
    {"input": "invalid-email", "output": "invalid"},

    # Edge cases
    {"input": "user+tag@example.com", "output": "valid"},  # Plus addressing
    {"input": "user@subdomain.example.com", "output": "valid"},  # Subdomain
    {"input": "user@example", "output": "invalid"},  # Missing TLD
]
```

### 3. Representative of Target Distribution

```python
# If 70% of real data is Type A, 20% Type B, 10% Type C:
examples = [
    # 3-4 Type A examples (70%)
    {"input": "...", "output": "type_a"},
    {"input": "...", "output": "type_a"},
    {"input": "...", "output": "type_a"},

    # 1 Type B example (20%)
    {"input": "...", "output": "type_b"},

    # 1 Type C example (10%)
    {"input": "...", "output": "type_c"},
]
```

## Best Practices

### 1. Consistent Formatting

```python
# BAD: Inconsistent format
examples = """
Example 1: Input is "text" -> Output: result
For example 2, when input="other", we get: different result
"""

# GOOD: Consistent structure
examples = """
Input: "text"
Output: result

Input: "other"
Output: different result
"""
```

### 2. Clear Separators

```python
prompt = """
Classify sentiment:

---
Example 1:
Text: "I love this product!"
Sentiment: positive
---

---
Example 2:
Text: "Waste of money."
Sentiment: negative
---

---
Your turn:
Text: "{new_text}"
Sentiment:
"""
```

### 3. Randomize Example Order

```python
import random

def create_few_shot_prompt(task, examples, new_input):
    # Shuffle to avoid position bias
    shuffled = random.sample(examples, len(examples))

    example_text = "\n\n".join([
        f"Input: {ex['input']}\nOutput: {ex['output']}"
        for ex in shuffled
    ])

    return f"""
{task}

Examples:
{example_text}

Now complete:
Input: {new_input}
Output:
"""
```

## Implementation Examples

### Python + OpenAI: Sentiment Classification

```python
from openai import OpenAI

client = OpenAI()

examples = [
    {"text": "Absolutely fantastic! Best purchase ever.", "sentiment": "positive"},
    {"text": "Complete waste of money. Terrible quality.", "sentiment": "negative"},
    {"text": "It's okay. Does what it says.", "sentiment": "neutral"},
    {"text": "Great features but too expensive.", "sentiment": "mixed"},
]

def few_shot_classify(text: str) -> str:
    example_text = "\n\n".join([
        f'Review: "{ex["text"]}"\nSentiment: {ex["sentiment"]}'
        for ex in examples
    ])

    prompt = f"""
Classify customer review sentiment as: positive, negative, neutral, or mixed.

Examples:
{example_text}

Review: "{text}"
Sentiment:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10
    )

    return response.choices[0].message.content.strip().lower()
```

### Python + Anthropic: Entity Extraction

```python
import anthropic
import json

client = anthropic.Anthropic()

examples = [
    {
        "text": "John Smith visited Paris last summer with Jane Doe.",
        "entities": {"people": ["John Smith", "Jane Doe"], "locations": ["Paris"]}
    },
    {
        "text": "The meeting in Tokyo was attended by Sarah Chen.",
        "entities": {"people": ["Sarah Chen"], "locations": ["Tokyo"]}
    },
]

def few_shot_extract(text: str) -> dict:
    example_text = "\n\n".join([
        f'Text: "{ex["text"]}"\nEntities: {json.dumps(ex["entities"])}'
        for ex in examples
    ])

    prompt = f"""
Extract person names and locations from text.

Examples:
{example_text}

Text: "{text}"
Entities:
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(message.content[0].text)
```

### TypeScript + Vercel AI SDK: Format Conversion

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const examples = [
  {
    input: 'Meeting on Jan 15 at 2pm',
    output: '{"date": "2025-01-15", "time": "14:00"}',
  },
  {
    input: 'Deadline: March 3rd 9am',
    output: '{"date": "2025-03-03", "time": "09:00"}',
  },
];

async function fewShotParse(text: string): Promise<object> {
  const exampleText = examples
    .map((ex) => `Input: ${ex.input}\nOutput: ${ex.output}`)
    .join('\n\n');

  const prompt = `
Convert natural language dates to JSON format.

Examples:
${exampleText}

Input: ${text}
Output:
  `;

  const { text: result } = await generateText({
    model: openai('gpt-4'),
    prompt,
    temperature: 0,
  });

  return JSON.parse(result);
}
```

## Common Pitfalls

### 1. Too Many Examples

```python
# BAD: 15 examples (expensive, diminishing returns)
# Each example costs tokens on every request

# GOOD: 3-5 carefully selected examples
# Sweet spot: quality over quantity
```

**Research finding:** Performance plateaus after 5-7 examples for most tasks.

### 2. Biased Example Selection

```python
# BAD: All examples from one category
examples = [
    {"text": "Great!", "label": "positive"},
    {"text": "Love it!", "label": "positive"},
    {"text": "Amazing!", "label": "positive"},
]

# GOOD: Balanced representation
examples = [
    {"text": "Great!", "label": "positive"},
    {"text": "Terrible", "label": "negative"},
    {"text": "Okay", "label": "neutral"},
]
```

### 3. Ambiguous Examples

```python
# BAD: Unclear what makes this output correct
Input: "Process this data"
Output: "Done"

# GOOD: Clear relationship between input and output
Input: "Extract email from: Contact us at support@example.com"
Output: "support@example.com"
```

### 4. Inconsistent Labeling

```python
# BAD: Same input, different outputs
Example 1:
Input: "It's okay"
Output: "neutral"

Example 2:
Input: "It's alright"
Output: "positive"  # Inconsistent!

# GOOD: Consistent labeling for similar inputs
```

## Dynamic Few-Shot Selection

### Retrieve Similar Examples

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_relevant_examples(new_input: str, example_pool: list, n: int = 3) -> list:
    """Select most relevant examples using embeddings."""

    # Get embeddings (pseudo-code)
    new_embedding = get_embedding(new_input)
    example_embeddings = [get_embedding(ex["input"]) for ex in example_pool]

    # Compute similarity
    similarities = cosine_similarity([new_embedding], example_embeddings)[0]

    # Get top N
    top_indices = np.argsort(similarities)[-n:][::-1]
    return [example_pool[i] for i in top_indices]

# Usage
relevant = get_relevant_examples("new input text", large_example_pool, n=3)
prompt = create_few_shot_prompt(task, relevant, new_input)
```

## Combining Few-Shot with Other Techniques

### Few-Shot + Chain-of-Thought

```python
examples = [
    {
        "question": "If 2x + 3 = 11, what is x?",
        "reasoning": "Subtract 3: 2x = 8\nDivide by 2: x = 4",
        "answer": "4"
    },
    {
        "question": "If 5y - 7 = 18, what is y?",
        "reasoning": "Add 7: 5y = 25\nDivide by 5: y = 5",
        "answer": "5"
    },
]

prompt = f"""
Solve algebra problems showing your work:

{format_examples_with_reasoning(examples)}

Question: {new_question}
Reasoning:
"""
```

### Few-Shot + Structured Output

```python
examples = [
    {
        "text": "John, 28, engineer",
        "json": '{"name": "John", "age": 28, "occupation": "engineer"}'
    },
]

prompt = f"""
Extract structured data as JSON.

{format_examples(examples)}

Text: {new_text}
JSON:
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
)
```

## Testing Few-Shot Prompts

```python
import pytest

def test_few_shot_classification():
    """Test few-shot vs zero-shot performance."""

    test_cases = [
        {"input": "Exceeded expectations!", "expected": "positive"},
        {"input": "Disappointed", "expected": "negative"},
        {"input": "Average product", "expected": "neutral"},
    ]

    for case in test_cases:
        result = few_shot_classify(case["input"])
        assert result == case["expected"], f"Failed on: {case['input']}"
```

## When to Upgrade from Few-Shot

Consider other approaches when:

1. **Task too complex for examples** → Use fine-tuning
2. **Need 100+ examples** → Fine-tuning more cost-effective
3. **Examples don't improve quality** → Try Chain-of-Thought or different technique
4. **High token costs** → Cache examples or use fine-tuning

## Summary

Few-shot learning bridges the gap between zero-shot and fine-tuning: provide just enough examples to guide model behavior without expensive training.

**Key takeaways:**
- 2-5 diverse, high-quality examples beat 10+ similar examples
- Include edge cases and maintain consistent formatting
- Randomize example order to avoid position bias
- Test on representative data to validate effectiveness
- Combine with CoT for complex reasoning tasks

**Sweet spot:** 3-5 examples for most classification and extraction tasks.
