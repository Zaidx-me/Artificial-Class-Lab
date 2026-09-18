# Creating a Class Person and defining _init_() function

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# create objects p1 and print values 

p1 = Person("John", 36)
print(p1.name)
print(p1.age)

