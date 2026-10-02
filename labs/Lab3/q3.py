# Question 3: Guess a Number (1 to 9)
import random

target = random.randint(1, 9)

while True:
    guess = int(input("Guess a number between 1 and 9: "))
    if guess == target:
        print("Well guessed!")
        break