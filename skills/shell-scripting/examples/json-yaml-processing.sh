#!/bin/bash
#
# JSON and YAML Processing Examples
#
# Demonstrates using jq and yq for processing structured data.

set -euo pipefail

#============================================================================
# Example 1: Basic JSON Parsing with jq
#============================================================================

example_json_basic() {
    echo "=== Example 1: Basic JSON Parsing ==="

    # Sample JSON
    json='{"name":"Alice","age":30,"city":"New York"}'

    echo "Original JSON:"
    echo "$json" | jq '.'

    # Extract fields
    echo "Name: $(echo "$json" | jq -r '.name')"
    echo "Age: $(echo "$json" | jq -r '.age')"
    echo "City: $(echo "$json" | jq -r '.city')"

    echo
}

#============================================================================
# Example 2: JSON Arrays
#============================================================================

example_json_arrays() {
    echo "=== Example 2: JSON Arrays ==="

    # Sample JSON array
    json='[
        {"name":"Alice","age":30},
        {"name":"Bob","age":25},
        {"name":"Charlie","age":35}
    ]'

    echo "All users:"
    echo "$json" | jq '.[] | .name'

    echo "Users over 26:"
    echo "$json" | jq '.[] | select(.age > 26) | .name'

    echo "Average age:"
    echo "$json" | jq '[.[].age] | add / length'

    echo
}

#============================================================================
# Example 3: Nested JSON
#============================================================================

example_json_nested() {
    echo "=== Example 3: Nested JSON ==="

    # Sample nested JSON
    json='{
        "user": {
            "name": "Alice",
            "contact": {
                "email": "alice@example.com",
                "phone": "555-1234"
            },
            "addresses": [
                {"type":"home","city":"New York"},
                {"type":"work","city":"Boston"}
            ]
        }
    }'

    echo "Email: $(echo "$json" | jq -r '.user.contact.email')"
    echo "Phone: $(echo "$json" | jq -r '.user.contact.phone')"

    echo "Cities:"
    echo "$json" | jq -r '.user.addresses[].city'

    echo "Work city:"
    echo "$json" | jq -r '.user.addresses[] | select(.type=="work") | .city'

    echo
}

#============================================================================
# Example 4: Constructing JSON
#============================================================================

example_json_construct() {
    echo "=== Example 4: Constructing JSON ==="

    # From variables
    name="Alice"
    age=30
    city="New York"

    jq -n \
        --arg name "$name" \
        --argjson age "$age" \
        --arg city "$city" \
        '{name: $name, age: $age, city: $city}'

    # Construct array
    jq -n --arg name1 "Alice" --arg name2 "Bob" \
        '[{name: $name1}, {name: $name2}]'

    echo
}

#============================================================================
# Example 5: JSON Transformation
#============================================================================

example_json_transform() {
    echo "=== Example 5: JSON Transformation ==="

    # Sample input
    input='[
        {"firstName":"Alice","lastName":"Smith"},
        {"firstName":"Bob","lastName":"Jones"}
    ]'

    # Transform structure
    echo "Transformed:"
    echo "$input" | jq '[.[] | {fullName: "\(.firstName) \(.lastName)"}]'

    # Add field
    echo "With ID:"
    echo "$input" | jq '[.[] | . + {id: (.firstName | ascii_downcase)}]'

    echo
}

#============================================================================
# Example 6: YAML Parsing with yq
#============================================================================

example_yaml_basic() {
    echo "=== Example 6: Basic YAML Parsing ==="

    # Create sample YAML file
    cat > /tmp/config.yaml <<EOF
database:
  host: localhost
  port: 5432
  name: mydb
servers:
  - name: web1
    ip: 192.168.1.10
  - name: web2
    ip: 192.168.1.11
EOF

    echo "Database host:"
    yq eval '.database.host' /tmp/config.yaml

    echo "Database port:"
    yq eval '.database.port' /tmp/config.yaml

    echo "Server names:"
    yq eval '.servers[].name' /tmp/config.yaml

    # Cleanup
    rm -f /tmp/config.yaml

    echo
}

#============================================================================
# Example 7: YAML Modification
#============================================================================

