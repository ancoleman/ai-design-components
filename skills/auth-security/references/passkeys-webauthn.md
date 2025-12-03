# Passkeys / WebAuthn Implementation Guide

Passkeys provide phishing-resistant, passwordless authentication using FIDO2/WebAuthn standards.

## What Are Passkeys?

**Passkeys** = Public key credentials stored in authenticators (devices, password managers)

**Benefits:**
- **Phishing-resistant:** Cryptographic challenge-response, domain-bound
- **No password reuse:** Each credential is unique
- **Biometric authentication:** Face ID, Touch ID, Windows Hello
- **Cross-device sync:** iCloud Keychain, Google Password Manager

**vs Passwords:**
- Password: User types secret → Server validates
- Passkey: Device signs challenge → Server verifies signature

## How Passkeys Work

### Registration Flow

```
┌──────────┐                ┌──────────┐                ┌──────────┐
│  Client  │                │  Server  │                │Authenticator│
└────┬─────┘                └────┬─────┘                └────┬─────┘
     │                           │                           │
     │ 1. Request registration   │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │ 2. Challenge + options    │                           │
     │<──────────────────────────┤                           │
     │                           │                           │
     │ 3. Create credential      │                           │
     ├───────────────────────────┼──────────────────────────>│
     │                           │                           │
     │                           │ 4. Generate key pair      │
     │                           │    Sign attestation       │
     │                           │                           │
     │ 5. Credential response    │                           │
     │<──────────────────────────┼───────────────────────────┤
     │                           │                           │
     │ 6. Send credential        │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │                           │ 7. Verify attestation     │
     │                           │    Store public key       │
     │                           │                           │
     │ 8. Success                │                           │
     │<──────────────────────────┤                           │
```

### Authentication Flow

```
┌──────────┐                ┌──────────┐                ┌──────────┐
│  Client  │                │  Server  │                │Authenticator│
└────┬─────┘                └────┬─────┘                └────┬─────┘
     │                           │                           │
     │ 1. Request login          │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │ 2. Challenge + cred IDs   │                           │
     │<──────────────────────────┤                           │
     │                           │                           │
     │ 3. Get credential         │                           │
     ├───────────────────────────┼──────────────────────────>│
     │                           │                           │
     │                           │ 4. User verification      │
     │                           │    Sign challenge         │
     │                           │                           │
     │ 5. Assertion response     │                           │
     │<──────────────────────────┼───────────────────────────┤
     │                           │                           │
     │ 6. Send assertion         │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │                           │ 7. Verify signature       │
     │                           │    with public key        │
     │                           │                           │
     │ 8. Success + session      │                           │
     │<──────────────────────────┤                           │
```

## Implementation (TypeScript)

### Install @simplewebauthn

```bash
npm install @simplewebauthn/server @simplewebauthn/browser
```

### Server Setup (Node.js/Next.js)

