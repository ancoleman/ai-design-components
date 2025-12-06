"""
Streaming RAG Implementation with LangChain

This example demonstrates streaming responses for better UX:
1. Token-by-token streaming from LLM
2. Async/await patterns for non-blocking I/O
3. Server-Sent Events (SSE) integration pattern
4. Progress indicators during retrieval

Use streaming when:
- Building chat interfaces (better perceived performance)
- Long-form answers (users see progress immediately)
- Production web applications (prevents timeout issues)
"""

import os
import asyncio
from typing import List, AsyncIterator
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.base import AsyncCallbackHandler
from qdrant_client import QdrantClient, models

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "streaming_rag_demo"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


class StreamingCallbackHandler(AsyncCallbackHandler):
    """
    Callback handler for tracking streaming events.

    Useful for debugging and monitoring streaming behavior.
    """

    async def on_llm_start(self, serialized: dict, prompts: List[str], **kwargs):
        """Called when LLM starts generating."""
        print("\n[Streaming] LLM generation started...")

    async def on_llm_new_token(self, token: str, **kwargs):
        """Called for each new token. Can be used for custom processing."""
        # Token is already printed by the main loop
        pass

    async def on_llm_end(self, response, **kwargs):
        """Called when LLM finishes generating."""
        print("\n[Streaming] LLM generation complete")


def get_embeddings():
    """
    Get embedding model for semantic search.

    Returns:
        Embeddings model instance
    """
    if os.getenv("VOYAGE_API_KEY"):
        return VoyageAIEmbeddings(
            model="voyage-3",
            voyage_api_key=os.getenv("VOYAGE_API_KEY")
        )
    else:
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )


def setup_vector_store() -> QdrantVectorStore:
    """
    Initialize Qdrant vector store.

    Returns:
        Configured QdrantVectorStore instance
    """
    client = QdrantClient(url=QDRANT_URL)
    embeddings = get_embeddings()

    # Detect embedding dimension
    test_embedding = embeddings.embed_query("test")
    dimension = len(test_embedding)

    # Create collection if needed
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=dimension,
                distance=models.Distance.COSINE
            )
        )

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )


def chunk_documents(texts: List[str]) -> List[Document]:
    """
    Split texts into chunks.

    Args:
        texts: List of text strings to chunk

    Returns:
        List of Document objects with chunked content
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    documents = [Document(page_content=text) for text in texts]
    chunks = splitter.split_documents(documents)
    return chunks


def create_streaming_rag_chain(vectorstore: QdrantVectorStore):
    """
    Build streaming RAG chain with LCEL.

    Key difference from basic RAG: streaming=True on ChatOpenAI

    Args:
        vectorstore: Configured vector store for retrieval

    Returns:
        Runnable chain that supports streaming
    """
    # Retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # Prompt template
    template = """Answer the question based only on the following context:

{context}

Question: {question}

Provide a detailed, informative answer. If the answer is not in the context, say "I don't have enough information to answer this question."

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # LLM with streaming enabled
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
        streaming=True,  # Enable streaming
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Build chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


async def stream_response(chain, question: str) -> AsyncIterator[str]:
    """
    Stream response from RAG chain asynchronously.

    This is the pattern to use in FastAPI endpoints or async contexts.

    Args:
        chain: RAG chain instance
        question: User question

    Yields:
        Token chunks as they're generated
    """
    async for chunk in chain.astream(question):
        yield chunk


async def async_streaming_example(chain, question: str):
    """
    Demonstrate async streaming (for web servers).

    Use this pattern in FastAPI/Starlette apps for streaming endpoints.

    Args:
        chain: RAG chain instance
        question: User question
    """
    print(f"\n[Async] Q: {question}")
    print("[Async] A: ", end="", flush=True)

    async for chunk in stream_response(chain, question):
        print(chunk, end="", flush=True)

    print()  # Newline after streaming completes


def sync_streaming_example(chain, question: str):
    """
    Demonstrate sync streaming (simpler, for scripts).

    Use this pattern in CLI tools or simple scripts.

    Args:
        chain: RAG chain instance
        question: User question
    """
    print(f"\n[Sync] Q: {question}")
    print("[Sync] A: ", end="", flush=True)

    for chunk in chain.stream(question):
        print(chunk, end="", flush=True)

    print()  # Newline after streaming completes


