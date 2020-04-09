import pandas as pd
import numpy as np
import time
import glob
import os
import csv

#Saving for testing using data from Load_Cell_Data.record_raw_values
def save_raw_to_csv( raw_values, LCs_num, file_name ):
   
    d  = {}
    df = pd.DataFrame(data=d)
    
    for i in range(len(raw_data)):
        
        datastep      = { 'Load Cell {}'.format( str( LCs_num[i] ) ): raw_values[i] }
        
        dataframestep = pd.DataFrame(data = datastep)
        df            = pd.concat((df, dataframestep),axis=1)
    
    df.to_csv('/home/pi/Documents/MSci-Project/Data/Raw_Data_Testing/{:s}.csv'.format(file_name))
            

def save_raw_data_to_file_from_walk(combined_data, today, custom_title_per_walk=False, custom_title_for_session=False, custom_title_name = False ):
    
    start_time = combined_data[3][1]
    start_time_date = time.strftime('(%Y-%m-%d)_%H-%M-%S', time.localtime(start_time))

    print(start_time_date)
    
    data = {}
    df = pd.DataFrame(data)
    
    for i in range(4):
        datastep = {'Raw Data LC{}'.format(i+1):combined_data[0][i]}
        
        dataframestep = pd.DataFrame(datastep)
        
        df = pd.concat((df,dataframestep),axis=1)
    
    for i in range(4):
        datastep = {'Pretimes LC{}'.format(i+1):combined_data[1][i]}
        
        dataframestep = pd.DataFrame(datastep)
        
        df = pd.concat((df,dataframestep),axis=1)
    
    for i in range(4):
        
        datastep = {'Post Times LC{}'.format(i+1):combined_data[2][i]}
        
        dataframestep = pd.DataFrame(datastep)
        
        df = pd.concat((df,dataframestep),axis=1)
    
    if custom_title_per_run == True:
        custom_title_name = input('Input Custom Title: ')
        save_df = df.to_csv( '/home/pi/Documents/MSci-Project/Data/Raw Recorded Data/{}/{}_{}.csv'.format(today, custom_title_name,start_time_date) )
        link_raw_and_tare(today, "{}_{}".format(custom_title_name, start_time_date) )
        
    elif custom_title == False:
        save_df = df.to_csv( '/home/pi/Documents/MSci-Project/Data/Raw Recorded Data/{}/{}.csv'.format(today, start_time_date) )
        link_raw_and_tare(today, "{}".format( start_time_date) )
        
    elif custom_title_for_run == True:
        save_df = df.to_csv( '/home/pi/Documents/MSci-Project/Data/Raw Recorded Data/{}/{}_{}.csv'.format(today, custom_title_name, start_time_date) )
        link_raw_and_tare(today, "{}_{}".format( custom_title_name, start_time_date) )

def save_tare_to_csv(tare, tare_title, LCs_num):

    save_location = '/home/pi/Documents/MSci-Project/Data/Tares/'
    
    d  = {}
    df = pd.DataFrame(data=d)
    
    for i in range(len(tare[0])):
        
        datastep      = { 'Tare Count Load Cell {}'.format( str( LCs_num[i] ) ): [tare[0][i]], 'Tare Stds Load Cell {}'.format( str( LCs_num[i]) ) : [tare[1][i]] }
        
        dataframestep = pd.DataFrame(data = datastep)
        df            = pd.concat((df, dataframestep),axis=1)
    
    df.to_csv(save_location + '{:s}.csv'.format(tare_title))

def data_from_file( filename, designate_location = False ):
    
    if designate_location == False:
        data_directory = '/home/pi/Documents/MSci-Project/Data/Raw Recorded Data/'
    
    file_to_read = data_directory + filename
    
    dataframe = pd.read_csv( file_to_read )
    
    raw_data  = [dataframe['Raw Data LC1'],dataframe['Raw Data LC2'],dataframe['Raw Data LC3'],dataframe['Raw Data LC4']]
    pretimes  = [dataframe['Pretimes LC1'],dataframe['Pretimes LC2'],dataframe['Pretimes LC3'],dataframe['Pretimes LC4']]
    posttimes = [dataframe['Post Times LC1'],dataframe['Post Times LC2'],dataframe['Post Times LC3'],dataframe['Post Times LC4']]
    
    filtered_values = LC.median_filter_values(raw_data)

    
    return raw_data, pretimes, posttimes, filtered_values


def read_tare_from_file(filename, designate_location = False):
    
    if designate_lcation == False:
        data_directory = '/home/pi/Documents/Msci-Project/Data/Tares/'
    
    file_to_read = data_directory + filename
    
    df = pd.read_csv( fie_to_read )
    
    tare_data = [[df['Tare Count Load Cell 1'],df['Tare Count Load Cell 2'],df['Tare Count Load Cell 3'],df['Tare Count Load Cell 4']],[df['Tare Stds Load Cell 1'],df['Tare Stds Load Cell 2'],df['Tare Stds Load Cell 3'],df['Tare Stds Load Cell 4']]]
    
    return tare_data

def save_CoP_data(x, y, total_force, mid_times, start_time_date):
    
    print('Length x: {}'.format(len(x)))
    print('Length y: {}'.format(len(y)))
    print('Length total_force: {}'.format(len(total_force)))
    print('Length mid_times: {}'.format(len(mid_times)))
    
    
    data = {'x':x,'y':y,'Force (N)':total_force, 'Time':mid_times[0]}
    
    dataframe_to_save = pd.DataFrame(data)
    
    dataframe_to_save.to_csv('/home/pi/Documents/MSci-Project/Data/Calibrated_Walks_Testing/CoM_{}.csv'.format(start_time_date))


def link_raw_and_tare(today, raw_file_name):
    
    """ AT END OF RUN: needs find_latest_tare() to run first.
        
        Takes a raw data file and tare data file 
        then appends the filenames to the index csv for
        easy viewing """
    
    tares_directory = '/home/pi/Documents/MSci-Project/Tares/{}'.format(today)
    
    list_of_files = glob.glob(tares_directory) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    tare_file_name = os.path.basename(latest_file)
    
    
    raw_and_tare = pd.DataFrame({"raw_file":[str(raw_file_name)], 
                        "tare_file":[str(tare_file_name)]}) 
    
    # Need header=True when csv file is first created. Need to turn False as 
    # soon as it has been made to stop headers getting added each time
    with open('/home/pi/Documents/MSci-Project/Raw Recorded Data/{}/Calibration_index.csv'.format(today), 'a') as f:
        raw_and_tare.to_csv(f, header=False)
    
    return

def find_tare_filename(raw_filename):
    """ POST PROCESSING
    Finds tare filename given its corresponding raw filename
        from calibration index csv """
    
    index_data = pd.read_csv('Calibration_index.csv', index_col=0)
    tare_filename = index_data[index_data.raw_file.str.contains(str(raw_filename),case=False)]['tare_file'][0]
    
    return raw_filename, tare_filename
