# Question 14: Password Strength Checker 

password = input("Enter password: ")

has_lower = False
has_upper = False
has_digit = False
special_count = 0

# Length check (6 to 16 characters)
if 6 <= len(password) <= 16:
    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in "$#@":
            special_count += 1

    # Check Validation 
    if has_lower and has_upper and has_digit and special_count>=2:
        print("Valid Password")
    else:
        print("Invalid Password")
else:
    print("Invalid Password")