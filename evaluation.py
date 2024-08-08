import numpy as np
# returns R(rotation) and T(translation) matrix that best fits input1 to input2
# Uses point cloud registration to match two inputs
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

# average difference of each point
def difference(input1:np.ndarray, input2:np.ndarray):
    if np.any(np.isnan(input1)) or np.any(input1 == np.inf) or np.any(np.isnan(input2)) or np.any(input2 == np.inf):
        return np.inf
    R, T = getTransform(input1, input2)
    input1_t = np.matmul(R, input1) + np.reshape(T, (3, 1))
    diff = np.sqrt(np.sum(np.square(input1_t - input2), axis=0))
    return np.average(diff)
