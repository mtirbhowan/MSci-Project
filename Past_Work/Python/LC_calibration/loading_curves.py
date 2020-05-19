import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from scipy.stats import linregress
import re

LC1 = read_csv('LC1.csv')
LC2 = read_csv('LC2.csv')
LC3 = read_csv('LC3.csv')
LC4 = read_csv('LC4.csv')


def values(df, column):
               
    # data from single column
    col_data = df[column]    
    
    # replace FALSE s with NaN s then delete NaNs
    z = col_data.replace(to_replace='False', value=np.nan).dropna().map(float)
    
    # calculate 'gradient' change
    z_der = np.asarray([z.iloc[i+1]-z.iloc[i] for i in range(len(z)-1)])
    
    # find outliers where gradient change is too high (spike)
    outliers = np.where(abs(z_der) > 1000)        
    
    # new data from single columm without FALSES and spikes
    z_new = np.delete(np.asarray(z), outliers)
    
    # remove last 
    z_new = np.delete(z_new, -1)
    
    # calculate graph data
    mean = np.average(z_new)
    std = np.std(z_new)
    
    return column, z, z_new, mean, std


    
def plotting_data(LC):
    
    mass = []
    output = []
    std_dev= []
    
    for i in range(len(LC.columns)-1):
        
        column, z, z_new, mean, std = values(LC, LC.columns[i+1])
        
        column = re.findall(r"\d*\.\d*", column)
       
        if len(column) != 0:
            mass.append(float(column[0]))
        output.append(mean)
        std_dev.append(std)
    
    print(len(mass))
    print(len(output))
    
    return mass, output, std_dev

#x, y, std_dev = plotting_data(LC2)


#fig, axs = plt.subplots(3)
#fig.suptitle('LC2')
#axs[0].errorbar(mass, mean_output, yerr=std_dev, fmt='o',
#             ecolor='orangered', color='steelblue', capsize=2)
#axs[1].plot(z)
#axs[2].plot(z_new)


#print(linregress(list(map(float,x)), list(map(float, y))))
#print(linregress(list(map(float,x[5:])), list(map(float, y[5:]))))
#fig, axs = plt.subplots(2)
#fig.suptitle('LC2')
#axs[0].errorbar(x, y, yerr=std_dev, fmt='o',
#             ecolor='orangered', color='steelblue', capsize=2)
#axs[0].plot(114.14291370261368*np.linspace(0,5889.38,33) + 112752.45433255972, '-k')
#axs[1].errorbar(x[5:], y[5:], yerr=std_dev[5:], fmt='o',
#             ecolor='orangered', color='steelblue', capsize=2)
#axs[1].plot(114.14470649223804*np.linspace(471.56,5890,28) + 112745.17170897644, '-k')



"""LC1"""
x1, y1, std_dev1 = plotting_data(LC1)
slope1, intercept1, r_value1, p_value1, std_error1 = linregress(list(map(float,
                                                    x1)), list(map(float, y1)))
#
#
plt.errorbar(np.float_(x1), np.float_(y1), yerr=std_dev1, fmt='o',
             capsize=2, color='gold')
plt.plot(np.float_(x1), intercept1 + slope1*np.float_(x1), '--',
         color='gold', label='LC1: y={:.4}x + {:.4}'.format(slope1,intercept1))


"""LC2"""
x2, y2, std_dev2 = plotting_data(LC2)
slope2, intercept2, r_value2, p_value2, std_error2 = linregress(list(map(float,
                                                    x2)), list(map(float,y2)))
#
#
plt.errorbar(np.float_(x2), np.float_(y2), yerr=std_dev2, fmt='o',
             capsize=2, color='cornflowerblue')
plt.plot(np.float_(x2), intercept2 + slope2*np.float_(x2),
         color='cornflowerblue', linestyle='dashed' ,
         label='LC2: y={:.4}x + {:.4}'.format(slope2,intercept2))



"""LC3""" 
x3, y3, std_dev3 = plotting_data(LC3)
slope3, intercept3, r_value3, p_value3, std_error3 = linregress(list(map(float,
                                                    x3)), list(map(float, y3)))
#
#
plt.errorbar(np.float_(x3), np.float_(y3), yerr=std_dev3, fmt='o',
             capsize=2, color='yellowgreen')
plt.plot(np.float_(x3), intercept3 + slope3*np.float_(x3),'--', 
         color='yellowgreen',label='LC3: y={:.4}x + {:.4}'.format(slope3,intercept3))


"""LC4"""
x4, y4, std_dev4 = plotting_data(LC4)
slope4, intercept4, r_value4, p_value4, std_error4 = linregress(list(map(float,
                                                    x4)), list(map(float, y4)))
#
#
plt.errorbar(np.float_(x4), np.float_(y4), yerr=std_dev4, fmt='o',
             capsize=2, color='tomato')
plt.plot(np.float_(x4), intercept4 + slope4*np.float_(x4), '--',
         color='tomato',label='LC4: y={:.4}x + {:.4}'.format(slope4,intercept4))

plt.legend()
plt.show()    