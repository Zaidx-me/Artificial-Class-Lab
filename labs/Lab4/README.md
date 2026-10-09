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
in, first out), and **binary search** on a sorted array. Each task is written in
**class and object form** — the data structure is a class, the operations are
its methods, and the driver code creates an object and calls those methods.
Every script reads its input from the user and demonstrates the core operations.

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
- A `Stack` **class**; `__init__()` creates the fixed-size array (`self.stack`)
  and the `top` pointer (instance attributes)
- `push(x)` — method that increments `self.top`, then assigns `self.stack[self.top] = x`
  (no `append()`)
- `peek()` — method returning `self.stack[self.top]`
- `pop()` — method that saves `self.stack[self.top]`, clears the slot,
  decrements `self.top`, and returns the saved value (no `pop()`)
- Creating an object `s = Stack(size)` and calling `s.push(x)`, `s.peek()`,
  `s.pop()`

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
- A `Queue` **class**; `__init__()` sets up the fixed-size array (`self.queue`)
  plus the `front` / `rear` pointers (instance attributes)
- `enqueue(y)` — method that increments `self.rear`, then assigns
  `self.queue[self.rear] = y` (no `append()`)
- `dequeue()` — method that reads `self.queue[self.front]`, clears the slot,
  increments `self.front`, and returns the value (no `pop(0)`)
- Creating an object `q = Queue(size)` and calling `q.enqueue(y)`,
  `q.dequeue()`
- Taking the queue size and values from user `input()`

**Example flow:**
```
Enter value for range : 3
Enter the value to push in queue : 1
Enter the value to push in queue : 2
Enter the value to push in queue : 3
The queue is :  [1, 2, 3]

The popped element is :  1
The queue after popping is :  [2, 3]

The popped element is :  2
```

**Note:** With `front`/`rear` pointers the dequeued slots stay in the array but
are ignored by the pointers. No built-in list methods are used — everything is
implemented from scratch.

---

### 03_binary_search.py — Binary Search

Binary search (half-interval search) finds a target in a **sorted** array in
logarithmic time by repeatedly halving the search space.

**Concepts demonstrated:**
- A `BinarySearch` **class** that wraps the array in `__init__()`
  (`self.array`)
- `bubble_sort()` — method that sorts the array **from scratch** with nested
  swaps (no `array.sort()`)
- `search(target)` — method that runs binary search on `self.array`
- `low` / `high` pointers narrow the search range
- `mid = (low + high) // 2` picks the middle index
- Comparing the middle value against the target to decide the next half
- Returning the index when found, or `-1` when the value is absent
- Creating an object `bs = BinarySearch(array)` and calling `bs.bubble_sort()`,
  `bs.search(target)`

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