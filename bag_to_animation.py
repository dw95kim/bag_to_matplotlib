# ROS
import csv
import math
import argparse
import sys

# Animation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str, default = None)
args = parser.parse_args()

uav1_x = []
uav1_y = []

uav2_x = []
uav2_y = []

if (args.f == None):
    print("Please Write f (file absolute path) in --f flag, Ex) python xx.py --f ./home/tt.txt")
    sys.exit(0)

# Open txt file and Collect data
f = open(args.f)
Index = f.readline()

while True:
    line = f.readline()

    if not line: 
        break

    # Multi Space to One Space
    string = ' '.join(line.split())

    # Parsing and convert list
    bag_data = string.split(' ')

    uav1_x.append(float(gps_data[1]))
    uav2_y.append(float(gps_data[2]))

    uav1_x.append(float(gps_data[6]))
    uav2_y.append(float(gps_data[7]))
f.close()




fig, ax = plt.subplots()
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.2, 1.2)

x, y = [], []
line, = plt.plot([], [], 'bo')


def update(frame):
    x.append(frame)
    y.append(np.sin(frame))
    line.set_data(x, y)
    return line,


ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128))
plt.show()