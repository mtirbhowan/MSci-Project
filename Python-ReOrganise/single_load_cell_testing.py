import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

def take_measurement_with_weight(print_vals=True):
    
    raw_data     = []
    
    added_weight = input('Input added weight in grams: ')
    for i in range(1000):
        raw_data.append(hx._read())
#     
#     if print_vals == True:
#         print('Added Weight = {:f}'.format(added_weight))
#         print('Raw value = {:f}'.format(raw_data))
    
    return added_weight, raw_data

def take_run(number_of_weights):
    
    weights   = []
    raw_datas = []
    
    for i in range(number_of_weights):
        
        weight, raw_data = take_measurement_with_weight()
        
        weights.append(weight)
        raw_datas.append(raw_data)
    
    return weights, raw_datas
    
def save_raw_to_csv(number_of_weights,file_name,plot=False):
    
    weights, raw_datas = take_run(number_of_weights)
    
    despiked_datas     = filter_spikes_with_median_filter( raw_datas )
    
    d  = {}
    df = pd.DataFrame(data=d)
    
    for i in range(number_of_weights):
        
        datastep = {'{:s} g'.format(str(weights[i])):raw_datas[i]}
        dataframestep = pd.DataFrame(data = datastep)
        
        df            = pd.concat((df, dataframestep),axis=1)
    
    df.to_csv('/home/pi/Documents/Load cell Testing/Single/{:s}.csv'.format(file_name))
    
    if plot == True:
        
        for i in range(number_of_weights):
            
            plt.plot(raw_datas[i], label='{:s} Unfiltered'.format(str(weights[i])),color = 'blue')
            plt.plot(raw_datas[i], label='{:s} Despiked'.format(str(weights[i])), color = 'red' )
                    
        plt.legend()
        plt.grid()
        
        plt.show()
        

def filter_spikes_with_median_filter(raw_datas, set_kernel = 5):
    
    filtered_datas = []
    
    for i in range(len(raw_datas)):
    
        filtered_datas.append(sig.medfilt(raw_datas[i], kernel_size = set_kernel))
        
    return filtered_datas
    
    



# def take_calibration(print_vals=True):
#     
#         
#     known_weight = input('Input known weight in grams: ')
#     
#     zero_raw = []
#     
#     for i in range(1000):
#         
#         zero_raw.append(hx._read())
#     mean_zero = np.mean(zero_raw)
# 
# 
# #     if print_vals == True:
# #         print('Added Weight = {:f}'.format(added_weight))
# #         print('Raw value = {:f}'.format(raw_data))
#     
#     return added_weight, raw_data
# 
# def take_run(number_of_weights):
#     
#     weights   = []
#     raw_datas = []
#     
#     for i in range(number_of_weights):
#         
#         weight, raw_data = take_measurement_with_weight()
#         
#         weights.append(weight)
#         raw_datas.append(raw_data)
#     
#     return weights, raw_datas
#     
# def save_calib_to_csv(number_of_weights,file_name):
#     
#     weights, calib_datas = take_run(number_of_weights)
#     
#     d  = {}
#     df = pd.DataFrame(data=d)
#     
#     for i in range(number_of_weights):
#         
#         datastep = {'{:s} g'.format(str(weights[i])):calib_datas[i]}
#         
#         dataframestep = pd.DataFrame(data = datastep)
#         df            = pd.concat((df, dataframestep),axis=1)
#     
#     df.to_csv('/home/pi/Documents/Load cell Testing/Single/{:s}'.format(file_name))
#     
# 



GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
# Create an object hx which represents your real hx711 chip
# Required input parameters are only 'dout_pin' and 'pd_sck_pin'
hx = HX711(dout_pin=5, pd_sck_pin=0)

# LC_1 = HX711(dout_pin=21, pd_sck_pin=20)
# LC_2 = HX711(dout_pin=5, pd_sck_pin=0)
# LC_3 = HX711(dout_pin=13, pd_sck_pin=6)
# LC_4 = HX711(dout_pin=26 , pd_sck_pin=19 )

file_name      = input('File name to save: ')
number_of_runs = int(input('Input number of weights: '))

save_raw_to_csv(number_of_runs, file_name, plot=True )
