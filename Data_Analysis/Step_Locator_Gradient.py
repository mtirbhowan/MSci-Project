import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

import time
import numpy as np
import more_itertools as mit



directory = r'C:\Users\mtirb\Documents\MSci-Project\Data\Calibrated Data'
image_directory = r'C:\Users\mtirb\Documents\UoB\4th Year\Penguin Project\Figures_to_analyse\Peaks_vs_Steps'
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        start = time.time()
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

        
        # plot and save F(t) to count number of successful peaks
        # and to view validity of data
        fig, axs = plt.subplots(2)
        axs[0].plot(t, tot)
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Force (N)')
        axs[0].set_title('{}'.format(filename))
        image_name = filename[:-4] + '.png'
        #plt.savefig(os.path.join(directory,image_name))#'{}.png'.format(filename[:-4]))
        #plt.close()
        
        
        # fig, ax = plt.subplots()
        # ax.plot(t, tot)
        
        # Divide data into N chunks
        N = 26
        t_chunks = np.array_split(t, N)    
        tot_chunks = np.array_split(tot, N)
        
        #
        conditions_met =  []
        
        # in each chunk, fit linear regression line to data.
        for i in range(N):
            x = t_chunks[i]
            y = tot_chunks[i]
            m, b = np.polyfit(x, y, 1)
            # find chunks whose linear regression line: 1) has gradient (m)
            # close to 0; 2) whose mean force value lies within the bodyweight
            # range as expected
            if abs(m) < 0.5 and np.mean(y)>2 and np.mean(y)<(9.81*mass*1.5):
                conditions_met.append(i)

        # group chunks in data which have satisfied above conditions
        grouped = [list(group) for group in mit.consecutive_groups(conditions_met)]
        
        # for consecutive chunks, use mean values
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
        
        #image_name = filename[:-4] + '.png'
        # plt.show()
        # plt.savefig(os.path.join(image_directory,image_name))#'{}.png'.format(filename[:-4]))
        # plt.close()

        
    else:
        continue
    
## [Below is the same as above without explicit loops]
        
# files = [filename for filename in os.listdir(directory) if filename.endswith(".csv")]


# file = files[43] #43
# df = pd.read_csv(os.path.join(directory, file))
# tot = df.Total_Forces.values
# t = df.Time.values
# left = df.Left_Forces.values
# right = df.Right_Forces.values
# back = df.Back_Forces.values
# front = df.Front_Forces.values
# mass = float(file.split('kg')[0])

# fig, ax = plt.subplots(2)
# ax[0].plot(t, tot)
# ax[0].set_ylabel('Total Force (N)', fontsize=14)
# ax[1].plot(t, left, 'r')
# ax[1].plot(t,right,'g')
# ax[1].set_xlabel('Times (s)', fontsize=14)
# ax[1].set_ylabel('Force (N)', fontsize=14)




# fig1, ax = plt.subplots()
# fig2, axs = plt.subplots()
# ax.plot(t, tot)
# ax.grid()
# ax.set_xlabel('Times (s)', fontsize=14)
# ax.set_ylabel('Force (N)', fontsize=14)

# axs.plot(t, tot)
# axs.set_xlabel('Times (s)', fontsize=14)
# axs.set_ylabel('Force (N)', fontsize=14)
# axs.grid()


# N = 26
# t_chunks = np.array_split(t, N)    
# tot_chunks = np.array_split(tot, N)

# conditions_met =  []

# for i in range(N):
#     x = t_chunks[i]
#     y = tot_chunks[i]
#     m, b = np.polyfit(x, y, 1)
#     ax.plot(x, m*x +b)
#     if abs(m) < 0.5 and np.mean(y)>2 and np.mean(y)<(9.81*mass*1.5):
#         conditions_met.append(i)
#         # axs[1].plot(x, m*x +b)
#         # axs[1].annotate("", xy=(x[0],(m*x[0]+b) ), xytext=(x[0], 0),
#         #       arrowprops=dict(arrowstyle="->"))

# grouped = [list(group) for group in mit.consecutive_groups(conditions_met)]


# for indicies in grouped:
#     mean_index = int(round(np.mean(np.array(indicies))))
    
    
#     m = t_chunks[mean_index][0]
    
#     n = tot_chunks[mean_index][0]
#     axs.annotate("", xy=(m,n), xytext=(m, 0),
#                 arrowprops=dict(arrowstyle="->"))

# axs.tick_params(axis="x", labelsize=14)
# axs.tick_params(axis="y", labelsize=14)

# ax.tick_params(axis="x", labelsize=14)
# ax.tick_params(axis="y", labelsize=14)