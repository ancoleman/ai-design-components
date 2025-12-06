"""
Dynamic Database Credentials - Python Example

Demonstrates fetching dynamic PostgreSQL credentials from Vault
with automatic lease renewal.

Dependencies:
    pip install hvac sqlalchemy psycopg2-binary

Usage:
    python python-hvac.py
"""

import hvac
import time
import threading
import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool


class VaultDatabaseClient:
    """
    Vault client for dynamic database credentials with automatic renewal.
    """

    def __init__(self, vault_url, role_name):
        self.vault_url = vault_url
        self.role_name = role_name
        self.client = None
        self.lease_id = None
        self.lease_duration = 0
        self.engine = None

        # Initialize Vault client
        self._authenticate()

        # Get initial credentials
        self._refresh_credentials()

        # Start background renewal thread
        threading.Thread(target=self._renewal_loop, daemon=True).start()

    def _authenticate(self):
        """Authenticate with Vault using Kubernetes service account"""
        self.client = hvac.Client(url=self.vault_url)

        # Read Kubernetes service account token
        token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'

        # For local development, use VAULT_TOKEN env var
        if os.path.exists(token_path):
            with open(token_path) as f:
                jwt = f.read()
            self.client.auth.kubernetes(role='app-role', jwt=jwt)
        else:
            # Fallback to token auth for local development
            vault_token = os.getenv('VAULT_TOKEN')
            if not vault_token:
                raise ValueError("VAULT_TOKEN environment variable required for local development")
            self.client.token = vault_token

    def _refresh_credentials(self):
        """Fetch new dynamic credentials from Vault"""
        try:
            response = self.client.secrets.database.generate_credentials(
                name=self.role_name
            )

            username = response['data']['username']
            password = response['data']['password']
            self.lease_id = response['lease_id']
            self.lease_duration = response['lease_duration']

            print(f"✓ Credentials generated:")
            print(f"  Username: {username}")
            print(f"  Lease ID: {self.lease_id}")
            print(f"  TTL: {self.lease_duration}s ({self.lease_duration / 3600:.1f}h)")

            # Dispose old engine if exists
            if self.engine:
                self.engine.dispose()

            # Create new database engine
            # NullPool prevents connection pooling (credentials rotate)
            self.engine = create_engine(
                f"postgresql://{username}:{password}@localhost:5432/mydb",
                poolclass=NullPool
            )

        except Exception as e:
            print(f"✗ Failed to generate credentials: {e}")
            raise

    def _renewal_loop(self):
        """Background thread to renew lease automatically"""
        while True:
            # Renew at 67% of lease duration
            renewal_time = self.lease_duration * 0.67
            print(f"⏰ Renewal scheduled in {renewal_time:.0f}s")
            time.sleep(renewal_time)

            try:
                # Attempt to renew existing lease
                response = self.client.sys.renew_lease(self.lease_id)
                self.lease_duration = response['lease_duration']
                print(f"✓ Lease renewed: {self.lease_id} (TTL: {self.lease_duration}s)")

            except Exception as e:
                print(f"✗ Renewal failed: {e}")
                print("  Requesting new credentials...")
                self._refresh_credentials()

    def query(self, sql):
        """Execute SQL query"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                return result.fetchall()
        except Exception as e:
            print(f"✗ Query failed: {e}")
            raise


def main():
    """Example usage"""
    # Configuration
    VAULT_URL = os.getenv('VAULT_ADDR', 'http://localhost:8200')
    ROLE_NAME = os.getenv('DB_ROLE', 'app-role')

    print(f"Connecting to Vault: {VAULT_URL}")
    print(f"Database role: {ROLE_NAME}")
    print()

    # Create client
    db_client = VaultDatabaseClient(VAULT_URL, ROLE_NAME)

    # Example queries
    try:
        # Create table
        db_client.query('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Table created")

        # Insert data
        db_client.query('''
            INSERT INTO users (username) VALUES ('alice')
            ON CONFLICT (username) DO NOTHING
        ''')
        print("✓ Data inserted")

        # Query data
        users = db_client.query('SELECT * FROM users')
        print(f"✓ Users: {users}")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Keep running to demonstrate renewal
    print("\nMonitoring lease renewal (press Ctrl+C to exit)...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == '__main__':
    main()
