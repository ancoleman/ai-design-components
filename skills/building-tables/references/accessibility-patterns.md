# Table Accessibility Patterns

## WCAG 2.1 Requirements

Tables must meet Level AA compliance:
- **Perceivable**: Information must be presentable in different ways
- **Operable**: All functionality available via keyboard
- **Understandable**: Information and UI operation must be understandable
- **Robust**: Content must work with assistive technologies

## Semantic HTML Structure

### Basic Table Structure

Always use semantic HTML elements:

```html
<table>
  <caption>Employee Directory for Q4 2024</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Department</th>
      <th scope="col">Email</th>
      <th scope="col">Start Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Jane Smith</th>
      <td>Engineering</td>
      <td>jane@example.com</td>
      <td>2020-03-15</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="4">Showing 10 of 245 employees</td>
    </tr>
  </tfoot>
</table>
```

### Required Elements

- `<caption>`: Provides table title and context
- `<thead>`: Groups header content
- `<tbody>`: Groups body content
- `<tfoot>`: Groups footer content
- `scope` attribute: Defines header relationships

## ARIA Grid Pattern

For interactive tables, use the grid pattern:

```html
<div role="application" aria-label="Employee data grid">
  <table role="grid" aria-rowcount="245" aria-colcount="4">
    <thead>
      <tr role="row">
        <th role="columnheader" aria-sort="ascending">
          Name
        </th>
        <th role="columnheader" aria-sort="none">
          Department
        </th>
      </tr>
    </thead>
    <tbody>
      <tr role="row" aria-rowindex="1">
        <td role="gridcell" tabindex="0">Jane Smith</td>
        <td role="gridcell" tabindex="-1">Engineering</td>
      </tr>
    </tbody>
  </table>
</div>
```

### ARIA Attributes Explained

- `role="grid"`: Indicates interactive table with keyboard navigation
- `role="columnheader"`: Column header cell
- `role="rowheader"`: Row header cell
- `role="gridcell"`: Data cell in grid
- `aria-sort`: Indicates sort direction (ascending/descending/none/other)
- `aria-rowcount`: Total rows when not all are in DOM
- `aria-colcount`: Total columns when not all are visible
- `aria-rowindex`: Row position in full dataset
- `aria-colindex`: Column position when columns hidden
- `aria-selected`: Selection state for rows/cells
- `aria-readonly`: Indicates non-editable cells
- `aria-invalid`: Marks cells with validation errors
- `aria-describedby`: Links to help text

## Keyboard Navigation

### Essential Keyboard Support

```javascript
const TableKeyboardHandler = ({ onCellFocus, onCellSelect }) => {
  const handleKeyDown = (event) => {
    const { key, shiftKey, ctrlKey } = event;
    const currentCell = document.activeElement;

    switch(key) {
      case 'ArrowRight':
        focusNextCell(currentCell, 'right');
        event.preventDefault();
        break;

      case 'ArrowLeft':
        focusNextCell(currentCell, 'left');
        event.preventDefault();
        break;

      case 'ArrowDown':
        focusNextCell(currentCell, 'down');
        event.preventDefault();
        break;

      case 'ArrowUp':
        focusNextCell(currentCell, 'up');
        event.preventDefault();
        break;

      case 'Home':
        if (ctrlKey) {
          focusFirstCell();
        } else {
          focusFirstCellInRow(currentCell);
        }
        event.preventDefault();
        break;

      case 'End':
        if (ctrlKey) {
          focusLastCell();
        } else {
          focusLastCellInRow(currentCell);
        }
        event.preventDefault();
        break;

      case 'PageDown':
        scrollPageDown();
        event.preventDefault();
        break;

      case 'PageUp':
        scrollPageUp();
        event.preventDefault();
        break;

      case 'Enter':
      case ' ':
        if (currentCell.getAttribute('role') === 'gridcell') {
          enterEditMode(currentCell);
          event.preventDefault();
        }
        break;

      case 'Escape':
        exitEditMode(currentCell);
        event.preventDefault();
        break;

      case 'Tab':
        // Allow normal tab navigation
        break;

      default:
        // Start typing to edit cell
        if (isEditable(currentCell) && key.length === 1) {
          enterEditMode(currentCell, key);
        }
    }
  };

  return { handleKeyDown };
};
```

### Focus Management

