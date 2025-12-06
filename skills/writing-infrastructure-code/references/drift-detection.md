# Drift Detection and Remediation

Detecting and remediating infrastructure drift - when actual cloud resources diverge from infrastructure code.

## What is Drift?

Drift occurs when cloud resources are modified outside of infrastructure as code:
- Manual changes via cloud console
- Direct API/CLI modifications
- Third-party tools making changes
- Emergency hotfixes bypassing IaC

## Drift Detection Methods

### Terraform Drift Detection

```bash
# Detect drift with exit codes
terraform plan -detailed-exitcode

# Exit codes:
# 0 - No changes (no drift)
# 1 - Error
# 2 - Changes needed (drift detected)
```

### Pulumi Drift Detection

```bash
# Preview changes to detect drift
pulumi preview --diff

# Refresh state
pulumi refresh
```

### Automated Drift Detection

```bash
# Schedule drift checks (cron example)
0 */6 * * * cd /path/to/infra && ./drift-check.sh >> drift.log 2>&1
```

## Drift Remediation

### Option 1: Apply Code (Recommended)

```bash
# Bring infrastructure back to desired state
terraform apply

# Or for Pulumi
pulumi up
```

### Option 2: Update Code to Match Reality

```bash
# Update state to match current infrastructure
terraform apply -refresh-only

# Review and accept changes
terraform plan

# Or for Pulumi
pulumi refresh --yes
```

### Option 3: Import Manual Changes

```bash
# Import manually created resource
terraform import aws_vpc.main vpc-12345678
```

## Prevention Strategies

- Enable CloudTrail/audit logging
- Use IAM policies to restrict manual changes
- Implement policy-as-code (OPA, Sentinel)
- Regular drift detection schedules
- Team training on IaC workflows
