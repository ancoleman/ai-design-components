#!/usr/bin/env python3
"""
dlt Pipeline Generator

Generates a dlt (data load tool) pipeline scaffold for common ingestion patterns.
Creates boilerplate code for API, file, or database sources.

Usage:
    python generate_dlt_pipeline.py --source api --name github_issues --output ./pipelines
    python generate_dlt_pipeline.py --source s3 --name raw_events --output ./pipelines
    python generate_dlt_pipeline.py --source database --name legacy_users --output ./pipelines
"""

import argparse
import sys
from pathlib import Path
from textwrap import dedent


def generate_api_pipeline(name: str) -> str:
    """Generate API source pipeline."""
    return dedent(f'''
        """
        dlt Pipeline: {name}

        Ingests data from REST API with incremental loading support.

        Usage:
            python {name}_pipeline.py
        """

        import dlt
        import requests
        from typing import Iterator


        @dlt.source
        def {name}_source(api_base_url: str, api_key: str = dlt.secrets.value):
            """
            Source for {name} API data.

            Args:
                api_base_url: Base URL of the API
                api_key: API key for authentication
            """

            @dlt.resource(
                write_disposition="merge",
                primary_key="id"
            )
            def items(
                updated_at=dlt.sources.incremental("updated_at", initial_value="2024-01-01T00:00:00Z")
            ) -> Iterator[dict]:
                """Fetch items with incremental loading."""
                headers = {{"Authorization": f"Bearer {{api_key}}"}}
                page = 1

                while True:
                    response = requests.get(
                        f"{{api_base_url}}/items",
                        headers=headers,
                        params={{
                            "updated_after": updated_at.last_value,
                            "page": page,
                            "per_page": 100
                        }}
                    )
                    response.raise_for_status()
                    data = response.json()

                    if not data["items"]:
                        break

                    yield from data["items"]
                    page += 1

            return items


        def main():
            # Create pipeline
            pipeline = dlt.pipeline(
                pipeline_name="{name}",
                destination="duckdb",  # Change to postgres, bigquery, etc.
                dataset_name="{name}_data"
            )

            # Run pipeline
            load_info = pipeline.run(
                {name}_source(api_base_url="https://api.example.com")
            )

            print(load_info)


        if __name__ == "__main__":
            main()
    ''').strip()


def generate_s3_pipeline(name: str) -> str:
    """Generate S3 source pipeline."""
    return dedent(f'''
        """
        dlt Pipeline: {name}

        Ingests Parquet/CSV files from S3 bucket.

        Usage:
            python {name}_pipeline.py
        """

        import dlt
        import boto3
        import polars as pl
        from io import BytesIO
        from typing import Iterator


        @dlt.source
        def {name}_source(bucket: str, prefix: str):
            """
            Source for {name} S3 data.

            Args:
                bucket: S3 bucket name
                prefix: Object prefix to filter
            """
            s3 = boto3.client("s3")

            @dlt.resource(write_disposition="append")
            def files() -> Iterator[dict]:
                """Ingest files from S3."""
                paginator = s3.get_paginator("list_objects_v2")

                for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
                    for obj in page.get("Contents", []):
                        key = obj["Key"]

                        # Skip non-data files
                        if not (key.endswith(".parquet") or key.endswith(".csv")):
                            continue

                        # Download and parse
                        response = s3.get_object(Bucket=bucket, Key=key)
                        body = response["Body"].read()

                        if key.endswith(".parquet"):
                            df = pl.read_parquet(BytesIO(body))
                        else:
                            df = pl.read_csv(BytesIO(body))

                        # Yield records
                        for record in df.to_dicts():
                            record["_source_file"] = key
                            yield record

            return files


        def main():
            # Create pipeline
            pipeline = dlt.pipeline(
                pipeline_name="{name}",
                destination="duckdb",
                dataset_name="{name}_data"
            )

            # Run pipeline
            load_info = pipeline.run(
                {name}_source(
                    bucket="my-data-bucket",
                    prefix="raw/events/"
                )
            )

            print(load_info)


        if __name__ == "__main__":
            main()
    ''').strip()


def generate_database_pipeline(name: str) -> str:
    """Generate database source pipeline."""
    return dedent(f'''
        """
        dlt Pipeline: {name}

        Migrates data from source database with incremental loading.

        Usage:
            python {name}_pipeline.py
        """

        import dlt
        from dlt.sources.sql_database import sql_database


        def main():
            # Source database connection
            source_db = sql_database(
                credentials=dlt.secrets["sources.{name}.credentials"],
                schema="public",
                table_names=["users", "orders", "products"],
                incremental=dlt.sources.incremental("updated_at")
            )

            # Create pipeline
            pipeline = dlt.pipeline(
                pipeline_name="{name}",
                destination="postgres",
                dataset_name="{name}_data"
            )

            # Run pipeline
            load_info = pipeline.run(source_db)

            print(load_info)


        if __name__ == "__main__":
            main()
    ''').strip()


TEMPLATES = {
    "api": generate_api_pipeline,
    "s3": generate_s3_pipeline,
    "database": generate_database_pipeline,
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate dlt pipeline scaffold"
    )
    parser.add_argument(
        "--source",
        choices=["api", "s3", "database"],
        required=True,
        help="Source type"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Pipeline name (snake_case)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("."),
        help="Output directory"
    )

    args = parser.parse_args()

    # Generate code
    generator = TEMPLATES[args.source]
    code = generator(args.name)

    # Write file
    output_file = args.output / f"{args.name}_pipeline.py"
    args.output.mkdir(parents=True, exist_ok=True)
    output_file.write_text(code)

    print(f"Generated: {output_file}")
    print("")
    print("Next steps:")
    print(f"  1. Edit {output_file} to configure your source")
    print("  2. Add credentials to .dlt/secrets.toml")
    print(f"  3. Run: python {output_file}")


if __name__ == "__main__":
    main()
