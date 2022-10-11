# Linear Search

# Reading list
import pickle as p
infile = open("numbers", "rb")
numbers = p.load(infile)
infile.close()

# Linear Search
def linear_search(list, target):

    length = len(list)

    for counter in range(length):
        if list[counter] == target:
            print(f"Found at {counter}")
            break

# Running code
linear_search(numbers,6466)