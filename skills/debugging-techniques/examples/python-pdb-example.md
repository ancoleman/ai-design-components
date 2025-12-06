# Python pdb Debugging Example

## Example: Debugging a Division Error

### Code with Bug

```python
# calculator.py
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return average

def main():
    # Test cases
    test_cases = [
        [10, 20, 30],
        [5, 15, 25, 35],
        []  # Bug: empty list causes ZeroDivisionError
    ]

    for i, numbers in enumerate(test_cases):
        print(f"Test {i+1}: {numbers}")
        result = calculate_average(numbers)
        print(f"Average: {result}\n")

if __name__ == "__main__":
    main()
```

### Running Without Debugger

```bash
$ python calculator.py
Test 1: [10, 20, 30]
Average: 20.0

Test 2: [5, 15, 25, 35]
Average: 20.0

Test 3: []
Traceback (most recent call last):
  File "calculator.py", line 18, in <module>
    main()
  File "calculator.py", line 15, in main
    result = calculate_average(numbers)
  File "calculator.py", line 5, in calculate_average
    average = total / count
ZeroDivisionError: division by zero
```

### Debugging with pdb

**Add breakpoint:**
```python
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    total = sum(numbers)
    count = len(numbers)
    breakpoint()  # Stop here to inspect variables
    average = total / count
    return average
```

**Debugging session:**
```bash
$ python calculator.py
Test 1: [10, 20, 30]
> /path/to/calculator.py(6)calculate_average()
-> average = total / count
(Pdb) list
  1     def calculate_average(numbers):
  2         """Calculate the average of a list of numbers."""
  3         total = sum(numbers)
  4         count = len(numbers)
  5         breakpoint()
  6  ->     average = total / count
  7         return average

(Pdb) print numbers
[10, 20, 30]
(Pdb) print total
60
(Pdb) print count
3
(Pdb) continue
Average: 20.0

Test 2: [5, 15, 25, 35]
> /path/to/calculator.py(6)calculate_average()
-> average = total / count
(Pdb) print numbers
[5, 15, 25, 35]
(Pdb) print total
80
(Pdb) print count
4
(Pdb) continue
Average: 20.0

Test 3: []
> /path/to/calculator.py(6)calculate_average()
-> average = total / count
(Pdb) print numbers
[]
(Pdb) print total
0
(Pdb) print count
0
(Pdb) print "About to divide by zero!"
About to divide by zero!
(Pdb) quit
```

### Fixed Code

```python
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:  # Guard against empty list
        raise ValueError("Cannot calculate average of empty list")

    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return average

def main():
    test_cases = [
        [10, 20, 30],
        [5, 15, 25, 35],
        []
    ]

    for i, numbers in enumerate(test_cases):
        print(f"Test {i+1}: {numbers}")
        try:
            result = calculate_average(numbers)
            print(f"Average: {result}\n")
        except ValueError as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
```

### Result

```bash
$ python calculator.py
Test 1: [10, 20, 30]
Average: 20.0

Test 2: [5, 15, 25, 35]
Average: 20.0

Test 3: []
Error: Cannot calculate average of empty list
```

## Key Takeaways

1. **Use breakpoint()** to pause execution
2. **Inspect variables** with `print` command
3. **Step through code** with `next`, `step`, `continue`
4. **Identify root cause** (empty list causes division by zero)
5. **Add proper validation** before risky operations
6. **Test edge cases** (empty list, single element, etc.)
