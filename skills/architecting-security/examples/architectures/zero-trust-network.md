# Zero Trust Network Architecture

## Overview

Zero Trust security architecture eliminates implicit trust based on network location. Verify every access request based on identity, device posture, and context regardless of origin. Enforce least privilege access with continuous verification and monitoring.

## Core Principles

1. **Never Trust, Always Verify** - Authenticate and authorize every request
2. **Assume Breach** - Minimize blast radius through segmentation
3. **Verify Explicitly** - Use all available data points (identity, location, device, data classification)
4. **Least Privilege Access** - Just-in-time and just-enough access
5. **Microsegmentation** - Isolate workloads and limit lateral movement
6. **End-to-End Encryption** - Encrypt data in transit and at rest

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ZERO TRUST CONTROL PLANE                          │
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │   Identity   │  │    Device    │  │   Policy     │  │  Telemetry   ││
│  │   Provider   │  │  Management  │  │   Engine     │  │  & Analytics ││
│  │              │  │              │  │              │  │              ││
│  │ - SSO/SAML   │  │ - MDM/UEM    │  │ - RBAC       │  │ - SIEM       ││
│  │ - MFA        │  │ - Posture    │  │ - ABAC       │  │ - Behavioral ││
│  │ - Context    │  │ - Compliance │  │ - Risk Score │  │ - Forensics  ││
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘│
│         │                 │                 │                 │         │
│         └─────────────────┴─────────────────┴─────────────────┘         │
│                                   │                                      │
└───────────────────────────────────┼──────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌──────────────────────┐        ┌──────────────────────┐
        │  Policy Enforcement  │        │  Policy Enforcement  │
        │  Point (PEP)         │        │  Point (PEP)         │
        │                      │        │                      │
        │  - Reverse Proxy     │        │  - Service Mesh      │
        │  - API Gateway       │        │  - Sidecar Proxy     │
        │  - Load Balancer     │        │  - eBPF              │
        └──────────┬───────────┘        └──────────┬───────────┘
                   │                               │
                   ▼                               ▼
        ┌──────────────────────┐        ┌──────────────────────┐
        │   External Users     │        │  Internal Services   │
        │                      │        │                      │
        │  Remote Workers ─────┼───────▶│  Microservices       │
        │  Partners            │        │  Databases           │
        │  Contractors         │        │  APIs                │
        └──────────────────────┘        └──────────────────────┘

                    TRUST BOUNDARIES ELIMINATED
                    ═════════════════════════════

     Every request verified │ Identity-based access │ Continuous monitoring
```

## Identity-Based Access Control

### Single Sign-On (SSO) Integration

**SAML Authentication Flow:**

```
┌──────┐                ┌──────────┐              ┌─────────┐
│User  │                │ Identity │              │Resource │
│      │                │ Provider │              │ (App)   │
└──┬───┘                └────┬─────┘              └────┬────┘
   │                         │                         │
   │ 1. Access Resource      │                         │
   ├────────────────────────────────────────────────────>
   │                         │                         │
   │ 2. Redirect to IdP      │                         │
   <─────────────────────────────────────────────────────
   │                         │                         │
   │ 3. Authenticate         │                         │
   ├────────────────────────>│                         │
   │                         │                         │
   │ 4. MFA Challenge        │                         │
   <─────────────────────────┤                         │
   │                         │                         │
   │ 5. MFA Response         │                         │
   ├────────────────────────>│                         │
   │                         │                         │
   │                         │ 6. Check Device Posture │
   │                         ├────────┐                │
   │                         │        │                │
   │                         <────────┘                │
   │                         │                         │
   │                         │ 7. Evaluate Risk Score  │
   │                         ├────────┐                │
   │                         │        │                │
   │                         <────────┘                │
   │                         │                         │
   │ 8. SAML Assertion       │                         │
   <─────────────────────────┤                         │
   │                         │                         │
   │ 9. Present Assertion    │                         │
   ├────────────────────────────────────────────────────>
   │                         │                         │
   │                         │  10. Validate Assertion │
   │                         │    <────────────────────┤
   │                         │                         │
   │ 11. Access Granted      │                         │
   <─────────────────────────────────────────────────────
```

**SAML Configuration:**

```xml
<saml:AttributeStatement>
  <saml:Attribute Name="email">
    <saml:AttributeValue>user@example.com</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="groups">
    <saml:AttributeValue>Engineering</saml:AttributeValue>
    <saml:AttributeValue>ProductionAccess</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="device_id">
    <saml:AttributeValue>device-12345</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="device_compliant">
    <saml:AttributeValue>true</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="ip_address">
    <saml:AttributeValue>203.0.113.45</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="risk_score">
    <saml:AttributeValue>low</saml:AttributeValue>
  </saml:Attribute>
