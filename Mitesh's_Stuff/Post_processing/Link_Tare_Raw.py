import glob
import os


list_of_files = glob.glob('C:\\Users\mtirb\Documents\MSci-Project\Data\Tares\*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
tarefile = os.path.basename(latest_file)

def find_latest_tare(directory):
    import glob
    import os
   
    list_of_files = glob.glob('C:\\Users\mtirb\Documents\MSci-Project\Data\Tares\*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    tarefile = os.path.basename(latest_file)
    
    return tarefile

directory = 'directory'
tester = '\*'
join = directory + tester 