import React from 'react';
import { Toaster, toast } from 'sonner';

/**
 * Success Toast Implementation Example
 *
 * Demonstrates various success notification patterns using Sonner
 */

// Basic App Setup with Toaster
export function App() {
  return (
    <>
      {/* Configure global toaster */}
      <Toaster
        position="bottom-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'var(--toast-bg)',
            color: 'var(--toast-text)',
            border: '1px solid var(--toast-border)'
          }
        }}
      />

      {/* Your application components */}
      <SuccessExamples />
    </>
  );
}

// Success Toast Examples
export function SuccessExamples() {
  // Simple success notification
  const handleSimpleSuccess = () => {
    toast.success('Changes saved successfully');
  };

  // Success with description
  const handleDetailedSuccess = () => {
    toast.success('Profile Updated', {
      description: 'Your profile information has been saved',
      duration: 5000
    });
  };

  // Success with custom icon
  const handleCustomIconSuccess = () => {
    toast('Upload Complete', {
      icon: '📁',
      description: '5 files uploaded successfully'
    });
  };

  // Success with action button
  const handleSuccessWithAction = () => {
    toast.success('Item created successfully', {
      action: {
        label: 'View',
        onClick: () => console.log('Viewing item')
      },
      duration: 10000 // Longer duration for action
    });
  };

  // Success with undo action
  const handleSuccessWithUndo = () => {
    let deletedItem = { id: 1, name: 'Important Document' };

    toast.success('Item deleted', {
      description: deletedItem.name,
      action: {
        label: 'Undo',
        onClick: () => {
          // Restore the item
          console.log('Restoring item:', deletedItem);
          toast.success('Item restored');
        }
      },
      duration: 10000
    });
  };

  // Promise-based success (async operation)
  const handleAsyncOperation = async () => {
    const saveData = () => new Promise((resolve) => {
      setTimeout(() => resolve({ id: 1, name: 'Document' }), 2000);
    });

    toast.promise(saveData(), {
      loading: 'Saving document...',
      success: (data) => ({
        title: 'Document saved',
        description: `${data.name} has been saved successfully`
      }),
      error: 'Failed to save document'
    });
  };

  // Batch success notifications
  const handleBatchSuccess = () => {
    const items = ['File1.pdf', 'File2.doc', 'File3.png'];

    items.forEach((item, index) => {
      setTimeout(() => {
        toast.success(`${item} uploaded`, {
          id: `upload-${index}` // Prevent duplicates
        });
      }, index * 200); // Stagger notifications
    });
  };

  // Custom styled success
  const handleCustomStyledSuccess = () => {
    toast.custom((t) => (
      <div
        className={`
          ${t.visible ? 'animate-enter' : 'animate-leave'}
          max-w-md w-full bg-white shadow-lg rounded-lg pointer-events-auto
          flex ring-1 ring-black ring-opacity-5
        `}
      >
        <div className="flex-1 w-0 p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0 pt-0.5">
              <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
            <div className="ml-3 flex-1">
              <p className="text-sm font-medium text-gray-900">
                Successfully saved!
              </p>
              <p className="mt-1 text-sm text-gray-500">
                Your changes have been saved to the cloud
              </p>
            </div>
          </div>
        </div>
        <div className="flex border-l border-gray-200">
          <button
            onClick={() => toast.dismiss(t.id)}
            className="w-full border border-transparent rounded-none rounded-r-lg p-4 flex items-center justify-center text-sm font-medium text-indigo-600 hover:text-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            Close
          </button>
        </div>
      </div>
    ));
  };

  // Success with progress update
  const handleProgressSuccess = () => {
    const toastId = toast.loading('Processing files...');

    // Simulate progress updates
    setTimeout(() => {
      toast.loading('Processing files... 25%', { id: toastId });
    }, 1000);

    setTimeout(() => {
      toast.loading('Processing files... 75%', { id: toastId });
    }, 2000);

    setTimeout(() => {
      toast.success('All files processed successfully!', { id: toastId });
    }, 3000);
  };

  return (
    <div className="p-8 space-y-4">
      <h2 className="text-2xl font-bold mb-6">Success Toast Examples</h2>

      <div className="grid grid-cols-2 gap-4">
        <button
          onClick={handleSimpleSuccess}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Simple Success
        </button>

        <button
          onClick={handleDetailedSuccess}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Detailed Success
        </button>

        <button
          onClick={handleCustomIconSuccess}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Custom Icon Success
        </button>

        <button
          onClick={handleSuccessWithAction}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Success with Action
        </button>

        <button
          onClick={handleSuccessWithUndo}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Success with Undo
        </button>

        <button
          onClick={handleAsyncOperation}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Async Operation
        </button>

        <button
          onClick={handleBatchSuccess}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Batch Success
        </button>

        <button
          onClick={handleCustomStyledSuccess}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Custom Styled
        </button>

        <button
          onClick={handleProgressSuccess}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Progress Success
        </button>
      </div>
    </div>
  );
}

// Alternative implementation with react-hot-toast
export function ReactHotToastExample() {
  import toast, { Toaster } from 'react-hot-toast';

  const handleSuccess = () => {
    toast.success('Operation successful!', {
      duration: 4000,
      position: 'bottom-right',
      style: {
        background: '#10b981',
        color: '#fff',
      },
      icon: '✅',
    });
  };

  const handlePromise = () => {
    const myPromise = fetch('/api/data');

    toast.promise(
      myPromise,
      {
        loading: 'Loading...',
        success: 'Got the data!',
        error: 'Error when fetching',
      }
    );
  };

  return (
    <>
      <Toaster />
      <button onClick={handleSuccess}>Show Success</button>
      <button onClick={handlePromise}>Promise Toast</button>
    </>
  );
}

// Success toast with accessibility
export function AccessibleSuccessToast({ message, onAction }) {
  const showAccessibleToast = () => {
    // Create custom toast with proper ARIA attributes
    toast.custom((t) => (
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="toast-success"
      >
        <div className="toast-content">
          <span className="sr-only">Success:</span>
          <span className="toast-icon" aria-hidden="true">✓</span>
          <span className="toast-message">{message}</span>
        </div>
        {onAction && (
          <button
            onClick={() => {
              onAction();
              toast.dismiss(t.id);
            }}
            className="toast-action"
            aria-label="View details"
          >
            View
          </button>
        )}
      </div>
    ));
  };

  return (
    <button onClick={showAccessibleToast}>
      Show Accessible Success
    </button>
  );
}

// Styled components for success toasts
const styles = `
  .toast-success {
    background: var(--color-success-bg, #10b981);
    color: var(--color-success-text, white);
    padding: var(--spacing-md, 16px);
    border-radius: var(--radius-md, 8px);
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 300px;
    max-width: 500px;
  }

  .toast-icon {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
  }

  .toast-message {
    flex: 1;
  }

  .toast-action {
    padding: 4px 12px;
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    color: white;
    font-size: 14px;
    cursor: pointer;
    transition: background 0.2s;
  }

  .toast-action:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  @keyframes animate-enter {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  @keyframes animate-leave {
    from {
      opacity: 1;
      transform: translateX(0);
    }
    to {
      opacity: 0;
      transform: translateX(100%);
    }
  }

  .animate-enter {
    animation: animate-enter 0.3s ease-out;
  }

  .animate-leave {
    animation: animate-leave 0.2s ease-in forwards;
  }
`;