### This file contains helper functions for the point sampler ###
### Author: Ayan Chaudhury (ayanchaudhury.cs@gmail.com) ###
### INRIA team MOSAIC ###
### Updated: August 2021 ###

from random import seed, random, randint, uniform, gauss
from numpy import arange
from math import *
import numpy as np 


# Extract floating point numbers from Vec3 format
def extractCoord(vec3coord):
  x = vec3coord[0]
  y = vec3coord[1]
  z = vec3coord[2]
  return x,y,z

# Computes the set of indices of vertices that form the triangles
def obtainVertexList(pointlist):
  vertexlist = []
  totalVertices = len(pointlist) # get the no. of triangles in the primitive
  for i in range(totalVertices):
    coord = pointlist[i]
    [x,y,z] = extractCoord(coord)
    #Store the vertex coordinates to vertexlist
    vertexlist.append([x])
    l = len(vertexlist)
    vertexlist[l-1].append(y)
    vertexlist[l-1].append(z)
  return vertexlist


# Extracts the vertices corresponding to each triangle
def obtainTriangleIdxList(idxList):
  triangleList = []
  totalTriangles = len(idxList)
  for i in range(totalTriangles):
    triIndices = idxList[i]
    [v1,v2,v3] = extractCoord(triIndices)
    triangleList.append([v1])
    l = len(triangleList)
    triangleList[l-1].append(v2)
    triangleList[l-1].append(v3)
  return triangleList


# Local triangle vertices are added to the global list
def addVertexToGlobalList(localVertexList, globalVertexList):
  localLen = len(localVertexList)
  for i in range(localLen):
    vertexExists = localVertexList[i] in globalVertexList
    if (vertexExists == False):
      globalVertexList.append(localVertexList[i])
  return globalVertexList


# Local triangle id's are  added to the global list 
def addTriangleIdToGlobalList(localVertexList, globalVertexList, localTriangleIdList, globalTriangleIdList, globalTriangleLabelList, currentLabel):
  totalTriangles = len(localTriangleIdList)
  totalLocalVertex = len(localVertexList)
  totalGlobalVertex = len(globalVertexList)
  for i in range(totalTriangles):
    currentTriangle = localTriangleIdList[i] #is a list
    v1_local_id = currentTriangle[0] #is a number
    v2_local_id = currentTriangle[1]
    v3_local_id = currentTriangle[2]
    v1_coord_local = localVertexList[v1_local_id] #is a list
    v2_coord_local = localVertexList[v2_local_id]
    v3_coord_local = localVertexList[v3_local_id]
    v1_idx_Global = globalVertexList.index(v1_coord_local)
    v2_idx_Global = globalVertexList.index(v2_coord_local)
    v3_idx_Global = globalVertexList.index(v3_coord_local)
    currentTriangleGlobalId = [v1_idx_Global, v2_idx_Global, v3_idx_Global]
    globalTriangleIdList.append(currentTriangleGlobalId)
    globalTriangleLabelList.append(currentLabel) # add the triangle label
  return globalTriangleIdList, globalTriangleLabelList
  

def addTriangleIdToGlobalList_new(localVertexList, globalVertexList, localTriangleIdList, globalTriangleIdList, globalTriangleLabelList, currentLabel):
  totalTriangles = len(localTriangleIdList)
  totalLocalVertex = len(localVertexList)
  totalGlobalVertex = len(globalVertexList)	
  LVL = np.array(localVertexList)
  GVL = np.array(globalVertexList)
  LTIL = np.array(localTriangleIdList)
  for i in range(totalTriangles):
    """
    currentTriangle = localTriangleIdList[i] #is a list
    v1_local_id = currentTriangle[0] #is a number
    v2_local_id = currentTriangle[1]
    v3_local_id = currentTriangle[2]
    v1_coord_local = localVertexList[v1_local_id] #is a list
    v2_coord_local = localVertexList[v2_local_id]
    v3_coord_local = localVertexList[v3_local_id]
    v1_idx_Global = globalVertexList.index(v1_coord_local)
    v2_idx_Global = globalVertexList.index(v2_coord_local)
    v3_idx_Global = globalVertexList.index(v3_coord_local)
    currentTriangleGlobalId = [v1_idx_Global, v2_idx_Global, v3_idx_Global]
    """
    
    #s0 = time.time()
    #currentTriangleGlobalId = [globalVertexList.index(localVertexList[localTriangleIdList[i][0]]), 
                               #globalVertexList.index(localVertexList[localTriangleIdList[i][1]]),
                               #globalVertexList.index(localVertexList[localTriangleIdList[i][2]])]
    #e0 = time.time()
    #print("currentTriangleGlobalId",e0-s0)

    #s_1 = time.time()
    currentTriangleGlobalId_new = [np.where(GVL == LVL[LTIL[i][0]])[0][0],np.where(GVL == LVL[LTIL[i][1]])[0][0],np.where(GVL == LVL[LTIL[i][2]])[0][0]]
    #e_1 = time.time()
    #print("currentTriangleGlobalId_new",e_1-s_1)
    #s1 = time.time()
    globalTriangleIdList.append(currentTriangleGlobalId_new)
    #e1 = time.time()
    #print("globalTriangleIdList", e1-s1)
    #s2 = time.time()
    globalTriangleLabelList.append(currentLabel) # add the triangle label
    #e2 = time.time()
    #print("globalTriangleLabelList", e2-s2)
  return globalTriangleIdList, globalTriangleLabelList



