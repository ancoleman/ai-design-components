"""
Azure OpenAI RAG (Retrieval-Augmented Generation) Example

This example demonstrates:
- Azure OpenAI integration with Managed Identity
- Vector embeddings generation
- Azure AI Search integration
- RAG pattern implementation
- Semantic search with hybrid scoring

Dependencies:
    pip install openai azure-identity azure-search-documents azure-core

Usage:
    python azure-openai-rag.py

Environment Variables (if not using Managed Identity):
    AZURE_OPENAI_ENDPOINT - Azure OpenAI endpoint URL
    AZURE_SEARCH_ENDPOINT - Azure AI Search endpoint URL
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery, QueryType
from azure.core.credentials import AzureKeyCredential


@dataclass
class SearchResult:
    """Search result from Azure AI Search"""
    content: str
    title: str
    category: str
    score: float


class AzureOpenAIRAG:
    """
    RAG implementation using Azure OpenAI and Azure AI Search.

    This class handles:
    - Generating embeddings for queries
    - Performing vector search in Azure AI Search
    - Constructing prompts with retrieved context
    - Generating answers using Azure OpenAI
    """

    def __init__(
        self,
        openai_endpoint: Optional[str] = None,
        search_endpoint: Optional[str] = None,
        search_index_name: str = "documents",
        embedding_model: str = "text-embedding-ada-002",
        chat_model: str = "gpt-4-turbo"
    ):
        """
        Initialize Azure OpenAI RAG client.

        Args:
            openai_endpoint: Azure OpenAI endpoint (uses env var if not provided)
            search_endpoint: Azure AI Search endpoint (uses env var if not provided)
            search_index_name: Name of the search index
            embedding_model: Deployment name for embeddings model
            chat_model: Deployment name for chat model
        """
        # Setup Managed Identity authentication
        self.credential = DefaultAzureCredential()

        # Azure OpenAI setup
        openai_endpoint = openai_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
        if not openai_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT must be set")

        token_provider = get_bearer_token_provider(
            self.credential,
            "https://cognitiveservices.azure.com/.default"
        )

        self.openai_client = AzureOpenAI(
            azure_endpoint=openai_endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2024-02-15-preview"
        )

        # Azure AI Search setup
        search_endpoint = search_endpoint or os.environ.get("AZURE_SEARCH_ENDPOINT")
        if not search_endpoint:
            raise ValueError("AZURE_SEARCH_ENDPOINT must be set")

        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=search_index_name,
            credential=self.credential
        )

        self.embedding_model = embedding_model
        self.chat_model = chat_model

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using Azure OpenAI.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (1536 dimensions for ada-002)
        """
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def search_documents(
        self,
        query: str,
        top_k: int = 3,
        use_hybrid_search: bool = True
    ) -> List[SearchResult]:
        """
        Search documents using vector similarity and optional keyword search.

        Args:
            query: Search query
            top_k: Number of results to return
            use_hybrid_search: Use both vector and keyword search

        Returns:
            List of search results with content and metadata
        """
        # Generate embedding for query
        query_embedding = self.generate_embedding(query)

        # Setup vector query
        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields="contentVector"
        )

        # Perform search
        search_text = query if use_hybrid_search else None
        search_results = self.search_client.search(
            search_text=search_text,
            vector_queries=[vector_query],
            query_type=QueryType.SEMANTIC if use_hybrid_search else None,
            select=["content", "title", "category"],
            top=top_k
        )

        # Convert to SearchResult objects
        results = []
        for result in search_results:
            results.append(SearchResult(
                content=result.get("content", ""),
                title=result.get("title", ""),
                category=result.get("category", ""),
                score=result.get("@search.score", 0.0)
            ))

        return results

    def generate_answer(
        self,
        question: str,
        context_results: List[SearchResult],
        temperature: float = 0.2,
        max_tokens: int = 500,
        include_citations: bool = True
    ) -> str:
        """
        Generate answer using retrieved context and Azure OpenAI.

        Args:
            question: User question
            context_results: Retrieved documents from search
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            include_citations: Include document citations in answer

        Returns:
            Generated answer
        """
        # Build context from search results
        context_parts = []
        for i, result in enumerate(context_results, 1):
            context_parts.append(
                f"[Document {i}]\n"
                f"Category: {result.category}\n"
                f"Title: {result.title}\n"
                f"Content: {result.content}\n"
                f"Relevance Score: {result.score:.2f}\n"
            )

        context = "\n".join(context_parts)

        # System message with instructions
        system_message = """You are a helpful assistant that answers questions based on provided context.

Instructions:
1. Only use information from the provided documents
2. If the answer is not in the context, say "I don't have enough information to answer that question based on the available documents."
3. Be concise and accurate
4. Cite which document(s) you used (e.g., "According to Document 1...")
5. If multiple documents provide relevant information, synthesize them

Be professional and helpful."""

        # Construct user message
        if include_citations:
            user_message = f"""Context:
{context}

Question: {question}

Please provide a clear answer based on the context above, citing which document(s) you used."""
        else:
            user_message = f"Context:\n{context}\n\nQuestion: {question}"

        # Generate answer
        response = self.openai_client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.95
        )

        return response.choices[0].message.content

    def query(
        self,
        question: str,
        top_k: int = 3,
        use_hybrid_search: bool = True,
        temperature: float = 0.2,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Complete RAG pipeline: search + generate.

        Args:
            question: User question
            top_k: Number of documents to retrieve
            use_hybrid_search: Use both vector and keyword search
            temperature: Sampling temperature
            verbose: Print intermediate steps

        Returns:
            Dictionary with answer, sources, and metadata
        """
        if verbose:
            print(f"Question: {question}\n")
            print("Searching documents...")

        # Search for relevant documents
        search_results = self.search_documents(
            query=question,
            top_k=top_k,
            use_hybrid_search=use_hybrid_search
        )

        if verbose:
            print(f"Found {len(search_results)} relevant documents\n")
            for i, result in enumerate(search_results, 1):
                print(f"  {i}. {result.title} (score: {result.score:.2f})")
            print("\nGenerating answer...")

        # Generate answer
        answer = self.generate_answer(
            question=question,
            context_results=search_results,
            temperature=temperature
        )

        if verbose:
            print(f"\nAnswer: {answer}\n")

        return {
            "answer": answer,
            "sources": [
                {
                    "title": r.title,
                    "category": r.category,
                    "score": r.score,
                    "content_preview": r.content[:200] + "..." if len(r.content) > 200 else r.content
                }
                for r in search_results
            ],
            "metadata": {
                "model": self.chat_model,
                "temperature": temperature,
                "top_k": top_k,
                "hybrid_search": use_hybrid_search
            }
        }


def main():
    """Example usage of Azure OpenAI RAG"""

    # Initialize RAG client
    rag = AzureOpenAIRAG(
        openai_endpoint="https://myopenai.openai.azure.com",
        search_endpoint="https://myaisearch.search.windows.net",
        search_index_name="product-docs",
        embedding_model="text-embedding-ada-002",
        chat_model="gpt-4-turbo"
    )

    # Example questions
    questions = [
        "What are the key features of Azure Container Apps?",
        "How do I implement autoscaling for my application?",
        "What is the difference between Azure Functions and Container Apps?"
    ]

    for question in questions:
        print("=" * 80)
        result = rag.query(
            question=question,
            top_k=3,
            use_hybrid_search=True,
            temperature=0.2,
            verbose=True
        )
        print(f"\nSources used: {len(result['sources'])}")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source['title']} (score: {source['score']:.2f})")
        print("=" * 80)
        print()


if __name__ == "__main__":
    main()
