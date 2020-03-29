import csv
import time
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711

GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

hx1 = HX711(dout_pin=21, pd_sck_pin=20)
hx2 = HX711(dout_pin=5, pd_sck_pin=0)
hx3 = HX711(dout_pin=13, pd_sck_pin=6)
hx4 = HX711(dout_pin=26 , pd_sck_pin=19 )

hx1.set_debug_mode(flag=True)
hx2.set_debug_mode(flag=True)
hx3.set_debug_mode(flag=True)
hx4.set_debug_mode(flag=True)

t = 0
LC1_raw = 0
LC2_raw = 0
LC3_raw = 0
LC4_raw = 0

fieldnames = ["t", "LC1", "LC2", "LC3", "LC4"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
while True:
    
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        info = {
                "t": t,
                "LC1": LC1_raw,
                "LC2": LC2_raw,
                "LC3": LC3_raw,
                "LC4": LC4_raw
                }
        csv_writer.writerow(info)
        print(t, LC1_raw, LC2_raw, LC3_raw, LC4_raw)
        
        t += 1
        LC1_raw = hx1._read()
        LC2_raw = hx2._read()
        LC3_raw = hx3._read()
        LC4_raw = hx4._read()
        
    time.sleep(1)
        
                
                