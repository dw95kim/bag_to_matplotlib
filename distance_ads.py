#######################################
# HOW TO USE IT
# python save.py \
# --opv_file '/media/usrg-asus/T7/Civil/2020-09-26-06_53_20/OPV_bag/200926_06_GPS_from_mavros_pos.txt' \
# --kla_file '/media/usrg-asus/T7/Civil/2020-09-26-06_53_20/KLA_ras_bag/200926_06_GPS_from_Rasberry.txt' \
# --save_file './200926_ras_distance.txt'
#######################################

import csv
import math
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--ads_file', type=str, default = None)
parser.add_argument('--save_file', type=str, default = None)
args = parser.parse_args()

##################################
# Define Parameter
WGS84_a_m = 6378137.0
WGS84_e = 0.08181919

d2r = math.pi / 180
r2d = 180 / math.pi

# Hanseo Univ
std_lat = 36.593133
std_lon = 126.295440
std_alt = 1000

std_sinLat = math.sin(std_lat * d2r)
std_sinLon = math.sin(std_lon * d2r)
std_cosLat = math.cos(std_lat * d2r)
std_cosLon = math.cos(std_lon * d2r)

N = WGS84_a_m / math.sqrt(1 - WGS84_e * WGS84_e * std_sinLat * std_sinLat)
ref_ECEF_x = (N + std_alt) * std_cosLat * std_cosLon
ref_ECEF_y = (N + std_alt) * std_cosLat * std_sinLon
ref_ECEF_z = (N * (1 - WGS84_e * WGS84_e) + std_alt) * std_sinLat

