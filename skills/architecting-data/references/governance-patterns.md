# Data Governance Patterns


## Table of Contents

- [Data Catalog](#data-catalog)
- [Data Lineage](#data-lineage)
- [Data Quality](#data-quality)
- [Access Control](#access-control)
- [Data Quality in Medallion](#data-quality-in-medallion)
- [Best Practices](#best-practices)

## Data Catalog

**Purpose:** Searchable inventory of all data assets

**Core Features:**
- Metadata management (schema, owner, lineage)
- Search and discovery
- Tagging (PII, confidential, deprecated)
- Business glossary
- Lineage visualization

**Tools:**
- **DataHub (LinkedIn):** Open-source, REST API
- **Alation:** Enterprise, AI-powered search
- **Collibra:** Governance-focused, compliance
- **AWS Glue Data Catalog:** Native AWS
- **Azure Purview:** Native Azure

## Data Lineage

**Purpose:** Track data flow from source to consumption

**Benefits:**
- Impact analysis (what breaks if I change this?)
- Root cause analysis (where did bad data come from?)
- Compliance (where is PII used?)

**Column-Level Lineage Example:**
```
customers.email
  → bronze.raw_customers._raw_data['email']
  → silver.customers.email
  → gold.customer_360.email_address
  → Marketing Tool (GDPR: track PII usage)
```

**Tools:**
- **OpenLineage:** Open standard
- **Marquez:** Reference implementation
- **DataHub:** Visualization

## Data Quality

**Six Dimensions:**
1. **Accuracy:** Does data reflect reality?
2. **Completeness:** Are required fields populated?
3. **Consistency:** Do related data agree?
4. **Timeliness:** Is data fresh enough?
5. **Validity:** Does data conform to schema?
6. **Uniqueness:** Are there unwanted duplicates?

**Tools:**

**Great Expectations:**
```python
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_unique("customer_id")
validator.expect_column_values_to_match_regex("email", r'^[\w\.-]+@[\w\.-]+\.\w+$')
```

**Soda Core:**
```yaml
checks for silver.customers:
  - row_count > 1000
  - missing_count(customer_id) = 0
  - duplicate_count(customer_id) = 0
  - invalid_percent(email) < 1%
```

**dbt Tests:**
```yaml
models:
  - name: customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
```

## Access Control

**1. Role-Based Access Control (RBAC):**
```sql
CREATE ROLE sales_analyst;
GRANT SELECT ON gold.fact_sales TO ROLE sales_analyst;
GRANT ROLE sales_analyst TO USER alice@company.com;
```

**2. Attribute-Based (Row-Level Security):**
```sql
CREATE ROW ACCESS POLICY customers_region_policy
AS (region string) RETURNS BOOLEAN ->
  CASE
    WHEN IS_ROLE_IN_SESSION('US_ANALYST') AND region = 'US' THEN TRUE
    WHEN IS_ROLE_IN_SESSION('EU_ANALYST') AND region = 'EU' THEN TRUE
    ELSE FALSE
  END;
```

**3. Column-Level Security (Dynamic Data Masking):**
```sql
CREATE MASKING POLICY mask_email AS (val string) RETURNS string ->
  CASE
    WHEN IS_ROLE_IN_SESSION('PII_VIEWER') THEN val
    ELSE '***MASKED***'
  END;

ALTER TABLE gold.customers
  MODIFY COLUMN email SET MASKING POLICY mask_email;
```

## Data Quality in Medallion

| Layer Transition | Quality Checks | Purpose |
|-----------------|---------------|---------|
| Bronze → Silver | Schema validation, type checks, deduplication | Ensure parseable and unique |
| Silver → Gold | Business rules, referential integrity | Ensure business logic |
| Gold | Anomaly detection, statistical checks | Ensure reasonable |

## Best Practices

1. **Automate quality checks:** Integrate into CI/CD
2. **Monitor lineage:** Track data flow end-to-end
3. **Catalog everything:** Make data discoverable
4. **Enforce access control:** Least privilege principle
5. **Track data quality:** Metrics and dashboards
6. **Document data products:** Schema, SLAs, examples
