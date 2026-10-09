# stack implementation using class and objects in python

class Stack:
    def __init__(self, size):
        self.stack = [None] * size   # fixed size array
        self.top = -1                # index of top element, -1 means empty

    # push
    def push(self, x):
        self.top = self.top + 1
        self.stack[self.top] = x

    # pop
    def pop(self):
        popped = self.stack[self.top]
        self.stack[self.top] = None
        self.top = self.top - 1
        return popped

    # peek
    def peek(self):
        return self.stack[self.top]


size = int(input("Enter the range of stack : "))
s = Stack(size)

for i in range(size):
    x = int(input("Enter the value to push in stack : "))
    s.push(x)

print("\nThe stack is : ", s.stack)
print("\nThe top element of the stack is : ", s.peek())

popped = s.pop()
print("\nThe popped element is : ", popped)
print("\nAfter popping, the stack is : ", s.stack[:s.top + 1])
print("\nTop of stack is : ", s.peek())