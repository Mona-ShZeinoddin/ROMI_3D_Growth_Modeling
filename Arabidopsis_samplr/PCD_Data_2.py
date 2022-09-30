from pathlib import Path
import shutil
import os
import open3d as o3d 
import numpy as np
import random

#src = '/home/mona/Documents/My_model_of_growth/PoinTr_data/Experiment_01/D2'
#trg = '/home/mona/Documents/My_model_of_growth/PoinTr_data/Experiment_01/data'
#src = '/mnt/diskSustainability/mona/PoinTr/Experiment01/D2'
#trg = '/mnt/diskSustainability/mona/PoinTr/Experiment01/data'
#src = '/home/mona/Documents/Plant_modeling_with_LPY/sampling_christophes_arabidopsis/Data'
#trg = '/home/mona/Documents/Plant_modeling_with_LPY/sampling_christophes_arabidopsis/data'
src = '/home/mona/Documents/My_model_of_growth/Arabidopsis_samplr/Data'
trg = '/home/mona/Documents/My_model_of_growth/Arabidopsis_samplr/data'

arr_complete = os.listdir(os.path.join(src,'complete'))
random.shuffle(arr_complete)
test,val,train = [],[],[]
test =  test + arr_complete[0:300]
val = val + arr_complete[800:]
train = train + arr_complete[300:800]

for i in train:
    original = os.path.join(src,'complete',i)
    target =  os.path.join(trg,'train','complete','00000001',i)
    shutil.copyfile(original, target)
    original = os.path.join(src,'partial',i)
    if(not(os.path.isdir(os.path.join(trg,'train','partial','00000001',i.split('.')[0])))):
        os.mkdir(os.path.join(trg,'train','partial','00000001',i.split('.')[0]))
    target =  os.path.join(trg,'train','partial','00000001',i.split('.')[0],'00.pcd')
    shutil.copyfile(original, target)

for j in test:
    original = os.path.join(src,'complete',j)
    target =  os.path.join(trg,'test','complete','00000001',j)
    shutil.copyfile(original, target)
    original = os.path.join(src,'partial',j)
    if (not(os.path.isdir(os.path.join(trg,'test','partial','00000001',j.split('.')[0])))):
        os.mkdir(os.path.join(trg,'test','partial','00000001',j.split('.')[0]))
    target =  os.path.join(trg,'test','partial','00000001',j.split('.')[0],'00.pcd')
    shutil.copyfile(original, target)


for k in val:
    original = os.path.join(src,'complete',k)
    target =  os.path.join(trg,'val','complete','00000001',k)
    shutil.copyfile(original, target)
    original = os.path.join(src,'partial',k)
    if (not(os.path.isdir(os.path.join(trg,'val','partial','00000001',k.split('.')[0])))):
        os.mkdir(os.path.join(trg,'val','partial','00000001',k.split('.')[0]))
    target =  os.path.join(trg,'val','partial','00000001',k.split('.')[0],'00.pcd')
    shutil.copyfile(original, target)

