# Lab 4 — Stacks, Queues & Binary Search

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
| **Official manual** | [Lab 4.pdf](Lab%204.pdf) — the original assignment sheet |

---

## Overview

Lab 4 implements three classic data structures and a search algorithm using
Python lists: a **stack** (LIFO — last in, first out), a **queue** (FIFO — first
in, first out), and **binary search** on a sorted array. Each task is an
independent script that reads its input from the user and demonstrates the core
operations.

## Files in This Lab

| # | File | Task |
|---|------|------|
| 01 | [`01_stack.py`](01_stack.py) | Implement a Stack using Python |
| 02 | [`02_queue.py`](02_queue.py) | Implement a Queue using Python |
| 03 | [`03_binary_search.py`](03_binary_search.py) | Binary search on a sorted array |

---

## Detailed File Guide

### 01_stack.py — Stack (LIFO)

A stack is a "last in, first out" structure — the last item pushed is the
first one popped.

**Concepts demonstrated:**
- Using a Python **list** as the underlying storage
- `append()` to **push** a value onto the stack
- `stack[-1]` to **peek** at the top element
- `pop()` to **remove** (pop) the top element
- Taking the stack size and values from user `input()`

**Example flow:**
```
Enter the range of stack : 3
Enter the value to push in stack : 10
Enter the value to push in stack : 20
Enter the value to push in stack : 30
[10, 20, 30]
The top element of the stack is :  30
The popped element is :  30
Top of stack is :  20
```

---

### 02_queue.py — Queue (FIFO)

A queue is a "first in, first out" structure — the item that arrived first is
the first one dequeued.

**Concepts demonstrated:**
- Using a Python **list** as the underlying storage
- `append()` to **enqueue** a value at the back
- `pop(0)` to **dequeue** from the front (FIFO order)
- Taking the queue size and values from user `input()`

**Example flow:**
```
Enter value for range : 3
Enter the value to push in queue : 1
Enter the value to push in queue : 2
Enter the value to push in queue : 3
[1, 2, 3]
1
[2, 3]
2
```

**Note:** With a list, dequeuing from the front (`pop(0)`) is O(n) because every
element shifts left; a `collections.deque` would make it O(1).

---

### 03_binary_search.py — Binary Search

Binary search (half-interval search) finds a target in a **sorted** array in
logarithmic time by repeatedly halving the search space.

**Concepts demonstrated:**
- The array is sorted first with `array.sort()` (a precondition of binary search)
- `low` / `high` pointers narrow the search range
- `mid = (low + high) // 2` picks the middle index
- Comparing the middle value against the target to decide the next half
- Returning the index when found, or `-1` when the value is absent
- Taking the target from user `input()`

**Example output:**
```
Sorted array: [5, 9, 12, 23, 34, 56, 70, 88, 90, 99]
Enter the number to search: 70
Element found at the index: 6
```

---

## How to Run

Each task is independent — run any of them with:

```bash
cd Lab4
python3 01_stack.py
python3 03_binary_search.py
# ... etc
```

> **Note:** All three scripts (01, 02, 03) require interactive input when run.

**Requirements:** Python 3.6+ · no external packages

---

## Manual Reference

The official lab manual for this lab: [`Lab 4.pdf`](Lab%204.pdf)

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |