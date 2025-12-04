# React SPA Dashboard Example

Single Page Application dashboard using React, Vite, and TanStack ecosystem.

## Stack

- React 18
- TypeScript
- Vite
- TanStack Query (data fetching)
- TanStack Table (data grid)
- React Router (routing)
- Recharts (visualization)
- Tailwind CSS + Shadcn/ui
- Zustand (state management)

## Project Structure

```
react-dashboard/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Analytics.tsx
│   │   ├── Reports.tsx
│   │   └── Settings.tsx
│   ├── components/
│   │   ├── ui/              # Shadcn/ui
│   │   ├── dashboard/
│   │   │   ├── KPICard.tsx
│   │   │   ├── MetricsChart.tsx
│   │   │   └── DataTable.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── Layout.tsx
│   ├── hooks/
│   │   ├── useMetrics.ts
│   │   ├── useAuth.ts
│   │   └── useSSE.ts
│   ├── services/
│   │   └── api.ts           # API client
│   ├── stores/
│   │   └── authStore.ts     # Zustand store
│   └── lib/
│       └── utils.ts
├── vite.config.ts
└── package.json
```

## Quick Start

```bash
# Install
npm install

# Configure
cp .env.example .env
# Set VITE_API_URL

# Start dev server
npm run dev
```

## Data Fetching Pattern

```typescript
import { useQuery } from '@tanstack/react-query';

function DashboardMetrics() {
  const { data, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: () => fetch('/api/metrics').then(r => r.json()),
    refetchInterval: 30000,  // Refresh every 30s
  });

  if (isLoading) return <Skeleton />;
  return <MetricsDisplay data={data} />;
}
```

## Real-Time Updates

```typescript
import { useSSE } from '@/hooks/useSSE';

function RealtimeChart() {
  const { data } = useSSE('/api/metrics/stream');
  return <LineChart data={data} />;
}
```

## Integration

Backend options:
- FastAPI (see examples/fastapi-dashboard/)
- Rust Axum (see examples/rust-axum-dashboard/)
- Node.js Hono/Express
