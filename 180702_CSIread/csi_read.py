import scipy.io as sio
import os
import re
import numpy as np
import matplotlib.pyplot as plt

# For Windows
dateid = 'csi201807231653'
file_path = '\\\\192.168.10.51\\hdd1tb\\Data\\CSI\\' + dateid
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
    if abs_val.shape==(1,2):
        list_abs.append(abs_val)

arr_abs = np.stack(list_abs, axis=-1)

for i in range(1):
    for j in range(2):
        plt.plot(arr_abs[i,j,:],label=str((i,j)))
        plt.legend(bbox_to_anchor=(1.01, 1.01))