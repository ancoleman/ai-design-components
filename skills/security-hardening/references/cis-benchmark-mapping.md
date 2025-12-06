# CIS Benchmark Mapping Reference

Mapping of CIS (Center for Internet Security) Benchmarks to hardening actions across all infrastructure layers.

## Table of Contents

1. [CIS Controls v8 Overview](#cis-controls-v8-overview)
2. [Linux CIS Benchmark Mapping](#linux-cis-benchmark-mapping)
3. [Docker CIS Benchmark Mapping](#docker-cis-benchmark-mapping)
4. [Kubernetes CIS Benchmark Mapping](#kubernetes-cis-benchmark-mapping)
5. [Cloud Provider CIS Benchmarks](#cloud-provider-cis-benchmarks)
6. [Automated CIS Scanning](#automated-cis-scanning)

---

## CIS Controls v8 Overview

The 18 CIS Controls provide a prioritized framework for cybersecurity:

| Control | Name | Hardening Impact |
|---------|------|------------------|
| 1 | Inventory and Control of Enterprise Assets | Asset discovery, tagging |
| 2 | Inventory and Control of Software Assets | SBOM, approved software lists |
| 3 | Data Protection | Encryption at rest/transit |
| 4 | Secure Configuration of Enterprise Assets | OS/container/cloud hardening |
| 5 | Account Management | Least privilege, MFA |
| 6 | Access Control Management | RBAC, network policies |
| 7 | Continuous Vulnerability Management | Scanning, patching |
| 8 | Audit Log Management | Centralized logging |
| 9 | Email and Web Browser Protections | Not infrastructure-focused |
| 10 | Malware Defenses | Runtime security (Falco) |
| 11 | Data Recovery | Backups, disaster recovery |
| 12 | Network Infrastructure Management | Firewall, segmentation |
| 13 | Network Monitoring and Defense | IDS/IPS, flow logs |
| 14 | Security Awareness Training | Not infrastructure-focused |
| 15 | Service Provider Management | Vendor assessments |
| 16 | Application Software Security | Container security, SAST/DAST |
| 17 | Incident Response Management | Playbooks, automation |
| 18 | Penetration Testing | Not hardening-focused |

**Focus for Hardening:** Controls 3, 4, 5, 6, 7, 8, 10, 12, 13, 16

---

## Linux CIS Benchmark Mapping

### Initial Setup (Section 1)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 1.1.1 | Disable unused filesystems | `modprobe -r cramfs squashfs udf` |
| 1.1.2-1.1.10 | Configure /tmp, /var/tmp, /home | Mount with noexec, nosuid, nodev |
| 1.3.1 | AIDE integrity checking | Install and configure AIDE |
| 1.4.1 | Bootloader password | Set GRUB password |
| 1.5.1-1.5.3 | Address space layout randomization | `kernel.randomize_va_space = 2` |
| 1.6.1 | SELinux/AppArmor enabled | Enable and enforce |

### Services (Section 2)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 2.1.x | Disable unnecessary services | `systemctl disable bluetooth cups avahi-daemon` |
| 2.2.1 | NTP configured | Configure chronyd/ntpd |
| 2.2.2-2.2.7 | Disable X11, rsync, LDAP, etc. | Remove or disable if unused |

### Network Configuration (Section 3)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 3.1.1 | Disable IP forwarding | `net.ipv4.ip_forward = 0` |
| 3.1.2 | Disable send packet redirects | `net.ipv4.conf.all.send_redirects = 0` |
| 3.2.1-3.2.9 | Network parameter hardening | sysctl settings (see linux-hardening.md) |
| 3.3.1 | Ensure firewall is active | Configure iptables/firewalld/nftables |

### Logging and Auditing (Section 4)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 4.1.1-4.1.17 | Configure auditd | Enable auditd, set audit rules |
| 4.2.1-4.2.3 | Configure rsyslog/syslog-ng | Centralized logging |
| 4.3 | Ensure logrotate configured | Rotate logs, retain 90+ days |

### Access Control (Section 5)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 5.1.1-5.1.9 | Configure cron | Restrict cron/at access |
| 5.2.1-5.2.23 | SSH server configuration | See SSH hardening section |
| 5.3.1-5.3.4 | Configure PAM | Password quality, account lockout |
| 5.4.1-5.4.5 | User accounts and environment | Password policies, umask, timeouts |
| 5.5 | Ensure root login restricted | `/etc/securetty` configuration |

### System Maintenance (Section 6)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 6.1.1-6.1.14 | File permissions | Secure /etc/passwd, /etc/shadow, etc. |
| 6.2.1-6.2.20 | User and group settings | Remove duplicate UIDs, empty passwords |

---

## Docker CIS Benchmark Mapping

### Host Configuration (Section 1)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 1.1.1 | Separate partition for containers | Mount /var/lib/docker on separate partition |
| 1.1.2-1.1.18 | Harden host OS | Follow Linux CIS benchmark |
| 1.2.1 | Restrict network traffic between containers | `"icc": false` in daemon.json |
| 1.2.2 | Set logging level | `"log-level": "info"` |

### Docker Daemon Configuration (Section 2)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 2.1 | Restrict network traffic | `"icc": false`, `"userland-proxy": false` |
| 2.2 | Set default ulimit | `"default-ulimits": { "nofile": { "Hard": 64000 } }` |
| 2.5 | Enable user namespace support | `"userns-remap": "default"` |
| 2.7 | Enable live restore | `"live-restore": true` |
| 2.8 | Disable userland proxy | `"userland-proxy": false` |
| 2.12 | No new privileges flag | `"no-new-privileges": true` |
| 2.14 | Enable daemon logging | Configure centralized logging |
| 2.18 | Disable experimental features | `"experimental": false` |

### Docker Daemon Files (Section 3)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 3.1-3.22 | File ownership and permissions | Set permissions on Docker files |
| 3.1 | /etc/docker/daemon.json | `chown root:root`, `chmod 644` |
| 3.9 | TLS CA certificate | `chmod 444` |

### Container Images (Section 4)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 4.1 | Create user for container | `USER nonroot` in Dockerfile |
| 4.2 | Use trusted base images | Chainguard, Distroless, Alpine |
| 4.3 | Do not install unnecessary packages | Minimal base images |
| 4.5 | Enable Content trust | `DOCKER_CONTENT_TRUST=1` |
| 4.6 | Add HEALTHCHECK | `HEALTHCHECK CMD curl -f http://localhost/` |
| 4.7 | Do not use update instructions alone | Combine RUN commands |

### Container Runtime (Section 5)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 5.1 | Verify AppArmor profile | `--security-opt apparmor=docker-default` |
| 5.2 | Verify SELinux | `--security-opt label=level:s0:c100,c200` |
| 5.3 | Restrict Linux Kernel Capabilities | `--cap-drop=ALL --cap-add=NET_BIND_SERVICE` |
| 5.4 | Do not use privileged containers | Avoid `--privileged` |
| 5.7 | Do not mount sensitive directories | Avoid `-v /:/host` |
| 5.10 | Set memory limit | `--memory="256m"` |
| 5.11 | Set CPU priority | `--cpu-shares=512` |
| 5.12 | Mount root filesystem as read-only | `--read-only` |
| 5.15 | Do not share host network namespace | Avoid `--net=host` |
| 5.25 | Restrict container from acquiring privileges | `--security-opt=no-new-privileges` |

---

## Kubernetes CIS Benchmark Mapping

### Control Plane Components (Section 1)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 1.1.1 | API server pod specification file permissions | `chmod 600` |
| 1.2.1 | --anonymous-auth argument | Set to `false` |
| 1.2.5 | --kubelet-certificate-authority argument | Set CA bundle |
| 1.2.6 | --authorization-mode argument | Include `RBAC,Node` |
| 1.2.9 | --admission-control-plugin argument | Enable PodSecurity, NodeRestriction |
| 1.2.12 | --enable-admission-plugins | AlwaysPullImages, PodSecurity |
| 1.2.19 | --audit-log-path argument | Enable audit logging |
| 1.2.22 | --audit-log-maxage | Set to 30 or greater |

### Etcd (Section 2)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 2.1 | --cert-file and --key-file arguments | Enable TLS |
| 2.2 | --client-cert-auth argument | Set to `true` |
| 2.3 | --auto-tls argument | Set to `false` |
| 2.7 | Ensure unique Certificate Authority | Separate CA for etcd |

### Control Plane Configuration (Section 3)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 3.1.1 | Client certificate authentication | Do not use `--insecure-bind-address` |
| 3.2.1 | Ensure minimal audit policy | Configure audit policy |

### Worker Nodes (Section 4)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 4.1.1-4.1.10 | Worker node configuration files | Secure file permissions |
| 4.2.1 | --anonymous-auth | Set to `false` on kubelet |
| 4.2.2 | --authorization-mode | Set to `Webhook` |
| 4.2.6 | --protect-kernel-defaults | Set to `true` |
| 4.2.10 | --tls-cert-file and --tls-private-key-file | Enable TLS on kubelet |

### Policies (Section 5)

| CIS ID | Requirement | Hardening Action |
|--------|-------------|------------------|
| 5.1.1 | RBAC policies minimized | Least privilege roles |
| 5.1.5 | Default service accounts not used | Create service accounts |
| 5.2.1 | Pod Security Standards | Apply `restricted` standard |
| 5.2.2 | Minimize privileged containers | `allowPrivilegeEscalation: false` |
| 5.2.3 | Minimize containers running as root | `runAsNonRoot: true` |
| 5.2.5 | Minimize NET_RAW capability | Drop all capabilities |
| 5.2.6 | Minimize containers with added capabilities | `capabilities: drop: [ALL]` |
| 5.3.1 | Network policies applied | Default deny, explicit allow |
| 5.4.1 | Secrets not in environment variables | Use volume mounts |
| 5.7.1 | Create administrative boundaries | Use namespaces |

---

## Cloud Provider CIS Benchmarks

### AWS Foundations Benchmark

**Key sections:**
- 1.x: Identity and Access Management (IAM)
- 2.x: Storage (S3 encryption, access controls)
- 3.x: Logging (CloudTrail, VPC Flow Logs)
- 4.x: Monitoring (CloudWatch, GuardDuty)
- 5.x: Networking (Security Groups, NACLs)

**Automated scanning:**
```bash
prowler aws --compliance cis_2.0_aws
```

### GCP CIS Benchmark

**Key sections:**
- 1.x: Identity and Access Management
- 2.x: Logging and Monitoring (Cloud Logging, Monitoring)
- 3.x: Networking (VPC, Firewall Rules)
- 4.x: Virtual Machines (Compute Engine)
- 5.x: Storage (Cloud Storage, encryption)
- 6.x: Cloud SQL Database Services

**Automated scanning:**
```bash
scout gcp --project-id my-project
```

### Azure CIS Benchmark

**Key sections:**
- 1.x: Identity and Access Management (Azure AD)
- 2.x: Microsoft Defender for Cloud
- 3.x: Storage Accounts
- 4.x: Database Services
- 5.x: Logging and Monitoring (Log Analytics)
- 6.x: Networking (NSGs, Virtual Networks)
- 7.x: Virtual Machines
- 8.x: Key Vault

**Automated scanning:**
```bash
scout azure
```

---

## Automated CIS Scanning

### Docker Bench Security

```bash
# Run Docker CIS benchmark
docker run --rm -it \
  --net host \
  --pid host \
  --userns host \
  --cap-add audit_control \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /etc:/etc:ro \
  docker/docker-bench-security

# Output includes:
# [PASS] 1.1.1 - Ensure a separate partition for containers
# [WARN] 1.2.1 - Ensure the container host has been Hardened
# [FAIL] 2.1 - Ensure network traffic is restricted between containers
```

### kube-bench (Kubernetes)

```bash
# Run as Kubernetes Job
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml

# View results
kubectl logs job/kube-bench

# Run on master node
kube-bench run --targets master

# Run on worker node
kube-bench run --targets node

# Output to JSON
kube-bench run --json --outputfile results.json
```

### Lynis (Linux)

```bash
# Install Lynis
apt-get install lynis

# Run full audit
lynis audit system

# Check specific category
lynis audit system --tests-from-category security

# Generate report
lynis audit system --quick --report-file /tmp/lynis-report.txt
```

### OpenSCAP (Linux)

```bash
# Install OpenSCAP
apt-get install libopenscap8 ssg-base ssg-debderived ssg-debian ssg-nondebian

# Run Ubuntu 20.04 CIS scan
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis_level1_server \
  --results scan-results.xml \
  --report scan-report.html \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2004-ds.xml
```

### Prowler (AWS)

```bash
# Install
pip install prowler

# Run full CIS scan
prowler aws --compliance cis_2.0_aws

# Specific services only
prowler aws --services s3 iam ec2

# Output to JSON
prowler aws --output-modes json html csv --output-directory ./reports/
```

---

## Compliance Mapping

### SOC 2 to CIS Mapping

| SOC 2 Control | CIS Controls | Hardening Action |
|---------------|--------------|------------------|
| CC6.1 (Logical Access) | CIS 5, 6 | IAM, RBAC, MFA |
| CC6.6 (Encryption) | CIS 3 | TLS, encryption at rest |
| CC6.7 (System Operations) | CIS 4 | Secure configuration |
| CC7.2 (System Monitoring) | CIS 8, 13 | Logging, monitoring |

### PCI DSS to CIS Mapping

| PCI DSS Requirement | CIS Controls | Hardening Action |
|---------------------|--------------|------------------|
| 1.x (Firewall) | CIS 12, 13 | Network segmentation |
| 2.x (Default passwords) | CIS 4, 5 | Secure configuration |
| 3.x (Cardholder data) | CIS 3 | Encryption |
| 8.x (Access control) | CIS 5, 6 | IAM, MFA |
| 10.x (Logging) | CIS 8 | Audit logging |

### HIPAA to CIS Mapping

| HIPAA Requirement | CIS Controls | Hardening Action |
|-------------------|--------------|------------------|
| §164.308(a)(1) (Risk Analysis) | CIS 7 | Vulnerability scanning |
| §164.308(a)(3) (Access Management) | CIS 5, 6 | Least privilege, RBAC |
| §164.308(a)(5) (Security Awareness) | CIS 14 | Training (not hardening) |
| §164.312(a)(1) (Access Control) | CIS 6 | Authentication, authorization |
| §164.312(e)(1) (Transmission Security) | CIS 3 | TLS, VPN |

---

## Additional Resources

- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- CIS Controls v8: https://www.cisecurity.org/controls/v8
- Docker Bench Security: https://github.com/docker/docker-bench-security
- kube-bench: https://github.com/aquasecurity/kube-bench
- Lynis: https://cisofy.com/lynis/
- OpenSCAP: https://www.open-scap.org/
- Prowler: https://github.com/prowler-cloud/prowler
