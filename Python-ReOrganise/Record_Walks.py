import Load_Cell_Data as LC
import Data_Collection as DC
import Data_Analysis as DA
import Data_Load_Save as LS

DC.continuous_measurement(med_filt=True, custom_title_for_session = True, custom_title_per_walk = True, carryout_CoP=True, plot_CoP = True)