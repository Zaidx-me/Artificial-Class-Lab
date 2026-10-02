# Question 10: 2D Array with i * j Values

m = int(input("Enter rows: "))
n = int(input("Enter columns: "))

matrix = []
for i in range(m):
    row = []
    for j in range(n):
        row.append(i * j)
    matrix.append(row)

print(matrix)