</saml:AttributeStatement>
```

### Multi-Factor Authentication (MFA)

**Adaptive MFA Policy:**

```json
{
  "policy_name": "adaptive_mfa",
  "conditions": [
    {
      "name": "always_require_mfa",
      "rule": "user.role in ['admin', 'privileged_user']",
      "action": {
        "mfa_required": true,
        "allowed_factors": ["webauthn", "totp", "push"],
        "step_up_required": true
      }
    },
    {
      "name": "risk_based_mfa",
      "rule": "risk_score > 50 OR ip_reputation == 'suspicious'",
      "action": {
        "mfa_required": true,
        "allowed_factors": ["webauthn"],
        "max_attempts": 3
      }
    },
    {
      "name": "new_device_mfa",
      "rule": "device.first_seen < 7d",
      "action": {
        "mfa_required": true,
        "allowed_factors": ["webauthn", "totp", "push"],
        "device_enrollment_required": true
      }
    },
    {
      "name": "location_based_mfa",
      "rule": "geo.country NOT IN allowed_countries",
      "action": {
        "mfa_required": true,
        "allowed_factors": ["webauthn"],
        "admin_notification": true
      }
    }
  ]
}
```

### Context-Aware Access

**Access Decision Factors:**

```python
class AccessDecisionEngine:
    """
    Evaluate access requests based on multiple context factors.
    """

    def evaluate_access(self, request):
        """
        Calculate risk score and make access decision.
        """
        risk_score = 0
        factors = []

        # Identity verification
        if not request.user.mfa_verified:
            risk_score += 50
            factors.append("MFA_NOT_VERIFIED")

        # Device posture
        if not request.device.is_compliant():
            risk_score += 30
            factors.append("DEVICE_NON_COMPLIANT")

        if not request.device.is_managed():
            risk_score += 20
            factors.append("DEVICE_UNMANAGED")

        if not request.device.has_latest_os():
            risk_score += 15
            factors.append("OS_OUTDATED")

        # Network context
        if request.ip_address.is_tor_exit_node():
            risk_score += 40
            factors.append("TOR_EXIT_NODE")

        if request.ip_address.reputation == "suspicious":
            risk_score += 35
            factors.append("SUSPICIOUS_IP")

        if request.geo_location.country not in self.allowed_countries:
            risk_score += 25
            factors.append("DISALLOWED_COUNTRY")

        # Behavioral analysis
        if self.is_impossible_travel(request):
            risk_score += 60
            factors.append("IMPOSSIBLE_TRAVEL")

        if self.is_anomalous_access_pattern(request):
            risk_score += 40
            factors.append("ANOMALOUS_PATTERN")

        # Time-based risk
        if not self.is_business_hours(request):
            risk_score += 10
            factors.append("AFTER_HOURS")

        # Resource sensitivity
        if request.resource.classification == "highly_confidential":
            risk_score += 20
            factors.append("SENSITIVE_RESOURCE")

        # Make decision
        decision = self.make_decision(risk_score, factors)

        return {
            "allowed": decision["allowed"],
            "risk_score": risk_score,
            "factors": factors,
            "action": decision["action"],
            "reason": decision["reason"]
        }

    def make_decision(self, risk_score, factors):
        """
        Determine access based on risk score.
        """
        if risk_score >= 80:
            return {
                "allowed": False,
                "action": "DENY",
                "reason": "Risk score too high"
            }
        elif risk_score >= 50:
            return {
                "allowed": True,
                "action": "ALLOW_WITH_STEP_UP",
                "reason": "Requires additional verification"
            }
        elif risk_score >= 30:
            return {
                "allowed": True,
                "action": "ALLOW_WITH_MONITORING",
                "reason": "Elevated monitoring required"
            }
        else:
            return {
                "allowed": True,
                "action": "ALLOW",
                "reason": "Normal access granted"
            }