example_yaml_modify() {
    echo "=== Example 7: YAML Modification ==="

    # Create sample YAML file
    cat > /tmp/config.yaml <<EOF
version: "1.0"
debug: false
port: 8080
EOF

    echo "Original:"
    cat /tmp/config.yaml

    # Update values
    yq eval '.version = "2.0"' -i /tmp/config.yaml
    yq eval '.debug = true' -i /tmp/config.yaml
    yq eval '.port = 9000' -i /tmp/config.yaml

    echo "Modified:"
    cat /tmp/config.yaml

    # Cleanup
    rm -f /tmp/config.yaml

    echo
}

#============================================================================
# Example 8: YAML to JSON Conversion
#============================================================================

example_yaml_to_json() {
    echo "=== Example 8: YAML to JSON Conversion ==="

    # Create YAML
    cat > /tmp/data.yaml <<EOF
name: Alice
age: 30
hobbies:
  - reading
  - coding
  - hiking
EOF

    echo "YAML:"
    cat /tmp/data.yaml

    echo "JSON:"
    yq eval -o=json /tmp/data.yaml

    # Cleanup
    rm -f /tmp/data.yaml

    echo
}

#============================================================================
# Example 9: Real-World API Processing
#============================================================================

example_api_processing() {
    echo "=== Example 9: Real-World API Processing ==="

    # Simulate API response
    api_response='{
        "status": "success",
        "data": {
            "users": [
                {"id":1,"name":"Alice","active":true},
                {"id":2,"name":"Bob","active":false},
                {"id":3,"name":"Charlie","active":true}
            ],
            "total": 3
        }
    }'

    # Check status
    status=$(echo "$api_response" | jq -r '.status')
    echo "Status: $status"

    if [ "$status" != "success" ]; then
        echo "API request failed"
        return 1
    fi

    # Extract active users
    echo "Active users:"
    echo "$api_response" | jq -r '.data.users[] | select(.active) | .name'

    # Count active users
    active_count=$(echo "$api_response" | jq '[.data.users[] | select(.active)] | length')
    echo "Active user count: $active_count"

    echo
}

#============================================================================
# Example 10: Error Handling
#============================================================================

example_error_handling() {
    echo "=== Example 10: Error Handling ==="

    # Check if jq is installed
    if ! command -v jq >/dev/null 2>&1; then
        echo "Error: jq is required but not installed"
        return 1
    fi

    # Validate JSON
    invalid_json='{"name": "Alice", invalid}'

    echo "Validating invalid JSON:"
    if echo "$invalid_json" | jq empty 2>/dev/null; then
        echo "JSON is valid"
    else
        echo "JSON is invalid (expected)"
    fi

    # Check if field exists
    json='{"name":"Alice"}'

    echo "Checking for email field:"
    if echo "$json" | jq -e '.email' >/dev/null 2>&1; then
        echo "Email field exists"
    else
        echo "Email field missing (expected)"
    fi

    echo
}

#============================================================================
# Example 11: Complex jq Queries
#============================================================================

example_complex_queries() {
    echo "=== Example 11: Complex jq Queries ==="

    # Sample data
    json='[
        {"name":"Alice","dept":"Engineering","salary":100000},
        {"name":"Bob","dept":"Sales","salary":80000},
        {"name":"Charlie","dept":"Engineering","salary":90000},
        {"name":"David","dept":"Sales","salary":85000}
    ]'

    # Group by department
    echo "Average salary by department:"
    echo "$json" | jq -r '
        group_by(.dept) |
        map({
            dept: .[0].dept,
            avg_salary: (map(.salary) | add / length)
        }) |
        .[] |
        "\(.dept): \(.avg_salary)"
    '

    # Top earners
    echo "Top 2 earners:"
    echo "$json" | jq -r 'sort_by(.salary) | reverse | .[0:2] | .[] | "\(.name): \(.salary)"'

    echo
}

#============================================================================
# Main
#============================================================================

main() {
    echo "JSON and YAML Processing Examples"
    echo "=================================="
    echo

    # Check dependencies
    if ! command -v jq >/dev/null 2>&1; then
        echo "Warning: jq not installed, skipping jq examples"
        echo "Install with: brew install jq (macOS) or apt-get install jq (Linux)"
    else
        example_json_basic
        example_json_arrays
        example_json_nested
        example_json_construct
        example_json_transform
        example_api_processing
        example_complex_queries
    fi

    if ! command -v yq >/dev/null 2>&1; then
        echo "Warning: yq not installed, skipping yq examples"
        echo "Install with: brew install yq (macOS)"
    else
        example_yaml_basic
        example_yaml_modify
        example_yaml_to_json
    fi

    example_error_handling

    echo "All examples completed"
}

main "$@"
