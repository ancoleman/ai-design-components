#!/usr/bin/env python3
"""
MongoDB Index Validation Script

Analyzes MongoDB collections and validates index coverage for common queries.
Suggests missing indexes and identifies unused indexes.

Usage:
    python validate_indexes.py --db myapp --collection orders
    python validate_indexes.py --db myapp --all
"""

import argparse
import sys
from typing import Dict, List, Any
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import json


class IndexValidator:
    def __init__(self, uri: str, database: str):
        self.client = MongoClient(uri)
        self.db = self.client[database]

    def get_indexes(self, collection_name: str) -> List[Dict[str, Any]]:
        """Get all indexes for a collection"""
        collection = self.db[collection_name]
        return list(collection.list_indexes())

    def analyze_queries(self, collection_name: str) -> List[Dict[str, Any]]:
        """Analyze slow queries from profiler"""
        try:
            # Get profiling data (last 100 slow queries)
            profiler_data = list(self.db.system.profile.find({
                'ns': f"{self.db.name}.{collection_name}",
                'millis': {'$gte': 100}  # Queries taking >= 100ms
            }).sort('ts', -1).limit(100))

            return profiler_data
        except OperationFailure:
            print("⚠️  Profiling not enabled. Enable with: db.setProfilingLevel(1, { slowms: 100 })")
            return []

    def validate_index_coverage(self, collection_name: str) -> Dict[str, Any]:
        """Validate index coverage for a collection"""
        collection = self.db[collection_name]
        indexes = self.get_indexes(collection_name)

        # Extract index fields
        index_fields = {}
        for idx in indexes:
            key = idx.get('key', {})
            name = idx['name']
            if name != '_id_':  # Skip default _id index
                index_fields[name] = list(key.keys())

        # Common query patterns to check
        common_patterns = [
            {'email': 1},
            {'status': 1},
            {'userId': 1},
            {'createdAt': -1},
            {'status': 1, 'createdAt': -1},
            {'userId': 1, 'createdAt': -1}
        ]

        results = {
            'collection': collection_name,
            'existing_indexes': indexes,
            'coverage': [],
            'missing_indexes': [],
            'unused_indexes': []
        }

        # Check coverage for common patterns
        for pattern in common_patterns:
            covered = self._check_coverage(pattern, index_fields)
            results['coverage'].append({
                'query': pattern,
                'covered': covered['covered'],
                'index': covered.get('index')
            })

            if not covered['covered']:
                results['missing_indexes'].append(pattern)

        return results

    def _check_coverage(self, query_pattern: Dict, index_fields: Dict) -> Dict:
        """Check if query pattern is covered by existing indexes"""
        query_keys = list(query_pattern.keys())

        for idx_name, idx_keys in index_fields.items():
            # Check if index covers query
            if len(query_keys) <= len(idx_keys):
                # Check if query keys are prefix of index keys
                if idx_keys[:len(query_keys)] == query_keys:
                    return {'covered': True, 'index': idx_name}

        return {'covered': False}

    def suggest_indexes(self, collection_name: str) -> List[Dict[str, Any]]:
        """Suggest indexes based on slow queries"""
        slow_queries = self.analyze_queries(collection_name)
        suggestions = []

        for query in slow_queries:
            if query.get('planSummary', '').startswith('COLLSCAN'):
                # Collection scan detected
                command = query.get('command', {})
                filter_keys = command.get('filter', {}).keys()

                if filter_keys:
                    suggestions.append({
                        'reason': 'Collection scan detected',
                        'query': command.get('filter'),
                        'execution_time': query.get('millis'),
                        'suggested_index': {field: 1 for field in filter_keys}
                    })

        return suggestions

    def get_index_usage_stats(self, collection_name: str) -> List[Dict[str, Any]]:
        """Get index usage statistics"""
        collection = self.db[collection_name]
        try:
            stats = collection.aggregate([
                {'$indexStats': {}}
            ])
            return list(stats)
        except OperationFailure:
            print("⚠️  Index stats not available (MongoDB 3.2+ required)")
            return []

    def print_report(self, collection_name: str):
        """Print comprehensive index report"""
        print(f"\n{'='*70}")
        print(f"Index Validation Report: {self.db.name}.{collection_name}")
        print(f"{'='*70}\n")

        # Existing indexes
        indexes = self.get_indexes(collection_name)
        print("📊 EXISTING INDEXES")
        print("-" * 70)
        for idx in indexes:
            key = idx.get('key', {})
            name = idx['name']
            unique = "UNIQUE" if idx.get('unique') else ""
            sparse = "SPARSE" if idx.get('sparse') else ""
            ttl = f"TTL ({idx.get('expireAfterSeconds')}s)" if idx.get('expireAfterSeconds') else ""
            flags = " ".join(filter(None, [unique, sparse, ttl]))

            print(f"  ✓ {name}")
            print(f"    Fields: {list(key.keys())}")
            if flags:
                print(f"    Flags: {flags}")

        # Coverage validation
        print("\n🔍 INDEX COVERAGE")
        print("-" * 70)
        validation = self.validate_index_coverage(collection_name)

        for item in validation['coverage']:
            query = item['query']
            if item['covered']:
                print(f"  ✓ Query {query} covered by index: {item['index']}")
            else:
                print(f"  ✗ Query {query} MISSING INDEX")

        # Missing indexes
        if validation['missing_indexes']:
            print("\n⚠️  RECOMMENDED INDEXES")
            print("-" * 70)
            for idx in validation['missing_indexes']:
                print(f"  → Add index: {idx}")
                print(f"    Command: db.{collection_name}.createIndex({json.dumps(idx)})")

        # Index usage stats
        usage_stats = self.get_index_usage_stats(collection_name)
        if usage_stats:
            print("\n📈 INDEX USAGE STATISTICS")
            print("-" * 70)
            for stat in usage_stats:
                name = stat['name']
                ops = stat['accesses']['ops']
                since = stat['accesses']['since']
                print(f"  • {name}: {ops} operations since {since}")

                if ops == 0 and name != '_id_':
                    print(f"    ⚠️  UNUSED - Consider removing")

        # Suggestions from slow queries
        suggestions = self.suggest_indexes(collection_name)
        if suggestions:
            print("\n💡 SUGGESTIONS FROM SLOW QUERIES")
            print("-" * 70)
            for suggestion in suggestions:
                print(f"  • Query: {suggestion['query']}")
                print(f"    Execution time: {suggestion['execution_time']} ms")
                print(f"    Suggested index: {suggestion['suggested_index']}")

        print("\n" + "="*70 + "\n")

    def validate_all_collections(self):
        """Validate indexes for all collections"""
        collections = self.db.list_collection_names()
        print(f"\nValidating {len(collections)} collections...\n")

        for coll in collections:
            if not coll.startswith('system.'):
                self.print_report(coll)


def main():
    parser = argparse.ArgumentParser(description='MongoDB Index Validator')
    parser.add_argument('--uri', default='mongodb://localhost:27017/',
                        help='MongoDB connection URI')
    parser.add_argument('--db', required=True,
                        help='Database name')
    parser.add_argument('--collection',
                        help='Collection name (optional if --all is used)')
    parser.add_argument('--all', action='store_true',
                        help='Validate all collections')

    args = parser.parse_args()

    if not args.collection and not args.all:
        parser.error("Either --collection or --all must be specified")

    try:
        validator = IndexValidator(args.uri, args.db)

        if args.all:
            validator.validate_all_collections()
        else:
            validator.print_report(args.collection)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
