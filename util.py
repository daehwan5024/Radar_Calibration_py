import numpy as np
import matplotlib.pyplot as plt
import math


def pairwiseDist(positions):
    n = np.shape(positions)[1]
    distance = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            distance[i, j] = np.linalg.norm(positions[:,i]-positions[:,j], 2)
    return distance


def getBetter(new1, new2, newIndex, posCalibrated, distance, known):
    known[newIndex] = True

    def rmse_modified(input1, input2):
        assert np.shape(input1) == np.shape(input2)
        error = 0
        num_row, num_col = np.shape(input1)[0]
        for i in range(num_row):
            for j in range(num_row):
                if known(i) and known(j):
                    error += (input1[i, j] - input2[i, j]) ** 2
        
        return error
    
    pos1 = posCalibrated; pos1[:,newIndex] = new1
    pos2 = posCalibrated; pos2[:,newIndex] = new2

    e1 = rmse_modified(pairwiseDist(pos1), distance)
    e2 = rmse_modified(pairwiseDist(pos2), distance)
    if e1 < e2:
        return new1
    else:
        return new2


def getInsertOrder(pdopList, num_radar):
    return None


def getPDOPList(distance):
    return None


def getTransform(result):
    transformMatrix = np.zeros((4,4))
    transformMatrix[4,4] = 1

    translation = np.identity(4)
    translation[1:3,4] = -result[:,1]

    return None


def getTriangle(dist12, dist23, dist31):
    x2 = dist12; x3 = (x2 ** 2 + dist31**2 - dist23**2)/(2*x2); y3 = math.sqrt(dist31**2 - x3**2)
    return x2, x3, y3


def getTrilateration(*args):
    return None
