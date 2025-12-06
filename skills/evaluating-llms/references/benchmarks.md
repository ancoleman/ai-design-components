# Benchmark Testing for LLMs

Guide to using standardized benchmarks for model capability assessment and comparison.

## Table of Contents

1. [Standard Benchmarks Overview](#standard-benchmarks-overview)
2. [General Knowledge and Reasoning](#general-knowledge-and-reasoning)
3. [Code Generation Benchmarks](#code-generation-benchmarks)
4. [Math Reasoning Benchmarks](#math-reasoning-benchmarks)
5. [Domain-Specific Benchmarks](#domain-specific-benchmarks)
6. [Running Benchmarks with lm-evaluation-harness](#running-benchmarks-with-lm-evaluation-harness)
7. [Creating Custom Benchmarks](#creating-custom-benchmarks)

---

## Standard Benchmarks Overview

### Why Use Benchmarks?

**Model Comparison:** Objectively compare models (GPT-4 vs Claude vs Llama)
**Capability Assessment:** Understand model strengths and weaknesses
**Regression Testing:** Detect performance degradation over time
**Model Selection:** Choose optimal model for specific use cases
**Research:** Academic publication and reproducibility

### Benchmark Selection Criteria

| Use Case | Recommended Benchmarks | Why |
|----------|----------------------|-----|
| General assistant | MMLU, HellaSwag, GPQA | Broad knowledge and reasoning |
| Code generation | HumanEval, MBPP, CodeContests | Programming capability |
| Math reasoning | MATH, GSM8K | Mathematical problem solving |
| Medical AI | MedQA, PubMedQA | Domain expertise |
| Legal AI | LegalBench | Legal reasoning |
| Research/Academic | Multiple benchmarks + SOTA comparison | Comprehensive evaluation |

---

## General Knowledge and Reasoning

### MMLU (Massive Multitask Language Understanding)

**What It Tests:** Broad knowledge across 57 subjects (STEM, humanities, social sciences)

**Format:** Multiple-choice questions with 4 options

**Size:** 15,908 questions total

**Difficulty:** High school to professional level

**Subjects Include:**
- STEM: Physics, Chemistry, Biology, Math, Computer Science
- Humanities: History, Philosophy, Law
- Social Sciences: Psychology, Economics, Sociology
- Professional: Medicine, Accounting, Business

**Current SOTA (2025):**
- GPT-4: 86.4%
- Claude 3 Opus: 86.8%
- Gemini 1.5 Pro: 85.9%

**Example Question:**
```
Subject: High School Chemistry
Question: Which of the following is a strong acid?
A) Acetic acid (CH3COOH)
B) Hydrochloric acid (HCl)
C) Carbonic acid (H2CO3)
D) Phosphoric acid (H3PO4)

Answer: B
```

**Running MMLU:**
```bash
# Install lm-evaluation-harness
pip install lm-eval

# Evaluate GPT-4 on MMLU
lm_eval --model openai-chat \
  --model_args model=gpt-4 \
  --tasks mmlu \
  --num_fewshot 5 \
  --output_path results/mmlu_gpt4.json

# Evaluate local HuggingFace model
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-chat-hf \
  --tasks mmlu \
  --num_fewshot 5
```

**Interpretation:**
- 85%+: Frontier model performance
- 70-85%: Strong general knowledge
- 50-70%: Moderate capability
- < 50%: Weak performance (random guessing is 25%)

---

### HellaSwag (Common Sense Reasoning)

**What It Tests:** Common sense reasoning and sentence completion

**Format:** Choose the most plausible continuation (4 options)

**Size:** 70,000 questions

**Difficulty:** Designed to be easy for humans (95%+), hard for models

**Current SOTA (2025):**
- GPT-4: 95.3% (near saturation)
- Claude 3 Opus: 95.4%
- Gemini 1.5 Pro: 92.5%

**Example:**
```
Context: A man is sitting on a roof. He
A) is using wrap to wrap a pair of skis.
B) uses a ladder to get down.
C) sits on a chair and drinks lemonade.
D) starts pulling up roofing on a roof.

Answer: D (most contextually plausible)
```

**Note:** HellaSwag is saturating (95%+ scores common). Consider newer benchmarks like GPQA for frontier models.

---

### GPQA (Graduate-Level Google-Proof Q&A)

**What It Tests:** Expert-level reasoning in science (PhD-level difficulty)

**Format:** Multiple-choice questions in biology, physics, chemistry

**Size:** 448 questions

**Difficulty:** Very high - experts need Google to answer correctly

**Current SOTA (2025):**
- GPT-4: 39.0%
- Claude 3 Opus: 50.4%
- Gemini 1.5 Pro: 45.2%

**Why GPQA Matters:**
- Not saturated (< 60% scores even for best models)
- Tests frontier model capabilities
- Requires deep reasoning, not just knowledge retrieval

**Example (Biology):**
```
Question: In C4 photosynthesis, the initial CO2 fixation occurs in which cells?
A) Bundle sheath cells
B) Mesophyll cells
C) Guard cells
D) Epidermal cells

Answer: B (requires expert-level plant biology knowledge)
```

---

## Code Generation Benchmarks

### HumanEval

**What It Tests:** Python function generation from docstrings

**Format:** Docstring + function signature → complete implementation

**Size:** 164 programming problems

**Evaluation:** Unit test pass rate (pass@1, pass@10)

**Current SOTA (2025):**
- GPT-4: 67.0% (pass@1)
- Claude 3 Opus: 84.9% (pass@1)
- Codex: 47.0% (pass@1)

**Metrics Explained:**
- **pass@1:** Generate 1 solution, check if it passes tests
- **pass@10:** Generate 10 solutions, check if any pass (measures model's best capability)

**Example Problem:**
```python
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    # Model must generate implementation
```

**Running HumanEval:**
```bash
pip install human-eval

# Generate solutions with your LLM
python generate_solutions.py --model gpt-4 --output samples.jsonl

# Evaluate functional correctness
evaluate_functional_correctness samples.jsonl

# Output: pass@1, pass@10, pass@100
```

---

### HumanEval+

**What It Tests:** HumanEval with 80x more tests per problem

**Why It Exists:** Original HumanEval has limited tests - models can pass with incorrect solutions

**Result:** Models score ~20% lower on HumanEval+ (reveals overfitting to specific tests)

**Example:**
```
HumanEval:    3 tests per problem → GPT-4: 67% pass@1
HumanEval+:  80+ tests per problem → GPT-4: 54% pass@1
```

**Recommendation:** Use HumanEval+ for more rigorous code evaluation.

---

### MBPP (Mostly Basic Python Problems)

**What It Tests:** Python programming with more basic problems than HumanEval

**Size:** 974 problems

**Format:** Natural language description → Python function

**Difficulty:** Entry to intermediate level programming

**Example:**
```
Problem: Write a function to find the minimum value in a list.
Input: [3, 1, 4, 1, 5, 9]
Expected Output: 1

def find_min(numbers: List[int]) -> int:
    # Implementation
```

**When to Use:**
- Testing models on easier programming tasks
- Comparing with HumanEval for difficulty range
- Entry-level coding assistance applications

---

## Math Reasoning Benchmarks

### MATH Dataset

**What It Tests:** Mathematical problem solving from competition math

**Size:** 12,500 problems

**Subjects:** Algebra, geometry, calculus, number theory, probability

**Difficulty:** High school math competition level

**Current SOTA (2025):**
- GPT-4: 52.9%
- Minerva (Google): 50.3%
- Claude 3 Opus: 60.1%

**Example:**
```
Problem: If x^2 + y^2 = 14 and xy = 3, what is (x + y)^2?

Solution:
(x + y)^2 = x^2 + 2xy + y^2
          = (x^2 + y^2) + 2xy
          = 14 + 2(3)
          = 20

Answer: 20
```

**Evaluation:** Exact match or numerical equivalence

---

### GSM8K (Grade School Math 8K)

**What It Tests:** Grade school math word problems

**Size:** 8,500 problems

**Difficulty:** Elementary to middle school level

**Current SOTA (2025):**
- GPT-4: 92.0%
- Claude 3 Opus: 95.0%

**Example:**
```
Problem: A store sells apples for $0.50 each. If you buy 12 apples and get a 10% discount, how much do you pay?

Solution:
Cost before discount: 12 × $0.50 = $6.00
Discount: 10% of $6.00 = $0.60
Final cost: $6.00 - $0.60 = $5.40

Answer: $5.40
```

**Note:** GSM8K is easier than MATH dataset. Use both to assess range of mathematical capability.

---

## Domain-Specific Benchmarks

### Medical: MedQA (USMLE)

**What It Tests:** US Medical Licensing Exam questions

**Format:** Multiple-choice clinical scenarios

**Size:** 12,723 questions

**Current SOTA (2025):**
- GPT-4: 81.4%
- Med-PaLM 2: 86.5%

**Example:**
```
A 45-year-old woman presents with fatigue, weight gain, and cold intolerance.
Lab results show elevated TSH and low free T4. What is the most likely diagnosis?

A) Hyperthyroidism
B) Hypothyroidism
C) Cushing's syndrome
D) Addison's disease

Answer: B (Hypothyroidism)
```

**When to Use:**
- Evaluating medical AI assistants
- Validating domain-specific fine-tuning
- Demonstrating capability for healthcare applications

---

### Medical: PubMedQA

**What It Tests:** Biomedical research question answering

**Format:** Yes/No/Maybe questions based on PubMed abstracts

**Size:** 1,000 expert-annotated questions

**Example:**
```
Context: [PubMed abstract about statins and muscle pain]
Question: Do statins cause muscle pain in most patients?
Answer: No
```

---

### Legal: LegalBench

**What It Tests:** Legal reasoning across 162 tasks

**Coverage:** Contract analysis, statutory interpretation, precedent application

**When to Use:**
- Evaluating legal AI systems
- Validating legal document analysis tools
- Comparing models for legal applications

---

### Finance: FinQA

**What It Tests:** Financial report question answering

**Format:** Questions about earnings reports, balance sheets

**Size:** 8,281 questions

**Example:**
```
Context: [Earnings report excerpt showing revenue of $10M in Q1, $12M in Q2]
Question: What was the revenue growth rate from Q1 to Q2?
Answer: 20%
```

---

## Running Benchmarks with lm-evaluation-harness

### Installation

```bash
pip install lm-eval
```

### Supported Models

**API-based:**
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Google (Gemini)

**Local Models:**
- HuggingFace Transformers
- vLLM (fast inference)
- GGUF (llama.cpp)

### Basic Usage

**Evaluate OpenAI Model:**
```bash
lm_eval --model openai-chat \
  --model_args model=gpt-4 \
  --tasks mmlu,hellaswag,humaneval \
  --num_fewshot 5 \
  --output_path results/
```

**Evaluate HuggingFace Model:**
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-70b-chat-hf,dtype=float16 \
  --tasks mmlu \
  --device cuda:0 \
  --batch_size 8
```

**Evaluate Anthropic Claude:**
```bash
export ANTHROPIC_API_KEY=your_key_here

lm_eval --model anthropic \
  --model_args model=claude-3-opus-20240229 \
  --tasks mmlu,hellaswag
```

### Available Tasks

**List all tasks:**
```bash
lm_eval --tasks list
```

**Common task groups:**
```bash
# All MMLU subjects
--tasks mmlu

# Specific MMLU subject
--tasks mmlu_high_school_chemistry

# Multiple benchmarks
--tasks mmlu,hellaswag,truthfulqa,gsm8k

# Code benchmarks
--tasks humaneval,mbpp
```

### Advanced Options

**Few-shot examples:**
```bash
--num_fewshot 5  # Use 5 examples per question (standard for MMLU)
```

**Limit number of questions:**
```bash
--limit 100  # Test on first 100 questions (for quick testing)
```

**Batch size (local models):**
```bash
--batch_size 16  # Process 16 questions at once (faster)
```

**Output format:**
```bash
--output_path results/my_eval.json  # Save detailed results
```

### Example: Complete Model Comparison

```bash
#!/bin/bash
# Compare multiple models on key benchmarks

TASKS="mmlu,hellaswag,humaneval,gsm8k"
OUTPUT_DIR="benchmarks_2025"

# GPT-4
lm_eval --model openai-chat \
  --model_args model=gpt-4 \
  --tasks $TASKS \
  --output_path $OUTPUT_DIR/gpt4.json

# Claude 3 Opus
lm_eval --model anthropic \
  --model_args model=claude-3-opus-20240229 \
  --tasks $TASKS \
  --output_path $OUTPUT_DIR/claude_opus.json

# Llama 2 70B
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-70b-chat-hf \
  --tasks $TASKS \
  --output_path $OUTPUT_DIR/llama2_70b.json

# Compare results
python compare_benchmarks.py $OUTPUT_DIR/*.json
```

---

## Creating Custom Benchmarks

### When to Create Custom Benchmarks

- Specialized domain not covered by standard benchmarks
- Internal evaluation for company-specific knowledge
- Regression testing for production LLMs
- Academic research requiring new evaluation tasks

### Custom Benchmark Format (lm-evaluation-harness)

**Step 1: Create task configuration (YAML)**

```yaml
# tasks/my_custom_task.yaml
task: my_custom_domain_qa
dataset_path: json
dataset_name: null
validation_split: test
output_type: multiple_choice
test_split: test
num_fewshot: 5
doc_to_text: "Question: {{question}}\nAnswer:"
doc_to_target: "{{answer}}"
doc_to_choice: "{{choices}}"
should_decontaminate: true
metadata:
  version: 1.0
```

**Step 2: Create dataset (JSON)**

```json
{
  "test": [
    {
      "question": "What is the primary function of X?",
      "choices": ["Option A", "Option B", "Option C", "Option D"],
      "answer": 1
    },
    {
      "question": "Which technique is best for Y?",
      "choices": ["Technique 1", "Technique 2", "Technique 3", "Technique 4"],
      "answer": 2
    }
  ]
}
```

**Step 3: Run custom benchmark**

```bash
lm_eval --model openai-chat \
  --model_args model=gpt-4 \
  --tasks my_custom_task \
  --include_path ./tasks/
```

---

## Best Practices

### Benchmark Selection Strategy

1. **Start Broad:** Use MMLU, HellaSwag for general capability
2. **Add Domain-Specific:** Include relevant specialized benchmarks
3. **Include Code:** Add HumanEval if code generation matters
4. **Test Reasoning:** Use GPQA or MATH for frontier models
5. **Custom Validation:** Create domain-specific tests for production use cases

### Avoiding Pitfalls

**Data Contamination:**
- Many models trained on benchmark datasets
- Results may be inflated
- Use held-out test sets or new benchmarks

**Overfitting to Benchmarks:**
- High benchmark scores != real-world performance
- Combine benchmarks with human evaluation
- Test on custom, unseen problems

**Single Metric Myopia:**
- No single benchmark captures all capabilities
- Use multiple benchmarks across domains
- Weight benchmarks by importance to your use case

### Reporting Best Practices

**Include:**
- Model name and version
- Benchmark name and version
- Number of few-shot examples
- Evaluation date
- Full results (not just aggregate)

**Example Report:**
```
Model: GPT-4 (gpt-4-0613)
Benchmark: MMLU (v1.0)
Few-shot: 5 examples
Date: 2025-12-04

Results:
  Overall: 86.4%
  STEM: 88.2%
  Humanities: 84.1%
  Social Sciences: 85.9%
```

---

## Summary

**Quick Reference:**

| Benchmark | Type | Difficulty | Use Case |
|-----------|------|------------|----------|
| MMLU | General knowledge | High school - professional | General capability |
| HellaSwag | Common sense | Easy (saturated) | Baseline reasoning |
| GPQA | Expert science | PhD-level | Frontier models |
| HumanEval | Code generation | Medium | Programming ability |
| MATH | Math reasoning | Competition-level | Advanced math |
| GSM8K | Grade school math | Elementary | Basic math |
| MedQA | Medical knowledge | USMLE-level | Medical AI |

**Recommended Workflow:**
1. Run standard benchmarks for model comparison
2. Add domain-specific benchmarks if applicable
3. Create custom benchmarks for production validation
4. Combine with human evaluation for final validation
