from util import *


def difference(input1:np.ndarray, input2:np.ndarray):
    if input1.shape != input2.shape:
        print("Input size different")
        return
    if input1.shape[0] != 3:
        print("wrong shape")
        return
    if np.shape(input1)[1] < 3:
        print("Need more radar points")
        return
    best = [np.inf, np.inf, np.inf, np.inf]
    for i in range(input1.shape[1]):
        for j in range(input1.shape[1]):
            for k in range(input1.shape[1]):
                if i==j or j==k or k==i:
                    continue
                T1 = getTransform(input1[:,[i, j, k]])
                T2 = getTransform(input2[:,[i, j, k]])
                trans1 = T1*np.vstack([input1, np.ones((1,input1.shape[1]))])
                trans2 = T2*np.vstack([input2, np.ones((1,input2.shape[1]))])

                trans1 = trans1[0:2, :]
                trans2 = trans2[0:2, :]
                d = 0
                trans1_r = np.vstack([trans1[1:2,:], -1*trans1[2,:]])
                if math.sqrt(np.sum(np.square(trans1 - trans2))) < math.sqrt(np.sum(np.square(trans1_r - trans2))):
                    d = math.sqrt(np.sum(np.square(trans1 - trans2)))
                else:
                    d = math.sqrt(np.sum(np.square(trans1_r - trans2)))
                if d < best[0]:
                    best =[d, k, j, i]
    return best

def addNoise(real):
    noise = np.zeros(real)
    for i in range(noise.shape[0]):
        for j in range(noise.shape[1]):
            noise_t = np.random.normal(0,1/30)
            noise[i, j] = real[i, j] + noise_t
            noise[j, i] = noise[i, j]
    return noise

def addNoise2(real, num_bottom):
    noise = np.zeros(real)
    for i in range(noise.shape[0]):
        for j in range(noise.shape[1]):
            noise_t = 0
            if i<num_bottom and j<num_bottom:
                noise_t = 0
            else:
                noise_t = np.random.normal(0,1/30)
            noise[i, j] = real[i, j] + noise_t
            noise[j, i] = noise[i, j]
    return noise

def radarData():
    num_radar = 8
    posAbsolute = np.random.rand(3, num_radar)
    posAbsolute[0:1,:] = posAbsolute[0:1,:] * 20 -10
    posAbsolute[2,:-3] = posAbsolute[2,:-3] + 2.5

    distAbsolute = pairwiseDist(posAbsolute)
    distMeasured = addNoise(distAbsolute)
    return num_radar, posAbsolute, distAbsolute, distMeasured

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
            num_wall = args[3]
    rand_pos = np.random.rand(num_top, 1)*20*num_wall
    if num_top >= num_wall:
        for i in range(num_wall):
            