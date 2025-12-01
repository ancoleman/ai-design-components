#!/usr/bin/env node

/**
 * Calculate Fluid Typography Scales
 * Generates fluid typography scales using CSS clamp() for responsive text
 */

const fs = require('fs');

// Parse command line arguments
const args = process.argv.slice(2);
const options = {};
args.forEach((arg, index) => {
  if (arg.startsWith('--')) {
    const key = arg.slice(2);
    const value = args[index + 1];
    options[key] = value && !value.startsWith('--') ? value : true;
  }
});

// Configuration with defaults
const minViewport = parseInt(options['min-vw']) || 320;  // Minimum viewport width in px
const maxViewport = parseInt(options['max-vw']) || 1920; // Maximum viewport width in px
const minFontSize = parseInt(options['min-font']) || 16;  // Base font size at min viewport
const maxFontSize = parseInt(options['max-font']) || 20;  // Base font size at max viewport
const scale = options.scale || 'major-third';              // Type scale ratio
const steps = parseInt(options.steps) || 9;               // Number of scale steps
const format = options.format || 'css';                    // Output format

// Type scale ratios
const typeScales = {
  'minor-second': 1.067,
  'major-second': 1.125,
  'minor-third': 1.2,
  'major-third': 1.25,
  'perfect-fourth': 1.333,
  'augmented-fourth': 1.414,
  'perfect-fifth': 1.5,
  'golden-ratio': 1.618,
  'major-sixth': 1.667,
  'minor-seventh': 1.778,
  'major-seventh': 1.875,
  'octave': 2
};

// Scale names for CSS variables
const scaleNames = [
  'xs',   // Extra small
  'sm',   // Small
  'base', // Base
  'lg',   // Large
  'xl',   // Extra large
  '2xl',  // 2X large
  '3xl',  // 3X large
  '4xl',  // 4X large
  '5xl',  // 5X large
  '6xl',  // 6X large
  '7xl',  // 7X large
  '8xl',  // 8X large
  '9xl'   // 9X large
];

/**
 * Calculate fluid value using clamp
 * Returns CSS clamp() function string
 */
function calculateFluidValue(minSize, maxSize, minVw = minViewport, maxVw = maxViewport) {
  // Calculate viewport width coefficient
  const slope = (maxSize - minSize) / (maxVw - minVw);
  const yAxisIntersection = -minVw * slope + minSize;

  // Convert to rem (assuming 16px base)
  const minRem = (minSize / 16).toFixed(3);
  const maxRem = (maxSize / 16).toFixed(3);
  const preferredRem = (yAxisIntersection / 16).toFixed(3);
  const preferredVw = (slope * 100).toFixed(3);

  // Generate clamp function
  return `clamp(${minRem}rem, ${preferredRem}rem + ${preferredVw}vw, ${maxRem}rem)`;
}

/**
 * Generate fluid typography scale
 */
function generateScale() {
  const ratio = typeScales[scale] || parseFloat(scale) || 1.25;
  const scales = [];

  // Find the base index (usually 2 for 'base')
  const baseIndex = 2;

  for (let i = 0; i < steps; i++) {
    const multiplier = Math.pow(ratio, i - baseIndex);
    const minSize = Math.round(minFontSize * multiplier);
    const maxSize = Math.round(maxFontSize * multiplier);

    scales.push({
      name: scaleNames[i] || `step-${i}`,
      minSize,
      maxSize,
      fluid: calculateFluidValue(minSize, maxSize),
      // Calculate line height that scales appropriately
      lineHeight: calculateLineHeight(i, baseIndex)
    });
  }

  return scales;
}

/**
 * Calculate appropriate line height for each scale step
 */
function calculateLineHeight(step, baseStep) {
  // Tighter line height for larger text, looser for smaller
  if (step < baseStep) {
    return 1.6; // Smaller text needs more line height
  } else if (step === baseStep) {
    return 1.5; // Base line height
  } else if (step <= baseStep + 2) {
    return 1.4; // Slightly larger text
  } else if (step <= baseStep + 4) {
    return 1.3; // Large text
  } else {
    return 1.2; // Display text
  }
}

/**
 * Generate CSS output
 */
