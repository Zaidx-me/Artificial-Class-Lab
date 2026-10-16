# Lab 6 — Depth First Search

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
| **Official manual** | [Lab 6.pdf](Lab%206.pdf) — the original assignment sheet |

---

## Overview

Lab 6 implements **Depth First Search (DFS)** — a traversal algorithm that
starts at a node and explores **as far as possible along each branch before
backtracking**. Where BFS (Lab 5) used a **queue** (FIFO), DFS uses a **stack**
(LIFO): the most recently discovered node is the next one explored.

Each task is written in **class and object form** — a `Graph` class with a
dict-based adjacency list, and an iterative `dfs()` method driven by an
explicit stack (the stack `pop` is implemented from scratch with a custom
function). Two tasks are covered:

1. Traversing an **undirected numbered graph** (nodes 0–4) from vertex 0
2. Searching a **tree** from `A` to the goal `G`, stopping the search as soon
   as the goal is reached

## Files in This Lab

| # | File | Task |
|---|------|------|
| 01 | [`01_dfs.py`](01_dfs.py) | DFS on an undirected graph + tree goal search |

---

## Detailed File Guide

### 01_dfs.py — Depth First Search

DFS goes deep first — it pops the top of the stack and pushes that node's
neighbours, so each new branch is explored to its end before backtracking to
the last junction. This file covers both tasks from the manual.

**Concepts demonstrated:**
- A custom `pop(stack)` function — reads `stack[-1]`, deletes it with `del`,
  returns it (from scratch, no `.pop()` method)
- A `Graph` **class** with a dict-based adjacency list (`self.adj`) — nodes
  can be numbers (Task 1) or letters (Task 2)
- `add_vertex(v)` — registers a node with an empty neighbour list
- `add_edge(v, w)` — builds an **undirected** edge (both directions) with a
  duplicate guard, so repeated `add_edge` calls never double up a neighbour
- `dfs(s, goal=None)` — iterative DFS with an explicit stack:
  - push the start node; pop the top; skip it if already visited
  - mark visited and print the node
  - stop immediately with `Goal Found` when the popped node is the goal
  - push unvisited neighbours **in reverse order** — a stack pops
    last-in-first-out, so reversing keeps the natural neighbour order
- The `goal=None` default argument lets the same method do a full traversal
  (`g.dfs(0)`) and a goal search (`g.dfs('A', 'G')`)
- `Goal not found` is printed only when a goal was requested but the stack
  emptied without hitting it

**Example output:**
```
Task 1 Traversal:
0 1 2 3 4
Task 2
A B K N M J F D G E C H I L
A B K N M J F D G
Goal Found: G
```

---

## How to Run

```bash
cd Lab6
python3 01_dfs.py
```

> **Note:** No interactive input — the graph, the tree, and the goal are
> hard-coded in the driver code. Task 1 and Task 2 share one `Graph` object.

**Requirements:** Python 3.6+ · no external packages

---

## Manual Reference

The official lab manual for this lab: [`Lab 6.pdf`](Lab%206.pdf)

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |