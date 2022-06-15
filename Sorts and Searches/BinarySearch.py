# Binary Search Iterative

# Reading list
import pickle as p
infile = open("numbers", "rb")
numbers = p.load(infile)
infile.close()

# Binary Search
def binary_search(list, target):

    found = False
    lower = 0
    upper = len(list)-1

    while not found and (lower <= upper):
        midpoint = (upper + lower) // 2
        print(midpoint)

        if list[midpoint] == target:
            found = True
            print(f"Found at {midpoint}")

        elif list[midpoint] > target:
            upper = midpoint

        elif list[midpoint] < target:
            lower = midpoint

# Running code
binary_search(numbers,6466)