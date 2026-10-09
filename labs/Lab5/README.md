# Lab 5 — Breadth First Search & Priority Queue

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
| **Official manual** | [Lab 5.pdf](Lab%205.pdf) — the original assignment sheet |

---

## Overview

Lab 5 implements **Breadth First Search (BFS)** — a graph traversal algorithm
that explores a graph layer by layer, visiting all neighbours of the current
node before moving to the next depth level. BFS uses a **queue** (FIFO) and
checks whether a vertex has been discovered before enqueueing it. Each task is
written in **class and object form**, and the queue is implemented **from
scratch** (`front`/`rear` pointers — no `deque`, no built-in list methods).

Three tasks are covered:

1. Converting the **C++ BFS walkthrough** from the manual into Python
2. Running BFS on a tree from `A` to the goal `G`, stopping the search as soon
   as the goal is achieved
3. Implementing a **Priority Queue** from scratch (highest priority out first)

## Files in This Lab

| # | File | Task |
|---|------|------|
| 01 | [`01_bfs.py`](01_bfs.py) | BFS on a graph (C++ walkthrough converted to Python) |
| 02 | [`02_bfs_tree_search.py`](02_bfs_tree_search.py) | BFS on a tree, stop when the goal is found |
| 03 | [`03_priority_queue.py`](03_priority_queue.py) | Priority queue implementation (from scratch) |

---

## Detailed File Guide

### 01_bfs.py — BFS on a Graph

This is the direct Python conversion of the C++ code given in the manual's
walkthrough. The C++ `Graph` class becomes a Python class, the C++
`list<int> adj[]` becomes a list of adjacency lists, and the C++ queue becomes
our own from-scratch `Queue` class.

**Concepts demonstrated:**
- A `Queue` **class** — fixed-size array with `front` / `rear` pointers;
  `enqueue(x)` writes at the rear, `dequeue()` reads from the front
  (no `append()`, no `pop(0)`)
- A `Graph` **class** — `__init__(v)` builds `self.adj`, a list holding the
  neighbours of every vertex (adjacency list representation)
- `addEdge(v, w)` — adds `w` to `v`'s neighbour list (used `list + [w]` to
  avoid `append()`)
- `bfs(s)` — marks all vertices "not visited", enqueues the source, then:
  - dequeues a vertex and prints it
  - for every neighbour, if it isn't visited yet, mark it and enqueue it
- Creating an object `g = Graph(4)`, adding edges, and calling `g.bfs(2)`

**Example output:**
```
Following is Breadth First Traversal (starting from vertex 2) :
2 0 3 1
```

---

### 02_bfs_tree_search.py — BFS until the Goal

The manual gives a tree whose starting node is `A` and goal node is `G`. BFS
visits nodes level by level, and the search **stops immediately when the goal
is achieved** — the nodes after `G` are never printed.

**Concepts demonstrated:**
- The tree stored as a dictionary: each node maps to its list of children
- The same from-scratch `Queue` class as in `01`
- BFS enqueues the start node, then for every dequeued node enqueues its
  children
- `if node == goal: break` — the early-termination check
- No `visited` array is needed here because a tree has no cycles (every node
  is enqueued exactly once)

**Example output:**
```
Breadth First Search from A until goal G is found :
A B F E D K J G
Goal G is found !
```

---

### 03_priority_queue.py — Priority Queue

A priority queue is a queue where the item with the **highest priority** is
dequeued first, no matter when it was enqueued. Implemented from scratch — no
`heapq`, no built-in list methods.

**Concepts demonstrated:**
- A `PriorityQueue` **class**; every slot stores a `(value, priority)` tuple
- `enqueue(value, priority)` — adds the pair at the back (`self.count` acts as
  the rear index)
- `dequeue()` — scans the array for the slot with the highest priority,
  saves it, then shifts every later item one place left to fill the gap
- Creating an object `pq = PriorityQueue(5)` and calling `pq.enqueue(...)`,
  `pq.dequeue()`

**Example output:**
```
Dequeue order (highest priority comes out first) :
('B', 5)
('C', 3)
('A', 2)
('D', 1)
```

---

## How to Run

Each task is independent — run any of them with:

```bash
cd Lab5
python3 01_bfs.py
python3 02_bfs_tree_search.py
python3 03_priority_queue.py
# ... etc
```

> **Note:** None of the Lab 5 scripts require interactive input — the graph,
> the tree, and the priority queue data are hard-coded in the driver code.

**Requirements:** Python 3.6+ · no external packages

---

## Manual Reference

The official lab manual for this lab: [`Lab 5.pdf`](Lab%205.pdf)

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |