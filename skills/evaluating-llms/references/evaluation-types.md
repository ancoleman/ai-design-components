# Evaluation Types by AI Task

Comprehensive guide to evaluation methods for different LLM task types.

## Table of Contents

1. [Classification Tasks](#classification-tasks)
2. [Generation Tasks](#generation-tasks)
3. [Question Answering Tasks](#question-answering-tasks)
4. [Code Generation Tasks](#code-generation-tasks)
5. [Conversational Tasks](#conversational-tasks)

---

## Classification Tasks

### Overview

Classification tasks involve assigning discrete labels to inputs.

**Common Examples:**
- Sentiment analysis (positive/negative/neutral)
- Intent detection (question/command/statement)
- Content moderation (safe/unsafe)
- Entity extraction (person/organization/location)
- Topic classification (sports/politics/technology)

### Evaluation Metrics

#### Accuracy
**Definition:** Proportion of correct predictions.

**Formula:** `Accuracy = Correct Predictions / Total Predictions`

**When to Use:** Balanced datasets where all classes are equally important.

**Limitation:** Misleading with imbalanced datasets (e.g., 95% negative, 5% positive).

#### Precision
**Definition:** Of all positive predictions, how many were actually positive?

**Formula:** `Precision = True Positives / (True Positives + False Positives)`

**When to Use:** When false positives are costly (e.g., spam detection).

**Interpretation:** High precision = few false alarms.

#### Recall
**Definition:** Of all actual positives, how many did we correctly identify?

**Formula:** `Recall = True Positives / (True Positives + False Negatives)`

**When to Use:** When false negatives are costly (e.g., fraud detection).

**Interpretation:** High recall = few missed positives.

#### F1 Score
**Definition:** Harmonic mean of precision and recall.

**Formula:** `F1 = 2 * (Precision * Recall) / (Precision + Recall)`

**When to Use:** Need to balance precision and recall.

**Interpretation:** Best for imbalanced datasets.

#### Confusion Matrix
**Definition:** Table showing actual vs predicted labels.

**Example:**
```
                Predicted
              Pos    Neg
Actual  Pos   90     10      (90 TP, 10 FN)
        Neg   5      95      (5 FP, 95 TN)
```

**When to Use:** Understanding which classes are confused with each other.

### Implementation Example

```python
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

# Ground truth and predictions
y_true = ["positive", "negative", "neutral", "positive", "negative", "neutral", "positive"]
y_pred = ["positive", "negative", "neutral", "neutral", "negative", "positive", "positive"]

# Calculate all metrics
accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1, support = precision_recall_fscore_support(
    y_true, y_pred, average='weighted'
)
conf_matrix = confusion_matrix(y_true, y_pred)

print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1 Score: {f1:.2%}")
print(f"\nConfusion Matrix:\n{conf_matrix}")

# Detailed report
print(classification_report(y_true, y_pred))
```

---

## Generation Tasks

### Overview

Generation tasks involve producing open-ended text outputs.

**Common Examples:**
- Text summarization
- Creative writing
- Product descriptions
- Email composition
- Code comments and documentation

### Evaluation Metrics

#### BLEU (Bilingual Evaluation Understudy)
**Definition:** Measures n-gram overlap between generated and reference text.

**Score Range:** 0-1 (or 0-100 if scaled)

**When to Use:** Translation tasks, text with clear reference outputs.

**Limitations:**
- Poor correlation with human judgment for creative tasks
- Favors shorter outputs
- Doesn't capture semantic meaning

**Example:**
```python
from nltk.translate.bleu_score import sentence_bleu

reference = [['the', 'cat', 'sat', 'on', 'the', 'mat']]
candidate = ['the', 'cat', 'is', 'on', 'the', 'mat']
score = sentence_bleu(reference, candidate)
print(f"BLEU score: {score:.2f}")
```

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
**Definition:** Measures recall-oriented n-gram overlap.

**Variants:**
- ROUGE-1: Unigram overlap
- ROUGE-2: Bigram overlap
- ROUGE-L: Longest common subsequence

**When to Use:** Summarization tasks, recall-oriented evaluation.

**Example:**
```python
from rouge import Rouge

rouge = Rouge()
reference = "The cat sat on the mat"
hypothesis = "The cat is on the mat"
scores = rouge.get_scores(hypothesis, reference)
print(f"ROUGE-1: {scores[0]['rouge-1']['f']:.2f}")
```

#### BERTScore
**Definition:** Contextual embedding similarity using BERT.

**Score Range:** 0-1

**Advantages:**
- Captures semantic similarity
- Better correlation with human judgment than BLEU/ROUGE
- Robust to paraphrasing

**When to Use:** Generation tasks where semantic meaning matters more than exact wording.

**Example:**
```python
from bert_score import score

references = ["The cat sat on the mat"]
candidates = ["A feline was sitting on a rug"]
P, R, F1 = score(candidates, references, lang="en")
print(f"BERTScore F1: {F1.mean():.2f}")
```

### LLM-as-Judge for Generation Quality

**Recommended Approach:** Use automated metrics for fast feedback, LLM-as-judge for nuanced quality.

**Sample Rubric (1-5 scale):**
- **Relevance:** Does the output address the input?
- **Coherence:** Is the output logically structured?
- **Fluency:** Is the language natural and grammatical?
- **Accuracy:** Are factual claims correct?
- **Helpfulness:** Does the output solve the user's problem?

---

## Question Answering Tasks

### Overview

Question answering tasks involve answering questions based on provided context or general knowledge.

**Types:**
- **Extractive QA:** Answer extracted from context (SQuAD)
- **Abstractive QA:** Answer generated from understanding (RAG)
- **Closed-book QA:** Answer without context (TriviaQA)

### Evaluation Metrics

#### Exact Match (EM)
**Definition:** Answer exactly matches reference (case-insensitive).

**Score:** Binary (0 or 1)

**When to Use:** Extractive QA with single correct answer.

**Example:**
```python
def exact_match(prediction: str, reference: str) -> float:
    return float(prediction.strip().lower() == reference.strip().lower())

em = exact_match("Paris", "paris")  # 1.0
```

#### F1 Score (Token-Level)
**Definition:** Overlap between predicted and reference tokens.

**Calculation:**
1. Tokenize prediction and reference
2. Calculate precision: Overlapping tokens / Prediction tokens
3. Calculate recall: Overlapping tokens / Reference tokens
4. F1 = harmonic mean of precision and recall

**When to Use:** QA tasks where partial credit is acceptable.

**Example:**
```python
def f1_score_tokens(prediction: str, reference: str) -> float:
    pred_tokens = prediction.lower().split()
    ref_tokens = reference.lower().split()

    common = set(pred_tokens) & set(ref_tokens)
    if len(common) == 0:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(ref_tokens)
    return 2 * (precision * recall) / (precision + recall)

f1 = f1_score_tokens("Paris, France", "Paris")  # 0.67
```

#### Semantic Similarity
**Definition:** Embedding-based similarity between answers.

**Methods:**
- Cosine similarity of sentence embeddings
- BERT-based similarity
- Cross-encoder scoring

**When to Use:** Multiple valid phrasings of correct answer.

**Example:**
```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
pred_embedding = model.encode("The capital is Paris")
ref_embedding = model.encode("Paris")
similarity = util.cos_sim(pred_embedding, ref_embedding)
print(f"Similarity: {similarity[0][0]:.2f}")
```

---

## Code Generation Tasks

### Overview

Code generation tasks involve producing executable code from natural language descriptions.

**Common Examples:**
- Function implementation from docstring
- Code completion
- Bug fixing
- Code translation between languages

### Evaluation Metrics

#### Functional Correctness (Pass@K)
**Definition:** Percentage of problems with at least one correct solution in K samples.

**Pass@1:** Generate 1 solution, check if correct
**Pass@10:** Generate 10 solutions, check if any are correct

**When to Use:** Primary metric for code generation evaluation.

**Calculation:**
```python
# Example: HumanEval Pass@1
correct_solutions = 134
total_problems = 164
pass_at_1 = correct_solutions / total_problems
print(f"Pass@1: {pass_at_1:.2%}")  # 81.7%
```

#### Unit Test Pass Rate
**Definition:** Percentage of unit tests passed by generated code.

**When to Use:** Code generation with comprehensive test suites.

**Example:**
```python
import subprocess

def evaluate_code(code: str, test_file: str) -> float:
    # Write code to temp file
    with open("solution.py", "w") as f:
        f.write(code)

    # Run pytest
    result = subprocess.run(
        ["pytest", test_file, "-v"],
        capture_output=True,
        text=True
    )

    # Parse results
    passed = result.stdout.count(" PASSED")
    total = result.stdout.count(" PASSED") + result.stdout.count(" FAILED")
    return passed / total if total > 0 else 0.0
```

#### Syntax Validity
**Definition:** Does the code parse without syntax errors?

**When to Use:** Quick sanity check before running tests.

**Example:**
```python
import ast

def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
```

#### Code Quality Metrics
**Metrics:**
- **Linting Score:** pylint, flake8, ESLint scores
- **Cyclomatic Complexity:** Code complexity measure
- **Code Coverage:** How much code is exercised by tests

**When to Use:** Evaluating code maintainability and quality.

---

## Conversational Tasks

### Overview

Conversational tasks involve multi-turn dialogues where context matters.

**Common Examples:**
- Customer support chatbots
- Virtual assistants
- Tutoring systems
- Interactive storytelling

### Evaluation Metrics

#### Context Maintenance
**Definition:** Does the system remember and reference earlier conversation turns?

**Evaluation Method:**
1. Create test conversations with references to earlier turns
2. Check if system responds appropriately
3. Use LLM-as-judge to assess context awareness

**Example Test:**
```
Turn 1: "I need to book a flight to Paris"
Turn 2: "What dates are available?" (expect: system remembers Paris)
Turn 3: "Actually, change the destination to London"
Turn 4: "What's the weather like there?" (expect: system knows "there" = London)
```

#### Topic Coherence
**Definition:** Does the conversation stay on track or derail?

**Evaluation Method:**
- Use topic modeling to track conversation topics
- Flag sudden, unexplained topic shifts
- LLM-as-judge to rate coherence (1-5 scale)

#### Task Completion Rate
**Definition:** Percentage of conversations where user achieves their goal.

**Evaluation Method:**
- Define success criteria per task type
- Track whether conversation reaches success state
- Collect user confirmation ("Did this solve your problem?")

#### Average Turns to Resolution
**Definition:** How many conversation turns to complete task?

**Target:** Minimize turns while maintaining quality.

**Calculation:**
```python
conversations = [
    {"turns": 5, "successful": True},
    {"turns": 3, "successful": True},
    {"turns": 10, "successful": False},
]

successful_convos = [c for c in conversations if c["successful"]]
avg_turns = sum(c["turns"] for c in successful_convos) / len(successful_convos)
print(f"Average turns to resolution: {avg_turns:.1f}")
```

---

## Best Practices

### Multi-Metric Evaluation
Never rely on a single metric. Combine:
- Automated metrics (fast, objective)
- LLM-as-judge (nuanced, scalable)
- Human evaluation (ground truth validation)

### Metric Selection Checklist
- [ ] Does the metric align with user satisfaction?
- [ ] Is the metric sensitive to quality differences?
- [ ] Can the metric be gamed or exploited?
- [ ] Is the metric cost-effective at scale?
- [ ] Does the metric capture what you actually care about?

### Common Mistakes
1. **Using BLEU for creative generation:** Weak correlation with quality
2. **Exact match for abstractive QA:** Too strict, ignores valid paraphrases
3. **Ignoring user feedback:** Automated metrics miss real-world failures
4. **No baseline comparison:** Always compare against baseline (random, simple heuristic)
