/**
 * LLM-as-Judge Evaluation (TypeScript)
 *
 * Demonstrates using GPT-4/Claude as evaluators with Vercel AI SDK,
 * structured outputs, and type-safe evaluation results.
 *
 * Installation:
 *   npm install ai openai @anthropic-ai/sdk zod
 *
 * Usage:
 *   export OPENAI_API_KEY=your_key
 *   npx tsx llm-as-judge.ts
 */

import OpenAI from "openai";
import { z } from "zod";

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

interface EvaluationResult {
  score: number;
  reasoning: string;
  metadata?: Record<string, any>;
}

interface RubricScore {
  score: number;
  reasoning: string;
}

interface RubricEvaluation {
  accuracy: RubricScore;
  relevance: RubricScore;
  clarity: RubricScore;
  completeness: RubricScore;
  overallReasoning: string;
}

interface PairwiseResult {
  winner: "A" | "B";
  reasoning: string;
}

// ============================================================================
// ZOD SCHEMAS FOR STRUCTURED OUTPUTS
// ============================================================================

const SinglePointSchema = z.object({
  score: z.number().min(1).max(5),
  reasoning: z.string(),
});

const RubricScoreSchema = z.object({
  score: z.number().min(1).max(5),
  reasoning: z.string(),
});

const RubricEvaluationSchema = z.object({
  accuracy: RubricScoreSchema,
  relevance: RubricScoreSchema,
  clarity: RubricScoreSchema,
  completeness: RubricScoreSchema,
  overall_reasoning: z.string(),
});

const PairwiseSchema = z.object({
  winner: z.enum(["A", "B"]),
  reasoning: z.string(),
});

const HallucinationSchema = z.object({
  supported_claims: z.array(z.string()),
  unsupported_claims: z.array(z.string()),
  faithfulness_score: z.number().min(0).max(1),
  reasoning: z.string(),
});

// ============================================================================
// SINGLE-POINT GRADING
// ============================================================================

async function evaluateQualitySinglePoint(
  prompt: string,
  response: string,
  evaluatorModel: string = "gpt-4"
): Promise<EvaluationResult> {
  const client = new OpenAI();

  const evalPrompt = `Evaluate the following LLM response for quality.

USER QUERY: ${prompt}
LLM RESPONSE: ${response}

Rate the response on a 1-5 scale:
5 - Excellent: Accurate, complete, directly addresses query
4 - Good: Mostly accurate, minor gaps or ambiguities
3 - Acceptable: Partially helpful, missing key information
2 - Poor: Tangentially related, mostly unhelpful
1 - Very Poor: Irrelevant or incorrect

Provide your evaluation in JSON format:
{
  "score": <1-5>,
  "reasoning": "<1-2 sentences explaining the score>"
}`;

  const completion = await client.chat.completions.create({
    model: evaluatorModel,
    messages: [{ role: "user", content: evalPrompt }],
    temperature: 0.3,
    response_format: { type: "json_object" },
  });

  const result = JSON.parse(completion.choices[0].message.content!);
  const validated = SinglePointSchema.parse(result);

  return {
    score: validated.score,
    reasoning: validated.reasoning,
  };
}

// ============================================================================
// RUBRIC-BASED EVALUATION
// ============================================================================

async function evaluateWithRubric(
  prompt: string,
  response: string,
  evaluatorModel: string = "gpt-4"
): Promise<EvaluationResult> {
  const client = new OpenAI();

  const evalPrompt = `Evaluate the LLM response across multiple dimensions.

USER QUERY: ${prompt}
LLM RESPONSE: ${response}

Rate each dimension on a 1-5 scale:

1. ACCURACY (Weight: 40%)
   1 - Major factual errors
   3 - Minor errors or ambiguities
   5 - Fully accurate and precise

2. RELEVANCE (Weight: 30%)
   1 - Off-topic or tangential
   3 - Partially addresses query
   5 - Directly and completely addresses query

3. CLARITY (Weight: 20%)
   1 - Confusing or poorly structured
   3 - Understandable with effort
   5 - Crystal clear and well-organized

4. COMPLETENESS (Weight: 10%)
   1 - Major information gaps
   3 - Minor missing details
   5 - Comprehensive and thorough

Provide evaluation in JSON format:
{
  "accuracy": {"score": <1-5>, "reasoning": "<explanation>"},
  "relevance": {"score": <1-5>, "reasoning": "<explanation>"},
  "clarity": {"score": <1-5>, "reasoning": "<explanation>"},
  "completeness": {"score": <1-5>, "reasoning": "<explanation>"},
  "overall_reasoning": "<2-3 sentences covering all dimensions>"
}`;

  const completion = await client.chat.completions.create({
    model: evaluatorModel,
    messages: [{ role: "user", content: evalPrompt }],
    temperature: 0.3,
    response_format: { type: "json_object" },
  });

  const result = JSON.parse(completion.choices[0].message.content!);
  const validated = RubricEvaluationSchema.parse(result);

  // Calculate weighted score
  const weights = {
    accuracy: 0.4,
    relevance: 0.3,
    clarity: 0.2,
    completeness: 0.1,
  };

  const weightedScore =
    validated.accuracy.score * weights.accuracy +
    validated.relevance.score * weights.relevance +
    validated.clarity.score * weights.clarity +
    validated.completeness.score * weights.completeness;

  return {
    score: weightedScore,
    reasoning: validated.overall_reasoning,
    metadata: {
      accuracy: validated.accuracy,
      relevance: validated.relevance,
      clarity: validated.clarity,
      completeness: validated.completeness,
    },
  };
}

