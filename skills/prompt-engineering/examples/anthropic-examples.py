"""
Anthropic Claude-Specific Prompt Engineering Examples

Demonstrates Claude's unique features:
- System prompts
- XML tag patterns
- Tool use / function calling
- Streaming responses
- Extended thinking
- Prompt caching

Installation:
    pip install anthropic

Usage:
    export ANTHROPIC_API_KEY="your-api-key"
    python anthropic-examples.py
"""

import os
import anthropic
from typing import List, Dict, Any


# Initialize client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# ============================================================================
# Example 1: Basic Claude Message
# ============================================================================

def basic_message_example():
    """Simple message with system prompt."""
    print("\n=== Basic Message Example ===")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system="You are a helpful AI assistant specialized in Python programming.",
        messages=[
            {"role": "user", "content": "Write a function to calculate factorial"}
        ]
    )

    print(message.content[0].text)


# ============================================================================
# Example 2: XML-Structured Prompts (Claude Best Practice)
# ============================================================================

def xml_structured_prompt():
    """Use XML tags for better structure (Claude's strength)."""
    print("\n=== XML-Structured Prompt ===")

    system_prompt = """
You are a document analyzer. Follow these guidelines:

<capabilities>
- Extract key information from documents
- Summarize content concisely
- Identify main themes and topics
</capabilities>

<output_format>
Provide analysis in this structure:
<analysis>
  <summary>Brief summary</summary>
  <key_points>
    <point>Key point 1</point>
    <point>Key point 2</point>
  </key_points>
  <themes>List of themes</themes>
</analysis>
</output_format>
"""

    user_message = """
<document>
<title>The Future of AI</title>
<content>
Artificial intelligence is transforming industries worldwide. From healthcare
to finance, AI systems are becoming increasingly sophisticated. However,
challenges remain in ethics, regulation, and ensuring AI benefits all of society.
</content>
</document>

Analyze this document.
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )

    print(message.content[0].text)


# ============================================================================
# Example 3: Tool Use / Function Calling
# ============================================================================

def tool_use_example():
    """Demonstrate Claude's tool use capabilities."""
    print("\n=== Tool Use Example ===")

    # Define tools
    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather for a specific location. Use this when users ask about weather conditions.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., 'San Francisco, CA'"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        },
        {
            "name": "calculate",
            "description": "Perform mathematical calculations. Use for any arithmetic operations.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate, e.g., '2 + 2 * 3'"
                    }
                },
                "required": ["expression"]
            }
        }
    ]

    # Make initial request
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in Tokyo and what's 15 * 23?"}
        ]
    )

    print("Claude's response:")
    print(f"Stop reason: {message.stop_reason}")

    # Check if Claude wants to use tools
    if message.stop_reason == "tool_use":
        for block in message.content:
            if block.type == "tool_use":
                print(f"\nTool called: {block.name}")
                print(f"Tool input: {block.input}")

                # Simulate tool execution
                if block.name == "get_weather":
                    tool_result = {
                        "temperature": 18,
                        "condition": "Partly cloudy",
                        "humidity": 65
                    }
                elif block.name == "calculate":
                    import ast
                    tool_result = {"result": eval(block.input["expression"])}

                print(f"Tool result: {tool_result}")


# ============================================================================
# Example 4: Multi-Turn Conversation
# ============================================================================

def multi_turn_conversation():
    """Demonstrate conversation history management."""
    print("\n=== Multi-Turn Conversation ===")

    conversation_history = []

    # Turn 1
    user_message_1 = "My name is Alice and I love Python programming."
    conversation_history.append({"role": "user", "content": user_message_1})

    response_1 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=conversation_history
    )

    assistant_message_1 = response_1.content[0].text
    conversation_history.append({"role": "assistant", "content": assistant_message_1})

    print(f"User: {user_message_1}")
    print(f"Claude: {assistant_message_1}")

    # Turn 2
    user_message_2 = "What's my name and what language do I like?"
    conversation_history.append({"role": "user", "content": user_message_2})

    response_2 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=conversation_history
    )

    assistant_message_2 = response_2.content[0].text

    print(f"\nUser: {user_message_2}")
    print(f"Claude: {assistant_message_2}")


# ============================================================================
# Example 5: Streaming Responses
# ============================================================================