```typescript
// lib/webauthn.ts
import {
  generateRegistrationOptions,
  verifyRegistrationResponse,
  generateAuthenticationOptions,
  verifyAuthenticationResponse,
} from '@simplewebauthn/server'
import type {
  RegistrationResponseJSON,
  AuthenticationResponseJSON,
} from '@simplewebauthn/types'

// Replace with your domain
const RP_NAME = 'Your App'
const RP_ID = 'example.com'
const ORIGIN = 'https://example.com'

// In-memory storage (use database in production)
const users = new Map<string, {
  id: string
  username: string
  credentials: Array<{
    id: string
    publicKey: Uint8Array
    counter: number
    transports?: string[]
  }>
}>()

const challenges = new Map<string, string>()

export async function startRegistration(userId: string, username: string) {
  const user = users.get(userId) || {
    id: userId,
    username,
    credentials: [],
  }

  const options = await generateRegistrationOptions({
    rpName: RP_NAME,
    rpID: RP_ID,
    userID: userId,
    userName: username,
    userDisplayName: username,

    // Attestation: 'none' = no attestation (fastest)
    attestationType: 'none',

    // Exclude existing credentials (prevent duplicate registration)
    excludeCredentials: user.credentials.map(cred => ({
      id: cred.id,
      type: 'public-key',
      transports: cred.transports,
    })),

    // Authenticator selection
    authenticatorSelection: {
      residentKey: 'preferred', // Discoverable credential
      userVerification: 'preferred', // Biometric/PIN
      authenticatorAttachment: 'platform', // Platform authenticator (device)
    },
  })

  // Store challenge for verification
  challenges.set(userId, options.challenge)

  return options
}

export async function finishRegistration(
  userId: string,
  response: RegistrationResponseJSON
) {
  const expectedChallenge = challenges.get(userId)
  if (!expectedChallenge) {
    throw new Error('Challenge not found')
  }

  const verification = await verifyRegistrationResponse({
    response,
    expectedChallenge,
    expectedOrigin: ORIGIN,
    expectedRPID: RP_ID,
  })

  if (!verification.verified || !verification.registrationInfo) {
    throw new Error('Verification failed')
  }

  const { credentialPublicKey, credentialID, counter } = verification.registrationInfo

  // Store credential
  const user = users.get(userId)!
  user.credentials.push({
    id: Buffer.from(credentialID).toString('base64url'),
    publicKey: credentialPublicKey,
    counter,
    transports: response.response.transports,
  })
  users.set(userId, user)

  // Clear challenge
  challenges.delete(userId)

  return { verified: true }
}

export async function startAuthentication(userId?: string) {
  const options = await generateAuthenticationOptions({
    rpID: RP_ID,

    // If userId provided, include their credentials
    // Otherwise, allow discoverable credentials
    allowCredentials: userId
      ? users.get(userId)?.credentials.map(cred => ({
          id: cred.id,
          type: 'public-key',
          transports: cred.transports,
        }))
      : [],

    userVerification: 'preferred',
  })

  // Store challenge
  const challengeId = userId || 'anonymous'
  challenges.set(challengeId, options.challenge)

  return options
}

export async function finishAuthentication(
  userId: string,
  response: AuthenticationResponseJSON
) {
  const expectedChallenge = challenges.get(userId)
  if (!expectedChallenge) {
    throw new Error('Challenge not found')
  }

  const user = users.get(userId)
  if (!user) {
    throw new Error('User not found')
  }

  const credential = user.credentials.find(
    cred => cred.id === response.id
  )
  if (!credential) {
    throw new Error('Credential not found')
  }

  const verification = await verifyAuthenticationResponse({
    response,
    expectedChallenge,
    expectedOrigin: ORIGIN,
    expectedRPID: RP_ID,
    authenticator: {
      credentialID: credential.id,
      credentialPublicKey: credential.publicKey,
      counter: credential.counter,
    },
  })

  if (!verification.verified) {
    throw new Error('Verification failed')
  }

  // Update counter (prevent replay attacks)
  credential.counter = verification.authenticationInfo.newCounter

  // Clear challenge
  challenges.delete(userId)

  return { verified: true, userId }
}
```

### Client Setup (React)

```typescript
// components/PasskeyRegistration.tsx
'use client'

import { startRegistration } from '@simplewebauthn/browser'
import { useState } from 'react'

export function PasskeyRegistration({ userId, username }: { userId: string; username: string }) {
  const [status, setStatus] = useState('')

  async function handleRegister() {
    try {
      setStatus('Requesting options...')

      // 1. Get registration options from server
      const optionsResponse = await fetch('/api/passkeys/register/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, username }),
      })
      const options = await optionsResponse.json()

      setStatus('Create passkey...')

      // 2. Create credential with browser WebAuthn API
      const credential = await startRegistration(options)

      setStatus('Verifying...')

      // 3. Send credential to server for verification
      const verifyResponse = await fetch('/api/passkeys/register/finish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, credential }),
      })

      if (verifyResponse.ok) {
        setStatus('Passkey registered successfully!')
      } else {
        setStatus('Registration failed')
      }
    } catch (error) {
      console.error(error)
      setStatus('Error: ' + (error as Error).message)
    }
  }

  return (
    <div>
      <button onClick={handleRegister}>Register Passkey</button>
      {status && <p>{status}</p>}
    </div>
  )
}
```

