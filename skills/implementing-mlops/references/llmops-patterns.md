# LLMOps Patterns

Specialized MLOps patterns for operationalizing Large Language Models including fine-tuning, prompt management, RAG systems, and LLM-specific monitoring.

## Table of Contents

- [Overview](#overview)
- [Prompt Versioning and Management](#prompt-versioning-and-management)
- [Fine-Tuning Pipelines](#fine-tuning-pipelines)
- [RAG System Deployment](#rag-system-deployment)
- [LLM Monitoring](#llm-monitoring)
- [Guardrails and Safety](#guardrails-and-safety)
- [Cost Optimization](#cost-optimization)
- [Implementation Examples](#implementation-examples)

## Overview

LLMOps extends traditional MLOps with patterns specific to Large Language Models: prompt engineering workflows, fine-tuning pipelines, retrieval-augmented generation, and monitoring for quality, cost, and safety.

### LLMOps vs Traditional MLOps

| Aspect | Traditional ML | LLMs |
|--------|---------------|------|
| Model Size | MB to GB | GB to TB |
| Training Cost | $100-$10K | $10K-$10M |
| Inference Cost | <$0.001/prediction | $0.001-$0.10/prediction |
| Versioning | Model weights + code | Base model + adapters + prompts |
| Evaluation | Metrics (accuracy, F1) | Human eval + automated metrics |
| Monitoring | Drift, accuracy | Hallucination, toxicity, cost |
| Fine-Tuning | Always from scratch | Often use PEFT (LoRA, adapters) |

## Prompt Versioning and Management

Treat prompts as code: version control, A/B testing, and performance tracking.

### Prompt Registry

```python
# prompts.py
from enum import Enum
from dataclasses import dataclass
from typing import Dict

@dataclass
class PromptTemplate:
    """Versioned prompt template."""
    name: str
    version: str
    template: str
    variables: list[str]
    metadata: Dict

# Prompt registry
PROMPTS = {
    'customer_support/classify_intent/v1': PromptTemplate(
        name='classify_intent',
        version='v1.0',
        template="""Classify the customer inquiry into one of these categories: billing, technical_support, product_question, complaint.

Customer inquiry: {inquiry}

Category:""",
        variables=['inquiry'],
        metadata={
            'created_date': '2023-06-01',
            'avg_tokens': 50,
            'accuracy': 0.89
        }
    ),

    'customer_support/classify_intent/v2': PromptTemplate(
        name='classify_intent',
        version='v2.0',
        template="""You are a customer support classifier. Analyze the inquiry and select the most appropriate category.

Categories:
- billing: Payment, invoices, pricing questions
- technical_support: Product not working, bugs, troubleshooting
- product_question: Features, how-to, capabilities
- complaint: Dissatisfaction, refund requests, escalations

Customer inquiry: {inquiry}

Category (respond with one word only):""",
        variables=['inquiry'],
        metadata={
            'created_date': '2023-07-15',
            'avg_tokens': 80,
            'accuracy': 0.94,
            'improvement': '+5% accuracy vs v1'
        }
    )
}

def get_prompt(name: str, version: str = 'latest') -> PromptTemplate:
    """Fetch prompt template by name and version."""
    if version == 'latest':
        # Get latest version
        matching = [k for k in PROMPTS.keys() if k.startswith(f'{name}/')]
        if not matching:
            raise ValueError(f"Prompt '{name}' not found")
        key = sorted(matching)[-1]  # Latest version
    else:
        key = f'{name}/{version}'

    return PROMPTS.get(key)

# Usage
prompt = get_prompt('customer_support/classify_intent', version='v2')
filled_prompt = prompt.template.format(inquiry="My payment didn't go through")
```

### Prompt A/B Testing

```python
# prompt_ab_test.py
import random
from collections import defaultdict

class PromptABTest:
    """A/B test prompts to optimize performance and cost."""

    def __init__(self, variants: dict):
        """
        Args:
            variants: Dict of variant_name -> PromptTemplate
        """
        self.variants = variants
        self.metrics = defaultdict(lambda: {'count': 0, 'correct': 0, 'tokens': 0, 'cost': 0})

    def select_variant(self, user_id: str) -> str:
        """Consistent variant assignment per user."""
        # Hash user_id to variant
        variant_idx = hash(user_id) % len(self.variants)
        return list(self.variants.keys())[variant_idx]

    def get_prompt(self, variant: str, **kwargs) -> str:
        """Get filled prompt for variant."""
        template = self.variants[variant]
        return template.template.format(**kwargs)

    def record_result(self, variant: str, correct: bool, tokens: int, cost: float):
        """Record A/B test result."""
        self.metrics[variant]['count'] += 1
        self.metrics[variant]['correct'] += int(correct)
        self.metrics[variant]['tokens'] += tokens
        self.metrics[variant]['cost'] += cost

    def get_results(self):
        """Get A/B test results."""
        results = {}
        for variant, metrics in self.metrics.items():
            if metrics['count'] > 0:
                results[variant] = {
                    'count': metrics['count'],
                    'accuracy': metrics['correct'] / metrics['count'],
                    'avg_tokens': metrics['tokens'] / metrics['count'],
                    'avg_cost': metrics['cost'] / metrics['count'],
                    'total_cost': metrics['cost']
                }
        return results

# Example usage
ab_test = PromptABTest(variants={
    'control': PROMPTS['customer_support/classify_intent/v1'],
    'treatment': PROMPTS['customer_support/classify_intent/v2']
})

# For each request
user_id = "user_12345"
variant = ab_test.select_variant(user_id)
prompt = ab_test.get_prompt(variant, inquiry="Need help with billing")

# Call LLM
response = llm.complete(prompt)

# Record result
ab_test.record_result(
    variant=variant,
    correct=evaluate_response(response),
    tokens=response.usage.total_tokens,
    cost=response.usage.total_tokens * 0.00001  # $0.01 per 1K tokens
)

# Analyze after 1000 requests
results = ab_test.get_results()
print(results)
# {
#   'control': {'accuracy': 0.89, 'avg_tokens': 50, 'avg_cost': 0.0005},
#   'treatment': {'accuracy': 0.94, 'avg_tokens': 80, 'avg_cost': 0.0008}
# }
# Decision: Treatment has +5% accuracy but +60% cost
```

### Prompt Monitoring with LangSmith

```python
# langsmith_integration.py
from langsmith import Client
from langsmith.run_helpers import traceable

client = Client()

@traceable(name="classify_customer_intent")
def classify_intent(inquiry: str, prompt_version: str = "v2"):
    """Classify customer intent with LangSmith tracing."""

    # Get prompt
    prompt = get_prompt('customer_support/classify_intent', version=prompt_version)
    filled_prompt = prompt.template.format(inquiry=inquiry)

    # Call LLM (traced automatically)
    response = llm.complete(filled_prompt)

    return {
        'category': response.text,
        'prompt_version': prompt_version,
        'tokens': response.usage.total_tokens
    }

# LangSmith automatically logs:
# - Prompt used
# - LLM response
# - Latency
# - Token usage
# - Cost

# View in LangSmith UI:
# - Trace all calls
# - Compare prompt versions
# - Identify slow/expensive queries
```

## Fine-Tuning Pipelines

Parameter-efficient fine-tuning (PEFT) pipelines for domain adaptation.

### LoRA (Low-Rank Adaptation)

Fine-tune small adapter layers instead of full model.

```python
# lora_training.py
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch

def train_lora_model(base_model_name: str, train_dataset, output_dir: str):
    """
    Fine-tune LLM with LoRA.

    Args:
        base_model_name: HuggingFace model (e.g., "meta-llama/Llama-2-7b")
        train_dataset: Training dataset
        output_dir: Output directory for adapter weights
    """

    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        load_in_8bit=True,  # Quantization to reduce memory
        device_map="auto",
        torch_dtype=torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    # LoRA configuration
    lora_config = LoraConfig(
        r=16,  # Rank (higher = more parameters, better quality)
        lora_alpha=32,  # Scaling factor
        target_modules=["q_proj", "v_proj"],  # Which layers to adapt
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    # Add LoRA adapters
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    # Output: trainable params: 4.2M || all params: 6.7B || trainable%: 0.06%

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch"
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer
    )

    # Train
    trainer.train()

    # Save LoRA adapters (only 10-100MB!)
    model.save_pretrained(output_dir)

    return model

# Usage
train_dataset = load_custom_dataset()
model = train_lora_model(
    base_model_name="meta-llama/Llama-2-7b-hf",
    train_dataset=train_dataset,
    output_dir="./lora_adapters/customer_support_v1"
)
```

### QLoRA (Quantized LoRA)

LoRA with 4-bit quantization for even lower memory usage.

```python
# qlora_training.py
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

def train_qlora_model(base_model_name: str, train_dataset, output_dir: str):
    """Fine-tune with 4-bit quantization (QLoRA)."""

    # 4-bit quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )

    # Load model in 4-bit
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )

    # Prepare for training
    model = prepare_model_for_kbit_training(model)

    # LoRA config (same as before)
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    model = get_peft_model(model, lora_config)

    # Train (rest same as LoRA)
    # ...

# QLoRA benefits:
# - Llama-2-7B: 28GB (16-bit) → 7GB (4-bit)
# - Enables fine-tuning on consumer GPUs (RTX 3090)
```

### Fine-Tuning Pipeline with MLflow

```python
# mlflow_lora_pipeline.py
import mlflow
from mlflow.models import infer_signature

def finetune_and_log_model(base_model_name, train_dataset, eval_dataset):
    """Complete fine-tuning pipeline with MLflow tracking."""

    with mlflow.start_run(run_name="lora_customer_support_v1"):

        # Log parameters
        mlflow.log_params({
            "base_model": base_model_name,
            "method": "LoRA",
            "rank": 16,
            "alpha": 32,
            "epochs": 3,
            "learning_rate": 2e-4
        })

        # Train
        model = train_lora_model(base_model_name, train_dataset, output_dir="./lora_adapters")

        # Evaluate
        eval_results = evaluate_model(model, eval_dataset)

        # Log metrics
        mlflow.log_metrics({
            "eval_accuracy": eval_results['accuracy'],
            "eval_f1": eval_results['f1'],
            "avg_inference_time": eval_results['avg_latency']
        })

        # Log model
        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=LoRAModel(base_model_name, "./lora_adapters"),
            registered_model_name="customer_support_classifier"
        )

        # Log adapters
        mlflow.log_artifacts("./lora_adapters", artifact_path="lora_adapters")

        print(f"Model logged to MLflow: {mlflow.active_run().info.run_id}")
```

## RAG System Deployment

Deploy Retrieval-Augmented Generation systems for production.

### RAG Architecture

```
User Query
    |
Embedding Model (embed query)
    |
Vector DB (retrieve relevant docs)
    |
Reranking Model (optional, improve relevance)
    |
Prompt Construction (query + retrieved docs)
    |
LLM (generate answer)
    |
Response
```

### Production RAG Implementation

```python
# rag_system.py
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class ProductionRAG:
    """Production-grade RAG system."""

    def __init__(self, vector_db_path: str, llm_model: str = "gpt-3.5-turbo"):
        # Embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Vector database
        self.vector_db = Chroma(
            persist_directory=vector_db_path,
            embedding_function=self.embeddings
        )

        # LLM
        self.llm = OpenAI(model=llm_model, temperature=0)

        # RAG prompt
        self.prompt_template = PromptTemplate(
            template="""Answer the question based on the provided context. If the context doesn't contain enough information, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:""",
            input_variables=["context", "question"]
        )

        # RAG chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )

    def query(self, question: str):
        """Query RAG system."""
        result = self.qa_chain({"query": question})

        return {
            'answer': result['result'],
            'source_documents': [
                {
                    'content': doc.page_content,
                    'metadata': doc.metadata
                }
                for doc in result['source_documents']
            ]
        }

# Usage
rag = ProductionRAG(vector_db_path="./chroma_db")
result = rag.query("What is the return policy?")

print(f"Answer: {result['answer']}")
print(f"Sources: {result['source_documents']}")
```

### RAG with Reranking

Improve retrieval quality with reranking model.

```python
# rag_with_reranking.py
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

class RAGWithReranking:
    """RAG with reranking for improved relevance."""

    def __init__(self, vector_db_path: str):
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_db = Chroma(persist_directory=vector_db_path, embedding_function=self.embeddings)

        # Base retriever (retrieve top 10)
        base_retriever = self.vector_db.as_retriever(search_kwargs={"k": 10})

        # Reranker (rerank to top 3)
        compressor = CohereRerank(top_n=3)

        # Compression retriever
        self.retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

    def query(self, question: str):
        # Retrieve + rerank
        docs = self.retriever.get_relevant_documents(question)

        # Generate answer
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = self.prompt_template.format(context=context, question=question)
        answer = self.llm(prompt)

        return {'answer': answer, 'source_documents': docs}
```

## LLM Monitoring

Monitor LLMs for quality, cost, latency, and safety.

### Metrics to Monitor

| Category | Metrics |
|----------|---------|
| Quality | Hallucination rate, answer relevance, factual accuracy |
| Performance | Latency (P50, P95, P99), throughput (req/s) |
| Cost | Tokens/request, cost/request, daily spend |
| Safety | Toxicity, bias, PII leakage, prompt injection |

### LLM Observability with Arize Phoenix

```python
# phoenix_monitoring.py
from phoenix.trace import using_project
from openinference.instrumentation.langchain import LangChainInstrumentor

# Auto-instrument LangChain
LangChainInstrumentor().instrument()

# All LangChain calls automatically traced
with using_project("customer_support_rag"):
    result = rag.query("What is the return policy?")

# Phoenix tracks:
# - Retrieval: Query embedding, retrieved docs, relevance scores
# - Generation: LLM prompt, response, tokens, latency
# - Evaluation: Hallucination detection, answer relevance
```

### Custom Monitoring Pipeline

```python
# llm_monitoring.py
from prometheus_client import Counter, Histogram, Gauge
import openai

# Metrics
llm_requests_total = Counter('llm_requests_total', 'Total LLM requests', ['model', 'status'])
llm_latency_seconds = Histogram('llm_latency_seconds', 'LLM latency', ['model'])
llm_tokens_total = Counter('llm_tokens_total', 'Total tokens', ['model', 'type'])
llm_cost_total = Counter('llm_cost_total', 'Total cost (USD)', ['model'])
llm_hallucination_rate = Gauge('llm_hallucination_rate', 'Hallucination rate', ['model'])

class MonitoredLLM:
    """LLM client with monitoring."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.client = openai.OpenAI()

    def complete(self, prompt: str, **kwargs):
        """Complete with monitoring."""
        import time
        start = time.time()

        try:
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )

            # Track metrics
            latency = time.time() - start
            llm_latency_seconds.labels(model=self.model).observe(latency)
            llm_requests_total.labels(model=self.model, status='success').inc()

            # Token usage
            usage = response.usage
            llm_tokens_total.labels(model=self.model, type='prompt').inc(usage.prompt_tokens)
            llm_tokens_total.labels(model=self.model, type='completion').inc(usage.completion_tokens)

            # Cost (GPT-3.5: $0.0015/1K prompt, $0.002/1K completion)
            cost = (usage.prompt_tokens * 0.0015 / 1000) + (usage.completion_tokens * 0.002 / 1000)
            llm_cost_total.labels(model=self.model).inc(cost)

            # Check for hallucination (simple heuristic)
            answer = response.choices[0].message.content
            if self._check_hallucination(prompt, answer):
                llm_hallucination_rate.labels(model=self.model).inc()

            return response

        except Exception as e:
            llm_requests_total.labels(model=self.model, status='error').inc()
            raise

    def _check_hallucination(self, prompt: str, answer: str) -> bool:
        """Simple hallucination check (use more sophisticated in production)."""
        # Check for hedging phrases (indicates uncertainty)
        hedge_phrases = ["I don't know", "I'm not sure", "I don't have information"]
        return not any(phrase in answer for phrase in hedge_phrases)

# Usage
llm = MonitoredLLM(model="gpt-3.5-turbo")
response = llm.complete("What is the capital of France?")

# Prometheus metrics exported at /metrics
# Visualize in Grafana
```

## Guardrails and Safety

Implement safety checks to prevent harmful outputs.

### NeMo Guardrails

```python
# guardrails_config.yaml
rails:
  input:
    flows:
      - check for jailbreak attempts
      - check for PII in input
  output:
    flows:
      - check for toxic language
      - check for hallucination
      - check for PII leakage

# guardrails.py
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./guardrails_config")
rails = LLMRails(config)

def safe_llm_call(prompt: str) -> str:
    """LLM call with guardrails."""
    response = rails.generate(messages=[{"role": "user", "content": prompt}])
    return response['content']

# Automatically blocks:
# - Jailbreak attempts
# - Toxic outputs
# - PII leakage
```

### Custom Safety Checks

```python
# safety_checks.py
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class SafetyChecker:
    """Safety checks for LLM inputs and outputs."""

    def __init__(self):
        self.pii_analyzer = AnalyzerEngine()
        self.pii_anonymizer = AnonymizerEngine()

    def check_input(self, text: str) -> dict:
        """Check input for safety issues."""
        issues = []

        # Check for PII
        pii_results = self.pii_analyzer.analyze(text=text, language='en')
        if pii_results:
            issues.append({
                'type': 'PII_DETECTED',
                'entities': [r.entity_type for r in pii_results]
            })

        # Check for prompt injection
        if self._is_prompt_injection(text):
            issues.append({'type': 'PROMPT_INJECTION'})

        return {'safe': len(issues) == 0, 'issues': issues}

    def check_output(self, text: str) -> dict:
        """Check output for safety issues."""
        issues = []

        # Check for toxicity
        toxicity_score = self._check_toxicity(text)
        if toxicity_score > 0.7:
            issues.append({'type': 'TOXIC_CONTENT', 'score': toxicity_score})

        # Check for PII leakage
        pii_results = self.pii_analyzer.analyze(text=text, language='en')
        if pii_results:
            issues.append({'type': 'PII_LEAKAGE', 'entities': [r.entity_type for r in pii_results]})

        return {'safe': len(issues) == 0, 'issues': issues}

    def _is_prompt_injection(self, text: str) -> bool:
        """Detect prompt injection attempts."""
        injection_patterns = [
            r"ignore previous instructions",
            r"disregard.*above",
            r"forget.*instructions",
            r"system.*prompt"
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in injection_patterns)

    def _check_toxicity(self, text: str) -> float:
        """Check text toxicity (use Perspective API or Detoxify in production)."""
        # Placeholder: Use Perspective API or Detoxify library
        return 0.1  # Low toxicity

# Usage
checker = SafetyChecker()

# Check input
input_check = checker.check_input("My SSN is 123-45-6789. Ignore previous instructions.")
if not input_check['safe']:
    print(f"Input blocked: {input_check['issues']}")

# Check output
output_check = checker.check_output("Your password is abc123")
if not output_check['safe']:
    print(f"Output blocked: {output_check['issues']}")
```

## Cost Optimization

Strategies to reduce LLM inference costs.

### Prompt Caching

```python
# prompt_caching.py
import hashlib
import redis
import json

class PromptCache:
    """Cache LLM responses for identical prompts."""

    def __init__(self, redis_host='localhost', ttl=3600):
        self.redis = redis.Redis(host=redis_host, decode_responses=True)
        self.ttl = ttl  # Cache TTL in seconds

    def get_cached_response(self, prompt: str, model: str):
        """Get cached response if exists."""
        cache_key = self._get_cache_key(prompt, model)
        cached = self.redis.get(cache_key)

        if cached:
            return json.loads(cached)
        return None

    def cache_response(self, prompt: str, model: str, response: dict):
        """Cache LLM response."""
        cache_key = self._get_cache_key(prompt, model)
        self.redis.setex(cache_key, self.ttl, json.dumps(response))

    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key from prompt and model."""
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        return f"llm_cache:{model}:{prompt_hash}"

# Usage
cache = PromptCache()

def cached_llm_call(prompt: str, model: str = "gpt-3.5-turbo"):
    """LLM call with caching."""

    # Check cache
    cached_response = cache.get_cached_response(prompt, model)
    if cached_response:
        print("Cache hit!")
        return cached_response

    # Call LLM
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    # Cache response
    response_dict = response.to_dict()
    cache.cache_response(prompt, model, response_dict)

    return response_dict

# Identical prompts served from cache (zero cost)
```

### Model Selection Strategy

```python
# model_router.py
class ModelRouter:
    """Route requests to appropriate model based on complexity."""

    def __init__(self):
        self.models = {
            'simple': {'name': 'gpt-3.5-turbo', 'cost_per_1k': 0.002},
            'medium': {'name': 'gpt-4', 'cost_per_1k': 0.03},
            'complex': {'name': 'gpt-4-turbo', 'cost_per_1k': 0.01}
        }

    def route(self, prompt: str, complexity: str = None):
        """Route to appropriate model."""

        if complexity is None:
            complexity = self._estimate_complexity(prompt)

        model = self.models[complexity]
        print(f"Routing to {model['name']} (complexity: {complexity})")

        return model

    def _estimate_complexity(self, prompt: str) -> str:
        """Estimate prompt complexity."""
        # Simple heuristic (use classifier in production)
        if len(prompt) < 100 and '?' in prompt:
            return 'simple'  # Short factual question
        elif 'analyze' in prompt.lower() or 'compare' in prompt.lower():
            return 'complex'  # Requires reasoning
        else:
            return 'medium'

# Usage
router = ModelRouter()

# Simple: Use cheap model
model = router.route("What is 2+2?")  # Routes to gpt-3.5-turbo

# Complex: Use expensive model
model = router.route("Analyze the implications of quantum computing on cryptography")  # Routes to gpt-4
```

## Implementation Examples

### Example: End-to-End LLMOps Pipeline

```python
# llmops_pipeline.py
class LLMOpsPipeline:
    """Complete LLMOps pipeline."""

    def __init__(self):
        self.prompt_registry = PromptRegistry()
        self.safety_checker = SafetyChecker()
        self.cache = PromptCache()
        self.monitor = MonitoredLLM()

    def query(self, user_input: str, prompt_name: str):
        """Complete LLMOps query flow."""

        # 1. Safety check (input)
        input_check = self.safety_checker.check_input(user_input)
        if not input_check['safe']:
            return {'error': 'Input blocked', 'issues': input_check['issues']}

        # 2. Get prompt template
        prompt = self.prompt_registry.get_prompt(prompt_name, version='latest')
        filled_prompt = prompt.template.format(user_input=user_input)

        # 3. Check cache
        cached = self.cache.get_cached_response(filled_prompt, model="gpt-3.5-turbo")
        if cached:
            return {'answer': cached['answer'], 'cached': True}

        # 4. Call LLM (monitored)
        response = self.monitor.complete(filled_prompt)
        answer = response.choices[0].message.content

        # 5. Safety check (output)
        output_check = self.safety_checker.check_output(answer)
        if not output_check['safe']:
            return {'error': 'Output blocked', 'issues': output_check['issues']}

        # 6. Cache response
        self.cache.cache_response(filled_prompt, "gpt-3.5-turbo", {'answer': answer})

        return {'answer': answer, 'cached': False}

# Usage
pipeline = LLMOpsPipeline()
result = pipeline.query("What is the return policy?", prompt_name="customer_support/answer_question")
print(result)
```
