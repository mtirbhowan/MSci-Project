import Load_Cell_Data as LC
import Data_Collection as DC
import Data_Analysis as DA
import Data_Load_Save as LS

folder_name = '25-04-2020/1.5Kg_5cm/'

walk_name = folder_name + '(2020-04-25)_18-13-55.csv'
tare_name = folder_name + '2020-04-25_18-13-42.csv'


raw_data, pre_times, post_times, filtered_values = LS.data_from_file(walk_name)

tare_data = LS.read_tare_from_file(tare_name)

print(len(raw_data))
print(tare_data)

#mid_times, measurement_lengths, time_between = calculate_times(pre_times, post_times, 
calibrated_values, calibrated_errors = LC.calibrate_values(filtered_values, tare_data, [1,2,3,4])

print(calibrated_values)

DA.calculate_CoP( calibrated_values, calibrated_errors, pre_times , plot_position_values = True, plot_position_over_time = True, save_CoP_data = False)