```javascript
// Roving tabindex pattern
function RovingTabIndex({ children }) {
  const [focusedIndex, setFocusedIndex] = useState(0);

  return React.Children.map(children, (child, index) => {
    return React.cloneElement(child, {
      tabIndex: index === focusedIndex ? 0 : -1,
      onFocus: () => setFocusedIndex(index),
    });
  });
}

// Focus visible cells only
function manageGridFocus() {
  const cells = document.querySelectorAll('[role="gridcell"]');

  cells.forEach((cell, index) => {
    if (index === 0) {
      cell.setAttribute('tabindex', '0');
    } else {
      cell.setAttribute('tabindex', '-1');
    }
  });
}
```

## Screen Reader Support

### Status Announcements

Use live regions for dynamic updates:

```html
<!-- Announce status changes -->
<div role="status" aria-live="polite" aria-atomic="true">
  <span id="table-status">Sorted by Name, ascending</span>
</div>

<!-- Announce results -->
<div role="status" aria-live="polite">
  <span id="filter-results">Showing 15 of 245 results</span>
</div>

<!-- Announce errors -->
<div role="alert" aria-live="assertive">
  <span id="error-message">Invalid date format in row 5</span>
</div>
```

### Loading States

```javascript
function LoadingTable() {
  return (
    <div role="region" aria-busy="true" aria-label="Loading table data">
      <table>
        <caption>
          <span aria-live="polite">Loading employee data...</span>
        </caption>
        {/* Skeleton or spinner */}
      </table>
    </div>
  );
}
```

### Empty States

```javascript
function EmptyTable() {
  return (
    <div role="region" aria-label="Employee table">
      <table>
        <caption>Employee Directory</caption>
        <tbody>
          <tr>
            <td colspan="4" role="status">
              No employees found matching your criteria.
              Try adjusting your filters.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
```

## Interactive Features

### Sortable Columns

```javascript
function SortableHeader({ column, sortConfig, onSort }) {
  const handleSort = () => {
    onSort(column.id);
  };

  const getSortDirection = () => {
    if (sortConfig.column !== column.id) return 'none';
    return sortConfig.direction;
  };

  return (
    <th
      role="columnheader"
      aria-sort={getSortDirection()}
      onClick={handleSort}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleSort();
        }
      }}
      tabIndex={0}
      style={{ cursor: 'pointer' }}
    >
      <span>{column.label}</span>
      <span aria-hidden="true">
        {getSortDirection() === 'ascending' && ' ↑'}
        {getSortDirection() === 'descending' && ' ↓'}
      </span>
      <span className="sr-only">
        {getSortDirection() === 'none' && 'Click to sort'}
        {getSortDirection() === 'ascending' && 'Sorted ascending. Click to sort descending'}
        {getSortDirection() === 'descending' && 'Sorted descending. Click to remove sort'}
      </span>
    </th>
  );
}
```

### Row Selection

```javascript
function SelectableRow({ row, isSelected, onSelect }) {
  return (
    <tr
      role="row"
      aria-selected={isSelected}
      onClick={() => onSelect(row.id)}
    >
      <td role="gridcell">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={() => onSelect(row.id)}
          aria-label={`Select ${row.name}`}
        />
      </td>
      <td role="gridcell">{row.name}</td>
      <td role="gridcell">{row.email}</td>
    </tr>
  );
}

// Announce selection changes
function announceSelection(count, total) {
  const message = count === 0
    ? 'No rows selected'
    : `${count} of ${total} rows selected`;

  const announcement = document.getElementById('selection-status');
  announcement.textContent = message;
}
```

### Inline Editing

```javascript
function EditableCell({ value, onSave, rowId, columnId }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(value);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const startEdit = () => {
    setIsEditing(true);
    setTimeout(() => inputRef.current?.focus(), 0);
  };

  const saveEdit = () => {
    if (validate(editValue)) {
      onSave(rowId, columnId, editValue);
      setIsEditing(false);
      setError(null);
    } else {
      setError('Invalid value');
    }
  };

  const cancelEdit = () => {
    setEditValue(value);
    setIsEditing(false);
    setError(null);
  };

  if (isEditing) {
    return (
      <td role="gridcell" aria-invalid={!!error}>
        <input
          ref={inputRef}
          type="text"
          value={editValue}
          onChange={(e) => setEditValue(e.target.value)}
          onBlur={saveEdit}
          onKeyDown={(e) => {
            if (e.key === 'Enter') saveEdit();
            if (e.key === 'Escape') cancelEdit();
          }}
          aria-label={`Edit ${columnId} for row ${rowId}`}
          aria-describedby={error ? `error-${rowId}-${columnId}` : undefined}
        />
        {error && (
          <span
            id={`error-${rowId}-${columnId}`}
            role="alert"
            className="error"
          >
            {error}
          </span>
        )}
      </td>
    );
  }

  return (
    <td
      role="gridcell"
      tabIndex={0}
      onClick={startEdit}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === 'F2') {
          e.preventDefault();
          startEdit();
        }
      }}
      aria-label={`${columnId}: ${value}. Press Enter to edit`}
    >
      {value}
    </td>
  );
}
```

