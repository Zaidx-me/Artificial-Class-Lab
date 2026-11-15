# Lab 8 — Greedy Best First Search & A* Search

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
| **Official manual** | [Lab 8.pdf](Lab%208.pdf) — the original assignment sheet |

---

## Overview

Lab 8 moves from **uninformed** search (BFS, DFS, DLS, IDDFS — they only know
the graph structure) to **informed** search, which uses domain knowledge in
the form of a **heuristic function** `h(n)` — an estimate of how far a node is
from the goal. The manual's guiding example is the **Bucharest map** from
Russell & Norvig: cities are nodes, roads are weighted edges, and the
straight-line distance from each city to Bucharest is the heuristic. All three
tasks are written in **class and object form**.

Three tasks are covered:

1. **Greedy Best First Search (GBFS)** — expands the node with the smallest
   `h(n)`, ignoring the cost already paid
2. **A\* Search** — expands the node with the smallest `f(n) = g(n) + h(n)`,
   where `g(n)` is the real cost from the start and `h(n)` is the estimate to
   the goal
3. **8-puzzle** — the sliding-tile puzzle solved with **A\***, counting
   **misplaced tiles** as the heuristic

The manual summarises the difference in one line:
`A*` uses `f(n) = g(n) + h(n)`, `GBFS` uses `f(n) = h(n)`, and uniform cost
search uses `f(n) = g(n)`.

## Files in This Lab

| # | File | Task |
|---|------|------|
| 01 | [`01_greedy_best_first.py`](01_greedy_best_first.py) | GBFS on the Bucharest map — `Arad` to `Bucharest` |
| 02 | [`02_a_star.py`](02_a_star.py) | A\* on the same map with `f(n) = g(n) + h(n)` |
| 03 | [`03_eight_puzzle.py`](03_eight_puzzle.py) | 8-puzzle solved with A\* and misplaced tiles |

---

## Detailed File Guide

### 01_greedy_best_first.py — Greedy Best First Search

GBFS always expands the node that **looks closest to the goal** according to
`h(n)`. It is fast and simple, but it can be misled: it never checks how much
the path to that node already cost, so the path it returns is not guaranteed
to be the cheapest one.

**Concepts demonstrated:**
- A `Graph` **class** with `self.adj` mapping a city to a list of
  `(neighbour, cost)` pairs, and `self.h` mapping a city to its straight-line
  distance from Bucharest
- `addEdge(u, v, cost)` — adds the road in **both** directions, because the
  map is undirected
- `addHeuristic(node, value)` — stores `h(n)` for a city
- `pathCost(path)` — walks the returned path and sums the road costs, so the
  driver can report the real cost of the greedy answer
- `GBFS(start, goal)` — maintains an OPEN list of `[node, path]` items and a
  CLOSED list:
  - scan OPEN for the **smallest `h(n)`** (no `heapq`, just like the Lab 5
    priority queue scan)
  - skip nodes already in CLOSED; otherwise mark the node closed and print it
  - stop when the goal is popped
  - push every non-closed neighbour with its path extended by that neighbour
- The 20-city Romania map (23 roads) and all 20 straight-line distances are
  added in the driver code

**Example output:**
```
Greedy Best First Search from Arad to Bucharest

Expand Arad (h = 366)
Expand Sibiu (h = 253)
Expand Fagaras (h = 176)
Expand Bucharest (h = 0)

Goal reached !
Final Path: Arad -> Sibiu -> Fagaras -> Bucharest
Total cost: 450
Nodes expanded: 4
```

---

### 02_a_star.py — A* Search

A\* adds the cost already paid. Each node is scored with
`f(n) = g(n) + h(n)`, so a road that is close in a straight line but far by
road is penalised. This is what makes A\* find the **cheapest** path instead
of just the most promising-looking one.

