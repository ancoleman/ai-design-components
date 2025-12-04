# Document Chunking Strategies for RAG

Comprehensive guide to chunking documents for optimal retrieval quality in RAG systems.

## Why Chunking Matters

Chunking is the most critical decision for RAG quality. Poor chunking causes:
- Lost context (chunks too small)
- Irrelevant retrieval (chunks too large)
- Information fragmentation (bad split points)
- Poor semantic coherence

**Impact:** Good chunking can improve RAG recall by 20-30%.

## Default Recommendation

**For most RAG systems:**
- **Chunk size:** 512 tokens
- **Overlap:** 50 tokens (10%)
- **Method:** Fixed token-based with recursive splitting

**Why these values:**
- 512 tokens balances context vs precision
- 50 token overlap prevents information loss at boundaries
- Fits within most embedding model limits (8K+ context)

## Chunking Methods

### 1. Fixed Token-Based (Default)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,          # Tokens, not characters
    chunk_overlap=50,
    length_function=len,     # Use tiktoken for accurate token count
    separators=["\n\n", "\n", ". ", " ", ""],  # Try splits in order
)

chunks = splitter.split_text(document_text)
```

**Use when:** General purpose, mixed content types

### 2. Semantic Chunking

```python
from langchain.text_splitter import SemanticChunker
from langchain_voyageai import VoyageAIEmbeddings

semantic_splitter = SemanticChunker(
    embeddings=VoyageAIEmbeddings(model="voyage-3"),
    breakpoint_threshold_type="percentile",  # Split at semantic boundaries
    breakpoint_threshold_amount=90,           # Top 10% similarity drops
)

chunks = semantic_splitter.split_text(document_text)
```

**Use when:** Narrative content (articles, books), need semantic coherence
**Trade-off:** Slower (requires embeddings), variable chunk sizes

### 3. Code-Aware Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python",       # python, javascript, rust, go, etc.
    chunk_size=512,
    chunk_overlap=50,
)

chunks = code_splitter.split_text(source_code)
```

**Splits on:**
- Function/class boundaries
- Logical blocks (if/for/while)
- Comment sections
- Import statements

**Use when:** Code documentation, API references, technical docs

### 4. Markdown-Aware Chunking

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
    ]
)

chunks = markdown_splitter.split_text(markdown_text)
```

**Use when:** Markdown documentation, README files, blog posts

### 5. Sentence-Based Chunking

```python
import nltk
nltk.download('punkt')

from langchain.text_splitter import NLTKTextSplitter

sentence_splitter = NLTKTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
)

chunks = sentence_splitter.split_text(text)
```

**Use when:** Need to preserve sentence boundaries, conversational content

## Content-Type Specific Strategies

### API Documentation

```python
# Chunk by endpoint + method
# Include endpoint metadata in each chunk
chunk_metadata = {
    "endpoint": "/api/users",
    "method": "POST",
    "section": "Authentication",
}
```

**Chunk size:** 256-512 tokens (API docs are dense)
**Split on:** Endpoint boundaries, parameter sections

### Research Papers (PDF)

```python
# Chunk by section hierarchy
# Preserve abstract, introduction, methods separately
chunk_metadata = {
    "section": "Methods",
    "page": 5,
    "paper_title": "...",
}
```

**Chunk size:** 512-1024 tokens (academic writing needs context)
**Split on:** Section headers, paragraph boundaries

### Chat Logs / Conversations

```python
# Chunk by conversation turn or time window
# Include speaker metadata
chunk_metadata = {
    "speaker": "user_123",
    "timestamp": "2025-12-03T10:00:00Z",
    "conversation_id": "conv_456",
}
```

**Chunk size:** 256-512 tokens
**Split on:** Speaker turns, time windows (5-10 messages)

### Code Repositories

```python
# Chunk by file or function
chunk_metadata = {
    "file_path": "src/api/users.py",
    "function": "create_user",
    "language": "python",
}
```

**Chunk size:** 256-512 tokens (functions are self-contained)
**Split on:** Function/class boundaries, file boundaries for small files

## Advanced Chunking Patterns

### Sliding Window

```python
def sliding_window_chunks(text, window_size=512, stride=256):
    """Create overlapping chunks with sliding window"""
    chunks = []
    for i in range(0, len(text), stride):
        chunk = text[i:i + window_size]
        if len(chunk) < window_size / 2:  # Skip small final chunk
            break
        chunks.append(chunk)
    return chunks
```

**Use when:** Dense documents where context is critical
**Trade-off:** More chunks = higher storage and query costs

### Parent-Child Chunking

```python
# Store both small chunks (for retrieval) and large parent chunks (for context)
small_chunks = split_text(document, chunk_size=128)
large_chunks = split_text(document, chunk_size=512)

