import open3d as o3d
import numpy as np
import cv2
import glob
import os
import imageio
​
​
​
def rotate_view(vis):
    global count
    global name
​
    # first thing, make the background black
    opt = vis.get_render_option()
    if opt.background_color.sum() != 0:
        opt.background_color = np.asarray([0, 0, 0])
        return False  # ? if you don't do this, first image will have white bg
​
    # then, rotate
    ctr = vis.get_view_control()
    if count==0:     ctr.rotate(-1100.0, 800.0)  # no idea the units here
    else: ctr.rotate(50, 0)  # no idea the units here
​
    # capture the image (colored)
    image = np.asarray(vis.capture_screen_float_buffer())
    cv2.imwrite("%s/%03d.png"%(name, count), (image[:,:,::-1]*255).astype(np.uint8))
    #plt.imshow(image)
    #print(image.shape)
    #plt.axis('off')
    #plt.savefig("lala_%03d.png"%count)
​
    count += 1
    if count > 40:
        x = 0/0  # idk how to stop it, this works
​
    return False
​
"""
count=0
files = ["small.ply", "medium.ply", "big.ply"] 
​
i = 0
pcd = o3d.io.read_point_cloud(files[i])
pcd.paint_uniform_color([0,1,0])
​
name=files[i].strip(".ply")
if not(os.path.exists(name)):
	os.mkdir(name)
​
o3d.visualization.draw_geometries_with_animation_callback( [pcd], rotate_view, width=600, height=1200)
"""
​
"""
count = 0
folder = "/home/kodda/Data/4d_plants/arabidopsis_lyon/recons_may2021/vs_0.2_dil_1/"
​
pcd_files = glob.glob(folder + "/*")
pcd_files.sort()
​
i=56
name = pcd_files[i].split("/")[-1].strip(".ply")
if not(os.path.exists(name)):
	os.mkdir(name)
​
pcd = o3d.io.read_point_cloud(pcd_files[i])
pcd.paint_uniform_color([0,1,0])
​
o3d.visualization.draw_geometries_with_animation_callback( [pcd], rotate_view, width=600, height=1200)
"""
​
f1 = glob.glob("small/*")
f1.sort()
f2 = glob.glob("medium/*")
f2.sort()
f3 = glob.glob("big/*")
f3.sort()
​
writer = imageio.get_writer('growth_clean.mp4', fps=6)
​
for i in range(1,41):
  im1 = cv2.imread(f1[i])
  im2 = cv2.imread(f2[i])
  im3 = cv2.imread(f3[i])
  im=np.hstack([im1,im2,im3])
​
  writer.append_data(im[:,:,::-1])
writer.close()