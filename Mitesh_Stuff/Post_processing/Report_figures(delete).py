""" Need this to open all the calibrated files and calculate the weight for
    each one. """

import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.integrate import simps
import time
import numpy as np

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

files = [filename for filename in os.listdir(directory) if filename.endswith(".csv")]

file = files[19]

df = pd.read_csv(os.path.join(directory, file))

# this turns df column to array
tot = df.Total_Forces.values
t = df.Time.values
left = df.Left_Forces.values
right = df.Right_Forces.values
back = df.Back_Forces.values
front = df.Front_Forces.values


# fig, axs = plt.subplots(3, sharex=True, sharey=True)
# axs[0].plot(t, tot, 'k', label = 'Total forces')
# axs[0].legend(loc="upper right")
# axs[1].plot(t, left,color='red', label = 'Left forces')
# axs[1].plot(t, right, color='b', label='Right forces')
# axs[1].legend(loc="upper right")
# axs[2].plot(t, back,'g', label = 'Back forces')
# axs[2].plot( t, front, 'orange', label = 'Front forces')
# axs[2].legend(loc="upper right")
# axs[2].set_xlabel('Time (s)', size='13')
# axs[1].set_ylabel('Force (N)', size='13')


plt.plot(t, back, 'r', label='Back forces')
plt.plot(t, front, 'g', label='Front forces')
plt.legend()
#plt.plot(t, back-front)
plt.xlabel('Times (s)', size='13')
plt.ylabel('Force (N)', size='13')
plt.show()
size = 13
# plt.plot(t, tot, 'k')
# plt.plot(t, np.ones(len(t))*10.75, ':', color='r')
# plt.xlabel('Time (s)', size=size)
# plt.xticks(fontsize= size)
# plt.yticks(fontsize= size)
# plt.ylabel('Force (N)', size=size)
# plt.show()