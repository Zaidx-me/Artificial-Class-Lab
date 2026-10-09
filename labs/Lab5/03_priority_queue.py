#priority queue implementation using class and objects in python

class PriorityQueue:
    def __init__(self, size):
        self.items = [None] * size   # every slot stores (value, priority)
        self.count = 0

    # add an item at the back
    def enqueue(self, value, priority):
        self.items[self.count] = (value, priority)
        self.count = self.count + 1

    # remove the item having the highest priority
    def dequeue(self):
        high = 0
        for i in range(1, self.count):
            if self.items[i][1] > self.items[high][1]:
                high = i

        popped = self.items[high]

        # shift the remaining items one place left
        for i in range(high, self.count - 1):
            self.items[i] = self.items[i + 1]

        self.items[self.count - 1] = None
        self.count = self.count - 1
        return popped


pq = PriorityQueue(5)
pq.enqueue("A", 2)
pq.enqueue("B", 5)
pq.enqueue("C", 3)
pq.enqueue("D", 1)

print("Dequeue order (highest priority comes out first) :")
print(pq.dequeue())
print(pq.dequeue())
print(pq.dequeue())
print(pq.dequeue())