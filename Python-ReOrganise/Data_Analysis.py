import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pandas as pd
import Centre_of_mass_calc as CoM
import Load_Cell_Data as LC

# def get_saved_tare( filename, designate_location = False ):
    
    

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
        
        
raw_data, pretimes, posttimes = calibrated_data_from_file('2020-03-09 14:51:41.csv')
step_locator( , plot=True)
    
