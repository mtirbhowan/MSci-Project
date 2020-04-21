""" Need this to open all the calibrated files and find the steps
    for each one. """

import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.integrate import simps
import numpy as np
import more_itertools as mit

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

def integrate_simps(total_forces, time, a, b):
    """ total_forces: F
        time: makes F -> F(t)
        a: lower integration bound (start of gait cycle)
        b: upper integration bound (end of gait cycle)
        """
    integrand = total_forces[a:b+1]
    time_interval = time[a:b+1]
    area = simps(y=integrand, x=time_interval)
    
    return area 

directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'
image_directory = r'C:\Users\mtirb\Documents\UoB\4th Year\Penguin Project\Figures_to_analyse\Steps'
   
files = [f for f in os.listdir(directory) if f.endswith('.csv')]
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


# filename = files[8]
# mass = float(filename.split('kg')[0])
# df = pd.read_csv(os.path.join(directory,filename))

# tot = df.Total_Forces.values
# t = df.Time.values
# left = df.Left_Forces.values
# right = df.Right_Forces.values
# back = df.Back_Forces.values
# front = df.Front_Forces.values
# # xcop = (left - right)*(180/tot)
# # ycop = (front - back)*(342/tot)

# fig, ax = plt.subplots()
# ax.plot(t, back)
# ax.plot(t, front)
# ax.plot(t, back-front, color='r')
# m1, b1 = np.polyfit(t, back-front, 1)