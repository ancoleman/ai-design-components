"""
Hybrid Search RAG Implementation (Semantic + Keyword)

This example demonstrates hybrid search combining:
1. Vector similarity search (semantic understanding)
2. BM25 keyword search (exact term matching)
3. Reciprocal Rank Fusion (RRF) for result merging

Use hybrid search when:
- Documents contain specific technical terms or codes
- Users query with exact keywords (product names, error codes)
- Pure semantic search misses important exact matches
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
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from qdrant_client import QdrantClient, models

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "hybrid_search_demo"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50


def get_embeddings():
    """
    Get embedding model for semantic search.

    Returns:
        Embeddings model instance
    """
    if os.getenv("VOYAGE_API_KEY"):
        print("Using Voyage AI voyage-3 for semantic search")
        return VoyageAIEmbeddings(
            model="voyage-3",
            voyage_api_key=os.getenv("VOYAGE_API_KEY")
        )
    else:
        print("Using OpenAI text-embedding-3-small for semantic search")
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )


def setup_vector_store() -> QdrantVectorStore:
    """
    Initialize Qdrant vector store for semantic search.

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
    Split texts into chunks for both semantic and keyword indexing.

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


def create_hybrid_retriever(
    vectorstore: QdrantVectorStore,
    chunks: List[Document],
    k: int = 5
):
    """
    Create hybrid retriever combining semantic and keyword search.

    Uses Reciprocal Rank Fusion (RRF) to merge results from:
    1. Vector similarity search (semantic understanding)
    2. BM25 keyword search (exact term matching)

    RRF formula: score = sum(1 / (rank + k)) for k=60 (standard)

    Args:
        vectorstore: Vector store for semantic search
        chunks: Document chunks for BM25 indexing
        k: Number of results to retrieve

    Returns:
        EnsembleRetriever combining both search methods
    """
    print("Creating hybrid retriever (semantic + keyword)...")

    # Semantic retriever (vector similarity)
    semantic_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    # Keyword retriever (BM25)
    keyword_retriever = BM25Retriever.from_documents(chunks)
    keyword_retriever.k = k

    # Combine with RRF (weights: 50% semantic, 50% keyword)
    # Adjust weights based on your use case:
    # - Higher semantic weight (0.7) for conceptual queries
    # - Higher keyword weight (0.7) for exact term searches
    hybrid_retriever = EnsembleRetriever(
        retrievers=[semantic_retriever, keyword_retriever],
        weights=[0.5, 0.5],  # Equal weighting
        c=60  # RRF constant (standard value)
    )

    print("Hybrid retriever ready (RRF fusion enabled)")
    return hybrid_retriever


def create_hybrid_rag_chain(retriever):
    """
    Build RAG chain using hybrid retriever.

    Args:
        retriever: Hybrid retriever instance

    Returns:
        Runnable chain for hybrid RAG queries
    """
    # Prompt template
    template = """Answer the question based only on the following context:

{context}

Question: {question}

Provide a clear, concise answer. If the answer is not in the context, say "I don't have enough information to answer this question."

Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Build chain
    def format_docs(docs):
        """Format retrieved documents for context."""
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def main():
    """
    Demonstrate hybrid search RAG with technical documentation.

    Shows how hybrid search handles both semantic and exact keyword queries.
    """
    print("=== Hybrid Search RAG Demo ===\n")

    # Sample technical documents with specific terms and codes
    sample_texts = [
        """Error Code E-RAG-001: Vector dimension mismatch

This error occurs when the embedding model dimensions don't match the Qdrant collection configuration.

Solution:
1. Check embedding model dimension (voyage-3 = 1024, text-embedding-3-small = 1536)
2. Verify Qdrant collection dimension matches
3. Recreate collection if dimensions differ

Example code:
```python
embeddings = VoyageAIEmbeddings(model="voyage-3")  # 1024 dimensions
test_vec = embeddings.embed_query("test")
print(f"Dimension: {len(test_vec)}")  # Should match collection
```""",

        """BM25 Algorithm for Keyword Search

BM25 (Best Match 25) is a ranking function used for keyword-based retrieval. It improves upon TF-IDF by considering document length normalization.

BM25 formula:
score(D,Q) = sum(IDF(qi) * (f(qi,D) * (k1 + 1)) / (f(qi,D) + k1 * (1 - b + b * |D| / avgdl)))

Where:
- f(qi,D): term frequency in document
- |D|: document length
- avgdl: average document length
- k1: term saturation parameter (typically 1.2-2.0)
- b: length normalization (typically 0.75)

BM25 works well for exact term matching, making it ideal for hybrid search.""",

        """Reciprocal Rank Fusion (RRF) Merging Strategy

RRF combines rankings from multiple retrieval systems. For each document, RRF calculates:

RRF_score = sum(1 / (k + rank_i))

Where:
- k: constant (typically 60)
- rank_i: rank from retrieval system i

Benefits:
- No score normalization needed
- Handles different scoring scales
- Simple and effective

Used in hybrid search to merge semantic and keyword results.""",

        """Product SKU-VEC-1024: Voyage AI Embedding Model

Specifications:
- Model: voyage-3
- Dimensions: 1024
- MTEB Score: 69.0
- Context length: 32,000 tokens
- Pricing: $0.12 per 1M tokens

Use cases:
- Production RAG systems
- Semantic search
- Document clustering

Alternative: SKU-VEC-1536 (OpenAI text-embedding-3-small)"""
    ]

    # Step 1: Chunk documents
    print("Step 1: Chunking documents...")
    chunks = chunk_documents(sample_texts)

    # Step 2: Setup vector store
    print("\nStep 2: Setting up vector store...")
    vectorstore = setup_vector_store()

    # Step 3: Index documents
    print("Step 3: Indexing chunks...")
    vectorstore.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks")

    # Step 4: Create hybrid retriever
    print("\nStep 4: Creating hybrid retriever...")
    hybrid_retriever = create_hybrid_retriever(vectorstore, chunks, k=3)

    # Step 5: Create RAG chain
    print("Step 5: Creating hybrid RAG chain...")
    chain = create_hybrid_rag_chain(hybrid_retriever)

    # Step 6: Test with different query types
    print("\n=== Hybrid Search Query Examples ===\n")

    queries = [
        # Exact keyword query (BM25 should excel)
        {
            "query": "What is error code E-RAG-001?",
            "type": "Keyword (exact match)"
        },
        # Semantic query (vector search should excel)
        {
            "query": "How do I merge results from different search methods?",
            "type": "Semantic (conceptual)"
        },
        # Product code query (hybrid should excel)
        {
            "query": "Tell me about SKU-VEC-1024",
            "type": "Hybrid (code + context)"
        },
        # Mixed query
        {
            "query": "What algorithm does BM25 use for ranking?",
            "type": "Hybrid (term + concept)"
        }
    ]

    for item in queries:
        print(f"Query Type: {item['type']}")
        print(f"Q: {item['query']}")
        answer = chain.invoke(item['query'])
        print(f"A: {answer}\n")
        print("-" * 80 + "\n")

    print("Demo complete! Hybrid search combines best of semantic + keyword retrieval.")


if __name__ == "__main__":
    main()
