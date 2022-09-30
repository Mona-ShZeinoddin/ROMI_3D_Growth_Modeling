from pathlib import Path
import shutil
import os
import open3d as o3d 
import numpy as np
import random
 


def NormalizeData(data, a, b):
    #a is np.min(data)
    #b is np.max(data)
    return ((data - a) / (b - a))-0.5

# defining source and destination
# paths
src = '/mnt/diskSustainability/mona/smplr'
#src = '/mnt/diskSustainability/mona/point_sampler_code'
#trg_h = '/mnt/diskSustainability/mona/PoinTr/Experiment01'
trg_h = '/mnt/diskSustainability/mona/smplr/Data'
 

# iterating over all the files in
# the source directory
for i in range(1,1000):
    for x in [15,1]:
        if x == 15:
            z = 'complete'
            fname = 'rawPoints'+'_'+str(i)+'_'+str(x)+'.'+'xyz'
            trg = os.path.join(trg_h,z)
            arr_hat = np.loadtxt(os.path.join(src,fname),delimiter = ',')
            a = np.amin(arr_hat)
            b = np.amax(arr_hat)
        else:
            z = 'partial'
            trg = os.path.join(trg_h,z)
        fname = 'rawPoints'+'_'+str(i)+'_'+str(x)+'.'+'xyz'
        #fname = 'rawPoints'+'_'+str(i)+'.'+'txt'
        tname = 'RawPoints'+'_'+str(i)+'.'+'pcd'
        arr = np.loadtxt(os.path.join(src,fname),delimiter = ',')
        scaled_arr = NormalizeData(arr,a,b)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(scaled_arr)
        o3d.io.write_point_cloud(os.path.join(trg,tname), pcd, write_ascii=True)