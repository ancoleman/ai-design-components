# Next.js Dashboard Example

Full-stack Next.js 14 dashboard with App Router, Server Components, and real-time updates.

## Features

- Next.js 14 App Router
- Server Components + Client Components
- Authentication (NextAuth.js)
- PostgreSQL with Prisma
- Real-time metrics (SSE)
- TanStack Table
- Recharts visualization
- Tailwind CSS + Shadcn/ui
- TypeScript strict mode

## Project Structure

```
nextjs-dashboard/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   ├── dashboard/
│   │   ├── layout.tsx       # Dashboard layout
│   │   ├── page.tsx         # Dashboard home
│   │   ├── metrics/
│   │   └── analytics/
│   ├── api/
│   │   ├── auth/[...nextauth]/route.ts
│   │   ├── dashboard/
│   │   │   └── metrics/route.ts
│   │   └── stream/
│   │       └── route.ts     # SSE endpoint
│   └── (auth)/
│       ├── login/page.tsx
│       └── register/page.tsx
├── components/
│   ├── ui/                  # Shadcn/ui components
│   ├── dashboard/
│   │   ├── KPICard.tsx
│   │   ├── MetricsChart.tsx
│   │   └── DataTable.tsx
│   └── layout/
│       ├── Header.tsx
│       └── Sidebar.tsx
├── lib/
│   ├── db.ts                # Prisma client
│   ├── auth.ts              # NextAuth config
│   └── utils.ts
├── prisma/
│   └── schema.prisma
├── next.config.js
└── package.json
```

## Quick Start

```bash
# Install
npm install

# Setup database
cp .env.example .env
npx prisma migrate dev

# Start dev server
npm run dev
```

Access: http://localhost:3000

## Key Features

### Server Components (Default)

```typescript
// app/dashboard/page.tsx (Server Component)
import { getMetrics } from '@/lib/api';

export default async function DashboardPage() {
  const metrics = await getMetrics();  // Fetched on server
  return <MetricsDisplay metrics={metrics} />;
}
```

### Client Components (Interactive)

```typescript
'use client';

import { useEffect, useState } from 'react';

export function RealtimeMetrics() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const es = new EventSource('/api/stream');
    es.onmessage = (e) => setMetrics(JSON.parse(e.data));
    return () => es.close();
  }, []);

  return <MetricsChart data={metrics} />;
}
```

## Integration

Combines skills:
- creating-dashboards (KPIs, charts)
- building-tables (data grids)
- visualizing-data (charts)
- auth-security (NextAuth)
- databases-relational (Prisma)
- realtime-sync (SSE streaming)
