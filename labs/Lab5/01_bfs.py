#BFS implementation in python converted from the c++ code given in the manual

class Queue:
    def __init__(self, size):
        self.queue = [None] * size   # fixed size array
        self.front = 0
        self.rear = -1

    # insert at the rear
    def enqueue(self, x):
        self.rear = self.rear + 1
        self.queue[self.rear] = x

    # remove and return from the front
    def dequeue(self):
        x = self.queue[self.front]
        self.queue[self.front] = None
        self.front = self.front + 1
        return x

    def empty(self):
        return self.front > self.rear


# graph class using adjacency list representation
class Graph:
    def __init__(self, v):
        self.vertices = v
        self.adj = [[] for i in range(v)]   # adjacency list of every vertex

    # add edge v -> w
    def addEdge(self, v, w):
        self.adj[v] = self.adj[v] + [w]

    # prints BFS traversal from a given source s
    def bfs(self, s):
        visited = [False] * self.vertices   # mark all vertices as not visited
        q = Queue(self.vertices)            # queue for BFS

        visited[s] = True
        q.enqueue(s)

        while not q.empty():
            s = q.dequeue()
            print(s, end=" ")

            # get all adjacent vertices of s, if not visited mark and enqueue
            for w in self.adj[s]:
                if not visited[w]:
                    visited[w] = True
                    q.enqueue(w)
        print()


# create the graph given in the manual diagram
g = Graph(4)
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 2)
g.addEdge(2, 0)
g.addEdge(2, 3)
g.addEdge(3, 3)

print("Following is Breadth First Traversal (starting from vertex 2) :")
g.bfs(2)