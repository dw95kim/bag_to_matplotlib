import csv
import math

OPV_icao = 7463479
KLA_icao = 7463475

timestamp_list = []

ac_lat_list = []
ac_lon_list = []
ac_alt_list = []

ac_roll_list = []
ac_pitch_list = []
ac_yaw_list = []

ac_vel_x_aed = []
ac_vel_y_aed = []
ac_vel_z_aed = []

ac_vel_x_ned = []
ac_vel_y_ned = []
ac_vel_z_ned = []

# with open('_slash_uav0_slash_mavros_slash_global_position_slash_compass_hdg.csv','r') as csvfile:
with open('_slash_UAV_slash_101_slash_FCC.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in plots:
        if index > 0:
            timestamp_list.append(float(row[0])/1000000000)

            gps = row[16][1:-1].split(", ")
            ac_lat_list.append(float(gps[0]))
            ac_lon_list.append(float(gps[1]))
            ac_alt_list.append(float(gps[2]))
            
            rpy = row[31][1:-1].split(", ")
            ac_roll_list.append(float(rpy[0]))
            ac_pitch_list.append(float(rpy[1]))
            ac_yaw_list.append(float(rpy[2]))

            # vel_aed = row[35][1:-1].split(", ")
            # ac_vel_x_aed.append(float(vel_aed[0]))
            # ac_vel_y_aed.append(float(vel_aed[1]))
            # ac_vel_z_aed.append(float(vel_aed[2]))

            # vel_ned = row[40][1:-1].split(", ")
            # ac_vel_x_ned.append(float(vel_ned[0]))
            # ac_vel_y_ned.append(float(vel_ned[1]))
            # ac_vel_z_ned.append(float(vel_ned[2]))
        index += 1


gps_file = open("200910_GPS_from_Rasberry.txt", 'w')
# strFormat = '%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n'
# index_Out = strFormat % ('Timestamp', 'AC_lat', 'AC_lon', 'AC_alt', 'AC_vel_x_AED', 'AC_vel_y_AED', 'AC_vel_z_AED', 'AC_vel_x_NED', 'AC_vel_y_NED', 'AC_vel_Z_NED')
# gps_file.write(index_Out)
# for i in range(len(timestamp_list)):
#     string_Out = strFormat % (str(timestamp_list[i]), str(ac_lat_list[i]), str(ac_lon_list[i]), str(ac_alt_list[i]), \
#                             str(ac_vel_x_aed[i]), str(ac_vel_y_aed[i]), str(ac_vel_z_aed[i]), \
#                             str(ac_vel_x_ned[i]), str(ac_vel_y_ned[i]), str(ac_vel_z_ned[i]))
#     gps_file.write(string_Out)
# gps_file.close()

strFormat = '%-20s%-20s%-20s%-20s%-20s%-20s%-20s\n'
index_Out = strFormat % ('Timestamp', 'AC_lat', 'AC_lon', 'AC_alt', 'AC_roll', 'AC_pitch', 'AC_yaw')
gps_file.write(index_Out)
for i in range(len(timestamp_list)):
    string_Out = strFormat % (str(timestamp_list[i]), str(ac_lat_list[i]), str(ac_lon_list[i]), str(ac_alt_list[i]), \
                            str(ac_roll_list[i]), str(ac_pitch_list[i]), str(ac_yaw_list[i]))
    gps_file.write(string_Out)
gps_file.close()