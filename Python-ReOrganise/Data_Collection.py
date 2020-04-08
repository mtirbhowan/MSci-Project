""" [What this script does and what it can output] """

import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pandas as pd
import Load_Cell_Data as LC
import Centre_of_Pressure_Calc as CoP
import Data_Load_Save as LS
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

LCs, LCnums = LC.setup_load_cells()
trigger_value_counts = 10000


def monitor(LCs, LCnums, tare, plot = False, med_filt = False):
    
    LC_offsets = [ 93022.3786, 112752.4543, -76321.8141, 230100.9711]
    
    difference = [0,0,0,0]
    
    print('Begin Monitoring')
    
    ## Runs a monitoring system with a variable value of the trigger value - saves data for cycle that triggers and feeds to penguin_data_recording
    
    while difference[0] <= trigger_value_counts and difference[1] <= trigger_value_counts and difference[2] <= trigger_value_counts and difference[3] <= trigger_value_counts:
        
        raw_values, pre_times, post_times, total_and_start = LC.record_raw_values( 200 , LCs )
        

        if med_filt == True:
            filtered_values = LC.median_filter_values(raw_values)
        else:
            filtered_values = LC.spike_filter_values(raw_values, 0 , data_array=True)
            
        for i in range(4):
            
            difference[i] = (abs(tare[0][i] - np.mean(filtered_values[i]) + LC_offsets[i]))
        
        print('Still Monitoring')
        print('Mean Values: {}, {}, {}, {}'.format( np.mean(filtered_values[0]), np.mean(filtered_values[1]), np.mean(filtered_values[2]), np.mean(filtered_values[3]) ))
        print('Differences: {}, {}, {}, {}'.format( difference[0], difference[1], difference[2], difference[3]))
    
    if plot == True:

        for i in range(4):
            
            plt.plot(raw_values[i],     label='raw'     )
            plt.plot(filtered_values[i],label='filtered')
        
        plt.legend()
        plt.grid()
        plt.show()
    
    # Returns data in combined array to feed to pre_trigger_data in penguin_data_recording 
    
    return [raw_values, pre_times, post_times, total_and_start]

def record_walk( LCs, LCnums , tare, med_filt= False):
    
    start_time = time.time()
    timeout_condition = False
    
    raw_values_rec      = [[],[],[],[]]
    pre_times_rec       = [[],[],[],[]]
    post_times_rec      = [[],[],[],[]]
    total_and_start_rec = []
    
    LC_offsets = [ 93022.3786, 112752.4543, -76321.8141, 230100.9711]
    
    difference = [0,0,0,0]
    
    start_time  = time.time()
    
    record_time = 0 
    
    print('Recording Walk')
    
    while record_time <= 30:
        
        raw_values, pre_times, post_times, total_and_start = LC.record_raw_values( 50 , LCs )
        
#         print('Recorded Raw Values; No.={}'.format(len(raw_values[0])))
        
        for i in range(4):
            
            raw_values_rec[i] += raw_values[i]
            pre_times_rec [i] += pre_times[i]
            post_times_rec[i] += post_times[i]
        
        total_and_start_rec += total_and_start
                
        if med_filt == True:
            filtered_values = LC.median_filter_values(raw_values)
        else:
            filtered_values = LC.spike_filter_values(raw_values, 0, data_array = True)
        
        for i in range(4):
            
            difference[i] = (abs(tare[0][i] - np.mean(filtered_values[i]) + LC_offsets[i]))
        
        if difference[0] + difference[1] + difference[2] + difference[3] <= trigger_value_counts:
            
            print('Minimum counts not met')
            
            break
        
        record_time = time.time() - start_time
        
    if record_time >= 30:
        print('Walk measurement timeout')
        timeout_condition = True
    
    print('Finished measurement cycle')
   
    return [raw_values_rec, pre_times_rec, post_times_rec, total_and_start_rec], timeout_condition

def penguin_data_recording(LCs, LCnums, custom_title = False,tare = False, carryout_CoP=False, save_raw= False, save_CoP=False, plot_CoP = False, plot_tare = False, med_filt = False):
    
    
    if type(tare) == bool:
    
        tare_data = LC.take_tare(LCs, LCnums, plot_tare = plot_tare, med_filt=med_filt)
    
    elif type(tare) != bool:
        
        tare_data = tare
    
    pre_trigger_data  = monitor(LCs, LCnums, tare_data, med_filt=med_filt)
    post_trigger_data, timeout_condition = record_walk(LCs, LCnums, tare_data, med_filt=med_filt)

    combined_data   = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[]]
    
    calibrated_data = []

    for i in range(4):
        
        combined_data[0][i] = pre_trigger_data[0][i] + post_trigger_data[0][i]
        combined_data[1][i] = pre_trigger_data[1][i] + post_trigger_data[1][i]
        combined_data[2][i] = pre_trigger_data[2][i] + post_trigger_data[2][i]
    
    combined_data[3] = pre_trigger_data[3] + post_trigger_data[3]
    
#     print(combined_data[3])
       
    filtered_data     = LC.median_filter_values(combined_data[0])
        
    calibrated_values = LC.calibrate_values(filtered_data, tare_data, LCnums)
    
    
    mid_times, measurement_lengths, time_between_data = LC.calculate_times (combined_data[1], combined_data[2], combined_data[3])
    
    if carryout_CoP == True:

        x, y, total_force, mid_times = CoP.calculate_CoP(calibrated_values, mid_times,plot_position_values=plot_CoP)
        
        if save_CoP == True:
            
            start_time = combined_data[3][1]
            start_time_date = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start_time))
            
            LS.save_CoP_data( x, y, total_force, mid_times, start_time_date )
    
    if save_raw == True:
    
        LS.save_raw_data_to_file_from_walk( combined_data, custom_title=True )
    
    return tare_data, timeout_condition

def continuous_measurement(med_filt = False):
    
    run_number = 0
    tare_taken = False
    
    while run_number >= 0:
        
        run_number += 1
        print('Run Number mod = {}'.format(run_number % 10))
        
        if run_number % 30 == 0 and tare_taken == True:
            print('Tare condition 1')
            take_tare = True
        
        elif tare_taken == False:
            print('Tare condition 2')
            take_tare = True
        
        else:
            print('Tare condition 3')
            take_tare = tare_data
        
        print('Take Tare Condition: {}'.format(take_tare))
        print('Measurement Number: {}'.format(run_number))
        
        tare_data, timeout_condition = penguin_data_recording( LCs, LCnums, tare = take_tare, save_raw = True , med_filt = med_filt)
        tare_taken = True
        if timeout_condition == True:
            tare_taken = False


