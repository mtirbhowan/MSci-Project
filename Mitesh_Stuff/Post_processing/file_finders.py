import glob
import os
import re

# Find date from folder name in raw data folder

date = '13-04-2020'

directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Tares'

for filename in os.listdir(directory):
    l = re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", filename)
    print(l[0])