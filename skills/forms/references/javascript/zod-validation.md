# Zod Validation: TypeScript-First Schema Validation

**Zod is a TypeScript-first schema validation library that provides runtime validation with automatic type inference. It's the recommended validation solution for TypeScript projects.**

## Why Zod?

**TypeScript Integration:**
- **Automatic type inference** - Types generated from schema
- **Type-safe** - Compile-time AND runtime validation
- **Zero dependencies** - Lightweight, no external deps
- **Composable** - Build complex schemas from simple ones

**Developer Experience:**
- **Excellent error messages** - Clear, customizable
- **Schema as single source of truth** - Types + validation in one place
- **Integrates with React Hook Form** - Via `@hookform/resolvers`
- **Supports all primitives** - String, number, boolean, date, etc.

**When to Use:**
- ✅ TypeScript projects (primary benefit)
- ✅ Need runtime validation
- ✅ Want type inference from schema
- ✅ Building APIs (validate request/response)
- ✅ Complex validation rules

---

## Installation

```bash
# NPM
npm install zod

# Yarn
yarn add zod

# With React Hook Form resolver
npm install @hookform/resolvers
```

---

## Basic Usage

### Simple Schema

```typescript
import * as z from 'zod';

// Define schema
const userSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  age: z.number().int().positive(),
});

// Infer TypeScript type
type User = z.infer<typeof userSchema>;
// Equivalent to: { name: string; email: string; age: number; }

// Validate data
const result = userSchema.safeParse({
  name: 'John Doe',
  email: 'john@example.com',
  age: 30,
});

if (result.success) {
  console.log(result.data); // Type-safe data
} else {
  console.log(result.error); // Validation errors
}
```

---

## Primitive Types

### String Validation

```typescript
import * as z from 'zod';

// Basic string
z.string();

// With constraints
z.string().min(3, 'Minimum 3 characters')
  .max(20, 'Maximum 20 characters')
  .length(5, 'Exactly 5 characters');

// Email
z.string().email('Invalid email address');

// URL
z.string().url('Invalid URL');

// UUID
z.string().uuid('Invalid UUID');

// Regex pattern
z.string().regex(/^[a-zA-Z0-9]+$/, 'Alphanumeric only');

// Specific format
z.string().startsWith('https://', 'Must start with https://')
  .endsWith('.com', 'Must end with .com');

// Transformations
z.string().toLowerCase(); // Convert to lowercase
z.string().toUpperCase(); // Convert to uppercase
z.string().trim(); // Trim whitespace

// Optional with default
z.string().default('default value');

// Optional (can be undefined)
z.string().optional();

// Nullable (can be null)
z.string().nullable();

// Optional and nullable
z.string().nullish(); // string | null | undefined
```

---

### Number Validation

```typescript
import * as z from 'zod';

// Basic number
z.number();

// Integer
z.number().int('Must be an integer');

// Constraints
z.number().min(0, 'Must be non-negative')
  .max(100, 'Must be less than or equal to 100')
  .positive('Must be positive')
  .negative('Must be negative')
  .nonnegative('Must be non-negative')
  .nonpositive('Must be non-positive');

// Specific values
z.number().multipleOf(5, 'Must be multiple of 5');

// Finite (not Infinity or NaN)
z.number().finite('Must be finite');

// Safe integer
z.number().safe('Must be safe integer'); // Between -(2^53 - 1) and 2^53 - 1

// With default
z.number().default(0);

// Transform string to number
z.string().transform((val) => parseInt(val, 10));

// Or use coerce (automatic conversion)
z.coerce.number(); // Converts '123' to 123
```

---

### Boolean Validation

```typescript
import * as z from 'zod';

// Basic boolean
z.boolean();

// With default
z.boolean().default(false);

// Coerce (convert truthy/falsy to boolean)
z.coerce.boolean(); // '1' → true, '0' → false, 'true' → true
```

---

### Date Validation

```typescript
import * as z from 'zod';

// Basic date
z.date();

// Constraints
z.date().min(new Date('2020-01-01'), 'Must be after 2020')
  .max(new Date('2030-12-31'), 'Must be before 2031');

// Coerce string to date
z.coerce.date(); // '2025-01-01' → Date object

// Custom validation
z.date().refine(
  (date) => date > new Date(),
  { message: 'Date must be in the future' }
);
```

---

## Complex Types

### Object Schema

```typescript
import * as z from 'zod';

const userSchema = z.object({
  id: z.number().int().positive(),
  username: z.string().min(3).max(20),
  email: z.string().email(),
  age: z.number().int().min(18).max(120),
  isActive: z.boolean().default(true),
  role: z.enum(['user', 'admin', 'moderator']),
  createdAt: z.date(),
  // Optional field
  bio: z.string().max(500).optional(),
  // Nullable field
  avatar: z.string().url().nullable(),
});

type User = z.infer<typeof userSchema>;

// Nested objects
const addressSchema = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string(),
  zip: z.string().regex(/^\d{5}$/),
  country: z.string().default('US'),
});

const userWithAddressSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  address: addressSchema, // Nested object
});
```

