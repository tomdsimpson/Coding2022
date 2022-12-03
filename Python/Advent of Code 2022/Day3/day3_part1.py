# AoC Day 3
# Rucksack Reorganization
# Part 1

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
    for line in f:
        line=line.strip("\n")
        s1, s2 = line[:(len(line)//2)], line[(len(line)//2):]
        #print(f"Section 1: {s1}, Section 2: {s2}")

        for character in s1:
            if character in s2:
                total += find_score(character)
                break

print(f"Score: {total}")