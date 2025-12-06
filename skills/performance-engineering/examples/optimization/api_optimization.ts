/**
 * API Performance Optimization Examples
 *
 * Demonstrates: Pagination, batching, and field selection patterns
 */

import express, { Request, Response } from 'express';

const app = express();
app.use(express.json());

// ===== PAGINATION: Cursor-Based =====

interface PaginationRequest {
  cursor?: string;
  limit?: number;
}

app.get('/api/products', async (req: Request, res: Response) => {
  const { cursor, limit = 20 } = req.query as PaginationRequest;

  // Cursor-based pagination (efficient for large datasets)
  const query = cursor
    ? `SELECT * FROM products WHERE id > ${cursor} ORDER BY id LIMIT ${limit}`
    : `SELECT * FROM products ORDER BY id LIMIT ${limit}`;

  const products = await db.query(query);
  const nextCursor = products[products.length - 1]?.id;

  res.json({
    data: products,
    next_cursor: nextCursor,
    has_more: products.length === limit,
  });
});

// ===== BATCH OPERATIONS =====

app.post('/api/users/batch', async (req: Request, res: Response) => {
  const { ids } = req.body;

  if (!Array.isArray(ids) || ids.length === 0) {
    return res.status(400).json({ error: 'ids must be non-empty array' });
  }

  // Single query for multiple IDs (vs N separate queries)
  const users = await db.query(
    `SELECT * FROM users WHERE id IN (${ids.join(',')})`,
  );

  res.json(users);
});

// ===== FIELD SELECTION =====

app.get('/api/users/:id', async (req: Request, res: Response) => {
  const { id } = req.params;
  const { fields } = req.query;

  // Allow client to request specific fields
  const fieldList = fields
    ? (fields as string).split(',').join(', ')
    : 'id, name, email, created_at';

  const user = await db.query(
    `SELECT ${fieldList} FROM users WHERE id = ${id}`,
  );

  res.json(user);
});

// ===== RESPONSE COMPRESSION =====

import compression from 'compression';

app.use(compression({
  level: 6,              // Compression level (1-9)
  threshold: 1024,       // Only compress > 1KB
}));

// ===== CACHING HEADERS =====

app.get('/api/products/:id', async (req: Request, res: Response) => {
  const { id } = req.params;
  const product = await db.query(`SELECT * FROM products WHERE id = ${id}`);

  // Cache for 5 minutes (browser and CDN)
  res.set({
    'Cache-Control': 'public, max-age=300',
    'ETag': generateETag(product),
  });

  res.json(product);
});

// Helper functions (placeholder)
const db = {
  query: async (sql: string) => {
    // Database query implementation
    return [];
  },
};

const generateETag = (data: any): string => {
  // ETag generation (hash of data)
  return 'etag';
};
