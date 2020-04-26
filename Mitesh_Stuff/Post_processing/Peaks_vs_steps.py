""" Need this to open all the calibrated files and calculate the weight for
    each one. """

import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.integrate import simps
import time
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



m_05 = []
m_10 = []
m_15 = []

directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'
image_directory = r'C:\Users\mtirb\Documents\UoB\4th Year\Penguin Project\Figures_to_analyse\Peaks_vs_Steps'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        start = time.time()
        #time.sleep(5)
        filename = filename
        mass = float(filename.split('kg')[0])
        df = pd.read_csv(os.path.join(directory,filename))

        # this turns df column to array
        tot = df.Total_Forces.values
        t = df.Time.values
        left = df.Left_Forces.values
        right = df.Right_Forces.values
        back = df.Back_Forces.values
        front = df.Front_Forces.values
        
        peaks = peak_positions(tot)
        """
        # plot and save F(t) to count number of successful peaks
        # and to view validity of data!
        fig, axs = plt.subplots(2)
        axs[0].plot(t, tot)
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Force (N)')
        axs[0].set_title('{}'.format(filename))
        axs[0].plot(t[peaks], tot[peaks], "x")
        image_name = filename[:-4] + '.png'
        #plt.savefig(os.path.join(directory,image_name))#'{}.png'.format(filename[:-4]))
        #plt.close()
        """
        
        fig, ax = plt.subplots()
        
        ax.plot(t, left)
        
        N = 26
        t_chunks = np.array_split(t, N)    
        tot_chunks = np.array_split(left, N)
        
        conditions_met =  []
        
        for i in range(N):
            x = t_chunks[i]
            y = tot_chunks[i]
            m, b = np.polyfit(x, y, 1)
            if abs(m) < 0.5 and np.mean(y)>2 and np.mean(y)<(9.81*mass*1.5):
                conditions_met.append(i)
                ax.plot(x, m*x +b)
                ax.annotate("", xy=(x[0],(m*x[0]+b) ), xytext=(x[0], 0),
                      arrowprops=dict(arrowstyle="->"))

        grouped = [list(group) for group in mit.consecutive_groups(conditions_met)]
        
        """     
        for indicies in grouped:
            mean_index = int(round(np.mean(np.array(indicies))))
            
            m = t_chunks[mean_index][0]
            n = tot_chunks[mean_index][0]
            axs[0].annotate("", xy=(m,n), xytext=(m, 0),
                        arrowprops=dict(arrowstyle="->"))
            
        axs[1].plot(t, right)
        axs[1].plot(t, left)
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Force (N)')
        
        image_name = filename[:-4] + '.png'
        plt.show()
        # plt.savefig(os.path.join(image_directory,image_name))#'{}.png'.format(filename[:-4]))
        # plt.close()
        """
        
    else:
        continue


