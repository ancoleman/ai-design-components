# React + Vite Template

Modern React template with TypeScript, Vite, TanStack Query, and Tailwind CSS.

## Stack

- React 18
- TypeScript
- Vite (build tool)
- TanStack Query (data fetching)
- React Router (routing)
- Tailwind CSS (styling)
- Shadcn/ui (components)

## Project Structure

```
my-react-app/
├── src/
│   ├── main.tsx             # Entry point
│   ├── App.tsx              # Root component
│   ├── components/          # Reusable components
│   │   ├── ui/              # Shadcn/ui components
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Layout.tsx
│   │   └── common/
│   ├── pages/               # Page components
│   │   ├── Home.tsx
│   │   ├── Dashboard.tsx
│   │   └── NotFound.tsx
│   ├── hooks/               # Custom hooks
│   │   ├── useAuth.ts
│   │   └── useApi.ts
│   ├── services/            # API clients
│   │   └── api.ts
│   ├── lib/                 # Utilities
│   │   └── utils.ts
│   ├── types/               # TypeScript types
│   │   └── index.ts
│   └── styles/
│       └── index.css
├── public/
├── index.html
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env with API URL

# 3. Start development server
npm run dev
```

Access app: http://localhost:5173

## Features

- Hot Module Replacement (HMR)
- TypeScript strict mode
- ESLint + Prettier configured
- Path aliases (@/components)
- TanStack Query for server state
- React Router for navigation

## Use with Skill

This template is referenced by the `assembling-components` skill for rapidly scaffolding React frontend applications.
