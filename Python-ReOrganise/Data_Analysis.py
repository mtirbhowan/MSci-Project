import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pandas as pd
import Load_Cell_Data as LC
import time
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import PatchCollection
import copy
import Data_Load_Save as LS
import Load_Cell_Data as LC

def calculate_CoP( calibrated_values, mid_times , plot_position_values = False, plot_position_over_time = False, save_CoP_data = False):
    
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
    
    if save_CoP_data == True:
        
        LS.save_CoP_data(x,y,total_force, mid_times)

    return x, y, total_force, mid_times


def step_locator( x, y, total_force, mid_times , plot = False):
    
    small_position_change_points = []
    
    derivative_trigger = 1
    
    for i in range(len(x)-1):
        
        position_difference = np.sqrt( (x[i+1]-x[i])**2 + (y[i+1]-y[i])**2 )
        time_difference     = ( mid_times[i+1] - mid_times[i] )
        
        pos_time_derivative = position_difference / time_differece
        
        if pos_time_derivative >= derivative_trigger:
            
            small_position_change_points.append(i)
    print( small_position_change_points )
    
    if plot == True:
        
        fig, (view_ax) = plt.subplots(1)
        
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
        
        
