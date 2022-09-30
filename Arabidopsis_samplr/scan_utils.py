### This script contains the functions to tessalate the shape into triangles, and performs the point sampling ###
### Author: Ayan Chaudhury (ayanchaudhury.cs@gmail.com) ###
### INRIA team MOSAIC ###
### Updated: August 2021 ###

from openalea.plantgl.all import *
import numpy as np
from math import *
from utilities import *
import ast


# Given a geometry in the lscene, the function performs tessalation to
# decompose the shape into triangles. Returns the list of points & the
# corresponding triangle indices.
def performTessalation(currentGeometry):
  t = Tesselator()
  currentGeometry.apply(t)
  triangleset = t.result
  ptList = triangleset.pointList
  idxList = triangleset.indexList
  return ptList, idxList



# This is the main function that performs the point sampling. It takes as argument the lstring, lscene coming
# from the virtual model, the label dictionary as text file total number of points to be sampled, and the 3
# output file names 
def pointSampler(lstring, lscene, dictionaryFile, totalNumberOfResampledPts, pointsWithColor, rawPoints, rawLabels):
  #totalNumberOfResampledPts = 2048 # desired number of points
  randomPointLabels = [] # stores the labels of all points
  globalVertexList = [] #stores all vertices (without repeatition)
  globalTriangleIdList = [] #stores id of vertices (as in globalVertexList) for the triangles
  globalTriangleLabelList = [] #stores the label of each triangle of globalTriangleIdList
  globalGeometryInfoList = [] #stores the geometry of all primitives
  cyllist = [] # stores all cylinder primitives
  geomInfoList = [] # stores geometry of all the primitives

  # reading the label dictionary from the file
  with open(dictionaryFile) as f:
    data = f.read()
  # reconstructing the data as a dictionary
  labelTable = ast.literal_eval(data)

  # loop over all elements in the lscene
  for shape in lscene:
    botpoint = Vector3(0,0,0) # the model is based at the origin
    heading = Vector3(0,0,1)
    geometry = shape
    id = shape.id
    currentModule = lstring[id].name
    labelCurrentModule = labelTable[currentModule]
    [ptList, idxList] = performTessalation(shape.geometry) # get the triangle corresponding to the primitive  
    vertexList = obtainVertexList(ptList) # store the set of indices of vertices that form triangles (local index)
    triangleList = obtainTriangleIdxList(idxList) # store the set of triangle indices
    ### Now perform the global storing operations ###
    globalVertexList = addVertexToGlobalList(vertexList, globalVertexList)
    [globalTriangleIdList, globalTriangleLabelList] = addTriangleIdToGlobalList(vertexList, globalVertexList, triangleList, globalTriangleIdList, globalTriangleLabelList, [labelCurrentModule])
    # the following loop runs over all the basic primitives we have considered in the model
    while not isinstance(geometry,Primitive):
      geometry = geometry.geometry
      ### When the primitive is a cylinder ###
      if isinstance(geometry,Cylinder):
        cyllist.append((botpoint,botpoint+heading*geometry.height,geometry.radius))
        toppoint = botpoint+heading*geometry.height
        rad = geometry.radius
        #print("Cylinder with label:", lstring[id][2], "Bottom point coordinate:", botpoint, "Top point coordinate:", toppoint, "Radius:",rad)
        # Now we store the label and geometry information of the primitive as the following tuple:
        # (primitive label, bottom_x, bottom_y, bottom_z, top_x, top_y, top_z, radius)
        primitiveLabel = [1] # the label for cylinder is given as '1'
        geomInfoList.append(primitiveLabel)
        [bot_x,bot_y,bot_z] = extractCoord(botpoint) #bottom point
        l = len(geomInfoList)
        geomInfoList[l-1].append(bot_x)
        geomInfoList[l-1].append(bot_y)
        geomInfoList[l-1].append(bot_z)
        [top_x,top_y,top_z] = extractCoord(toppoint) #top point
        geomInfoList[l-1].append(top_x)
        geomInfoList[l-1].append(top_y)
        geomInfoList[l-1].append(top_z)
        geomInfoList[l-1].append(rad) #radius
      ### When the primitive is a frustum ###
      elif isinstance(geometry,Frustum):
        frustumTopPt = botpoint+heading*geometry.height
        frustumRad = geometry.radius
        taperFactor = geometry.taper
        topRad = frustumRad * taperFactor
        #print("Frustum with label:", lstring[id][2], "Bottom point coordinate:", botpoint, "Top point coordinate:", frustumTopPt, "Base radius:", frustumRad, "Top radius:", topRad)
        # Now we store the label and geometry information of the primitive as the following tuple:
        # (primitive label, bottom_x, bottom_y, bottom_z, top_x, top_y, top_z, base radius, top radius)
        primitiveLabel = [2] # the label for frustum is given as '2'
        geomInfoList.append(primitiveLabel)
        [bot_x,bot_y,bot_z] = extractCoord(botpoint) #bottom point
        l = len(geomInfoList)
        geomInfoList[l-1].append(bot_x)
        geomInfoList[l-1].append(bot_y)
        geomInfoList[l-1].append(bot_z)
        [top_x,top_y,top_z] = extractCoord(frustumTopPt) #top point
        geomInfoList[l-1].append(top_x)
        geomInfoList[l-1].append(top_y)
        geomInfoList[l-1].append(top_z)
        geomInfoList[l-1].append(frustumRad) #base radius
        geomInfoList[l-1].append(topRad) #top radius
      ### When the primitive is a sphere ###
      elif isinstance(geometry,Sphere):
        sphereRad = geometry.radius
        #print("Sphere with label:", lstring[id][1], "Radius:", sphereRad)
        # Now we store the label and geometry information of the primitive as the following tuple:
        # (primitive label, sphere radius)
        #So the tuple contains: (primitive label, sphere radius)
        primitiveLabel = [3] # the label for sphere is given as '3'
        geomInfoList.append(primitiveLabel)
        l = len(geomInfoList)
        geomInfoList[l-1].append(sphereRad)
      elif isinstance(geometry,Translated):
        botpoint = geometry.translation
      elif isinstance(geometry,Oriented):
        heading = cross(geometry.primary, geometry.secondary)
  #print(vertexList), print(triangleList), print(geomInfoList), print(globalVertexList), print(globalTriangleIdList), print(globalTriangleLabelList)
  ##### So at this point, we are done with storing all the labelled geometry primitives and the labelled vertices of the coarse mesh model #####
  ##### Next, we will do the point sampling to generate points on the surface of the model. #####
  
  ######################## Basic point sampler ########################

  ### Generate exactly totalNumberOfResampledPts number of points ###
  finalSampledPoints = []
  finalRandomPointLabels = []
  totalSampledPointsSoFar = 0
  initialPointRequirement = totalNumberOfResampledPts
  while(totalNumberOfResampledPts != totalSampledPointsSoFar):
    randomPointLabels = []
    randomTriangleList = selectRandomTriangle(globalTriangleIdList, globalVertexList, initialPointRequirement) # stores a list of random triangles with 'totalNumberOfResampledPts' number of elements. Next, we will sample one point per triangle to generate the point cloud
    [newSampledPoints, randomPointLabels] = sampleRandomPoints(randomTriangleList, globalTriangleIdList, globalVertexList, initialPointRequirement, globalTriangleLabelList, randomPointLabels) # samples a random point on each triangle in the list 'randomTriangleList'
    [ultimateSampledPoints, ultimateRandomPointLabels] = determineInsideness(geomInfoList, newSampledPoints, randomPointLabels) # perform insideness testing of the generated points & discard the points which are inside any primitive
    currentNumberOfPoints = len(ultimateSampledPoints)
    totalSampledPointsSoFar = totalSampledPointsSoFar + currentNumberOfPoints
    pointDifference = totalNumberOfResampledPts - totalSampledPointsSoFar
    initialPointRequirement = pointDifference
    #finalSampledPoints = ultimateSampledPoints
    #finalRandomPointLabels = ultimateRandomPointLabels
    newPtLen = len(ultimateSampledPoints)
    for l in range(newPtLen):
      finalSampledPoints.append(ultimateSampledPoints[l])
      finalRandomPointLabels.append(ultimateRandomPointLabels[l])
    if(totalSampledPointsSoFar > totalNumberOfResampledPts):
      break 

  [onlyPoints, onlyLabels,finalLabelledPoints] = createLabelledPointForDisplay(finalSampledPoints, finalRandomPointLabels) #this is after insidenss testing
  write2File(pointsWithColor, finalLabelledPoints) # the data format is: x, y, z, r, g, b (each r,g,b combination is unique for a specific label)
  write2File(rawPoints, onlyPoints) # the data format is: x, y, z
  write2File(rawLabels, onlyLabels) # the data format is: label
