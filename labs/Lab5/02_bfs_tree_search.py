#BFS on a tree, the search stops as soon as the goal node is achieved

class Queue:
    def __init__(self, size):
        self.queue = [None] * size   # fixed size array
        self.front = 0
        self.rear = -1

    def enqueue(self, x):
        self.rear = self.rear + 1
        self.queue[self.rear] = x

    def dequeue(self):
        x = self.queue[self.front]
        self.queue[self.front] = None
        self.front = self.front + 1
        return x

    def empty(self):
        return self.front > self.rear


# graph class using adjacency list representation
class Graph:
    def __init__(self):
        self.adj = {}   # adjacency list of every node

    # add edge v -> w, creates both nodes if they don't exist yet
    def addEdge(self, v, w):
        if v not in self.adj:
            self.adj[v] = []
        if w not in self.adj:
            self.adj[w] = []
        self.adj[v] = self.adj[v] + [w]

    # prints BFS traversal from the start node, True if goal is found
    def bfs(self, s, goal):
        q = Queue(len(self.adj))   # queue for BFS, one slot per node

        q.enqueue(s)
        while not q.empty():
            node = q.dequeue()
            print(node, end=" ")

            # stop the search when the goal is achieved
            if node == goal:
                return True

            # tree has no cycles so a visited array is not needed
            for w in self.adj[node]:
                q.enqueue(w)

        return False   # queue emptied without finding the goal


# tree given in the manual, starting node is A and goal node is G
g = Graph()
g.addEdge("A", "B")
g.addEdge("A", "F")
g.addEdge("A", "E")
g.addEdge("B", "D")
g.addEdge("B", "K")
g.addEdge("B", "J")
g.addEdge("F", "G")
g.addEdge("E", "C")
g.addEdge("E", "H")
g.addEdge("E", "N")
g.addEdge("D", "M")

start = "A"
goal = "J"

print("Breadth First Search from", start, "until goal", goal, "is found :")
found = g.bfs(start, goal)
print()
if found:
    print("Goal", goal, "is found !")
else:
    print("Goal", goal, "is not in the tree !")