#!/usr/bin/env node

/**
 * Timing Calculation Utilities for Feedback Components
 *
 * Calculates auto-dismiss timings for notifications based on
 * content length, urgency, and user preferences.
 *
 * Usage: node calculate_timing.js [options]
 *
 * Options:
 *   --message <text>     Message content to analyze
 *   --type <type>        Message type (success, error, warning, info)
 *   --has-action         Whether message has action button
 *   --word-count <n>     Override word count
 *   --complexity <n>     Content complexity (1-10)
 */

// Parse command line arguments
const args = process.argv.slice(2);
const options = {};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--has-action') {
    options['hasAction'] = true;
  } else if (args[i].startsWith('--')) {
    const key = args[i].replace('--', '').replace(/-/g, '');
    const value = args[i + 1];
    options[key] = value;
    i++;
  }
}

// Base timing configurations by type
const BASE_TIMINGS = {
  success: 3000,  // 3 seconds
  info: 4000,     // 4 seconds
  warning: 5000,  // 5 seconds
  error: 7000     // 7 seconds
};

// Reading speed constants
const READING_SPEED = {
  fast: 250,      // 250 words per minute
  average: 200,   // 200 words per minute (default)
  slow: 150       // 150 words per minute
};

/**
 * Calculate auto-dismiss duration for a notification
 *
 * @param {string} message - The message content
 * @param {string} type - Message type (success, error, etc.)
 * @param {Object} config - Additional configuration
 * @returns {number} Duration in milliseconds
 */
function calculateDuration(message, type = 'info', config = {}) {
  // Never auto-dismiss if action is present
  if (config.hasAction) {
    return Infinity;
  }

  // Get base duration for type
  const baseDuration = BASE_TIMINGS[type] || 4000;

  // Calculate reading time
  const readingTime = calculateReadingTime(message, config.readingSpeed);

  // Factor in complexity
  const complexityMultiplier = getComplexityMultiplier(config.complexity || analyzeComplexity(message));

  // Calculate final duration
  let duration = Math.max(baseDuration, readingTime * complexityMultiplier);

  // Apply min/max constraints
  duration = Math.max(duration, config.minDuration || 2000);  // Minimum 2 seconds
  duration = Math.min(duration, config.maxDuration || 10000); // Maximum 10 seconds

  return Math.round(duration);
}

/**
 * Calculate reading time for a message
 *
 * @param {string} message - The message to read
 * @param {string} speed - Reading speed (fast, average, slow)
 * @returns {number} Reading time in milliseconds
 */
function calculateReadingTime(message, speed = 'average') {
  const wordCount = message.trim().split(/\s+/).length;
  const wordsPerMinute = READING_SPEED[speed] || READING_SPEED.average;
  const wordsPerSecond = wordsPerMinute / 60;
  const readingTimeSeconds = wordCount / wordsPerSecond;

  return readingTimeSeconds * 1000; // Convert to milliseconds
}

/**
 * Analyze message complexity
 *
 * @param {string} message - The message to analyze
 * @returns {number} Complexity score (1-10)
 */
