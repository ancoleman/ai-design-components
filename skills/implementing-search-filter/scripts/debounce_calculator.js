#!/usr/bin/env node

/**
 * Calculate optimal debounce timing based on user behavior and network conditions.
 *
 * This script analyzes typing speed, network latency, and device type
 * to recommend the best debounce delay for search inputs.
 */

class DebounceCalculator {
  constructor() {
    // Default configurations
    this.config = {
      // Base delays by user type (milliseconds)
      userTypeDelays: {
        fastTypist: 200,    // 60+ WPM
        averageTypist: 300, // 40-60 WPM
        slowTypist: 400,    // <40 WPM
        mobileUser: 500     // Touch typing
      },

      // Network latency adjustments
      networkAdjustments: {
        fast: 0,      // <50ms latency
        moderate: 50, // 50-150ms latency
        slow: 100,    // 150-300ms latency
        verySlow: 200 // >300ms latency
      },

      // Search complexity adjustments
      complexityAdjustments: {
        simple: 0,     // Basic text search
        moderate: 50,  // Filters + text
        complex: 100,  // Multiple filters, facets
        heavy: 150     // Aggregations, analytics
      }
    };
  }

  /**
   * Calculate typing speed from keystroke timings
   * @param {number[]} keystrokeDelays - Array of delays between keystrokes (ms)
   * @returns {number} Words per minute estimate
   */
  calculateTypingSpeed(keystrokeDelays) {
    if (!keystrokeDelays || keystrokeDelays.length < 5) {
      return 40; // Default to average
    }

    // Calculate average delay between keystrokes
    const avgDelay = keystrokeDelays.reduce((a, b) => a + b, 0) / keystrokeDelays.length;

    // Convert to characters per minute (assuming average 5 chars per word)
    const charsPerMinute = (60000 / avgDelay);
    const wordsPerMinute = charsPerMinute / 5;

    return Math.round(wordsPerMinute);
  }

  /**
   * Determine user type based on typing speed
   * @param {number} wpm - Words per minute
   * @returns {string} User type category
   */
  getUserType(wpm) {
    if (wpm >= 60) return 'fastTypist';
    if (wpm >= 40) return 'averageTypist';
    return 'slowTypist';
  }

  /**
   * Measure network latency category
   * @param {number} latencyMs - Average network latency in milliseconds
   * @returns {string} Network speed category
   */
  getNetworkSpeed(latencyMs) {
    if (latencyMs < 50) return 'fast';
    if (latencyMs < 150) return 'moderate';
    if (latencyMs < 300) return 'slow';
    return 'verySlow';
  }

  /**
   * Determine search complexity
   * @param {Object} searchParams - Search parameters object
   * @returns {string} Complexity level
   */
  getSearchComplexity(searchParams) {
    const filterCount = Object.keys(searchParams.filters || {}).length;
    const hasAggregations = searchParams.includeFacets || false;
    const hasFullText = !!searchParams.query;

    if (filterCount > 5 || hasAggregations) return 'heavy';
    if (filterCount > 2 || (hasFullText && filterCount > 0)) return 'complex';
    if (filterCount > 0 || hasFullText) return 'moderate';
    return 'simple';
  }

  /**
   * Calculate optimal debounce delay
   * @param {Object} params - Calculation parameters
   * @returns {Object} Recommended delays and analysis
   */
  calculateOptimalDebounce(params = {}) {
    const {
      keystrokeDelays = [],
      networkLatency = 100,
      searchParams = {},
      deviceType = 'desktop',
      adaptiveMode = true
    } = params;

    // Calculate typing speed
    const typingSpeed = this.calculateTypingSpeed(keystrokeDelays);
    const userType = deviceType === 'mobile' ? 'mobileUser' : this.getUserType(typingSpeed);

    // Get base delay
    let baseDelay = this.config.userTypeDelays[userType];

    // Adjust for network
    const networkSpeed = this.getNetworkSpeed(networkLatency);
    const networkAdjustment = this.config.networkAdjustments[networkSpeed];

    // Adjust for search complexity
    const complexity = this.getSearchComplexity(searchParams);
    const complexityAdjustment = this.config.complexityAdjustments[complexity];

    // Calculate final delay
    let optimalDelay = baseDelay + networkAdjustment + complexityAdjustment;

    // Apply bounds
    const minDelay = 150; // Minimum to avoid excessive requests
    const maxDelay = 750; // Maximum to maintain responsiveness

    optimalDelay = Math.max(minDelay, Math.min(maxDelay, optimalDelay));

    // Calculate adaptive delays for different scenarios
    const adaptiveDelays = adaptiveMode ? {
      initial: optimalDelay * 1.5,      // First keystroke
      subsequent: optimalDelay,          // Following keystrokes
      idle: optimalDelay * 2,           // After pause in typing
      burst: optimalDelay * 0.75        // Rapid typing detected
    } : null;

    return {
      optimal: Math.round(optimalDelay),
      adaptive: adaptiveDelays,
      analysis: {
        typingSpeed,
        userType,
        networkSpeed,
        complexity,
        adjustments: {
          network: networkAdjustment,
          complexity: complexityAdjustment
        }
      },
      recommendations: this.getRecommendations(optimalDelay, params)
    };
  }

