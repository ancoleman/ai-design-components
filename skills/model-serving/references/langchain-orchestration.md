# LangChain Orchestration for LLM Applications


## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Basic RAG Pipeline](#basic-rag-pipeline)
  - [Complete Example](#complete-example)
- [Chain Types for RAG](#chain-types-for-rag)
  - [1. Stuff Chain (Recommended for Most Cases)](#1-stuff-chain-recommended-for-most-cases)
  - [2. Map-Reduce Chain](#2-map-reduce-chain)
  - [3. Refine Chain](#3-refine-chain)
  - [4. Map-Rerank Chain](#4-map-rerank-chain)
- [Advanced Retrieval](#advanced-retrieval)
  - [Hybrid Search (Keyword + Semantic)](#hybrid-search-keyword-semantic)
  - [Re-ranking](#re-ranking)
  - [Multi-Query Retrieval](#multi-query-retrieval)
- [Conversational RAG](#conversational-rag)
- [Agents](#agents)
  - [ReAct Agent (Recommended)](#react-agent-recommended)
  - [Structured Tool Calling](#structured-tool-calling)
- [Streaming Responses](#streaming-responses)
- [Custom Chains](#custom-chains)
- [Error Handling](#error-handling)
- [Integration with vLLM](#integration-with-vllm)
- [Best Practices](#best-practices)
- [Resources](#resources)

## Overview

LangChain is a framework for building applications with LLMs through composable components: chains, agents, retrievers, and tools. Supports RAG (Retrieval-Augmented Generation), multi-step reasoning, and tool use.

**Key Use Cases:**
- RAG pipelines (document Q&A)
- Conversational agents with memory
- Multi-step reasoning (ReAct, Plan-and-Execute)
- Tool integration (search, calculators, APIs)

## Installation

```bash
# Core
pip install langchain

# LLM providers
pip install langchain-openai      # OpenAI, Azure OpenAI
pip install langchain-anthropic   # Anthropic Claude
pip install langchain-google      # Google (Gemini, Vertex AI)

# Vector stores
pip install langchain-qdrant
pip install langchain-chroma
pip install langchain-pinecone

# Community integrations
pip install langchain-community
```

## Basic RAG Pipeline

### Complete Example

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from qdrant_client import QdrantClient

# 1. Load documents
loader = TextLoader("./data/documents.txt")
documents = loader.load()

# For PDFs
pdf_loader = PyPDFLoader("./data/manual.pdf")
pdf_docs = pdf_loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

client = QdrantClient(url="http://localhost:6333")
vectorstore = Qdrant.from_documents(
    chunks,
    embeddings,
    url="http://localhost:6333",
    collection_name="documents",
    force_recreate=True
)

# 4. Create retrieval chain
llm = ChatOpenAI(model="gpt-4o", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # stuff, map_reduce, refine, map_rerank
    retriever=vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    ),
    return_source_documents=True
)

# 5. Query
result = qa_chain.invoke({"query": "What is PagedAttention?"})

print(f"Answer: {result['result']}")
print(f"\nSources:")
for doc in result['source_documents']:
    print(f"- {doc.metadata.get('source', 'Unknown')}: {doc.page_content[:100]}...")
```

## Chain Types for RAG

### 1. Stuff Chain (Recommended for Most Cases)

Concatenates all retrieved documents into a single prompt.

**Pros:**
- Simple and fast
- Single LLM call
- Works well when documents fit in context

**Cons:**
- Limited by context window
- Fails if total text > max tokens

**When to use:** 3-5 documents, each <1000 tokens

### 2. Map-Reduce Chain

Processes documents individually, then combines results.

**Pros:**
- Handles large document sets
- Parallel processing possible
- No context limit

**Cons:**
- Multiple LLM calls (expensive)
- Slower than stuff
- May lose cross-document context

**When to use:** 10+ documents or documents > context window

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_reduce",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
)
```

### 3. Refine Chain

Iteratively refines answer by processing documents sequentially.

**Pros:**
- Better synthesis than map-reduce
- Handles large document sets

**Cons:**
- Many sequential LLM calls (slow, expensive)
- Later documents may dominate

**When to use:** Need high-quality synthesis of many documents

### 4. Map-Rerank Chain

Scores each document's relevance, uses highest-scoring.

**Pros:**
- Good for finding specific info
- Handles irrelevant retrievals

**Cons:**
- May miss multi-document answers

**When to use:** Looking for single best answer from many candidates

## Advanced Retrieval

### Hybrid Search (Keyword + Semantic)

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Semantic retriever
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Keyword retriever
keyword_retriever = BM25Retriever.from_documents(chunks)
keyword_retriever.k = 5

# Combine with weights
ensemble_retriever = EnsembleRetriever(
    retrievers=[semantic_retriever, keyword_retriever],
    weights=[0.7, 0.3]  # 70% semantic, 30% keyword
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=ensemble_retriever
)
```

### Re-ranking

Improve retrieval quality by re-ranking results:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Base retriever (gets 10 candidates)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Re-ranker (selects top 3)
compressor = CohereRerank(model="rerank-english-v2.0", top_n=3)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=compression_retriever
)
```

### Multi-Query Retrieval

Generate multiple query variations for better recall:

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# User query: "How does vLLM work?"
# LLM generates variations:
# - "Explain vLLM architecture"
# - "What are vLLM's key features?"
# - "vLLM performance optimizations"
# Retrieves for all variations and deduplicates
```

## Conversational RAG

Add memory to maintain conversation context:

```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Create memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# Conversational chain
conv_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    memory=memory,
    return_source_documents=True
)

# First turn
result1 = conv_chain.invoke({"question": "What is PagedAttention?"})
print(result1["answer"])

# Follow-up (uses conversation history)
result2 = conv_chain.invoke({"question": "How does it improve throughput?"})
print(result2["answer"])  # References PagedAttention from context
```

## Agents

Agents use LLMs to decide which tools to use and in what order.

### ReAct Agent (Recommended)

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub

# Define tools
def search_docs(query: str) -> str:
    """Search documentation for technical information."""
    results = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in results])

def calculate(expression: str) -> str:
    """Calculate mathematical expressions. Use Python syntax."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

tools = [
    Tool(
        name="SearchDocs",
        func=search_docs,
        description="Search documentation for technical information about vLLM, PagedAttention, and model serving"
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Calculate mathematical expressions. Input should be valid Python expression."
    )
]

# Create agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# Run agent
result = agent_executor.invoke({
    "input": "What is PagedAttention and calculate GPU memory for Llama-3.1-8B (8B params × 2 bytes)"
})

print(result["output"])
```

**Agent reasoning flow:**
```
Thought: I need to search docs for PagedAttention and calculate memory
Action: SearchDocs
Action Input: PagedAttention
Observation: [retrieved doc content]

Thought: Now I need to calculate GPU memory
Action: Calculator
Action Input: 8000000000 * 2 / (1024**3)
Observation: 14.901161193847656

Thought: I have enough information to answer
Final Answer: PagedAttention is... and requires approximately 14.9 GB of GPU memory.
```

### Structured Tool Calling

For newer models with native tool calling:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool

@tool
def search_database(query: str, limit: int = 5) -> str:
    """Search the vector database for relevant documents.

    Args:
        query: Search query
        limit: Maximum number of results (default: 5)
    """
    results = vectorstore.similarity_search(query, k=limit)
    return "\n\n".join([doc.page_content for doc in results])

llm = ChatOpenAI(model="gpt-4o")
tools = [search_database]

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

## Streaming Responses

Stream tokens as they're generated:

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# For web applications
from langchain.callbacks.base import BaseCallbackHandler

class StreamingHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = []

    def on_llm_new_token(self, token: str, **kwargs):
        self.tokens.append(token)
        # Send token to frontend via SSE
        yield f"data: {json.dumps({'token': token})}\n\n"

handler = StreamingHandler()
llm = ChatOpenAI(model="gpt-4o", streaming=True, callbacks=[handler])
```

## Custom Chains

Build application-specific chains:

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Custom prompt
template = """You are a technical documentation expert.

Context from documentation:
{context}

Question: {question}

Provide a detailed, accurate answer based on the context. If the context doesn't contain enough information, say so clearly.

Answer:"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# Custom chain
def custom_rag(question: str) -> str:
    # 1. Retrieve
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    # 2. Generate
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    answer = llm_chain.run(context=context, question=question)

    return answer
```

## Error Handling

```python
from langchain.callbacks import get_openai_callback

try:
    with get_openai_callback() as cb:
        result = qa_chain.invoke({"query": question})

        print(f"Tokens used: {cb.total_tokens}")
        print(f"Cost: ${cb.total_cost:.4f}")
        print(f"Answer: {result['result']}")

except Exception as e:
    print(f"Error: {e}")
    # Fallback logic
    result = {"result": "Sorry, I encountered an error. Please try again."}
```

## Integration with vLLM

Use vLLM as LLM backend:

```python
from langchain_community.llms import VLLM

llm = VLLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    vllm_kwargs={
        "max_new_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    },
    trust_remote_code=True
)

# Or use OpenAI-compatible endpoint
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
    model="meta-llama/Llama-3.1-8B-Instruct"
)
```

## Best Practices

1. **Chunk Size Matters:**
   - Too small: Loses context
   - Too large: Irrelevant info
   - Sweet spot: 512-1024 tokens with 10-20% overlap

2. **Use Appropriate Chain Type:**
   - Few docs (<5): stuff
   - Many docs (>10): map_reduce
   - Quality synthesis needed: refine

3. **Add Metadata for Filtering:**
   ```python
   chunks = text_splitter.split_documents(documents)
   for chunk in chunks:
       chunk.metadata["source"] = "manual.pdf"
       chunk.metadata["date"] = "2025-12-02"

   # Filter during retrieval
   retriever = vectorstore.as_retriever(
       search_kwargs={
           "k": 5,
           "filter": {"source": "manual.pdf"}
       }
   )
   ```

4. **Monitor Token Usage:**
   ```python
   from langchain.callbacks import get_openai_callback

   with get_openai_callback() as cb:
       result = chain.invoke({"query": question})
       print(f"Cost: ${cb.total_cost:.4f}")
   ```

5. **Cache Embeddings:**
   ```python
   from langchain.embeddings import CacheBackedEmbeddings
   from langchain.storage import LocalFileStore

   store = LocalFileStore("./cache/")
   cached_embedder = CacheBackedEmbeddings.from_bytes_store(
       OpenAIEmbeddings(),
       store,
       namespace="openai-embeddings"
   )
   ```

## Resources

- LangChain Docs: https://python.langchain.com/
- LangChain Hub (prompts): https://smith.langchain.com/hub
- LangSmith (tracing): https://smith.langchain.com/
- GitHub: https://github.com/langchain-ai/langchain
