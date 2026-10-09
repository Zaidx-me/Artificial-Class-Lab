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


# tree given in the manual, starting node is A and goal node is G
tree = {
    "A": ["B", "F", "E"],
    "B": ["D", "K", "J"],
    "F": ["G"],
    "E": ["C", "H", "N"],
    "D": ["M"],
    "K": [],
    "J": [],
    "G": [],
    "C": [],
    "H": [],
    "N": [],
    "M": []
}

start = "A"
goal = "G"

q = Queue(12)   # one slot per node, every node enters the queue once
q.enqueue(start)

print("Breadth First Search from", start, "until goal", goal, "is found :")
while not q.empty():
    node = q.dequeue()
    print(node, end=" ")

    # stop the search when the goal is achieved
    if node == goal:
        break

    # tree has no cycles so a visited array is not needed
    for child in tree[node]:
        q.enqueue(child)

print()
print("Goal", goal, "is found !")