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
parser.add_argument('--opv_file', type=str, default = None)
parser.add_argument('--kla_file', type=str, default = None)
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
###################################

opv_time_list = []
avg_opv_time_list = []

kla_time_list = []
avg_kla_time_list = []

opv_lat_list = []
opv_lon_list = []
opv_alt_list = []

avg_opv_lat_list = []
avg_opv_lon_list = []
avg_opv_alt_list = []

kla_lat_list = []
kla_lon_list = []
kla_alt_list = []

avg_kla_lat_list = []
avg_kla_lon_list = []
avg_kla_alt_list = []

if (args.opv_file == None):
    sys.exit(0)

if (args.kla_file == None):
    sys.exit(0)    

if (args.save_file == None):
    sys.exit(0)

# Open txt file and Collect data
opv_file = open(args.opv_file)
Index = opv_file.readline()

kla_file = open(args.kla_file)
Index = kla_file.readline()

while True:
    opv_line = opv_file.readline()

    if not opv_line: 
        break

    # Multi Space to One Space
    string = ' '.join(opv_line.split())

    # Parsing and convert list
    gps_data = string.split(' ')

    # (0) = Time
    # (1, 2, 3) = OPV(lat, lon, alt)
    opv_time_list.append(float(gps_data[0]))
    opv_lat_list.append(float(gps_data[1]))
    opv_lon_list.append(float(gps_data[2]))
    opv_alt_list.append(float(gps_data[3]))

opv_file.close()

while True:
    kla_line = kla_file.readline()

    if not kla_line: 
        break

    # Multi Space to One Space
    string = ' '.join(kla_line.split())

    # Parsing and convert list
    gps_data = string.split(' ')

    # (0) = Time
    # (1, 2, 3) = KLA(lat, lon, alt)
    kla_time_list.append(float(gps_data[0]))
    kla_lat_list.append(float(gps_data[1]))
    kla_lon_list.append(float(gps_data[2]))
    kla_alt_list.append(float(gps_data[3]))

kla_file.close()

index = 0
while True:
    cnt = 1
    if (index >= len(opv_time_list)):
        break
    start_int_time = int(opv_time_list[index])
    for i in range(1000):
        if (index + cnt >= len(opv_time_list)):
            break
        cur_int_time = int(opv_time_list[index + cnt])
        if (cur_int_time != start_int_time):
            break
        cnt += 1

    temp_lat_list = opv_lat_list[index:index+cnt]
    temp_lon_list = opv_lon_list[index:index+cnt]
    temp_alt_list = opv_alt_list[index:index+cnt]
    avg_opv_time_list.append(start_int_time)
    avg_opv_lat_list.append(sum(temp_lat_list)/len(temp_lat_list))
    avg_opv_lon_list.append(sum(temp_lon_list)/len(temp_lon_list))
    avg_opv_alt_list.append(sum(temp_alt_list)/len(temp_alt_list))

    index += cnt

index = 0
while True:
    cnt = 1
    if (index >= len(kla_time_list)):
        break
    start_int_time = int(kla_time_list[index])
    for i in range(1000):
        if (index + cnt >= len(kla_time_list)):
            break
        cur_int_time = int(kla_time_list[index + cnt])
        if (cur_int_time != start_int_time):
            break
        cnt += 1
    
    temp_lat_list = kla_lat_list[index:index+cnt]
    temp_lon_list = kla_lon_list[index:index+cnt]
    temp_alt_list = kla_alt_list[index:index+cnt]
    avg_kla_time_list.append(start_int_time)
    avg_kla_lat_list.append(sum(temp_lat_list)/len(temp_lat_list))
    avg_kla_lon_list.append(sum(temp_lon_list)/len(temp_lon_list))
    avg_kla_alt_list.append(sum(temp_alt_list)/len(temp_alt_list))

    index += cnt

start_time = min(avg_opv_time_list[0], avg_kla_time_list[0])
end_time = max(avg_kla_time_list[-1], avg_kla_time_list[-1])

time_list = []

all_avg_kla_lat_list = []
all_avg_kla_lon_list = []
all_avg_kla_alt_list = []

