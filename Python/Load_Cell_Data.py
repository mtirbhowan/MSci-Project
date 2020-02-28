import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pandas as pd


GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering


def setup_load_cells( cells = [1,2,3,4] , debug_cells = False ):
   
    LCs     = []
    LCs_num = []
    
    for i in cells:
        
        if i == 1:
            LC_1 = HX711(dout_pin=21, pd_sck_pin=20)
            LC_1.select_channel('A')
            LCs.append(LC_1)
            LCs_num.append('1')
            
        if i == 2:
            LC_2 = HX711(dout_pin=5, pd_sck_pin=0)
            LCs.append(LC_2)
            LCs_num.append('2')
            
        if i == 3:
            LC_3 = HX711(dout_pin=13, pd_sck_pin=6)
            LCs.append(LC_3)
            LCs_num.append('3')
            
        if i == 4:
            LC_4 = HX711(dout_pin=26 , pd_sck_pin=19 )
            LCs.append(LC_4)
            LCs_num.append('4')
    
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
    
    pre_times  = []
    post_times = []
    raw_values = []
    
    
    for i in range(len(LCs)):
        
        pre_times  .append([])
        post_times .append([])
        raw_values .append([])
        
    print('\n')
    print('Starting Recording in: 3')
    time.sleep(1)
    for i in range(2):
        
        print('                       {}'.format(2-i))
        time.sleep(1)
        
    print('\n')
    print('Start')
    
    start_time = time.time()
    
    for j in range(number_of_measurements):
        
        for i in range(len(LCs)):
            
            pre_times [i].append(time.time())
            raw_values[i].append(LCs[i]._read())
            post_times[i].append(time.time())


    total_record_time = time.time() - start_time
    print('\n')
    print('End Recording')
    print('\n')

    return raw_values, pre_times, post_times, [total_record_time, start_time]

def calculate_times(pre_times, post_times, total_and_start ):
    
    measurement_lengths = []
    mid_times           = []
    time_between        = []
    
    for i in range( len( pre_times ) ):
        
        measurement_lengths.append([])
        mid_times          .append([])
        time_between       .append([0])
    
    
    for i in range(len(pre_times)):
        
        for j in range(len(pre_times[i])):
            
            measurement_lengths[i].append(post_times[i][j]-pre_times[i][j])
            mid_times          [i].append((post_times[i][j]-total_and_start[1])-(measurement_lengths[i][j]/2))
    
        for j in range(len(mid_times[i])-1):
            
            time_between[i].append(mid_times[i][j+1]-mid_times[i][j])
    
    return mid_times, measurement_lengths, time_between


def save_raw_to_csv( raw_data, LCs_num, file_name ):
   
    d  = {}
    df = pd.DataFrame(data=d)
    
    for i in range(len(raw_data)):
        
        datastep      = { 'Load Cell {}'.format( str( LCs_num[i] ) ): raw_data[i] }
        
        dataframestep = pd.DataFrame(data = datastep)
        df            = pd.concat((df, dataframestep),axis=1)
    
    df.to_csv('/home/pi/Documents/Load cell Testing/{:s}.csv'.format(file_name))
            

def calibrate_values( filtered_values, tare_value, load_cells_to_test ):
    
    calibrated_weight = [] # In grams
    
    for i in range(len(filtered_values)):
        
        tare_calibrated_values  = tare_calibrate( filtered_values[i], tare_value[i] )
        
        cooef_calibrated_values = calibrate_from_cooef( tare_calibrated_values, load_cells_to_test[i] )
              
        calibrated_weight.append( cooef_calibrated_values )
        
    return calibrated_weight
   
   
def calibrate_from_cooef( filtered_values_LC , load_cell_number ):
    
    LC_1 = [  93022.3786, 112.6440*1000]
    LC_2 = [ 112752.4543, 114.1429*1000]
    LC_3 = [ -76321.8141, 113.9544*1000]
    LC_4 = [ 230100.9711, 113.3840*1000]
    
