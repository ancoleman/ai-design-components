"""
OpenAI Prompt Engineering Examples

Demonstrates OpenAI-specific features:
- Chat completions API
- Function calling
- JSON mode
- Structured outputs
- Vision prompts (GPT-4o)
- Streaming

Installation:
    pip install openai

Usage:
    export OPENAI_API_KEY="your-api-key"
    python openai-examples.py
"""

import os
import json
from openai import OpenAI
from typing import List, Dict, Any


# Initialize client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ============================================================================
# Example 1: Basic Chat Completion
# ============================================================================

def basic_completion():
    """Simple chat completion with system and user messages."""
    print("\n=== Basic Chat Completion ===")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant specialized in Python programming."
            },
            {
                "role": "user",
                "content": "Write a function to check if a string is a palindrome."
            }
        ],
        temperature=0.7,
        max_tokens=500
    )

    print(response.choices[0].message.content)
    print(f"\nTokens used: {response.usage.total_tokens}")


# ============================================================================
# Example 2: JSON Mode (Reliable JSON Output)
# ============================================================================

def json_mode_example():
    """Use JSON mode for guaranteed valid JSON output."""
    print("\n=== JSON Mode Example ===")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a data extraction assistant. Extract information as JSON."
            },
            {
                "role": "user",
                "content": """
Extract the following information as JSON:

"Sarah Johnson, a 28-year-old software engineer from San Francisco,
enjoys hiking and photography. Contact: sarah@email.com"

Include: name, age, occupation, city, hobbies (array), email
"""
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    json_output = json.loads(response.choices[0].message.content)
    print("Extracted JSON:")
    print(json.dumps(json_output, indent=2))


# ============================================================================
# Example 3: Function Calling
# ============================================================================

def function_calling_example():
    """Demonstrate function calling for tool use."""
    print("\n=== Function Calling Example ===")

    # Define available functions
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and state, e.g., 'San Francisco, CA'"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Temperature unit"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform a mathematical calculation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression, e.g., '2 + 2 * 3'"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    ]

    # Initial request
    messages = [
        {"role": "user", "content": "What's the weather in Tokyo and what's 15 * 23?"}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    print(f"Assistant wants to call {len(response_message.tool_calls or [])} tool(s)")

    # Process tool calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"\nTool: {function_name}")
            print(f"Arguments: {function_args}")

            # Simulate function execution
            if function_name == "get_weather":
                result = json.dumps({
                    "temperature": 18,
                    "condition": "Partly cloudy",
                    "humidity": 65
                })
            elif function_name == "calculate":
                result = json.dumps({
                    "result": eval(function_args["expression"])
                })

            print(f"Result: {result}")


# ============================================================================
# Example 4: Multi-Turn Conversation with Memory
# ============================================================================

def conversation_example():
    """Demonstrate conversation history management."""
    print("\n=== Multi-Turn Conversation ===")

    conversation = []

    def chat(user_message: str) -> str:
        """Send message and get response."""
        conversation.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            temperature=0.7,
            max_tokens=200
        )

        assistant_message = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    # Turn 1
    user_msg_1 = "My favorite color is blue and I work as a teacher."
    response_1 = chat(user_msg_1)
    print(f"User: {user_msg_1}")
    print(f"Assistant: {response_1}\n")

    # Turn 2
    user_msg_2 = "What's my favorite color and what do I do for work?"
    response_2 = chat(user_msg_2)
    print(f"User: {user_msg_2}")
    print(f"Assistant: {response_2}")


# ============================================================================
# Example 5: Streaming Responses
# ============================================================================

def streaming_example():
    """Stream response token-by-token."""
    print("\n=== Streaming Example ===")
    print("Assistant (streaming): ", end="", flush=True)

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Write a haiku about programming"}
        ],
        stream=True,
        temperature=0.8
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n")


# ============================================================================
# Example 6: Few-Shot Learning
# ============================================================================

def few_shot_example():
    """Use few-shot examples to guide model behavior."""
    print("\n=== Few-Shot Learning ===")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Classify the sentiment of movie reviews as positive, negative, or neutral."
            },
            # Example 1
            {
                "role": "user",
                "content": "This movie was absolutely fantastic! Best film of the year."
            },
            {
                "role": "assistant",
                "content": "Sentiment: positive"
            },
            # Example 2
            {
                "role": "user",
                "content": "Terrible acting and boring plot. Waste of time."
            },
            {
                "role": "assistant",
                "content": "Sentiment: negative"
            },
            # Example 3
            {
                "role": "user",
                "content": "It was okay. Nothing special but not terrible either."
            },
            {
                "role": "assistant",
                "content": "Sentiment: neutral"
            },
            # Actual query
            {
                "role": "user",
                "content": "The cinematography was beautiful but the story dragged on too long."
            }
        ],
        temperature=0,
        max_tokens=50
    )

    print(response.choices[0].message.content)


# ============================================================================
# Example 7: Chain-of-Thought Prompting
# ============================================================================

def chain_of_thought_example():
    """Use chain-of-thought for complex reasoning."""
    print("\n=== Chain-of-Thought Example ===")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a math tutor. Always show your step-by-step reasoning."
            },
            {
                "role": "user",
                "content": """
A store sells apples for $0.50 each and oranges for $0.75 each.
If John buys 12 apples and 8 oranges, and he pays with a $20 bill,
how much change does he receive?

Think step-by-step:
"""
            }
        ],
        temperature=0,
        max_tokens=500
    )

    print(response.choices[0].message.content)


