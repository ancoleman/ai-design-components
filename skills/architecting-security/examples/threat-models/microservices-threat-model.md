# Microservices Threat Model

## Overview

Comprehensive threat model for microservices architecture using STRIDE methodology. Analyze threats across service-to-service communication, container security, secrets management, network segmentation, and supply chain risks.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MICROSERVICES ARCHITECTURE                       │
│                                                                           │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │  API Gateway │────▶│   Service A  │────▶│   Service B  │            │
│  │              │     │  (Auth)      │     │  (Business)  │            │
│  │ - Auth       │     │              │     │              │            │
│  │ - Routing    │     │ - User Mgmt  │     │ - Orders     │            │
│  │ - Rate Limit │     │ - Sessions   │     │ - Inventory  │            │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘            │
│         │                    │                    │                     │
│         │                    └────────────────────┼─────────────┐       │
│         │                                         │             │       │
│         ▼                                         ▼             ▼       │
│  ┌──────────────┐                         ┌──────────────┬──────────┐  │
│  │ Service Mesh │                         │   Service C  │Database  │  │
│  │ (Istio)      │                         │  (Payment)   │(Postgres)│  │
│  │              │                         │              │          │  │
│  │ - mTLS       │                         │ - Stripe API │          │  │
│  │ - AuthZ      │                         │ - PCI DSS    │          │  │
│  │ - Observ.    │                         └──────────────┴──────────┘  │
│  └──────────────┘                                                       │
│                                                                           │
│  Supporting Services:                                                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐          │
│  │ Message    │ │ Config     │ │ Secrets    │ │ Monitoring │          │
│  │ Queue      │ │ Server     │ │ Manager    │ │ (Prom/Gr)  │          │
│  │ (RabbitMQ) │ │ (Consul)   │ │ (Vault)    │ │            │          │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
```

## STRIDE Analysis

### Spoofing (Identity)

**Threat 1.1: Service Impersonation**

- **Description:** Malicious service impersonates legitimate service to intercept requests
- **Attack Vector:** Compromised container, DNS poisoning, service registry manipulation
- **Impact:** CRITICAL - Data exfiltration, unauthorized access, man-in-the-middle
- **Likelihood:** MEDIUM - Requires container or infrastructure compromise

**Mitigations:**

```yaml
- control: Mutual TLS (mTLS) authentication
  effectiveness: CRITICAL
  implementation:
    service_mesh: Istio
    configuration:
      mode: STRICT
      mtls:
        enabled: true
      certificate_rotation: 24h
      trusted_ca: cluster-ca
    code_example: |
      apiVersion: security.istio.io/v1beta1
      kind: PeerAuthentication
      metadata:
        name: default
        namespace: production
      spec:
        mtls:
          mode: STRICT

- control: Service identity certificates
  effectiveness: HIGH
  implementation:
    - Use SPIFFE/SPIRE for service identity
    - Short-lived certificates (24 hour TTL)
    - Automatic certificate rotation
    - Bind certificates to pod identity
    code_example: |
      # SPIRE registration entry
      spire-server entry create \
        -spiffeID spiffe://example.com/service-a \
        -parentID spiffe://example.com/k8s-node \
        -selector k8s:ns:production \
        -selector k8s:sa:service-a

- control: Service registry authentication
  effectiveness: HIGH
  implementation:
    - Authenticate to service registry (Consul, Eureka)
    - ACL tokens for service registration
    - Verify service identity before registration
    - Monitor for unauthorized registrations

- control: Network policies
  effectiveness: MEDIUM
  implementation:
    - Kubernetes NetworkPolicy for pod-to-pod
    - Deny all ingress by default
    - Explicit allow rules for service dependencies
    code_example: |
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      metadata:
        name: service-b-policy
      spec:
        podSelector:
          matchLabels:
            app: service-b
        policyTypes:
          - Ingress
        ingress:
          - from:
              - podSelector:
                  matchLabels:
                    app: service-a
            ports:
              - protocol: TCP
                port: 8080
```

**Threat 1.2: Container Image Tampering**

- **Description:** Attacker replaces legitimate container image with malicious version
- **Attack Vector:** Compromised registry, supply chain attack, insider threat
- **Impact:** CRITICAL - Malicious code execution, data theft, backdoor installation
- **Likelihood:** MEDIUM - Requires registry access or CI/CD compromise

**Mitigations:**

```yaml
- control: Image signing and verification
  effectiveness: CRITICAL
  implementation:
    tool: Sigstore/Cosign
    process:
      - Sign all images during CI/CD
      - Verify signatures before deployment
      - Reject unsigned images
    code_example: |
      # Sign image
      cosign sign --key cosign.key \
        gcr.io/project/service-a:v1.2.3

      # Verify on deployment
      cosign verify --key cosign.pub \
        gcr.io/project/service-a:v1.2.3