function analyzeComplexity(message) {
  let complexity = 5; // Base complexity

  // Check for numbers (harder to read quickly)
  const numberCount = (message.match(/\d+/g) || []).length;
  if (numberCount > 2) complexity += 1;
  if (numberCount > 5) complexity += 1;

  // Check for technical terms (common in errors)
  const technicalTerms = [
    'API', 'HTTP', 'SQL', 'JSON', 'XML', 'URL', 'UUID',
    'authentication', 'authorization', 'validation',
    'configuration', 'synchronization', 'initialization'
  ];
  const techTermCount = technicalTerms.filter(term =>
    message.toLowerCase().includes(term.toLowerCase())
  ).length;
  if (techTermCount > 0) complexity += 1;
  if (techTermCount > 2) complexity += 1;

  // Check for special characters
  const specialChars = (message.match(/[!@#$%^&*()_+=\[\]{};':"\\|,.<>\/?]/g) || []).length;
  if (specialChars > 5) complexity += 1;

  // Check sentence length
  const avgWordPerSentence = message.split(/[.!?]/).reduce((acc, sentence) => {
    return acc + sentence.trim().split(/\s+/).length;
  }, 0) / Math.max(1, message.split(/[.!?]/).length);

  if (avgWordPerSentence > 15) complexity += 1;
  if (avgWordPerSentence > 20) complexity += 1;

  return Math.min(10, Math.max(1, complexity));
}

/**
 * Get complexity multiplier for duration calculation
 *
 * @param {number} complexity - Complexity score (1-10)
 * @returns {number} Multiplier for duration
 */
function getComplexityMultiplier(complexity) {
  // Linear scale from 1.0 to 1.5 based on complexity
  return 1.0 + (complexity - 1) * 0.055;
}

/**
 * Calculate timing for multiple notifications (queue/stack)
 *
 * @param {Array} notifications - Array of notification objects
 * @param {string} strategy - Stacking strategy (queue, stack, replace)
 * @returns {Array} Notifications with calculated timings
 */
function calculateBatchTimings(notifications, strategy = 'stack') {
  const timings = [];

  notifications.forEach((notification, index) => {
    const baseDuration = calculateDuration(
      notification.message,
      notification.type,
      notification.config || {}
    );

    let adjustedDuration = baseDuration;
    let delay = 0;

    switch (strategy) {
      case 'queue':
        // Each notification waits for previous to complete
        delay = timings.reduce((sum, t) => sum + t.duration, 0);
        break;

      case 'stack':
        // Increase duration for each additional notification
        adjustedDuration = baseDuration + (index * 500);
        delay = index * 100; // Small stagger
        break;

      case 'replace':
        // New notification replaces old immediately
        delay = 0;
        adjustedDuration = baseDuration;
        break;
    }

    timings.push({
      id: notification.id || index,
      duration: adjustedDuration,
      delay: delay,
      startTime: delay,
      endTime: delay + adjustedDuration
    });
  });

  return timings;
}

/**
 * Calculate optimal display time for progress indicators
 *
 * @param {number} expectedDuration - Expected operation duration in ms
 * @returns {Object} Progress indicator configuration
 */
function calculateProgressTiming(expectedDuration) {
  const config = {
    showIndicator: true,
    type: 'none',
    showPercentage: false,
    showTimeEstimate: false,
    updateInterval: 100
  };

  if (expectedDuration < 100) {
    // No indicator for very fast operations
    config.showIndicator = false;
  } else if (expectedDuration < 1000) {
    // Small spinner for quick operations
    config.type = 'spinner-small';
    config.updateInterval = null;
  } else if (expectedDuration < 5000) {
    // Spinner with message for moderate operations
    config.type = 'spinner-with-message';
    config.updateInterval = 500;
  } else if (expectedDuration < 30000) {
    // Progress bar for longer operations
    config.type = 'progress-bar';
    config.showPercentage = true;
    config.updateInterval = 250;
  } else {
    // Full progress with time estimate for very long operations
    config.type = 'progress-bar-advanced';
    config.showPercentage = true;
    config.showTimeEstimate = true;
    config.updateInterval = 1000;
  }

  return config;
}

/**
 * Calculate animation durations
 *
 * @param {string} animationType - Type of animation
 * @param {boolean} reducedMotion - Whether reduced motion is preferred
 * @returns {Object} Animation timing configuration
 */
function calculateAnimationTiming(animationType, reducedMotion = false) {
  if (reducedMotion) {
    return {
      enter: 0,
      exit: 0,
      update: 0
    };
  }

  const timings = {
    toast: {
      enter: 300,
      exit: 200,
      update: 150
    },
    modal: {
      enter: 200,
      exit: 150,
      update: 0
    },
    alert: {
      enter: 300,
      exit: 200,
      update: 150
    },
    progress: {
      enter: 150,
      exit: 150,
      update: 100
    }
  };

  return timings[animationType] || timings.toast;
}

/**
 * Generate timing configuration for React component
 */
function generateTimingConfig() {
  const message = options.message || 'This is a sample notification message.';
  const type = options.type || 'info';
  const hasAction = options.hasaction || false;

  const duration = calculateDuration(message, type, {
    hasAction: hasAction,
    complexity: options.complexity ? parseInt(options.complexity) : undefined
  });

  const config = {
    duration: duration,
    type: type,
    message: message,
    hasAction: hasAction,
    readingTime: calculateReadingTime(message),
    complexity: analyzeComplexity(message),
    animation: calculateAnimationTiming('toast'),
    humanReadable: formatDuration(duration)
  };

  return config;
}

/**
 * Format duration in human-readable format
 *
 * @param {number} ms - Duration in milliseconds
 * @returns {string} Human-readable duration
 */
function formatDuration(ms) {
  if (ms === Infinity) {
    return 'No auto-dismiss';
  }
  if (ms < 1000) {
    return `${ms}ms`;
  }
  return `${(ms / 1000).toFixed(1)}s`;
}

// Main execution
if (require.main === module) {
  const config = generateTimingConfig();

  console.log('Timing Configuration');
  console.log('===================\n');

  console.log('Input:');
  console.log(`  Message: "${config.message}"`);
  console.log(`  Type: ${config.type}`);
  console.log(`  Has Action: ${config.hasAction}`);
  console.log();

  console.log('Analysis:');
  console.log(`  Word Count: ${config.message.split(/\s+/).length}`);
  console.log(`  Complexity Score: ${config.complexity}/10`);
  console.log(`  Reading Time: ${formatDuration(config.readingTime)}`);
  console.log();

  console.log('Timing:');
  console.log(`  Auto-dismiss: ${config.humanReadable}`);
  console.log(`  Enter Animation: ${config.animation.enter}ms`);
  console.log(`  Exit Animation: ${config.animation.exit}ms`);
  console.log();

  console.log('Configuration Object:');
  console.log(JSON.stringify(config, null, 2));
}

// Export for use in other scripts
module.exports = {
  calculateDuration,
  calculateReadingTime,
  analyzeComplexity,
  calculateBatchTimings,
  calculateProgressTiming,
  calculateAnimationTiming,
  BASE_TIMINGS
};