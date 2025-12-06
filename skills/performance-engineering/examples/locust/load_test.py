"""
Basic Load Test Example (Locust)

Demonstrates: User behavior modeling with weighted tasks

Usage:
    # Web UI mode
    locust -f load_test.py

    # Headless mode
    locust -f load_test.py --headless -u 100 -r 10 --run-time 10m

Scenario:
    - Simulate e-commerce user behavior
    - View products (most common)
    - View product details
    - Add to cart (less common)
"""

from locust import HttpUser, task, between


class EcommerceUser(HttpUser):
    """
    Simulates typical e-commerce user behavior
    """
    wait_time = between(1, 3)  # Think time: 1-3 seconds between requests
    host = "https://api.example.com"

    def on_start(self):
        """
        Called once when virtual user starts
        Simulates login
        """
        self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass"
        })

    @task(5)  # Weight: 5 (most likely task)
    def view_products(self):
        """Browse products list"""
        self.client.get("/products")

    @task(3)  # Weight: 3
    def view_product_detail(self):
        """View specific product"""
        product_id = 123  # Could randomize
        self.client.get(f"/products/{product_id}")

    @task(1)  # Weight: 1 (least likely)
    def add_to_cart(self):
        """Add product to cart"""
        self.client.post("/cart", json={
            "product_id": 123,
            "quantity": 1
        })
