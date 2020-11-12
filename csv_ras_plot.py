import csv
import math
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


parser = argparse.ArgumentParser()
parser.add_argument('--opv_f', type=str, default = None)
parser.add_argument('--kla_f', type=str, default = None)
args = parser.parse_args()

time_list = []

opv_lat_list = []
opv_lon_list = []
opv_alt_list = []

kla_lat_list = []
kla_lon_list = []
kla_alt_list = []

if (args.opv_f == None or args.kla_f == None):
    print("Please Write f (file absolute path) in --f flag, Ex) python xx.py --f ./home/tt.txt")
    sys.exit(0)

# Open txt file and Collect data
opv_f = open(args.opv_f)
kla_f = open(args.kla_f)

opv_Index = opv_f.readline()
kla_Index = kla_f.readline()

first_line = True
while True:
    opv_line = opv_f.readline()

    if not opv_line: 
        break

    # Multi Space to One Space
    string = ' '.join(opv_line.split())

    # Parsing and convert list
    gps_data = string.split(' ')

    if (first_line == True):
        start_time = float(gps_data[0])
    # (0) = Time
    # (1, 2, 3) = OPV(lat, lon, alt)
    # (6, 7, 8) = KLA(lat, lon, alt)
    if (float(gps_data[0]) > 1600331048.47):
        time_list.append(float(gps_data[0]) - start_time)
        opv_lat_list.append(float(gps_data[1]))
        opv_lon_list.append(float(gps_data[2]))
        opv_alt_list.append(float(gps_data[3]))

    first_line = False

first_line = True
while True:
    kla_line = kla_f.readline()

    if not kla_line: 
        break

    # Multi Space to One Space
    string = ' '.join(kla_line.split())

    # Parsing and convert list
    gps_data = string.split(' ')

    if (first_line == True):
        start_time = float(gps_data[0])
    # (0) = Time
    # (1, 2, 3) = OPV(lat, lon, alt)
    # (6, 7, 8) = KLA(lat, lon, alt)
    if (float(gps_data[0]) > 1600331048.47):
        time_list.append(float(gps_data[0]) - start_time)
        kla_lat_list.append(float(gps_data[1]))
        kla_lon_list.append(float(gps_data[2]))
        kla_alt_list.append(float(gps_data[3]))
    
    first_line = False
   
opv_f.close()
kla_f.close()

# Plot Part
fig = plt.figure()
ax = p3.Axes3D(fig)

# Setting the axes properties
ax.set_xlim3d([36.5, 36.68])
ax.set_xlabel('Lat')

ax.set_ylim3d([126.2, 126.4])
ax.set_ylabel('Lon')

ax.set_zlim3d([0.0, 1500.0])
ax.set_zlabel('Alt')

# plt.scatter(opv_lat_list, opv_lon_list, c='b', alpha=0.5)
# plt.scatter(kla_lat_list, kla_lon_list, c='r', alpha=0.5)
# plt.show()

redDot, = plt.plot([0], [0], [0], 'ro')  #KLA-100
blueDot, = plt.plot([0], [0], [0], 'bo') #Ownship

def animate(i):
    if (opv_lat_list[i] != 0 and opv_lat_list[i] > 36.5 and opv_lat_list[i] < 36.68):
        redDot.set_data(opv_lat_list[i], opv_lon_list[i])
        redDot.set_3d_properties(opv_alt_list[i])
    
    if (kla_lat_list[i] != 0 and kla_lat_list[i] > 36.5 and kla_lat_list[i] < 36.68):
        blueDot.set_data(kla_lat_list[i], kla_lon_list[i])
        blueDot.set_3d_properties(kla_alt_list[i])

    return redDot, blueDot, 

myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0, len(opv_lat_list)), \
                                      interval=1, blit=True, repeat=True)

plt.show()