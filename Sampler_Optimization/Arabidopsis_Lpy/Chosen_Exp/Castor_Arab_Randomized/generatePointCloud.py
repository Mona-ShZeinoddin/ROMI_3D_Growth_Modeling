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



lsys = lpy.Lsystem(model_filename)
lstring = lsys.derive()
lscene = lsys.sceneInterpretation(lstring)
pointSampler(lstring, lscene, dictFileName, pointsToBeSampled, coloredPointCloudFileName, rawPointCloudFileName, labelFileName)

