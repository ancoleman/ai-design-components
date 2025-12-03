"""
LangChain Agent Example

Demonstrates ReAct agent with tools for document search and calculations.
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
import os

# Initialize LLM
# For vLLM: ChatOpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Initialize vector store (requires Qdrant running)
def init_vector_store():
    """Initialize Qdrant vector store for document search."""
    try:
        client = QdrantClient(url="http://localhost:6333")
        embeddings = OpenAIEmbeddings()

        vectorstore = Qdrant(
            client=client,
            collection_name="documents",
            embeddings=embeddings
        )

        return vectorstore
    except Exception as e:
        print(f"Warning: Could not connect to Qdrant: {e}")
        print("Document search tool will be disabled.")
        return None

vectorstore = init_vector_store()

# Define tools
def search_documents(query: str) -> str:
    """
    Search documentation for technical information.

    Use this tool when the user asks about technical concepts,
    API documentation, or implementation details.
    """
    if vectorstore is None:
        return "Document search unavailable (Qdrant not running)"

    try:
        results = vectorstore.similarity_search(query, k=3)

        if not results:
            return "No relevant documents found."

        # Format results
        formatted = []
        for i, doc in enumerate(results, 1):
            formatted.append(f"Document {i}:\n{doc.page_content}\n")

        return "\n".join(formatted)
    except Exception as e:
        return f"Search error: {e}"

def calculate(expression: str) -> str:
    """
    Calculate mathematical expressions.

    Input should be a valid Python expression.
    Example: "8 * 1000000000 * 2 / (1024**3)"
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Calculation error: {e}. Ensure expression is valid Python."

def get_current_weather(location: str) -> str:
    """
    Get current weather for a location.

    This is a mock tool for demonstration.
    In production, integrate with weather API.
    """
    # Mock response
    return f"Weather in {location}: Sunny, 72°F"

# Create tool list
tools = [
    Tool(
        name="SearchDocs",
        func=search_documents,
        description="Search technical documentation for information about vLLM, PagedAttention, model serving, and related concepts. Input should be a search query."
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Calculate mathematical expressions. Input should be a valid Python expression like '8 * 2 / 3' or '2048 * 0.9'."
    ),
    Tool(
        name="Weather",
        func=get_current_weather,
        description="Get current weather for a location. Input should be a city name."
    )
]

# Create ReAct agent
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

def run_agent(query: str):
    """Run agent on a query."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)

    try:
        result = agent_executor.invoke({"input": query})
        print(f"\nFinal Answer: {result['output']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("LangChain ReAct Agent Example")
    print("=" * 60)

    # Example 1: Simple calculation
    run_agent("Calculate 2048 * 0.9")

    # Example 2: Document search (requires Qdrant)
    run_agent("What is PagedAttention and how does it work?")

    # Example 3: Multi-step reasoning
    run_agent(
        "What is PagedAttention? After explaining, calculate the GPU memory "
        "needed for Llama-3.1-8B in FP16 (8 billion parameters × 2 bytes per parameter)"
    )

    # Example 4: Multiple tools
    run_agent(
        "Search for information about vLLM performance optimizations, "
        "then calculate 70 billion parameters × 0.5 bytes (INT4 quantization)"
    )

    # Example 5: Weather (mock tool)
    run_agent("What's the weather in San Francisco?")

    # Interactive mode
    print("\n" + "=" * 60)
    print("Interactive Mode (type 'quit' to exit)")
    print("=" * 60)

    while True:
        query = input("\nYour query: ").strip()

        if query.lower() in ["quit", "exit", "q"]:
            break

        if query:
            run_agent(query)
