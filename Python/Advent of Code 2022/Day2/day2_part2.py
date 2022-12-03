# AoC Day 2
# Rock Paper Scissors
# Part 2

# Reading in Data

with open("input.txt") as f:

    num_con = {"A": 1, "B": 2,"C": 3}
    total = 0

    for line in f:
        x = (line.strip("\n")).split(" ")

        if x[1] == "X":
            n = num_con[x[0]]-1
            if n == 0: total += 3 
            else: total += n
        elif x[1] == "Y":
            total += num_con[x[0]] + 3
        else:
            total += 6 + (num_con[x[0]] % 3 + 1)


    print(total)
