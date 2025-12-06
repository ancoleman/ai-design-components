/**
 * Hono Edge-First REST API Example
 *
 * Demonstrates:
 * - Edge-first architecture (runs on any runtime)
 * - Zod validation
 * - OpenAPI documentation
 * - Cursor pagination
 * - Type-safe routing
 */

import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { z } from 'zod'
import { zValidator } from '@hono/zod-validator'
import { swaggerUI } from '@hono/swagger-ui'
import { OpenAPIHono, createRoute, z as zod } from '@hono/zod-openapi'

// Initialize app
const app = new OpenAPIHono()

// CORS middleware
app.use('/*', cors({
  origin: ['http://localhost:3000'],
  credentials: true
}))

// Schemas
const ItemSchema = z.object({
  id: z.string().openapi({ example: '1' }),
  name: z.string().min(1).max(100).openapi({ example: 'Widget A' }),
  description: z.string().max(500).openapi({ example: 'A useful widget' }),
  price: z.number().positive().openapi({ example: 29.99 }),
  createdAt: z.string().datetime().openapi({ example: '2025-12-02T10:00:00Z' })
})

const CreateItemSchema = ItemSchema.omit({ id: true, createdAt: true })

const PaginatedResponseSchema = z.object({
  items: z.array(ItemSchema),
  nextCursor: z.string().nullable(),
  hasMore: z.boolean()
})

const ErrorSchema = z.object({
  error: z.string()
})

// In-memory database
interface Item {
  id: string
  name: string
  description: string
  price: number
  createdAt: string
}

const itemsDB: Map<string, Item> = new Map([
  ['1', {
    id: '1',
    name: 'Widget A',
    description: 'First widget',
    price: 19.99,
    createdAt: new Date().toISOString()
  }],
  ['2', {
    id: '2',
    name: 'Widget B',
    description: 'Second widget',
    price: 29.99,
    createdAt: new Date().toISOString()
  }]
])

// Routes

// Health check
const healthRoute = createRoute({
  method: 'get',
  path: '/health',
  tags: ['health'],
  responses: {
    200: {
      description: 'Service is healthy',
      content: {
        'application/json': {
          schema: z.object({
            status: z.string(),
            timestamp: z.string()
          })
        }
      }
    }
  },
  summary: 'Health check'
})

app.openapi(healthRoute, (c) => {
  return c.json({
    status: 'healthy',
    timestamp: new Date().toISOString()
  })
})

// List items with pagination
const listItemsRoute = createRoute({
  method: 'get',
  path: '/items',
  tags: ['items'],
  request: {
    query: z.object({
      cursor: z.string().optional(),
      limit: z.string().transform(Number).pipe(z.number().min(1).max(100)).default('20')
    })
  },
  responses: {
    200: {
      description: 'Paginated list of items',
      content: {
        'application/json': {
          schema: PaginatedResponseSchema
        }
      }
    }
  },
  summary: 'List items with cursor pagination'
})

app.openapi(listItemsRoute, (c) => {
  const { cursor, limit } = c.req.valid('query')

  // Convert map to sorted array
  let items = Array.from(itemsDB.values()).sort((a, b) => a.id.localeCompare(b.id))

  // Apply cursor filter
  if (cursor) {
    items = items.filter(item => item.id > cursor)
  }

  // Check if more results exist
  const hasMore = items.length > limit
  const resultItems = items.slice(0, limit)
  const nextCursor = resultItems.length > 0 && hasMore ? resultItems[resultItems.length - 1].id : null

  return c.json({
    items: resultItems,
    nextCursor,
    hasMore
  })
})

// Get item by ID
const getItemRoute = createRoute({
  method: 'get',
  path: '/items/{id}',
  tags: ['items'],
  request: {
    params: z.object({
      id: z.string()
    })
  },
  responses: {
    200: {
      description: 'Item found',
      content: {
        'application/json': {
          schema: ItemSchema
        }
      }
    },
    404: {
      description: 'Item not found',
      content: {
        'application/json': {
          schema: ErrorSchema
        }
      }
    }
  },
  summary: 'Get item by ID'
})

app.openapi(getItemRoute, (c) => {
  const { id } = c.req.valid('param')
  const item = itemsDB.get(id)

  if (!item) {
    return c.json({ error: `Item with id '${id}' not found` }, 404)
  }

  return c.json(item)
})

// Create item
const createItemRoute = createRoute({
  method: 'post',
  path: '/items',
  tags: ['items'],
  request: {
    body: {
      content: {
        'application/json': {
          schema: CreateItemSchema
        }
      }
    }
  },
  responses: {
    201: {
      description: 'Item created',
      content: {
        'application/json': {
          schema: ItemSchema
        }
      }
    },
    400: {
      description: 'Validation error',
      content: {
        'application/json': {
          schema: ErrorSchema
        }
      }
    }
  },
  summary: 'Create new item'
})

app.openapi(createItemRoute, async (c) => {
  const body = c.req.valid('json')

  // Generate new ID
  const newId = String(itemsDB.size + 1)

  const newItem: Item = {
    id: newId,
    ...body,
    createdAt: new Date().toISOString()
  }

  itemsDB.set(newId, newItem)

  return c.json(newItem, 201)
})

// Update item
const updateItemRoute = createRoute({
  method: 'put',
  path: '/items/{id}',
  tags: ['items'],
  request: {
    params: z.object({
      id: z.string()
    }),
    body: {
      content: {
        'application/json': {
          schema: CreateItemSchema
        }
      }
    }
  },
  responses: {
    200: {
      description: 'Item updated',
      content: {
        'application/json': {
          schema: ItemSchema
        }
      }
    },
    404: {
      description: 'Item not found',
      content: {
        'application/json': {
          schema: ErrorSchema
        }
      }
    }
  },
  summary: 'Update item'
})

app.openapi(updateItemRoute, async (c) => {
  const { id } = c.req.valid('param')
  const body = c.req.valid('json')

  const item = itemsDB.get(id)

  if (!item) {
    return c.json({ error: `Item with id '${id}' not found` }, 404)
  }

  const updatedItem: Item = {
    ...item,
    ...body
  }

  itemsDB.set(id, updatedItem)

  return c.json(updatedItem)
})

// Delete item
const deleteItemRoute = createRoute({
  method: 'delete',
  path: '/items/{id}',
  tags: ['items'],
  request: {
    params: z.object({
      id: z.string()
    })
  },
  responses: {
    204: {
      description: 'Item deleted'
    },
    404: {
      description: 'Item not found',
      content: {
        'application/json': {
          schema: ErrorSchema
        }
      }
    }
  },
  summary: 'Delete item'
})

app.openapi(deleteItemRoute, (c) => {
  const { id } = c.req.valid('param')

  if (!itemsDB.has(id)) {
    return c.json({ error: `Item with id '${id}' not found` }, 404)
  }

  itemsDB.delete(id)

  return c.body(null, 204)
})

// OpenAPI documentation
app.doc('/openapi.json', {
  openapi: '3.1.0',
  info: {
    title: 'Items API',
    version: '1.0.0',
    description: 'Edge-first REST API built with Hono'
  }
})

// Swagger UI
app.get('/docs', swaggerUI({ url: '/openapi.json' }))

export default app

// Run with Node.js/Bun:
// bun run index.ts
// node --loader ts-node/esm index.ts

// Deploy to Cloudflare Workers, Vercel Edge, Deno Deploy, etc.
