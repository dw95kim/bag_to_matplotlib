import csv
import math

timestamp_list = []

ac_roll_list = []
ac_pitch_list = []
ac_yaw_list = []

d2r = math.pi/180.0
r2d = 180.0/math.pi

def QuaterniontoEuler(q):
    t0 = 2 * (q[3] * q[0] + q[1] * q[2])
    t1 = 1 - 2 * (q[0] * q[0] + q[1] * q[1])
    roll = math.atan2(t0, t1) * r2d

    t2 = 2 * (q[3] * q[1] + q[2] * q[0])
    if (t2 > 1.0):
        t2 = 1.0
    if (t2 < -1.0):
        t2 = -1
    pitch = -math.asin(t2) * r2d

    t3 = 2 * (q[3] * q[2] + q[0] * q[1])
    t4 = 1 - 2 * (q[1] * q[1] + q[2] * q[2])
    yaw = math.atan2(t3, t4) * r2d
    if (yaw < 0):
        yaw += 360.0

    return [roll, pitch, yaw]

with open('_slash_mavros_slash_global_position_slash_local.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in plots:
        if index > 0:
            timestamp_list.append(float(row[0])/1000000000)

            q = [float(row[15]), float(row[16]), float(row[17]), float(row[18])]
            roll, pitch, yaw = QuaterniontoEuler(q)

            ac_roll_list.append(roll)
            ac_pitch_list.append(pitch)
            ac_yaw_list.append(yaw)
        index += 1

gps_file = open("200910_GPS_from_mavros_ori.txt", 'w')
strFormat = '%-20s%-20s%-20s%-20s\n'
index_Out = strFormat % ('Timestamp', 'AC_roll', 'AC_pitch', 'AC_yaw')
gps_file.write(index_Out)
for i in range(len(timestamp_list)):
    string_Out = strFormat % (str(timestamp_list[i]), str(ac_roll_list[i]), str(ac_pitch_list[i]), str(ac_yaw_list[i]))
    gps_file.write(string_Out)
gps_file.close()
