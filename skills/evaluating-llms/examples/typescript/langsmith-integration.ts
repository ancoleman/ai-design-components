/**
 * LangSmith Integration for Production Evaluation
 *
 * Demonstrates using LangSmith for dataset management, evaluation runs,
 * and production monitoring with TypeScript.
 *
 * Installation:
 *   npm install langsmith openai @langchain/openai @langchain/core
 *
 * Usage:
 *   export LANGCHAIN_API_KEY=your_key
 *   export OPENAI_API_KEY=your_key
 *   npx tsx langsmith-integration.ts
 */

import { Client, Run, Example } from "langsmith";
import { ChatOpenAI } from "@langchain/openai";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { ChatPromptTemplate } from "@langchain/core/prompts";

// ============================================================================
// LANGSMITH CLIENT SETUP
// ============================================================================

const client = new Client({
  apiKey: process.env.LANGCHAIN_API_KEY,
});

// ============================================================================
// DATASET MANAGEMENT
// ============================================================================

interface DatasetExample {
  input: string;
  expectedOutput?: string;
  metadata?: Record<string, any>;
}

async function createDataset(
  datasetName: string,
  examples: DatasetExample[]
): Promise<void> {
  console.log(`Creating dataset: ${datasetName}...`);

  // Create dataset
  const dataset = await client.createDataset(datasetName, {
    description: "Evaluation dataset for LLM testing",
  });

  // Add examples
  for (const example of examples) {
    await client.createExample(
      { input: example.input },
      { output: example.expectedOutput },
      { datasetId: dataset.id, metadata: example.metadata }
    );
  }

  console.log(`✅ Created dataset with ${examples.length} examples`);
}

async function listDatasets(): Promise<void> {
  console.log("\nListing datasets...");

  const datasets = [];
  for await (const dataset of client.listDatasets()) {
    datasets.push(dataset);
  }

  console.log(`\nFound ${datasets.length} datasets:`);
  datasets.forEach((ds) => {
    console.log(`  - ${ds.name} (${ds.example_count || 0} examples)`);
  });
}

// ============================================================================
// EVALUATION FUNCTIONS
// ============================================================================

async function questionAnswerSystem(input: string): Promise<string> {
  const llm = new ChatOpenAI({
    modelName: "gpt-3.5-turbo",
    temperature: 0,
  });

  const prompt = ChatPromptTemplate.fromMessages([
    ["system", "Answer the question concisely and accurately."],
    ["human", "{input}"],
  ]);

  const chain = prompt.pipe(llm).pipe(new StringOutputParser());
  const response = await chain.invoke({ input });

  return response;
}

async function exactMatchEvaluator(
  run: Run,
  example: Example
): Promise<{ key: string; score: number }> {
  const predicted = run.outputs?.output || "";
  const expected = example.outputs?.output || "";

  const score = predicted.toLowerCase().trim() === expected.toLowerCase().trim() ? 1 : 0;

  return {
    key: "exact_match",
    score,
  };
}

async function containsEvaluator(
  run: Run,
  example: Example
): Promise<{ key: string; score: number }> {
  const predicted = run.outputs?.output || "";
  const expected = example.outputs?.output || "";

  const score = predicted.toLowerCase().includes(expected.toLowerCase()) ? 1 : 0;

  return {
    key: "contains",
    score,
  };
}

// ============================================================================
// RUNNING EVALUATIONS
// ============================================================================

async function runEvaluation(datasetName: string): Promise<void> {
  console.log(`\nRunning evaluation on dataset: ${datasetName}...`);

  // Wrapper function for LangSmith
  async function predictFn(input: Record<string, any>): Promise<Record<string, any>> {
    const output = await questionAnswerSystem(input.input);
    return { output };
  }

  // Run evaluation
  const results = await client.evaluate(predictFn, {
    data: datasetName,
    evaluators: [exactMatchEvaluator, containsEvaluator],
    experimentPrefix: "qa-eval",
    metadata: {
      model: "gpt-3.5-turbo",
      temperature: 0,
    },
  });

  console.log("\n✅ Evaluation complete!");
  console.log(`Results: ${results.results?.length || 0} examples evaluated`);
}

// ============================================================================
// PRODUCTION MONITORING
// ============================================================================

interface ProductionRunConfig {
  projectName: string;
  runName: string;
  tags?: string[];
}

async function trackProductionRun(
  config: ProductionRunConfig,
  inputData: any,
  runFunction: (input: any) => Promise<any>
): Promise<any> {
  // Create run
  const run = await client.createRun({
    name: config.runName,
    run_type: "chain",
    inputs: inputData,
    project_name: config.projectName,
    tags: config.tags,
  });

  try {
    // Execute function
    const output = await runFunction(inputData);

    // Update run with output
    await client.updateRun(run.id, {
      outputs: output,
      end_time: Date.now(),
    });

    return output;
  } catch (error) {
    // Log error
    await client.updateRun(run.id, {
      error: error instanceof Error ? error.message : String(error),
      end_time: Date.now(),
    });

    throw error;
  }
}

async function addUserFeedback(
  runId: string,
  score: number,
  comment?: string
): Promise<void> {
  await client.createFeedback(runId, "user_rating", {
    score,
    comment,
  });

  console.log(`✅ Feedback added to run ${runId}`);
}

// ============================================================================
// A/B TESTING
// ============================================================================

interface ABTestConfig {
  variantA: {
    name: string;
    runFn: (input: any) => Promise<any>;
  };
  variantB: {
    name: string;
    runFn: (input: any) => Promise<any>;
  };
  datasetName: string;
}

