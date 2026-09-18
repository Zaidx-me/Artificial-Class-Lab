
# for loop, iterating by index

list = ["geeks", "for", "geeks"]

for index in range(len(list)):
    print (list[index])


# Loop Control Statement: Continue
# It brings control back to the beginning of the loop

# Print all letters except "e and "s"

print ("\nPrint all letters except \"e\" and \"s\"")
for letter in "geeksforgeeks":
    if letter == 'e' or letter == 's':
        continue
    
    print('Current letter : ', letter)


# Loop Control Statement: break
# It brings control out of the loop

# break the loop as soon it sees 'e'
print ("\nBreak  the loop as soon it sees \"e\" or \"s\"")

# or 's'

for letter in "geeksforgeeks":
    if letter == 'e' or letter == 's':
        break
    
    print('Current letter : ', letter)

