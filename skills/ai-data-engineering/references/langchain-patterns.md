# LangChain 0.3+ Implementation Patterns

Production patterns for LangChain-based RAG pipelines and LLM orchestration.

## Table of Contents

- [Overview](#overview)
- [LangChain Architecture](#langchain-architecture)
- [RAG Patterns](#rag-patterns)
- [Chain Patterns](#chain-patterns)
- [Agent Patterns](#agent-patterns)
- [Tool Integration](#tool-integration)
- [Production Best Practices](#production-best-practices)

## Overview

**Context7 Library ID:** `/websites/langchain_oss_python_langchain` (Trust: High, Snippets: 435)

LangChain 0.3+ introduces significant performance improvements and better composability through the LCEL (LangChain Expression Language) syntax.

**Key Changes in 0.3+:**
- Unified chain syntax with `|` operator
- Better streaming support
- Improved error handling
- Async-first design
- Modular imports (langchain-core, langchain-openai, etc.)

## LangChain Architecture

### Module Structure (0.3+)

```
langchain-core          # Core abstractions
langchain-openai        # OpenAI integration
langchain-anthropic     # Anthropic/Claude integration
langchain-voyageai      # Voyage AI embeddings
langchain-qdrant        # Qdrant vector store
langchain-postgres      # PostgreSQL/pgvector
langchain-community     # Community integrations
```

**Install only what you need:**

```bash
# Minimal RAG setup
pip install langchain-core langchain-openai langchain-qdrant

# Full RAG with Voyage AI
pip install langchain-core langchain-openai langchain-voyageai langchain-qdrant

# Anthropic/Claude
pip install langchain-core langchain-anthropic langchain-qdrant
```

## RAG Patterns

### Pattern 1: Basic RAG Chain

Simplest production RAG implementation:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_voyageai import VoyageAIEmbeddings

# Setup vector store
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name="docs",
    embedding=VoyageAIEmbeddings(model="voyage-3")
)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Prompt template
template = """Answer the question based only on the following context:

{context}

Question: {question}

If the answer is not in the context, say "I don't have enough information to answer this question."
"""
prompt = ChatPromptTemplate.from_template(template)

# LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

# Build chain using LCEL
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Invoke
answer = chain.invoke("What is machine learning?")
```

### Pattern 2: Streaming RAG

Essential for production UX:

```python
# Same setup as above, then:

# Streaming invocation
for chunk in chain.stream("What is machine learning?"):
    print(chunk, end="", flush=True)
```

### Pattern 3: RAG with Sources

Return citations to source documents:

```python
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import ChatOpenAI

chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o"),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

result = chain({"question": "What is machine learning?"})

print(f"Answer: {result['answer']}")
print("\nSources:")
for doc in result['source_documents']:
    print(f"- {doc.metadata['source']} (page {doc.metadata.get('page', 'N/A')})")
```

### Pattern 4: Hybrid Search (Vector + BM25)

Combine semantic and keyword search:

```python
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever
from langchain_qdrant import QdrantVectorStore

# Vector retriever
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# BM25 keyword retriever
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 5

# Ensemble with weights
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.7, 0.3]  # 70% vector, 30% keyword
)

# Use in chain
chain = (
    {"context": ensemble_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### Pattern 5: Multi-Query Retrieval

Generate multiple queries for better recall:

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

# Generate multiple query variations
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI(model="gpt-4o", temperature=0.5)
)

# Automatically generates 3-5 query variations
results = multi_query_retriever.get_relevant_documents(
    "How does machine learning work?"
)
```

### Pattern 6: Contextual Compression (Re-Ranking)

Improve precision with re-ranking:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Base retriever (fetch 20 candidates)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

# Cohere re-ranker (return best 5)
compressor = CohereRerank(
    model="rerank-english-v3.0",
    top_n=5,
    cohere_api_key="your-api-key"
)

# Compression retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# Use in chain
chain = (
    {"context": compression_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

## Chain Patterns

### Pattern 7: Sequential Chains

Chain multiple LLM calls:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Chain 1: Extract key points
extract_prompt = ChatPromptTemplate.from_template(
    "Extract key points from:\n{text}"
)

# Chain 2: Summarize
summarize_prompt = ChatPromptTemplate.from_template(
    "Summarize these points:\n{key_points}"
)

llm = ChatOpenAI(model="gpt-4o")

# Sequential chain
chain = (
    {"text": RunnablePassthrough()}
    | extract_prompt
    | llm
    | StrOutputParser()
    | (lambda key_points: {"key_points": key_points})
    | summarize_prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("Long document text here...")
```

### Pattern 8: Parallel Chains

Run multiple chains in parallel:

```python
from langchain_core.runnables import RunnableParallel

# Define multiple chains
summary_chain = prompt1 | llm | StrOutputParser()
keywords_chain = prompt2 | llm | StrOutputParser()
sentiment_chain = prompt3 | llm | StrOutputParser()

# Run in parallel
parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    sentiment=sentiment_chain
)

result = parallel_chain.invoke({"text": document_text})
# Returns: {"summary": "...", "keywords": "...", "sentiment": "..."}
```

### Pattern 9: Conditional Routing

Route based on input classification:

```python
from langchain_core.runnables import RunnableBranch

# Classification chain
classification_chain = (
    ChatPromptTemplate.from_template("Classify: {input}")
    | llm
    | StrOutputParser()
)

# Different handlers for different types
technical_chain = prompt_technical | llm | StrOutputParser()
general_chain = prompt_general | llm | StrOutputParser()

# Route based on classification
router = RunnableBranch(
    (lambda x: "technical" in x["type"].lower(), technical_chain),
    (lambda x: "general" in x["type"].lower(), general_chain),
    general_chain  # Default
)

# Use router
chain = (
    {"type": classification_chain, "input": RunnablePassthrough()}
    | router
)
```

## Agent Patterns

### Pattern 10: ReAct Agent

Agent with reasoning and action steps:

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

# Define tools
def search_tool(query: str) -> str:
    """Search documentation."""
    results = vectorstore.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])

def calculator_tool(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

tools = [
    Tool(
        name="search",
        func=search_tool,
        description="Search documentation for information"
    ),
    Tool(
        name="calculator",
        func=calculator_tool,
        description="Calculate mathematical expressions"
    )
]

# Create agent
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
agent = create_react_agent(llm, tools, prompt_template)

# Agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# Run agent
result = agent_executor.invoke({
    "input": "What is the average of the first 3 prime numbers?"
})
```

### Pattern 11: OpenAI Functions Agent

Use OpenAI function calling:

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def search_documentation(query: str) -> str:
    """Search the documentation for information.

    Args:
        query: The search query string

    Returns:
        Relevant documentation content
    """
    results = vectorstore.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])

@tool
def get_current_weather(location: str) -> str:
    """Get the current weather for a location.

    Args:
        location: City name or zip code

    Returns:
        Weather information
    """
    # API call here
    return f"Weather in {location}: Sunny, 72°F"

tools = [search_documentation, get_current_weather]

# Create agent
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)
```

## Tool Integration

### Pattern 12: Custom Tool Creation

```python
from langchain_core.tools import BaseTool
from typing import Optional
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input for search tool."""
    query: str = Field(description="The search query")
    filters: Optional[dict] = Field(default=None, description="Metadata filters")

class VectorSearchTool(BaseTool):
    name: str = "vector_search"
    description: str = "Search the vector database for relevant documents"
    args_schema: type[BaseModel] = SearchInput

    vectorstore: QdrantVectorStore = Field(exclude=True)

    def _run(self, query: str, filters: Optional[dict] = None) -> str:
        """Execute the search."""
        if filters:
            # Apply metadata filters
            results = self.vectorstore.similarity_search(
                query,
                k=5,
                filter=filters
            )
        else:
            results = self.vectorstore.similarity_search(query, k=5)

        return "\n\n".join([
            f"Source: {doc.metadata['source']}\n{doc.page_content}"
            for doc in results
        ])

    async def _arun(self, query: str, filters: Optional[dict] = None) -> str:
        """Async execution."""
        # Async implementation
        raise NotImplementedError("Async not implemented")

# Use tool
search_tool = VectorSearchTool(vectorstore=vectorstore)
```

## Production Best Practices

### Pattern 13: Error Handling

```python
from langchain_core.runnables import RunnableConfig

def safe_chain_invoke(chain, input_data, max_retries=3):
    """Invoke chain with retry logic."""
    for attempt in range(max_retries):
        try:
            return chain.invoke(input_data)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff

# Usage
result = safe_chain_invoke(chain, "What is machine learning?")
```

### Pattern 14: Caching

```python
from langchain.cache import RedisSemanticCache
from langchain.globals import set_llm_cache
from langchain_voyageai import VoyageAIEmbeddings

# Semantic caching (cache similar queries)
set_llm_cache(RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=VoyageAIEmbeddings(model="voyage-3"),
    score_threshold=0.95  # 95% similarity = cache hit
))

# Now LLM calls are automatically cached
llm = ChatOpenAI(model="gpt-4o")
response1 = llm.invoke("What is ML?")  # API call
response2 = llm.invoke("What is machine learning?")  # Cache hit!
```

### Pattern 15: Callbacks for Monitoring

```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List

class CustomCallbackHandler(BaseCallbackHandler):
    """Custom callback for monitoring."""

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts."""
        print(f"LLM started with prompt: {prompts[0][:100]}...")

    def on_llm_end(self, response: Any, **kwargs: Any) -> Any:
        """Run when LLM ends."""
        print(f"LLM finished. Tokens used: {response.llm_output.get('token_usage')}")

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        """Run when chain starts."""
        print(f"Chain started with inputs: {inputs.keys()}")

# Use callback
callback = CustomCallbackHandler()
result = chain.invoke(
    "What is machine learning?",
    config={"callbacks": [callback]}
)
```

### Pattern 16: OpenLLMetry Integration

```python
from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow, task

# Initialize tracing
Traceloop.init(
    app_name="rag_pipeline",
    api_endpoint="http://localhost:4318",
    disable_batch=True
)

@workflow(name="rag_query")
def rag_query(question: str):
    """RAG query with automatic tracing."""
    # All LangChain calls are automatically traced
    result = chain.invoke(question)
    return result

# Usage - automatically sends traces to OpenLLMetry
answer = rag_query("What is machine learning?")
```

### Pattern 17: Async Chains

```python
import asyncio
from langchain_core.runnables import RunnablePassthrough

# Async chain
async_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Async invocation
async def process_question(question: str):
    result = await async_chain.ainvoke(question)
    return result

# Async streaming
async def stream_question(question: str):
    async for chunk in async_chain.astream(question):
        print(chunk, end="", flush=True)

# Run async
asyncio.run(process_question("What is ML?"))
```

### Pattern 18: Batch Processing

```python
# Batch invoke (parallel execution)
questions = [
    "What is machine learning?",
    "What is deep learning?",
    "What is reinforcement learning?"
]

# Process all in parallel
results = chain.batch(questions)

# With concurrency limit
results = chain.batch(questions, config={"max_concurrency": 5})
```

### Pattern 19: Configuration Management

```python
from pydantic_settings import BaseSettings

class RAGConfig(BaseSettings):
    """RAG pipeline configuration."""

    # Vector store
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "documents"

    # Embeddings
    embedding_model: str = "voyage-3"
    voyage_api_key: str

    # LLM
    llm_model: str = "gpt-4o"
    openai_api_key: str
    temperature: float = 0.0

    # Retrieval
    top_k: int = 5
    search_type: str = "mmr"

    class Config:
        env_file = ".env"

# Load config
config = RAGConfig()

# Use in chain
embeddings = VoyageAIEmbeddings(
    model=config.embedding_model,
    voyage_api_key=config.voyage_api_key
)
llm = ChatOpenAI(
    model=config.llm_model,
    temperature=config.temperature,
    openai_api_key=config.openai_api_key
)
```

### Pattern 20: FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str
    stream: bool = False

@app.post("/api/rag/query")
async def query_rag(query: Query):
    """RAG query endpoint."""
    try:
        if query.stream:
            async def generate():
                async for chunk in chain.astream(query.question):
                    yield chunk

            return StreamingResponse(generate(), media_type="text/plain")
        else:
            result = await chain.ainvoke(query.question)
            return {"answer": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

## Common Patterns Summary

| Pattern | Use Case | Complexity |
|---------|----------|-----------|
| Basic RAG | Standard retrieval + generation | Low |
| Streaming RAG | Better UX for long responses | Low |
| Hybrid Search | Improve recall with keyword | Medium |
| Multi-Query | Better recall with query variations | Medium |
| Re-Ranking | Improve precision | Medium |
| Sequential Chains | Multi-step processing | Medium |
| Parallel Chains | Multiple operations at once | Medium |
| ReAct Agent | Tool use with reasoning | High |
| Functions Agent | OpenAI function calling | High |

## Performance Tips

1. **Use async** - Better throughput for concurrent requests
2. **Batch when possible** - Process multiple inputs in parallel
3. **Cache aggressively** - Semantic caching for similar queries
4. **Stream responses** - Better UX and error recovery
5. **Monitor with callbacks** - Track token usage and latency
6. **Limit context** - Only retrieve k=3-5 chunks
7. **Use MMR** - Avoid redundant chunks
8. **Re-rank** - Fetch 20, return best 5
