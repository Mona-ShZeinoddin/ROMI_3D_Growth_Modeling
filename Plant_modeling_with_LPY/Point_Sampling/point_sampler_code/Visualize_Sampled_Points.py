import open3d as o3d 
import numpy as np
arr = np.loadtxt("rawPoints.xyz",delimiter = ',')
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(arr)
#print(np.asarray(pcd_new))
o3d.visualization.draw_geometries([pcd])