```

## Device Posture Verification

### Device Trust Requirements

**Compliance Checks:**

```yaml
device_posture_policy:
  name: "corporate_device_policy"
  requirements:
    - check: "device_managed"
      description: "Device must be enrolled in MDM"
      severity: "critical"
      required: true

    - check: "encryption_enabled"
      description: "Full disk encryption required"
      severity: "critical"
      required: true

    - check: "os_version"
      description: "Operating system must be up to date"
      severity: "high"
      required: true
      min_versions:
        windows: "10.0.19044"
        macos: "13.0"
        ios: "16.0"
        android: "13.0"

    - check: "antivirus_running"
      description: "Antivirus must be active and updated"
      severity: "high"
      required: true
      max_definition_age: "7d"

    - check: "firewall_enabled"
      description: "Host firewall must be enabled"
      severity: "medium"
      required: true

    - check: "screen_lock"
      description: "Screen lock must be configured"
      severity: "medium"
      required: true
      max_idle_time: "10m"

    - check: "password_policy"
      description: "Strong password required"
      severity: "high"
      required: true
      min_length: 14
      complexity: true

    - check: "unauthorized_apps"
      description: "No blacklisted applications"
      severity: "high"
      required: true
      blacklist:
        - "remote_access_tools"
        - "file_sharing_apps"
        - "cryptocurrency_miners"

    - check: "certificate_valid"
      description: "Valid device certificate"
      severity: "critical"
      required: true
      max_age: "365d"
```

### Continuous Verification

```python
import asyncio
from datetime import datetime, timedelta

class DevicePostureMonitor:
    """
    Continuously monitor device posture and revoke access if non-compliant.
    """

    def __init__(self, check_interval=300):
        self.check_interval = check_interval  # 5 minutes
        self.active_sessions = {}

    async def monitor_session(self, session_id, device_id):
        """
        Monitor device posture for an active session.
        """
        while session_id in self.active_sessions:
            try:
                # Check device posture
                posture = await self.check_device_posture(device_id)

                if not posture["compliant"]:
                    # Device is no longer compliant
                    await self.revoke_session(
                        session_id,
                        reason=f"Device non-compliant: {posture['violations']}"
                    )
                    break

                # Check for certificate expiry
                cert_expiry = await self.get_certificate_expiry(device_id)
                if cert_expiry < datetime.utcnow() + timedelta(hours=1):
                    await self.notify_renewal_required(device_id)

                # Sleep until next check
                await asyncio.sleep(self.check_interval)

            except Exception as e:
                # Error checking posture - assume non-compliant
                await self.revoke_session(
                    session_id,
                    reason=f"Unable to verify device posture: {str(e)}"
                )
                break

    async def check_device_posture(self, device_id):
        """
        Query MDM/UEM for current device compliance status.
        """
        # Integration with MDM (Intune, Workspace ONE, Jamf, etc.)
        compliance_status = await self.mdm_client.get_compliance(device_id)

        violations = []
        if not compliance_status["encryption_enabled"]:
            violations.append("DISK_NOT_ENCRYPTED")
        if not compliance_status["av_running"]:
            violations.append("ANTIVIRUS_DISABLED")
        if compliance_status["os_outdated"]:
            violations.append("OS_VERSION_OUTDATED")

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "last_checked": datetime.utcnow()
        }

    async def revoke_session(self, session_id, reason):
        """
        Immediately terminate non-compliant session.
        """
        session = self.active_sessions.pop(session_id, None)
        if session:
            # Revoke tokens
            await self.identity_provider.revoke_tokens(session["tokens"])

            # Notify user
            await self.notification_service.send(
                to=session["user_email"],
                subject="Session Terminated - Device Non-Compliant",
                body=f"Your session was terminated: {reason}"
            )

            # Log event
            await self.audit_log.record({
                "event": "SESSION_REVOKED",
                "session_id": session_id,
                "reason": reason,
                "timestamp": datetime.utcnow()
            })
```

## Microsegmentation

### Service-to-Service Communication

**Identity-Based Segmentation:**

```yaml
# Service Mesh Policy (Istio example)
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: frontend-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: frontend
  action: ALLOW
  rules:
    # Only API gateway can call frontend
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/api-gateway"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/*"]
      when:
        - key: request.auth.claims[iss]
          values: ["https://auth.example.com"]
        - key: request.auth.claims[aud]
          values: ["frontend-service"]

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: backend-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
    # Only frontend can call backend
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/frontend"]
      to:
        - operation:
            methods: ["GET", "POST", "PUT", "DELETE"]
            paths: ["/api/v1/*"]
      when:
        - key: source.namespace
          values: ["production"]

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: database-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: database-proxy
  action: ALLOW
  rules:
    # Only backend can access database
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/backend"]
      to:
        - operation:
            ports: ["5432"]
      when:
        - key: connection.sni
          values: ["postgres.production.svc.cluster.local"]