- control: Image vulnerability scanning
  effectiveness: HIGH
  implementation:
    tool: Trivy, Clair, Anchore
    process:
      - Scan images in CI/CD pipeline
      - Block deployment of critical vulnerabilities
      - Daily rescans of running images
    code_example: |
      trivy image --severity HIGH,CRITICAL \
        --exit-code 1 \
        gcr.io/project/service-a:v1.2.3

- control: Admission control
  effectiveness: CRITICAL
  implementation:
    tool: OPA Gatekeeper, Kyverno
    policies:
      - Require signed images
      - Require images from approved registries
      - Reject images with critical vulnerabilities
    code_example: |
      apiVersion: constraints.gatekeeper.sh/v1beta1
      kind: K8sAllowedRepos
      metadata:
        name: prod-repo-restriction
      spec:
        match:
          kinds:
            - apiGroups: [""]
              kinds: ["Pod"]
          namespaces: ["production"]
        parameters:
          repos:
            - "gcr.io/approved-project/"

- control: Private container registry
  effectiveness: HIGH
  implementation:
    - Use private registry (GCR, ECR, ACR)
    - Require authentication to pull images
    - Enable vulnerability scanning
    - Audit image access logs
```

**Threat 1.3: API Token Theft**

- **Description:** Service-to-service API tokens stolen from environment variables or logs
- **Attack Vector:** Container escape, log aggregation access, compromised secrets
- **Impact:** HIGH - Unauthorized service access, lateral movement
- **Likelihood:** HIGH - Common misconfiguration

**Mitigations:**

```yaml
- control: Short-lived tokens
  effectiveness: HIGH
  implementation:
    - Token TTL: 15 minutes maximum
    - Automatic token rotation
    - Service mesh handles token refresh
    code_example: |
      # Istio JWT configuration
      apiVersion: security.istio.io/v1beta1
      kind: RequestAuthentication
      metadata:
        name: jwt-auth
      spec:
        jwtRules:
          - issuer: "https://auth.example.com"
            jwksUri: "https://auth.example.com/.well-known/jwks.json"
            audiences:
              - "service-b"
            forwardOriginalToken: false

- control: Secrets management system
  effectiveness: CRITICAL
  implementation:
    tool: HashiCorp Vault, AWS Secrets Manager
    process:
      - Store tokens in secrets manager
      - Inject at runtime only
      - Never log tokens
      - Rotate on suspected compromise
    code_example: |
      # Vault Kubernetes auth
      vault write auth/kubernetes/role/service-a \
        bound_service_account_names=service-a \
        bound_service_account_namespaces=production \
        policies=service-a-policy \
        ttl=1h

- control: Workload identity
  effectiveness: HIGH
  implementation:
    - Use cloud provider workload identity
    - Bind pod to cloud IAM role
    - No static credentials needed
    code_example: |
      # GKE Workload Identity
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        annotations:
          iam.gke.io/gcp-service-account: service-a@project.iam.gserviceaccount.com

- control: Token scope limitation
  effectiveness: MEDIUM
  implementation:
    - Limit token to specific service endpoints
    - Implement audience validation
    - Shortest privilege duration
```

### Tampering (Data Integrity)

**Threat 2.1: Message Queue Tampering**

- **Description:** Attacker modifies messages in transit between services via message queue
- **Attack Vector:** Compromised queue credentials, queue admin access
- **Impact:** HIGH - Data corruption, fraudulent transactions, system instability
- **Likelihood:** MEDIUM - Requires queue access

**Mitigations:**

```yaml
- control: Message signing
  effectiveness: HIGH
  implementation:
    - Sign messages with HMAC or digital signature
    - Include timestamp to prevent replay
    - Verify signature before processing
    code_example: |
      import hmac
      import hashlib
      import json
      from datetime import datetime

      def sign_message(message, secret_key):
          payload = {
              "data": message,
              "timestamp": datetime.utcnow().isoformat()
          }
          payload_json = json.dumps(payload, sort_keys=True)
          signature = hmac.new(
              secret_key.encode(),
              payload_json.encode(),
              hashlib.sha256
          ).hexdigest()
          return {
              "payload": payload,
              "signature": signature
          }

      def verify_message(signed_message, secret_key):
          payload_json = json.dumps(
              signed_message["payload"],
              sort_keys=True
          )
          expected_sig = hmac.new(
              secret_key.encode(),
              payload_json.encode(),
              hashlib.sha256
          ).hexdigest()

          if not hmac.compare_digest(
              expected_sig,
              signed_message["signature"]
          ):
              raise ValueError("Invalid signature")

          return signed_message["payload"]["data"]

