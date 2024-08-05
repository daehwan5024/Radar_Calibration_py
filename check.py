from scipy.io import loadmat
import matplotlib.pyplot as plt
import math
import numpy as np

file = "add_noise1.mat"

data = loadmat(file)

noise_list = data['noise_list'][0]
err_list = data['err_list'][0]

for i in range(len(noise_list), 0):
    if noise_list[i] == math.inf or err_list[i] == math.inf:
        nonise_list = np.delete(noise_list, i)
        err_list = np.delete(err_list, i)

plt.plot(noise_list, err_list, '.')
plt.show()
