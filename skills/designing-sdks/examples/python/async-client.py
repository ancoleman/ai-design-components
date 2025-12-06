"""
Async SDK Client Example (Python)

Demonstrates:
- Asynchronous API client with asyncio
- Async pagination with async generators
- Context manager support
- Error handling

Dependencies:
    pip install httpx

Usage:
    export API_KEY="your_key"
    python async-client.py
"""

import os
import asyncio
from typing import Dict, Any, Optional, AsyncIterator
import httpx


class APIError(Exception):
    def __init__(self, message: str, status: int, code: str, request_id: str):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id


class AsyncAPIClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.example.com",
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.AsyncClient(timeout=timeout)

    @property
    def users(self):
        return AsyncUsersResource(self)

    async def request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, str]] = None
    ) -> Any:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = await self._client.request(
            method=method,
            url=f"{self.base_url}{path}",
            json=body,
            params=query,
            headers=headers
        )

        request_id = response.headers.get('x-request-id', 'unknown')

        if not response.is_success:
            error_data = response.json() if response.text else {}
            raise APIError(
                error_data.get('message', f"HTTP {response.status_code}"),
                response.status_code,
                error_data.get('code', 'unknown_error'),
                request_id
            )

        return response.json()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def close(self):
        await self._client.aclose()


class AsyncUsersResource:
    def __init__(self, client: AsyncAPIClient):
        self._client = client

    async def create(self, name: str, email: str) -> Dict[str, Any]:
        return await self._client.request('POST', '/users', body={'name': name, 'email': email})

    async def retrieve(self, user_id: str) -> Dict[str, Any]:
        return await self._client.request('GET', f'/users/{user_id}')

    async def update(self, user_id: str, **kwargs) -> Dict[str, Any]:
        return await self._client.request('PATCH', f'/users/{user_id}', body=kwargs)

    async def delete(self, user_id: str) -> Dict[str, Any]:
        return await self._client.request('DELETE', f'/users/{user_id}')

    async def list(self, limit: int = 100) -> AsyncIterator[Dict[str, Any]]:
        """Async generator for automatic pagination"""
        cursor = None

        while True:
            query = {'limit': str(limit)}
            if cursor:
                query['cursor'] = cursor

            response = await self._client.request('GET', '/users', query=query)

            for user in response.get('data', []):
                yield user

            if not response.get('has_more'):
                break
            cursor = response.get('next_cursor')


async def main():
    async with AsyncAPIClient(api_key=os.environ.get('API_KEY', 'test_key')) as client:
        try:
            # Create user
            user = await client.users.create(name='Bob', email='bob@example.com')
            print(f"Created user: {user}")

            # Retrieve user
            retrieved = await client.users.retrieve(user['id'])
            print(f"Retrieved user: {retrieved}")

            # Pagination with async for
            print("All users:")
            async for user in client.users.list(limit=10):
                print(f"- {user['name']} ({user['email']})")

            # Delete user
            await client.users.delete(user['id'])
            print("Deleted user")

        except APIError as e:
            print(f"API Error: {e.message} ({e.code})")
            print(f"Request ID: {e.request_id}")


if __name__ == '__main__':
    asyncio.run(main())