- control: TLS for message queue connections
  effectiveness: HIGH
  implementation:
    - Enable TLS for RabbitMQ, Kafka, SQS
    - Mutual TLS for producer/consumer authentication
    - Certificate validation
    code_example: |
      # RabbitMQ TLS config
      ssl_options = {
          "certfile": "/certs/client-cert.pem",
          "keyfile": "/certs/client-key.pem",
          "ca_certs": "/certs/ca-cert.pem",
          "cert_reqs": ssl.CERT_REQUIRED
      }
      connection = pika.BlockingConnection(
          pika.ConnectionParameters(
              host='rabbitmq.example.com',
              port=5671,
              credentials=credentials,
              ssl_options=ssl_options
          )
      )

- control: Queue access controls
  effectiveness: HIGH
  implementation:
    - Separate credentials per service
    - Read-only vs. write-only permissions
    - Queue-level ACLs
    - Audit queue access

- control: Message validation
  effectiveness: MEDIUM
  implementation:
    - Schema validation (JSON Schema, Protobuf)
    - Reject malformed messages
    - Size limits on messages
    - Content type verification
```

**Threat 2.2: Database Injection via Service Chain**

- **Description:** Malicious input propagates through service chain to database query
- **Attack Vector:** Unsanitized input passed between services, SQL/NoSQL injection
- **Impact:** CRITICAL - Data breach, data corruption, privilege escalation
- **Likelihood:** MEDIUM - Requires multiple validation failures

**Mitigations:**

```yaml
- control: Input validation at every service boundary
  effectiveness: CRITICAL
  implementation:
    - Validate at API gateway
    - Re-validate at each service
    - Never trust upstream service input
    code_example: |
      from pydantic import BaseModel, validator, constr

      class OrderRequest(BaseModel):
          order_id: constr(regex=r'^[A-Z0-9]{8}$')
          quantity: int

          @validator('quantity')
          def validate_quantity(cls, v):
              if v < 1 or v > 1000:
                  raise ValueError('Quantity must be 1-1000')
              return v

      def process_order(request_data):
          # Validate even from trusted service
          validated = OrderRequest(**request_data)
          # Use parameterized query
          query = """
              INSERT INTO orders (id, quantity)
              VALUES (?, ?)
          """
          db.execute(query, [validated.order_id, validated.quantity])

- control: Parameterized queries
  effectiveness: CRITICAL
  implementation:
    - Use prepared statements always
    - ORM with parameter binding
    - Never concatenate user input

- control: Least privilege database access
  effectiveness: HIGH
  implementation:
    - Each service has separate DB user
    - Grant minimum required permissions
    - Read-only accounts where possible
    - No shared credentials

- control: Database firewall
  effectiveness: MEDIUM
  implementation:
    - Monitor and block suspicious queries
    - Pattern-based SQL injection detection
    - Alert on anomalous database access
```

**Threat 2.3: Configuration Tampering**

- **Description:** Attacker modifies service configuration to alter behavior
- **Attack Vector:** Compromised config server, insecure config files, environment variable injection
- **Impact:** HIGH - Service malfunction, security bypass, data exfiltration
- **Likelihood:** MEDIUM - Requires config system access

**Mitigations:**

```yaml
- control: Configuration encryption
  effectiveness: HIGH
  implementation:
    - Encrypt sensitive config at rest
    - Decrypt only at runtime
    - Use sealed secrets for Kubernetes
    code_example: |
      # Sealed Secrets
      kubeseal --format yaml < secret.yaml > sealed-secret.yaml
      kubectl apply -f sealed-secret.yaml

- control: Configuration version control
  effectiveness: HIGH
  implementation:
    - Store config in Git
    - Require code review for changes
    - Audit trail of config modifications
    - Rollback capability

- control: Immutable infrastructure
  effectiveness: HIGH
  implementation:
    - Bake config into container image
    - No runtime config changes
    - Redeploy to change config
    - ConfigMaps as read-only volumes

- control: Configuration validation
  effectiveness: MEDIUM
  implementation:
    - Schema validation on startup
    - Reject invalid configuration
    - Fail-safe defaults
    code_example: |
      import schema

      config_schema = schema.Schema({
          'database_url': schema.And(str, len),
          'api_timeout': schema.And(int, lambda n: 1 <= n <= 300),
          'log_level': schema.Or('DEBUG', 'INFO', 'WARNING', 'ERROR')
      })

      config = load_config()
      validated_config = config_schema.validate(config)
```

### Repudiation (Accountability)

**Threat 3.1: Distributed Tracing Blind Spots**

- **Description:** Lack of correlation between service calls prevents audit trail
- **Attack Vector:** Missing trace IDs, incomplete logging, log deletion
- **Impact:** MEDIUM - Cannot investigate incidents, compliance violations
- **Likelihood:** HIGH - Common in complex microservices

**Mitigations:**

```yaml
- control: Distributed tracing
  effectiveness: HIGH
  implementation:
    tool: OpenTelemetry, Jaeger, Zipkin
    process:
      - Propagate trace ID across all services
      - Include trace ID in all logs
      - Sample critical paths at 100%
    code_example: |
      from opentelemetry import trace
      from opentelemetry.instrumentation.flask import FlaskInstrumentor

      tracer = trace.get_tracer(__name__)

      @app.route('/api/order')
      def create_order():
          with tracer.start_as_current_span("create_order") as span:
              span.set_attribute("order.id", order_id)
              span.set_attribute("user.id", user_id)

              # Call downstream service
              response = requests.post(
                  "http://service-b/process",
                  json=order_data,
                  headers={
                      "traceparent": span.get_span_context()
                  }
              )

