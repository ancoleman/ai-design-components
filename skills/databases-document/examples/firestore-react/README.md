# Firestore + React Real-Time Example

React application with Firestore real-time listeners, offline support, and security rules.

## Stack

- React 18
- Firebase/Firestore
- Real-time listeners (onSnapshot)
- Offline persistence
- Firestore Security Rules
- TypeScript

## Features

- Real-time data synchronization
- Offline support with local cache
- Optimistic updates
- Security rules enforcement
- Subcollection queries

## Project Structure

```
firestore-react/
├── src/
│   ├── firebase.ts          # Firebase configuration
│   ├── hooks/
│   │   ├── useCollection.ts # Real-time collection hook
│   │   └── useDocument.ts   # Real-time document hook
│   ├── components/
│   │   ├── PostList.tsx
│   │   └── CreatePost.tsx
│   └── App.tsx
├── firestore.rules          # Security rules
└── package.json
```

## Quick Start

```bash
# Install
npm install firebase

# Configure Firebase (create project at console.firebase.google.com)
# Add config to .env

# Run
npm run dev
```

## Firebase Setup

```typescript
// src/firebase.ts
import { initializeApp } from 'firebase/app';
import { getFirestore, enableIndexedDbPersistence } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: "myapp.firebaseapp.com",
  projectId: "myapp",
  storageBucket: "myapp.appspot.com",
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

// Enable offline persistence
enableIndexedDbPersistence(db).catch((err) => {
  if (err.code === 'failed-precondition') {
    console.warn('Multiple tabs open, persistence can only be enabled in one tab');
  }
});
```

## Real-Time Hooks

```typescript
// hooks/useCollection.ts
import { useEffect, useState } from 'react';
import { collection, query, onSnapshot, QueryConstraint } from 'firebase/firestore';
import { db } from '../firebase';

export function useCollection<T>(
  collectionName: string,
  ...queryConstraints: QueryConstraint[]
) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const q = query(collection(db, collectionName), ...queryConstraints);

    const unsubscribe = onSnapshot(
      q,
      (snapshot) => {
        const items = snapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        })) as T[];

        setData(items);
        setLoading(false);
      },
      (err) => {
        setError(err);
        setLoading(false);
      }
    );

    return () => unsubscribe();
  }, [collectionName]);

  return { data, loading, error };
}
```

## Real-Time Component

```typescript
// components/PostList.tsx
import { useCollection } from '../hooks/useCollection';
import { orderBy, limit } from 'firebase/firestore';

interface Post {
  id: string;
  title: string;
  content: string;
  createdAt: Date;
}

export function PostList() {
  const { data: posts, loading } = useCollection<Post>(
    'posts',
    orderBy('createdAt', 'desc'),
    limit(20)
  );

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {posts.map((post) => (
        <div key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
}
```

## CRUD Operations

```typescript
import {
  collection,
  addDoc,
  updateDoc,
  deleteDoc,
  doc,
  serverTimestamp,
} from 'firebase/firestore';

// Create
const createPost = async (title: string, content: string) => {
  await addDoc(collection(db, 'posts'), {
    title,
    content,
    createdAt: serverTimestamp(),
    userId: currentUser.uid,
  });
};

// Update
const updatePost = async (postId: string, updates: Partial<Post>) => {
  await updateDoc(doc(db, 'posts', postId), {
    ...updates,
    updatedAt: serverTimestamp(),
  });
};

// Delete
const deletePost = async (postId: string) => {
  await deleteDoc(doc(db, 'posts', postId));
};
```

## Security Rules

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Posts: Read public, write authenticated
    match /posts/{postId} {
      allow read: if true;
      allow create: if request.auth != null
                    && request.resource.data.userId == request.auth.uid;
      allow update, delete: if request.auth != null
                             && resource.data.userId == request.auth.uid;
    }

    // Comments: Nested under posts
    match /posts/{postId}/comments/{commentId} {
      allow read: if true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth.uid == resource.data.userId;
    }

    // User profiles: Read public, write owner only
    match /users/{userId} {
      allow read: if true;
      allow write: if request.auth.uid == userId;
    }
  }
}
```

## Optimistic Updates

```typescript
import { doc, updateDoc, writeBatch } from 'firebase/firestore';

function PostActions({ postId }: { postId: string }) {
  const [likes, setLikes] = useState(0);

  const handleLike = async () => {
    // Optimistic update
    setLikes((prev) => prev + 1);

    try {
      await updateDoc(doc(db, 'posts', postId), {
        likes: increment(1),
      });
    } catch (error) {
      // Rollback on error
      setLikes((prev) => prev - 1);
    }
  };

  return <button onClick={handleLike}>❤️ {likes}</button>;
}
```

## Batch Operations

```typescript
import { writeBatch, doc } from 'firebase/firestore';

const batch = writeBatch(db);

// Add operations to batch
batch.set(doc(db, 'users', 'user1'), { name: 'Alice' });
batch.update(doc(db, 'posts', 'post1'), { views: increment(1) });
batch.delete(doc(db, 'temp', 'temp1'));

// Commit atomically
await batch.commit();
```

## Real-Time Presence

```typescript
import { onDisconnect, ref, set } from 'firebase/database';
import { getDatabase } from 'firebase/database';

const rtdb = getDatabase();
const userStatusRef = ref(rtdb, `/status/${currentUser.uid}`);

// Set online
await set(userStatusRef, {
  state: 'online',
  lastSeen: serverTimestamp(),
});

// Set offline on disconnect
onDisconnect(userStatusRef).set({
  state: 'offline',
  lastSeen: serverTimestamp(),
});
```

## Integration Summary

- **Real-time updates** - onSnapshot for live data
- **Offline support** - IndexedDB persistence
- **Security** - Firestore rules enforce access control
- **Optimistic UI** - Update UI before server confirms
- **Batch writes** - Atomic multi-document operations

## Best Practices

1. **Enable offline persistence** - Better UX on poor connections
2. **Security rules** - Never trust client, validate server-side
3. **Optimize queries** - Create indexes for filtered/sorted fields
4. **Limit listeners** - Unsubscribe when component unmounts
5. **Handle errors** - Network failures, permission denied
6. **Batch writes** - Atomic multi-operation updates
7. **Denormalize** - Duplicate data for read performance

## Resources

- Firestore Docs: https://firebase.google.com/docs/firestore
- React Fire: https://github.com/FirebaseExtended/reactfire
- Security Rules: https://firebase.google.com/docs/firestore/security/get-started
