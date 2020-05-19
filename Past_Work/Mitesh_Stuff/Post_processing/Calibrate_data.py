""" Enter date and this script will, in turn,:
        
    - Open the valid data folders in the raw data directory (in this case,
        valid if  containing 'Kg' in folder name
        
    - Find the mass if said folder
        
    - Open and read the calibration index for that mass' set of data 
        (c. index per mass)
        
    - Iterate through the valid data files (containing, say '2020' in their
        name (other possibility is opening calibration_index.csv (not wanted)))
        
    - Uses the time in the raw file's name to find the corresponding
        raw-tare files (whole raw filename doesn't work for some reason)'
        
    - Get rid of /directory/ in calibration index's filename because / 
        needs to be \. Also, adds .csv to end
        
    - Since tare file path shares same date and folder name, use same
        one as used for raw to open up tare file
        
    - Calibrate as before,
        
    - In some instances, filter function raises ValueError and KeyError,
        use try, except, else to ignore these cases. Add misbehaving files
        to a list to make note of and *FIX WHEN YOU HAVE MORE TIME*
        
    - Make new dataframe for calibrated values, using raw['time(s)'] to 
        inititialise new df
        
    - Save this df as csv ALL IN THE SAME FOLDER (enough info in 
        csv file names to ID)
        """
        
import glob
import os
import pandas as pd
import re
import Post_processing_functions as pp
VE = []
KE = []
badfiles = []
j = 0
# # # Make table of masses to actual masses 1kg --> 1.09kg


# Find date from folder name in raw data folder
date = '26-04-2020'

# OPEN RAW 
raw_loc = r'C:\Users\mtirb\Documents\MSci-Project\Data\Raw Recorded Data'
date = date
tare_loc = r'C:\Users\mtirb\Documents\MSci-Project\Data\Tares'
calibrated_folder = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'


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
                raw_file = pd.read_csv(raw_path) # df

                # Find corresponding tare file here, using calibraion index
                """ For some reason, str.contains method cannot returns 
                Falses when you try and find the whole raw filename
                (minus the .csv) Instead, use time as the unique ID 
                (last hh-mm-ss (-12 to -4 chars b/c of .csv)"""
                 
                time = raw_filename[-12:-4] # use unique time to ID file

                tare_filename = index_data[index_data.iloc[:,0].str.contains(time,case=False)].iloc[:,1][0]
                
                """ Note: formatting not consistent. If date = 13-04-2020 then
                    do this because tare files in calibration index
                    has the format /0.5Kg_Steps/2020-04-13_10-54-39 instead
                    of 2020-04-13_10-54-39.csv: 
                        
                # Note: 
                # 1) 1st column raw, 2nd column tare  
                # 2) returns tare_filename in the format /0.5Kg_Steps/2020-04-13_10-54-39
                
                # Not ideal because os.join can't join because of / needs to be \
                # GRRR do manually
                tare_filename = tare_filename[-19:] +'.csv'
                # Now in format: 2020-04-13_10-54-39.csv"""


                tare_path =  os.path.join(tare_loc,date,folder,tare_filename)
                tare_file = pd.read_csv(tare_path) # df
                
                
                """Calibrate"""
                # (1) Filter 
                try: 
                    filtered_values = pp.filter_values(raw_file)
                except (ValueError):#,KeyError):
                    VE.append([folder,raw_filename])
                except (KeyError):
                    KE.append([folder,raw_filename])
                else:
                    # (2) Calibrate
                    calibrated_forces = pp.post_calibrate_values(filtered_values, tare_file)
                    calibratedLC1 = calibrated_forces[0]
                    calibratedLC2 = calibrated_forces[1]
                    calibratedLC3 = calibrated_forces[2]
                    calibratedLC4 = calibrated_forces[3]
                    
                    
                    # (3) Group forces
                    total_forces, left_forces, right_forces, back_forces, front_forces = pp.group_forces(calibrated_forces)
    
                    # (4) Calibrate timings
                    raw_file['Time'] = pp.calibrate_timings(raw_file)
                    
                    # (5) Make new calibrated df with time column from raw df
                    calibrated_data = raw_file[['Time']].copy()
                    
                    # (6) Add helpful columns of data
                    calibrated_data['Total_Forces'] = total_forces
                    calibrated_data['Left_Forces'] = left_forces
                    calibrated_data['Right_Forces'] = right_forces
                    calibrated_data['Back_Forces'] = back_forces
                    calibrated_data['Front_Forces'] = front_forces
                    calibrated_data['Total_Mass'] = total_forces/9.81

                    calibrated_data['LC1'] =  calibratedLC1
                    calibrated_data['LC2'] =  calibratedLC2
                    calibrated_data['LC3'] =  calibratedLC3
                    calibrated_data['LC4'] =  calibratedLC4
                    
                    # (7) Save df as csv
                    calibrated_filename = '{}kg_({})_{}.csv'.format(mass, date, time)
                    calibrated_path = os.path.join(calibrated_folder, calibrated_filename)
                    calibrated_data.to_csv(calibrated_path)
                
print(len(VE), len(KE))

# Problem with filter function on some data ---> try to debug (see try, except)
# In the meanwhile, append troublesome files to VE, KE (Value/KeyError)                    
#print(len(VE))
# print(len(KE))

# KE
# VE

# calibrated_data.Total_Forces.round(3).mode()

# calibrated_data.Total_Forces.plot.hist()
  
#calibrated_data.plot(x='Time', y='Total_Forces')  

# calibrated_data.Total_Forces.round(2).value_counts()    

#calibrated_data.Total_Forces[calibrated_data.Total_Forces>12].dropna()
