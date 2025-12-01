# Navigation Components

## Table of Contents
- [Breadcrumbs](#breadcrumbs)
- [Tabs](#tabs)
- [Pagination](#pagination)
- [Stepper/Wizard](#stepperwizard)
- [Table of Contents](#table-of-contents-component)
- [Command Palette](#command-palette)

## Breadcrumbs

### Basic Breadcrumb Implementation

```tsx
interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
  separator?: React.ReactNode;
}

const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  items,
  separator = '/'
}) => {
  return (
    <nav aria-label="Breadcrumb" className="breadcrumbs">
      <ol itemScope itemType="https://schema.org/BreadcrumbList">
        {items.map((item, index) => {
          const isLast = index === items.length - 1;

          return (
            <li
              key={index}
              itemProp="itemListElement"
              itemScope
              itemType="https://schema.org/ListItem"
              className="breadcrumb-item"
            >
              {isLast ? (
                <span
                  itemProp="name"
                  aria-current="page"
                  className="current"
                >
                  {item.label}
                </span>
              ) : (
                <>
                  <a
                    href={item.href}
                    itemProp="item"
                  >
                    <span itemProp="name">{item.label}</span>
                  </a>
                  <span
                    className="separator"
                    aria-hidden="true"
                  >
                    {separator}
                  </span>
                </>
              )}
              <meta itemProp="position" content={String(index + 1)} />
            </li>
          );
        })}
      </ol>
    </nav>
  );
};
```

### Dynamic Breadcrumbs with React Router

```tsx
import { useMatches } from 'react-router-dom';

interface RouteHandle {
  breadcrumb?: (data?: any) => BreadcrumbItem;
}

const useBreadcrumbs = (): BreadcrumbItem[] => {
  const matches = useMatches();

  const breadcrumbs = matches
    .filter(match => (match.handle as RouteHandle)?.breadcrumb)
    .map(match => {
      const handle = match.handle as RouteHandle;
      return handle.breadcrumb!(match.data);
    });

  return [
    { label: 'Home', href: '/' },
    ...breadcrumbs
  ];
};

// Usage in routes
const routes = [
  {
    path: '/products',
    element: <Products />,
    handle: {
      breadcrumb: () => ({ label: 'Products', href: '/products' })
    }
  },
  {
    path: '/products/:id',
    element: <ProductDetail />,
    loader: async ({ params }) => {
      const product = await fetchProduct(params.id);
      return { product };
    },
    handle: {
      breadcrumb: (data) => ({
        label: data?.product?.name || 'Product',
        href: `/products/${data?.product?.id}`
      })
    }
  }
];
```

### Collapsible Breadcrumbs for Long Paths

```tsx
const CollapsibleBreadcrumbs: React.FC<{ items: BreadcrumbItem[] }> = ({
  items
}) => {
  const [expanded, setExpanded] = useState(false);
  const maxVisible = 3;

  if (items.length <= maxVisible) {
    return <Breadcrumbs items={items} />;
  }

  const visibleItems = expanded
    ? items
    : [
        items[0],
        { label: '...', href: undefined },
        ...items.slice(-2)
      ];

  return (
    <nav aria-label="Breadcrumb" className="breadcrumbs collapsible">
      <ol>
        {visibleItems.map((item, index) => (
          <li key={index}>
            {item.label === '...' ? (
              <button
                onClick={() => setExpanded(true)}
                aria-label={`Show ${items.length - maxVisible} more items`}
                className="expand-button"
              >
                ...
              </button>
            ) : item.href ? (
              <a href={item.href}>{item.label}</a>
            ) : (
              <span aria-current="page">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};
```

## Tabs

### Basic Tabs with URL Sync

```tsx
interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  urlParam?: string;
}

const Tabs: React.FC<TabsProps> = ({
  tabs,
  defaultTab,
  urlParam = 'tab'
}) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get(urlParam) || defaultTab || tabs[0].id;

  const handleTabChange = (tabId: string) => {
    setSearchParams(prev => {
      prev.set(urlParam, tabId);
      return prev;
    });
  };

  return (
    <div className="tabs">
      <div
        role="tablist"
        aria-label="Tabs"
        className="tab-list"
      >
        {tabs.map(tab => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            aria-controls={`panel-${tab.id}`}
            tabIndex={activeTab === tab.id ? 0 : -1}
            onClick={() => handleTabChange(tab.id)}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          >
            {tab.icon}
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {tabs.map(tab => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== tab.id}
          tabIndex={0}
          className="tab-panel"
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
};
```

### Scrollable Tabs

```tsx
const ScrollableTabs: React.FC<TabsProps> = ({ tabs }) => {
  const [activeTab, setActiveTab] = useState(tabs[0].id);
  const tabListRef = useRef<HTMLDivElement>(null);
  const [showLeftScroll, setShowLeftScroll] = useState(false);
  const [showRightScroll, setShowRightScroll] = useState(false);

  const checkScroll = () => {
    if (!tabListRef.current) return;

    const { scrollLeft, scrollWidth, clientWidth } = tabListRef.current;
    setShowLeftScroll(scrollLeft > 0);
    setShowRightScroll(scrollLeft < scrollWidth - clientWidth);
  };

  useEffect(() => {
    checkScroll();
    window.addEventListener('resize', checkScroll);
    return () => window.removeEventListener('resize', checkScroll);
  }, [tabs]);

  const scroll = (direction: 'left' | 'right') => {
    if (!tabListRef.current) return;

    const scrollAmount = 200;
    tabListRef.current.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    });

    setTimeout(checkScroll, 300);
  };

  return (
    <div className="scrollable-tabs">
      {showLeftScroll && (
        <button
          className="scroll-button left"
          onClick={() => scroll('left')}
          aria-label="Scroll tabs left"
        >
          <ChevronLeft />
        </button>
      )}

      <div
        ref={tabListRef}
        role="tablist"
        className="tab-list-scroll"
        onScroll={checkScroll}
      >
        {tabs.map(tab => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={activeTab === tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {showRightScroll && (
        <button
          className="scroll-button right"
          onClick={() => scroll('right')}
          aria-label="Scroll tabs right"
        >
          <ChevronRight />
        </button>
      )}
    </div>
  );
};
```

## Pagination

### Accessible Pagination Component

```tsx
interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  siblingCount?: number;
  boundaryCount?: number;
}

const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  siblingCount = 1,
  boundaryCount = 1
}) => {
  // Generate page numbers with ellipsis
  const range = (start: number, end: number) => {
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  };

  const generatePages = (): (number | string)[] => {
    const totalNumbers = siblingCount * 2 + 3 + boundaryCount * 2;

    if (totalNumbers >= totalPages) {
      return range(1, totalPages);
    }

    const leftSiblingIndex = Math.max(currentPage - siblingCount, 1);
    const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages);

    const shouldShowLeftDots = leftSiblingIndex > boundaryCount + 2;
    const shouldShowRightDots = rightSiblingIndex < totalPages - boundaryCount - 1;

    if (!shouldShowLeftDots && shouldShowRightDots) {
      const leftRange = range(1, 3 + siblingCount * 2);
      return [...leftRange, '...', ...range(totalPages - boundaryCount + 1, totalPages)];
    }

    if (shouldShowLeftDots && !shouldShowRightDots) {
      const rightRange = range(totalPages - (3 + siblingCount * 2) + 1, totalPages);
      return [...range(1, boundaryCount), '...', ...rightRange];
    }

    return [
      ...range(1, boundaryCount),
      '...',
      ...range(leftSiblingIndex, rightSiblingIndex),
      '...',
      ...range(totalPages - boundaryCount + 1, totalPages)
    ];
  };

  const pages = generatePages();

  return (
    <nav
      role="navigation"
      aria-label="Pagination Navigation"
      className="pagination"
    >
      <ul className="pagination-list">
        <li>
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
            aria-label="Go to previous page"
            className="pagination-prev"
          >
            Previous
          </button>
        </li>

        {pages.map((page, index) => {
          if (page === '...') {
            return (
              <li key={`ellipsis-${index}`} className="pagination-ellipsis">
                <span aria-hidden="true">...</span>
              </li>
            );
          }

          const pageNumber = page as number;
          return (
            <li key={pageNumber}>
              <button
                onClick={() => onPageChange(pageNumber)}
                aria-label={`Go to page ${pageNumber}`}
                aria-current={currentPage === pageNumber ? 'page' : undefined}
                className={`pagination-button ${
                  currentPage === pageNumber ? 'active' : ''
                }`}
              >
                {pageNumber}
              </button>
            </li>
          );
        })}

        <li>
          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            aria-label="Go to next page"
            className="pagination-next"
          >
            Next
          </button>
        </li>
      </ul>
    </nav>
  );
};
```

### Simple Pagination

```tsx
const SimplePagination: React.FC<{
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}> = ({ currentPage, totalPages, onPageChange }) => {
  return (
    <div className="simple-pagination">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Previous page"
      >
        <ChevronLeft /> Previous
      </button>

      <span className="page-info">
        Page <strong>{currentPage}</strong> of <strong>{totalPages}</strong>
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Next page"
      >
        Next <ChevronRight />
      </button>
    </div>
  );
};
```

## Stepper/Wizard

### Multi-Step Form Navigation

```tsx
interface Step {
  id: string;
  label: string;
  description?: string;
  content: React.ReactNode;
  validation?: () => boolean;
}

interface StepperProps {
  steps: Step[];
  onComplete: () => void;
}

const Stepper: React.FC<StepperProps> = ({ steps, onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  const canProceed = () => {
    const step = steps[currentStep];
    return !step.validation || step.validation();
  };

  const handleNext = () => {
    if (canProceed()) {
      setCompletedSteps(prev => new Set(prev).add(currentStep));

      if (currentStep === steps.length - 1) {
        onComplete();
      } else {
        setCurrentStep(currentStep + 1);
      }
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleStepClick = (index: number) => {
    // Allow navigation to completed steps or previous steps
    if (completedSteps.has(index) || index < currentStep) {
      setCurrentStep(index);
    }
  };

  return (
    <div className="stepper">
      {/* Progress indicator */}
      <nav aria-label="Progress">
        <ol className="stepper-nav">
          {steps.map((step, index) => {
            const isActive = index === currentStep;
            const isCompleted = completedSteps.has(index);
            const isClickable = isCompleted || index < currentStep;

            return (
              <li
                key={step.id}
                className={`stepper-item ${isActive ? 'active' : ''} ${
                  isCompleted ? 'completed' : ''
                }`}
              >
                {isClickable ? (
                  <button
                    onClick={() => handleStepClick(index)}
                    aria-current={isActive ? 'step' : undefined}
                    aria-label={`${step.label}${
                      isCompleted ? ' (completed)' : ''
                    }`}
                  >
                    <span className="step-indicator">
                      {isCompleted ? '✓' : index + 1}
                    </span>
                    <span className="step-label">{step.label}</span>
                  </button>
                ) : (
                  <div aria-current={isActive ? 'step' : undefined}>
                    <span className="step-indicator">{index + 1}</span>
                    <span className="step-label">{step.label}</span>
                  </div>
                )}
              </li>
            );
          })}
        </ol>
      </nav>

      {/* Step content */}
      <div className="stepper-content">
        <div
          role="region"
          aria-label={`Step ${currentStep + 1}: ${steps[currentStep].label}`}
        >
          <h2>{steps[currentStep].label}</h2>
          {steps[currentStep].description && (
            <p className="step-description">{steps[currentStep].description}</p>
          )}

          {steps[currentStep].content}
        </div>
      </div>

      {/* Navigation buttons */}
      <div className="stepper-actions">
        <button
          onClick={handlePrevious}
          disabled={currentStep === 0}
          className="btn-secondary"
        >
          Previous
        </button>

        <span className="step-counter">
          Step {currentStep + 1} of {steps.length}
        </span>

        <button
          onClick={handleNext}
          disabled={!canProceed()}
          className="btn-primary"
        >
          {currentStep === steps.length - 1 ? 'Complete' : 'Next'}
        </button>
      </div>
    </div>
  );
};
```

## Table of Contents Component

### Auto-Generated TOC with Scroll Spy

```tsx
interface TOCItem {
  id: string;
  title: string;
  level: number;
  children?: TOCItem[];
}

const TableOfContents: React.FC = () => {
  const [tocItems, setTocItems] = useState<TOCItem[]>([]);
  const [activeId, setActiveId] = useState<string>('');

  useEffect(() => {
    // Generate TOC from headings
    const headings = document.querySelectorAll('h2, h3, h4');
    const items: TOCItem[] = [];
    const stack: TOCItem[] = [];

    headings.forEach(heading => {
      const id = heading.id || heading.textContent?.toLowerCase().replace(/\s+/g, '-');
      if (!heading.id) heading.id = id!;

      const level = parseInt(heading.tagName[1]);
      const item: TOCItem = {
        id: id!,
        title: heading.textContent || '',
        level
      };

      // Build hierarchy
      while (stack.length > 0 && stack[stack.length - 1].level >= level) {
        stack.pop();
      }

      if (stack.length === 0) {
        items.push(item);
      } else {
        const parent = stack[stack.length - 1];
        if (!parent.children) parent.children = [];
        parent.children.push(item);
      }

      stack.push(item);
    });

    setTocItems(items);
  }, []);

  useEffect(() => {
    // Scroll spy
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      {
        rootMargin: '-20% 0% -70% 0%'
      }
    );

    const headings = document.querySelectorAll('h2, h3, h4');
    headings.forEach(heading => observer.observe(heading));

    return () => {
      headings.forEach(heading => observer.unobserve(heading));
    };
  }, []);

  const renderTOCItems = (items: TOCItem[]) => {
    return (
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <a
              href={`#${item.id}`}
              className={activeId === item.id ? 'active' : ''}
              onClick={(e) => {
                e.preventDefault();
                document.getElementById(item.id)?.scrollIntoView({
                  behavior: 'smooth'
                });
              }}
            >
              {item.title}
            </a>
            {item.children && renderTOCItems(item.children)}
          </li>
        ))}
      </ul>
    );
  };

  return (
    <nav className="table-of-contents" aria-label="Table of contents">
      <h2>On this page</h2>
      {renderTOCItems(tocItems)}
    </nav>
  );
};
```

## Command Palette

### Keyboard-Driven Navigation

```tsx
interface Command {
  id: string;
  label: string;
  shortcut?: string;
  icon?: React.ReactNode;
  action: () => void;
  category?: string;
}

