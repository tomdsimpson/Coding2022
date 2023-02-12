import math

def move_node(node1, node2):

    # Check distances
    x_dis = node1[0] - node2[0]
    y_dis = node1[1] - node2[1]
    
    if abs(x_dis) < 2 and abs(y_dis) < 2:
        pass # Not getting pulled
    else:
        if x_dis != 0:
            node2[0] += int(math.copysign(1, x_dis))
        if y_dis != 0:
            node2[1] += int(math.copysign(1, y_dis))

    
    return node1, node2




# Reading in data
with open("input.txt") as f:
    positions = {}
    nodes = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    for line in f:
        line = line.strip()
        line = line.split(" ")
        moves = int(line[1])
        
        for x in range(moves):

            if line[0] == "U":
                nodes[0][1] += 1            
            if line[0] == "R":
                nodes[0][0] += 1
            if line[0] == "D":
                nodes[0][1] -= 1
            if line[0] == "L":
                nodes[0][0] -= 1

            for i in range(len(nodes)-1):
                nodes[i], nodes[i+1] = move_node(nodes[i], nodes[i+1])
            positions[(nodes[9][0], nodes[9][1])] = 0

print(len(positions))



