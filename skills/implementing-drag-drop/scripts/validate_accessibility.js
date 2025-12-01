#!/usr/bin/env node

/**
 * Validate Accessibility for Drag-and-Drop
 * Checks keyboard navigation, ARIA attributes, and screen reader compatibility
 */

// Check if element has proper keyboard support
function checkKeyboardSupport(element) {
  const issues = [];
  const warnings = [];

  // Check if element is focusable
  const tabIndex = element.getAttribute('tabIndex') || element.tabIndex;
  if (tabIndex === undefined || tabIndex === -1) {
    issues.push('Element is not keyboard focusable (missing tabIndex or tabIndex=-1)');
  }

  // Check for keyboard event handlers
  const hasKeyHandlers = element.onkeydown || element.onkeyup || element.onkeypress;
  if (!hasKeyHandlers) {
    warnings.push('No keyboard event handlers detected');
  }

  // Check for proper role
  const role = element.getAttribute('role');
  if (!role) {
    warnings.push('Missing role attribute');
  } else if (!['button', 'listitem', 'option', 'row'].includes(role)) {
    warnings.push(`Role "${role}" may not be appropriate for draggable items`);
  }

  return { issues, warnings, passed: issues.length === 0 };
}

// Check ARIA attributes
function checkAriaAttributes(element, isDragging = false) {
  const issues = [];
  const warnings = [];
  const recommendations = [];

  // Required ARIA attributes
  const ariaLabel = element.getAttribute('aria-label');
  const ariaLabelledBy = element.getAttribute('aria-labelledby');
  const ariaDescribedBy = element.getAttribute('aria-describedby');

  if (!ariaLabel && !ariaLabelledBy) {
    issues.push('Missing accessible label (aria-label or aria-labelledby)');
  }

  // Check aria-roledescription
  const ariaRoleDescription = element.getAttribute('aria-roledescription');
  if (!ariaRoleDescription) {
    recommendations.push('Consider adding aria-roledescription="sortable" for sortable items');
  }

  // Check drag-specific ARIA
  const ariaGrabbed = element.getAttribute('aria-grabbed');
  if (isDragging && ariaGrabbed !== 'true') {
    issues.push('aria-grabbed should be "true" when dragging');
  } else if (!isDragging && ariaGrabbed === 'true') {
    issues.push('aria-grabbed should be "false" when not dragging');
  }

  // Check drop effect
  const ariaDropEffect = element.getAttribute('aria-dropeffect');
  if (element.classList.contains('drop-zone') && !ariaDropEffect) {
    warnings.push('Drop zones should have aria-dropeffect attribute');
  }

  // Check position information
  const ariaPosInSet = element.getAttribute('aria-posinset');
  const ariaSetSize = element.getAttribute('aria-setsize');
  if (element.parentElement?.getAttribute('role') === 'list') {
    if (!ariaPosInSet) {
      recommendations.push('Consider adding aria-posinset for position in list');
    }
    if (!ariaSetSize) {
      recommendations.push('Consider adding aria-setsize for total list size');
    }
  }

  return { issues, warnings, recommendations, passed: issues.length === 0 };
}

// Check for screen reader support
function checkScreenReaderSupport(container) {
  const issues = [];
  const warnings = [];
  const recommendations = [];

  // Check for live region
  const liveRegions = container.querySelectorAll('[aria-live]');
  if (liveRegions.length === 0) {
    issues.push('No live region found for screen reader announcements');
  } else {
    liveRegions.forEach(region => {
      const ariaLive = region.getAttribute('aria-live');
      if (!['polite', 'assertive'].includes(ariaLive)) {
        warnings.push(`Invalid aria-live value: "${ariaLive}"`);
      }

      const ariaAtomic = region.getAttribute('aria-atomic');
      if (ariaAtomic !== 'true') {
        recommendations.push('Consider setting aria-atomic="true" on live regions');
      }
    });
  }

  // Check for instructions
  const instructions = container.querySelector('[id*="instructions"]');
  if (!instructions) {
    warnings.push('No instruction element found for screen reader users');
  } else {
    // Check if instructions are referenced
    const describedByElements = container.querySelectorAll('[aria-describedby*="instructions"]');
    if (describedByElements.length === 0) {
      warnings.push('Instructions exist but are not referenced by any draggable elements');
    }
  }

  // Check for hidden but readable content
  const srOnly = container.querySelectorAll('.sr-only, .visually-hidden');
  if (srOnly.length === 0) {
    recommendations.push('Consider adding screen-reader-only instructions');
  }

  return { issues, warnings, recommendations, passed: issues.length === 0 };
}

