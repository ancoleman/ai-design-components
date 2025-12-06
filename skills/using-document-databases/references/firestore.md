# Firestore Complete Guide

Firebase/GCP Firestore real-time sync, security rules, and mobile-first patterns.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Data Model](#data-model)
- [Real-Time Listeners](#real-time-listeners)
- [Security Rules](#security-rules)
- [Queries](#queries)
- [Offline Support](#offline-support)
- [Performance Best Practices](#performance-best-practices)

---

## Core Concepts

### Firestore vs Realtime Database

| Feature | Firestore | Realtime Database |
|---------|-----------|-------------------|
| **Data Model** | Collections & documents | JSON tree |
| **Queries** | Rich queries, indexes | Limited queries |
| **Scaling** | Automatic | Manual sharding |
| **Offline** | Full offline support | Limited |
| **Pricing** | Per operation | Per GB downloaded |

### Key Features

- **Real-time sync**: Live updates across all clients
- **Offline-first**: Local cache, auto-sync when online
- **Security rules**: Declarative access control
- **Atomic operations**: Batched writes, transactions
- **Automatic indexing**: Composite indexes for queries

---

## Data Model

### Collections and Documents

```
users (collection)
├── user123 (document)
│   ├── email: "user@example.com"
│   ├── name: "Jane Doe"
│   └── orders (subcollection)
│       ├── order001 (document)
│       └── order002 (document)
└── user456 (document)
    └── ...
```

### Document Structure

```typescript
// Document in users collection
{
  // Auto-generated ID
  id: "user123",

  // Document data
  email: "user@example.com",
  name: "Jane Doe",
  age: 32,
  address: {
    street: "123 Main St",
    city: "Boston",
    state: "MA"
  },
  tags: ["premium", "verified"],
  createdAt: Timestamp,
  metadata: {
    lastLogin: Timestamp,
    loginCount: 42
  }
}
```

**Document Limits:**
- Max size: 1 MB
- Max depth: 20 levels
- Max field name: 1,500 bytes

---

## Real-Time Listeners

### React Component with Real-Time Updates

```typescript
import { collection, query, where, onSnapshot } from 'firebase/firestore'
import { useEffect, useState } from 'react'

function OrderList({ userId }: { userId: string }) {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const q = query(
      collection(db, 'orders'),
      where('userId', '==', userId),
      where('status', '==', 'pending')
    )

    // Real-time listener
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const orderData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      setOrders(orderData)
      setLoading(false)
    }, (error) => {
      console.error('Error:', error)
    })

    // Cleanup on unmount
    return () => unsubscribe()
  }, [userId])

  if (loading) return <div>Loading...</div>

  return (
    <div>
      {orders.map(order => (
        <div key={order.id}>{order.orderNumber}</div>
      ))}
    </div>
  )
}
```

### Listening to Document Changes

```typescript
import { doc, onSnapshot } from 'firebase/firestore'

// Listen to single document
const unsubscribe = onSnapshot(doc(db, 'users', userId), (doc) => {
  if (doc.exists()) {
    console.log('User data:', doc.data())
  }
})

// Detect change type
onSnapshot(collection(db, 'orders'), (snapshot) => {
  snapshot.docChanges().forEach((change) => {
    if (change.type === 'added') {
      console.log('New order:', change.doc.data())
    }
    if (change.type === 'modified') {
      console.log('Modified order:', change.doc.data())
    }
    if (change.type === 'removed') {
      console.log('Removed order:', change.doc.data())
    }
  })
})
```

---

## Security Rules

### Basic Rules Structure

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Rules go here
  }
}
```

### Common Patterns

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 1. Public read, authenticated write
    match /products/{productId} {
      allow read: if true;
      allow write: if request.auth != null;
    }

    // 2. User can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // 3. Orders: users can only see their own
    match /orders/{orderId} {
      // Read: must be authenticated and own the order
      allow read: if request.auth != null &&
                     resource.data.userId == request.auth.uid;

      // Create: must be authenticated and set userId to their own ID
      allow create: if request.auth != null &&
                       request.resource.data.userId == request.auth.uid;

      // Update/Delete: must own the order
      allow update, delete: if request.auth != null &&
                               resource.data.userId == request.auth.uid;
    }

    // 4. Admin-only writes
    match /config/{document} {
      allow read: if true;
      allow write: if request.auth != null &&
                      request.auth.token.admin == true;
    }

    // 5. Validate data on write
    match /posts/{postId} {
      allow create: if request.auth != null &&
                       request.resource.data.title is string &&
                       request.resource.data.title.size() > 0 &&
                       request.resource.data.title.size() <= 100 &&
                       request.resource.data.userId == request.auth.uid;
    }

    // 6. Subcollection access
    match /users/{userId}/orders/{orderId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // 7. Rate limiting (prevent abuse)
    match /posts/{postId} {
      allow create: if request.auth != null &&
                       request.time > resource.data.lastPost + duration.value(1, 'm');
    }
  }
}
```

### Rule Functions

```javascript
// Helper functions
function isSignedIn() {
  return request.auth != null;
}

function isOwner(userId) {
  return request.auth.uid == userId;
}

function isAdmin() {
  return isSignedIn() && request.auth.token.admin == true;
}

function validString(field, minLen, maxLen) {
  let value = request.resource.data[field];
  return value is string &&
         value.size() >= minLen &&
         value.size() <= maxLen;
}

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /posts/{postId} {
      allow read: if true;
      allow create: if isSignedIn() &&
                       isOwner(request.resource.data.userId) &&
                       validString('title', 1, 100);
    }
  }
}
```

---

## Queries

### Basic Queries

```typescript
import { collection, query, where, orderBy, limit, getDocs } from 'firebase/firestore'

// Simple equality
const q = query(
  collection(db, 'orders'),
  where('userId', '==', 'user123')
)
const snapshot = await getDocs(q)
snapshot.forEach(doc => console.log(doc.data()))

// Multiple conditions (AND)
const q = query(
  collection(db, 'products'),
  where('category', '==', 'electronics'),
  where('price', '<=', 500),
  orderBy('price', 'asc')
)

// OR queries (requires composite index)
const q = query(
  collection(db, 'products'),
  or(
    where('category', '==', 'electronics'),
    where('category', '==', 'books')
  )
)

// In queries (up to 10 values)
const q = query(
  collection(db, 'products'),
  where('category', 'in', ['electronics', 'books', 'toys'])
)

// Array contains
const q = query(
  collection(db, 'users'),
  where('tags', 'array-contains', 'premium')
)

// Array contains any
const q = query(
  collection(db, 'users'),
  where('tags', 'array-contains-any', ['premium', 'verified'])
)
```

### Pagination

```typescript
// First page
const first = query(
  collection(db, 'products'),
  orderBy('price'),
  limit(20)
)
const snapshot = await getDocs(first)
const lastVisible = snapshot.docs[snapshot.docs.length - 1]

// Next page
const next = query(
  collection(db, 'products'),
  orderBy('price'),
  startAfter(lastVisible),
  limit(20)
)
```

### Composite Indexes

Firestore automatically creates indexes for simple queries. Composite indexes required for:
- Multiple inequality filters
- Inequality + orderBy on different fields
- OR queries

```typescript
// Requires composite index: category (asc), price (asc)
const q = query(
  collection(db, 'products'),
  where('category', '==', 'electronics'),
  orderBy('price', 'asc')
)
```

**Create index via Firebase Console or CLI:**
```bash
firebase deploy --only firestore:indexes
```

---

## CRUD Operations

### Create

```typescript
import { collection, addDoc, setDoc, doc } from 'firebase/firestore'

// Auto-generate ID
const docRef = await addDoc(collection(db, 'users'), {
  email: 'user@example.com',
  name: 'Jane Doe',
  createdAt: new Date()
})
console.log('Created with ID:', docRef.id)

// Custom ID
await setDoc(doc(db, 'users', 'user123'), {
  email: 'user@example.com',
  name: 'Jane Doe'
})

// Merge (update if exists, create if not)
await setDoc(doc(db, 'users', 'user123'), {
  lastLogin: new Date()
}, { merge: true })
```

### Read

```typescript
import { doc, getDoc, collection, getDocs } from 'firebase/firestore'

// Get single document
const docSnap = await getDoc(doc(db, 'users', 'user123'))
if (docSnap.exists()) {
  console.log(docSnap.data())
}

// Get all documents in collection
const querySnapshot = await getDocs(collection(db, 'users'))
querySnapshot.forEach(doc => console.log(doc.id, doc.data()))
```

### Update

```typescript
import { doc, updateDoc, increment, arrayUnion, serverTimestamp } from 'firebase/firestore'

// Update fields
await updateDoc(doc(db, 'users', 'user123'), {
  name: 'Jane Smith',
  'address.city': 'Boston'  // Nested field
})

// Increment counter
await updateDoc(doc(db, 'posts', 'post123'), {
  views: increment(1)
})

// Add to array (no duplicates)
await updateDoc(doc(db, 'users', 'user123'), {
  tags: arrayUnion('premium')
})

// Remove from array
await updateDoc(doc(db, 'users', 'user123'), {
  tags: arrayRemove('trial')
})

// Server timestamp
await updateDoc(doc(db, 'users', 'user123'), {
  updatedAt: serverTimestamp()
})
```

### Delete

```typescript
import { doc, deleteDoc, deleteField } from 'firebase/firestore'

// Delete document
await deleteDoc(doc(db, 'users', 'user123'))

// Delete field
await updateDoc(doc(db, 'users', 'user123'), {
  phoneNumber: deleteField()
})
```

---

## Transactions and Batches

### Transactions (Atomic Reads and Writes)

```typescript
import { runTransaction } from 'firebase/firestore'

// Transfer credits between users
await runTransaction(db, async (transaction) => {
  const fromRef = doc(db, 'users', 'user123')
  const toRef = doc(db, 'users', 'user456')

  const fromDoc = await transaction.get(fromRef)
  if (!fromDoc.exists()) {
    throw new Error('User not found')
  }

  const currentBalance = fromDoc.data().credits
  if (currentBalance < 100) {
    throw new Error('Insufficient credits')
  }

  transaction.update(fromRef, { credits: currentBalance - 100 })
  transaction.update(toRef, { credits: increment(100) })
})
```

### Batched Writes

```typescript
import { writeBatch } from 'firebase/firestore'

// Batch write (up to 500 operations)
const batch = writeBatch(db)

batch.set(doc(db, 'users', 'user1'), { name: 'User 1' })
batch.update(doc(db, 'users', 'user2'), { active: true })
batch.delete(doc(db, 'users', 'user3'))

await batch.commit()
```

---

## Offline Support

### Enable Offline Persistence

```typescript
import { initializeFirestore, persistentLocalCache } from 'firebase/firestore'

const db = initializeFirestore(app, {
  localCache: persistentLocalCache()
})
```

### Offline Behavior

```typescript
import { onSnapshot } from 'firebase/firestore'

// Listener works offline
onSnapshot(collection(db, 'orders'), (snapshot) => {
  snapshot.forEach(doc => {
    // fromCache indicates if data is from local cache
    console.log(`${doc.id} (from cache: ${doc.metadata.fromCache})`)
  })
})

// Writes queued offline, synced when online
await addDoc(collection(db, 'orders'), {
  userId: 'user123',
  items: [...]
})
// If offline, write is queued and will sync when online
```

---

## Performance Best Practices

### Minimize Document Reads

```typescript
// BAD: Read same document multiple times
const userDoc = await getDoc(doc(db, 'users', userId))
// ... later ...
const userDoc2 = await getDoc(doc(db, 'users', userId))  // Duplicate read!

// GOOD: Cache document in memory
const userDoc = await getDoc(doc(db, 'users', userId))
const userData = userDoc.data()
// Use userData throughout component
```

### Use Subcollections for Large Arrays

```typescript
// BAD: Store unbounded array in document
{
  userId: "user123",
  orders: [
    { orderId: "order1", ... },
    { orderId: "order2", ... },
    // ... 1000s of orders (exceeds 1MB limit!)
  ]
}

// GOOD: Use subcollection
// users/user123/orders/order1
// users/user123/orders/order2
const ordersRef = collection(db, 'users', userId, 'orders')
```

### Denormalize for Read Performance

```typescript
// Store frequently accessed data together
{
  postId: "post123",
  title: "My Post",
  content: "...",
  // Denormalize author info (instead of reference)
  author: {
    id: "user123",
    name: "Jane Doe",
    avatar: "/avatars/jane.jpg"
  },
  // Update pattern: when user updates profile, update all posts
}
```

### Use Server Timestamps

```typescript
import { serverTimestamp } from 'firebase/firestore'

// Better than client timestamp (avoids clock skew)
await addDoc(collection(db, 'posts'), {
  title: 'My Post',
  createdAt: serverTimestamp()
})
```

---

## Mobile Integration (React Native)

```typescript
import { initializeApp } from 'firebase/app'
import { getFirestore, collection, onSnapshot } from 'firebase/firestore'
import { useEffect, useState } from 'react'

const firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  projectId: "..."
}

const app = initializeApp(firebaseConfig)
const db = getFirestore(app)

function OrdersScreen({ userId }) {
  const [orders, setOrders] = useState([])

  useEffect(() => {
    const unsubscribe = onSnapshot(
      collection(db, 'orders'),
      where('userId', '==', userId),
      (snapshot) => {
        const orderData = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }))
        setOrders(orderData)
      }
    )

    return () => unsubscribe()
  }, [userId])

  return (
    <FlatList
      data={orders}
      keyExtractor={item => item.id}
      renderItem={({ item }) => <OrderItem order={item} />}
    />
  )
}
```

---

This guide covers Firestore real-time patterns and mobile-first architecture. For complete React implementation, see `../examples/firestore-react/`.
