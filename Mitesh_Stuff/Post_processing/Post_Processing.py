""" This script will open a raw data file and its corresponding tare file.
    It will then combine these to output calibrated values.
    
    1) Open raw_data (YYYY-MM-DD_H-M-S.csv
    2) Open tare data(TARE_YYYY-MM-DD_H-M-S.csv
    *Note: H-M-S will be slightly different
    3) Filter values
    4) Calibrate using *slightly* modified calibration function"""
    
"""" NEED TO MAKE INTO FUNCTION AND TIDY UP"""
    
from pandas import read_csv
from Spike_filter import spike_filter
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps
from scipy.signal import find_peaks

def open_raw(raw_data_file,raw_data_dir='C:\\Users\mtirb\Documents\MSci-Project\Data\Raw Recorded Data'):
    """ Takes raw data filename (as string) and its directory as input(s)
        
        Returns: raw_data as a DataFrame """
    
    raw_data_path = (raw_data_dir + '/' + raw_data_file)
    raw_data = read_csv(raw_data_path)
    
    return raw_data

def open_tare(tare_file,tare_dir='C:\\Users\mtirb\Documents\MSci-Project\Data\Tares'):
    """ Takes tare data filename (as string) and its directory as input(s)
        
        Returns: tares as a DataFrame """
    tare_path = (tare_dir + '/' + tare_file)
    tares = read_csv(tare_path)
    
    return tares

def filtered_values(raw_data):
    """ Takes in raw data and performs spike filtering on each of the LC data.
    
        Then returns list of these numpy arrays in filtered_vals.
        
        Eg. filtered_vals[i] = LC(i+1)_filtered data """
    LC1_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 1',num_of_filters=2))
    LC2_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 2',num_of_filters=2))
    LC3_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 3',num_of_filters=2))
    LC4_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 4',num_of_filters=2))
    filtered_vals = [LC1_filtered,LC2_filtered,LC3_filtered,LC4_filtered]
    
    return filtered_vals

def post_calibrate_values(filtered_vals, tares):
    """ calibrates values post-processing """
    load_cells = [1,2,3,4]

    LC_1 = [  93022.3786, 112.6440*1000/9.807] #calibration coef for counts to Newtons
    LC_2 = [ 112752.4543, 114.1429*1000/9.807]
    LC_3 = [ -76321.8141, 113.9544*1000/9.807]
    LC_4 = [ 230100.9711, 113.3840*1000/9.807]
    
    LC_calibration_coef = [LC_1,LC_2,LC_3,LC_4] #sort to array
    
    calibrated_forces = [] # In Newtons
    # Next run through number of load cells and calibrate counts to new array
    
    for i in range(len(filtered_vals)):
    
        calibrated_forces.append([])        
        
        for j in range(len(filtered_vals[i])):
            
            subtracted_data = (filtered_vals[i][j] - LC_calibration_coef[load_cells[i]-1][0] - float(tares['Tare Count Load Cell {}'.format(load_cells[i])]))
            
            force_gram = (subtracted_data / LC_calibration_coef[load_cells[i]-1][1]) 
        
            calibrated_forces[i].append(force_gram)
    
    return calibrated_forces

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
        
        One cycle is from i-th peak, to i-th + 2 peak. Therefore, minimum
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

def integrate_simps(total_forces, a, b):
    """ total_forces: f(t)
        a: lower integration bound (start of gait cycle)
        b: upper integration bound (end of gait cycle)
        """
    integrand = total_forces[a:b+1]
    area = simps(integrand,dx=1)
    
    return area

def group_forces(calibrated_forces):
    
    """ Groups:
        LC1 and 2 for the forces on the back of the plate
        LC3 and 4 for the forces on the front of the plate
        LC1 and 4 for the forces on the left hand side of the plate
        LC2 and 3 for the forces on the right hand side of the plate. """
    
    back_forces = np.add(calibrated_forces[0],calibrated_forces[1])
    front_forces = np.add(calibrated_forces[2],calibrated_forces[3])
    left_forces = np.add(calibrated_forces[0],calibrated_forces[3])
    right_forces = np.add(calibrated_forces[1],calibrated_forces[2])
    total_forces = np.add(back_forces,front_forces)
    
    return total_forces, left_forces, right_forces, back_forces, front_forces

