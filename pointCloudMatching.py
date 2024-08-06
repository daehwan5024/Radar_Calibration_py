import numpy as np
import math
from scipy.io import loadmat

def transform(input1:np.ndarray, input2:np.ndarray):
    n = input1.shape[1]
    assert(input1.shape == input2.shape)
    cm1 = np.average(input1, axis=1)
    cm2 = np.average(input2, axis=1)
    H = np.zeros((3,3))
    for i in range(input1.shape[1]):
        temp = np.matmul(np.reshape(input1[:,i]-cm1, (3,1)), np.reshape([input2[:,i] - cm2], (1, 3)))
        H += temp/n
    U, S, Vh = np.linalg.svd(H)
    R = np.matmul(Vh.T, U.T)
    translation = cm2 - np.matmul(R, cm1)

    return R, translation

data = loadmat("Data/Aug__5_11_57_26_2024.mat")
R, T = transform(data['posAbsolute'], data['posCal'])

pos_T = np.matmul(R, data['posAbsolute']) + np.reshape(T, (3,1))
print(math.sqrt(np.sum(np.square(pos_T - data['posCal'])))/16)
print(data['err'][0][0])