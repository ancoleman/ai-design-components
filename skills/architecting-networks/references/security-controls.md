# Security Controls

Network security control mechanisms for cloud environments.

## Security Groups vs Network ACLs

### Security Groups (Recommended)

**Characteristics:**
- Stateful (return traffic automatically allowed)
- Instance-level control
- Allow rules only (implicit deny)
- Can reference other security groups

**Best Practices:**
- Use descriptive names
- Reference other SGs instead of CIDR blocks
- Keep rules minimal and specific
- One security group per service

### Network ACLs

**Characteristics:**
- Stateless (must allow both request and response)
- Subnet-level control
- Allow and deny rules
- Rules processed in order

**When to Use:**
- Explicit deny rules (block specific IPs)
- Compliance requirements
- Additional layer beyond security groups

**Important:**
- Remember ephemeral ports (1024-65535)
- Test thoroughly (stateless nature causes issues)

## Decision Matrix

| Requirement | Security Group | Network ACL |
|-------------|----------------|-------------|
| Block specific IP | No | Yes (deny rule) |
| Instance-level control | Yes | No |
| Stateful filtering | Yes | No |
| Reference other SGs | Yes | No |
| Default recommendation | Yes | Only if needed |
