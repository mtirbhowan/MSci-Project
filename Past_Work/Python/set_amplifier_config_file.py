import json

amplifier_configuration = {'A_1_DAT':'N/A','A_1_CLK':'N/A','A_2_DAT':'20','A_2_CLK':'21','A_3_DAT':'5','A_3_CLK':'6','A_4_DAT':'N/A','A_4_CLK':'N/A'}

with open('/home/pi/Documents/Python/Amplifier_configuration.json','w') as file:
    json.dump(amplifier_configuration, file)
    
amplifier_config_values = json.load(open('/home/pi/Documents/Python/Amplifier_configuration.json'))

print(amplifier_config_values["A_2_DAT"])