def streaming_example():
    """Stream Claude's response token-by-token."""
    print("\n=== Streaming Example ===")
    print("Claude's response (streaming): ", end="", flush=True)

    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=[
            {"role": "user", "content": "Write a haiku about artificial intelligence"}
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")


# ============================================================================
# Example 6: Prompt Caching (Cost Optimization)
# ============================================================================

def prompt_caching_example():
    """Use prompt caching to reduce costs for repeated context."""
    print("\n=== Prompt Caching Example ===")

    # Large context that will be reused
    large_codebase = """
# Authentication Module
class UserAuth:
    def __init__(self, db):
        self.db = db

    def login(self, username, password):
        user = self.db.find_user(username)
        if user and user.verify_password(password):
            return self.create_session(user)
        return None

    def create_session(self, user):
        # Creates JWT token
        pass

# Payment Module
class PaymentProcessor:
    def process_payment(self, amount, card):
        # Process payment logic
        pass
"""

    # First call - cache is created
    print("First call (creates cache):")
    message1 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": "You are a code reviewer specializing in Python."
            },
            {
                "type": "text",
                "text": f"Codebase to review:\n\n{large_codebase}",
                "cache_control": {"type": "ephemeral"}  # Cache this block
            }
        ],
        messages=[
            {"role": "user", "content": "Review the UserAuth class for security issues"}
        ]
    )

    print(f"Usage: {message1.usage}")
    print(f"Response: {message1.content[0].text[:200]}...\n")

    # Second call - uses cache (90% cost reduction on cached portion)
    print("Second call (uses cache):")
    message2 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": "You are a code reviewer specializing in Python."
            },
            {
                "type": "text",
                "text": f"Codebase to review:\n\n{large_codebase}",
                "cache_control": {"type": "ephemeral"}  # Same cached block
            }
        ],
        messages=[
            {"role": "user", "content": "Review the PaymentProcessor class"}
        ]
    )

    print(f"Usage: {message2.usage}")
    print(f"Cache hits: {getattr(message2.usage, 'cache_read_input_tokens', 0)} tokens")


# ============================================================================
# Example 7: Extended Thinking (Claude's Chain-of-Thought)
# ============================================================================

def extended_thinking_example():
    """Use Claude's extended thinking for complex reasoning."""
    print("\n=== Extended Thinking Example ===")

    # Note: Extended thinking is available on Claude 3.5 Sonnet and Opus
    system_prompt = """
You are a mathematics tutor. When solving problems:
1. Show all your work step-by-step
2. Explain your reasoning at each step
3. Verify your answer

Use <thinking> tags to show your internal reasoning process.
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": """
A train leaves Station A at 2:00 PM traveling at 60 mph.
Another train leaves Station B at 3:00 PM traveling at 80 mph toward Station A.
The stations are 300 miles apart.
At what time do the trains meet?
"""
            }
        ]
    )

    print(message.content[0].text)


# ============================================================================
# Example 8: Structured Data Extraction with Tool Use
# ============================================================================

def structured_extraction_example():
    """Extract structured data using tool use (Claude's JSON mode)."""
    print("\n=== Structured Data Extraction ===")

    # Define schema as a tool
    tools = [{
        "name": "record_user_info",
        "description": "Record structured user information",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name"},
                "age": {"type": "integer", "description": "Age in years"},
                "email": {"type": "string", "description": "Email address"},
                "interests": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of interests"
                }
            },
            "required": ["name", "age", "email"]
        }
    }]

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[{
            "role": "user",
            "content": """
Extract information from this bio:

"Hi, I'm Sarah Johnson, a 28-year-old software engineer.
You can reach me at sarah.j@email.com.
I'm passionate about machine learning, rock climbing, and photography."
"""
        }]
    )

    # Extract structured data
    for block in message.content:
        if block.type == "tool_use":
            print(f"Extracted data:")
            import json
            print(json.dumps(block.input, indent=2))


# ============================================================================
# Example 9: RAG Pattern with Citations
# ============================================================================

def rag_with_citations():
    """Retrieval-augmented generation with source citations."""
    print("\n=== RAG with Citations ===")

    system_prompt = """
Answer questions using ONLY information from the provided documents.
Cite sources using <citation source="document_name">fact</citation> tags.
If information is not in the documents, say "I don't have this information."
"""

    user_message = """
<documents>
  <document id="1" source="product_manual.pdf">
    The XYZ-2000 operates at 120V AC and consumes 500W maximum power.
    Recommended for indoor use only.
  </document>
  <document id="2" source="safety_guide.pdf">
    Always unplug the device before performing any maintenance.
    Keep away from water and moisture.
  </document>
  <document id="3" source="warranty.pdf">
    Product includes a 2-year manufacturer warranty covering defects.
    Warranty void if device is opened by unauthorized personnel.
  </document>
</documents>

<question>
What voltage does the XYZ-2000 use, what safety precautions should I take,
and what's the warranty period?
</question>
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )

    print(message.content[0].text)


# ============================================================================
# Example 10: Prefill Pattern (Control Output Format)
# ============================================================================

def prefill_pattern():
    """Use prefill to control Claude's response format."""
    print("\n=== Prefill Pattern ===")

    # Prefill forces Claude to start response in specific way
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=[
            {"role": "user", "content": "List 3 benefits of exercise"},
            {
                "role": "assistant",
                "content": "Here are the benefits:\n1."  # Prefill
            }
        ]
    )

    print("Prefilled response:")
    print("Here are the benefits:\n1." + message.content[0].text)


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run all examples."""
    examples = [
        ("Basic Message", basic_message_example),
        ("XML-Structured Prompt", xml_structured_prompt),
        ("Tool Use", tool_use_example),
        ("Multi-Turn Conversation", multi_turn_conversation),
        ("Streaming", streaming_example),
        ("Prompt Caching", prompt_caching_example),
        ("Extended Thinking", extended_thinking_example),
        ("Structured Extraction", structured_extraction_example),
        ("RAG with Citations", rag_with_citations),
        ("Prefill Pattern", prefill_pattern),
    ]

    print("Anthropic Claude Examples")
    print("=" * 60)

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\nError in {name}: {e}")

    print("\n" + "=" * 60)
    print("All examples completed!")


if __name__ == "__main__":
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-api-key'")
        exit(1)

    main()
