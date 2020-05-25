"""Finds steps by searching for areas on the top of the force plate
    which have collected the most number of data points"""
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib._png import read_png
from functools import reduce 
from itertools import product

# get calibrated data files
directory = r'./Calibrated Data'
files = [f for f in os.listdir(directory) if f.endswith('.csv')]
filename = files[12]

# find mass from filename
mass = float(filename.split('kg')[0])

# read data
df = pd.read_csv(os.path.join(directory,filename))
tot = df.Total_Forces.values
t = df.Time.values
right = df.Right_Forces.values
front = df.Front_Forces.values
calibrated_vals = [df.LC1.values,df.LC2.values,df.LC3.values,df.LC4.values]



# Calculate COP
x = (right)*(180/tot) # RIGHT = LC1 & 4
y = (front)*(342/tot) # LEFT = LC3 & 4


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

x = x[np.logical_not(np.isnan(x))] 
y = y[np.logical_not(np.isnan(y))] 


# Plot COP

# plt.plot(x, y, 'ro', markersize=3)
# plt.xlabel('x (mm)', fontsize=13)
# plt.ylabel('y (mm)', fontsize=13)
# plt.gca().set_aspect('equal', adjustable='box')
# #plt.savefig("COP",dpi=300)
# plt.show()


# Plot 2D Histogram

# plt.hist2d(x,y,15)
# plt.xlabel('x (mm)', fontsize=13)
# plt.ylabel('y (mm)', fontsize=13)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.colorbar()
# #plt.savefig("COP-heat",dpi=300)


# Histogram
bin_val = 12
arr, bx ,by = np.histogram2d(x,y,bins=bin_val)

coord_val = [(i,j,arr[i,j]) for i,j in product(range(len(arr)),range(len(arr[0])))]
# i, j = bin index of bin array
# arr[i,j] is hist value at that index
# i is x, j is y (above hist rotated 90 clockwise to array below)
# product: gives every possible index of the input array (instead of for x in range, for y in range)
# (i, j, hist value)

coord_val_sorted = sorted(coord_val, key = lambda x:x[2], reverse=True)
# find the largest bins
# sort it by the 3rd element x[2]
# reverse=True gives largest to smallest
# pack it into tuple to help keep track of relevant indicies alongside their value

cut_off_val =30
significant_coord = list(filter(lambda x: x[2]>=cut_off_val, coord_val_sorted))
# filter keeps items that return True on input condition
# filter takes two args (cond, data)
# x[2] is histogram frequency
# This finds the coordinates of bins which have highest frequencies
 
# print(significant_coord)    
# print(bx)
# print(by)
# bx, by are x, y bin start and end values



# Dimensions of Force Plate
height = 342
width = 180

# bin_val = number of bins
bin_height = height/bin_val #j
bin_width = width/bin_val #i


def index_to_pos(entry):
    # turns index -> position and do nothing on actual value
    # not actually used
    i,j,val = entry
    return (j*bin_height+bin_height/2), (i*bin_width+bin_width/2), val
    
significant_pos =  list(map(index_to_pos, significant_coord))
# map takes in a function and its possible arguments then retuns a list with the outputs



def gen_bound(i,j):
    # for a given coordinate here are where the bins start and stop (real world positions not indicies)
    low_x= bx[i]
    high_x = bx[i+1]
    low_y = by[j]
    high_y = by[j+1]
    return low_x,low_y,high_x,high_y


x_y = list(zip(x,y,t))
# eg x_y[0] = (x[0],y[0],t[0])


steps =[]

for i, j, number in significant_coord:
    # for each coordinate and their associated value
    
    lx, ly, hx, hy = gen_bound(i,j) # physical pos in coord

    x_y_selected = list(filter(lambda xy : (lx<=xy[0]<=hx)and (ly<=xy[1]<=hy),x_y))
    # look at all orginal data and find the data points that fall within the physical 'box' as found by significant coord

    num_points = len(x_y_selected)
    # how many fall within above box
    
    pos_totals = list(reduce(lambda val1,val2: (val1[0]+val2[0],val1[1]+val2[1],val1[2]+val2[2]), x_y_selected))
    # recursively adds all x's, y's and t's for average to be taken
    # (sum(x),sum(y),sum(t))
    x_ave = pos_totals[0]/num_points
    y_ave = pos_totals[1]/num_points
    t_ave = pos_totals[2]/num_points
    
    steps.append((x_ave,y_ave,t_ave))
    

# Plot steps
fig = plt.gcf()
fig.clf()
ax = plt.subplot(111)

feet_img = read_png("feet.PNG")

imagebox = OffsetImage(feet_img,zoom=.015)

for step in steps:
    x,y,t=step
    ab = AnnotationBbox(imagebox,step[:2],xybox=(-2., 4.),xycoords='data',boxcoords="offset points") 
    ax.add_artist(ab)
    ax.annotate(f"( ({x:.1f},{y:.1f}); time: {t:.2f}s", xy = step[:2], xytext =(step[0]+10,step[1]))

plt.xlim([-10,180])
plt.ylim([-50, 380])
plt.xlabel('x (mm)', fontsize=13)
plt.ylabel('y (mm)', fontsize=13)
plt.gca().set_aspect('equal', adjustable='box')
plt.draw()
#plt.savefig("Steps",dpi=300)
plt.show()


# #Sort by time
# steps = sorted(steps, key = lambda x:x[2], reverse=False)
# speed = (len(steps)-1)*60/(steps[-1][2]-steps[0][2]) # [steps/min]


