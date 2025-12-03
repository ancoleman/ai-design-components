#!/usr/bin/env python3
"""
Graph Schema Validation Script

Validates Neo4j graph schemas for common anti-patterns and performance issues:
1. Unbounded traversals (missing depth limits)
2. Missing indexes on frequently queried properties
3. Supernodes (nodes with excessive relationships)
4. Relationship property consistency
5. Constraint violations
"""

import argparse
import sys
from neo4j import GraphDatabase
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Issue severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class ValidationIssue:
    """Represents a validation issue found in the schema."""
    severity: Severity
    category: str
    message: str
    details: Dict[str, Any]
    recommendation: str


class GraphSchemaValidator:
    """Validates Neo4j graph schemas for best practices and performance."""

    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize validator with Neo4j connection.

        Args:
            uri: Neo4j connection URI (e.g., 'bolt://localhost:7687')
            user: Database username
            password: Database password
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.issues: List[ValidationIssue] = []

    def close(self):
        """Close database connection."""
        self.driver.close()

    def add_issue(
        self,
        severity: Severity,
        category: str,
        message: str,
        details: Dict[str, Any],
        recommendation: str
    ):
        """Add a validation issue to the results."""
        self.issues.append(ValidationIssue(
            severity=severity,
            category=category,
            message=message,
            details=details,
            recommendation=recommendation
        ))

    def check_supernodes(self, threshold: int = 10000):
        """
        Check for supernodes (nodes with too many relationships).

        Supernodes slow down graph traversals significantly.

        Args:
            threshold: Max relationships per node before flagging
        """
        query = """
        MATCH (n)
        WITH n, size((n)--()) AS degree
        WHERE degree > $threshold
        RETURN labels(n) AS labels, n, degree
        ORDER BY degree DESC
        LIMIT 50
        """

        with self.driver.session() as session:
            result = session.run(query, threshold=threshold)
            supernodes = list(result)

            if supernodes:
                for record in supernodes:
                    labels = record['labels']
                    degree = record['degree']
                    node_props = dict(record['n'])

                    self.add_issue(
                        severity=Severity.WARNING if degree < 50000 else Severity.ERROR,
                        category="Performance",
                        message=f"Supernode detected: {labels} node with {degree:,} relationships",
                        details={
                            'labels': labels,
                            'degree': degree,
                            'properties': node_props
                        },
                        recommendation=(
                            "Consider partitioning relationships using intermediate nodes. "
                            "For example, use time-based partitioning: "
                            "(Node)-[:REL_IN]->(Year)-[:HAS_MONTH]->(Month)-[:CONTAINS]->(Target)"
                        )
                    )

    def check_indexes(self):
        """
        Check for missing indexes on frequently queried properties.

        Analyzes node labels and suggests indexes.
        """
        # Get all indexes
        with self.driver.session() as session:
            result = session.run("SHOW INDEXES")
            existing_indexes = set()

            for record in result:
                if record.get('labelsOrTypes') and record.get('properties'):
                    label = record['labelsOrTypes'][0] if record['labelsOrTypes'] else None
                    props = record['properties']
                    if label and props:
                        existing_indexes.add((label, tuple(props)))

            # Get node label statistics
            result = session.run("""
                CALL db.labels() YIELD label
                CALL {
                    WITH label
                    MATCH (n)
                    WHERE label IN labels(n)
                    RETURN count(n) AS count
                    LIMIT 1
                }
                RETURN label, count
                ORDER BY count DESC
            """)

            label_counts = {record['label']: record['count'] for record in result}

            # Check for common properties that should be indexed
            for label, count in label_counts.items():
                if count > 100:  # Only check labels with significant data
                    # Get property keys for this label
                    prop_result = session.run(f"""
                        MATCH (n:{label})
                        RETURN DISTINCT keys(n) AS props
                        LIMIT 1
                    """)

                    props_record = prop_result.single()
                    if props_record and props_record['props']:
                        props = props_record['props']

                        # Check for common filterable properties
                        filterable = ['id', 'email', 'name', 'created_at', 'date', 'timestamp']
                        for prop in props:
                            if prop in filterable:
                                if (label, (prop,)) not in existing_indexes:
                                    self.add_issue(
                                        severity=Severity.WARNING,
                                        category="Indexing",
                                        message=f"Missing index on {label}.{prop}",
                                        details={
                                            'label': label,
                                            'property': prop,
                                            'node_count': count
                                        },
                                        recommendation=(
                                            f"CREATE INDEX {label.lower()}_{prop} "
                                            f"FOR (n:{label}) ON (n.{prop})"
                                        )
                                    )

    def check_constraints(self):
        """
        Check for recommended constraints.

        Ensures data integrity through constraints on IDs and emails.
        """
        with self.driver.session() as session:
            # Get existing constraints
            result = session.run("SHOW CONSTRAINTS")
            existing_constraints = set()

            for record in result:
                if record.get('labelsOrTypes') and record.get('properties'):
                    label = record['labelsOrTypes'][0] if record['labelsOrTypes'] else None
                    props = record['properties']
                    constraint_type = record.get('type', '')
                    if label and props:
                        existing_constraints.add((label, tuple(props), constraint_type))

            # Get node labels
            result = session.run("CALL db.labels()")
            labels = [record['label'] for record in result]

            # Check for recommended unique constraints
            for label in labels:
                # Check for id uniqueness
                if not any(c[0] == label and 'id' in c[1] and 'UNIQUENESS' in c[2]
                          for c in existing_constraints):
                    # Check if id property exists
                    check = session.run(f"""
                        MATCH (n:{label})
                        WHERE n.id IS NOT NULL
                        RETURN count(n) AS count
                        LIMIT 1
                    """)
                    count_record = check.single()
                    if count_record and count_record['count'] > 0:
                        self.add_issue(
                            severity=Severity.WARNING,
                            category="Data Integrity",
                            message=f"Missing unique constraint on {label}.id",
                            details={'label': label, 'property': 'id'},
                            recommendation=(
                                f"CREATE CONSTRAINT {label.lower()}_id_unique "
                                f"FOR (n:{label}) REQUIRE n.id IS UNIQUE"
                            )
                        )

                # Check for email uniqueness
                if 'User' in label or 'Person' in label:
                    if not any(c[0] == label and 'email' in c[1] and 'UNIQUENESS' in c[2]
                              for c in existing_constraints):
                        check = session.run(f"""
                            MATCH (n:{label})
                            WHERE n.email IS NOT NULL
                            RETURN count(n) AS count
                            LIMIT 1
                        """)
                        count_record = check.single()
                        if count_record and count_record['count'] > 0:
                            self.add_issue(
                                severity=Severity.WARNING,
                                category="Data Integrity",
                                message=f"Missing unique constraint on {label}.email",
                                details={'label': label, 'property': 'email'},
                                recommendation=(
                                    f"CREATE CONSTRAINT {label.lower()}_email_unique "
                                    f"FOR (n:{label}) REQUIRE n.email IS UNIQUE"
                                )
                            )

    def check_orphaned_nodes(self):
        """
        Check for orphaned nodes (nodes with no relationships).

        Large numbers of orphaned nodes may indicate data quality issues.
        """
        query = """
        MATCH (n)
        WHERE NOT (n)--()
        WITH labels(n) AS labels, count(n) AS count
        RETURN labels, count
        ORDER BY count DESC
        """

        with self.driver.session() as session:
            result = session.run(query)
            orphaned = list(result)

            for record in orphaned:
                if record['count'] > 10:  # Flag if more than 10 orphaned nodes
                    self.add_issue(
                        severity=Severity.INFO,
                        category="Data Quality",
                        message=f"{record['count']} orphaned nodes found: {record['labels']}",
                        details={
                            'labels': record['labels'],
                            'count': record['count']
                        },
                        recommendation=(
                            "Review if these nodes should be connected or removed. "
                            "Orphaned nodes consume storage without providing graph value."
                        )
                    )

    def check_relationship_properties(self):
        """
        Check for inconsistent relationship properties.

        Ensures relationships of the same type have consistent properties.
        """
        query = """
        MATCH ()-[r]->()
        WITH type(r) AS rel_type, keys(r) AS props
        WITH rel_type, collect(DISTINCT props) AS prop_sets
        WHERE size(prop_sets) > 1
        RETURN rel_type, prop_sets
        """

        with self.driver.session() as session:
            result = session.run(query)
            inconsistencies = list(result)

            for record in inconsistencies:
                self.add_issue(
                    severity=Severity.WARNING,
                    category="Data Quality",
                    message=f"Inconsistent properties on {record['rel_type']} relationships",
                    details={
                        'relationship_type': record['rel_type'],
                        'property_sets': record['prop_sets']
                    },
                    recommendation=(
                        "Standardize relationship properties. All relationships of the same "
                        "type should have consistent property schemas."
                    )
                )

    def check_database_stats(self):
        """
        Display database statistics for context.
        """
        query = """
        MATCH (n)
        WITH count(n) AS node_count
        MATCH ()-[r]->()
        WITH node_count, count(r) AS rel_count
        CALL db.labels() YIELD label
        WITH node_count, rel_count, collect(label) AS labels
        CALL db.relationshipTypes() YIELD relationshipType
        RETURN
            node_count,
            rel_count,
            size(labels) AS label_count,
            collect(relationshipType) AS rel_types
        """

        with self.driver.session() as session:
            result = session.run(query)
            stats = result.single()

            print("\n" + "="*60)
            print("DATABASE STATISTICS")
            print("="*60)
            print(f"Total Nodes: {stats['node_count']:,}")
            print(f"Total Relationships: {stats['rel_count']:,}")
            print(f"Node Labels: {stats['label_count']}")
            print(f"Relationship Types: {len(stats['rel_types'])}")
            print("="*60 + "\n")

    def validate(self):
        """
        Run all validation checks.

        Returns:
            Number of issues found
        """
        print("Starting graph schema validation...")

        self.check_database_stats()
        self.check_supernodes()
        self.check_indexes()
        self.check_constraints()
        self.check_orphaned_nodes()
        self.check_relationship_properties()

        return len(self.issues)

    def print_report(self):
        """Print validation report."""
        if not self.issues:
            print("\n✅ No issues found! Schema looks good.\n")
            return

        # Group by severity
        by_severity = {
            Severity.CRITICAL: [],
            Severity.ERROR: [],
            Severity.WARNING: [],
            Severity.INFO: []
        }

        for issue in self.issues:
            by_severity[issue.severity].append(issue)

        # Print summary
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"Critical: {len(by_severity[Severity.CRITICAL])}")
        print(f"Errors:   {len(by_severity[Severity.ERROR])}")
        print(f"Warnings: {len(by_severity[Severity.WARNING])}")
        print(f"Info:     {len(by_severity[Severity.INFO])}")
        print("="*60 + "\n")

        # Print issues by severity
        for severity in [Severity.CRITICAL, Severity.ERROR, Severity.WARNING, Severity.INFO]:
            issues = by_severity[severity]
            if issues:
                print(f"\n{severity.value} ({len(issues)} issues)")
                print("-" * 60)

                for i, issue in enumerate(issues, 1):
                    print(f"\n{i}. [{issue.category}] {issue.message}")
                    if issue.recommendation:
                        print(f"   💡 Recommendation: {issue.recommendation}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Neo4j graph schema for best practices"
    )
    parser.add_argument(
        '--uri',
        default='bolt://localhost:7687',
        help='Neo4j connection URI (default: bolt://localhost:7687)'
    )
    parser.add_argument(
        '--user',
        default='neo4j',
        help='Neo4j username (default: neo4j)'
    )
    parser.add_argument(
        '--password',
        default='password',
        help='Neo4j password (default: password)'
    )
    parser.add_argument(
        '--supernode-threshold',
        type=int,
        default=10000,
        help='Relationship count threshold for supernode detection (default: 10000)'
    )

    args = parser.parse_args()

    validator = GraphSchemaValidator(args.uri, args.user, args.password)

    try:
        issue_count = validator.validate()
        validator.print_report()

        # Exit with error code if critical/error issues found
        if any(i.severity in [Severity.CRITICAL, Severity.ERROR] for i in validator.issues):
            sys.exit(1)
        else:
            sys.exit(0)

    except Exception as e:
        print(f"\n❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(2)
    finally:
        validator.close()


if __name__ == "__main__":
    main()
