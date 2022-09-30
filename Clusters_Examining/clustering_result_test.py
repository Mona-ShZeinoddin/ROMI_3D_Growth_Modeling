import sklearn 
from sklearn.cluster import KMeans
import os
import open3d as o3d
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KDTree

i = 1
fname = 'pred'+'_'+str(i)+'.xyz'
addr =  "/home/mona/Documents/My_model_of_growth/PoinTr_data/test_stem_1000"
pcd_pred = o3d.io.read_point_cloud(os.path.join(addr,fname))
X = np.array(pcd_pred.points)
#print(X.shape)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
a = kmeans.labels_
indice_one = np.where(a==1)
data_one = X[indice_one]
#print(type(data_one))
pcd_reconstructed = o3d.geometry.PointCloud()
pcd_reconstructed.points = o3d.utility.Vector3dVector(data_one)
#print(np.asarray(pcd_new))
o3d.visualization.draw_geometries([pcd_reconstructed])
np.savetxt(os.path.join("/home/mona/Documents/My_model_of_growth","cluster.txt"),data_one)

def chamfer_d(pc_1, pc_2):
    tree = KDTree(pc_1)
    ds, _ = tree.query(pc_2)
    d_21 = np.mean(ds)
    tree = KDTree(pc_2)
    ds, _ = tree.query(pc_1)
    d_12 = np.mean(ds)
    return d_21 + d_12

gname = 'gt'+'_'+str(i)+'.xyz'
addr =  "/home/mona/Documents/My_model_of_growth/PoinTr_data/test_stem_1000"
pcd_gt = o3d.io.read_point_cloud(os.path.join(addr,gname))
Y = np.array(pcd_gt.points)

print(chamfer_d(Y,data_one))