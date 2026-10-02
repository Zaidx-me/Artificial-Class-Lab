#implementation of stack using list in python
stack = []
inrange=int(input("Enter the range of stack : "))

for i in range(inrange):
     x=int(input("Enter the value to push in stack : "))
     stack.append(x)   
      
print(stack)
print("The top element of the stack is : ",stack[-1])
print("The popped element is : ",stack.pop())
print("Top of stack is : ",stack[-1])
     