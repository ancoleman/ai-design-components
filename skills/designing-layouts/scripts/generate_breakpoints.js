#!/usr/bin/env node

/**
 * Generate Responsive Breakpoint System
 * Calculates and generates breakpoint configurations based on approach and device targets
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
const options = {};
args.forEach((arg, index) => {
  if (arg.startsWith('--')) {
    const key = arg.slice(2);
    const value = args[index + 1];
    options[key] = value;
  }
});

// Configuration
const approach = options.approach || 'mobile-first'; // mobile-first or desktop-first
const format = options.format || 'css'; // css, scss, js, json
const outputFile = options.output || null;

// Standard breakpoint system based on common device sizes
const standardBreakpoints = {
  'xs': { min: 0, max: 639, label: 'Extra Small (Phones < 640px)' },
  'sm': { min: 640, max: 767, label: 'Small (Large Phones 640px-767px)' },
  'md': { min: 768, max: 1023, label: 'Medium (Tablets 768px-1023px)' },
  'lg': { min: 1024, max: 1279, label: 'Large (Desktops 1024px-1279px)' },
  'xl': { min: 1280, max: 1535, label: 'Extra Large (Wide Screens 1280px-1535px)' },
  '2xl': { min: 1536, max: null, label: '2X Large (Ultra Wide > 1536px)' }
};

// Content-based breakpoints (based on line length and readability)
const contentBreakpoints = {
  'compact': { min: 0, max: 479, label: 'Compact (Single column)' },
  'narrow': { min: 480, max: 719, label: 'Narrow (Comfortable mobile reading)' },
  'medium': { min: 720, max: 959, label: 'Medium (2-column layouts possible)' },
  'wide': { min: 960, max: 1199, label: 'Wide (Multi-column layouts)' },
  'full': { min: 1200, max: null, label: 'Full (Maximum content width)' }
};

// Device-specific breakpoints
const deviceBreakpoints = {
  'iphone-se': { width: 375, height: 667 },
  'iphone-12': { width: 390, height: 844 },
  'iphone-14-pro-max': { width: 430, height: 932 },
  'ipad-mini': { width: 768, height: 1024 },
  'ipad-air': { width: 820, height: 1180 },
  'ipad-pro-12': { width: 1024, height: 1366 },
  'macbook-air': { width: 1440, height: 900 },
  'imac-24': { width: 1920, height: 1080 },
  'imac-27': { width: 2560, height: 1440 }
};

/**
 * Generate CSS output
 */
function generateCSS(breakpoints, approach) {
  let css = `/* Generated Responsive Breakpoints */\n`;
  css += `/* Approach: ${approach} */\n`;
  css += `/* Generated: ${new Date().toISOString()} */\n\n`;

  // CSS Custom Properties
  css += `:root {\n`;
  Object.entries(breakpoints).forEach(([key, value]) => {
    if (value.min !== null && value.min !== 0) {
      css += `  --breakpoint-${key}-min: ${value.min}px;\n`;
    }
    if (value.max !== null) {
      css += `  --breakpoint-${key}-max: ${value.max}px;\n`;
    }
  });
  css += `}\n\n`;

  // Media queries
  if (approach === 'mobile-first') {
    css += `/* Mobile First Media Queries */\n`;
    Object.entries(breakpoints).forEach(([key, value]) => {
      if (value.min > 0) {
        css += `\n/* ${value.label} */\n`;
        css += `@media (min-width: ${value.min}px) {\n`;
        css += `  .container {\n`;
        css += `    max-width: ${value.min}px;\n`;
        css += `  }\n`;
        css += `}\n`;
      }
    });
  } else {
    css += `/* Desktop First Media Queries */\n`;
    Object.entries(breakpoints).forEach(([key, value]) => {
      if (value.max !== null) {
        css += `\n/* ${value.label} */\n`;
        css += `@media (max-width: ${value.max}px) {\n`;
        css += `  .container {\n`;
        css += `    max-width: 100%;\n`;
        css += `  }\n`;
        css += `}\n`;
      }
    });
  }

  // Container queries
  css += `\n/* Container Queries */\n`;
  Object.entries(breakpoints).forEach(([key, value]) => {
    if (value.min > 0) {
      css += `@container (min-width: ${value.min}px) {\n`;
      css += `  .responsive-component {\n`;
      css += `    /* Styles for ${key} container size */\n`;
      css += `  }\n`;
      css += `}\n`;
    }
  });

  return css;
}

/**
 * Generate SCSS output
 */
