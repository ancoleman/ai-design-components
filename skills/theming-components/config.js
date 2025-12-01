/**
 * Style Dictionary Configuration
 * Transforms W3C design tokens to multiple platform formats
 *
 * Supports: CSS, SCSS, JavaScript, TypeScript, iOS Swift, Android XML
 */

import StyleDictionary from 'style-dictionary';

export default {
  // Source token files
  source: [
    'tokens/global/**/*.json',
    'tokens/themes/light.json',  // Default theme
    'tokens/components/**/*.json'
  ],

  // Platform outputs
  platforms: {
    // CSS Custom Properties (Web)
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [
        {
          destination: 'variables.css',
          format: 'css/variables',
          options: {
            outputReferences: true,  // Use CSS var() references
            showFileHeader: true
          }
        }
      ]
    },

    // CSS - Dark Theme
    'css-dark': {
      transformGroup: 'css',
      buildPath: 'build/css/',
      source: [
        'tokens/global/**/*.json',
        'tokens/themes/light.json',
        'tokens/themes/dark.json',  // Dark theme overrides
        'tokens/components/**/*.json'
      ],
      files: [
        {
          destination: 'variables-dark.css',
          format: 'css/variables',
          options: {
            outputReferences: true,
            showFileHeader: true,
            selector: ':root[data-theme="dark"]'  // Dark theme selector
          }
        }
      ]
    },

    // CSS - High Contrast Theme
    'css-high-contrast': {
      transformGroup: 'css',
      buildPath: 'build/css/',
      source: [
        'tokens/global/**/*.json',
        'tokens/themes/light.json',
        'tokens/themes/high-contrast.json',
        'tokens/components/**/*.json'
      ],
      files: [
        {
          destination: 'variables-high-contrast.css',
          format: 'css/variables',
          options: {
            outputReferences: true,
            showFileHeader: true,
            selector: ':root[data-theme="high-contrast"]'
          }
        }
      ]
    },

    // SCSS Variables
    scss: {
      transformGroup: 'scss',
      buildPath: 'build/scss/',
      files: [
        {
          destination: '_variables.scss',
          format: 'scss/variables',
          options: {
            outputReferences: true,
            showFileHeader: true
          }
        }
      ]
    },

    // JavaScript/TypeScript ES6
    js: {
      transformGroup: 'js',
      buildPath: 'build/js/',
      files: [
        {
          destination: 'tokens.js',
          format: 'javascript/es6',
          options: {
            showFileHeader: true
          }
        },
        {
          destination: 'tokens.d.ts',
          format: 'typescript/es6-declarations',
          options: {
            showFileHeader: true
          }
        }
      ]
    },

    // iOS Swift
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'build/ios/',
      files: [
        {
          destination: 'DesignTokens.swift',
          format: 'ios-swift/class.swift',
          options: {
            className: 'DesignTokens',
            showFileHeader: true
          }
        }
      ]
    },

    // Android XML
    android: {
      transformGroup: 'android',
      buildPath: 'build/android/res/values/',
      files: [
        {
          destination: 'colors.xml',
          format: 'android/colors',
          filter: {
            type: 'color'
          }
        },
        {
          destination: 'dimens.xml',
          format: 'android/dimens',
          filter: {
            type: 'dimension'
          }
        },
        {
          destination: 'font_dimens.xml',
          format: 'android/fontDimens',
          filter: {
            type: 'fontSize'
          }
        }
      ]
    }
  }
};
