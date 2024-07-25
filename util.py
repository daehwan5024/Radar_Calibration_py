import numpy as np
import matplotlib.pyplot as plt
import cmath
from itertools import permutations


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


def getInsertOrder(pdopList, num_radar:int):
    radars = np.arange(0, num_radar)
    result = np.array([])

    for i in range(num_radar):
        for j in range(i):
            for k in range(j):
                temp = np.delete(radars, i)
                temp = np.delete(temp, j)
                temp = np.delete(temp, k)
                for t in permutations(temp):
                    if np.shape(result) == (0,):
                        result = np.array([np.append([k, j, i], t)])
                    else:
                        result = np.append(result, np.array([np.append([k, j, i], t)]), axis=0)
    return result


def getPDOPList(distance):
    num_radar = np.shape(distance)[0]
    dist_nan = np.isnan(distance)
    def posRelative(target, radar1, radar2, radar3):
        if dist_nan[radar1, radar2] or dist_nan[radar1, radar3] or dist_nan(radar1, target) or dist_nan(radar2, radar3) or dist_nan(radar2, target) or dist_nan(radar3, target):
            return np.array([1j, 1j, 1j]), np.array([1j, 1j, 1j]), np.array([1j, 1j, 1j])
        x2, x3, y3 = getTriangle(distance(radar1, radar2), distance(radar2, radar3), distance(radar3, radar1))
        targetPos = getTrilateration([0,0,0], [x2,0,0], [x3,y3,0], distance(target, radar1), distance(target, radar2), distance(target, radar3))
        if not(np.isreal(targetPos)):
            return [1j,1j,1j],[1j,1j,1j],[1j,1j,1j]
        return np.array([0,0,0]) - targetPos, np.array([x2,0,0]) - targetPos, np.array(x3,y3,0) - targetPos
    pdopList = np.array([])
    for i in range(num_radar):
        for j in range(i):
            for k in range(j):
                for radar in range(num_radar):
                    if i==radar or j== radar or k==radar:
                        continue
                    # calculates PDOP assuming that target is at the origin
                    radar1, radar2, radar3 = posRelative(radar, i, j, k)
                    if not(np.isreal(radar1).all()):
                        continue

                    A = np.array([radar1, radar2, radar3]).transpose
                    B = np.square(A)
                    C = np.zeros((3,3))
                    C[1,:] = A[1,:]/cmath.sqrt(np.sum(B[1,:]))
                    C[2,:] = A[2,:]/cmath.sqrt(np.sum(B[2,:]))
                    C[3,:] = A[3,:]/cmath.sqrt(np.sum(B[3,:]))
                    D = np.linalg.inv(C.transpose * C)
                    pdopList = np.append(pdopList, [cmath.sqrt(np.trace(np.square(D))), radar, k, j, i]).reshape(-1,3)
    return np.sort(pdopList, axis=0)


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
    x2 = dist12; x3 = (x2 ** 2 + dist31**2 - dist23**2)/(2*x2); y3 = cmath.sqrt(dist31**2 - x3**2)
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
                triangleList = np.append(triangleList, [area, k , j, i]).reshape(-1,4)
    return np.sort(triangleList, axis=0)[::-1]

def getTrilateration(*args):
    if len(args) == 2:
        r = args[0]; positions = args[1]
    elif len(args) == 6:
        r = np.array([args[0], args[1], args[2]])
        positions = np.array([args[3], args[4], args[5]]).transpose
    else:
        print("Wrong input")
        return np.array([1j,1j,1j])
    assert np.shape(r) == (3,)
    assert np.shape(positions) == (3,3)

    p21 = positions[:,1] - positions[:,0]
    p31 = positions[:,2] - positions[:,0]

    c = np.cross(p21, p31)
    c2 = np.sum(np.square(c))
    u1 = np.cross( ((np.sum(np.square(p21)) + r[0]**2 - r[1]**2)*p31 - (np.sum(np.square(p31)) + r[0]**2 - r[2]**2)*p21)/2, c )/c2
    v = cmath.sqrt(r[0]**2 - np.sum(np.square(u1)))&c/cmath.sqrt(c2)
    return positions[:,1] + u1 + v


def CalibrationPDOP(distance, num_radar):
    if num_radar < 3:
        print("Need at least 3 radars")
    
    pdopList = getPDOPList(distance)
    orders = getInsertOrder(pdopList, num_radar)

def CalibrationTriangleSize(distance, num_radar):
    if num_radar < 3:
        print("Need at least 3 radars")
    triangleList = getTriangleList(distance)

    radar1 = triangleList[0,1]
    radar2 = triangleList[0,2]
    radar3 = triangleList[0,3]

    x2, x3, y3 = getTriangle(distance(radar1, radar2), distance(radar2, radar3), distance(radar3, radar1))
    

