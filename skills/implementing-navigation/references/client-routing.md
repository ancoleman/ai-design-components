# Client-Side Routing Patterns

## Table of Contents
- [React Router v6](#react-router-v6)
- [Next.js App Router](#nextjs-app-router)
- [Route Guards & Protection](#route-guards--protection)
- [Navigation State Management](#navigation-state-management)
- [Deep Linking & URL State](#deep-linking--url-state)

## React Router v6

### Basic Route Setup

```tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

// Define routes with type safety
const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorBoundary />,
    children: [
      {
        index: true,
        element: <HomePage />
      },
      {
        path: 'products',
        element: <ProductsLayout />,
        children: [
          {
            index: true,
            element: <ProductList />
          },
          {
            path: ':productId',
            element: <ProductDetail />,
            loader: productLoader
          }
        ]
      },
      {
        path: 'dashboard/*',
        element: <DashboardLayout />,
        children: [
          {
            path: 'analytics',
            element: <Analytics />
          },
          {
            path: 'settings',
            element: <Settings />
          }
        ]
      }
    ]
  }
]);

function App() {
  return <RouterProvider router={router} />;
}
```

### Nested Routes with Outlets

```tsx
import { Outlet, NavLink } from 'react-router-dom';

const RootLayout: React.FC = () => {
  return (
    <div className="app-layout">
      <header>
        <nav>
          <NavLink
            to="/"
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Home
          </NavLink>
          <NavLink
            to="/products"
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Products
          </NavLink>
          <NavLink
            to="/dashboard"
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Dashboard
          </NavLink>
        </nav>
      </header>

      <main>
        <Outlet /> {/* Child routes render here */}
      </main>

      <footer>
        <p>© 2025 Company</p>
      </footer>
    </div>
  );
};

const DashboardLayout: React.FC = () => {
  return (
    <div className="dashboard-layout">
      <aside className="dashboard-sidebar">
        <nav>
          <NavLink to="/dashboard/analytics">Analytics</NavLink>
          <NavLink to="/dashboard/settings">Settings</NavLink>
        </nav>
      </aside>

      <div className="dashboard-content">
        <Outlet /> {/* Nested dashboard routes render here */}
      </div>
    </div>
  );
};
```

### Data Loading with Loaders

```tsx
import { LoaderFunctionArgs, defer, Await } from 'react-router-dom';

// Type-safe loader
interface Product {
  id: string;
  name: string;
  price: number;
}

export async function productLoader({ params }: LoaderFunctionArgs) {
  const productId = params.productId;

  if (!productId) {
    throw new Response('Product ID required', { status: 400 });
  }

  // Parallel data loading
  const productPromise = fetch(`/api/products/${productId}`).then(r => r.json());
  const reviewsPromise = fetch(`/api/products/${productId}/reviews`).then(r => r.json());

  // Defer reviews for streaming
  return defer({
    product: await productPromise,
    reviews: reviewsPromise
  });
}

// Component using loader data
const ProductDetail: React.FC = () => {
  const data = useLoaderData() as {
    product: Product;
    reviews: Promise<Review[]>;
  };

  return (
    <div>
      <h1>{data.product.name}</h1>
      <p>${data.product.price}</p>

      <Suspense fallback={<div>Loading reviews...</div>}>
        <Await resolve={data.reviews}>
          {(reviews) => (
            <ReviewList reviews={reviews} />
          )}
        </Await>
      </Suspense>
    </div>
  );
};
```

### Programmatic Navigation

```tsx
import { useNavigate, useLocation } from 'react-router-dom';

const SearchForm: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleSearch = (query: string) => {
    // Navigate with search params
    navigate({
      pathname: '/search',
      search: `?q=${encodeURIComponent(query)}`
    });
  };

  const handleFilter = (filters: FilterParams) => {
    // Replace current route with new filters
    navigate(
      {
        pathname: location.pathname,
        search: buildSearchParams(filters)
      },
      { replace: true }
    );
  };

  const goBack = () => {
    navigate(-1); // Go back one step
  };

  const goToProduct = (id: string) => {
    // Navigate with state
    navigate(`/products/${id}`, {
      state: { from: location.pathname }
    });
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const formData = new FormData(e.currentTarget);
      handleSearch(formData.get('query') as string);
    }}>
      <input name="query" type="search" placeholder="Search..." />
      <button type="submit">Search</button>
    </form>
  );
};
```

### Route Actions for Mutations

```tsx
import { Form, useActionData, redirect } from 'react-router-dom';

// Action for form submission
export async function createProductAction({ request }: ActionFunctionArgs) {
  const formData = await request.formData();

  const product = {
    name: formData.get('name'),
    price: formData.get('price'),
    description: formData.get('description')
  };

  try {
    const response = await fetch('/api/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product)
    });

    if (!response.ok) {
      return { error: 'Failed to create product' };
    }

    const newProduct = await response.json();
    return redirect(`/products/${newProduct.id}`);
  } catch (error) {
    return { error: 'Network error' };
  }
}

const CreateProduct: React.FC = () => {
  const actionData = useActionData() as { error?: string };

  return (
    <Form method="post" className="product-form">
      {actionData?.error && (
        <div className="error">{actionData.error}</div>
      )}

      <label>
        Name:
        <input name="name" required />
      </label>

      <label>
        Price:
        <input name="price" type="number" step="0.01" required />
      </label>

      <label>
        Description:
        <textarea name="description" required />
      </label>

      <button type="submit">Create Product</button>
    </Form>
  );
};
```

## Next.js App Router

### File-Based Routing

```tsx
// app/layout.tsx - Root layout
export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <nav>
          <Link href="/">Home</Link>
          <Link href="/products">Products</Link>
          <Link href="/about">About</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}

// app/products/layout.tsx - Nested layout
export default function ProductsLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="products-layout">
      <aside>
        <Link href="/products">All Products</Link>
        <Link href="/products/featured">Featured</Link>
        <Link href="/products/sale">On Sale</Link>
      </aside>
      <main>{children}</main>
    </div>
  );
}

// app/products/[productId]/page.tsx - Dynamic route
interface PageProps {
  params: { productId: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function ProductPage({
  params,
  searchParams
}: PageProps) {
  const product = await getProduct(params.productId);

  return (
    <div>
      <h1>{product.name}</h1>
      <p>Variant: {searchParams.variant || 'default'}</p>
    </div>
  );
}
```

### Parallel and Intercepting Routes

```tsx
// app/dashboard/@analytics/page.tsx - Parallel route
export default function Analytics() {
  return <div>Analytics Dashboard</div>;
}

// app/dashboard/@team/page.tsx - Another parallel route
export default function Team() {
  return <div>Team Overview</div>;
}

// app/dashboard/layout.tsx - Layout using parallel routes
export default function DashboardLayout({
  children,
  analytics,
  team
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
}) {
  return (
    <div className="dashboard-grid">
      <div className="main">{children}</div>
      <div className="analytics">{analytics}</div>
      <div className="team">{team}</div>
    </div>
  );
}

// app/@modal/(.)products/[id]/page.tsx - Intercepting route for modal
export default function ProductModal({
  params
}: {
  params: { id: string };
}) {
  return (
    <Modal>
      <ProductQuickView id={params.id} />
    </Modal>
  );
}
```

### Server Components with Navigation

```tsx
// app/products/page.tsx - Server Component
import { Suspense } from 'react';
import Link from 'next/link';

async function ProductList() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 } // Cache for 1 hour
  }).then(r => r.json());

  return (
    <ul>
      {products.map((product: Product) => (
        <li key={product.id}>
          <Link
            href={`/products/${product.id}`}
            prefetch={false} // Prefetch on hover
          >
            {product.name}
          </Link>
        </li>
      ))}
    </ul>
  );
}

export default function ProductsPage() {
  return (
    <div>
      <h1>Products</h1>
      <Suspense fallback={<ProductsSkeleton />}>
        <ProductList />
      </Suspense>
    </div>
  );
}
```

### Client-Side Navigation Hooks

```tsx
'use client';

import { useRouter, usePathname, useSearchParams } from 'next/navigation';

export function NavigationControls() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const updateFilters = (newFilters: Record<string, string>) => {
    const params = new URLSearchParams(searchParams);

    Object.entries(newFilters).forEach(([key, value]) => {
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
    });

    // Update URL without navigation
    router.push(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const navigateWithTransition = async (href: string) => {
    // Start transition
    if ('startViewTransition' in document) {
      (document as any).startViewTransition(() => {
        router.push(href);
      });
    } else {
      router.push(href);
    }
  };

  return (
    <div>
      <button onClick={() => router.back()}>Back</button>
      <button onClick={() => router.forward()}>Forward</button>
      <button onClick={() => router.refresh()}>Refresh</button>
      <button onClick={() => router.prefetch('/products')}>
        Prefetch Products
      </button>
    </div>
  );
}
```

## Route Guards & Protection

### Protected Routes Pattern

```tsx
// React Router
import { Navigate, useLocation } from 'react-router-dom';

interface ProtectedRouteProps {
  children: React.ReactNode;
  isAuthenticated: boolean;
  redirectTo?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  isAuthenticated,
  redirectTo = '/login'
}) => {
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to login, preserving the attempted location
    return (
      <Navigate
        to={redirectTo}
        state={{ from: location }}
        replace
      />
    );
  }

  return <>{children}</>;
};

// Usage in route config
const router = createBrowserRouter([
  {
    path: '/dashboard',
    element: (
      <ProtectedRoute isAuthenticated={isLoggedIn}>
        <Dashboard />
      </ProtectedRoute>
    )
  }
]);
```

### Role-Based Access Control

```tsx
interface RouteGuardProps {
  children: React.ReactNode;
  requiredRoles?: string[];
  requiredPermissions?: string[];
}

const RouteGuard: React.FC<RouteGuardProps> = ({
  children,
  requiredRoles = [],
  requiredPermissions = []
}) => {
  const { user } = useAuth();
  const location = useLocation();

  // Check authentication
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} />;
  }

  // Check roles
  if (requiredRoles.length > 0) {
    const hasRole = requiredRoles.some(role => user.roles.includes(role));
    if (!hasRole) {
      return <AccessDenied message="Insufficient role privileges" />;
    }
  }

  // Check permissions
  if (requiredPermissions.length > 0) {
    const hasPermission = requiredPermissions.every(permission =>
      user.permissions.includes(permission)
    );
    if (!hasPermission) {
      return <AccessDenied message="Missing required permissions" />;
    }
  }

  return <>{children}</>;
};

// Usage
<RouteGuard requiredRoles={['admin', 'moderator']}>
  <AdminPanel />
</RouteGuard>
```

## Navigation State Management

### Navigation History Stack

```tsx
interface NavigationState {
  history: string[];
  currentIndex: number;
}

const useNavigationHistory = () => {
  const location = useLocation();
  const [navState, setNavState] = useState<NavigationState>({
    history: [location.pathname],
    currentIndex: 0
  });

  useEffect(() => {
    setNavState(prev => {
      const newHistory = [...prev.history.slice(0, prev.currentIndex + 1), location.pathname];

      // Limit history size
      if (newHistory.length > 50) {
        newHistory.shift();
      }

      return {
        history: newHistory,
        currentIndex: newHistory.length - 1
      };
    });
  }, [location]);

  const canGoBack = navState.currentIndex > 0;
  const canGoForward = navState.currentIndex < navState.history.length - 1;

  const goToIndex = (index: number) => {
    if (index >= 0 && index < navState.history.length) {
      setNavState(prev => ({ ...prev, currentIndex: index }));
      // Navigate to that path
    }
  };

  return {
    history: navState.history,
    currentIndex: navState.currentIndex,
    canGoBack,
    canGoForward,
    goToIndex
  };
};
```

### Pending Navigation UI

```tsx
import { useNavigation } from 'react-router-dom';

const NavigationIndicator: React.FC = () => {
  const navigation = useNavigation();

  if (navigation.state === 'idle') return null;

  return (
    <div className="navigation-indicator">
      {navigation.state === 'loading' && (
        <div className="loading-bar">
          <div className="loading-progress" />
        </div>
      )}

      {navigation.state === 'submitting' && (
        <div className="submitting">
          <Spinner /> Submitting...
        </div>
      )}
    </div>
  );
};
```

## Deep Linking & URL State

### URL State Synchronization

```tsx
interface FilterState {
  category?: string;
  priceMin?: number;
  priceMax?: number;
  sortBy?: 'price' | 'name' | 'date';
}

const useURLState = <T extends Record<string, any>>(
  defaultState: T
): [T, (updates: Partial<T>) => void] => {
  const [searchParams, setSearchParams] = useSearchParams();

  // Parse URL to state
  const state = useMemo(() => {
    const urlState = {} as T;

    for (const [key, value] of searchParams.entries()) {
      if (key in defaultState) {
        // Type coercion based on default state
        const defaultValue = defaultState[key];
        if (typeof defaultValue === 'number') {
          urlState[key] = Number(value);
        } else if (typeof defaultValue === 'boolean') {
          urlState[key] = value === 'true';
        } else {
          urlState[key] = value;
        }
      }
    }

    return { ...defaultState, ...urlState };
  }, [searchParams, defaultState]);

  // Update URL from state
  const setState = useCallback((updates: Partial<T>) => {
    setSearchParams(prev => {
      const params = new URLSearchParams(prev);

      Object.entries(updates).forEach(([key, value]) => {
        if (value === undefined || value === defaultState[key]) {
          params.delete(key);
        } else {
          params.set(key, String(value));
        }
      });

      return params;
    });
  }, [setSearchParams, defaultState]);

  return [state, setState];
};

// Usage
const ProductFilters: React.FC = () => {
  const [filters, setFilters] = useURLState<FilterState>({
    category: undefined,
    priceMin: undefined,
    priceMax: undefined,
    sortBy: 'name'
  });

  return (
    <div>
      <select
        value={filters.sortBy}
        onChange={(e) => setFilters({ sortBy: e.target.value as any })}
      >
        <option value="name">Name</option>
        <option value="price">Price</option>
        <option value="date">Date</option>
      </select>

      <input
        type="number"
        value={filters.priceMin || ''}
        onChange={(e) => setFilters({ priceMin: Number(e.target.value) })}
        placeholder="Min price"
      />
    </div>
  );
};
```

### Shareable Links

```tsx
const ShareableLink: React.FC = () => {
  const location = useLocation();
  const [copied, setCopied] = useState(false);

  const shareableUrl = `${window.location.origin}${location.pathname}${location.search}`;

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shareableUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const share = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: document.title,
          url: shareableUrl
        });
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Share failed:', err);
        }
      }
    } else {
      copyToClipboard();
    }
  };

  return (
    <div className="shareable-link">
      <input
        type="text"
        value={shareableUrl}
        readOnly
        onClick={(e) => e.currentTarget.select()}
      />
      <button onClick={copyToClipboard}>
        {copied ? 'Copied!' : 'Copy'}
      </button>
      {navigator.share && (
        <button onClick={share}>Share</button>
      )}
    </div>
  );
};
```