###################################
# helper function
def distance_3d(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def lla_to_ECEF(lat, lon, alt):
    sinLat = math.sin(lat * d2r)
    sinLon = math.sin(lon * d2r)
    cosLat = math.cos(lat * d2r)
    cosLon = math.cos(lon * d2r)

    N = WGS84_a_m / math.sqrt(1 - WGS84_e * WGS84_e * sinLat * sinLat)
    ECEF_x = (N + alt) * cosLat * cosLon
    ECEF_y = (N + alt) * cosLat * sinLon
    ECEF_z = (N * (1 - WGS84_e * WGS84_e) + alt) * sinLat
    return [ECEF_x, ECEF_y, ECEF_z]

def ECEF_to_Local(x, y, z):
    ROT_MAT = [ [-std_sinLat * std_cosLon,       -std_sinLat * std_sinLon,        std_cosLat],
                [             -std_sinLon,                     std_cosLon,               0.0],
                [-std_cosLat * std_cosLon,       -std_cosLat * std_sinLon,       -std_sinLat]]

    diff_ECEF = [x - ref_ECEF_x, y - ref_ECEF_y, z - ref_ECEF_z]

    local_pos = np.matmul(np.array(ROT_MAT), np.array(diff_ECEF))
    return local_pos

# Linear Interpolation
# input description : l will be interpolated list, value will be changed element
# ex) l = [0, 0, 1, 0, 0, 0, 5, 0]
# ex) l' = linear_Interpolation(l, 0)
# ex) l' = [0, 0, 1, 2, 3, 4, 5, 0]
def linear_Interpolation(l, value):
    flag = 0 # 0 : find start position / 1 : find end position
    ret_list = l

    cnt = 0
    if (ret_list[0] == value):
        while True:
            cnt += 1
            if (ret_list[cnt] != value):
                break

    start_index = cnt
    end_index = 0

    for i in range(start_index, len(ret_list)):
        if (flag == 0 and ret_list[i] == value):
            start_index = i-1
            flag = 1
        elif (flag == 1 and ret_list[i] != value):
            end_index = i
            flag = 0
            
            interval = end_index - start_index
            add_value = (ret_list[end_index] - ret_list[start_index])/float(interval)

            for j in range(1, interval):
                ret_list[start_index + j] = ret_list[start_index] + add_value * j

    return ret_list

# find start, end index first instance of NOT value in list
# ex) l = [0, 0, 1, 0, 2, 0], value = 0
# ex) return value = [2, 4]
def find_start_end_index(l, value):
    start_index = next((i for i, x in enumerate(l) if x != value), None)
    end_index = next((i for i, x in reversed(list(enumerate(l))) if x != value), None)
    return start_index, end_index
###################################

time_list = []
opv_lat_list, opv_lon_list, opv_alt_list = [], [], []
kla_lat_list, kla_lon_list, kla_alt_list = [], [], []

if (args.ads_file == None or args.save_file == None):
    sys.exit(0)

# Open txt file and Collect data
ads_file = open(args.ads_file)
Index = ads_file.readline()

while True:
    ads_line = ads_file.readline()

    if not ads_line: 
        break

    # Multi Space to One Space
    string = ' '.join(ads_line.split())

    # Parsing and convert list
    gps_data = string.split(' ')

    # (0) = Time
    # (1, 2, 3) = OPV(lat, lon, alt)
    time = float(gps_data[0])

    opv_lat = float(gps_data[1])
    opv_lon = float(gps_data[2])
    opv_alt = float(gps_data[3])

    kla_lat = float(gps_data[7])
    kla_lon = float(gps_data[8])
    kla_alt = float(gps_data[9])

    if (opv_alt < 2000 and kla_alt < 2000 and opv_alt > 0 and kla_alt > 0):
        time_list.append(int(time))

        opv_lat_list.append(opv_lat)
        opv_lon_list.append(opv_lon)
        opv_alt_list.append(opv_alt)

        kla_lat_list.append(kla_lat)
        kla_lon_list.append(kla_lon)
        kla_alt_list.append(kla_alt)


ads_file.close()

###############################################
full_time_list = []

full_kla_lat_list = []
full_kla_lon_list = []
full_kla_alt_list = []

full_opv_lat_list = []
full_opv_lon_list = []
full_opv_alt_list = []

distance_list = []

for time in range(time_list[0], time_list[-1] + 1):
    full_time_list.append(time)
    if (time in time_list):
        index = time_list.index(time)
        full_kla_lat_list.append(kla_lat_list[index])
        full_kla_lon_list.append(kla_lon_list[index])
        full_kla_alt_list.append(kla_alt_list[index])

        full_opv_lat_list.append(opv_lat_list[index])
        full_opv_lon_list.append(opv_lon_list[index])
        full_opv_alt_list.append(opv_alt_list[index])
    else:
        full_kla_lat_list.append(0)
        full_kla_lon_list.append(0)
        full_kla_alt_list.append(0)

        full_opv_lat_list.append(0)
        full_opv_lon_list.append(0)
        full_opv_alt_list.append(0)

    if (full_kla_alt_list[-1] != 0 and full_opv_alt_list[-1] != 0):
        opv_pos = lla_to_ECEF(full_opv_lat_list[-1], full_opv_lon_list[-1], full_opv_alt_list[-1])
        local_opv_pos = ECEF_to_Local(opv_pos[0], opv_pos[1], opv_pos[2])

        kla_pos = lla_to_ECEF(full_kla_lat_list[-1], full_kla_lon_list[-1], full_kla_alt_list[-1])
        local_kla_pos = ECEF_to_Local(kla_pos[0], kla_pos[1], kla_pos[2])

        distance_list.append(distance_3d(local_opv_pos, local_kla_pos))
    else:
        distance_list.append(0)

#######################################################
# Linear Interpolation

interpol_distance_list = linear_Interpolation(distance_list, 0)

interpol_kla_lat_list = linear_Interpolation(full_kla_lat_list, 0)
interpol_kla_lon_list = linear_Interpolation(full_kla_lon_list, 0)
interpol_kla_alt_list = linear_Interpolation(full_kla_alt_list, 0)

interpol_opv_lat_list = linear_Interpolation(full_opv_lat_list, 0)
interpol_opv_lon_list = linear_Interpolation(full_opv_lon_list, 0)
interpol_opv_alt_list = linear_Interpolation(full_opv_alt_list, 0)

save_file = open(args.save_file, 'w')
strFormat = '%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n'
index_Out = strFormat % ('Timestamp', 'Distance', 'OPV_lat', 'OPV_lon', 'OPV_alt', 'KLA_lat', 'KLA_lon', 'KLA_alt')
save_file.write(index_Out)

for i in range(len(full_time_list)):
    string_Out = strFormat % (str(full_time_list[i]), str(interpol_distance_list[i]), \
                            str(interpol_opv_lat_list[i]), str(interpol_opv_lon_list[i]), str(interpol_opv_alt_list[i]), \
                            str(interpol_kla_lat_list[i]), str(interpol_kla_lon_list[i]), str(interpol_kla_alt_list[i]))
    save_file.write(string_Out)

save_file.close()

# Plot Part
plt.plot(interpol_opv_lat_list, interpol_opv_lon_list)
plt.plot(interpol_kla_lat_list, interpol_kla_lon_list)

plt.legend(['OPV', 'KLA'])
plt.xlabel('LAT')
plt.ylabel('LON')

# plt.xlim([36.5, 36.68])
# plt.ylim([126.2, 126.4])

plt.show()