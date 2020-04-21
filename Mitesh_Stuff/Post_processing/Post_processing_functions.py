from pandas import read_csv
from Spike_filter import spike_filter
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps
from scipy.signal import find_peaks
import os

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

def filter_values(raw_data):
    """ Takes in raw data and performs spike filtering on each of the LC data.
    
        Then returns list of these numpy arrays in filtered_vals.
        
        Eg. filtered_vals[i] = LC(i+1)_filtered data """
    LC1_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC1',num_of_filters=2))
    LC2_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC2',num_of_filters=2))
    LC3_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC3',num_of_filters=2))
    LC4_filtered = np.asarray(spike_filter(raw_data, 'Raw Data LC4',num_of_filters=2))
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

def integrate_simps(total_forces, x, a, b):
    """ total_forces: f(t)
        a: lower integration bound (start of gait cycle)
        b: upper integration bound (end of gait cycle)
        """
    integrand = total_forces[a:b+1]
    area = simps(y=integrand, x=x)
    
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

def plot_all(calibrated_forces):
    
    total_forces, left_forces, right_forces, back_forces, front_forces = group_forces(calibrated_forces)
    x = np.linspace(0, len(total_forces)-1, len(total_forces))
    
    fig, axs = plt.subplots(5)
    axs[0].plot(x,total_forces,'tab:orange', label='Total Forces')
    #axs[0].set_title('Total Forces')
    axs[0].legend()
    axs[1].plot(x,left_forces,'tab:green', label='Left LCs')
    #axs[1].set_title('Left LCs')
    axs[1].legend()
    axs[2].plot(x,right_forces, 'tab:green', label='Right LCs')
    #axs[2].set_title('Right LCs')
    axs[2].legend()
    axs[3].plot(x,back_forces, 'tab:red', label='Back LCs')
    #axs[3].set_title('Back LCs')
    axs[3].legend()
    axs[4].plot(x,front_forces, 'tab:red', label='Front LCs')
    #axs[4].set_title('Front LCs')
    axs[4].legend()
    fig.text(0.5, 0.06, 'Not time (s)', ha='center')
    fig.text(0.08, 0.5, 'Force (N)', va='center', rotation='vertical')

    return

def calibrate_timings(raw_file):
    """ Takes in raw_file dataframe """
    
    # Determine the average times that each measurement is taken at 
    # (using the post time for each load cell then avg the sum)
    
    raw_file['Average Timing'] = 0.25*(raw_file['Post Times LC1'] + 
                                       raw_file['Post Times LC2'] +
                                       raw_file['Post Times LC3'] + 
                                       raw_file['Post Times LC4'])
    # Make it start from t = 0 s
    raw_file['Time_(s)'] = (raw_file['Average Timing'] - 
                            raw_file['Average Timing'][0]) 
    
    return raw_file['Time_(s)']
