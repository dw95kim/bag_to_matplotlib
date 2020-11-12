import os

path = '/home/kla-100/Civil/KLA_img_test/2020-09-10-14:55:01/frame2/'
file_name_list = []
file_name_sort = []
for filename in os.listdir(path):
	date = os.path.getmtime(path + filename)
	# print(filename, float(date))
	file_name_list.append(float(date))
	file_name_sort.append(float(date))

file_name_sort.sort()
rename_index_list = []

for i in range(len(file_name_list)):
	new_index = file_name_sort.index(file_name_list[i]) + 1
	rename_index_list.append(new_index)

index = 0
for filename in os.listdir(path):
	str_index = str(rename_index_list[index])
	new_name = str_index.zfill(5)
	index += 1

	os.rename(path+filename, path+new_name + '.jpg')
