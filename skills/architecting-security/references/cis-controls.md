# CIS Critical Security Controls v8 Reference


## Table of Contents

- [Overview](#overview)
- [Implementation Groups](#implementation-groups)
- [18 CIS Controls](#18-cis-controls)
  - [CIS 1: Inventory and Control of Enterprise Assets](#cis-1-inventory-and-control-of-enterprise-assets)
  - [CIS 2: Inventory and Control of Software Assets](#cis-2-inventory-and-control-of-software-assets)
  - [CIS 3: Data Protection](#cis-3-data-protection)
  - [CIS 4: Secure Configuration of Enterprise Assets and Software](#cis-4-secure-configuration-of-enterprise-assets-and-software)
  - [CIS 5: Account Management](#cis-5-account-management)
  - [CIS 6: Access Control Management](#cis-6-access-control-management)
  - [CIS 7: Continuous Vulnerability Management](#cis-7-continuous-vulnerability-management)
  - [CIS 8: Audit Log Management](#cis-8-audit-log-management)
  - [CIS 13: Network Monitoring and Defense](#cis-13-network-monitoring-and-defense)
  - [CIS 17: Incident Response Management](#cis-17-incident-response-management)

## Overview

CIS Controls provide prioritized, prescriptive security guidance organized in 3 Implementation Groups (IG1, IG2, IG3).

## Implementation Groups

**IG1 (Basic Cyber Hygiene):**
- 56 safeguards
- Small organizations, limited IT security staff
- Essential security baseline

**IG2 (Intermediate):**
- +74 safeguards (130 total)
- Mid-sized organizations with IT security staff
- More sophisticated controls

**IG3 (Advanced):**
- +23 safeguards (153 total)
- Large enterprises with dedicated security teams
- Advanced threat detection and response

## 18 CIS Controls

### CIS 1: Inventory and Control of Enterprise Assets

**Objective:** Maintain accurate asset inventory

**Key Safeguards:**
- 1.1: Establish and maintain detailed asset inventory
- 1.2: Address unauthorized assets
- 1.3: Utilize asset inventory tool
- 1.4: Use dynamic host configuration (DHCP) logging

### CIS 2: Inventory and Control of Software Assets

**Objective:** Track all software and prevent unauthorized software

**Key Safeguards:**
- 2.1: Establish software inventory
- 2.2: Ensure authorized software is supported
- 2.3: Address unauthorized software
- 2.4: Utilize software inventory tools

### CIS 3: Data Protection

**Objective:** Protect sensitive data

**Key Safeguards:**
- 3.1: Establish data management process
- 3.2: Establish data inventory
- 3.3: Configure data access control lists
- 3.6: Encrypt data on end-user devices
- 3.11: Encrypt sensitive data at rest
- 3.14: Log sensitive data access

### CIS 4: Secure Configuration of Enterprise Assets and Software

**Objective:** Harden configurations

**Key Safeguards:**
- 4.1: Establish secure configurations
- 4.2: Establish configuration management
- 4.7: Manage default accounts
- 4.8: Uninstall or disable unnecessary services

### CIS 5: Account Management

**Objective:** Manage user accounts and credentials

**Key Safeguards:**
- 5.1: Establish centralized account management
- 5.2: Use unique passwords
- 5.3: Disable dormant accounts
- 5.4: Restrict admin privileges to dedicated accounts

### CIS 6: Access Control Management

**Objective:** Control access to resources

**Key Safeguards:**
- 6.1: Establish access granting process
- 6.2: Establish access revoking process
- 6.3: Require MFA
- 6.5: Require MFA for remote network access
- 6.8: Define and maintain role-based access control

### CIS 7: Continuous Vulnerability Management

**Objective:** Identify and remediate vulnerabilities

**Key Safeguards:**
- 7.1: Establish vulnerability management process
- 7.2: Remediate vulnerabilities
- 7.3: Perform automated operating system patch management
- 7.4: Perform automated application patch management
- 7.5: Perform automated vulnerability scans

### CIS 8: Audit Log Management

**Objective:** Collect, alert, review, and retain audit logs

**Key Safeguards:**
- 8.1: Establish audit log management process
- 8.2: Collect audit logs
- 8.3: Ensure adequate storage for logs
- 8.9: Centralize audit log collection
- 8.10: Retain audit logs
- 8.11: Conduct audit log reviews

### CIS 13: Network Monitoring and Defense

**Objective:** Monitor and defend network traffic

**Key Safeguards:**
- 13.1: Centralize security event collection
- 13.2: Deploy network-based IDS sensors
- 13.3: Deploy network-based IPS
- 13.6: Collect network traffic flow logs
- 13.10: Perform application layer filtering

### CIS 17: Incident Response Management

**Objective:** Establish incident response capability

**Key Safeguards:**
- 17.1: Designate incident response personnel
- 17.2: Establish incident response process
- 17.3: Maintain incident response contact information
- 17.6: Maintain incident response documentation
- 17.9: Conduct post-incident reviews