- control: Structured logging
  effectiveness: HIGH
  implementation:
    - JSON formatted logs
    - Include trace ID, span ID, service name
    - Centralized log aggregation
    code_example: |
      import structlog

      log = structlog.get_logger()

      log.info(
          "order.created",
          order_id=order_id,
          user_id=user_id,
          amount=total,
          trace_id=trace_id,
          span_id=span_id
      )

- control: Service mesh observability
  effectiveness: HIGH
  implementation:
    - Automatic request tracking
    - Service dependency graph
    - Request flow visualization
    - Anomaly detection

- control: Immutable audit logs
  effectiveness: CRITICAL
  implementation:
    - Stream logs to external SIEM
    - Append-only log storage
    - Log integrity verification
    - Long-term retention (7 years for compliance)
```

**Threat 3.2: Service-to-Service Call Denial**

- **Description:** Service denies making unauthorized API call to another service
- **Attack Vector:** Compromised service credentials, lack of audit trail
- **Impact:** MEDIUM - Cannot prove malicious activity, insider threat investigation difficulty
- **Likelihood:** LOW - Requires sophisticated attack

**Mitigations:**

```yaml
- control: Service call authentication logs
  effectiveness: HIGH
  implementation:
    - Log all outbound service calls
    - Include service identity, timestamp, endpoint
    - Record request/response correlation
    code_example: |
      def call_downstream_service(endpoint, data):
          request_id = str(uuid.uuid4())

          log.info(
              "service.call.start",
              request_id=request_id,
              source_service="service-a",
              target_service="service-b",
              endpoint=endpoint,
              method="POST"
          )

          try:
              response = requests.post(
                  endpoint,
                  json=data,
                  headers={
                      "X-Request-ID": request_id,
                      "X-Source-Service": "service-a"
                  }
              )

              log.info(
                  "service.call.complete",
                  request_id=request_id,
                  status_code=response.status_code,
                  response_time_ms=response.elapsed.total_seconds() * 1000
              )

              return response
          except Exception as e:
              log.error(
                  "service.call.failed",
                  request_id=request_id,
                  error=str(e)
              )
              raise

- control: mTLS audit trail
  effectiveness: HIGH
  implementation:
    - Service mesh logs all mTLS handshakes
    - Record client certificate details
    - Cannot be disabled by service

- control: API gateway logging
  effectiveness: MEDIUM
  implementation:
    - Log all requests at gateway
    - Include authenticated service identity
    - Centralized visibility
```

### Information Disclosure (Confidentiality)

**Threat 4.1: Secrets in Container Images**

- **Description:** Secrets hardcoded in container images or accessible in image layers
- **Attack Vector:** Image inspection, leaked images, registry compromise
- **Impact:** CRITICAL - Credential exposure, lateral movement, data breach
- **Likelihood:** HIGH - Very common mistake

**Mitigations:**

```yaml
- control: Secrets management integration
  effectiveness: CRITICAL
  implementation:
    tool: HashiCorp Vault, AWS Secrets Manager
    process:
      - Never hardcode secrets
      - Retrieve secrets at runtime
      - Short-lived dynamic secrets
    code_example: |
      import hvac

      # Initialize Vault client
      client = hvac.Client(url='https://vault.example.com')
      client.auth.kubernetes.login(
          role='service-a',
          jwt=open('/var/run/secrets/kubernetes.io/serviceaccount/token').read()
      )

      # Retrieve secret
      secret = client.secrets.kv.v2.read_secret_version(
          path='database/credentials/service-a'
      )
      db_password = secret['data']['data']['password']

- control: Image scanning for secrets
  effectiveness: HIGH
  implementation:
    tool: ggshield, TruffleHog, GitGuardian
    process:
      - Scan images in CI/CD
      - Block builds with detected secrets
      - Scan base images
    code_example: |
      # GitLab CI secret detection
      secret_detection:
        stage: test
        script:
          - ggshield scan docker service-a:$CI_COMMIT_SHA
        allow_failure: false

- control: Kubernetes secrets with encryption at rest
  effectiveness: HIGH
  implementation:
    - Enable encryption at rest for etcd
    - Use external KMS (AWS KMS, GCP KMS)
    - Rotate encryption keys regularly
    code_example: |
      # EncryptionConfiguration
      apiVersion: apiserver.config.k8s.io/v1
      kind: EncryptionConfiguration
      resources:
        - resources:
            - secrets
          providers:
            - aescbc:
                keys:
                  - name: key1
                    secret: <base64-encoded-key>
            - identity: {}

