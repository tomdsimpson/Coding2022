from genericpath import isfile
import os

# Folder Path
base_root = "/home/tom/Desktop/DofE_Silver/JPG/"
files = []

def insertionSort(arr):
 
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
 
        key = int(arr[i][4:-4])
        key2 = arr[i]
 
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >=0 and key < int(arr[j][4:-4]) :
                arr[j+1] = arr[j]
                j -= 1
        arr[j+1] = key2

    return arr

for path in os.listdir(base_root):
    if os.path.isfile(os.path.join(base_root, path)):
        files.append(path)

files = insertionSort(files)
for x in files:print(x)


for x, picture in enumerate(files):
    new_name = f"Silver_Exp{x+1}.JPG"
    os.rename(base_root + picture, base_root + new_name)
