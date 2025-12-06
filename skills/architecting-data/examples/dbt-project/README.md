# dbt Project Example

Example dbt project structure demonstrating medallion architecture (bronze → silver → gold).

## Project Structure

```
my_dbt_project/
├── models/
│   ├── staging/           # Silver layer (bronze → silver)
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   └── schema.yml     # Tests and documentation
│   ├── intermediate/      # Silver layer joins
│   │   └── int_customer_orders.sql
│   └── marts/             # Gold layer (business-level)
│       ├── fact_sales.sql
│       ├── dim_customer.sql
│       └── schema.yml
├── dbt_project.yml
└── profiles.yml
```

## Installation

```bash
pip install dbt-snowflake
dbt init my_dbt_project
cd my_dbt_project
dbt run
dbt test
```

## Model Examples

See individual SQL files for transformation logic and schema.yml for tests.