- control: Secret rotation
  effectiveness: HIGH
  implementation:
    - Automatic rotation every 90 days
    - Zero-downtime rotation
    - Audit secret access
```

**Threat 4.2: Service-to-Service Traffic Eavesdropping**

- **Description:** Attacker intercepts unencrypted traffic between services
- **Attack Vector:** Network snooping, compromised network infrastructure, ARP spoofing
- **Impact:** HIGH - Data exposure, credential theft, PII leakage
- **Likelihood:** MEDIUM - Requires network access

**Mitigations:**

```yaml
- control: Mutual TLS for all service communication
  effectiveness: CRITICAL
  implementation:
    service_mesh: Istio, Linkerd
    configuration:
      - Enforce mTLS globally
      - Automatic certificate management
      - Certificate rotation every 24 hours
    code_example: |
      apiVersion: security.istio.io/v1beta1
      kind: PeerAuthentication
      metadata:
        name: default
        namespace: istio-system
      spec:
        mtls:
          mode: STRICT

- control: Network encryption
  effectiveness: HIGH
  implementation:
    - TLS 1.3 minimum
    - Strong cipher suites only
    - Disable insecure protocols
    code_example: |
      # Nginx TLS config
      ssl_protocols TLSv1.3;
      ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384';
      ssl_prefer_server_ciphers on;

- control: Network segmentation
  effectiveness: MEDIUM
  implementation:
    - Separate network namespaces
    - VPC/subnet isolation
    - No direct pod-to-pod without policy

- control: Encrypted message queues
  effectiveness: HIGH
  implementation:
    - Enable TLS for Kafka, RabbitMQ
    - Encrypt messages at application level for sensitive data
    - Key rotation
```

**Threat 4.3: Log Data Exposure**

- **Description:** Sensitive data logged in plaintext and accessible to unauthorized users
- **Attack Vector:** Log aggregation access, log file access, log forwarding to external systems
- **Impact:** HIGH - PII exposure, credential leaks, compliance violations (GDPR, PCI DSS)
- **Likelihood:** HIGH - Very common mistake

**Mitigations:**

```yaml
- control: Log sanitization
  effectiveness: CRITICAL
  implementation:
    - Never log passwords, tokens, credit cards, PII
    - Redact sensitive fields automatically
    - Use structured logging with field filtering
    code_example: |
      import structlog

      def sanitize_log_data(logger, method_name, event_dict):
          sensitive_fields = ['password', 'token', 'ssn', 'credit_card']
          for field in sensitive_fields:
              if field in event_dict:
                  event_dict[field] = '***REDACTED***'
          return event_dict

      structlog.configure(
          processors=[
              sanitize_log_data,
              structlog.processors.JSONRenderer()
          ]
      )

- control: Log access controls
  effectiveness: HIGH
  implementation:
    - RBAC on log aggregation system
    - Separate logs by sensitivity level
    - Audit log access
    - Encrypt logs at rest

- control: Log retention policies
  effectiveness: MEDIUM
  implementation:
    - Automatic deletion of old logs
    - Compliance-based retention (7 years financial, 90 days debug)
    - Secure log disposal

- control: Dynamic data masking
  effectiveness: HIGH
  implementation:
    - Mask PII in logs based on viewer role
    - Show full data only to authorized users
    - Audit unmasking events
```

### Denial of Service

**Threat 5.1: Cascading Failures**

- **Description:** Failure in one service cascades through dependent services, causing system-wide outage
- **Attack Vector:** Service overload, resource exhaustion, synchronous blocking calls
- **Impact:** CRITICAL - Complete system unavailability
- **Likelihood:** MEDIUM - Common in tightly coupled systems

**Mitigations:**

```yaml
- control: Circuit breakers
  effectiveness: HIGH
  implementation:
    library: Hystrix, Resilience4j, Polly
    configuration:
      - Open circuit after 50% failure rate
      - 10-second wait before retry
      - Fallback to cached data or degraded mode
    code_example: |
      from pybreaker import CircuitBreaker

      breaker = CircuitBreaker(
          fail_max=5,
          timeout_duration=60,
          expected_exception=ServiceException
      )

      @breaker
      def call_downstream_service():
          response = requests.get('http://service-b/api/data')
          return response.json()

      try:
          data = call_downstream_service()
      except CircuitBreakerError:
          # Circuit open, use fallback
          data = get_cached_data()

- control: Bulkheads
  effectiveness: HIGH
  implementation:
    - Separate thread pools per dependency
    - Resource isolation per service
    - Limit concurrent requests
    code_example: |
      from concurrent.futures import ThreadPoolExecutor

      # Separate pools for different dependencies
      db_pool = ThreadPoolExecutor(max_workers=20)
      api_pool = ThreadPoolExecutor(max_workers=10)
      cache_pool = ThreadPoolExecutor(max_workers=5)

