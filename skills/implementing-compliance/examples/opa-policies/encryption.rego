# Encryption Compliance Policies
#
# Validates encryption requirements across SOC 2, HIPAA, PCI-DSS, and GDPR
# Control IDs: ENC-001 (at rest), ENC-002 (in transit), ENC-003 (key rotation)

package compliance.encryption

# METADATA
# title: Encryption at Rest
# description: Ensure all data stores use encryption at rest with KMS
# frameworks:
#   - SOC 2 (CC6.1, CC6.7)
#   - HIPAA (§164.312(a)(2)(iv))
#   - PCI-DSS (Req 3.4)
#   - GDPR (Article 32(1)(a))
# control_id: ENC-001
# severity: CRITICAL

# ============================================================================
# S3 Bucket Encryption
# ============================================================================

# Deny S3 buckets without encryption configuration
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not has_bucket_encryption(resource.address)

  msg := sprintf(
    "CRITICAL [ENC-001]: S3 bucket '%s' must have encryption enabled\n  Frameworks: SOC2-CC6.1, HIPAA-164.312(a)(2)(iv), PCI-DSS-Req3.4, GDPR-Art32\n  Action: Add aws_s3_bucket_server_side_encryption_configuration resource",
    [resource.address]
  )
}

# Check if bucket has encryption configuration
has_bucket_encryption(bucket_address) {
  encryption_resource := input.resource_changes[_]
  encryption_resource.type == "aws_s3_bucket_server_side_encryption_configuration"
  startswith(encryption_resource.address, bucket_address)
}

# Require KMS encryption (not default S3 AES256)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_server_side_encryption_configuration"
  rule := resource.change.after.rule[_]
  encryption := rule.apply_server_side_encryption_by_default
  encryption.sse_algorithm == "AES256"  # Default S3 encryption

  msg := sprintf(
    "HIGH [ENC-001]: Bucket '%s' must use aws:kms encryption, not default AES256\n  Frameworks: SOC2-CC6.7\n  Action: Change sse_algorithm to 'aws:kms' and specify kms_master_key_id",
    [resource.address]
  )
}

# ============================================================================
# RDS Encryption
# ============================================================================

# Deny unencrypted RDS instances
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  resource.change.after.storage_encrypted != true

  msg := sprintf(
    "CRITICAL [ENC-001]: RDS instance '%s' must enable storage_encrypted\n  Frameworks: HIPAA-164.312(a)(2)(iv), PCI-DSS-Req3.4\n  Action: Set storage_encrypted = true and specify kms_key_id",
    [resource.address]
  )
}

# Deny unencrypted RDS clusters (Aurora)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_rds_cluster"
  resource.change.after.storage_encrypted != true

  msg := sprintf(
    "CRITICAL [ENC-001]: RDS cluster '%s' must enable storage_encrypted\n  Frameworks: HIPAA-164.312(a)(2)(iv), PCI-DSS-Req3.4\n  Action: Set storage_encrypted = true and specify kms_key_id",
    [resource.address]
  )
}

# ============================================================================
# DynamoDB Encryption
# ============================================================================

# Deny DynamoDB tables without encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_dynamodb_table"
  not has_dynamodb_encryption(resource)

  msg := sprintf(
    "CRITICAL [ENC-001]: DynamoDB table '%s' must have server-side encryption enabled\n  Frameworks: SOC2-CC6.1, HIPAA-164.312(a)(2)(iv)\n  Action: Add server_side_encryption block with enabled = true",
    [resource.address]
  )
}

has_dynamodb_encryption(resource) {
  resource.change.after.server_side_encryption[_].enabled == true
}

# Require customer-managed KMS keys for DynamoDB
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_dynamodb_table"
  encryption := resource.change.after.server_side_encryption[_]
  encryption.enabled == true
  not encryption.kms_key_arn  # Using AWS-managed key

  msg := sprintf(
    "HIGH [ENC-001]: DynamoDB table '%s' should use customer-managed KMS key\n  Frameworks: SOC2-CC6.7\n  Action: Specify kms_key_arn in server_side_encryption block",
    [resource.address]
  )
}

# ============================================================================
# EBS Volume Encryption
# ============================================================================

# Deny unencrypted EBS volumes
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_ebs_volume"
  resource.change.after.encrypted != true

  msg := sprintf(
    "CRITICAL [ENC-001]: EBS volume '%s' must be encrypted\n  Frameworks: HIPAA-164.312(a)(2)(iv), PCI-DSS-Req3.4\n  Action: Set encrypted = true and specify kms_key_id",
    [resource.address]
  )
}

# Require EBS encryption by default
deny[msg] {
  not has_ebs_default_encryption

  msg := "CRITICAL [ENC-001]: EBS encryption by default must be enabled\n  Frameworks: HIPAA-164.312(a)(2)(iv)\n  Action: Add aws_ebs_encryption_by_default resource with enabled = true"
}

has_ebs_default_encryption {
  resource := input.resource_changes[_]
  resource.type == "aws_ebs_encryption_by_default"
  resource.change.after.enabled == true
}

# ============================================================================
# EFS File System Encryption
# ============================================================================

