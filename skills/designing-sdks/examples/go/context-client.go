/*
Context-Aware Go Client Example

Demonstrates using context.Context for timeouts and cancellation.
*/

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

type ContextClient struct {
	apiKey     string
	baseURL    string
	httpClient *http.Client
}

func NewContextClient(apiKey string) *ContextClient {
	return &ContextClient{
		apiKey:  apiKey,
		baseURL: "https://api.example.com",
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

func (c *ContextClient) request(ctx context.Context, method, path string) (interface{}, error) {
	req, err := http.NewRequestWithContext(ctx, method, c.baseURL+path, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", "Bearer "+c.apiKey)

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result interface{}
	json.NewDecoder(resp.Body).Decode(&result)
	return result, nil
}

func main() {
	client := NewContextClient(os.Getenv("API_KEY"))

	// With timeout
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	result, err := client.request(ctx, "GET", "/users/123")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Printf("Result: %v\n", result)
}
