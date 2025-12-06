# Access Control Compliance Policies
#
# Validates IAM, RBAC, and authentication requirements
# Control IDs: MFA-001, RBAC-001, ACCESS-001, ACCESS-002

package compliance.access_control

# METADATA
# title: Access Control and Authentication
# description: Enforce MFA, RBAC, and least privilege access
# frameworks:
#   - SOC 2 (CC6.1, CC6.2, CC6.3)
#   - HIPAA (§164.312(a)(2)(i), §164.312(d))
#   - PCI-DSS (Req 7.1, Req 8.3)
#   - GDPR (Article 32)

# ============================================================================
# IAM Policy - Wildcard Resource Restrictions
# ============================================================================

# Deny overly broad IAM policies with wildcard resources
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_iam_policy"
  policy := json.unmarshal(resource.change.after.policy)
  statement := policy.Statement[_]
  statement.Effect == "Allow"
  statement.Resource == "*"
  not is_allowed_wildcard_action(statement)

  actions := array_or_string_to_array(statement.Action)
  msg := sprintf(
    "HIGH [ACCESS-001]: IAM policy '%s' grants overly broad permissions\n  Resource: '*'\n  Actions: %v\n  Frameworks: SOC2-CC6.2, PCI-DSS-Req7.1\n  Action: Use specific resource ARNs or allowed wildcard actions",
    [resource.address, actions]
  )
}

# Allow specific read-only wildcard actions
is_allowed_wildcard_action(statement) {
  actions := array_or_string_to_array(statement.Action)
  allowed_prefixes := [
    "s3:List",
    "s3:Get",
    "ec2:Describe",
    "cloudwatch:Get",
    "cloudwatch:List",
    "logs:Describe",
    "iam:Get",
    "iam:List"
  ]
  action := actions[_]
  startswith(action, allowed_prefixes[_])
}

# Helper to convert string or array to array
array_or_string_to_array(value) = result {
  is_array(value)
  result := value
}
array_or_string_to_array(value) = result {
  is_string(value)
  result := [value]
}

# ============================================================================
# IAM Role - MFA Requirements
# ============================================================================

# Require MFA for privileged roles
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_iam_role"
  is_privileged_role(resource)
  policy := json.unmarshal(resource.change.after.assume_role_policy)
  not requires_mfa(policy)

  msg := sprintf(
    "CRITICAL [MFA-001]: Privileged role '%s' must require MFA\n  Frameworks: SOC2-CC6.1, HIPAA-164.312(d), PCI-DSS-Req8.3\n  Action: Add MFA condition to assume role policy",
    [resource.address]
  )
}

# Check if role name indicates privileged access
is_privileged_role(resource) {
  privileged_keywords := ["admin", "power", "elevated", "root", "superuser"]
  role_name := lower(resource.name)
  contains(role_name, privileged_keywords[_])
}

# Check if policy requires MFA
requires_mfa(policy) {
  statement := policy.Statement[_]
  statement.Condition.Bool["aws:MultiFactorAuthPresent"] == "true"
}

requires_mfa(policy) {
  statement := policy.Statement[_]
  statement.Condition.BoolIfExists["aws:MultiFactorAuthPresent"] == "true"
}

# ============================================================================
# IAM User - Prevent Console Access Without MFA
# ============================================================================

# Prevent IAM users from accessing console without MFA policy
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_iam_user"
  not has_mfa_enforcement_policy(resource.address)

  msg := sprintf(
    "HIGH [MFA-001]: IAM user '%s' should have MFA enforcement policy attached\n  Frameworks: PCI-DSS-Req8.3, SOC2-CC6.1\n  Action: Attach IAM policy that denies actions without MFA",
    [resource.address]
  )
}

# Check if user has MFA enforcement policy
has_mfa_enforcement_policy(user_address) {
  resource := input.resource_changes[_]
  resource.type == "aws_iam_user_policy_attachment"
  startswith(resource.address, user_address)
  policy_arn := resource.change.after.policy_arn
  contains(policy_arn, "RequireMFA")
}

# ============================================================================
# Security Group Rules - Ingress Restrictions
# ============================================================================

# Deny security groups open to the internet on non-standard ports
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.type == "ingress"
  is_open_to_internet(resource)
  not is_allowed_public_port(resource.change.after.from_port)

  msg := sprintf(
    "HIGH [NET-001]: Security group rule '%s' allows ingress from 0.0.0.0/0 on port %d\n  Frameworks: PCI-DSS-Req1.3, SOC2-CC6.6\n  Action: Restrict source to specific IP ranges or use approved ports only (80, 443)",
    [resource.address, resource.change.after.from_port]
  )
}

is_open_to_internet(resource) {
  cidr_blocks := resource.change.after.cidr_blocks
  cidr_blocks[_] == "0.0.0.0/0"
}

is_open_to_internet(resource) {
  ipv6_cidr_blocks := resource.change.after.ipv6_cidr_blocks
  ipv6_cidr_blocks[_] == "::/0"
}

is_allowed_public_port(port) {
  allowed_ports := [80, 443]
  port == allowed_ports[_]
}

# Deny SSH (22) and RDP (3389) open to internet
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.type == "ingress"
  is_open_to_internet(resource)
  port := resource.change.after.from_port
  is_management_port(port)

  msg := sprintf(
    "CRITICAL [NET-001]: Security group rule '%s' exposes management port %d to the internet\n  Frameworks: PCI-DSS-Req1.3, HIPAA-164.312(a)(2)(ii)\n  Action: Restrict SSH/RDP access to VPN or bastion host IP ranges",
    [resource.address, port]
  )
}

