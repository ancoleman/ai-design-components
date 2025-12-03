# Password Hashing with Argon2id

Argon2id is the recommended password hashing algorithm (OWASP 2025, winner of Password Hashing Competition 2015).

## Why Argon2id?

### Argon2 Variants

| Variant | Resistance | Use Case |
|---------|-----------|----------|
| **Argon2d** | Data-dependent (GPU-resistant) | Cryptocurrencies, no side-channel concerns |
| **Argon2i** | Data-independent (side-channel resistant) | Password hashing where timing attacks possible |
| **Argon2id** | Hybrid (best of both) | **Recommended for passwords** |

**Argon2id = First half Argon2i + Second half Argon2d**

### vs Other Algorithms

| Algorithm | Year | Memory-Hard | GPU-Resistant | Recommended |
|-----------|------|-------------|---------------|-------------|
| **Argon2id** | 2015 | Yes | Yes | ✅ Yes |
| bcrypt | 2009 | No | Partial | ⚠️ Legacy only |
| scrypt | 2009 | Yes | Partial | ⚠️ Legacy only |
| PBKDF2 | 2000 | No | No | ❌ Avoid |
| MD5 | 1992 | No | No | ❌ Never use |
| SHA-256 | 2001 | No | No | ❌ Never use |

**Memory-hard** = Requires significant memory, makes GPU/ASIC attacks expensive.

## OWASP 2025 Parameters

```
Algorithm: Argon2id
Version: 0x13 (19)
Memory cost (m): 64 MB (65536 KiB)
Time cost (t): 3 iterations
Parallelism (p): 4 threads
Salt length: 16 bytes (128 bits)
Output length: 32 bytes (256 bits)
Target hash time: 150-250ms
```

### Why These Parameters?

**Memory cost (64 MB):**
- Balances security and server capacity
- Too low: GPU attacks feasible
- Too high: DoS risk (attacker forces many hash operations)

**Time cost (3 iterations):**
- Minimum for security
- Higher values = slower hashing

**Parallelism (4 threads):**
- Utilizes modern multi-core CPUs
- Match to available CPU cores

**Hash time (150-250ms):**
- Slow enough to resist brute-force
- Fast enough for good UX
- Adjust memory cost to hit this target on YOUR hardware

## Implementation

### TypeScript (via Rust FFI)

JavaScript has no native Argon2id implementation. Use Rust via FFI or external binary.

**Option 1: @node-rs/argon2 (Rust binding)**

```bash
npm install @node-rs/argon2
```

```typescript
import { hash, verify } from '@node-rs/argon2'

// Hash password
const password = 'user_password'
const passwordHash = await hash(password, {
  memoryCost: 65536,    // 64 MB
  timeCost: 3,          // iterations
  parallelism: 4,       // threads
  outputLen: 32,        // 32 bytes
})

console.log(passwordHash)
// $argon2id$v=19$m=65536,t=3,p=4$randomsalt$hashoutput

// Verify password (timing-safe)
const isValid = await verify(passwordHash, password)
console.log(isValid) // true
```

**Option 2: argon2 (Node.js C++ binding)**

```bash
npm install argon2
```

```typescript
import * as argon2 from 'argon2'

// Hash password
const passwordHash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 65536,
  timeCost: 3,
  parallelism: 4,
  hashLength: 32,
})

// Verify password
const isValid = await argon2.verify(passwordHash, password)
```

### Python (argon2-cffi)

```bash
pip install argon2-cffi
```

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize with OWASP 2025 parameters
ph = PasswordHasher(
    time_cost=3,        # iterations
    memory_cost=65536,  # 64 MB in KiB
    parallelism=4,      # threads
    hash_len=32,        # output length
    salt_len=16         # salt length
)

# Hash password
password = "user_password"
password_hash = ph.hash(password)
print(password_hash)
# $argon2id$v=19$m=65536,t=3,p=4$randomsalt$hashoutput

# Verify password (timing-safe)
try:
    ph.verify(password_hash, password)
    print("Password matches")

    # Check if rehashing needed (parameters changed)
    if ph.check_needs_rehash(password_hash):
        new_hash = ph.hash(password)
        # Update database with new_hash

except VerifyMismatchError:
    print("Invalid password")
```

### Rust (argon2)

```bash
cargo add argon2
```

```rust
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2, Params, Algorithm, Version
};