```

### Network-Level Segmentation

**Zero Trust Network Zones:**

```
┌─────────────────────────────────────────────────────────────┐
│                     DMZ Zone                                 │
│  - WAF / Reverse Proxy                                       │
│  - DDoS Protection                                           │
│  - No direct internet access to apps                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ mTLS required
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 Application Zone                             │
│  - Stateless services                                        │
│  - No persistent data                                        │
│  - Identity-based access only                                │
│  - East-west traffic encrypted                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ JWT + mTLS required
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Zone                                  │
│  - Databases                                                 │
│  - Object storage                                            │
│  - No ingress from internet                                  │
│  - Encryption at rest enforced                               │
└─────────────────────────────────────────────────────────────┘
```

**eBPF-Based Segmentation (Cilium):**

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: l7-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
          rules:
            http:
              - method: "GET"
                path: "/api/data"
              - method: "POST"
                path: "/api/data"
                headerMatches:
                  - mismatch: EQUAL
                    name: X-API-Key
                    secret:
                      name: api-keys
                      namespace: production

  egress:
    - toEndpoints:
        - matchLabels:
            app: database
      toPorts:
        - ports:
            - port: "5432"
              protocol: TCP

    - toFQDNs:
        - matchName: "api.external-service.com"
      toPorts:
        - ports:
            - port: "443"
              protocol: TCP
```

## Just-In-Time Access

### Temporary Privilege Escalation

**Access Request Workflow:**

```python
from datetime import datetime, timedelta
import uuid

class JITAccessManager:
    """
    Manage just-in-time privileged access requests.
    """

    def request_access(self, user_id, resource, role, duration_hours,
                      justification, ticket_id=None):
        """
        Request temporary elevated access.
        """
        # Validate request
        if duration_hours > 8:
            raise ValueError("Maximum access duration is 8 hours")

        if not justification or len(justification) < 20:
            raise ValueError("Detailed justification required")

        # Create access request
        request_id = str(uuid.uuid4())
        request = {
            "request_id": request_id,
            "user_id": user_id,
            "resource": resource,
            "role": role,
            "duration": duration_hours,
            "justification": justification,
            "ticket_id": ticket_id,
            "requested_at": datetime.utcnow(),
            "status": "PENDING_APPROVAL",
            "approvers": self.get_required_approvers(resource, role)
        }

        # Store request
        self.db.save_request(request)

        # Notify approvers
        self.notification_service.notify_approvers(
            approvers=request["approvers"],
            request=request
        )

        return request_id

    def approve_request(self, request_id, approver_id, approval_note):
        """
        Approve access request and grant temporary permissions.
        """
        request = self.db.get_request(request_id)

        if request["status"] != "PENDING_APPROVAL":
            raise ValueError("Request is not pending approval")

        if approver_id not in request["approvers"]:
            raise ValueError("User is not authorized to approve this request")

        # Grant access
        expiry = datetime.utcnow() + timedelta(hours=request["duration"])

        access_grant = {
            "grant_id": str(uuid.uuid4()),
            "request_id": request_id,
            "user_id": request["user_id"],
            "resource": request["resource"],
            "role": request["role"],
            "granted_at": datetime.utcnow(),
            "expires_at": expiry,
            "approver_id": approver_id,
            "approval_note": approval_note
        }

        # Apply IAM policy
        self.iam_service.grant_temporary_role(
            user_id=request["user_id"],
            resource=request["resource"],
            role=request["role"],
            expiry=expiry
        )

        # Update request status
        request["status"] = "APPROVED"
        request["approved_at"] = datetime.utcnow()
        request["access_grant"] = access_grant
        self.db.update_request(request)

        # Schedule automatic revocation
        self.scheduler.schedule_revocation(
            grant_id=access_grant["grant_id"],
            revoke_at=expiry
        )

        # Notify requester
        self.notification_service.notify_user(
            user_id=request["user_id"],
            subject="Access Request Approved",
            body=f"Access granted until {expiry}"
        )

        # Audit log
        self.audit_log.record({
            "event": "JIT_ACCESS_GRANTED",
            "request_id": request_id,
            "grant_id": access_grant["grant_id"],
            "user_id": request["user_id"],
            "resource": request["resource"],
            "role": request["role"],
            "approver_id": approver_id,
            "expires_at": expiry
        })

        return access_grant

    def revoke_access(self, grant_id, reason="EXPIRED"):
        """
        Revoke temporary access.
        """
        grant = self.db.get_grant(grant_id)

        # Remove IAM permissions
        self.iam_service.revoke_role(
            user_id=grant["user_id"],
            resource=grant["resource"],
            role=grant["role"]
        )

        # Update grant status
        grant["revoked_at"] = datetime.utcnow()
        grant["revocation_reason"] = reason
        self.db.update_grant(grant)

        # Audit log
        self.audit_log.record({
            "event": "JIT_ACCESS_REVOKED",
            "grant_id": grant_id,
            "user_id": grant["user_id"],
            "reason": reason
        })
```