is_management_port(port) {
  management_ports := [22, 3389]
  port == management_ports[_]
}

# ============================================================================
# S3 Bucket - Public Access
# ============================================================================

# Require S3 public access block
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not has_public_access_block(resource.address)

  msg := sprintf(
    "CRITICAL [ACCESS-001]: S3 bucket '%s' must have public access block configured\n  Frameworks: SOC2-CC6.1, HIPAA-164.312(a)(2)(i), PCI-DSS-Req7.1\n  Action: Add aws_s3_bucket_public_access_block resource",
    [resource.address]
  )
}

has_public_access_block(bucket_address) {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_public_access_block"
  startswith(resource.address, bucket_address)
  after := resource.change.after
  after.block_public_acls == true
  after.block_public_policy == true
  after.ignore_public_acls == true
  after.restrict_public_buckets == true
}

# ============================================================================
# Kubernetes RBAC (if applicable)
# ============================================================================

# Deny ClusterRoleBindings granting cluster-admin to service accounts
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "kubernetes_cluster_role_binding"
  resource.change.after.role_ref.name == "cluster-admin"
  subject := resource.change.after.subject[_]
  subject.kind == "ServiceAccount"

  msg := sprintf(
    "CRITICAL [RBAC-001]: ClusterRoleBinding '%s' grants cluster-admin to ServiceAccount '%s'\n  Frameworks: SOC2-CC6.2, PCI-DSS-Req7.1\n  Action: Use least privilege roles instead of cluster-admin",
    [resource.address, subject.name]
  )
}

# Require approval annotation for production namespace access
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "kubernetes_role_binding"
  resource.change.after.metadata[_].namespace == "production"
  annotations := resource.change.after.metadata[_].annotations
  not annotations["approved-by"]

  msg := sprintf(
    "HIGH [ACCESS-002]: Production RoleBinding '%s' requires 'approved-by' annotation\n  Frameworks: SOC2-CC6.3\n  Action: Add 'approved-by' annotation with approver name",
    [resource.address]
  )
}

# Deny wildcard verbs in production namespace
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "kubernetes_role"
  resource.change.after.metadata[_].namespace == "production"
  rule := resource.change.after.rule[_]
  verb := rule.verbs[_]
  verb == "*"

  msg := sprintf(
    "HIGH [RBAC-001]: Production Role '%s' uses wildcard verbs\n  Frameworks: PCI-DSS-Req7.1.2\n  Action: Specify explicit verbs (get, list, watch, create, update, delete)",
    [resource.address]
  )
}

# ============================================================================
# Database Access Controls
# ============================================================================

# Require RDS IAM authentication
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  resource.change.after.iam_database_authentication_enabled != true

  msg := sprintf(
    "HIGH [ACCESS-001]: RDS instance '%s' should enable IAM database authentication\n  Frameworks: SOC2-CC6.1, HIPAA-164.312(a)(2)(i)\n  Action: Set iam_database_authentication_enabled = true",
    [resource.address]
  )
}

# Deny publicly accessible databases
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  resource.change.after.publicly_accessible == true

  msg := sprintf(
    "CRITICAL [NET-002]: RDS instance '%s' must not be publicly accessible\n  Frameworks: PCI-DSS-Req1.3, HIPAA-164.312(a)(2)(ii)\n  Action: Set publicly_accessible = false",
    [resource.address]
  )
}

# ============================================================================
# Lambda Function Access
# ============================================================================

# Deny Lambda functions with overly permissive execution roles
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_lambda_function"
  role_arn := resource.change.after.role
  is_overly_permissive_lambda_role(role_arn)

  msg := sprintf(
    "HIGH [ACCESS-001]: Lambda function '%s' execution role may be overly permissive\n  Frameworks: SOC2-CC6.2, PCI-DSS-Req7.1\n  Action: Review and restrict IAM role permissions",
    [resource.address]
  )
}

is_overly_permissive_lambda_role(role_arn) {
  # Check for common overly permissive patterns
  # This is a simplified check; thorough validation requires role policy inspection
  overly_permissive_names := ["admin", "poweruser", "full"]
  role_name := lower(role_arn)
  contains(role_name, overly_permissive_names[_])
}

# ============================================================================
# ECS/EKS Task Execution Roles
# ============================================================================

# Deny ECS task definitions with privileged containers
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_ecs_task_definition"
  container := json.unmarshal(resource.change.after.container_definitions)[_]
  container.privileged == true

  msg := sprintf(
    "CRITICAL [ACCESS-001]: ECS task '%s' uses privileged container '%s'\n  Frameworks: PCI-DSS-Req7.1, SOC2-CC6.2\n  Action: Remove privileged flag or add strong justification",
    [resource.address, container.name]
  )
}

# ============================================================================
# Summary Functions
# ============================================================================

# Count access control violations by framework
violations_by_framework[framework] = count {
  framework := ["SOC2", "HIPAA", "PCI-DSS", "GDPR"][_]
  violations := [msg | msg := deny[_]; contains(msg, framework)]
  count := count(violations)
}

# List all access control violations
access_violations[violation] {
  violation := deny[_]
}
