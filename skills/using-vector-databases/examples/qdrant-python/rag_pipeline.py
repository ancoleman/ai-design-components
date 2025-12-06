"""
Complete RAG pipeline implementation with Qdrant.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from typing import List, Dict, Optional
import tiktoken
import uuid
import os


class RAGPipeline:
    def __init__(
        self,
        qdrant_url: str = "localhost",
        qdrant_port: int = 6333,
        collection_name: str = "documents",
        embedding_model: str = "text-embedding-3-large"
    ):
        self.client = QdrantClient(qdrant_url, port=qdrant_port)
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4-turbo-preview"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.1"))
        )

        # Initialize collection
        self._init_collection()

    def _init_collection(self):
        """Create collection if it doesn't exist."""
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # Get embedding dimensions
            test_embedding = self.embeddings.embed_query("test")
            vector_size = len(test_embedding)

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def _chunk_text(self, text: str) -> List[str]:
        """Chunk text using token-based splitting."""
        def tiktoken_len(text):
            tokenizer = tiktoken.get_encoding('cl100k_base')
            return len(tokenizer.encode(text, disallowed_special=()))

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=int(os.getenv("CHUNK_SIZE", "512")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50")),
            length_function=tiktoken_len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        return splitter.split_text(text)

    def ingest_document(
        self,
        file_path: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Ingest a document into the vector database."""
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Chunk document
        chunks = self._chunk_text(content)

        # Generate embeddings
        embeddings = self.embeddings.embed_documents(chunks)

        # Prepare points
        points = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_metadata = {
                "text": chunk,
                "source": file_path,
                "chunk_index": idx,
                "total_chunks": len(chunks),
                **(metadata or {})
            }

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=point_metadata
                )
            )

        # Upsert to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True
        )

        return {
            "file_path": file_path,
            "chunks_created": len(chunks),
            "total_tokens": sum(len(c.split()) for c in chunks)
        }

    def search(
        self,
        query: str,
        limit: int = 5,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for relevant documents."""
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)

        # Build filter
        query_filter = None
        if filter:
            conditions = [
                FieldCondition(
                    key=key,
                    match=MatchValue(value=value)
                )
                for key, value in filter.items()
            ]
            query_filter = Filter(must=conditions)

        # Search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter=query_filter,
            with_payload=True
        )

        return [
            {
                "text": r.payload["text"],
                "score": r.score,
                "metadata": {
                    k: v for k, v in r.payload.items()
                    if k != "text"
                }
            }
            for r in results
        ]

    def generate_answer(
        self,
        query: str,
        limit: int = 5,
        filter: Optional[Dict] = None
    ) -> Dict:
        """Generate an answer using RAG."""
        # Retrieve relevant documents
        search_results = self.search(query, limit, filter)

        # Build context
        context = "\n\n".join([
            f"Source: {r['metadata'].get('source', 'unknown')}\n{r['text']}"
            for r in search_results
        ])

        # Generate answer
        prompt = f"""Answer the following question based only on the provided context.
If the context doesn't contain enough information, say "I don't have enough information to answer that."

Context:
{context}

Question: {query}

Answer:"""

        response = self.llm.predict(prompt)

        return {
            "answer": response,
            "sources": search_results
        }
