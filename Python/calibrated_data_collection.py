""" Hope to make this script output UNFILTERED LC1-4 forces
    & total forces ONLY (for spike filtering testing)
    
    from modifiying Load_Cell_Data.py"""

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pandas as pd
import spike_filter

GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering


def setup_load_cells( cells = [1,2,3,4] , debug_cells = False ):
   
    LCs     = []
    LCs_num = []
    
    for i in cells:
        
        if i == 1:
            LC_1 = HX711(dout_pin=21, pd_sck_pin=20)
            LC_1.select_channel('A')
            LCs.append(LC_1)
            LCs_num.append(1)
            
        if i == 2:
            LC_2 = HX711(dout_pin=5, pd_sck_pin=0)
            LCs.append(LC_2)
            LCs_num.append(2)
            
        if i == 3:
            LC_3 = HX711(dout_pin=13, pd_sck_pin=6)
            LCs.append(LC_3)
            LCs_num.append(3)
            
        if i == 4:
            LC_4 = HX711(dout_pin=26 , pd_sck_pin=19 )
            LCs.append(LC_4)
            LCs_num.append(4)
    
    if debug_cells == True:
        
        try:
            LC_1.set_debug_mode(flag=True)
            LC_2.set_debug_mode(flag=True)
            LC_3.set_debug_mode(flag=True)
            LC_4.set_debug_mode(flag=True)
        except:
            pass

    
    return LCs, LCs_num

def record_raw_values(number_of_measurements, LCs ):
    """ records and returns raw recordings"""
    raw_values = []
     
    for i in range(len(LCs)):
        raw_values .append([])
    
    for j in range(number_of_measurements):
        
        for i in range(len(LCs)):
            
            raw_values[i].append(LCs[i]._read())

    return raw_values

# def median_filter_values(raw_values):
#     
#     filtered_values = []
#     
#     for i in range(len(raw_values)):
#         
#         filtered_values.append([])
#         filtered_values[i] = sig.medfilt(raw_values[i],5)
#     
#     return filtered_values

# def spike_filter_values(raw_values, df = False, col = False, data_array=True):
#     
#     filtered_values = []
#     
#     for i in range(len(raw_values)):
#         
#         filtered_values.append([])
#         filtered_values[i] = spike_filter.spike_filter(raw_values[i], col = False, data_array=data_array)
#     
#     return filtered_values


# def save_raw_to_csv(raw_data, LCs_num, file_name ):
#    
#     d  = {}
#     df = pd.DataFrame(data=d)
#     
#     for i in range(len(raw_data)):
#         
#         datastep      = { 'Load Cell {}'.format( str( LCs_num[i] ) ): raw_data[i] }
#         
#         dataframestep = pd.DataFrame(data = datastep)
#         df            = pd.concat((df, dataframestep),axis=1)
#     
#     df.to_csv('/home/pi/Documents/MSci-Project/Data/Raw_Data_Testing/{:s}.csv'.format(file_name))
            

def calibrate_values(raw_data, tare, load_cells_to_test ):
    
    LC_1 = [  93022.3786, 112.6440*1000/9.807] #calibration coef for counts to Newtons
    LC_2 = [ 112752.4543, 114.1429*1000/9.807]
    LC_3 = [ -76321.8141, 113.9544*1000/9.807]
    LC_4 = [ 230100.9711, 113.3840*1000/9.807]
    
    LC_calibration_coef = [LC_1,LC_2,LC_3,LC_4] #sort to array
    
    calibrated_force = [] # In Newtons
    # Next run through number of load cells and calibrate counts to new array
    
    for i in range(len(raw_data)):
        
        calibrated_force.append([])        
        
        for j in range(len(raw_data[i])):
            
            subtracted_data = (raw_data[i][j] - LC_calibration_coef[load_cells_to_test[i]-1][0] - tare[0][load_cells_to_test[i]-1] )
            
            force_gram = (subtracted_data / LC_calibration_coef[load_cells_to_test[i]-1][1]) 
        
            calibrated_force[i].append(force_gram)
    
    return calibrated_force