```typescript
// components/PasskeyLogin.tsx
'use client'

import { startAuthentication } from '@simplewebauthn/browser'
import { useState } from 'react'

export function PasskeyLogin({ userId }: { userId?: string }) {
  const [status, setStatus] = useState('')

  async function handleLogin() {
    try {
      setStatus('Requesting challenge...')

      // 1. Get authentication options from server
      const optionsResponse = await fetch('/api/passkeys/login/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      })
      const options = await optionsResponse.json()

      setStatus('Authenticate...')

      // 2. Get credential with browser WebAuthn API
      const credential = await startAuthentication(options)

      setStatus('Verifying...')

      // 3. Send assertion to server for verification
      const verifyResponse = await fetch('/api/passkeys/login/finish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, credential }),
      })

      if (verifyResponse.ok) {
        const { session } = await verifyResponse.json()
        setStatus('Login successful!')
        // Redirect to dashboard
        window.location.href = '/dashboard'
      } else {
        setStatus('Authentication failed')
      }
    } catch (error) {
      console.error(error)
      setStatus('Error: ' + (error as Error).message)
    }
  }

  return (
    <div>
      <button onClick={handleLogin}>Login with Passkey</button>
      {status && <p>{status}</p>}
    </div>
  )
}
```

### API Routes (Next.js App Router)

```typescript
// app/api/passkeys/register/start/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { startRegistration } from '@/lib/webauthn'

export async function POST(request: NextRequest) {
  const { userId, username } = await request.json()
  const options = await startRegistration(userId, username)
  return NextResponse.json(options)
}
```

```typescript
// app/api/passkeys/register/finish/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { finishRegistration } from '@/lib/webauthn'

export async function POST(request: NextRequest) {
  const { userId, credential } = await request.json()
  const result = await finishRegistration(userId, credential)
  return NextResponse.json(result)
}
```

```typescript
// app/api/passkeys/login/start/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { startAuthentication } from '@/lib/webauthn'

export async function POST(request: NextRequest) {
  const { userId } = await request.json()
  const options = await startAuthentication(userId)
  return NextResponse.json(options)
}
```

```typescript
// app/api/passkeys/login/finish/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { finishAuthentication } from '@/lib/webauthn'

export async function POST(request: NextRequest) {
  const { userId, credential } = await request.json()
  const result = await finishAuthentication(userId, credential)

  // Create session (use your session library)
  const session = await createSession(result.userId)

  return NextResponse.json({ verified: true, session })
}
```

## Implementation (Python)

### Install py_webauthn

```bash
pip install webauthn pydantic
```

### Server Setup (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)
from webauthn.helpers.structs import (
    PublicKeyCredentialDescriptor,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    ResidentKeyRequirement,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier
from pydantic import BaseModel
import base64

app = FastAPI()

RP_NAME = "Your App"
RP_ID = "example.com"
ORIGIN = "https://example.com"

# In-memory storage (use database in production)
users = {}
challenges = {}

class RegistrationStart(BaseModel):
    user_id: str
    username: str

class RegistrationFinish(BaseModel):
    user_id: str
    credential: dict

@app.post("/api/passkeys/register/start")
async def start_registration(data: RegistrationStart):
    user = users.get(data.user_id, {
        "id": data.user_id,
        "username": data.username,
        "credentials": []
    })

    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=data.user_id,
        user_name=data.username,
        user_display_name=data.username,

        exclude_credentials=[
            PublicKeyCredentialDescriptor(id=base64.urlsafe_b64decode(cred["id"]))
            for cred in user.get("credentials", [])
        ],

        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.PREFERRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),

        supported_pub_key_algs=[
            COSEAlgorithmIdentifier.EDDSA,
            COSEAlgorithmIdentifier.ES256,
        ],
    )

    challenges[data.user_id] = options.challenge
    users[data.user_id] = user

    return options_to_json(options)

@app.post("/api/passkeys/register/finish")
async def finish_registration(data: RegistrationFinish):
    expected_challenge = challenges.get(data.user_id)
    if not expected_challenge:
        raise HTTPException(400, "Challenge not found")

    verification = verify_registration_response(
        credential=data.credential,
        expected_challenge=expected_challenge,
        expected_origin=ORIGIN,
        expected_rp_id=RP_ID,
    )

    if not verification.verified:
        raise HTTPException(400, "Verification failed")

    # Store credential
    user = users[data.user_id]
    user["credentials"].append({
        "id": base64.urlsafe_b64encode(verification.credential_id).decode(),
        "public_key": base64.urlsafe_b64encode(verification.credential_public_key).decode(),
        "counter": verification.sign_count,
    })

    del challenges[data.user_id]

    return {"verified": True}
