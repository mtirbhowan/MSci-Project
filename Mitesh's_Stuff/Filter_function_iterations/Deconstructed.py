from pandas import read_csv
import matplotlib.pyplot as plt
import numpy as np
import more_itertools as mit
from scipy import interpolate

#PARAMS
df = read_csv('2kg(2).csv')

col = 'Load Cell 1'

filter_param1=-3500

filter_param2=-3500 #2000

    # data from single column
y = df[col]


# replace FALSEs with NaNs
y = y.replace(to_replace='False', value=np.nan).map(float)

x = np.linspace(0, len(y)-1, len(y))

# find NaNs
NaNs = np.where(np.isnan(y))[0]

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

# replace these with NaNs in original data
for positions in anomalies:
    y[positions] = np.nan

# find the 2nd spikes
delta_y2 = np.asarray([y[i]-y[i+1] for i in range(len(y)-1)])
spikes2 = (np.where(delta_y2 < filter_param2)[0])
#spikes2 = (np.where(abs(delta_y2) > abs(filter_param2))[0])

# plot
#
'''
x = np.linspace(0, len(y)-1, len(y))
plt.plot(x,y,color='g',label='removed')
plt.legend()
plt.show()
#'''

# take derivatives from the other end to avoid doing maths with NaNs

# plt.plot(x,y,'-ro',label='data')
# plt.show()
# replace these with NaNs
for positions in spikes2:
    y[positions] = np.nan

# plt.plot(x,y,'b',label='Anoms removed')
# plt.show()
    
#plot
x = np.linspace(0, len(y)-1, len(y))
plt.plot(x,y,'-go',label='Survivor')
plt.legend()
plt.show()

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
plt.plot(x,y,'--b', label='First filter')
plt.legend()
plt.show()
# #'''
# """ """