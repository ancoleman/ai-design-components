"""
Dagster Pipeline for Embedding Generation

This example demonstrates production-grade orchestration for RAG pipelines:
1. Document ingestion from various sources
2. Chunking with configurable strategies
3. Embedding generation with batching
4. Vector database indexing
5. Asset lineage tracking and versioning

Use Dagster when:
- Building production RAG systems requiring orchestration
- Need to track data lineage and dependencies
- Want to schedule and monitor pipeline runs
- Require asset versioning and recomputation
"""

import os
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

from dagster import (
    asset,
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue,
    Config,
    OpExecutionContext,
    Definitions,
    define_asset_job,
    ScheduleDefinition,
    AssetSelection,
)
from dotenv import load_dotenv

# LangChain imports
from langchain_core.documents import Document
from langchain_voyageai import VoyageAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

# Load environment variables
load_dotenv()


class RAGPipelineConfig(Config):
    """Configuration for RAG pipeline assets."""

    # Source configuration
    source_directory: str = "data/raw_documents"
    file_extensions: List[str] = [".txt", ".md", ".pdf"]

    # Chunking configuration
    chunk_size: int = 512
    chunk_overlap: int = 50

    # Embedding configuration
    embedding_model: str = "voyage-3"  # or "text-embedding-3-small"
    batch_size: int = 100

    # Qdrant configuration
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "production_docs"


@asset(
    description="Raw documents loaded from source directory",
    metadata={
        "dagster/priority": "high",
        "owner": "data-team"
    }
)
def raw_documents(context: AssetExecutionContext, config: RAGPipelineConfig) -> List[Dict[str, Any]]:
    """
    Load raw documents from source directory.

    Supports multiple file formats and tracks metadata for lineage.

    Returns:
        List of document dictionaries with content and metadata
    """
    source_path = Path(config.source_directory)

    if not source_path.exists():
        context.log.warning(f"Source directory {source_path} does not exist. Creating sample documents...")
        source_path.mkdir(parents=True, exist_ok=True)
        _create_sample_documents(source_path)

    documents = []
    file_count = 0

    for ext in config.file_extensions:
        for file_path in source_path.rglob(f"*{ext}"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                documents.append({
                    "content": content,
                    "metadata": {
                        "source": str(file_path),
                        "file_name": file_path.name,
                        "file_type": ext,
                        "loaded_at": datetime.now().isoformat()
                    }
                })
                file_count += 1

            except Exception as e:
                context.log.error(f"Failed to load {file_path}: {e}")

    context.log.info(f"Loaded {len(documents)} documents from {file_count} files")

    # Track metadata for Dagster UI
    return documents


@asset(
    description="Documents chunked into 512-token segments with 50-token overlap",
    deps=[raw_documents]
)
def chunked_documents(
    context: AssetExecutionContext,
    config: RAGPipelineConfig,
    raw_documents: List[Dict[str, Any]]
) -> List[Document]:
    """
    Split raw documents into chunks for embedding generation.

    Uses recursive character splitting with configurable size and overlap.

    Args:
        raw_documents: Output from raw_documents asset

    Returns:
        List of LangChain Document objects
    """
    context.log.info(f"Chunking {len(raw_documents)} documents...")

    # Initialize splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    # Convert to LangChain documents and split
    all_chunks = []
    for doc in raw_documents:
        langchain_doc = Document(
            page_content=doc["content"],
            metadata=doc["metadata"]
        )
        chunks = splitter.split_documents([langchain_doc])
        all_chunks.extend(chunks)

    context.log.info(f"Created {len(all_chunks)} chunks")

    # Log metadata for Dagster UI
    context.log_event(
        MaterializeResult(
            metadata={
                "num_chunks": len(all_chunks),
                "avg_chunk_size": sum(len(c.page_content) for c in all_chunks) / len(all_chunks),
                "chunk_size": config.chunk_size,
                "chunk_overlap": config.chunk_overlap,
                "preview": MetadataValue.md(all_chunks[0].page_content[:200] + "..." if all_chunks else "No chunks")
            }
        )
    )

    return all_chunks


@asset(
    description="Embeddings generated using Voyage AI or OpenAI",
    deps=[chunked_documents]
)
def document_embeddings(
    context: AssetExecutionContext,
    config: RAGPipelineConfig,
    chunked_documents: List[Document]
) -> List[List[float]]:
    """
    Generate embeddings for all document chunks.

    Implements batching for efficient API usage and cost control.

    Args:
        chunked_documents: Output from chunked_documents asset

    Returns:
        List of embedding vectors
    """
    context.log.info(f"Generating embeddings for {len(chunked_documents)} chunks...")

    # Select embedding model
    if config.embedding_model == "voyage-3":
        if not os.getenv("VOYAGE_API_KEY"):
            context.log.error("VOYAGE_API_KEY not set, falling back to OpenAI")
            config.embedding_model = "text-embedding-3-small"

    if config.embedding_model == "voyage-3":
        context.log.info("Using Voyage AI voyage-3 (MTEB: 69.0)")
        embeddings_model = VoyageAIEmbeddings(
            model="voyage-3",
            voyage_api_key=os.getenv("VOYAGE_API_KEY"),
            batch_size=config.batch_size
        )
    else:
        context.log.info("Using OpenAI text-embedding-3-small (MTEB: 62.3)")
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            chunk_size=config.batch_size
        )

    # Generate embeddings in batches
    texts = [doc.page_content for doc in chunked_documents]

    try:
        embeddings = embeddings_model.embed_documents(texts)
        context.log.info(f"Successfully generated {len(embeddings)} embeddings")

        # Log metadata
        context.log_event(
            MaterializeResult(
                metadata={
                    "num_embeddings": len(embeddings),
                    "embedding_dimension": len(embeddings[0]),
                    "model": config.embedding_model,
                    "batch_size": config.batch_size
                }
            )
        )

        return embeddings

    except Exception as e:
        context.log.error(f"Embedding generation failed: {e}")
        raise


