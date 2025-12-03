# LangChain Agent Example

Demonstrates building ReAct agents with tools for document search, calculations, and API integration.

## Features

- ReAct (Reasoning + Acting) agent pattern
- Tool integration (document search, calculator, weather)
- Multi-step reasoning
- Interactive mode

## Prerequisites

1. **Python 3.8+**
2. **OpenAI API key** (or vLLM server)
3. **Qdrant vector database** (optional, for document search)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY=your_key_here

# Or use vLLM (modify main.py to use vLLM endpoint)
```

## Setup

### Option 1: With Qdrant (Full Features)

```bash
# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Index documents (see ../langchain-rag-qdrant/ example)
python index_documents.py

# Run agent
python main.py
```

### Option 2: Without Qdrant (Calculator + Weather Only)

```bash
# Run agent (document search will be disabled)
python main.py
```

## Usage

### Run Examples

```bash
python main.py
```

This will run several example queries:
1. Simple calculation
2. Document search
3. Multi-step reasoning (search + calculate)
4. Multiple tool usage

### Interactive Mode

After examples, enter interactive mode:

```
Your query: What is PagedAttention and calculate 8B × 2 bytes
```

### Example Agent Reasoning

**Query:** "What is PagedAttention? Then calculate GPU memory for 8B params × 2 bytes"

**Agent Execution:**
```
Thought: I need to first search for PagedAttention information
Action: SearchDocs
Action Input: PagedAttention

Observation: [Document search results about PagedAttention]

Thought: Now I need to calculate GPU memory
Action: Calculator
Action Input: 8000000000 * 2 / (1024**3)

Observation: 14.90 GB

Thought: I have all information needed
Final Answer: PagedAttention is a memory optimization technique...
GPU memory needed: approximately 14.9 GB.
```

## Custom Tools

### Add Your Own Tool

```python
from langchain.tools import Tool

def my_custom_tool(input_str: str) -> str:
    """Your custom tool logic."""
    # Process input
    result = process(input_str)
    return result

tools.append(
    Tool(
        name="MyTool",
        func=my_custom_tool,
        description="Description of when to use this tool. Be specific!"
    )
)
```

### Example: Database Query Tool

```python
import sqlite3

def query_database(query: str) -> str:
    """Query SQLite database for user information."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return str(results)
    except Exception as e:
        return f"Database error: {e}"
    finally:
        conn.close()

tools.append(
    Tool(
        name="DatabaseQuery",
        func=query_database,
        description="Query the user database. Input should be a valid SQL SELECT statement."
    )
)
```

### Example: API Integration

```python
import requests

def search_web(query: str) -> str:
    """Search the web using external API."""
    response = requests.get(
        "https://api.example.com/search",
        params={"q": query}
    )
    return response.json()["results"]

tools.append(
    Tool(
        name="WebSearch",
        func=search_web,
        description="Search the web for current information. Input should be a search query."
    )
)
```

## Using with vLLM

Replace OpenAI with vLLM endpoint:

```python
from langchain_openai import ChatOpenAI

# Instead of: llm = ChatOpenAI(model="gpt-4o")
llm = ChatOpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
    model="meta-llama/Llama-3.1-8B-Instruct"
)
```

## Agent Types

### ReAct (Used in Example)

**Best for:**
- General-purpose reasoning
- Multi-step tasks
- Combining search + actions

**How it works:**
1. Thought: Reason about what to do
2. Action: Choose tool to use
3. Observation: See tool result
4. Repeat until answer found

### Structured Tool Calling

For models with native tool calling (GPT-4o, Claude 3.5):

```python
from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(llm, tools, prompt)
```

**Advantages:**
- More reliable tool selection
- Better error handling
- Faster execution

### Plan-and-Execute

For complex multi-step tasks:

```python
from langchain.agents import create_plan_and_execute_agent

agent = create_plan_and_execute_agent(llm, tools)
```

**How it works:**
1. Plan: Create step-by-step plan
2. Execute: Run each step with tools
3. Re-plan: Adjust based on results

## Best Practices

1. **Write Clear Tool Descriptions:**
   - Be specific about inputs and outputs
   - Include examples in description
   - Explain when to use the tool

2. **Handle Errors in Tools:**
   ```python
   def my_tool(input_str: str) -> str:
       try:
           result = process(input_str)
           return result
       except Exception as e:
           return f"Error: {e}. Try a different approach."
   ```

3. **Limit Agent Iterations:**
   ```python
   agent_executor = AgentExecutor(
       agent=agent,
       tools=tools,
       max_iterations=5,  # Prevent infinite loops
       handle_parsing_errors=True
   )
   ```

4. **Monitor Token Usage:**
   ```python
   from langchain.callbacks import get_openai_callback

   with get_openai_callback() as cb:
       result = agent_executor.invoke({"input": query})
       print(f"Tokens: {cb.total_tokens}, Cost: ${cb.total_cost:.4f}")
   ```

## Troubleshooting

**Agent gets stuck in loop:**
- Reduce `max_iterations`
- Improve tool descriptions
- Add explicit stop conditions

**Tool selection is wrong:**
- Make tool descriptions more specific
- Use structured tool calling
- Try different prompts

**Out of context window:**
- Use summarization tool
- Reduce max_iterations
- Use models with larger context

## Resources

- LangChain Agents: https://python.langchain.com/docs/modules/agents/
- ReAct Paper: https://arxiv.org/abs/2210.03629
- LangChain Hub: https://smith.langchain.com/hub
- Tool Examples: https://python.langchain.com/docs/modules/tools/
