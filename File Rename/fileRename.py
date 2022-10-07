import os


running = True
counter = 1
rename_root = "/home/tom/Desktop/TomCamera/DSC_"

while running:

    old_name = f"{rename_root}{'0'*(4-len(str(counter)))}{str(counter)} (1).JPG"
    new_name = f"{rename_root}{'0'*(4-len(str(counter+907)))}{str(counter+907)}.JPG"
    #print(old_name, new_name)
    
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
    else:
        print(f"Finished at {counter-1}")
        running = False
    
    counter += 1