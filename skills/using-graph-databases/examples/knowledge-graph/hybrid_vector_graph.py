"""
Knowledge Graph + Vector Search Hybrid
Demonstrates combining graph relationships with vector similarity for AI/RAG applications.

This example shows how to:
1. Perform vector similarity search (find relevant concepts)
2. Expand results using graph relationships (find related concepts)
3. Combine both for context-rich retrieval
"""

from neo4j import GraphDatabase
from typing import List, Dict, Optional
import numpy as np


class KnowledgeGraphRAG:
    """
    Hybrid knowledge graph + vector search for RAG applications.

    Combines:
    - Vector similarity search (find semantically similar concepts)
    - Graph traversal (find related concepts through relationships)
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """
        Initialize Neo4j connection.

        Note: Vector embeddings can be stored in Neo4j or external vector DB.
        This example assumes embeddings are stored in Neo4j node properties.
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        """Close database connection."""
        self.driver.close()

    def create_knowledge_graph_schema(self):
        """
        Create knowledge graph schema with constraints and indexes.
        """
        queries = [
            # Constraints
            "CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",

            # Indexes
            "CREATE INDEX concept_name IF NOT EXISTS FOR (c:Concept) ON (c.name)",
            "CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name)",
            "CREATE FULLTEXT INDEX concept_search IF NOT EXISTS FOR (c:Concept) ON EACH [c.name, c.description]",
        ]

        with self.driver.session() as session:
            for query in queries:
                session.run(query)

    def add_concept(
        self,
        concept_id: str,
        name: str,
        description: str,
        embedding: List[float]
    ) -> str:
        """
        Add a concept node to the knowledge graph.

        Args:
            concept_id: Unique identifier
            name: Concept name
            description: Concept description
            embedding: Vector embedding (from sentence transformers, OpenAI, etc.)

        Returns:
            Created concept ID
        """
        query = """
        CREATE (c:Concept {
            id: $id,
            name: $name,
            description: $description,
            embedding: $embedding
        })
        RETURN c.id AS id
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                id=concept_id,
                name=name,
                description=description,
                embedding=embedding
            )
            return result.single()['id']

    def add_relationship(
        self,
        from_concept_id: str,
        to_concept_id: str,
        relationship_type: str,
        strength: float = 1.0
    ):
        """
        Add a relationship between two concepts.

        Args:
            from_concept_id: Source concept ID
            to_concept_id: Target concept ID
            relationship_type: Type (RELATED_TO, IS_A, HAS_PROPERTY, etc.)
            strength: Relationship strength (0.0 - 1.0)
        """
        query = f"""
        MATCH (c1:Concept {{id: $fromId}}), (c2:Concept {{id: $toId}})
        CREATE (c1)-[r:{relationship_type} {{strength: $strength}}]->(c2)
        RETURN r
        """

        with self.driver.session() as session:
            session.run(
                query,
                fromId=from_concept_id,
                toId=to_concept_id,
                strength=strength
            )

    def vector_similarity_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Find concepts using vector similarity (cosine similarity).

        Note: Neo4j 5.13+ supports native vector indexes. For older versions,
        this is a simple implementation. For production, use Qdrant/Pinecone/pgvector.

        Args:
            query_embedding: Query vector
            limit: Max results
            similarity_threshold: Minimum similarity score

        Returns:
            List of similar concepts with scores
        """
        query = """
        MATCH (c:Concept)
        WHERE c.embedding IS NOT NULL
        WITH c,
             gds.similarity.cosine(c.embedding, $queryEmbedding) AS similarity
        WHERE similarity >= $threshold
        RETURN
            c.id AS id,
            c.name AS name,
            c.description AS description,
            similarity
        ORDER BY similarity DESC
        LIMIT $limit
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                queryEmbedding=query_embedding,
                threshold=similarity_threshold,
                limit=limit
            )
            return [dict(record) for record in result]

    def expand_with_graph_context(
        self,
        concept_ids: List[str],
        max_depth: int = 2,
        relationship_types: Optional[List[str]] = None
    ) -> Dict:
        """
        Expand initial results with graph relationships.

        This is where graph databases shine: enriching vector search results
        with structured relationships.

        Args:
            concept_ids: Starting concept IDs (from vector search)
            max_depth: How many hops to traverse
            relationship_types: Filter by specific relationships (optional)

        Returns:
            Dict with expanded concepts and relationships
        """
        # Build relationship filter
        rel_filter = ""
        if relationship_types:
            rel_filter = ":" + "|:".join(relationship_types)

        query = f"""
        MATCH (c:Concept) WHERE c.id IN $conceptIds

        // Traverse graph to find related concepts
        OPTIONAL MATCH path = (c)-[r{rel_filter}*1..$maxDepth]-(related:Concept)

        // Collect results
        WITH c, related, relationships(path) AS rels
        WHERE related IS NOT NULL

        RETURN
            c.id AS source_id,
            c.name AS source_name,
            collect(DISTINCT {{
                id: related.id,
                name: related.name,
                description: related.description,
                depth: size(rels),
                relationship_path: [r IN rels | type(r)]
            }}) AS related_concepts
        """

        with self.driver.session() as session:
            result = session.run(query, conceptIds=concept_ids, maxDepth=max_depth)
            return {record['source_id']: record for record in result}

    def hybrid_search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        expand_depth: int = 2,
        vector_weight: float = 0.7,
        graph_weight: float = 0.3
    ) -> List[Dict]:
        """
        Hybrid search: Combine vector similarity + graph traversal.

        Strategy:
        1. Vector search finds semantically similar concepts
        2. Graph traversal expands with related concepts
        3. Combine scores with weighted averaging

        Args:
            query_embedding: Query vector
            limit: Max results from vector search
            expand_depth: How far to traverse graph
            vector_weight: Weight for vector similarity score
            graph_weight: Weight for graph relationship score

        Returns:
            Combined results ranked by hybrid score
        """
        # Step 1: Vector similarity search
        vector_results = self.vector_similarity_search(
            query_embedding,
            limit=limit,
            similarity_threshold=0.5
        )

        if not vector_results:
            return []

        # Extract concept IDs
        concept_ids = [r['id'] for r in vector_results]

        # Step 2: Expand with graph context
        graph_expansion = self.expand_with_graph_context(
            concept_ids,
            max_depth=expand_depth,
            relationship_types=['RELATED_TO', 'IS_A', 'HAS_PROPERTY']
        )

        # Step 3: Combine results
        combined = []

        # Add direct vector results
        for result in vector_results:
            combined.append({
                'id': result['id'],
                'name': result['name'],
                'description': result['description'],
                'vector_score': result['similarity'],
                'graph_score': 1.0,  # Direct match
                'hybrid_score': (vector_weight * result['similarity']) + (graph_weight * 1.0),
                'source': 'direct'
            })

        # Add expanded graph results
        for source_id, expansion in graph_expansion.items():
            source_score = next(r['similarity'] for r in vector_results if r['id'] == source_id)

            for related in expansion['related_concepts']:
                # Calculate graph score based on depth (closer = higher score)
                graph_score = 1.0 / related['depth']

                # Check if already in combined results
                existing = next((c for c in combined if c['id'] == related['id']), None)
                if existing:
                    # Update scores if better
                    existing['graph_score'] = max(existing['graph_score'], graph_score)
                else:
                    # Add new related concept
                    combined.append({
                        'id': related['id'],
                        'name': related['name'],
                        'description': related['description'],
                        'vector_score': source_score * 0.8,  # Inherited from source
                        'graph_score': graph_score,
                        'hybrid_score': (vector_weight * source_score * 0.8) + (graph_weight * graph_score),
                        'source': 'expanded',
                        'relationship_path': ' -> '.join(related['relationship_path'])
                    })

        # Sort by hybrid score
        combined.sort(key=lambda x: x['hybrid_score'], reverse=True)

        return combined[:limit * 2]  # Return more results due to expansion

    def get_context_for_llm(
        self,
        query_embedding: List[float],
        max_concepts: int = 10
    ) -> str:
        """
        Generate context for LLM prompt using hybrid search.

        This is the core RAG function: retrieve relevant context from
        knowledge graph to augment LLM prompts.

        Args:
            query_embedding: User query embedding
            max_concepts: Maximum concepts to include

        Returns:
            Formatted context string for LLM
        """
        results = self.hybrid_search(query_embedding, limit=max_concepts)

        context_parts = []
        context_parts.append("# Relevant Knowledge Graph Context\n")

        for i, result in enumerate(results[:max_concepts], 1):
            context_parts.append(f"\n## {i}. {result['name']}")
            context_parts.append(f"{result['description']}")

            if result['source'] == 'expanded':
                context_parts.append(f"_Related via: {result['relationship_path']}_")

            context_parts.append(f"_Relevance: {result['hybrid_score']:.2f}_")

        return '\n'.join(context_parts)


def example_usage():
    """
    Example: Building a knowledge graph for a technical domain.
    """
    # Initialize
    kg = KnowledgeGraphRAG(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    try:
        # Setup schema
        kg.create_knowledge_graph_schema()

        # Add concepts (with mock embeddings - use real embeddings in production)
        concepts = [
            {
                'id': 'c1',
                'name': 'Graph Databases',
                'description': 'Database systems that use graph structures for semantic queries',
                'embedding': np.random.rand(384).tolist()  # Mock 384-dim embedding
            },
            {
                'id': 'c2',
                'name': 'Neo4j',
                'description': 'Popular graph database using Cypher query language',
                'embedding': np.random.rand(384).tolist()
            },
            {
                'id': 'c3',
                'name': 'Cypher',
                'description': 'Declarative graph query language for Neo4j',
                'embedding': np.random.rand(384).tolist()
            },
            {
                'id': 'c4',
                'name': 'Recommendation Engines',
                'description': 'Systems that predict user preferences using collaborative filtering',
                'embedding': np.random.rand(384).tolist()
            },
        ]

        for concept in concepts:
            kg.add_concept(**concept)

        # Add relationships
        kg.add_relationship('c2', 'c1', 'IS_A', strength=1.0)
        kg.add_relationship('c2', 'c3', 'USES', strength=1.0)
        kg.add_relationship('c1', 'c4', 'ENABLES', strength=0.8)

        # Hybrid search example
        query_embedding = np.random.rand(384).tolist()
        results = kg.hybrid_search(query_embedding, limit=5)

        print("\n=== Hybrid Search Results ===")
        for result in results:
            print(f"\n{result['name']} (score: {result['hybrid_score']:.3f})")
            print(f"  {result['description']}")
            print(f"  Source: {result['source']}")

        # Get LLM context
        context = kg.get_context_for_llm(query_embedding, max_concepts=3)
        print("\n=== Generated LLM Context ===")
        print(context)

    finally:
        kg.close()


if __name__ == "__main__":
    example_usage()