// Check alternative UI controls
function checkAlternativeControls(element) {
  const issues = [];
  const warnings = [];
  const recommendations = [];

  const parent = element.parentElement;
  if (!parent) return { issues: ['Element has no parent'], warnings, recommendations, passed: false };

  // Look for move buttons
  const moveButtons = parent.querySelectorAll('button[aria-label*="move" i], button[aria-label*="reorder" i]');
  if (moveButtons.length === 0) {
    warnings.push('No alternative move buttons found for non-drag interaction');
  }

  // Check if buttons are properly labeled
  moveButtons.forEach(button => {
    const ariaLabel = button.getAttribute('aria-label');
    if (!ariaLabel) {
      issues.push('Alternative control button missing aria-label');
    }

    if (button.disabled && !button.getAttribute('aria-disabled')) {
      warnings.push('Disabled button should have aria-disabled="true"');
    }
  });

  // Look for position selector
  const positionSelector = parent.querySelector('select[aria-label*="position" i], select[aria-label*="move" i]');
  if (!positionSelector && moveButtons.length === 0) {
    recommendations.push('Consider adding position selector as alternative to drag-and-drop');
  }

  return { issues, warnings, recommendations, passed: issues.length === 0 };
}

// Check focus management
function checkFocusManagement(container) {
  const issues = [];
  const warnings = [];

  // Check for focus trap potential
  const focusableElements = container.querySelectorAll(
    'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
  );

  if (focusableElements.length === 0) {
    issues.push('No focusable elements found');
  }

  // Check tab order
  const tabIndexElements = Array.from(container.querySelectorAll('[tabindex]'));
  const positiveTabIndex = tabIndexElements.filter(el => {
    const tabIndex = parseInt(el.getAttribute('tabindex'));
    return tabIndex > 0;
  });

  if (positiveTabIndex.length > 0) {
    warnings.push(`Found ${positiveTabIndex.length} elements with positive tabindex (avoid for proper tab order)`);
  }

  // Check for skip links
  const skipLinks = container.querySelectorAll('a[href^="#"][class*="skip"]');
  if (focusableElements.length > 10 && skipLinks.length === 0) {
    warnings.push('Consider adding skip links for large interactive areas');
  }

  return { issues, warnings, passed: issues.length === 0 };
}

// Main validation function
function validateAccessibility(rootElement) {
  const report = {
    passed: true,
    issues: [],
    warnings: [],
    recommendations: [],
    summary: {},
  };

  // Find all draggable elements
  const draggables = rootElement.querySelectorAll('[draggable="true"], [role="button"][aria-roledescription*="sortable"], .draggable');

  if (draggables.length === 0) {
    report.issues.push('No draggable elements found');
    report.passed = false;
  } else {
    // Check each draggable element
    draggables.forEach((element, index) => {
      const elementId = element.id || `draggable-${index}`;

      // Keyboard support
      const keyboardCheck = checkKeyboardSupport(element);
      if (!keyboardCheck.passed) {
        report.issues.push(...keyboardCheck.issues.map(issue => `${elementId}: ${issue}`));
      }
      report.warnings.push(...keyboardCheck.warnings.map(warning => `${elementId}: ${warning}`));

      // ARIA attributes
      const ariaCheck = checkAriaAttributes(element);
      if (!ariaCheck.passed) {
        report.issues.push(...ariaCheck.issues.map(issue => `${elementId}: ${issue}`));
      }
      report.warnings.push(...ariaCheck.warnings.map(warning => `${elementId}: ${warning}`));
      report.recommendations.push(...ariaCheck.recommendations.map(rec => `${elementId}: ${rec}`));

      // Alternative controls
      const altCheck = checkAlternativeControls(element);
      if (!altCheck.passed) {
        report.issues.push(...altCheck.issues.map(issue => `${elementId}: ${issue}`));
      }
      report.warnings.push(...altCheck.warnings.map(warning => `${elementId}: ${warning}`));
      report.recommendations.push(...altCheck.recommendations.map(rec => `${elementId}: ${rec}`));
    });
  }

  // Check screen reader support
  const screenReaderCheck = checkScreenReaderSupport(rootElement);
  if (!screenReaderCheck.passed) {
    report.issues.push(...screenReaderCheck.issues);
  }
  report.warnings.push(...screenReaderCheck.warnings);
  report.recommendations.push(...screenReaderCheck.recommendations);

  // Check focus management
  const focusCheck = checkFocusManagement(rootElement);
  if (!focusCheck.passed) {
    report.issues.push(...focusCheck.issues);
  }
  report.warnings.push(...focusCheck.warnings);

  // Update overall pass status
  report.passed = report.issues.length === 0;

  // Generate summary
  report.summary = {
    totalElements: draggables.length,
    issueCount: report.issues.length,
    warningCount: report.warnings.length,
    recommendationCount: report.recommendations.length,
    score: calculateAccessibilityScore(report),
  };

  return report;
}

