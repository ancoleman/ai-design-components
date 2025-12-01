#!/usr/bin/env python3
"""
Generate optimized SQL and Elasticsearch queries from filter parameters.

This script generates database queries dynamically based on search filters,
handling both SQL (PostgreSQL/MySQL) and Elasticsearch query generation.
"""

import json
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class SQLQueryBuilder:
    """Build SQL queries dynamically from filter parameters."""

    def __init__(self, dialect: str = 'postgresql'):
        self.dialect = dialect
        self.query_parts = {
            'select': [],
            'from': '',
            'join': [],
            'where': [],
            'group_by': [],
            'having': [],
            'order_by': [],
            'limit': None,
            'offset': None
        }

    def build_search_query(self, filters: Dict[str, Any]) -> str:
        """Build a complete search query from filters."""

        # Base query
        self.query_parts['select'] = ['p.*']
        self.query_parts['from'] = 'products p'

        # Text search
        if filters.get('query'):
            self._add_text_search(filters['query'])

        # Category filter
        if filters.get('categories'):
            self._add_category_filter(filters['categories'])

        # Price range
        if filters.get('min_price') or filters.get('max_price'):
            self._add_price_filter(
                filters.get('min_price'),
                filters.get('max_price')
            )

        # Brand filter
        if filters.get('brands'):
            self._add_brand_filter(filters['brands'])

        # Stock filter
        if filters.get('in_stock'):
            self.query_parts['where'].append('p.in_stock = TRUE')

        # Date range
        if filters.get('date_from') or filters.get('date_to'):
            self._add_date_filter(
                filters.get('date_from'),
                filters.get('date_to')
            )

        # Sorting
        self._add_sorting(filters.get('sort_by', 'relevance'))

        # Pagination
        self._add_pagination(
            filters.get('page', 1),
            filters.get('per_page', 20)
        )

        return self._build_query_string()

    def _add_text_search(self, query: str):
        """Add full-text search condition."""
        if self.dialect == 'postgresql':
            # PostgreSQL full-text search
            search_vector = """
                to_tsvector('english', COALESCE(p.title, '') || ' ' ||
                                       COALESCE(p.description, '') || ' ' ||
                                       COALESCE(p.tags, ''))
            """
            self.query_parts['where'].append(
                f"{search_vector} @@ plainto_tsquery('english', '{query}')"
            )

            # Add relevance score
            self.query_parts['select'].append(
                f"ts_rank({search_vector}, plainto_tsquery('english', '{query}')) AS relevance"
            )
        else:
            # MySQL FULLTEXT
            self.query_parts['where'].append(
                f"MATCH(p.title, p.description) AGAINST('{query}' IN NATURAL LANGUAGE MODE)"
            )

    def _add_category_filter(self, categories: List[str]):
        """Add category filter."""
        placeholders = ', '.join([f"'{cat}'" for cat in categories])
        self.query_parts['where'].append(f"p.category IN ({placeholders})")

    def _add_price_filter(self, min_price: Optional[float], max_price: Optional[float]):
        """Add price range filter."""
        if min_price is not None:
            self.query_parts['where'].append(f"p.price >= {min_price}")
        if max_price is not None:
            self.query_parts['where'].append(f"p.price <= {max_price}")

    def _add_brand_filter(self, brands: List[str]):
        """Add brand filter."""
        placeholders = ', '.join([f"'{brand}'" for brand in brands])
        self.query_parts['where'].append(f"p.brand IN ({placeholders})")

    def _add_date_filter(self, date_from: Optional[str], date_to: Optional[str]):
        """Add date range filter."""
        if date_from:
            self.query_parts['where'].append(f"p.created_at >= '{date_from}'")
        if date_to:
            self.query_parts['where'].append(f"p.created_at <= '{date_to}'")

    def _add_sorting(self, sort_by: str):
        """Add sorting clause."""
        sort_options = {
            'relevance': 'relevance DESC' if 'relevance' in str(self.query_parts['select']) else 'p.created_at DESC',
            'price_asc': 'p.price ASC',
            'price_desc': 'p.price DESC',
            'newest': 'p.created_at DESC',
            'oldest': 'p.created_at ASC',
            'rating': 'p.rating DESC',
            'popularity': 'p.view_count DESC'
        }

        self.query_parts['order_by'] = [sort_options.get(sort_by, 'p.created_at DESC')]

    def _add_pagination(self, page: int, per_page: int):
        """Add pagination."""
        self.query_parts['limit'] = per_page
        self.query_parts['offset'] = (page - 1) * per_page

    def _build_query_string(self) -> str:
        """Build final SQL query string."""
        query = f"SELECT {', '.join(self.query_parts['select'])}\n"
        query += f"FROM {self.query_parts['from']}\n"

        if self.query_parts['join']:
            query += '\n'.join(self.query_parts['join']) + '\n'

        if self.query_parts['where']:
            query += f"WHERE {' AND '.join(self.query_parts['where'])}\n"

        if self.query_parts['group_by']:
            query += f"GROUP BY {', '.join(self.query_parts['group_by'])}\n"

        if self.query_parts['having']:
            query += f"HAVING {' AND '.join(self.query_parts['having'])}\n"

        if self.query_parts['order_by']:
            query += f"ORDER BY {', '.join(self.query_parts['order_by'])}\n"

        if self.query_parts['limit']:
            query += f"LIMIT {self.query_parts['limit']}\n"

        if self.query_parts['offset']:
            query += f"OFFSET {self.query_parts['offset']}\n"

        return query


