"""
LangChain Prompt Engineering Examples

Demonstrates LangChain patterns:
- PromptTemplates
- ChatPromptTemplates
- Few-shot examples
- Output parsers
- Chain composition (LCEL)

Installation:
    pip install langchain langchain-openai langchain-anthropic

Usage:
    export OPENAI_API_KEY="your-api-key"
    export ANTHROPIC_API_KEY="your-api-key"  # Optional
    python langchain-examples.py
"""

import os
from typing import List, Dict
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    PydanticOutputParser,
)
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI


# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.environ.get("OPENAI_API_KEY")
)


# ============================================================================
# Example 1: Basic PromptTemplate
# ============================================================================

def basic_prompt_template():
    """Simple string-based prompt template."""
    print("\n=== Basic PromptTemplate ===")

    template = PromptTemplate.from_template(
        "Translate the following text to {language}: {text}"
    )

    prompt = template.format(language="French", text="Hello, how are you?")
    print(f"Formatted prompt: {prompt}")

    # Use with LLM
    response = llm.invoke(prompt)
    print(f"Response: {response.content}")


# ============================================================================
# Example 2: ChatPromptTemplate
# ============================================================================

def chat_prompt_template():
    """Chat-based prompt template with system and user messages."""
    print("\n=== ChatPromptTemplate ===")

    template = ChatPromptTemplate.from_messages([
        ("system", "You are a {role} who {style}."),
        ("user", "{task}")
    ])

    messages = template.format_messages(
        role="creative writer",
        style="uses vivid imagery and metaphors",
        task="Write a short description of a sunset."
    )

    print("Formatted messages:")
    for msg in messages:
        print(f"  {msg.type}: {msg.content}")

    response = llm.invoke(messages)
    print(f"\nResponse: {response.content}")


# ============================================================================
# Example 3: Few-Shot Prompting
# ============================================================================

def few_shot_example():
    """Few-shot learning with examples."""
    print("\n=== Few-Shot Prompting ===")

    # Define examples
    examples = [
        {
            "input": "happy",
            "output": "😊"
        },
        {
            "input": "sad",
            "output": "😢"
        },
        {
            "input": "excited",
            "output": "🎉"
        }
    ]

    # Example formatter
    example_template = PromptTemplate(
        input_variables=["input", "output"],
        template="Emotion: {input}\nEmoji: {output}"
    )

    # Prefix and suffix
    prefix = "Convert emotions to emojis:\n\n"
    suffix = "\nEmotion: {input}\nEmoji:"

    # Create few-shot prompt
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_template,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input"]
    )

    # Format and invoke
    prompt = few_shot_prompt.format(input="surprised")
    print(f"Formatted prompt:\n{prompt}\n")

    response = llm.invoke(prompt)
    print(f"Response: {response.content}")


# ============================================================================
# Example 4: Output Parsers - String Parser
# ============================================================================

def string_output_parser():
    """Parse string output."""
    print("\n=== String Output Parser ===")

    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{question}")
    ])

    parser = StrOutputParser()

    # Create chain using LCEL
    chain = template | llm | parser

    result = chain.invoke({"question": "What is the capital of France?"})
    print(f"Parsed result (string): {result}")
    print(f"Type: {type(result)}")


# ============================================================================
# Example 5: Output Parsers - JSON Parser
# ============================================================================

def json_output_parser():
    """Parse JSON output."""
    print("\n=== JSON Output Parser ===")

    parser = JsonOutputParser()

    template = ChatPromptTemplate.from_messages([
        ("system", "Extract information as JSON."),
        ("user", "{query}\n\n{format_instructions}")
    ])

    chain = template | llm | parser

    result = chain.invoke({
        "query": "Extract name and age: 'John is 25 years old'",
        "format_instructions": parser.get_format_instructions()
    })

    print(f"Parsed result (dict): {result}")
    print(f"Type: {type(result)}")


# ============================================================================
# Example 6: Output Parsers - Pydantic Parser
# ============================================================================