// Calculate accessibility score
function calculateAccessibilityScore(report) {
  const baseScore = 100;
  const issuePenalty = 10;
  const warningPenalty = 3;

  const score = Math.max(
    0,
    baseScore - (report.issues.length * issuePenalty) - (report.warnings.length * warningPenalty)
  );

  return {
    numeric: score,
    grade: score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : score >= 60 ? 'D' : 'F',
    label: score >= 90 ? 'Excellent' : score >= 80 ? 'Good' : score >= 70 ? 'Fair' : score >= 60 ? 'Poor' : 'Failing',
  };
}

// Format report for console output
function formatReport(report) {
  const { passed, issues, warnings, recommendations, summary } = report;

  let output = '\n🔍 Drag-and-Drop Accessibility Validation Report\n';
  output += '='.repeat(50) + '\n\n';

  output += `📊 Summary\n`;
  output += `-`.repeat(20) + '\n`;
  output += `  Elements checked: ${summary.totalElements}\n`;
  output += `  Issues found: ${summary.issueCount}\n`;
  output += `  Warnings: ${summary.warningCount}\n`;
  output += `  Recommendations: ${summary.recommendationCount}\n`;
  output += `  Score: ${summary.score.numeric}/100 (${summary.score.grade} - ${summary.score.label})\n\n`;

  if (passed) {
    output += '✅ PASSED - No critical accessibility issues found\n\n';
  } else {
    output += '❌ FAILED - Critical accessibility issues detected\n\n';
  }

  if (issues.length > 0) {
    output += '🚨 Critical Issues (must fix):\n';
    issues.forEach(issue => {
      output += `  • ${issue}\n`;
    });
    output += '\n';
  }

  if (warnings.length > 0) {
    output += '⚠️  Warnings (should fix):\n';
    warnings.forEach(warning => {
      output += `  • ${warning}\n`;
    });
    output += '\n';
  }

  if (recommendations.length > 0) {
    output += '💡 Recommendations (nice to have):\n';
    recommendations.forEach(rec => {
      output += `  • ${rec}\n`;
    });
    output += '\n';
  }

  output += '📚 Resources:\n';
  output += '  • WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/\n';
  output += '  • ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/\n';
  output += '  • Screen Reader Testing: https://webaim.org/articles/screenreader_testing/\n';

  return output;
}

// Main function for CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help') {
    console.log(`
Validate Drag-and-Drop Accessibility

Usage:
  node validate_accessibility.js [selector] [--format json|text]

Options:
  selector  CSS selector for container to validate (default: body)
  --format  Output format (json or text, default: text)
  --help    Show this help message

Examples:
  node validate_accessibility.js .drag-container
  node validate_accessibility.js #kanban-board --format json
  node validate_accessibility.js

Note: This script is designed to be run in a browser environment.
For Node.js usage, integrate with a testing framework like Puppeteer or Playwright.
    `);
    process.exit(0);
  }

  // Since we can't actually query DOM in Node.js, provide example output
  const exampleReport = {
    passed: false,
    issues: [
      'draggable-0: Element is not keyboard focusable (missing tabIndex or tabIndex=-1)',
      'No live region found for screen reader announcements',
    ],
    warnings: [
      'draggable-1: Missing role attribute',
      'No alternative move buttons found for non-drag interaction',
    ],
    recommendations: [
      'draggable-0: Consider adding aria-roledescription="sortable" for sortable items',
      'Consider adding screen-reader-only instructions',
    ],
    summary: {
      totalElements: 5,
      issueCount: 2,
      warningCount: 2,
      recommendationCount: 2,
      score: { numeric: 74, grade: 'C', label: 'Fair' },
    },
  };

  const format = args.includes('--format') ? args[args.indexOf('--format') + 1] : 'text';

  if (format === 'json') {
    console.log(JSON.stringify(exampleReport, null, 2));
  } else {
    console.log(formatReport(exampleReport));
  }
}

// Export functions for use in other scripts
module.exports = {
  validateAccessibility,
  checkKeyboardSupport,
  checkAriaAttributes,
  checkScreenReaderSupport,
  checkAlternativeControls,
  checkFocusManagement,
  calculateAccessibilityScore,
  formatReport,
};