def pop(stack):
    last = stack[-1]
    del stack[-1]
    return last

 
class Graph:

    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, v, w):
        self.add_vertex(v)
        self.add_vertex(w)

        if w not in self.adj[v]:
            self.adj[v].append(w)
        if v not in self.adj[w]:
            self.adj[w].append(v)

    def dfs(self, s, goal=None):
        if s not in self.adj:
            print(f"Vertex {s} does not exist in graph.")
            return

        visited = []
        stack = []

        stack.append(s)

        while stack:
            s = pop(stack)

            if s in visited:
                continue

            visited.append(s)
            print(s, end=" ")

            if s == goal:
                print()
                print(f"Goal Found: {s}")
                return

            # push in reverse so the first neighbour is visited first
            for i in reversed(self.adj[s]):
                if i not in visited:
                    stack.append(i)

        print()
        if goal is not None:
            print("Goal not found")


g = Graph()

g.add_edge(0, 1)
g.add_edge(0, 4)

g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)

g.add_edge(2, 1)
g.add_edge(2, 3)

g.add_edge(3, 1)
g.add_edge(3, 2)
g.add_edge(3, 4)

print("Task 1 Traversal:")
g.dfs(0)

print("Task 2")

g.add_edge('A', 'B')
g.add_edge('A', 'F')
g.add_edge('A', 'D')
g.add_edge('A', 'E')
g.add_edge('B', 'K')
g.add_edge('B', 'J')
g.add_edge('D', 'G')
g.add_edge('E', 'C')
g.add_edge('E', 'H')
g.add_edge('E', 'I')
g.add_edge('K', 'N')
g.add_edge('K', 'M')
g.add_edge('I', 'L')

g.dfs('A')
g.dfs('A', 'G')