all_avg_opv_lat_list = []
all_avg_opv_lon_list = []
all_avg_opv_alt_list = []

distance_list = []

for time in range(start_time, end_time + 1):
    time_list.append(time)
    if (time in avg_kla_time_list):
        kla_index = avg_kla_time_list.index(time)
        all_avg_kla_lat_list.append(avg_kla_lat_list[kla_index])
        all_avg_kla_lon_list.append(avg_kla_lon_list[kla_index])
        all_avg_kla_alt_list.append(avg_kla_alt_list[kla_index])
    else:
        all_avg_kla_lat_list.append(0)
        all_avg_kla_lon_list.append(0)
        all_avg_kla_alt_list.append(0)

    if (time in avg_opv_time_list):
        opv_index = avg_opv_time_list.index(time)
        all_avg_opv_lat_list.append(avg_opv_lat_list[opv_index])
        all_avg_opv_lon_list.append(avg_opv_lon_list[opv_index])
        all_avg_opv_alt_list.append(avg_opv_alt_list[opv_index])
    else:
        all_avg_opv_lat_list.append(0)
        all_avg_opv_lon_list.append(0)
        all_avg_opv_alt_list.append(0)
    
    if (all_avg_opv_lat_list[-1] != 0 and all_avg_kla_lat_list[-1] != 0):
        opv_pos = lla_to_ECEF(all_avg_opv_lat_list[-1], all_avg_opv_lon_list[-1], all_avg_opv_alt_list[-1])
        local_opv_pos = ECEF_to_Local(opv_pos[0], opv_pos[1], opv_pos[2])
        kla_pos = lla_to_ECEF(all_avg_kla_lat_list[-1], all_avg_kla_lon_list[-1], all_avg_kla_alt_list[-1])
        local_kla_pos = ECEF_to_Local(kla_pos[0], kla_pos[1], kla_pos[2])
        distance_list.append(distance_3d(local_opv_pos, local_kla_pos))
    else:
        distance_list.append(0)

#######################################################
# Linear Interpolation
# ex) distance list = [0, 0, 1, 0, 0, 0, 5, 0] --> [0, 0, 1, 2, 3, 4, 5, 0]
flag = 0 # 0 : find start position / 1 : find end position
interpol_distance_list = distance_list

cnt = 0
if (interpol_distance_list[0] == 0):
    while True:
        cnt += 1
        if (interpol_distance_list[cnt] != 0):
            break

start_index = cnt
end_index = 0

for i in range(start_index, len(interpol_distance_list)):
    if (flag == 0 and interpol_distance_list[i] == 0):
        start_index = i-1
        flag = 1
    elif (flag == 1 and interpol_distance_list[i] != 0):
        end_index = i
        flag = 0
        
        interval = end_index - start_index
        add_value = (interpol_distance_list[end_index] - interpol_distance_list[start_index])/float(interval)

        for j in range(1, interval):
            interpol_distance_list[start_index + j] = interpol_distance_list[start_index] + add_value * j

save_file = open(args.save_file, 'w')
strFormat = '%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n'
index_Out = strFormat % ('Timestamp', 'Distance', 'OPV_lat', 'OPV_lon', 'OPV_alt', 'KLA_lat', 'KLA_lon', 'KLA_alt')
save_file.write(index_Out)

for i in range(len(time_list)):
    string_Out = strFormat % (str(time_list[i]), str(interpol_distance_list[i]), \
                            str(all_avg_opv_lat_list[i]), str(all_avg_opv_lon_list[i]), str(all_avg_opv_alt_list[i]), \
                            str(all_avg_kla_lat_list[i]), str(all_avg_kla_lon_list[i]), str(all_avg_kla_alt_list[i]))
    save_file.write(string_Out)

save_file.close()

# Plot Part
plt.plot(avg_opv_lat_list, avg_opv_lon_list)
plt.plot(avg_kla_lat_list, avg_kla_lon_list)

plt.legend(['OPV', 'KLA'])
plt.xlabel('LAT')
plt.ylabel('LON')

# plt.xlim([36.5, 36.68])
# plt.ylim([126.2, 126.4])

plt.show()