  /**
   * Generate recommendations based on analysis
   * @param {number} delay - Calculated delay
   * @param {Object} params - Input parameters
   * @returns {string[]} List of recommendations
   */
  getRecommendations(delay, params) {
    const recommendations = [];

    if (delay > 500) {
      recommendations.push('Consider implementing a loading indicator for better UX');
      recommendations.push('Cache recent searches to improve perceived performance');
    }

    if (params.networkLatency > 200) {
      recommendations.push('Implement request cancellation for outdated queries');
      recommendations.push('Consider using a CDN or edge computing for search');
    }

    if (params.deviceType === 'mobile') {
      recommendations.push('Implement touch-friendly autocomplete UI');
      recommendations.push('Consider voice search as an alternative');
    }

    const complexity = this.getSearchComplexity(params.searchParams || {});
    if (complexity === 'heavy') {
      recommendations.push('Consider server-side caching for complex queries');
      recommendations.push('Implement progressive loading for large result sets');
    }

    return recommendations;
  }

  /**
   * Simulate typing patterns for testing
   * @param {string} pattern - Typing pattern (fast, average, slow, burst)
   * @returns {number[]} Array of keystroke delays
   */
  simulateTypingPattern(pattern = 'average') {
    const patterns = {
      fast: () => 80 + Math.random() * 40,    // 80-120ms
      average: () => 150 + Math.random() * 100, // 150-250ms
      slow: () => 300 + Math.random() * 200,    // 300-500ms
      burst: () => {
        // Simulate burst typing with pauses
        return Math.random() < 0.8 ? 60 + Math.random() * 40 : 500 + Math.random() * 500;
      }
    };

    const generator = patterns[pattern] || patterns.average;
    const delays = [];

    // Generate 20 keystrokes
    for (let i = 0; i < 20; i++) {
      delays.push(generator());
    }

    return delays;
  }

  /**
   * Benchmark different debounce delays
   * @param {Object} testParams - Test parameters
   * @returns {Object} Benchmark results
   */
  benchmark(testParams = {}) {
    const delays = [100, 200, 300, 400, 500, 600];
    const results = {};

    delays.forEach(delay => {
      const metrics = this.calculateMetrics(delay, testParams);
      results[delay] = metrics;
    });

    // Find optimal based on score
    let optimal = null;
    let bestScore = -Infinity;

    Object.entries(results).forEach(([delay, metrics]) => {
      if (metrics.score > bestScore) {
        bestScore = metrics.score;
        optimal = parseInt(delay);
      }
    });

    return {
      results,
      optimal,
      analysis: this.analyzeBenchmark(results)
    };
  }

  /**
   * Calculate metrics for a given delay
   * @param {number} delay - Debounce delay to test
   * @param {Object} params - Test parameters
   * @returns {Object} Calculated metrics
   */
  calculateMetrics(delay, params) {
    const {
      avgSessionLength = 30000,  // 30 seconds
      avgQueryLength = 10,        // 10 characters
      typingSpeed = 40,           // WPM
      networkLatency = 100        // ms
    } = params;

    // Calculate requests saved
    const keystrokesPerSession = (avgSessionLength / (60000 / (typingSpeed * 5)));
    const requestsWithoutDebounce = keystrokesPerSession;
    const requestsWithDebounce = Math.ceil(keystrokesPerSession / (delay / 100));
    const requestsSaved = requestsWithoutDebounce - requestsWithDebounce;

    // Calculate perceived latency
    const perceivedLatency = delay + networkLatency;

    // Calculate responsiveness score (lower delay = higher score)
    const responsivenessScore = 1000 / (delay + 50);

    // Calculate efficiency score (more requests saved = higher score)
    const efficiencyScore = requestsSaved / requestsWithoutDebounce * 100;

    // Combined score (weighted)
    const score = (responsivenessScore * 0.6) + (efficiencyScore * 0.4);

    return {
      requestsSaved,
      perceivedLatency,
      responsivenessScore: Math.round(responsivenessScore * 10) / 10,
      efficiencyScore: Math.round(efficiencyScore),
      score: Math.round(score * 10) / 10
    };
  }