---

### Array Schema

```typescript
import * as z from 'zod';

// Array of strings
z.array(z.string());

// Array with constraints
z.array(z.string()).min(1, 'At least one item required')
  .max(10, 'Maximum 10 items')
  .nonempty('Array cannot be empty');

// Array of objects
const tagSchema = z.object({
  id: z.number(),
  name: z.string(),
});

z.array(tagSchema);

// Infer type
type Tags = z.infer<typeof z.array(tagSchema)>;
// Tags = { id: number; name: string; }[]
```

---

### Enum and Literals

```typescript
import * as z from 'zod';

// Enum (recommended)
const roleSchema = z.enum(['user', 'admin', 'moderator']);
type Role = z.infer<typeof roleSchema>; // 'user' | 'admin' | 'moderator'

// Native enum
enum NativeRole {
  User = 'user',
  Admin = 'admin',
  Moderator = 'moderator',
}
z.nativeEnum(NativeRole);

// Union of literals
z.union([
  z.literal('user'),
  z.literal('admin'),
  z.literal('moderator'),
]);

// Single literal
z.literal('exact_value');
```

---

### Union Types

```typescript
import * as z from 'zod';

// Union (one of multiple types)
const stringOrNumber = z.union([z.string(), z.number()]);
type StringOrNumber = z.infer<typeof stringOrNumber>; // string | number

// Discriminated union (tagged union)
const successResponse = z.object({
  status: z.literal('success'),
  data: z.object({ id: z.number(), name: z.string() }),
});

const errorResponse = z.object({
  status: z.literal('error'),
  error: z.string(),
});

const apiResponse = z.discriminatedUnion('status', [
  successResponse,
  errorResponse,
]);

type ApiResponse = z.infer<typeof apiResponse>;
// { status: 'success'; data: { id: number; name: string; } }
// | { status: 'error'; error: string; }
```

---

## Advanced Validation

### Custom Validation with .refine()

```typescript
import * as z from 'zod';

// Single refinement
const passwordSchema = z.string()
  .min(8)
  .refine(
    (password) => /[A-Z]/.test(password),
    { message: 'Password must contain at least one uppercase letter' }
  )
  .refine(
    (password) => /[0-9]/.test(password),
    { message: 'Password must contain at least one number' }
  );

// Multiple refinements (array)
const strongPasswordSchema = z.string()
  .min(8)
  .refine((val) => /[A-Z]/.test(val), 'Must contain uppercase')
  .refine((val) => /[a-z]/.test(val), 'Must contain lowercase')
  .refine((val) => /[0-9]/.test(val), 'Must contain number')
  .refine((val) => /[!@#$%^&*]/.test(val), 'Must contain special character');

// Async refinement
const usernameSchema = z.string()
  .min(3)
  .refine(
    async (username) => {
      const response = await fetch(`/api/check-username?name=${username}`);
      const { available } = await response.json();
      return available;
    },
    { message: 'Username already taken' }
  );
```

---

### Cross-Field Validation

```typescript
import * as z from 'zod';

// Password confirmation
const registrationSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: 'Passwords do not match',
    path: ['confirmPassword'], // Error appears on this field
  }
);

// Date range validation
const dateRangeSchema = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
}).refine(
  (data) => data.endDate >= data.startDate,
  {
    message: 'End date must be after start date',
    path: ['endDate'],
  }
);

// Conditional field requirement
const shippingSchema = z.object({
  shippingMethod: z.enum(['standard', 'express']),
  phoneNumber: z.string().optional(),
}).refine(
  (data) => {
    // If express shipping, phone number is required
    if (data.shippingMethod === 'express') {
      return !!data.phoneNumber && data.phoneNumber.length > 0;
    }
    return true;
  },
  {
    message: 'Phone number required for express shipping',
    path: ['phoneNumber'],
  }
);
```

---

### Transformations

```typescript
import * as z from 'zod';

// Transform string to number
const numberSchema = z.string().transform((val) => parseInt(val, 10));

// Transform to lowercase
const emailSchema = z.string().email().toLowerCase();

// Transform and validate
const ageSchema = z.string()
  .transform((val) => parseInt(val, 10))
  .pipe(z.number().int().min(18).max(120));

// Complex transformation
const userSchema = z.object({
  name: z.string().transform((val) => val.trim()),
  email: z.string().email().toLowerCase(),
  age: z.coerce.number().int().positive(),
});
```

---

