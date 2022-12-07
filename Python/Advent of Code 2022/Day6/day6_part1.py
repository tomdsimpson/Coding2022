# AoC Day 6
# Tuning Trouble
# Part 1

# Reading in data
with open("input.txt") as f:

    code = ["" for _ in range(4)]

    for line in f:
        for counter, character in enumerate(line):
            code.append(character)
            del(code[0])

            if len(set(code)) == 4 and counter > 4:
                print(counter+1)
                break

