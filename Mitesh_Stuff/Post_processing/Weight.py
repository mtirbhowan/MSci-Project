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


m_05 = []
m_10 = []
m_15 = []

directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'
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
    
        # use peak finder to find positions of peaks in total_force data
        # returns the indicies of peaks
        peaks = peak_positions(tot)
        
        # plot and save F(t) to count number of successful peaks
        # and to view validity of data!
        fig, ax = plt.subplots()
        ax.plot(t, tot)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Force (N)')
        ax.set_title('{}'.format(filename))
        ax.plot(t[peaks], tot[peaks], "x")
        #image_name = filename[:-4] + '.png'
        #plt.savefig(os.path.join(directory,image_name))#'{}.png'.format(filename[:-4]))
        #plt.close()

        
        # cycle_positions = gait_cycle_positions(peaks)
        # print(filename, ':')
        # print(cycle_positions)
        # print('----------')
        
        # for a, b in cycle_positions:
        #     area = simps(y=tot[a:b+1], x=t[a:b+1])
        #     mg = area/(t[b+1]-t[a])
        #     m = mg/9.81
            
        #     if mass == 0.5:
        #         m_05.append(m)
        #     elif mass ==1.0:
        #         m_10.append(m)
        #         print('1:', m)
        #     elif mass ==1.5:
        #         print('1.5:', m)
        #         m_15.append(m)
        #     print('-------')
    else:
        continue

m_05 = np.mean(np.array(m_05))
m_10 = np.mean(np.array(m_10))
m_15 = np.mean(np.array(m_15))

# measured = np.array([m_05,m_10,m_15]) - 0.1
# actual = np.array([0.5, 1.0, 1.5])

# plt.scatter(measured, actual)
# plt.show()








# filename = '1.5kg_(13-04-2020)_11-13-03.csv'

# mass = float(filename.split('kg')[0])

# df = pd.read_csv(os.path.join(directory,filename))

# # this turns df column to array
# tot = df.Total_Forces.values
# time = df.Time.values
# left = df.Left_Forces.values
# right = df.Right_Forces.values
# back = df.Back_Forces.values
# front = df.Front_Forces.values

# peaks = peak_positions(tot)

# plt.plot(tot)
# plt.plot(peaks, tot[peaks], "x")
# plt.show()


# peaks, _ = find_peaks(tot, prominence=(1))



# plt.plot(tot)
# plt.plot(peaks, tot[peaks], "x")
# plt.show()

# a = peaks[-2]
# b = peaks[-1]
# integrand = tot[a:b+1]
# area = simps(y=integrand, x=time[a:b+1])

# mass=[]
# for i in range(0,len(peaks)-2):
#     print(i)
#     a = peaks[i]
#     b = peaks[i+2]
#     area = simps(y=tot[a:b+1], x=time[a:b+1])
#     mg = area/(time[b+1]-time[a])
#     m = mg/9.81
#     mass.append(m)
# avg_mass = sum(mass)/len(mass)
# print(avg_mass, 'kg')