// ============================================================================
// PAIRWISE COMPARISON
// ============================================================================

async function pairwiseComparison(
  prompt: string,
  responseA: string,
  responseB: string,
  evaluatorModel: string = "gpt-4"
): Promise<{ winner: string; reasoning: string }> {
  const client = new OpenAI();

  const evalPrompt = `Compare the following two LLM responses to the same query.

USER QUERY: ${prompt}

RESPONSE A:
${responseA}

RESPONSE B:
${responseB}

Evaluate which response is better based on:
- Accuracy: Factual correctness
- Relevance: Addresses the query directly
- Clarity: Easy to understand
- Completeness: Covers all important aspects

Provide evaluation in JSON format:
{
  "winner": "<A or B>",
  "reasoning": "<2-3 sentences explaining why>"
}`;

  const completion = await client.chat.completions.create({
    model: evaluatorModel,
    messages: [{ role: "user", content: evalPrompt }],
    temperature: 0.3,
    response_format: { type: "json_object" },
  });

  const result = JSON.parse(completion.choices[0].message.content!);
  const validated = PairwiseSchema.parse(result);

  return {
    winner: validated.winner,
    reasoning: validated.reasoning,
  };
}

// ============================================================================
// HALLUCINATION DETECTION
// ============================================================================

async function detectHallucinations(
  response: string,
  context: string,
  evaluatorModel: string = "gpt-4"
): Promise<EvaluationResult> {
  const client = new OpenAI();

  const evalPrompt = `Determine if the LLM response contains hallucinations (unsupported claims).

CONTEXT:
${context}

LLM RESPONSE:
${response}

Task: Identify claims in the response and verify each against the context.

Provide evaluation in JSON format:
{
  "supported_claims": ["<list of claims supported by context>"],
  "unsupported_claims": ["<list of claims NOT supported by context>"],
  "faithfulness_score": <percentage of supported claims (0.0-1.0)>,
  "reasoning": "<explanation>"
}`;

  const completion = await client.chat.completions.create({
    model: evaluatorModel,
    messages: [{ role: "user", content: evalPrompt }],
    temperature: 0.3,
    response_format: { type: "json_object" },
  });

  const result = JSON.parse(completion.choices[0].message.content!);
  const validated = HallucinationSchema.parse(result);

  return {
    score: validated.faithfulness_score,
    reasoning: validated.reasoning,
    metadata: {
      supportedClaims: validated.supported_claims,
      unsupportedClaims: validated.unsupported_claims,
    },
  };
}

// ============================================================================
// BATCH EVALUATION
// ============================================================================

interface TestCase {
  prompt: string;
  response: string;
}

async function batchEvaluate(
  testCases: TestCase[],
  evaluationFn: (prompt: string, response: string) => Promise<EvaluationResult>,
  evaluatorModel: string = "gpt-4"
): Promise<EvaluationResult[]> {
  const results: EvaluationResult[] = [];

  for (let i = 0; i < testCases.length; i++) {
    console.log(`Evaluating ${i + 1}/${testCases.length}...`);

    const result = await evaluationFn(
      testCases[i].prompt,
      testCases[i].response
    );

    results.push(result);
  }

  return results;
}

// ============================================================================
// EXAMPLES
// ============================================================================