## Form Validation Patterns

### React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

// Define schema
const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginData = z.infer<typeof loginSchema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data: LoginData) => {
    console.log(data); // Type-safe!
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} type="email" />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

---

### Registration Form with Complex Validation

```typescript
import * as z from 'zod';

const registrationSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),

  email: z.string()
    .email('Invalid email address')
    .toLowerCase(),

  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number')
    .regex(/[!@#$%^&*]/, 'Password must contain at least one special character'),

  confirmPassword: z.string(),

  age: z.number()
    .int('Age must be a whole number')
    .min(18, 'You must be at least 18 years old')
    .max(120, 'Please enter a valid age'),

  terms: z.boolean()
    .refine((val) => val === true, {
      message: 'You must accept the terms and conditions',
    }),

  newsletter: z.boolean().default(false),
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  }
);

type RegistrationData = z.infer<typeof registrationSchema>;
```

---

### Multi-Step Form Validation

```typescript
import * as z from 'zod';

// Step 1: Personal Info
const step1Schema = z.object({
  firstName: z.string().min(2),
  lastName: z.string().min(2),
  email: z.string().email(),
});

// Step 2: Address
const step2Schema = z.object({
  street: z.string().min(5),
  city: z.string().min(2),
  state: z.string().length(2),
  zip: z.string().regex(/^\d{5}$/),
});

// Step 3: Preferences
const step3Schema = z.object({
  newsletter: z.boolean(),
  notifications: z.boolean(),
});

// Combined schema (all steps)
const completeFormSchema = z.object({
  ...step1Schema.shape,
  ...step2Schema.shape,
  ...step3Schema.shape,
});

type CompleteFormData = z.infer<typeof completeFormSchema>;

// Usage in multi-step form
function MultiStepForm() {
  const [step, setStep] = useState(1);

  const step1Form = useForm({
    resolver: zodResolver(step1Schema),
  });

  const step2Form = useForm({
    resolver: zodResolver(step2Schema),
  });

  const step3Form = useForm({
    resolver: zodResolver(step3Schema),
  });

  // ... form implementation
}
```

---

### Dynamic Form with Conditional Fields

```typescript
import * as z from 'zod';

const baseSchema = z.object({
  accountType: z.enum(['personal', 'business']),
  email: z.string().email(),
});

const personalSchema = baseSchema.extend({
  accountType: z.literal('personal'),
  firstName: z.string().min(2),
  lastName: z.string().min(2),
});

const businessSchema = baseSchema.extend({
  accountType: z.literal('business'),
  companyName: z.string().min(2),
  taxId: z.string().regex(/^\d{9}$/),
  contactPerson: z.string().min(2),
});

const accountSchema = z.discriminatedUnion('accountType', [
  personalSchema,
  businessSchema,
]);

type AccountData = z.infer<typeof accountSchema>;
// { accountType: 'personal'; email: string; firstName: string; lastName: string; }
// | { accountType: 'business'; email: string; companyName: string; taxId: string; contactPerson: string; }
```

---

## Common Validation Patterns

### Email Validation

```typescript
import * as z from 'zod';

// Basic email
z.string().email();

// With custom error message
z.string().email('Please enter a valid email address');

// With transformation (lowercase)
z.string().email().toLowerCase();

// Specific domain
z.string().email().refine(
  (email) => email.endsWith('@company.com'),
  { message: 'Must be a company email (@company.com)' }
);
```

---

### Phone Number Validation

```typescript
import * as z from 'zod';

// US phone number (10 digits)
z.string().regex(
  /^\d{10}$/,
  'Phone number must be 10 digits'
);

// US phone with formatting
z.string().regex(
  /^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$/,
  'Phone format: (555) 123-4567 or 555-123-4567'
);

// International format
z.string().regex(
  /^\+?[1-9]\d{1,14}$/,
  'Please enter a valid international phone number'
);

// With transformation (remove formatting)
z.string()
  .transform((val) => val.replace(/\D/g, '')) // Remove non-digits
  .pipe(z.string().regex(/^\d{10}$/, 'Must be 10 digits'));
```

---

### Credit Card Validation

```typescript
import * as z from 'zod';

// Credit card number (Luhn algorithm)
function luhnCheck(cardNumber: string): boolean {
  const digits = cardNumber.replace(/\D/g, '');
  let sum = 0;
  let isEven = false;

  for (let i = digits.length - 1; i >= 0; i--) {
    let digit = parseInt(digits[i], 10);

    if (isEven) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }

    sum += digit;
    isEven = !isEven;
  }

  return sum % 10 === 0;
}

const creditCardSchema = z.string()
  .regex(/^\d{13,19}$/, 'Credit card must be 13-19 digits')
  .refine(luhnCheck, { message: 'Invalid credit card number' });

// Expiry date (MM/YY)
const expirySchema = z.string()
  .regex(/^(0[1-9]|1[0-2])\/\d{2}$/, 'Format: MM/YY')
  .refine(
    (expiry) => {
      const [month, year] = expiry.split('/');
      const expiryDate = new Date(2000 + parseInt(year), parseInt(month) - 1);
      return expiryDate > new Date();
    },
    { message: 'Card has expired' }
  );

// CVV
const cvvSchema = z.string().regex(/^\d{3,4}$/, 'CVV must be 3-4 digits');
```

