import os
import time

SaveDirectory = os.getcwd()
# SaveAs = os.path.join(SaveDirectory)
# print(SaveDirectory)
files = os.listdir(SaveDirectory)

for file in files:
    print(file)