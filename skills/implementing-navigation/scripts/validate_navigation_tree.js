#!/usr/bin/env node

/**
 * Validate navigation tree structure for accessibility and usability.
 *
 * Usage:
 *   node validate_navigation_tree.js nav-config.json
 *   node validate_navigation_tree.js --strict nav-config.json
 */

const fs = require('fs');
const path = require('path');

// Validation rules
const RULES = {
  maxDepth: 3,
  maxTopLevelItems: 7,
  maxDropdownItems: 10,
  minTouchTargetSize: 44, // pixels
  maxLabelLength: 30,
  requiredFields: ['label', 'href'],
  ariaPatternsRequired: true
};

// Validation results
let errors = [];
let warnings = [];
let info = [];

/**
 * Load navigation configuration
 */
function loadConfig(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error loading config: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Validate navigation item
 */
function validateItem(item, depth = 0, path = '') {
  const currentPath = path ? `${path} > ${item.label || 'unnamed'}` : item.label || 'unnamed';

  // Check required fields
  RULES.requiredFields.forEach(field => {
    if (!item[field] && !item.children) {
      errors.push(`Missing required field '${field}' at: ${currentPath}`);
    }
  });

  // Check label length
  if (item.label && item.label.length > RULES.maxLabelLength) {
    warnings.push(`Label too long (${item.label.length} chars) at: ${currentPath}`);
  }

  // Check depth
  if (depth > RULES.maxDepth) {
    errors.push(`Navigation too deep (depth: ${depth}) at: ${currentPath}`);
  }

  // Check href format
  if (item.href && !isValidHref(item.href)) {
    warnings.push(`Invalid href format at: ${currentPath}`);
  }

  // Check ARIA attributes
  if (RULES.ariaPatternsRequired) {
    validateAriaAttributes(item, currentPath);
  }

  // Check children
  if (item.children && Array.isArray(item.children)) {
    if (depth === 0 && item.children.length > RULES.maxDropdownItems) {
      warnings.push(`Too many dropdown items (${item.children.length}) at: ${currentPath}`);
    }

    item.children.forEach(child => {
      validateItem(child, depth + 1, currentPath);
    });
  }

  // Check icons
  if (item.icon && !item.iconAlt) {
    warnings.push(`Icon without alt text at: ${currentPath}`);
  }

  // Check external links
  if (item.external && !item.target) {
    info.push(`External link without target="_blank" at: ${currentPath}`);
  }
}

/**
 * Validate href format
 */
function isValidHref(href) {
  // Check for valid URL patterns
  const patterns = [
    /^https?:\/\//, // HTTP(S) URLs
    /^\//, // Absolute paths
    /^#/, // Anchors
    /^mailto:/, // Email links
    /^tel:/ // Phone links
  ];

  return patterns.some(pattern => pattern.test(href));
}

/**
 * Validate ARIA attributes
 */
function validateAriaAttributes(item, path) {
  // Check dropdown triggers
  if (item.children && item.children.length > 0) {
    if (!item.ariaHaspopup) {
      warnings.push(`Missing aria-haspopup for dropdown at: ${path}`);
    }
    if (!item.ariaExpanded !== undefined) {
      warnings.push(`Missing aria-expanded for dropdown at: ${path}`);
    }
  }

  // Check current page indicator
  if (item.active && !item.ariaCurrent) {
    warnings.push(`Active item missing aria-current at: ${path}`);
  }

  // Check keyboard navigation attributes
  if (item.role && !['menuitem', 'link', 'button'].includes(item.role)) {
    warnings.push(`Invalid role "${item.role}" at: ${path}`);
  }
}

/**
 * Validate navigation structure
 */
function validateStructure(config) {
  // Check top-level items count
  if (config.items && config.items.length > RULES.maxTopLevelItems) {
    warnings.push(`Too many top-level items (${config.items.length}, recommended: ${RULES.maxTopLevelItems})`);
  }

  // Check for duplicate hrefs
  const hrefs = extractHrefs(config.items);
  const duplicates = findDuplicates(hrefs);
  if (duplicates.length > 0) {
    errors.push(`Duplicate hrefs found: ${duplicates.join(', ')}`);
  }

  // Check for duplicate labels at same level
  checkDuplicateLabels(config.items);

  // Validate each item
  if (config.items) {
    config.items.forEach(item => validateItem(item));
  }
}

/**
 * Extract all hrefs from navigation tree
 */
function extractHrefs(items, hrefs = []) {
  if (!items) return hrefs;

  items.forEach(item => {
    if (item.href) {
      hrefs.push(item.href);
    }
    if (item.children) {
      extractHrefs(item.children, hrefs);
    }
  });

  return hrefs;
}

/**
 * Find duplicate values in array
 */
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();

  arr.forEach(item => {
    if (seen.has(item)) {
      duplicates.add(item);
    }
    seen.add(item);
  });

  return Array.from(duplicates);
}

/**
 * Check for duplicate labels at same level
 */
function checkDuplicateLabels(items, path = 'root') {
  if (!items) return;

  const labels = items.map(item => item.label).filter(Boolean);
  const duplicates = findDuplicates(labels);

  if (duplicates.length > 0) {
    warnings.push(`Duplicate labels at ${path}: ${duplicates.join(', ')}`);
  }

  // Check children recursively
  items.forEach(item => {
    if (item.children) {
      checkDuplicateLabels(item.children, `${path} > ${item.label || 'unnamed'}`);
    }
  });
}