@asset(
    description="Embeddings indexed in Qdrant vector database",
    deps=[chunked_documents, document_embeddings]
)
def vector_index(
    context: AssetExecutionContext,
    config: RAGPipelineConfig,
    chunked_documents: List[Document],
    document_embeddings: List[List[float]]
) -> Dict[str, Any]:
    """
    Index embeddings in Qdrant vector database.

    Creates collection if needed and uploads all vectors with metadata.

    Args:
        chunked_documents: Document chunks
        document_embeddings: Generated embeddings

    Returns:
        Indexing statistics and metadata
    """
    context.log.info("Indexing embeddings in Qdrant...")

    # Initialize Qdrant client
    client = QdrantClient(url=config.qdrant_url)

    # Get embedding dimension
    dimension = len(document_embeddings[0])

    # Create collection if doesn't exist
    collections = [c.name for c in client.get_collections().collections]

    if config.collection_name not in collections:
        context.log.info(f"Creating collection '{config.collection_name}' with dimension {dimension}")
        client.create_collection(
            collection_name=config.collection_name,
            vectors_config=models.VectorParams(
                size=dimension,
                distance=models.Distance.COSINE
            )
        )
    else:
        context.log.info(f"Collection '{config.collection_name}' already exists")

    # Index documents using LangChain wrapper
    if config.embedding_model == "voyage-3":
        embeddings_model = VoyageAIEmbeddings(
            model="voyage-3",
            voyage_api_key=os.getenv("VOYAGE_API_KEY")
        )
    else:
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=config.collection_name,
        embedding=embeddings_model
    )

    # Add documents with embeddings
    try:
        vectorstore.add_documents(chunked_documents)
        context.log.info(f"Successfully indexed {len(chunked_documents)} documents")

        # Get collection info
        collection_info = client.get_collection(config.collection_name)

        stats = {
            "collection_name": config.collection_name,
            "total_vectors": collection_info.points_count,
            "dimension": dimension,
            "indexed_at": datetime.now().isoformat()
        }

        # Log metadata
        context.log_event(
            MaterializeResult(
                metadata={
                    "collection_name": config.collection_name,
                    "total_vectors": collection_info.points_count,
                    "dimension": dimension,
                    "distance_metric": "cosine"
                }
            )
        )

        return stats

    except Exception as e:
        context.log.error(f"Indexing failed: {e}")
        raise


# Define the complete pipeline job
embedding_pipeline_job = define_asset_job(
    name="embedding_pipeline_job",
    selection=AssetSelection.all(),
    description="Complete RAG embedding pipeline from documents to vector index"
)

