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
#dictFileName = "labelDictionary.txt"
#model_filename = "Arabido.lpy"


parser = argparse.ArgumentParser()
parser.add_argument("InputFileName")
parser.add_argument("InputLabelDictionary")
parser.add_argument("TotalNumberOfPoints")
args = parser.parse_args()
model_filename = args.InputFileName
dictFileName = args.InputLabelDictionary
pointsToBeSampled = int(args.TotalNumberOfPoints)


from openalea.lpy import *
from openalea.plantgl.all import *
A = list(range(1,36))

       
def sample_arab(x):
# x is the seed 
# y is the derivation length
    lsys = Lsystem(model_filename,{'SEED':x})
    lstring = lsys.derive()
    lscene = lsys.sceneInterpretation(lstring)
    coloredPointCloudFileName = "pointsWithColor"+"_"+str(x)+".xyz"
    rawPointCloudFileName = "rawPoints"+"_"+str(x)+".xyz"
    labelFileName = "rawLabels"+"_"+str(x)+".txt"
    pointSampler(lstring, lscene, dictFileName,20000,coloredPointCloudFileName,rawPointCloudFileName, labelFileName)

#for x in A:
#    for y in B:
#        sample_stem(x,y)
        
        
        
Parallel(n_jobs=35)(delayed(sample_arab)(x) for x in A)       
        
        
        
        
        
        
        
