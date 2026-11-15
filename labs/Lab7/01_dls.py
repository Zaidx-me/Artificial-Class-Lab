#depth limited search implementation using class and objects in python

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

    # depth limited search from start to goal
    def DLS(self, start, goal, depth_limit):

        # every item stores node, its depth and the path taken
        stack = [(start, 0, [start])]

        print(f"DLS traversal from {start} to {goal}:")
        print(f"Depth Limit: {depth_limit}")

        while stack:
            vertex, depth, path = stack.pop()
            print(vertex, end=" ")

            # stop the search as soon as the goal is reached
            if vertex == goal:
                print(f"\nGoal node '{goal}' reached successfully!")
                print("Final Path:", " -> ".join(path))
                return

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

        print(f"\nGoal node '{goal}' not found within depth limit!")


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

# run DLS with depth limit 2
g.DLS('A', 'G', 2)
