#!/usr/bin/env python3
"""
Interactive Severity Classifier

Guides users through severity classification using impact and urgency criteria.
Helps teams consistently classify incidents as SEV0, SEV1, SEV2, or SEV3.

Usage:
    python classify-severity.py

Requirements:
    - Python 3.7+
    - No external dependencies (uses only standard library)
"""

import sys
from typing import Optional


class SeverityClassifier:
    """Interactive severity classification tool."""

    def __init__(self):
        self.answers = {}

    def clear_screen(self):
        """Clear terminal screen (cross-platform)."""
        print("\n" * 2)

    def print_header(self):
        """Print tool header."""
        print("=" * 70)
        print("                 INCIDENT SEVERITY CLASSIFIER")
        print("=" * 70)
        print()
        print("Answer the following questions to determine incident severity.")
        print("Be honest and conservative - when in doubt, choose higher severity.")
        print()

    def ask_yes_no(self, question: str) -> bool:
        """Ask a yes/no question and return boolean."""
        while True:
            response = input(f"{question} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please answer 'y' or 'n'")

    def ask_percentage(self, question: str) -> int:
        """Ask for a percentage (0-100) and return integer."""
        while True:
            try:
                response = input(f"{question} (0-100): ").strip()
                value = int(response)
                if 0 <= value <= 100:
                    return value
                else:
                    print("Please enter a number between 0 and 100")
            except ValueError:
                print("Please enter a valid number")

    def ask_choice(self, question: str, choices: list) -> str:
        """Ask a multiple choice question and return selected choice."""
        print(f"\n{question}")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")

        while True:
            try:
                response = input(f"Select 1-{len(choices)}: ").strip()
                index = int(response) - 1
                if 0 <= index < len(choices):
                    return choices[index]
                else:
                    print(f"Please select a number between 1 and {len(choices)}")
            except ValueError:
                print("Please enter a valid number")

    def classify(self) -> str:
        """Run classification questionnaire and return severity."""
        self.clear_screen()
        self.print_header()

        # Question 1: Production down?
        print("QUESTION 1: Production Status")
        print("-" * 70)
        prod_down = self.ask_yes_no(
            "Is production COMPLETELY down or is critical data at risk?"
        )
        self.answers['prod_down'] = prod_down

        if prod_down:
            print("\n→ This indicates SEV0 (Critical Outage)")
            return "SEV0"

        # Question 2: Customer impact percentage
        print("\n\nQUESTION 2: Customer Impact")
        print("-" * 70)
        customer_pct = self.ask_percentage(
            "What percentage of customers are affected?"
        )
        self.answers['customer_pct'] = customer_pct

        # Question 3: Core functionality impacted?
        print("\n\nQUESTION 3: Functionality Impact")
        print("-" * 70)
        functionality = self.ask_choice(
            "Which functionality is impacted?",
            [
                "Core revenue-generating feature (e.g., checkout, payments)",
                "Important feature (e.g., search, notifications)",
                "Non-critical feature (e.g., analytics, reports)",
                "Cosmetic or internal-only (e.g., UI glitch, admin tool)"
            ]
        )
        self.answers['functionality'] = functionality

        # Question 4: Workaround available?
        print("\n\nQUESTION 4: Workaround Availability")
        print("-" * 70)
        has_workaround = self.ask_yes_no(
            "Is there a reasonable workaround available for customers?"
        )
        self.answers['workaround'] = has_workaround

        # Question 5: Revenue impact?
        print("\n\nQUESTION 5: Revenue Impact")
        print("-" * 70)
        revenue_impact = self.ask_yes_no(
            "Is revenue actively being lost due to this issue?"
        )
        self.answers['revenue_impact'] = revenue_impact

        # Question 6: Urgency
        print("\n\nQUESTION 6: Urgency")
        print("-" * 70)
        urgency = self.ask_choice(
            "How urgent is this issue?",
            [
                "Extremely urgent - getting worse rapidly",
                "Urgent - stable but significant",
                "Moderate - noticeable but contained",
                "Low - minor or scheduled fix acceptable"
            ]
        )
        self.answers['urgency'] = urgency

        # Classification logic
        return self._determine_severity()

    def _determine_severity(self) -> str:
        """Determine severity based on collected answers."""
        prod_down = self.answers['prod_down']
        customer_pct = self.answers['customer_pct']
        functionality = self.answers['functionality']
        has_workaround = self.answers['workaround']
        revenue_impact = self.answers['revenue_impact']
        urgency = self.answers['urgency']

        # SEV0: Critical outage
        if prod_down:
            return "SEV0"

        # SEV0: Core functionality + high impact + no workaround
        if (functionality == "Core revenue-generating feature (e.g., checkout, payments)"
                and customer_pct > 25
                and not has_workaround):
            return "SEV0"

        # SEV0: Active revenue loss + high customer impact
        if revenue_impact and customer_pct > 50:
            return "SEV0"

        # SEV1: Major functionality degraded
        if customer_pct > 25 or revenue_impact:
            if "Core revenue" in functionality or "Important feature" in functionality:
                if urgency in ["Extremely urgent - getting worse rapidly",
                               "Urgent - stable but significant"]:
                    return "SEV1"

        # SEV1: High customer impact even with workaround
        if customer_pct > 50:
            return "SEV1"

        # SEV2: Moderate impact
        if customer_pct > 5:
            return "SEV2"

        # SEV2: Non-critical but affecting customers
        if "Non-critical feature" in functionality and customer_pct > 0:
            return "SEV2"

        # SEV3: Low impact
        return "SEV3"

    def explain_severity(self, severity: str):
        """Explain the determined severity and provide guidance."""
        print("\n\n" + "=" * 70)
        print(f"                     RESULT: {severity}")
        print("=" * 70)

        explanations = {
            "SEV0": {
                "definition": "Critical Outage",
                "impact": "Complete service outage or critical data loss",
                "response": "Page all hands immediately, 24/7",
                "escalation": "Executive notification required",
                "communication": "Status updates every 15 minutes",
                "examples": [
                    "API completely down",
                    "Payment processing broken",
                    "Database unavailable",
                    "Active security breach"
                ]
            },
            "SEV1": {
                "definition": "Major Degradation",
                "impact": "Major functionality degraded, significant customer impact",
                "response": "Page on-call during business hours, escalate off-hours",
                "escalation": "Team lead notification, IC assigned",
                "communication": "Status updates every 30 minutes",
                "examples": [
                    "15% API error rate",
                    "Critical feature unavailable",
                    "Severe performance degradation",
                    "Authentication issues"
                ]
            },
            "SEV2": {
                "definition": "Minor Issues",
                "impact": "Minor functionality impaired, small customer subset affected",
                "response": "Email/Slack alert, next business day response",
                "escalation": "Standard on-call response",
                "communication": "Status updates at major milestones",
                "examples": [
                    "Edge case bug",
                    "Non-critical feature slow",
                    "UI rendering issue on specific browser",
                    "Export feature timeout"
                ]
            },
            "SEV3": {
                "definition": "Low Impact",
                "impact": "Cosmetic issues, low-impact bugs, no customer functionality affected",
                "response": "Create ticket, no immediate notification",
                "escalation": "None required",
                "communication": "None required",
                "examples": [
                    "Button color wrong",
                    "Tooltip typo",
                    "Log formatting incorrect",
                    "Documentation outdated"
                ]
            }
        }

        info = explanations[severity]

        print(f"\nDefinition: {info['definition']}")
        print(f"Impact: {info['impact']}")
        print()
        print("RESPONSE REQUIREMENTS:")
        print(f"  • Response: {info['response']}")
        print(f"  • Escalation: {info['escalation']}")
        print(f"  • Communication: {info['communication']}")
        print()
        print("EXAMPLES OF THIS SEVERITY:")
        for example in info['examples']:
            print(f"  • {example}")
        print()

    def show_summary(self):
        """Show summary of answers provided."""
        print("\n" + "=" * 70)
        print("                        SUMMARY OF ANSWERS")
        print("=" * 70)
        print()
        print(f"Production completely down: {self.answers.get('prod_down', 'N/A')}")
        print(f"Customers affected: {self.answers.get('customer_pct', 'N/A')}%")
        print(f"Functionality impacted: {self.answers.get('functionality', 'N/A')}")
        print(f"Workaround available: {self.answers.get('workaround', 'N/A')}")
        print(f"Revenue impact: {self.answers.get('revenue_impact', 'N/A')}")
        print(f"Urgency level: {self.answers.get('urgency', 'N/A')}")

    def provide_recommendations(self, severity: str):
        """Provide actionable recommendations based on severity."""
        print("\n" + "=" * 70)
        print("                        RECOMMENDED ACTIONS")
        print("=" * 70)
        print()

        if severity == "SEV0":
            print("IMMEDIATE ACTIONS:")
            print("  1. Declare incident in Slack channel immediately")
            print("  2. Page all on-call engineers and team leads")
            print("  3. Assign Incident Commander (IC)")
            print("  4. Assign Communications Lead")
            print("  5. Update status page: 'Investigating'")
            print("  6. Notify executives within 15 minutes")
            print()
            print("Commands to run:")
            print("  /incident-declare SEV0 [brief description]")
            print("  # Post in status page: 'Investigating service outage'")

        elif severity == "SEV1":
            print("IMMEDIATE ACTIONS:")
            print("  1. Declare incident in Slack channel")
            print("  2. Page primary on-call engineer")
            print("  3. Assign Incident Commander (IC)")
            print("  4. Update status page: 'Investigating'")
            print("  5. Post status update every 30 minutes")
            print()
            print("Commands to run:")
            print("  /incident-declare SEV1 [brief description]")

        elif severity == "SEV2":
            print("RECOMMENDED ACTIONS:")
            print("  1. Create incident ticket")
            print("  2. Notify on-call via Slack")
            print("  3. Update status page if customer-visible")
            print("  4. Plan fix for next business day")
            print()
            print("Commands to run:")
            print("  # Create Jira/GitHub issue")
            print("  # Post in #on-call: '@oncall SEV2 issue detected...'")

        else:  # SEV3
            print("RECOMMENDED ACTIONS:")
            print("  1. Create ticket in backlog")
            print("  2. No immediate notification required")
            print("  3. Address in next sprint")
            print()
            print("Commands to run:")
            print("  # Create Jira/GitHub issue")
            print("  # Label: priority=low")

        print()

    def run(self):
        """Run the full classification workflow."""
        try:
            severity = self.classify()
            self.show_summary()
            self.explain_severity(severity)
            self.provide_recommendations(severity)

            print("\n" + "=" * 70)
            print("Classification complete!")
            print()
            print("Next steps:")
            print("  1. Declare incident if SEV0/SEV1")
            print("  2. Follow incident response runbooks")
            print("  3. Update stakeholders per severity guidelines")
            print("=" * 70)
            print()

        except KeyboardInterrupt:
            print("\n\nClassification cancelled.")
            sys.exit(0)


def main():
    """Main entry point."""
    classifier = SeverityClassifier()
    classifier.run()


if __name__ == "__main__":
    main()
