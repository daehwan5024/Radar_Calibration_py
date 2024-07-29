import ctypes
from scipy.io import loadmat
from util import *
clib = ctypes.CDLL("./gradient.so")
data = loadmat('./test.mat')

num_radar = data['num_radar'][0][0] + data['num_bottom'][0][0]
distance = data['distMeasured']
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
print(posCalibrated)


clib.gradient.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

posgrad = np.zeros((3, num_radar), dtype=np.float64)
clib.gradient(num_radar, posCalibrated.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), distance.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), posgrad.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
print(posgrad)
