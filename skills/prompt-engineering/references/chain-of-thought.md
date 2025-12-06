# Chain-of-Thought (CoT) Prompting

Chain-of-Thought prompting improves LLM reasoning by eliciting intermediate steps before final answers.

## Table of Contents

- [Research Foundation](#research-foundation)
- [When to Use CoT](#when-to-use-cot)
- [Zero-Shot CoT](#zero-shot-cot)
- [Few-Shot CoT](#few-shot-cot)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)
- [Implementation Examples](#implementation-examples)

## Research Foundation

**Wei et al. (2022): "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"**
- ArXiv: https://arxiv.org/abs/2201.11903
- Key finding: 20-50% accuracy improvement on reasoning benchmarks
- Works better with larger models (>100B parameters)
- Shows emergent ability in models like GPT-3, PaLM, LaMDA

**Key insight:** Prompting models to show reasoning steps significantly improves performance on:
- Arithmetic reasoning
- Commonsense reasoning
- Symbolic reasoning
- Multi-hop question answering

## When to Use CoT

**Ideal for:**
- Math problems and calculations
- Logic puzzles
- Multi-step reasoning tasks
- Complex analysis requiring intermediate steps
- Tasks where "showing work" improves accuracy
- Debugging complex code or systems

**Not necessary for:**
- Simple factual recall
- Single-step tasks
- Classification (unless reasoning needed)
- Tasks where model already performs well zero-shot

## Zero-Shot CoT

### Pattern

```
{Task description}
"Let's think step by step."
{Input}
```

### Basic Example

```python
from openai import OpenAI

client = OpenAI()

prompt = """
Solve this problem step by step:

A train leaves Station A at 2:00 PM traveling at 60 mph.
Another train leaves Station B at 3:00 PM traveling at 80 mph.
The stations are 300 miles apart. When do they meet?

Let's think step by step:
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

print(response.choices[0].message.content)
```

### Expected Output

```
Let's think step by step:

1. Calculate distance first train travels before second starts:
   - Time difference: 1 hour (3 PM - 2 PM)
   - Distance: 60 mph × 1 hour = 60 miles

2. Remaining distance between trains when both moving:
   - 300 miles - 60 miles = 240 miles

3. Combined closing speed:
   - 60 mph + 80 mph = 140 mph

4. Time to close remaining distance:
   - 240 miles ÷ 140 mph = 1.71 hours (≈ 1 hour 43 minutes)

5. Meeting time:
   - Second train starts at 3:00 PM
   - 3:00 PM + 1:43 = 4:43 PM

Answer: The trains meet at approximately 4:43 PM.
```

### Variations

**"Let's think step by step."** (Most common)
**"Let's break this down:"**
**"Let's solve this systematically:"**
**"Let's reason through this carefully:"**

All variations work - choose based on task context.

## Few-Shot CoT

### Pattern

```
{Task description}

{Example 1 with reasoning steps}
{Example 2 with reasoning steps}
{Example 3 with reasoning steps (optional)}

{Actual task}
```

### Example: Math Word Problems

```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Solve these word problems showing your reasoning:

Example 1:
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?

A: Let's think step by step:
- Roger started with 5 balls
- He bought 2 cans with 3 balls each
- 2 cans × 3 balls = 6 balls
- Total: 5 + 6 = 11 balls

Answer: 11 tennis balls

Example 2:
Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?

A: Let's think step by step:
- Started with 23 apples
- Used 20 for lunch: 23 - 20 = 3 apples left
- Bought 6 more: 3 + 6 = 9 apples
Answer: 9 apples

Now solve:
Q: A store had 27 bottles of water. They sold 18 bottles and then received a shipment of 35 more. How many bottles do they have now?

A: Let's think step by step:
"""

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)
```

## Advanced Patterns

### 1. Self-Consistency CoT

Generate multiple reasoning paths and pick the most consistent answer.

```python
from collections import Counter

def self_consistency_cot(prompt: str, n_samples: int = 5) -> str:
    """Generate multiple CoT responses and pick most common answer."""

    responses = []
    for _ in range(n_samples):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # Higher temp for diversity
        )
        responses.append(extract_answer(response.choices[0].message.content))

    # Return most common answer
    answer_counts = Counter(responses)
    return answer_counts.most_common(1)[0][0]
```

### 2. Tree-of-Thoughts (ToT)

Explore multiple reasoning branches and select the best path.

```python
prompt = """
Consider three different approaches to solve this problem:

Problem: {problem_description}

Approach 1: [Method A]
- Step 1: ...
- Step 2: ...
- Conclusion: ...

Approach 2: [Method B]
- Step 1: ...
- Step 2: ...
- Conclusion: ...

Approach 3: [Method C]
- Step 1: ...
- Step 2: ...
- Conclusion: ...

Evaluate which approach is most sound and proceed with it to get the final answer.
"""
```

### 3. Structured CoT with XML Tags (Claude)

```python
system_prompt = """
When solving problems, use the following structure:

<thinking>
Break down the problem step by step here.
</thinking>

<answer>
Provide the final answer here.
</answer>
"""

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=system_prompt,
    messages=[{"role": "user", "content": "What is 15% of 240?"}]
)

# Extract answer from XML tags
import re
answer = re.search(r'<answer>(.*?)</answer>', message.content[0].text, re.DOTALL)
```

### 4. Progressive CoT Refinement

```python
# Step 1: Initial reasoning
initial = generate_cot_response(problem)

# Step 2: Review and refine
refinement_prompt = f"""
Review this solution and identify any errors or improvements:

{initial}

If there are errors, provide a corrected step-by-step solution.
If correct, confirm and explain why.
"""

refined = generate_cot_response(refinement_prompt)
```

## Best Practices

### 1. Explicit Step Markers

**GOOD:**
```
Step 1: Identify given information
Step 2: Determine what to calculate
Step 3: Apply formula
Step 4: Solve
```

**BETTER:**
```python
prompt = """
Solve systematically:

1. List known values
2. Identify unknowns
3. Choose relevant formulas
4. Solve step-by-step
5. Verify answer makes sense

Problem: {problem}
"""
```

### 2. Request Work to be Shown

```python
# For math
"Show your work for each calculation."

# For code
"Explain your reasoning for each design decision."

# For analysis
"Justify each conclusion with evidence from the text."
```

### 3. Use Clear Delimiters

```python
prompt = """
Problem:
---
{problem}
---

Solution (show reasoning):
"""
```

### 4. Combine with Few-Shot for Complex Domains

```python
prompt = f"""
Here are examples of good step-by-step reasoning:

{example_1_with_reasoning}

{example_2_with_reasoning}

Now apply the same reasoning process:

{new_problem}

Let's think step by step:
"""
```

## Implementation Examples

### Python + OpenAI

```python
from openai import OpenAI
import re

client = OpenAI()

def cot_solver(problem: str) -> dict:
    """Solve problem with chain-of-thought reasoning."""

    prompt = f"""
Solve this problem step by step. Show your reasoning before providing the final answer.

Problem: {problem}

Solution:
Let's think step by step:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    full_response = response.choices[0].message.content

    # Extract final answer (if present)
    answer_match = re.search(r'(?:Answer|Final answer):\s*(.+)', full_response, re.IGNORECASE)

    return {
        "reasoning": full_response,
        "answer": answer_match.group(1) if answer_match else None,
        "tokens": response.usage.total_tokens
    }

# Usage
result = cot_solver("If a car travels 240 miles in 4 hours, what is its average speed in mph?")
print(f"Reasoning:\n{result['reasoning']}\n")
print(f"Answer: {result['answer']}")
```

### Python + Anthropic (with XML)

```python
import anthropic
import re

client = anthropic.Anthropic()

def claude_cot_solver(problem: str) -> dict:
    """Solve with structured CoT using Claude."""

    system_prompt = """
Solve problems using this structure:

<thinking>
Work through the problem step-by-step here.
Show all calculations and reasoning.
</thinking>

<answer>
State the final answer clearly.
</answer>
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": f"Problem: {problem}"}],
        temperature=0
    )

    content = message.content[0].text

    # Extract sections
    thinking = re.search(r'<thinking>(.*?)</thinking>', content, re.DOTALL)
    answer = re.search(r'<answer>(.*?)</answer>', content, re.DOTALL)

    return {
        "thinking": thinking.group(1).strip() if thinking else None,
        "answer": answer.group(1).strip() if answer else None,
        "tokens": message.usage.input_tokens + message.usage.output_tokens
    }
```

### TypeScript + Vercel AI SDK

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

async function cotSolver(problem: string): Promise<{ reasoning: string; answer: string | null }> {
  const prompt = `
Solve this problem step by step:

Problem: ${problem}

Solution:
Let's think step by step:
  `;

  const { text } = await generateText({
    model: openai('gpt-4'),
    prompt,
    temperature: 0,
  });

  // Extract answer
  const answerMatch = text.match(/(?:Answer|Final answer):\s*(.+)/i);

  return {
    reasoning: text,
    answer: answerMatch ? answerMatch[1] : null,
  };
}

// Usage
const result = await cotSolver(
  'A rectangle has length 12cm and width 8cm. What is its area?'
);
console.log(result.reasoning);
```

## When CoT Fails

### 1. Model Hallucinates Steps

**Problem:** Model invents facts or calculations.

**Solution:**
- Use few-shot with accurate examples
- Add "Only use information provided in the problem"
- Validate intermediate steps programmatically

### 2. Overly Verbose Reasoning

**Problem:** Unnecessary verbosity increases token costs.

**Solution:**
- Specify "Be concise in reasoning"
- Request specific number of steps
- Use structured output format

### 3. Incorrect Final Answer Despite Good Reasoning

**Problem:** Logic is sound but calculation error.

**Solution:**
- Use code execution for math (tools/function calling)
- Self-consistency (multiple samples)
- Verification prompt after initial solution

## Combining CoT with Other Techniques

### CoT + Few-Shot

```python
prompt = """
Solve geometry problems step by step:

Example:
Q: Circle has radius 5cm. Find circumference.
A: Step 1: Formula is C = 2πr
   Step 2: Substitute r = 5
   Step 3: C = 2 × π × 5 = 10π ≈ 31.4 cm

Now solve:
Q: {new_geometry_problem}
A: Step 1:
"""
```

### CoT + Structured Output

```python
from pydantic import BaseModel

class CoTSolution(BaseModel):
    steps: list[str]
    final_answer: str
    confidence: float

prompt = """
Solve and return as JSON:
{
  "steps": ["Step 1: ...", "Step 2: ..."],
  "final_answer": "...",
  "confidence": 0.95
}

Problem: {problem}
"""
```

### CoT + RAG (Knowledge-Grounded Reasoning)

```python
# Retrieve relevant documents
docs = retriever.get_relevant_documents(query)

prompt = f"""
Use the following information to reason through the question:

Context:
{docs}

Question: {question}

Reasoning (cite specific information from context):
"""
```

## Measuring CoT Effectiveness

```python
import pytest

def test_cot_accuracy():
    """Test CoT vs zero-shot on reasoning tasks."""

    test_cases = [
        {
            "problem": "If 3x + 5 = 20, what is x?",
            "expected": "5"
        },
        # ... more test cases
    ]

    cot_correct = 0
    zero_shot_correct = 0

    for case in test_cases:
        # Zero-shot
        zs_answer = zero_shot_solve(case["problem"])
        if zs_answer == case["expected"]:
            zero_shot_correct += 1

        # CoT
        cot_answer = cot_solver(case["problem"])["answer"]
        if cot_answer == case["expected"]:
            cot_correct += 1

    print(f"Zero-shot accuracy: {zero_shot_correct / len(test_cases)}")
    print(f"CoT accuracy: {cot_correct / len(test_cases)}")
```

## Summary

Chain-of-Thought prompting is essential for complex reasoning tasks. The key insight is simple: asking the model to show its work significantly improves accuracy.

**Key takeaways:**
- Use "Let's think step by step" for zero-shot CoT
- Provide reasoning examples for few-shot CoT
- Combine with self-consistency for higher accuracy
- Use structured formats (XML tags) to extract reasoning
- Validate intermediate steps when possible
- Works best with larger models (GPT-4, Claude Opus/Sonnet)

**When to use:**
- Math and arithmetic problems
- Logic puzzles
- Multi-hop question answering
- Complex analysis requiring intermediate steps

**When not to use:**
- Simple factual recall
- Classification tasks (unless reasoning needed)
- Time/cost-sensitive simple tasks
