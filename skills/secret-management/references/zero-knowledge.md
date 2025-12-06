# Zero-Knowledge Secret Patterns

Client-side encryption and threshold cryptography for zero-knowledge secret management.

## Table of Contents

1. [Zero-Knowledge Principles](#zero-knowledge-principles)
2. [Client-Side Encryption (E2EE)](#client-side-encryption-e2ee)
3. [Shamir's Secret Sharing](#shamirs-secret-sharing)
4. [Use Cases](#use-cases)

## Zero-Knowledge Principles

**Definition:** Server never has access to decryption keys or plaintext secrets.

**Key Properties:**
- Encryption/decryption happens client-side only
- Server stores only encrypted blobs
- Master key derived from user password (never transmitted)
- Compromise of server doesn't expose secrets

**Use Cases:**
- Password managers (1Password, Bitwarden)
- Encrypted notes (Standard Notes)
- Secure messaging (Signal, WhatsApp)
- Vault root token recovery (Shamir shares)

## Client-Side Encryption (E2EE)

### Pattern: User Password → Encryption Key

```typescript
// Client-side encryption (browser)
import { pbkdf2, randomBytes, createCipheriv, createDecipheriv } from 'crypto';

class ZeroKnowledgeVault {
  // Derive encryption key from user password
  static async deriveKey(
    password: string,
    salt: Buffer
  ): Promise<Buffer> {
    return new Promise((resolve, reject) => {
      // PBKDF2 with 100k iterations
      pbkdf2(password, salt, 100000, 32, 'sha256', (err, key) => {
        if (err) reject(err);
        else resolve(key);
      });
    });
  }

  // Encrypt secret client-side
  static async encrypt(
    plaintext: string,
    password: string,
    salt: Buffer
  ): Promise<{ encrypted: string; iv: string; salt: string }> {
    const key = await this.deriveKey(password, salt);
    const iv = randomBytes(16);

    const cipher = createCipheriv('aes-256-gcm', key, iv);
    let encrypted = cipher.update(plaintext, 'utf8', 'base64');
    encrypted += cipher.final('base64');

    const authTag = cipher.getAuthTag();

    return {
      encrypted: encrypted + ':' + authTag.toString('base64'),
      iv: iv.toString('base64'),
      salt: salt.toString('base64'),
    };
  }

  // Decrypt secret client-side
  static async decrypt(
    encryptedData: { encrypted: string; iv: string; salt: string },
    password: string
  ): Promise<string> {
    const salt = Buffer.from(encryptedData.salt, 'base64');
    const key = await this.deriveKey(password, salt);
    const iv = Buffer.from(encryptedData.iv, 'base64');

    const [ciphertext, authTagB64] = encryptedData.encrypted.split(':');
    const authTag = Buffer.from(authTagB64, 'base64');

    const decipher = createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(ciphertext, 'base64', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  }
}

// Usage
async function example() {
  const masterPassword = 'user-entered-password';
  const salt = randomBytes(32);

  // Encrypt secret (client-side)
  const encrypted = await ZeroKnowledgeVault.encrypt(
    'my-database-password',
    masterPassword,
    salt
  );

  // Send to server (server CANNOT decrypt)
  await fetch('/api/secrets', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(encrypted),
  });

  // Later: Decrypt secret (client-side)
  const decrypted = await ZeroKnowledgeVault.decrypt(encrypted, masterPassword);
  console.log(decrypted); // 'my-database-password'
}
```

### Server-Side (Zero-Knowledge)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import sqlite3

app = FastAPI()

class EncryptedSecret(BaseModel):
    encrypted: str
    iv: str
    salt: str

# Server stores ONLY encrypted data (cannot decrypt)
@app.post("/api/secrets")
async def store_secret(secret: EncryptedSecret):
    # Server has NO access to plaintext
    conn = sqlite3.connect('secrets.db')
    conn.execute('''
        INSERT INTO secrets (encrypted_data, iv, salt, created_at)
        VALUES (?, ?, ?, datetime('now'))
    ''', (secret.encrypted, secret.iv, secret.salt))
    conn.commit()
    conn.close()

    return {"status": "stored", "message": "Secret encrypted and stored"}

@app.get("/api/secrets/{id}")
async def get_secret(id: int):
    # Server returns encrypted blob (client decrypts)
    conn = sqlite3.connect('secrets.db')
    cursor = conn.execute(
        'SELECT encrypted_data, iv, salt FROM secrets WHERE id = ?',
        (id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Secret not found")

    return {
        "encrypted": row[0],
        "iv": row[1],
        "salt": row[2]
    }
```

### Web Crypto API (Browser)

```javascript
// Modern browser-based encryption
class WebCryptoVault {
  // Derive key from password
  static async deriveKey(password, salt) {
    const encoder = new TextEncoder();
    const passwordKey = await crypto.subtle.importKey(
      'raw',
      encoder.encode(password),
      'PBKDF2',
      false,
      ['deriveKey']
    );

    return crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: salt,
        iterations: 100000,
        hash: 'SHA-256',
      },
      passwordKey,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt', 'decrypt']
    );
  }

  // Encrypt
  static async encrypt(plaintext, password) {
    const salt = crypto.getRandomValues(new Uint8Array(32));
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const key = await this.deriveKey(password, salt);

    const encoder = new TextEncoder();
    const encrypted = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv: iv },
      key,
      encoder.encode(plaintext)
    );

    return {
      encrypted: btoa(String.fromCharCode(...new Uint8Array(encrypted))),
      iv: btoa(String.fromCharCode(...iv)),
      salt: btoa(String.fromCharCode(...salt)),
    };
  }

  // Decrypt
  static async decrypt(encryptedData, password) {
    const salt = Uint8Array.from(atob(encryptedData.salt), c => c.charCodeAt(0));
    const iv = Uint8Array.from(atob(encryptedData.iv), c => c.charCodeAt(0));
    const encrypted = Uint8Array.from(atob(encryptedData.encrypted), c => c.charCodeAt(0));

    const key = await this.deriveKey(password, salt);

    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: iv },
      key,
      encrypted
    );

    const decoder = new TextDecoder();
    return decoder.decode(decrypted);
  }
}

