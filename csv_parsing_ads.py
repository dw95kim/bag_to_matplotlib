import csv
import math


OPV_icao = 7463479
KLA_icao = 7463475

timestamp_list = []

OPV_lat_list = []
OPV_lon_list = []
OPV_alt_list = []
OPV_hor_vel = []
OPV_ver_vel = []
OPV_heading = []

KLA_lat_list = []
KLA_lon_list = []
KLA_alt_list = []
KLA_hor_vel = []
KLA_ver_vel = []
KLA_heading = []

# with open('_slash_uav0_slash_mavros_slash_global_position_slash_compass_hdg.csv','r') as csvfile:
with open('_slash_ADS_B_slash_Traffic_Report_Array.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in plots:
        if index > 0:
            timestamp_list.append(float(row[0])/1000000000)

            OPV_found_number = 0
            KLA_found_number = 0

            multi_val = 0
            break_ok = 0

            for start_ind in [8, 36, 64, 92, 110, 138, 166, 194, 222]:
                if (len(row) < start_ind+1):
                    break

                if (len(row[start_ind]) == 0):
                    break

                if (int(row[start_ind]) == OPV_icao):
                    OPV_found_number = start_ind
                if (int(row[start_ind]) == KLA_icao):
                    KLA_found_number = start_ind
                
                multi_val += 1

            if OPV_found_number == 0:
                OPV_lat_list.append(0)
                OPV_lon_list.append(0)
                OPV_alt_list.append(0)
                OPV_hor_vel.append(0)
                OPV_ver_vel.append(0)
                OPV_heading.append(0)
            else:
                OPV_lat_list.append(float(row[OPV_found_number+1])/10000000)
                OPV_lon_list.append(float(row[OPV_found_number+2])/10000000)
                OPV_alt_list.append(float(row[OPV_found_number+3])/1000)
                OPV_heading.append(float(row[OPV_found_number+4])/100)
                OPV_hor_vel.append(float(row[OPV_found_number+5])/100)
                OPV_ver_vel.append(float(row[OPV_found_number+6])/100)

            if KLA_found_number == 0:
                KLA_lat_list.append(0)
                KLA_lon_list.append(0)
                KLA_alt_list.append(0)
                KLA_hor_vel.append(0)
                KLA_ver_vel.append(0)
                KLA_heading.append(0)
            else:
                KLA_lat_list.append(float(row[KLA_found_number+1])/10000000)
                KLA_lon_list.append(float(row[KLA_found_number+2])/10000000)
                KLA_alt_list.append(float(row[KLA_found_number+3])/1000)
                KLA_heading.append(float(row[KLA_found_number+4]/100))
                KLA_hor_vel.append(float(row[KLA_found_number+5]/100))
                KLA_ver_vel.append(float(row[KLA_found_number+6]/100))
            

        index += 1


gps_file = open("200910_GPS_from_ADS_B.txt", 'w')
strFormat = '%-20s%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s%-15s\n'
index_Out = strFormat % ('Timestamp', 'OPV_lat', 'OPV_lon', 'OPV_alt', 'OPV_Heading', 'OPV_Hor_Vel', 'OPV_Ver_Vel', \
                                    'KLA_lat', 'KLA_lon', 'KLA_alt', 'KLA_Heading', 'KLA_Hor_Vel', 'KLA_Ver_Vel')
gps_file.write(index_Out)
for i in range(len(timestamp_list)):
    string_Out = strFormat % (str(timestamp_list[i]), str(OPV_lat_list[i]), str(OPV_lon_list[i]), str(OPV_alt_list[i]), str(OPV_heading[i]),  str(OPV_hor_vel[i]),  str(OPV_ver_vel[i]), \
                            str(KLA_lat_list[i]), str(KLA_lon_list[i]), str(KLA_alt_list[i]), str(KLA_heading[i]), str(KLA_hor_vel[i]), str(KLA_ver_vel[i]))
    gps_file.write(string_Out)
gps_file.close()
