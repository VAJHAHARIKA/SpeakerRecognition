import os
import numpy as np
import pickle
import os.path

rootdir = os.path.join(os.getcwd(), 'samples') 
attendance_file_path = os.path.join(os.getcwd(), r'Attendance_data\Attendance_data.pickle')

names = []

for subdir, dirs, files in os.walk(rootdir):
    for dir_name in dirs:
    	names.append(dir_name)
    	#print('person dir : ', dir_name)
    	#print('person dir files : \n', os.listdir(os.path.join(rootdir, dir_name)))
    	#for file_name in os.listdir(os.path.join(rootdir, dir_name)):
    		#print(file_name)
    		#print('person dir files seperate : \n', os.path.join(rootdir, dir_name, file_name))
        #print(os.path.join(subdir, file))\

#print('Names : ', names)

#print('dir keys: ', list(Attendance.keys()))

# with open(r'Attendance_data\Attendance_data.pickle', 'wb') as handle:
#     pickle.dump(Attendance, handle, protocol=pickle.HIGHEST_PROTOCOL)

def print_data(info):
	with open(r'Attendance_data\Attendance_data.pickle', 'rb') as handle:
		unserialized_data = pickle.load(handle)
		print(info, unserialized_data)

# if data exists but new folder added
if os.path.exists(attendance_file_path) and os.path.isfile(attendance_file_path):
	# Load data (deserialize)
	with open(r'Attendance_data\Attendance_data.pickle', 'rb') as handle:
		unserialized_data = pickle.load(handle)

	#print(Attendance == unserialized_data)

	#print('pickle : ', unserialized_data)
	#print(type(unserialized_data))
	#print('pickle dat keys : ', list(unserialized_data.keys()))

	#unserialized_data1 = {key: 0 for key in names - list(unserialized_data.keys())}
	for key in names:
		if key not in list(unserialized_data.keys()):
			unserialized_data[key] = 0
	#print('\nend', unserialized_data)
	with open(r'Attendance_data\Attendance_data.pickle', 'wb') as handle:
		pickle.dump(unserialized_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

	print_data('Data is updated : \n')

# if data doesn't exist
if not os.path.exists(attendance_file_path) and not os.path.isfile(attendance_file_path):
	
	if not os.path.exists('Attendance_data'):
		os.makedirs('Attendance_data')

	empty = dict()
	for key in names:
		if key not in list(empty.keys()):
			empty[key] = 1

	with open(r'Attendance_data\Attendance_data.pickle', 'wb') as handle:
		pickle.dump(empty, handle, protocol=pickle.HIGHEST_PROTOCOL)

	print_data('Data is created : \n')



# np.save(r'Attendance_data\Attendance', Attendance)

#data = np.load(r'Attendance_data\Attendance.npy',  allow_pickle=True) 
#print(type(data))
#print(data)
#print(dict(data))
#print('dat keys : ', list(data.keys()))