// Usage
async function example() {
  const encrypted = await WebCryptoVault.encrypt('my-secret', 'user-password');
  console.log(encrypted); // { encrypted, iv, salt }

  const decrypted = await WebCryptoVault.decrypt(encrypted, 'user-password');
  console.log(decrypted); // 'my-secret'
}
```

## Shamir's Secret Sharing

### Pattern: Threshold Cryptography

Split a secret into N shares, require M shares to reconstruct.

**Use Cases:**
- Vault root token recovery (3 of 5 key holders)
- Multi-party approval workflows
- Distributed trust (no single point of failure)

### Python Implementation

```python
from secretsharing import PlaintextToHexSecretSharer

# Split secret into 5 shares (require 3 to reconstruct)
root_token = "your-secret-root-token-here"
shares = PlaintextToHexSecretSharer.split_secret(root_token, 3, 5)

print(f"Share 1 (CTO): {shares[0]}")
print(f"Share 2 (Security Lead): {shares[1]}")
print(f"Share 3 (DevOps Lead): {shares[2]}")
print(f"Share 4 (Compliance Officer): {shares[3]}")
print(f"Share 5 (Backup - secure storage): {shares[4]}")

# Reconstruct with any 3 of 5 shares
recovered_token = PlaintextToHexSecretSharer.recover_secret(shares[0:3])
assert recovered_token == root_token

# Only 2 shares? Cannot reconstruct
try:
    PlaintextToHexSecretSharer.recover_secret(shares[0:2])
except Exception as e:
    print(f"Error: {e}")  # "Not enough shares to reconstruct"
```

### Vault Initialization with Shamir

```bash
# Initialize Vault with Shamir shares
vault operator init \
  -key-shares=5 \
  -key-threshold=3

# Output:
# Unseal Key 1: abc123...
# Unseal Key 2: def456...
# Unseal Key 3: ghi789...
# Unseal Key 4: jkl012...
# Unseal Key 5: mno345...
# Initial Root Token: hvs.CAES...

# Distribute shares to different key holders
# - Share 1 → CTO (printed to paper, secure safe)
# - Share 2 → Security Lead (password manager)
# - Share 3 → DevOps Lead (HSM)
# - Share 4 → Compliance Officer (encrypted USB)
# - Share 5 → Backup (bank vault)
```

### Unsealing Vault (Requires 3 of 5 Shares)

```bash
# Key holder 1 (CTO) provides share
vault operator unseal abc123...
# Output: Sealed: true, Progress: 1/3

# Key holder 2 (Security Lead) provides share
vault operator unseal def456...
# Output: Sealed: true, Progress: 2/3

