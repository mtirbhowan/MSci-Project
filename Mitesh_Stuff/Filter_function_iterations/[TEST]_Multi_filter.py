from spike_filter import spike_filter
from pandas import read_csv
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import more_itertools as mit
from scipy import interpolate

#PARAMS
df = read_csv('2kg(static).csv')

col = 'Load Cell 2'

filter_param1=-200

filter_param2=-1000
    # data from single column
y = df[col]


# replace FALSEs with NaNs
y = y.replace(to_replace='False', value=np.nan).map(float)
#'''
# plot
x = np.linspace(0, len(y)-1, len(y))
plt.plot(x,y,'--gv',label='Original')
plt.legend()
plt.show()
#'''
# calculate 'gradients'
delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])
print(delta_y[840:860])

# find outlier where gradient change is too high (1st spikes)
spikes = np.where(delta_y < filter_param1)[0]

# find NaNs
NaNs = np.where(np.isnan(y))[0]

# combine and remove any duplicates (just in case!)
anomalies = np.sort(np.unique(np.concatenate((spikes, NaNs))))

# replace these with NaNs in original data
for positions in anomalies:
    y[positions] = np.nan

# plot
#
#'''
#x = np.linspace(0, len(y), len(y))
#plt.plot(x,y,color='r')
#plt.show()
#'''

# take derivatives from the other end to avoid doing maths with NaNs
delta_y2 = np.asarray([y[i]-y[i+1] for i in range(len(y)-1)])

# find the 2nd spikes
spikes2 = np.where(delta_y2 < filter_param2)[0]

# replace these with NaNs
for positions in spikes2:
    y[positions] = np.nan
    
# plot
#x = np.linspace(0, len(y), len(y))
#plt.plot(x,y,color='b')
#plt.show()

#'''    
# combine anomalies (all original spikes and Falses (if params right!))
all_anomalies = np.sort(np.concatenate((anomalies,spikes2)))

# group up indicies of consecutive anomalies
grouped = [list(group) for group in mit.consecutive_groups(all_anomalies)]

# do stuff in anomaly indicies depending on if they are single or 
# consecutive
for sections in grouped:
    
    # solo anomalies
    if len(sections) == 1:
        index = sections[0]
        # Replace with average of neighbours
        y[index] = 0.5*(y[index+1]+y[index-1])
    
    # consecutive anomalies
    else:
        lower_index = sections[0]
        upper_index = sections[-1]
        
        # take slice of original data for y vals around the NaN values
        y_temp = np.array(y[lower_index-3: upper_index+2]) 
        x_temp = np.arange(0,len(y_temp))

        
        # Find NaNs in y_temp (must be a quicker way 
        #    bc they have already been found)
        find_NaNs = np.argwhere(np.isnan(y_temp))
        
        # Get rid of array of arrays
        find_NaNs = np.concatenate(find_NaNs, axis=0)
        
        # Delete NaN rows for x and y 
        x_temp = np.delete(x_temp,find_NaNs)
        y_temp = np.delete(y_temp,find_NaNs)
        
        # Interpolate stats on slice of data
        f = interpolate.interp1d(x_temp, y_temp, kind='slinear')
        
        # Calculate NaN replacements by feeding in their x values
        interpolated_y = list(f(find_NaNs))   # use interpolation function returned by `interp1d`

        # Finally, replace NaN values with interpolated values            
        y[lower_index:upper_index+1] = interpolated_y 

#'''            
x=np.linspace(0, len(y), len(y))
plt.plot(x,y,'--bo', label='First filter')
plt.legend()
plt.show()
#'''

filter_param3=-400
filter_param4=-200
    # data from single column

# calculate 'gradients'
delta_y3 = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])

# find outlier where gradient change is too high (1st spikes)
spikes3 = np.where(delta_y3 < filter_param3)[0]

# find NaNs
NaNs3 = np.where(np.isnan(y))[0]

# combine and remove any duplicates (just in case!)
anomalies3 = np.sort(np.unique(np.concatenate((spikes3, NaNs3))))

# replace these with NaNs in original data
for positions3 in anomalies3:
    y[positions3] = np.nan

# plot
#x = np.linspace(0, len(y), len(y))
#plt.plot(x,y,color='r')
#plt.show()
#'''

# take derivatives from the other end to avoid doing maths with NaNs
delta_y4 = np.asarray([y[i]-y[i+1] for i in range(len(y)-1)])

# find the 2nd spikes
spikes4 = np.where(delta_y4 < filter_param4)[0]

# replace these with NaNs
for positions in spikes4:
    y[positions] = np.nan
    
## plot
#'''
#x = np.linspace(0, len(y), len(y))
#plt.plot(x,y,color='b')
#plt.show()
#'''    
# combine anomalies (all original spikes and Falses (if params right!))
all_anomalies3 = np.sort(np.concatenate((anomalies3,spikes4)))

# group up indicies of consecutive anomalies
grouped3 = [list(group) for group in mit.consecutive_groups(all_anomalies3)]

