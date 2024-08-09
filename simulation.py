import math

import numpy as np
import matplotlib.pyplot as plt

from evaluation import getTransform
from calibration import pairwiseDist

# add random noise based on normal distribution
def addNoise(real):
    noise = np.zeros(real.shape)
    for i in range(noise.shape[0]):
        for j in range(i):
            noise_t = np.random.normal(1,1/30)
            noise[i, j] = real[i, j] + noise_t
            noise[j, i] = noise[i, j]
    return noise


# add noise except to tags
# tags should be placed first
def addNoise2(real, num_bottom):
    noise = np.zeros(real.shape)
    for i in range(noise.shape[0]):
        for j in range(i):
            noise_t = 0
            if i<num_bottom and j<num_bottom:
                noise_t = 0
            elif i==j:
                noise_t = 0
            else:
                noise_t = np.random.normal(-0.1,1/30)
            noise[i, j] = real[i, j] + noise_t
            noise[j, i] = noise[i, j]
    return noise

# generates random radar points
def radarData():
    num_radar = 8
    posAbsolute = np.random.rand(3, num_radar)
    posAbsolute[0:1,:] = posAbsolute[0:1,:] * 20 -10
    posAbsolute[2,:-3] = posAbsolute[2,:-3] + 2.5

    distAbsolute = pairwiseDist(posAbsolute)
    distMeasured = addNoise(distAbsolute)
    return num_radar, posAbsolute, distAbsolute, distMeasured

# generates random radar points
# All radars are positioned following the boundary of 20x20 room
def radarData2(*args):
    num_wall = 4
    num_top = 4
    num_bottom = 3
    if len(args) == 1:
        num_top = args[0]
    elif len(args) == 2:
        num_top = args[0]
        num_bottom = args[1]
    elif len(args) == 3:
        num_top = args[0]
        num_bottom = args[1]
        if args[2]>4 or args[2] < 1:
            print("Wrong wall number")
        else:
            num_wall = args[2]
    rand_pos = np.random.rand(num_top, 1)*20*num_wall
    if num_top >= num_wall:
        for i in range(num_wall):
            rand_pos[i] = np.random.rand(1)*20+20*i
    posAbsolute = np.random.rand(3, num_top) +2.5
    for i in range(num_top):
        if rand_pos[i] <= 20:
            posAbsolute[0, i] = rand_pos[i] - 10
            posAbsolute[1, i] = -10
        elif rand_pos[i]<=40:
            posAbsolute[0, i] = 10
            posAbsolute[1, i] = rand_pos[i] - 30
        elif rand_pos[i] <= 60:
            posAbsolute[0, i] = 50 - rand_pos[i]
            posAbsolute[1, i] = 10
        else:
            posAbsolute[0, i] = -10
            posAbsolute[1, i] = 70 - rand_pos[i]

    centerPos = np.random.normal(0, 10/3, (3, 1))
    centerPos[2] = 0

    theta = np.random.rand(1) * 2 * math.pi
    rotationMatrix = np.array([[math.cos(theta), -1*math.sin(theta), 0], [math.sin(theta), math.cos(theta), 0],[0,0,1]])
    if num_bottom == 1:
        posAbsolute = np.hstack([centerPos, posAbsolute])
    elif num_bottom == 2:
        posBottom = np.matmul(rotationMatrix , np.array([[-0.5, 0.5], [0, 0], [0, 0]])) + centerPos
        posAbsolute = np.hstack([posBottom, posAbsolute])
    elif num_bottom == 3:
        posBottom = np.matmul(rotationMatrix, np.array([[0, -0.5, 0.5], [math.sqrt(1/3), -1/(2*math.sqrt(3)), -1/(2*math.sqrt(3))], [0,0,0]])) + centerPos
        posAbsolute = np.hstack([posBottom, posAbsolute])
    elif num_bottom == 4:
        posBottom = np.matmul(rotationMatrix, [[0.5, 0.5, -0.5, -0.5], [0.5, -0.5, -0.5, 0.5], [0,0,0,0]]) + centerPos
        posAbsolute = np.hstack([posBottom, posAbsolute])
    else:
        print("Too many on the bottom")
    
    distAbsolute = pairwiseDist(posAbsolute)
    distMeasured = addNoise2(distAbsolute, num_bottom)
    return num_top, num_bottom, posAbsolute, distAbsolute, distMeasured




