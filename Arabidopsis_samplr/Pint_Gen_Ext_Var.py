### Main automating script for point sampling (generating labelled point cloud on virtual model) ###
### Usage: python generatePointCloud.py LpyModelFile labelDictionaryFile numberOfPoints ###
### Example: python generatePointCloud.py Arabidopsis.lpy labelDictionary.txt 1000 ###
### The label dictionary file "labelDictionary.txt" should be updated accordingly for each model ###
### Author: Ayan Chaudhury (ayanchaudhury.cs@gmail.com) ###
### INRIA team MOSAIC ###
### Updated: August 2021 ###

from openalea import lpy
from openalea.plantgl.all import *
import argparse
from scan_utils import *
from joblib import Parallel, delayed
coloredPointCloudFileName = "pointsWithColor.xyz"
rawPointCloudFileName = "rawPoints.xyz"
labelFileName = "rawLabels.txt"
dictFileName = "labelDictionary.txt"
model_filename = "my_arabidopsis.lpy"


parser = argparse.ArgumentParser()
parser.add_argument("InputFileName")
parser.add_argument("InputLabelDictionary")
parser.add_argument("TotalNumberOfPoints")
args = parser.parse_args()
#model_filename = args.InputFileName
#dictFileName = args.InputLabelDictionary
pointsToBeSampled = int(args.TotalNumberOfPoints)

from openalea.lpy import *
from openalea.plantgl.all import *


#def arabidopsis_sampling(y):
y = 10
lsys = lpy.Lsystem(model_filename,{'a':y})
lstring = lsys.derive()
lscene = lsys.sceneInterpretation(lstring)
print(lscene)
coloredPointCloudFileName = "pointsWithColor"+"_"+str(y)+".xyz"
rawPointCloudFileName = "rawPoints"+"_"+str(y)+".xyz"
labelFileName = "rawLabels"+"_"+str(y)+".txt"
pointSampler(lstring, lscene, dictFileName, 16384, coloredPointCloudFileName, rawPointCloudFileName, labelFileName)



#arabidopsis_sampling(10)
##Parallel(n_jobs=1)(delayed(arabidopsis_sampling)(x) for x in range(1,3))
        




