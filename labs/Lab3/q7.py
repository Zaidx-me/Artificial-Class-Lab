# Question 7: Print Item and Type from List

datalist = [
            1452, 11.23, 1+2j, True, 'w3resource', 
            (0, -1), [5, 12], {"class": 'V', "section": 'A'},
            {1,4,7,7,8,9}
            ]

for item in datalist:
    print(f"Item: {item}, Type: {type(item)}")