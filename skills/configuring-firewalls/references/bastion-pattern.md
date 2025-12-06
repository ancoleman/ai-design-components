# Bastion Host Pattern

A bastion host (jump box) is a hardened server that provides secure access to private instances in a network.


## Table of Contents

- [Architecture](#architecture)
- [UFW Configuration (Bastion Host)](#ufw-configuration-bastion-host)
- [UFW Configuration (Private Instances)](#ufw-configuration-private-instances)
- [AWS Security Groups](#aws-security-groups)
  - [Bastion Security Group](#bastion-security-group)
  - [Private Instance Security Group](#private-instance-security-group)
- [Connecting Through Bastion](#connecting-through-bastion)
  - [Manual SSH Jump](#manual-ssh-jump)
  - [SSH ProxyJump (Recommended)](#ssh-proxyjump-recommended)
  - [SSH Agent Forwarding (Not Recommended)](#ssh-agent-forwarding-not-recommended)
  - [SCP Through Bastion](#scp-through-bastion)
- [Hardening the Bastion Host](#hardening-the-bastion-host)
  - [OS-Level Hardening](#os-level-hardening)
  - [SSH Configuration (/etc/ssh/sshd_config)](#ssh-configuration-etcsshsshd_config)
  - [Monitoring and Auditing](#monitoring-and-auditing)
  - [CloudWatch Alarms (AWS)](#cloudwatch-alarms-aws)
- [Terraform Complete Example](#terraform-complete-example)
- [Alternative: AWS Systems Manager Session Manager](#alternative-aws-systems-manager-session-manager)
- [Best Practices Summary](#best-practices-summary)
- [Troubleshooting](#troubleshooting)

## Architecture

```
Internet
    │
    └─ Public Subnet
        └─ Bastion Host (Single Entry Point)
            │
            └─ Private Subnet(s)
                ├─ App Server 1
                ├─ App Server 2
                └─ Database Server
```

**Key Principles:**
- Single hardened entry point for administrative access
- Bastion in public subnet with public IP
- Private instances in private subnets (no public IPs)
- SSH from private instances only via bastion
- Heavily monitored and audited

## UFW Configuration (Bastion Host)

```bash
# On bastion host
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH from office/VPN only (NOT 0.0.0.0/0)
sudo ufw allow from 203.0.113.0/24 to any port 22

# Or specific IPs
sudo ufw allow from 203.0.113.10 to any port 22
sudo ufw allow from 203.0.113.20 to any port 22

# Rate limit SSH (prevent brute force)
sudo ufw limit ssh

# Enable logging
sudo ufw logging on

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status verbose
```

## UFW Configuration (Private Instances)

```bash
# On private app/database servers
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH from bastion only (use bastion's private IP)
sudo ufw allow from 10.0.1.5 to any port 22

# Allow application-specific ports from appropriate sources
# Example for web server:
sudo ufw allow from 10.0.0.0/16 to any port 80  # Internal traffic only

# Enable
sudo ufw enable
```

## AWS Security Groups

### Bastion Security Group

```hcl
resource "aws_security_group" "bastion" {
  name        = "bastion-sg"
  description = "Security group for bastion host"
  vpc_id      = aws_vpc.main.id

  # Inbound: SSH from office/VPN only
  ingress {
    description = "SSH from office"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.office_ip_ranges  # ["203.0.113.0/24"]
  }

  # Outbound: SSH to private instances
  egress {
    description = "SSH to VPC instances"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  # Outbound: HTTPS for updates
  egress {
    description = "HTTPS for package updates"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: DNS
  egress {
    description = "DNS"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "bastion-sg"
    Environment = var.environment
  }
}
```

### Private Instance Security Group

```hcl
resource "aws_security_group" "private_instance" {
  name        = "private-instance-sg"
  description = "Security group for private instances (SSH via bastion)"
  vpc_id      = aws_vpc.main.id

  # Inbound: SSH from bastion only
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]  # Reference bastion SG
  }

  # Inbound: Application-specific ports
  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  # Outbound: All (or restrict as needed)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "private-instance-sg"
    Environment = var.environment
  }
}
```

## Connecting Through Bastion

### Manual SSH Jump

```bash
# Two-step SSH
ssh -i bastion-key.pem ec2-user@bastion-public-ip
# Then from bastion:
ssh -i private-key.pem ec2-user@private-instance-ip
```

### SSH ProxyJump (Recommended)

```bash
# Single command
ssh -J ec2-user@bastion-public-ip ec2-user@private-instance-ip

# Or configure in ~/.ssh/config
Host bastion
    HostName bastion-public-ip
    User ec2-user
    IdentityFile ~/.ssh/bastion-key.pem

Host private-*
    User ec2-user
    IdentityFile ~/.ssh/private-key.pem
    ProxyJump bastion

# Then simply:
ssh private-app-server-ip
```

### SSH Agent Forwarding (Not Recommended)

```bash
# Forward SSH agent (security risk - avoid if possible)
ssh -A ec2-user@bastion-public-ip
```

**Why Not Recommended:**
- Forwarded agent can be hijacked if bastion compromised
- Use ProxyJump instead

### SCP Through Bastion

```bash
# Copy file to private instance via bastion
scp -o ProxyJump=ec2-user@bastion-public-ip \
    local-file.txt ec2-user@private-instance-ip:/home/ec2-user/

# Copy from private instance
scp -o ProxyJump=ec2-user@bastion-public-ip \
    ec2-user@private-instance-ip:/var/log/app.log ./
```

## Hardening the Bastion Host

### OS-Level Hardening

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install fail2ban (block brute force)
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Disable password authentication (key-only)
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Restart SSH
sudo systemctl restart sshd

# Enable automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### SSH Configuration (/etc/ssh/sshd_config)

```bash
# Best practices for bastion
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server

# Limit SSH users (optional)
AllowUsers ec2-user admin

# Use strong ciphers only
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
```

### Monitoring and Auditing

```bash
# Enable auditd
sudo apt install auditd
sudo systemctl enable auditd
sudo systemctl start auditd

# Monitor SSH logins
sudo tail -f /var/log/auth.log

# CloudWatch Logs (AWS)
# Install CloudWatch agent and configure to ship:
# - /var/log/auth.log (SSH attempts)
# - /var/log/fail2ban.log (blocked IPs)
# - /var/log/ufw.log (firewall logs)
```

### CloudWatch Alarms (AWS)

```hcl
resource "aws_cloudwatch_log_metric_filter" "bastion_ssh_failed" {
  name           = "bastion-ssh-failed-attempts"
  log_group_name = aws_cloudwatch_log_group.bastion.name
  pattern        = "[Mon, day, timestamp, ip, id, msg1 = Failed, msg2 = password, ...]"

  metric_transformation {
    name      = "SSHFailedLoginAttempts"
    namespace = "Bastion"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "bastion_ssh_failed" {
  alarm_name          = "bastion-ssh-failed-attempts"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "SSHFailedLoginAttempts"
  namespace           = "Bastion"
  period              = "300"  # 5 minutes
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "Alert on multiple failed SSH attempts"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

## Terraform Complete Example

```hcl
# Bastion host EC2 instance
resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.bastion.id]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.bastion.key_name

  user_data = <<-EOF
              #!/bin/bash
              apt update
              apt upgrade -y
              apt install -y fail2ban ufw

              # Configure UFW
              ufw default deny incoming
              ufw default allow outgoing
              ufw allow from ${var.office_cidr} to any port 22
              ufw limit ssh
              ufw enable

              # Configure fail2ban
              systemctl enable fail2ban
              systemctl start fail2ban
              EOF

  tags = {
    Name        = "bastion-host"
    Environment = var.environment
    Role        = "bastion"
  }

  monitoring = true  # Enable detailed CloudWatch monitoring
}

# Elastic IP for bastion (static IP)
resource "aws_eip" "bastion" {
  instance = aws_instance.bastion.id
  domain   = "vpc"

  tags = {
    Name = "bastion-eip"
  }
}
```

## Alternative: AWS Systems Manager Session Manager

Instead of bastion host, use AWS SSM Session Manager:

**Advantages:**
- No public IP needed on bastion
- No SSH keys to manage
- Built-in audit logging
- Port forwarding support
- No inbound firewall rules

**Setup:**

```hcl
# IAM role for EC2 instances
resource "aws_iam_role" "ssm" {
  name = "ec2-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.ssm.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Attach to instances
resource "aws_iam_instance_profile" "ssm" {
  name = "ec2-ssm-profile"
  role = aws_iam_role.ssm.name
}

resource "aws_instance" "private" {
  # ... other config
  iam_instance_profile = aws_iam_instance_profile.ssm.name
}
```

**Connect:**

```bash
# Install AWS CLI and Session Manager plugin
# https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

# Connect to instance
aws ssm start-session --target i-1234567890abcdef0

# Port forwarding
aws ssm start-session --target i-1234567890abcdef0 \
    --document-name AWS-StartPortForwardingSession \
    --parameters '{"portNumber":["22"],"localPortNumber":["9999"]}'

# Then SSH via localhost:9999
ssh -i private-key.pem ec2-user@localhost -p 9999
```

## Best Practices Summary

1. **Limit Access** - Bastion accessible from office/VPN only (never 0.0.0.0/0)
2. **Key-Based Auth Only** - Disable password authentication
3. **Rate Limiting** - Use UFW limit or fail2ban
4. **Monitoring** - CloudWatch Logs + Alarms for failed attempts
5. **Hardening** - Disable root, strong SSH ciphers, automatic updates
6. **Minimal Bastion** - No application code, minimal packages
7. **Audit Logging** - Ship all logs to centralized logging (CloudWatch, Splunk)
8. **Regular Updates** - Automated security patches
9. **Use Session Manager** - Consider SSM Session Manager for bastion-less access
10. **Multiple Availability Zones** - Deploy bastion in multiple AZs for HA

## Troubleshooting

**Can't SSH to bastion:**
- Check Security Group allows SSH from your IP
- Verify bastion has public IP
- Check NACL allows SSH inbound + ephemeral ports outbound
- Verify SSH key is correct

**Can't SSH from bastion to private instance:**
- Check private instance SG allows SSH from bastion SG
- Verify bastion can reach private subnet (route table)
- Ensure SSH key for private instance is available
- Check private instance NACL allows SSH

**Locked out of bastion:**
- Use EC2 Instance Connect (if enabled)
- Use AWS Systems Manager Session Manager
- Last resort: Stop instance, detach root volume, mount to rescue instance, fix SSH config

**Session Manager not working:**
- Verify IAM role attached with AmazonSSMManagedInstanceCore
- Check instance has outbound HTTPS to SSM endpoints
- Ensure SSM agent installed and running: `sudo systemctl status amazon-ssm-agent`
- Check VPC endpoints configured (if private subnet with no NAT)
