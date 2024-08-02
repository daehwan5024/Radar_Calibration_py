from util_t import *
from matplotlib import pyplot as plt
from scipy.io import savemat
import time


def plot(posAbs, posCal, distance, err, tags, plotDiff=False):
    fig = plt.figure()
    
    def plot_config(ax, position, distance, tags):
        ax.scatter(position[0,:], position[1,:], position[2,:], marker='.')
        for i in range(position.shape[1]):
            ax.text(position[0,i], position[1,i], position[2, i], '%d'%(i), fontsize=13.5)
        for i in range(distance.shape[0]):
            for j in range(distance.shape[1]):
                if np.isnan(distance[i,j]):
                    # ax.plot(position[0,[i, j]], position[1, [i, j]], position[2, [i, j]], "r-")
                    continue
                else:
                    if (i in tags[0]) or (i in tags[1]) or (j in tags[0]) or (j in tags[1]):
                        ax.plot(position[0,[i, j]], position[1, [i, j]], position[2, [i, j]], "b-")
                    else:
                        ax.plot(position[0,[i, j]], position[1, [i, j]], position[2, [i, j]], "g-")
        ax.plot([-10, 10, 10, -10, -10], [-10, -10, 10, 10, -10],[3.5, 3.5,3.5,3.5,3.5], color=[0,0,0])
        ax.plot([15, 35, 35, 15, 15], [-10, -10, 10, 10, -10],[3.5, 3.5, 3.5, 3.5, 3.5], color=[0,0,0])
    
    def plot_diff(ax, pos1, pos2, err):
        T1 = getTransform(pos1[:,err[1:4]])
        T2 = getTransform(pos2[:,err[1:4]])
        pos1_t = np.matmul( T1, np.vstack([pos1, np.ones((1,pos1.shape[1]))]) )[0:3,:]
        pos2_t = np.matmul( T2, np.vstack([pos2, np.ones((1,pos2.shape[1]))]) )[0:3,:]
        if err[4]:
            pos2_t = np.vstack([pos2_t[0:2,:], -1*pos2_t[2,:]])
        ax.scatter(pos1_t[0,:], pos1_t[1,:], pos1_t[2,:], marker='.', color='r')
        ax.scatter(pos2_t[0,:], pos2_t[1,:], pos2_t[2,:], marker='.', color='b')
        for i in range(pos1.shape[1]):
            ax.text(pos1_t[0,i], pos1_t[1,i], pos1_t[2,i], '%d'%(i), fontsize=13.5)

    if plotDiff:
        a1 = fig.add_subplot(1,2,1, projection='3d')
        a2 = fig.add_subplot(1,2,2, projection='3d')
        plot_config(a1, posAbs, distance, tags)
        plot_diff(a2, posAbs, posCal, err)
    else:
        a1 = fig.add_subplot(1,1,1, projection='3d')
        plot_config(a1, posAbs, distance, tags)
    
    plt.show()


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
    _, _, posAbsolute1, _, _ = radarData2(5, 3, 4)
    _, _, posAbsolute2, _, _ = radarData2(5, 3, 4)
    pairwiseDist(posAbsolute1)
    posAbsolute2[0,:] += 25
    posAbsolute = np.hstack([posAbsolute1, posAbsolute2])
    distAbsolute = pairwiseDist(posAbsolute)
    distMeasured = noise(distAbsolute)
    for i in range(distMeasured.shape[0]):
        for j in range(distMeasured.shape[1]):
            if distMeasured[i, j] >= 30:
                distMeasured[i, j] = np.nan

    tags = [[0,1,2],[8,9,10]]
    for i in tags[0]:
        for j in tags[1]:
            distMeasured[i, j] = np.nan
            distMeasured[j, i] = np.nan
    return posAbsolute, distMeasured, tags

if __name__ == '__main__':
    try:
        while True:
            posAbsolute, distMeasured, tags = generate()

            posCal = calibrationTriangleSize(distMeasured, 16)
            err = difference(posCal, posAbsolute)

            print(err)
            data = {'posAbsolute':posAbsolute, 'distMeasured':distMeasured, 'posCal':posCal, 'err':err}
            file_name = "Data/"+((time.ctime().replace(":", "_").replace(" ", "_"))+(".mat"))[4:]
            savemat(file_name, data)
            print()
    except KeyboardInterrupt:
        print()
        pass
