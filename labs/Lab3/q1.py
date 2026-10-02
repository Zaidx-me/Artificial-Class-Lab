#Question 1: Divisible by 7 and Multiple of 5 (1500 to 2700)

result = []
for num in range(1500, 2701):
    if num % 7 == 0 and num % 5 == 0:
        result.append(num)

print(result)