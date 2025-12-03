"""
LlamaIndex RAG Example

Simpler API compared to LangChain for RAG-focused applications.
"""

import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    Document,
    Settings,
    StorageContext
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.voyageai import VoyageAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()


def setup_llama_index():
    """Configure LlamaIndex settings."""

    # LLM
    Settings.llm = OpenAI(
        model="gpt-4o",
        temperature=0.0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Embeddings (Voyage AI if available)
    if os.getenv("VOYAGE_API_KEY"):
        print("Using Voyage AI embeddings")
        Settings.embed_model = VoyageAIEmbedding(
            model_name="voyage-3",
            voyage_api_key=os.getenv("VOYAGE_API_KEY")
        )
    else:
        print("Using OpenAI embeddings")
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    # Chunking settings
    Settings.chunk_size = 512
    Settings.chunk_overlap = 50


def create_index():
    """Create vector index with Qdrant."""

    # Sample documents
    documents = [
        Document(
            text="""Machine Learning Basics

Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions.

Types of Machine Learning:
1. Supervised Learning - Training with labeled data
2. Unsupervised Learning - Finding patterns in unlabeled data
3. Reinforcement Learning - Learning through trial and error

Common applications include image recognition, natural language processing, and recommendation systems.""",
            metadata={"source": "ml_basics", "category": "fundamentals"}
        ),
        Document(
            text="""Deep Learning Overview

Deep learning is a subset of machine learning that uses neural networks with multiple layers (hence "deep"). These networks can automatically learn hierarchical representations of data.

Neural networks consist of:
- Input layer: Receives data
- Hidden layers: Process and transform data
- Output layer: Produces predictions

Popular architectures include CNNs for images, RNNs for sequences, and Transformers for language tasks.""",
            metadata={"source": "deep_learning", "category": "advanced"}
        )
    ]

    # Setup Qdrant
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="llamaindex_demo"
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create index (automatically chunks and embeds)
    print("Creating index...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    print("Index created!")

    return index


def query_index(index):
    """Query the index."""

    # Create query engine
    query_engine = index.as_query_engine(
        similarity_top_k=5,
        streaming=True  # Stream responses
    )

    # Sample queries
    questions = [
        "What is machine learning?",
        "What are the types of machine learning?",
        "How do neural networks work?",
        "What are transformers used for?"
    ]

    print("\n=== LlamaIndex RAG Q&A ===\n")

    for question in questions:
        print(f"Q: {question}")
        print("A: ", end="", flush=True)

        # Stream response
        response = query_engine.query(question)
        for text in response.response_gen:
            print(text, end="", flush=True)

        print("\n")


def main():
    """Main LlamaIndex RAG demo."""

    print("=== LlamaIndex RAG Demo ===\n")

    # Setup
    setup_llama_index()

    # Create index
    index = create_index()

    # Query
    query_index(index)

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