def save_calibrated_to_csv(calibrated_data, LCs_num, file_name ):
    """ Note: unfiltered calibrated data """
    d  = {}
    df = pd.DataFrame(data=d)
    
    for i in range(len(calibrated_data)):
        
        datastep      = { 'Load Cell {}'.format( str( LCs_num[i] ) ): calibrated_data[i] }
        
        dataframestep = pd.DataFrame(data = datastep)
        df            = pd.concat((df, dataframestep),axis=1)
    
    df.to_csv('/home/pi/Documents/MSci-Project/Data/Calibrated_Data_Testing/{:s}.csv'.format(file_name))
   
   
def take_tare( LCs, LCs_num , med_filt = False,
               save_tare = True):
    
    
    tare_stds = 10000
    max_stds  = 1000
    
    while tare_stds >= max_stds:
        
        print('Recording Tare in : 3')
        time.sleep(1)
        print('                    2')
        time.sleep(1)
        print('                    1')
        time.sleep(1)
        print('Recording..')
        
        raw_values =  record_raw_values(200, LCs )
        
        start_time = total_and_start[1]    
    
        LC_offsets = [ 93022.3786, 112752.4543, -76321.8141, 230100.9711]
        
        tare = [[],[]]
        
        filtered_values = []
        
        
        if med_filt == True:
        
            for i in range(len(raw_values)):
                
                filter_name = ('Median')
                
                filtered_values.append(sig.medfilt(raw_values[i],5))
                
                tare[0].append(np.mean  (filtered_values[i]) - LC_offsets[i])
                tare[1].append(np.std   (filtered_values[i]))
                        
        else:
            
            for i in range(len(raw_values)):
                
                filter_name = ('Spike')
                
                filtered_values.append(spike_filter.spike_filter(raw_values[i], 0, data_array = True))
                
                tare[0].append(np.mean  (filtered_values[i]) - LC_offsets[i])
                tare[1].append(np.std   (filtered_values[i]))

        tare_stds = np.sum(tare[1])
        
        print('Tare Stds = {}'.format(tare[1]))
        print('Summed Tare stds = {}'.format(tare_stds))
    
    Default_Tares = [-32800,95200,95800,87050]
    
    for i in range(len(LCs_num)):
        print('Tares Recorded: LC1: Default = {} , Recorded: {}, '.format(Default_Tares[i],tare[0][i]))
    

    
    time.sleep(1)
    

    

    start_time_date = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start_time))
    
    if save_tare == True:
    
        tare_title = 'TARE_'+ start_time_date
        save_tare_to_csv(tare, tare_title, LCs_num)
    
    return tare
    

def save_tare_to_csv(tare, tare_title, LCs_num):

    save_location = '/home/pi/Documents/MSci-Project/Data/Tares/'
    
    d  = {}
    df = pd.DataFrame(data=d)
    
    for i in range(len(tare[0])):
        
        datastep      = { 'Tare Count Load Cell {}'.format( str( LCs_num[i] ) ): [tare[0][i]], 'Tare Stds Load Cell {}'.format( str( LCs_num[i]) ) : [tare[1][i]] }
        
        dataframestep = pd.DataFrame(data = datastep)
        df            = pd.concat((df, dataframestep),axis=1)
    
    df.to_csv(save_location + '{:s}.csv'.format(tare_title))