# Key holder 3 (DevOps Lead) provides share
vault operator unseal ghi789...
# Output: Sealed: false, Progress: 3/3

# Vault is now unsealed (3 of 5 threshold met)
```

### TypeScript Implementation (sss-wasm)

```typescript
import { split, combine } from 'sss-wasm';

// Split secret
const secret = Buffer.from('my-vault-root-token', 'utf8');
const shares = split(secret, { shares: 5, threshold: 3 });

console.log(`Share 1: ${shares[0].toString('hex')}`);
console.log(`Share 2: ${shares[1].toString('hex')}`);
console.log(`Share 3: ${shares[2].toString('hex')}`);
console.log(`Share 4: ${shares[3].toString('hex')}`);
console.log(`Share 5: ${shares[4].toString('hex')}`);

// Reconstruct with 3 shares
const recovered = combine([shares[0], shares[2], shares[4]]);
console.log(recovered.toString('utf8')); // 'my-vault-root-token'

// Only 2 shares? Cannot reconstruct
try {
  combine([shares[0], shares[1]]);
} catch (err) {
  console.error('Error: Not enough shares');
}
```

## Use Cases

### Use Case 1: Password Manager

```typescript
// User registers
const masterPassword = 'user-chosen-password';
const salt = crypto.getRandomValues(new Uint8Array(32));

// Server stores salt (NOT the password)
await fetch('/api/register', {
  method: 'POST',
  body: JSON.stringify({
    username: 'alice',
    salt: btoa(String.fromCharCode(...salt)),
  }),
});

// User stores a password
const encrypted = await WebCryptoVault.encrypt('my-gmail-password', masterPassword);
await fetch('/api/passwords', {
  method: 'POST',
  body: JSON.stringify({
    site: 'gmail.com',
    ...encrypted,
  }),
});

// Server has ZERO knowledge of:
// - Master password
// - Stored password (my-gmail-password)
// - Encryption key
```

### Use Case 2: Vault Root Token Recovery

```bash
# Scenario: All Vault nodes lost, need to recover root token

# Step 1: Gather 3 of 5 key holders
# - CTO provides share 1
# - Security Lead provides share 2
# - DevOps Lead provides share 3

# Step 2: Reconstruct root token (offline)
python3 <<EOF
from secretsharing import PlaintextToHexSecretSharer
shares = [
    "abc123...",  # Share 1 from CTO
    "def456...",  # Share 2 from Security Lead
    "ghi789..."   # Share 3 from DevOps Lead
]
root_token = PlaintextToHexSecretSharer.recover_secret(shares)
print(f"Root Token: {root_token}")
EOF

# Step 3: Use root token to initialize new Vault cluster
vault login hvs.CAES...
vault operator init -recovery-shares=5 -recovery-threshold=3
```

### Use Case 3: Multi-Party Approval

```python
# Scenario: Deploy requires approval from 2 of 3 leads

from secretsharing import PlaintextToHexSecretSharer

# Deploy key (required to trigger production deployment)
deploy_key = "prod-deploy-key-2025-12-03"

# Split into 3 shares (require 2 to reconstruct)
shares = PlaintextToHexSecretSharer.split_secret(deploy_key, 2, 3)

# Distribute shares
# - Tech Lead: shares[0]
# - Product Lead: shares[1]
# - Security Lead: shares[2]

# Deployment request: Tech Lead + Product Lead provide shares
recovered_key = PlaintextToHexSecretSharer.recover_secret([shares[0], shares[1]])

# CI/CD validates key before deploying
if recovered_key == deploy_key:
    print("✓ Deployment approved by 2 of 3 leads. Proceeding...")
    deploy_to_production()
else:
    print("✗ Invalid deployment key. Approval required.")
```

## Security Considerations

**Key Derivation:**
- Use PBKDF2 with 100k+ iterations (or Argon2id)
- Random salt (32 bytes, unique per user)
- Never transmit master password

**Encryption Algorithm:**
- AES-256-GCM (authenticated encryption)
- Random IV (12 bytes for GCM, 16 for CBC)
- Verify auth tag on decryption

**Shamir Shares:**
- Distribute shares to independent key holders
- Store in different locations (geographic separation)
- Document recovery procedure
- Test recovery annually

**Password Strength:**
- Enforce minimum entropy (80+ bits)
- Use password strength meter
- Consider passphrase (4+ random words)
- Offer 2FA for account recovery
