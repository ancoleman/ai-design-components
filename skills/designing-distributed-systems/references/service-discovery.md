# Service Discovery

## Table of Contents

1. [Client-Side Discovery](#client-side-discovery)
2. [Server-Side Discovery](#server-side-discovery)
3. [Service Mesh](#service-mesh)

## Client-Side Discovery

### Architecture

```
Service Registry (Consul, etcd, Eureka)
  ↑
  | (register)
  |
Services (register on startup)
  ↑
  | (query & call)
  |
Client (queries registry, selects instance, calls directly)
```

### Implementation (Consul)

```python
import consul
import random
import requests

class ServiceDiscovery:
    def __init__(self, consul_host='localhost', consul_port=8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)
    
    def register(self, service_name, service_id, host, port, health_check_url):
        self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=host,
            port=port,
            check=consul.Check.http(health_check_url, interval='10s')
        )
    
    def discover(self, service_name):
        index, services = self.consul.health.service(service_name, passing=True)
        return [{'host': s['Service']['Address'], 'port': s['Service']['Port']} 
                for s in services]
    
    def call_service(self, service_name, path):
        instances = self.discover(service_name)
        if not instances:
            raise Exception(f"No instances of {service_name}")
        
        # Load balance (random)
        instance = random.choice(instances)
        url = f"http://{instance['host']}:{instance['port']}{path}"
        return requests.get(url)

# Usage
sd = ServiceDiscovery()
sd.register('payment-service', 'payment-1', 'localhost', 8080, 'http://localhost:8080/health')
response = sd.call_service('payment-service', '/process-payment')
```

## Server-Side Discovery

### Architecture

```
Client → Load Balancer → Service Registry → Services
```

The load balancer queries the service registry and routes requests.

### Benefits: Simple clients
### Trade-off: Load balancer as single point of failure

## Service Mesh

### Concept

Sidecar proxies handle service discovery, routing, retries, circuit breaking.

### Examples

- Istio: Full-featured service mesh
- Linkerd: Lightweight service mesh
- Consul Connect: Service mesh from Consul

### Architecture

```
Service A Container + Envoy Sidecar
  ↓ (routes through)
Service B Container + Envoy Sidecar
```

### Benefits

- Decouples communication logic
- Centralized traffic management
- mTLS encryption
- Observability (tracing, metrics)

### Trade-offs

- Operational complexity
- Latency overhead (proxy hop)
- Resource usage (sidecar per service)
