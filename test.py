import numpy as np

a = np.array([[1,2,1],[0,0,0],[1,1,1]])
b = np.zeros((3,3))

print(np.sum(np.square(a-b)))