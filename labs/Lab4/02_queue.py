# queue implementation using class and objects in python

class Queue:
    def __init__(self, size):
        self.queue = [None] * size   # fixed size array
        self.front = 0               
        self.rear = -1               
    # enqueue
    def enqueue(self, y):
        self.rear = self.rear + 1
        self.queue[self.rear] = y

    # dequeue
    def dequeue(self):
        dequeued = self.queue[self.front]
        self.queue[self.front] = None
        self.front = self.front + 1
        return dequeued


size = int(input("Enter value for range : "))
q = Queue(size)

for i in range(size):
    y = int(input("Enter the value to push in queue : "))
    q.enqueue(y)

print("\nThe queue is : ", q.queue[q.front:q.rear + 1])

dequeued = q.dequeue()
print("\nThe popped element is : ", dequeued)
print("\nThe queue after popping is : ", q.queue[q.front:q.rear + 1])

dequeued = q.dequeue()
print("\nThe popped element is : ", dequeued)