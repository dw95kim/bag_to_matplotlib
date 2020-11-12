import csv
import math

timestamp_list = []

ac_lat_list = []
ac_lon_list = []
ac_alt_list = []

with open('_slash_mavros_slash_global_position_slash_global.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in plots:
        if index > 0:
            timestamp_list.append(float(row[0])/1000000000)

            ac_lat_list.append(float(row[10]))
            ac_lon_list.append(float(row[11]))
            ac_alt_list.append(float(row[12]))
        index += 1


gps_file = open("200910_GPS_from_mavros_pos.txt", 'w')
strFormat = '%-20s%-20s%-20s%-20s\n'
index_Out = strFormat % ('Timestamp', 'AC_lat', 'AC_lon', 'AC_alt')
gps_file.write(index_Out)
for i in range(len(timestamp_list)):
    string_Out = strFormat % (str(timestamp_list[i]), str(ac_lat_list[i]), str(ac_lon_list[i]), str(ac_alt_list[i]))
    gps_file.write(string_Out)
gps_file.close()
