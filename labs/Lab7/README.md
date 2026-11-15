# Lab 7 — Depth Limited Search & Iterative Deepening DFS

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
| **Official manual** | [Lab07.pdf](Lab07.pdf) — the original assignment sheet |

---

## Overview

Lab 7 implements two ways of making DFS more practical on very tall or very
wide trees:

- **Depth Limited Search (DLS)** — plain DFS with a **cut-off limit**: it stops
  expanding a branch once that branch reaches the given depth
- **Iterative Deepening DFS (IDDFS)** — runs DLS again and again, each time
  with a **bigger limit** (0, 1, 2, …), so shallow goals are found quickly
  while memory use stays as low as DFS

The manual motivates this with the flaws of the earlier searches: DFS can
reach a goal close to the root very late (and may not return the shortest
path), while BFS needs space proportional to the whole tree — around `n/2`
nodes on the last level alone. IDDFS keeps DFS's `O(d)` space and BFS's
level-by-level discovery. Each task is written in **class and object form** —
a `Graph` class with a dict-based adjacency list and iterative search methods
driven by an explicit stack.

Two tasks are covered:

1. Finding goal node `G` from start `A` with **DLS** and depth limit 2
2. Finding the same goal with **IDDFS** and a maximum depth of 3

## Files in This Lab

| # | File | Task |
|---|------|------|
| 01 | [`01_dls.py`](01_dls.py) | DLS on the manual's tree — goal `G`, depth limit 2 |
| 02 | [`02_iddfs.py`](02_iddfs.py) | IDDFS on the same tree — limits 0 to 3 |

---

## Detailed File Guide

### 01_dls.py — Depth Limited Search

DLS works exactly like the Lab 6 DFS, with one extra rule: a node that is
already at the depth limit is not expanded any further. The limit is what
protects DFS from endless branches on huge or cyclic graphs.

**Concepts demonstrated:**
- A `Graph` **class** with a dict-based adjacency list (`self.adj`), so nodes
  can be letters
- `addEdge(u, v)` — registers both nodes, then appends `v` to `u`'s neighbour
  list (this is a directed tree, so only one direction is added)
- `DLS(start, goal, depth_limit)` — iterative search with an explicit stack;
  every stack item is a `(node, depth, path)` tuple:
  - pop the last item and print the node
  - stop immediately with the final path when the popped node is the goal
  - if the node is already at the limit, don't push its neighbours
  - otherwise push the unvisited neighbours **in reverse order**, so the first
    neighbour in the adjacency list is popped first
- The `path` stored with each item also acts as the cycle guard — a neighbour
  that already appears in the current path is skipped
- A clear failure message is printed when the stack empties without reaching
  the goal inside the limit

**Example output:**
```
DLS traversal from A to G:
Depth Limit: 2
A B K J F D G 
Goal node 'G' reached successfully!
Final Path: A -> D -> G
```

---

### 02_iddfs.py — Iterative Deepening DFS

IDDFS does not visit the tree once — it calls **DLS for every limit** from 0
up to the maximum depth. Shallow nodes are found on early iterations; deep
nodes are found once the limit is large enough.

**Concepts demonstrated:**
- The same `Graph` **class** and tree as in `01`
- `DLS(start, goal, depth_limit)` now **returns two things**:
  - the `path` to the goal, or `None` if the goal was not reached
  - the `visited` list — the traversal order of that iteration
- `IDDFS(start, goal, max_depth)` — loops `limit` from 0 to `max_depth`,
  prints the limit, calls `DLS`, prints the traversal, and returns as soon as
  a path comes back
- If every limit fails, the method prints `Goal node ... not found!`
- Because DLS is re-run from the root each time, the traversal of each
  iteration is printed separately — this shows how IDDFS behaves like BFS on
  shallow goals

**Example output:**
```

Depth Limit: 0
Traversal: A

Depth Limit: 1
Traversal: A -> B -> F -> D -> E

Depth Limit: 2
Traversal: A -> B -> K -> J -> F -> D -> G
Goal node 'G' reached successfully!
Final Path: A -> D -> G
```

> **Note:** the goal `G` sits directly below `A`, but DFS order reaches it
> through `D` after exploring `B`'s subtree first. IDDFS still finds it at the
> first limit large enough to reach it (limit 2), which is what makes it
> attractive compared to a single deep DFS.

---

## DLS vs IDDFS (Manual Task c)

| Property | DLS | IDDFS |
|----------|-----|-------|
| Idea | DFS with a fixed cut-off | DLS repeated with limits 0, 1, 2, … |
| Space | `O(d)` — one stack | `O(d)` — same stack, one DLS at a time |
| Time | depends on the chosen limit | higher than one DLS — shallow levels are re-visited |
| Finds shallow goals fast? | Only if the limit is large enough | Yes — small limits run first |
| Completeness | No — a too-small limit cuts off the goal | Yes, for a finite graph if the maximum depth is large enough |
| Main problem | Choosing a good limit in advance | Repeated work from re-running the lower levels |

The re-expansion is cheaper than it looks: the nodes on the deepest level
dominate the total work, so the repeated shallow runs add only a constant
factor — IDDFS is still `O(b^d)` time like DFS, but with BFS-like discovery of
nodes near the root.

---

## How to Run

```bash
cd Lab7
python3 01_dls.py
python3 02_iddfs.py
```

> **Note:** No interactive input — the tree, start node, goal, and depth
> limits are hard-coded in the driver code.

**Requirements:** Python 3.6+ · no external packages

---

## Manual Reference

The official lab manual for this lab: [`Lab07.pdf`](Lab07.pdf)

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
