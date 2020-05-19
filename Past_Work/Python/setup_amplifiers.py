import RPi.GPIO as GPIO
import pandas
import json
from hx711 import HX711

config_file = '/home/pi/Documents/Python/Amplifier_configuration.json'


def setup_amplifiers_and_GPIO(use_default_values=True):
    
    try:
        GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
        
        # Set up pin numbers for amplifiers from config file
        
        with open('/home/pi/Documents/Python/Amplifier_configuration.json','r') as calibration_file:
            
            calib_data = json.load(calibration_file)
            
            print(type(calib_data["A_2_DAT"]))
            
            if type(calib_data["A_1_DAT"]) == int:
            
                amplifier_1 = HX711(dout_pin = calib_data["A_1_DAT"], pd_sck_pin=["A_1_CLK"])
                
            if type(calib_data["A_2_DAT"]) == int:
            
                amplifier_2 = HX711(dout_pin = calib_data["A_2_DAT"], pd_sck_pin=["A_2_CLK"])
    
            if type(calib_data["A_3_DAT"]) == int:
            
                amplifier_3 = HX711(dout_pin = calib_data["A_3_DAT"], pd_sck_pin=["A_3_CLK"])
    
            if type(calib_data["A_4_DAT"]) == int:
            
                amplifier_4 = HX711(dout_pin = calib_data["A_4_DAT"], pd_sck_pin=["A_4_CLK"])
    
    
            
        print(amplifier_2.get_current_gain())
            
    except (KeyboardInterrupt, SystemExit):
        print('Bye :)')

setup_amplifiers_and_GPIO()