class ElasticsearchQueryBuilder:
    """Build Elasticsearch queries from filter parameters."""

    def build_search_query(self, filters: Dict[str, Any]) -> Dict:
        """Build Elasticsearch query DSL from filters."""

        query = {
            'query': {
                'bool': {
                    'must': [],
                    'filter': [],
                    'should': [],
                    'must_not': []
                }
            }
        }

        # Text search
        if filters.get('query'):
            query['query']['bool']['must'].append({
                'multi_match': {
                    'query': filters['query'],
                    'fields': ['title^3', 'description^2', 'tags'],
                    'type': 'best_fields',
                    'fuzziness': 'AUTO'
                }
            })

        # Category filter
        if filters.get('categories'):
            query['query']['bool']['filter'].append({
                'terms': {'category.keyword': filters['categories']}
            })

        # Price range
        if filters.get('min_price') or filters.get('max_price'):
            price_range = {}
            if filters.get('min_price'):
                price_range['gte'] = filters['min_price']
            if filters.get('max_price'):
                price_range['lte'] = filters['max_price']

            query['query']['bool']['filter'].append({
                'range': {'price': price_range}
            })

        # Brand filter
        if filters.get('brands'):
            query['query']['bool']['filter'].append({
                'terms': {'brand.keyword': filters['brands']}
            })

        # Stock filter
        if filters.get('in_stock'):
            query['query']['bool']['filter'].append({
                'term': {'in_stock': True}
            })

        # Date range
        if filters.get('date_from') or filters.get('date_to'):
            date_range = {}
            if filters.get('date_from'):
                date_range['gte'] = filters['date_from']
            if filters.get('date_to'):
                date_range['lte'] = filters['date_to']

            query['query']['bool']['filter'].append({
                'range': {'created_at': date_range}
            })

        # Sorting
        query['sort'] = self._get_sort_clause(filters.get('sort_by', 'relevance'))

        # Pagination
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 20)
        query['from'] = (page - 1) * per_page
        query['size'] = per_page

        # Aggregations for facets
        if filters.get('include_facets', True):
            query['aggs'] = self._build_aggregations()

        # Clean up empty sections
        if not query['query']['bool']['must']:
            del query['query']['bool']['must']
        if not query['query']['bool']['filter']:
            del query['query']['bool']['filter']
        if not query['query']['bool']['should']:
            del query['query']['bool']['should']
        if not query['query']['bool']['must_not']:
            del query['query']['bool']['must_not']

        # If no conditions, use match_all
        if not query['query']['bool']:
            query['query'] = {'match_all': {}}

        return query

    def _get_sort_clause(self, sort_by: str) -> List[Dict]:
        """Get Elasticsearch sort clause."""
        sort_options = {
            'relevance': [{'_score': 'desc'}],
            'price_asc': [{'price': 'asc'}],
            'price_desc': [{'price': 'desc'}],
            'newest': [{'created_at': 'desc'}],
            'oldest': [{'created_at': 'asc'}],
            'rating': [{'rating': 'desc'}],
            'popularity': [{'view_count': 'desc'}]
        }

        return sort_options.get(sort_by, [{'_score': 'desc'}])

    def _build_aggregations(self) -> Dict:
        """Build aggregations for faceted search."""
        return {
            'categories': {
                'terms': {
                    'field': 'category.keyword',
                    'size': 20
                }
            },
            'brands': {
                'terms': {
                    'field': 'brand.keyword',
                    'size': 20
                }
            },
            'price_ranges': {
                'range': {
                    'field': 'price',
                    'ranges': [
                        {'key': 'Under $50', 'to': 50},
                        {'key': '$50-$100', 'from': 50, 'to': 100},
                        {'key': '$100-$200', 'from': 100, 'to': 200},
                        {'key': 'Over $200', 'from': 200}
                    ]
                }
            },
            'avg_price': {
                'avg': {'field': 'price'}
            },
            'in_stock_count': {
                'filter': {'term': {'in_stock': True}}
            }
        }


def main():
    """Main function to generate queries from command line."""
    parser = argparse.ArgumentParser(
        description='Generate search queries from filter parameters'
    )

    parser.add_argument(
        '--type',
        choices=['sql', 'elasticsearch'],
        default='sql',
        help='Query type to generate'
    )

    parser.add_argument(
        '--dialect',
        choices=['postgresql', 'mysql'],
        default='postgresql',
        help='SQL dialect (for SQL queries)'
    )

    parser.add_argument(
        '--filters',
        type=str,
        required=True,
        help='JSON string of filter parameters'
    )

    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty print output'
    )

    args = parser.parse_args()

    try:
        filters = json.loads(args.filters)
    except json.JSONDecodeError as e:
        print(f"Error parsing filters JSON: {e}")
        return 1

    if args.type == 'sql':
        builder = SQLQueryBuilder(dialect=args.dialect)
        query = builder.build_search_query(filters)
        print(query)
    else:
        builder = ElasticsearchQueryBuilder()
        query = builder.build_search_query(filters)

        if args.pretty:
            print(json.dumps(query, indent=2))
        else:
            print(json.dumps(query))

    return 0


if __name__ == '__main__':
    exit(main())