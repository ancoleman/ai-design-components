#!/usr/bin/env node

/**
 * Validate Layout Accessibility
 * Checks semantic HTML structure, ARIA landmarks, and accessibility best practices
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
const filePath = args[0];
const options = {};

args.forEach((arg, index) => {
  if (arg.startsWith('--')) {
    const key = arg.slice(2);
    const value = args[index + 1];
    options[key] = value && !value.startsWith('--') ? value : true;
  }
});

// Validation rules
const rules = {
  landmarks: {
    required: ['header', 'main', 'footer'],
    recommended: ['nav', 'aside'],
    aria: {
      'header': 'banner',
      'nav': 'navigation',
      'main': 'main',
      'aside': 'complementary',
      'footer': 'contentinfo'
    }
  },
  skipLinks: {
    required: ['#main', '#nav'],
    pattern: /href="#(main|nav|content|navigation)"/gi
  },
  headings: {
    hierarchy: true,
    singleH1: true,
    noSkip: true
  },
  focusManagement: {
    tabindex: {
      valid: ['-1', '0'],
      warn: ['1', '2', '3', '4', '5']
    },
    focusVisible: true
  },
  aria: {
    required: {
      'button': ['aria-label', 'aria-labelledby', 'text-content'],
      'nav': ['aria-label', 'aria-labelledby'],
      'region': ['aria-label', 'aria-labelledby'],
      'img': ['alt']
    },
    states: ['aria-expanded', 'aria-hidden', 'aria-current', 'aria-selected', 'aria-checked'],
    live: ['aria-live', 'role="alert"', 'role="status"']
  },
  touchTargets: {
    minSize: 44, // 44x44px minimum
    checkSelectors: ['button', 'a', 'input', 'select', '[role="button"]']
  }
};

// Validation results
const results = {
  errors: [],
  warnings: [],
  info: [],
  passes: []
};

/**
 * Read and parse file content
 */
