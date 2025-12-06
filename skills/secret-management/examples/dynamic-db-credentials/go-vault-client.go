// Dynamic Database Credentials - Go Example
//
// Demonstrates fetching dynamic PostgreSQL credentials from Vault
// with automatic lease renewal.
//
// Dependencies:
//   go get github.com/hashicorp/vault/api
//   go get github.com/hashicorp/vault/api/auth/kubernetes
//   go get github.com/lib/pq
//
// Usage:
//   go run go-vault-client.go

package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	vault "github.com/hashicorp/vault/api"
	auth "github.com/hashicorp/vault/api/auth/kubernetes"
	_ "github.com/lib/pq"
)

type VaultDatabaseClient struct {
	vaultClient   *vault.Client
	db            *sql.DB
	leaseID       string
	leaseDuration int
	roleName      string
}

// NewVaultDatabaseClient creates a new client with Vault integration
func NewVaultDatabaseClient(vaultAddr, roleName string) (*VaultDatabaseClient, error) {
	client := &VaultDatabaseClient{
		roleName: roleName,
	}

	// Create Vault client
	config := vault.DefaultConfig()
	config.Address = vaultAddr

	var err error
	client.vaultClient, err = vault.NewClient(config)
	if err != nil {
		return nil, fmt.Errorf("failed to create Vault client: %w", err)
	}

	// Authenticate
	if err := client.authenticate(); err != nil {
		return nil, fmt.Errorf("failed to authenticate: %w", err)
	}

	// Get initial credentials
	if err := client.refreshCredentials(); err != nil {
		return nil, fmt.Errorf("failed to get credentials: %w", err)
	}

	// Start renewal loop
	go client.renewalLoop()

	return client, nil
}

// authenticate with Vault using Kubernetes service account
func (c *VaultDatabaseClient) authenticate() error {
	// Try Kubernetes auth first
	tokenPath := "/var/run/secrets/kubernetes.io/serviceaccount/token"
	if _, err := os.Stat(tokenPath); err == nil {
		k8sAuth, err := auth.NewKubernetesAuth(
			"app-role",
			auth.WithServiceAccountTokenPath(tokenPath),
		)
		if err != nil {
			return fmt.Errorf("failed to create Kubernetes auth: %w", err)
		}

		authInfo, err := c.vaultClient.Auth().Login(context.Background(), k8sAuth)
		if err != nil {
			return fmt.Errorf("Kubernetes login failed: %w", err)
		}

		log.Printf("✓ Authenticated with Vault (token: %s...)", authInfo.Auth.ClientToken[:8])
		return nil
	}

	// Fallback to token auth for local development
	vaultToken := os.Getenv("VAULT_TOKEN")
	if vaultToken == "" {
		return fmt.Errorf("VAULT_TOKEN environment variable required for local development")
	}

	c.vaultClient.SetToken(vaultToken)
	log.Println("✓ Authenticated with Vault (token auth)")
	return nil
}

// refreshCredentials fetches new dynamic credentials from Vault
func (c *VaultDatabaseClient) refreshCredentials() error {
	// Generate dynamic credentials
	secret, err := c.vaultClient.Logical().Read(fmt.Sprintf("database/creds/%s", c.roleName))
	if err != nil {
		return fmt.Errorf("failed to read database credentials: %w", err)
	}

	username := secret.Data["username"].(string)
	password := secret.Data["password"].(string)
	c.leaseID = secret.LeaseID
	c.leaseDuration = secret.LeaseDuration

	log.Printf("✓ Credentials generated:")
	log.Printf("  Username: %s", username)
	log.Printf("  Lease ID: %s", c.leaseID)
	log.Printf("  TTL: %ds (%.1fh)", c.leaseDuration, float64(c.leaseDuration)/3600)

	// Close old connection if exists
	if c.db != nil {
		c.db.Close()
	}

	// Create new database connection
	dbHost := getEnv("DB_HOST", "localhost")
	dbPort := getEnv("DB_PORT", "5432")
	dbName := getEnv("DB_NAME", "mydb")
	sslMode := getEnv("DB_SSL_MODE", "disable")

	connStr := fmt.Sprintf(
		"postgres://%s:%s@%s:%s/%s?sslmode=%s",
		username, password, dbHost, dbPort, dbName, sslMode,
	)

	c.db, err = sql.Open("postgres", connStr)
	if err != nil {
		return fmt.Errorf("failed to open database connection: %w", err)
	}

	// Verify connection
	if err := c.db.Ping(); err != nil {
		return fmt.Errorf("failed to ping database: %w", err)
	}

	return nil
}