const CommandPalette: React.FC<{ commands: Command[] }> = ({ commands }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  // Open with Cmd+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Focus input when opened
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Filter commands
  const filteredCommands = commands.filter(cmd =>
    cmd.label.toLowerCase().includes(search.toLowerCase()) ||
    cmd.category?.toLowerCase().includes(search.toLowerCase())
  );

  // Group by category
  const groupedCommands = filteredCommands.reduce((acc, cmd) => {
    const category = cmd.category || 'General';
    if (!acc[category]) acc[category] = [];
    acc[category].push(cmd);
    return acc;
  }, {} as Record<string, Command[]>);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev =>
          Math.min(prev + 1, filteredCommands.length - 1)
        );
        break;

      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => Math.max(prev - 1, 0));
        break;

      case 'Enter':
        e.preventDefault();
        if (filteredCommands[selectedIndex]) {
          filteredCommands[selectedIndex].action();
          setIsOpen(false);
        }
        break;

      case 'Escape':
        setIsOpen(false);
        break;
    }
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="command-backdrop"
        onClick={() => setIsOpen(false)}
        aria-hidden="true"
      />

      {/* Command Palette */}
      <div
        className="command-palette"
        role="dialog"
        aria-label="Command palette"
      >
        <div className="command-input-wrapper">
          <SearchIcon />
          <input
            ref={inputRef}
            type="text"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setSelectedIndex(0);
            }}
            onKeyDown={handleKeyDown}
            placeholder="Type a command or search..."
            className="command-input"
            role="combobox"
            aria-expanded="true"
            aria-controls="command-list"
            aria-activedescendant={`command-${filteredCommands[selectedIndex]?.id}`}
          />
        </div>

        <div id="command-list" role="listbox" className="command-list">
          {Object.entries(groupedCommands).map(([category, cmds]) => (
            <div key={category} className="command-category">
              <div className="command-category-title">{category}</div>
              {cmds.map((cmd, idx) => {
                const globalIndex = filteredCommands.indexOf(cmd);
                const isSelected = globalIndex === selectedIndex;

                return (
                  <button
                    key={cmd.id}
                    id={`command-${cmd.id}`}
                    role="option"
                    aria-selected={isSelected}
                    className={`command-item ${isSelected ? 'selected' : ''}`}
                    onClick={() => {
                      cmd.action();
                      setIsOpen(false);
                    }}
                    onMouseEnter={() => setSelectedIndex(globalIndex)}
                  >
                    <span className="command-item-content">
                      {cmd.icon}
                      <span>{cmd.label}</span>
                    </span>
                    {cmd.shortcut && (
                      <kbd className="command-shortcut">{cmd.shortcut}</kbd>
                    )}
                  </button>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    </>
  );
};
```

### CSS for Navigation Components

```css
/* Breadcrumbs */
.breadcrumbs ol {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--breadcrumb-gap);
  list-style: none;
  padding: 0;
  margin: 0;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
}

.breadcrumbs a {
  color: var(--nav-item-color);
  text-decoration: none;
  transition: color 200ms;
}

.breadcrumbs a:hover {
  color: var(--nav-item-hover-color);
  text-decoration: underline;
}

.breadcrumbs .current {
  color: var(--nav-item-active-color);
  font-weight: 500;
}

.breadcrumbs .separator {
  color: var(--breadcrumb-separator-color);
  margin: 0 var(--breadcrumb-gap);
}

/* Tabs */
.tab-list {
  display: flex;
  gap: var(--spacing-xs);
  border-bottom: 1px solid var(--tab-border-color);
  overflow-x: auto;
  scrollbar-width: thin;
}

.tab-button {
  padding: var(--spacing-sm) var(--spacing-md);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--nav-item-color);
  cursor: pointer;
  transition: all 200ms;
  white-space: nowrap;
}

.tab-button:hover {
  background: var(--tab-hover-bg);
}

.tab-button.active {
  color: var(--nav-item-active-color);
  border-bottom-color: var(--tab-active-border-color);
  font-weight: 500;
}

.tab-panel {
  padding: var(--spacing-md);
  animation: fadeIn 200ms;
}

/* Pagination */
.pagination-list {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  list-style: none;
}

.pagination-button {
  min-width: 40px;
  height: 40px;
  padding: var(--spacing-xs) var(--spacing-sm);
  border: 1px solid var(--nav-border-color);
  background: var(--nav-bg);
  border-radius: var(--nav-item-border-radius);
  color: var(--nav-item-color);
  cursor: pointer;
  transition: all 200ms;
}

.pagination-button:hover:not(:disabled) {
  background: var(--nav-item-hover-bg);
  border-color: var(--color-primary);
}

.pagination-button.active {
  background: var(--nav-item-active-bg);
  color: var(--nav-item-active-color);
  border-color: var(--color-primary);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Stepper */
.stepper-nav {
  display: flex;
  justify-content: space-between;
  counter-reset: step;
  margin-bottom: var(--spacing-lg);
}

.stepper-item {
  flex: 1;
  position: relative;
  text-align: center;
}

.stepper-item:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 20px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: var(--nav-border-color);
  z-index: -1;
}

.stepper-item.completed::after {
  background: var(--color-success);
}

.step-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 2px solid var(--nav-border-color);
  border-radius: 50%;
  background: var(--nav-bg);
  margin-bottom: var(--spacing-xs);
}

.stepper-item.active .step-indicator {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.stepper-item.completed .step-indicator {
  background: var(--color-success);
  color: white;
  border-color: var(--color-success);
}
```