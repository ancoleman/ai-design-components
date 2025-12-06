"""
Smart Content-Aware Chunking

Demonstrates recursive chunking strategies for different content types.

Dependencies:
    pip install langchain-text-splitters

Usage:
    python smart_chunker.py
"""

from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter


class SmartChunker:
    """Content-aware chunking with recursive splitting."""

    # Separators for different content types
    SEPARATORS = {
        'markdown': ['\n## ', '\n### ', '\n#### ', '\n\n', '\n', ' ', ''],
        'code_python': ['\nclass ', '\ndef ', '\n\n', '\n', ' ', ''],
        'code_js': ['\nfunction ', '\nconst ', '\nclass ', '\nexport ', '\n\n', '\n', ' ', ''],
        'plaintext': ['\n\n', '\n', '. ', ' ', ''],
        'legal': ['\n\n', '. ', ' ', ''],  # Preserve full sentences
    }

    def __init__(self, content_type: str = 'plaintext'):
        """
        Initialize chunker for specific content type.

        Args:
            content_type: 'markdown', 'code_python', 'code_js', 'plaintext', 'legal'
        """
        self.content_type = content_type
        self.separators = self.SEPARATORS.get(content_type, self.SEPARATORS['plaintext'])

    def chunk(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 100
    ) -> List[str]:
        """
        Split text into chunks using recursive splitting.

        Args:
            text: Input text to chunk
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks (prevents context loss)

        Returns:
            List of text chunks
        """
        splitter = RecursiveCharacterTextSplitter(
            separators=self.separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

        chunks = splitter.split_text(text)
        return chunks

    def chunk_with_metadata(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        source_metadata: Dict = None
    ) -> List[Dict]:
        """
        Chunk text and attach metadata to each chunk.

        Args:
            text: Input text
            chunk_size: Target chunk size
            chunk_overlap: Overlap size
            source_metadata: Metadata to attach (e.g., document_id, title)

        Returns:
            List of dicts with 'text' and 'metadata' keys
        """
        chunks = self.chunk(text, chunk_size, chunk_overlap)

        result = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = source_metadata.copy() if source_metadata else {}
            chunk_metadata.update({
                'chunk_index': i,
                'total_chunks': len(chunks),
                'chunk_size': len(chunk),
                'content_type': self.content_type
            })

            result.append({
                'text': chunk,
                'metadata': chunk_metadata
            })

        return result

    def analyze_chunks(self, chunks: List[str]) -> Dict:
        """
        Analyze chunk quality metrics.

        Args:
            chunks: List of text chunks

        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {}

        sizes = [len(chunk) for chunk in chunks]

        return {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(sizes) / len(sizes),
            'min_chunk_size': min(sizes),
            'max_chunk_size': max(sizes),
            'total_chars': sum(sizes)
        }


def example_markdown():
    """Example: Chunking markdown documentation."""
    print("\n1. Markdown Documentation Chunking")
    print("=" * 60)

    markdown_text = """
# Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that enables systems to learn from data.

## Supervised Learning

Supervised learning uses labeled data to train models. Common algorithms include:

### Linear Regression

Linear regression predicts continuous values by fitting a line to the data.

### Decision Trees

Decision trees split data based on feature values to make predictions.

## Unsupervised Learning

Unsupervised learning finds patterns in unlabeled data.

### K-Means Clustering

K-means groups similar data points into clusters.

### Principal Component Analysis

PCA reduces dimensionality while preserving variance.
"""

    chunker = SmartChunker(content_type='markdown')
    chunks = chunker.chunk(markdown_text, chunk_size=200, chunk_overlap=50)

    print(f"Original text: {len(markdown_text)} characters")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({len(chunk)} chars):")
        print(chunk[:100] + "..." if len(chunk) > 100 else chunk)

    stats = chunker.analyze_chunks(chunks)
    print(f"\nChunk Statistics:")
    print(f"  Average size: {stats['avg_chunk_size']:.0f} chars")
    print(f"  Min size: {stats['min_chunk_size']} chars")
    print(f"  Max size: {stats['max_chunk_size']} chars")


def example_code():
    """Example: Chunking Python code."""
    print("\n2. Python Code Chunking")
    print("=" * 60)

    python_code = """
class DataProcessor:
    \"\"\"Process and transform data.\"\"\"

    def __init__(self, config):
        self.config = config

    def load_data(self, filepath):
        \"\"\"Load data from file.\"\"\"
        with open(filepath, 'r') as f:
            return f.read()

    def transform(self, data):
        \"\"\"Transform raw data.\"\"\"
        return data.strip().lower()

def main():
    \"\"\"Main entry point.\"\"\"
    processor = DataProcessor(config={})
    data = processor.load_data('data.txt')
    transformed = processor.transform(data)
    print(transformed)

if __name__ == "__main__":
    main()
"""

    chunker = SmartChunker(content_type='code_python')
    chunks = chunker.chunk(python_code, chunk_size=300, chunk_overlap=50)

    print(f"Original code: {len(python_code)} characters")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({len(chunk)} chars):")
        print(chunk)

    print("\nNote: Code chunks preserve function/class boundaries")


def example_with_metadata():
    """Example: Chunking with metadata attachment."""
    print("\n3. Chunking with Metadata")
    print("=" * 60)

    text = """
Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. These machines are programmed to think like humans and mimic their actions.

Machine Learning is a subset of AI that enables machines to learn from data without being explicitly programmed. It uses algorithms to parse data, learn from it, and make determinations or predictions.

Deep Learning is a subset of machine learning that uses neural networks with multiple layers. These networks can learn complex patterns in large amounts of data.
"""

    chunker = SmartChunker(content_type='plaintext')

    # Chunk with metadata
    chunks_with_meta = chunker.chunk_with_metadata(
        text=text,
        chunk_size=150,
        chunk_overlap=30,
        source_metadata={
            'document_id': 'doc_123',
            'title': 'AI Overview',
            'author': 'Data Science Team',
            'category': 'technical'
        }
    )

    print(f"Total chunks: {len(chunks_with_meta)}")

    for chunk_data in chunks_with_meta:
        print(f"\nChunk {chunk_data['metadata']['chunk_index'] + 1}:")
        print(f"  Text: {chunk_data['text'][:80]}...")
        print(f"  Metadata: {chunk_data['metadata']}")


def example_overlap_comparison():
    """Example: Comparing different overlap sizes."""
    print("\n4. Overlap Size Comparison")
    print("=" * 60)

    text = "The quick brown fox jumps over the lazy dog. " * 10  # 450 chars

    chunker = SmartChunker(content_type='plaintext')

    for overlap in [0, 25, 50]:
        chunks = chunker.chunk(text, chunk_size=100, chunk_overlap=overlap)
        print(f"\nOverlap: {overlap} chars")
        print(f"  Chunks created: {len(chunks)}")
        print(f"  Chunk 1: {chunks[0]}")
        if len(chunks) > 1:
            print(f"  Chunk 2: {chunks[1]}")
            # Show overlap
            overlap_text = chunks[0][-overlap:] if overlap > 0 else ""
            print(f"  Overlap text: '{overlap_text}'")


def example_content_type_detection():
    """Example: Auto-detect content type."""
    print("\n5. Content Type Auto-Detection")
    print("=" * 60)

    def detect_content_type(text: str) -> str:
        """Simple content type detection."""
        if 'def ' in text or 'class ' in text:
            return 'code_python'
        elif '# ' in text or '## ' in text:
            return 'markdown'
        else:
            return 'plaintext'

    samples = {
        'markdown': "# Heading\n\nParagraph text here.",
        'code': "def function():\n    return 42",
        'plaintext': "Just some regular text without special formatting."
    }

    for name, text in samples.items():
        detected = detect_content_type(text)
        print(f"\nSample: {name}")
        print(f"  Detected: {detected}")
        print(f"  Text: {text[:50]}...")


def main():
    """Run all chunking examples."""

    print("Smart Content-Aware Chunking Demo")
    print("=" * 60)

    example_markdown()
    example_code()
    example_with_metadata()
    example_overlap_comparison()
    example_content_type_detection()

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("\nKey Takeaways:")
    print("  1. Choose separators based on content type")
    print("  2. Use overlap (10-20%) to prevent context loss")
    print("  3. Attach metadata for tracking chunk provenance")
    print("  4. Analyze chunk sizes to ensure quality")


if __name__ == "__main__":
    main()
