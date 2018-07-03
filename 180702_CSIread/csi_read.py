import scipy.io as sio
import os
import re
import numpy as np
import matplotlib.pyplot as plt

# For Windows
file_path = 'D:\\Matlab_Drive\\Data\\WIFI\\csi_0703_1503'
file_list = os.listdir(file_path)

abs_csi = {}
for file in file_list:
    data_read = sio.loadmat(os.path.join(file_path,file))
    num_search = re.search('\d+',file)
    csi_num = num_search.group(0)
    abs_csi[csi_num] = np.abs(data_read['csi'])

list_abs = []
for i in range(len(abs_csi)):
    abs_val = np.mean(abs_csi[str(i+1)],axis=2)
    if abs_val.shape==(2,3):
        list_abs.append(abs_val)

arr_abs = np.stack(list_abs, axis=-1)

for i in range(2):
    for j in range(3):
        plt.plot(arr_abs[i,j,:],label=str((i,j)))
        plt.legend(bbox_to_anchor=(1.01, 1.01))
