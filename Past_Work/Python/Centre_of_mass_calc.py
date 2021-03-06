import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import threading
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
import scipy.signal as sig
import pandas as pd
import Load_Cell_Data
import copy

GPIO.setmode(GPIO.BCM)

def calculate_CoM( calibrated_values, mid_times , plot_position_values = False, plot_position_over_time = False, save_CoM_data = False):
    
    LC_force    = copy.deepcopy( calibrated_values )
    
    
    LC_force = np.asarray(LC_force)
    
    total_force = LC_force[0] + LC_force[1] + LC_force[2] + LC_force[3]
    
    x = (LC_force[0]+LC_force[3]) * 180/total_force #top half of RHS scales to mm
    y = (LC_force[2]+LC_force[3]) * 342/total_force
    
    for i in range(len(x)):
        
        if x[i] >= 227.5 or x[i] <= -46.5:
            x[i] = np.nan
            y[i] = np.nan
            
        if y[i] >= 370 or y[i] <= -24:
            x[i] = np.nan
            y[i] = np.nan

        
    for i in range(len(total_force)):
        
        if total_force[i] <= 0.05:
                
                x[i] = np.nan
                y[i] = np.nan
      
    if plot_position_values == True:
        

        fig = plt.figure(constrained_layout = True)
        
        gs = GridSpec( 3,2, figure = fig )
        
        all_force_ax   = fig.add_subplot(gs[ 0, 0])
        total_force_ax = fig.add_subplot(gs[ 1, 0], sharex = all_force_ax )
        position_ax    = fig.add_subplot(gs[ 2, 0], sharex = all_force_ax )
        view_ax        = fig.add_subplot(gs[ :,-1])
                
        for i in range(len(mid_times)):
            
            all_force_ax    .plot   ( mid_times[i], LC_force[i] , label = 'LC {}'.format(LCs_num[i]) )
#             all_force_ax    .scatter( mid_times[i], LC_force[i]     )            
        
#         position_ax .scatter( mid_times[0], x   )
#         position_ax .scatter( mid_times[0], y   )
        position_ax .plot   ( mid_times[0], x ,label = 'X Position'  )
        position_ax .plot   ( mid_times[0], y ,label = 'Y Position'  )
                    
        
        all_force_ax .legend()
        position_ax  .legend()
        
        all_force_ax .grid()
        position_ax  .grid()
                
        all_force_ax .set_title ('Force on LCs')
        all_force_ax .set_xlabel('Time (s)'  )
        all_force_ax .set_ylabel('Output (counts)')
        
        position_ax .set_title ('Position with Time')
        position_ax .set_xlabel('Time (s)'   )
        position_ax .set_ylabel('Position (mm)')
        
#         print('length')
#         print(len(total_force))
#         print(len(mid_times[0]))
#         
#         total_force_ax .scatter(mid_times[0], total_force)
        total_force_ax .plot   (mid_times[0], total_force)
        
        total_force_ax .set_title ('Total Force')
        total_force_ax .set_xlabel('Time (s)'  )
        total_force_ax .set_ylabel('Weight (N)')
        
        total_force_ax .grid()
        
        viridis = cm.get_cmap('viridis',len(x))
        time_colours = viridis(np.linspace(0,1,len(x)))
        
        LC_positions = [(181.5,0),(0,0),(0,366),(180.5,343)]
        
        patches = []
        
        for i in range(4):
            circle= Circle((LC_positions[i]), 10)
            patches
        
        patches.append(Rectangle((-46.5,-24),width = 274, height = 394))
        
        colours = (0,0,0,0,1)
        FP_collection = PatchCollection(patches, cmap = 'jet',alpha = 0.3)
        FP_collection.set_array(np.array(colours))
        
        view_ax.add_collection(FP_collection)
        
#         print(total_force)        
        
        total_force = np.asarray(total_force)
        
        force_plot_scaled = 50*(total_force/np.max(total_force))
        
        
#         print(force_plot_scaled)
        
        view_ax.scatter(x,y, s=force_plot_scaled,c=mid_times[0],alpha=0.8,edgecolors='black')
        
        view_ax.set_xlabel('X Position (mm)')
        view_ax.set_ylabel('Y Position (mm)')
        
        view_ax.set_xlim(-50,250)
        view_ax.set_ylim(-30,400)
        view_ax.axis('equal')
        
        view_ax.set_title('Force Plate Centre of Pressure Map')
        view_ax.grid()
        
        plt.show()
    
    if save_CoM_data == True:
        
        save_CoM_data(x,y,total_force, mid_times)
    
    len(x)
    len(y)
    len(total_force)
    
    return x, y, total_force, mid_times







if __name__ == '__main__':
    LCs_num = [1,2,3,4]
    
    LC_force, filtered_values, calibrated_values, mid_times = Load_Cell_Data.take_run( 500, plot_compare_filtered = False, plot_with_times = False, plot_force_calibrated_data = False)

    calculate_CoM( calibrated_values, mid_times , plot_position_values = True ,plot_position_over_time = True , save_CoM_data = True)