def pydantic_output_parser():
    """Parse output into Pydantic model."""
    print("\n=== Pydantic Output Parser ===")

    try:
        from pydantic import BaseModel, Field

        class Person(BaseModel):
            name: str = Field(description="Person's name")
            age: int = Field(description="Person's age")
            occupation: str = Field(description="Person's occupation")

        parser = PydanticOutputParser(pydantic_object=Person)

        template = ChatPromptTemplate.from_messages([
            ("system", "Extract person information."),
            ("user", "{query}\n\n{format_instructions}")
        ])

        chain = template | llm | parser

        result = chain.invoke({
            "query": "Parse: 'Alice is a 30-year-old engineer'",
            "format_instructions": parser.get_format_instructions()
        })

        print(f"Parsed result: {result}")
        print(f"Name: {result.name}")
        print(f"Age: {result.age}")
        print(f"Occupation: {result.occupation}")

    except ImportError:
        print("Install pydantic: pip install pydantic")


# ============================================================================
# Example 7: LCEL Chain Composition
# ============================================================================

def lcel_chain_composition():
    """Compose chains using LangChain Expression Language."""
    print("\n=== LCEL Chain Composition ===")

    # Step 1: Generate a topic
    topic_template = ChatPromptTemplate.from_template(
        "Suggest a specific topic related to: {subject}"
    )

    # Step 2: Write about the topic
    writing_template = ChatPromptTemplate.from_template(
        "Write a 2-sentence paragraph about: {topic}"
    )

    # Step 3: Summarize
    summary_template = ChatPromptTemplate.from_template(
        "Summarize this in one sentence: {paragraph}"
    )

    # Compose chain
    chain = (
        topic_template
        | llm
        | StrOutputParser()
        | (lambda topic: {"topic": topic})
        | writing_template
        | llm
        | StrOutputParser()
        | (lambda paragraph: {"paragraph": paragraph})
        | summary_template
        | llm
        | StrOutputParser()
    )

    result = chain.invoke({"subject": "artificial intelligence"})
    print(f"Final summary: {result}")


# ============================================================================
# Example 8: Conversation Memory
# ============================================================================

def conversation_with_memory():
    """Maintain conversation history."""
    print("\n=== Conversation with Memory ===")

    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])

    chain = template | llm | StrOutputParser()

    # Conversation history
    history = []

    def chat(user_input: str) -> str:
        """Send message and update history."""
        response = chain.invoke({
            "history": history,
            "input": user_input
        })

        # Update history
        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=response))

        return response

    # Turn 1
    response1 = chat("My name is Alice and I love Python.")
    print(f"User: My name is Alice and I love Python.")
    print(f"Assistant: {response1}\n")

    # Turn 2
    response2 = chat("What's my name and what language do I like?")
    print(f"User: What's my name and what language do I like?")
    print(f"Assistant: {response2}")


# ============================================================================
# Example 9: Conditional Chain (Routing)
# ============================================================================

def conditional_routing():
    """Route to different chains based on input."""
    print("\n=== Conditional Routing ===")

    from langchain_core.runnables import RunnableBranch

    # Classification chain
    classify_template = ChatPromptTemplate.from_template(
        """Classify this query into ONE category:
- technical
- billing
- general

Query: {query}

Category (one word):"""
    )

    classify_chain = classify_template | llm | StrOutputParser()

    # Technical support chain
    technical_template = ChatPromptTemplate.from_template(
        "Provide technical support for: {query}"
    )
    technical_chain = technical_template | llm | StrOutputParser()

    # Billing chain
    billing_template = ChatPromptTemplate.from_template(
        "Provide billing assistance for: {query}"
    )
    billing_chain = billing_template | llm | StrOutputParser()

    # General chain
    general_template = ChatPromptTemplate.from_template(
        "Provide general assistance for: {query}"
    )
    general_chain = general_template | llm | StrOutputParser()

    # Route based on classification
    def route_query(query: str):
        category = classify_chain.invoke({"query": query}).strip().lower()
        print(f"Classified as: {category}")

        if "technical" in category:
            return technical_chain.invoke({"query": query})
        elif "billing" in category:
            return billing_chain.invoke({"query": query})
        else:
            return general_chain.invoke({"query": query})

    # Test
    query = "How do I reset my password?"
    response = route_query(query)
    print(f"\nQuery: {query}")
    print(f"Response: {response}")


# ============================================================================
# Example 10: Parallel Chain Execution
# ============================================================================