- control: Timeouts
  effectiveness: CRITICAL
  implementation:
    - Set aggressive timeouts (1-5 seconds)
    - Timeout at every network boundary
    - Cancel long-running operations
    code_example: |
      import requests

      response = requests.get(
          'http://service-b/api/data',
          timeout=(2, 5)  # (connection, read) timeout
      )

- control: Rate limiting per service
  effectiveness: HIGH
  implementation:
    - Limit requests to each dependency
    - Protect downstream services
    - Graceful degradation
    code_example: |
      apiVersion: networking.istio.io/v1alpha3
      kind: DestinationRule
      metadata:
        name: service-b-circuit-breaker
      spec:
        host: service-b
        trafficPolicy:
          connectionPool:
            tcp:
              maxConnections: 100
            http:
              http1MaxPendingRequests: 10
              http2MaxRequests: 100
              maxRequestsPerConnection: 2
          outlierDetection:
            consecutiveErrors: 5
            interval: 30s
            baseEjectionTime: 30s
```

**Threat 5.2: Resource Exhaustion**

- **Description:** Attacker or bug causes service to consume excessive CPU, memory, or connections
- **Attack Vector:** Unbounded loops, memory leaks, connection pool exhaustion
- **Impact:** HIGH - Service crashes, degraded performance
- **Likelihood:** HIGH - Common in production systems

**Mitigations:**

```yaml
- control: Resource limits and requests
  effectiveness: CRITICAL
  implementation:
    platform: Kubernetes
    configuration:
      - Set CPU and memory limits
      - Define resource requests
      - Use LimitRanges and ResourceQuotas
    code_example: |
      apiVersion: v1
      kind: Pod
      metadata:
        name: service-a
      spec:
        containers:
          - name: service-a
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"

- control: Horizontal Pod Autoscaling
  effectiveness: HIGH
  implementation:
    - Scale based on CPU/memory metrics
    - Custom metrics (request queue depth)
    - Minimum and maximum replicas
    code_example: |
      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      metadata:
        name: service-a-hpa
      spec:
        scaleTargetRef:
          apiVersion: apps/v1
          kind: Deployment
          name: service-a
        minReplicas: 3
        maxReplicas: 10
        metrics:
          - type: Resource
            resource:
              name: cpu
              target:
                type: Utilization
                averageUtilization: 70

- control: Connection pooling
  effectiveness: MEDIUM
  implementation:
    - Limit database connections per instance
    - Reuse connections
    - Close idle connections
    code_example: |
      from sqlalchemy import create_engine

      engine = create_engine(
          database_url,
          pool_size=10,
          max_overflow=20,
          pool_timeout=30,
          pool_recycle=3600
      )

- control: Memory leak detection
  effectiveness: MEDIUM
  implementation:
    - Monitor memory usage trends
    - Alert on gradual memory increase
    - Automatic pod restart on memory threshold
```

**Threat 5.3: Message Queue Flooding**

- **Description:** Attacker floods message queue with messages, overwhelming consumers
- **Attack Vector:** Compromised publisher, malicious internal service, bug causing message loop
- **Impact:** HIGH - Queue backup, consumer crashes, message loss
- **Likelihood:** MEDIUM - Can happen accidentally or maliciously

**Mitigations:**

```yaml
- control: Message rate limiting
  effectiveness: HIGH
  implementation:
    - Limit messages per producer
    - Queue size limits
    - Dead letter queue for poison messages
    code_example: |
      # RabbitMQ queue limits
      channel.queue_declare(
          queue='orders',
          arguments={
              'x-max-length': 10000,
              'x-overflow': 'reject-publish',
              'x-message-ttl': 3600000  # 1 hour
          }
      )

- control: Consumer backpressure
  effectiveness: HIGH
  implementation:
    - Consumer acknowledges only when processed
    - Prefetch limit to prevent overwhelming consumer
    - Reject messages if consumer overloaded
    code_example: |
      channel.basic_qos(prefetch_count=10)

      def callback(ch, method, properties, body):
          try:
              process_message(body)
              ch.basic_ack(delivery_tag=method.delivery_tag)
          except Exception:
              ch.basic_nack(
                  delivery_tag=method.delivery_tag,
                  requeue=False
              )

- control: Message validation
  effectiveness: MEDIUM
  implementation:
    - Reject malformed messages
    - Size limits on messages
    - Schema validation
    - Publisher authentication

- control: Dead letter queue
  effectiveness: HIGH
  implementation:
    - Route failed messages to DLQ
    - Analyze patterns in DLQ
    - Alert on DLQ growth