async function runABTest(config: ABTestConfig): Promise<void> {
  console.log("\nRunning A/B test...");

  // Evaluate Variant A
  console.log(`\nEvaluating ${config.variantA.name}...`);
  const resultsA = await client.evaluate(
    async (input: Record<string, any>) => {
      const output = await config.variantA.runFn(input.input);
      return { output };
    },
    {
      data: config.datasetName,
      evaluators: [exactMatchEvaluator, containsEvaluator],
      experimentPrefix: `ab-test-${config.variantA.name}`,
    }
  );

  // Evaluate Variant B
  console.log(`\nEvaluating ${config.variantB.name}...`);
  const resultsB = await client.evaluate(
    async (input: Record<string, any>) => {
      const output = await config.variantB.runFn(input.input);
      return { output };
    },
    {
      data: config.datasetName,
      evaluators: [exactMatchEvaluator, containsEvaluator],
      experimentPrefix: `ab-test-${config.variantB.name}`,
    }
  );

  console.log("\n" + "=".repeat(60));
  console.log("A/B TEST RESULTS");
  console.log("=".repeat(60));
  console.log(`Variant A (${config.variantA.name}): ${resultsA.results?.length || 0} examples`);
  console.log(`Variant B (${config.variantB.name}): ${resultsB.results?.length || 0} examples`);
}

// ============================================================================
// REGRESSION TESTING
// ============================================================================

async function runRegressionTest(
  datasetName: string,
  baselineExperimentId: string
): Promise<void> {
  console.log("\nRunning regression test...");

  // Run current evaluation
  const currentResults = await client.evaluate(
    async (input: Record<string, any>) => {
      const output = await questionAnswerSystem(input.input);
      return { output };
    },
    {
      data: datasetName,
      evaluators: [exactMatchEvaluator],
      experimentPrefix: "regression-test",
    }
  );

  console.log("\n✅ Regression test complete!");
  console.log(`Compare results against baseline: ${baselineExperimentId}`);
  console.log("View comparison at: https://smith.langchain.com/");
}

// ============================================================================
// EXAMPLES
// ============================================================================

async function exampleDatasetCreation() {
  console.log("\n" + "=".repeat(60));
  console.log("DATASET CREATION EXAMPLE");
  console.log("=".repeat(60));

  const examples: DatasetExample[] = [
    {
      input: "What is the capital of France?",
      expectedOutput: "Paris",
      metadata: { category: "geography" },
    },
    {
      input: "Who wrote Romeo and Juliet?",
      expectedOutput: "William Shakespeare",
      metadata: { category: "literature" },
    },
    {
      input: "What is 2+2?",
      expectedOutput: "4",
      metadata: { category: "math" },
    },
  ];

  const datasetName = `qa-dataset-${Date.now()}`;

  try {
    await createDataset(datasetName, examples);
    await listDatasets();
  } catch (error) {
    console.error("Error creating dataset:", error);
  }
}

async function exampleEvaluation() {
  console.log("\n" + "=".repeat(60));
  console.log("EVALUATION EXAMPLE");
  console.log("=".repeat(60));

  // Note: Replace with actual dataset name
  const datasetName = "qa-dataset-example";

  try {
    await runEvaluation(datasetName);
  } catch (error) {
    console.error("Error running evaluation:", error);
    console.log("\nTip: Create a dataset first using exampleDatasetCreation()");
  }
}

async function exampleProductionMonitoring() {
  console.log("\n" + "=".repeat(60));
  console.log("PRODUCTION MONITORING EXAMPLE");
  console.log("=".repeat(60));

  const config: ProductionRunConfig = {
    projectName: "production-qa-system",
    runName: "customer-query",
    tags: ["production", "customer-support"],
  };

  const input = { input: "How do I reset my password?" };

  try {
    const output = await trackProductionRun(config, input, async (data) => {
      return await questionAnswerSystem(data.input);
    });

    console.log(`\nInput: ${input.input}`);
    console.log(`Output: ${output}`);
  } catch (error) {
    console.error("Error in production run:", error);
  }
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  // Check for API keys
  if (!process.env.LANGCHAIN_API_KEY) {
    console.error("⚠️  Error: LANGCHAIN_API_KEY not set");
    console.error("Set it with: export LANGCHAIN_API_KEY=your_key");
    console.error("Get your key at: https://smith.langchain.com/");
    process.exit(1);
  }

  if (!process.env.OPENAI_API_KEY) {
    console.error("⚠️  Error: OPENAI_API_KEY not set");
    console.error("Set it with: export OPENAI_API_KEY=your_key");
    process.exit(1);
  }

  console.log("=".repeat(60));
  console.log("LANGSMITH INTEGRATION EXAMPLES");
  console.log("=".repeat(60));

  try {
    await exampleDatasetCreation();
    // await exampleEvaluation();  // Uncomment after dataset created
    await exampleProductionMonitoring();

    console.log("\n" + "=".repeat(60));
    console.log("EXAMPLES COMPLETE");
    console.log("=".repeat(60));

    console.log("\nNext steps:");
    console.log("1. View results at: https://smith.langchain.com/");
    console.log("2. Create evaluation datasets for your use case");
    console.log("3. Set up continuous evaluation in CI/CD");
    console.log("4. Monitor production runs and collect user feedback");
  } catch (error) {
    console.error("\n❌ Error:", error);
    console.error("\nTroubleshooting:");
    console.error("1. Verify LANGCHAIN_API_KEY is set correctly");
    console.error("2. Verify OPENAI_API_KEY is set correctly");
    console.error("3. Check internet connection");
    console.error("4. Ensure LangSmith account is active");
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

// Export functions
export {
  createDataset,
  listDatasets,
  runEvaluation,
  trackProductionRun,
  addUserFeedback,
  runABTest,
  runRegressionTest,
};
