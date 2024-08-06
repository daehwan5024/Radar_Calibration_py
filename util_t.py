from util import *


def getTransform(input1:np.ndarray, input2:np.ndarray):
    assert(input1.shape == input2.shape)
    n = input1.shape[1]

    cm1 = np.average(input1, axis=1)
    cm2 = np.average(input2, axis=1)
    H = np.zeros((3,3))
    for i in range(n):
        H += np.matmul(np.reshape(input1[:,i] - cm1, (3,1)), np.reshape(input2[:,i]-cm2, (1,3)))/n
    U, S, Vh = np.linalg.svd(H)
    R = np.matmul(Vh.T, U.T)
    T = cm2 - np.matmul(R, cm1)
    return R, T



def difference(input1:np.ndarray, input2:np.ndarray):
    if np.any(np.isnan(input1)) or np.any(input1 == np.inf) or np.any(np.isnan(input2)) or np.any(input2 == np.inf):
        return np.inf
    R, T = getTransform(input1, input2)
    input1_t = np.matmul(R, input1) + np.reshape(T, (3, 1))
    diff = np.sqrt(np.sum(np.square(input1_t - input2), axis=0))
    return np.average(diff)

def addNoise(real):
    noise = np.zeros(real.shape)
    for i in range(noise.shape[0]):
        for j in range(noise.shape[1]):
            noise_t = np.random.normal(0,1/30)
            noise[i, j] = real[i, j] + noise_t
            noise[j, i] = noise[i, j]
    return noise


def addNoise2(real, num_bottom):
    noise = np.zeros(real.shape)
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