```

### Elevation of Privilege

**Threat 6.1: Container Escape**

- **Description:** Attacker escapes container to gain access to host or other containers
- **Attack Vector:** Kernel vulnerabilities, privileged containers, host path mounts
- **Impact:** CRITICAL - Full cluster compromise, data breach across all services
- **Likelihood:** LOW - Requires specific vulnerabilities or misconfigurations

**Mitigations:**

```yaml
- control: Security Context constraints
  effectiveness: CRITICAL
  implementation:
    - Run containers as non-root
    - Drop all capabilities
    - Read-only root filesystem
    - No privileged mode
    code_example: |
      apiVersion: v1
      kind: Pod
      metadata:
        name: service-a
      spec:
        securityContext:
          runAsNonRoot: true
          runAsUser: 10000
          fsGroup: 10000
          seccompProfile:
            type: RuntimeDefault
        containers:
          - name: service-a
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              capabilities:
                drop:
                  - ALL

- control: Pod Security Standards
  effectiveness: HIGH
  implementation:
    - Enforce Restricted PSS in production
    - Use Pod Security Admission controller
    - Block non-compliant pods
    code_example: |
      apiVersion: v1
      kind: Namespace
      metadata:
        name: production
        labels:
          pod-security.kubernetes.io/enforce: restricted
          pod-security.kubernetes.io/audit: restricted
          pod-security.kubernetes.io/warn: restricted

- control: Runtime security monitoring
  effectiveness: HIGH
  implementation:
    tool: Falco, Aqua, Sysdig
    detection:
      - Unexpected process execution
      - File system modifications
      - Network connections
      - Privilege escalation attempts
    code_example: |
      # Falco rule
      - rule: Unexpected outbound connection
        desc: Detect unexpected outbound network connection
        condition: >
          outbound and container and
          not proc.name in (expected_programs)
        output: >
          Unexpected outbound connection
          (user=%user.name command=%proc.cmdline connection=%fd.name)
        priority: WARNING

- control: Kernel hardening
  effectiveness: MEDIUM
  implementation:
    - Use hardened kernel
    - Enable SELinux/AppArmor
    - Disable unused kernel modules
    - Regular kernel patching
```

**Threat 6.2: Kubernetes RBAC Bypass**

- **Description:** Service obtains excessive Kubernetes API permissions
- **Attack Vector:** Overly permissive ServiceAccount, default ServiceAccount usage, RBAC misconfiguration
- **Impact:** HIGH - Cluster-wide access, secret theft, pod manipulation
- **Likelihood:** MEDIUM - Common RBAC misconfigurations

**Mitigations:**

```yaml
- control: Least privilege ServiceAccounts
  effectiveness: CRITICAL
  implementation:
    - Dedicated ServiceAccount per service
    - Minimal required permissions only
    - Never use default ServiceAccount
    code_example: |
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        name: service-a-sa
        namespace: production
      automountServiceAccountToken: true
      ---
      apiVersion: rbac.authorization.k8s.io/v1
      kind: Role
      metadata:
        name: service-a-role
        namespace: production
      rules:
        - apiGroups: [""]
          resources: ["configmaps"]
          verbs: ["get", "list"]
          resourceNames: ["service-a-config"]
      ---
      apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata:
        name: service-a-binding
        namespace: production
      subjects:
        - kind: ServiceAccount
          name: service-a-sa
          namespace: production
      roleRef:
        kind: Role
        name: service-a-role
        apiGroup: rbac.authorization.k8s.io

- control: Disable ServiceAccount token automounting
  effectiveness: HIGH
  implementation:
    - Set automountServiceAccountToken: false
    - Only mount when Kubernetes API access needed
    - Use projected volumes for fine-grained control

- control: RBAC audit
  effectiveness: MEDIUM
  implementation:
    tool: rbac-lookup, kubectl-who-can
    process:
      - Regular RBAC permission reviews
      - Identify overly permissive roles
      - Remove unused ServiceAccounts

- control: Admission controller validation
  effectiveness: HIGH
  implementation:
    - OPA policy to enforce RBAC best practices
    - Block pods using default ServiceAccount
    - Require explicit RBAC bindings
```

**Threat 6.3: Supply Chain Compromise**

- **Description:** Malicious code injected through compromised dependencies
- **Attack Vector:** Compromised npm/pip package, typosquatting, dependency confusion
- **Impact:** CRITICAL - Backdoor installation, data exfiltration, ransomware
- **Likelihood:** MEDIUM - Increasing trend in supply chain attacks

**Mitigations:**

```yaml
- control: Dependency scanning
  effectiveness: HIGH
  implementation:
    tool: Snyk, Dependabot, Renovate
    process:
      - Scan dependencies in CI/CD
      - Block high/critical vulnerabilities
      - Automated security updates
    code_example: |
      # GitHub Dependabot config
      version: 2
      updates:
        - package-ecosystem: "pip"
          directory: "/"
          schedule:
            interval: "weekly"
          open-pull-requests-limit: 10
          reviewers:
            - "security-team"

