import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.integrate import simps

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

err=[]
acc=[]
m_05 = []
m_10 = []
m_15 = []
m_20 = []


directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):

        filename = filename
        mass = float(filename.split('kg')[0])
        df = pd.read_csv(os.path.join(directory,filename))

        # this turns df column to array
        tot = df.Total_Forces.values
        t = df.Time.values
        left = df.Left_Forces.values
        right = df.Right_Forces.values

        peaks = peak_positions(tot)
        


        
        cycle_positions = gait_cycle_positions(peaks)

        
        for a, b in cycle_positions:
            area = simps(y=tot[a:b+1], x=t[a:b+1])
            mg = area/(t[b+1]-t[a])
            m = mg/9.807
            
            if mass == 0.5:
                m_05.append(m)
                accuracy = abs((m-0.5)*100/m)
                acc.append(accuracy)
                error = m-0.5
                err.append(error)
            elif mass ==1.0:
                m_10.append(m)
                accuracy = abs((m-1.0)*100/m)
                acc.append(accuracy)
                error = m-1.0
                err.append(error)
                #print('1:', m)
            elif mass ==1.5:
                accuracy = abs((m-1.5)*100/m)
                acc.append(accuracy)
                #print('1.5:', m)
                m_15.append(m)
                error = m-1.5
                err.append(error)
            elif mass ==2.0:
                accuracy = abs((m-2.0)*100/m)
                acc.append(accuracy)
                #print('2.0:', m)
                m_20.append(m)
                error = m-2.0
                err.append(error)
            print('-------')
    else:
        continue

# difference = np.array(difference)
# plt.hist(difference, bins=38)
acc = np.array(acc)
plt.hist(acc, bins=range(0, 101), edgecolor='black', normed=1, color='cornflowerblue')#, hatch='/')
plt.xlabel('Accuracy (%)', size='12')
plt.ylabel('Frequency density', size='12')
plt.xlim([-1,27])
plt.show()

size = 13
err = np.array(err)
plt.hist(err,bins=np.arange(-0.5, 1,0.05), edgecolor='black', color='cornflowerblue')
plt.xlabel('Error (kg)', size=size)
plt.ylabel('Frequency', size=size)
plt.xticks(fontsize= size)
plt.yticks(fontsize= size)
plt.show()

len(np.where(acc<23)[0])
print(8*100/342)

m_05 = np.array(m_05)
m_10 = np.array(m_10)
m_15 = np.array(m_15)
m_20 = np.array(m_20)

y5 = np.mean(m_05)
y5err = np.std(m_05)

y10 = np.mean(m_10)
y10err = np.std(m_10)

y15 = np.mean(m_15)
y15err = np.std(m_15)

y20 = np.mean(m_20)
y20err = np.std(m_20)

measured = np.array([y5,y10,y15,y20])
actual = np.array([0.603, 1.1, 1.6, 2.1])
errors = np.array([y5err,y10err,y15err,y20err])
xerror = np.array([0.003,0.01,0.02,0.01])

m, b = np.polyfit(actual, measured, 1)
print(m, b)


plt.errorbar(actual, measured, yerr=errors,xerr=xerror, ls='none')#plt.scatter(measured, actual)
plt.scatter(actual, measured, color='b')
plt.plot(actual, m*actual+b,'red')
plt.xlabel('Actual mass (kg)', size=13)
plt.ylabel('Mass measured by the force plate (kg)', size=13)
plt.xticks(fontsize= size)
plt.yticks(fontsize= size)
plt.show()

