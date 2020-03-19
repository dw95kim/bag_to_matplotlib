import matplotlib.pyplot as plt
import csv

import math

def get_transform_point(x, y, yaw):
    temp_x = x
    temp_y = y

    yaw_offset = yaw

    real_x = temp_x * math.cos(yaw_offset) + temp_y *math.sin(yaw_offset)
    real_y = temp_x * -1 * math.sin(yaw_offset) + temp_y * math.cos(yaw_offset)
    return [real_x, real_y]

x = []
y = []

# with open('_slash_uav0_slash_mavros_slash_global_position_slash_compass_hdg.csv','r') as csvfile:
with open('_slash_uav0_slash_mavros_slash_global_position_slash_local.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in plots:
        if (index < 5):
            index += 1
        else:
            temp_x, temp_y = get_transform_point(float(row[11]), float(row[12]), 167 * math.pi / 180)

            x.append(temp_x)
            y.append(temp_y)

            # x.append(float(row[11]))
            # y.append(float(row[12]))

            # x.append(index)
            # y.append(float(row[1]))

            # print(type(x[0]))
            index += 1

            # if (index > 5):
            #     break
            # if(index > 0 and index < 10):
            #     print(row[1])
        
# plt.plot(x,y, 'x', label='Loaded from file!')

plt.plot(x, y, 'x')
plt.plot(x[:1000], y[:1000], 'x')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim([-30,30])
plt.ylim([-30,30])
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
plt.show()

