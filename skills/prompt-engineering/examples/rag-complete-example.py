"""
Complete RAG (Retrieval-Augmented Generation) Implementation

A production-ready RAG system demonstrating:
- Document chunking
- Embedding generation
- Vector search
- Context assembly
- Answer generation with citations
- Full working example

Installation:
    pip install openai chromadb pypdf sentence-transformers

Usage:
    export OPENAI_API_KEY="your-api-key"
    python rag-complete-example.py
"""

import os
import hashlib
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from openai import OpenAI


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class RAGConfig:
    """RAG system configuration."""
    chunk_size: int = 512
    chunk_overlap: int = 100
    top_k: int = 5
    model: str = "gpt-4"
    embedding_model: str = "text-embedding-3-small"
    temperature: float = 0.3


# ============================================================================
# Document Processing
# ============================================================================

class DocumentChunker:
    """Split documents into chunks for embedding."""

    def __init__(self, chunk_size: int = 512, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            metadata: Optional metadata (source, date, etc.)

        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                for punctuation in ['. ', '! ', '? ', '\n\n']:
                    last_punct = text.rfind(punctuation, start, end)
                    if last_punct > start:
                        end = last_punct + len(punctuation)
                        break

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk = {
                    'text': chunk_text,
                    'start_pos': start,
                    'end_pos': end,
                    'chunk_id': len(chunks)
                }

                # Add metadata if provided
                if metadata:
                    chunk.update(metadata)

                chunks.append(chunk)

            start = end - self.overlap

        return chunks


# ============================================================================
# Vector Store (using ChromaDB)
# ============================================================================

class VectorStore:
    """Vector database for storing and retrieving embeddings."""

    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.client = OpenAI()
        self.embedding_model = embedding_model
        self.documents: List[Dict] = []
        self.embeddings: List[List[float]] = []

    def add_documents(self, chunks: List[Dict]):
        """
        Add documents to the vector store.

        Args:
            chunks: List of document chunks with text and metadata
        """
        print(f"Adding {len(chunks)} chunks to vector store...")

        for chunk in chunks:
            # Generate embedding
            embedding = self._get_embedding(chunk['text'])

            # Store
            self.documents.append(chunk)
            self.embeddings.append(embedding)

        print(f"Vector store now contains {len(self.documents)} chunks")

    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for most similar documents.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of (document, similarity_score) tuples
        """
        # Get query embedding
        query_embedding = self._get_embedding(query)

        # Calculate cosine similarity
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((self.documents[i], similarity))

        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (magnitude1 * magnitude2)


# ============================================================================
# RAG System
# ============================================================================

class RAGSystem:
    """Complete RAG system for question-answering."""

    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        self.client = OpenAI()
        self.chunker = DocumentChunker(
            chunk_size=self.config.chunk_size,
            overlap=self.config.chunk_overlap
        )
        self.vector_store = VectorStore(
            embedding_model=self.config.embedding_model
        )

    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Add documents to the knowledge base.

        Args:
            documents: List of dicts with 'text' and optional metadata
        """
        all_chunks = []

        for doc in documents:
            # Extract text and metadata
            text = doc['text']
            metadata = {k: v for k, v in doc.items() if k != 'text'}

            # Chunk document
            chunks = self.chunker.chunk_text(text, metadata)
            all_chunks.extend(chunks)

        # Add to vector store
        self.vector_store.add_documents(all_chunks)

    def query(self, question: str, return_sources: bool = True) -> Dict:
        """
        Answer a question using RAG.

        Args:
            question: User question
            return_sources: Whether to return source documents

        Returns:
            Dictionary with answer and optional sources
        """
        # Step 1: Retrieve relevant documents
        retrieved_docs = self.vector_store.search(
            question,
            top_k=self.config.top_k
        )

        # Step 2: Format context
        context = self._format_context(retrieved_docs)

        # Step 3: Generate answer
        answer = self._generate_answer(question, context)

        result = {'answer': answer}

        if return_sources:
            result['sources'] = [
                {
                    'text': doc['text'][:200] + '...',  # Preview
                    'source': doc.get('source', 'unknown'),
                    'similarity': score
                }
                for doc, score in retrieved_docs
            ]

        return result

    def _format_context(self, retrieved_docs: List[Tuple[Dict, float]]) -> str:
        """Format retrieved documents as context."""
        context_parts = []

        for i, (doc, score) in enumerate(retrieved_docs):
            source = doc.get('source', 'Unknown')
            text = doc['text']

            context_parts.append(f"""
[Document {i+1}]
Source: {source}
Relevance: {score:.2f}
Content: {text}
""")

        return "\n".join(context_parts)

    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using LLM."""
        system_prompt = """
You are a helpful AI assistant that answers questions based on provided context.

IMPORTANT RULES:
1. Answer ONLY using information from the provided documents
2. Cite sources using [Document N] notation
3. If the answer is not in the documents, say "I don't have enough information to answer this question."
4. Be concise but complete
5. Use direct quotes when appropriate
"""

        user_prompt = f"""
Context:
{context}

Question: {question}

Answer (with citations):
"""

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.config.temperature,
            max_tokens=1024
        )

        return response.choices[0].message.content


# ============================================================================
# Advanced RAG Features
# ============================================================================

class AdvancedRAG(RAGSystem):
    """RAG system with advanced features."""

    def query_with_rerank(self, question: str) -> Dict:
        """
        Query with re-ranking for better relevance.

        Uses a two-stage retrieval:
        1. Retrieve top-K candidates (e.g., 20)
        2. Re-rank to select best top-N (e.g., 5)
        """
        # Stage 1: Retrieve more candidates
        candidates = self.vector_store.search(question, top_k=20)

        # Stage 2: Re-rank (simplified - in production use cross-encoder)
        reranked = self._rerank(question, candidates)

        # Use top-k after reranking
        top_docs = reranked[:self.config.top_k]

        # Generate answer
        context = self._format_context(top_docs)
        answer = self._generate_answer(question, context)

        return {
            'answer': answer,
            'sources': [
                {
                    'text': doc['text'][:200] + '...',
                    'source': doc.get('source', 'unknown'),
                    'similarity': score
                }
                for doc, score in top_docs
            ]
        }

    def _rerank(
        self,
        query: str,
        candidates: List[Tuple[Dict, float]]
    ) -> List[Tuple[Dict, float]]:
        """
        Re-rank candidates for better relevance.

        Simplified reranking - in production, use a cross-encoder model.
        """
        # For this example, we'll just boost scores based on exact keyword matches
        query_keywords = set(query.lower().split())

        reranked = []
        for doc, score in candidates:
            # Calculate keyword overlap
            doc_keywords = set(doc['text'].lower().split())
            overlap = len(query_keywords & doc_keywords)

            # Boost score
            boosted_score = score * (1 + 0.1 * overlap)
            reranked.append((doc, boosted_score))

        # Sort by boosted score
        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked

    def conversational_query(
        self,
        question: str,
        conversation_history: List[Dict]
    ) -> Dict:
        """
        Query with conversation history for context.

        Args:
            question: Current question
            conversation_history: List of previous Q&A pairs

        Returns:
            Answer with updated conversation history
        """
        # Retrieve relevant documents
        retrieved_docs = self.vector_store.search(question, top_k=self.config.top_k)
        context = self._format_context(retrieved_docs)

        # Build conversation with history
        messages = [
            {
                "role": "system",
                "content": """You are a helpful AI assistant that answers questions
based on provided context. Maintain context from previous conversation."""
            }
        ]

        # Add conversation history
        for item in conversation_history[-3:]:  # Last 3 turns
            messages.append({"role": "user", "content": item['question']})
            messages.append({"role": "assistant", "content": item['answer']})

        # Add current query
        messages.append({
            "role": "user",
            "content": f"""
Context:
{context}

Question: {question}

Answer (with citations):
"""
        })

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature
        )

        answer = response.choices[0].message.content

        return {
            'answer': answer,
            'sources': [
                {'text': doc['text'][:200] + '...', 'source': doc.get('source', 'unknown')}
                for doc, _ in retrieved_docs
            ]
        }


# ============================================================================
# Example Usage
# ============================================================================

def demo_basic_rag():
    """Demonstrate basic RAG functionality."""
    print("\n" + "=" * 60)
    print("DEMO: Basic RAG System")
    print("=" * 60)

    # Initialize RAG system
    rag = RAGSystem()

    # Add sample documents
    documents = [
        {
            'text': """
Python is a high-level, interpreted programming language known for its
clear syntax and readability. It was created by Guido van Rossum and
first released in 1991. Python supports multiple programming paradigms
including procedural, object-oriented, and functional programming.
""",
            'source': 'python_intro.txt',
            'date': '2024-01-15'
        },
        {
            'text': """
Machine learning is a subset of artificial intelligence that enables
systems to learn and improve from experience without being explicitly
programmed. It focuses on developing computer programs that can access
data and use it to learn for themselves.
""",
            'source': 'ml_basics.txt',
            'date': '2024-01-20'
        },
        {
            'text': """
Neural networks are computing systems inspired by biological neural
networks in animal brains. They consist of interconnected nodes (neurons)
organized in layers. Deep learning uses neural networks with many layers
to learn from large amounts of data.
""",
            'source': 'neural_networks.txt',
            'date': '2024-01-25'
        }
    ]

    print("\nAdding documents to knowledge base...")
    rag.add_documents(documents)

    # Query the system
    questions = [
        "Who created Python?",
        "What is machine learning?",
        "How do neural networks work?"
    ]

    for question in questions:
        print(f"\n{'─' * 60}")
        print(f"Question: {question}")
        print(f"{'─' * 60}")

        result = rag.query(question)

        print(f"\nAnswer:\n{result['answer']}")

        print("\nSources:")
        for i, source in enumerate(result['sources'], 1):
            print(f"\n{i}. {source['source']} (Similarity: {source['similarity']:.3f})")
            print(f"   {source['text']}")


def demo_advanced_rag():
    """Demonstrate advanced RAG features."""
    print("\n" + "=" * 60)
    print("DEMO: Advanced RAG with Re-ranking")
    print("=" * 60)

    # Initialize advanced RAG
    rag = AdvancedRAG()

    # Add technical documentation
    documents = [
        {
            'text': """
FastAPI is a modern, fast web framework for building APIs with Python 3.7+
based on standard Python type hints. It's one of the fastest Python frameworks
available, comparable to NodeJS and Go. Key features include automatic API
documentation, data validation using Pydantic, and async support.
""",
            'source': 'fastapi_docs.md'
        },
        {
            'text': """
Django is a high-level Python web framework that encourages rapid development
and clean, pragmatic design. It follows the model-template-view (MTV) architectural
pattern. Django includes an ORM, authentication system, and admin interface
out of the box.
""",
            'source': 'django_docs.md'
        },
        {
            'text': """
Flask is a lightweight WSGI web application framework in Python. It's designed
to make getting started quick and easy, with the ability to scale up to complex
applications. Flask is considered more Pythonic than Django because it's explicit
and doesn't make many decisions for you.
""",
            'source': 'flask_docs.md'
        }
    ]

    print("\nAdding documents...")
    rag.add_documents(documents)

    # Query with re-ranking
    question = "Which Python web framework is fastest?"
    print(f"\nQuestion: {question}")

    result = rag.query_with_rerank(question)

    print(f"\nAnswer:\n{result['answer']}")

    print("\nTop Sources (after re-ranking):")
    for i, source in enumerate(result['sources'], 1):
        print(f"{i}. {source['source']} (Score: {source['similarity']:.3f})")


def demo_conversational_rag():
    """Demonstrate conversational RAG."""
    print("\n" + "=" * 60)
    print("DEMO: Conversational RAG")
    print("=" * 60)

    rag = AdvancedRAG()

    # Add context
    documents = [
        {
            'text': """
React is a JavaScript library for building user interfaces, maintained by
Facebook. It uses a component-based architecture and a virtual DOM for
efficient updates. React introduced the concept of JSX, a syntax extension
that allows writing HTML-like code in JavaScript.
""",
            'source': 'react_guide.md'
        }
    ]

    rag.add_documents(documents)

    # Conversation
    conversation_history = []

    questions = [
        "What is React?",
        "Who maintains it?",
        "What is JSX?"
    ]

    for question in questions:
        print(f"\n{'─' * 60}")
        print(f"User: {question}")

        result = rag.conversational_query(question, conversation_history)

        print(f"Assistant: {result['answer']}")

        # Update history
        conversation_history.append({
            'question': question,
            'answer': result['answer']
        })


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all demos."""
    print("Complete RAG System Demo")
    print("=" * 60)

    try:
        demo_basic_rag()
        demo_advanced_rag()
        demo_conversational_rag()

        print("\n" + "=" * 60)
        print("All demos completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        exit(1)

    main()
