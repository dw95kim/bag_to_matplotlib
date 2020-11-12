import csv
import math
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str, default = None)
args = parser.parse_args()

time_list = []

opv_lat_list = []
opv_lon_list = []

kla_lat_list = []
kla_lon_list = []

first_line = True

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
    gps_data = string.split(' ')

    if (first_line == True):
        start_time = float(gps_data[0])
    # (0) = Time
    # (1, 2, 3) = OPV(lat, lon, alt)
    # (6, 7, 8) = KLA(lat, lon, alt)
    time_list.append(float(gps_data[0]) - start_time)

    opv_lat_list.append(float(gps_data[1])/10000000)
    opv_lon_list.append(float(gps_data[2])/10000000)

    kla_lat_list.append(float(gps_data[6])/10000000)
    kla_lon_list.append(float(gps_data[7])/10000000)

    first_line = False
f.close()

# Plot Part
fig, ax = plt.subplots()
ax = plt.axis([36.5, 36.68, 126.2, 126.4])

# plt.scatter(opv_lat_list, opv_lon_list, c='b', alpha=0.5)
# plt.scatter(kla_lat_list, kla_lon_list, c='r', alpha=0.5)
# plt.show()

redDot, = plt.plot([0], [0], 'ro')  #KLA-100
blueDot, = plt.plot([0], [0], 'bo') #Ownship

def animate(i):
    if (opv_lat_list[i] != 0):
        redDot.set_data(opv_lat_list[i], opv_lon_list[i])
    
    if (kla_lat_list[i] != 0):
        blueDot.set_data(kla_lat_list[i], kla_lon_list[i])

    return redDot, blueDot, 

myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0, len(opv_lat_list)), \
                                      interval=10, blit=True, repeat=True)

plt.show()