#!/usr/bin/env python3
"""
Generate realistic mock data for testing tables and data grids.
Supports various data types and configurable row counts.
"""

import json
import random
import argparse
from datetime import datetime, timedelta
import string
import sys

# Sample data pools
FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa',
                'James', 'Mary', 'William', 'Jennifer', 'Richard', 'Linda', 'Thomas', 'Barbara']

LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Taylor']

DEPARTMENTS = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations',
                'Customer Support', 'Product', 'Design', 'Legal']

COMPANIES = ['Tech Corp', 'Global Industries', 'Innovate LLC', 'Digital Solutions',
             'Cloud Systems', 'Data Dynamics', 'Future Tech', 'Smart Services']

CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
          'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Seattle']

COUNTRIES = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia', 'Brazil']

STATUSES = ['Active', 'Pending', 'Inactive', 'Suspended', 'Archived']

PRIORITIES = ['Low', 'Medium', 'High', 'Critical']

def generate_email(first_name, last_name):
    """Generate realistic email address"""
    domains = ['example.com', 'email.com', 'company.org', 'business.net']
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

def generate_phone():
    """Generate phone number"""
    return f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_date(start_year=2020, end_year=2024):
    """Generate random date"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)

    time_between = end - start
    days_between = time_between.days
    random_days = random.randrange(days_between)

    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

def generate_id(index, prefix=''):
    """Generate unique ID"""
    if prefix:
        return f"{prefix}-{str(index).zfill(6)}"
    return f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}-{str(index).zfill(6)}"

def generate_row(index, columns):
    """Generate a single row of data"""
    row = {}

    for col in columns:
        col_name = col['name']
        col_type = col['type']

        if col_type == 'id':
            row[col_name] = generate_id(index, col.get('prefix', ''))

        elif col_type == 'name':
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            row[col_name] = f"{first} {last}"

        elif col_type == 'email':
            if 'name' in row:
                parts = row['name'].split()
                row[col_name] = generate_email(parts[0], parts[-1])
            else:
                row[col_name] = generate_email(
                    random.choice(FIRST_NAMES),
                    random.choice(LAST_NAMES)
                )

        elif col_type == 'phone':
            row[col_name] = generate_phone()

        elif col_type == 'date':
            row[col_name] = generate_date(
                col.get('start_year', 2020),
                col.get('end_year', 2024)
            )

        elif col_type == 'number':
            min_val = col.get('min', 0)
            max_val = col.get('max', 100)
            decimals = col.get('decimals', 0)

            if decimals > 0:
                value = random.uniform(min_val, max_val)
                row[col_name] = round(value, decimals)
            else:
                row[col_name] = random.randint(min_val, max_val)

        elif col_type == 'currency':
            min_val = col.get('min', 0)
            max_val = col.get('max', 10000)
            value = random.uniform(min_val, max_val)
            row[col_name] = round(value, 2)

        elif col_type == 'boolean':
            row[col_name] = random.choice([True, False])

        elif col_type == 'select':
            options = col.get('options', [])
            if col_name == 'department':
                options = DEPARTMENTS
            elif col_name == 'company':
                options = COMPANIES
            elif col_name == 'city':
                options = CITIES
            elif col_name == 'country':
                options = COUNTRIES
            elif col_name == 'status':
                options = STATUSES
            elif col_name == 'priority':
                options = PRIORITIES

            row[col_name] = random.choice(options) if options else None

        elif col_type == 'text':
            min_length = col.get('min_length', 10)
            max_length = col.get('max_length', 100)
            length = random.randint(min_length, max_length)
            row[col_name] = ''.join(random.choices(string.ascii_letters + ' ', k=length))

        elif col_type == 'url':
            row[col_name] = f"https://example.com/{random.choice(string.ascii_lowercase)}/{random.randint(1, 1000)}"

        elif col_type == 'percentage':
            row[col_name] = random.randint(0, 100)

        else:
            row[col_name] = f"{col_name}_{index}"

    return row

def generate_dataset(rows, columns, format='json'):
    """Generate complete dataset"""
    data = []

    for i in range(1, rows + 1):
        data.append(generate_row(i, columns))

        # Progress indicator for large datasets
        if rows >= 10000 and i % 1000 == 0:
            print(f"Generated {i}/{rows} rows...", file=sys.stderr)

    return data

def save_data(data, filename, format):
    """Save data to file in specified format"""
    if format == 'json':
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    elif format == 'csv':
        import csv
        if data:
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

    elif format == 'sql':
        # Generate SQL insert statements
        with open(filename, 'w') as f:
            f.write("-- Generated SQL Insert Statements\n")
            f.write("-- Table: mock_data\n\n")

            if data:
                columns = list(data[0].keys())
                for row in data:
                    values = []
                    for col in columns:
                        val = row[col]
                        if isinstance(val, str):
                            values.append(f"'{val}'")
                        elif isinstance(val, bool):
                            values.append('TRUE' if val else 'FALSE')
                        elif val is None:
                            values.append('NULL')
                        else:
                            values.append(str(val))

                    f.write(f"INSERT INTO mock_data ({', '.join(columns)}) VALUES ({', '.join(values)});\n")

# Predefined column schemas
SCHEMAS = {
    'employees': [
        {'name': 'id', 'type': 'id', 'prefix': 'EMP'},
        {'name': 'name', 'type': 'name'},
        {'name': 'email', 'type': 'email'},
        {'name': 'phone', 'type': 'phone'},
        {'name': 'department', 'type': 'select'},
        {'name': 'salary', 'type': 'currency', 'min': 30000, 'max': 150000},
        {'name': 'start_date', 'type': 'date'},
        {'name': 'is_active', 'type': 'boolean'},
    ],

    'products': [
        {'name': 'id', 'type': 'id', 'prefix': 'PROD'},
        {'name': 'product_name', 'type': 'text', 'min_length': 10, 'max_length': 50},
        {'name': 'sku', 'type': 'id', 'prefix': 'SKU'},
        {'name': 'price', 'type': 'currency', 'min': 10, 'max': 1000},
        {'name': 'quantity', 'type': 'number', 'min': 0, 'max': 1000},
        {'name': 'category', 'type': 'select', 'options': ['Electronics', 'Clothing', 'Food', 'Books', 'Home']},
        {'name': 'in_stock', 'type': 'boolean'},
        {'name': 'created_date', 'type': 'date'},
    ],

    'orders': [
        {'name': 'order_id', 'type': 'id', 'prefix': 'ORD'},
        {'name': 'customer_name', 'type': 'name'},
        {'name': 'email', 'type': 'email'},
        {'name': 'order_date', 'type': 'date'},
        {'name': 'total_amount', 'type': 'currency', 'min': 10, 'max': 5000},
        {'name': 'status', 'type': 'select'},
        {'name': 'priority', 'type': 'select'},
        {'name': 'shipping_city', 'type': 'select'},
    ],

    'logs': [
        {'name': 'id', 'type': 'id', 'prefix': 'LOG'},
        {'name': 'timestamp', 'type': 'date'},
        {'name': 'level', 'type': 'select', 'options': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']},
        {'name': 'message', 'type': 'text', 'min_length': 20, 'max_length': 200},
        {'name': 'user', 'type': 'name'},
        {'name': 'ip_address', 'type': 'text', 'min_length': 7, 'max_length': 15},
        {'name': 'response_time', 'type': 'number', 'min': 10, 'max': 5000},
    ],
}

def main():
    parser = argparse.ArgumentParser(description='Generate mock data for table testing')
    parser.add_argument('--rows', type=int, default=100, help='Number of rows to generate')
    parser.add_argument('--schema', choices=SCHEMAS.keys(), default='employees',
                        help='Predefined schema to use')
    parser.add_argument('--format', choices=['json', 'csv', 'sql'], default='json',
                        help='Output format')
    parser.add_argument('--output', type=str, help='Output filename')
    parser.add_argument('--columns', type=int, help='Number of generic columns (if not using schema)')

    args = parser.parse_args()

    # Use predefined schema or generate generic columns
    if args.columns:
        columns = []
        for i in range(args.columns):
            col_types = ['name', 'email', 'number', 'date', 'boolean', 'select', 'text']
            columns.append({
                'name': f'column_{i+1}',
                'type': random.choice(col_types)
            })
    else:
        columns = SCHEMAS[args.schema]

    # Generate data
    print(f"Generating {args.rows} rows with {len(columns)} columns...", file=sys.stderr)
    data = generate_dataset(args.rows, columns, args.format)

    # Save or output data
    if args.output:
        save_data(data, args.output, args.format)
        print(f"Data saved to {args.output}", file=sys.stderr)
    else:
        # Output to stdout
        if args.format == 'json':
            print(json.dumps(data, indent=2))
        elif args.format == 'csv':
            import csv
            if data:
                writer = csv.DictWriter(sys.stdout, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

    print(f"Successfully generated {len(data)} rows", file=sys.stderr)

if __name__ == '__main__':
    main()