import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import time
import matplotlib.pyplot as plt
import numpy as np
# import scipy.signal as sig


GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

# Create an object hx which represents your real hx711 chip
# Required input parameters are only 'dout_pin' and 'pd_sck_pin'

hx1 = HX711(dout_pin=21, pd_sck_pin=20)
hx2 = HX711(dout_pin=5, pd_sck_pin=0)
hx3 = HX711(dout_pin=13, pd_sck_pin=6)
hx4 = HX711(dout_pin=26 , pd_sck_pin=19 )

# measure tare and save the value as offset for current channel
# and gain selected. That means channel A and gain 128

hx1.set_debug_mode(flag=True)
hx2.set_debug_mode(flag=True)
hx3.set_debug_mode(flag=True)
hx4.set_debug_mode(flag=True)

recorded_raw1 = []
recorded_raw2 = []
recorded_raw3 = []
recorded_raw4 = []

start = time.time()

for i in range(1000):
    
    
    raw_data_test1 = hx1._read()

    raw_data_test2 = hx2._read()
    raw_data_test3 = hx3._read()
    raw_data_test4 = hx4._read()
    if raw_data_test1 >= 0 and type(raw_data_test1) == int :    
        recorded_raw1.append(raw_data_test1)
    
#     else:
#         recorded_raw1.append(np.Nan)
    recorded_raw2.append(raw_data_test2)
    recorded_raw3.append(raw_data_test3)
    recorded_raw4.append(raw_data_test4)
    
    #print(raw_data_test)

end      = time.time()

total    = end - start

# filtered = sig.medfilt(recorded_raw1,5)

# print(len(filtered))

print(1/(total/1000))

plt.plot(recorded_raw1,label='1')
plt.plot(recorded_raw2,label='2')
plt.plot(recorded_raw3,label='3')
plt.plot(recorded_raw4,label='4')

plt.grid()
plt.legend()
plt.show()