---

### Password Validation

```typescript
import * as z from 'zod';

// Strong password
const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .max(100, 'Password must be less than 100 characters')
  .refine((val) => /[a-z]/.test(val), {
    message: 'Password must contain at least one lowercase letter',
  })
  .refine((val) => /[A-Z]/.test(val), {
    message: 'Password must contain at least one uppercase letter',
  })
  .refine((val) => /[0-9]/.test(val), {
    message: 'Password must contain at least one number',
  })
  .refine((val) => /[!@#$%^&*(),.?":{}|<>]/.test(val), {
    message: 'Password must contain at least one special character',
  });

// Password strength levels
enum PasswordStrength {
  Weak = 'weak',
  Medium = 'medium',
  Strong = 'strong',
}

function calculatePasswordStrength(password: string): PasswordStrength {
  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[!@#$%^&*]/.test(password)) score++;

  if (score >= 5) return PasswordStrength.Strong;
  if (score >= 3) return PasswordStrength.Medium;
  return PasswordStrength.Weak;
}
```

---

## Error Handling

### Parsing Results

```typescript
import * as z from 'zod';

const schema = z.object({
  name: z.string(),
  age: z.number(),
});

// Safe parse (returns result object)
const result = schema.safeParse({ name: 'John', age: '30' });

if (result.success) {
  console.log(result.data); // { name: 'John', age: 30 }
} else {
  console.log(result.error); // ZodError object
  console.log(result.error.issues); // Array of validation errors
}

// Parse (throws on error)
try {
  const data = schema.parse({ name: 'John', age: '30' });
  console.log(data);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.log(error.issues);
  }
}
```

---

### Custom Error Messages

```typescript
import * as z from 'zod';

// Per-field messages
const schema = z.object({
  email: z.string({ required_error: 'Email is required' })
    .email('Please enter a valid email address'),

  age: z.number({ required_error: 'Age is required' })
    .int('Age must be a whole number')
    .positive('Age must be positive'),
});

// Error map (global customization)
const customErrorMap: z.ZodErrorMap = (issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    if (issue.expected === 'string') {
      return { message: 'Please enter text' };
    }
  }
  return { message: ctx.defaultError };
};

z.setErrorMap(customErrorMap);
```

---

## Best Practices

1. **Use .infer for types** - Let Zod generate TypeScript types
   ```typescript
   const schema = z.object({ name: z.string() });
   type Data = z.infer<typeof schema>; // ✅ Single source of truth
   ```

2. **Validate at boundaries** - API requests, form submissions
   ```typescript
   // API endpoint
   app.post('/api/users', async (req, res) => {
     const result = userSchema.safeParse(req.body);
     if (!result.success) {
       return res.status(400).json({ errors: result.error });
     }
     // ... use result.data
   });
   ```

3. **Reuse schemas** - Build complex schemas from simple ones
   ```typescript
   const baseUserSchema = z.object({
     name: z.string(),
     email: z.string().email(),
   });

   const createUserSchema = baseUserSchema.extend({
     password: z.string().min(8),
   });

   const updateUserSchema = baseUserSchema.partial(); // All fields optional
   ```

4. **Use discriminated unions** - For conditional schemas
   ```typescript
   const responseSchema = z.discriminatedUnion('status', [
     z.object({ status: z.literal('success'), data: z.any() }),
     z.object({ status: z.literal('error'), error: z.string() }),
   ]);
   ```

5. **Transform and validate** - Clean data, then validate
   ```typescript
   const schema = z.string()
     .trim() // Transform first
     .min(3) // Then validate
     .toLowerCase();
   ```

---

## Resources

**Official Documentation:**
- Zod: https://zod.dev/
- GitHub: https://github.com/colinhacks/zod

**Integration Guides:**
- React Hook Form: https://react-hook-form.com/get-started#SchemaValidation
- tRPC: https://trpc.io/docs/server/validators

**TypeScript Resources:**
- Type inference: https://zod.dev/?id=type-inference
- Error handling: https://zod.dev/?id=error-handling

---

## Next Steps

- Use with React Hook Form → `react-hook-form.md`
- See working examples → `examples/`
- Validation concepts → `../validation-concepts.md`
