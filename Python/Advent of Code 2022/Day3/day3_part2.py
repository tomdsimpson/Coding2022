# AoC Day 3
# Rucksack Reorganization
# Part 2

# Finding priority
def find_score(character):
    if character.isupper():
        score = ord(character) - 38
    else:
        score = ord(character) - 96
    return score

# Reading in the data
with open("input.txt") as f:

    total = 0
    group = []
    for counter, line in enumerate(f):
        if counter % 3 == 0:
            group = []
        group.append(line.strip())
        if len(group) == 3:
            for char in group[0]:
                if char in group[1] and char in group[2]:
                    total += find_score(char)
                    break

print(f"Score: {total}")