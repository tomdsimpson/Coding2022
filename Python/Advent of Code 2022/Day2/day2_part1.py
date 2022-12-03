# AoC Day 2
# Rock Paper Scissors
# Part 1

# Reading in Data

with open("input.txt") as f:

    num_con = {"A": 1, "B": 2,"C": 3,"X": 1,"Y": 2,"Z": 3}
    total = 0

    for line in f:
        x = (line.strip("\n")).split(" ")
        x[0], x[1] = num_con[x[0]], num_con[x[1]]

        if x[0] == x[1]:
            total += 3
        elif (x[0])%3+1 == x[1]:
            total += 6
        total += x[1]

    print(total)

print((1+2)%3)