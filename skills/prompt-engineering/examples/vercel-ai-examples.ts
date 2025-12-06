/**
 * Vercel AI SDK Prompt Engineering Examples
 *
 * Demonstrates Vercel AI SDK patterns:
 * - generateText / streamText
 * - generateObject (structured outputs)
 * - Tool definitions
 * - Multi-step agents
 * - TypeScript type safety
 *
 * Installation:
 *   npm install ai @ai-sdk/openai @ai-sdk/anthropic zod
 *
 * Usage:
 *   export OPENAI_API_KEY="your-api-key"
 *   export ANTHROPIC_API_KEY="your-api-key"  // Optional
 *   npx tsx vercel-ai-examples.ts
 */

import { generateText, streamText, generateObject, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

// ============================================================================
// Example 1: Basic Text Generation
// ============================================================================

async function basicTextGeneration() {
  console.log('\n=== Basic Text Generation ===');

  const { text } = await generateText({
    model: openai('gpt-4'),
    prompt: 'Write a haiku about TypeScript',
  });

  console.log(text);
}

// ============================================================================
// Example 2: System Prompts and Messages
// ============================================================================

async function systemPromptExample() {
  console.log('\n=== System Prompt Example ===');

  const { text } = await generateText({
    model: openai('gpt-4'),
    system: 'You are a helpful Python programming tutor. Explain concepts clearly with examples.',
    prompt: 'What is a decorator?',
  });

  console.log(text);
}

// ============================================================================
// Example 3: Streaming Text
// ============================================================================

async function streamingExample() {
  console.log('\n=== Streaming Example ===');
  console.log('Streaming response: ');

  const { textStream } = await streamText({
    model: openai('gpt-4'),
    prompt: 'Explain quantum computing in 3 sentences',
  });

  for await (const chunk of textStream) {
    process.stdout.write(chunk);
  }

  console.log('\n');
}

// ============================================================================
// Example 4: Structured Output with Zod
// ============================================================================

async function structuredOutputExample() {
  console.log('\n=== Structured Output Example ===');

  const UserSchema = z.object({
    name: z.string().describe('User full name'),
    age: z.number().describe('User age in years'),
    email: z.string().email().describe('User email address'),
    interests: z.array(z.string()).describe('List of user interests'),
  });

  const { object } = await generateObject({
    model: openai('gpt-4'),
    schema: UserSchema,
    prompt: 'Extract info: "Sarah Johnson, 28, loves hiking and photography. Email: sarah@example.com"',
  });

  console.log('Extracted data:');
  console.log(JSON.stringify(object, null, 2));
}

// ============================================================================
// Example 5: Multi-Turn Conversation
// ============================================================================

async function conversationExample() {
  console.log('\n=== Multi-Turn Conversation ===');

  // Turn 1
  const { text: response1 } = await generateText({
    model: openai('gpt-4'),
    messages: [
      { role: 'user', content: 'My favorite color is blue and I work as a teacher.' },
    ],
  });

  console.log('User: My favorite color is blue and I work as a teacher.');
  console.log(`Assistant: ${response1}\n`);

  // Turn 2 (with conversation history)
  const { text: response2 } = await generateText({
    model: openai('gpt-4'),
    messages: [
      { role: 'user', content: 'My favorite color is blue and I work as a teacher.' },
      { role: 'assistant', content: response1 },
      { role: 'user', content: "What's my favorite color and what do I do for work?" },
    ],
  });

  console.log("User: What's my favorite color and what do I do for work?");
  console.log(`Assistant: ${response2}`);
}

// ============================================================================
// Example 6: Tool Use / Function Calling
// ============================================================================

async function toolUseExample() {
  console.log('\n=== Tool Use Example ===');

  const { text, toolCalls } = await generateText({
    model: openai('gpt-4'),
    tools: {
      weather: tool({
        description: 'Get the weather for a location',
        parameters: z.object({
          location: z.string().describe('City name, e.g., "San Francisco, CA"'),
          units: z.enum(['celsius', 'fahrenheit']).optional(),
        }),
        execute: async ({ location, units = 'celsius' }) => {
          // Simulate API call
          return {
            location,
            temperature: 18,
            condition: 'Partly cloudy',
            units,
          };
        },
      }),
      calculate: tool({
        description: 'Perform a mathematical calculation',
        parameters: z.object({
          expression: z.string().describe('Math expression, e.g., "2 + 2 * 3"'),
        }),
        execute: async ({ expression }) => {
          // Evaluate expression (in production, use a safe math parser)
          const result = eval(expression);
          return { expression, result };
        },
      }),
    },
    prompt: "What's the weather in Tokyo and what's 15 * 23?",
    maxToolRoundtrips: 5,
  });

  console.log('Tool calls made:');
  console.log(JSON.stringify(toolCalls, null, 2));
  console.log('\nFinal response:');
  console.log(text);
}

// ============================================================================
// Example 7: Temperature and Model Parameters
// ============================================================================

async function temperatureExample() {
  console.log('\n=== Temperature Comparison ===');

  const prompt = 'Describe a sunset in one sentence.';
  const temperatures = [0, 0.5, 1.0, 1.5];

  for (const temp of temperatures) {
    const { text } = await generateText({
      model: openai('gpt-4'),
      prompt,
      temperature: temp,
      maxTokens: 100,
    });

    console.log(`\nTemperature ${temp}:`);
    console.log(text);
  }
}

// ============================================================================
// Example 8: Multi-Provider Support
// ============================================================================

async function multiProviderExample() {
  console.log('\n=== Multi-Provider Example ===');

  const prompt = 'Explain recursion in programming in 2 sentences.';

  // OpenAI
  console.log('OpenAI GPT-4:');
  const { text: openaiResponse } = await generateText({
    model: openai('gpt-4'),
    prompt,
  });
  console.log(openaiResponse);

  // Anthropic Claude (if API key available)
  if (process.env.ANTHROPIC_API_KEY) {
    console.log('\nAnthropic Claude:');
    const { text: claudeResponse } = await generateText({
      model: anthropic('claude-3-5-sonnet-20241022'),
      prompt,
    });
    console.log(claudeResponse);
  }
}

// ============================================================================
// Example 9: Complex Structured Output
// ============================================================================

async function complexStructuredOutput() {
  console.log('\n=== Complex Structured Output ===');

  const RecipeSchema = z.object({
    name: z.string(),
    description: z.string(),
    ingredients: z.array(
      z.object({
        name: z.string(),
        amount: z.string(),
        unit: z.string(),
      })
    ),
    steps: z.array(z.string()),
    prepTime: z.number().describe('Preparation time in minutes'),
    cookTime: z.number().describe('Cooking time in minutes'),
    servings: z.number(),
    difficulty: z.enum(['easy', 'medium', 'hard']),
  });

  const { object: recipe } = await generateObject({
    model: openai('gpt-4'),
    schema: RecipeSchema,
    prompt: 'Generate a recipe for chocolate chip cookies',
  });

  console.log('Generated Recipe:');
  console.log(JSON.stringify(recipe, null, 2));
}

// ============================================================================
// Example 10: Chained Generation
// ============================================================================

async function chainedGeneration() {
  console.log('\n=== Chained Generation ===');

  // Step 1: Generate topic
  const { text: topic } = await generateText({
    model: openai('gpt-4'),
    prompt: 'Suggest a specific topic related to artificial intelligence',
  });

  console.log(`Topic: ${topic}`);

  // Step 2: Create outline
  const { text: outline } = await generateText({
    model: openai('gpt-4'),
    prompt: `Create a brief 3-point outline for an article about: ${topic}`,
  });

  console.log(`\nOutline:\n${outline}`);

  // Step 3: Write content
  const { text: article } = await generateText({
    model: openai('gpt-4'),
    prompt: `Write a 2-paragraph article based on this outline:\n${outline}\n\nTopic: ${topic}`,
    maxTokens: 500,
  });

  console.log(`\nArticle:\n${article}`);
}

// ============================================================================
// Example 11: Streaming with Tool Calls
// ============================================================================

async function streamingWithTools() {
  console.log('\n=== Streaming with Tool Calls ===');

  const result = await streamText({
    model: openai('gpt-4'),
    tools: {
      getWeather: tool({
        description: 'Get weather for a location',
        parameters: z.object({
          location: z.string(),
        }),
        execute: async ({ location }) => ({
          location,
          temperature: 22,
          condition: 'Sunny',
        }),
      }),
    },
    prompt: 'What is the weather in Paris?',
    maxToolRoundtrips: 3,
  });

  console.log('Streaming response with tool calls:');

  for await (const chunk of result.fullStream) {
    if (chunk.type === 'tool-call') {
      console.log(`\nTool called: ${chunk.toolName}`);
      console.log(`Arguments: ${JSON.stringify(chunk.args)}`);
    } else if (chunk.type === 'tool-result') {
      console.log(`Tool result: ${JSON.stringify(chunk.result)}`);
    } else if (chunk.type === 'text-delta') {
      process.stdout.write(chunk.textDelta);
    }
  }

  console.log('\n');
}

// ============================================================================
// Example 12: Error Handling and Retries
// ============================================================================

async function errorHandlingExample() {
  console.log('\n=== Error Handling Example ===');

  try {
    const { text } = await generateText({
      model: openai('gpt-4'),
      prompt: 'Explain machine learning',
      maxRetries: 3, // Retry on failures
      abortSignal: AbortSignal.timeout(30000), // 30 second timeout
    });

    console.log(text);
  } catch (error) {
    if (error instanceof Error) {
      console.error(`Error: ${error.message}`);

      // Fallback to different model
      console.log('\nRetrying with Claude...');
      if (process.env.ANTHROPIC_API_KEY) {
        const { text } = await generateText({
          model: anthropic('claude-3-haiku-20240307'), // Faster, cheaper fallback
          prompt: 'Explain machine learning',
        });
        console.log(text);
      }
    }
  }
}

// ============================================================================
// Example 13: JSON Mode vs Structured Output
// ============================================================================

async function jsonModeComparison() {
  console.log('\n=== JSON Mode vs Structured Output ===');

  // Method 1: Prompt engineering for JSON
  console.log('Method 1: Prompt Engineering');
  const { text: jsonText } = await generateText({
    model: openai('gpt-4'),
    prompt: `Extract name and age as JSON: "Alice is 25 years old"

Output valid JSON only:`,
  });

  console.log(jsonText);

  // Method 2: Structured output with schema
  console.log('\nMethod 2: Structured Output (type-safe)');
  const { object } = await generateObject({
    model: openai('gpt-4'),
    schema: z.object({
      name: z.string(),
      age: z.number(),
    }),
    prompt: 'Extract name and age: "Alice is 25 years old"',
  });

  console.log(JSON.stringify(object, null, 2));
  console.log(`Type-safe access: ${object.name} is ${object.age} years old`);
}

// ============================================================================
// Example 14: Multi-Step Agent
// ============================================================================

async function multiStepAgent() {
  console.log('\n=== Multi-Step Agent ===');

  const researchTool = tool({
    description: 'Research a topic and return findings',
    parameters: z.object({
      topic: z.string(),
    }),
    execute: async ({ topic }) => {
      return `Research findings about ${topic}: [Mock research data about ${topic}]`;
    },
  });

  const analyzeTool = tool({
    description: 'Analyze data and extract insights',
    parameters: z.object({
      data: z.string(),
    }),
    execute: async ({ data }) => {
      return `Analysis of data: [Mock analysis insights from: ${data.substring(0, 50)}...]`;
    },
  });

  const { text, toolCalls } = await generateText({
    model: openai('gpt-4'),
    tools: {
      research: researchTool,
      analyze: analyzeTool,
    },
    prompt: 'Research quantum computing and analyze the findings',
    maxToolRoundtrips: 5,
  });

  console.log('Agent steps:');
  toolCalls.forEach((call, index) => {
    console.log(`\nStep ${index + 1}: ${call.toolName}`);
    console.log(`Arguments: ${JSON.stringify(call.args)}`);
  });

  console.log('\nFinal response:');
  console.log(text);
}

// ============================================================================
// Main Execution
// ============================================================================

async function main() {
  const examples: Array<[string, () => Promise<void>]> = [
    ['Basic Text Generation', basicTextGeneration],
    ['System Prompt', systemPromptExample],
    ['Streaming', streamingExample],
    ['Structured Output', structuredOutputExample],
    ['Multi-Turn Conversation', conversationExample],
    ['Tool Use', toolUseExample],
    ['Temperature Comparison', temperatureExample],
    ['Multi-Provider', multiProviderExample],
    ['Complex Structured Output', complexStructuredOutput],
    ['Chained Generation', chainedGeneration],
    ['Streaming with Tools', streamingWithTools],
    ['Error Handling', errorHandlingExample],
    ['JSON Mode Comparison', jsonModeComparison],
    ['Multi-Step Agent', multiStepAgent],
  ];

  console.log('Vercel AI SDK Examples');
  console.log('='.repeat(60));

  for (const [name, exampleFunc] of examples) {
    try {
      await exampleFunc();
    } catch (error) {
      console.error(`\nError in ${name}:`, error);
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('All examples completed!');
}

// Check for API key
if (!process.env.OPENAI_API_KEY) {
  console.error('Error: OPENAI_API_KEY environment variable not set');
  console.error('Set it with: export OPENAI_API_KEY="your-api-key"');
  process.exit(1);
}

main().catch(console.error);
