# Form Component Selection Decision Tree

**Universal framework for selecting the appropriate form input component based on data type and requirements.**


## Table of Contents

- [The Golden Rule](#the-golden-rule)
- [Complete Decision Tree](#complete-decision-tree)
  - [Short Text (<100 characters)](#short-text-100-characters)
  - [Long Text (>100 characters)](#long-text-100-characters)
  - [Numeric Values](#numeric-values)
  - [Date & Time](#date-time)
  - [Boolean (Yes/No, True/False)](#boolean-yesno-truefalse)
  - [Single Choice (Select one option)](#single-choice-select-one-option)
  - [Multiple Choice (Select multiple options)](#multiple-choice-select-multiple-options)
  - [File & Media](#file-media)
  - [Color Selection](#color-selection)
  - [Structured & Complex Data](#structured-complex-data)
  - [Rating & Feedback](#rating-feedback)
- [Decision Helpers](#decision-helpers)
  - [When to use Autocomplete vs. Select Dropdown?](#when-to-use-autocomplete-vs-select-dropdown)
  - [When to use Checkbox vs. Toggle Switch?](#when-to-use-checkbox-vs-toggle-switch)
  - [When to use Radio Group vs. Select Dropdown?](#when-to-use-radio-group-vs-select-dropdown)
  - [When to use Text Input vs. Autocomplete?](#when-to-use-text-input-vs-autocomplete)
- [Mobile-Specific Considerations](#mobile-specific-considerations)
  - [Input Type → Keyboard Type](#input-type-keyboard-type)
- [Quick Reference Table](#quick-reference-table)
- [Anti-Patterns (What NOT to Do)](#anti-patterns-what-not-to-do)
- [Next Steps](#next-steps)

## The Golden Rule

**Data Type → Input Component → Validation Pattern**

Always start by identifying:
1. **What type of data** are you collecting?
2. **How many options** are there (for choices)?
3. **What constraints** exist (min/max, format, required)?

## Complete Decision Tree

### Short Text (<100 characters)

**Free-form text?**
→ **Text Input**
- Use for: Names, titles, simple text
- HTML: `<input type="text">`
- Validation: Min/max length, pattern matching
- Example: First name, job title, city name

**Email address?**
→ **Email Input**
- Use for: Email addresses
- HTML: `<input type="email">`
- Validation: Email format (RFC 5322), domain verification
- Mobile: Shows email keyboard (@, .)
- Example: user@example.com

**Password?**
→ **Password Input**
- Use for: Passwords, PINs, secrets
- HTML: `<input type="password">`
- Features: Visibility toggle, strength meter
- Validation: Min length, complexity requirements
- Example: Login password, new password

**Phone number?**
→ **Tel Input**
- Use for: Phone numbers
- HTML: `<input type="tel">`
- Features: International formatting, country code selector
- Mobile: Shows numeric keyboard
- Validation: Format by country (E.164 standard)
- Example: (555) 123-4567, +1-555-123-4567

**URL/Website?**
→ **URL Input**
- Use for: Web addresses
- HTML: `<input type="url">`
- Validation: Protocol, domain, valid URL structure
- Example: https://example.com

**Search query?**
→ **Search Input**
- Use for: Search/filter interfaces
- HTML: `<input type="search">`
- Features: Clear button, suggestions, autocomplete
- Example: Search products, filter results

---

### Long Text (>100 characters)

**Plain text without formatting?**
→ **Textarea**
- Use for: Comments, descriptions, notes
- HTML: `<textarea>`
- Features: Resizable, character count
- Validation: Max length, word count
- Example: Product description, feedback

**Rich text with formatting (bold, italic, lists)?**
→ **Rich Text Editor**
- Use for: Content creation, blog posts
- Features: Formatting toolbar, media insertion
- Libraries: TipTap, Slate, Quill
- Example: Blog post editor, email composer

**Code or technical content?**
→ **Code Editor**
- Use for: Code snippets, JSON, configuration
- Features: Syntax highlighting, linting, autocomplete
- Libraries: Monaco Editor, CodeMirror
- Example: API configuration, custom CSS

**Markdown content?**
→ **Markdown Editor**
- Use for: Documentation, README files
- Features: Live preview, formatting shortcuts
- Libraries: react-markdown-editor, SimpleMDE
- Example: Project documentation, GitHub-style editor

---

### Numeric Values

**Integer (whole numbers)?**
→ **Number Input (step=1)**
- Use for: Age, quantity, count
- HTML: `<input type="number" step="1">`
- Features: Increment/decrement buttons
- Validation: Min/max range, integer only
- Example: Quantity (1, 2, 3), Age (18, 25)

**Decimal (floating point)?**
→ **Number Input (step=0.01)**
- Use for: Measurements, ratings
- HTML: `<input type="number" step="0.01">`
- Validation: Min/max, decimal precision
- Example: Weight (65.5 kg), Rating (4.5)

**Currency (money)?**
→ **Currency Input**
- Use for: Prices, salaries, financial amounts
- Features: Currency symbol, decimal handling, thousand separators
- Validation: Non-negative, max decimals
- Example: $1,234.56, €500.00

**Percentage (0-100)?**
→ **Percentage Input**
- Use for: Discounts, completion, ratios
- Features: % symbol, 0-100 constraint
- Validation: Min 0, max 100
- Example: 15% off, 75% complete

**Value in range?**
→ **Slider / Range Input**
- Use for: Volume, brightness, price ranges
- HTML: `<input type="range">`
- Features: Visual feedback, dual handles (min/max)
- Best for: Continuous values, approximate selection
- Example: Price filter $50-$500, Volume 0-100

---

### Date & Time

**Single date selection?**
→ **Date Picker**
- Use for: Birthday, event date, deadline
- HTML: `<input type="date">`
- Features: Calendar interface, min/max dates, disabled dates
- Validation: Date range, not in past/future
- Example: Date of birth, appointment date

**Date range (start and end)?**
→ **Date Range Picker**
- Use for: Booking periods, report date ranges
- Features: Two calendars, visual range selection
- Validation: End date after start date
- Example: Hotel booking (check-in/check-out), Date filter

**Time only?**
→ **Time Picker**
- Use for: Appointment times, schedules
- HTML: `<input type="time">`
- Features: 12/24 hour format, step intervals
- Example: Meeting time (2:30 PM), Opening hours

**Date and time combined?**
→ **DateTime Picker**
- Use for: Event scheduling, timestamps
- HTML: `<input type="datetime-local">`
- Features: Combined calendar and time selection
- Example: Event start (Dec 25, 2025 2:00 PM)

**Duration (elapsed time)?**
→ **Duration Input**
- Use for: Timer values, time tracking
- Features: Hours, minutes, seconds inputs
- Example: Video length (1h 23m), Task duration

---

### Boolean (Yes/No, True/False)

**Single on/off choice?**
→ **Checkbox**
- Use for: Agreements, opt-ins, toggles
- HTML: `<input type="checkbox">`
- Best for: Required acceptance (terms of service)
- Example: "I agree to terms", "Subscribe to newsletter"

**Clear binary state (on/off, enabled/disabled)?**
→ **Toggle Switch**
- Use for: Settings, feature flags
- Better UX: Immediate visual feedback of state
- Best for: Actions that take effect immediately
- Example: Enable notifications, Dark mode

**Part of mutually exclusive group?**
→ **Radio Group** (see Single Choice section)

---

### Single Choice (Select one option)

**2-5 options, all should be visible?**
→ **Radio Group**
- Use for: Small, mutually exclusive choices
- HTML: `<input type="radio" name="group">`
- Best for: Visible options, clear comparison
- Layout: Vertical (preferred) or horizontal
- Example: Gender (Male/Female/Other), Shipping method (Standard/Express)

**6-15 options?**
→ **Select Dropdown**
- Use for: Medium-sized option lists
- HTML: `<select>`
- Best for: Known categories, conserving space
- Features: Search within options (native or enhanced)
- Example: Country selection, Department

**More than 15 options?**
→ **Autocomplete / Combobox**
- Use for: Large option lists
- Features: Type to filter, keyboard navigation
- Best for: Searchable lists (cities, products, users)
- Example: City (1000s of options), Product search

**Need search functionality?**
→ **Autocomplete with Search**
- Features: Server-side search, debouncing
- Best for: Very large datasets, API-backed options
- Example: User search, Product catalog

---

### Multiple Choice (Select multiple options)

**2-7 options, all visible?**
→ **Checkbox Group**
- Use for: Small set of related options
- HTML: Multiple `<input type="checkbox">`
- Layout: Vertical list
- Example: Interests (Sports, Music, Art), Features to enable

**8-20 options?**
→ **Multi-Select Dropdown**
- Use for: Medium-sized lists, multiple selections
- HTML: `<select multiple>`
- Features: Select/deselect all, selected count
- Example: Skills selection, Categories

**More than 20 options?**
→ **Transfer List** or **Autocomplete Multi**
- Transfer List: Two columns (available/selected)
- Autocomplete Multi: Type to add, chips for selected
- Best for: Large lists, clear visual of selections
- Example: Assign permissions, Email recipients

**Free-form tags (user can create)?**
→ **Tag Input**
- Use for: User-generated tags, keywords
- Features: Autocomplete existing, create new, remove chips
- Example: Article tags, Email addresses

---

### File & Media

**Single file upload?**
→ **File Upload**
- Use for: Resume, avatar, document
- HTML: `<input type="file">`
- Features: File type restriction, size validation
- Example: Upload resume (PDF), Profile picture

**Multiple files?**
→ **Multi-File Upload**
- Use for: Photo galleries, document batches
- HTML: `<input type="file" multiple>`
- Features: Drag-and-drop zone, progress bars, preview
- Example: Upload product images, Attach documents

**Images only (with preview/editing)?**
→ **Image Upload**
- Use for: Profile pictures, product photos
- Features: Preview, crop, resize, rotate
- Validation: Image format, dimensions, file size
- Example: Avatar upload, Product photo

**Specific file format?**
→ **File Upload with Type Restriction**
- Features: Accept only specific MIME types
- Validation: File extension, MIME type verification
- Example: Upload CSV, Upload video (MP4)

---

### Color Selection

**Any color needed?**
→ **Color Picker**
- Use for: Theme customization, design tools
- HTML: `<input type="color">`
- Features: Hex, RGB, HSL inputs, swatches
- Example: Brand color, Background color

**Limited color palette?**
→ **Color Swatches**
- Use for: Predefined color options
- Better UX: Visual selection of preset colors
- Example: Product color (Red, Blue, Green)

---

### Structured & Complex Data

**Address (street, city, postal code)?**
→ **Address Input**
- Use for: Shipping, billing addresses
- Features: Multi-field, autocomplete (Google Places), validation by country
- Fields: Street, city, state/province, postal code, country
- Example: Shipping address, Business location

**Credit card details?**
→ **Credit Card Input**
- Use for: Payment information
- Features: Card type detection, Luhn validation, formatting, CVV masking
- Fields: Card number, expiry, CVV, name
- Security: Never store raw card data
- Example: Checkout payment

**Phone number (international)?**
→ **Phone Number Input**
- Use for: International phone numbers
- Features: Country code selector, format by region, validation
- Standard: E.164 format (+1234567890)
- Example: Contact phone, WhatsApp number

**List of items (dynamic)?**
→ **Field Array / Repeating Section**
- Use for: Multiple related items
- Features: Add/remove rows, reorder
- Example: Multiple email addresses, Line items in invoice

**Nested object (complex structure)?**
→ **Nested Form** or **Accordion**
- Use for: Hierarchical data
- Best for: Complex objects, grouped data
- Example: User profile (personal info, address, preferences)

---

### Rating & Feedback

**Rating scale (1-5 or 1-10)?**
→ **Star Rating** or **Radio Group**
- Use for: Product reviews, satisfaction surveys
- Star Rating: Visual, 1-5 common
- Radio Group: Precise scale (1-10)
- Example: Rate your experience (⭐⭐⭐⭐⭐)

**Satisfaction level?**
→ **Emoji Rating**
- Use for: Quick feedback, user sentiment
- Features: Visual emoji scale (😞 😐 😊)
- Best for: Simple, emotional responses
- Example: How was your experience?

**Net Promoter Score (NPS)?**
→ **0-10 Scale with Labels**
- Use for: Customer loyalty measurement
- Layout: 0-10 with labels (Detractor/Passive/Promoter)
- Example: How likely are you to recommend us?

---

## Decision Helpers

### When to use Autocomplete vs. Select Dropdown?

**Use Select Dropdown when:**
- 6-15 options
- Options are well-known categories
- User knows what they're looking for
- Options fit in dropdown without scroll

**Use Autocomplete when:**
- More than 15 options
- Need search/filter functionality
- Options are searchable (cities, products, names)
- Better mobile experience needed

### When to use Checkbox vs. Toggle Switch?

**Use Checkbox when:**
- Part of a form that requires submission
- User must explicitly agree (terms of service)
- Multiple related options (checkbox group)
- Effect happens on form submit

**Use Toggle Switch when:**
- Settings that take effect immediately
- Clear binary state (on/off, enabled/disabled)
- Modern UI, app-like interface
- Single standalone option

### When to use Radio Group vs. Select Dropdown?

**Use Radio Group when:**
- 2-5 options
- All options should be visible for comparison
- Options are short (1-3 words)
- Frequently used, important choices

**Use Select Dropdown when:**
- 6+ options
- Space is limited
- Options are longer text
- Less frequently used

### When to use Text Input vs. Autocomplete?

**Use Text Input when:**
- Truly free-form (no predefined options)
- Value is unique (name, custom text)
- No common suggestions available

**Use Autocomplete when:**
- Predefined options exist but user can add new
- Common values can be suggested
- Better UX with autocomplete
- Want to reduce typos

---

## Mobile-Specific Considerations

### Input Type → Keyboard Type

Choosing the correct input type automatically shows the appropriate mobile keyboard:

| Input Type | Mobile Keyboard | Best For |
|------------|-----------------|----------|
| `type="text"` | Standard QWERTY | General text |
| `type="email"` | Email (@ key) | Email addresses |
| `type="tel"` | Numeric dialpad | Phone numbers |
| `type="number"` | Numeric | Numbers, quantities |
| `type="url"` | URL (.com, /) | Website addresses |
| `type="search"` | Search (Go button) | Search queries |
| `type="date"` | Date picker | Date selection |
| `type="time"` | Time picker | Time selection |

**Impact:** Improves mobile UX by showing the right keyboard for the data type.

---

## Quick Reference Table

| Data Type | Primary Choice | Alternative | Example |
|-----------|----------------|-------------|---------|
| Short text | Text input | - | First name |
| Email | Email input | - | user@example.com |
| Password | Password input | - | Login password |
| Phone | Tel input | Phone input component | (555) 123-4567 |
| URL | URL input | - | https://example.com |
| Long text | Textarea | Rich text editor | Description |
| Number | Number input | Slider | Quantity (5) |
| Currency | Currency input | Number input | $99.99 |
| Date | Date picker | - | 2025-12-25 |
| Date range | Date range picker | Two date pickers | Check-in to Check-out |
| Time | Time picker | - | 2:30 PM |
| Boolean | Checkbox | Toggle switch | I agree |
| 2-5 choices | Radio group | Select | Shipping method |
| 6-15 choices | Select dropdown | Radio group | Country |
| 15+ choices | Autocomplete | Select with search | City |
| Multi-choice (few) | Checkbox group | - | Interests |
| Multi-choice (many) | Multi-select | Transfer list | Skills |
| Tags | Tag input | - | Keywords |
| File | File upload | - | Resume (PDF) |
| Image | Image upload | File upload | Profile picture |
| Color | Color picker | Swatches | Brand color |
| Address | Address input | Multiple text inputs | Shipping address |
| Credit card | Card input | Separate inputs | Payment details |
| Rating | Star rating | Radio group | Product rating |

---

## Anti-Patterns (What NOT to Do)

❌ **Don't use text input for dates** → Use date picker
❌ **Don't use dropdown for 2-3 options** → Use radio group
❌ **Don't use radio group for 10+ options** → Use select or autocomplete
❌ **Don't use select for boolean** → Use checkbox or toggle
❌ **Don't use textarea for single-line text** → Use text input
❌ **Don't use text input for email** → Use email input (mobile keyboard!)
❌ **Don't use text input for large option list** → Use autocomplete
❌ **Don't use placeholder as label** → Use explicit `<label>`

---

## Next Steps

After selecting the appropriate component:

1. **Implement validation** → See `validation-concepts.md`
2. **Ensure accessibility** → See `accessibility-forms.md`
3. **Apply UX patterns** → See `ux-patterns.md`
4. **Choose language implementation:**
   - JavaScript/React → `javascript/react-hook-form.md`
   - Python → `python/pydantic-forms.md`