- control: Software Bill of Materials (SBOM)
  effectiveness: HIGH
  implementation:
    tool: Syft, CycloneDX
    process:
      - Generate SBOM for each image
      - Track all dependencies
      - Vulnerability correlation
    code_example: |
      # Generate SBOM
      syft packages gcr.io/project/service-a:v1.2.3 \
        -o cyclonedx-json > sbom.json

- control: Private package registry
  effectiveness: HIGH
  implementation:
    - Use Artifactory, Nexus, or cloud registry
    - Proxy and cache public packages
    - Scan packages before caching
    - Block unapproved packages

- control: Vendor dependency pinning
  effectiveness: MEDIUM
  implementation:
    - Pin exact versions (not ranges)
    - Use lock files (package-lock.json, Pipfile.lock)
    - Review all dependency updates
    code_example: |
      # requirements.txt with pinned versions
      flask==2.3.2
      sqlalchemy==2.0.18
      pyjwt==2.8.0

- control: Code signing and verification
  effectiveness: HIGH
  implementation:
    - Verify package signatures
    - Use trusted registries only
    - Checksum verification
```

## Threat Risk Matrix

| Threat | Impact | Likelihood | Risk | Priority |
|--------|--------|------------|------|----------|
| Service Impersonation | CRITICAL | MEDIUM | CRITICAL | P0 |
| Container Image Tampering | CRITICAL | MEDIUM | CRITICAL | P0 |
| Container Escape | CRITICAL | LOW | HIGH | P1 |
| Secrets in Images | CRITICAL | HIGH | CRITICAL | P0 |
| Database Injection | CRITICAL | MEDIUM | CRITICAL | P0 |
| Kubernetes RBAC Bypass | HIGH | MEDIUM | HIGH | P1 |
| Supply Chain Compromise | CRITICAL | MEDIUM | CRITICAL | P0 |
| Cascading Failures | CRITICAL | MEDIUM | CRITICAL | P0 |
| API Token Theft | HIGH | HIGH | HIGH | P1 |
| Traffic Eavesdropping | HIGH | MEDIUM | HIGH | P1 |
| Log Data Exposure | HIGH | HIGH | HIGH | P1 |
| Resource Exhaustion | HIGH | HIGH | HIGH | P1 |
| Message Queue Tampering | HIGH | MEDIUM | MEDIUM | P2 |
| Configuration Tampering | HIGH | MEDIUM | MEDIUM | P2 |
| Message Queue Flooding | HIGH | MEDIUM | MEDIUM | P2 |
| Tracing Blind Spots | MEDIUM | HIGH | MEDIUM | P2 |
| Service Call Denial | MEDIUM | LOW | LOW | P3 |

## Security Controls Summary

**Critical (P0):**
- Mutual TLS (mTLS) for all service-to-service communication
- Image signing and admission control
- Secrets management system (Vault)
- Container security contexts (non-root, read-only, no privileges)
- Parameterized queries at every service
- Circuit breakers and timeouts
- RBAC least privilege
- Dependency scanning and SBOM

**High Priority (P1):**
- Short-lived tokens with rotation
- Network policies and segmentation
- Distributed tracing
- Log sanitization
- Resource limits and autoscaling
- Runtime security monitoring (Falco)
- Private package registry

**Recommended (P2):**
- Message signing
- Configuration encryption
- Structured logging with trace context
- Connection pooling
- Dead letter queues
- RBAC audit tools

## Implementation Checklist

- [ ] Deploy service mesh (Istio/Linkerd) with strict mTLS
- [ ] Configure image signing and admission controller
- [ ] Deploy HashiCorp Vault for secrets management
- [ ] Set Pod Security Standards to Restricted
- [ ] Implement least privilege RBAC for all services
- [ ] Deploy distributed tracing (OpenTelemetry)
- [ ] Configure structured logging with sanitization
- [ ] Implement circuit breakers for all service calls
- [ ] Set resource limits on all pods
- [ ] Deploy horizontal pod autoscalers
- [ ] Configure network policies
- [ ] Enable Kubernetes audit logging
- [ ] Deploy runtime security monitoring (Falco)
- [ ] Implement dependency scanning in CI/CD
- [ ] Generate SBOMs for all images
- [ ] Configure message queue encryption
- [ ] Set up centralized log aggregation (ELK/Splunk)
- [ ] Implement rate limiting at API gateway and service mesh
- [ ] Deploy monitoring and alerting (Prometheus/Grafana)
- [ ] Conduct regular penetration testing

## References

- [OWASP Microservices Security](https://owasp.org/www-project-microservices-security/)
- [NIST SP 800-204: Security Strategies for Microservices](https://csrc.nist.gov/publications/detail/sp/800-204/final)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/security-best-practices/)
- [CNCF Cloud Native Security Whitepaper](https://www.cncf.io/wp-content/uploads/2020/11/CNCF_Cloud_Native_Security_Whitepaper_Nov_2020.pdf)
- [Container Security Guide (NIST SP 800-190)](https://csrc.nist.gov/publications/detail/sp/800-190/final)