// Create Argon2 instance with OWASP 2025 parameters
let params = Params::new(
    65536,  // memory cost (64 MB in KiB)
    3,      // time cost
    4,      // parallelism
    Some(32) // output length
).unwrap();

let argon2 = Argon2::new(
    Algorithm::Argon2id,
    Version::V0x13,
    params
);

// Hash password
let password = b"user_password";
let salt = SaltString::generate(&mut OsRng);
let password_hash = argon2
    .hash_password(password, &salt)
    .unwrap()
    .to_string();

println!("{}", password_hash);

// Verify password (timing-safe)
let parsed_hash = PasswordHash::new(&password_hash).unwrap();
match argon2.verify_password(password, &parsed_hash) {
    Ok(_) => println!("Password matches"),
    Err(_) => println!("Invalid password"),
}
```

### Go (golang.org/x/crypto/argon2)

```bash
go get golang.org/x/crypto/argon2
```

```go
package main

import (
    "crypto/rand"
    "crypto/subtle"
    "encoding/base64"
    "fmt"
    "strings"

    "golang.org/x/crypto/argon2"
)

// Hash password
func HashPassword(password string) (string, error) {
    // Generate 16-byte salt
    salt := make([]byte, 16)
    if _, err := rand.Read(salt); err != nil {
        return "", err
    }

    // Hash with OWASP 2025 parameters
    hash := argon2.IDKey(
        []byte(password),
        salt,
        3,      // time cost
        65536,  // memory cost (64 MB in KiB)
        4,      // parallelism
        32,     // output length
    )

    // Encode as PHC string format
    b64Salt := base64.RawStdEncoding.EncodeToString(salt)
    b64Hash := base64.RawStdEncoding.EncodeToString(hash)

    return fmt.Sprintf("$argon2id$v=19$m=65536,t=3,p=4$%s$%s", b64Salt, b64Hash), nil
}

// Verify password (timing-safe)
func VerifyPassword(password, encodedHash string) (bool, error) {
    parts := strings.Split(encodedHash, "$")
    if len(parts) != 6 {
        return false, fmt.Errorf("invalid hash format")
    }

    // Parse parameters (simplified, use library for production)
    salt, _ := base64.RawStdEncoding.DecodeString(parts[4])
    hash, _ := base64.RawStdEncoding.DecodeString(parts[5])

    // Hash input password
    compareHash := argon2.IDKey(
        []byte(password),
        salt,
        3,      // time cost
        65536,  // memory cost
        4,      // parallelism
        32,     // output length
    )

    // Timing-safe comparison
    return subtle.ConstantTimeCompare(hash, compareHash) == 1, nil
}
```

## PHC String Format

Password Hashing Competition (PHC) standard format:

```
$argon2id$v=19$m=65536,t=3,p=4$salt$hash
│         │     │              │    │
│         │     │              │    └─ Base64-encoded hash (32 bytes)
│         │     │              └────── Base64-encoded salt (16 bytes)
│         │     └───────────────────── Parameters (m, t, p)
│         └─────────────────────────── Version (19 = 0x13)
└───────────────────────────────────── Algorithm (argon2id)
```

**Components:**
- `argon2id`: Algorithm variant
- `v=19`: Version (0x13 in hex)
- `m=65536`: Memory cost in KiB
- `t=3`: Time cost (iterations)
- `p=4`: Parallelism (threads)
- `salt`: Base64-encoded random salt
- `hash`: Base64-encoded hash output

## Tuning Parameters for Your Hardware

### Benchmark Script

Use `scripts/benchmark_argon2.py` to tune parameters:

```bash
python scripts/benchmark_argon2.py

