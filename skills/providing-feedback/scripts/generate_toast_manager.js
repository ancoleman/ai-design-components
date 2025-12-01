#!/usr/bin/env node

/**
 * Toast Manager Configuration Generator
 *
 * Generates toast notification configurations with proper timing,
 * stacking behavior, and position calculations.
 *
 * Usage: node generate_toast_manager.js [options]
 *
 * Options:
 *   --type <type>        Toast type (success, error, warning, info)
 *   --position <pos>     Position (bottom-right, top-center, etc.)
 *   --max-visible <n>    Maximum visible toasts (default: 5)
 *   --duration <ms>      Auto-dismiss duration
 *   --stacking <type>    Stacking strategy (queue, stack, replace)
 */

// Parse command line arguments
const args = process.argv.slice(2);
const options = {};

for (let i = 0; i < args.length; i += 2) {
  const key = args[i].replace('--', '');
  const value = args[i + 1];
  options[key] = value;
}

// Default configurations
const TOAST_CONFIGS = {
  success: {
    duration: 3000,
    icon: '✓',
    className: 'toast-success',
    ariaRole: 'status',
    ariaLive: 'polite'
  },
  error: {
    duration: 7000,
    icon: '✕',
    className: 'toast-error',
    ariaRole: 'alert',
    ariaLive: 'assertive',
    dismissible: true
  },
  warning: {
    duration: 5000,
    icon: '⚠',
    className: 'toast-warning',
    ariaRole: 'status',
    ariaLive: 'polite'
  },
  info: {
    duration: 4000,
    icon: 'ℹ',
    className: 'toast-info',
    ariaRole: 'status',
    ariaLive: 'polite'
  }
};

// Position configurations
const POSITIONS = {
  'bottom-right': {
    className: 'toast-bottom-right',
    css: {
      bottom: '24px',
      right: '24px',
      left: 'auto',
      top: 'auto'
    }
  },
  'bottom-left': {
    className: 'toast-bottom-left',
    css: {
      bottom: '24px',
      left: '24px',
      right: 'auto',
      top: 'auto'
    }
  },
  'top-right': {
    className: 'toast-top-right',
    css: {
      top: '24px',
      right: '24px',
      left: 'auto',
      bottom: 'auto'
    }
  },
  'top-center': {
    className: 'toast-top-center',
    css: {
      top: '24px',
      left: '50%',
      transform: 'translateX(-50%)',
      right: 'auto',
      bottom: 'auto'
    }
  },
  'bottom-center': {
    className: 'toast-bottom-center',
    css: {
      bottom: '24px',
      left: '50%',
      transform: 'translateX(-50%)',
      right: 'auto',
      top: 'auto'
    }
  }
};

// Stacking strategies
const STACKING_STRATEGIES = {
  queue: {
    maxVisible: 1,
    behavior: 'sequential',
    overlap: false,
    zIndexIncrement: 1
  },
  stack: {
    maxVisible: options['max-visible'] || 5,
    behavior: 'simultaneous',
    overlap: true,
    spacing: 12,
    zIndexIncrement: -1
  },
  replace: {
    maxVisible: 1,
    behavior: 'replace',
    overlap: false,
    zIndexIncrement: 0
  }
};

// Calculate timing based on content
function calculateDuration(type, message = '', hasAction = false) {
  const baseTime = TOAST_CONFIGS[type]?.duration || 4000;

  // Never auto-dismiss if action present
  if (hasAction) {
    return Infinity;
  }

  // Adjust for message length (200ms per word)
  const words = message.split(' ').length;
  const readingTime = words * 200;

  // Use longer of base time or reading time
  const calculatedTime = Math.max(baseTime, readingTime);

  // Cap at 10 seconds
  return Math.min(calculatedTime, 10000);
}

// Generate toast manager configuration
function generateToastManager() {
  const type = options.type || 'info';
  const position = options.position || 'bottom-right';
  const stacking = options.stacking || 'stack';
  const customDuration = options.duration ? parseInt(options.duration) : null;

  const config = {
    type: type,
    ...TOAST_CONFIGS[type],
    position: POSITIONS[position],
    stacking: STACKING_STRATEGIES[stacking],
    duration: customDuration || TOAST_CONFIGS[type].duration,
    animations: {
      enter: generateEnterAnimation(position),
      exit: generateExitAnimation(position)
    },
    styles: generateStyles(type, position),
    accessibility: generateAccessibilityProps(type)
  };

  return config;
}

// Generate enter animation based on position
function generateEnterAnimation(position) {
  const animations = {
    'bottom-right': {
      from: { transform: 'translateX(100%)', opacity: 0 },
      to: { transform: 'translateX(0)', opacity: 1 }
    },
    'bottom-left': {
      from: { transform: 'translateX(-100%)', opacity: 0 },
      to: { transform: 'translateX(0)', opacity: 1 }
    },
    'top-right': {
      from: { transform: 'translateX(100%)', opacity: 0 },
      to: { transform: 'translateX(0)', opacity: 1 }
    },
    'top-center': {
      from: { transform: 'translateX(-50%) translateY(-100%)', opacity: 0 },
      to: { transform: 'translateX(-50%) translateY(0)', opacity: 1 }
    },
    'bottom-center': {
      from: { transform: 'translateX(-50%) translateY(100%)', opacity: 0 },
      to: { transform: 'translateX(-50%) translateY(0)', opacity: 1 }
    }
  };

  return {
    keyframes: animations[position] || animations['bottom-right'],
    duration: 300,
    easing: 'ease-out'
  };
}

