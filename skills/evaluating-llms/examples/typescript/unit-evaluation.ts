/**
 * Unit Testing for LLM Outputs (TypeScript)
 *
 * Demonstrates unit testing patterns using Vitest/Jest with type safety,
 * exact match, fuzzy matching, and semantic similarity checks.
 *
 * Installation:
 *   npm install vitest openai @types/node
 *
 * Usage:
 *   npx vitest run unit-evaluation.ts
 *   # Or run directly:
 *   npx tsx unit-evaluation.ts
 */

import { describe, test, expect } from "vitest";
import OpenAI from "openai";

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

async function classifySentiment(
  text: string,
  model: string = "gpt-3.5-turbo"
): Promise<string> {
  const client = new OpenAI();

  const response = await client.chat.completions.create({
    model,
    messages: [
      {
        role: "system",
        content:
          "Classify sentiment as positive, negative, or neutral. Return only the label.",
      },
      { role: "user", content: text },
    ],
    temperature: 0,
  });

  return response.choices[0].message.content!.trim().toLowerCase();
}

async function extractEmail(
  text: string,
  model: string = "gpt-3.5-turbo"
): Promise<string> {
  const client = new OpenAI();

  const response = await client.chat.completions.create({
    model,
    messages: [
      {
        role: "system",
        content: "Extract the email address from the text. Return only the email.",
      },
      { role: "user", content: text },
    ],
    temperature: 0,
  });

  return response.choices[0].message.content!.trim();
}

async function extractStructuredData(
  text: string,
  model: string = "gpt-3.5-turbo"
): Promise<string> {
  const client = new OpenAI();

  const response = await client.chat.completions.create({
    model,
    messages: [
      {
        role: "system",
        content:
          'Extract name, age, and city as JSON: {"name": "...", "age": ..., "city": "..."}',
      },
      { role: "user", content: text },
    ],
    temperature: 0,
    response_format: { type: "json_object" },
  });

  return response.choices[0].message.content!;
}

function normalizeText(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function fuzzyMatch(text1: string, text2: string, threshold: number = 0.8): boolean {
  const norm1 = normalizeText(text1);
  const norm2 = normalizeText(text2);

  // Simple Levenshtein-based similarity
  const maxLen = Math.max(norm1.length, norm2.length);
  if (maxLen === 0) return true;

  const distance = levenshteinDistance(norm1, norm2);
  const similarity = 1 - distance / maxLen;

  return similarity >= threshold;
}

function levenshteinDistance(s1: string, s2: string): number {
  const m = s1.length;
  const n = s2.length;
  const dp: number[][] = Array(m + 1)
    .fill(null)
    .map(() => Array(n + 1).fill(0));

  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (s1[i - 1] === s2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
      }
    }
  }

  return dp[m][n];
}

// ============================================================================
// EXACT MATCH TESTS
// ============================================================================

describe("Sentiment Classification - Exact Match", () => {
  test("should classify positive sentiment correctly", async () => {
    const result = await classifySentiment("I love this product!");
    expect(result).toBe("positive");
  });

  test("should classify negative sentiment correctly", async () => {
    const result = await classifySentiment("This is terrible and disappointing.");
    expect(result).toBe("negative");
  });

  test("should classify neutral sentiment correctly", async () => {
    const result = await classifySentiment("The product arrived on time.");
    expect(result).toBe("neutral");
  });
});

// ============================================================================
// REGEX PATTERN MATCHING
// ============================================================================

describe("Email Extraction - Pattern Matching", () => {
  test("should extract email in valid format", async () => {
    const text = "Please contact me at john.doe@example.com for more information.";
    const result = await extractEmail(text);

    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    expect(result).toMatch(emailPattern);
  });

  test("should extract correct email", async () => {
    const text = "Contact support@company.com for help.";
    const result = await extractEmail(text);
    expect(result).toBe("support@company.com");
  });
});

// ============================================================================
// JSON SCHEMA VALIDATION
// ============================================================================

describe("Structured Data Extraction - JSON Validation", () => {
  test("should return valid JSON", async () => {
    const text = "John Smith is 35 years old and lives in San Francisco.";
    const result = await extractStructuredData(text);

    const data = JSON.parse(result);
    expect(typeof data).toBe("object");
  });

  test("should contain required fields", async () => {
    const text = "Jane Doe is 28 years old and lives in New York.";
    const result = await extractStructuredData(text);

    const data = JSON.parse(result);
    expect(data).toHaveProperty("name");
    expect(data).toHaveProperty("age");
    expect(data).toHaveProperty("city");
  });

  test("should have correct field types", async () => {
    const text = "Bob Johnson is 42 years old and lives in Chicago.";
    const result = await extractStructuredData(text);

    const data = JSON.parse(result);
    expect(typeof data.name).toBe("string");
    expect(typeof data.age).toBe("number");
    expect(typeof data.city).toBe("string");
  });
});

// ============================================================================
// KEYWORD PRESENCE TESTS
// ============================================================================