# Output:
# Testing Argon2id parameters...
# m=32768 (32 MB), t=3, p=4: 120ms ⚠️ Too fast
# m=65536 (64 MB), t=3, p=4: 180ms ✅ Target range
# m=98304 (96 MB), t=3, p=4: 270ms ⚠️ Too slow
#
# Recommended: m=65536, t=3, p=4
```

### Guidelines

**Start with OWASP defaults:**
- m=65536, t=3, p=4

**Adjust memory cost (m) if needed:**
- Hash time < 100ms → Increase m (e.g., 98304 = 96 MB)
- Hash time > 300ms → Decrease m (e.g., 49152 = 48 MB)

**Don't decrease time cost (t) below 3:**
- Security requirement

**Match parallelism (p) to CPU cores:**
- p=4 for 4+ core servers
- p=2 for 2-core servers

## Migration from bcrypt/scrypt

### Gradual Migration Strategy

Don't force password resets. Migrate on next login.

```python
def verify_and_migrate(password: str, stored_hash: str) -> tuple[bool, str | None]:
    """Verify password and migrate to Argon2id if needed."""

    # Already using Argon2id
    if stored_hash.startswith('$argon2id$'):
        try:
            ph.verify(stored_hash, password)

            # Check if parameters changed
            if ph.check_needs_rehash(stored_hash):
                new_hash = ph.hash(password)
                return (True, new_hash)  # Valid, needs rehash

            return (True, None)  # Valid, no rehash needed

        except VerifyMismatchError:
            return (False, None)  # Invalid password

    # Legacy bcrypt
    elif stored_hash.startswith('$2a$') or stored_hash.startswith('$2b$'):
        import bcrypt
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            # Valid password - migrate to Argon2id
            new_hash = ph.hash(password)
            return (True, new_hash)
        else:
            return (False, None)

    # Legacy scrypt (example format: scrypt$salt$hash)
    elif stored_hash.startswith('scrypt$'):
        # Verify with scrypt
        is_valid = verify_scrypt(password, stored_hash)
        if is_valid:
            new_hash = ph.hash(password)
            return (True, new_hash)
        else:
            return (False, None)

    else:
        raise ValueError(f"Unknown hash format: {stored_hash[:10]}")
```

**Login handler:**
```python
@app.post("/login")
async def login(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(401, "Invalid credentials")

    is_valid, new_hash = verify_and_migrate(password, user["password_hash"])

    if not is_valid:
        raise HTTPException(401, "Invalid credentials")

    # Update hash if migration occurred
    if new_hash:
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password_hash": new_hash}}
        )

    # Create session
    session = create_session(user["_id"])
    return {"session": session}
```

### Migration Tracking

Track migration progress:

```python
# Add field to users table
await db.users.update_many(
    {},
    {"$set": {"password_hash_algorithm": "bcrypt"}}
)

# After migration
await db.users.update_one(
    {"_id": user_id},
    {"$set": {
        "password_hash": new_hash,
        "password_hash_algorithm": "argon2id"
    }}
)

# Check migration progress
bcrypt_count = await db.users.count_documents({"password_hash_algorithm": "bcrypt"})
argon2_count = await db.users.count_documents({"password_hash_algorithm": "argon2id"})

print(f"Migration progress: {argon2_count}/{bcrypt_count + argon2_count} users")
```

## Security Best Practices

### 1. Use Timing-Safe Comparison

All implementations above use timing-safe comparison (constant-time).

**Why:** Prevent timing attacks that reveal password length or hash details.

### 2. Never Store Plaintext Passwords

**Bad:**
```sql
INSERT INTO users (email, password) VALUES ('alice@example.com', 'password123')
```

**Good:**
```sql
INSERT INTO users (email, password_hash) VALUES ('alice@example.com', '$argon2id$...')
```

### 3. Salt is Automatic

Argon2 implementations generate random salt automatically. Never reuse salts.

### 4. Don't Log Passwords or Hashes

**Bad:**
```python
logger.info(f"User {email} attempted login with password: {password}")
```

**Good:**
```python
logger.info(f"User {email} attempted login")
```

### 5. Rate Limit Login Attempts

```typescript
import rateLimit from 'express-rate-limit'

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: 'Too many login attempts, try again later',
  standardHeaders: true,
  legacyHeaders: false,
})

app.post('/login', loginLimiter, async (req, res) => {
  // Login logic
})
```

### 6. Use Pepper (Optional)

Pepper = Secret key added to password before hashing (stored separately from database).

```python
import os

PEPPER = os.environ.get('PASSWORD_PEPPER')  # Store in env var, not database

def hash_password_with_pepper(password: str) -> str:
    peppered = password + PEPPER
    return ph.hash(peppered)

def verify_password_with_pepper(password: str, hash: str) -> bool:
    peppered = password + PEPPER
    try:
        ph.verify(hash, peppered)
        return True
    except VerifyMismatchError:
        return False