### Break-Glass Access

**Emergency Access Procedure:**

```yaml
break_glass_policy:
  name: "emergency_access"
  description: "Break-glass access for critical incidents"

  accounts:
    - account_id: "breakglass-001"
      stored_in: "physical_safe"
      rotation_frequency: "quarterly"
      permissions: ["full_admin"]

    - account_id: "breakglass-002"
      stored_in: "physical_safe"
      rotation_frequency: "quarterly"
      permissions: ["full_admin"]

  activation_triggers:
    - "Major security incident (P0)"
    - "Complete system failure"
    - "All admin accounts locked"
    - "Identity provider outage"

  activation_procedure:
    1: "Incident commander declares break-glass event"
    2: "Retrieve credentials from physical safe (requires two keyholders)"
    3: "Log break-glass activation in offline system"
    4: "Authenticate with break-glass account"
    5: "All actions logged to immutable audit trail"
    6: "Notify security team immediately"
    7: "Mandatory post-incident review within 24 hours"

  automatic_alerts:
    - channel: "security_team_pager"
      severity: "CRITICAL"
    - channel: "exec_team_email"
      severity: "HIGH"
    - channel: "siem"
      severity: "CRITICAL"

  post_activation:
    - "Rotate break-glass credentials within 4 hours"
    - "Review all actions taken"
    - "Root cause analysis within 48 hours"
    - "Update incident response procedures"
```

## Continuous Verification

### Session Monitoring

```python
class SessionMonitor:
    """
    Monitor active sessions for anomalous behavior.
    """

    def monitor_session(self, session_id):
        """
        Continuously analyze session for suspicious activity.
        """
        session = self.get_session(session_id)
        baseline = self.get_user_baseline(session["user_id"])

        anomalies = []

        # Check access patterns
        recent_resources = self.get_recent_resource_access(session_id)
        if self.is_unusual_resource_access(recent_resources, baseline):
            anomalies.append({
                "type": "UNUSUAL_RESOURCE_ACCESS",
                "severity": "MEDIUM",
                "details": "Accessing resources outside normal pattern"
            })

        # Check data volume
        data_transferred = self.get_data_transfer_volume(session_id)
        if data_transferred > baseline["avg_data_transfer"] * 10:
            anomalies.append({
                "type": "EXCESSIVE_DATA_TRANSFER",
                "severity": "HIGH",
                "details": f"Transferred {data_transferred}MB (baseline: {baseline['avg_data_transfer']}MB)"
            })

        # Check geographic location changes
        current_location = self.get_session_location(session_id)
        if self.is_impossible_travel(session["previous_location"], current_location):
            anomalies.append({
                "type": "IMPOSSIBLE_TRAVEL",
                "severity": "CRITICAL",
                "details": "Location changed faster than physically possible"
            })

        # Check API call patterns
        api_calls = self.get_api_call_frequency(session_id)
        if api_calls > baseline["avg_api_calls"] * 5:
            anomalies.append({
                "type": "EXCESSIVE_API_CALLS",
                "severity": "MEDIUM",
                "details": f"API call rate {api_calls}/min (baseline: {baseline['avg_api_calls']}/min)"
            })

        # Take action on anomalies
        if anomalies:
            self.handle_anomalies(session_id, anomalies)

        return anomalies

    def handle_anomalies(self, session_id, anomalies):
        """
        Respond to detected anomalies based on severity.
        """
        max_severity = max(a["severity"] for a in anomalies)

        if max_severity == "CRITICAL":
            # Immediately terminate session
            self.terminate_session(session_id, reason="Critical anomaly detected")
            self.create_security_incident(session_id, anomalies)

        elif max_severity == "HIGH":
            # Require step-up authentication
            self.require_step_up_auth(session_id)
            self.alert_security_team(session_id, anomalies)

        elif max_severity == "MEDIUM":
            # Increase monitoring frequency
            self.increase_monitoring(session_id)
            self.log_suspicious_activity(session_id, anomalies)
```

