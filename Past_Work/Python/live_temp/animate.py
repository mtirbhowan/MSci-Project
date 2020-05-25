from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style('fivethirtyeight')

t_vals = []
y_vals =[]

index = count()

def animate(i):
    data = pd.read.csv('data.csv')
    x = data['t']
    y1 = data['LC1']
    y2 = data['LC2']
    y3 = data['LC3']
    y4 = data['LC4']
    
    plt.cla()
    
    plt.plot(x, y1, label='LC1')
    plt.plot(x, y2, label='LC2')
    plt.plot(x, y3, label='LC3')
    plt.plot(x, y4, label='LC4')
    
    plt.legend(loc='upper left')
    plt.tight_layout()
    
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)

plt.tight_layout()
plt.show()