# Retrieve small, return large
for small_chunk in retrieved_chunks:
    parent_chunk = find_parent_chunk(small_chunk)
    context.append(parent_chunk)
```

**Use when:** Need precise retrieval but broad context
**Trade-off:** Complex indexing, higher storage

### Contextual Compression

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Retrieve large chunks, compress to relevant portions
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_store.as_retriever(),
)
```

**Use when:** Want to reduce irrelevant content in context
**Trade-off:** Extra LLM call per query

## Chunking Strategy Decision Tree

```
CONTENT TYPE?
├─ CODE
│  └─ Code-aware chunking (256-512 tokens, split on functions)
│
├─ STRUCTURED DOCS (Markdown, API docs)
│  └─ Header/section-based (256-512 tokens)
│
├─ NARRATIVE (Articles, books)
│  └─ Semantic chunking (variable size, meaning-based)
│
├─ CONVERSATIONAL (Chat logs)
│  └─ Turn-based or time-window (256-512 tokens)
│
└─ MIXED CONTENT
   └─ Fixed token with overlap (512 tokens, 50 overlap)
```

## Chunking Metadata

**Essential metadata for production:**
```python
chunk_metadata = {
    # Source tracking
    "source": "docs/api-reference.md",
    "source_type": "documentation",
    "last_updated": "2025-12-03",

    # Hierarchical context
    "section": "Authentication",
    "subsection": "OAuth 2.1",
    "heading_hierarchy": ["API", "Auth", "OAuth 2.1"],

    # Chunking info
    "chunk_index": 3,
    "total_chunks": 12,
    "chunk_method": "fixed_token",

    # Content classification
    "content_type": "code_example",
    "programming_language": "python",
}
```

## Validation and Testing

### Test Chunk Quality

```python
def validate_chunks(chunks: List[str]) -> Dict:
    """Validate chunk quality"""
    stats = {
        "total_chunks": len(chunks),
        "avg_length": sum(len(c) for c in chunks) / len(chunks),
        "min_length": min(len(c) for c in chunks),
        "max_length": max(len(c) for c in chunks),
        "empty_chunks": sum(1 for c in chunks if not c.strip()),
    }

    # Check for issues
    issues = []
    if stats["empty_chunks"] > 0:
        issues.append(f"{stats['empty_chunks']} empty chunks")
    if stats["min_length"] < 50:
        issues.append("Very small chunks detected")
    if stats["max_length"] > 2000:
        issues.append("Very large chunks detected")

    return {"stats": stats, "issues": issues}
```

### Evaluate Retrieval Quality

```python
from ragas.metrics import context_recall

# Test if chunking preserves retrievable information
test_data = {
    "question": ["How do I refresh OAuth tokens?"],
    "contexts": [retrieved_chunks],
    "ground_truth": ["Full answer from original doc"],
}

result = evaluate(test_data, metrics=[context_recall])
# Target: >0.80 recall
```

## Common Pitfalls

**❌ Chunking by character count instead of tokens**
```python
# Wrong: Characters != tokens
chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]

# Right: Use token-aware splitting
import tiktoken
tokenizer = tiktoken.get_encoding("cl100k_base")
```

**❌ No overlap between chunks**
```python
# Loses information at boundaries
chunks = split_text(text, chunk_size=512, chunk_overlap=0)

# Better: 10% overlap
chunks = split_text(text, chunk_size=512, chunk_overlap=50)
```

**❌ One-size-fits-all chunking**
```python
# Code and prose need different strategies
chunks = split_text(mixed_content, chunk_size=512)  # Suboptimal

# Better: Detect content type and adjust
if is_code(content):
    chunks = code_aware_split(content)
else:
    chunks = semantic_split(content)
```

## Best Practices

1. **Start with 512/50** - Optimize later based on metrics
2. **Measure retrieval quality** - Use RAGAS context_recall
3. **Preserve hierarchy** - Include heading paths in metadata
4. **Test edge cases** - Very long docs, mixed content
5. **Monitor chunk sizes** - Track distribution over time
6. **A/B test strategies** - Compare retrieval quality
7. **Document your choice** - Explain why you chose specific parameters
8. **Version your chunking** - Re-chunk if strategy changes

## Resources

- LangChain Text Splitters: https://python.langchain.com/docs/modules/data_connection/document_transformers/
- Semantic Chunking Paper: https://arxiv.org/abs/2312.06648
- LTTB Downsampling: https://github.com/sveinn-steinarsson/flot-downsample