# ============================================================================
# Example 8: Temperature Variations
# ============================================================================

def temperature_comparison():
    """Compare outputs at different temperature settings."""
    print("\n=== Temperature Comparison ===")

    prompt = "Describe a sunset in one sentence."
    temperatures = [0, 0.5, 1.0, 1.5]

    for temp in temperatures:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=100
        )

        print(f"\nTemperature {temp}:")
        print(response.choices[0].message.content)


# ============================================================================
# Example 9: System Prompt Engineering
# ============================================================================

def system_prompt_comparison():
    """Compare different system prompts for the same task."""
    print("\n=== System Prompt Comparison ===")

    user_question = "Should I invest in cryptocurrency?"

    # System prompt 1: Neutral advisor
    print("\n1. Neutral Financial Advisor:")
    response1 = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a neutral financial advisor.
Provide balanced information about investment risks and opportunities.
Always mention that this is not personalized financial advice."""
            },
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        max_tokens=200
    )
    print(response1.choices[0].message.content)

    # System prompt 2: Conservative advisor
    print("\n2. Conservative Financial Advisor:")
    response2 = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a conservative financial advisor who prioritizes
capital preservation and risk mitigation. You are skeptical of high-risk investments."""
            },
            {"role": "user", "content": user_question}
        ],
        temperature=0.5,
        max_tokens=200
    )
    print(response2.choices[0].message.content)


# ============================================================================
# Example 10: Structured Outputs (Pydantic Models)
# ============================================================================

def structured_outputs_example():
    """Use OpenAI's structured outputs with Pydantic."""
    print("\n=== Structured Outputs with Pydantic ===")

    try:
        from pydantic import BaseModel
        from typing import List

        class UserProfile(BaseModel):
            name: str
            age: int
            email: str
            interests: List[str]
            occupation: str

        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",  # Requires model with structured outputs
            messages=[
                {
                    "role": "system",
                    "content": "Extract user profile information in the specified format."
                },
                {
                    "role": "user",
                    "content": """
Parse this bio:
"I'm Alex Chen, 32 years old, working as a data scientist.
I love hiking, photography, and reading sci-fi novels.
You can email me at alex.chen@example.com"
"""
                }
            ],
            response_format=UserProfile
        )

        user_profile = response.choices[0].message.parsed
        print("Parsed Profile:")
        print(f"Name: {user_profile.name}")
        print(f"Age: {user_profile.age}")
        print(f"Email: {user_profile.email}")
        print(f"Occupation: {user_profile.occupation}")
        print(f"Interests: {', '.join(user_profile.interests)}")

    except ImportError:
        print("Note: Install pydantic for structured outputs: pip install pydantic")
    except Exception as e:
        print(f"Structured outputs not available: {e}")
        print("Falling back to JSON mode...")

        # Fallback to regular JSON mode
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Extract user profile as JSON with fields: name, age, email, interests (array), occupation"
                },
                {
                    "role": "user",
                    "content": """
Parse this bio:
"I'm Alex Chen, 32 years old, working as a data scientist.
I love hiking, photography, and reading sci-fi novels.
You can email me at alex.chen@example.com"
"""
                }
            ],
            response_format={"type": "json_object"}
        )

        profile = json.loads(response.choices[0].message.content)
        print(json.dumps(profile, indent=2))


# ============================================================================
# Example 11: Vision (GPT-4o Image Analysis)
# ============================================================================

def vision_example():
    """Analyze images with GPT-4o (vision capabilities)."""
    print("\n=== Vision Example (GPT-4o) ===")

    # Using a publicly accessible image URL
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/320px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in detail. What's the setting, mood, and key elements?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    print(response.choices[0].message.content)


# ============================================================================
# Example 12: Token Usage Tracking
# ============================================================================

def token_usage_example():
    """Track token usage and estimate costs."""
    print("\n=== Token Usage Tracking ===")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "Explain quantum computing in 2 paragraphs."
            }
        ]
    )

    usage = response.usage
    print(f"Prompt tokens: {usage.prompt_tokens}")
    print(f"Completion tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")

    # Cost estimation (approximate prices as of 2024)
    input_cost_per_1k = 0.01  # $0.01 per 1K input tokens for GPT-4
    output_cost_per_1k = 0.03  # $0.03 per 1K output tokens for GPT-4

    estimated_cost = (
        (usage.prompt_tokens / 1000) * input_cost_per_1k +
        (usage.completion_tokens / 1000) * output_cost_per_1k
    )

    print(f"Estimated cost: ${estimated_cost:.6f}")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run all examples."""
    examples = [
        ("Basic Completion", basic_completion),
        ("JSON Mode", json_mode_example),
        ("Function Calling", function_calling_example),
        ("Multi-Turn Conversation", conversation_example),
        ("Streaming", streaming_example),
        ("Few-Shot Learning", few_shot_example),
        ("Chain-of-Thought", chain_of_thought_example),
        ("Temperature Comparison", temperature_comparison),
        ("System Prompt Comparison", system_prompt_comparison),
        ("Structured Outputs", structured_outputs_example),
        ("Vision (GPT-4o)", vision_example),
        ("Token Usage Tracking", token_usage_example),
    ]

    print("OpenAI Prompt Engineering Examples")
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
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        exit(1)

    main()
