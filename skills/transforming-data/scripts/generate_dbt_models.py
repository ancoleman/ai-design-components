#!/usr/bin/env python3
"""
Generate dbt Model Boilerplate

Creates standardized dbt model files with proper structure.

Usage:
    python generate_dbt_models.py --name stg_orders --layer staging --source ecommerce
"""

import argparse
import os
from pathlib import Path

STAGING_TEMPLATE = """-- models/{layer}/{name}.sql
-- Staging layer: 1:1 with source, minimal transformations

{{{{
  config(
    materialized='view',
    tags=['{layer}', 'daily']
  )
}}}}

with source as (
    select * from {{{{ source('{source}', '{source_table}') }}}}
),

renamed as (
    select
        -- Add column transformations here
        id,
        created_at,
        updated_at

    from source
    where id is not null
)

select * from renamed
"""

INTERMEDIATE_TEMPLATE = """-- models/{layer}/{name}.sql
-- Intermediate layer: Business logic

{{{{
  config(
    materialized='ephemeral',
    tags=['{layer}']
  )
}}}}

with base as (
    select * from {{{{ ref('{ref_model}') }}}}
),

transformed as (
    select
        -- Add transformations here
        *
    from base
)

select * from transformed
"""

MART_TEMPLATE = """-- models/{layer}/{name}.sql
-- Mart layer: Final analytics model

{{{{
  config(
    materialized='table',
    tags=['{layer}', 'daily']
  )
}}}}

with base as (
    select * from {{{{ ref('{ref_model}') }}}}
),

final as (
    select
        -- Add final transformations
        *
    from base
)

select * from final
"""

def generate_model(name, layer, source=None, source_table=None, ref_model=None):
    """Generate dbt model file"""

    if layer == 'staging':
        template = STAGING_TEMPLATE
        content = template.format(
            layer=layer,
            name=name,
            source=source or 'raw',
            source_table=source_table or name.replace('stg_', '')
        )
    elif layer == 'intermediate':
        template = INTERMEDIATE_TEMPLATE
        content = template.format(
            layer=layer,
            name=name,
            ref_model=ref_model or 'stg_model'
        )
    else:  # marts
        template = MART_TEMPLATE
        content = template.format(
            layer=layer,
            name=name,
            ref_model=ref_model or 'int_model'
        )

    # Create directory if it doesn't exist
    model_dir = Path(f'models/{layer}')
    model_dir.mkdir(parents=True, exist_ok=True)

    # Write file
    file_path = model_dir / f'{name}.sql'
    with open(file_path, 'w') as f:
        f.write(content)

    print(f"Created: {file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate dbt model boilerplate')
    parser.add_argument('--name', required=True, help='Model name (e.g., stg_orders)')
    parser.add_argument('--layer', required=True, choices=['staging', 'intermediate', 'marts'])
    parser.add_argument('--source', help='Source name for staging models')
    parser.add_argument('--source-table', help='Source table name')
    parser.add_argument('--ref-model', help='Referenced model for intermediate/marts')

    args = parser.parse_args()

    generate_model(
        name=args.name,
        layer=args.layer,
        source=args.source,
        source_table=args.source_table,
        ref_model=args.ref_model
    )