# Define a schedule (daily at 2 AM)
embedding_pipeline_schedule = ScheduleDefinition(
    name="daily_embedding_pipeline",
    job=embedding_pipeline_job,
    cron_schedule="0 2 * * *",  # Daily at 2 AM
    description="Run embedding pipeline daily to index new documents"
)

# Group all assets and jobs
defs = Definitions(
    assets=[raw_documents, chunked_documents, document_embeddings, vector_index],
    jobs=[embedding_pipeline_job],
    schedules=[embedding_pipeline_schedule]
)


def _create_sample_documents(directory: Path):
    """
    Create sample documents for demonstration.

    Args:
        directory: Directory to create sample documents in
    """
    samples = {
        "rag_overview.txt": """Retrieval-Augmented Generation (RAG) Overview

RAG is a technique that enhances LLM responses by retrieving relevant information from a knowledge base before generation. This approach significantly reduces hallucinations and enables LLMs to work with proprietary or up-to-date information.

The RAG pipeline consists of five stages:
1. Ingestion - Load documents from various sources
2. Indexing - Chunk and embed documents
3. Retrieval - Find relevant chunks for queries
4. Generation - Inject context into LLM prompts
5. Evaluation - Measure quality with RAGAS metrics

Benefits include improved accuracy, transparency (ability to cite sources), and easy knowledge updates without retraining.""",

        "embedding_models.txt": """Embedding Model Comparison

Choosing the right embedding model impacts retrieval quality and cost:

Voyage AI voyage-3:
- Dimensions: 1024
- MTEB Score: 69.0 (best-in-class)
- Cost: $$$ ($0.12 per 1M tokens)
- Use case: Production systems requiring highest quality

OpenAI text-embedding-3-small:
- Dimensions: 1536
- MTEB Score: 62.3
- Cost: $ ($0.02 per 1M tokens)
- Use case: Development, prototyping, cost-sensitive apps

Never mix embedding models in the same index. If changing models, re-embed all documents.""",

        "dagster_orchestration.md": """# Dagster for RAG Pipelines

Dagster is an asset-centric orchestration framework ideal for ML/AI pipelines.

## Key Features

1. **Asset Lineage**: Track dependencies between pipeline stages
2. **Versioning**: Automatic versioning of pipeline outputs
3. **Observability**: Rich UI for monitoring pipeline runs
4. **Type Safety**: Strong typing for asset dependencies
5. **Scheduling**: Cron-based or sensor-based execution

## Why Dagster for RAG?

- Clear data lineage from documents → chunks → embeddings → index
- Easy recomputation when upstream assets change
- Built-in metadata tracking for each asset
- Perfect for production ML systems

## Alternative: Prefect

Prefect is more workflow-oriented. Choose Dagster for data-centric pipelines, Prefect for workflow orchestration."""
    }

    for filename, content in samples.items():
        file_path = directory / filename
        with open(file_path, 'w') as f:
            f.write(content)


if __name__ == "__main__":
    """
    Run the pipeline locally for testing.

    For production deployment:
    1. Install Dagster: pip install dagster dagster-webserver
    2. Start UI: dagster dev -f embedding_pipeline.py
    3. Access UI: http://localhost:3000
    4. Materialize assets from UI or CLI
    """
    print("""
=== Dagster Embedding Pipeline ===

To run this pipeline:

1. Install dependencies:
   pip install dagster dagster-webserver langchain-qdrant langchain-voyageai

2. Start Dagster UI:
   dagster dev -f embedding_pipeline.py

3. Open browser:
   http://localhost:3000

4. Materialize assets:
   - Click "Materialize all" in UI
   - Or use CLI: dagster asset materialize -f embedding_pipeline.py

5. View lineage:
   - Asset graph shows dependencies
   - Metadata shows stats for each asset
   - Logs show execution details

Asset Pipeline:
raw_documents → chunked_documents → document_embeddings → vector_index

Schedule:
Daily at 2 AM (configurable in embedding_pipeline_schedule)

Configuration:
Edit RAGPipelineConfig class to customize:
- Source directory
- Chunk size/overlap
- Embedding model
- Qdrant settings
    """)
