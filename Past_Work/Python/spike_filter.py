""" Need to find consecutive spikes and smooth over in between range of this.
    If solo spike then just replace by average of neighbours."""
    
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
import more_itertools as mit
from scipy import interpolate

def spike_filter(df, col, filter_param1=-400000, filter_param2=-40000, data_array = False):

    print('Using Spike Filter with p_1 = {}, p_2 = {}'.format(filter_param1, filter_param2))
    
    if data_array == True:
        
        d = {'0':df}
        
        df = pd.DataFrame(data=d)
       
        col ='0'
    
    # data from single column
    
        y = df[col]

    elif data_array == False:
        
        y = df[col]
        
    # replace FALSEs with NaNs
    
    print(len(y))
    
    y = y.replace(to_replace='False', value=np.nan).map(float)
    
    # calculate 'gradients'
    delta_y = np.asarray([y.iloc[i+1]-y.iloc[i] for i in range(len(y)-1)])
    
    # find outlier where gradient change is too high (1st spikes)
    spikes = np.where(delta_y < filter_param1)[0]
    
    # find NaNs
    NaNs = np.where(np.isnan(y))[0]
    
    # combine and remove any duplicates (just in case!)
    anomalies = np.sort(np.unique(np.concatenate((spikes, NaNs))))
    
    # replace these with NaNs in original data
    for positions in anomalies:
        y[positions] = np.nan
    
    # take derivatives from the other end to avoid doing maths with NaNs
    delta_y2 = np.asarray([y[i]-y[i+1] for i in range(len(y)-1)])
    
    # find the 2nd spikes
    spikes2 = np.where(delta_y2 < filter_param2)[0]
    
    # replace these with NaNs
    for positions in spikes2:
        y[positions] = np.nan
        
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
            f = interpolate.interp1d(x_temp, y_temp, kind='cubic')
            
            # Calculate NaN replacements by feeding in their x values
            interpolated_y = list(f(find_NaNs))   # use interpolation function returned by `interp1d`

            # Finally, replace NaN values with interpolated values            
            y[lower_index:upper_index+1] = interpolated_y 
            
    return y

if __name__ == '__main__':

    LC1 = read_csv('LC1.csv')
    y = spike_filter(LC1, '0')

    plt.plot(y)
    plt.show()

#''' open files '''
#LC1 = read_csv('LC1.csv')
#LC2 = read_csv('LC2.csv')
#LC3 = read_csv('LC3.csv')
#LC4 = read_csv('LC4.csv')
#
#''' data from single column '''
#col_data = LC3['72.65']   
##col_data = LC['72.65']
#
#
#''' replace FALSE s with NaN s (for NaNs)'''
#z_before = col_data.replace(to_replace='FALSE', value=np.nan).map(float)
#
#''' calculate 'gradient' change '''
## ignore the RuntimeWarning when ecountering NaN values
#z = abs(deepcopy(z_before))
#z_der = np.asarray([z.iloc[i+1]-z.iloc[i] for i in range(len(z)-1)])
#
#''' find outliers where gradient change is too high (spike) '''
## mostly works but fails to ID double spike(!)
## looks at large -ve gradient signifying a spike since all values have had
## their values modulied
#spikes_and_more = np.where(z_der < -1000)[0]     
#
#''' find NaNs '''
#NaNs = np.where(np.isnan(z))[0]
#
#''' combine and remove any dumplicates '''
#anomalies = np.sort(np.unique(np.concatenate((spikes_and_more, NaNs))))
#
#
#''' replace with NaN s'''        
#for positions in anomalies:
#    z[positions] = np.nan
#    
#''' start taking derivatives from other end to manouveur around 
#    doing maths with NaNs (removes spikes after NaNs/spikes'''
#x = deepcopy(z) # copy made for checking, can remove
#z_der2 = np.asarray([x[i]-x[i+1] for i in range(len(x)-1)])
#
#''' find 2nd spikes '''
#spikes2 = np.where(z_der2 < -10000)[0] # change param and look how anom size changes
#
#''' replace with NaN s'''
#for places in spikes2:
#    x[places] = np.nan
#
#''' combine all anomalies '''
#all_anomalies = np.sort(np.concatenate((anomalies,spikes2)))
#
#''' group up indexes of consecutive anomalies '''
#grouped = [list(group) for group in mit.consecutive_groups(all_anomalies)]
#    
#''' do stuff in anomaly indicies depending if they are grouped
#    or not '''
#y = deepcopy(x)
#for sections in grouped:
##    lower_index = sections[0]
##    upper_index = sections[-1]
##    print(x[lower_index - 1], x[upper_index + 1])
#    if len(sections) == 1:
#        index = sections[0]
#        ''' Replace with average of neighbours '''
#        y[index] = 0.5*(y[index+1]+y[index-1])
#
#    else:
#        lower_index = sections[0]
#        upper_index = sections[-1]
#
#        y_temp = np.array(y[lower_index-3: upper_index+2]) # take slice of data for y vals, need to check how interp1d deals with NaNs  
#        print(y_temp)
#        print( '\n')
#        x_temp = np.arange(0,len(y_temp))
#
#        
#        """ Find NaNs in y_temp (must be a quicker way 
#            bc they have already been found) """
#        find_NaNs = np.argwhere(np.isnan(y_temp))
#        
#        """  # Get rid of array of arrays """
#        find_NaNs = np.concatenate(find_NaNs, axis=0)
#        
#        """ Delete NaN rows for x and y """
#        x_temp = np.delete(x_temp,find_NaNs)
#        
#        """ Convert y to list now makes it easier to insert interpolated values back
#         later > y[insert_pos:insert_pos] = interpolated_y """
#        y_temp = list(np.delete(y_temp,find_NaNs))
#        
#        """ Interpolate stats """
#        f = interpolate.interp1d(x_temp, y_temp, kind='cubic')
#        
#        """ Calculate NaN replacements """
#        interpolated_y = list(f(find_NaNs))   # use interpolation function returned by `interp1d`
##        print(len(interpolated_y))
#        
##        print(interpolated_y)
#        
#        """ Finally replace NaN values"""
#        insert_pos = min(find_NaNs)
#        
#        y[lower_index:upper_index+1] = interpolated_y 
#        
#        print(find_NaNs)
        
        
     


          