function generateCSS(scales) {
  let css = `/* Fluid Typography Scale */\n`;
  css += `/* Scale: ${scale} (${typeScales[scale] || scale}) */\n`;
  css += `/* Viewport range: ${minViewport}px - ${maxViewport}px */\n`;
  css += `/* Font size range: ${minFontSize}px - ${maxFontSize}px (base) */\n`;
  css += `/* Generated: ${new Date().toISOString()} */\n\n`;

  css += `:root {\n`;

  // Font sizes
  scales.forEach(item => {
    css += `  --text-${item.name}: ${item.fluid};\n`;
  });

  css += `\n  /* Line heights */\n`;
  scales.forEach(item => {
    css += `  --leading-${item.name}: ${item.lineHeight};\n`;
  });

  css += `\n  /* Letter spacing (tracking) */\n`;
  scales.forEach((item, index) => {
    const tracking = index < 2 ? '0.025em' : index < 4 ? '0' : '-0.025em';
    css += `  --tracking-${item.name}: ${tracking};\n`;
  });

  css += `}\n\n`;

  // Utility classes
  css += `/* Utility classes */\n`;
  scales.forEach(item => {
    css += `.text-${item.name} {\n`;
    css += `  font-size: var(--text-${item.name});\n`;
    css += `  line-height: var(--leading-${item.name});\n`;
    css += `  letter-spacing: var(--tracking-${item.name});\n`;
    css += `}\n\n`;
  });

  // Typography elements
  css += `/* Default HTML elements */\n`;
  css += `body { font-size: var(--text-base); line-height: var(--leading-base); }\n`;
  css += `h1 { font-size: var(--text-4xl); line-height: var(--leading-4xl); }\n`;
  css += `h2 { font-size: var(--text-3xl); line-height: var(--leading-3xl); }\n`;
  css += `h3 { font-size: var(--text-2xl); line-height: var(--leading-2xl); }\n`;
  css += `h4 { font-size: var(--text-xl); line-height: var(--leading-xl); }\n`;
  css += `h5 { font-size: var(--text-lg); line-height: var(--leading-lg); }\n`;
  css += `h6 { font-size: var(--text-base); line-height: var(--leading-base); }\n`;
  css += `small { font-size: var(--text-sm); line-height: var(--leading-sm); }\n`;

  return css;
}

/**
 * Generate SCSS output
 */
function generateSCSS(scales) {
  let scss = `// Fluid Typography Scale\n`;
  scss += `// Scale: ${scale} (${typeScales[scale] || scale})\n`;
  scss += `// Viewport range: ${minViewport}px - ${maxViewport}px\n\n`;

  scss += `// Font size variables\n`;
  scales.forEach(item => {
    scss += `$text-${item.name}: ${item.fluid};\n`;
  });

  scss += `\n// Line height variables\n`;
  scales.forEach(item => {
    scss += `$leading-${item.name}: ${item.lineHeight};\n`;
  });

  scss += `\n// Typography map\n`;
  scss += `$typography: (\n`;
  scales.forEach((item, index) => {
    scss += `  "${item.name}": (\n`;
    scss += `    "size": ${item.fluid},\n`;
    scss += `    "line-height": ${item.lineHeight},\n`;
    scss += `    "min": ${item.minSize}px,\n`;
    scss += `    "max": ${item.maxSize}px\n`;
    scss += `  )${index < scales.length - 1 ? ',' : ''}\n`;
  });
  scss += `);\n\n`;

  scss += `// Typography mixin\n`;
  scss += `@mixin text($size) {\n`;
  scss += `  font-size: map-get(map-get($typography, $size), "size");\n`;
  scss += `  line-height: map-get(map-get($typography, $size), "line-height");\n`;
  scss += `}\n`;

  return scss;
}

/**
 * Generate JavaScript output
 */
