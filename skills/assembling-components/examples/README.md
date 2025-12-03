# Assembly Examples

This directory contains example implementations demonstrating the assembling-components skill.

## Available Examples

### Existing Dashboard Example

The Palo Alto Security Dashboard in `demo/examples/palo-alto-security-dashboard/` serves as a reference implementation showing:

- Complete token system integration
- Theme toggle with dark mode support
- Component composition (KPICard, DonutChart, Toast, Spinner)
- Proper CSS token usage

### Generating New Examples

Use the scaffolding script to create new project examples:

```bash
# React + Vite
python scripts/generate_scaffold.py react-dashboard react-vite ./examples

# Next.js
python scripts/generate_scaffold.py nextjs-dashboard nextjs ./examples

# Python FastAPI
python scripts/generate_scaffold.py fastapi-dashboard python-fastapi ./examples

# Rust Axum
python scripts/generate_scaffold.py rust-dashboard rust-axum ./examples
```

## Validation

After creating or modifying examples, validate them:

```bash
# Validate CSS tokens
python scripts/validate_tokens.py examples/react-dashboard/src

# Check import chains
python scripts/check_imports.py examples/react-dashboard/src

# Generate barrel exports
python scripts/generate_exports.py examples/react-dashboard/src/components
```

## Example Structure

Each example should follow this structure:

```
example-name/
├── src/
│   ├── main.tsx              # Entry point
│   ├── App.tsx               # Root component
│   ├── styles/
│   │   ├── tokens.css        # Design tokens (imported FIRST)
│   │   └── globals.css       # Global styles
│   ├── context/
│   │   └── theme-provider.tsx
│   ├── components/
│   │   ├── ui/               # Shared UI components
│   │   │   └── index.ts      # Barrel export
│   │   ├── layout/           # Layout components
│   │   │   └── index.ts
│   │   └── features/         # Feature components
│   │       └── dashboard/
│   │           └── index.ts
│   └── lib/
│       └── utils.ts
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Integration Checklist

Before considering an example complete:

- [ ] `tokens.css` exists and is imported first
- [ ] All CSS uses token variables (no hardcoded values)
- [ ] ThemeProvider wraps the app
- [ ] Theme toggle works (light/dark)
- [ ] Barrel exports exist for component directories
- [ ] Build completes without errors
- [ ] `npm run validate:tokens` passes
