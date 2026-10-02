# Question 12: Comma-separated 4-digit Binary Divisible by 5

binary_inputs = input("Enter comma separated binary numbers: ").split(',')
divisible_by_5 = []

for b in binary_inputs:
    decimal_val = int(b, 2)
    if decimal_val % 5 == 0:
        divisible_by_5.append(b)

print(",".join(divisible_by_5))