```

## Cross-Device Passkeys

### iCloud Keychain (Apple)

**Requirements:**
- iOS 16+ or macOS 13+
- iCloud account with two-factor authentication
- Same Apple ID across devices

**How It Works:**
- Passkey stored in iCloud Keychain
- Synced across iPhone, iPad, Mac
- Accessible via Face ID, Touch ID, or password

### Google Password Manager

**Requirements:**
- Android or Chrome
- Google account
- Google Password Manager enabled

**How It Works:**
- Passkey stored in Google Password Manager
- Synced across Android devices and Chrome browsers
- Accessible via biometric or screen lock

### Third-Party Password Managers

**Supported:**
- 1Password (iOS 17+, Android, desktop)
- Bitwarden (beta support)
- Dashlane (iOS, Android)

## Discoverable Credentials

**Discoverable credentials** = Passkeys stored on authenticator, no username required for login.

### Registration

```typescript
authenticatorSelection: {
  residentKey: 'required', // Force discoverable credential
  userVerification: 'required',
}
```

### Authentication

```typescript
// No allowCredentials → browser shows passkey picker
const options = await generateAuthenticationOptions({
  rpID: RP_ID,
  allowCredentials: [], // Empty = discoverable
  userVerification: 'required',
})
```

**User Experience:**
1. User clicks "Sign in with passkey"
2. Browser shows list of available passkeys
3. User selects passkey
4. Biometric authentication
5. Logged in

## Security Considerations

### Attestation

**Attestation** = Cryptographic proof of authenticator authenticity.

**Types:**
- `none`: No attestation (fastest, recommended)
- `indirect`: Anonymized attestation
- `direct`: Full attestation (identify authenticator model)

**Use `none` unless:**
- Compliance requires device verification
- Risk-based authentication (trust certain authenticator types more)

### User Verification

**User verification** = Biometric or PIN.

**Options:**
- `required`: Must verify (most secure)
- `preferred`: Verify if possible (recommended)
- `discouraged`: Don't verify (presence only)

**Recommendation:** Use `preferred` for balance of security and UX.

### Counter (Replay Attack Prevention)

Each authentication increments counter. If counter doesn't increase, possible cloned authenticator.

```typescript
if (verification.authenticationInfo.newCounter <= credential.counter) {
  // Possible cloned credential
  throw new Error('Counter did not increase')
}
```

## Migration from Passwords

### Hybrid Approach

Allow both passkeys and passwords during transition.

```typescript
// Login page
<button onClick={loginWithPasskey}>Login with Passkey</button>
<button onClick={loginWithPassword}>Login with Password</button>

// After password login, prompt to register passkey
if (session.hasPassword && !session.hasPasskey) {
  return <PasskeyRegistrationPrompt />
}
```

### Gradual Rollout

1. **Phase 1:** Offer passkey registration (optional)
2. **Phase 2:** Encourage passkey adoption (show benefits)
3. **Phase 3:** Default to passkeys, password as fallback
4. **Phase 4:** Deprecate passwords (if feasible)

## Browser Support

| Browser | Version | Platform | Support |
|---------|---------|----------|---------|
| Chrome | 108+ | All | Full |
| Safari | 16+ | macOS 13+, iOS 16+ | Full |
| Firefox | 119+ | All | Full |
| Edge | 108+ | All | Full |

**Fallback:** Detect support and provide alternative login method.

```typescript
if (window.PublicKeyCredential) {
  // Passkeys supported
  return <PasskeyLogin />
} else {
  // Fallback to password
  return <PasswordLogin />
}
```

## Testing

### Unit Tests

```typescript
import { expect, test } from 'vitest'
import { startRegistration, finishRegistration } from './webauthn'

test('registration flow', async () => {
  const options = await startRegistration('user-123', 'alice')

  expect(options.challenge).toBeTruthy()
  expect(options.rp.id).toBe('example.com')
  expect(options.user.id).toBe('user-123')
})
```

### Integration Tests

Use [@simplewebauthn/browser-testing](https://github.com/MasterKale/SimpleWebAuthn/tree/master/packages/browser-testing) for automated testing.

## Common Issues

### Error: "The operation is insecure"

**Cause:** WebAuthn requires HTTPS (except localhost).

**Solution:** Use HTTPS in production, localhost in development.

### Error: "Credential excluded"

**Cause:** Attempting to register duplicate passkey.

**Solution:** Check `excludeCredentials` includes existing credentials.

### Error: "User verification failed"

**Cause:** Biometric authentication failed or not available.

**Solution:** Retry or fall back to password.

## Example Implementation

See `examples/passkeys-demo/` for complete runnable implementation with:
- Next.js 15 App Router
- @simplewebauthn/server and @simplewebauthn/browser
- PostgreSQL storage
- Session management
- Error handling
