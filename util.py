import numpy as np
import matplotlib.pyplot as plt
import cmath
import math
from itertools import permutations
import time
import ctypes

def pairwiseDist(positions):
    n = np.shape(positions)[1]
    distance = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            distance[i, j] = np.linalg.norm(positions[:,i]-positions[:,j])
    return distance


def getBetter(new1, new2, newIndex, posCalibrated, distance, known):
    known[newIndex] = True

    def rmse_modified(input1, input2):
        assert np.shape(input1) == np.shape(input2)
        error = 0
        num_row = np.shape(input1)[0]
        for i in range(num_row):
            for j in range(num_row):
                if known[i] and known[j]:
                    error += (input1[i, j] - input2[i, j]) ** 2
        
        return error
    
    pos1 = posCalibrated.copy(); pos1[:,newIndex] = new1
    pos2 = posCalibrated.copy(); pos2[:,newIndex] = new2

    e1 = rmse_modified(pairwiseDist(pos1), distance)
    e2 = rmse_modified(pairwiseDist(pos2), distance)
    if e1 < e2:
        return new1
    else:
        return new2


def getTransform(result):
    assert np.shape(result)[0] == 3
    assert np.shape(result)[1] >= 3
    transformMatrix = np.zeros((4,4))
    transformMatrix[4,4] = 1

    translation = np.identity(4)
    translation[0:3,3] = -result[:,0]

    relative_vec = result - result[:,0]
    cosTheta1 = relative_vec[0,1]/cmath.sqrt(relative_vec[0,1]**2 + relative_vec[1,1]**2)
    sinTheta1 = -relative_vec[1,1]/cmath.sqrt(relative_vec[0,1]**2 + relative_vec[1,1]**2)
    cosTheta2 = cmath.sqrt(relative_vec[0,1]**2 + relative_vec[1,1]**2) / cmath.sqrt(np.linalg.norm(relative_vec[:,1]))
    sinTheta2 = relative_vec[2,1]/cmath.sqrt(np.linalg.norm(relative_vec[:,1]))
    rotation_t = np.array([[cosTheta2, 0, sinTheta2], [0, 1, 0], [-1*sinTheta2, 0, cosTheta2]]) * np.array([[cosTheta1, -1*sinTheta1, 0], [sinTheta1, cosTheta1, 0], [0, 0, 1]])
    pos_t = rotation_t*relative_vec[:,2]
    cosTheta3 = pos_t[1]/cmath.sqrt(pos_t[1]**2 + pos_t[2]**2)
    sinTheta3 = pos_t[2]/cmath.sqrt(pos_t[1]**2 + pos_t[2]**2)

    rotation = np.array([[1, 0, 0], [0, cosTheta3, -1*sinTheta3], [0, sinTheta3, cosTheta3]]) *rotation_t
    transformMatrix[1:3,1:3] = rotation
    transformMatrix = transformMatrix*translation
    return transformMatrix


def getTriangle(dist12:float, dist23:float, dist31:float):
    x2 = dist12; x3 = (x2 ** 2 + dist31**2 - dist23**2)/(2*x2); y3 = math.sqrt(dist31**2 - x3**2)
    return x2, x3, y3


def getTriangleList(distance):
    n = np.shape(distance)[1]
    triangleList = np.array([])
    for i in range(n):
        for j in range(i):
            for k in range(j):
                a = distance[i, j]; b = distance[j, k]; c = distance[k, i]; s = (a+b+c)/2
                area = cmath.sqrt(s*(s-a)*(s-b)*(s-c))
                if area.imag != 0:
                    continue
                triangleList = np.append(triangleList, [area.real, k , j, i]).reshape(-1,4)
    print()
    return triangleList[triangleList[:,0].argsort()][::-1]

def getTrilateration(*args):
    if len(args) == 2:
        positions = args[0]; r = args[1]
    elif len(args) == 6:
        positions = np.array([args[0], args[1], args[2]]).transpose
        r = np.array([args[3], args[4], args[5]])
    else:
        print("Wrong input")
        return np.array([1j,1j,1j])
    assert np.shape(r)[0] == 3
    assert np.shape(positions) == (3,3)

    p21 = positions[:,1] - positions[:,0]
    p31 = positions[:,2] - positions[:,0]

    c = np.cross(p21, p31)
    c2 = np.sum(np.square(c))
    u1 = np.cross( ((np.sum(np.square(p21)) + r[0]**2 - r[1]**2)*p31 - (np.sum(np.square(p31)) + r[0]**2 - r[2]**2)*p21)/2, c )/c2
    v = cmath.sqrt(r[0]**2 - np.sum(np.square(u1)))*c/cmath.sqrt(c2)
    return positions[:,0] + u1 + v


def calibrationTriangleSize(distance, num_radar):
    if num_radar < 3:
        print("Need at least 3 radars")
    posCalibrated = np.zeros((3, num_radar))
    triangleList = getTriangleList(distance)

    radar1 = int(triangleList[0,1])
    radar2 = int(triangleList[0,2])
    radar3 = int(triangleList[0,3])

    x2, x3, y3 = getTriangle(distance[radar1, radar2], distance[radar2, radar3], distance[radar3, radar1])
    known = [False for i in range(num_radar)]
    known[radar1] = True

    posCalibrated[0, radar2] = x2; known[radar2] = True
    posCalibrated[0, radar3] = x3; posCalibrated[1, radar3] = y3; known[radar3] = True
    
    triangleListIndex = 0
    while not(all(known)):
        for target_radar in range(num_radar):
            if known[target_radar]:
                continue
            pos1 = getTrilateration(posCalibrated[:,[radar1, radar2, radar3]], [distance[target_radar, radar1], distance[target_radar, radar2], distance[target_radar, radar3]])
            if np.any(pos1.imag != 0):
                continue
            pos2 = getTrilateration(posCalibrated[:,[radar1, radar3, radar2]], [distance[target_radar, radar1], distance[target_radar, radar3], distance[target_radar, radar2]])
            posCalibrated[:,target_radar] = getBetter(pos1, pos2, target_radar, posCalibrated, distance, known)
            known[target_radar] = True
        triangleFound = False
        while triangleListIndex < np.shape(triangleList)[0]-1:
            triangleListIndex += 1
            radar1 = int(triangleList[triangleListIndex, 1]); radar2 = int(triangleList[triangleListIndex, 2]); radar3 = int(triangleList[triangleListIndex, 3])
            if known[radar1] and known[radar2] and known[radar3]:
                triangleFound = True
                break
        if not(triangleFound):
            print("Data can't be calibrated")
            break
    # C library for gradient descent
    grad_lib = ctypes.CDLL("./gradient.so")
    grad_lib.gradient.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
    result = np.zeros((3, num_radar), dtype=np.float64)
    grad_lib.gradient(num_radar, posCalibrated.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), distance.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), result.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
    return result