## Responsive Accessibility

### Mobile Touch Support

```javascript
function TouchAccessibleTable() {
  const [touchStart, setTouchStart] = useState(null);

  const handleTouchStart = (e) => {
    setTouchStart(e.touches[0].clientX);
  };

  const handleTouchMove = (e) => {
    if (!touchStart) return;

    const touchEnd = e.touches[0].clientX;
    const diff = touchStart - touchEnd;

    if (Math.abs(diff) > 50) {
      // Horizontal swipe detected
      if (diff > 0) {
        // Swiped left - show more columns
        showNextColumns();
      } else {
        // Swiped right - show previous columns
        showPreviousColumns();
      }
      setTouchStart(null);
    }
  };

  return (
    <div
      className="table-container"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      role="region"
      aria-label="Swipe left or right to view more columns"
    >
      <table>{/* Table content */}</table>
    </div>
  );
}
```

### Skip Links

```html
<!-- Allow users to skip complex tables -->
<a href="#after-table" className="skip-link">
  Skip employee table
</a>

<table id="employee-table">
  <!-- Large table content -->
</table>

<div id="after-table">
  <!-- Content after table -->
</div>
```

## Color and Contrast

### High Contrast Support

```css
/* Ensure sufficient contrast ratios */
table {
  color: #212529; /* 7:1 contrast on white */
  background: white;
}

th {
  background: #f8f9fa;
  color: #212529;
  font-weight: 600;
}

/* Support Windows High Contrast Mode */
@media (prefers-contrast: high) {
  table, th, td {
    border: 2px solid;
  }

  th {
    border-bottom: 3px solid;
  }

  tr:hover {
    outline: 2px solid;
  }
}

/* Don't rely on color alone */
.sorted-column {
  background-color: #e9ecef;
  font-weight: 600; /* Additional indicator */
}

.selected-row {
  background-color: #cfe2ff;
  border-left: 4px solid #0d6efd; /* Additional indicator */
}
```

## Testing Checklist

### Keyboard Testing
- [ ] Navigate with Tab key through interactive elements
- [ ] Use arrow keys to move between cells (grid pattern)
- [ ] Home/End keys work as expected
- [ ] Enter/Space activate buttons and links
- [ ] Escape cancels operations
- [ ] All interactive elements are reachable
- [ ] Focus is never lost or trapped

### Screen Reader Testing
- [ ] Table caption is announced
- [ ] Column headers are read with data cells
- [ ] Sort state is announced
- [ ] Selection state is communicated
- [ ] Live regions announce changes
- [ ] Empty and loading states are clear
- [ ] Error messages are announced

### Visual Testing
- [ ] 4.5:1 contrast for normal text
- [ ] 3:1 contrast for large text
- [ ] Focus indicators are visible
- [ ] Information isn't conveyed by color alone
- [ ] Works in high contrast mode
- [ ] Zoom to 200% without horizontal scroll

### Mobile Testing
- [ ] Touch targets are at least 44x44 pixels
- [ ] Swipe gestures have alternatives
- [ ] Pinch-zoom is not disabled
- [ ] Works with screen readers (TalkBack/VoiceOver)

## Tools and Resources

### Automated Testing
- axe DevTools: Browser extension for accessibility testing
- WAVE: Web Accessibility Evaluation Tool
- Pa11y: Command line accessibility testing
- Jest-axe: Automated testing in unit tests

### Manual Testing Tools
- NVDA (Windows): Free screen reader
- JAWS (Windows): Commercial screen reader
- VoiceOver (macOS/iOS): Built-in screen reader
- TalkBack (Android): Built-in screen reader

### References
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices - Data Grid](https://www.w3.org/WAI/ARIA/apg/patterns/grid/)
- [WebAIM Screen Reader Testing](https://webaim.org/articles/screenreader_testing/)