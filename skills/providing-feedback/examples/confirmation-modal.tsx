import React, { useState, useRef, useEffect } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Transition } from '@headlessui/react';

/**
 * Confirmation Modal Implementation Examples
 *
 * Demonstrates deletion confirmations and other critical actions
 * using both Radix UI and Headless UI
 */

// Radix UI Confirmation Modal
export function RadixConfirmationModal() {
  const [itemToDelete, setItemToDelete] = useState(null);

  const handleDelete = async () => {
    if (!itemToDelete) return;

    try {
      // Perform deletion
      await deleteItem(itemToDelete.id);
      toast.success(`${itemToDelete.name} deleted successfully`);
      setItemToDelete(null);
    } catch (error) {
      toast.error('Failed to delete item');
    }
  };

  return (
    <Dialog.Root open={!!itemToDelete} onOpenChange={(open) => !open && setItemToDelete(null)}>
      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />

        <Dialog.Content className="modal-content">
          <Dialog.Title className="modal-title">
            Confirm Deletion
          </Dialog.Title>

          <Dialog.Description className="modal-description">
            Are you sure you want to delete "{itemToDelete?.name}"?
            This action cannot be undone.
          </Dialog.Description>

          <div className="modal-actions">
            <Dialog.Close asChild>
              <button className="btn-secondary">
                Cancel
              </button>
            </Dialog.Close>

            <button
              onClick={handleDelete}
              className="btn-danger"
              autoFocus
            >
              Delete
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

// Headless UI Confirmation Modal
export function HeadlessConfirmationModal({ isOpen, onClose, onConfirm, item }) {
  const [isDeleting, setIsDeleting] = useState(false);
  const cancelButtonRef = useRef(null);

  const handleConfirm = async () => {
    setIsDeleting(true);
    try {
      await onConfirm();
      onClose();
    } catch (error) {
      console.error('Deletion failed:', error);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <Transition.Root show={isOpen} as={React.Fragment}>
      <Dialog
        as="div"
        className="relative z-50"
        initialFocus={cancelButtonRef}
        onClose={onClose}
      >
        <Transition.Child
          as={React.Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-50 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={React.Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                      <ExclamationTriangleIcon
                        className="h-6 w-6 text-red-600"
                        aria-hidden="true"
                      />
                    </div>
                    <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                      <Dialog.Title
                        as="h3"
                        className="text-base font-semibold leading-6 text-gray-900"
                      >
                        Delete {item?.type || 'item'}
                      </Dialog.Title>
                      <div className="mt-2">
                        <p className="text-sm text-gray-500">
                          Are you sure you want to delete "{item?.name}"?
                          All of the data will be permanently removed.
                          This action cannot be undone.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                  <button
                    type="button"
                    className="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto"
                    onClick={handleConfirm}
                    disabled={isDeleting}
                  >
                    {isDeleting ? 'Deleting...' : 'Delete'}
                  </button>
                  <button
                    type="button"
                    className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
                    onClick={onClose}
                    ref={cancelButtonRef}
                    disabled={isDeleting}
                  >
                    Cancel
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}

// Custom Confirmation Modal with Focus Management
export function CustomConfirmationModal({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  message = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  type = 'warning' // 'warning', 'danger', 'info'
}) {
  const modalRef = useRef(null);
  const previousFocusRef = useRef(null);
  const confirmButtonRef = useRef(null);

  // Focus management
  useEffect(() => {
    if (isOpen) {
      // Save current focus
      previousFocusRef.current = document.activeElement;

      // Focus confirm button (most dangerous action)
      setTimeout(() => {
        confirmButtonRef.current?.focus();
      }, 0);

      // Add ESC key handler
      const handleEscape = (e) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };
      document.addEventListener('keydown', handleEscape);

      return () => {
        document.removeEventListener('keydown', handleEscape);
      };
    } else {
      // Restore focus when closing
      previousFocusRef.current?.focus();
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const getIconForType = () => {
    switch (type) {
      case 'danger':
        return '⚠️';
      case 'warning':
        return '⚠';
      case 'info':
        return 'ℹ';
      default:
        return '?';
    }
  };

  const getColorForType = () => {
    switch (type) {
      case 'danger':
        return 'red';
      case 'warning':
        return 'yellow';
      case 'info':
        return 'blue';
      default:
        return 'gray';
    }
  };

  return (
    <div
      className="modal-root"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-describedby="modal-description"
      ref={modalRef}
    >
      <div
        className="modal-backdrop"
        onClick={onClose}
        aria-hidden="true"
      />

      <div className="modal-container">
        <div className={`modal-icon modal-icon-${type}`}>
          {getIconForType()}
        </div>

        <h2 id="modal-title" className="modal-title">
          {title}
        </h2>

        <p id="modal-description" className="modal-description">
          {message}
        </p>

        <div className="modal-actions">
          <button
            onClick={onClose}
            className="btn-secondary"
          >
            {cancelText}
          </button>

          <button
            ref={confirmButtonRef}
            onClick={onConfirm}
            className={`btn-primary btn-${type}`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

// Unsaved Changes Confirmation
export function UnsavedChangesModal({ isOpen, onClose, onDiscard, onSave }) {
  return (
    <Dialog.Root open={isOpen} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />

        <Dialog.Content className="modal-content">
          <Dialog.Title>Unsaved Changes</Dialog.Title>

          <Dialog.Description>
            You have unsaved changes. What would you like to do?
          </Dialog.Description>

          <div className="modal-actions-three">
            <Dialog.Close asChild>
              <button className="btn-secondary">
                Cancel
              </button>
            </Dialog.Close>

            <button
              onClick={onDiscard}
              className="btn-danger-outline"
            >
              Discard Changes
            </button>

            <button
              onClick={onSave}
              className="btn-primary"
              autoFocus
            >
              Save Changes
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

// Bulk Action Confirmation
export function BulkActionModal({ isOpen, onClose, onConfirm, selectedItems, action }) {
  const itemCount = selectedItems?.length || 0;
  const itemLabel = itemCount === 1 ? 'item' : 'items';

  const getActionMessage = () => {
    switch (action) {
      case 'delete':
        return `permanently delete ${itemCount} ${itemLabel}`;
      case 'archive':
        return `archive ${itemCount} ${itemLabel}`;
      case 'export':
        return `export ${itemCount} ${itemLabel}`;
      default:
        return `perform this action on ${itemCount} ${itemLabel}`;
    }
  };

  return (
    <Dialog.Root open={isOpen} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />

        <Dialog.Content className="modal-content">
          <Dialog.Title>Confirm Bulk Action</Dialog.Title>

          <Dialog.Description>
            You are about to {getActionMessage()}.
          </Dialog.Description>

          {itemCount > 5 && (
            <div className="modal-warning">
              <InfoIcon />
              <span>This is a large number of items and may take some time.</span>
            </div>
          )}

          <div className="selected-items-preview">
            <h4>Selected Items:</h4>
            <ul className="item-list">
              {selectedItems?.slice(0, 5).map(item => (
                <li key={item.id}>{item.name}</li>
              ))}
              {itemCount > 5 && (
                <li className="more-items">...and {itemCount - 5} more</li>
              )}
            </ul>
          </div>

          <div className="modal-actions">
            <Dialog.Close asChild>
              <button className="btn-secondary">
                Cancel
              </button>
            </Dialog.Close>

            <button
              onClick={() => onConfirm(selectedItems)}
              className={`btn-primary ${action === 'delete' ? 'btn-danger' : ''}`}
            >
              {action === 'delete' ? 'Delete All' : 'Confirm'}
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

// Styles for confirmation modals
const styles = `
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    animation: overlay-fade-in 200ms ease-out;
  }

  .modal-content {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 8px;
    padding: 24px;
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    animation: modal-enter 200ms ease-out;
  }

  .modal-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .modal-description {
    color: #6b7280;
    margin-bottom: 24px;
    line-height: 1.5;
  }

  .modal-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }

  .modal-actions-three {
    display: flex;
    gap: 12px;
    justify-content: space-between;
  }

  .btn-danger {
    background: #ef4444;
    color: white;
  }

  .btn-danger:hover {
    background: #dc2626;
  }

  .btn-danger-outline {
    border: 1px solid #ef4444;
    color: #ef4444;
  }

  .modal-warning {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
    background: #fef3c7;
    border: 1px solid #fbbf24;
    border-radius: 6px;
    margin-bottom: 16px;
    color: #92400e;
  }

  .selected-items-preview {
    background: #f9fafb;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 24px;
  }

  .item-list {
    list-style: none;
    padding: 0;
    margin: 8px 0 0 0;
  }

  .item-list li {
    padding: 4px 0;
    color: #4b5563;
  }

  .more-items {
    font-style: italic;
    color: #9ca3af;
  }

  @keyframes overlay-fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes modal-enter {
    from {
      opacity: 0;
      transform: translate(-50%, -48%) scale(0.96);
    }
    to {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .modal-overlay,
    .modal-content {
      animation: none;
    }
  }
`;