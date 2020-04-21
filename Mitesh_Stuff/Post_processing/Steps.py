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

# for filename in os.listdir(directory):
#     if filename.endswith(".csv"):
#         start = time.time()
#         #time.sleep(5)
#         filename = filename
#         mass = float(filename.split('kg')[0])
#         df = pd.read_csv(os.path.join(directory,filename))

#         # this turns df column to array
#         tot = df.Total_Forces.values
#         t = df.Time.values
#         left = df.Left_Forces.values
#         right = df.Right_Forces.values
#         back = df.Back_Forces.values
#         front = df.Front_Forces.values
        
#         peaksL = peak_positions(left)
#         peaksR = peak_positions(right)
        
#         # plot and save F(t) to count number of successful peaks
#         # and to view validity of data!
#         # plt.plot(right)
#         # plt.plot(peaksR, right[peaksR], "x")
#         # plt.plot(np.diff(right))
        
#         # fig, axs = plt.subplots(2)
#         # fig.suptitle('Vertically stacked subplots')
#         # axs[0].plot(right)
#         # axs[0].plot(peaksR, right[peaksR], "x")
#         # axs[1].plot(abs(np.diff(right).round(1)))
        
        
#         N = 25
#         t_chunks = np.array_split(t, N)    
#         tot_chunks = np.array_split(tot, N)
#         fig, axs = plt.subplots(2)
#         axs[0].plot(t, tot)
#         for i in range(N):
#             x = t_chunks[i]
#             y = tot_chunks[i]
#             m, b = np.polyfit(x, y, 1)
#             axs[0].plot(x, m*x +b)
#             plt.xlabel('Time')
#             plt.ylabel('Right LC Forces')
#             print(m)
        
#         axs[1].plot(t, right)
        
#         M = 30
#         t_chunks = np.array_split(t, M)
#         r_chunks = np.array_split(right, M)
#         for j in range(M):
#             x = t_chunks[j]
#             y = r_chunks[j]
#             m, b = np.polyfit(x, y, 1)
#             axs[1].plot(x, m*x +b)
#         #axs[1].plot(t, left, color='green')
        
        
#         image_name = filename[:-4] + '.png'
#         plt.savefig(os.path.join(image_directory,image_name))#'{}.png'.format(filename[:-4]))
#         plt.close()

        

#     else:
#         continue
   
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
    
    peaksL = peak_positions(left)
    peaksR = peak_positions(right)
    
    
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
    image_name = filename[:-4] + '.png'
    plt.savefig(os.path.join(image_directory,image_name))#'{}.png'.format(filename[:-4]))
    plt.close()

# N = 15
# t_chunks = np.array_split(t, N)    
# r_chunks = np.array_split(right, N)
# plt.plot(t, right)
# for i in range(N):
#     x = t_chunks[i]
#     y = r_chunks[i]
#     m, b = np.polyfit(x, y, 1)
#     plt.plot(x, m*x +b)
#     print(m)
    
