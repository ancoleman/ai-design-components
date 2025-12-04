# Responsive Table Strategies

Patterns for making data tables work on mobile devices.

## Strategy 1: Horizontal Scroll

**Simplest - wraps table in scrollable container.**

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

**Pros:** Simple, preserves table structure
**Cons:** Horizontal scrolling on mobile is poor UX

## Strategy 2: Card Layout (Mobile)

**Transform table rows into cards on mobile.**

```tsx
function ResponsiveDataTable({ data }: { data: User[] }) {
  return (
    <>
      {/* Desktop: Table */}
      <table className="hidden md:table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id}>
              <td>{row.name}</td>
              <td>{row.email}</td>
              <td>{row.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Mobile: Cards */}
      <div className="md:hidden space-y-4">
        {data.map((row) => (
          <div key={row.id} className="border rounded-lg p-4">
            <div className="font-semibold">{row.name}</div>
            <div className="text-sm text-gray-600">{row.email}</div>
            <div className="mt-2">
              <span className={`px-2 py-1 rounded text-xs ${
                row.status === 'active' ? 'bg-green-100' : 'bg-gray-100'
              }`}>
                {row.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
```

**Pros:** Optimized for mobile, better UX
**Cons:** More code, duplicate rendering logic

## Strategy 3: Priority Columns

**Show important columns, hide others on mobile.**

```tsx
const columns = [
  { id: 'name', header: 'Name', priority: 1 },           // Always visible
  { id: 'email', header: 'Email', priority: 2 },         // Hidden on mobile
  { id: 'phone', header: 'Phone', priority: 3 },         // Hidden on tablet
  { id: 'address', header: 'Address', priority: 4 },     // Hidden on mobile/tablet
  { id: 'actions', header: 'Actions', priority: 1 },     // Always visible
];

<table>
  <thead>
    <tr>
      {columns.map((col) => (
        <th
          key={col.id}
          className={`
            ${col.priority > 2 ? 'hidden lg:table-cell' : ''}
            ${col.priority > 1 ? 'hidden md:table-cell' : ''}
          `}
        >
          {col.header}
        </th>
      ))}
    </tr>
  </thead>
</table>
```

## Strategy 4: Accordion Table

**Each row expands to show all data.**

```tsx
function AccordionTable({ data }: { data: User[] }) {
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  return (
    <div className="md:hidden">
      {data.map((row) => (
        <div key={row.id} className="border-b">
          <div
            onClick={() => {
              setExpanded((prev) => {
                const next = new Set(prev);
                next.has(row.id) ? next.delete(row.id) : next.add(row.id);
                return next;
              });
            }}
            className="flex justify-between p-4 cursor-pointer"
          >
            <span className="font-semibold">{row.name}</span>
            <span>{expanded.has(row.id) ? '▼' : '▶'}</span>
          </div>

          {expanded.has(row.id) && (
            <div className="p-4 bg-gray-50 space-y-2">
              <div><strong>Email:</strong> {row.email}</div>
              <div><strong>Phone:</strong> {row.phone}</div>
              <div><strong>Address:</strong> {row.address}</div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
```

## Strategy 5: Stacked Labels

**Labels inline with each value on mobile.**

```tsx
<table className="md:table-auto">
  <thead className="hidden md:table-header-group">
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    {data.map((row) => (
      <tr key={row.id} className="block md:table-row border-b md:border-0">
        <td className="block md:table-cell before:content-['Name:'] before:font-semibold before:mr-2 md:before:content-none">
          {row.name}
        </td>
        <td className="block md:table-cell before:content-['Email:'] before:font-semibold before:mr-2 md:before:content-none">
          {row.email}
        </td>
        <td className="block md:table-cell before:content-['Status:'] before:font-semibold before:mr-2 md:before:content-none">
          {row.status}
        </td>
      </tr>
    ))}
  </tbody>
</table>
```

## Comparison

| Strategy | Complexity | UX (Mobile) | UX (Desktop) | Best For |
|----------|------------|-------------|--------------|----------|
| Horizontal Scroll | Low | Poor | Good | Quick implementation |
| Card Layout | Medium | Excellent | N/A | Mobile-first apps |
| Priority Columns | Low | Good | Good | 5-8 columns max |
| Accordion | Medium | Good | N/A | Many columns (10+) |
| Stacked Labels | Low | Good | Good | Small tables (3-5 cols) |

## Best Practices

1. **Test on real devices** - Don't rely on browser emulation
2. **Touch targets 44px min** - Buttons, checkboxes, links
3. **Reduce columns** - Show only essential on mobile
4. **Horizontal scroll as fallback** - If other strategies don't fit
5. **Fixed first column** - Keep name/ID visible during scroll
6. **Expandable details** - Hide secondary info, expand on tap
7. **Search/filter first** - Reduce rows before displaying

## Resources

- Responsive Tables: https://css-tricks.com/responsive-data-tables/
- Mobile UX: https://www.nngroup.com/articles/mobile-tables/
