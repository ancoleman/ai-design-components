# React Hook Form: Complete Implementation Guide

**React Hook Form is the recommended form library for React applications, offering best-in-class performance, minimal re-renders, and excellent TypeScript support.**

## Why React Hook Form?

**Performance Benefits:**
- **30-40% fewer re-renders** compared to Formik
- **Uncontrolled components** - Better performance, less state management
- **Small bundle size** - ~8KB (vs Formik's ~15KB)
- **No dependencies** - Zero external dependencies

**Developer Experience:**
- **TypeScript-first** - Excellent type inference
- **Minimal boilerplate** - Less code, more productivity
- **Flexible validation** - Works with any validation library (Zod, Yup, built-in)
- **DevTools** - Browser extension for debugging

**When to Use:**
- ✅ New React projects (start with this)
- ✅ Performance-critical forms (checkout, login)
- ✅ TypeScript projects (best type inference)
- ✅ Any form complexity (simple to complex)

---

## Installation

```bash
# NPM
npm install react-hook-form

# Yarn
yarn add react-hook-form

# Optional: Validation resolvers (for Zod, Yup, etc.)
npm install @hookform/resolvers

# Optional: DevTools (development only)
npm install -D @hookform/devtools
```

---

## Basic Usage

### Simple Form (No Validation)

```tsx
import { useForm } from 'react-hook-form';

type FormData = {
  firstName: string;
  lastName: string;
  email: string;
};

function BasicForm() {
  const { register, handleSubmit } = useForm<FormData>();

  const onSubmit = (data: FormData) => {
    console.log(data);
    // { firstName: 'John', lastName: 'Doe', email: 'john@example.com' }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('firstName')} placeholder="First Name" />
      <input {...register('lastName')} placeholder="Last Name" />
      <input {...register('email')} type="email" placeholder="Email" />

      <button type="submit">Submit</button>
    </form>
  );
}
```

**Key Concepts:**
- `useForm()` - Hook that provides form methods
- `register()` - Registers input to form (name, ref, onChange, onBlur)
- `handleSubmit()` - Validates and calls onSubmit with data

---

### Form with Built-in Validation

```tsx
import { useForm } from 'react-hook-form';

type FormData = {
  username: string;
  email: string;
  password: string;
  age: number;
};

function ValidationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    mode: 'onBlur', // Validate on blur (recommended)
  });

  const onSubmit = async (data: FormData) => {
    await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          {...register('username', {
            required: 'Username is required',
            minLength: { value: 3, message: 'Min 3 characters' },
            maxLength: { value: 20, message: 'Max 20 characters' },
          })}
        />
        {errors.username && (
          <span className="error" role="alert">
            {errors.username.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Invalid email address',
            },
          })}
        />
        {errors.email && (
          <span className="error" role="alert">
            {errors.email.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          {...register('password', {
            required: 'Password is required',
            minLength: { value: 8, message: 'Min 8 characters' },
            validate: {
              hasUpperCase: (value) =>
                /[A-Z]/.test(value) || 'Must contain uppercase letter',
              hasNumber: (value) =>
                /\d/.test(value) || 'Must contain number',
            },
          })}
        />
        {errors.password && (
          <span className="error" role="alert">
            {errors.password.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="age">Age</label>
        <input
          id="age"
          type="number"
          {...register('age', {
            valueAsNumber: true, // Convert to number
            required: 'Age is required',
            min: { value: 18, message: 'Must be at least 18' },
            max: { value: 120, message: 'Must be less than 120' },
          })}
        />
        {errors.age && (
          <span className="error" role="alert">
            {errors.age.message}
          </span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

**Built-in Validation Rules:**
- `required` - Field is required
- `min` / `max` - Numeric min/max values
- `minLength` / `maxLength` - String length
- `pattern` - Regex pattern
- `validate` - Custom validation function

---

## Validation Modes

```tsx
const { register } = useForm({
  mode: 'onBlur', // When to validate
});
```

**Available Modes:**

| Mode | When Validated | Best For |
|------|----------------|----------|
| `onSubmit` | On form submit only | Simple forms, infrequent validation |
| `onBlur` | When field loses focus | **RECOMMENDED** - Most forms |
| `onChange` | As user types | Password strength, character count |
| `onTouched` | After field touched and blurred | Similar to onBlur |
| `all` | onChange + onBlur | Maximum validation |

**reValidateMode (after first error):**

```tsx
const { register } = useForm({
  mode: 'onBlur', // Initial validation
  reValidateMode: 'onChange', // After error, validate on change
});
```

**Progressive Enhancement Pattern (RECOMMENDED):**
```tsx
const { register } = useForm({
  mode: 'onBlur', // Validate when user leaves field
  reValidateMode: 'onChange', // After error, validate on every keystroke
});
```

---

## Schema Validation with Zod

**Recommended:** Use Zod for TypeScript-first schema validation.

```bash
npm install zod @hookform/resolvers
```

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

// Define validation schema
const userSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[0-9]/, 'Must contain number'),
  confirmPassword: z.string(),
  age: z.number()
    .int('Age must be an integer')
    .min(18, 'Must be at least 18')
    .max(120, 'Must be less than 120'),
  terms: z.boolean().refine((val) => val === true, {
    message: 'You must accept the terms and conditions',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'], // Error appears on confirmPassword field
});

// Infer TypeScript type from schema
type UserFormData = z.infer<typeof userSchema>;

function RegistrationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: UserFormData) => {
    console.log(data); // Fully type-safe!
    await registerUser(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="username">Username</label>
        <input id="username" {...register('username')} />
        {errors.username && <span>{errors.username.message}</span>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register('email')} />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" {...register('password')} />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input id="confirmPassword" type="password" {...register('confirmPassword')} />
        {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}
      </div>

      <div>
        <label htmlFor="age">Age</label>
        <input id="age" type="number" {...register('age', { valueAsNumber: true })} />
        {errors.age && <span>{errors.age.message}</span>}
      </div>

      <div>
        <label>
          <input type="checkbox" {...register('terms')} />
          I accept the terms and conditions
        </label>
        {errors.terms && <span>{errors.terms.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}
```

**Benefits of Zod + React Hook Form:**
- ✅ Single source of truth (schema defines types and validation)
- ✅ Type-safe (TypeScript infers types from schema)
- ✅ Reusable schemas (use same schema on frontend and backend)
- ✅ Excellent error messages
- ✅ Complex validation (cross-field, conditional)

**See:** `zod-validation.md` for complete Zod guide

---

## Async Validation

### Username Availability Check

```tsx
import { useForm } from 'react-hook-form';

function AsyncValidationForm() {
  const { register, formState: { errors } } = useForm();

  return (
    <form>
      <input
        {...register('username', {
          required: 'Username is required',
          validate: async (value) => {
            const response = await fetch(`/api/check-username?name=${value}`);
            const { available } = await response.json();
            return available || 'Username already taken';
          },
        })}
        placeholder="Username"
      />
      {errors.username && <span>{errors.username.message}</span>}
    </form>
  );
}
```

### Debounced Async Validation

```tsx
import { useForm } from 'react-hook-form';
import { useCallback } from 'react';
import debounce from 'lodash/debounce';

function DebouncedValidationForm() {
  const { register } = useForm({
    mode: 'onChange', // Validate as user types
  });

  // Debounce the API call (500ms)
  const debouncedCheck = useCallback(
    debounce(async (value: string) => {
      const response = await fetch(`/api/check-username?name=${value}`);
      return response.json();
    }, 500),
    []
  );

  return (
    <form>
      <input
        {...register('username', {
          validate: async (value) => {
            const { available } = await debouncedCheck(value);
            return available || 'Username already taken';
          },
        })}
        placeholder="Username"
      />
    </form>
  );
}
```

---

## Advanced Patterns

### Watch Field Values

```tsx
function WatchExample() {
  const { register, watch } = useForm();

  // Watch specific field
  const password = watch('password');

  // Watch all fields
  const allValues = watch();

  // Watch multiple fields
  const [firstName, lastName] = watch(['firstName', 'lastName']);

  return (
    <form>
      <input {...register('password')} type="password" />
      <p>Password length: {password?.length || 0}</p>
    </form>
  );
}
```

### Conditional Fields (Show/Hide Based on Selection)

```tsx
function ConditionalFieldsForm() {
  const { register, watch } = useForm();

  const accountType = watch('accountType');

  return (
    <form>
      <select {...register('accountType')}>
        <option value="personal">Personal</option>
        <option value="business">Business</option>
      </select>

      {accountType === 'business' && (
        <div>
          <input {...register('companyName')} placeholder="Company Name" />
          <input {...register('taxId')} placeholder="Tax ID" />
        </div>
      )}
    </form>
  );
}
```

### Field Arrays (Dynamic Lists)

```tsx
import { useForm, useFieldArray } from 'react-hook-form';

type FormData = {
  emails: { value: string }[];
};

function FieldArrayForm() {
  const { register, control } = useForm<FormData>({
    defaultValues: {
      emails: [{ value: '' }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'emails',
  });

  return (
    <form>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`emails.${index}.value`, {
              required: 'Email is required',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Invalid email',
              },
            })}
            placeholder="Email"
          />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={() => append({ value: '' })}>
        Add Email
      </button>
    </form>
  );
}
```

### Reset Form

```tsx
function ResetForm() {
  const { register, reset } = useForm();

  return (
    <form>
      <input {...register('name')} />

      {/* Reset to empty */}
      <button type="button" onClick={() => reset()}>
        Reset
      </button>

      {/* Reset to specific values */}
      <button
        type="button"
        onClick={() => reset({ name: 'Default Name' })}
      >
        Reset to Default
      </button>
    </form>
  );
}
```

### Set Field Value Programmatically

```tsx
function SetValueForm() {
  const { register, setValue } = useForm();

  return (
    <form>
      <input {...register('name')} />

      <button
        type="button"
        onClick={() => setValue('name', 'John Doe', {
          shouldValidate: true, // Trigger validation
          shouldDirty: true, // Mark as dirty
        })}
      >
        Set Name
      </button>
    </form>
  );
}
```

---

## Integration with UI Libraries

### Radix UI (Unstyled, Accessible)

```tsx
import { useForm, Controller } from 'react-hook-form';
import * as Select from '@radix-ui/react-select';

function RadixForm() {
  const { control, handleSubmit } = useForm();

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <Controller
        name="country"
        control={control}
        rules={{ required: 'Country is required' }}
        render={({ field }) => (
          <Select.Root value={field.value} onValueChange={field.onChange}>
            <Select.Trigger>
              <Select.Value placeholder="Select country" />
            </Select.Trigger>
            <Select.Content>
              <Select.Item value="us">United States</Select.Item>
              <Select.Item value="ca">Canada</Select.Item>
              <Select.Item value="mx">Mexico</Select.Item>
            </Select.Content>
          </Select.Root>
        )}
      />

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Material-UI

```tsx
import { useForm, Controller } from 'react-hook-form';
import { TextField, Checkbox, FormControlLabel } from '@mui/material';

function MUIForm() {
  const { control, handleSubmit } = useForm();

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <Controller
        name="email"
        control={control}
        defaultValue=""
        rules={{ required: 'Email is required' }}
        render={({ field, fieldState: { error } }) => (
          <TextField
            {...field}
            label="Email"
            error={!!error}
            helperText={error?.message}
          />
        )}
      />

      <Controller
        name="terms"
        control={control}
        defaultValue={false}
        render={({ field }) => (
          <FormControlLabel
            control={<Checkbox {...field} checked={field.value} />}
            label="I accept terms"
          />
        )}
      />

      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## Error Handling

### Display Errors

```tsx
function ErrorHandling() {
  const { register, formState: { errors } } = useForm();

  return (
    <form>
      <input
        {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Invalid email',
          },
        })}
        aria-invalid={errors.email ? 'true' : 'false'}
        aria-describedby={errors.email ? 'email-error' : undefined}
      />

      {errors.email && (
        <span id="email-error" role="alert" className="error">
          {errors.email.message}
        </span>
      )}
    </form>
  );
}
```

### Error Summary (Accessibility)

```tsx
function ErrorSummary() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      {Object.keys(errors).length > 0 && (
        <div role="alert" className="error-summary">
          <h2>There are {Object.keys(errors).length} error(s) in this form:</h2>
          <ul>
            {Object.entries(errors).map(([field, error]) => (
              <li key={field}>
                <a href={`#${field}`}>{error.message}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <input id="email" {...register('email', { required: 'Email is required' })} />
      <input id="password" {...register('password', { required: 'Password is required' })} />

      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## DevTools (Development Only)

```tsx
import { useForm } from 'react-hook-form';
import { DevTool } from '@hookform/devtools';

function FormWithDevTools() {
  const { register, control } = useForm();

  return (
    <>
      <form>
        <input {...register('name')} />
      </form>

      {/* Only in development */}
      {process.env.NODE_ENV === 'development' && <DevTool control={control} />}
    </>
  );
}
```

**DevTools Features:**
- View form state in real-time
- See validation errors
- Inspect field values
- Track touched/dirty state
- Debug validation issues

---

## Complete Example: Registration Form

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const registrationSchema = z.object({
  firstName: z.string().min(2, 'First name must be at least 2 characters'),
  lastName: z.string().min(2, 'Last name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[0-9]/, 'Must contain number'),
  confirmPassword: z.string(),
  age: z.number().int().min(18, 'Must be at least 18'),
  terms: z.boolean().refine((val) => val === true, 'You must accept terms'),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type RegistrationData = z.infer<typeof registrationSchema>;

export default function RegistrationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isSubmitSuccessful },
  } = useForm<RegistrationData>({
    resolver: zodResolver(registrationSchema),
    mode: 'onBlur',
    reValidateMode: 'onChange',
  });

  const onSubmit = async (data: RegistrationData) => {
    await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  if (isSubmitSuccessful) {
    return <div>Registration successful! Check your email.</div>;
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <h2>Register</h2>

      <div className="field">
        <label htmlFor="firstName">First Name</label>
        <input id="firstName" {...register('firstName')} />
        {errors.firstName && <span role="alert">{errors.firstName.message}</span>}
      </div>

      <div className="field">
        <label htmlFor="lastName">Last Name</label>
        <input id="lastName" {...register('lastName')} />
        {errors.lastName && <span role="alert">{errors.lastName.message}</span>}
      </div>

      <div className="field">
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register('email')} />
        {errors.email && <span role="alert">{errors.email.message}</span>}
      </div>

      <div className="field">
        <label htmlFor="password">Password</label>
        <input id="password" type="password" {...register('password')} />
        {errors.password && <span role="alert">{errors.password.message}</span>}
      </div>

      <div className="field">
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input id="confirmPassword" type="password" {...register('confirmPassword')} />
        {errors.confirmPassword && <span role="alert">{errors.confirmPassword.message}</span>}
      </div>

      <div className="field">
        <label htmlFor="age">Age</label>
        <input id="age" type="number" {...register('age', { valueAsNumber: true })} />
        {errors.age && <span role="alert">{errors.age.message}</span>}
      </div>

      <div className="field">
        <label>
          <input type="checkbox" {...register('terms')} />
          I accept the terms and conditions
        </label>
        {errors.terms && <span role="alert">{errors.terms.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}
```

---

## Best Practices

1. **Use TypeScript** - Type-safe forms prevent bugs
2. **Use Zod for validation** - Single source of truth, type inference
3. **Use onBlur mode** - Best UX balance (not annoying, timely feedback)
4. **Use reValidateMode: onChange** - After first error, validate on change
5. **Provide clear error messages** - Explain what's wrong and how to fix
6. **Show success indicators** - Green checkmark when valid
7. **Use aria attributes** - `aria-invalid`, `aria-describedby`, `role="alert"`
8. **Debounce async validation** - Reduce API calls (500ms recommended)
9. **Use DevTools in development** - Debug form state easily
10. **Handle loading states** - Disable submit button while submitting

---

## Common Patterns

**Login Form:** See `examples/basic-form.tsx`
**Multi-Step Wizard:** See `examples/multi-step-wizard.tsx`
**Inline Validation:** See `examples/inline-validation.tsx`
**Dynamic Field Arrays:** See `examples/field-arrays.tsx`
**Conditional Fields:** See `examples/conditional-fields.tsx`

---

## Resources

**Official Documentation:**
- React Hook Form: https://react-hook-form.com/
- API Reference: https://react-hook-form.com/api
- Examples: https://react-hook-form.com/get-started

**Integration Guides:**
- Zod: https://react-hook-form.com/get-started#SchemaValidation
- Yup: https://react-hook-form.com/get-started#SchemaValidation
- Material-UI: https://react-hook-form.com/get-started#IntegratingwithUILibraries
- Radix UI: https://www.radix-ui.com/primitives/docs/guides/integrating-with-forms

**Tools:**
- DevTools: https://react-hook-form.com/dev-tools
- Form Builder: https://react-hook-form.com/form-builder

---

## Next Steps

- Schema validation with Zod → `zod-validation.md`
- Working examples → `examples/`
- Accessibility patterns → `../accessibility-forms.md`
- UX best practices → `../ux-patterns.md`
