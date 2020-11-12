import csv
import math
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt

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

    if(float(gps_data[1]) != 0):
        opv_lat_list.append(float(gps_data[1]))
        opv_lon_list.append(float(gps_data[2]))

    if(float(gps_data[7]) != 0):
        kla_lat_list.append(float(gps_data[7]))
        kla_lon_list.append(float(gps_data[8]))

    first_line = False
f.close()

# print(opv_lat_list)

# Plot Part
plt.plot(opv_lat_list, opv_lon_list)
plt.plot(kla_lat_list, kla_lon_list)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
plt.show()