function readFile(filepath) {
  if (!filepath) {
    console.error('Error: Please provide a file path to validate');
    console.log('Usage: node validate_layout_accessibility.js <filepath> [options]');
    process.exit(1);
  }

  try {
    const content = fs.readFileSync(filepath, 'utf8');
    return content;
  } catch (error) {
    console.error(`Error reading file: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Check for semantic landmarks
 */
function checkLandmarks(content) {
  // Check required landmarks
  rules.landmarks.required.forEach(landmark => {
    const regex = new RegExp(`<${landmark}[\\s>]`, 'i');
    const ariaRole = rules.landmarks.aria[landmark];
    const ariaRegex = new RegExp(`role="${ariaRole}"`, 'i');

    if (!regex.test(content) && !ariaRegex.test(content)) {
      results.errors.push(`Missing required landmark: <${landmark}> or role="${ariaRole}"`);
    } else {
      results.passes.push(`✓ Found ${landmark} landmark`);
    }
  });

  // Check recommended landmarks
  rules.landmarks.recommended.forEach(landmark => {
    const regex = new RegExp(`<${landmark}[\\s>]`, 'i');
    const ariaRole = rules.landmarks.aria[landmark];
    const ariaRegex = new RegExp(`role="${ariaRole}"`, 'i');

    if (!regex.test(content) && !ariaRegex.test(content)) {
      results.warnings.push(`Consider adding: <${landmark}> or role="${ariaRole}"`);
    } else {
      results.passes.push(`✓ Found ${landmark} landmark`);
    }
  });

  // Check for multiple main elements
  const mainCount = (content.match(/<main[\s>]/gi) || []).length;
  if (mainCount > 1) {
    results.errors.push(`Multiple <main> elements found (${mainCount}). Only one allowed per page.`);
  }
}

/**
 * Check for skip links
 */
function checkSkipLinks(content) {
  const skipLinkFound = rules.skipLinks.pattern.test(content);

  if (!skipLinkFound) {
    results.errors.push('No skip links found. Add skip links for keyboard navigation.');
  } else {
    // Check for specific skip link targets
    rules.skipLinks.required.forEach(target => {
      const regex = new RegExp(`href="${target}"`, 'i');
      if (!regex.test(content)) {
        results.warnings.push(`Consider adding skip link to ${target}`);
      } else {
        results.passes.push(`✓ Found skip link to ${target}`);
      }
    });
  }

  // Check if skip links are properly hidden
  if (content.includes('skip-link') || content.includes('skiplink')) {
    if (!content.includes('position: absolute') && !content.includes('sr-only')) {
      results.warnings.push('Skip links should be visually hidden but accessible to screen readers');
    }
  }
}

/**
 * Check heading hierarchy
 */
function checkHeadings(content) {
  const headingMatches = content.match(/<h[1-6][^>]*>.*?<\/h[1-6]>/gi) || [];
  const headingLevels = [];

  headingMatches.forEach(match => {
    const level = parseInt(match.match(/<h([1-6])/i)[1]);
    headingLevels.push(level);
  });

  // Check for single H1
  const h1Count = headingLevels.filter(level => level === 1).length;
  if (h1Count === 0) {
    results.errors.push('No <h1> found. Each page should have exactly one <h1>.');
  } else if (h1Count > 1) {
    results.warnings.push(`Multiple <h1> elements found (${h1Count}). Consider using only one per page.`);
  } else {
    results.passes.push('✓ Single <h1> found');
  }

  // Check heading hierarchy
  let previousLevel = 0;
  let skippedLevel = false;

  headingLevels.forEach((level, index) => {
    if (previousLevel > 0 && level > previousLevel + 1) {
      skippedLevel = true;
      results.errors.push(`Heading hierarchy broken at heading ${index + 1}: h${previousLevel} → h${level}`);
    }
    previousLevel = level;
  });

  if (!skippedLevel && headingLevels.length > 0) {
    results.passes.push('✓ Heading hierarchy is correct');
  }
}

/**
 * Check ARIA attributes
 */
function checkARIA(content) {
  // Check for aria-label or aria-labelledby on interactive elements
  const interactiveElements = ['button', 'a', 'input', 'select', 'textarea'];

  interactiveElements.forEach(element => {
    const regex = new RegExp(`<${element}[^>]*>`, 'gi');
    const matches = content.match(regex) || [];

    matches.forEach(match => {
      const hasAriaLabel = /aria-label(ledby)?=/i.test(match);
      const hasTextContent = /<button[^>]*>[^<]+<\/button>/i.test(match + '</button>');

      if (!hasAriaLabel && !hasTextContent && element === 'button') {
        results.warnings.push(`Button without accessible label found. Add aria-label or text content.`);
      }
    });
  });

  // Check for aria-hidden on focusable elements
  if (/aria-hidden="true"[^>]*tabindex="0"/i.test(content)) {
    results.errors.push('Found focusable element with aria-hidden="true". This creates accessibility issues.');
  }

  // Check for aria-live regions
  const hasLiveRegion = rules.aria.live.some(attr => content.includes(attr));
  if (hasLiveRegion) {
    results.passes.push('✓ Live regions found for dynamic content');
  } else {
    results.info.push('No live regions found. Consider adding for dynamic content updates.');
  }

  // Check for proper aria-expanded usage
  if (content.includes('aria-expanded')) {
    const expandedMatches = content.match(/aria-expanded="(true|false)"/gi) || [];
    if (expandedMatches.length > 0) {
      results.passes.push('✓ Proper aria-expanded usage found');
    }
  }
}

/**
 * Check focus management
 */
function checkFocusManagement(content) {
  // Check for tabindex usage
  const tabindexMatches = content.match(/tabindex="(-?\d+)"/gi) || [];

  tabindexMatches.forEach(match => {
    const value = match.match(/tabindex="(-?\d+)"/i)[1];

    if (!rules.focusManagement.tabindex.valid.includes(value)) {
      if (parseInt(value) > 0) {
        results.warnings.push(`Avoid tabindex="${value}". Use 0 for focusable or -1 for programmatic focus only.`);
      }
    }
  });

  // Check for focus styles
  const hasFocusStyles = /:focus|focus-visible|focus-within/i.test(content);
  if (!hasFocusStyles) {
    results.warnings.push('No focus styles detected. Ensure visible focus indicators are provided.');
  } else {
    results.passes.push('✓ Focus styles detected');
  }

  // Check for outline removal
  if (/outline:\s*(none|0)/i.test(content) && !/:focus-visible/i.test(content)) {
    results.warnings.push('Outline removed without alternative focus indicator. Provide visible focus styles.');
  }
}

/**
 * Check responsive considerations
 */
function checkResponsive(content) {
  // Check for viewport meta tag
  if (!/<meta[^>]*viewport/i.test(content)) {
    results.errors.push('Missing viewport meta tag. Add <meta name="viewport" content="width=device-width, initial-scale=1">');
  } else {
    results.passes.push('✓ Viewport meta tag found');
  }

  // Check for touch target sizes (basic check)
  if (options.strict) {
    const smallTargets = /(?:padding|height|width):\s*(\d+)px/gi;
    const matches = content.match(smallTargets) || [];

    matches.forEach(match => {
      const size = parseInt(match.match(/(\d+)px/)[1]);
      if (size < 44) {
        results.info.push(`Potential small touch target found (${size}px). Minimum recommended: 44px`);
      }
    });
  }
}

/**
 * Check semantic HTML usage
 */
function checkSemanticHTML(content) {
  // Check for div soup
  const divCount = (content.match(/<div/gi) || []).length;
  const semanticTags = ['article', 'section', 'nav', 'aside', 'header', 'footer', 'main'];
  const semanticCount = semanticTags.reduce((count, tag) => {
    return count + (content.match(new RegExp(`<${tag}`, 'gi')) || []).length;
  }, 0);

  if (divCount > semanticCount * 3) {
    results.warnings.push(`High div to semantic element ratio (${divCount} divs, ${semanticCount} semantic). Consider using more semantic HTML.`);
  }

  // Check for list usage
  if (/<li[^>]*>/.test(content) && !/<[uo]l[^>]*>/.test(content)) {
    results.errors.push('List items (<li>) found without parent <ul> or <ol>');
  }

  // Check for form labels
  const inputCount = (content.match(/<input/gi) || []).length;
  const labelCount = (content.match(/<label/gi) || []).length;

  if (inputCount > 0 && labelCount < inputCount) {
    results.warnings.push(`Possible missing labels. Found ${inputCount} inputs but only ${labelCount} labels.`);
  }
}

/**
 * Display results
 */
function displayResults() {
  console.log('\n=== Accessibility Validation Results ===\n');

  if (results.errors.length > 0) {
    console.log('❌ ERRORS (Must fix):');
    results.errors.forEach(error => console.log(`   • ${error}`));
    console.log('');
  }

  if (results.warnings.length > 0) {
    console.log('⚠️  WARNINGS (Should fix):');
    results.warnings.forEach(warning => console.log(`   • ${warning}`));
    console.log('');
  }

  if (results.info.length > 0) {
    console.log('ℹ️  INFO (Consider):');
    results.info.forEach(info => console.log(`   • ${info}`));
    console.log('');
  }

  if (options.verbose && results.passes.length > 0) {
    console.log('✅ PASSES:');
    results.passes.forEach(pass => console.log(`   ${pass}`));
    console.log('');
  }

  // Summary
  console.log('--- Summary ---');
  console.log(`Errors: ${results.errors.length}`);
  console.log(`Warnings: ${results.warnings.length}`);
  console.log(`Info: ${results.info.length}`);
  console.log(`Passes: ${results.passes.length}`);

  // Exit code
  process.exit(results.errors.length > 0 ? 1 : 0);
}

/**
 * Main validation function
 */
function validate() {
  if (options.help) {
    console.log(`
Layout Accessibility Validator

Validates HTML/JSX files for accessibility best practices in layout components.

Usage:
  node validate_layout_accessibility.js <filepath> [options]

Options:
  --strict       Enable strict checking (touch targets, etc.)
  --verbose      Show passing checks
  --help         Show this help message

Checks performed:
  • Semantic landmark regions (header, main, nav, aside, footer)
  • Skip links for keyboard navigation
  • Heading hierarchy (single h1, no skipped levels)
  • ARIA attributes and roles
  • Focus management (tabindex, focus styles)
  • Responsive considerations (viewport, touch targets)
  • Semantic HTML usage

Examples:
  node validate_layout_accessibility.js component.tsx
  node validate_layout_accessibility.js layout.html --strict --verbose
    `);
    process.exit(0);
  }

  const content = readFile(filePath);

  console.log(`Validating: ${filePath}`);

  // Run all checks
  checkLandmarks(content);
  checkSkipLinks(content);
  checkHeadings(content);
  checkARIA(content);
  checkFocusManagement(content);
  checkResponsive(content);
  checkSemanticHTML(content);

  // Display results
  displayResults();
}

// Run validation
validate();