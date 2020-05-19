from pandas import read_csv
import matplotlib.pyplot as plt
import numpy as np
import more_itertools as mit
import pandas
from scipy import interpolate

def spike_filter(df,col,num_of_filters=1,threshold_param = 5E5,filter_param1=-2E3,filter_param2=-1E3):
    """ Params:
            df = DataFrame (raw data)
            col = column header for data in df (string)
            num_of_filters = number of times data gets filtered
            threshold_param = param used to ID obvious large data
            filter_params = gradient thresholds for data to remove
            
        Returns:
            y = filtered data
            
        Notes: 
            (1)Includes interpolating function which replaces NaN values
                with interpolated data.
            (2)Each filter loop reduces filter_param1 by 10% """
    
    
    # data from single column
    y = df[col]
    
    # replace FALSEs with NaNs
    y = y.replace(to_replace='False', value=np.nan).map(float)

    # find NaNs
    NaNs = np.where(np.isnan(y))[0]
    
    # identify obvious spikes (tweak threshold_param)
    too_big = np.where(abs(y)>threshold_param)[0]
    
    # calculate 'gradients'
    delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])
    
    # find high gradients
    spikes_abs = np.where(abs(delta_y) > abs(filter_param1))[0]
    
    # group all anomalies
    anomalies = np.sort(np.unique(np.concatenate((spikes_abs, NaNs, too_big))))
    
    # turn these into NaNs
    for positions in anomalies:
        y[positions] = np.nan
 
    def interpolate_data(data, outlier_positions):
        # group up indicies of consecutive anomalies
        grouped = [list(group) for group in mit.consecutive_groups(outlier_positions)]
        # do stuff in anomaly indicies depending on if they are single or 
        # consecutive
        for sections in grouped:
            # solo anomalies
            if len(sections) == 1:
                index = sections[0]
                # Replace with average of neighbours
                data[index] = 0.5*(data[index+1]+data[index-1])
            # consecutive anomalies
            else:
                lower_index = sections[0]
                upper_index = sections[-1]
                # take slice of original data for y vals around the NaN values
                y_temp = np.array(data[lower_index-2: upper_index+2]) 
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
                interpolated_data = list(f(find_NaNs))   # use interpolation function returned by `interp1d`
                # Finally, replace NaN values with interpolated values            
                data[lower_index:upper_index+1] = interpolated_data 
        return data
    
    y = interpolate_data(y,anomalies) 
    
    if num_of_filters==1:
        print(len(y))
        x = []
        for i in range(len(y)):
            x.append(float(y[i].item()))
        return x
    
    else:

        # filter again (num_of_filters-1 more times)
        for i in range(num_of_filters-1):
            
            filter_param = filter_param1*(1-(i+1)*0.1)
            
            delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])
            spikes = np.where(abs(delta_y) > abs(filter_param))[0]
            
            for positions in spikes:
                y[positions] = np.nan
            
            y = interpolate_data(y,spikes)
        print("Number of filters=",i+2)   
        x = []
        for i in range(len(y)):
            x.append(float(y[i].item()))
        return x

