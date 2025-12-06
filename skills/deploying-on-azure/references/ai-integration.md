# Azure AI Integration Reference

Comprehensive guide to integrating Azure OpenAI Service, Cognitive Services, and Azure Machine Learning.

## Table of Contents

1. [Azure OpenAI Service](#azure-openai-service)
2. [Retrieval-Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
3. [Function Calling](#function-calling)
4. [Cognitive Services](#cognitive-services)
5. [Azure Machine Learning](#azure-machine-learning)

---

## Azure OpenAI Service

**Enterprise-grade access to GPT-4, GPT-3.5, embeddings, and other OpenAI models**

### Key Advantages

| Feature | Benefit |
|---------|---------|
| **Data Privacy** | Customer data not used for model training |
| **Regional Deployment** | Data residency compliance |
| **Enterprise SLA** | 99.9% uptime guarantee |
| **Content Filtering** | Built-in abuse monitoring |
| **Microsoft Support** | Enterprise support contracts |
| **Managed Identity** | Secure authentication without API keys |

### Available Models (2025)

| Model | Use Case | Context Window | Cost per 1K tokens |
|-------|----------|----------------|-------------------|
| **GPT-4 Turbo** | Complex reasoning, coding | 128K | $0.01 input, $0.03 output |
| **GPT-4** | Advanced tasks | 8K | $0.03 input, $0.06 output |
| **GPT-3.5 Turbo** | Simple tasks, chatbots | 16K | $0.0005 input, $0.0015 output |
| **text-embedding-ada-002** | Embeddings for RAG | 8K | $0.0001 |

### Python SDK Setup

```python
# requirements.txt
openai==1.10.0
azure-identity==1.15.0
azure-search-documents==11.4.0
azure-core==1.29.0

# app.py
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Use Managed Identity (recommended)
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint="https://myopenai.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview"
)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that provides concise answers."
        },
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    temperature=0.2,
    max_tokens=500,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0
)

print(response.choices[0].message.content)
```

### TypeScript SDK Setup

```typescript
// package.json
{
  "dependencies": {
    "@azure/openai": "^1.0.0-beta.11",
    "@azure/identity": "^4.0.0"
  }
}

// app.ts
import { OpenAIClient, AzureKeyCredential } from "@azure/openai";
import { DefaultAzureCredential } from "@azure/identity";

// Use Managed Identity
const credential = new DefaultAzureCredential();
const endpoint = "https://myopenai.openai.azure.com";

const client = new OpenAIClient(endpoint, credential);

async function getChatCompletion() {
  const deploymentName = "gpt-4-turbo";

  const messages = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "What is the capital of France?" }
  ];

  const result = await client.getChatCompletions(deploymentName, messages, {
    temperature: 0.2,
    maxTokens: 500,
    topP: 0.95
  });

  for (const choice of result.choices) {
    console.log(choice.message?.content);
  }
}

getChatCompletion();
```

### Bicep Deployment

```bicep
resource openAI 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: 'myopenai'
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: 'myopenai'
    publicNetworkAccess: 'Disabled'  // Use Private Endpoint
    networkAcls: {
      defaultAction: 'Deny'
    }
  }
}

// Deploy GPT-4 Turbo model
resource gpt4Deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openAI
  name: 'gpt-4-turbo'
  sku: {
    name: 'Standard'
    capacity: 10  // Tokens per minute (thousands)
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4'
      version: 'turbo-2024-04-09'
    }
  }
}

// Deploy embedding model
resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openAI
  name: 'text-embedding-ada-002'
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'text-embedding-ada-002'
      version: '2'
    }
  }
}

// Private Endpoint for OpenAI
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'openai-pe'
  location: location
  properties: {
    subnet: {
      id: subnet.id
    }
    privateLinkServiceConnections: [
      {
        name: 'openai-connection'
        properties: {
          privateLinkServiceId: openAI.id
          groupIds: ['account']
        }
      }
    ]
  }
}
```

---

## Retrieval-Augmented Generation (RAG)

**Combine Azure OpenAI with Azure AI Search for grounded responses**

### RAG Architecture

```
User Query
    ↓
Azure AI Search (vector search)
    ↓
Retrieve top-k relevant documents
    ↓
Construct prompt with context
    ↓
Azure OpenAI (GPT-4)
    ↓
Grounded response
```

### Python RAG Implementation

```python
import os
import json
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential

# Azure OpenAI setup
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)

openai_client = AzureOpenAI(
    azure_endpoint="https://myopenai.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview"
)

# Azure AI Search setup
search_client = SearchClient(
    endpoint="https://myaisearch.search.windows.net",
    index_name="product-docs",
    credential=credential
)

def generate_embedding(text: str) -> list[float]:
    """Generate embedding using Azure OpenAI."""
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def rag_query(user_question: str, top_k: int = 3) -> str:
    """Answer question using RAG pattern with vector search."""

    # 1. Generate embedding for user question
    question_embedding = generate_embedding(user_question)

    # 2. Perform vector search in Azure AI Search
    vector_query = VectorizedQuery(
        vector=question_embedding,
        k_nearest_neighbors=top_k,
        fields="contentVector"
    )

    search_results = search_client.search(
        search_text=None,  # Pure vector search
        vector_queries=[vector_query],
        select=["content", "title", "category"]
    )

    # 3. Build context from search results
    context_parts = []
    for i, doc in enumerate(search_results, 1):
        context_parts.append(
            f"Document {i} (Category: {doc['category']}):\n"
            f"Title: {doc['title']}\n"
            f"Content: {doc['content']}\n"
        )

    context = "\n".join(context_parts)

    # 4. Generate answer with context
    system_message = """You are a helpful assistant that answers questions based on the provided context.

Rules:
- Only use information from the provided documents
- If the answer is not in the context, say "I don't have enough information to answer that question."
- Cite which document(s) you used
- Be concise and accurate
"""

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_question}"}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    question = "What are the key features of Azure Container Apps?"
    answer = rag_query(question)
    print(f"Question: {question}\n")
    print(f"Answer: {answer}")
```

### Azure AI Search Index Setup

```bicep
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: 'myaisearch'
  location: location
  sku: {
    name: 'basic'  // basic, standard, standard2, standard3
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'disabled'  // Use Private Endpoint
  }
}

// Note: Index schema defined via SDK or REST API
```

### Index Schema Example (Python SDK)

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

index_client = SearchIndexClient(
    endpoint="https://myaisearch.search.windows.net",
    credential=credential
)

# Define index schema
index = SearchIndex(
    name="product-docs",
    fields=[
        SearchField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            sortable=True
        ),
        SearchField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True
        ),
        SearchField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
            filterable=True
        ),
        SearchField(
            name="category",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True
        ),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,  # text-embedding-ada-002 dimension
            vector_search_profile_name="my-vector-profile"
        )
    ],
    vector_search=VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="my-vector-profile",
                algorithm_configuration_name="my-hnsw-config"
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(
                name="my-hnsw-config",
                parameters={
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            )
        ]
    )
)