// renewalLoop automatically renews lease
func (c *VaultDatabaseClient) renewalLoop() {
	for {
		// Renew at 67% of lease duration
		renewalTime := time.Duration(float64(c.leaseDuration)*0.67) * time.Second
		log.Printf("⏰ Renewal scheduled in %s", renewalTime)
		time.Sleep(renewalTime)

		// Attempt renewal
		secret, err := c.vaultClient.Sys().Renew(c.leaseID, 0)
		if err != nil {
			log.Printf("✗ Renewal failed: %v", err)
			log.Println("  Requesting new credentials...")

			if err := c.refreshCredentials(); err != nil {
				log.Printf("✗ Failed to refresh credentials: %v", err)
			}
		} else {
			c.leaseDuration = secret.LeaseDuration
			log.Printf("✓ Lease renewed: %s (TTL: %ds)", c.leaseID, c.leaseDuration)
		}
	}
}

// Query executes a SQL query
func (c *VaultDatabaseClient) Query(query string, args ...interface{}) (*sql.Rows, error) {
	if c.db == nil {
		return nil, fmt.Errorf("database connection not initialized")
	}

	return c.db.Query(query, args...)
}

// Exec executes a SQL statement
func (c *VaultDatabaseClient) Exec(query string, args ...interface{}) (sql.Result, error) {
	if c.db == nil {
		return nil, fmt.Errorf("database connection not initialized")
	}

	return c.db.Exec(query, args...)
}

// Close closes the database connection
func (c *VaultDatabaseClient) Close() error {
	if c.db != nil {
		return c.db.Close()
	}
	return nil
}

// getEnv gets environment variable with default value
func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}

func main() {
	vaultAddr := getEnv("VAULT_ADDR", "http://localhost:8200")
	roleName := getEnv("DB_ROLE", "app-role")

	log.Printf("Connecting to Vault: %s", vaultAddr)
	log.Printf("Database role: %s", roleName)
	log.Println()

	// Create client
	client, err := NewVaultDatabaseClient(vaultAddr, roleName)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer client.Close()

	// Example queries
	log.Println("Running example queries...")

	// Create table
	_, err = client.Exec(`
		CREATE TABLE IF NOT EXISTS users (
			id SERIAL PRIMARY KEY,
			username VARCHAR(50) UNIQUE NOT NULL,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`)
	if err != nil {
		log.Fatalf("Failed to create table: %v", err)
	}
	log.Println("✓ Table created")

	// Insert data
	_, err = client.Exec(
		`INSERT INTO users (username) VALUES ($1) ON CONFLICT (username) DO NOTHING`,
		"alice",
	)
	if err != nil {
		log.Fatalf("Failed to insert data: %v", err)
	}
	log.Println("✓ Data inserted")

	// Query data
	rows, err := client.Query("SELECT id, username, created_at FROM users")
	if err != nil {
		log.Fatalf("Failed to query data: %v", err)
	}
	defer rows.Close()

	log.Println("✓ Users:")
	for rows.Next() {
		var id int
		var username string
		var createdAt time.Time
		if err := rows.Scan(&id, &username, &createdAt); err != nil {
			log.Printf("  Error scanning row: %v", err)
			continue
		}
		log.Printf("  - %d: %s (created: %s)", id, username, createdAt.Format("2006-01-02 15:04:05"))
	}

	// Keep running to demonstrate renewal
	log.Println("\nMonitoring lease renewal (press Ctrl+C to exit)...")
	select {}
}
