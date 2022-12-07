# AoC Day 4
# Camp Cleanup
# Part 1

# Reading in data
with open("input.txt") as f:

    total = 0

    for line in f:
        e1, e2 = ((line.strip()).split(","))
        
        e1, e2 = e1.split("-"), e2.split("-")
        e1 = list(range(int(e1[0]), int(e1[1])+1))
        e2 = list(range(int(e2[0]), int(e2[1])+1))

        if len(set((e1+e2))) == len(e1) or len(set((e1+e2))) == len(e2):
            total += 1
print(total)