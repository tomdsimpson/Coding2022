# AoC Day 7
# No Space Left On Device
# Part 1

# Reading in data
with open("input.txt") as f:
    active_dir = []
    dir_sizes = []

    for line in f:
        line = line.strip("\n")

        if line == "$ cd ..":
            dir_sizes.append(active_dir.pop())
        elif line[:4] == "$ cd":
            active_dir.append(0)     
        elif line == "$ ls":
            pass
        elif line[:3] == "dir":
            pass
        else:
            data = line.split(" ")
            for x in range(len(active_dir)):
                active_dir[x] += int(data[0])
    dir_sizes = dir_sizes + active_dir

total = 0
for value in dir_sizes:
    if value <= 100000:
        total += value

print(total)