**Concepts demonstrated:**
- The same `Graph` **class**, map, and heuristic table as in `01`
- `AStar(start, goal)` — OPEN stores `[node, g, f, path]`, CLOSED stores
  expanded nodes:
  - pick the item with the smallest `f` (again a manual scan)
  - skip stale entries whose node is already closed
  - print each expansion with its `g`, `h`, and `f` values — this is the trace
    the manual draws step by step on the map
  - for every neighbour, compute `new_g = g + road cost` and
    `new_f = new_g + h(neighbour)`, then push it with the extended path
- The result matches the manual's walkthrough: A\* prefers
  `Sibiu -> Rimnicu Vilcea -> Pitesti` over the greedy `Fagaras` route,
  because `Pitesti` has the lower total estimate

**Example output:**
```
A* Search from Arad to Bucharest

Expand Arad: g = 0, h = 366, f = 366
Expand Sibiu: g = 140, h = 253, f = 393
Expand Rimnicu Vilcea: g = 220, h = 193, f = 413
Expand Fagaras: g = 239, h = 176, f = 415
Expand Pitesti: g = 317, h = 100, f = 417
Expand Bucharest: g = 418, h = 0, f = 418

Goal reached !
Final Path: Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
Total cost: 418
Nodes expanded: 6
```

> **Compare with `01`:** GBFS reaches Bucharest with a cost of **450** by
> expanding 4 nodes; A\* expands 6 nodes but finds the cheaper path with cost
> **418**. That trade-off — a few more expansions for an optimal answer — is
> the core lesson of the lab.

---

### 03_eight_puzzle.py — 8-Puzzle with A*

The 8-puzzle is a 3×3 grid with tiles 1–8 and one blank (`0`). A move slides a
neighbouring tile into the blank. A\* searches the space of board
configurations, using the number of **misplaced tiles** as the heuristic.

**Concepts demonstrated:**
- A `Puzzle` **class** that stores the start and goal states as tuples of 9
  numbers (row-major order), so states can be compared and stored in lists
- `misplaced(state)` — counts tiles that are not in their goal position
  (the blank is ignored); this is an admissible heuristic because every
  misplaced tile needs at least one move
- `swap(state, i, j)` — returns a new tuple with two tiles exchanged (states
  are immutable)
- `neighbours(state)` — finds the blank with `state.index(0)`, converts it to
  a row and column, and generates the legal moves (up/down/left/right) inside
  the grid
- `printState(state)` — prints one state as a 3×3 grid
- `solve()` — A\* with OPEN storing `[state, g, f, path]`:
  - `g` is the number of moves made, every move costs 1
  - `f = g + misplaced(state)`
  - the goal is printed as the start grid followed by one grid per move
- The driver uses the manual's start and goal layouts

**Example output:**
```
8 Puzzle using A* Search (misplaced tiles heuristic)

Start state:
1 2 3
0 4 6
7 5 8

Step 1:
1 2 3
4 0 6
7 5 8

Step 2:
1 2 3
4 5 6
7 0 8

Step 3:
1 2 3
4 5 6
7 8 0

Goal reached !
Moves: 3
States expanded: 4
```

---

## GBFS vs A* (Quick Reference)

| | Greedy Best First | A\* |
|---|---|---|
| Evaluation | `f(n) = h(n)` | `f(n) = g(n) + h(n)` |
| Uses path cost so far? | No | Yes |
| Optimal path? | Not guaranteed | Yes, with an admissible heuristic |
| Typical behaviour | Rushes toward the goal | Balances cost paid and distance left |

---

## How to Run

```bash
cd Lab8
python3 01_greedy_best_first.py
python3 02_a_star.py
python3 03_eight_puzzle.py
```

> **Note:** No interactive input — the map, the heuristic table, and the
> puzzle states are hard-coded in the driver code.

**Requirements:** Python 3.6+ · no external packages

---

## Manual Reference

The official lab manual for this lab: [`Lab 8.pdf`](Lab%208.pdf)

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
