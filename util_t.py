from util import *


def getTransform(result):
    assert np.shape(result)[0] == 3
    assert np.shape(result)[1] >= 3
    transformMatrix = np.zeros((4,4))
    transformMatrix[3,3] = 1

    translation = np.identity(4)
    translation[0:3,3] = -1*result[:,0]

    relative_vec = result - result[:,0] # problem here
    cosTheta1 = relative_vec[0,1]/math.sqrt(relative_vec[0,1]**2 + relative_vec[1,1]**2)
    sinTheta1 = -relative_vec[1,1]/math.sqrt(relative_vec[0,1]**2 + relative_vec[1,1]**2)
    cosTheta2 = math.sqrt(relative_vec[0,1]**2 + relative_vec[1,1]**2) / math.sqrt(np.linalg.norm(relative_vec[:,1]))
    sinTheta2 = relative_vec[2,1]/math.sqrt(np.linalg.norm(relative_vec[:,1]))
    rotation_t = np.matmul(np.array([[cosTheta2, 0, sinTheta2], [0, 1, 0], [-1*sinTheta2, 0, cosTheta2]]), np.array([[cosTheta1, -1*sinTheta1, 0], [sinTheta1, cosTheta1, 0], [0, 0, 1]]))
    pos_t =np.matmul(rotation_t, relative_vec[:,2])
    cosTheta3 = pos_t[1]/math.sqrt(pos_t[1]**2 + pos_t[2]**2)
    sinTheta3 = pos_t[2]/math.sqrt(pos_t[1]**2 + pos_t[2]**2)

    rotation = np.matmul(np.array([[1, 0, 0], [0, cosTheta3, -1*sinTheta3], [0, sinTheta3, cosTheta3]]), rotation_t)
    transformMatrix[0:3,0:3] = rotation
    transformMatrix = np.matmul(transformMatrix, translation)
    return transformMatrix


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
                trans1 = np.matmul(T1, np.vstack([input1, np.ones((1,input1.shape[1]))]))
                trans2 = np.matmul(T2, np.vstack([input2, np.ones((1,input2.shape[1]))]))

                trans1 = trans1[0:3, :]
                trans2 = trans2[0:3, :]
                d = 0
                trans1_r = np.vstack([trans1[0:2,:], -1*trans1[2,:]])
                if math.sqrt(np.sum(np.square(trans1 - trans2))) < math.sqrt(np.sum(np.square(trans1_r - trans2))):
                    d = math.sqrt(np.sum(np.square(trans1 - trans2)))
                else:
                    d = math.sqrt(np.sum(np.square(trans1_r - trans2)))
                d = d/input1.shape[1]
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
        posBottom = rotationMatrix * np.array([[-0.5, 0.5], [0, 0], [0, 0]]) + centerPos
        posAbsolute = np.hstack([posBottom, posAbsolute])
    elif num_bottom == 3:
        posBottom = rotationMatrix * np.array([[0, -0.5, 0.5], [math.sqrt(1/3), -1/(2*math.sqrt(3)), -1/(2*math.sqrt(3))], [0,0,0]]) + centerPos
        posAbsolute = np.hstack([posBottom, posAbsolute])
    elif num_bottom == 4:
        posBottom = rotationMatrix * [[0.5, 0.5, -0.5, -0.5], [0.5, -0.5, -0.5, 0.5], [0,0,0,0]] + centerPos
        posAbsolute = np.hstack([posBottom, posAbsolute])
    else:
        print("Too many on the bottom")
    
    distAbsolute = pairwiseDist(posAbsolute)
    distMeasured = addNoise2(distAbsolute, num_bottom)
    return num_top, num_bottom, posAbsolute, distAbsolute, distMeasured