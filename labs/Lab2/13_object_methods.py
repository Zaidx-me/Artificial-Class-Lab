# Creating a methods in Person and defining _init_() function

class Person:
    def __init__( self, name, age ):
        self.name = name
        self.age = age
    
    def myfunc(self):
        print("Hello my name is " + self.name)
# create objects p1 and print values 

p1 = Person ("John", 36)
p1.myfunc()