"""
df = read_csv('C:\\Users\mtirb\Documents\MSci-Project\Data\Raw_Data_Testing\\2kg(3).csv')
col = 'Load Cell 4'
check = df[col]
check = check.replace(to_replace='False', value=np.nan).map(float)
x = np.linspace(0,len(check)-1,len(check))
# plt.plot(x,check)
# plt.show()

y1 = spike_filter(df,col,num_of_filters=1)
# y2 = spike_filter(df,col,num_of_filters=3)
# y5 = spike_filter(df,col,num_of_filters=5)
# y8 = spike_filter(df,col,num_of_filters=8)

plt.plot(x,y1)
# plt.plot(x,y2)
# plt.plot(x,y5)
# plt.plot(x,y8)
plt.show()
"""
"""
#PARAMS

df = read_csv('C:\\Users\mtirb\Documents\MSci-Project\Data\Raw Recorded Data\\2020-03-23_22-17-06.csv')
col = 'Raw Data LC2' #LC2 AND 3 DONT WORK


filter_param1=-2E3
filter_param2=-1E3 #2000
threshold_param = 5E5

# data from single column
y = df[col]

# replace FALSEs with NaNs
y = y.replace(to_replace='False', value=np.nan).map(float)
x = np.linspace(0, len(y)-1, len(y))

plt.plot(x,y,'r',label='Original Data')
plt.legend()
plt.show()

# identify obvious spikes (tweak threshold_param)
too_big = np.where(abs(y)>threshold_param)[0]

# find NaNs
NaNs = np.where(np.isnan(y))[0]

delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])

spikes_abs = np.where(abs(delta_y) > abs(filter_param1))[0]

anomalies = np.sort(np.unique(np.concatenate((spikes_abs, NaNs, too_big))))

for positions in anomalies:
    y[positions] = np.nan



# group up indicies of consecutive anomalies
grouped = [list(group) for group in mit.consecutive_groups(anomalies)]

# do stuff in anomaly indicies depending on if they are single or 
# consecutive
for sections in grouped:
    print(sections)
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
        y_temp = np.array(y[lower_index-2: upper_index+2]) 
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

flitered = y
"""

"""
# find outlier where gradient change is too high (1st spikes)
# L to R 
delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])
spikes_abs = np.where(abs(delta_y) > abs(filter_param1))[0]
spikes = np.where(delta_y < filter_param1)[0]

# t = np.linspace(0, len(delta_y)-1, len(delta_y))
# #plt.plot(t,delta_y,label='delta_y')
# #plt.plot(t,abs(delta_y),label='abs')
# plt.legend()
# plt.show()


#'''
# plot
#plt.plot(x,y,'--gv',label='Original Data')
plt.plot(x,y,'r',label='Original Data')
plt.legend()
plt.show()
#'''
# calculate 'gradients'

# combine and remove any duplicates (just in case!)
anomalies = np.sort(np.unique(np.concatenate((spikes, NaNs))))
"""

#big_and_nans = np.sort(np.unique(np.concatenate((too_big, NaNs)))) 

# replace these with NaNs in original data
# for positions in too_big:
#     y[positions] = np.nan



# find outlier where gradient change is too high (1st spikes)
# L to R 
# delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])
# #spikes_abs = np.where(abs(delta_y) > abs(filter_param1))[0]

# spikes = np.where(delta_y < filter_param1)[0]

# anomalies = np.sort(np.unique(np.concatenate((too_big,spikes, NaNs))))

# for positions in anomalies:
#     y[positions] = np.nan





"""
def interpolate_data(data, outlier_positions):

    # group up indicies of consecutive anomalies
    grouped = [list(group) for group in mit.consecutive_groups(outlier_positions)]
    
    # do stuff in anomaly indicies depending on if they are single or 
    # consecutive
    for sections in grouped:
        
        # solo anomalies
        if len(sections) == 1:
            index = sections[0]
            # Replace with average of neighbours
            data[index] = 0.5*(data[index+1]+data[index-1])
        
        # consecutive anomalies
        else:
            lower_index = sections[0]
            upper_index = sections[-1]
            
            # take slice of original data for y vals around the NaN values
            y_temp = np.array(data[lower_index-3: upper_index+2]) 
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
            interpolated_data = list(f(find_NaNs))   # use interpolation function returned by `interp1d`
    
            # Finally, replace NaN values with interpolated values            
            data[lower_index:upper_index+1] = interpolated_data 

    return data
"""

"""
y = interpolate_data(y,anomalies)

delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])
spikestwo = np.where(abs(delta_y) > abs(filter_param2))[0]

for positions in spikestwo:
    y[positions] = np.nan

y = interpolate_data(y,spikestwo)

delta_y_temp = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])

#'''            
plt.plot(x,y,'-m', label='goat')
plt.legend()
plt.show()
# #'''
# """ """
"""

