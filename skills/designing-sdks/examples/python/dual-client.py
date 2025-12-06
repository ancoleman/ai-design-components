"""
Dual Sync/Async Client Example (Python)

Demonstrates both sync and async clients sharing common logic.
"""

import os
import asyncio
from typing import Dict, Any


class BaseClient:
    """Shared logic between sync and async clients"""

    def __init__(self, api_key: str, base_url: str = "https://api.example.com"):
        self.api_key = api_key
        self.base_url = base_url


class SyncClient(BaseClient):
    @property
    def users(self):
        from .resources_sync import UsersResource
        return UsersResource(self)

    def request(self, method: str, path: str, body=None) -> Any:
        import requests
        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            json=body,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()


class AsyncClient(BaseClient):
    @property
    def users(self):
        from .resources_async import AsyncUsersResource
        return AsyncUsersResource(self)

    async def request(self, method: str, path: str, body=None) -> Any:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=f"{self.base_url}{path}",
                json=body,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()


# Usage
def sync_example():
    client = SyncClient(api_key=os.environ['API_KEY'])
    user = client.users.create(name='Alice', email='alice@example.com')
    print(f"Created: {user}")


async def async_example():
    client = AsyncClient(api_key=os.environ['API_KEY'])
    user = await client.users.create(name='Bob', email='bob@example.com')
    print(f"Created: {user}")


if __name__ == '__main__':
    sync_example()
    asyncio.run(async_example())