# Write the given list to a file
def write2File(myfilename, mylist):
  import csv
  with open(myfilename, 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(mylist)
    

# Based on the camera position, the distance factor is computed for each triangle. The center of mass is
# chosen as the representative point inside each triangle (although that is not a good idea for big triangles,
# and other types of strategies to have a gradient effect inside each triangle will be better). The function
# returns the distances in the form of probabilties.
def computeDistanceFactor(vertices_1, vertices_2, vertices_3, cameraPosition):
  #cameraPosition = np.asarray([73.0, -69.0, 31.5])
  #cameraPosition = np.asarray([0.0, 0.0, 0.0]) # use custom camera position according to the need of the application
  midpoints = (vertices_1 + vertices_2 + vertices_3) / 3
  distances = np.linalg.norm((cameraPosition - midpoints), axis = 1)
  maxdist = max(distances)
  mindist = min(distances)
  distances = (distances - mindist) / (maxdist - mindist)
  distances = 1 - distances ### small distances have high score, long distances have low score ###
  return distances
    


# This function computes the number of points to be sampled in each triangle. Initially the number of points per
# square unit area is computed, which is multiplied by the area of the triangle under consideration. So that gives
# the number of points to be sampled for uniform sampling case. Since we aim at having a distance factor, the factor
# is weighted by a distance probability - small distances yield large weightage, and big distances yield small weightage.
# The ceil() calculations are done because in many cases there are many tiny triabgles and the total number of estimated
# points inside the triangles are computed as < 1.0. Performing ceil() operation prevents us in having empty triangles.
# PS- the number of sampled points should be specified as large in these cases, then only we can see the distance effect.
def distanceSampledTriangles(triangleIdList, distanceList, areaList, totalArea, meanPoints):
  from math import floor, ceil, exp
  newTriangleList = []
  perSqAreaPoints_uniform = ceil(meanPoints / totalArea)
  totalTriangles = len(triangleIdList)
  for i in range(totalTriangles):
    currentArea = areaList[i]
    currentDistance = distanceList[i]
    perSqAreaPoints_new = int(ceil(perSqAreaPoints_uniform * currentArea * currentDistance * currentDistance)) #square distance function
    #perSqAreaPoints_new = int(ceil(perSqAreaPoints_uniform * currentArea * exp(-currentDistance))) # exponential distance function
    for j in range(perSqAreaPoints_new):
      newTriangleList.append(i)
  npNewTriangleList = np.asarray(newTriangleList)
  return npNewTriangleList



# Triangle selection in advanced point sampler where the distance effect is modelled. Triangles near the camera are more
# frequently selected than the triangles which are far away. 
def selectRandomTriangleWithDistanceEffect(triangleIdList, triangleVertexList, totalNumberOfResampledPts, cameraPosition):
  v1 = []
  v2 = []
  v3 = []
  totalTriangles = len(triangleIdList)
  for i in range(totalTriangles):
    currentTriangle = triangleIdList[i]
    v1_local_id = currentTriangle[0]
    v2_local_id = currentTriangle[1]
    v3_local_id = currentTriangle[2]
    v1_coordinate = triangleVertexList[v1_local_id]
    v2_coordinate = triangleVertexList[v2_local_id]
    v3_coordinate = triangleVertexList[v3_local_id]
    v1.append(v1_coordinate)
    v2.append(v2_coordinate)
    v3.append(v3_coordinate)
  v1np = np.asarray(v1) # just a data type conversion for the ease of calculations
  v2np = np.asarray(v2)
  v3np = np.asarray(v3)
  allTriangleAreas = 0.5 * np.linalg.norm(np.cross(v2np - v1np, v3np - v1np), axis = 1)
  totalArea = allTriangleAreas.sum() # total area of all the triangles (total surface area)
  distances = computeDistanceFactor(v1np, v2np, v3np, cameraPosition) # close points to the camera will have low value
  newSampledTriangles = distanceSampledTriangles(triangleIdList, distances, allTriangleAreas, totalArea, totalNumberOfResampledPts)
  return newSampledTriangles


# Random triangle selection in basic point sampler. Among a list of triangles, random selection is performed based on the
# probability of triangle area. This allows us not to over-sample from areas having large number of small triangles.
def selectRandomTriangle(triangleIdList, triangleVertexList, totalNumberOfResampledPts):
  v1 = []
  v2 = []
  v3 = []
  totalTriangles = len(triangleIdList)
  for i in range(totalTriangles):
    currentTriangle = triangleIdList[i]
    v1_local_id = currentTriangle[0]
    v2_local_id = currentTriangle[1]
    v3_local_id = currentTriangle[2]
    v1_coordinate = triangleVertexList[v1_local_id]
    v2_coordinate = triangleVertexList[v2_local_id]
    v3_coordinate = triangleVertexList[v3_local_id]
    v1.append(v1_coordinate)
    v2.append(v2_coordinate)
    v3.append(v3_coordinate)
  v1np = np.asarray(v1) # just a data type conversion for the ease of calculations
  v2np = np.asarray(v2)
  v3np = np.asarray(v3)
  allTriangleAreas = 0.5 * np.linalg.norm(np.cross(v2np - v1np, v3np - v1np), axis = 1)
  weightedAreas = allTriangleAreas / allTriangleAreas.sum()
  randomTriangleList = np.random.choice(range(totalTriangles), size = totalNumberOfResampledPts, p = weightedAreas)
  return randomTriangleList
  

# Randomly chooses 3 variables in the range [0,1]
# such that their sum equals to 1 
def generateAlphaBetaGamma():
  alpha = np.random.rand(1)
  beta = np.random.rand(1)
  gamma = np.random.rand(1)
  totalSum = alpha + beta + gamma
  newAlpha = alpha / totalSum
  newBeta = beta / totalSum
  newGamma = gamma / totalSum
  return newAlpha, newBeta, newGamma
  

# Given a list of triangles, this function generates one point inside each triangle in a random position,
# and returns sampled points along with its label obtained from the label of the triangles in which the points are sampled from
def sampleRandomPoints(randomTriangleIdList, globalTriangleIdList, globalTriangleVertexList, totalNumberOfResampledPts, globalTriangleLabelList, randomPointLabels):
  allSampledPoints = []
  totalNumberOfResampledPts = randomTriangleIdList.shape[0]
  for i in range(totalNumberOfResampledPts):
    currentRandomTriangle = randomTriangleIdList[i]
    currentLabel = globalTriangleLabelList[currentRandomTriangle][0]
    currentTriangleVertexIds = globalTriangleIdList[currentRandomTriangle] #a list
    v1_id = currentTriangleVertexIds[0]
    v2_id = currentTriangleVertexIds[1]
    v3_id = currentTriangleVertexIds[2]
    v1_corrd = globalTriangleVertexList[v1_id] #a list
    v2_corrd = globalTriangleVertexList[v2_id]
    v3_corrd = globalTriangleVertexList[v3_id]
    [alpha, beta, gamma] = generateAlphaBetaGamma()
    sampledPoint = [sum(x) for x in zip([i * alpha for i in v1_corrd],[i * beta for i in v2_corrd],[i * gamma for i in v3_corrd])]
    sampledPoint_x = sampledPoint[0][0] #because these are in the form of list of list
    sampledPoint_y = sampledPoint[1][0]
    sampledPoint_z = sampledPoint[2][0]
    newPoint = [sampledPoint_x, sampledPoint_y, sampledPoint_z]
    allSampledPoints.append(newPoint)
    randomPointLabels.append(currentLabel)
  return allSampledPoints, randomPointLabels


# Returns unique elements of a list
def distinctElements(list1): 
  distinct_list = []
  for x in list1:
    if x not in distinct_list:
      distinct_list.append(x)
  return distinct_list


# Given a list of labels, this function performs relabelling sequentially starting
# from 1. So if a given list of label is [30, 31, 37, 37, 37, 42, 42, 51, 51, 51],
# then the new labelling is obtained as, [1, 2, 3, 3, 3, 4, 4, 5, 5, 5]
def refineLabels(a):
  newLabelList = []
  b = distinctElements(a)
  b.sort()
  totalLabels = len(b)
  labelSeq = np.linspace(1, totalLabels, totalLabels)
  labelSeq = [int(i) for i in labelSeq]
  for i in range(len(a)):
    for j in range(len(b)):
        if (a[i] == b[j]):
            newLabelList.append(labelSeq[j])
  return newLabelList


# This function takes as argument the list of points and labels, and returns
# 3 types of formats: (x,y,z,r,g,b), (x,y,z), (labels). The r,g,b triplets are
# generated uniquely for different labels
def createLabelledPointForDisplay(newSampledPoints, randomPointLabels):
  refinedLabels = refineLabels(randomPointLabels)
  allLabelledPoints = []
  onlyPoints = []
  onlyLabels = []
  totalPoints = len(newSampledPoints)
  #We keep the first 3 label colours as r, g, b & the rest are random colours
  color1 = [255, 0, 0] + list(np.random.choice(range(256), size=2000)) #label max up to 2000
  color2 = [0, 255, 0] + list(np.random.choice(range(256), size=2000))
  color3 = [0, 0, 255] + list(np.random.choice(range(256), size=2000))
  for i in range(totalPoints):
    currentPoint = newSampledPoints[i]
    currentLabel = refinedLabels[i]
    color = [color1[currentLabel-1], color2[currentLabel-1], color3[currentLabel-1]] # labels start from '1', array idx from '0'
    currentLabelledPoint = currentPoint + color
    allLabelledPoints.append(currentLabelledPoint)
    onlyPoints.append(currentPoint)
    onlyLabels.append([currentLabel])
  return onlyPoints, onlyLabels, allLabelledPoints
  


# This is a simple trick used for the ease of floating point calculations,
# especially to handle rounding off problems
def applyFloatingPointTrick(n1, n2, n):
  from math import floor, ceil
  if (0.1 <= n < 10.0):
    n1 = floor(n1 * 10) / 10.0
    n2 = ceil(n2 * 10) / 10.0
  elif(0.01 <= n < 0.1):
    n1 = floor(n1 * 100) / 100.0
    n2 = ceil(n2 * 100) / 100.0
  elif(0.001 <= n < 0.01):
    n1 = floor(n1 * 1000) / 1000.0
    n2 = ceil(n2 * 1000) / 1000.0
  return n1, n2


# Given a list of geometric primitives in a model, a list of points and their corresponding labels,
# this function checks which points are falling inside any of the primitives. These points are then
# discarded and rest of the points along with their labels are returned
def determineInsideness(geomInfoList, allPointsList, allPointLabels):
  from math import floor, ceil
  selectedPointsList = []
  selectedPointsLabels = []
  totalPoints = len(allPointsList)
  totalPrimitives = len(geomInfoList)
  for i in range(totalPoints):
    currentPoint = np.asarray(allPointsList[i])
    insidenessFlag = False
    for j in range(totalPrimitives):
      currentPrimitive = geomInfoList[j]
      #cylinder primitive (we assigned it as label '1' in the End() function)
      if(currentPrimitive[0] == 1):
        bottomPoint = np.asarray([currentPrimitive[1], currentPrimitive[2], currentPrimitive[3]])
        topPoint = np.asarray([currentPrimitive[4], currentPrimitive[5], currentPrimitive[6]])
        rad = currentPrimitive[7]
        vec = topPoint - bottomPoint
        c = rad * np.linalg.norm(vec) 
        condition1 = np.dot(currentPoint - bottomPoint, vec) >= 0
        condition2 = np.dot(currentPoint - topPoint, vec) <= 0
        condition3 = np.linalg.norm(np.cross(currentPoint - bottomPoint, vec))
        minimum_number = min(c, condition3)
        [c, condition3] = applyFloatingPointTrick(c, condition3, minimum_number)
        z = (condition1 and condition2 and condition3 < c)
        #if z returns true, that means the point is inside the cylinder
        if(z == True):
          insidenessFlag = True
      #frustum primitive (we assigned it as label '2' in the End() function)
      elif(currentPrimitive[0] == 2):
        bottomPoint = np.asarray([currentPrimitive[1], currentPrimitive[2], currentPrimitive[3]])
        topPoint = np.asarray([currentPrimitive[4], currentPrimitive[5], currentPrimitive[6]])
        bottomRad = currentPrimitive[7]
        topRad = currentPrimitive[8]
        pointToAxisVector = currentPoint - bottomPoint
        axisVector = topPoint - bottomPoint
        condition1 = np.dot(currentPoint - bottomPoint, axisVector) >= 0
        condition2 = np.dot(currentPoint - topPoint, axisVector) <= 0
        projectedPoint = bottomPoint + np.dot(pointToAxisVector, axisVector) / np.dot(axisVector, axisVector) * axisVector
        factor1 = np.linalg.norm(projectedPoint - bottomPoint) / np.linalg.norm(bottomPoint - topPoint) * bottomRad
        factor2 = np.linalg.norm(projectedPoint - topPoint) / np.linalg.norm(bottomPoint - topPoint) * topRad
        currentRadius = factor1 + factor2
        currentDistance = np.linalg.norm(projectedPoint - currentPoint)
        minimum_number = min(currentRadius, currentDistance)
        [currentRadius, currentDistance] = applyFloatingPointTrick(currentRadius, currentDistance, minimum_number)
        #if the distance is < frustum radius at that point, then it is inside
        if (condition1 and condition2 and currentDistance < currentRadius):
          insidenessFlag = True
      # If there is sphere or other primitives in the model, then put it here as another condition(s)
    if (insidenessFlag == False):
      selectedPointsList.append(allPointsList[i])
      selectedPointsLabels.append(allPointLabels[i])
  return selectedPointsList, selectedPointsLabels
  

# Modelling plain noise. Given a list of points, corresponding labels, and all the geometric
# primitives of the model, this function applies random normal distribution to the point position.
# Simultaneously it is also checked if the noisy point lies inside any primitive: this is performed
# for finite number of trials (here it is chosen as 5), out of which one trial is assumed to generate
# noisy point which does not lie inside a primitive. This is a very naive and simple strategy which 
# works fine. However, other alternatives can also be modelled (or simply the number of trials can be
# increased to have higher chances). The function returns noisy points and their labels.
def convertToNoisyData(geomInfo, points, labels):
  noisyPoints = []
  noisyPointLabels = []
  sigma = 0.07
  n = len(points)
  for i in range(n):
    for j in range(5):
      currentPoint = np.asarray(points[i])
      x = np.random.normal(currentPoint[0], sigma)
      y = np.random.normal(currentPoint[1], sigma)
      z = np.random.normal(currentPoint[2], sigma)
      noisyPoint = [[x, y, z]]
      currentLabel = [labels[i]]
      [insideTestedPts, insideTestedLabels] = determineInsideness(geomInfo, noisyPoint, currentLabel)
      if(len(insideTestedPts) > 0):
        noisyPoints.append(insideTestedPts[0])
        noisyPointLabels.append(insideTestedLabels[0])
        break
  return noisyPoints, noisyPointLabels


# Modelling sensor noise. As a point gets further away from the camera, the noise increases. The insideness
# is tested following the similar strategy as done in plain noise modelling. The function returns noisy points
# and their labels.
def convertToSensorNoisyData(geomInfo, points, labels, cameraPosition):
  cameraPosition = np.asarray([0.0, 0.0, 0.0]) # use custom camera position here
  noisyPoints = []
  noisyPointLabels = []
  maxSigma = 0.1 # maximum sigma occus to the furthest point(s)
  distances = np.linalg.norm((cameraPosition - points), axis = 1)
  maxdist = max(distances)
  mindist = min(distances)
  distances = (distances - mindist) / (maxdist - mindist) # normalize distance in the range [0,1]
  n = len(points)
  for i in range(n):
    for j in range(5):
      currentPoint = np.asarray(points[i])
      currentSigma = maxSigma * (distances[i]) # small distances have lower effect than large distances
      x = np.random.normal(currentPoint[0], currentSigma)
      y = np.random.normal(currentPoint[1], currentSigma)
      z = np.random.normal(currentPoint[2], currentSigma)
      noisyPoint = [[x, y, z]]
      currentLabel = [labels[i]]
      [insideTestedPts, insideTestedLabels] = determineInsideness(geomInfo, noisyPoint, currentLabel)
      if(len(insideTestedPts) > 0):
        noisyPoints.append(insideTestedPts[0])
        noisyPointLabels.append(insideTestedLabels[0])
        break
  return noisyPoints, noisyPointLabels
