import glob
import os
import pandas as pd
import re

i = 0
# # # Make table of masses to actual masses 1kg --> 1.09kg


# Find date from folder name in raw data folder
date = '13-04-2020'

# OPEN RAW 
raw_loc = r'C:\Users\mtirb\Documents\MSci-Project\Data\Raw Recorded Data'
date = date
tare_loc = r'C:\Users\mtirb\Documents\MSci-Project\Data\Tares'

# find date's data
for folder in os.listdir(os.path.join(raw_loc, date)):
    
    # find valid data folders i.e don't open testing
    if "Kg" in folder:
        # printing folders here gives 0.5Kg_Steps,...

        # determine mass used from folder name
        mass = float(folder.split('Kg')[0])
        
        # open calibration index for \date\xKg here
        index_path = os.path.join(raw_loc,date,folder,'Calibration_index.csv')
        index_data = pd.read_csv(index_path, index_col=0, header=None)     

        
        # All data files in given date folder
        for raw_filename in os.listdir(os.path.join(raw_loc, date, folder)):
            # find valid data files i.e don't open index.csv
            
            if "2020" in raw_filename:
                print('folder: ', folder)
                print('raw data file: ', raw_filename)
                # Open raw data file as df
                raw_path = os.path.join(raw_loc,date,folder,raw_filename)
                raw_file = pd.read_csv(raw_path)

                # Find corresponding tare file here, using calibraion index
                """ For some reason, str.contains method cannot returns 
                Falses when you try and find the whole raw filename
                (minus the .csv) Instead, use time as the unique ID 
                (last hh-mm-ss (-12 to -4 chars b/c of .csv)"""

                tare_filename = index_data[index_data.iloc[:,0].str.contains(raw_filename[-12:-4],case=False)].iloc[:,1][0]#['2'] used to be ['tare_ file', header of tarefilename column in df]

                # Note: 
                # 1) 1st column raw, 2nd column tare  
                # 2) returns tare_filename in the format /0.5Kg_Steps/2020-04-13_10-54-39
                
                # Not ideal because os.join can't join because of / needs to be \
                # GRRR do manually
                tare_filename = tare_filename[-19:] +'.csv'
                # Now in format: 2020-04-13_10-54-39.csv
                print('tare data file: ', tare_filename)
                tare_path =  os.path.join(tare_loc,date,folder,tare_filename)
                tare_file = pd.read_csv(tare_path)
                print('---------', '\n')
                
                # RAWS AND TARES OPEN(!)

                




  
        
