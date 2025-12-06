# Basic Table Patterns

Foundational patterns for HTML tables, simple React tables, and accessibility compliance.


## Table of Contents

- [Semantic HTML Table](#semantic-html-table)
- [Basic React Table](#basic-react-table)
- [Responsive Wrapper](#responsive-wrapper)
- [Empty State](#empty-state)
- [Loading State](#loading-state)
- [Accessibility](#accessibility)
- [Best Practices](#best-practices)
- [Sticky Header](#sticky-header)
- [Resources](#resources)

## Semantic HTML Table

```html
<table>
  <caption>User List</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
      <th scope="col">Status</th>
      <th scope="col">Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">John Doe</th>
      <td>john@example.com</td>
      <td>Active</td>
      <td><button>Edit</button></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="4">Total: 156 users</td>
    </tr>
  </tfoot>
</table>
```

**Key elements:**
- `<caption>` - Table title for screen readers
- `scope="col"` - Column headers
- `scope="row"` - Row headers (first column)
- `<tfoot>` - Summary row

## Basic React Table

```tsx
interface User {
  id: number;
  name: string;
  email: string;
  status: 'active' | 'inactive';
}

function BasicTable({ data }: { data: User[] }) {
  return (
    <table className="w-full border-collapse">
      <thead>
        <tr className="bg-gray-100">
          <th className="p-3 text-left">Name</th>
          <th className="p-3 text-left">Email</th>
          <th className="p-3 text-left">Status</th>
        </tr>
      </thead>
      <tbody>
        {data.map((user) => (
          <tr key={user.id} className="border-b">
            <td className="p-3">{user.name}</td>
            <td className="p-3">{user.email}</td>
            <td className="p-3">
              <span className={user.status === 'active' ? 'text-green-600' : 'text-gray-400'}>
                {user.status}
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Responsive Wrapper

```tsx
function ResponsiveTable({ children }: { children: React.ReactNode }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full">
        {children}
      </table>
    </div>
  );
}
```

## Empty State

```tsx
function TableWithEmpty({ data }: { data: any[] }) {
  if (data.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <div className="text-4xl mb-4">📋</div>
        <p>No data available</p>
      </div>
    );
  }

  return <BasicTable data={data} />;
}
```

## Loading State

```tsx
function TableSkeleton({ rows = 5, cols = 4 }) {
  return (
    <table className="w-full">
      <tbody>
        {Array.from({ length: rows }).map((_, i) => (
          <tr key={i}>
            {Array.from({ length: cols }).map((_, j) => (
              <td key={j} className="p-3">
                <div className="h-4 bg-gray-200 rounded animate-pulse" />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## Accessibility

```tsx
<table
  role="table"
  aria-label="User data table"
  aria-describedby="table-description"
>
  <caption id="table-description">
    List of users with name, email, and status
  </caption>
  {/* ... */}
</table>
```

## Best Practices

1. **Use semantic HTML** - `<table>`, `<th>`, `<td>`, not divs
2. **Add caption** - Describes table purpose
3. **Scope attributes** - `scope="col"` and `scope="row"`
4. **Keyboard navigation** - Tab through interactive cells
5. **Responsive wrapper** - Horizontal scroll on mobile
6. **Loading states** - Skeleton during fetch
7. **Empty states** - Clear message when no data
8. **Stripe rows** - Alternating background colors
9. **Sticky header** - Header visible during scroll
10. **ARIA labels** - For screen readers

## Sticky Header

```css
thead {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

## Resources

- MDN Table: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table
- WCAG Tables: https://www.w3.org/WAI/tutorials/tables/
