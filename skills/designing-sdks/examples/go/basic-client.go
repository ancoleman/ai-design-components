/*
Basic SDK Client Example (Go)

Demonstrates:
- Idiomatic Go client with context.Context
- Error handling with typed errors
- Resource-based organization

Dependencies:
    None (uses standard library)

Usage:
    export API_KEY="your_key"
    go run basic-client.go
*/

package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

// APIError represents an API error
type APIError struct {
	Message   string
	Status    int
	Code      string
	RequestID string
}

func (e *APIError) Error() string {
	return fmt.Sprintf("API error %d: %s (code: %s, request_id: %s)",
		e.Status, e.Message, e.Code, e.RequestID)
}

// Client configuration
type ClientOptions struct {
	APIKey  string
	BaseURL string
	Timeout time.Duration
}

// Client represents the API client
type Client struct {
	apiKey     string
	baseURL    string
	httpClient *http.Client
}

// New creates a new API client
func New(apiKey string) *Client {
	return NewWithOptions(ClientOptions{
		APIKey:  apiKey,
		BaseURL: "https://api.example.com",
		Timeout: 30 * time.Second,
	})
}

// NewWithOptions creates a new client with custom options
func NewWithOptions(opts ClientOptions) *Client {
	if opts.BaseURL == "" {
		opts.BaseURL = "https://api.example.com"
	}
	if opts.Timeout == 0 {
		opts.Timeout = 30 * time.Second
	}

	return &Client{
		apiKey:  opts.APIKey,
		baseURL: opts.BaseURL,
		httpClient: &http.Client{
			Timeout: opts.Timeout,
		},
	}
}

// Users returns the users resource
func (c *Client) Users() *UsersResource {
	return &UsersResource{client: c}
}

// request makes an HTTP request
func (c *Client) request(
	ctx context.Context,
	method string,
	path string,
	body interface{},
) (interface{}, error) {
	url := c.baseURL + path

	var bodyReader io.Reader
	if body != nil {
		bodyBytes, err := json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("marshal body: %w", err)
		}
		bodyReader = bytes.NewReader(bodyBytes)
	}

	req, err := http.NewRequestWithContext(ctx, method, url, bodyReader)
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+c.apiKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("do request: %w", err)
	}
	defer resp.Body.Close()

	requestID := resp.Header.Get("X-Request-ID")
	if requestID == "" {
		requestID = "unknown"
	}

	if resp.StatusCode >= 400 {
		var errData struct {
			Message string `json:"message"`
			Code    string `json:"code"`
		}
		json.NewDecoder(resp.Body).Decode(&errData)

		return nil, &APIError{
			Message:   errData.Message,
			Status:    resp.StatusCode,
			Code:      errData.Code,
			RequestID: requestID,
		}
	}

	var result interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}

	return result, nil
}

// User represents a user
type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// CreateUserRequest represents a user creation request
type CreateUserRequest struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

// UsersResource handles user operations
type UsersResource struct {
	client *Client
}

// Create creates a new user
func (r *UsersResource) Create(ctx context.Context, req CreateUserRequest) (*User, error) {
	result, err := r.client.request(ctx, "POST", "/users", req)
	if err != nil {
		return nil, err
	}

	var user User
	data, _ := json.Marshal(result)
	json.Unmarshal(data, &user)
	return &user, nil
}

// Retrieve retrieves a user by ID
func (r *UsersResource) Retrieve(ctx context.Context, id string) (*User, error) {
	result, err := r.client.request(ctx, "GET", "/users/"+id, nil)
	if err != nil {
		return nil, err
	}

	var user User
	data, _ := json.Marshal(result)
	json.Unmarshal(data, &user)
	return &user, nil
}

// Update updates a user
func (r *UsersResource) Update(ctx context.Context, id string, updates map[string]interface{}) (*User, error) {
	result, err := r.client.request(ctx, "PATCH", "/users/"+id, updates)
	if err != nil {
		return nil, err
	}

	var user User
	data, _ := json.Marshal(result)
	json.Unmarshal(data, &user)
	return &user, nil
}

// Delete deletes a user
func (r *UsersResource) Delete(ctx context.Context, id string) error {
	_, err := r.client.request(ctx, "DELETE", "/users/"+id, nil)
	return err
}

func main() {
	apiKey := os.Getenv("API_KEY")
	if apiKey == "" {
		apiKey = "test_key"
	}

	client := New(apiKey)
	ctx := context.Background()

	// Create user
	user, err := client.Users().Create(ctx, CreateUserRequest{
		Name:  "Alice",
		Email: "alice@example.com",
	})
	if err != nil {
		if apiErr, ok := err.(*APIError); ok {
			fmt.Printf("API Error: %s (%s)\n", apiErr.Message, apiErr.Code)
			fmt.Printf("Request ID: %s\n", apiErr.RequestID)
		} else {
			fmt.Printf("Error: %v\n", err)
		}
		return
	}
	fmt.Printf("Created user: %s (%s)\n", user.Name, user.Email)

	// Retrieve user
	retrieved, err := client.Users().Retrieve(ctx, user.ID)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Retrieved user: %s\n", retrieved.Name)

	// Update user
	updated, err := client.Users().Update(ctx, user.ID, map[string]interface{}{
		"name": "Alice Smith",
	})
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Updated user: %s\n", updated.Name)

	// Delete user
	err = client.Users().Delete(ctx, user.ID)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Println("Deleted user")
}