# Open files

date = '13-04-2020'
    
tare_dir = r'C:\\Users\mtirb\Documents\MSci-Project\Data\Tares'

tare_folder = '1Kg_Walks'

tare_file = tare_dir

"""
# Open files
tares = open_tare('TARE_2020-03-23_22-17-49.csv')
raw_data = open_raw('2020-03-23_22-17-06.csv')

# Filter (make function?)
LC1_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC1',num_of_filters=1))
LC2_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC2',num_of_filters=1))
LC3_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC3',num_of_filters=1))
LC4_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC4',num_of_filters=1))
filtered_vals = [LC1_filtered,LC2_filtered,LC3_filtered,LC4_filtered]

# Calbrate
calibrated_forces = post_calibrate_values(filtered_vals, tares)
x = np.linspace(0, len(calibrated_forces[0])-1, len(calibrated_forces[0]))

# Group together sets of relevant forces
left_forces = np.add(calibrated_forces[0],calibrated_forces[3])
right_forces = np.add(calibrated_forces[1],calibrated_forces[2])
back_forces = np.add(calibrated_forces[0],calibrated_forces[1])
front_forces = np.add(calibrated_forces[2],calibrated_forces[3])
total_forces = np.add(left_forces,right_forces)

# Plotting

fig, axs = plt.subplots(5)
axs[0].plot(x,total_forces,'tab:orange')
axs[0].set_title('Total Forces')
axs[1].plot(x,back_forces, 'tab:red')
axs[1].set_title('Back LCs')
axs[2].plot(x,front_forces, 'tab:red')
axs[2].set_title('Front LCs')
axs[3].plot(x,left_forces,'tab:green')
axs[3].set_title('Left LCs')
axs[4].plot(x,right_forces, 'tab:green')
axs[4].set_title('Right LCs')
"""

"""

raw_data = open_raw('2kg(1).csv', raw_data_dir='C:\\Users\mtirb\Documents\MSci-Project\Data\Raw_Data_Testing')
tares = open_tare('TARE_2020-03-23_22-17-49.csv')



# LC1_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 1',num_of_filters=2))
# LC2_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 2',num_of_filters=2))
# LC3_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 3',num_of_filters=2))
# LC4_filtered = np.asarray(spike_filter(raw_data, 'Load Cell 4',num_of_filters=2))
# filtered_vals = [LC1_filtered,LC2_filtered,LC3_filtered,LC4_filtered]

filtered_vals = filtered_values(raw_data)

calibrated_forces = post_calibrate_values(filtered_vals, tares)
x = np.linspace(0, len(calibrated_forces[0])-1, len(calibrated_forces[0]))


        

    
back_forces = np.add(calibrated_forces[0],calibrated_forces[1])
front_forces = np.add(calibrated_forces[2],calibrated_forces[3])
left_forces = np.add(calibrated_forces[0],calibrated_forces[3])
right_forces = np.add(calibrated_forces[1],calibrated_forces[2])
total_forces = np.add(back_forces,front_forces)

# plt.plot(x, total_forces)
# plt.plot(x, left_forces)
# plt.plot(x, right_forces)
# plt.plot(x, back_forces)
# plt.plot(x, front_forces)
# plt.show()


    

int_data = total_forces[293:457+1]
area = simps(int_data,dx=1)
mg = area/(len(int_data)-1)
m = mg/9.81
print("mass in kilograms is", m, " kg")





peaks, _ = find_peaks(total_forces, prominence=1)
plt.plot(peaks, total_forces[peaks], "xr"); plt.plot(total_forces, 'k')
plt.show()

"""
    




