# Code Documentation Reference

Comprehensive guide to code documentation across TypeScript, Python, Go, and Rust.

## Table of Contents

1. [TypeScript: TypeDoc](#typescript-typedoc)
2. [Python: Sphinx](#python-sphinx)
3. [Go: godoc](#go-godoc)
4. [Rust: rustdoc](#rust-rustdoc)
5. [Best Practices](#best-practices)

## TypeScript: TypeDoc

Generate API documentation from TypeScript code with TSDoc comments.

### Installation

```bash
npm install -D typedoc
```

### Configuration

Create `typedoc.json`:

```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "exclude": [
    "**/*.test.ts",
    "**/*.spec.ts",
    "**/__tests__/**",
    "**/node_modules/**"
  ],
  "excludePrivate": true,
  "excludeProtected": false,
  "includeVersion": true,
  "readme": "README.md",
  "categorizeByGroup": true,
  "categoryOrder": [
    "Core",
    "Utilities",
    "*",
    "Internal"
  ],
  "sort": ["source-order"],
  "navigation": {
    "includeCategories": true,
    "includeGroups": true
  },
  "plugin": [
    "typedoc-plugin-markdown",
    "typedoc-plugin-mermaid"
  ]
}
```

### TSDoc Comment Syntax

#### Functions

```typescript
/**
 * Calculate the factorial of a number.
 *
 * @param n - The number to calculate factorial for
 * @returns The factorial of n
 *
 * @throws {@link RangeError}
 * Thrown if n is negative
 *
 * @example
 * Calculate factorial of 5:
 * ```typescript
 * const result = factorial(5);
 * console.log(result); // 120
 * ```
 *
 * @example
 * Handle errors:
 * ```typescript
 * try {
 *   factorial(-1);
 * } catch (error) {
 *   console.error(error.message);
 * }
 * ```
 *
 * @public
 */
export function factorial(n: number): number {
  if (n < 0) {
    throw new RangeError('n must be non-negative');
  }
  if (n === 0) return 1;
  return n * factorial(n - 1);
}
```

#### Classes

```typescript
/**
 * A generic HTTP client for making requests.
 *
 * This client provides methods for GET, POST, PUT, and DELETE requests
 * with automatic retry logic, timeout handling, and request/response
 * interceptors.
 *
 * @typeParam T - The type of the response data
 *
 * @example
 * Create a client for user data:
 * ```typescript
 * interface User {
 *   id: string;
 *   name: string;
 *   email: string;
 * }
 *
 * const client = new HttpClient<User>({
 *   baseURL: 'https://api.example.com',
 *   timeout: 30000
 * });
 *
 * const user = await client.get('/users/123');
 * console.log(user.name);
 * ```
 *
 * @public
 */
export class HttpClient<T> {
  /**
   * Creates a new HttpClient instance.
   *
   * @param options - Configuration options for the client
   *
   * @example
   * ```typescript
   * const client = new HttpClient({
   *   baseURL: 'https://api.example.com',
   *   timeout: 30000,
   *   headers: {
   *     'Authorization': 'Bearer token123'
   *   }
   * });
   * ```
   */
  constructor(private options: HttpOptions) {}

  /**
   * Performs a GET request.
   *
   * @param path - The request path (relative to baseURL)
   * @param config - Optional request configuration
   * @returns A promise resolving to the response data
   *
   * @throws {@link NetworkError}
   * Thrown when the network request fails
   *
   * @throws {@link TimeoutError}
   * Thrown when the request times out
   *
   * @example
   * ```typescript
   * const user = await client.get('/users/123');
   * ```
   *
   * @example
   * With query parameters:
   * ```typescript
   * const users = await client.get('/users', {
   *   params: { limit: 10, offset: 0 }
   * });
   * ```
   */
  async get(path: string, config?: RequestConfig): Promise<T> {
    // Implementation
    throw new Error('Not implemented');
  }
}
```

#### Interfaces

```typescript
/**
 * Configuration options for the HTTP client.
 *
 * @example
 * Basic configuration:
 * ```typescript
 * const options: HttpOptions = {
 *   baseURL: 'https://api.example.com',
 *   timeout: 30000
 * };
 * ```
 *
 * @example
 * With retry configuration:
 * ```typescript
 * const options: HttpOptions = {
 *   baseURL: 'https://api.example.com',
 *   timeout: 30000,
 *   retry: {
 *     maxRetries: 3,
 *     backoff: 'exponential'
 *   }
 * };
 * ```
 *
 * @public
 */
export interface HttpOptions {
  /**
   * The base URL for all requests.
   *
   * All request paths will be relative to this URL.
   *
   * @example
   * ```typescript
   * baseURL: 'https://api.example.com/v1'
   * ```
   */
  baseURL: string;

  /**
   * Request timeout in milliseconds.
   *
   * @defaultValue `30000` (30 seconds)
   */
  timeout?: number;

  /**
   * HTTP headers to include with every request.
   *
   * @example
   * ```typescript
   * headers: {
   *   'Authorization': 'Bearer token123',
   *   'Content-Type': 'application/json'
   * }
   * ```
   */
  headers?: Record<string, string>;

  /**
   * Retry configuration.
   *
   * @defaultValue `{ maxRetries: 3, backoff: 'exponential' }`
   */
  retry?: {
    /** Maximum number of retry attempts */
    maxRetries: number;
    /** Backoff strategy for retries */
    backoff: 'linear' | 'exponential';
  };
}
```

#### Type Aliases

```typescript
/**
 * A callback function for handling HTTP responses.
 *
 * @param response - The HTTP response object
 * @returns Processed response data or void
 *
 * @example
 * ```typescript
 * const handler: ResponseHandler<User> = (response) => {
 *   console.log('User received:', response.data);
 *   return response.data;
 * };
 * ```
 *
 * @public
 */
export type ResponseHandler<T> = (response: Response<T>) => T | void;
```

### TSDoc Tags Reference

| Tag | Purpose | Example |
|-----|---------|---------|
| `@param` | Document function parameter | `@param name - User's name` |
| `@returns` | Document return value | `@returns The user object` |
| `@throws` | Document exceptions | `@throws {@link Error} When...` |
| `@example` | Provide code example | See above |
| `@typeParam` | Document generic type | `@typeParam T - The data type` |
| `@public` | Mark as public API | `@public` |
| `@internal` | Mark as internal | `@internal` |
| `@deprecated` | Mark as deprecated | `@deprecated Use newFunc instead` |
| `@see` | Cross-reference | `@see {@link OtherClass}` |
| `@remarks` | Additional notes | `@remarks This is experimental` |
| `@defaultValue` | Document default value | `@defaultValue `true`` |

### Generate Documentation

```bash
# Generate HTML documentation
npx typedoc

# Generate Markdown documentation
npx typedoc --plugin typedoc-plugin-markdown

# Watch mode
npx typedoc --watch

# With custom config
npx typedoc --options typedoc.json
```

### Add to package.json

```json
{
  "scripts": {
    "docs": "typedoc",
    "docs:watch": "typedoc --watch",
    "docs:serve": "npx http-server docs"
  }
}
```

## Python: Sphinx

Generate documentation from Python docstrings.

### Installation

```bash
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
```

### Quick Start

```bash
# Initialize Sphinx
sphinx-quickstart docs

# Answer prompts:
# - Separate source and build directories: yes
# - Project name: My Project
# - Author name: Your Name
# - Project release: 1.0.0
```

### Configuration

Edit `docs/source/conf.py`:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'My Project'
copyright = '2025, My Company'
author = 'My Name'
release = '1.0.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',        # Auto-generate from docstrings
    'sphinx.ext.napoleon',       # Support Google/NumPy style
    'sphinx.ext.viewcode',       # Add source code links
    'sphinx.ext.intersphinx',    # Link to other docs
    'sphinx.ext.autosummary',    # Generate summary tables
    'sphinx_autodoc_typehints',  # Type hints support
]

# Napoleon settings (Google/NumPy docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Theme
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
}
```

### Google-Style Docstrings

#### Functions

```python
def calculate_total(items: list[dict], tax_rate: float = 0.0) -> float:
    """Calculate the total price including tax.

    This function sums up the price of all items and applies
    the specified tax rate.

    Args:
        items: A list of item dictionaries with 'price' and 'quantity' keys.
            Each item should have the following structure:
            - price (float): The unit price
            - quantity (int): The quantity
        tax_rate: The tax rate as a decimal (e.g., 0.1 for 10%).
            Defaults to 0.0 (no tax).

    Returns:
        The total price including tax.

    Raises:
        ValueError: If any item is missing 'price' or 'quantity'.
        TypeError: If tax_rate is not a number.

    Example:
        Calculate total with tax:

        >>> items = [
        ...     {'price': 10.0, 'quantity': 2},
        ...     {'price': 5.0, 'quantity': 1}
        ... ]
        >>> calculate_total(items, tax_rate=0.1)
        27.5

        Calculate without tax:

        >>> calculate_total(items)
        25.0

    Note:
        Tax is calculated on the subtotal (sum of all items).

    See Also:
        calculate_tax: For calculating tax separately.
        apply_discount: For applying discounts before tax.
    """
    if not all('price' in item and 'quantity' in item for item in items):
        raise ValueError("All items must have 'price' and 'quantity'")

    subtotal = sum(item['price'] * item['quantity'] for item in items)
    return subtotal * (1 + tax_rate)
```

#### Classes

```python
class HttpClient:
    """A simple HTTP client for making requests.

    This client provides methods for GET, POST, PUT, and DELETE requests
    with automatic retry logic and timeout handling.

    Attributes:
        base_url (str): The base URL for all requests.
        timeout (int): Request timeout in seconds.
        headers (dict): Default headers for all requests.

    Example:
        Create a client and make a request:

        >>> client = HttpClient('https://api.example.com')
        >>> response = client.get('/users/123')
        >>> print(response['name'])
        'John Doe'

        With custom timeout and headers:

        >>> client = HttpClient(
        ...     base_url='https://api.example.com',
        ...     timeout=60,
        ...     headers={'Authorization': 'Bearer token'}
        ... )
    """

    def __init__(self, base_url: str, timeout: int = 30):
        """Initialize the HTTP client.

        Args:
            base_url: The base URL for all requests.
            timeout: Request timeout in seconds. Defaults to 30.

        Raises:
            ValueError: If base_url is empty or invalid.
        """
        if not base_url:
            raise ValueError("base_url cannot be empty")

        self.base_url = base_url
        self.timeout = timeout
        self.headers = {}

    def get(self, path: str, params: dict = None) -> dict:
        """Perform a GET request.

        Args:
            path: The request path (relative to base_url).
            params: Optional query parameters.

        Returns:
            The JSON response as a dictionary.

        Raises:
            NetworkError: If the request fails.
            TimeoutError: If the request times out.

        Example:
            Simple GET request:

            >>> response = client.get('/users/123')

            With query parameters:

            >>> response = client.get('/users', params={'limit': 10})
        """
        pass  # Implementation
```

### NumPy-Style Docstrings

```python
def process_data(data: list, threshold: float = 0.5) -> list:
    """Process data with threshold filtering.

    Parameters
    ----------
    data : list
        Input data to process. Each element should be numeric.
    threshold : float, optional
        Threshold value for filtering, by default 0.5

    Returns
    -------
    list
        Processed and filtered data.

    Raises
    ------
    ValueError
        If data is empty or contains non-numeric values.

    Examples
    --------
    >>> process_data([0.3, 0.6, 0.8], threshold=0.5)
    [0.6, 0.8]

    >>> process_data([1, 2, 3])
    [1, 2, 3]

    Notes
    -----
    This function filters values below the threshold and applies
    a transformation to the remaining values.

    See Also
    --------
    filter_data : For filtering without transformation.
    transform_data : For transformation without filtering.
    """
    pass
```

### Generate Documentation

```bash
# Generate API docs from source code
cd docs
sphinx-apidoc -o source ../src

# Build HTML documentation
make html

# Build PDF documentation
make latexpdf

# Clean build artifacts
make clean

# Watch for changes (requires sphinx-autobuild)
pip install sphinx-autobuild
sphinx-autobuild source build/html
```

## Go: godoc

Document Go packages using doc comments (built-in).

### Package Documentation

Create `doc.go` in package directory:

```go
// Package mathutil provides utility functions for mathematical operations.
//
// This package includes functions for basic arithmetic, statistics,
// and numerical analysis.
//
// # Example Usage
//
//	result := mathutil.Add(2, 3)
//	fmt.Println(result) // Output: 5
//
// # Features
//
//   - Basic arithmetic operations
//   - Statistical functions (mean, median, mode)
//   - Numerical analysis utilities
//
// # Installation
//
//	go get github.com/example/mathutil
package mathutil
```

### Function Documentation

```go
package mathutil

// Add returns the sum of two integers.
//
// Parameters:
//   - a: The first integer
//   - b: The second integer
//
// Returns the sum of a and b.
//
// Example:
//
//	sum := Add(5, 3)
//	fmt.Println(sum) // Output: 8
func Add(a, b int) int {
	return a + b
}

// Divide returns the quotient and remainder of a divided by b.
//
// Returns an error if b is zero.
//
// Example:
//
//	quotient, remainder, err := Divide(10, 3)
//	if err != nil {
//		log.Fatal(err)
//	}
//	fmt.Printf("%d remainder %d\n", quotient, remainder)
//	// Output: 3 remainder 1
func Divide(a, b int) (int, int, error) {
	if b == 0 {
		return 0, 0, errors.New("division by zero")
	}
	return a / b, a % b, nil
}
```

### Type Documentation

```go
// HttpClient provides methods for making HTTP requests.
//
// The client includes automatic retry logic and timeout handling.
//
// Example:
//
//	client := &HttpClient{
//		BaseURL: "https://api.example.com",
//		Timeout: 30 * time.Second,
//	}
//	response, err := client.Get("/users/123")
//	if err != nil {
//		log.Fatal(err)
//	}
type HttpClient struct {
	// BaseURL is the base URL for all requests.
	BaseURL string

	// Timeout is the request timeout duration.
	Timeout time.Duration

	// Headers are the default headers for all requests.
	Headers map[string]string
}

// Get performs a GET request to the specified path.
//
// The path is relative to the client's BaseURL.
//
// Returns the response body as a byte slice and any error encountered.
//
// Example:
//
//	data, err := client.Get("/users/123")
//	if err != nil {
//		log.Fatal(err)
//	}
func (c *HttpClient) Get(path string) ([]byte, error) {
	// Implementation
	return nil, nil
}
```

### Generate Documentation

```bash
# View local documentation
godoc -http=:6060
# Visit http://localhost:6060/pkg/your-package/

# Generate static HTML
godoc -html your-package > docs.html

# Publish to pkg.go.dev
# Push to GitHub and it will auto-index
```

## Rust: rustdoc

Document Rust code with doc comments (built-in).

### Module Documentation

```rust
//! # Mathutil
//!
//! A utility library for mathematical operations.
//!
//! This crate provides functions for basic arithmetic, statistics,
//! and numerical analysis.
//!
//! ## Example
//!
//! ```
//! use mathutil::add;
//!
//! let result = add(2, 3);
//! assert_eq!(result, 5);
//! ```
//!
//! ## Features
//!
//! - Basic arithmetic operations
//! - Statistical functions
//! - Numerical analysis utilities

/// Adds two numbers together.
///
/// # Arguments
///
/// * `a` - The first number
/// * `b` - The second number
///
/// # Returns
///
/// The sum of `a` and `b`.
///
/// # Examples
///
/// ```
/// use mathutil::add;
///
/// let sum = add(2, 3);
/// assert_eq!(sum, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### Struct Documentation

```rust
/// Configuration options for the HTTP client.
///
/// # Examples
///
/// ```
/// use mathutil::HttpOptions;
///
/// let options = HttpOptions {
///     base_url: String::from("https://api.example.com"),
///     timeout: Some(30),
///     headers: None,
/// };
/// ```
#[derive(Debug, Clone)]
pub struct HttpOptions {
    /// The base URL for all requests.
    pub base_url: String,

    /// Request timeout in seconds.
    pub timeout: Option<u64>,

    /// HTTP headers to include with every request.
    pub headers: Option<std::collections::HashMap<String, String>>,
}

/// A generic HTTP client for making requests.
///
/// # Type Parameters
///
/// * `T` - The type of the response data
///
/// # Examples
///
/// ```
/// use mathutil::{HttpClient, HttpOptions};
///
/// let options = HttpOptions {
///     base_url: String::from("https://api.example.com"),
///     timeout: Some(30),
///     headers: None,
/// };
///
/// let client = HttpClient::<String>::new(options);
/// ```
pub struct HttpClient<T> {
    options: HttpOptions,
    _phantom: std::marker::PhantomData<T>,
}

impl<T> HttpClient<T> {
    /// Creates a new `HttpClient` instance.
    ///
    /// # Arguments
    ///
    /// * `options` - Configuration options for the client
    ///
    /// # Examples
    ///
    /// ```
    /// use mathutil::{HttpClient, HttpOptions};
    ///
    /// let options = HttpOptions {
    ///     base_url: String::from("https://api.example.com"),
    ///     timeout: Some(30),
    ///     headers: None,
    /// };
    ///
    /// let client = HttpClient::<String>::new(options);
    /// ```
    pub fn new(options: HttpOptions) -> Self {
        Self {
            options,
            _phantom: std::marker::PhantomData,
        }
    }

    /// Performs a GET request.
    ///
    /// # Arguments
    ///
    /// * `path` - The request path (relative to base_url)
    ///
    /// # Returns
    ///
    /// A `Result` containing the response data or an error.
    ///
    /// # Errors
    ///
    /// Returns an error if:
    /// - The request fails
    /// - The request times out
    /// - The response cannot be parsed
    ///
    /// # Examples
    ///
    /// ```no_run
    /// # use mathutil::{HttpClient, HttpOptions};
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// # let options = HttpOptions {
    /// #     base_url: String::from("https://api.example.com"),
    /// #     timeout: Some(30),
    /// #     headers: None,
    /// # };
    /// let client = HttpClient::<String>::new(options);
    /// let response = client.get("/users/123").await?;
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get(&self, path: &str) -> Result<T, Box<dyn std::error::Error>> {
        // Implementation
        unimplemented!()
    }
}
```

### Generate Documentation

```bash
# Generate and open documentation
cargo doc --open

# Generate without dependencies
cargo doc --no-deps

# Generate with private items
cargo doc --document-private-items

# Generate and check for broken links
cargo doc --no-deps && cargo deadlinks
```

## Best Practices

### 1. Document Public APIs

Focus on public interfaces. Internal implementation details can use inline comments.

### 2. Include Examples

Working code examples are more valuable than descriptions.

### 3. Document Parameters and Returns

Clearly describe inputs, outputs, and side effects.

### 4. Document Errors

List all possible exceptions/errors and when they occur.

### 5. Keep Documentation Updated

Update docs when code changes. Use CI to validate.

### 6. Use Consistent Style

Choose one documentation style (Google, NumPy, TSDoc) and stick to it.

### 7. Test Examples

Ensure examples are runnable and correct.

### 8. Link Related Items

Cross-reference related functions, classes, and types.

### 9. Provide Context

Explain why something exists, not just what it does.

### 10. Use Type Hints

Type hints improve generated documentation (TypeScript, Python 3.5+).
