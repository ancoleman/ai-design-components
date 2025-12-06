# Parameter Expansion and String Manipulation

Complete reference for parameter expansion, string manipulation, and array handling in shell scripts.

## Table of Contents

- [Basic Parameter Expansion](#basic-parameter-expansion)
- [Default Values and Assignments](#default-values-and-assignments)
- [String Length](#string-length)
- [Substring Extraction](#substring-extraction)
- [Pattern Removal (Prefix/Suffix)](#pattern-removal-prefixsuffix)
- [Pattern Replacement](#pattern-replacement)
- [Case Modification](#case-modification)
- [Array Handling (Bash)](#array-handling-bash)
- [Associative Arrays (Bash)](#associative-arrays-bash)
- [POSIX-Compliant Alternatives](#posix-compliant-alternatives)

---

## Basic Parameter Expansion

### Simple Expansion

```bash
#!/bin/bash

# Basic variable expansion
name="Alice"
echo "$name"          # Output: Alice
echo "${name}"        # Output: Alice (same, explicit braces)

# Concatenation
first="John"
last="Doe"
full="$first $last"   # Output: John Doe
echo "${first}_${last}"  # Output: John_Doe
```

### Brace Expansion vs Variable Expansion

```bash
#!/bin/bash

# Variable expansion
files="file1 file2 file3"
echo $files           # Output: file1 file2 file3

# Brace expansion (generates sequences)
echo file{1,2,3}      # Output: file1 file2 file3
echo {a..z}           # Output: a b c ... z
echo {1..10}          # Output: 1 2 3 ... 10
```

---

## Default Values and Assignments

### Use Default if Unset

```bash
#!/bin/bash

# ${var:-default} - Use default if var is unset or null
echo "${UNDEFINED:-default}"     # Output: default
echo "${EMPTY:-default}"         # Output: default (if EMPTY="")

# Practical example
PORT="${PORT:-8080}"
echo "Server port: $PORT"

# Multiple levels
CONFIG_FILE="${CONFIG_FILE:-${HOME}/.config/app.conf}"
```

### Assign Default if Unset

```bash
#!/bin/bash

# ${var:=default} - Assign default if var is unset or null
: "${PORT:=8080}"
echo "Port: $PORT"  # PORT is now set to 8080

# Common pattern for configuration
: "${LOG_LEVEL:=info}"
: "${DATABASE_HOST:=localhost}"
: "${DATABASE_PORT:=5432}"

echo "Log level: $LOG_LEVEL"
echo "Database: $DATABASE_HOST:$DATABASE_PORT"
```

### Error if Unset

```bash
#!/bin/bash

# ${var:?message} - Exit with error if var is unset or null
: "${API_KEY:?Error: API_KEY environment variable is required}"

# Custom error message
: "${DATABASE_URL:?Error: DATABASE_URL must be set}"

# Practical example
validate_required() {
    : "${INPUT_FILE:?Error: INPUT_FILE is required}"
    : "${OUTPUT_DIR:?Error: OUTPUT_DIR is required}"
}

validate_required
```

### Use Alternative if Set

```bash
#!/bin/bash

# ${var:+alternative} - Use alternative if var is set and not null
DEBUG="${DEBUG:+--verbose}"
echo "Running with $DEBUG"

# Practical example
DOCKER_ARGS=""
DOCKER_ARGS+="${PRIVILEGED:+ --privileged}"
DOCKER_ARGS+="${NETWORK:+ --network=$NETWORK}"
DOCKER_ARGS+="${VOLUME:+ -v $VOLUME}"

docker run $DOCKER_ARGS image_name
```

---

## String Length

```bash
#!/bin/bash

# ${#var} - Length of variable
name="Alice"
echo "${#name}"       # Output: 5

path="/usr/local/bin"
echo "${#path}"       # Output: 14

# Check if empty
if [ "${#INPUT_FILE}" -eq 0 ]; then
    echo "INPUT_FILE is empty"
fi

# Validate length
PASSWORD="secret123"
if [ "${#PASSWORD}" -lt 8 ]; then
    echo "Error: Password must be at least 8 characters"
fi
```

---

## Substring Extraction

### Basic Extraction

```bash
#!/bin/bash

# ${var:offset} - Extract from offset to end
text="Hello, World!"
echo "${text:7}"      # Output: World!

# ${var:offset:length} - Extract substring
echo "${text:0:5}"    # Output: Hello
echo "${text:7:5}"    # Output: World
```

### Negative Offsets (Bash 4.2+)

```bash
#!/bin/bash

# Extract from end
text="Hello, World!"
echo "${text: -6}"    # Output: World! (note space after colon)
echo "${text: -6:5}"  # Output: World

# Without space (POSIX alternative)
echo "${text:${#text}-6}"  # Output: World!
```

### Practical Examples

```bash
#!/bin/bash

# Extract file extension
filename="document.tar.gz"
extension="${filename:${#filename}-3}"  # Output: .gz

# Extract directory from path
path="/usr/local/bin/myapp"
dirname="${path:0:${#path}-6}"  # Output: /usr/local/bin

# Extract first N characters
uuid="550e8400-e29b-41d4-a716-446655440000"
short_id="${uuid:0:8}"  # Output: 550e8400
```

---

## Pattern Removal (Prefix/Suffix)

### Remove Shortest Match

```bash
#!/bin/bash

# ${var#pattern} - Remove shortest prefix match
path="/usr/local/bin/myapp"
echo "${path#*/}"     # Output: usr/local/bin/myapp (remove first /)

# ${var%pattern} - Remove shortest suffix match
filename="report.csv.gz"
echo "${filename%.gz}"     # Output: report.csv
echo "${filename%.*}"      # Output: report.csv (remove .gz)
```

### Remove Longest Match

```bash
#!/bin/bash

# ${var##pattern} - Remove longest prefix match
path="/usr/local/bin/myapp"
echo "${path##*/}"    # Output: myapp (basename)

email="user@example.com"
echo "${email##*@}"   # Output: example.com (domain)

# ${var%%pattern} - Remove longest suffix match
filename="report.csv.gz"
echo "${filename%%.*}"     # Output: report (remove all extensions)

path="/usr/local/bin/myapp"
echo "${path%%/*}"         # Output: (empty, removes everything after first /)
```

### Practical Examples

```bash
#!/bin/bash

# Get filename without extension
file="document.tar.gz"
name="${file%%.*}"         # Output: document (all extensions)
name="${file%.*}"          # Output: document.tar (last extension only)

# Get basename (filename without path)
path="/usr/local/bin/myapp"
basename="${path##*/}"     # Output: myapp

# Get dirname (path without filename)
dirname="${path%/*}"       # Output: /usr/local/bin

# Extract domain from email
email="user@example.com"
domain="${email##*@}"      # Output: example.com

# Extract username from email
username="${email%%@*}"    # Output: user

# Remove protocol from URL
url="https://example.com/path"
no_protocol="${url#*://}"  # Output: example.com/path
```

---

## Pattern Replacement

### Replace First Match

```bash
#!/bin/bash

# ${var/pattern/replacement} - Replace first match
text="hello world world"
echo "${text/world/universe}"  # Output: hello universe world
```

### Replace All Matches

```bash
#!/bin/bash

# ${var//pattern/replacement} - Replace all matches
text="hello world world"
echo "${text//world/universe}"  # Output: hello universe universe

# Remove all occurrences (empty replacement)
path="/usr//local//bin"
echo "${path//\/\//\/}"         # Output: /usr/local/bin (normalize path)

# Replace spaces with underscores
filename="My Document.txt"
echo "${filename// /_}"         # Output: My_Document.txt
```

### Replace Prefix/Suffix Only

```bash
#!/bin/bash

# ${var/#pattern/replacement} - Replace if matches prefix
url="http://example.com"
echo "${url/#http:/https:}"    # Output: https://example.com

# ${var/%pattern/replacement} - Replace if matches suffix
file="document.txt"
echo "${file/%.txt/.md}"       # Output: document.md
```

### Practical Examples

```bash
#!/bin/bash

# Sanitize filename
filename="My Document (Copy).txt"
safe="${filename// /_}"          # Replace spaces
safe="${safe//[()]/}"            # Remove parentheses
safe="${safe//_-_/-}"            # Normalize separators
echo "$safe"  # Output: My_Document_Copy.txt

# Convert path separators (Windows to Unix)
winpath="C:\\Users\\Alice\\Documents"
unixpath="${winpath//\\//}"
echo "$unixpath"  # Output: C:/Users/Alice/Documents

# URL encoding (simple example)
text="hello world"
encoded="${text// /%20}"
echo "$encoded"  # Output: hello%20world
```

---

## Case Modification

### Uppercase/Lowercase (Bash 4+)

```bash
#!/bin/bash

# ${var^^} - Convert to uppercase
name="alice"
echo "${name^^}"      # Output: ALICE

# ${var,,} - Convert to lowercase
name="ALICE"
echo "${name,,}"      # Output: alice

# ${var^} - Uppercase first character only
name="alice"
echo "${name^}"       # Output: Alice

# ${var,} - Lowercase first character only
name="ALICE"
echo "${name,}"       # Output: aLICE
```

### Pattern-Based Case Modification

```bash
#!/bin/bash

# ${var^^pattern} - Uppercase matching pattern
text="hello world"
echo "${text^^[hw]}"  # Output: Hello World

# ${var,,pattern} - Lowercase matching pattern
text="HELLO WORLD"
echo "${text,,[HW]}"  # Output: hELLO wORLD
```

### POSIX-Compliant Alternatives

```bash
#!/bin/sh

# Uppercase using tr
name="alice"
upper=$(echo "$name" | tr '[:lower:]' '[:upper:]')
echo "$upper"  # Output: ALICE

# Lowercase using tr
name="ALICE"
lower=$(echo "$name" | tr '[:upper:]' '[:lower:]')
echo "$lower"  # output: alice

# Capitalize first letter (POSIX)
name="alice"
first=$(echo "$name" | cut -c1 | tr '[:lower:]' '[:upper:]')
rest=$(echo "$name" | cut -c2-)
capitalized="${first}${rest}"
echo "$capitalized"  # Output: Alice
```

---

## Array Handling (Bash)

### Array Basics

```bash
#!/bin/bash

# Declare array
files=("file1.txt" "file2.txt" "file3.txt")

# Access elements
echo "${files[0]}"      # Output: file1.txt (first element)
echo "${files[1]}"      # Output: file2.txt
echo "${files[-1]}"     # Output: file3.txt (last element, Bash 4.2+)

# All elements
echo "${files[@]}"      # Output: file1.txt file2.txt file3.txt
echo "${files[*]}"      # Output: file1.txt file2.txt file3.txt

# Array length
echo "${#files[@]}"     # Output: 3

# Element length
echo "${#files[0]}"     # Output: 9 (length of "file1.txt")
```

### Array Manipulation

```bash
#!/bin/bash

# Append to array
files=("file1.txt")
files+=("file2.txt")
files+=("file3.txt")

# Prepend to array
files=("file0.txt" "${files[@]}")

# Insert at specific position (replace element)
files[1]="new_file.txt"

# Remove element (unset)
unset 'files[1]'

# Reassign indices (compact array after unset)
files=("${files[@]}")
```

### Iterating Arrays

```bash
#!/bin/bash

files=("file1.txt" "file2.txt" "file3.txt")

# Iterate over elements
for file in "${files[@]}"; do
    echo "Processing: $file"
done

# Iterate with indices
for i in "${!files[@]}"; do
    echo "Index $i: ${files[$i]}"
done

# C-style loop
for ((i=0; i<${#files[@]}; i++)); do
    echo "File $i: ${files[$i]}"
done
```

### Array Slicing

```bash
#!/bin/bash

files=("file1" "file2" "file3" "file4" "file5")

# Extract slice: ${array[@]:offset:length}
echo "${files[@]:1:3}"   # Output: file2 file3 file4
echo "${files[@]:2}"     # Output: file3 file4 file5 (from index 2 to end)

# Copy array
files_copy=("${files[@]}")

# Subset matching pattern
matching=("${files[@]/*2*/}")  # Elements containing "2"
```

### Practical Examples

```bash
#!/bin/bash

# Collect files matching pattern
png_files=(*.png)
if [ ${#png_files[@]} -eq 0 ]; then
    echo "No PNG files found"
fi

# Process multiple inputs
process_files() {
    local files=("$@")

    for file in "${files[@]}"; do
        echo "Processing: $file"
        # Process file
    done
}

process_files "${png_files[@]}"

# Split string into array
IFS=',' read -ra items <<< "item1,item2,item3"
for item in "${items[@]}"; do
    echo "Item: $item"
done
```

---

## Associative Arrays (Bash)

### Declare and Use

```bash
#!/bin/bash

# Declare associative array
declare -A config

# Assign values
config[host]="localhost"
config[port]="8080"
config[database]="mydb"

# Access values
echo "${config[host]}"      # Output: localhost
echo "${config[port]}"      # Output: 8080

# Check if key exists
if [ -n "${config[host]:-}" ]; then
    echo "Host is configured"
fi

# Delete key
unset 'config[port]'
```

### Iterate Associative Arrays

```bash
#!/bin/bash

declare -A config=(
    [host]="localhost"
    [port]="8080"
    [database]="mydb"
)

# Iterate over keys
for key in "${!config[@]}"; do
    echo "$key = ${config[$key]}"
done

# Iterate over values
for value in "${config[@]}"; do
    echo "Value: $value"
done
```

### Practical Examples

```bash
#!/bin/bash

# Configuration map
declare -A settings=(
    [log_level]="info"
    [max_connections]="100"
    [timeout]="30"
)

# Function using associative array
get_setting() {
    local key=$1
    local default=$2
    echo "${settings[$key]:-$default}"
}

log_level=$(get_setting "log_level" "warn")
echo "Log level: $log_level"

# Count occurrences
declare -A counts
while read -r line; do
    ((counts[$line]++))
done < data.txt

for key in "${!counts[@]}"; do
    echo "$key: ${counts[$key]}"
done
```

---

## POSIX-Compliant Alternatives

### Simulating Arrays in POSIX sh

```sh
#!/bin/sh

# Space-separated list (simple cases)
files="file1.txt file2.txt file3.txt"

for file in $files; do
    echo "Processing: $file"
done

# Using positional parameters as array
set -- "item1" "item2" "item3"
echo "$1"  # Output: item1
echo "$2"  # Output: item2
echo "$#"  # Output: 3 (number of items)

# Iterate
for item in "$@"; do
    echo "Item: $item"
done
```

### String Operations Without Parameter Expansion

```sh
#!/bin/sh

# Remove prefix using sed
path="/usr/local/bin/myapp"
basename=$(echo "$path" | sed 's|.*/||')
echo "$basename"  # Output: myapp

# Remove suffix using sed
filename="document.txt"
name=$(echo "$filename" | sed 's/\.[^.]*$//')
echo "$name"  # Output: document

# Replace pattern using sed
text="hello world"
replaced=$(echo "$text" | sed 's/world/universe/')
echo "$replaced"  # Output: hello universe

# Uppercase using tr
name="alice"
upper=$(echo "$name" | tr '[:lower:]' '[:upper:]')
echo "$upper"  # Output: ALICE
```

---

## Summary

**Bash Features:**
- Parameter expansion provides powerful string manipulation
- Arrays and associative arrays for structured data
- Case modification (Bash 4+)
- Substring extraction and pattern replacement

**POSIX Alternatives:**
- Use external tools: sed, awk, tr, cut
- Positional parameters as simple arrays
- More verbose but portable

**Best Practices:**
- Use parameter expansion for simple operations
- Use external tools for complex transformations
- Quote all expansions: `"${var}"` not `$var`
- Use arrays (Bash) for multiple values, not space-separated strings
