"""
Service Discovery with Consul

Demonstrates: Client-side service discovery

Dependencies:
    - pip install python-consul requests

Usage:
    # Start Consul first:
    # consul agent -dev

    python consul_discovery.py
"""

import random

class MockConsul:
    """Mock Consul client for demonstration"""

    def __init__(self):
        self.services = {
            'payment-service': [
                {'Address': 'localhost', 'Port': 8001},
                {'Address': 'localhost', 'Port': 8002}
            ],
            'inventory-service': [
                {'Address': 'localhost', 'Port': 9001},
                {'Address': 'localhost', 'Port': 9002},
                {'Address': 'localhost', 'Port': 9003}
            ]
        }

    def health_service(self, service_name, passing=True):
        """Mock health service query"""
        services = self.services.get(service_name, [])
        # Format: (index, [{'Service': {...}}])
        return (0, [{'Service': s} for s in services])


class ServiceDiscovery:
    """Client-side service discovery"""

    def __init__(self, consul_client=None):
        self.consul = consul_client or MockConsul()

    def discover(self, service_name: str):
        """Discover healthy service instances"""
        index, services = self.consul.health_service(service_name, passing=True)
        instances = [
            {'host': s['Service']['Address'], 'port': s['Service']['Port']}
            for s in services
        ]
        return instances

    def call_service(self, service_name: str, path: str = '/'):
        """Call service with load balancing"""
        instances = self.discover(service_name)

        if not instances:
            raise Exception(f"No healthy instances of {service_name}")

        # Load balance (random selection)
        instance = random.choice(instances)
        url = f"http://{instance['host']}:{instance['port']}{path}"

        print(f"  Calling {service_name} at {url}")
        return {'url': url, 'instance': instance}


if __name__ == "__main__":
    print("Service Discovery Pattern Demo\n")

    sd = ServiceDiscovery()

    # Discover payment service instances
    print("Discovering payment-service...")
    instances = sd.discover('payment-service')
    print(f"Found {len(instances)} instances:")
    for inst in instances:
        print(f"  - {inst['host']}:{inst['port']}")

    # Call payment service (load balanced)
    print("\nCalling payment-service 5 times (observe load balancing):")
    for i in range(5):
        result = sd.call_service('payment-service', '/process-payment')

    # Discover inventory service
    print("\nDiscovering inventory-service...")
    instances = sd.discover('inventory-service')
    print(f"Found {len(instances)} instances:")
    for inst in instances:
        print(f"  - {inst['host']}:{inst['port']}")

    print("\nCalling inventory-service 5 times:")
    for i in range(5):
        result = sd.call_service('inventory-service', '/check-stock')
