import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pandas as pd
import Load_Cell_Data
import copy

GPIO.setmode(GPIO.BCM)



def calculate_CoM( calibrated_values, mid_times , plot_position_values = False, plot_position_over_time = False):
    
    LC_force    = copy.deepcopy( calibrated_values )
    
    
    LC_force = np.asarray(LC_force)
    
    total_force = LC_force[0] + LC_force[1] + LC_force[2] + LC_force[3]
    
    for i in range(len(LC_force)):
        
        for j in range(len(LC_force[i])):
            
            if total_force[j] <= 0.01:
                
                LC_force[i][j] = np.nan
    
    
    x = (LC_force[0]+LC_force[3]) * 1/total_force
    y = (LC_force[2]+LC_force[3]) * 1/total_force
        
    if plot_position_values == True:
        

        fig, (force, position ) = plt.subplots(nrows = 2 ,sharex=True)
                
        for i in range(len(mid_times)):
            
            force    .plot   ( mid_times[i], LC_force[i] , label = 'LC {}'.format(LCs_num[i]) )
            force    .scatter( mid_times[i], LC_force[i]     )            
        
        position .scatter( mid_times[0], x   )
        position .scatter( mid_times[0], y   )
        position .plot   ( mid_times[0], x ,label = 'X Position'  )
        position .plot   ( mid_times[0], y ,label = 'Y Position'  )
                    
        
        force    .legend()
        position .legend()
        
        force    .grid()
        position .grid()
                
        force       .set_title ('Raw Values')
        force       .set_xlabel('Time (s)'  )
        force       .set_ylabel('Output (counts)')
        
        position.set_title ('Calibrated Weights')
        position.set_xlabel('Time (s)'   )
        position.set_ylabel('Weight (Kg)')
        
        plt.show()
    
    if plot_position_over_time == True:
        
        plt.scatter(x,y)
        plt.show()
        
        
LCs_num = [1,2,3,4]
LC_force, filtered_values, calibrated_values, mid_times = Load_Cell_Data.take_raw_values( 1000, plot_compare_filtered = False, plot_with_times = False, plot_weight_calibrated_data = False)
calculate_CoM( calibrated_values, mid_times , plot_position_values = True ,plot_position_over_time = True )