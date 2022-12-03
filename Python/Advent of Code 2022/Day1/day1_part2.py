# AoC Day 1
# Calorie Counting
# Part 2

# Find max algorithm
def find_max(array):
    m = [0, 0, 0]
    for x in array:
        for y in range(3):
            if x > m[y]:
                m.insert(y, x)
                del(m[3])
                break

    return (m[0] + m[1] + m[2])

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