# Deny unencrypted EFS file systems
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_efs_file_system"
  resource.change.after.encrypted != true

  msg := sprintf(
    "CRITICAL [ENC-001]: EFS file system '%s' must be encrypted\n  Frameworks: HIPAA-164.312(a)(2)(iv)\n  Action: Set encrypted = true and specify kms_key_id",
    [resource.address]
  )
}

# ============================================================================
# KMS Key Management
# ============================================================================

# Require KMS key rotation (PCI-DSS Req 3.6)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_kms_key"
  resource.change.after.enable_key_rotation != true

  msg := sprintf(
    "MEDIUM [ENC-003]: KMS key '%s' must have automatic rotation enabled\n  Frameworks: PCI-DSS-Req3.6, SOC2-CC6.7\n  Action: Set enable_key_rotation = true",
    [resource.address]
  )
}

# Require reasonable deletion window (min 7 days)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_kms_key"
  deletion_window := resource.change.after.deletion_window_in_days
  deletion_window < 7

  msg := sprintf(
    "MEDIUM [ENC-003]: KMS key '%s' deletion window must be at least 7 days (current: %d)\n  Frameworks: SOC2-CC6.7\n  Action: Set deletion_window_in_days >= 7 (recommended: 30)",
    [resource.address, deletion_window]
  )
}

# ============================================================================
# CloudWatch Logs Encryption
# ============================================================================

# Require encryption for CloudWatch log groups
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_cloudwatch_log_group"
  not resource.change.after.kms_key_id

  msg := sprintf(
    "HIGH [ENC-001]: CloudWatch log group '%s' should be encrypted with KMS\n  Frameworks: SOC2-CC6.1, HIPAA-164.312(a)(2)(iv)\n  Action: Specify kms_key_id",
    [resource.address]
  )
}

# ============================================================================
# SNS Topic Encryption
# ============================================================================

# Require SNS topic encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_sns_topic"
  not resource.change.after.kms_master_key_id

  msg := sprintf(
    "HIGH [ENC-001]: SNS topic '%s' should be encrypted with KMS\n  Frameworks: HIPAA-164.312(a)(2)(iv)\n  Action: Specify kms_master_key_id",
    [resource.address]
  )
}

# ============================================================================
# SQS Queue Encryption
# ============================================================================

# Require SQS queue encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_sqs_queue"
  not resource.change.after.kms_master_key_id

  msg := sprintf(
    "HIGH [ENC-001]: SQS queue '%s' should be encrypted with KMS\n  Frameworks: HIPAA-164.312(a)(2)(iv)\n  Action: Specify kms_master_key_id",
    [resource.address]
  )
}

# ============================================================================
# Secrets Manager Encryption
# ============================================================================

# Require Secrets Manager encryption with KMS
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_secretsmanager_secret"
  not resource.change.after.kms_key_id

  msg := sprintf(
    "HIGH [ENC-001]: Secrets Manager secret '%s' should use customer-managed KMS key\n  Frameworks: SOC2-CC6.7, PCI-DSS-Req3.4\n  Action: Specify kms_key_id",
    [resource.address]
  )
}

# ============================================================================
# Encryption in Transit (TLS)
# ============================================================================

# METADATA
# control_id: ENC-002
# severity: CRITICAL

# Require TLS 1.3 for ALB listeners (PCI-DSS 4.0)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_lb_listener"
  resource.change.after.protocol == "HTTPS"
  ssl_policy := resource.change.after.ssl_policy
  not is_tls13_policy(ssl_policy)

  msg := sprintf(
    "CRITICAL [ENC-002]: ALB listener '%s' must use TLS 1.3 policy\n  Frameworks: PCI-DSS-Req4.1, HIPAA-164.312(e)(1)\n  Action: Set ssl_policy to 'ELBSecurityPolicy-TLS13-1-2-2021-06'",
    [resource.address]
  )
}

is_tls13_policy(policy) {
  tls13_policies := [
    "ELBSecurityPolicy-TLS13-1-2-2021-06",
    "ELBSecurityPolicy-TLS13-1-3-2021-06"
  ]
  policy == tls13_policies[_]
}

# Require RDS SSL enforcement
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  not has_ssl_enforcement(resource)

  msg := sprintf(
    "HIGH [ENC-002]: RDS instance '%s' should enforce SSL connections\n  Frameworks: HIPAA-164.312(e)(1), PCI-DSS-Req4.1\n  Action: Set parameter group with rds.force_ssl = 1",
    [resource.address]
  )
}

has_ssl_enforcement(resource) {
  # Check if using a parameter group with SSL enforcement
  # This is a simplified check; full validation requires parameter group inspection
  resource.change.after.parameter_group_name
}

# Require ElastiCache in-transit encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_elasticache_replication_group"
  resource.change.after.transit_encryption_enabled != true

  msg := sprintf(
    "CRITICAL [ENC-002]: ElastiCache replication group '%s' must enable in-transit encryption\n  Frameworks: HIPAA-164.312(e)(1), PCI-DSS-Req4.1\n  Action: Set transit_encryption_enabled = true",
    [resource.address]
  )
}

# ============================================================================
# Summary Functions
# ============================================================================

# Count violations by severity
violation_count[severity] = count {
  severity := ["CRITICAL", "HIGH", "MEDIUM", "LOW"][_]
  violations := [msg | msg := deny[_]; contains(msg, severity)]
  count := count(violations)
}

# List all encryption violations
encryption_violations[violation] {
  violation := deny[_]
}
