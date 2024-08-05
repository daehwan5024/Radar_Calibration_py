from scipy.io import loadmat
import matplotlib.pyplot as plt
import math
import numpy as np

file = "add_noise5.mat"

data = loadmat(file)

noise_list = data['noise_list']
err_list = data['err_list'][0]

x_data = []
y_data = []

avg_list = np.max(noise_list, axis=1)

for i in range(len(err_list)):
    if err_list[i] == math.inf or avg_list[i] == math.inf:
        continue
    x_data.append(err_list[i])
    y_data.append(avg_list[i])

plt.plot(x_data, y_data, '.')
plt.show()
