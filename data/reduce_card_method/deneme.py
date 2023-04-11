my_tuple = (1, 2, 3, 4, 4, 5, 6, 6)

repeated_elements = [x for x in my_tuple if my_tuple.count(x) > 1]

if len(repeated_elements) > 0:
    print("Some elements appear more than once:", repeated_elements)
else:
    print("No element appears more than once")