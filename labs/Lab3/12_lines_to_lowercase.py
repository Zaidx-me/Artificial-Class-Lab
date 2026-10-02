# Question 11: Accept Lines and Print Lowercase (Blank Line to Terminate)

lines = []
print("Enter lines (press Enter on empty line to stop):")

while True:
    line = input()
    if line == "":
        break
    lines.append(line.lower())

for l in lines:
    print(l)