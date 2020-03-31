""" TARE READING """
from pandas import read_csv
from spike_filter import spike_filter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

tare_dir = 'C:\\Users\mtirb\Documents\MSci-Project\Data\Tares'

tare_file = 'TARE_2020-03-23_22-17-49.csv'

tare_path = (tare_dir + '/' + tare_file)

tares = read_csv(tare_path)


raw_data_dir = 'C:\\Users\mtirb\Documents\MSci-Project\Data\Raw Recorded Data'

raw_data_file = '2020-03-23_22-17-06.csv'

raw_data_path = (raw_data_dir + '/' + raw_data_file)

raw_data = read_csv(raw_data_path)

y = raw_data['Raw Data LC1']
y = y.replace(to_replace='False', value=np.nan).map(float)
y = y.map(float)

x = np.linspace(0, len(y)-1, len(y))


#test = filtered_data.iloc[:,1]
""" FILTER VALUES """
# need to change series to df to get column header
LC1_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC1',filter_param1=-2000, filter_param2=-2000).to_frame()
                ,'Raw Data LC1',filter_param1=-1000, filter_param2=-1000))

LC2_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC2',filter_param1=-2000, filter_param2=-2000).to_frame()
                ,'Raw Data LC2',filter_param1=-1000, filter_param2=-1000))

LC3_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC3',filter_param1=-2000, filter_param2=-2000).to_frame()
                ,'Raw Data LC3',filter_param1=-1000, filter_param2=-1000))

LC4_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC4', filter_param1=-2000, filter_param2=-2000).to_frame()
                ,'Raw Data LC4',filter_param1=-1000, filter_param2=-1000))

filtered_vals = [LC1_filtered, LC2_filtered, LC3_filtered, LC4_filtered]


load_cells_to_test = [1,2,3,4]

LC_1 = [  93022.3786, 112.6440*1000/9.807] #calibration coef for counts to Newtons
LC_2 = [ 112752.4543, 114.1429*1000/9.807]
LC_3 = [ -76321.8141, 113.9544*1000/9.807]
LC_4 = [ 230100.9711, 113.3840*1000/9.807]

LC_calibration_coef = [LC_1,LC_2,LC_3,LC_4] #sort to array

calibrated_force = [] # In Newtons
# Next run through number of load cells and calibrate counts to new array

for i in range(len(filtered_vals)):

    calibrated_force.append([])        
    
    for j in range(len(filtered_vals[i])):
        
        subtracted_data = (filtered_vals[i][j] - LC_calibration_coef[load_cells_to_test[i]-1][0] - float(tares['Tare Count Load Cell {}'.format(load_cells_to_test[i])]))
        
        force_gram = (subtracted_data / LC_calibration_coef[load_cells_to_test[i]-1][1]) 
    
        calibrated_force[i].append(force_gram)
        
plt.plot(x, calibrated_force[0])
plt.plot(x, calibrated_force[1])
plt.plot(x, calibrated_force[2])
plt.plot(x, calibrated_force[3])
plt.show()

"""
def calibrate_values(filtered_values, tare, load_cells_to_test ):
    
    LC_1 = [  93022.3786, 112.6440*1000/9.807] #calibration coef for counts to Newtons
    LC_2 = [ 112752.4543, 114.1429*1000/9.807]
    LC_3 = [ -76321.8141, 113.9544*1000/9.807]
    LC_4 = [ 230100.9711, 113.3840*1000/9.807]
    
    LC_calibration_coef = [LC_1,LC_2,LC_3,LC_4] #sort to array
    
    calibrated_force = [] # In Newtons
    # Next run through number of load cells and calibrate counts to new array
    
    for i in range(len(filtered_values)):
        
        calibrated_force.append([])        
        
        for j in range(len(filtered_values[i])):
            
            subtracted_data = (filtered_values[i][j] - LC_calibration_coef[load_cells_to_test[i]-1][0] - tare[0][load_cells_to_test[i]-1] )
            
            force_gram = (subtracted_data / LC_calibration_coef[load_cells_to_test[i]-1][1]) 
        
            calibrated_force[i].append(force_gram)
    
    return calibrated_force

#calibrated_forces = calibrate_values(raw_data, tares, [1,2,3,4])

def post_calibrating_values():
    return
"""    