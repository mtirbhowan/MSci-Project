""" Need to insert this into function which records raw and saves.
    Put this after raw_saved, then append 'raw_title.csv'
    and 'linked_tare.csv' filenames into DataFrame"""

import glob
import os
import pandas as pd
import csv

def find_latest_tare(tares_directory):

    """ Searches tare directory to find the most recent 
        tare file.
        
        For use when linking a raw data file with the most
        recent tare.
        
        This must be done as soon as raw data file has
        been created.
    
        Note: Takes directory as string NOT ending with '\'.
        for example: 'C:\\path\folder' """

    tares_directory = tares_directory + '\*'
    list_of_files = glob.glob(tares_directory) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    tare_file = os.path.basename(latest_file)
    
    return tare_file

def link_raw_and_tare(raw_file_name, tare_file_name):
    """ AT END OF RUN: needs find_latest_tare() to run first.
        
        Takes a raw data file and tare data file 
        then appends the filenames to the index csv for
        easy viewing """
        
    raw_and_tare = pd.DataFrame({"raw_file":[str(raw_file_name)], 
                        "tare_file":[str(tare_file_name)]}) 
    
    # Need header=True when csv file is first created. Need to turn False as 
    # soon as it has been made to stop headers getting added each time
    with open('Calibration_index_{}.csv'.format(), 'a') as f:
        raw_and_tare.to_csv(f, header=False)
 
    return

def find_tare_filename(raw_filename):
    """ POST PROCESSING
    Finds tare filename given its corresponding raw filename
        from calibration index csv """
    
    index_data = pd.read_csv('Calibration_index.csv', index_col=0)
    tare_filename = index_data[index_data.raw_file.str.contains(str(raw_filename),case=False)]['tare_file'][0]
    
    return raw_filename, tare_filename

"""
https://stackoverflow.com/questions/29129095/save-additional-attributes-in-pandas-dataframe

def h5store(filename, df, **kwargs):
    store = pd.HDFStore(filename)
    store.put('mydata', df)
    store.get_storer('mydata').attrs.metadata = kwargs
    store.close()

def h5load(store):
    data = store['mydata']
    metadata = store.get_storer('mydata').attrs.metadata
    return data, metadata

a = pd.DataFrame(
    data=pd.np.random.randint(0, 100, (10, 5)), columns=list('ABCED'))

filename = 'data.h5' # path
# metadata = dict(tare_file='TARE.cvs')
# h5store(filename, a, **metadata)
with pd.HDFStore(filename) as store:
    data, metadata = h5load(store)
    
print(metadata['tare_file'])
"""    


#Creating the Second Dataframe using dictionary 
# raw_and_tare = pd.DataFrame({"raw_file":['raw1.csv'], 
#                     "tare_file":['tare1.csv']}) 

# with open('Calibration_index.csv', 'a') as f:
# #     raw_and_tare.to_csv(f, header=False)

# check = pd.read_csv('Calibration_index.csv', index_col=0)

# # Finds row needed! then selects data from column needed(!)	
# check[check.raw_file.str.contains('raw1.csv',case=False)]['raw_file'][0]

# # finds data given index known(!)
# check.iloc[2,:]['raw_file']
