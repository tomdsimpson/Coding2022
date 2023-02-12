# AoC Day 9
# Rope Bridge
# Part 1

# Defining Functions
def check_adj(p1, p2):

    if abs(p1["x"] - p2["x"]) > 1:
        return False
    if abs(p1["y"] - p2["y"]) > 1:
        return False
    return True



# Reading in data
with open("input.txt") as f:

    hp = {"x":0, "y":0}
    tp = {"x":0, "y":0}
    locales = {}
    locales[(tp["x"], tp["y"])] = 1

    for line in f:
        line = line.strip()
        move = int(line.split(" ")[1])

        if line[0] == "U":
            for i in range(move):
                hp["y"] += 1
                if check_adj(hp, tp):
                    pass
                else:
                    tp["y"] += 1
                    tp["x"] = hp["x"]
                    locales[(tp["x"], tp["y"])] = 1

        elif line[0] == "R":
             for i in range(move):
                hp["x"] += 1
                if check_adj(hp, tp):
                    pass
                else:
                    tp["x"] += 1
                    tp["y"] = hp["y"]
                    locales[(tp["x"], tp["y"])] = 1

        elif line[0] == "D":
            for i in range(move):
                hp["y"] -= 1
                if check_adj(hp, tp):
                    pass
                else:
                    tp["y"] -= 1
                    tp["x"] = hp["x"]
                    locales[(tp["x"], tp["y"])] = 1       

        elif line[0] == "L":
            for i in range(move):
                hp["x"] -= 1
                if check_adj(hp, tp):
                    pass
                else:
                    tp["x"] -= 1
                    tp["y"] = hp["y"]
                    locales[(tp["x"], tp["y"])] = 1

print(f"Unique Coordinates: {len(locales.keys())}")