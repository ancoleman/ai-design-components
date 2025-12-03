# Document Chunking Strategies for RAG

## Overview

Chunking splits long documents into smaller pieces that fit within embedding model context windows and provide focused semantic meaning for retrieval.

**Core principle:** Balance between context (larger chunks) and precision (smaller chunks).

## Default Strategy (Works for 80% of Cases)

```python
CHUNK_SIZE = 512  # tokens, not characters
CHUNK_OVERLAP = 50  # tokens (10% overlap)
```

**Why these numbers?**
- **512 tokens:** Sweet spot between context and precision
  - Too small (128-256): Fragments concepts, loses context
  - Too large (1024-2048): Dilutes relevance, wastes LLM tokens
- **50 token overlap:** Ensures sentences/paragraphs aren't split awkwardly

## Chunking by Content Type

| Content Type | Chunk Size | Overlap | Strategy | Example |
|--------------|------------|---------|----------|---------|
| **Technical Docs** | 512 tokens | 50 tokens | Semantic (by section) | API reference, tutorials |
| **Code Files** | 100-200 lines | Function boundaries | AST-based | Python, JavaScript, Rust |
| **Long Articles** | 768 tokens | 100 tokens | Paragraph-aware | Blog posts, whitepapers |
| **Chat Logs** | 256 tokens | 20 tokens | Turn-based | Customer support, Slack |
| **Legal Docs** | 1024 tokens | 150 tokens | Clause-based | Contracts, policies |
| **API Logs (JSON)** | 512 tokens | 0 tokens | Structure-preserving | Request/response pairs |
| **Emails** | 384 tokens | 40 tokens | Thread-aware | Email conversations |
| **PDFs (scanned)** | 512 tokens | 100 tokens | Page-aware | Research papers, reports |

## Implementation Strategies

### 1. Recursive Character Splitting (General Purpose)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

# Token counting function (OpenAI tokenizer)
def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

# Create splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", ". ", " ", ""]  # Try in order
)

# Split documents
chunks = splitter.split_text(document)
```

**How it works:**
1. Try splitting on `\n\n` (paragraphs)
2. If chunks still too large, try `\n` (lines)
3. Then `. ` (sentences)
4. Then ` ` (words)
5. Finally split by character

**Best for:**
- General text documents
- Unknown/mixed content types
- Markdown files
- README files

### 2. Semantic Chunking (Intelligent Boundaries)

```python
from langchain.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",  # or "standard_deviation"
    breakpoint_threshold_amount=95  # Top 5% semantic differences
)

chunks = splitter.split_text(document)
```

**How it works:**
1. Generates embeddings for sentences
2. Computes similarity between consecutive sentences
3. Splits where similarity drops significantly (semantic shift)

**Best for:**
- Structured documentation
- Technical articles with clear sections
- Content with logical flow
- When preserving semantic coherence is critical

**Trade-off:** Slower (generates embeddings for splitting), but better quality.

### 3. Code-Aware Chunking (AST-Based)

```python
from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Python code splitter
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=200,  # lines of code
    chunk_overlap=0   # Don't split functions
)

chunks = python_splitter.split_text(python_code)

# Supported languages
# Language.PYTHON, .JS, .TS, .JAVA, .CPP, .GO, .RUST, .RUBY, etc.
```

**Separators for Python:**
```python
[
    "\nclass ",      # Class definitions
    "\ndef ",       # Function definitions
    "\n\tdef ",     # Indented methods
    "\n\n",         # Blank lines
    "\n",           # Lines
    " ",            # Spaces
]
```

**Best for:**
- Code search
- Documentation generation
- Code analysis RAG systems

### 4. Markdown-Aware Chunking

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Split by headers
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

md_chunks = markdown_splitter.split_text(markdown_document)

# Then apply recursive splitting to long sections
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
final_chunks = text_splitter.split_documents(md_chunks)
```

**Best for:**
- Documentation sites
- GitHub README files
- Technical blogs
- Preserving document hierarchy

### 5. Fixed-Size Chunking (Simple, Fast)

```python
def fixed_size_chunks(text, chunk_size=512, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks
```

**Best for:**
- Prototyping
- Uniform content (chat logs, logs)
- When speed matters more than quality

**Drawbacks:**
- May split sentences/paragraphs awkwardly
- Doesn't respect semantic boundaries

## Advanced Patterns

### Hierarchical Chunking (Parent-Child)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Parent chunks (large context)
parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2048,
    chunk_overlap=200
)

# Child chunks (for retrieval)
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)

# Create hierarchy
parent_chunks = parent_splitter.split_text(document)
all_child_chunks = []

for parent in parent_chunks:
    child_chunks = child_splitter.split_text(parent)
    for child in child_chunks:
        all_child_chunks.append({
            "child_text": child,
            "parent_text": parent  # Store parent for context expansion
        })

# Retrieve child, return parent to LLM
# This gives precise retrieval + full context
```

**Benefits:**
- Retrieve with precision (small chunks)
- Provide LLM with full context (large chunks)
- Best of both worlds

**Use case:** Complex technical documentation where context is critical.

### Sliding Window Chunking

```python
def sliding_window_chunks(text, window_size=512, step_size=256):
    words = text.split()
    chunks = []

    for i in range(0, len(words), step_size):
        chunk = " ".join(words[i:i + window_size])
        chunks.append(chunk)
        if i + window_size >= len(words):
            break

    return chunks
