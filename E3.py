import numpy as np
import matplotlib.pyplot as plt
import copy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from util_t import *

np.set_printoptions(linewidth=1000)
def rect_line_intersect(rect, line):
    a, b, c = line[1][0] - line[0][0], line[1][1] - line[0][1], line[1][2] - line[0][2]
    x, y, z = 0, 0, 0
    if (rect[0][0] == rect[1][0]) and (rect[1][0] == rect[2][0]) and (rect[2][0]==rect[3][0]):
        try:
            x = rect[0][0]
            y = line[0][1] + b*(x-line[0][0])/a
            z = line[0][2] + c*(x-line[0][0])/a
        except:
            x, y, z = math.nan, math.nan, math.nan
        # parallel to y-z plane
    elif (rect[0][1] == rect[1][1]) and (rect[1][1] == rect[2][1]) and (rect[2][1]==rect[3][1]):
        try:
            y = rect[0][1]
            x = line[0][0] + a*(y-line[0][1])/b
            z = line[0][2] + c*(y-line[0][1])/b
        except:
            x, y, z = math.nan, math.nan, math.nan
        # parallel to x-z plane
    elif (rect[0][2] == rect[1][2]) and (rect[1][2] == rect[2][2]) and (rect[2][2]==rect[3][2]):
        try:
            z = rect[0][2]
            x = line[0][0] + a*(z-line[0][2])/c
            y = line[0][1] + b*(z-line[0][2])/c
        except:
            x, y, z = math.nan, math.nan, math.nan
        # parallel to x-y plane
    else:
        assert(False)
    
    line_xlim = [min(line[0][0], line[1][0]), max(line[0][0], line[1][0])]
    line_ylim = [min(line[0][1], line[1][1]), max(line[0][1], line[1][1])]
    line_zlim = [min(line[0][2], line[1][2]), max(line[0][2], line[1][2])]

    rect_xlim = [min(rect[0][0], rect[1][0], rect[2][0], rect[3][0]), max(rect[0][0], rect[1][0], rect[2][0], rect[3][0])]
    rect_ylim = [min(rect[0][1], rect[1][1], rect[2][1], rect[3][1]), max(rect[0][1], rect[1][1], rect[2][1], rect[3][1])]
    rect_zlim = [min(rect[0][2], rect[1][2], rect[2][2], rect[3][2]), max(rect[0][2], rect[1][2], rect[2][2], rect[3][2])]

    if x>=rect_xlim[0] and x<=rect_xlim[1] and y>=rect_ylim[0] and y<=rect_ylim[1] and z>=rect_zlim[0] and z<=rect_zlim[1]:
        if x>=line_xlim[0] and x<=line_xlim[1]and y>=line_ylim[0] and y<=line_ylim[1] and z>=line_zlim[0] and z<=line_zlim[1]:
            return True
    return False

# Check if two points are in LOS
def NLOS(shape, point1, point2):
    for rect in shape:
        if rect_line_intersect(rect, [point1, point2]):
            return True
    return False

# return 4 faces of cuboid
def getPillar(left_bt, width=1, depth=1, height=5):
    p1 = copy.deepcopy(left_bt)
    p2 = copy.deepcopy(p1); p2[0] += width
    p3 = copy.deepcopy(p2); p3[1] += depth
    p4 = copy.deepcopy(p3); p4[0] -= width
    p5 = copy.deepcopy(p1); p5[2] = height
    p6 = copy.deepcopy(p2); p6[2] = height
    p7 = copy.deepcopy(p3); p7[2] = height
    p8 = copy.deepcopy(p4); p8[2] = height
    return [[p1, p2, p6, p5], [p2, p3, p7, p6], [p3, p4, p8, p7], [p4, p1, p5, p8]]

groundTruth = np.array([[8.9603, 8.9399, 7.922, 3.8117, -2.9476, -8.243, -8.4543], [1.8411, -3.9836, -4.2672, -7.414, -7.4861, -4.157, -0.1732], [4.068, 4.068, 2.282, 2.396, 2.396, 2.282, 1.692]])
pillar_height_short = 2.5

# left bottom of each pillar
pillar1_point = [-3.742, 1.919, 0.001]
pillar2_point = [3.458, 1.919, 0.001]
pillar3_point = [3.458, -5.181, 0.001]
pillar4_point = [-3.742, -5.181, 0.001]
# lower ceiling near the exit
ceiling_point =[[[-10, -4, pillar_height_short], [10, -4, pillar_height_short], [10, -8, pillar_height_short], [-10, -8, pillar_height_short]]]

ceiling = Poly3DCollection(ceiling_point, alpha=0.2)
pillar1 = Poly3DCollection(getPillar(pillar1_point), alpha=0.2)
pillar2 = Poly3DCollection(getPillar(pillar2_point), alpha=0.2)
pillar3 = Poly3DCollection(getPillar(pillar3_point, height=pillar_height_short), alpha=0.2)
pillar4 = Poly3DCollection(getPillar(pillar4_point, height=pillar_height_short), alpha=0.2)

# add Triangle at bottom
centerPos = np.reshape(np.array([0,-3,0]), (3, 1))
theta = np.random.rand() * 2 * math.pi
rotationMatrix = np.array([[math.cos(theta), -1*math.sin(theta), 0], [math.sin(theta), math.cos(theta), 0],[0,0,1]])
posBottom = np.matmul(rotationMatrix, np.array([[0, -0.5, 0.5], [math.sqrt(1/3), -1/(2*math.sqrt(3)), -1/(2*math.sqrt(3))], [0,0,0]])) + centerPos
measure_point = np.hstack([posBottom, groundTruth])

# Calculate distance and add noise
distAbsolute = pairwiseDist(measure_point)
for i in range(distAbsolute.shape[0]):
    for j in range(distAbsolute.shape[1]):
        if i==j:
            continue
        if NLOS(getPillar(pillar1_point)+getPillar(pillar2_point)+getPillar(pillar3_point)+getPillar(pillar4_point)+ceiling_point, measure_point[:,i], measure_point[:,j]):
            distAbsolute[i, j] = np.nan
            distAbsolute[j, i] = np.nan
distMeasured = addNoise2(distAbsolute, 3)

# Calibrate
pos_Cal = calibrationTriangleSize(distMeasured, distAbsolute.shape[1])
print(difference(pos_Cal, measure_point))

#plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')

ax.add_collection3d(ceiling)
ax.add_collection3d(pillar1)
ax.add_collection3d(pillar2)
ax.add_collection3d(pillar3)
ax.add_collection3d(pillar4)
R, T = getTransform(pos_Cal, measure_point)
pos_t = np.matmul(R, pos_Cal) + np.reshape(T, (3,1))
diff_arr = pos_t - measure_point
print(diff_arr)
ax.scatter(measure_point[0,:], measure_point[1,:], measure_point[2,:], c='r', marker='.')
ax.scatter(pos_t[0,:], pos_t[1,:], pos_t[2,:], c='b', marker='.')
plt.show()