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
err=[]
acc=[]
m_05 = []
m_10 = []
m_15 = []
m_20 = []

# difference = []

directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        #start = time.time()
        #time.sleep(5)
        filename = filename
        mass = float(filename.split('kg')[0])
        df = pd.read_csv(os.path.join(directory,filename))

        # this turns df column to array
        tot = df.Total_Forces.values
        t = df.Time.values
        left = df.Left_Forces.values
        right = df.Right_Forces.values
        # back = df.Back_Forces.values
        # front = df.Front_Forces.values
        
        # ar = simps(y=right, x=t)
        # al = simps(y=left, x=t)
        # fr = ar/t[-1]-t[0]
        # fl = al/t[-1]-t[0]
        
        # diff = fl-fr
        
        # difference.append(diff)
        
        # use peak finder to find positions of peaks in total_force data
        # returns the indicies of peaks
        peaks = peak_positions(tot)
        
        # plot and save F(t) to count number of successful peaks
        # and to view validity of data!
        # fig, ax = plt.subplots()
        # ax.plot(t, tot)
        # ax.set_xlabel('Time (s)')
        # ax.set_ylabel('Force (N)')
        # ax.set_title('{}'.format(filename))
        # ax.plot(t[peaks], tot[peaks], "x")
        #image_name = filename[:-4] + '.png'
        #plt.savefig(os.path.join(directory,image_name))#'{}.png'.format(filename[:-4]))
        #plt.close()

        
        cycle_positions = gait_cycle_positions(peaks)
        #print(filename, ':')
        #print(cycle_positions)
        #print('----------')
        
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

# # y = a*x + b
# # a = 1.05 pm 0.04
# # b = 0.05 pm 0.05


# # print(np.mean([0.60143, 0.60574]))

"""

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

# plt.plot(t,back, color='r', label='left forces')
# plt.plot(t,front, color='g',label='right forces')
# plt.xlabel('t (s)', fontsize=14)
# plt.ylabel('F(N)', fontsize=14)
# a = 160
# b = 520
# plt.fill_between(t[a:b], tot[a:b], edgecolor='k', hatch="/", facecolor='cornflowerblue')
# # plt.plot(t, [1.6*9.81]*len(t), '--', color='r')
# plt.show()

plt.plot(t,tot) # 100, 510
plt.show()

x = np.arange(0, 9)
y = np.arange(0, 10)

print(simps(y,x))

idx = (np.abs(t - 8.0)).argmin()
print(idx)

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


"""
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