```

**When to use:**
- Need high overlap for dense coverage
- Content has critical information at unpredictable locations
- Willing to trade storage for retrieval quality

### Sentence-Based Chunking

```python
from langchain.text_splitter import SentenceTransformersTokenTextSplitter

splitter = SentenceTransformersTokenTextSplitter(
    chunk_overlap=50,
    tokens_per_chunk=512
)

chunks = splitter.split_text(document)
```

**Best for:**
- Preserving sentence boundaries
- Natural language text
- When readability matters

## Metadata Enrichment During Chunking

```python
def chunk_with_metadata(document, source, section):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        length_function=tiktoken_len
    )

    chunks = splitter.split_text(document)

    # Enrich with metadata
    enriched_chunks = []
    for idx, chunk in enumerate(chunks):
        enriched_chunks.append({
            "text": chunk,
            "source": source,
            "section": section,
            "chunk_index": idx,
            "total_chunks": len(chunks),
            "has_code": "```" in chunk,
            "char_count": len(chunk),
            "token_count": tiktoken_len(chunk)
        })

    return enriched_chunks
```

## Chunking PDFs

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load()

# Chunk with page context
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)

all_chunks = []
for page in pages:
    chunks = splitter.split_text(page.page_content)
    for chunk in chunks:
        all_chunks.append({
            "text": chunk,
            "page_number": page.metadata['page'],
            "source": "document.pdf"
        })
```

## Chunking for Different RAG Patterns

### Extractive QA (Precise Answers)
- **Chunk size:** 256-384 tokens
- **Overlap:** 30-50 tokens
- **Strategy:** Sentence-based
- **Goal:** Find exact answer location

### Conversational RAG (Context Understanding)
- **Chunk size:** 512-768 tokens
- **Overlap:** 50-100 tokens
- **Strategy:** Semantic chunking
- **Goal:** Provide conversational context

### Summarization
- **Chunk size:** 1024-2048 tokens
- **Overlap:** 100-200 tokens
- **Strategy:** Hierarchical (parent-child)
- **Goal:** Capture full context for summaries

### Code Search
- **Chunk size:** 100-200 lines
- **Overlap:** 0 (function boundaries)
- **Strategy:** AST-based
- **Goal:** Preserve code structure

## Evaluating Chunking Quality

```python
def evaluate_chunks(chunks):
    """Evaluate chunking quality metrics."""
    metrics = {
        "total_chunks": len(chunks),
        "avg_length": sum(len(c) for c in chunks) / len(chunks),
        "min_length": min(len(c) for c in chunks),
        "max_length": max(len(c) for c in chunks),
        "std_dev": np.std([len(c) for c in chunks])
    }
    return metrics

# Good chunking: Low std_dev (uniform sizes)
# Bad chunking: High std_dev (inconsistent)
```

## Common Mistakes to Avoid

### 1. Using Character Count Instead of Tokens
```python
# ❌ BAD: Character count
splitter = RecursiveCharacterTextSplitter(chunk_size=2000)  # 2000 chars

# ✅ GOOD: Token count
def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    return len(tokenizer.encode(text))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,  # 512 tokens
    length_function=tiktoken_len
)
```

### 2. No Overlap
```python
# ❌ BAD: No overlap, may split sentences
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)

# ✅ GOOD: 10% overlap
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
```

### 3. Ignoring Content Structure
```python
# ❌ BAD: Treat code like prose
general_splitter.split_text(python_code)

# ✅ GOOD: Use language-specific splitter
python_splitter = RecursiveCharacterTextSplitter.from_language(Language.PYTHON)
python_splitter.split_text(python_code)
```

### 4. Chunks Too Large
```python
# ❌ BAD: Chunks too large, dilutes relevance
splitter = RecursiveCharacterTextSplitter(chunk_size=2048)

# ✅ GOOD: 512 tokens balances context and precision
splitter = RecursiveCharacterTextSplitter(chunk_size=512)
```

## Performance Optimization

### Parallel Chunking

```python
from concurrent.futures import ThreadPoolExecutor

def chunk_document(doc):
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    return splitter.split_text(doc)

# Process multiple documents in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    all_chunks = list(executor.map(chunk_document, documents))
```

### Caching Chunked Documents

```python
import hashlib
import pickle

def get_cached_chunks(document, cache_dir="chunk_cache"):
    # Hash document content
    doc_hash = hashlib.sha256(document.encode()).hexdigest()
    cache_path = f"{cache_dir}/{doc_hash}.pkl"

    # Check cache
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            return pickle.load(f)

    # Chunk and cache
    chunks = chunk_document(document)
    with open(cache_path, 'wb') as f:
        pickle.dump(chunks, f)

    return chunks
```

## Production Checklist

- [ ] Use token count, not character count
- [ ] Apply 10% overlap (50 tokens for 512 chunk size)
- [ ] Choose strategy based on content type
- [ ] Enrich chunks with metadata (source, section, index)
- [ ] Test chunking with sample documents
- [ ] Validate chunk sizes (min, max, avg)
- [ ] Consider hierarchical chunking for complex docs
- [ ] Cache chunked documents for efficiency
- [ ] Monitor chunk quality over time
- [ ] Document chunking strategy for the team

## Additional Resources

- **LangChain Text Splitters:** https://python.langchain.com/docs/modules/data_connection/document_transformers/
- **Chunking Strategies Guide:** https://www.pinecone.io/learn/chunking-strategies/
- **RAG Chunking Best Practices:** https://docs.anthropic.com/en/docs/build-with-claude/rag
