# DNS-as-Code Tools Comparison

Comprehensive comparison of DNS automation tools with recommendations, examples, and decision frameworks.

## Table of Contents

1. [Tool Overview](#tool-overview)
2. [ExternalDNS](#externaldns)
3. [OctoDNS](#octodns)
4. [DNSControl](#dnscontrol)
5. [Terraform](#terraform)
6. [Comparison Matrix](#comparison-matrix)
7. [Selection Guide](#selection-guide)

---

## Tool Overview

### What is DNS-as-Code?

DNS-as-Code treats DNS records as declarative configuration files, enabling:
- Version control for DNS changes (Git)
- Code review for DNS updates
- Automated deployment pipelines
- Consistency across environments
- Rollback capabilities

### Tool Categories

**1. Kubernetes-Native:** external-dns
- Watches Kubernetes resources
- Automatically syncs to DNS providers
- Annotation-based configuration

**2. Multi-Provider Sync:** OctoDNS, DNSControl
- Define DNS in configuration files
- Sync to multiple providers simultaneously
- Provider-agnostic abstraction

**3. Infrastructure-as-Code:** Terraform, Pulumi
- Manage DNS alongside other infrastructure
- Provider-specific resources
- State management

---

## ExternalDNS

### Overview

Kubernetes controller that synchronizes Service and Ingress resources with DNS providers.

**Repository:** `/kubernetes-sigs/external-dns`
**Language:** Go
**License:** Apache 2.0
**Maturity:** Production-ready (CNCF project)

**Trust Indicators:**
- Context7 Code Snippets: 671+
- GitHub Stars: 7k+
- Active maintenance: Kubernetes SIG project
- Production use: Thousands of clusters

### Key Features

**Automatic Sync:**
- Watches Kubernetes Services (LoadBalancer, NodePort)
- Watches Ingress resources
- Creates/updates/deletes DNS records automatically
- No manual DNS updates required

**Annotation-Based:**
```yaml
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: app.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
```

**Provider Support (20+):**
- AWS Route53
- Google Cloud DNS
- Azure DNS
- Cloudflare
- DigitalOcean
- Linode
- OVH
- RFC2136 (BIND, PowerDNS)
- Many more...

### Strengths

✅ **Kubernetes-native** - Seamless integration
✅ **Automatic** - No manual DNS updates
✅ **Annotation-based** - Simple configuration
✅ **Multi-provider** - 20+ supported providers
✅ **Production-ready** - Widely used, stable

### Limitations

❌ **Kubernetes-only** - Cannot manage non-K8s DNS
❌ **Limited logic** - Cannot express complex rules
❌ **Single cluster** - Each cluster needs own external-dns
❌ **No preview mode** - Changes applied directly (policy=sync)

### When to Use

Use external-dns when:
- Running Kubernetes workloads
- Want automatic DNS for Services/Ingresses
- Need zero manual DNS management
- GitOps workflow (ArgoCD, Flux)

Skip external-dns when:
- Not using Kubernetes
- Need complex DNS logic
- Managing DNS across multiple non-K8s systems

### Configuration Example

**Helm Installation:**
```bash
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm repo update

helm install external-dns external-dns/external-dns \
  --namespace external-dns \
  --create-namespace \
  --set provider=aws \
  --set aws.region=us-east-1 \
  --set txtOwnerId=my-k8s-cluster \
  --set domainFilters[0]=example.com \
  --set policy=sync \
  --set registry=txt
```

**Service with Annotation:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  annotations:
    external-dns.alpha.kubernetes.io/hostname: nginx.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
```

**Result:**
```
# DNS record automatically created:
nginx.example.com.  300  IN  A  <LoadBalancer-IP>
```

### Best Practices

1. **Use TXT registry** - Tracks ownership
2. **Set domain filter** - Prevent accidental changes to other domains
3. **Use policy=sync** - Allows deletions when resources removed
4. **One external-dns per cluster** - Avoid conflicts
5. **Monitor logs** - Watch for errors/rate limits

### Common Issues

**Issue: Records not created**
```bash
# Check logs
kubectl logs -n external-dns deployment/external-dns

# Verify annotation
kubectl get service nginx -o yaml | grep external-dns

# Check domain filter
kubectl describe deployment -n external-dns external-dns | grep domain-filter
```

**Issue: Permission denied**
```bash
# AWS: Check IAM policy
aws iam get-policy-version \
  --policy-arn arn:aws:iam::123456789012:policy/external-dns \
  --version-id v1

# GCP: Check service account
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:external-dns@"
```

---

## OctoDNS

### Overview

Python-based DNS-as-code tool that syncs DNS records from YAML configuration files to multiple providers.

**Repository:** `/octodns/octodns`
**Language:** Python
**License:** MIT
**Maturity:** Production-ready

**Trust Indicators:**
- Context7 Code Snippets: 128+
- Context7 Benchmark Score: 88.2/100
- Source Reputation: High
- Used by: GitHub (internally)

### Key Features

**YAML Configuration:**
- Define DNS zones in YAML files
- Version control with Git
- Human-readable format

**Multi-Provider Sync:**
- Sync same zone to multiple providers
- Provider-agnostic abstraction
- Automatic conflict resolution

**Preview Mode:**
```bash
# Dry run - see what would change
octodns-sync --config-file=config.yaml

# Apply changes
octodns-sync --config-file=config.yaml --doit
```

**Provider Support (15+):**
- AWS Route53
- Google Cloud DNS
- Azure DNS
- Cloudflare
- DigitalOcean
- NS1
- Dyn
- RFC2136 (BIND)
- And more...

### Strengths

✅ **Multi-provider** - Sync to multiple providers simultaneously
✅ **YAML-based** - Easy to read and write
✅ **Git-friendly** - Perfect for version control
✅ **Preview mode** - See changes before applying
✅ **Provider abstraction** - Write once, deploy anywhere

### Limitations

❌ **Python dependency** - Requires Python 3.7+
❌ **Manual sync** - Must run octodns-sync command
❌ **Complex setup** - More setup than external-dns
❌ **Learning curve** - YAML schema to learn

### When to Use

Use OctoDNS when:
- Managing DNS across multiple providers
- Need version control for DNS records
- Want preview mode before applying changes
- Migrating between DNS providers
- Multi-environment DNS (dev, staging, prod)

Skip OctoDNS when:
- Only using one provider (Terraform may be simpler)
- Prefer JavaScript over Python/YAML
- Need Kubernetes automation (use external-dns)

### Configuration Example

**Main Config (`octodns-config.yaml`):**
```yaml
---
providers:
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config
    default_ttl: 3600

  route53:
    class: octodns_route53.Route53Provider
    access_key_id: env/AWS_ACCESS_KEY_ID
    secret_access_key: env/AWS_SECRET_ACCESS_KEY

  cloudflare:
    class: octodns_cloudflare.CloudflareProvider
    token: env/CLOUDFLARE_TOKEN

zones:
  example.com.:
    sources:
      - config
    targets:
      - route53
      - cloudflare
```

**Zone Records (`config/example.com.yaml`):**
```yaml
---
# Root domain
'':
  - type: A
    ttl: 300
    values:
      - 192.0.2.1
      - 192.0.2.2
  - type: MX
    ttl: 3600
    values:
      - exchange: mail1.example.com.
        preference: 10
      - exchange: mail2.example.com.
        preference: 20

# Subdomains
www:
  type: CNAME
  ttl: 3600
  value: example.com.

api:
  type: A
  ttl: 300
  values:
    - 192.0.2.10

'_dmarc':
  type: TXT
  ttl: 3600
  value: "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

**Usage:**
```bash
# Install
pip install octodns octodns-route53 octodns-cloudflare

# Validate configuration
octodns-validate --config-file=octodns-config.yaml

# Preview changes (dry run)
octodns-sync --config-file=octodns-config.yaml

# Apply changes
octodns-sync --config-file=octodns-config.yaml --doit

# Sync specific zone
octodns-sync --config-file=octodns-config.yaml --doit example.com
```

### Best Practices

1. **Version control** - Commit config to Git
2. **CI/CD integration** - Automate sync on merge
3. **Preview first** - Always dry-run before --doit
4. **Environment variables** - Store credentials securely
5. **Separate environments** - Different configs for dev/staging/prod

### Common Issues

**Issue: Provider authentication failed**
```bash
# Check environment variables
echo $AWS_ACCESS_KEY_ID
echo $CLOUDFLARE_TOKEN

# Test provider access
octodns-validate --config-file=octodns-config.yaml
```

**Issue: Sync conflicts**
```bash
# OctoDNS detects manual changes in provider
# Solution: Sync from provider to config first
octodns-dump --config-file=octodns-config.yaml --output-dir=./backup

# Or force sync (overwrite provider)
octodns-sync --config-file=octodns-config.yaml --doit --force
```

---

## DNSControl

### Overview

JavaScript-based DNS-as-code tool with expressive DSL and multi-provider support.

**Repository:** `/stackexchange/dnscontrol`
**Language:** Go (runtime), JavaScript (config)
**License:** MIT
**Maturity:** Production-ready

**Trust Indicators:**
- Context7 Code Snippets: 649+
- Source Reputation: High
- Used by: StackExchange (at scale)
- GitHub Stars: 3k+

### Key Features

**JavaScript DSL:**
- Expressive configuration language
- Variables, functions, loops
- Reusable code patterns

**Preview Mode:**
```bash
# See what would change
dnscontrol preview

# Apply changes
dnscontrol push
```

**Provider Support (30+):**
- Largest provider support among DNS tools
- AWS Route53, Cloud DNS, Azure DNS, Cloudflare
- Many niche providers
- Custom providers via Go plugins

### Strengths

✅ **JavaScript DSL** - Familiar syntax, powerful logic
✅ **Most providers** - 30+ supported
✅ **Preview mode** - Safe dry-run
✅ **Helper functions** - DRY configuration
✅ **Large community** - Active development

### Limitations

❌ **Go runtime required** - Binary installation needed
❌ **JavaScript only** - Not YAML (preference)
❌ **Learning curve** - DSL to learn
❌ **Less Kubernetes-friendly** - Manual integration needed

### When to Use

Use DNSControl when:
- Comfortable with JavaScript
- Need complex DNS logic (functions, variables)
- Managing many similar domains
- Want most provider options
- Prefer expressive DSL over YAML

Skip DNSControl when:
- Prefer YAML configuration (use OctoDNS)
- Don't want JavaScript dependency
- Need Kubernetes automation (use external-dns)
- Want simpler setup (use Terraform)

### Configuration Example

**Main Config (`dnsconfig.js`):**
```javascript
var REG_NONE = NewRegistrar("none");
var DNS_CLOUDFLARE = NewDnsProvider("cloudflare");
var DNS_ROUTE53 = NewDnsProvider("route53");

// Helper function for standard web setup
function StandardWeb(domain, ip) {
  return [
    A("@", ip, TTL(300)),
    A("www", ip, TTL(300)),
    CNAME("blog", domain + "."),
  ];
}

// Helper function for Google Workspace email
function GoogleMail(domain) {
  return [
    MX("@", 1, "aspmx.l.google.com.", TTL(3600)),
    MX("@", 5, "alt1.aspmx.l.google.com."),
    MX("@", 5, "alt2.aspmx.l.google.com."),
    TXT("@", "v=spf1 include:_spf.google.com ~all"),
  ];
}

// Main domain - synced to both providers
D("example.com", REG_NONE,
  DnsProvider(DNS_CLOUDFLARE),
  DnsProvider(DNS_ROUTE53),

  // Use helper functions
  StandardWeb("example.com", "192.0.2.1"),
  GoogleMail("example.com"),

  // API endpoint
  A("api", "192.0.2.10", TTL(300)),

  // Certificate verification
  CAA("@", "issue", "letsencrypt.org"),
  CAA("@", "iodef", "mailto:security@example.com"),
);

// Staging environment
D("staging.example.com", REG_NONE,
  DnsProvider(DNS_CLOUDFLARE),

  A("@", "192.0.2.100", TTL(300)),
  A("*", "192.0.2.100", TTL(300)),  // Wildcard
);
```

**Credentials (`creds.json`):**
```json
{
  "cloudflare": {
    "TYPE": "CLOUDFLAREAPI",
    "accountid": "your-account-id",
    "apitoken": "your-api-token"
  },
  "route53": {
    "TYPE": "ROUTE53",
    "KeyId": "your-key-id",
    "SecretKey": "your-secret-key"
  }
}
```

**Usage:**
```bash
# Install
# macOS
brew install dnscontrol

# Linux
curl -L https://github.com/StackExchange/dnscontrol/releases/download/v3.x.x/dnscontrol-Linux -o dnscontrol
chmod +x dnscontrol

# Validate configuration
dnscontrol check

# Preview changes
dnscontrol preview

# Apply changes
dnscontrol push

# Push to specific provider
dnscontrol push --providers cloudflare
```

### Best Practices

1. **Use helper functions** - DRY configuration
2. **Variables for IPs** - Easy environment switching
3. **Git version control** - Track changes
4. **CI/CD integration** - Automate deployments
5. **Separate credentials** - Don't commit creds.json

### Advanced Examples

**Using Variables:**
```javascript
var IP_PROD = "192.0.2.1";
var IP_STAGING = "192.0.2.100";

D("example.com", REG_NONE, DnsProvider(DNS_CLOUDFLARE),
  A("@", IP_PROD),
  A("www", IP_PROD),
);

D("staging.example.com", REG_NONE, DnsProvider(DNS_CLOUDFLARE),
  A("@", IP_STAGING),
  A("www", IP_STAGING),
);
```

**Loop for Subdomains:**
```javascript
var subdomains = ["app1", "app2", "app3"];

D("example.com", REG_NONE, DnsProvider(DNS_CLOUDFLARE),
  ...subdomains.map(sub => A(sub, "192.0.2.1", TTL(300))),
);
```

---

## Terraform

### Overview

General-purpose infrastructure-as-code tool with DNS provider support.

**Benefits:**
- Manage DNS alongside other infrastructure
- State management (track changes)
- Plan/apply workflow
- Strong typing

**Providers:**
- aws (Route53)
- google (Cloud DNS)
- azurerm (Azure DNS)
- cloudflare (Cloudflare)
- 100+ other providers

### When to Use Terraform

Use Terraform when:
- Already using Terraform for infrastructure
- Want state management
- Need to manage DNS + compute + storage together
- Prefer HCL over YAML/JavaScript

Skip Terraform when:
- Only managing DNS (OctoDNS/DNSControl lighter)
- Need Kubernetes automation (use external-dns)
- Don't want state file management

### Example

```hcl
# Route53 zone
resource "aws_route53_zone" "main" {
  name = "example.com"
}

# A record
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.example.com"
  type    = "A"
  ttl     = 300
  records = ["192.0.2.1"]
}

# MX records
resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "MX"
  ttl     = 3600
  records = [
    "10 mail1.example.com",
    "20 mail2.example.com",
  ]
}
```

---

## Comparison Matrix

### Feature Comparison

| Feature | external-dns | OctoDNS | DNSControl | Terraform |
|---------|--------------|---------|------------|-----------|
| **Language** | Go | Python/YAML | JavaScript | HCL |
| **Config Format** | K8s annotations | YAML | JavaScript | HCL |
| **Preview Mode** | ❌ | ✅ | ✅ | ✅ (plan) |
| **Multi-Provider** | ✅ (separate) | ✅ (native) | ✅ (native) | ✅ (modules) |
| **Kubernetes** | ✅ Native | ❌ | ❌ | ⚠️ Possible |
| **Learning Curve** | Low | Medium | Medium | Medium-High |
| **Provider Count** | 20+ | 15+ | 30+ | 100+ |
| **State Management** | K8s objects | No | No | ✅ State file |
| **Version Control** | K8s manifests | YAML files | JS files | HCL files |
| **Automation** | Automatic | Manual sync | Manual push | Manual apply |

### Strengths and Weaknesses

| Tool | Best For | Avoid If |
|------|----------|----------|
| **external-dns** | Kubernetes DNS automation | Not using Kubernetes |
| **OctoDNS** | Multi-provider sync, YAML preference | Prefer JavaScript, complex logic |
| **DNSControl** | Complex logic, many providers | Prefer YAML, simpler setup |
| **Terraform** | Infrastructure + DNS together | Only managing DNS |

---

## Selection Guide

### Decision Flow

```
Are you using Kubernetes?
├─ Yes → external-dns (if only K8s DNS needs)
│        or Terraform (if managing infrastructure too)
└─ No  → Continue...

Managing multiple DNS providers?
├─ Yes → OctoDNS or DNSControl
└─ No  → Continue...

Already using Terraform?
├─ Yes → Terraform (manage DNS with infrastructure)
└─ No  → Continue...

Prefer YAML or JavaScript?
├─ YAML → OctoDNS
└─ JavaScript → DNSControl
```

### By Use Case

**Use Case 1: Kubernetes Services**
```
Best: external-dns
Why: Automatic, annotation-based, Kubernetes-native
Alternative: Terraform + external-dns (for non-K8s DNS)
```

**Use Case 2: Multi-Provider Redundancy**
```
Best: OctoDNS or DNSControl
Why: Native multi-provider sync
Example: Sync same zone to Route53 + Cloudflare
```

**Use Case 3: Infrastructure + DNS**
```
Best: Terraform
Why: Manage compute, network, DNS together
Example: Create EC2 + Route53 record in one apply
```

**Use Case 4: Complex DNS Logic**
```
Best: DNSControl
Why: JavaScript functions, variables, loops
Example: Generate 100 subdomains programmatically
```

**Use Case 5: DNS Migration**
```
Best: OctoDNS
Why: Export from old provider, sync to new
Example: Migrate from GoDaddy to Cloudflare
```

### Combination Strategies

**Strategy 1: Kubernetes + Non-Kubernetes**
```
external-dns: Automatic K8s Service/Ingress DNS
OctoDNS:      Static DNS records (MX, TXT, etc.)
```

**Strategy 2: Infrastructure + Dynamic DNS**
```
Terraform:    Zones, static records, infrastructure
external-dns: Dynamic K8s workload DNS
```

**Strategy 3: Multi-Environment**
```
DNSControl: Dev and staging zones
Terraform:  Production zone (with infrastructure)
```

---

## Summary

### Quick Recommendations

**Choose external-dns if:**
- Running Kubernetes
- Want automatic DNS for Services/Ingresses
- Prefer zero manual management

**Choose OctoDNS if:**
- Managing multiple DNS providers
- Prefer YAML configuration
- Need version control and preview mode

**Choose DNSControl if:**
- Comfortable with JavaScript
- Need complex DNS logic
- Want most provider options

**Choose Terraform if:**
- Already using Terraform
- Managing infrastructure + DNS together
- Want state management

### Can't Decide?

**Start simple:**
1. Kubernetes → external-dns
2. Static DNS → OctoDNS (YAML) or DNSControl (JavaScript)
3. Infrastructure → Terraform

**Grow as needed:**
- Combine tools for different use cases
- Migrate between tools with export/import
- All support Git version control