def take_run(number_of_measurements, use_default_tare = False, to_filter=False, med_filt = False, debug = False, plot_compare_filtered = False, plot_force_calibrated_data = False):
    
    # Setup Load Cells To Read

    load_cells_to_test_array = [1,2,3,4]
     
    LCs, LCs_num  = setup_load_cells( cells = load_cells_to_test_array , debug_cells = debug )
    
    ## Data collection

    # Tare measurements 
    
    if use_default_tare == False:
        
        tare = take_tare( LCs, LCs_num, med_filt = med_filt )
    
    #Run Measurements
    
    print('\n')
    print('Starting Recording in: 3')
    time.sleep(1)
    for i in range(2):
        
        print('                       {}'.format(2-i))
        time.sleep(1)
        
    print('\n')
    print('Start')
    
    raw_values = record_raw_values(number_of_measurements ,LCs)
   
    print('\n')
    print('End Recording')
    print('\n')
    
    ############################## Filter, Caluculate Times, and Calibrate ################################
    if to_filter == True:
        
        if med_filt == True:
        
            filtered_values = median_filter_values(raw_values)
            
        else:
            
            filtered_values = spike_filter_values(raw_values)
    
    ######################################### START HERE ##################################################
    
    if use_default_tare == True:
    
        tare = [[-32815,95200,95800,87050],[]]
    
    calibrated_values = calibrate_values(raw_values, tare, load_cells_to_test_array)

    
    
    #######################################################################################################
    ####################################### Plot Measurement Data #########################################
    #######################################################################################################
    
    
    ########################################## Raw and Filtered ###########################################
    
#     if plot_compare_filtered == True:
#         
#         fig, (raw_ax, filtered_ax) = plt.subplots(nrows = 2 ,sharex=True)
#         fig.suptitle('Recorded Raw Values and \n Spike Filtered {} Measurements \n {}s Time'.format( str(number_of_measurements) , str(total_and_start[0]) ) )
#         
#         for i in range(len(mid_times)):
#             
#             raw_ax      .plot( mid_times[i], raw_values[i]       , label = 'LC {}'.format(LCs_num[i]) )
#             filtered_ax .plot( mid_times[i], filtered_values[i]  , label = 'LC {}'.format(LCs_num[i]) )
#             
#             raw_ax      .scatter(mid_times[i], raw_values[i]     )            
#             filtered_ax .scatter(mid_times[i], filtered_values[i]     )
#                     
#         
#         filtered_ax .legend()
#         
#         raw_ax      .grid()
#         filtered_ax .grid()
#                 
#         raw_ax      .set_title ('Raw Values')
#         raw_ax      .set_xlabel('Time (s)')
#         raw_ax      .set_ylabel('Output (counts)')
#         
#         filtered_ax .set_title('Median Filtered Values')
#         filtered_ax .set_xlabel('Time (s)')
#         filtered_ax .set_ylabel('Output (counts)')
#         
#         plt.show()

    ##################################### Time Data with Filtered ##########################################


    
#     if plot_force_calibrated_data == True:
#         
#         fig, (raw_ax, calibrated_ax) = plt.subplots(nrows = 2 ,sharex=True)
#         fig.suptitle('Recorded Raw Values and \n Spike calibrated {} Measurements \n {}s Time'.format( str(number_of_measurements) , str(total_and_start[0]) ) )
#         
#         for i in range(len(mid_times)):
#             
#             raw_ax        .plot   ( mid_times[i], raw_values[i]         , label = 'LC {}'.format(LCs_num[i]) )
#             calibrated_ax .plot   ( mid_times[i], calibrated_values[i]  , label = 'LC {}'.format(LCs_num[i]) )
#             
#             raw_ax        .scatter(mid_times[i], raw_values[i]     )            
#             calibrated_ax .scatter(mid_times[i], calibrated_values[i]     )
#                     
#         
#         calibrated_ax .legend()
#         
#         raw_ax        .grid()
#         calibrated_ax .grid()
#                 
#         raw_ax       .set_title ('Raw Values')
#         raw_ax       .set_xlabel('Time (s)'  )
#         raw_ax       .set_ylabel('Output (counts)')
#         
#         calibrated_ax.set_title ('Calibrated Force')
#         calibrated_ax.set_xlabel('Time (s)'   )
#         calibrated_ax.set_ylabel('Force (N)')
#         
#         plt.show()
        
    
    save = input('Save calibrated data to /Load cell Testing/(name).csv? (Y/N): ')
    
    if save == 'Y' or save == 'y':
        
        save_title = input('Filename to save: ')
        
        save_calibrated_to_csv (calibrated_values, LCs_num, save_title )
        
    return calibrated_values

     
   
if __name__ == '__main__':
    take_run ( 1000, med_filt = True, plot_compare_filtered = False,plot_force_calibrated_data = True)



