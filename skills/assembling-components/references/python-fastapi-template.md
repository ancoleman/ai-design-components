# Python FastAPI Template

> Complete scaffolding template for modern async APIs using FastAPI with Pydantic validation.


## Table of Contents

- [Project Structure](#project-structure)
- [Core Files](#core-files)
  - [pyproject.toml](#pyprojecttoml)
  - [requirements.txt](#requirementstxt)
  - [src/project_name/main.py](#srcproject_namemainpy)
  - [src/project_name/config.py](#srcproject_nameconfigpy)
  - [src/project_name/api/routes/health.py](#srcproject_nameapirouteshealthpy)
  - [src/project_name/api/routes/dashboard.py](#srcproject_nameapiroutesdashboardpy)
  - [src/project_name/templates/base.html](#srcproject_nametemplatesbasehtml)
  - [src/project_name/templates/dashboard.html](#srcproject_nametemplatesdashboardhtml)
  - [Dockerfile](#dockerfile)
  - [docker-compose.yml](#docker-composeyml)
- [Commands](#commands)
- [Integration Checklist](#integration-checklist)

## Project Structure

```
project-name/
├── pyproject.toml             # Modern Python packaging
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .env                       # Environment variables
├── .env.example              # Example environment file
├── Dockerfile
├── docker-compose.yml
├── src/
│   └── project_name/          # Main package
│       ├── __init__.py
│       ├── main.py            # Application entry point
│       ├── config.py          # Configuration management
│       ├── api/               # API routes
│       │   ├── __init__.py
│       │   ├── dependencies.py
│       │   └── routes/
│       │       ├── __init__.py
│       │       ├── dashboard.py
│       │       └── health.py
│       ├── core/              # Core business logic
│       │   ├── __init__.py
│       │   └── security.py
│       ├── models/            # Data models
│       │   ├── __init__.py
│       │   ├── schemas.py     # Pydantic schemas
│       │   └── database.py    # SQLAlchemy models
│       ├── services/          # Business logic services
│       │   ├── __init__.py
│       │   └── dashboard_service.py
│       ├── static/            # Static files (CSS, JS)
│       │   ├── css/
│       │   │   └── tokens.css
│       │   └── js/
│       └── templates/         # Jinja2 templates
│           ├── base.html
│           └── dashboard.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_dashboard.py
└── scripts/
    └── validate_tokens.py
```

## Core Files

### pyproject.toml

```toml
[project]
name = "{{PROJECT_NAME}}"
version = "1.0.0"
description = "{{PROJECT_DESCRIPTION}}"
readme = "README.md"
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
    "mypy>=1.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/project_name"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

### requirements.txt

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
jinja2>=3.1.0
```

### src/project_name/main.py

```python
"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .api.routes import dashboard, health
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name}...")
    yield
    # Shutdown
    print("Shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        lifespan=lifespan,
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory="src/project_name/static"), name="static")

    # Include routers
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### src/project_name/config.py

```python
"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "{{PROJECT_NAME}}"
    version: str = "1.0.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database (if needed)
    # database_url: str = "sqlite:///./app.db"


settings = Settings()
```

### src/project_name/api/routes/health.py

```python
"""Health check routes."""

from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: datetime
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check API health status."""
    from ...config import settings

    return HealthResponse(
        status="ok",
        timestamp=datetime.now(),
        version=settings.version,
    )
```

### src/project_name/api/routes/dashboard.py

```python
"""Dashboard routes."""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


router = APIRouter()
templates = Jinja2Templates(directory="src/project_name/templates")


class KPIData(BaseModel):
    """KPI data model."""

    label: str
    value: int
    trend: float
    trend_direction: str


class DashboardData(BaseModel):
    """Dashboard data model."""

    kpis: list[KPIData]


@router.get("/dashboard")
async def get_dashboard(request: Request):
    """Render dashboard page."""
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "theme": "light",
            "title": "Dashboard",
        }
    )


@router.get("/dashboard/data", response_model=DashboardData)
async def get_dashboard_data() -> DashboardData:
    """Get dashboard data as JSON."""
    return DashboardData(
        kpis=[
            KPIData(label="Total Threats", value=1234, trend=15.3, trend_direction="up"),
            KPIData(label="Blocked Attacks", value=892, trend=8.2, trend_direction="up"),
            KPIData(label="Active Alerts", value=23, trend=-5.1, trend_direction="down"),
        ]
    )
```

### src/project_name/templates/base.html

```html
<!DOCTYPE html>
<html lang="en" data-theme="{{ theme | default('light') }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }} - {{PROJECT_NAME}}</title>

  <!-- Design tokens FIRST -->
  <link rel="stylesheet" href="{{ url_for('static', path='css/tokens.css') }}">
  <!-- Component styles -->
  <link rel="stylesheet" href="{{ url_for('static', path='css/dashboard.css') }}">

  <script>
    // Theme toggle
    (function() {
      const theme = localStorage.getItem('theme') || 'light';
      document.documentElement.setAttribute('data-theme', theme);
    })();
  </script>
</head>
<body>
  {% block content %}{% endblock %}

  <script>
    // Theme toggle button
    function toggleTheme() {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    }
  </script>
</body>
</html>
```

### src/project_name/templates/dashboard.html

```html
{% extends "base.html" %}

{% block content %}
<div class="dashboard">
  <header class="dashboard__header">
    <h1>Dashboard</h1>
    <button onclick="toggleTheme()" class="theme-toggle">
      Toggle Theme
    </button>
  </header>

  <main class="dashboard__content">
    <section class="kpi-grid" id="kpi-container">
      <!-- KPI cards loaded via JavaScript -->
    </section>
  </main>
</div>

<script>
  // Fetch and render KPI data
  async function loadDashboard() {
    const response = await fetch('/api/dashboard/data');
    const data = await response.json();

    const container = document.getElementById('kpi-container');
    container.innerHTML = data.kpis.map(kpi => `
      <div class="kpi-card">
        <h3 class="kpi-card__label">${kpi.label}</h3>
        <div class="kpi-card__value">${kpi.value.toLocaleString()}</div>
        <div class="kpi-card__trend trend--${kpi.trend_direction === 'up' ? 'positive' : 'negative'}">
          ${kpi.trend_direction === 'up' ? '↑' : '↓'} ${Math.abs(kpi.trend)}%
        </div>
      </div>
    `).join('');
  }

  loadDashboard();
</script>
{% endblock %}
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/

# Run application
CMD ["uvicorn", "src.project_name.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
    environment:
      - DEBUG=true
    command: uvicorn src.project_name.main:app --host 0.0.0.0 --port 8000 --reload
```

## Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -e ".[dev]"

# Start development server
uvicorn src.project_name.main:app --reload

# Validate CSS tokens
python scripts/validate_tokens.py src/project_name/static

# Run tests
pytest

# Type checking
mypy src/

# Linting
ruff check src/
```

## Integration Checklist

- [ ] `tokens.css` exists in static/css/
- [ ] Templates load tokens.css before other styles
- [ ] Theme toggle updates `data-theme` attribute
- [ ] Pydantic models validate all API data
- [ ] Configuration uses pydantic-settings
- [ ] Tests cover critical endpoints
- [ ] Dockerfile builds successfully