function generateJS(scales) {
  const jsObject = {
    scale: scale,
    ratio: typeScales[scale] || scale,
    viewport: {
      min: minViewport,
      max: maxViewport
    },
    fontSize: {
      min: minFontSize,
      max: maxFontSize
    },
    scales: {}
  };

  scales.forEach(item => {
    jsObject.scales[item.name] = {
      fluid: item.fluid,
      min: `${item.minSize}px`,
      max: `${item.maxSize}px`,
      lineHeight: item.lineHeight
    };
  });

  let js = `// Fluid Typography Scale\n`;
  js += `// Generated: ${new Date().toISOString()}\n\n`;
  js += `export const typography = ${JSON.stringify(jsObject, null, 2)};\n\n`;

  js += `// Helper function to get typography styles\n`;
  js += `export function getTextStyle(size) {\n`;
  js += `  const style = typography.scales[size];\n`;
  js += `  if (!style) {\n`;
  js += `    console.warn(\`Unknown text size: \${size}\`);\n`;
  js += `    return {};\n`;
  js += `  }\n`;
  js += `  return {\n`;
  js += `    fontSize: style.fluid,\n`;
  js += `    lineHeight: style.lineHeight\n`;
  js += `  };\n`;
  js += `};\n`;

  return js;
}

/**
 * Generate Tailwind config
 */
function generateTailwind(scales) {
  const config = {
    fontSize: {}
  };

  scales.forEach(item => {
    config.fontSize[item.name] = [
      item.fluid,
      {
        lineHeight: item.lineHeight.toString(),
        letterSpacing: item.name.includes('xl') ? '-0.025em' : '0'
      }
    ];
  });

  let output = `// Tailwind Typography Config\n`;
  output += `// Add to tailwind.config.js theme.extend.fontSize\n\n`;
  output += `module.exports = {\n`;
  output += `  theme: {\n`;
  output += `    extend: {\n`;
  output += `      fontSize: ${JSON.stringify(config.fontSize, null, 8)}\n`;
  output += `    }\n`;
  output += `  }\n`;
  output += `};\n`;

  return output;
}

/**
 * Main function
 */
function main() {
  if (options.help) {
    console.log(`
Fluid Typography Calculator

Generates fluid typography scales using CSS clamp() for responsive text that scales
smoothly between minimum and maximum viewport widths.

Usage:
  node calculate_fluid_typography.js [options]

Options:
  --min-vw <pixels>      Minimum viewport width (default: 320)
  --max-vw <pixels>      Maximum viewport width (default: 1920)
  --min-font <pixels>    Base font size at min viewport (default: 16)
  --max-font <pixels>    Base font size at max viewport (default: 20)
  --scale <name|ratio>   Type scale ratio (default: major-third)
  --steps <number>       Number of scale steps (default: 9)
  --format <type>        Output format: css|scss|js|tailwind (default: css)
  --output <file>        Output file path
  --help                 Show this help message

Available scales:
  minor-second (1.067), major-second (1.125), minor-third (1.2),
  major-third (1.25), perfect-fourth (1.333), augmented-fourth (1.414),
  perfect-fifth (1.5), golden-ratio (1.618), major-sixth (1.667),
  minor-seventh (1.778), major-seventh (1.875), octave (2)

Examples:
  # Generate CSS with golden ratio scale
  node calculate_fluid_typography.js --scale golden-ratio

  # Generate Tailwind config
  node calculate_fluid_typography.js --format tailwind --output tailwind-typography.js

  # Custom viewport and font ranges
  node calculate_fluid_typography.js --min-vw 375 --max-vw 1440 --min-font 14 --max-font 18
    `);
    process.exit(0);
  }

  const scales = generateScale();

  let output;
  switch (format) {
    case 'scss':
      output = generateSCSS(scales);
      break;
    case 'js':
    case 'javascript':
      output = generateJS(scales);
      break;
    case 'tailwind':
      output = generateTailwind(scales);
      break;
    case 'css':
    default:
      output = generateCSS(scales);
      break;
  }

  if (options.output) {
    fs.writeFileSync(options.output, output);
    console.log(`✓ Fluid typography generated and saved to ${options.output}`);
  } else {
    console.log(output);
  }

  // Display summary
  console.log('\n--- Typography Summary ---');
  console.log(`Scale: ${scale} (${typeScales[scale] || scale})`);
  console.log(`Viewport: ${minViewport}px → ${maxViewport}px`);
  console.log(`Base font: ${minFontSize}px → ${maxFontSize}px`);
  console.log(`Steps: ${steps}`);
  console.log('\nGenerated sizes:');
  scales.forEach(item => {
    console.log(`  ${item.name}: ${item.minSize}px → ${item.maxSize}px`);
  });
}

// Run the script
main();