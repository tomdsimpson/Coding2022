# AoC Day 6
# Tuning Trouble
# Part 2

# Reading in data
with open("input.txt") as f:

    code = ["" for _ in range(14)]

    for line in f:
        for counter, character in enumerate(line):
            code.append(character)
            del(code[0])

            if len(set(code)) == 14 and counter > 14:
                print(counter+1)
                break