## Policy Enforcement Points

### API Gateway Enforcement

```yaml
# Kong Gateway Configuration
plugins:
  - name: oidc
    config:
      issuer: "https://auth.example.com"
      client_id: "api-gateway"
      client_secret: "${OIDC_CLIENT_SECRET}"
      scopes:
        - openid
        - profile
        - email
      bearer_only: true
      realm: "production"
      introspection_endpoint: "https://auth.example.com/introspect"

  - name: rate-limiting
    config:
      minute: 100
      hour: 1000
      policy: "cluster"
      fault_tolerant: true

  - name: request-transformer
    config:
      add:
        headers:
          - "X-User-Id:$(claims.sub)"
          - "X-User-Email:$(claims.email)"
          - "X-User-Roles:$(claims.roles)"

  - name: acl
    config:
      allow:
        - "authenticated_users"
      hide_groups_header: true

  - name: correlation-id
    config:
      header_name: "X-Correlation-ID"
      generator: "uuid"
      echo_downstream: true
```

### Reverse Proxy Enforcement (Nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # mTLS enforcement
    ssl_client_certificate /etc/nginx/ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;

    # Extract client certificate details
    set $ssl_client_subject_dn_cn "";
    if ($ssl_client_s_dn ~ "CN=([^,]+)") {
        set $ssl_client_subject_dn_cn $1;
    }

    location /api/ {
        # Verify JWT token
        auth_jwt "API Access";
        auth_jwt_key_file /etc/nginx/jwt_public_key.pem;

        # Check required claims
        auth_jwt_claim_set $jwt_email email;
        auth_jwt_claim_set $jwt_roles roles;

        # Rate limiting
        limit_req zone=api_limit burst=20 nodelay;

        # Forward auth context
        proxy_set_header X-Client-Cert-CN $ssl_client_subject_dn_cn;
        proxy_set_header X-JWT-Email $jwt_email;
        proxy_set_header X-JWT-Roles $jwt_roles;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Backend upstream
        proxy_pass https://backend-service;
        proxy_ssl_verify on;
        proxy_ssl_trusted_certificate /etc/nginx/backend-ca.crt;
    }
}
```

## Key Security Metrics

Monitor these metrics for Zero Trust effectiveness:

1. **Authentication Metrics:**
   - MFA adoption rate (target: 100%)
   - Failed authentication attempts
   - Step-up authentication triggers
   - Break-glass account usage (target: 0)

2. **Device Metrics:**
   - Device compliance rate (target: 100%)
   - Certificate expiry warnings
   - Unauthorized device access attempts
   - Average time to remediation

3. **Access Metrics:**
   - JIT access requests per day
   - Average approval time
   - Access denials by reason
   - Excessive privilege usage

4. **Network Metrics:**
   - Microsegmentation policy violations
   - East-west traffic encryption rate (target: 100%)
   - Lateral movement attempts blocked
   - Service-to-service auth failures

5. **Behavioral Metrics:**
   - Anomaly detection alerts
   - Risk score distribution
   - Sessions terminated due to anomalies
   - False positive rate

## Implementation Checklist

- [ ] Deploy identity provider with MFA
- [ ] Integrate device management (MDM/UEM)
- [ ] Configure adaptive authentication policies
- [ ] Implement device posture verification
- [ ] Deploy service mesh for microsegmentation
- [ ] Configure identity-based network policies
- [ ] Implement JIT access system
- [ ] Create break-glass procedures
- [ ] Deploy API gateway with policy enforcement
- [ ] Configure reverse proxy with mTLS
- [ ] Enable end-to-end encryption (mTLS)
- [ ] Deploy SIEM for continuous monitoring
- [ ] Create behavioral analysis baselines
- [ ] Implement session monitoring
- [ ] Configure automated response playbooks
- [ ] Create security metrics dashboard
- [ ] Conduct user training
- [ ] Perform tabletop exercises
- [ ] Document incident response procedures
- [ ] Establish continuous improvement process

## References

- [NIST Zero Trust Architecture (SP 800-207)](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Google BeyondCorp](https://cloud.google.com/beyondcorp)
- [Microsoft Zero Trust](https://www.microsoft.com/en-us/security/business/zero-trust)
- [CISA Zero Trust Maturity Model](https://www.cisa.gov/zero-trust-maturity-model)
- [Forrester Zero Trust eXtended (ZTX)](https://www.forrester.com/what-it-means/zero-trust/)
