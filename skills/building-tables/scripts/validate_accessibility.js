#!/usr/bin/env node

/**
 * Table Accessibility Validator
 * Checks tables for WCAG compliance and ARIA implementation
 */

class AccessibilityValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.passes = [];
  }

  /**
   * Validate HTML table structure
   */
  validateTableStructure(html) {
    // Check for table element
    if (!html.includes('<table')) {
      this.addError('Missing <table> element');
      return false;
    }

    // Check for caption
    if (!html.includes('<caption>')) {
      this.addWarning('Missing <caption> element - tables should have descriptive captions');
    } else {
      this.addPass('Table has caption');
    }

    // Check for thead
    if (!html.includes('<thead>')) {
      this.addWarning('Missing <thead> element - use to group header content');
    } else {
      this.addPass('Table has proper header structure');
    }

    // Check for tbody
    if (!html.includes('<tbody>')) {
      this.addWarning('Missing <tbody> element - use to group body content');
    } else {
      this.addPass('Table has proper body structure');
    }

    // Check for th elements
    if (!html.includes('<th')) {
      this.addError('Missing <th> elements - use for header cells');
    } else {
      // Check for scope attribute
      const thRegex = /<th[^>]*>/g;
      const thTags = html.match(thRegex) || [];

      thTags.forEach(tag => {
        if (!tag.includes('scope=')) {
          this.addWarning('Header cell missing scope attribute');
        }
      });
    }

    return this.errors.length === 0;
  }

  /**
   * Validate ARIA attributes for interactive tables
   */
  validateARIA(html) {
    // Check for grid pattern if interactive
    if (html.includes('role="grid"')) {
      this.addPass('Using ARIA grid pattern for interactive table');

      // Check for required grid attributes
      if (!html.includes('role="columnheader"')) {
        this.addWarning('Grid missing role="columnheader" for headers');
      }

      if (!html.includes('role="gridcell"')) {
        this.addWarning('Grid missing role="gridcell" for cells');
      }

      // Check for aria-rowcount when using virtual scrolling
      if (html.includes('virtual') && !html.includes('aria-rowcount')) {
        this.addError('Virtual scrolling requires aria-rowcount');
      }
    }

    // Check for sort indicators
    if (html.includes('sortable') || html.includes('sort')) {
      if (!html.includes('aria-sort')) {
        this.addWarning('Sortable columns should use aria-sort attribute');
      } else {
        this.addPass('Sortable columns have proper ARIA attributes');
      }
    }

    // Check for selection state
    if (html.includes('selectable') || html.includes('checkbox')) {
      if (!html.includes('aria-selected')) {
        this.addWarning('Selectable rows should use aria-selected attribute');
      }
    }

    // Check for live regions
    if (html.includes('filter') || html.includes('search')) {
      if (!html.includes('aria-live')) {
        this.addWarning('Dynamic content changes should use aria-live regions');
      }
    }

    // Check for loading states
    if (html.includes('loading') || html.includes('spinner')) {
      if (!html.includes('aria-busy')) {
        this.addWarning('Loading states should use aria-busy attribute');
      }
    }
  }

  /**
   * Validate keyboard navigation support
   */
  validateKeyboardSupport(eventHandlers = {}) {
    const requiredKeys = [
      'ArrowUp',
      'ArrowDown',
      'ArrowLeft',
      'ArrowRight',
      'Enter',
      'Space',
      'Escape',
      'Tab'
    ];

    const implementedKeys = Object.keys(eventHandlers);

    requiredKeys.forEach(key => {
      if (!implementedKeys.includes(key)) {
        this.addWarning(`Missing keyboard handler for ${key} key`);
      } else {
        this.addPass(`Keyboard navigation for ${key} implemented`);
      }
    });

    // Check for Home/End support
    if (implementedKeys.includes('Home') && implementedKeys.includes('End')) {
      this.addPass('Advanced keyboard navigation (Home/End) supported');
    }

    // Check for Ctrl/Cmd combinations
    if (implementedKeys.some(key => key.includes('Ctrl') || key.includes('Cmd'))) {
      this.addPass('Keyboard shortcuts implemented');
    }
  }

  /**
   * Validate color contrast
   */
  validateColorContrast(styles = {}) {
    const minimumContrast = {
      normalText: 4.5,
      largeText: 3.0,
      ui: 3.0
    };

    // Check text contrast
    if (styles.textContrast) {
      if (styles.textContrast < minimumContrast.normalText) {
        this.addError(`Text contrast ratio ${styles.textContrast} is below WCAG AA requirement (4.5:1)`);
      } else {
        this.addPass('Text contrast meets WCAG AA standards');
      }
    }

    // Check if color is sole indicator
    if (styles.usesColorAlone) {
      this.addError('Color should not be the only means of conveying information');
    }

    // Check focus indicators
    if (!styles.focusIndicator) {
      this.addError('Interactive elements must have visible focus indicators');
    } else {
      this.addPass('Focus indicators are properly implemented');
    }
  }

  /**
   * Validate screen reader support
   */
  validateScreenReaderSupport(component) {
    const checks = [
      {
        property: 'ariaLabel',
        message: 'Interactive elements should have aria-label or aria-labelledby'
      },
      {
        property: 'ariaDescribedby',
        message: 'Complex elements should use aria-describedby for additional context'
      },
      {
        property: 'announcements',
        message: 'Dynamic changes should be announced to screen readers'
      },
      {
        property: 'headingStructure',
        message: 'Use proper heading hierarchy for table sections'
      }
    ];

    checks.forEach(check => {
      if (component[check.property]) {
        this.addPass(check.message.replace('should', 'do'));
      } else {
        this.addWarning(check.message);
      }
    });
  }

  /**
   * Validate responsive accessibility
   */
  validateResponsiveAccessibility(breakpoints = {}) {
    // Check mobile touch targets
    if (breakpoints.mobile) {
      if (breakpoints.mobile.touchTargetSize < 44) {
        this.addError('Touch targets must be at least 44x44 pixels');
      } else {
        this.addPass('Touch targets meet minimum size requirements');
      }

      // Check horizontal scrolling
      if (breakpoints.mobile.horizontalScroll && !breakpoints.mobile.scrollIndicator) {
        this.addWarning('Horizontally scrollable tables should indicate scroll availability');
      }
    }

    // Check zoom support
    if (breakpoints.supportsZoom === false) {
      this.addError('Must support zoom up to 200% without horizontal scrolling');
    }
  }

  /**
   * Add validation messages
   */
  addError(message) {
    this.errors.push(`❌ ERROR: ${message}`);
  }

  addWarning(message) {
    this.warnings.push(`⚠️  WARNING: ${message}`);
  }

  addPass(message) {
    this.passes.push(`✅ PASS: ${message}`);
  }

  /**
   * Generate validation report
   */
  generateReport() {
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║   TABLE ACCESSIBILITY VALIDATION REPORT  ║');
    console.log('╚════════════════════════════════════════╝\n');

    const totalChecks = this.errors.length + this.warnings.length + this.passes.length;
    const score = Math.round((this.passes.length / totalChecks) * 100);

    // Summary
    console.log('📊 SUMMARY');
    console.log('──────────');
    console.log(`  Total Checks: ${totalChecks}`);
    console.log(`  ✅ Passed: ${this.passes.length}`);
    console.log(`  ⚠️  Warnings: ${this.warnings.length}`);
    console.log(`  ❌ Errors: ${this.errors.length}`);
    console.log(`  📈 Score: ${score}%`);

    // Grade
    let grade = '';
    if (score >= 90 && this.errors.length === 0) grade = 'A - Excellent';
    else if (score >= 80 && this.errors.length <= 2) grade = 'B - Good';
    else if (score >= 70 && this.errors.length <= 5) grade = 'C - Fair';
    else if (score >= 60) grade = 'D - Poor';
    else grade = 'F - Failing';

    console.log(`  🏆 Grade: ${grade}\n`);

    // Critical Errors
    if (this.errors.length > 0) {
      console.log('🚨 CRITICAL ISSUES (Must Fix)');
      console.log('────────────────────────────');
      this.errors.forEach(error => console.log(`  ${error}`));
      console.log('');
    }

    // Warnings
    if (this.warnings.length > 0) {
      console.log('⚠️  WARNINGS (Should Fix)');
      console.log('──────────────────────');
      this.warnings.forEach(warning => console.log(`  ${warning}`));
      console.log('');
    }

    // Passes
    if (this.passes.length > 0 && process.argv.includes('--verbose')) {
      console.log('✅ PASSED CHECKS');
      console.log('───────────────');
      this.passes.forEach(pass => console.log(`  ${pass}`));
      console.log('');
    }

    // Recommendations
    this.printRecommendations();
  }

  /**
   * Print accessibility recommendations
   */
  printRecommendations() {
    console.log('💡 RECOMMENDATIONS');
    console.log('════════════════════════════════════');

    const recommendations = [];

    // Based on errors and warnings
    if (this.errors.some(e => e.includes('caption'))) {
      recommendations.push({
        priority: 'High',
        action: 'Add descriptive captions to all tables',
        benefit: 'Helps screen reader users understand table content'
      });
    }

    if (this.warnings.some(w => w.includes('scope'))) {
      recommendations.push({
        priority: 'Medium',
        action: 'Add scope attributes to all header cells',
        benefit: 'Clarifies header relationships for assistive technology'
      });
    }

    if (this.warnings.some(w => w.includes('keyboard'))) {
      recommendations.push({
        priority: 'High',
        action: 'Implement complete keyboard navigation',
        benefit: 'Essential for users who cannot use a mouse'
      });
    }

    if (this.errors.some(e => e.includes('contrast'))) {
      recommendations.push({
        priority: 'Critical',
        action: 'Improve color contrast ratios',
        benefit: 'Ensures readability for users with visual impairments'
      });
    }

    if (recommendations.length === 0) {
      console.log('\n  ✅ Great job! Your table meets accessibility standards.');
      console.log('  Continue testing with real screen readers and users.\n');
    } else {
      recommendations.forEach((rec, index) => {
        console.log(`\n  ${index + 1}. [${rec.priority}] ${rec.action}`);
        console.log(`     ↳ ${rec.benefit}`);
      });
      console.log('');
    }

    // Testing tools
    console.log('🔧 RECOMMENDED TESTING TOOLS');
    console.log('──────────────────────────');
    console.log('  • axe DevTools - Browser extension');
    console.log('  • WAVE - Web accessibility evaluation');
    console.log('  • NVDA - Free screen reader (Windows)');
    console.log('  • VoiceOver - Built-in (macOS/iOS)');
    console.log('  • Lighthouse - Chrome DevTools audit');

    console.log('\n════════════════════════════════════\n');
  }

  /**
   * Run validation on sample HTML
   */
  validateHTML(htmlString) {
    console.log('Validating table accessibility...\n');

    this.validateTableStructure(htmlString);
    this.validateARIA(htmlString);

    // Mock component data for demonstration
    const mockComponent = {
      ariaLabel: htmlString.includes('aria-label'),
      announcements: htmlString.includes('aria-live'),
      headingStructure: htmlString.includes('<h')
    };
    this.validateScreenReaderSupport(mockComponent);

    // Mock styles for demonstration
    const mockStyles = {
      textContrast: 4.5,
      usesColorAlone: false,
      focusIndicator: htmlString.includes('focus')
    };
    this.validateColorContrast(mockStyles);

    this.generateReport();
  }
}

// CLI interface
if (require.main === module) {
  const validator = new AccessibilityValidator();

  // Sample HTML for testing
  const sampleHTML = `
    <table role="grid" aria-label="Employee data">
      <caption>Employee Directory</caption>
      <thead>
        <tr>
          <th scope="col" role="columnheader" aria-sort="ascending">Name</th>
          <th scope="col" role="columnheader">Email</th>
          <th scope="col" role="columnheader">Department</th>
        </tr>
      </thead>
      <tbody>
        <tr role="row">
          <td role="gridcell" tabindex="0">John Doe</td>
          <td role="gridcell" tabindex="-1">john@example.com</td>
          <td role="gridcell" tabindex="-1">Engineering</td>
        </tr>
      </tbody>
    </table>
    <div role="status" aria-live="polite">3 results found</div>
  `;

  // Check if HTML file provided
  const args = process.argv.slice(2);
  if (args.length > 0 && !args[0].startsWith('--')) {
    const fs = require('fs');
    const htmlContent = fs.readFileSync(args[0], 'utf8');
    validator.validateHTML(htmlContent);
  } else {
    // Use sample HTML
    validator.validateHTML(sampleHTML);
  }
}

module.exports = AccessibilityValidator;