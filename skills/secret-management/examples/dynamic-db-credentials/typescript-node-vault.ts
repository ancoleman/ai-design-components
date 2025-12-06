/**
 * Dynamic Database Credentials - TypeScript Example
 *
 * Demonstrates fetching dynamic PostgreSQL credentials from Vault
 * with automatic lease renewal using node-vault.
 *
 * Dependencies:
 *   npm install node-vault pg
 *
 * Usage:
 *   npx ts-node typescript-node-vault.ts
 */

import vault from 'node-vault';
import { Pool, PoolClient } from 'pg';
import { readFileSync } from 'fs';

interface VaultCredentials {
  username: string;
  password: string;
  leaseId: string;
  leaseDuration: number;
}

class VaultDatabaseClient {
  private vaultClient: any;
  private pool: Pool | null = null;
  private leaseId: string | null = null;
  private leaseDuration: number = 0;

  constructor(
    private vaultUrl: string,
    private roleName: string
  ) {
    this.vaultClient = vault({
      apiVersion: 'v1',
      endpoint: vaultUrl,
    });

    this.authenticate().then(() => {
      this.refreshCredentials().then(() => {
        this.startRenewalLoop();
      });
    });
  }

  /**
   * Authenticate with Vault using Kubernetes service account
   */
  private async authenticate(): Promise<void> {
    try {
      // Read Kubernetes service account token
      const tokenPath = '/var/run/secrets/kubernetes.io/serviceaccount/token';
      let jwt: string;

      if (require('fs').existsSync(tokenPath)) {
        jwt = readFileSync(tokenPath, 'utf8');
      } else {
        // Fallback to VAULT_TOKEN for local development
        const vaultToken = process.env.VAULT_TOKEN;
        if (!vaultToken) {
          throw new Error('VAULT_TOKEN environment variable required for local development');
        }
        this.vaultClient.token = vaultToken;
        return;
      }

      // Kubernetes auth
      const result = await this.vaultClient.kubernetesLogin({
        role: 'app-role',
        jwt: jwt,
      });

      this.vaultClient.token = result.auth.client_token;
      console.log('✓ Authenticated with Vault');
    } catch (error) {
      console.error('✗ Authentication failed:', error);
      throw error;
    }
  }

  /**
   * Fetch new dynamic credentials from Vault
   */
  private async refreshCredentials(): Promise<void> {
    try {
      const response = await this.vaultClient.read(`database/creds/${this.roleName}`);

      const username = response.data.username;
      const password = response.data.password;
      this.leaseId = response.lease_id;
      this.leaseDuration = response.lease_duration;

      console.log('✓ Credentials generated:');
      console.log(`  Username: ${username}`);
      console.log(`  Lease ID: ${this.leaseId}`);
      console.log(`  TTL: ${this.leaseDuration}s (${(this.leaseDuration / 3600).toFixed(1)}h)`);

      // Close old pool if exists
      if (this.pool) {
        await this.pool.end();
      }

      // Create new connection pool
      this.pool = new Pool({
        user: username,
        password: password,
        host: process.env.DB_HOST || 'localhost',
        database: process.env.DB_NAME || 'mydb',
        port: parseInt(process.env.DB_PORT || '5432'),
        ssl: process.env.DB_SSL === 'true',
      });

    } catch (error) {
      console.error('✗ Failed to generate credentials:', error);
      throw error;
    }
  }

  /**
   * Background renewal loop
   */
  private startRenewalLoop(): void {
    setInterval(async () => {
      // Renew at 67% of lease duration
      const renewalTime = this.leaseDuration * 0.67;

      console.log(`⏰ Renewal scheduled in ${renewalTime.toFixed(0)}s`);

      setTimeout(async () => {
        try {
          // Attempt to renew existing lease
          const response = await this.vaultClient.renew({
            lease_id: this.leaseId!,
          });

          this.leaseDuration = response.lease_duration;
          console.log(`✓ Lease renewed: ${this.leaseId} (TTL: ${this.leaseDuration}s)`);

        } catch (error) {
          console.error('✗ Renewal failed:', error);
          console.log('  Requesting new credentials...');
          await this.refreshCredentials();
        }
      }, renewalTime * 1000);

    }, this.leaseDuration * 1000);
  }

  /**
   * Execute SQL query
   */
  async query(sql: string, params?: any[]): Promise<any[]> {
    if (!this.pool) {
      throw new Error('Database pool not initialized');
    }

    try {
      const result = await this.pool.query(sql, params);
      return result.rows;
    } catch (error) {
      console.error('✗ Query failed:', error);
      throw error;
    }
  }

  /**
   * Close database connection
   */
  async close(): Promise<void> {
    if (this.pool) {
      await this.pool.end();
    }
  }
}

/**
 * Example usage
 */
async function main() {
  const VAULT_URL = process.env.VAULT_ADDR || 'http://localhost:8200';
  const ROLE_NAME = process.env.DB_ROLE || 'app-role';

  console.log(`Connecting to Vault: ${VAULT_URL}`);
  console.log(`Database role: ${ROLE_NAME}`);
  console.log('');

  // Create client
  const dbClient = new VaultDatabaseClient(VAULT_URL, ROLE_NAME);

  // Wait for initialization
  await new Promise(resolve => setTimeout(resolve, 2000));

  try {
    // Create table
    await dbClient.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✓ Table created');

    // Insert data
    await dbClient.query(
      `INSERT INTO users (username) VALUES ($1) ON CONFLICT (username) DO NOTHING`,
      ['alice']
    );
    console.log('✓ Data inserted');

    // Query data
    const users = await dbClient.query('SELECT * FROM users');
    console.log('✓ Users:', users);

  } catch (error) {
    console.error('✗ Error:', error);
  }

  // Keep running to demonstrate renewal
  console.log('\nMonitoring lease renewal (press Ctrl+C to exit)...');
}

main().catch(console.error);
