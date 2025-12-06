# Prompt Chaining Patterns

Comprehensive guide to composing multiple LLM calls into robust, multi-step workflows.

## Table of Contents

1. [Overview](#overview)
2. [Sequential Chains](#sequential-chains)
3. [Parallel Chains](#parallel-chains)
4. [Conditional Chains](#conditional-chains)
5. [Self-Correction Chains](#self-correction-chains)
6. [Verification Chains](#verification-chains)
7. [Tool-Use Chains](#tool-use-chains)
8. [Framework Implementations](#framework-implementations)
9. [Best Practices](#best-practices)

## Overview

**What is Prompt Chaining?**
Prompt chaining breaks complex tasks into sequential or parallel LLM calls, where outputs from one prompt become inputs to another. This creates more reliable, debuggable, and modular AI workflows.

**Benefits:**
- **Modularity:** Test and optimize each step independently
- **Reliability:** Simpler prompts are more reliable than complex ones
- **Debuggability:** Inspect intermediate outputs
- **Cost optimization:** Cache common prefixes, skip unnecessary steps
- **Specialization:** Use different models for different tasks

**When to use chaining:**
- Task requires multiple distinct steps (research → outline → write)
- Need intermediate validation or human review
- Different steps require different models or parameters
- Task is too complex for a single prompt

## Sequential Chains

### Pattern 1: Linear Pipeline

**Structure:** Step 1 → Step 2 → Step 3 → Output

**Example: Article Generation**
```python
from openai import OpenAI

client = OpenAI()

def generate_article(topic: str) -> str:
    # Step 1: Research and extract key points
    research_prompt = f"""
    Research the topic: {topic}

    List 5 key points that should be covered in an article.
    Format as a numbered list.
    """
    research = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": research_prompt}],
        temperature=0.7
    ).choices[0].message.content

    # Step 2: Create outline
    outline_prompt = f"""
    Create an article outline for: {topic}

    Key points to cover:
    {research}

    Provide a structured outline with sections and subsections.
    """
    outline = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": outline_prompt}],
        temperature=0.5
    ).choices[0].message.content

    # Step 3: Write full article
    writing_prompt = f"""
    Write a comprehensive article following this outline:

    {outline}

    Topic: {topic}

    Write in an engaging, informative style. Include examples.
    """
    article = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": writing_prompt}],
        temperature=0.8,
        max_tokens=2000
    ).choices[0].message.content

    return article
```

**Diagram:**
```
Topic → [Research] → Key Points → [Outline] → Structure → [Write] → Article
```

### Pattern 2: Accumulative Chain

**Structure:** Each step adds to previous outputs.

**Example: Iterative Story Building**
```python
def build_story_iteratively(theme: str, num_chapters: int = 3) -> str:
    story = ""
    previous_summary = f"Theme: {theme}"

    for chapter_num in range(1, num_chapters + 1):
        chapter_prompt = f"""
        Previous story summary:
        {previous_summary}

        Write Chapter {chapter_num} that:
        1. Continues from the previous narrative
        2. Introduces new developments
        3. Ends with a compelling hook

        Chapter {chapter_num}:
        """

        chapter = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": chapter_prompt}],
            temperature=0.8
        ).choices[0].message.content

        story += f"\n\n## Chapter {chapter_num}\n\n{chapter}"

        # Update summary for next iteration
        summary_prompt = f"""
        Summarize the story so far in 2-3 sentences:

        {story}

        Summary:
        """
        previous_summary = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0,
            max_tokens=150
        ).choices[0].message.content

    return story
```

### Pattern 3: Transform Chain

**Structure:** Apply successive transformations.

**Example: Text Refinement Pipeline**
```python
def refine_text(raw_text: str) -> str:
    # Step 1: Fix grammar and spelling
    grammar_prompt = f"Fix grammar and spelling:\n\n{raw_text}"
    corrected = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": grammar_prompt}],
        temperature=0
    ).choices[0].message.content

    # Step 2: Improve clarity
    clarity_prompt = f"Improve clarity and readability:\n\n{corrected}"
    clarified = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": clarity_prompt}],
        temperature=0.3
    ).choices[0].message.content

    # Step 3: Make concise
    concise_prompt = f"Make this more concise without losing meaning:\n\n{clarified}"
    final = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": concise_prompt}],
        temperature=0.2
    ).choices[0].message.content

    return final
```

**Diagram:**
```
Raw → [Grammar Fix] → Corrected → [Clarity] → Clear → [Concise] → Final
```

## Parallel Chains

### Pattern 1: Fan-Out, Fan-In

**Structure:** Split task, process in parallel, merge results.

**Example: Multi-Perspective Analysis**
```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def analyze_from_perspective(text: str, perspective: str) -> str:
    """Analyze text from a specific perspective."""
    prompt = f"""
    Analyze the following text from the perspective of a {perspective}.

    Text:
    {text}

    Analysis:
    """

    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

async def multi_perspective_analysis(text: str) -> str:
    """Analyze text from multiple perspectives in parallel."""

    # Fan-out: Create parallel tasks
    perspectives = ["economist", "sociologist", "ethicist", "technologist"]

    analyses = await asyncio.gather(*[
        analyze_from_perspective(text, p) for p in perspectives
    ])

    # Fan-in: Synthesize results
    synthesis_prompt = f"""
    Synthesize these different perspectives into a comprehensive analysis:

    Economist's view:
    {analyses[0]}

    Sociologist's view:
    {analyses[1]}

    Ethicist's view:
    {analyses[2]}

    Technologist's view:
    {analyses[3]}

    Comprehensive synthesis:
    """

    synthesis = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{"role": "user", "content": synthesis_prompt}]
    )

    return synthesis.content[0].text
```

**Diagram:**
```
                  → [Economist] →
                 /                \
Text → Split → [Sociologist] →    Merge → Synthesis
                \                /
                  → [Ethicist] →
                  → [Tech] →
```

### Pattern 2: Parallel Validation

**Structure:** Multiple validators check different aspects.

**Example: Code Review Chain**
```python
async def parallel_code_review(code: str) -> dict:
    """Review code across multiple dimensions in parallel."""

    # Define review tasks
    async def check_security(code: str) -> str:
        prompt = f"Identify security vulnerabilities:\n\n{code}"
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    async def check_performance(code: str) -> str:
        prompt = f"Identify performance issues:\n\n{code}"
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    async def check_style(code: str) -> str:
        prompt = f"Check code style and best practices:\n\n{code}"
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    # Execute in parallel
    security, performance, style = await asyncio.gather(
        check_security(code),
        check_performance(code),
        check_style(code)
    )

    return {
        "security": security,
        "performance": performance,
        "style": style
    }
```

## Conditional Chains

### Pattern 1: Router Chain

**Structure:** Route to different chains based on classification.

**Example: Customer Support Router**
```python
def handle_customer_query(query: str) -> str:
    # Step 1: Classify query type
    classification_prompt = f"""
    Classify this customer query into ONE category:
    - technical_issue
    - billing_question
    - feature_request
    - general_inquiry

    Query: {query}

    Category (one word):
    """

    category = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": classification_prompt}],
        temperature=0,
        max_tokens=10
    ).choices[0].message.content.strip()

    # Step 2: Route to appropriate handler
    if category == "technical_issue":
        return handle_technical_issue(query)
    elif category == "billing_question":
        return handle_billing(query)
    elif category == "feature_request":
        return handle_feature_request(query)
    else:
        return handle_general_inquiry(query)

def handle_technical_issue(query: str) -> str:
    """Specialized technical support chain."""
    # Step 1: Gather diagnostic info
    diagnostic_prompt = f"""
    What information do we need to diagnose this issue?
    Query: {query}

    List required diagnostic questions:
    """
    diagnostics = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": diagnostic_prompt}],
        temperature=0
    ).choices[0].message.content

    # Step 2: Generate response
    response_prompt = f"""
    Respond to this technical issue:
    {query}

    Request these diagnostics:
    {diagnostics}
    """
    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": response_prompt}],
        temperature=0.3
    ).choices[0].message.content
```

**Diagram:**
```
Query → [Classify] → technical_issue → [Tech Handler] → Response
                  → billing_question → [Billing Handler] → Response
                  → feature_request → [Feature Handler] → Response
                  → general_inquiry → [General Handler] → Response
```

### Pattern 2: Conditional Expansion

**Structure:** Expand chain based on intermediate results.

**Example: Adaptive Research Chain**
```python
def adaptive_research(question: str) -> str:
    # Step 1: Initial answer attempt
    initial_prompt = f"Answer this question concisely: {question}"
    initial_answer = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": initial_prompt}],
        temperature=0.5
    ).choices[0].message.content

    # Step 2: Assess confidence
    confidence_prompt = f"""
    Rate your confidence in this answer (1-10):
    Question: {question}
    Answer: {initial_answer}

    Confidence (number only):
    """
    confidence = int(client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": confidence_prompt}],
        temperature=0,
        max_tokens=5
    ).choices[0].message.content.strip())

    # Step 3: If low confidence, do more research
    if confidence < 7:
        research_prompt = f"""
        The question requires more research: {question}

        Current answer (low confidence): {initial_answer}

        Conduct deeper research and provide a more comprehensive answer.
        """
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": research_prompt}],
            temperature=0.7,
            max_tokens=2000
        ).choices[0].message.content
    else:
        return initial_answer
```

## Self-Correction Chains

### Pattern 1: Generate-Critique-Refine

**Structure:** Generate → Self-critique → Revise based on critique.

**Example: Essay Writing with Self-Critique**
```python
def write_with_self_correction(topic: str) -> str:
    # Step 1: Generate initial draft
    draft_prompt = f"Write a 3-paragraph essay on: {topic}"
    draft = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": draft_prompt}],
        temperature=0.8
    ).choices[0].message.content

    # Step 2: Self-critique
    critique_prompt = f"""
    Critique this essay and identify specific improvements:

    {draft}

    Provide 3-5 specific critiques with examples:
    """
    critique = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": critique_prompt}],
        temperature=0.3
    ).choices[0].message.content

    # Step 3: Revise based on critique
    revision_prompt = f"""
    Revise this essay based on the critique:

    Original Essay:
    {draft}

    Critique:
    {critique}

    Revised Essay:
    """
    revised = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": revision_prompt}],
        temperature=0.7
    ).choices[0].message.content

    return revised
```

### Pattern 2: Iterative Refinement

**Structure:** Refine until quality threshold met.

**Example: Code Generation with Refinement**
```python
def generate_code_with_refinement(requirements: str, max_iterations: int = 3) -> str:
    code = ""

    for iteration in range(max_iterations):
        if iteration == 0:
            # Initial generation
            prompt = f"Write Python code for: {requirements}"
        else:
            # Refinement
            prompt = f"""
            Improve this code:
            {code}

            Issues found:
            {issues}

            Provide improved code:
            """

        code = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        ).choices[0].message.content

        # Check for issues
        check_prompt = f"""
        Review this code and list any issues:
        {code}

        Issues (or "NONE" if code is good):
        """
        issues = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": check_prompt}],
            temperature=0
        ).choices[0].message.content

        if "NONE" in issues or "no issues" in issues.lower():
            break

    return code
```

## Verification Chains

### Pattern 1: Fact-Checking Chain

**Structure:** Generate → Extract claims → Verify → Revise.

**Example: Verified Article Generation**
```python
def generate_verified_article(topic: str, sources: list[str]) -> str:
    # Step 1: Generate article
    article_prompt = f"Write an article about: {topic}"
    article = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": article_prompt}],
        temperature=0.7
    ).choices[0].message.content

    # Step 2: Extract factual claims
    claims_prompt = f"""
    Extract all factual claims from this article:

    {article}

    List each claim on a separate line:
    """
    claims = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": claims_prompt}],
        temperature=0
    ).choices[0].message.content

    # Step 3: Verify against sources
    verification_prompt = f"""
    Verify these claims against the provided sources:

    Claims:
    {claims}

    Sources:
    {chr(10).join(sources)}

    For each claim, state: VERIFIED, UNVERIFIED, or CONTRADICTED
    """
    verification = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": verification_prompt}],
        temperature=0
    ).choices[0].message.content

    # Step 4: Revise article if needed
    if "CONTRADICTED" in verification or "UNVERIFIED" in verification:
        revision_prompt = f"""
        Revise this article to fix unverified or contradicted claims:

        Original Article:
        {article}

        Verification Results:
        {verification}

        Revised Article (only include verified information):
        """
        article = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": revision_prompt}],
            temperature=0.6
        ).choices[0].message.content

    return article
```

### Pattern 2: Consistency Checking

**Structure:** Generate multiple outputs → Check consistency → Merge or flag.

**Example: Consensus-Based Answer**
```python
async def consensus_answer(question: str, num_attempts: int = 3) -> str:
    """Generate multiple answers and check for consistency."""

    # Generate multiple answers
    tasks = [
        client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )
        for _ in range(num_attempts)
    ]

    responses = await asyncio.gather(*tasks)
    answers = [r.choices[0].message.content for r in responses]

    # Check consistency
    consistency_prompt = f"""
    Compare these answers to the question: "{question}"

    Answer 1: {answers[0]}
    Answer 2: {answers[1]}
    Answer 3: {answers[2]}

    Are they consistent? If not, what are the differences?
    Provide a single, consensus answer that reconciles any differences.

    Consensus Answer:
    """

    consensus = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": consistency_prompt}],
        temperature=0
    ).choices[0].message.content

    return consensus
```

## Tool-Use Chains

### Pattern 1: ReAct (Reasoning + Acting)

**Structure:** Thought → Action → Observation → (repeat) → Answer

**Example: Web Search ReAct Chain**
```python
def react_search(question: str, max_steps: int = 5) -> str:
    """ReAct pattern for web search tasks."""

    conversation = []
    observation = ""

    for step in range(max_steps):
        # Reasoning step
        reasoning_prompt = f"""
Question: {question}

Previous Observations:
{observation}

Think step-by-step:
1. What do I know so far?
2. What information do I still need?
3. What action should I take next?

Thought:
"""
        thought = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": reasoning_prompt}],
            temperature=0.5
        ).choices[0].message.content

        # Decide action
        action_prompt = f"""
Based on this thought: {thought}

Choose an action:
- SEARCH: [search query]
- FINISH: [final answer]

Action:
"""
        action = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": action_prompt}],
            temperature=0
        ).choices[0].message.content

        if action.startswith("FINISH"):
            return action.replace("FINISH:", "").strip()

        # Execute action (mock search)
        if action.startswith("SEARCH"):
            query = action.replace("SEARCH:", "").strip()
            observation += f"\nSearch results for '{query}': [mock results]"

    return "Max steps reached without conclusion"
```

### Pattern 2: Multi-Tool Workflow

**Structure:** Plan → Execute tools → Synthesize → Answer

**Example: Data Analysis Chain**
```python
def data_analysis_chain(dataset_path: str, question: str) -> str:
    # Step 1: Plan analysis
    plan_prompt = f"""
    Question: {question}
    Dataset: {dataset_path}

    What tools/functions do you need?
    - load_data
    - calculate_statistics
    - create_visualization
    - correlation_analysis

    Create a step-by-step plan:
    """
    plan = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": plan_prompt}],
        temperature=0
    ).choices[0].message.content

    # Step 2: Execute plan (simplified)
    results = {
        "data_summary": "Loaded 1000 rows, 10 columns",
        "statistics": "Mean: 45.2, Median: 42.1, Std: 12.3",
        "correlation": "Strong positive correlation (r=0.85)"
    }

    # Step 3: Synthesize results
    synthesis_prompt = f"""
    Original Question: {question}

    Analysis Plan:
    {plan}

    Results:
    {results}

    Provide a comprehensive answer to the question based on the analysis results.

    Answer:
    """
    answer = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": synthesis_prompt}],
        temperature=0.3
    ).choices[0].message.content

    return answer
```

## Framework Implementations

### LangChain LCEL (LangChain Expression Language)

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Define prompts
translate_prompt = ChatPromptTemplate.from_template(
    "Translate to {language}: {text}"
)

summarize_prompt = ChatPromptTemplate.from_template(
    "Summarize in 1 sentence: {text}"
)

# Create chain
llm = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()

chain = (
    translate_prompt
    | llm
    | parser
    | (lambda x: {"text": x})  # Transform for next step
    | summarize_prompt
    | llm
    | parser
)

# Execute
result = chain.invoke({"language": "French", "text": "Hello world"})
```

### LangChain Sequential Chain

```python
from langchain.chains import SequentialChain, LLMChain
from langchain_openai import OpenAI

llm = OpenAI(model="gpt-4")

# Chain 1: Generate synopsis
synopsis_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template("Write a synopsis for: {title}"),
    output_key="synopsis"
)

# Chain 2: Generate review
review_chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template("Review this synopsis: {synopsis}"),
    output_key="review"
)

# Combine
overall_chain = SequentialChain(
    chains=[synopsis_chain, review_chain],
    input_variables=["title"],
    output_variables=["synopsis", "review"],
    verbose=True
)

result = overall_chain({"title": "AI Revolution"})
```

### Vercel AI SDK Chaining

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

async function chainedGeneration(topic: string) {
  // Step 1: Research
  const { text: research } = await generateText({
    model: openai('gpt-4'),
    prompt: `Research key points about: ${topic}`,
  });

  // Step 2: Outline
  const { text: outline } = await generateText({
    model: openai('gpt-4'),
    prompt: `Create an outline based on: ${research}`,
  });

  // Step 3: Write
  const { text: article } = await generateText({
    model: openai('gpt-4'),
    prompt: `Write an article following: ${outline}`,
  });

  return article;
}
```

## Best Practices

### 1. Error Handling in Chains

```python
def robust_chain(input_data: str) -> str:
    try:
        # Step 1
        result1 = step1(input_data)
    except Exception as e:
        logging.error(f"Step 1 failed: {e}")
        result1 = fallback_step1(input_data)

    try:
        # Step 2
        result2 = step2(result1)
    except Exception as e:
        logging.error(f"Step 2 failed: {e}")
        # Decide: retry, skip, or fail
        return result1  # Return partial result

    return result2
```

### 2. Logging Intermediate Steps

```python
import logging

def logged_chain(input_data: str) -> str:
    logging.info(f"Chain started with input: {input_data[:100]}")

    step1_result = step1(input_data)
    logging.info(f"Step 1 complete. Output length: {len(step1_result)}")

    step2_result = step2(step1_result)
    logging.info(f"Step 2 complete. Output length: {len(step2_result)}")

    return step2_result
```

### 3. Cost Optimization

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_step(input_hash: str, input_data: str) -> str:
    """Cache expensive LLM calls."""
    return expensive_llm_call(input_data)

def optimized_chain(data: str) -> str:
    # Use hash for caching
    data_hash = hashlib.md5(data.encode()).hexdigest()
    return cached_step(data_hash, data)
```

### 4. Parallel Execution When Possible

```python
import asyncio

async def optimized_multi_step(data: str) -> dict:
    # If steps are independent, run in parallel
    results = await asyncio.gather(
        independent_step_a(data),
        independent_step_b(data),
        independent_step_c(data)
    )

    # Then do sequential step that depends on all
    final = synthesis_step(results)
    return final
```

---

**Related Files:**
- `rag-patterns.md` - RAG-specific chain patterns
- `tool-use-guide.md` - Tool-calling in chains
- `examples/langchain-examples.py` - LangChain chain implementations

**Key Takeaways:**
1. Break complex tasks into simple, focused steps
2. Log intermediate outputs for debugging
3. Use parallel execution when steps are independent
4. Implement error handling and fallbacks
5. Cache repeated computations
6. Choose the right chain type (sequential, parallel, conditional)
7. Validate intermediate outputs before proceeding
