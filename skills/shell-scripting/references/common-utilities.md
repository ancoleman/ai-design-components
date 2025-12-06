# Common Utilities Integration

Guide to integrating common command-line utilities in shell scripts: jq, yq, awk, sed, and more.

## Table of Contents

- [jq: JSON Processing](#jq-json-processing)
- [yq: YAML Processing](#yq-yaml-processing)
- [awk: Text Processing](#awk-text-processing)
- [sed: Stream Editing](#sed-stream-editing)
- [grep: Pattern Matching](#grep-pattern-matching)
- [Other Useful Utilities](#other-useful-utilities)

---

## jq: JSON Processing

### Installation

```bash
# macOS
brew install jq

# Ubuntu/Debian
apt-get install jq

# Fedora/RHEL
dnf install jq

# Docker
docker run --rm -i stedolan/jq
```

### Basic Usage

```bash
# Pretty-print JSON
echo '{"name":"Alice","age":30}' | jq '.'

# Extract field
echo '{"name":"Alice","age":30}' | jq '.name'
# Output: "Alice"

# Extract field without quotes (-r for raw output)
echo '{"name":"Alice","age":30}' | jq -r '.name'
# Output: Alice

# Extract nested field
echo '{"user":{"name":"Alice"}}' | jq '.user.name'
# Output: "Alice"
```

### Working with Arrays

```bash
# Extract array element
echo '["a","b","c"]' | jq '.[0]'
# Output: "a"

# Extract all array elements
echo '["a","b","c"]' | jq '.[]'
# Output: "a" "b" "c" (one per line)

# Array length
echo '["a","b","c"]' | jq 'length'
# Output: 3

# Extract field from each object in array
echo '[{"name":"Alice"},{"name":"Bob"}]' | jq '.[].name'
# Output: "Alice" "Bob"
```

### Filtering and Selecting

```bash
# Filter array by condition
echo '[{"name":"Alice","age":30},{"name":"Bob","age":25}]' | \
    jq '.[] | select(.age > 26)'
# Output: {"name":"Alice","age":30}

# Filter and extract field
echo '[{"name":"Alice","active":true},{"name":"Bob","active":false}]' | \
    jq '.[] | select(.active == true) | .name'
# Output: "Alice"

# Map array
echo '[1,2,3]' | jq 'map(. * 2)'
# Output: [2,4,6]
```

### Constructing JSON

```bash
# Create object
jq -n '{"name": "Alice", "age": 30}'

# Create array
jq -n '["a", "b", "c"]'

# Construct from variables
name="Alice"
age=30
jq -n --arg name "$name" --argjson age "$age" '{"name": $name, "age": $age}'
```

### Practical Examples

```bash
#!/bin/bash

# Parse API response
response=$(curl -sSL https://api.example.com/users)

# Extract specific field
user_id=$(echo "$response" | jq -r '.data.id')

# Check for error
if echo "$response" | jq -e '.error' >/dev/null; then
    error_msg=$(echo "$response" | jq -r '.error.message')
    echo "Error: $error_msg" >&2
    exit 1
fi

# Extract array of values
ids=$(echo "$response" | jq -r '.users[].id')

# Transform JSON
echo "$response" | jq '{
    id: .data.id,
    name: .data.name,
    email: .data.contact.email
}'

# Merge JSON files
jq -s '.[0] * .[1]' file1.json file2.json > merged.json
```

### Error Handling

```bash
#!/bin/bash

# Check if jq is installed
command -v jq >/dev/null 2>&1 || {
    echo "Error: jq is required but not installed" >&2
    exit 1
}

# Validate JSON
if ! echo "$json" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON" >&2
    exit 1
fi

# Check if field exists
if ! echo "$json" | jq -e '.field' >/dev/null 2>&1; then
    echo "Error: Required field missing" >&2
    exit 1
fi
```

---

## yq: YAML Processing

### Installation

```bash
# macOS (yq v4, jq-compatible syntax)
brew install yq

# Ubuntu/Debian
wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
chmod +x yq_linux_amd64
mv yq_linux_amd64 /usr/local/bin/yq

# Docker
docker run --rm -v "$PWD":/workdir mikefarah/yq
```

**Note:** yq v4 uses jq-compatible syntax. yq v3 has different syntax.

### Basic Usage (yq v4)

```bash
# Read YAML
yq eval '.key' config.yaml

# Read nested value
yq eval '.database.host' config.yaml

# Read array element
yq eval '.servers[0]' config.yaml

# Read all array elements
yq eval '.servers[]' config.yaml
```

### Modifying YAML

```bash
# Update value
yq eval '.database.port = 5432' config.yaml

# Update in-place
yq eval '.database.port = 5432' -i config.yaml

# Add new key
yq eval '.newkey = "value"' config.yaml

# Delete key
yq eval 'del(.oldkey)' config.yaml
```

### Converting Formats

```bash
# YAML to JSON
yq eval -o=json config.yaml > config.json

# JSON to YAML
yq eval -P config.json > config.yaml

# YAML to XML
yq eval -o=xml config.yaml

# YAML to properties
yq eval -o=props config.yaml
```

### Practical Examples

```bash
#!/bin/bash

# Read configuration
database_host=$(yq eval '.database.host' config.yaml)
database_port=$(yq eval '.database.port' config.yaml)

# Update configuration
yq eval ".environment = \"$ENV\"" -i config.yaml
yq eval ".version = \"$VERSION\"" -i config.yaml

# Merge YAML files
yq eval-all '. as $item ireduce ({}; . * $item)' file1.yaml file2.yaml

# Extract subset
yq eval '.services.web' docker-compose.yaml > web-service.yaml

# Validate YAML
if ! yq eval '.' config.yaml >/dev/null 2>&1; then
    echo "Error: Invalid YAML" >&2
    exit 1
fi
```

---

## awk: Text Processing

### Basic Usage

```bash
# Print entire line
awk '{print}' file.txt
# Same as: cat file.txt

# Print specific field (space-separated)
awk '{print $1}' file.txt  # First field
awk '{print $2}' file.txt  # Second field
awk '{print $NF}' file.txt # Last field

# Print multiple fields
awk '{print $1, $3}' file.txt

# Custom field separator
awk -F',' '{print $1}' file.csv  # CSV
awk -F':' '{print $1}' /etc/passwd  # Colon-separated
```

### Pattern Matching

```bash
# Print lines matching pattern
awk '/pattern/' file.txt

# Print lines NOT matching pattern
awk '!/pattern/' file.txt

# Print lines where field matches
awk '$3 == "value"' file.txt
awk '$2 > 100' file.txt
awk '$1 ~ /^prefix/' file.txt  # Regex match
```

### Arithmetic Operations

```bash
# Sum column
awk '{sum += $1} END {print sum}' numbers.txt

# Average
awk '{sum += $1; count++} END {print sum/count}' numbers.txt

# Min/Max
awk 'NR==1 {max=$1; min=$1} {if($1>max) max=$1; if($1<min) min=$1} END {print min, max}' numbers.txt

# Count occurrences
awk '{count[$1]++} END {for (word in count) print word, count[word]}' file.txt
```

### Practical Examples

```bash
#!/bin/bash

# Extract specific columns from CSV
awk -F',' '{print $2, $5}' data.csv

# Filter and process
awk -F',' '$3 > 100 {print $1, $2}' data.csv

# Calculate totals
total=$(awk '{sum += $1} END {print sum}' sales.txt)

# Format output
awk '{printf "Name: %-20s Age: %3d\n", $1, $2}' people.txt

# Process log file
awk '/ERROR/ {print $1, $2, $NF}' application.log

# Group and sum
awk '{sum[$1] += $2} END {for (key in sum) print key, sum[key]}' data.txt
```

---

## sed: Stream Editing

### Basic Usage

```bash
# Substitute pattern
sed 's/old/new/' file.txt  # First occurrence per line
sed 's/old/new/g' file.txt  # All occurrences

# In-place editing
sed -i 's/old/new/g' file.txt       # Linux
sed -i '' 's/old/new/g' file.txt    # macOS
```

### Pattern Matching

```bash
# Delete lines matching pattern
sed '/pattern/d' file.txt

# Delete empty lines
sed '/^$/d' file.txt

# Print only lines matching pattern
sed -n '/pattern/p' file.txt

# Print line range
sed -n '10,20p' file.txt  # Lines 10-20
sed -n '10p' file.txt     # Line 10 only
```

### Advanced Substitution

```bash
# Case-insensitive substitution
sed 's/pattern/replacement/gi' file.txt

# Substitute with backreferences
sed 's/\(.*\)@\(.*\)/\2: \1/' emails.txt
# Input: user@example.com
# Output: example.com: user

# Multiple substitutions
sed -e 's/old1/new1/g' -e 's/old2/new2/g' file.txt

# Substitute on specific line
sed '5s/old/new/' file.txt  # Only line 5
```

### Insertion and Deletion

```bash
# Insert line before pattern
sed '/pattern/i\New line' file.txt

# Insert line after pattern
sed '/pattern/a\New line' file.txt

# Delete lines
sed '5d' file.txt          # Delete line 5
sed '5,10d' file.txt       # Delete lines 5-10
sed '/pattern/d' file.txt  # Delete matching lines
```

### Practical Examples

```bash
#!/bin/bash

# Replace config values
sed -i "s/^PORT=.*/PORT=$NEW_PORT/" config.env

# Remove comments
sed 's/#.*//' file.txt

# Extract email addresses
sed -n 's/.*\([a-z0-9._%+-]\+@[a-z0-9.-]\+\.[a-z]\{2,\}\).*/\1/p' file.txt

# Remove trailing whitespace
sed 's/[[:space:]]*$//' file.txt

# Double-space file
sed G file.txt

# Portable in-place editing
sed 's/old/new/g' file.txt > file.txt.tmp && mv file.txt.tmp file.txt
```

---

## grep: Pattern Matching

### Basic Usage

```bash
# Search for pattern
grep "pattern" file.txt

# Case-insensitive search
grep -i "pattern" file.txt

# Invert match (lines NOT matching)
grep -v "pattern" file.txt

# Count matches
grep -c "pattern" file.txt

# Show line numbers
grep -n "pattern" file.txt
```

### Regular Expressions

```bash
# Extended regex (-E)
grep -E "pattern1|pattern2" file.txt

# Beginning of line
grep "^pattern" file.txt

# End of line
grep "pattern$" file.txt

# Word boundaries
grep "\bword\b" file.txt

# Character classes
grep "[0-9]" file.txt       # Any digit
grep "[a-z]" file.txt       # Any lowercase letter
grep "[^0-9]" file.txt      # Any non-digit
```

### Context and Output

```bash
# Show context (lines before/after)
grep -A 3 "pattern" file.txt  # 3 lines after
grep -B 3 "pattern" file.txt  # 3 lines before
grep -C 3 "pattern" file.txt  # 3 lines before and after

# Show only matched text
grep -o "pattern" file.txt

# Quiet mode (exit code only)
grep -q "pattern" file.txt
if [ $? -eq 0 ]; then
    echo "Pattern found"
fi
```

### Practical Examples

```bash
#!/bin/bash

# Check if file contains pattern
if grep -q "ERROR" logfile.txt; then
    echo "Errors found in log"
fi

# Extract lines with email addresses
grep -Eo "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" file.txt

# Find files containing pattern
grep -r "pattern" directory/

# Exclude files/directories
grep -r "pattern" --exclude="*.log" directory/
grep -r "pattern" --exclude-dir="node_modules" directory/

# Count occurrences
count=$(grep -c "ERROR" logfile.txt)
echo "Found $count errors"
```

---

## Other Useful Utilities

### cut: Extract Fields

```bash
# Extract specific field
cut -d',' -f1 file.csv     # First field (comma-separated)
cut -d':' -f1,3 /etc/passwd # Fields 1 and 3

# Extract character range
cut -c1-10 file.txt        # Characters 1-10
```

### sort: Sort Lines

```bash
# Sort alphabetically
sort file.txt

# Sort numerically
sort -n numbers.txt

# Reverse sort
sort -r file.txt

# Sort by specific field
sort -t',' -k2 file.csv    # Sort by 2nd field (CSV)

# Unique sort
sort -u file.txt           # Same as: sort file.txt | uniq
```

### uniq: Remove Duplicates

```bash
# Remove adjacent duplicates
uniq file.txt

# Count occurrences
uniq -c file.txt

# Show only duplicates
uniq -d file.txt

# Show only unique lines
uniq -u file.txt
```

### tr: Translate Characters

```bash
# Uppercase
echo "hello" | tr '[:lower:]' '[:upper:]'
# Output: HELLO

# Delete characters
echo "hello123" | tr -d '[:digit:]'
# Output: hello

# Squeeze repeats
echo "hello   world" | tr -s ' '
# Output: hello world

# Replace characters
echo "hello" | tr 'el' 'ip'
# Output: hippo
```

### find: Find Files

```bash
# Find by name
find . -name "*.txt"

# Find by type
find . -type f             # Files
find . -type d             # Directories

# Find and execute
find . -name "*.log" -delete
find . -name "*.sh" -exec chmod +x {} \;

# Find modified recently
find . -mtime -7           # Modified in last 7 days
```

### xargs: Build Command Lines

```bash
# Process find results
find . -name "*.txt" | xargs grep "pattern"

# Parallel execution
find . -name "*.jpg" | xargs -P 4 -I {} convert {} {}.png

# Handle spaces in filenames
find . -name "*.txt" -print0 | xargs -0 grep "pattern"
```

---

## Summary

**JSON Processing:**
- jq for parsing and transforming JSON
- Use -r for raw output
- Use -e to check existence

**YAML Processing:**
- yq v4 for YAML (jq-compatible syntax)
- Convert between YAML, JSON, XML
- Modify YAML in-place

**Text Processing:**
- awk for field extraction and calculations
- sed for pattern replacement and editing
- grep for pattern matching

**Utilities:**
- cut: Extract fields
- sort: Sort lines
- uniq: Remove duplicates
- tr: Character translation
- find: Find files
- xargs: Build commands

**Best Practices:**
- Check command availability before use
- Handle errors gracefully
- Quote variables
- Use appropriate tool for task
