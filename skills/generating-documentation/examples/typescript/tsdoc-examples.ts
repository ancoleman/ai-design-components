/**
 * Example TypeScript code demonstrating TSDoc comment best practices.
 *
 * This file shows how to document functions, classes, interfaces, and types
 * using TSDoc comments that TypeDoc can process into documentation.
 */

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
   * Simple GET request:
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
   *
   * @public
   */
  async get(path: string, config?: RequestConfig): Promise<T> {
    // Implementation
    throw new Error('Not implemented');
  }

  /**
   * Performs a POST request.
   *
   * @param path - The request path (relative to baseURL)
   * @param data - The request body data
   * @param config - Optional request configuration
   * @returns A promise resolving to the response data
   *
   * @throws {@link NetworkError}
   * Thrown when the network request fails
   *
   * @example
   * ```typescript
   * const newUser = await client.post('/users', {
   *   name: 'John Doe',
   *   email: 'john@example.com'
   * });
   * ```
   *
   * @public
   */
  async post(path: string, data: unknown, config?: RequestConfig): Promise<T> {
    // Implementation
    throw new Error('Not implemented');
  }
}

/**
 * Request configuration options.
 *
 * @public
 */
export interface RequestConfig {
  /** Query parameters to append to the URL */
  params?: Record<string, string | number>;
  /** Additional headers for this request */
  headers?: Record<string, string>;
  /** Override the default timeout for this request */
  timeout?: number;
}

/**
 * Custom error thrown when a network request fails.
 *
 * @example
 * ```typescript
 * try {
 *   await client.get('/users/123');
 * } catch (error) {
 *   if (error instanceof NetworkError) {
 *     console.error('Network error:', error.message);
 *   }
 * }
 * ```
 *
 * @public
 */
export class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

/**
 * Custom error thrown when a request times out.
 *
 * @example
 * ```typescript
 * try {
 *   await client.get('/slow-endpoint');
 * } catch (error) {
 *   if (error instanceof TimeoutError) {
 *     console.error('Request timed out');
 *   }
 * }
 * ```
 *
 * @public
 */
export class TimeoutError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'TimeoutError';
  }
}
