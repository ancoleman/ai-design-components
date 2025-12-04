# Python GraphQL with Strawberry

GraphQL API using Strawberry (type-hint based) with FastAPI integration.

## Features

- Strawberry GraphQL (async)
- FastAPI integration
- Type-hint based schema
- DataLoaders (N+1 prevention)
- Subscriptions (WebSocket)
- GraphQL Playground

## Files

```
graphql-strawberry/
├── main.py                  # FastAPI + GraphQL
├── schema.py                # GraphQL schema
├── types/
│   ├── user.py
│   ├── post.py
│   └── comment.py
├── resolvers/
│   ├── user_resolver.py
│   └── post_resolver.py
├── dataloaders.py           # DataLoader setup
└── requirements.txt
```

## Quick Start

```bash
# Install
pip install 'strawberry-graphql[fastapi]' fastapi uvicorn

# Run
uvicorn main:app --reload
```

Access GraphiQL: http://localhost:8000/graphql

## Example Schema

```python
import strawberry
from typing import List

@strawberry.type
class User:
    id: int
    email: str
    name: str
    posts: List['Post']

@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author: User

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> User:
        return await fetch_user(id)

    @strawberry.field
    async def users(self) -> List[User]:
        return await fetch_all_users()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_post(self, title: str, content: str) -> Post:
        return await create_post_in_db(title, content)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

## FastAPI Integration

```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```

## DataLoader (N+1 Prevention)

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: List[int]) -> List[User]:
    users = await db.query("SELECT * FROM users WHERE id = ANY($1)", keys)
    return [users_dict[k] for k in keys]

user_loader = DataLoader(load_fn=load_users)
```