def parallel_chains():
    """Execute multiple chains in parallel."""
    print("\n=== Parallel Chain Execution ===")

    from langchain_core.runnables import RunnableParallel

    # Define parallel tasks
    pros_template = ChatPromptTemplate.from_template(
        "List 3 pros of: {topic}"
    )
    cons_template = ChatPromptTemplate.from_template(
        "List 3 cons of: {topic}"
    )
    summary_template = ChatPromptTemplate.from_template(
        "Summarize in one sentence: {topic}"
    )

    # Create parallel chain
    parallel_chain = RunnableParallel(
        pros=pros_template | llm | StrOutputParser(),
        cons=cons_template | llm | StrOutputParser(),
        summary=summary_template | llm | StrOutputParser()
    )

    result = parallel_chain.invoke({"topic": "remote work"})

    print("Parallel results:")
    print(f"\nPros:\n{result['pros']}")
    print(f"\nCons:\n{result['cons']}")
    print(f"\nSummary:\n{result['summary']}")


# ============================================================================
# Example 11: Custom Prompt Template
# ============================================================================

def custom_prompt_template():
    """Create custom prompt template with validation."""
    print("\n=== Custom Prompt Template ===")

    class EmailPromptTemplate(PromptTemplate):
        """Custom template for email generation."""

        def format(self, **kwargs) -> str:
            # Validate inputs
            if "recipient" not in kwargs:
                raise ValueError("recipient is required")
            if "tone" not in kwargs:
                kwargs["tone"] = "professional"

            # Add default signature
            if "signature" not in kwargs:
                kwargs["signature"] = "Best regards,\n[Your Name]"

            return super().format(**kwargs)

    template = EmailPromptTemplate(
        input_variables=["recipient", "subject", "tone", "signature"],
        template="""
Write a {tone} email to {recipient} with the subject: {subject}

Email:

{signature}
"""
    )

    prompt = template.format(
        recipient="Sarah",
        subject="Project Update",
        tone="friendly"
    )

    print(f"Formatted prompt:\n{prompt}")

    response = llm.invoke(prompt)
    print(f"\nGenerated email:\n{response.content}")


# ============================================================================
# Example 12: Multi-Step Reasoning Chain
# ============================================================================

def multi_step_reasoning():
    """Chain for complex multi-step reasoning."""
    print("\n=== Multi-Step Reasoning Chain ===")

    # Step 1: Break down the problem
    breakdown_template = ChatPromptTemplate.from_template(
        """Break this problem into 3-5 logical steps:

Problem: {problem}

Steps:"""
    )

    # Step 2: Solve each step
    solve_template = ChatPromptTemplate.from_template(
        """Original problem: {problem}

Steps to solve:
{steps}

Solve each step and provide the final answer:"""
    )

    # Create chain
    chain = (
        breakdown_template
        | llm
        | StrOutputParser()
        | (lambda steps: {"problem": "PLACEHOLDER", "steps": steps})
        | solve_template
        | llm
        | StrOutputParser()
    )

    # We need to manually handle the problem variable
    problem = "If a train travels 120 miles in 2 hours, then speeds up to travel 180 miles in 2 hours, what is its average speed for the entire journey?"

    # Step 1
    steps = (breakdown_template | llm | StrOutputParser()).invoke({"problem": problem})
    print(f"Steps:\n{steps}\n")

    # Step 2
    solution = (solve_template | llm | StrOutputParser()).invoke({
        "problem": problem,
        "steps": steps
    })
    print(f"Solution:\n{solution}")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run all examples."""
    examples = [
        ("Basic PromptTemplate", basic_prompt_template),
        ("ChatPromptTemplate", chat_prompt_template),
        ("Few-Shot Example", few_shot_example),
        ("String Output Parser", string_output_parser),
        ("JSON Output Parser", json_output_parser),
        ("Pydantic Output Parser", pydantic_output_parser),
        ("LCEL Chain Composition", lcel_chain_composition),
        ("Conversation with Memory", conversation_with_memory),
        ("Conditional Routing", conditional_routing),
        ("Parallel Chains", parallel_chains),
        ("Custom Prompt Template", custom_prompt_template),
        ("Multi-Step Reasoning", multi_step_reasoning),
    ]

    print("LangChain Prompt Engineering Examples")
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
