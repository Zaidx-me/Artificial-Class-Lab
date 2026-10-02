# Question 14: Password Validity Checker
import re

password = input("Enter password: ")
is_valid = True

if len(password) < 6 or len(password) > 16:
    is_valid = False
elif not re.search("[a-z]", password):
    is_valid = False
elif not re.search("[A-Z]", password):
    is_valid = False
elif not re.search("[0-9]", password):
    is_valid = False
elif not re.search("[$#@]", password):
    is_valid = False

if is_valid:
    print("Valid Password")
else:
    print("Invalid Password")