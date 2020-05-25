""" Need this to open all the calibrated files and find the steps
    for each one. """

import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.integrate import simps
import numpy as np
import more_itertools as mit
import copy
from matplotlib.gridspec import GridSpec
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import cm

def peak_positions(total_force_data):
    
    """ Uses scipy.signal.find_peaks to find peaks in F(t) curve. 
        
        Peaks here signify mid-point in transition from left to right 
        foot (or vice-versa) """
    
    peaks, _ = find_peaks(total_force_data, prominence=1)
    
    return peaks

def gait_cycle_positions(peaks):
    """ For a given run, this takes in a list of peak positions (relative
        to total_forces data (i.e numbers possible from 0 to len(total_forces)))
        and groups these up into the bounds for each gait cycle.
        
        One cycle is from i-th peak, to (i+2)-th peak. Therefore, minimum
        len(peaks) necessary is 3.
        
        E.g.for N = 5 peaks, returns:[ [peaks[0],peaks[2]], [peaks[1],peaks[3]],
        [peaks[2], peaks[4]] ]
        
        For N<3, gait_cycle_bounds = []"""
    
    N = len(peaks) # number of peaks
    
    gait_cycle_bounds = []
    
    for i in range(0, N-2): # need i to go from 0 to N-3 (so range N-2)
        
        interval = [peaks[i], peaks[i+2]]
        gait_cycle_bounds.append(interval)
    
    return gait_cycle_bounds



directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'
   
files = [f for f in os.listdir(directory) if f.endswith('.csv')]
"""
for filename in files:
    
    filename = filename
    mass = float(filename.split('kg')[0])
    df = pd.read_csv(os.path.join(directory,filename))
    
    tot = df.Total_Forces.values
    t = df.Time.values
    left = df.Left_Forces.values
    right = df.Right_Forces.values
    back = df.Back_Forces.values
    front = df.Front_Forces.values
    
    N = 25
    t_chunks = np.array_split(t, N)    
    tot_chunks = np.array_split(tot, N)
    
    fig, ax = plt.subplots()
    ax.plot(t, tot)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Force (N)')
    ax.set_title('{}'.format(filename))
    conditions_met =  []
    
    for i in range(N):
        x = t_chunks[i]
        y = tot_chunks[i]
        m, b = np.polyfit(x, y, 1)
        if abs(m) < 0.5 and np.mean(y)>2 and np.mean(y)<(9.81*mass*1.5):
            conditions_met.append(i)
            # If uncommented, plots all that meet above criterion (includes
            # double counts steps)
            # ax.plot(x, m*x +b)
            # ax.annotate("", xy=(x[0],(m*x[0]+b) ), xytext=(x[0], 0),
            #       arrowprops=dict(arrowstyle="->"))

    grouped = [list(group) for group in mit.consecutive_groups(conditions_met)]
    print(grouped)
            
    for j in grouped:
        j = j[0]
        m = t_chunks[j][0]
        n = tot_chunks[j][0]
        ax.annotate("", xy=(m,n), xytext=(m, 0),
                    arrowprops=dict(arrowstyle="->"))
    # image_name = filename[:-4] + '.png'
    # plt.savefig(os.path.join(image_directory,image_name))#'{}.png'.format(filename[:-4]))
    # plt.close()
"""

def calculate_CoP( calibrated_values, mid_times , plot_position_values = False, plot_position_over_time = False, save_CoP_data = False):
    
    LCs_num = [1,2,3,4]
    
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
                
        for i in range(4):
            
            all_force_ax    .plot   ( mid_times, LC_force[i] , label = 'LC {}'.format(LCs_num[i]) )
#             all_force_ax    .scatter( mid_times[i], LC_force[i]     )            
        
#         position_ax .scatter( mid_times[0], x   )
#         position_ax .scatter( mid_times[0], y   )
        position_ax .plot   ( mid_times, x ,label = 'X Position'  )
        position_ax .plot   ( mid_times, y ,label = 'Y Position'  )
                    
        
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
        total_force_ax .plot   (mid_times, total_force)
        
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
        
        view_ax.scatter(x,y, s=force_plot_scaled,c=mid_times,alpha=0.8,edgecolors='black')
        
        view_ax.set_xlabel('X Position (mm)')
        view_ax.set_ylabel('Y Position (mm)')
        
        view_ax.set_xlim(-50,250)
        view_ax.set_ylim(-30,400)
        view_ax.axis('equal')
        
        view_ax.set_title('Force Plate Centre of Pressure Map')
        view_ax.grid()
        
        plt.show()
    


    return x, y, total_force, mid_times


filename = files[5]
mass = float(filename.split('kg')[0])
df = pd.read_csv(os.path.join(directory,filename))

tot = df.Total_Forces.values
t = df.Time.values
left = df.Left_Forces.values
right = df.Right_Forces.values
back = df.Back_Forces.values
front = df.Front_Forces.values
calibrated_vals = [df.LC1.values,df.LC2.values,df.LC3.values,df.LC4.values]




#x, y, total_force, mid_times = calculate_CoP(calibrated_vals, t, plot_position_values = True, plot_position_over_time = False)






x = (right)*(180/tot) # RIGHT = LC1 & 4
y = (front)*(342/tot) # LEFT = LC3 & 4


# plt.plot(t, front)
# plt.show()


for i in range(len(x)):
    
    if x[i] >= 227.5 or x[i] <= -46.5:
        x[i] = np.nan
        y[i] = np.nan
        
    if y[i] >= 370 or y[i] <= -24:
        x[i] = np.nan
        y[i] = np.nan

    
for i in range(len(tot)):
    
    if tot[i] <= 0.05:
            
            x[i] = np.nan
            y[i] = np.nan

from scipy.signal import argrelextrema

maxInd = argrelextrema(x, np.greater)


# plt.scatter(x, y, s=8, color='g')
# plt.scatter(x[maxInd], y[maxInd], s=1,color='red')
plt.plot(t,x)
plt.plot(t,y)
plt.show()

gridx = np.linspace(0, np.nanmax(x), 10)
gridy = np.linspace(0, np.nanmax(y), 10)
plt.gca().set_aspect('equal', adjustable='box')
grid, _, _ = np.histogram2d(x, y, bins=[gridx, gridy])
plt.figure()
plt.gca().set_aspect('equal', adjustable='box')
plt.pcolormesh(gridx, gridy, grid)
plt.plot(x, y, 'ro')
plt.colorbar()

x = x[np.logical_not(np.isnan(x))] 
y = y[np.logical_not(np.isnan(y))] 
plt.plot(x, y, 'ro')
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
plt.colorbar()
arr, x, y, i= plt.hist2d(x,y,bins=15)
maxind = arr.argmax()
print(np.unravel_index(maxind,arr.shape))

from itertools import product
indices = [(i,j,arr[i,j]) for i,j in product(range(len(arr)),range(len(arr[0])))]
sorted_indices = sorted(indices,key= lambda x : x[2],reverse=True)
print(sorted_indices[:7])
print(list(filter(lambda x: x[2]>30,sorted_indices)))

# plt.ylim(0,342)
# plt.xlim(0,180)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.draw()
# plt.show()
            
           

# fig, ax = plt.subplots()
# ax.plot(t, back)
# ax.plot(t, front)
# ax.plot(t, back-front, color='r')
# m1, b1 = np.polyfit(t, back-front, 1)