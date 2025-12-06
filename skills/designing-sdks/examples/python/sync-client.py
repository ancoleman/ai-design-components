"""
Basic Sync SDK Client Example (Python)

Demonstrates:
- Synchronous API client
- API key authentication
- Resource-based organization
- Error handling

Dependencies:
    pip install requests

Usage:
    export API_KEY="your_key"
    python sync-client.py
"""

import os
import requests
from typing import Dict, Any, Optional, List


class APIError(Exception):
    def __init__(self, message: str, status: int, code: str, request_id: str):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id


class APIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.example.com"):
        self.api_key = api_key
        self.base_url = base_url

    @property
    def users(self):
        return UsersResource(self)

    def request(
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

        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            json=body,
            params=query,
            headers=headers
        )

        request_id = response.headers.get('x-request-id', 'unknown')

        if not response.ok:
            error_data = response.json() if response.text else {}
            raise APIError(
                error_data.get('message', f"HTTP {response.status_code}"),
                response.status_code,
                error_data.get('code', 'unknown_error'),
                request_id
            )

        return response.json()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class UsersResource:
    def __init__(self, client: APIClient):
        self._client = client

    def create(self, name: str, email: str) -> Dict[str, Any]:
        return self._client.request('POST', '/users', body={'name': name, 'email': email})

    def retrieve(self, user_id: str) -> Dict[str, Any]:
        return self._client.request('GET', f'/users/{user_id}')

    def update(self, user_id: str, **kwargs) -> Dict[str, Any]:
        return self._client.request('PATCH', f'/users/{user_id}', body=kwargs)

    def delete(self, user_id: str) -> Dict[str, Any]:
        return self._client.request('DELETE', f'/users/{user_id}')

    def list(self, limit: int = 100) -> List[Dict[str, Any]]:
        response = self._client.request('GET', '/users', query={'limit': str(limit)})
        return response.get('data', [])


def main():
    # Use context manager for automatic cleanup
    with APIClient(api_key=os.environ.get('API_KEY', 'test_key')) as client:
        try:
            # Create user
            user = client.users.create(name='Alice', email='alice@example.com')
            print(f"Created user: {user}")

            # Retrieve user
            retrieved = client.users.retrieve(user['id'])
            print(f"Retrieved user: {retrieved}")

            # Update user
            updated = client.users.update(user['id'], name='Alice Smith')
            print(f"Updated user: {updated}")

            # List users
            users = client.users.list(limit=10)
            print(f"Found {len(users)} users")

            # Delete user
            client.users.delete(user['id'])
            print("Deleted user")

        except APIError as e:
            print(f"API Error: {e.message} ({e.code})")
            print(f"Request ID: {e.request_id}")


if __name__ == '__main__':
    main()
