# AoC Day 8
# Treetop Tree House
# Part 1

# [y, x] Remeber

# importing modules
import numpy as np


# Reading in data
with open("input.txt") as f:
    map = np.zeros((99, 99), int)
    total = 0
    length = 99

    for x, line in enumerate(f):
        for y, height in enumerate(line.strip()):
            map[x][y] = height

    for x in range(1, length - 1):
        for y in range(1, length - 1):

            if map[y, x] > max(map[y, x+1:]):
                total += 1
            elif map[y, x] > max(map[y, :x]):
                total += 1
            elif map[y, x] > max(map[y+1:, x]):
                total += 1
            elif map[y, x] > max(map[:y, x]):
                total += 1

    print(total + 4*length - 4)