/**
 * Generate accessibility report
 */
function generateAccessibilityReport(config) {
  const report = [];

  // Check skip link
  if (!config.skipLink) {
    report.push('Consider adding a skip navigation link');
  }

  // Check keyboard navigation support
  if (!config.keyboardNavigation) {
    report.push('Ensure keyboard navigation is supported');
  }

  // Check mobile configuration
  if (!config.mobile) {
    report.push('Consider adding mobile navigation configuration');
  }

  // Check focus indicators
  if (!config.focusIndicators) {
    report.push('Ensure visible focus indicators are implemented');
  }

  // Check landmark roles
  if (!config.landmarkRole) {
    report.push('Add appropriate ARIA landmark role (navigation)');
  }

  return report;
}

/**
 * Generate statistics
 */
function generateStats(config) {
  const stats = {
    totalItems: 0,
    maxDepth: 0,
    averageChildrenPerParent: 0,
    externalLinks: 0,
    dropdowns: 0
  };

  function analyzeItems(items, depth = 0) {
    if (!items) return;

    items.forEach(item => {
      stats.totalItems++;
      stats.maxDepth = Math.max(stats.maxDepth, depth);

      if (item.external) stats.externalLinks++;
      if (item.children && item.children.length > 0) {
        stats.dropdowns++;
        analyzeItems(item.children, depth + 1);
      }
    });
  }

  analyzeItems(config.items);

  if (stats.dropdowns > 0) {
    const totalChildren = stats.totalItems - config.items.length;
    stats.averageChildrenPerParent = (totalChildren / stats.dropdowns).toFixed(1);
  }

  return stats;
}

/**
 * Print validation results
 */
function printResults(config, strict = false) {
  const stats = generateStats(config);
  const accessibilityReport = generateAccessibilityReport(config);

  console.log('\n📊 Navigation Structure Statistics:');
  console.log('─'.repeat(40));
  console.log(`Total items: ${stats.totalItems}`);
  console.log(`Maximum depth: ${stats.maxDepth}`);
  console.log(`Dropdown menus: ${stats.dropdowns}`);
  console.log(`External links: ${stats.externalLinks}`);
  if (stats.dropdowns > 0) {
    console.log(`Avg children per dropdown: ${stats.averageChildrenPerParent}`);
  }

  if (errors.length > 0) {
    console.log('\n❌ Errors:');
    console.log('─'.repeat(40));
    errors.forEach(error => console.log(`  • ${error}`));
  }

  if (warnings.length > 0) {
    console.log('\n⚠️  Warnings:');
    console.log('─'.repeat(40));
    warnings.forEach(warning => console.log(`  • ${warning}`));
  }

  if (info.length > 0) {
    console.log('\nℹ️  Information:');
    console.log('─'.repeat(40));
    info.forEach(item => console.log(`  • ${item}`));
  }

  if (accessibilityReport.length > 0) {
    console.log('\n♿ Accessibility Recommendations:');
    console.log('─'.repeat(40));
    accessibilityReport.forEach(item => console.log(`  • ${item}`));
  }

  // Exit code based on validation results
  if (errors.length > 0) {
    console.log('\n❌ Validation failed with errors');
    process.exit(1);
  } else if (strict && warnings.length > 0) {
    console.log('\n⚠️  Validation failed in strict mode (warnings present)');
    process.exit(1);
  } else {
    console.log('\n✅ Navigation structure is valid');
    process.exit(0);
  }
}

/**
 * Main function
 */
function main() {
  const args = process.argv.slice(2);
  let strict = false;
  let configFile = null;

  // Parse arguments
  args.forEach(arg => {
    if (arg === '--strict') {
      strict = true;
    } else if (!configFile) {
      configFile = arg;
    }
  });

  if (!configFile) {
    console.error('Usage: node validate_navigation_tree.js [--strict] <config-file>');
    process.exit(1);
  }

  // Load and validate configuration
  const config = loadConfig(configFile);
  validateStructure(config);
  printResults(config, strict);
}

// Example configuration format:
const exampleConfig = {
  skipLink: true,
  keyboardNavigation: true,
  landmarkRole: "navigation",
  mobile: {
    breakpoint: 768,
    type: "hamburger"
  },
  focusIndicators: {
    style: "outline",
    color: "#0066cc",
    width: 2
  },
  items: [
    {
      label: "Home",
      href: "/",
      active: true,
      ariaCurrent: "page"
    },
    {
      label: "Products",
      href: "/products",
      ariaHaspopup: true,
      ariaExpanded: false,
      children: [
        {
          label: "Category 1",
          href: "/products/category1"
        },
        {
          label: "Category 2",
          href: "/products/category2"
        }
      ]
    },
    {
      label: "About",
      href: "/about"
    },
    {
      label: "Contact",
      href: "/contact",
      external: true,
      target: "_blank"
    }
  ]
};

// Run if executed directly
if (require.main === module) {
  main();
}

// Export for use as module
module.exports = {
  validateStructure,
  validateItem,
  generateStats,
  generateAccessibilityReport,
  RULES
};