```

**Benefits:**
- Even if database compromised, attacker needs pepper to crack passwords
- Pepper stored separately (env var, secrets manager)

**Drawbacks:**
- If pepper lost, all passwords invalid (users must reset)
- Rotating pepper requires rehashing all passwords

## Password Policies

### NIST SP 800-63B Guidelines (2025)

**Recommended:**
- Minimum length: 8 characters
- Maximum length: 64+ characters
- Allow all printable ASCII + Unicode
- Check against known breached passwords (Have I Been Pwned API)
- No complexity requirements (upper, lower, number, symbol)
- No periodic password changes

**Avoid:**
- Short maximum length (< 64)
- Forced complexity rules (leads to weak patterns: "Password1!")
- Password expiration (leads to "Password1", "Password2", etc.)

### Implementation

```typescript
import { z } from 'zod'
import axios from 'axios'

const PasswordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password must be at most 128 characters')

async function checkPasswordBreach(password: string): Promise<boolean> {
  // Check against Have I Been Pwned API
  const hash = createHash('sha1').update(password).digest('hex').toUpperCase()
  const prefix = hash.substring(0, 5)
  const suffix = hash.substring(5)

  const response = await axios.get(`https://api.pwnedpasswords.com/range/${prefix}`)
  const hashes = response.data.split('\n')

  return hashes.some((line: string) => line.startsWith(suffix))
}

async function validatePassword(password: string) {
  // Schema validation
  const result = PasswordSchema.safeParse(password)
  if (!result.success) {
    throw new Error(result.error.errors[0].message)
  }

  // Breach check
  const isBreached = await checkPasswordBreach(password)
  if (isBreached) {
    throw new Error('Password has been found in data breaches. Please choose a different password.')
  }
}
```

## Common Issues

### Issue: Hash Time Too Long

**Symptom:** Password hashing takes > 500ms

**Solution:**
- Reduce memory cost (m) to 49152 (48 MB) or 32768 (32 MB)
- Keep time cost (t) at 3 minimum
- Benchmark on production hardware, not development laptop

### Issue: Hash Format Not Recognized

**Symptom:** `PasswordHash::new() failed: invalid PHC string`

**Solution:**
- Ensure hash starts with `$argon2id$`
- Check for truncated hashes (database field too short)
- Validate base64 encoding of salt/hash

### Issue: Verification Always Fails

**Symptom:** Correct password fails verification

**Solution:**
- Check if pepper is being used inconsistently
- Ensure hash stored completely (not truncated)
- Verify parameters match between hash and verify
- Check for character encoding issues (UTF-8)

## Performance Considerations

### Database Storage

Store hash in VARCHAR or TEXT field (minimum 100 characters).

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,  -- Argon2id hash
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Async Hashing (Node.js)

Hash passwords asynchronously to avoid blocking event loop:

```typescript
// Good - async
const hash = await argon2.hash(password)

// Bad - blocks event loop
const hash = argon2.hashSync(password)
```

### Worker Threads (Heavy Load)

For high-concurrency applications, offload hashing to worker threads:

```typescript
import { Worker } from 'worker_threads'

function hashPasswordWorker(password: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./hash-worker.js', {
      workerData: { password },
    })

    worker.on('message', resolve)
    worker.on('error', reject)
  })
}
```

## Testing

### Unit Tests

```typescript
import { expect, test } from 'vitest'
import { hash, verify } from '@node-rs/argon2'

test('hash and verify password', async () => {
  const password = 'test_password'
  const passwordHash = await hash(password)

  expect(passwordHash).toMatch(/^\$argon2id\$/)

  const isValid = await verify(passwordHash, password)
  expect(isValid).toBe(true)

  const isInvalid = await verify(passwordHash, 'wrong_password')
  expect(isInvalid).toBe(false)
})

test('hash time within target range', async () => {
  const start = Date.now()
  await hash('test_password')
  const duration = Date.now() - start

  expect(duration).toBeGreaterThan(100) // > 100ms (secure)
  expect(duration).toBeLessThan(500)    // < 500ms (good UX)
})
```

## Benchmarking

Use `scripts/benchmark_argon2.py` to measure hash performance:

```bash
python scripts/benchmark_argon2.py --samples 10

# Output:
# Benchmarking Argon2id with 10 samples...
# m=65536, t=3, p=4
# Average: 182ms
# Min: 175ms
# Max: 195ms
# Std Dev: 6ms
```

Adjust parameters to achieve 150-250ms on your production hardware.