function generateSCSS(breakpoints, approach) {
  let scss = `// Generated Responsive Breakpoints\n`;
  scss += `// Approach: ${approach}\n`;
  scss += `// Generated: ${new Date().toISOString()}\n\n`;

  // SCSS variables
  scss += `// Breakpoint variables\n`;
  Object.entries(breakpoints).forEach(([key, value]) => {
    scss += `$breakpoint-${key}: ${value.min || 0}px;\n`;
  });

  scss += `\n// Breakpoint map\n`;
  scss += `$breakpoints: (\n`;
  Object.entries(breakpoints).forEach(([key, value], index, array) => {
    scss += `  "${key}": ${value.min || 0}px${index < array.length - 1 ? ',' : ''}\n`;
  });
  scss += `);\n\n`;

  // Mixins
  scss += `// Responsive mixins\n`;
  scss += `@mixin respond-to($breakpoint) {\n`;
  if (approach === 'mobile-first') {
    scss += `  @media (min-width: map-get($breakpoints, $breakpoint)) {\n`;
  } else {
    scss += `  @media (max-width: map-get($breakpoints, $breakpoint)) {\n`;
  }
  scss += `    @content;\n`;
  scss += `  }\n`;
  scss += `}\n\n`;

  scss += `// Usage example:\n`;
  scss += `// .component {\n`;
  scss += `//   @include respond-to("md") {\n`;
  scss += `//     display: grid;\n`;
  scss += `//   }\n`;
  scss += `// }\n`;

  return scss;
}

/**
 * Generate JavaScript output
 */
function generateJS(breakpoints, approach) {
  const jsObject = {
    approach,
    generated: new Date().toISOString(),
    breakpoints: {},
    utils: {}
  };

  Object.entries(breakpoints).forEach(([key, value]) => {
    jsObject.breakpoints[key] = {
      min: value.min || 0,
      max: value.max || Infinity,
      label: value.label
    };
  });

  let js = `// Generated Responsive Breakpoints\n`;
  js += `// Approach: ${approach}\n\n`;
  js += `export const breakpoints = ${JSON.stringify(jsObject.breakpoints, null, 2)};\n\n`;

  js += `// Utility functions\n`;
  js += `export const media = {\n`;
  Object.keys(breakpoints).forEach((key) => {
    if (approach === 'mobile-first') {
      js += `  ${key}: \`@media (min-width: \${breakpoints.${key}.min}px)\`,\n`;
    } else {
      js += `  ${key}: \`@media (max-width: \${breakpoints.${key}.max}px)\`,\n`;
    }
  });
  js += `};\n\n`;

  js += `// Check current breakpoint\n`;
  js += `export function getCurrentBreakpoint() {\n`;
  js += `  const width = window.innerWidth;\n`;
  js += `  for (const [key, value] of Object.entries(breakpoints)) {\n`;
  js += `    if (width >= value.min && width <= (value.max || Infinity)) {\n`;
  js += `      return key;\n`;
  js += `    }\n`;
  js += `  }\n`;
  js += `  return null;\n`;
  js += `};\n`;

  return js;
}

/**
 * Generate JSON output
 */
function generateJSON(breakpoints, approach) {
  const jsonObject = {
    approach,
    generated: new Date().toISOString(),
    breakpoints: breakpoints,
    devices: deviceBreakpoints
  };

  return JSON.stringify(jsonObject, null, 2);
}

/**
 * Main generation function
 */
function generateBreakpoints() {
  const breakpoints = options.content === 'content' ? contentBreakpoints : standardBreakpoints;

  let output;
  switch (format) {
    case 'scss':
      output = generateSCSS(breakpoints, approach);
      break;
    case 'js':
    case 'javascript':
      output = generateJS(breakpoints, approach);
      break;
    case 'json':
      output = generateJSON(breakpoints, approach);
      break;
    case 'css':
    default:
      output = generateCSS(breakpoints, approach);
      break;
  }

  if (outputFile) {
    fs.writeFileSync(outputFile, output);
    console.log(`✓ Breakpoints generated and saved to ${outputFile}`);
  } else {
    console.log(output);
  }

  // Summary
  console.log('\n--- Breakpoint Summary ---');
  console.log(`Approach: ${approach}`);
  console.log(`Format: ${format}`);
  console.log(`Breakpoints: ${Object.keys(breakpoints).join(', ')}`);
  console.log('\nBreakpoint ranges:');
  Object.entries(breakpoints).forEach(([key, value]) => {
    const range = value.max ? `${value.min}px - ${value.max}px` : `${value.min}px+`;
    console.log(`  ${key}: ${range} - ${value.label}`);
  });
}

// Display help if requested
if (options.help) {
  console.log(`
Generate Responsive Breakpoint System

Usage:
  node generate_breakpoints.js [options]

Options:
  --approach [mobile-first|desktop-first]  Breakpoint approach (default: mobile-first)
  --format [css|scss|js|json]              Output format (default: css)
  --content                                 Use content-based breakpoints instead of device-based
  --output <file>                          Output file path
  --help                                   Show this help message

Examples:
  node generate_breakpoints.js --approach mobile-first --format css
  node generate_breakpoints.js --format scss --output breakpoints.scss
  node generate_breakpoints.js --content --format json --output content-breakpoints.json
  `);
  process.exit(0);
}

// Run generation
generateBreakpoints();