async def fastapi_integration_example():
    """
    Show how to integrate streaming RAG with FastAPI.

    This is a complete example you can copy into your FastAPI app.
    """
    print("\n=== FastAPI Integration Example ===\n")
    print("""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore

app = FastAPI()

# Initialize once at startup
vectorstore = setup_vector_store()
chain = create_streaming_rag_chain(vectorstore)

@app.post("/api/rag/stream")
async def stream_rag(question: str):
    \"\"\"
    Stream RAG responses using Server-Sent Events.

    Usage:
        curl -N -X POST "http://localhost:8000/api/rag/stream" \\
             -H "Content-Type: application/json" \\
             -d '{"question": "What is RAG?"}'
    \"\"\"
    async def generate():
        async for chunk in chain.astream(question):
            # SSE format: data: {chunk}\\n\\n
            yield f"data: {chunk}\\n\\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

@app.post("/api/rag/complete")
async def complete_rag(question: str):
    \"\"\"
    Non-streaming endpoint (waits for full response).

    Use when you need the complete response before sending.
    \"\"\"
    response = await chain.ainvoke(question)
    return {"answer": response}

# Run with: uvicorn main:app --reload
    """)


def main():
    """
    Demonstrate streaming RAG patterns.

    Shows both sync and async streaming approaches.
    """
    print("=== Streaming RAG Demo ===\n")

    # Sample documents
    sample_texts = [
        """Streaming in Large Language Models

Streaming responses improves user experience by providing immediate feedback. Instead of waiting for the complete response, users see tokens appear in real-time, similar to ChatGPT.

Benefits:
1. Better perceived performance (users see progress)
2. Prevents timeout issues (long responses)
3. Lower memory usage (process tokens incrementally)
4. Early cancellation possible (stop generating if not relevant)

Technical implementation uses Server-Sent Events (SSE) or WebSockets.""",

        """Server-Sent Events (SSE) for Streaming

SSE is a standard for server-to-client streaming over HTTP. It's simpler than WebSockets for one-way communication.

SSE format:
data: {message}\\n\\n

Python (FastAPI) example:
```python
async def generate():
    for chunk in stream:
        yield f"data: {chunk}\\n\\n"

return StreamingResponse(generate(), media_type="text/event-stream")
```

JavaScript client:
```javascript
const eventSource = new EventSource('/api/stream');
eventSource.onmessage = (event) => {
    console.log(event.data);
};
```""",

        """Async vs Sync Streaming in Python

Async streaming (asyncio):
- Non-blocking I/O
- Handles multiple concurrent requests
- Required for FastAPI/Starlette
- Uses: astream(), ainvoke()

Sync streaming:
- Blocking I/O
- Simpler code
- Good for CLI tools, scripts
- Uses: stream(), invoke()

LangChain supports both patterns. Choose based on your use case."""
    ]

    # Setup
    print("Setting up vector store...")
    chunks = chunk_documents(sample_texts)
    vectorstore = setup_vector_store()
    vectorstore.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks\n")

    # Create streaming chain
    chain = create_streaming_rag_chain(vectorstore)

    # Example 1: Sync streaming (simple)
    print("=== Example 1: Sync Streaming (for CLI tools) ===")
    sync_streaming_example(
        chain,
        "How does streaming improve user experience?"
    )

    # Example 2: Async streaming (for web servers)
    print("\n=== Example 2: Async Streaming (for FastAPI) ===")
    asyncio.run(async_streaming_example(
        chain,
        "What is the difference between SSE and WebSockets?"
    ))

    # Example 3: Show FastAPI integration
    asyncio.run(fastapi_integration_example())

    print("\n=== Key Takeaways ===")
    print("""
1. Enable streaming with: ChatOpenAI(streaming=True)
2. Use chain.stream() for sync contexts (CLI tools)
3. Use chain.astream() for async contexts (FastAPI)
4. SSE format: "data: {chunk}\\n\\n"
5. Always flush output for real-time display

For production: Combine streaming with error handling, retry logic,
and rate limiting for robust RAG applications.
    """)


if __name__ == "__main__":
    main()