# Create index
index_client.create_or_update_index(index)
```

---

## Function Calling

**Structured outputs and tool use with Azure OpenAI**

### Use Cases

- Extract structured data from unstructured text
- Execute actions based on user intent (book appointments, query databases)
- Multi-step workflows (agent patterns)
- API integration (call external services)

### Python Function Calling Example

```python
import json
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint="https://myopenai.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview"
)

# Define available functions
def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a location (mock implementation)."""
    # In production, call actual weather API
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "conditions": "Partly cloudy"
    }

def book_appointment(date: str, time: str, service: str) -> dict:
    """Book an appointment (mock implementation)."""
    return {
        "confirmation": "APT-12345",
        "date": date,
        "time": time,
        "service": service,
        "status": "confirmed"
    }

# Define function schemas for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for a service",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The appointment date in YYYY-MM-DD format"
                    },
                    "time": {
                        "type": "string",
                        "description": "The appointment time in HH:MM format"
                    },
                    "service": {
                        "type": "string",
                        "description": "The service type (e.g., haircut, consultation)"
                    }
                },
                "required": ["date", "time", "service"]
            }
        }
    }
]

# Map function names to actual functions
available_functions = {
    "get_current_weather": get_current_weather,
    "book_appointment": book_appointment
}

def run_conversation(user_message: str) -> str:
    """Run conversation with function calling."""

    messages = [
        {"role": "system", "content": "You are a helpful assistant that can check weather and book appointments."},
        {"role": "user", "content": user_message}
    ]

    # Initial API call with tools
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # Let model decide when to use functions
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    # Check if model wants to call functions
    if response_message.tool_calls:
        # Execute each function call
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"Calling function: {function_name}")
            print(f"Arguments: {function_args}")

            # Call the function
            function_response = available_functions[function_name](**function_args)

            # Add function response to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(function_response)
            })

        # Get final response after function execution
        second_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )

        return second_response.choices[0].message.content
    else:
        return response_message.content

# Example usage
if __name__ == "__main__":
    # Weather query
    result = run_conversation("What's the weather like in Seattle?")
    print(f"Result: {result}\n")

    # Appointment booking
    result = run_conversation("Book me a haircut appointment tomorrow at 2pm")
    print(f"Result: {result}")
```

---

## Cognitive Services

**Pre-built AI models for vision, speech, language, and decision**

### Service Categories

| Category | Services | Use Cases |
|----------|----------|-----------|
| **Vision** | Computer Vision, Custom Vision, Face | OCR, object detection, image classification |
| **Speech** | Speech-to-Text, Text-to-Speech, Translation | Transcription, voice assistants, real-time translation |
| **Language** | Text Analytics, Translator, Language Understanding | Sentiment analysis, entity extraction, NER |
| **Decision** | Anomaly Detector, Content Moderator | Fraud detection, content filtering |

### Computer Vision Example

```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.identity import DefaultAzureCredential
from msrest.authentication import CognitiveServicesCredentials

# Using API key (or use Managed Identity)
credential = CognitiveServicesCredentials(os.environ["VISION_KEY"])
client = ComputerVisionClient(
    endpoint="https://myregion.api.cognitive.microsoft.com",
    credentials=credential
)

# Analyze image
image_url = "https://example.com/image.jpg"

features = ["categories", "description", "tags", "objects", "brands", "faces"]

analysis = client.analyze_image(image_url, visual_features=features)

print(f"Description: {analysis.description.captions[0].text}")
print(f"Tags: {[tag.name for tag in analysis.tags]}")
print(f"Objects detected: {len(analysis.objects)}")

for obj in analysis.objects:
    print(f"  - {obj.object_property} (confidence: {obj.confidence:.2f})")
```

### Text Analytics Example

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = TextAnalyticsClient(
    endpoint="https://myregion.api.cognitive.microsoft.com",
    credential=credential
)

documents = [
    "The food was delicious and the service was excellent!",
    "I had a terrible experience. The product broke after one day."
]

# Sentiment analysis
result = client.analyze_sentiment(documents, show_opinion_mining=True)

for idx, doc in enumerate(result):
    print(f"\nDocument {idx + 1}: {documents[idx]}")
    print(f"Sentiment: {doc.sentiment} (confidence: {doc.confidence_scores})")

    # Opinion mining
    for sentence in doc.sentences:
        for opinion in sentence.mined_opinions:
            print(f"  Target: {opinion.target.text} ({opinion.target.sentiment})")
            for assessment in opinion.assessments:
                print(f"    Assessment: {assessment.text} ({assessment.sentiment})")

# Named Entity Recognition (NER)
entities_result = client.recognize_entities(documents)

for doc in entities_result:
    for entity in doc.entities:
        print(f"Entity: {entity.text} (Type: {entity.category}, Confidence: {entity.confidence_score:.2f})")
```

---

## Azure Machine Learning

**End-to-end platform for custom model training and MLOps**

### When to Use Azure ML

Choose Azure ML when:
- Training custom models (pre-built Cognitive Services insufficient)
- Need MLOps capabilities (experiment tracking, model versioning)
- Require distributed training (multi-GPU, multi-node)
- Building feature engineering pipelines
- Deploying models to managed endpoints

### Azure ML Workspace Bicep

```bicep
resource mlWorkspace 'Microsoft.MachineLearningServices/workspaces@2023-10-01' = {
  name: 'ml-workspace'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'ML Workspace'
    storageAccount: storageAccount.id
    keyVault: keyVault.id
    applicationInsights: appInsights.id
    containerRegistry: acr.id
    publicNetworkAccess: 'Disabled'
  }
}

// Compute cluster for training
resource computeCluster 'Microsoft.MachineLearningServices/workspaces/computes@2023-10-01' = {
  parent: mlWorkspace
  name: 'gpu-cluster'
  location: location
  properties: {
    computeType: 'AmlCompute'
    properties: {
      vmSize: 'Standard_NC6s_v3'
      vmPriority: 'Dedicated'
      scaleSettings: {
        minNodeCount: 0
        maxNodeCount: 4
        nodeIdleTimeBeforeScaleDown: 'PT120S'
      }
    }
  }
}
```

### Python SDK Training Example

```python
from azure.ai.ml import MLClient, command, Input
from azure.identity import DefaultAzureCredential

# Connect to workspace
credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id="<subscription-id>",
    resource_group_name="<resource-group>",
    workspace_name="ml-workspace"
)

# Define training job
job = command(
    code="./src",
    command="python train.py --data ${{inputs.training_data}} --epochs ${{inputs.epochs}}",
    inputs={
        "training_data": Input(
            type="uri_folder",
            path="azureml://datastores/workspaceblobstore/paths/training-data/"
        ),
        "epochs": 10
    },
    environment="azureml:sklearn-env@latest",
    compute="gpu-cluster",
    display_name="train-model-v1"
)

# Submit job
returned_job = ml_client.jobs.create_or_update(job)
print(f"Job URL: {returned_job.studio_url}")
```

---

## Summary

| Service | Best For | Complexity | Cost Model |
|---------|----------|------------|------------|
| **Azure OpenAI** | Chat, embeddings, content generation | Low | Per token |
| **Cognitive Services** | Pre-built AI (vision, speech, language) | Low | Per transaction |
| **Azure ML** | Custom models, MLOps | High | Compute + storage |
| **Azure AI Search** | Semantic search, RAG patterns | Medium | Index size + queries |

**Recommendation:** Start with Azure OpenAI and Cognitive Services for 90% of AI use cases. Use Azure ML only when custom model training required.