async function exampleSinglePointGrading() {
  console.log("\n" + "=".repeat(60));
  console.log("SINGLE-POINT GRADING EXAMPLE");
  console.log("=".repeat(60));

  const prompt = "What is the capital of France?";
  const response =
    "The capital of France is Paris, a beautiful city known for the Eiffel Tower.";

  const result = await evaluateQualitySinglePoint(prompt, response);

  console.log(`\nPrompt: ${prompt}`);
  console.log(`Response: ${response}`);
  console.log(`\nScore: ${result.score}/5`);
  console.log(`Reasoning: ${result.reasoning}`);
}

async function exampleRubricEvaluation() {
  console.log("\n" + "=".repeat(60));
  console.log("RUBRIC-BASED EVALUATION EXAMPLE");
  console.log("=".repeat(60));

  const prompt = "Explain how photosynthesis works";
  const response =
    "Photosynthesis is the process by which plants convert light energy into chemical energy. " +
    "Chlorophyll absorbs sunlight, which is used to convert CO2 and water into glucose and oxygen.";

  const result = await evaluateWithRubric(prompt, response);

  console.log(`\nPrompt: ${prompt}`);
  console.log(`Response: ${response.substring(0, 100)}...`);
  console.log(`\nOverall Score: ${result.score.toFixed(2)}/5`);
  console.log(`Reasoning: ${result.reasoning}`);

  if (result.metadata) {
    console.log("\nDimension Breakdown:");
    for (const [dim, details] of Object.entries(result.metadata)) {
      const d = details as RubricScore;
      console.log(`  ${dim}: ${d.score}/5 - ${d.reasoning}`);
    }
  }
}

async function examplePairwiseComparison() {
  console.log("\n" + "=".repeat(60));
  console.log("PAIRWISE COMPARISON EXAMPLE");
  console.log("=".repeat(60));

  const prompt = "What are the benefits of exercise?";
  const responseA = "Exercise is good for you. It helps you stay healthy.";
  const responseB =
    "Exercise has numerous benefits including improved cardiovascular health, " +
    "stronger muscles and bones, better mental health, and reduced risk of chronic diseases.";

  const result = await pairwiseComparison(prompt, responseA, responseB);

  console.log(`\nPrompt: ${prompt}`);
  console.log(`\nResponse A: ${responseA}`);
  console.log(`Response B: ${responseB}`);
  console.log(`\nWinner: ${result.winner}`);
  console.log(`Reasoning: ${result.reasoning}`);
}

async function exampleHallucinationDetection() {
  console.log("\n" + "=".repeat(60));
  console.log("HALLUCINATION DETECTION EXAMPLE");
  console.log("=".repeat(60));

  const context =
    "Paris is the capital of France. The population of Paris is approximately 2.2 million people. " +
    "The Eiffel Tower is located in Paris.";
  const response =
    "Paris is the capital of France with a population of 5 million people.";

  const result = await detectHallucinations(response, context);

  console.log(`\nContext: ${context}`);
  console.log(`Response: ${response}`);
  console.log(`\nFaithfulness Score: ${result.score.toFixed(2)}`);
  console.log(`Reasoning: ${result.reasoning}`);

  if (result.metadata) {
    console.log(`\nSupported Claims: ${result.metadata.supportedClaims}`);
    console.log(`Unsupported Claims: ${result.metadata.unsupportedClaims}`);
  }
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  // Check for API key
  if (!process.env.OPENAI_API_KEY) {
    console.error("⚠️  Error: OPENAI_API_KEY not set");
    console.error("Set it with: export OPENAI_API_KEY=your_key");
    process.exit(1);
  }

  console.log("=".repeat(60));
  console.log("LLM-AS-JUDGE EVALUATION (TypeScript)");
  console.log("=".repeat(60));

  try {
    await exampleSinglePointGrading();
    await exampleRubricEvaluation();
    await examplePairwiseComparison();
    await exampleHallucinationDetection();

    console.log("\n" + "=".repeat(60));
    console.log("ALL EXAMPLES COMPLETE");
    console.log("=".repeat(60));
  } catch (error) {
    console.error("\n❌ Error:", error);
    console.error("\nTroubleshooting:");
    console.error("1. Verify OPENAI_API_KEY is set correctly");
    console.error("2. Check internet connection");
    console.error("3. Ensure sufficient API credits");
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

// Export functions for use in other modules
export {
  evaluateQualitySinglePoint,
  evaluateWithRubric,
  pairwiseComparison,
  detectHallucinations,
  batchEvaluate,
};