// Generate exit animation based on position
function generateExitAnimation(position) {
  const animations = {
    'bottom-right': {
      from: { transform: 'translateX(0)', opacity: 1 },
      to: { transform: 'translateX(100%)', opacity: 0 }
    },
    'bottom-left': {
      from: { transform: 'translateX(0)', opacity: 1 },
      to: { transform: 'translateX(-100%)', opacity: 0 }
    },
    'top-right': {
      from: { transform: 'translateX(0)', opacity: 1 },
      to: { transform: 'translateX(100%)', opacity: 0 }
    },
    'top-center': {
      from: { transform: 'translateX(-50%) translateY(0)', opacity: 1 },
      to: { transform: 'translateX(-50%) translateY(-100%)', opacity: 0 }
    },
    'bottom-center': {
      from: { transform: 'translateX(-50%) translateY(0)', opacity: 1 },
      to: { transform: 'translateX(-50%) translateY(100%)', opacity: 0 }
    }
  };

  return {
    keyframes: animations[position] || animations['bottom-right'],
    duration: 200,
    easing: 'ease-in'
  };
}

// Generate CSS styles
function generateStyles(type, position) {
  const colorMap = {
    success: {
      background: '#10b981',
      color: '#ffffff',
      border: '#059669'
    },
    error: {
      background: '#ef4444',
      color: '#ffffff',
      border: '#dc2626'
    },
    warning: {
      background: '#f59e0b',
      color: '#ffffff',
      border: '#d97706'
    },
    info: {
      background: '#3b82f6',
      color: '#ffffff',
      border: '#2563eb'
    }
  };

  return {
    container: {
      position: 'fixed',
      zIndex: 9999,
      pointerEvents: 'none',
      ...POSITIONS[position].css
    },
    toast: {
      background: colorMap[type].background,
      color: colorMap[type].color,
      borderLeft: `4px solid ${colorMap[type].border}`,
      padding: '12px 16px',
      borderRadius: '6px',
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      minWidth: '300px',
      maxWidth: '500px',
      pointerEvents: 'auto'
    }
  };
}

// Generate accessibility properties
function generateAccessibilityProps(type) {
  return {
    role: TOAST_CONFIGS[type].ariaRole,
    'aria-live': TOAST_CONFIGS[type].ariaLive,
    'aria-atomic': 'true',
    'aria-relevant': 'additions text',
    tabIndex: 0
  };
}

// Generate React component code
function generateReactComponent(config) {
  return `
import React, { useEffect, useState } from 'react';

const ToastManager = ({ toasts, onDismiss }) => {
  const [visibleToasts, setVisibleToasts] = useState([]);

  useEffect(() => {
    // Manage toast visibility based on stacking strategy
    const strategy = '${config.stacking.behavior}';
    const maxVisible = ${config.stacking.maxVisible};

    if (strategy === 'stack') {
      setVisibleToasts(toasts.slice(-maxVisible));
    } else if (strategy === 'queue') {
      setVisibleToasts(toasts.slice(0, 1));
    } else if (strategy === 'replace') {
      setVisibleToasts(toasts.slice(-1));
    }
  }, [toasts]);

  return (
    <div
      className="toast-container"
      style={${JSON.stringify(config.styles.container, null, 4)}}
    >
      {visibleToasts.map((toast, index) => (
        <div
          key={toast.id}
          className="toast ${config.type}"
          style={{
            ...${JSON.stringify(config.styles.toast, null, 6)},
            marginTop: index > 0 ? '${config.stacking.spacing || 12}px' : 0,
            zIndex: ${config.stacking.zIndexIncrement} * index
          }}
          role="${config.accessibility.role}"
          aria-live="${config.accessibility['aria-live']}"
          aria-atomic="${config.accessibility['aria-atomic']}"
        >
          <span className="toast-icon">${config.icon}</span>
          <span className="toast-message">{toast.message}</span>
          {toast.dismissible !== false && (
            <button
              className="toast-dismiss"
              onClick={() => onDismiss(toast.id)}
              aria-label="Dismiss notification"
            >
              ×
            </button>
          )}
        </div>
      ))}
    </div>
  );
};

export default ToastManager;
`;
}

// Generate CSS animation code
function generateCSSAnimations(config) {
  return `
@keyframes toast-enter {
  from {
    transform: ${config.animations.enter.keyframes.from.transform};
    opacity: ${config.animations.enter.keyframes.from.opacity};
  }
  to {
    transform: ${config.animations.enter.keyframes.to.transform};
    opacity: ${config.animations.enter.keyframes.to.opacity};
  }
}

@keyframes toast-exit {
  from {
    transform: ${config.animations.exit.keyframes.from.transform};
    opacity: ${config.animations.exit.keyframes.from.opacity};
  }
  to {
    transform: ${config.animations.exit.keyframes.to.transform};
    opacity: ${config.animations.exit.keyframes.to.opacity};
  }
}

.toast {
  animation: toast-enter ${config.animations.enter.duration}ms ${config.animations.enter.easing};
}

.toast.exiting {
  animation: toast-exit ${config.animations.exit.duration}ms ${config.animations.exit.easing};
}
`;
}

// Main execution
const config = generateToastManager();

// Output results
console.log('Toast Manager Configuration Generated:');
console.log('=====================================\n');

console.log('Configuration Object:');
console.log(JSON.stringify(config, null, 2));
console.log('\n');

console.log('React Component:');
console.log(generateReactComponent(config));
console.log('\n');

console.log('CSS Animations:');
console.log(generateCSSAnimations(config));

// Export for use in other scripts
module.exports = {
  generateToastManager,
  calculateDuration,
  TOAST_CONFIGS,
  POSITIONS,
  STACKING_STRATEGIES
};