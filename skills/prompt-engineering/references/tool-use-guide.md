# Tool Use and Function Calling Guide

Enable LLMs to interact with external systems, APIs, and execute code through structured tool definitions.

## Table of Contents

- [Concept Overview](#concept-overview)
- [OpenAI Function Calling](#openai-function-calling)
- [Anthropic Tool Use](#anthropic-tool-use)
- [Tool Description Best Practices](#tool-description-best-practices)
- [Multi-Tool Workflows](#multi-tool-workflows)
- [ReAct Pattern](#react-pattern)

## Concept Overview

**Tool use pattern:**
1. Define available tools with schemas
2. LLM decides when to call tools based on user request
3. Execute tool with LLM-provided parameters
4. Return results to LLM
5. LLM synthesizes final response

**When to use:**
- LLM needs real-time data (weather, stock prices)
- Database queries or searches
- Calculations or code execution
- API integrations
- Multi-step agent behaviors

## OpenAI Function Calling

### Basic Pattern

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
}]

messages = [{"role": "user", "content": "What's the weather in Tokyo?"}]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=tools,
    tool_choice="auto"  # Let model decide
)

# Check if model wants to call function
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_args = json.loads(tool_call.function.arguments)

    # Execute function
    weather_data = get_weather(**function_args)

    # Send result back
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(weather_data)
    })

    # Get final response
    final_response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    print(final_response.choices[0].message.content)
```

### Multiple Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search customer database by name or email",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create support ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]}
                },
                "required": ["title", "description"]
            }
        }
    }
]
```

## Anthropic Tool Use

### Basic Pattern

```python
import anthropic

client = anthropic.Anthropic()

tools = [{
    "name": "get_weather",
    "description": "Get current weather for a location. Use when user asks about weather conditions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["location"]
    }
}]

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

# Process tool use
if message.stop_reason == "tool_use":
    tool_use_block = next(block for block in message.content if block.type == "tool_use")

    # Execute tool
    weather = get_weather(**tool_use_block.input)

    # Continue conversation
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"},
            {"role": "assistant", "content": message.content},
            {
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": json.dumps(weather)
                }]
            }
        ]
    )
    print(response.content[0].text)
```

## Tool Description Best Practices

### BAD: Vague Descriptions

```python
# Too vague
"name": "search",
"description": "Search for stuff"

# Ambiguous purpose
"name": "process",
"description": "Process data"
```

### GOOD: Specific Descriptions

```python
# Clear purpose and usage
{
    "name": "search_knowledge_base",
    "description": "Search internal knowledge base for product documentation. Use when user asks about product features, specifications, troubleshooting, or how-to guides. Returns top 5 most relevant articles with snippets.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query. Use keywords from user's question. Example: 'password reset' or 'shipping policy'"
            },
            "category": {
                "type": "string",
                "enum": ["features", "troubleshooting", "billing", "general"],
                "description": "Filter results by category if user's question clearly fits one"
            }
        },
        "required": ["query"]
    }
}
```

### Description Template

```python
{
    "name": "tool_name",
    "description": "[What it does]. [When to use it]. [What it returns].",
    "parameters": {
        "properties": {
            "param_name": {
                "type": "string",
                "description": "[What this parameter is]. [Format or example if helpful]."
            }
        }
    }
}
```

## Multi-Tool Workflows

### Sequential Tool Use

```python
tools = [
    {
        "name": "search_products",
        "description": "Search product catalog. Returns product IDs and basic info.",
        ...
    },
    {
        "name": "get_product_details",
        "description": "Get detailed information for a specific product. Requires product ID from search_products.",
        ...
    },
    {
        "name": "check_inventory",
        "description": "Check stock levels for a product. Requires product ID.",
        ...
    }
]

# Model can chain: search → get_details → check_inventory
```

### Parallel Tool Use

```python
# Some models can call multiple tools simultaneously
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in NYC and London?"}],
    tools=tools
)

# May return multiple tool_calls
for tool_call in response.choices[0].message.tool_calls:
    execute_tool(tool_call)
```

## ReAct Pattern

**ReAct = Reasoning + Acting**

Pattern: Thought → Action → Observation → (repeat)

### Implementation

```python
def react_agent(query: str, max_steps: int = 5):
    """ReAct agent that thinks and acts iteratively."""

    messages = [{"role": "user", "content": query}]

    for step in range(max_steps):
        # Model thinks and decides action
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # If no tool call, agent is done
        if not message.tool_calls:
            return message.content

        # Execute tools
        messages.append(message)
        for tool_call in message.tool_calls:
            result = execute_tool(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Max steps reached"
```

### Example ReAct Conversation

```
User: Find the cheapest laptop with 16GB RAM in stock.

Thought: I need to search for laptops with 16GB RAM first.
Action: search_products(query="laptop 16GB RAM")
Observation: Found 5 laptops: [A, B, C, D, E]

Thought: Now I need to check which are in stock.
Action: check_inventory(product_ids=["A", "B", "C", "D", "E"])
Observation: In stock: [A, C, E]

Thought: Now I need to compare prices.
Action: get_prices(product_ids=["A", "C", "E"])
Observation: A=$899, C=$1099, E=$799

Final Answer: Laptop E at $799 is the cheapest option with 16GB RAM in stock.
```

## TypeScript Examples

### Vercel AI SDK

```typescript
import { generateText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const tools = {
  getWeather: tool({
    description: 'Get current weather for a city',
    parameters: z.object({
      city: z.string().describe('City name'),
    }),
    execute: async ({ city }) => {
      // Call weather API
      const data = await fetchWeather(city);
      return { temperature: data.temp, conditions: data.conditions };
    },
  }),

  calculator: tool({
    description: 'Perform calculations',
    parameters: z.object({
      expression: z.string().describe('Math expression'),
    }),
    execute: async ({ expression }) => {
      return { result: eval(expression) };
    },
  }),
};

const { text, toolCalls } = await generateText({
  model: openai('gpt-4'),
  tools,
  maxSteps: 5,  // Allow multi-step tool use
  prompt: 'What is 25 degrees Celsius in Fahrenheit and what is the weather in Tokyo?',
});

console.log(text);
console.log(toolCalls); // All tools called
```

## Error Handling

### Validate Tool Inputs

```python
from pydantic import BaseModel, ValidationError

class WeatherParams(BaseModel):
    location: str
    unit: str = "celsius"

def safe_get_weather(params: dict) -> dict:
    """Execute tool with validation."""
    try:
        validated = WeatherParams(**params)
        return get_weather(validated.location, validated.unit)
    except ValidationError as e:
        return {"error": f"Invalid parameters: {e}"}
```

### Handle Tool Execution Failures

```python
def execute_tool_safe(tool_name: str, params: dict) -> dict:
    """Execute tool with error handling."""
    try:
        if tool_name == "get_weather":
            return get_weather(**params)
        elif tool_name == "search_db":
            return search_db(**params)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    except Exception as e:
        return {"error": str(e), "tool": tool_name}
```

## Summary

Tool use transforms LLMs from text generators to interactive agents. The key is clear tool descriptions and robust execution handling.

**Key takeaways:**
- Describe tools clearly: what, when, and what returns
- Use schemas to validate inputs
- Handle execution errors gracefully
- Enable multi-step workflows with ReAct pattern
- Test tool descriptions with real user queries
