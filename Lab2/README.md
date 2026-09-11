# Lab 2 — Search Algorithms

> Practice with fundamental array search algorithms.

| Navigation | |
|---|---|
| **Repository hub** | [Back to main README](../README.md) |

---

## Overview

Lab 2 introduces three classic array search problems, solved from scratch with
plain Python (no external libraries):

1. **Linear search** — find the position of an element in a single array.
2. **Find in two arrays** — search for one element across two arrays and classify
   where it appears (first, second, both, or neither).
3. **Common elements in two arrays** — compute the intersection of two arrays.

## Files in This Lab

| # | File | Purpose |
|---|------|---------|
| 01 | [`01_linear_search.py`](01_linear_search.py) | Linear search over one array |
| 02 | [`02_find_in_two_arrays.py`](02_find_in_two_arrays.py) | Search one element across two arrays |
| 03 | [`03_common_in_two_arrays.py`](03_common_in_two_arrays.py) | Common elements (intersection) of two arrays |

---

## Detailed File Guide

### 01_linear_search.py — Linear Search

Walks the array element by element until the target is found.

**Concepts demonstrated:**
- `linear_search(items, target)` returns the matching index or `-1` if absent
- `range(len(items))` indexing vs. the cleaner `enumerate()` loop
- `find_all_occurrences()` returns every index where a repeated value appears
- Works with numbers and strings

**Example output:**
```
List: [10, 23, 45, 70, 11, 15, 70, 20]
Searching for 70...
  Found at index 3
...
```

---

### 02_find_in_two_arrays.py — Find in Two Arrays

Reuses `linear_search()` on two separate arrays and reports where the target
was found.

**Concepts demonstrated:**
- Searching the same target in two independent arrays
- Combining two boolean results into four possible outcomes
- Reusing a helper function (`linear_search`) inside a larger function

**Example output:**
```
25 found in BOTH arrays (first[3], second[2])
3 found only in the FIRST array at index 0
8 found only in the SECOND array at index 0
99 is not present in either array
```

---

### 03_common_in_two_arrays.py — Common Elements

Computes the values shared by two arrays, three different ways.

**Concepts demonstrated:**
- **Brute force** with nested loops — easy to read, but `O(n * m)`
- **Set intersection** — `set(first) & set(second)`, fast but unordered
- **Ordered intersection** — set lookup for speed while preserving the order
  of the first array, with `seen` to avoid duplicates

**Example output:**
```
Array A: [1, 2, 3, 4, 5, 5]
Array B: [4, 5, 6, 7, 8]

Common, brute force (nested loops): [4, 5]
Common, using sets:                 [4, 5]
Common, ordered (keeps A's order):  [4, 5]
```

---

## How to Run

Each script is independent — run any of them with:

```bash
cd Lab2
python3 01_linear_search.py
python3 02_find_in_two_arrays.py
python3 03_common_in_two_arrays.py
```

**Requirements:** Python 3.6+ · no external packages

---

| Navigation | |
|---|---|
| **Repository hub** | [Back to main README](../README.md) |