#     LC_1 = [ 0, 1]
#     LC_2 = [ 0, 1]
#     LC_3 = [ 0, 1]
#     LC_4 = [ 0, 1]
#     
#     LC_1 = [  93022.3786, 1 ]
#     LC_2 = [ 112752.4543, 1 ]
#     LC_3 = [ -76321.8141, 1 ]
#     LC_4 = [ 230100.9711, 1 ]
    
    
    LC_calibration_cooef = [LC_1,LC_2,LC_3,LC_4]
    
    calibrated_values = []
    
    for i in range(len(filtered_values_LC)):
        
        weight_gram = (filtered_values_LC[i] - LC_calibration_cooef[load_cell_number-1][0]) / LC_calibration_cooef[load_cell_number-1][1]
        
        calibrated_values.append(weight_gram)
        
    return calibrated_values

def tare_calibrate( filtered_values, tare_value ):
    
    tared = []
    
    for i in range(len(filtered_values)):
              
        tared.append( filtered_values[i] - tare_value ) 
            
    return tared

def take_raw_values( number_of_measurements, debug = False , plot_compare_filtered = False, plot_with_times = False , plot_weight_calibrated_data = False ):
    
    #######################################################################################################
    ######################################## Setup Load Cells To Read######################################
    #######################################################################################################
    load_cells_to_test = input('Input load cells to test or hit ENTER to test all 4: ')
    load_cells_to_test_array = []
    
    if load_cells_to_test == '':
    
        load_cells_to_test_array = [1,2,3,4]

    else:
                
        for symb in load_cells_to_test:
            
            try:
                
                load_cells_to_test_array.append(int(symb))
            
            except:
                pass
            
    LCs, LCs_num  = setup_load_cells( cells = load_cells_to_test_array , debug_cells = debug )
    
    #######################################################################################################
    ########################################## Data Collection ############################################
    #######################################################################################################

    ########################################## Tare Measurements ##########################################
    
    # tare_raw, tare_times, tare_times, tare_total_and_start = record_raw_values( 100 , LCs )
    
    ########################################### Run Measurements ##########################################
    
    raw_values, pre_times, post_times, total_and_start = record_raw_values( number_of_measurements , LCs )
   
    
    ############################## Filter, Caluculate Times, and Calibrate ################################
    
    filtered_values = []
    
    for i in range(len(raw_values)):
        
        filtered_values.append([])
        filtered_values[i] = sig.medfilt(raw_values[i],5)
    
    print(len(filtered_values))
    
    ######################################### START HERE ##################################################
    
    tare = [-32815,95200,95800,87050]
    
    # tare = [0,0,0,0]
    
    calibrated_values = calibrate_values( filtered_values, tare, load_cells_to_test_array )
    
    mid_times, measurement_lengths, time_between_data = calculate_times (pre_times, post_times, total_and_start)
    
    #######################################################################################################
    ################################## Print Info on Measurement Times ####################################
    #######################################################################################################
    
    print('Total Time from timer: {}'.format(total_and_start[0]))
    
    total_measurement_lengths = 0
    
    for i in range(len(raw_values)):
        print('Summed time per measurement LC {}: {}'.format(LCs_num[i], ( post_times[i][-1] - pre_times[i][0] ) ) )
        total_measurement_lengths += np.sum(measurement_lengths[i])
    
    print('Summed times total: {}'.format(total_measurement_lengths))
        
    print('Mean Sample Rate: {} Hz'.format(number_of_measurements/total_measurement_lengths))
    
    print('Difference: {}'.format(total_and_start[0] - total_measurement_lengths))
    
    
    #######################################################################################################
    ####################################### Plot Measurement Data #########################################
    #######################################################################################################
    
    
    ########################################## Raw and Filtered ###########################################
    
    if plot_compare_filtered == True:
        
        fig, (raw_ax, filtered_ax) = plt.subplots(nrows = 2 ,sharex=True)
        fig.suptitle('Recorded Raw Values and \n Spike Filtered {} Measurements \n {}s Time'.format( str(number_of_measurements) , str(total_and_start[0]) ) )
        
        for i in range(len(mid_times)):
            
            raw_ax      .plot( mid_times[i], raw_values[i]       , label = 'LC {}'.format(LCs_num[i]) )
            filtered_ax .plot( mid_times[i], filtered_values[i]  , label = 'LC {}'.format(LCs_num[i]) )
            
            raw_ax      .scatter(mid_times[i], raw_values[i]     )            
            filtered_ax .scatter(mid_times[i], filtered_values[i]     )
                    
        
        filtered_ax .legend()
        
        raw_ax      .grid()
        filtered_ax .grid()
                
        raw_ax      .set_title ('Raw Values')
        raw_ax      .set_xlabel('Time (s)')
        raw_ax      .set_ylabel('Output (counts)')
        
        filtered_ax .set_title('Median Filtered Values')
        filtered_ax .set_xlabel('Time (s)')
        filtered_ax .set_ylabel('Output (counts)')
        
        plt.show()

    ##################################### Time Data with Filtered ##########################################

    if plot_with_times == True:
        
        fig, (values_raw, times_per, time_between) = plt.subplots(nrows = 3 ,sharex=True)
        fig.suptitle('Recorded Raw Values and \n Times Taken Per Measurement, {} Measurements \n {}s Time'.format( str(number_of_measurements) , str(total_and_start[0]) ) )
        
        for i in range(len(mid_times)):
            
            values_raw   .plot( mid_times[i], raw_values[i]           , label = 'LC {}'.format(str(LCs_num[i])) )
            times_per    .plot( mid_times[i], measurement_lengths[i]  , label = 'LC {}'.format(str(LCs_num[i])) )
            time_between .plot( mid_times[i], time_between_data[i]    , label = 'LC {}'.format(str(LCs_num[i])) ) 
        
        times_per.legend()
        
        values_raw   .grid()
        times_per    .grid()
        time_between .grid()
        
        values_raw   .set_title ('Raw Values')
        values_raw   .set_xlabel('Time (s)')
        values_raw   .set_ylabel('Output (counts)')
        
        times_per    .set_title ('Time Per Measurement')
        times_per    .set_xlabel('Time (s)')
        times_per    .set_ylabel('Time (s)')
        
        time_between .set_title('Time Between Measurements')
        time_between .set_xlabel('Time (s)')
        time_between .set_ylabel('Time (s)')
        
        plt.show()
    
    if plot_weight_calibrated_data == True:
        
        fig, (raw_ax, calibrated_ax) = plt.subplots(nrows = 2 ,sharex=True)
        fig.suptitle('Recorded Raw Values and \n Spike calibrated {} Measurements \n {}s Time'.format( str(number_of_measurements) , str(total_and_start[0]) ) )
        
        for i in range(len(mid_times)):
            
            raw_ax        .plot   ( mid_times[i], raw_values[i]         , label = 'LC {}'.format(LCs_num[i]) )
            calibrated_ax .plot   ( mid_times[i], calibrated_values[i]  , label = 'LC {}'.format(LCs_num[i]) )
            
            raw_ax        .scatter(mid_times[i], raw_values[i]     )            
            calibrated_ax .scatter(mid_times[i], calibrated_values[i]     )
                    
        
        calibrated_ax .legend()
        
        raw_ax        .grid()
        calibrated_ax .grid()
                
        raw_ax       .set_title ('Raw Values')
        raw_ax       .set_xlabel('Time (s)'  )
        raw_ax       .set_ylabel('Output (counts)')
        
        calibrated_ax.set_title ('Calibrated Weights')
        calibrated_ax.set_xlabel('Time (s)'   )
        calibrated_ax.set_ylabel('Weight (Kg)')
        
        plt.show()
        
      ### Here will be a dank graph with time image of position and force applied to the load cells over time ###
    
    
    save = input('Save Raw Data to /Load cell Testing/(name).csv? (Y/N): ')
    
    if save == 'Y' or save == 'y':
        
        save_title = input('Filename to save: ')
        
        save_raw_to_csv ( raw_values, LCs_num, save_title )
        
    return raw_values, filtered_values, calibrated_values, mid_times
        
    
   
if __name__ == '__main__':
    take_raw_values ( 1000, plot_compare_filtered = False, plot_with_times = False ,plot_weight_calibrated_data = True)


