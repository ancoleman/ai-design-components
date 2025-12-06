# Shell Portability Guide: POSIX sh vs Bash

Comprehensive guide to writing portable shell scripts and understanding differences between POSIX sh and Bash.

## Table of Contents

- [Decision Framework](#decision-framework)
- [POSIX sh Features](#posix-sh-features)
- [Bash-Specific Features](#bash-specific-features)
- [Common Bashisms and Alternatives](#common-bashisms-and-alternatives)
- [Platform Differences](#platform-differences)
- [Testing for Portability](#testing-for-portability)
- [Best Practices](#best-practices)

---

## Decision Framework

### Use POSIX sh (#!/bin/sh) When:

✅ **Maximum portability required:**
- Script runs on Linux, macOS, BSD, Solaris, AIX
- Minimal container images (Alpine, Distroless)
- Embedded systems
- Unknown target environments

✅ **Guaranteed availability:**
- POSIX sh is guaranteed on all Unix-like systems
- No need to check if Bash is installed

✅ **Minimal dependencies:**
- Alpine Linux base images (`/bin/sh` is dash or busybox)
- Distroless containers
- Restricted environments

### Use Bash (#!/bin/bash) When:

✅ **Controlled environment:**
- Known OS/distribution (CentOS, Ubuntu, Debian)
- Specific container base image with Bash
- Development environment (macOS, Linux workstations)

✅ **Complexity justifies Bash features:**
- Arrays or associative arrays needed
- Advanced parameter expansion simplifies logic
- Process substitution `<(cmd)` beneficial
- `[[]]` for safer conditionals

✅ **Performance matters:**
- Bash builtins are faster than external commands
- String manipulation without spawning processes

---

## POSIX sh Features

### Guaranteed Features in POSIX sh

```sh
#!/bin/sh

# Variable assignment
name="Alice"

# Command substitution (backticks or $(...))
current_date=$(date +%Y-%m-%d)
current_date=`date +%Y-%m-%d`  # Old style, still POSIX

# Conditionals with [ or test
if [ -f "$file" ]; then
    echo "File exists"
fi

# Case statements
case "$var" in
    pattern1) echo "Match 1" ;;
    pattern2) echo "Match 2" ;;
    *) echo "Default" ;;
esac

# Loops
for item in item1 item2 item3; do
    echo "$item"
done

while [ "$count" -lt 10 ]; do
    echo "$count"
    count=$((count + 1))
done

# Functions
my_function() {
    echo "Arguments: $*"
    return 0
}

# Arithmetic with $((...))
result=$((5 + 3))

# Here documents
cat <<EOF
This is a here document
With multiple lines
EOF

# Redirection
echo "Output" > file.txt
echo "Append" >> file.txt
command 2>&1  # Redirect stderr to stdout
```

### POSIX String Operations

```sh
#!/bin/sh

# Parameter expansion
echo "${var:-default}"     # Default value
echo "${var:=default}"     # Assign default
echo "${var:?error}"       # Error if unset

# Remove shortest prefix/suffix
echo "${var#prefix}"       # Remove shortest prefix
echo "${var##prefix}"      # Remove longest prefix
echo "${var%suffix}"       # Remove shortest suffix
echo "${var%%suffix}"      # Remove longest suffix

# String length (POSIX-compliant method)
var="hello"
length=$(echo "$var" | wc -c)
length=$((length - 1))  # Remove newline
```

---

## Bash-Specific Features

### Arrays (NOT in POSIX sh)

```bash
#!/bin/bash

# Indexed arrays
files=("file1.txt" "file2.txt" "file3.txt")
echo "${files[0]}"        # First element
echo "${files[@]}"        # All elements
echo "${#files[@]}"       # Array length

# Associative arrays (Bash 4+)
declare -A config
config[host]="localhost"
config[port]="8080"
echo "${config[host]}"
```

**POSIX Alternative:**
```sh
#!/bin/sh

# Space-separated list
files="file1.txt file2.txt file3.txt"
for file in $files; do
    echo "$file"
done

# Positional parameters as array
set -- "item1" "item2" "item3"
echo "$1"  # First item
echo "$#"  # Count
```

### [[ ]] Conditionals (NOT in POSIX sh)

```bash
#!/bin/bash

# [[ ]] is Bash-specific
if [[ -f "$file" && -r "$file" ]]; then
    echo "File exists and is readable"
fi

# Pattern matching
if [[ "$var" == pattern* ]]; then
    echo "Matches pattern"
fi

# Regular expressions
if [[ "$email" =~ ^[a-z]+@[a-z]+\.[a-z]+$ ]]; then
    echo "Valid email"
fi
```

**POSIX Alternative:**
```sh
#!/bin/sh

# Use [ ] with separate conditions
if [ -f "$file" ] && [ -r "$file" ]; then
    echo "File exists and is readable"
fi

# Pattern matching with case
case "$var" in
    pattern*) echo "Matches pattern" ;;
esac

# Regular expressions with grep
if echo "$email" | grep -qE '^[a-z]+@[a-z]+\.[a-z]+$'; then
    echo "Valid email"
fi
```

### Process Substitution (NOT in POSIX sh)

```bash
#!/bin/bash

# Process substitution <(...)
diff <(sort file1.txt) <(sort file2.txt)

# Named pipe alternative
while read -r line; do
    echo "Line: $line"
done < <(command)
```

**POSIX Alternative:**
```sh
#!/bin/sh

# Use temporary files
sort file1.txt > /tmp/sorted1.txt
sort file2.txt > /tmp/sorted2.txt
diff /tmp/sorted1.txt /tmp/sorted2.txt
rm -f /tmp/sorted1.txt /tmp/sorted2.txt
```

### Advanced Parameter Expansion

```bash
#!/bin/bash

# Pattern replacement
echo "${var/old/new}"      # Replace first
echo "${var//old/new}"     # Replace all

# Case modification (Bash 4+)
echo "${var^^}"            # Uppercase
echo "${var,,}"            # Lowercase

# Substring extraction
echo "${var:0:5}"          # First 5 characters
```

**POSIX Alternative:**
```sh
#!/bin/sh

# Pattern replacement with sed
new_var=$(echo "$var" | sed 's/old/new/')      # Replace first
new_var=$(echo "$var" | sed 's/old/new/g')     # Replace all

# Case modification with tr
upper=$(echo "$var" | tr '[:lower:]' '[:upper:]')
lower=$(echo "$var" | tr '[:upper:]' '[:lower:]')

# Substring extraction with cut/sed
first_five=$(echo "$var" | cut -c1-5)
```

### Local Variables (NOT in POSIX sh)

```bash
#!/bin/bash

my_function() {
    local var="local scope"
    echo "$var"
}

var="global scope"
my_function
echo "$var"  # Still "global scope"
```

**POSIX Alternative:**
```sh
#!/bin/sh

my_function() {
    # Use unique variable names
    _my_function_var="function scope"
    echo "$_my_function_var"
}

# Or save/restore
my_function() {
    _saved_var="$var"
    var="function scope"
    echo "$var"
    var="$_saved_var"
}
```

---

## Common Bashisms and Alternatives

### String Comparison

```bash
# ❌ Bashism: [[ ]] with ==
if [[ "$var" == "value" ]]; then

# ✅ POSIX: [ ] with =
if [ "$var" = "value" ]; then
```

### Arithmetic

```bash
# ❌ Bashism: ((  ))
((count++))
((count = count + 1))

# ✅ POSIX: $(( ))
count=$((count + 1))
count=$((count + 1))
```

### Function Declaration

```bash
# ❌ Bashism: function keyword
function my_func {
    echo "Hello"
}

# ✅ POSIX: No function keyword
my_func() {
    echo "Hello"
}
```

### echo vs printf

```bash
# ⚠️ Inconsistent: echo (varies by platform)
echo -n "No newline"    # Works on Linux, not portable
echo -e "Line\nBreak"   # Works on Linux, not portable

# ✅ POSIX: printf
printf "No newline"
printf "Line\nBreak\n"
```

### Source vs Dot

```bash
# ❌ Bashism: source
source script.sh

# ✅ POSIX: . (dot)
. script.sh
```

### Brace Expansion

```bash
# ❌ Bashism: Brace expansion
echo {1..10}
mkdir -p dir/{sub1,sub2,sub3}

# ✅ POSIX: Explicit or loop
echo 1 2 3 4 5 6 7 8 9 10
mkdir -p dir/sub1 dir/sub2 dir/sub3

# Or use seq
for i in $(seq 1 10); do
    echo "$i"
done
```

---

## Platform Differences

### Linux vs macOS

#### sed -i (In-Place Editing)

```bash
# macOS requires empty string
sed -i '' 's/old/new/g' file.txt

# Linux doesn't
sed -i 's/old/new/g' file.txt

# Portable solution: Use temporary file
sed 's/old/new/g' file.txt > file.txt.tmp
mv file.txt.tmp file.txt
```

#### readlink (Resolve Symlinks)

```bash
# Linux (GNU coreutils)
realpath=$(readlink -f /path/to/symlink)

# macOS (BSD)
# readlink -f not supported

# Portable solution
script_dir="$(cd "$(dirname "$0")" && pwd)"

# Or install GNU coreutils on macOS
# brew install coreutils
realpath=$(greadlink -f /path/to/symlink)
```

#### date (Date Arithmetic)

```bash
# Linux (GNU date)
yesterday=$(date -d "yesterday" +%Y-%m-%d)
next_week=$(date -d "+7 days" +%Y-%m-%d)

# macOS (BSD date)
yesterday=$(date -v-1d +%Y-%m-%d)
next_week=$(date -v+7d +%Y-%m-%d)

# Portable solution: Use date -u and timestamps
timestamp=$(date +%s)
yesterday_ts=$((timestamp - 86400))
yesterday=$(date -u -r "$yesterday_ts" +%Y-%m-%d)  # macOS
yesterday=$(date -u -d "@$yesterday_ts" +%Y-%m-%d)  # Linux
```

#### find (Extended Options)

```bash
# GNU find (Linux)
find . -type f -newer reference_file

# BSD find (macOS)
# Some options differ

# Portable: Stick to POSIX find options
find . -type f -name "*.txt"
```

### Alpine Linux (Busybox)

Alpine uses Busybox, which provides limited versions of common utilities:

```sh
#!/bin/sh

# Busybox sh is POSIX-compliant but minimal
# No Bash features
# Limited options for common commands

# Check if running in Busybox
if [ -L /bin/sh ] && [ "$(readlink /bin/sh)" = "busybox" ]; then
    echo "Running in Busybox"
fi

# Use POSIX-compliant patterns
# Avoid GNU-specific options (--long-options)
```

---

## Testing for Portability

### Test with Different Shells

```bash
# Test with sh (POSIX)
sh script.sh

# Test with dash (strict POSIX)
dash script.sh

# Test with bash
bash script.sh

# Test with busybox
busybox sh script.sh
```

### ShellCheck for Portability

```bash
# Check for POSIX compliance
shellcheck --shell=sh script.sh

# Check for Bash-specific issues
shellcheck --shell=bash script.sh

# Check for specific issues
shellcheck --exclude=SC2086 script.sh
```

**Common ShellCheck Warnings:**
- SC2006: Use $(...) instead of backticks
- SC2039: POSIX sh doesn't support arrays, [[ ]], etc.
- SC2086: Quote variables to prevent word splitting
- SC2046: Quote command substitution

### Docker Testing

```bash
# Test in Alpine (Busybox)
docker run --rm -v "$PWD:/scripts" alpine:latest sh /scripts/script.sh

# Test in Debian (dash for /bin/sh)
docker run --rm -v "$PWD:/scripts" debian:latest sh /scripts/script.sh

# Test in Ubuntu (dash for /bin/sh)
docker run --rm -v "$PWD:/scripts" ubuntu:latest sh /scripts/script.sh
```

### Platform Detection

```bash
#!/bin/sh

# Detect OS
case "$(uname -s)" in
    Linux*)
        OS="Linux"
        ;;
    Darwin*)
        OS="macOS"
        ;;
    FreeBSD*|OpenBSD*|NetBSD*)
        OS="BSD"
        ;;
    SunOS*)
        OS="Solaris"
        ;;
    *)
        OS="Unknown"
        ;;
esac

echo "Detected OS: $OS"

# Platform-specific behavior
if [ "$OS" = "macOS" ]; then
    sed -i '' 's/old/new/g' file.txt
else
    sed -i 's/old/new/g' file.txt
fi
```

---

## Best Practices

### 1. Choose Shebang Carefully

```bash
#!/bin/sh        # POSIX sh (portable)
#!/bin/bash      # Bash-specific
#!/usr/bin/env bash  # Find Bash in PATH (more portable)
```

### 2. Test on Target Platforms

- Develop on one platform, test on all targets
- Use Docker for cross-platform testing
- Test with dash (strict POSIX compliance)

### 3. Use ShellCheck

```bash
# Install ShellCheck
# macOS: brew install shellcheck
# Ubuntu: apt-get install shellcheck

# Check script
shellcheck --shell=sh script.sh
```

### 4. Quote Variables

```bash
# ❌ Unquoted (word splitting, glob expansion)
echo $var
cp $source $dest

# ✅ Quoted
echo "$var"
cp "$source" "$dest"
```

### 5. Avoid Bashisms in sh Scripts

```bash
# ❌ Using [[ ]] in #!/bin/sh
#!/bin/sh
if [[ "$var" == "value" ]]; then

# ✅ Use [ ] in #!/bin/sh
#!/bin/sh
if [ "$var" = "value" ]; then
```

### 6. Use POSIX Utilities

```bash
# Avoid GNU-specific long options
grep --color=auto  # GNU
grep -E            # POSIX

# Avoid GNU-specific features
date -d "tomorrow"  # GNU
date -v+1d          # BSD
```

### 7. Provide Fallbacks

```bash
#!/bin/sh

# Check for command availability
if command -v jq >/dev/null 2>&1; then
    # Use jq
    result=$(echo "$json" | jq -r '.field')
else
    # Fallback to sed/awk
    result=$(echo "$json" | sed -n 's/.*"field": "\([^"]*\)".*/\1/p')
fi
```

### 8. Document Requirements

```bash
#!/bin/sh

# Requirements:
# - POSIX sh
# - jq (for JSON parsing)
# - curl (for HTTP requests)

# Check dependencies
for cmd in jq curl; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "Error: $cmd is required but not installed" >&2
        exit 1
    }
done
```

---

## Summary

**POSIX sh:**
- Maximum portability
- Guaranteed on all Unix-like systems
- Smaller feature set, more verbose
- Use for production scripts in unknown environments

**Bash:**
- Rich feature set (arrays, [[ ]], process substitution)
- More concise for complex tasks
- Requires Bash installation
- Use in controlled environments

**Testing:**
- ShellCheck for static analysis
- dash for strict POSIX compliance
- Docker for cross-platform testing

**Portability Checklist:**
- [ ] Use `#!/bin/sh` for portable scripts
- [ ] Avoid Bashisms (arrays, [[ ]], function keyword)
- [ ] Test with ShellCheck --shell=sh
- [ ] Test on target platforms
- [ ] Quote all variables
- [ ] Use POSIX utilities and options
- [ ] Document dependencies
