import csv
import math

timestamp_list = []

ac_lin_vel_x_list = []
ac_lin_vel_y_list = []
ac_lin_vel_z_list = []

ac_ang_vel_x_list = []
ac_ang_vel_y_list = []
ac_ang_vel_z_list = []

with open('_slash_mavros_slash_global_position_slash_raw_slash_gps_vel.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in plots:
        if index > 0:
            timestamp_list.append(float(row[0])/1000000000)

            ac_lin_vel_x_list.append(float(row[9]))
            ac_lin_vel_y_list.append(float(row[10]))
            ac_lin_vel_z_list.append(float(row[11]))

            ac_ang_vel_x_list.append(float(row[13]))
            ac_ang_vel_y_list.append(float(row[14]))
            ac_ang_vel_z_list.append(float(row[15]))
        index += 1


gps_file = open("200910_GPS_from_mavros_vel.txt", 'w')
strFormat = '%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n'
index_Out = strFormat % ('Timestamp', 'AC_lin_x_vel', 'AC_lin_y_vel', 'AC_lin_z_vel', 'AC_ang_x_vel', 'AC_ang_y_vel', 'AC_ang_z_vel')
gps_file.write(index_Out)
for i in range(len(timestamp_list)):
    string_Out = strFormat % (str(timestamp_list[i]), str(ac_lin_vel_x_list[i]), str(ac_lin_vel_y_list[i]), str(ac_lin_vel_z_list[i]), \
                            str(ac_ang_vel_x_list[i]), str(ac_ang_vel_y_list[i]), str(ac_ang_vel_z_list[i]))
    gps_file.write(string_Out)
gps_file.close()
