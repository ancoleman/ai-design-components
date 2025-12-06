# Structured Output Generation

Generate reliable JSON and schema-compliant data from LLMs using native API features.

## Table of Contents

- [Why Structured Outputs](#why-structured-outputs)
- [Native JSON Modes](#native-json-modes)
- [Schema Validation](#schema-validation)
- [Tool Use for Structured Data](#tool-use-for-structured-data)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Why Structured Outputs

**Problem with text parsing:**
```python
# Fragile - model may return malformed JSON
response = "Here's the data: {name: John, age: 28}"  # Missing quotes
data = json.loads(response)  # CRASHES
```

**Solution - Native structured outputs:**
- Guaranteed valid JSON
- Schema validation
- Type safety
- No parsing errors

## Native JSON Modes

### OpenAI JSON Mode

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Extract user data as JSON."},
        {"role": "user", "content": 'Parse: "Sarah Chen, 28, sarah@example.com"'}
    ],
    response_format={"type": "json_object"}  # Force JSON
)

import json
data = json.loads(response.choices[0].message.content)
print(data)  # Valid JSON guaranteed
```

### OpenAI Structured Outputs (JSON Schema)

```python
from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    age: int
    email: str

response = client.beta.chat.completions.parse(
    model="gpt-4",
    messages=[
        {"role": "user", "content": 'Extract: "Sarah, 28, sarah@example.com"'}
    ],
    response_format=UserProfile
)

user = response.choices[0].message.parsed  # Fully typed!
print(user.name)  # "Sarah"
```

### Google Gemini JSON Mode

```python
import google.generativeai as genai

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(
    'Extract as JSON: "John, 25, engineer"',
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json"
    )
)

import json
data = json.loads(response.text)
```

## Schema Validation

### Pydantic (Python)

```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    categories: List[str]
    email: EmailStr
    quantity: Optional[int] = None

    @validator('price')
    def price_must_be_reasonable(cls, v):
        if v > 1000000:
            raise ValueError('Price too high')
        return v

# Usage
try:
    product = Product(
        name="Laptop",
        price=999.99,
        categories=["electronics"],
        email="sales@example.com"
    )
except ValidationError as e:
    print(e.json())
```

### Zod (TypeScript)

```typescript
import { z } from 'zod';

const ProductSchema = z.object({
  name: z.string().min(1).max(100),
  price: z.number().positive(),
  categories: z.array(z.string()),
  email: z.string().email(),
  quantity: z.number().int().optional(),
});

type Product = z.infer<typeof ProductSchema>;

// Validation
try {
  const product = ProductSchema.parse(data);
} catch (error) {
  console.error(error.errors);
}
```

## Tool Use for Structured Data

### Anthropic Tool Use

```python
import anthropic

client = anthropic.Anthropic()

tools = [{
    "name": "extract_user_data",
    "description": "Extract structured user information",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
            "email": {"type": "string", "format": "email"},
            "interests": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["name", "age"]
    }
}]

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": 'Extract: "Sarah, 28, sarah@example.com, loves hiking"'}]
)

# Extract validated data
tool_use = next(block for block in message.content if block.type == "tool_use")
data = tool_use.input  # Schema-validated!
print(data)  # {"name": "Sarah", "age": 28, "email": "sarah@example.com", ...}
```

### OpenAI Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "record_user",
        "description": "Record user information",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "email": {"type": "string"}
            },
            "required": ["name", "age", "email"]
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": 'Extract: "John, 30, john@example.com"'}],
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "record_user"}}
)

tool_call = response.choices[0].message.tool_calls[0]
data = json.loads(tool_call.function.arguments)
```

## Error Handling

### Retry with Schema Correction

```python
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt

class DataSchema(BaseModel):
    name: str
    age: int

@retry(stop=stop_after_attempt(3))
def extract_with_retry(text: str) -> DataSchema:
    """Extract data with automatic retry on validation failure."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Extract as JSON matching: {DataSchema.model_json_schema()}"},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )

    try:
        data = DataSchema.model_validate_json(response.choices[0].message.content)
        return data
    except ValidationError as e:
        # Add error context for retry
        raise ValueError(f"Validation failed: {e}")
```

### Graceful Fallback

```python
def safe_extract(text: str) -> dict:
    """Extract with fallback to defaults."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Extract as JSON: {text}"}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse", "raw": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
```

## Best Practices

### 1. Always Validate Output

```python
# BAD
data = json.loads(response.content)
print(data["name"])  # May not exist!

# GOOD
class Response(BaseModel):
    name: str
    age: int

try:
    data = Response.model_validate_json(response.content)
    print(data.name)  # Type-safe!
except ValidationError as e:
    handle_error(e)
```

### 2. Provide Schema in Prompt

```python
schema = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "number"}
                }
            }
        }
    }
}

prompt = f"""
Extract product data matching this schema:

{json.dumps(schema, indent=2)}

Text: {input_text}
"""
```

### 3. Use Enums for Constrained Values

```python
from enum import Enum
from pydantic import BaseModel

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Review(BaseModel):
    text: str
    sentiment: Sentiment  # Only these values allowed
    score: int = Field(ge=1, le=5)

# In TypeScript
const SentimentEnum = z.enum(['positive', 'negative', 'neutral']);
```

### 4. Handle Missing/Optional Fields

```python
from typing import Optional

class UserData(BaseModel):
    name: str
    age: int
    email: Optional[str] = None  # May not be present
    phone: Optional[str] = None

    class Config:
        # Allow extra fields (don't fail)
        extra = "allow"
```

## Vercel AI SDK Examples

### generateObject

```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const schema = z.object({
  products: z.array(
    z.object({
      name: z.string(),
      price: z.number().positive(),
      inStock: z.boolean(),
    })
  ),
});

const { object } = await generateObject({
  model: openai('gpt-4'),
  schema,
  prompt: 'Extract products from: "Laptop $999 (in stock), Mouse $29 (sold out)"',
});

console.log(object.products); // Fully typed!
```

### streamObject

```typescript
import { streamObject } from 'ai';

const { partialObjectStream } = await streamObject({
  model: openai('gpt-4'),
  schema,
  prompt: 'Generate 10 product listings',
});

for await (const partialObject of partialObjectStream) {
  console.log(partialObject); // Partial updates
}
```

## Complex Schema Example

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: Optional[str] = None

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)

class Order(BaseModel):
    order_id: str
    customer_name: str
    customer_email: str
    shipping_address: Address
    items: List[OrderItem]
    order_date: datetime
    total: float = Field(gt=0)
    notes: Optional[str] = None

# Usage with LLM
prompt = f"""
Extract order data from this email:

{email_text}

Return JSON matching this structure:
{Order.model_json_schema()}
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
)

order = Order.model_validate_json(response.choices[0].message.content)
```

## Summary

Structured outputs eliminate JSON parsing errors and enable type-safe LLM applications. Always use native JSON modes, validate with schemas, and handle errors gracefully.

**Key takeaways:**
- Use `response_format={"type": "json_object"}` for OpenAI
- Use tool calling for complex schemas with validation
- Always validate with Pydantic/Zod
- Provide schema in prompt for clarity
- Handle validation errors with retry logic
- Use enums for constrained values