# do stuff in anomaly indicies depending on if they are single or 
# consecutive
for sections in grouped3:
    
    # solo anomalies
    if len(sections) == 1:
        index = sections[0]
        # Replace with average of neighbours
        y[index] = 0.5*(y[index+1]+y[index-1])
    
    # consecutive anomalies
    else:
        lower_index = sections[0]
        upper_index = sections[-1]
        
        # take slice of original data for y vals around the NaN values
        y_temp = np.array(y[lower_index-3: upper_index+2]) 
        x_temp = np.arange(0,len(y_temp))

        
        # Find NaNs in y_temp (must be a quicker way 
        #    bc they have already been found)
        find_NaNs = np.argwhere(np.isnan(y_temp))
        
        # Get rid of array of arrays
        find_NaNs = np.concatenate(find_NaNs, axis=0)
        
        # Delete NaN rows for x and y 
        x_temp = np.delete(x_temp,find_NaNs)
        y_temp = np.delete(y_temp,find_NaNs)
        
        # Interpolate stats on slice of data
        f = interpolate.interp1d(x_temp, y_temp, kind='slinear')
        
        # Calculate NaN replacements by feeding in their x values
        interpolated_y = list(f(find_NaNs))   # use interpolation function returned by `interp1d`

        # Finally, replace NaN values with interpolated values            
        y[lower_index:upper_index+1] = interpolated_y 
'''
x=np.linspace(0, len(y), len(y))
plt.plot(x,y, '-ro', label='Second filter')
plt.legend()
plt.show()
#'''
""" #TRIPLE FILTER
"""
# calculate 'gradients'
delta_y3 = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])

# find outlier where gradient change is too high (1st spikes)
spikes3 = np.where(delta_y3 < filter_param3)[0]

# find NaNs
NaNs3 = np.where(np.isnan(y))[0]

# combine and remove any duplicates (just in case!)
anomalies3 = np.sort(np.unique(np.concatenate((spikes3, NaNs3))))

# replace these with NaNs in original data
for positions3 in anomalies3:
    y[positions3] = np.nan

# plot
#x = np.linspace(0, len(y), len(y))
#plt.plot(x,y,color='r')
#plt.show()
#'''

# take derivatives from the other end to avoid doing maths with NaNs
delta_y4 = np.asarray([y[i]-y[i+1] for i in range(len(y)-1)])

# find the 2nd spikes
spikes4 = np.where(delta_y4 < filter_param4)[0]

# replace these with NaNs
for positions in spikes4:
    y[positions] = np.nan
    
## plot
#'''
#x = np.linspace(0, len(y), len(y))
#plt.plot(x,y,color='b')
#plt.show()
#'''    
# combine anomalies (all original spikes and Falses (if params right!))
all_anomalies3 = np.sort(np.concatenate((anomalies3,spikes4)))

# group up indicies of consecutive anomalies
grouped3 = [list(group) for group in mit.consecutive_groups(all_anomalies3)]

# do stuff in anomaly indicies depending on if they are single or 
# consecutive
for sections in grouped3:
    
    # solo anomalies
    if len(sections) == 1:
        index = sections[0]
        # Replace with average of neighbours
        y[index] = 0.5*(y[index+1]+y[index-1])
    
    # consecutive anomalies
    else:
        lower_index = sections[0]
        upper_index = sections[-1]
        
        # take slice of original data for y vals around the NaN values
        y_temp = np.array(y[lower_index-3: upper_index+2]) 
        x_temp = np.arange(0,len(y_temp))

        
        # Find NaNs in y_temp (must be a quicker way 
        #    bc they have already been found)
        find_NaNs = np.argwhere(np.isnan(y_temp))
        
        # Get rid of array of arrays
        find_NaNs = np.concatenate(find_NaNs, axis=0)
        
        # Delete NaN rows for x and y 
        x_temp = np.delete(x_temp,find_NaNs)
        y_temp = np.delete(y_temp,find_NaNs)
        
        # Interpolate stats on slice of data
        f = interpolate.interp1d(x_temp, y_temp, kind='slinear')
        
        # Calculate NaN replacements by feeding in their x values
        interpolated_y = list(f(find_NaNs))   # use interpolation function returned by `interp1d`

        # Finally, replace NaN values with interpolated values            
        y[lower_index:upper_index+1] = interpolated_y 

'''        
x=np.linspace(0, len(y), len(y))
plt.plot(x,y,'--ko', label='Third filter')
plt.legend()
plt.show()
#'''










"""

































#d = {[0]:LC}
#
#df = pd.DataFrame(data=d)
#   
#col ='0'
#
## data from single column
#
#y = df[col]
#
#t=np.linspace(0, len(LC), len(LC))
#plt.plot(t,LC,'--','red')
#plt.show()

#'''
#data = read_csv('2kg(1).csv')
#
#column = 'Load Cell 2
#
#'
#
#LC_data = data[column]
#
#LC_data = LC_data.replace(to_replace='False', value=np.nan).map(float)
#
#x = np.linspace(0, len(LC_data), len(LC_data))
#
## spike_filter(df, col, filter_param1=-1000, filter_param2=-10000)
#LC = spike_filter(data, column, filter_param1=-180000, filter_param2=-180000)
#LCY = spike_filter(data, column, filter_param1=-400, filter_param2=-5000)
#
#
##plt.plot(x, LC_data, 'r')
#plt.plot(x, LC_data, '--', color='black')
#plt.plot(x, LCY, '--', color='red')
#plt.show()
