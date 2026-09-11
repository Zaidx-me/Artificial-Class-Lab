# Lab 1 — Python Fundamentals

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../README.md) |
| **Official manual** | [manual.md](manual.md) — the original assignment sheet |

---

## Overview

Lab 1 introduces the core building blocks of Python: syntax, input/output, data types, strings, lists, and conditional statements. Each topic below has its own runnable script, listed in teaching order.

## Files in This Lab

| # | File | Topic |
|---|------|-------|
| 01 | [`01_python_syntax.py`](01_python_syntax.py) | Print statements & comments |
| 02 | [`02_input_output.py`](02_input_output.py) | User input & output |
| 03 | [`03_multiple_statements.py`](03_multiple_statements.py) | Multiple statements on one line |
| 04 | [`04_indentation.py`](04_indentation.py) | Indentation rules |
| 05 | [`05_reserved_words.py`](05_reserved_words.py) | Reserved keywords |
| 06 | [`06_data_types.py`](06_data_types.py) | Numbers, Booleans, Strings, type casting |
| 07 | [`07_lists.py`](07_lists.py) | Lists: creation, indexing, slicing |
| 08 | [`08_conditionals.py`](08_conditionals.py) | Comparison operators & if/elif/else |
| 09 | [`09_linear_search.py`](09_linear_search.py) | Linear search in a list |
| 10 | [`10_find_in_two_arrays.py`](10_find_in_two_arrays.py) | Find a value in two arrays |
| 11 | [`11_common_in_two_arrays.py`](11_common_in_two_arrays.py) | Common values in two arrays |

---

## Detailed File Guide

### 01_python_syntax.py — Print Statements & Comments

Covers the basics of Python syntax including the `print()` function and single-line comments.

**Concepts demonstrated:**
- `print()` with multiple arguments
- Printing different data types (int, float, string)
- The `sep` and `end` parameters of `print()`
- Single-line comments using `#`

**Example output:**
```
Hello, World!
Python is fun
Python-is-fun
Hello World
```

---

### 02_input_output.py — User Input and Output

Demonstrates how to read user input and produce output.

**Concepts demonstrated:**
- `input()` with a prompt string
- Strings are the default return type of `input()`
- Type conversion: `int()` to do math
- Arithmetic on user-provided numbers

**Key point:** `input()` always returns a string — you must cast it explicitly for math.

---

### 03_multiple_statements.py — Multiple Statements on One Line

Shows how to write several Python statements on a single line using semicolons (`;`).

**Concepts demonstrated:**
- Variable assignment with `;` separator
- Multiple `print()` calls on one line
- When semicolons are useful vs. why they should be used sparingly

**Note:** While valid syntax, this pattern reduces readability and is discouraged in production code.

---

### 04_indentation.py — Indentation Rules

Python uses whitespace indentation instead of braces `{}` to define code blocks.

**Concepts demonstrated:**
- Basic `if` block indentation
- `for` loops and their indented body
- `while` loops and their indented body
- Function definitions and their indented body
- Consistent 4-space indentation convention

**Key rule:** All statements in the same block must share identical indentation.

---

### 05_reserved_words.py — Python Keywords

Lists all Python 3 reserved words and demonstrates how to check if a word is a keyword.

**Concepts demonstrated:**
- Complete list of Python 3 reserved keywords (35 total)
- Using the `keyword` module (`keyword.iskeyword()`)
- Why reserved words cannot be used as variable names

**Output includes:** A formatted table of all reserved words and a test showing which sample words are reserved.

---

### 06_data_types.py — Numbers, Booleans, Strings, and Type Casting

The most comprehensive file — covers all fundamental Python data types.

**Concepts demonstrated:**

| Category | Topics |
|----------|--------|
| **Numeric types** | `int`, `float`, complex numbers (`3+4j`) |
| **Booleans** | `True`/`False`, booleans as integers (`True + True = 2`) |
| **Strings** | Creation, immutability, `len()`, escape sequences (`\n`, `\t`) |
| **String indexing** | Positive index (`name[0]`), negative index (`name[-1]`) |
| **String slicing** | `name[0:3]` |
| **Type casting** | `int()`, `float()`, `str()` conversions |

**Escape sequences covered:**
| Sequence | Meaning |
|----------|---------|
| `\n` | Newline |
| `\t` | Horizontal tab |
| `\\` | Backslash |
| `\'` | Single quote |
| `\"` | Double quote |

---

### 07_lists.py — List Creation, Indexing, and Slicing

Covers Python's most versatile data structure — the list.

**Concepts demonstrated:**
- Creating lists with values
- Positive and negative indexing
- Slicing: `fruits[0:2]`
- Adding items with `append()`, removing with `remove()`
- Looping through a list with `for`
- Membership testing with `in`
- Built-in functions: `len()`, `min()`, `max()`, `sum()`
- Sorting with `sort()`

**Indexing example:**
```
colors = ["RED", "Blue", "Green", "Black"]

Index from left:   0      1       2       3
Index from right: -4     -3      -2      -1
```

---

### 08_conditionals.py — Comparison Operators and Conditional Statements

Covers all comparison operators and control flow with `if`/`elif`/`else`.

**Concepts demonstrated:**

| Operator | Meaning |
|----------|---------|
| `==` | Equals |
| `!=` | Not equals |
| `<` | Less than |
| `<=` | Less than or equal |
| `>` | Greater than |
| `>=` | Greater than or equal |

**Also covers:**
- Simple `if` statements
- `if`/`else` branching
- `if`/`elif`/`else` chains (grade calculator)
- Logical operators: `and`, `or`, `not`

---

### 09_linear_search.py — Linear Search

Searches a list for a value by checking each element in order.

**Concepts demonstrated:**
- A single `linear_search(items, target)` function using a `for` loop with `range()`
- Returning the index when found, or `-1` when the value is not present

**Example output:**
```
45 is at index: 2
99 is at index: -1   # -1 means not found
```

---

### 10_find_in_two_arrays.py — Find a Value in Two Arrays

Searches one value across two arrays and reports where it was found.

**Concepts demonstrated:**
- One `find_in_two_arrays(first, second, target)` function
- Two linear scans (one per array) combined with `if`/`elif`/`else` into
  four possible answers: in both, only the first, only the second, or neither

**Example output:**
```
25 is in both arrays
3 is only in the first array
8 is only in the second array
99 is in neither array
```

---

### 11_common_in_two_arrays.py — Common Values in Two Arrays

Finds the values that appear in both arrays.

**Concepts demonstrated:**
- One `common_elements(first, second)` function
- The `in` operator to test membership
- Building a result list with `append()`, avoiding duplicates with `not in`

**Example output:**
```
Array A: [1, 2, 3, 4, 5]
Array B: [4, 5, 6, 7, 8]
Common elements: [4, 5]
```

---

## How to Run

Each script is independent — run any of them with:

```bash
cd Lab1
python3 01_python_syntax.py
python3 06_data_types.py
# ... etc
```

> **Note:** `02_input_output.py` requires interactive input when run.

**Requirements:** Python 3.6+ · no external packages

---

## Manual Reference

The official lab manual for this lab: [`manual.md`](manual.md)

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../README.md) |