# AoC Day 8
# Treetop Tree House
# Part 2

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

    scores = []
    
    for x in range(length):
        for y in range(length):
            
            value = map[y, x]
            a, b, c, d = 0, 0, 0, 0

            for i in range(len(map[y, x+1:])):
                a += 1
                if map[y, x+1:][i] >= value:
                    break
            for i in range(len(map[y, :x])-1, -1, -1):
                b += 1
                if map[y, :x][i] >= value:
                    break
            for i in range(len(map[y+1:, x])):
                c += 1
                if map[y+1:, x][i] >= value:
                    break
            for i in range(len(map[:y, x])-1, -1, -1):
                d += 1
                if map[:y, x][i] >= value:
                    break

            scores.append(a*b*c*d)

print(max(scores))