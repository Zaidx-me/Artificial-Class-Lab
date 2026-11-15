#iterative deepening depth first search implementation using class and objects in python

class Graph:
    def __init__(self):
        self.adj = {}

    # add edge u -> v
    def addEdge(self, u, v):
        if u not in self.adj:
            self.adj[u] = []

        if v not in self.adj:
            self.adj[v] = []

        self.adj[u].append(v)

    # one depth limited search, returns path and traversal order
    def DLS(self, start, goal, depth_limit):

        # every item stores node, its depth and the path taken
        stack = [(start, 0, [start])]

        # keeps the order in which nodes were visited
        visited = []

        while stack:
            vertex, depth, path = stack.pop()
            visited.append(vertex)

            # return as soon as the goal is reached
            if vertex == goal:
                return path, visited

            # do not expand a node that is already at the limit
            if depth >= depth_limit:
                continue

            # push neighbours in reverse so the first neighbour is popped first
            i = len(self.adj[vertex]) - 1
            while i >= 0:
                neighbour = self.adj[vertex][i]

                # skip nodes already present in the current path
                if neighbour not in path:
                    stack.append((neighbour, depth + 1, path + [neighbour]))

                i -= 1

        return None, visited

    # iddfs runs dls again and again with a bigger limit
    def IDDFS(self, start, goal, max_depth):
        for limit in range(max_depth + 1):
            print(f"\nDepth Limit: {limit}")

            path, visited = self.DLS(start, goal, limit)
            print("Traversal:", " -> ".join(visited))

            # goal found in this iteration
            if path is not None:
                print(f"Goal node '{goal}' reached successfully!")
                print("Final Path:", " -> ".join(path))
                return

        print(f"\nGoal node '{goal}' not found!")


# tree given in the manual, start node A and goal node G
g = Graph()

g.addEdge('A', 'B')
g.addEdge('A', 'F')
g.addEdge('A', 'D')
g.addEdge('A', 'E')

g.addEdge('B', 'K')
g.addEdge('B', 'J')

g.addEdge('K', 'N')
g.addEdge('K', 'M')

g.addEdge('D', 'G')

g.addEdge('E', 'C')
g.addEdge('E', 'H')
g.addEdge('E', 'I')

g.addEdge('I', 'L')

# run IDDFS with maximum depth 3
g.IDDFS('A', 'G', 3)
