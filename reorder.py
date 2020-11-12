import os
import time

path = '/home/usrg-asus/Civil/KLA_img_test/2020-09-10-12:39:22/frame0/'

file_name_list = []
file_name_sort = []
for filename in os.listdir(path):
	if (len(filename) == 16):
		new_filename = filename[:12] + "0" + ".jpg"
		os.rename(path+filename, path+new_filename)
