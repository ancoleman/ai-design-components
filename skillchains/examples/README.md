# Skill Chain Examples

**Working code demonstrating skill chaining patterns**

---

## Available Examples

### Current Examples (Skills Complete)

**1. themed-sales-dashboard.tsx**
- **Chain:** design-tokens + data-viz + forms
- **Pattern:** Parallel composition
- **Features:** Interactive filters, themed charts
- **Skills:** 3
- **Token efficiency:** 80%

---

## Running Examples

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

---

## Example Structure

Each example demonstrates:
- ✅ Multi-skill coordination
- ✅ Token usage from design-tokens
- ✅ Theme switching support
- ✅ RTL/i18n compatibility
- ✅ Accessibility features

---

## Future Examples (When Skills Complete)

**2. data-table-with-charts.tsx** (Requires: tables)
- Chain: design-tokens + tables + data-viz
- Pattern: Linear chain
- Features: Sortable table with embedded sparklines

**3. ai-chat-interface.tsx** (Requires: ai-chat)
- Chain: design-tokens + ai-chat + forms
- Pattern: Hub-and-spoke
- Features: Themed chat UI with input forms

**4. full-admin-panel.tsx** (Requires: dashboards, tables, navigation)
- Chain: design-tokens + dashboards + tables + data-viz + forms + navigation
- Pattern: Parallel composition
- Features: Complete admin interface

---

## Integration

To use these examples in your project:

```tsx
// 1. Import design-tokens CSS
import '../skills/design-tokens/build/css/variables.css';
import '../skills/design-tokens/build/css/variables-dark.css';

// 2. Wrap with ThemeProvider
import { ThemeProvider } from '../skills/design-tokens/examples/ThemeProvider';

// 3. Use example component
import { ThemedSalesDashboard } from './themed-sales-dashboard';

function App() {
  return (
    <ThemeProvider>
      <ThemedSalesDashboard />
    </ThemeProvider>
  );
}
```

---

**Status:** 1 example complete, 3 planned
**Skills required:** design-tokens (✅), data-viz (✅), forms (✅)
