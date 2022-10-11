# Time Calculator for Hiking

times = []
walk_speed = 4
tot = 0
with open("segments.csv", "r") as f:

    for line in f:
        line = (line.strip()).split(",")
        horizontal = float(line[0]) / walk_speed
        
        vertical = float(line[1]) / 600
        if vertical < 0: vertical = 0
        
        times.append(round((horizontal + vertical)*60, 0))
for x in times:
    print(int(x))
    tot += x
print(tot/60)