  /**
   * Analyze benchmark results
   * @param {Object} results - Benchmark results
   * @returns {Object} Analysis summary
   */
  analyzeBenchmark(results) {
    const delays = Object.keys(results).map(Number);
    const scores = delays.map(d => results[d].score);
    const latencies = delays.map(d => results[d].perceivedLatency);

    return {
      bestScore: Math.max(...scores),
      worstScore: Math.min(...scores),
      avgPerceivedLatency: Math.round(latencies.reduce((a, b) => a + b, 0) / latencies.length),
      recommendation: this.getBenchmarkRecommendation(results)
    };
  }

  /**
   * Get recommendation from benchmark
   * @param {Object} results - Benchmark results
   * @returns {string} Recommendation text
   */
  getBenchmarkRecommendation(results) {
    const optimal = Object.entries(results)
      .sort(([, a], [, b]) => b.score - a.score)[0];

    const [delay, metrics] = optimal;

    if (metrics.perceivedLatency < 300) {
      return `Use ${delay}ms for optimal balance of performance and UX`;
    } else if (metrics.efficiencyScore > 80) {
      return `Use ${delay}ms to minimize server load despite higher latency`;
    } else {
      return `Consider adaptive debouncing starting at ${delay}ms`;
    }
  }
}

// Command-line interface
if (require.main === module) {
  const calculator = new DebounceCalculator();

  // Parse command line arguments
  const args = process.argv.slice(2);
  const mode = args[0] || 'calculate';

  if (mode === 'calculate') {
    // Example calculation
    const params = {
      keystrokeDelays: calculator.simulateTypingPattern('average'),
      networkLatency: 100,
      searchParams: {
        query: 'laptop',
        filters: {
          category: ['Electronics'],
          priceRange: [500, 1500]
        },
        includeFacets: true
      },
      deviceType: 'desktop',
      adaptiveMode: true
    };

    const result = calculator.calculateOptimalDebounce(params);

    console.log('Debounce Calculation Results:');
    console.log('============================');
    console.log(`Optimal Delay: ${result.optimal}ms`);
    console.log('\nAdaptive Delays:');
    if (result.adaptive) {
      Object.entries(result.adaptive).forEach(([key, value]) => {
        console.log(`  ${key}: ${Math.round(value)}ms`);
      });
    }
    console.log('\nAnalysis:');
    Object.entries(result.analysis).forEach(([key, value]) => {
      if (typeof value === 'object') {
        console.log(`  ${key}:`);
        Object.entries(value).forEach(([k, v]) => {
          console.log(`    ${k}: ${v}`);
        });
      } else {
        console.log(`  ${key}: ${value}`);
      }
    });
    console.log('\nRecommendations:');
    result.recommendations.forEach(rec => {
      console.log(`  • ${rec}`);
    });

  } else if (mode === 'benchmark') {
    // Run benchmark
    const testParams = {
      avgSessionLength: 30000,
      avgQueryLength: 10,
      typingSpeed: 40,
      networkLatency: 100
    };

    const benchmark = calculator.benchmark(testParams);

    console.log('Debounce Benchmark Results:');
    console.log('==========================');
    console.log(`Optimal Delay: ${benchmark.optimal}ms\n`);

    console.log('Delay Comparison:');
    Object.entries(benchmark.results).forEach(([delay, metrics]) => {
      console.log(`${delay}ms:`);
      console.log(`  Score: ${metrics.score}`);
      console.log(`  Requests Saved: ${metrics.requestsSaved}`);
      console.log(`  Perceived Latency: ${metrics.perceivedLatency}ms`);
      console.log(`  Responsiveness: ${metrics.responsivenessScore}`);
      console.log(`  Efficiency: ${metrics.efficiencyScore}%\n`);
    });

    console.log('Analysis:');
    console.log(`  Best Score: ${benchmark.analysis.bestScore}`);
    console.log(`  Worst Score: ${benchmark.analysis.worstScore}`);
    console.log(`  Avg Perceived Latency: ${benchmark.analysis.avgPerceivedLatency}ms`);
    console.log(`  Recommendation: ${benchmark.analysis.recommendation}`);

  } else {
    console.log('Usage: node debounce_calculator.js [calculate|benchmark]');
  }
}

module.exports = DebounceCalculator;