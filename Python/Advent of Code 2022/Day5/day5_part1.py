# AoC Day 5
# Supply Stacks
# Part 1

# Reading in Data
with open("input.txt") as f:
    stacks = 9
    map = [[] for _ in range(stacks)]

    for line in f:
        line = line.strip("\n")

        if "[" in line:
            for x in range(1, stacks*4, 4):
                if line[x] != " ":
                    map[(x+2)//4].insert(0, line[x])
        
        elif line == "" or "move" not in line:
            pass

        else:
            inst = line.split(" ")
            n = int(inst[1])
            i = int(inst[3])-1
            t = int(inst[5])-1
            for crate in range(n):
                map[t].append(map[i].pop())

message = ""
for x in map:
    message += x[-1]
print(message)
