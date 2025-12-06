"""
Basic RAG Implementation with LangChain

This example demonstrates the fundamental RAG pattern:
1. Document loading and chunking
2. Embedding generation
3. Vector storage
4. Retrieval-augmented generation

Perfect starting point for understanding RAG architecture.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "basic_rag_demo"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


def get_embeddings():
    """
    Get embedding model based on available API keys.

    Prioritizes Voyage AI (best quality) but falls back to OpenAI.

    Returns:
        Embeddings model instance
    """
    if os.getenv("VOYAGE_API_KEY"):
        print("Using Voyage AI voyage-3 (MTEB: 69.0)")
        return VoyageAIEmbeddings(
            model="voyage-3",
            voyage_api_key=os.getenv("VOYAGE_API_KEY")
        )
    else:
        print("Using OpenAI text-embedding-3-small (MTEB: 62.3)")
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )


def setup_vector_store() -> QdrantVectorStore:
    """
    Initialize Qdrant vector store with proper collection setup.

    Creates collection if it doesn't exist with appropriate vector dimensions.

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
        print(f"Creating collection '{COLLECTION_NAME}' (dim={dimension})")
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
    Split texts into 512-token chunks with 50-token overlap.

    This is the recommended default chunking strategy that balances:
    - Context preservation (not too small)
    - Relevance precision (not too large)
    - Token limit handling (fits in most contexts)

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

    print(f"Created {len(chunks)} chunks from {len(texts)} documents")
    return chunks


def create_rag_chain(vectorstore: QdrantVectorStore):
    """
    Build a basic RAG chain using LCEL (LangChain Expression Language).

    Chain flow:
    1. Retrieve relevant chunks from vector store
    2. Format into prompt with context
    3. Generate response with LLM
    4. Parse output as string

    Args:
        vectorstore: Configured vector store for retrieval

    Returns:
        Runnable chain for RAG queries
    """
    # Retriever: Get top 5 most relevant chunks
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # Prompt template with context injection
    template = """Answer the question based only on the following context:

{context}

Question: {question}

Provide a clear, concise answer. If the answer is not in the context, say "I don't have enough information to answer this question."

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # LLM with zero temperature for factual responses
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Build chain using LCEL pipe operator
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def main():
    """
    Demonstrate basic RAG workflow with sample documents.

    Shows complete pipeline from document ingestion to question answering.
    """
    print("=== Basic RAG Pipeline Demo ===\n")

    # Sample documents about AI/ML concepts
    sample_texts = [
        """Retrieval-Augmented Generation (RAG) is a technique that enhances large language models by retrieving relevant information from a knowledge base before generating responses. This approach combines the benefits of retrieval systems with generative models.

RAG works in three steps:
1. Convert user query to embedding
2. Retrieve most similar documents from vector database
3. Inject retrieved context into LLM prompt

Benefits include reduced hallucinations, ability to cite sources, and easy knowledge updates without retraining.""",

        """Vector databases store data as high-dimensional embeddings, enabling semantic similarity search. Popular vector databases include Qdrant, Pinecone, Weaviate, and pgvector.

Key features:
- Fast approximate nearest neighbor (ANN) search
- Filtering by metadata
- Horizontal scalability
- HNSW (Hierarchical Navigable Small World) indexing

Qdrant is recommended for production RAG systems due to its performance and filtering capabilities.""",

        """Chunking strategy is critical for RAG quality. The recommended default is 512 tokens with 50-token overlap.

Why 512 tokens:
- Too small (<256): Loses context, requires more retrievals
- Too large (>1024): Includes irrelevant content, hits token limits
- 512 is the sweet spot for most use cases

Overlap prevents information loss at chunk boundaries and ensures continuity."""
    ]

    # Step 1: Chunk documents
    print("Step 1: Chunking documents...")
    chunks = chunk_documents(sample_texts)

    # Step 2: Setup vector store and index
    print("\nStep 2: Setting up vector store...")
    vectorstore = setup_vector_store()

    print("Step 3: Indexing chunks...")
    vectorstore.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks successfully")

    # Step 4: Create RAG chain
    print("\nStep 4: Creating RAG chain...")
    chain = create_rag_chain(vectorstore)

    # Step 5: Query the system
    print("\n=== RAG Query Examples ===\n")

    questions = [
        "What is RAG and how does it work?",
        "Why are vector databases important for RAG?",
        "What is the recommended chunk size and why?"
    ]

    for question in questions:
        print(f"Q: {question}")
        answer = chain.invoke(question)
        print(f"A: {answer}\n")

    print("Demo complete! Basic RAG pipeline working successfully.")


if __name__ == "__main__":
    main()
