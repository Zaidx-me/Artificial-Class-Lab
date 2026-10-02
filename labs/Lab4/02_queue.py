# implermentation of queue using python
queue = []

rng=int(input("Enter value for range : "))

for i in range(rng):
     y=int(input("Enter the value to push in queue : "))
     queue.append(y)
    
print(queue)
    
print(queue.pop(0))
print(queue)
print(queue.pop(0))     
