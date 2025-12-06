/*
Channel-Based Pagination Example (Go)

Demonstrates using channels for concurrent iteration over paginated results.
*/

package main

import (
	"context"
	"fmt"
	"os"
)

type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

type ChannelPaginationClient struct {
	apiKey string
}

func NewChannelPaginationClient(apiKey string) *ChannelPaginationClient {
	return &ChannelPaginationClient{apiKey: apiKey}
}

// ListUsers returns channels for users and errors
func (c *ChannelPaginationClient) ListUsers(ctx context.Context, limit int) (<-chan User, <-chan error) {
	userCh := make(chan User)
	errCh := make(chan error, 1)

	go func() {
		defer close(userCh)
		defer close(errCh)

		cursor := ""
		for {
			// Fetch page (simplified - would call real API)
			users := []User{
				{ID: "1", Name: "Alice", Email: "alice@example.com"},
				{ID: "2", Name: "Bob", Email: "bob@example.com"},
			}

			for _, user := range users {
				select {
				case <-ctx.Done():
					errCh <- ctx.Err()
					return
				case userCh <- user:
				}
			}

			// No more pages (simplified)
			break
		}
	}()

	return userCh, errCh
}

func main() {
	client := NewChannelPaginationClient(os.Getenv("API_KEY"))
	ctx := context.Background()

	userCh, errCh := client.ListUsers(ctx, 100)

	for user := range userCh {
		fmt.Printf("- %s (%s)\n", user.Name, user.Email)
	}

	if err := <-errCh; err != nil {
		fmt.Printf("Error: %v\n", err)
	}
}
