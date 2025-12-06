# Form UX Patterns & Best Practices

**Modern user experience patterns for forms (2024-2025), covering progressive disclosure, smart defaults, mobile-first design, and cognitive load reduction.**


## Table of Contents

- [Core UX Principles for Forms](#core-ux-principles-for-forms)
  - [The Three Goals of Excellent Form UX](#the-three-goals-of-excellent-form-ux)
- [Modern Form UX Patterns (2024-2025)](#modern-form-ux-patterns-2024-2025)
  - [1. Progressive Disclosure](#1-progressive-disclosure)
  - [2. Smart Defaults](#2-smart-defaults)
  - [3. Inline Validation with Positive Feedback](#3-inline-validation-with-positive-feedback)
  - [4. Mobile-First Considerations](#4-mobile-first-considerations)
  - [5. Reduce Cognitive Load](#5-reduce-cognitive-load)
  - [6. Error Prevention](#6-error-prevention)
  - [7. Autosave and Recovery](#7-autosave-and-recovery)
- [UX Anti-Patterns (What NOT to Do)](#ux-anti-patterns-what-not-to-do)
  - [Common UX Mistakes](#common-ux-mistakes)
- [UX Testing Checklist](#ux-testing-checklist)
  - [Manual Testing](#manual-testing)
  - [Analytics to Monitor](#analytics-to-monitor)
- [Summary: UX Best Practices](#summary-ux-best-practices)
- [Next Steps](#next-steps)

## Core UX Principles for Forms

### The Three Goals of Excellent Form UX

1. **Minimize user effort** - Reduce typing, clicks, and cognitive load
2. **Prevent errors** - Design to avoid mistakes before they happen
3. **Provide clear feedback** - Help users understand what's happening

**Success Metrics:**
- High completion rate (users finish the form)
- Low error rate (few validation failures)
- Fast completion time (users move through quickly)
- Low abandonment rate (users don't give up)

---

## Modern Form UX Patterns (2024-2025)

### 1. Progressive Disclosure

**Principle:** Show only essential fields initially, reveal advanced options on demand.

**Benefits:**
- Reduces cognitive load
- Appears less daunting (fewer fields visible)
- Focuses user attention
- Maintains advanced functionality

**When to Use:**
- Forms with 10+ fields
- Mix of required and optional fields
- Advanced/expert settings
- Conditional fields based on user type

---

#### Pattern 1A: Show More / Show Less

```html
<!-- Initial view: Essential fields only -->
<form>
  <input type="text" id="name" placeholder="Name" />
  <input type="email" id="email" placeholder="Email" />
  <input type="tel" id="phone" placeholder="Phone" />

  <!-- Optional fields (hidden initially) -->
  <div id="optional-fields" hidden>
    <input type="text" id="company" placeholder="Company (optional)" />
    <input type="text" id="title" placeholder="Job Title (optional)" />
    <input type="url" id="website" placeholder="Website (optional)" />
  </div>

  <button type="button" onclick="toggleOptional()">
    + Show more fields
  </button>

  <button type="submit">Submit</button>
</form>
```

**Best Practices:**
- ✅ Clearly indicate fields are optional
- ✅ Use "Show more fields" not just "More"
- ✅ Change button text when expanded ("Show less fields")
- ✅ Maintain scroll position when toggling

---

#### Pattern 1B: Accordion Sections

```html
<form>
  <!-- Section 1: Always visible (required) -->
  <fieldset>
    <legend>Personal Information</legend>
    <input type="text" name="name" required />
    <input type="email" name="email" required />
  </fieldset>

  <!-- Section 2: Collapsible (optional) -->
  <details>
    <summary>Shipping Address (Optional)</summary>
    <fieldset>
      <input type="text" name="street" />
      <input type="text" name="city" />
      <input type="text" name="zip" />
    </fieldset>
  </details>

  <!-- Section 3: Collapsible (optional) -->
  <details>
    <summary>Additional Preferences (Optional)</summary>
    <fieldset>
      <label>
        <input type="checkbox" name="newsletter" />
        Subscribe to newsletter
      </label>
      <label>
        <input type="checkbox" name="notifications" />
        Enable notifications
      </label>
    </fieldset>
  </details>

  <button type="submit">Submit</button>
</form>
```

**Best Practices:**
- ✅ Use `<details>` and `<summary>` for native accordion
- ✅ Expand sections with errors automatically
- ✅ Remember user's expansion preferences
- ✅ Indicate section status (incomplete/complete)

---

#### Pattern 1C: Conditional Fields (Show Based on Answer)

```html
<form>
  <label>
    <input type="radio" name="account-type" value="personal" />
    Personal Account
  </label>
  <label>
    <input type="radio" name="account-type" value="business" />
    Business Account
  </label>

  <!-- Show only if "business" selected -->
  <div id="business-fields" hidden>
    <input type="text" name="company-name" placeholder="Company Name" />
    <input type="text" name="tax-id" placeholder="Tax ID" />
  </div>

  <button type="submit">Continue</button>
</form>

<script>
  document.querySelectorAll('[name="account-type"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      document.getElementById('business-fields').hidden =
        e.target.value !== 'business';
    });
  });
</script>
```

**Best Practices:**
- ✅ Show/hide immediately when selection changes
- ✅ Clear hidden field values when hidden
- ✅ Don't validate hidden fields
- ✅ Announce changes to screen readers (`aria-live`)

---

### 2. Smart Defaults

**Principle:** Pre-fill known information, suggest values, remember previous entries.

**Benefits:**
- Reduces typing effort
- Faster completion
- Fewer errors (typos)
- Better user experience

---

#### Pattern 2A: Auto-detect Values

```javascript
// Auto-detect timezone
const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
document.getElementById('timezone').value = timezone;

// Auto-detect language
const language = navigator.language || 'en-US';
document.getElementById('language').value = language;

// Auto-detect country (from IP - server-side)
fetch('/api/detect-country')
  .then(res => res.json())
  .then(data => {
    document.getElementById('country').value = data.country;
  });
```

**What to Auto-Detect:**
- Timezone
- Language/locale
- Country (from IP address)
- Currency (based on country)
- Date format preference

---

#### Pattern 2B: Remember Previous Entries

```javascript
// Save form data to localStorage
form.addEventListener('input', (e) => {
  localStorage.setItem(e.target.name, e.target.value);
});

// Restore on page load
document.addEventListener('DOMContentLoaded', () => {
  form.querySelectorAll('[name]').forEach(input => {
    const saved = localStorage.getItem(input.name);
    if (saved) input.value = saved;
  });
});

// Clear after successful submission
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const success = await submitForm();
  if (success) {
    localStorage.clear();
  }
});
```

**Best Practices:**
- ✅ Save drafts automatically (autosave)
- ✅ Restore on page refresh
- ✅ Clear after successful submission
- ✅ Respect privacy (don't save sensitive data like passwords)

---

#### Pattern 2C: Suggest Based on Context

```html
<!-- Email suggestion based on common domains -->
<input
  type="email"
  id="email"
  list="email-suggestions"
/>
<datalist id="email-suggestions">
  <option value="@gmail.com">
  <option value="@yahoo.com">
  <option value="@outlook.com">
  <option value="@hotmail.com">
</datalist>

<!-- Address autocomplete (Google Places API) -->
<input
  type="text"
  id="address"
  placeholder="Start typing address..."
  autocomplete="street-address"
/>
```

**What to Suggest:**
- Email domains (@gmail.com)
- Common addresses (via Google Places, USPS)
- Product names, categories
- Previously entered values
- Common responses

---

### 3. Inline Validation with Positive Feedback

**Principle:** Provide real-time feedback with both errors and success indicators.

**Modern Pattern (2024-2025):** Show errors AND success states

---

#### Pattern 3A: Success Indicators

```html
<div class="field">
  <label for="email">Email</label>
  <input type="email" id="email" aria-describedby="email-status" />

  <!-- Error state -->
  <p id="email-error" class="error-message" hidden>
    Please enter a valid email address
  </p>

  <!-- Success state (NEW in modern UX) -->
  <p id="email-success" class="success-message" hidden>
    <span aria-hidden="true">✓</span> Valid email format
  </p>
</div>

<style>
  /* Visual feedback via border color */
  .field input.valid {
    border-color: #22c55e; /* Green */
  }

  .field input.invalid {
    border-color: #ef4444; /* Red */
  }

  .success-message {
    color: #22c55e;
    font-size: 0.875rem;
  }

  .error-message {
    color: #ef4444;
    font-size: 0.875rem;
  }
</style>
```

**Best Practices:**
- ✅ Show green checkmark when field is valid
- ✅ Provide positive reinforcement
- ✅ Use color + icon (not color alone)
- ✅ Clear success message when field changes
- ⚠️ Don't overuse (can be distracting if every field has checkmark)

---

#### Pattern 3B: Password Strength Meter

```html
<div class="field">
  <label for="password">Password</label>
  <input
    type="password"
    id="password"
    aria-describedby="password-strength password-requirements"
  />

  <!-- Strength meter -->
  <div id="password-strength" class="strength-meter">
    <div class="strength-bar" data-strength="weak"></div>
    <span class="strength-text">Weak</span>
  </div>

  <!-- Requirements checklist -->
  <ul id="password-requirements" class="requirements">
    <li data-met="false">✗ At least 8 characters</li>
    <li data-met="false">✗ Contains uppercase letter</li>
    <li data-met="false">✗ Contains number</li>
    <li data-met="false">✗ Contains special character</li>
  </ul>
</div>

<script>
  passwordInput.addEventListener('input', (e) => {
    const value = e.target.value;
    const strength = calculateStrength(value); // weak, medium, strong

    // Update strength meter
    strengthBar.dataset.strength = strength;
    strengthText.textContent = strength.charAt(0).toUpperCase() + strength.slice(1);

    // Update requirements checklist
    updateRequirement(0, value.length >= 8);
    updateRequirement(1, /[A-Z]/.test(value));
    updateRequirement(2, /\d/.test(value));
    updateRequirement(3, /[!@#$%^&*]/.test(value));
  });
</script>
```

**Best Practices:**
- ✅ Show strength meter (Weak/Medium/Strong)
- ✅ Provide checklist of requirements
- ✅ Update in real-time (on-change)
- ✅ Use visual indicators (color, icons)
- ✅ Make requirements actionable

---

#### Pattern 3C: Real-Time Character Count

```html
<div class="field">
  <label for="tweet">Tweet</label>
  <textarea
    id="tweet"
    maxlength="280"
    aria-describedby="tweet-count"
  ></textarea>

  <!-- Character count -->
  <p id="tweet-count" aria-live="polite">
    <span id="current-count">0</span> / 280 characters
  </p>
</div>

<script>
  tweetTextarea.addEventListener('input', (e) => {
    const current = e.target.value.length;
    const max = 280;
    const remaining = max - current;

    currentCount.textContent = current;

    // Warning when approaching limit
    if (remaining < 20) {
      tweetCount.classList.add('warning');
    } else {
      tweetCount.classList.remove('warning');
    }

    // Error when over limit (if not using maxlength)
    if (remaining < 0) {
      tweetCount.classList.add('error');
    } else {
      tweetCount.classList.remove('error');
    }
  });
</script>
```

**Best Practices:**
- ✅ Show current count, not just remaining
- ✅ Warn when approaching limit (last 20 characters)
- ✅ Use `aria-live="polite"` for screen reader announcements
- ✅ Consider soft limit (warn) vs hard limit (prevent)

---

### 4. Mobile-First Considerations

**Principle:** Design for mobile devices first, enhance for desktop.

**Mobile Challenges:**
- Small screens (less visible area)
- Touch input (larger targets needed)
- Virtual keyboards (different types)
- Variable connectivity (offline considerations)

---

#### Pattern 4A: Appropriate Input Types

```html
<!-- Email input → Shows @ key -->
<input type="email" autocomplete="email" />

<!-- Phone input → Shows numeric keypad -->
<input type="tel" autocomplete="tel" />

<!-- Number input → Shows numeric keyboard -->
<input type="number" inputmode="numeric" />

<!-- URL input → Shows .com key -->
<input type="url" autocomplete="url" />

<!-- Date input → Shows native date picker -->
<input type="date" />

<!-- Numeric code (OTP) → Numeric keyboard without spinners -->
<input type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="one-time-code" />
```

**Mobile Keyboard Types:**

| Input Type | Mobile Keyboard | Best For |
|------------|-----------------|----------|
| `type="email"` | Email keyboard (@, .) | Email addresses |
| `type="tel"` | Numeric dialpad | Phone numbers |
| `type="number"` | Numeric with +/- | Quantities, ages |
| `type="url"` | URL keyboard (.com, /) | Website URLs |
| `type="search"` | Search keyboard (Go) | Search queries |
| `inputmode="numeric"` | Numeric only | Credit cards, OTP codes |
| `inputmode="decimal"` | Numeric with decimal | Prices, measurements |

**Best Practices:**
- ✅ Use semantic input types (email, tel, url)
- ✅ Use `inputmode` for numeric inputs without spinners
- ✅ Use `autocomplete` attributes for autofill
- ✅ Test on actual mobile devices (iOS and Android)

---

#### Pattern 4B: Large Touch Targets

```css
/* Minimum touch target: 44x44px (iOS), 48x48px (Android) */
.button,
.input,
.checkbox,
.radio {
  min-height: 44px;
  min-width: 44px;
}

/* Increase clickable area with padding */
label {
  padding: 12px;
  cursor: pointer;
}

/* Checkbox/radio: Larger click area */
.checkbox-wrapper,
.radio-wrapper {
  position: relative;
  min-height: 44px;
  display: flex;
  align-items: center;
}

.checkbox-wrapper input[type="checkbox"],
.radio-wrapper input[type="radio"] {
  width: 24px;
  height: 24px;
  margin-right: 12px;
}

/* Make entire label clickable */
.checkbox-wrapper label,
.radio-wrapper label {
  flex: 1;
  cursor: pointer;
}
```

**Best Practices:**
- ✅ Minimum 44x44px touch targets (iOS HIG)
- ✅ Minimum 48x48px recommended (Material Design)
- ✅ Add padding to increase clickable area
- ✅ Make entire label clickable (not just checkbox)
- ✅ Ensure spacing between targets (8px minimum)

---

#### Pattern 4C: Single-Column Layout

```css
/* Mobile-first: Single column */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field {
  width: 100%;
}

/* Desktop: Multi-column when space allows */
@media (min-width: 768px) {
  .form-fields.two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem 2rem;
  }

  /* Some fields span full width */
  .field.full-width {
    grid-column: 1 / -1;
  }
}
```

**Best Practices:**
- ✅ Single column on mobile (default)
- ✅ Multi-column on desktop (when helpful)
- ✅ Related fields side-by-side (first/last name)
- ✅ Long fields full-width (address, description)
- ✅ Labels above inputs (not beside) on mobile

---

#### Pattern 4D: Sticky Submit Button (Mobile)

```html
<form>
  <!-- Form fields -->
  <div class="form-fields">
    <!-- inputs here -->
  </div>

  <!-- Sticky footer on mobile -->
  <div class="form-footer">
    <button type="submit" class="submit-button">
      Submit Form
    </button>
  </div>
</form>

<style>
  /* Mobile: Sticky submit button */
  @media (max-width: 767px) {
    .form-footer {
      position: sticky;
      bottom: 0;
      background: white;
      padding: 1rem;
      border-top: 1px solid #e5e7eb;
      box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    }

    .submit-button {
      width: 100%;
      min-height: 48px;
      font-size: 1rem;
      font-weight: 600;
    }
  }

  /* Desktop: Normal flow -->
  @media (min-width: 768px) {
    .form-footer {
      margin-top: 2rem;
    }
  }
</style>
```

**Best Practices:**
- ✅ Sticky submit button on long forms (mobile)
- ✅ Full-width button on mobile
- ✅ Clear visual separation (border, shadow)
- ✅ Show progress indicator if multi-step
- ❌ Don't hide submit button below fold

---

### 5. Reduce Cognitive Load

**Principle:** Minimize mental effort required to complete the form.

---

#### Pattern 5A: One Question Per Page (When Appropriate)

```html
<!-- Multi-step form: One question per page -->

<!-- Step 1: What's your name? -->
<form>
  <h2>What's your name?</h2>
  <input type="text" name="name" placeholder="Enter your full name" />
  <button type="submit">Continue</button>
</form>

<!-- Step 2: What's your email? -->
<form>
  <h2>What's your email address?</h2>
  <input type="email" name="email" placeholder="name@example.com" />
  <button type="submit">Continue</button>
</form>

<!-- Step 3: Choose a password -->
<form>
  <h2>Choose a password</h2>
  <input type="password" name="password" />
  <div class="strength-meter"><!-- ... --></div>
  <button type="submit">Continue</button>
</form>
```

**When to Use:**
- ✅ Complex decisions (requires thought)
- ✅ Mobile-first applications
- ✅ Conversational interfaces (chatbot-like)
- ✅ Progressive profiling (collect data over time)

**When NOT to Use:**
- ❌ Short forms (3-5 fields)
- ❌ Related fields (address fields together)
- ❌ Desktop-focused applications
- ❌ Power users (prefer speed over simplicity)

---

#### Pattern 5B: Group Related Fields

```html
<form>
  <!-- Personal Information group -->
  <fieldset>
    <legend>Personal Information</legend>
    <div class="field-group">
      <div class="field">
        <label for="first-name">First Name</label>
        <input type="text" id="first-name" />
      </div>
      <div class="field">
        <label for="last-name">Last Name</label>
        <input type="text" id="last-name" />
      </div>
    </div>
  </fieldset>

  <!-- Contact Information group -->
  <fieldset>
    <legend>Contact Information</legend>
    <div class="field">
      <label for="email">Email</label>
      <input type="email" id="email" />
    </div>
    <div class="field">
      <label for="phone">Phone</label>
      <input type="tel" id="phone" />
    </div>
  </fieldset>

  <button type="submit">Submit</button>
</form>
```

**Best Practices:**
- ✅ Use `<fieldset>` and `<legend>` for semantic grouping
- ✅ Visual separation between groups (spacing, borders)
- ✅ Logical grouping (related fields together)
- ✅ Clear group labels (`<legend>`)

---

#### Pattern 5C: Clear, Concise Labels

```html
<!-- ❌ Unclear labels -->
<label>Input 1</label>
<input type="text" />

<label>Data</label>
<input type="text" />

<!-- ✅ Clear, specific labels -->
<label>First Name</label>
<input type="text" placeholder="John" />

<label>Email Address</label>
<input type="email" placeholder="john@example.com" />

<!-- ✅ Labels with examples -->
<label>
  Phone Number
  <span class="example">(e.g., 555-123-4567)</span>
</label>
<input type="tel" placeholder="555-123-4567" />

<!-- ✅ Labels with help text -->
<label for="username">
  Username
  <span class="help-text">This will be visible to other users</span>
</label>
<input type="text" id="username" />
```

**Best Practices:**
- ✅ Use clear, descriptive labels
- ✅ Provide examples when helpful
- ✅ Explain why data is needed (privacy concern)
- ✅ Keep labels short (1-3 words ideal)
- ❌ Don't use technical jargon
- ❌ Don't use ambiguous terms ("Data", "Input 1")

---

#### Pattern 5D: Show Character/Word Count

```html
<div class="field">
  <label for="bio">Bio (Max 200 characters)</label>
  <textarea id="bio" maxlength="200" aria-describedby="bio-count"></textarea>
  <p id="bio-count" class="character-count">
    <span id="current">0</span> / 200 characters
  </p>
</div>

<div class="field">
  <label for="essay">Essay (500-1000 words)</label>
  <textarea id="essay" aria-describedby="essay-count"></textarea>
  <p id="essay-count" class="word-count">
    <span id="words">0</span> words (minimum 500)
  </p>
</div>
```

**Best Practices:**
- ✅ Show character count for limited fields (tweets, bios)
- ✅ Show word count for essays, descriptions
- ✅ Warn when approaching limit
- ✅ Use `aria-live="polite"` for screen reader updates

---

### 6. Error Prevention

**Principle:** Design to prevent errors before they occur.

---

#### Pattern 6A: Constraints Prevent Invalid Input

```html
<!-- Numeric input: Prevent non-numeric -->
<input type="number" min="1" max="100" step="1" />

<!-- Date input: Prevent past dates -->
<input type="date" min="2025-01-01" />

<!-- Time input: Specific time intervals -->
<input type="time" step="900" /> <!-- 15-minute intervals -->

<!-- Text input: Max length -->
<input type="text" maxlength="20" />

<!-- Pattern validation (credit card) -->
<input
  type="text"
  pattern="[0-9]{13,19}"
  title="Credit card number (13-19 digits)"
/>
```

**Best Practices:**
- ✅ Use `min`, `max` for numeric/date ranges
- ✅ Use `maxlength` for character limits
- ✅ Use `pattern` for specific formats
- ✅ Use `step` for specific increments
- ⚠️ Don't block input entirely (allow paste, then validate)

---

#### Pattern 6B: Autocomplete Reduces Typos

```html
<!-- Browser autocomplete -->
<input type="text" name="name" autocomplete="name" />
<input type="email" name="email" autocomplete="email" />
<input type="tel" name="phone" autocomplete="tel" />
<input type="text" name="street" autocomplete="street-address" />
<input type="text" name="city" autocomplete="address-level2" />
<input type="text" name="state" autocomplete="address-level1" />
<input type="text" name="zip" autocomplete="postal-code" />
<input type="text" name="country" autocomplete="country-name" />

<!-- Credit card autocomplete -->
<input type="text" autocomplete="cc-number" />
<input type="text" autocomplete="cc-name" />
<input type="text" autocomplete="cc-exp" />
<input type="text" autocomplete="cc-csc" />
```

**Autocomplete Attribute Values:**
- `name` - Full name
- `given-name` - First name
- `family-name` - Last name
- `email` - Email address
- `tel` - Phone number
- `street-address` - Street address
- `address-level1` - State/province
- `address-level2` - City
- `postal-code` - ZIP/postal code
- `country-name` - Country
- `cc-number` - Credit card number
- `cc-exp` - Credit card expiry

**Best Practices:**
- ✅ Use autocomplete attributes for common fields
- ✅ Reduces typos and speeds up form completion
- ✅ Required for accessibility (WCAG 1.3.5, Level AA)
- ✅ Respects browser's saved data

---

#### Pattern 6C: Confirmation Fields (When Necessary)

```html
<!-- Password confirmation -->
<div class="field">
  <label for="password">Password</label>
  <input type="password" id="password" name="password" />
</div>

<div class="field">
  <label for="confirm-password">Confirm Password</label>
  <input
    type="password"
    id="confirm-password"
    name="confirm-password"
    aria-describedby="confirm-error"
  />
  <p id="confirm-error" class="error-message" hidden>
    Passwords do not match
  </p>
</div>

<!-- Email confirmation (use sparingly) -->
<div class="field">
  <label for="email">Email Address</label>
  <input type="email" id="email" name="email" />
</div>

<div class="field">
  <label for="confirm-email">Confirm Email</label>
  <input
    type="email"
    id="confirm-email"
    name="confirm-email"
    aria-describedby="email-confirm-error"
  />
</div>
```

**When to Use Confirmation Fields:**
- ✅ Passwords (prevent account lockout)
- ✅ Email (prevents wrong receipts, hard to recover)
- ✅ Irreversible actions (account deletion)

**When NOT to Use:**
- ❌ Most fields (adds friction)
- ❌ When autocomplete available
- ❌ When email/phone verification available
- ❌ When undo is possible

---

### 7. Autosave and Recovery

**Principle:** Save user data automatically to prevent loss.

---

#### Pattern 7A: Autosave Draft

```javascript
// Autosave every 30 seconds
let autosaveTimer;

form.addEventListener('input', () => {
  clearTimeout(autosaveTimer);
  autosaveTimer = setTimeout(() => {
    saveDraft();
  }, 30000); // 30 seconds
});

async function saveDraft() {
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);

  await fetch('/api/save-draft', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  showSaveStatus('Draft saved');
}

// Show save status
function showSaveStatus(message) {
  const status = document.getElementById('save-status');
  status.textContent = message;
  status.setAttribute('aria-live', 'polite');
}
```

**Best Practices:**
- ✅ Autosave every 30-60 seconds
- ✅ Save on field blur (when user leaves field)
- ✅ Show "Last saved at" timestamp
- ✅ Debounce to avoid excessive saves
- ✅ Use server-side or localStorage

---

#### Pattern 7B: Warn Before Leaving

```javascript
let hasUnsavedChanges = false;

form.addEventListener('input', () => {
  hasUnsavedChanges = true;
});

form.addEventListener('submit', () => {
  hasUnsavedChanges = false;
});

// Warn before leaving page
window.addEventListener('beforeunload', (e) => {
  if (hasUnsavedChanges) {
    e.preventDefault();
    e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
    return e.returnValue;
  }
});
```

**Best Practices:**
- ✅ Warn only if there are unsaved changes
- ✅ Clear warning after successful submit
- ✅ Use native browser dialog (can't customize much)
- ✅ Combine with autosave for best UX

---

#### Pattern 7C: Resume Where User Left Off

```javascript
// Save form state to localStorage
function saveFormState() {
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);
  localStorage.setItem('form-draft', JSON.stringify(data));
  localStorage.setItem('form-draft-timestamp', Date.now());
}

// Restore form state
function restoreFormState() {
  const draft = localStorage.getItem('form-draft');
  const timestamp = localStorage.getItem('form-draft-timestamp');

  if (draft && timestamp) {
    const age = Date.now() - parseInt(timestamp);
    const daysOld = age / (1000 * 60 * 60 * 24);

    // Only restore if less than 7 days old
    if (daysOld < 7) {
      const data = JSON.parse(draft);
      Object.entries(data).forEach(([name, value]) => {
        const input = form.elements[name];
        if (input) input.value = value;
      });

      showNotification('Draft restored from ' + new Date(parseInt(timestamp)).toLocaleDateString());
    } else {
      // Clear old drafts
      localStorage.removeItem('form-draft');
      localStorage.removeItem('form-draft-timestamp');
    }
  }
}

// Run on page load
document.addEventListener('DOMContentLoaded', restoreFormState);
```

**Best Practices:**
- ✅ Save to localStorage or server
- ✅ Show notification when draft is restored
- ✅ Expire old drafts (7-30 days)
- ✅ Allow user to discard draft
- ✅ Clear draft after successful submission

---

## UX Anti-Patterns (What NOT to Do)

### Common UX Mistakes

❌ **Captcha for every form**
- Frustrating user experience
- Accessibility issues (vision, cognitive)
- Use only when necessary (spam is actual problem)
- Consider alternatives (honeypot, rate limiting, reCAPTCHA v3)

❌ **Required fields not indicated**
- User doesn't know what's required until submit error
- Indicate required fields clearly (* or "(required)")

❌ **Disabled submit button without explanation**
- User doesn't know why they can't submit
- Allow submit, then show errors
- Or show clear message ("Complete all required fields")

❌ **Too many required fields**
- Asks for unnecessary information
- High abandonment rate
- Only require what's absolutely necessary

❌ **Long forms without progress indication**
- User doesn't know how much longer
- Use progress bar or step indicator
- Consider breaking into multi-step

❌ **Unclear error messages**
- "Invalid input" (what's wrong?)
- "Error" (not helpful)
- Use specific, actionable messages

❌ **Reset button next to submit**
- Accidental clicks clear entire form
- Rarely needed (users can manually clear)
- Remove reset button entirely

❌ **Placeholders as labels**
- Disappears when user types (confusion)
- Accessibility issue (screen readers)
- Use explicit `<label>` instead

---

## UX Testing Checklist

### Manual Testing

- [ ] Complete form on actual mobile device (iOS and Android)
- [ ] Test all input keyboards (email shows @, tel shows numbers)
- [ ] Test autofill/autocomplete works correctly
- [ ] Test with low connectivity (slow network)
- [ ] Test form interruption (leave page, come back)
- [ ] Test autosave works (wait 30 seconds, refresh page)
- [ ] Measure completion time (aim for <2 minutes for most forms)
- [ ] Test validation timing (not too early, not too late)
- [ ] Test error messages are clear and helpful
- [ ] Test success indicators show when field is valid

### Analytics to Monitor

- **Completion rate** - % of users who start and finish form
- **Time to complete** - Average time from start to submit
- **Abandonment points** - Which fields cause users to leave
- **Error rate per field** - Which fields have most validation errors
- **Field interaction time** - Time spent on each field
- **Device breakdown** - Mobile vs desktop completion rates

---

## Summary: UX Best Practices

1. **Progressive Disclosure** - Show essential fields first, reveal advanced options
2. **Smart Defaults** - Auto-detect values, remember previous entries, suggest completions
3. **Positive Feedback** - Show success indicators, not just errors
4. **Mobile-First** - Appropriate keyboards, large touch targets, single-column
5. **Reduce Cognitive Load** - Group fields, clear labels, one question per page when appropriate
6. **Error Prevention** - Constraints, autocomplete, confirmation fields (sparingly)
7. **Autosave** - Save drafts automatically, warn before leaving, restore on return

**The Golden Rule of Form UX:**
> Minimize effort, prevent errors, provide clear feedback.

---

## Next Steps

- Ensure accessibility compliance → `accessibility-forms.md`
- Implement validation strategies → `validation-concepts.md`
- Choose component types → `decision-tree.md`
- Select language implementation:
  - JavaScript/React → `javascript/react-hook-form.md`
  - Python → `python/pydantic-forms.md`
