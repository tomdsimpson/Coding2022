# My insertion sort

array = [["Tom1", 20], ["Tom2", 50], ["Tom3", 40], ["Tom4", 30], ["Tom5", 10]]

def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

def sort_scores(max_scores):

    for x in range(1, len(max_scores)):
        value = max_scores[x][1]
        pointer = x-1
        while pointer >=0 and value < max_scores[pointer][1]:
            max_scores = swap(max_scores, pointer, pointer +1)
            pointer -= 1
    
    return max_scores

print(array)
array = sort_scores(array)
print(array)