describe("Summary Generation - Keyword Presence", () => {
  async function generateSummary(
    text: string,
    model: string = "gpt-3.5-turbo"
  ): Promise<string> {
    const client = new OpenAI();

    const response = await client.chat.completions.create({
      model,
      messages: [
        { role: "system", content: "Summarize the following text in 2-3 sentences." },
        { role: "user", content: text },
      ],
      temperature: 0,
    });

    return response.choices[0].message.content!;
  }

  test("should contain important keywords", async () => {
    const text =
      "Climate change is causing rising global temperatures. " +
      "Scientists warn that immediate action is needed to reduce greenhouse gas emissions. " +
      "Renewable energy sources are crucial for addressing this challenge.";

    const result = await generateSummary(text);

    const keywords = ["climate", "temperature", "emission", "energy"];
    const foundKeywords = keywords.filter((kw) =>
      result.toLowerCase().includes(kw.toLowerCase())
    );

    expect(foundKeywords.length).toBeGreaterThanOrEqual(2);
  });

  test("should have appropriate length", async () => {
    const text = "Lorem ipsum dolor sit amet. ".repeat(50);
    const result = await generateSummary(text);

    const wordCount = result.split(/\s+/).length;
    expect(wordCount).toBeGreaterThanOrEqual(10);
    expect(wordCount).toBeLessThanOrEqual(100);
  });
});

// ============================================================================
// FUZZY MATCHING
// ============================================================================

describe("Question Answering - Fuzzy Match", () => {
  async function answerQuestion(
    question: string,
    model: string = "gpt-3.5-turbo"
  ): Promise<string> {
    const client = new OpenAI();

    const response = await client.chat.completions.create({
      model,
      messages: [
        { role: "system", content: "Answer the question concisely." },
        { role: "user", content: question },
      ],
      temperature: 0,
    });

    return response.choices[0].message.content!;
  }

  test("should match expected answer (fuzzy)", async () => {
    const question = "What is the capital of Japan?";
    const expected = "Tokyo";

    const result = await answerQuestion(question);

    expect(fuzzyMatch(result, expected, 0.5)).toBe(true);
  });

  test("should be deterministic with temperature=0", async () => {
    const question = "What is 2+2?";

    const result1 = await answerQuestion(question);
    const result2 = await answerQuestion(question);

    expect(fuzzyMatch(result1, result2, 0.9)).toBe(true);
  });
});

// ============================================================================
// BINARY PASS/FAIL TESTS
// ============================================================================

describe("Response Quality - Binary Checks", () => {
  function isResponseHelpful(response: string): boolean {
    if (response.length < 10) return false;

    const unhelpfulPhrases = [
      "i don't know",
      "i cannot help",
      "i can't answer",
      "no information",
    ];

    const responseLower = response.toLowerCase();
    return !unhelpfulPhrases.some((phrase) => responseLower.includes(phrase));
  }

  async function answerQuestion(question: string): Promise<string> {
    const client = new OpenAI();

    const response = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "Answer the question concisely." },
        { role: "user", content: question },
      ],
      temperature: 0,
    });

    return response.choices[0].message.content!;
  }

  test("should provide helpful response", async () => {
    const question = "How do I reset my password?";
    const result = await answerQuestion(question);

    expect(isResponseHelpful(result)).toBe(true);
  });
});

// ============================================================================
// PARAMETRIZED TESTS
// ============================================================================

describe("Sentiment Classification - Parametrized", () => {
  const testCases: [string, string][] = [
    ["I absolutely love this!", "positive"],
    ["This is awful and terrible.", "negative"],
    ["The package arrived.", "neutral"],
    ["Amazing product, highly recommend!", "positive"],
  ];

  test.each(testCases)(
    "should classify '%s' as '%s'",
    async (input, expected) => {
      const result = await classifySentiment(input);
      expect(result).toBe(expected);
    }
  );
});

// ============================================================================
// PROGRAMMATIC TEST RUNNER (for non-vitest execution)
// ============================================================================

async function runAllTests() {
  console.log("=".repeat(60));
  console.log("RUNNING UNIT TESTS FOR LLM OUTPUTS (TypeScript)");
  console.log("=".repeat(60));

  const tests: [string, () => Promise<void>][] = [
    [
      "Positive Sentiment",
      async () => {
        const result = await classifySentiment("I love this product!");
        if (result !== "positive") throw new Error(`Expected positive, got ${result}`);
      },
    ],
    [
      "Email Format",
      async () => {
        const text = "Contact john@example.com";
        const result = await extractEmail(text);
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(result)) throw new Error("Invalid email format");
      },
    ],
    [
      "JSON Format",
      async () => {
        const text = "John is 30 and lives in NYC";
        const result = await extractStructuredData(text);
        JSON.parse(result); // Will throw if invalid
      },
    ],
  ];

  let passed = 0;
  let failed = 0;

  for (const [name, testFn] of tests) {
    try {
      await testFn();
      console.log(`✅ ${name}: PASS`);
      passed++;
    } catch (error) {
      console.log(`❌ ${name}: FAIL - ${error}`);
      failed++;
    }
  }

  console.log("\n" + "=".repeat(60));
  console.log(`Results: ${passed} passed, ${failed} failed`);
  console.log("=".repeat(60));
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("⚠️  Warning: OPENAI_API_KEY not set");
    console.error("Set it with: export OPENAI_API_KEY=your_key");
    console.error("\nSome tests will fail without API key.\n");
  }

  console.log("Run with vitest for better output:");
  console.log("  npx vitest run unit-evaluation.ts\n");
  console.log("Running tests programmatically...\n");

  await runAllTests();
}

// Run if executed directly
if (require.main === module) {
  main();
}
