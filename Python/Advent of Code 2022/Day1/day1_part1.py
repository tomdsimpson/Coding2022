# AoC Day 1
# Calorie Counting
# Part 1

# Find max algorithm
def find_max(array):
    m = 0
    for x in array:
        if x > m:
            m = x
    return m

# Reading in data
with open("input.txt") as f:

    totals = [0]
    for line in f:
        if line == "\n":
            totals.append(0)
        else:
            totals[-1] += int(line.strip("\n"))
    
    max = find_max(totals)
    print(max)