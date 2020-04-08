import pandas as pd
import matplotlib.pyplot as plt

directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Raw Recorded Data'
file = '\\2kg_2020-03-23_22-26-51.csv'
path = directory  + file

df = pd.read_csv(path)

len(df) # number of rows

# for i in range(2,3):
#     df['LC{} Time Taken'.format(i)] = df['Post Times LC{}'.format(i)] - df['Pretimes LC{}'.format(i)]


# df['Pretimes LC2'].plot()
# plt.show()

""" Creates folder of todays date ONCE and only ONCE"""
# import os
# import datetime

# today = datetime.date.today()
# today = today.strftime('%d-%m-%Y')
# if not os.path.exists('{}'.format(today)):
#     os.makedirs('{}'.format(today))
    
""" Creates incrementing filenames"""
# i = 0
# while os.path.exists("sample({}).txt".format(i)):
#     i += 1


# fh = open("sample({}).txt".format(i), "w")
# rs = ['blockresult']
# fh.writelines(rs)
# fh.close()

""" Finds x kg from filename"""
# s1 = '2kg_2020-03-23_22-23-13.csv'
# mass = float(s1.split('kg')[0])


import os
# for filename in os.listdir(directory):
    # print(filename)
import re
from datetime import datetime

for filename in os.listdir(directory):

    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    date = datetime.strptime(match.group(), '%Y-%m-%d').date()        
    
    print(date)
    
