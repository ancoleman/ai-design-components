#!/usr/bin/env python3
"""
generate_scaffold.py - Project Scaffolding Generator

Generates project scaffolding for React/Vite, Next.js, Python FastAPI, or Rust Axum
based on templates from the assembling-components skill.

ZERO CONTEXT TOKEN COST - Executed without loading into Claude's context.

Usage:
    python generate_scaffold.py <project_name> <framework> [output_dir]

Examples:
    python generate_scaffold.py my-dashboard react-vite ./output
    python generate_scaffold.py my-app nextjs ./output
    python generate_scaffold.py my-api python-fastapi ./output
    python generate_scaffold.py my-server rust-axum ./output
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ProjectConfig:
    """Project configuration."""
    name: str
    title: str
    description: str
    author: str
    version: str = "1.0.0"


FRAMEWORKS = {
    'react-vite': 'React + Vite (SPA)',
    'nextjs': 'Next.js 14/15 (SSR/SSG)',
    'python-fastapi': 'Python FastAPI',
    'rust-axum': 'Rust Axum',
}


# ============================================================================
# REACT/VITE SCAFFOLDING
# ============================================================================

def create_react_vite_scaffold(output_dir: Path, config: ProjectConfig) -> List[str]:
    """Generate React/Vite project scaffolding."""
    created_files = []

    # Directory structure
    dirs = [
        'src',
        'src/components/ui',
        'src/components/layout',
        'src/components/charts',
        'src/components/feedback',
        'src/components/features/dashboard',
        'src/context',
        'src/hooks',
        'src/lib',
        'src/styles',
        'src/types',
        'public',
    ]

    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    # package.json
    package_json = {
        "name": config.name,
        "private": True,
        "version": config.version,
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview",
            "lint": "eslint . --ext ts,tsx",
            "validate:tokens": "python scripts/validate_tokens.py src"
        },
        "dependencies": {
            "react": "^18.3.1",
            "react-dom": "^18.3.1"
        },
        "devDependencies": {
            "@types/react": "^18.3.0",
            "@types/react-dom": "^18.3.0",
            "@vitejs/plugin-react": "^4.3.0",
            "typescript": "^5.4.0",
            "vite": "^5.4.0"
        }
    }
    write_json(output_dir / 'package.json', package_json)
    created_files.append('package.json')

    # vite.config.ts
    vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
'''
    write_file(output_dir / 'vite.config.ts', vite_config)
    created_files.append('vite.config.ts')

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": True,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "ESNext",
            "skipLibCheck": True,
            "moduleResolution": "bundler",
            "allowImportingTsExtensions": True,
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx",
            "strict": True,
            "noUnusedLocals": True,
            "noUnusedParameters": True,
            "noFallthroughCasesInSwitch": True,
            "baseUrl": ".",
            "paths": {"@/*": ["./src/*"]}
        },
        "include": ["src"],
        "references": [{"path": "./tsconfig.node.json"}]
    }
    write_json(output_dir / 'tsconfig.json', tsconfig)
    created_files.append('tsconfig.json')

    # tsconfig.node.json
    tsconfig_node = {
        "compilerOptions": {
            "composite": True,
            "skipLibCheck": True,
            "module": "ESNext",
            "moduleResolution": "bundler",
            "allowSyntheticDefaultImports": True,
            "strict": True
        },
        "include": ["vite.config.ts"]
    }
    write_json(output_dir / 'tsconfig.node.json', tsconfig_node)
    created_files.append('tsconfig.node.json')

    # index.html
    index_html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="{config.description}" />
    <title>{config.title}</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
    write_file(output_dir / 'index.html', index_html)
    created_files.append('index.html')

    # src/main.tsx
    main_tsx = '''import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from '@/context/theme-provider'
import App from './App'

// CRITICAL: Import tokens FIRST
import './styles/tokens.css'
import './styles/globals.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
'''
    write_file(output_dir / 'src/main.tsx', main_tsx)
    created_files.append('src/main.tsx')

    # src/App.tsx
    app_tsx = '''function App() {
  return (
    <div className="app">
      <h1>Welcome to {PROJECT_TITLE}</h1>
      <p>Edit src/App.tsx to get started.</p>
    </div>
  )
}

export default App
'''.replace('{PROJECT_TITLE}', config.title)
    write_file(output_dir / 'src/App.tsx', app_tsx)
    created_files.append('src/App.tsx')

    # Create placeholder files
    placeholder_files = [
        'src/styles/tokens.css',
        'src/styles/globals.css',
        'src/context/theme-provider.tsx',
        'src/components/ui/index.ts',
        'src/components/layout/index.ts',
        'src/lib/utils.ts',
    ]

    for pf in placeholder_files:
        write_file(output_dir / pf, f'// TODO: Implement {Path(pf).name}\n')
        created_files.append(pf)

    return created_files


# ============================================================================
# NEXT.JS SCAFFOLDING
# ============================================================================

def create_nextjs_scaffold(output_dir: Path, config: ProjectConfig) -> List[str]:
    """Generate Next.js project scaffolding."""
    created_files = []

    # Directory structure
    dirs = [
        'src/app',
        'src/app/api/health',
        'src/app/dashboard',
        'src/components/ui',
        'src/components/layout',
        'src/components/features/dashboard',
        'src/context',
        'src/hooks',
        'src/lib',
        'src/styles',
        'src/types',
        'public',
    ]

    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    # package.json
    package_json = {
        "name": config.name,
        "version": config.version,
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint",
            "validate:tokens": "python scripts/validate_tokens.py src"
        },
        "dependencies": {
            "next": "^14.2.0",
            "react": "^18.3.1",
            "react-dom": "^18.3.1"
        },
        "devDependencies": {
            "@types/node": "^20.0.0",
            "@types/react": "^18.3.0",
            "@types/react-dom": "^18.3.0",
            "typescript": "^5.4.0"
        }
    }
    write_json(output_dir / 'package.json', package_json)
    created_files.append('package.json')

    # next.config.mjs
    next_config = '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

export default nextConfig
'''
    write_file(output_dir / 'next.config.mjs', next_config)
    created_files.append('next.config.mjs')

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "paths": {"@/*": ["./src/*"]}
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }
    write_json(output_dir / 'tsconfig.json', tsconfig)
    created_files.append('tsconfig.json')

    # src/app/layout.tsx
    layout_tsx = f'''import type {{ Metadata }} from 'next'
import {{ ThemeProvider }} from '@/context/theme-provider'

import '@/styles/tokens.css'
import './globals.css'

export const metadata: Metadata = {{
  title: '{config.title}',
  description: '{config.description}',
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          {{children}}
        </ThemeProvider>
      </body>
    </html>
  )
}}
'''
    write_file(output_dir / 'src/app/layout.tsx', layout_tsx)
    created_files.append('src/app/layout.tsx')

    # src/app/page.tsx
    page_tsx = f'''export default function Home() {{
  return (
    <main>
      <h1>Welcome to {config.title}</h1>
      <p>Edit src/app/page.tsx to get started.</p>
    </main>
  )
}}
'''
    write_file(output_dir / 'src/app/page.tsx', page_tsx)
    created_files.append('src/app/page.tsx')

    # src/app/globals.css
    globals_css = '''/* Global styles - tokens.css imported in layout.tsx */

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-family: var(--font-sans);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
}
'''
    write_file(output_dir / 'src/app/globals.css', globals_css)
    created_files.append('src/app/globals.css')

    # Placeholder files
    placeholder_files = [
        'src/styles/tokens.css',
        'src/context/theme-provider.tsx',
        'src/components/ui/index.ts',
        'src/lib/utils.ts',
    ]

    for pf in placeholder_files:
        write_file(output_dir / pf, f'// TODO: Implement {Path(pf).name}\n')
        created_files.append(pf)

    return created_files


# ============================================================================
# PYTHON FASTAPI SCAFFOLDING
# ============================================================================

def create_python_fastapi_scaffold(output_dir: Path, config: ProjectConfig) -> List[str]:
    """Generate Python FastAPI project scaffolding."""
    created_files = []

    package_name = config.name.replace('-', '_')

    # Directory structure
    dirs = [
        f'src/{package_name}',
        f'src/{package_name}/api',
        f'src/{package_name}/api/routes',
        f'src/{package_name}/core',
        f'src/{package_name}/models',
        f'src/{package_name}/services',
        f'src/{package_name}/static/css',
        f'src/{package_name}/static/js',
        f'src/{package_name}/templates',
        'tests',
        'scripts',
    ]

    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    # pyproject.toml
    pyproject = f'''[project]
name = "{config.name}"
version = "{config.version}"
description = "{config.description}"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "python-dotenv>=1.0.0",
    "jinja2>=3.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]
'''
    write_file(output_dir / 'pyproject.toml', pyproject)
    created_files.append('pyproject.toml')

    # requirements.txt
    requirements = '''fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
jinja2>=3.1.0
'''
    write_file(output_dir / 'requirements.txt', requirements)
    created_files.append('requirements.txt')

    # src/package_name/__init__.py
    write_file(output_dir / f'src/{package_name}/__init__.py', f'"""{{package_name}} package."""\n')
    created_files.append(f'src/{package_name}/__init__.py')

    # src/package_name/main.py
    main_py = f'''"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.routes import health
from .config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
    )

    app.mount("/static", StaticFiles(directory="src/{package_name}/static"), name="static")
    app.include_router(health.router, prefix="/api", tags=["health"])

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
    write_file(output_dir / f'src/{package_name}/main.py', main_py)
    created_files.append(f'src/{package_name}/main.py')

    # src/package_name/config.py
    config_py = f'''"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "{config.title}"
    version: str = "{config.version}"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
'''
    write_file(output_dir / f'src/{package_name}/config.py', config_py)
    created_files.append(f'src/{package_name}/config.py')

    # API routes
    write_file(output_dir / f'src/{package_name}/api/__init__.py', '')
    write_file(output_dir / f'src/{package_name}/api/routes/__init__.py', '')

    health_py = '''"""Health check routes."""

from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now())
'''
    write_file(output_dir / f'src/{package_name}/api/routes/health.py', health_py)
    created_files.append(f'src/{package_name}/api/routes/health.py')

    # .env.example
    env_example = '''DEBUG=false
HOST=0.0.0.0
PORT=8000
'''
    write_file(output_dir / '.env.example', env_example)
    created_files.append('.env.example')

    return created_files


# ============================================================================
# RUST AXUM SCAFFOLDING
# ============================================================================

def create_rust_axum_scaffold(output_dir: Path, config: ProjectConfig) -> List[str]:
    """Generate Rust Axum project scaffolding."""
    created_files = []

    # Directory structure
    dirs = [
        'src/routes',
        'src/handlers',
        'src/models',
        'src/services',
        'static/css',
        'static/js',
        'templates',
        'tests',
    ]

    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)

    # Cargo.toml
    cargo_toml = f'''[package]
name = "{config.name}"
version = "{config.version}"
edition = "2021"
description = "{config.description}"

[dependencies]
axum = "0.7"
tokio = {{ version = "1.35", features = ["full"] }}
tower = "0.4"
tower-http = {{ version = "0.5", features = ["fs", "trace"] }}
serde = {{ version = "1.0", features = ["derive"] }}
serde_json = "1.0"
dotenvy = "0.15"
tracing = "0.1"
tracing-subscriber = {{ version = "0.3", features = ["env-filter"] }}
thiserror = "1.0"
anyhow = "1.0"

[dev-dependencies]
axum-test = "14.0"
'''
    write_file(output_dir / 'Cargo.toml', cargo_toml)
    created_files.append('Cargo.toml')

    # src/main.rs
    main_rs = '''mod config;
mod routes;

use axum::Router;
use std::net::SocketAddr;
use tower_http::services::ServeDir;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::try_from_default_env()
            .unwrap_or_else(|_| "info".into()))
        .with(tracing_subscriber::fmt::layer())
        .init();

    let app = Router::new()
        .merge(routes::create_router())
        .nest_service("/static", ServeDir::new("static"))
        .layer(TraceLayer::new_for_http());

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    tracing::info!("Listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
'''
    write_file(output_dir / 'src/main.rs', main_rs)
    created_files.append('src/main.rs')

    # src/config.rs
    config_rs = '''use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Config {
    #[serde(default = "default_port")]
    pub port: u16,
}

fn default_port() -> u16 {
    3000
}
'''
    write_file(output_dir / 'src/config.rs', config_rs)
    created_files.append('src/config.rs')

    # src/routes/mod.rs
    routes_mod = '''pub mod health;

use axum::{routing::get, Router};

pub fn create_router() -> Router {
    Router::new()
        .route("/api/health", get(health::health_check))
}
'''
    write_file(output_dir / 'src/routes/mod.rs', routes_mod)
    created_files.append('src/routes/mod.rs')

    # src/routes/health.rs
    health_rs = '''use axum::Json;
use serde::Serialize;

#[derive(Serialize)]
pub struct HealthResponse {
    status: String,
    version: String,
}

pub async fn health_check() -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok".into(),
        version: env!("CARGO_PKG_VERSION").into(),
    })
}
'''
    write_file(output_dir / 'src/routes/health.rs', health_rs)
    created_files.append('src/routes/health.rs')

    # .env
    env_file = '''RUST_LOG=info
PORT=3000
'''
    write_file(output_dir / '.env', env_file)
    created_files.append('.env')

    return created_files


# ============================================================================
# UTILITIES
# ============================================================================

def write_file(path: Path, content: str) -> None:
    """Write content to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def write_json(path: Path, data: dict) -> None:
    """Write JSON data to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def to_title(name: str) -> str:
    """Convert kebab-case to Title Case."""
    return ' '.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate project scaffolding for various frameworks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Frameworks:
  react-vite      React + Vite (SPA)
  nextjs          Next.js 14/15 (SSR/SSG)
  python-fastapi  Python FastAPI
  rust-axum       Rust Axum

Examples:
  %(prog)s my-dashboard react-vite ./output
  %(prog)s my-app nextjs ./projects
  %(prog)s my-api python-fastapi ./services
        """
    )
    parser.add_argument('project_name', help='Project name (kebab-case)')
    parser.add_argument('framework', choices=FRAMEWORKS.keys(), help='Target framework')
    parser.add_argument('output_dir', nargs='?', default='.', help='Output directory')
    parser.add_argument('--description', '-d', default='', help='Project description')
    parser.add_argument('--author', '-a', default='', help='Author name')

    args = parser.parse_args()

    output_dir = Path(args.output_dir) / args.project_name
    if output_dir.exists():
        print(f"Error: Directory already exists: {output_dir}", file=sys.stderr)
        sys.exit(1)

    config = ProjectConfig(
        name=args.project_name,
        title=to_title(args.project_name),
        description=args.description or f'A {FRAMEWORKS[args.framework]} project',
        author=args.author or os.environ.get('USER', 'developer'),
    )

    print(f"\n{'=' * 60}")
    print(f"  GENERATING {FRAMEWORKS[args.framework].upper()} PROJECT")
    print(f"{'=' * 60}\n")
    print(f"  Name: {config.name}")
    print(f"  Title: {config.title}")
    print(f"  Output: {output_dir}\n")

    # Create scaffold based on framework
    if args.framework == 'react-vite':
        created_files = create_react_vite_scaffold(output_dir, config)
    elif args.framework == 'nextjs':
        created_files = create_nextjs_scaffold(output_dir, config)
    elif args.framework == 'python-fastapi':
        created_files = create_python_fastapi_scaffold(output_dir, config)
    elif args.framework == 'rust-axum':
        created_files = create_rust_axum_scaffold(output_dir, config)
    else:
        print(f"Error: Unknown framework: {args.framework}", file=sys.stderr)
        sys.exit(1)

    print(f"  Created {len(created_files)} files:\n")
    for f in created_files[:10]:
        print(f"    - {f}")
    if len(created_files) > 10:
        print(f"    ... and {len(created_files) - 10} more")

    print(f"\n{'=' * 60}")
    print(f"  NEXT STEPS")
    print(f"{'=' * 60}\n")

    if args.framework == 'react-vite':
        print(f"  cd {output_dir}")
        print("  npm install")
        print("  npm run dev")
    elif args.framework == 'nextjs':
        print(f"  cd {output_dir}")
        print("  npm install")
        print("  npm run dev")
    elif args.framework == 'python-fastapi':
        print(f"  cd {output_dir}")
        print("  pip install -e '.[dev]'")
        print("  uvicorn src.<package>.main:app --reload")
    elif args.framework == 'rust-axum':
        print(f"  cd {output_dir}")
        print("  cargo run")

    print()


if __name__ == "__main__":
    main()
