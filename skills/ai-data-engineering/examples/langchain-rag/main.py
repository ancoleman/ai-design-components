"""
Complete RAG Pipeline Example with LangChain 0.3+

This example demonstrates:
1. Document loading
2. Chunking (512 tokens, 50 overlap)
3. Embedding generation (Voyage AI)
4. Vector storage (Qdrant)
5. Retrieval + generation
6. Streaming responses
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_voyageai import VoyageAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from qdrant_client import QdrantClient, models

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "rag_demo_docs"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


def get_embeddings():
    """Get embedding model (Voyage AI if available, else OpenAI)."""
    if os.getenv("VOYAGE_API_KEY"):
        print("Using Voyage AI embeddings (best quality)")
        return VoyageAIEmbeddings(
            model="voyage-3",
            voyage_api_key=os.getenv("VOYAGE_API_KEY"),
            batch_size=128
        )
    else:
        print("Using OpenAI embeddings (VOYAGE_API_KEY not set)")
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )


def setup_qdrant():
    """Initialize Qdrant client and collection."""
    client = QdrantClient(url=QDRANT_URL)

    # Get embedding dimension
    embeddings = get_embeddings()
    test_embedding = embeddings.embed_query("test")
    dimension = len(test_embedding)

    # Create collection if doesn't exist
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in collections:
        print(f"Creating collection '{COLLECTION_NAME}' with dimension {dimension}")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=dimension,
                distance=models.Distance.COSINE
            )
        )
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists")

    return client


def load_and_chunk_documents(file_paths: list[str]):
    """Load documents and split into chunks."""
    all_chunks = []

    for file_path in file_paths:
        print(f"Loading: {file_path}")
        loader = TextLoader(file_path)
        documents = loader.load()

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = splitter.split_documents(documents)
        all_chunks.extend(chunks)

    print(f"Created {len(all_chunks)} chunks")
    return all_chunks


def index_documents(chunks):
    """Index documents in Qdrant."""
    client = setup_qdrant()
    embeddings = get_embeddings()

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )

    print(f"Indexing {len(chunks)} chunks...")
    vectorstore.add_documents(chunks)
    print("Indexing complete!")

    return vectorstore


def create_rag_chain(vectorstore):
    """Create RAG chain with retrieval + generation."""

    # Retriever (use MMR for diversity)
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20,
            "lambda_mult": 0.5
        }
    )

    # Prompt template
    template = """Answer the question based only on the following context:

{context}

Question: {question}

Provide a clear, concise answer. If the answer is not in the context, say "I don't have enough information to answer this question."

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # LLM (streaming for better UX)
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,  # Factual responses
        streaming=True,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Build chain using LCEL
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def main():
    """Main RAG pipeline demonstration."""

    print("=== LangChain RAG Pipeline Demo ===\n")

    # Step 1: Create sample documents
    sample_docs = [
        {
            "path": "ml_basics.txt",
            "content": """Machine Learning Basics

Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions.

Types of Machine Learning:
1. Supervised Learning - Training with labeled data
2. Unsupervised Learning - Finding patterns in unlabeled data
3. Reinforcement Learning - Learning through trial and error

Common applications include image recognition, natural language processing, and recommendation systems."""
        },
        {
            "path": "deep_learning.txt",
            "content": """Deep Learning Overview

Deep learning is a subset of machine learning that uses neural networks with multiple layers (hence "deep"). These networks can automatically learn hierarchical representations of data.

Neural networks consist of:
- Input layer: Receives data
- Hidden layers: Process and transform data
- Output layer: Produces predictions

Popular architectures include CNNs for images, RNNs for sequences, and Transformers for language tasks."""
        }
    ]

    # Write sample documents
    for doc in sample_docs:
        with open(doc["path"], "w") as f:
            f.write(doc["content"])

    # Step 2: Load and chunk documents
    chunks = load_and_chunk_documents([doc["path"] for doc in sample_docs])

    # Step 3: Index in Qdrant
    vectorstore = index_documents(chunks)

    # Step 4: Create RAG chain
    chain = create_rag_chain(vectorstore)

    # Step 5: Query the system
    questions = [
        "What is machine learning?",
        "What are the types of machine learning?",
        "How do neural networks work?",
        "What are transformers used for?"
    ]

    print("\n=== RAG Q&A Demo ===\n")

    for question in questions:
        print(f"Q: {question}")
        print("A: ", end="", flush=True)

        # Stream response
        for chunk in chain.stream(question):
            print(chunk, end="", flush=True)

        print("\n")

    # Cleanup
    for doc in sample_docs:
        os.remove(doc["path"])

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
