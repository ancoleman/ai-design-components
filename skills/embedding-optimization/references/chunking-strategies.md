# Chunking Strategies for Embedding Optimization

Comprehensive guide to text chunking strategies for optimal embedding quality and retrieval performance.

## Table of Contents

1. [Chunking Fundamentals](#chunking-fundamentals)
2. [Chunking Methods](#chunking-methods)
3. [Content-Type Specific Strategies](#content-type-specific-strategies)
4. [Chunk Size Selection](#chunk-size-selection)
5. [Overlap Strategies](#overlap-strategies)
6. [Implementation Patterns](#implementation-patterns)

## Chunking Fundamentals

### Why Chunking Matters

**Problem:** Embedding models have context limits (512-8,192 tokens)
- Documents often exceed these limits
- Long texts dilute semantic information
- Retrieval precision decreases with large chunks

**Solution:** Split documents into semantically coherent chunks
- Each chunk fits within embedding context window
- Preserves semantic boundaries (paragraphs, sections, functions)
- Overlap prevents context loss at boundaries

### Chunk Quality Metrics

**Good Chunks:**
- Self-contained (understandable without surrounding context)
- Semantically coherent (single topic or concept)
- Optimal size (500-1,500 characters for most content)
- Preserve natural boundaries (paragraphs, sections, functions)

**Bad Chunks:**
- Split mid-sentence or mid-paragraph
- Orphaned context (references without definitions)
- Too small (incomplete information)
- Too large (multiple unrelated topics)

### Chunk Size Impact on Retrieval

**Small Chunks (200-500 chars):**
- **Pros:** Precise retrieval, less noise, faster search
- **Cons:** Context loss, may miss relevant information
- **Best For:** Q&A systems, fact retrieval

**Medium Chunks (500-1,000 chars):**
- **Pros:** Balance precision and context, general purpose
- **Cons:** May still split related content
- **Best For:** Documentation, blog posts, general RAG

**Large Chunks (1,000-2,000 chars):**
- **Pros:** Maximum context, preserves relationships
- **Cons:** Slower search, more noise in results
- **Best For:** Legal documents, technical papers, summarization

## Chunking Methods

### Method 1: Fixed-Size Chunking

**Description:** Split text into chunks of fixed character/token count.

**Advantages:**
- Simple to implement
- Predictable chunk sizes
- Fast processing

**Disadvantages:**
- Ignores semantic boundaries
- May split sentences, paragraphs mid-thought
- Orphaned context

**Implementation:**
```python
def fixed_chunk(text, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```

**Use Cases:**
- Uniform content (chat logs, transcripts)
- Quick prototyping
- When content structure is unknown

### Method 2: Recursive Chunking

**Description:** Hierarchical splitting using ordered separators (paragraphs → sentences → words).

**Advantages:**
- Respects natural boundaries
- Content-aware (markdown headings, code functions)
- Configurable separators for different content types

**Disadvantages:**
- More complex implementation
- Requires content-type detection

**Implementation:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def recursive_chunk(text, content_type='markdown', chunk_size=800, overlap=100):
    separators = {
        'markdown': ['\n## ', '\n### ', '\n\n', '\n', ' '],
        'code': ['\nclass ', '\ndef ', '\n\n', '\n'],
        'text': ['\n\n', '\n', '. ', ' ']
    }

    splitter = RecursiveCharacterTextSplitter(
        separators=separators.get(content_type, separators['text']),
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    return splitter.split_text(text)
```

**Use Cases:**
- Documentation (heading structure)
- Code (function/class boundaries)
- Structured content (markdown, HTML)

### Method 3: Semantic Chunking

**Description:** Split based on semantic similarity changes between sentences.

**Advantages:**
- Preserves semantic coherence
- Natural topic boundaries
- High retrieval quality

**Disadvantages:**
- Computationally expensive (requires sentence embeddings)
- Variable chunk sizes
- Complex implementation

**Implementation Concept:**
```python
def semantic_chunk(text, similarity_threshold=0.7):
    sentences = split_into_sentences(text)
    embeddings = embed_sentences(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        similarity = cosine_similarity(embeddings[i-1], embeddings[i])

        if similarity > similarity_threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentences[i]]

    chunks.append(' '.join(current_chunk))
    return chunks
```

**Use Cases:**
- Long-form content with topic shifts
- Academic papers
- News articles

### Method 4: Sliding Window

**Description:** Fixed-size chunks with large overlap (50%+).

**Advantages:**
- No context loss at boundaries
- Multiple perspectives on same content
- Good for precise retrieval

**Disadvantages:**
- High storage overhead (2x+ chunks)
- Duplicate information
- Slower search

**Implementation:**
```python
def sliding_window_chunk(text, window_size=500, stride=250):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + window_size, len(text))
        chunks.append(text[start:end])
        start += stride
    return chunks
```

**Use Cases:**
- Critical applications (legal, medical)
- When missing information is costly
- Short queries requiring precise matches

## Content-Type Specific Strategies

### Documentation (Markdown, HTML)

**Characteristics:**
- Hierarchical structure (headings)
- Self-contained sections
- Mixed text and code examples

**Recommended Strategy:** Recursive (heading-aware)

**Configuration:**
```python
RecursiveCharacterTextSplitter(
    separators=['\n## ', '\n### ', '\n#### ', '\n\n', '\n', ' '],
    chunk_size=800,
    chunk_overlap=100
)
```

**Chunk Size Reasoning:**
- 800 characters ≈ 1-2 paragraphs
- Preserves section context
- Small enough for precise retrieval

**Example:**
```markdown
## Installation

To install the package:
```bash
pip install mypackage
```

## Usage

Import and use:
```python
from mypackage import feature
```

# Split into 2 chunks:
# Chunk 1: Installation section (complete)
# Chunk 2: Usage section (complete)
```

### Code (Python, JavaScript, etc.)

**Characteristics:**
- Function/class boundaries
- Logical units (complete functions)
- Comments and docstrings

**Recommended Strategy:** Recursive (language-aware)

**Configuration:**
```python
# Python
RecursiveCharacterTextSplitter(
    separators=['\nclass ', '\ndef ', '\n\n', '\n', ' '],
    chunk_size=1000,
    chunk_overlap=100
)

# JavaScript
RecursiveCharacterTextSplitter(
    separators=['\nfunction ', '\nclass ', '\nconst ', '\n\n', '\n', ' '],
    chunk_size=1000,
    chunk_overlap=100
)
```

**Chunk Size Reasoning:**
- 1,000 characters ≈ 1 complete function
- Preserves full function context
- Includes docstrings and comments

**Example:**
```python
def calculate_total(items):
    """Calculate total price."""
    return sum(item.price for item in items)

def apply_discount(total, discount_pct):
    """Apply discount to total."""
    return total * (1 - discount_pct / 100)

# Split into 2 chunks (one function per chunk)
```

### Q&A / FAQ Content

**Characteristics:**
- Question-answer pairs
- Self-contained entries
- Short, precise information

**Recommended Strategy:** Fixed-size (small chunks)

**Configuration:**
```python
RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', '. ', ' '],
    chunk_size=500,
    chunk_overlap=50
)
```

**Chunk Size Reasoning:**
- 500 characters ≈ 1 Q&A pair
- Precise retrieval (return exact answer)
- Minimal overlap needed

**Example:**
```
Q: What is the capital of France?
A: The capital of France is Paris.

Q: When was the Eiffel Tower built?
A: The Eiffel Tower was built in 1889.

# Split into 2 chunks (one Q&A per chunk)
```

### Legal / Technical Documents

**Characteristics:**
- Dense information
- Context-critical (references to earlier sections)
- Formal structure (clauses, sections)

**Recommended Strategy:** Semantic or large recursive chunks

**Configuration:**
```python
RecursiveCharacterTextSplitter(
    separators=['\n\n', '. ', ' '],
    chunk_size=1500,
    chunk_overlap=200
)
```

**Chunk Size Reasoning:**
- 1,500 characters ≈ 1-2 paragraphs
- Large overlap (200) prevents context loss
- Preserves clause relationships

**Example:**
```
Section 3.1: Definitions

For purposes of this agreement:
(a) "Service" means the software service provided...
(b) "User" means any person accessing...

Section 3.2: Grant of Rights

Subject to Section 3.1, the Company grants...

# Chunk 1: Section 3.1 (complete definitions)
# Chunk 2: Section 3.1(b) + Section 3.2 (overlap includes context)
```

### Blog Posts / Articles

**Characteristics:**
- Paragraph-based structure
- Topic flow
- Conversational tone

**Recommended Strategy:** Semantic or paragraph-aware recursive

**Configuration:**
```python
RecursiveCharacterTextSplitter(
    separators=['\n\n', '. ', ' '],
    chunk_size=1000,
    chunk_overlap=100
)
```

**Chunk Size Reasoning:**
- 1,000 characters ≈ 1-2 paragraphs
- Natural paragraph boundaries
- Good balance of context and precision

### Chat Transcripts / Conversations

**Characteristics:**
- Turn-based structure (user/assistant)
- Time-ordered
- Varying message lengths

**Recommended Strategy:** Fixed-size with time-based splitting

**Configuration:**
```python
# Custom: Split on speaker changes, then chunk if too large
def chunk_conversation(messages, max_chunk_size=800):
    chunks = []
    current_chunk = []
    current_size = 0

    for msg in messages:
        msg_size = len(msg['content'])
        if current_size + msg_size > max_chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0

        current_chunk.append(msg)
        current_size += msg_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
```

**Chunk Size Reasoning:**
- 800 characters ≈ 2-4 chat turns
- Preserves conversation flow
- Time-based context

### Academic Papers

**Characteristics:**
- Structured sections (Abstract, Introduction, Methods, Results)
- Citations and references
- Figures and tables

**Recommended Strategy:** Recursive (section-aware)

**Configuration:**
```python
RecursiveCharacterTextSplitter(
    separators=['\n## ', '\n### ', '\n\n', '. ', ' '],
    chunk_size=1200,
    chunk_overlap=150
)
```

**Chunk Size Reasoning:**
- 1,200 characters ≈ 1 subsection or 2-3 paragraphs
- Preserves logical structure
- Large enough for context, small enough for precision

## Chunk Size Selection

### Token vs. Character Count

**Character Count (Simpler):**
- Fast calculation: `len(text)`
- Approximation: 1 token ≈ 4 characters
- Use for quick estimates

**Token Count (Accurate):**
- Use tokenizer: `tiktoken` (OpenAI), model-specific tokenizers
- Exact for embedding model limits
- Slower but precise

**Recommendation:** Use character count during chunking, validate token count before embedding.

### Chunk Size Decision Matrix

| Content Type | Recommended Size (chars) | Token Estimate | Reasoning |
|-------------|------------------------|----------------|-----------|
| Q&A / FAQ | 500 | ~125 | Single question-answer pair |
| Code Snippets | 1,000 | ~250 | Complete function |
| Documentation | 800 | ~200 | 1-2 paragraphs, section-level |
| Blog Posts | 1,000 | ~250 | 1-2 paragraphs |
| Legal | 1,500 | ~375 | Context-critical, larger chunks |
| Academic Papers | 1,200 | ~300 | Subsection or 2-3 paragraphs |
| Chat Logs | 800 | ~200 | 2-4 conversation turns |
| News Articles | 1,000 | ~250 | 1-2 paragraphs |

### Embedding Model Context Limits

| Model | Max Tokens | Recommended Chunk Size (tokens) | Character Estimate |
|-------|-----------|-------------------------------|-------------------|
| text-embedding-3-small | 8,191 | 200-400 | 800-1,600 |
| text-embedding-3-large | 8,191 | 200-400 | 800-1,600 |
| all-MiniLM-L6-v2 | 512 | 100-250 | 400-1,000 |
| BGE-base-en-v1.5 | 512 | 100-250 | 400-1,000 |

**Note:** Shorter chunks (200-400 tokens) improve retrieval precision even when model supports 8K+ tokens.

## Overlap Strategies

### Why Overlap Matters

**Problem:** Information at chunk boundaries can be lost or fragmented.

**Example (Without Overlap):**
```
Chunk 1: "...the product was launched in"
Chunk 2: "2019 and achieved great success..."
```
→ Neither chunk contains complete information about the launch year.

**Solution (With 100-character Overlap):**
```
Chunk 1: "...the product was launched in 2019 and achieved"
Chunk 2: "was launched in 2019 and achieved great success..."
```
→ Both chunks contain the complete fact.

### Overlap Size Guidelines

| Chunk Size | Recommended Overlap | Overlap % | Reasoning |
|-----------|-------------------|----------|-----------|
| 500 | 50 | 10% | Minimal context preservation |
| 800 | 100 | 12.5% | Standard for documentation |
| 1,000 | 100-150 | 10-15% | Balanced context/storage |
| 1,500 | 200 | 13% | High-context content (legal) |
| 2,000 | 200-300 | 10-15% | Maximum context preservation |

**General Rule:** 10-20% overlap is optimal for most content.

### Trade-offs

**Small Overlap (5-10%):**
- **Pros:** Lower storage costs, fewer duplicate chunks
- **Cons:** Risk of context loss at boundaries
- **Use When:** Storage-constrained, low-context content

**Medium Overlap (10-20%):**
- **Pros:** Good balance, minimal context loss
- **Cons:** Modest storage increase (10-20%)
- **Use When:** General purpose RAG, documentation

**Large Overlap (30-50%):**
- **Pros:** Maximum context preservation, sliding window
- **Cons:** High storage overhead (2x+), duplicate info
- **Use When:** Critical applications (legal, medical)

## Implementation Patterns

### Pattern 1: Simple Fixed-Size

```python
from langchain.text_splitter import CharacterTextSplitter

def chunk_simple(text, chunk_size=1000, overlap=100):
    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separator='\n\n'
    )
    return splitter.split_text(text)
```

**Use For:** Quick prototyping, uniform content.

### Pattern 2: Recursive with Metadata

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_with_metadata(text, content_type='markdown', chunk_size=800, overlap=100, metadata=None):
    separators = {
        'markdown': ['\n## ', '\n### ', '\n\n', '\n'],
        'code': ['\nclass ', '\ndef ', '\n\n', '\n'],
        'text': ['\n\n', '\n', '. ', ' ']
    }

    splitter = RecursiveCharacterTextSplitter(
        separators=separators.get(content_type, separators['text']),
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    chunks = splitter.split_text(text)

    # Attach metadata to each chunk
    result = []
    for i, chunk in enumerate(chunks):
        chunk_meta = metadata.copy() if metadata else {}
        chunk_meta.update({
            'chunk_index': i,
            'total_chunks': len(chunks),
            'chunk_size': len(chunk)
        })
        result.append({'text': chunk, 'metadata': chunk_meta})

    return result
```

**Use For:** Production systems, tracking chunk provenance.

### Pattern 3: Content-Type Detection

```python
def detect_content_type(text):
    """Auto-detect content type for optimal chunking."""

    # Check for code
    if 'def ' in text or 'function ' in text or 'class ' in text:
        return 'code'

    # Check for markdown
    if '# ' in text or '## ' in text:
        return 'markdown'

    # Default to plaintext
    return 'text'

def chunk_auto(text, chunk_size=1000, overlap=100):
    content_type = detect_content_type(text)
    return chunk_with_metadata(text, content_type, chunk_size, overlap)
```

**Use For:** Mixed content, automated pipelines.

### Pattern 4: Validation and Quality Check

```python
def validate_chunks(chunks, min_size=100, max_size=2000):
    """Validate chunk quality."""
    issues = []

    for i, chunk in enumerate(chunks):
        # Check size
        if len(chunk) < min_size:
            issues.append(f"Chunk {i} too small: {len(chunk)} chars")
        if len(chunk) > max_size:
            issues.append(f"Chunk {i} too large: {len(chunk)} chars")

        # Check completeness (not mid-word)
        if chunk and not chunk[-1].isspace() and not chunk[-1] in '.!?':
            issues.append(f"Chunk {i} may be incomplete (ends mid-word)")

    return issues

# Usage
chunks = chunk_auto(text)
issues = validate_chunks(chunks)
if issues:
    print("Chunking quality issues:", issues)
```

**Use For:** Quality assurance, production pipelines.

## Chunking Checklist

Before finalizing chunking strategy:

**Content Analysis:**
- [ ] Identified content type (code, docs, legal, etc.)
- [ ] Analyzed structure (headings, paragraphs, functions)
- [ ] Determined optimal chunk size (500-1,500 chars)
- [ ] Selected appropriate overlap (10-20%)

**Strategy Selection:**
- [ ] Chose chunking method (fixed, recursive, semantic)
- [ ] Configured separators for content type
- [ ] Validated chunk sizes (not too small/large)
- [ ] Tested on sample documents

**Quality Validation:**
- [ ] Chunks are self-contained
- [ ] No mid-sentence splits
- [ ] Overlap prevents context loss
- [ ] Metadata attached (source, index, etc.)

**Performance:**
- [ ] Chunk count manageable (not millions for small corpus)
- [ ] Average chunk size consistent
- [ ] Retrieval tested on sample queries
- [ ] Quality metrics tracked (precision, recall)
