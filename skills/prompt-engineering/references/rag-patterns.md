# RAG (Retrieval-Augmented Generation) Patterns

Comprehensive patterns for implementing retrieval-augmented generation systems that ground LLM outputs in external knowledge sources.

## Table of Contents

1. [Overview](#overview)
2. [Context Injection Strategies](#context-injection-strategies)
3. [Citation and Attribution](#citation-and-attribution)
4. [Multi-Document Synthesis](#multi-document-synthesis)
5. [Handling Conflicting Information](#handling-conflicting-information)
6. [Context Window Optimization](#context-window-optimization)
7. [Chunk Size Considerations](#chunk-size-considerations)
8. [Prompt Templates for RAG](#prompt-templates-for-rag)
9. [Common Pitfalls](#common-pitfalls)

## Overview

**What is RAG?**
Retrieval-Augmented Generation combines information retrieval (search) with language generation. Instead of relying solely on the model's training data, RAG systems:

1. Retrieve relevant documents from a knowledge base
2. Inject retrieved context into the prompt
3. Generate answers grounded in the retrieved information

**When to use RAG:**
- Domain-specific knowledge not in training data
- Frequently updated information (news, documentation)
- Need for factual grounding and citations
- Reducing hallucination on specialized topics

**Basic RAG workflow:**
```
User Query → Embed Query → Search Vector DB → Retrieve Top-K Docs
→ Format Context → LLM Prompt → Generate Answer → Return with Citations
```

## Context Injection Strategies

### 1. Simple Context Injection

**Pattern:** Place retrieved context before the question.

```python
def simple_rag_prompt(query: str, documents: list[str]) -> str:
    context = "\n\n".join([
        f"Document {i+1}:\n{doc}"
        for i, doc in enumerate(documents)
    ])

    return f"""
Answer the question based on the provided context.

Context:
{context}

Question: {query}

Answer:
"""
```

**Best practices:**
- Clearly separate context from question
- Number documents for citation
- Use consistent formatting

### 2. Structured Context with Metadata

**Pattern:** Include source metadata for better attribution.

```python
def structured_rag_prompt(query: str, chunks: list[dict]) -> str:
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(f"""
[Document {i+1}]
Source: {chunk['source']}
Date: {chunk['date']}
Content: {chunk['text']}
""")

    context = "\n".join(context_parts)

    return f"""
Answer the question using only information from the provided documents.
Cite sources using [Document N] notation.

{context}

Question: {query}

Answer (with citations):
"""
```

**Metadata to include:**
- Source URL/filename
- Publication date
- Author/organization
- Section/page number
- Relevance score

### 3. XML-Structured Context (Claude Preferred)

**Pattern:** Use XML tags for clear structure.

```python
def xml_rag_prompt(query: str, documents: list[dict]) -> str:
    context_xml = []
    for doc in documents:
        context_xml.append(f"""
<document>
  <source>{doc['source']}</source>
  <date>{doc['date']}</date>
  <content>
{doc['text']}
  </content>
</document>
""")

    return f"""
Answer the user's question using only information from the provided documents.

<context>
{"".join(context_xml)}
</context>

<question>
{query}
</question>

Provide a comprehensive answer with citations in the format [Source: filename].
"""
```

**Advantages:**
- Clear hierarchical structure
- Easy for model to parse
- Works exceptionally well with Claude
- Supports nested metadata

### 4. Role-Based Context Injection

**Pattern:** Use system message for context, user message for question.

```python
from anthropic import Anthropic

client = Anthropic()

def role_based_rag(query: str, documents: list[str]) -> str:
    context = "\n\n---\n\n".join(documents)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=f"""
You are a helpful research assistant with access to the following knowledge base.
Answer questions using ONLY information from this knowledge base.
Always cite your sources.

Knowledge Base:
{context}
""",
        messages=[
            {"role": "user", "content": query}
        ]
    )
    return response.content[0].text
```

**When to use:** Long-running conversations where context stays constant.

## Citation and Attribution

### 1. Inline Citations

**Prompt pattern:**
```python
prompt = """
Answer the question and cite sources using inline citations [1], [2], etc.

Documents:
[1] Source A: "Content from source A..."
[2] Source B: "Content from source B..."

Question: {query}

Answer with inline citations:
"""
```

**Example output:**
```
The capital of France is Paris [1]. It has been the capital since 987 CE [2].
```

### 2. Block Citations with Quotes

**Prompt pattern:**
```python
prompt = """
Answer the question and include exact quotes from source documents.

Format:
Answer: [your answer]

Supporting Evidence:
- "exact quote" (Source: document.pdf, Page 5)
- "another quote" (Source: article.html)

Documents:
{context}

Question: {query}
"""
```

### 3. Anthropic Citation Pattern

**Recommended for Claude:**
```python
system_prompt = """
When answering questions:
1. Use ONLY information from provided documents
2. For each claim, cite the source using <citation source="filename">claim</citation>
3. If information is not in documents, state "I don't have information about this in the provided documents"
"""

user_prompt = """
<documents>
  <document id="doc1" source="product_manual.pdf">
    The device operates at 120V AC.
  </document>
  <document id="doc2" source="safety_guide.pdf">
    Always unplug before maintenance.
  </document>
</documents>

<question>
What voltage does the device use and what safety precautions should I take?
</question>
"""
```

**Expected output:**
```
<citation source="product_manual.pdf">The device operates at 120V AC</citation>.
For safety, <citation source="safety_guide.pdf">always unplug before maintenance</citation>.
```

### 4. Confidence-Weighted Citations

**Pattern:** Ask model to indicate confidence in each cited fact.

```python
prompt = """
Answer with citations and confidence levels.

Format:
[CLAIM] - Source: [document], Confidence: [HIGH/MEDIUM/LOW]

Use:
- HIGH: Direct quote or explicit statement
- MEDIUM: Strong inference from context
- LOW: Weak inference or unclear source

Documents:
{context}

Question: {query}
"""
```

## Multi-Document Synthesis

### 1. Comparative Analysis

**Pattern:** Synthesize across multiple sources.

```python
prompt = """
Compare and synthesize information from multiple sources.

Sources:
{numbered_sources}

Task: {query}

Provide a comprehensive answer that:
1. Identifies common themes across sources
2. Notes any disagreements or contradictions
3. Cites specific sources for each point
4. Synthesizes into a coherent narrative

Analysis:
"""
```

### 2. Timeline Construction

**Pattern:** Organize information chronologically.

```python
prompt = """
Create a timeline from the provided documents.

Documents (with dates):
{dated_documents}

Question: {query}

Timeline format:
- YYYY-MM-DD: Event description [Source: doc.pdf]
- YYYY-MM-DD: Next event [Source: article.html]

Timeline:
"""
```

### 3. Evidence Aggregation

**Pattern:** Collect supporting and contradicting evidence.

```python
prompt = """
Evaluate the claim by examining all evidence.

Claim: {claim}

Documents:
{context}

Analysis:
## Supporting Evidence
- [Quote/summary] (Source: X)

## Contradicting Evidence
- [Quote/summary] (Source: Y)

## Conclusion
[Synthesis with confidence level]
"""
```

## Handling Conflicting Information

### 1. Conflict Detection

**Prompt pattern:**
```python
prompt = """
Identify and resolve conflicts in the provided information.

Documents:
{context}

Question: {query}

Response format:
## Answer
[Your synthesized answer]

## Conflicting Information Found
- Source A states: "..."
- Source B states: "..."

## Resolution Strategy
[How you resolved the conflict: newest source, most authoritative, majority, etc.]
"""
```

### 2. Source Prioritization

**Pattern:** Define source authority hierarchy.

```python
def prioritized_rag(query: str, documents: list[dict]) -> str:
    # Sort by priority: official docs > recent articles > older articles
    sorted_docs = sorted(
        documents,
        key=lambda d: (
            d.get('is_official', False),
            d.get('date', '1900-01-01')
        ),
        reverse=True
    )

    prompt = f"""
Answer using the provided sources. In case of conflicts:
1. Prioritize official documentation
2. Prefer more recent information
3. Note when sources disagree

Sources (in priority order):
{format_documents(sorted_docs)}

Question: {query}
"""
    return prompt
```

### 3. Temporal Awareness

**Pattern:** Handle time-sensitive information.

```python
prompt = """
Answer the question with awareness of temporal context.

Current date: {current_date}

Documents:
{context_with_dates}

Question: {query}

If information has changed over time:
1. Provide the most recent information
2. Note historical context if relevant
3. Cite the date of each source

Answer:
"""
```

## Context Window Optimization

### 1. Re-Ranking Retrieved Documents

**Pattern:** Retrieve top-K (e.g., 20), then re-rank to select top-N (e.g., 5) for LLM.

```python
from sentence_transformers import CrossEncoder

def rerank_documents(query: str, documents: list[str], top_k: int = 5) -> list[str]:
    """Re-rank using cross-encoder for better relevance."""
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    pairs = [[query, doc] for doc in documents]
    scores = model.predict(pairs)

    # Sort by score and take top_k
    ranked_docs = [doc for _, doc in sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True
    )]

    return ranked_docs[:top_k]
```

### 2. Chunk Summarization

**Pattern:** Summarize retrieved chunks before final prompt.

```python
def summarize_then_answer(query: str, documents: list[str]) -> str:
    # Step 1: Summarize each document
    summaries = []
    for doc in documents:
        summary_prompt = f"Summarize key points relevant to '{query}':\n\n{doc}"
        summary = llm.generate(summary_prompt, max_tokens=150)
        summaries.append(summary)

    # Step 2: Answer using summaries
    final_prompt = f"""
    Question: {query}

    Relevant Information:
    {chr(10).join(summaries)}

    Answer:
    """
    return llm.generate(final_prompt)
```

### 3. Hybrid Approach: Full Context + Summaries

**Pattern:** Provide summaries upfront, full text in system message with caching.

```python
from anthropic import Anthropic

client = Anthropic()

def hybrid_context_rag(query: str, documents: list[dict]) -> str:
    # Generate summaries
    summaries = [f"Doc {i+1} Summary: {doc['summary']}" for i, doc in enumerate(documents)]

    # Full context in cached system message
    full_context = "\n\n".join([doc['full_text'] for doc in documents])

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": f"Full document context:\n\n{full_context}",
                "cache_control": {"type": "ephemeral"}  # Cache for 5 minutes
            }
        ],
        messages=[{
            "role": "user",
            "content": f"""
Document Summaries:
{chr(10).join(summaries)}

Question: {query}

Answer using the full document context (check system message for details).
"""
        }]
    )
    return response.content[0].text
```

**Benefits:**
- Summaries guide initial understanding
- Full context available for detailed questions
- Caching reduces cost for follow-up queries

### 4. Sliding Window Context

**Pattern:** For long documents, use sliding windows with overlap.

```python
def sliding_window_rag(query: str, long_document: str, window_size: int = 1000, overlap: int = 200):
    """Process long documents in overlapping windows."""
    windows = []
    start = 0

    while start < len(long_document):
        end = min(start + window_size, len(long_document))
        windows.append(long_document[start:end])
        start += (window_size - overlap)

    # Score each window
    answers = []
    for i, window in enumerate(windows):
        prompt = f"Based on this excerpt, answer: {query}\n\nExcerpt:\n{window}"
        answer = llm.generate(prompt)
        answers.append((answer, i))

    # Synthesize answers
    synthesis_prompt = f"""
Synthesize these answers into a single coherent response:

{chr(10).join([f"Answer {i+1}: {ans}" for ans, i in answers])}

Final Answer:
"""
    return llm.generate(synthesis_prompt)
```

## Chunk Size Considerations

### 1. Optimal Chunk Sizes by Model

**Guidelines:**
- **Small chunks (100-300 tokens):** Better precision, more chunks needed
- **Medium chunks (300-800 tokens):** Balanced precision/recall
- **Large chunks (800-1500 tokens):** Better context, may include irrelevant info

**Model-specific recommendations:**
```python
CHUNK_SIZES = {
    "gpt-4": {
        "default": 512,
        "context_window": 8192,
        "max_chunks": 12  # ~6k tokens for context
    },
    "claude-3-sonnet": {
        "default": 800,
        "context_window": 200000,
        "max_chunks": 50  # Can handle much more context
    },
    "gpt-3.5-turbo": {
        "default": 400,
        "context_window": 4096,
        "max_chunks": 8  # ~3k tokens for context
    }
}
```

### 2. Semantic Chunking

**Pattern:** Split on semantic boundaries, not just token count.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def semantic_chunking(document: str) -> list[str]:
    """Split on paragraph/section boundaries."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        separators=[
            "\n\n\n",  # Section breaks
            "\n\n",    # Paragraph breaks
            "\n",      # Line breaks
            ". ",      # Sentences
            " ",       # Words
        ],
        length_function=len
    )
    return splitter.split_text(document)
```

### 3. Chunk Overlap Strategies

**Pattern:** Maintain context across chunk boundaries.

```python
def chunk_with_overlap(text: str, chunk_size: int = 500, overlap: int = 100) -> list[dict]:
    """Create chunks with overlap and metadata."""
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Find sentence boundary
        if end < len(text):
            last_period = text.rfind('. ', start, end)
            if last_period > start:
                end = last_period + 2

        chunks.append({
            'text': text[start:end],
            'start_pos': start,
            'end_pos': end,
            'chunk_id': len(chunks)
        })

        start = end - overlap

    return chunks
```

**Overlap benefits:**
- Preserves context across boundaries
- Reduces information loss
- Better for questions spanning multiple topics

**Recommended overlap:**
- 10-20% for general documents
- 20-30% for technical documents
- 30-50% for code or structured content

### 4. Dynamic Chunk Sizing

**Pattern:** Adjust chunk size based on document structure.

```python
def adaptive_chunking(document: str, metadata: dict) -> list[str]:
    """Adapt chunk size to document type."""

    if metadata.get('type') == 'code':
        # Larger chunks for code (preserve function/class context)
        chunk_size = 1000
        overlap = 200
    elif metadata.get('type') == 'legal':
        # Smaller chunks for legal (precise citation needed)
        chunk_size = 300
        overlap = 50
    elif metadata.get('type') == 'narrative':
        # Medium chunks for stories/articles
        chunk_size = 600
        overlap = 100
    else:
        # Default
        chunk_size = 512
        overlap = 100

    return chunk_with_overlap(document, chunk_size, overlap)
```

## Prompt Templates for RAG

### Template 1: Basic QA

```python
BASIC_RAG_TEMPLATE = """
Answer the question based solely on the provided context.
If the answer is not in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {query}

Answer:
"""
```

### Template 2: QA with Citations

```python
CITED_RAG_TEMPLATE = """
Answer the question using only the provided documents.
Cite your sources using [Document N] notation.

{documents}

Question: {query}

Answer (with citations):
"""
```

### Template 3: Summarization RAG

```python
SUMMARIZATION_RAG_TEMPLATE = """
Summarize the key information from these documents that relates to the query.

Query: {query}

Documents:
{documents}

Summary (3-5 sentences):
"""
```

### Template 4: Adversarial RAG

```python
ADVERSARIAL_RAG_TEMPLATE = """
Answer the question using the provided context.

CRITICAL RULES:
1. ONLY use information explicitly stated in the context
2. Do NOT use your general knowledge
3. If making any inference, clearly mark it as an inference
4. If the answer is not in the context, say so explicitly

Context:
{context}

Question: {query}

Answer (following all rules):
"""
```

### Template 5: Multi-Hop RAG

```python
MULTI_HOP_TEMPLATE = """
Answer the question by reasoning across multiple documents.

Documents:
{documents}

Question: {query}

Think step-by-step:
1. Identify relevant information in each document
2. Connect information across documents
3. Provide final answer with citations

Response:
"""
```

## Common Pitfalls

### 1. Context Overflow

**Problem:** Too many documents exceed context window.

**Solution:**
```python
def safe_context_injection(query: str, documents: list[str], max_tokens: int = 6000):
    """Add documents until token limit reached."""
    from tiktoken import encoding_for_model

    enc = encoding_for_model("gpt-4")
    context_parts = []
    total_tokens = 0

    for i, doc in enumerate(documents):
        doc_tokens = len(enc.encode(doc))
        if total_tokens + doc_tokens > max_tokens:
            break
        context_parts.append(f"[Document {i+1}]\n{doc}")
        total_tokens += doc_tokens

    return "\n\n".join(context_parts)
```

### 2. Hallucination Despite RAG

**Problem:** Model still hallucinates or uses general knowledge.

**Solution:** Use stronger constraints.

```python
ANTI_HALLUCINATION_PROMPT = """
You are a retrieval system. You can ONLY answer using the exact information below.

STRICT RULES:
- DO NOT use any knowledge from your training
- DO NOT make inferences beyond what is explicitly stated
- If the answer is not in the documents, respond: "This information is not available in the provided documents."

Documents:
{context}

Question: {query}

Answer (must be directly from documents):
"""
```

### 3. Poor Chunk Retrieval

**Problem:** Retrieved chunks don't contain the answer.

**Solutions:**
- Use query expansion (rephrase query multiple ways)
- Implement hybrid search (keyword + semantic)
- Add re-ranking step
- Increase top-k and use re-ranker

```python
def enhanced_retrieval(query: str, vector_db):
    # Query expansion
    expanded_queries = [
        query,
        f"What is {query}?",
        f"Explain {query}",
        f"{query} definition"
    ]

    # Hybrid search
    all_chunks = []
    for q in expanded_queries:
        chunks = vector_db.similarity_search(q, k=5)
        all_chunks.extend(chunks)

    # Deduplicate and re-rank
    unique_chunks = list(set(all_chunks))
    return rerank_documents(query, unique_chunks, top_k=5)
```

### 4. Ignoring Metadata

**Problem:** Treating all sources equally.

**Solution:** Include metadata in prompts.

```python
def metadata_aware_prompt(query: str, chunks: list[dict]) -> str:
    enriched_context = []

    for chunk in chunks:
        enriched_context.append(f"""
Source: {chunk['source']}
Authority: {chunk.get('authority', 'Unknown')}
Date: {chunk.get('date', 'Unknown')}
Relevance Score: {chunk.get('score', 0):.2f}

Content:
{chunk['text']}
---
""")

    return f"""
Answer the question considering source authority and recency.
Prefer authoritative and recent sources.

{chr(10).join(enriched_context)}

Question: {query}

Answer:
"""
```

---

**Related Files:**
- `prompt-chaining.md` - Multi-step RAG workflows
- `structured-outputs.md` - Structured data extraction from RAG
- `examples/rag-complete-example.py` - Full RAG implementation

**Key Takeaways:**
1. Structure context clearly (XML for Claude, numbered for others)
2. Always request citations to reduce hallucination
3. Optimize chunk size for your model and use case
4. Re-rank retrieved documents before LLM call
5. Use prompt caching for repeated context (90% cost savings)
6. Handle conflicts explicitly with source prioritization
7. Monitor context window usage to avoid truncation