# from matplotlib.patches import Polygon
# a, b, c, d, e = 222, 293, 370, 457, 536
# plt.fill_between(x[a:b+1],total_forces[a:b+1],facecolor='lightpink')#,facecolor='crimson')
# plt.fill_between(x[b:c+1],total_forces[b:c+1],facecolor='lightpink')
# plt.fill_between(x[c:d+1],total_forces[c:d+1],facecolor='cornflowerblue')
# plt.fill_between(x[d:e+1],total_forces[d:e+1],facecolor='cornflowerblue')#,facecolor='hotpink')
# plt.show()

# raw_data_dir = 'C:\\Users\mtirb\Documents\MSci-Project\Data\Raw Recorded Data'
# raw_data_file = '2020-03-23_22-17-06.csv'
# raw_data_path = (raw_data_dir + '/' + raw_data_file)
# raw_data = read_csv(raw_data_path)


# tare_dir = 'C:\\Users\mtirb\Documents\MSci-Project\Data\Tares'
# tare_file = 'TARE_2020-03-23_22-17-49.csv'
# tare_path = (tare_dir + '/' + tare_file)
# tares = read_csv(tare_path)

# y = raw_data['Raw Data LC1']
# y = y.replace(to_replace='False', value=np.nan).map(float)
# y = y.map(float)

# x = np.linspace(0, len(y)-1, len(y))


# #test = filtered_data.iloc[:,1]
# """ FILTER VALUES """
# # need to change series to df to get column header
# LC1_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC1',filter_param1=-2000, filter_param2=-2000).to_frame()
#                 ,'Raw Data LC1',filter_param1=-1000, filter_param2=-1000))

# LC2_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC2',filter_param1=-2000, filter_param2=-2000).to_frame()
#                 ,'Raw Data LC2',filter_param1=-1000, filter_param2=-1000))

# LC3_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC3',filter_param1=-2000, filter_param2=-2000).to_frame()
#                 ,'Raw Data LC3',filter_param1=-1000, filter_param2=-1000))

# LC4_filtered = np.asarray(spike_filter(spike_filter(raw_data, 'Raw Data LC4', filter_param1=-2000, filter_param2=-2000).to_frame()
#                 ,'Raw Data LC4',filter_param1=-1000, filter_param2=-1000))

# filtered_vals = [LC1_filtered, LC2_filtered, LC3_filtered, LC4_filtered]


# load_cells_to_test = [1,2,3,4]

# LC_1 = [  93022.3786, 112.6440*1000/9.807] #calibration coef for counts to Newtons
# LC_2 = [ 112752.4543, 114.1429*1000/9.807]
# LC_3 = [ -76321.8141, 113.9544*1000/9.807]
# LC_4 = [ 230100.9711, 113.3840*1000/9.807]

# LC_calibration_coef = [LC_1,LC_2,LC_3,LC_4] #sort to array

# calibrated_force = [] # In Newtons
# # Next run through number of load cells and calibrate counts to new array

# for i in range(len(filtered_vals)):

#     calibrated_force.append([])        
    
#     for j in range(len(filtered_vals[i])):
        
#         subtracted_data = (filtered_vals[i][j] - LC_calibration_coef[load_cells_to_test[i]-1][0] - float(tares['Tare Count Load Cell {}'.format(load_cells_to_test[i])]))
        
#         force_gram = (subtracted_data / LC_calibration_coef[load_cells_to_test[i]-1][1]) 
    
#         calibrated_force[i].append(force_gram)
        
# # plt.plot(x, calibrated_force[0])
# # plt.plot(x, calibrated_force[1])
# # plt.plot(x, calibrated_force[2])
# # plt.plot(x, calibrated_force[3])
# # plt.xlabel('Time')
# # plt.ylabel('Force (N)')
# # plt.show()

# left_forces = np.add(calibrated_force[0],calibrated_force[3])
# right_forces = np.add(calibrated_force[1],calibrated_force[2])
# back_forces = np.add(calibrated_force[0],calibrated_force[1])
# front_forces = np.add(calibrated_force[2],calibrated_force[3])
# total_forces = np.add(left_forces,right_forces)
# #plt.plot(x,total_forces)
# # plt.plot(x,right_forces)
# # # plt.plot(x,left_forces)
# plt.plot(x,front_forces)
# plt.show()
