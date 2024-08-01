from util_t import *
from matplotlib import pyplot as plt
from scipy.io import savemat
import time

def noise(real):
    res = np.zeros(real.shape)
    for i in range(real.shape[0]):
        for j in range(i):
            noise_t = 0
            if np.isclose(real[i, j], 1.0):
                noise_t = 0
            else:
                noise_t = np.random.normal(0,1/30)
            res[i, j] = real[i, j] + noise_t
            res[j, i] = res[i, j]
    return res


def generate():
    num_top1, num_bottom1, posAbsolute1, a, a = radarData2(5, 3, 4)
    num_top2, num_bottom2, posAbsolute2, a, a = radarData2(5, 3, 4)
    pairwiseDist(posAbsolute1)
    posAbsolute2[0,:] += 25
    posAbsolute = np.hstack([posAbsolute1, posAbsolute2])
    distAbsolute = pairwiseDist(posAbsolute)
    distMeasured = noise(distAbsolute)
    return posAbsolute, distMeasured

while True:
    posAbsolute, distMeasured = generate()
    blind = 0
    for i in range(distMeasured.shape[0]):
        for j in range(distMeasured.shape[1]):
            if distMeasured[i, j] >= 30:
                distMeasured[i, j] = np.nan
                blind += 1

    posCal = calibrationTriangleSize(distMeasured, 16)
    err = difference(posCal, posAbsolute)
    print(blind)
    print(err)
    if err[0] > 0.20:
        # fig = plt.figure()
        # ax = fig.add_subplot(1,1,1,projection='3d')
        # ax.scatter(posAbsolute[0,:], posAbsolute[1,:], posAbsolute[2,:], marker='.')
        # for i in range(posAbsolute.shape[1]):
        #     ax.text(posAbsolute[0,i], posAbsolute[1,i], posAbsolute[2, i], '%d'%(i))
        data = {'posAbsolute':posAbsolute, 'distMeasured':distMeasured, 'posCal':posCal, 'err':err}
        file_name = "Data/"+(time.ctime().replace(":", "_").replace(" ", "_"))+(".mat")
        savemat(file_name, data)
