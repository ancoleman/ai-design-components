/**
 * First-Time Product Tour Example
 *
 * Demonstrates a complete product tour implementation using react-joyride
 * with design token integration and accessibility features.
 */

import { useState, useEffect } from 'react';
import Joyride, { Step, CallBackProps, STATUS, ACTIONS } from 'react-joyride';

const steps: Step[] = [
  {
    target: 'body',
    content: 'Welcome! Let\'s take a quick tour of the key features.',
    placement: 'center',
    disableBeacon: true,
  },
  {
    target: '.dashboard-header',
    content: 'This is your dashboard where you\'ll find all your recent activity.',
    placement: 'bottom',
  },
  {
    target: '.create-button',
    content: 'Click here anytime to create a new project.',
    placement: 'bottom',
  },
  {
    target: '.navigation-menu',
    content: 'Use this menu to navigate between different sections.',
    placement: 'right',
  },
  {
    target: '.help-button',
    content: 'Need help? Click here to access documentation and support.',
    placement: 'bottom',
  },
];

export function FirstTimeTour() {
  const [run, setRun] = useState(false);
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    // Check if user has completed tour
    const tourCompleted = localStorage.getItem('tourCompleted');
    if (!tourCompleted) {
      // Delay tour start to let page load
      const timer = setTimeout(() => setRun(true), 500);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status, action, index } = data;

    if (status === STATUS.FINISHED) {
      // Tour completed successfully
      setRun(false);
      localStorage.setItem('tourCompleted', 'true');
      // Optional: Track completion analytics
      console.log('Tour completed');
    } else if (status === STATUS.SKIPPED) {
      // User skipped tour
      setRun(false);
      localStorage.setItem('tourSkipped', 'true');
      // Optional: Track skip analytics
      console.log('Tour skipped');
    }

    if (action === ACTIONS.NEXT) {
      setStepIndex(index + 1);
    } else if (action === ACTIONS.PREV) {
      setStepIndex(index - 1);
    }
  };

  return (
    <Joyride
      steps={steps}
      run={run}
      stepIndex={stepIndex}
      continuous
      showProgress
      showSkipButton
      callback={handleJoyrideCallback}
      locale={{
        back: 'Back',
        close: 'Close',
        last: 'Finish',
        next: 'Next',
        skip: 'Skip tour',
      }}
      styles={{
        options: {
          // Use design tokens for theming
          backgroundColor: 'var(--tour-spotlight-bg)',
          textColor: 'var(--tour-spotlight-text)',
          primaryColor: 'var(--color-primary)',
          overlayColor: 'var(--tour-overlay-bg)',
          arrowColor: 'var(--tour-spotlight-bg)',
          borderRadius: 'var(--tour-spotlight-border-radius)',
          zIndex: 10000,
        },
        tooltip: {
          padding: 'var(--tour-spotlight-padding)',
          boxShadow: 'var(--tour-spotlight-shadow)',
        },
        tooltipContent: {
          fontSize: 'var(--tour-body-font-size)',
        },
        tooltipTitle: {
          fontSize: 'var(--tour-title-font-size)',
          fontWeight: 'var(--tour-title-font-weight)',
        },
      }}
    />
  );
}
