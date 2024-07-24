import numpy as np

def pairwiseDist(positions):
    n = np.shape(positions)[1]
    distance = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            distance[i, j] = np.linalg.norm(positions[:,i]-positions[:,j], 2)
    return distance


def getBetter(new1, new2, newIndex, posCalibrated, distance, known):
    known[newIndex] = True

    def rmse_modified(input1, input2):
        assert input1.shape is input2.shape
        error = 0
        num_row, num_col = np.shape(input1)[0]
        for i in range(num_row):
            for j in range(num_row):
                if known(i) and known(j):
                    error += (input1[i, j] - input2[i, j]) ** 2
        
        return error
    
    pos1 = posCalibrated; pos1[:,newIndex] = new1
    pos2 = posCalibrated; pos2[:,newIndex] = new2

    e1 = rmse_modified()

